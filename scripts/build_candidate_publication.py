#!/usr/bin/env python3
"""Build and verify a metadata-only candidate publication from immutable Git objects."""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "publications" / "m7_sol_candidate_v1.json"
SCHEMA = ROOT / "schemas" / "multi-model-candidate-publication.schema.json"


class PublicationError(RuntimeError):
    """Stable publication-contract failure."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationError("PUB-FILE", f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PublicationError("PUB-FILE", f"{path} must contain an object")
    return value


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _run_git(args: list[str], *, text: bool = False) -> bytes | str:
    process = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    if process.returncode != 0:
        stderr = process.stderr.strip() if text else process.stderr.decode("utf-8", errors="replace").strip()
        raise PublicationError("PUB-GIT", f"git {' '.join(args)} failed: {stderr}")
    return process.stdout


def validate_contract(contract: dict[str, Any]) -> None:
    schema = _load_json(SCHEMA)
    errors = sorted(Draft202012Validator(schema).iter_errors(contract), key=lambda item: list(item.path))
    if errors:
        location = "/".join(str(part) for part in errors[0].path) or "<root>"
        raise PublicationError("PUB-SCHEMA", f"{location}: {errors[0].message}")


def _verify_source(contract: dict[str, Any]) -> None:
    source = contract["source"]
    commit = str(_run_git(["rev-parse", f"{source['commit_sha']}^{{commit}}"], text=True)).strip()
    if commit != source["commit_sha"]:
        raise PublicationError("PUB-COMMIT", f"resolved {commit}, expected {source['commit_sha']}")
    tree = str(_run_git(["show", "-s", "--format=%T", commit], text=True)).strip()
    if tree != source["tree_sha"]:
        raise PublicationError("PUB-TREE", f"resolved {tree}, expected {source['tree_sha']}")


def _tree(commit: str) -> dict[str, dict[str, Any]]:
    raw = _run_git(["ls-tree", "-r", "-z", "--long", commit])
    assert isinstance(raw, bytes)
    rows: dict[str, dict[str, Any]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        header, path_bytes = record.split(b"\t", 1)
        mode, object_type, blob, size = header.decode("ascii").split()
        path = path_bytes.decode("utf-8")
        if object_type != "blob":
            continue
        rows[path] = {"mode": mode, "git_blob": blob, "bytes": int(size)}
    return rows


def _blob(commit: str, path: str) -> bytes:
    data = _run_git(["show", f"{commit}:{path}"])
    assert isinstance(data, bytes)
    return data


def _blobs_batch(commit: str, paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    result: dict[str, bytes] = {}
    try:
        for path in paths:
            process.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline().decode("utf-8", errors="replace").strip()
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise PublicationError("PUB-GIT-BATCH", f"unexpected header for {path}: {header}")
            size = int(parts[2])
            data = process.stdout.read(size)
            separator = process.stdout.read(1)
            if len(data) != size or separator != b"\n":
                raise PublicationError("PUB-GIT-BATCH", f"truncated blob response for {path}")
            result[path] = data
    finally:
        process.stdin.close()
        return_code = process.wait()
    if return_code != 0:
        assert process.stderr is not None
        raise PublicationError("PUB-GIT-BATCH", process.stderr.read().decode("utf-8", errors="replace"))
    return result


def _parse_canonical_books(data: bytes, path: str) -> list[str]:
    try:
        value = yaml.safe_load(data.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise PublicationError("PUB-BOOKS", f"cannot parse {path}: {exc}") from exc
    books = value.get("canonical_66_books") if isinstance(value, dict) else None
    if not isinstance(books, list) or len(books) != 66 or len(set(books)) != 66:
        raise PublicationError("PUB-BOOKS", f"{path} is not an exact 66-book allowlist")
    return [str(book) for book in books]


def _canonical_books(commit: str, path: str) -> list[str]:
    return _parse_canonical_books(_blob(commit, path), path)


def _require_exact_canonical_book_set(observed: set[str], expected: list[str]) -> None:
    expected_set = set(expected)
    if observed == expected_set:
        return
    missing = sorted(expected_set - observed)
    extra = sorted(observed - expected_set)
    raise PublicationError(
        "PUB-MAP-CANONICAL-BOOKS",
        f"candidate map book IDs differ from the pinned canonical allowlist; missing={missing}, extra={extra}",
    )


def _compile_patterns(patterns: list[str], code: str) -> list[re.Pattern[str]]:
    compiled: list[re.Pattern[str]] = []
    for pattern in patterns:
        try:
            compiled.append(re.compile(pattern))
        except re.error as exc:
            raise PublicationError(code, f"invalid pattern {pattern!r}: {exc}") from exc
    return compiled


def select_inventory(contract: dict[str, Any], tree: dict[str, dict[str, Any]]) -> tuple[list[str], dict[str, int]]:
    selection = contract["selection"]
    commit = contract["source"]["commit_sha"]
    selected = set(str(path) for path in selection["exact_paths"])
    missing = sorted(path for path in selected if path not in tree)
    if missing:
        raise PublicationError("PUB-MISSING", f"exact source paths are absent: {missing[:5]}")

    strategy = selection["canonical_book_strategies"]
    books = _canonical_books(commit, strategy["book_list_path"])
    selected.add(strategy["book_list_path"])
    strategy_paths = [strategy["path_template"].format(book=book) for book in books]
    missing_strategies = [path for path in strategy_paths if path not in tree]
    if missing_strategies or len(strategy_paths) != strategy["expected_count"]:
        raise PublicationError("PUB-STRATEGIES", f"missing or miscounted strategies: {missing_strategies[:5]}")
    selected.update(strategy_paths)

    group_counts: dict[str, int] = {"canonical-book-strategies": len(strategy_paths)}
    for group in selection["tree_groups"]:
        try:
            basename = re.compile(group["basename_regex"])
        except re.error as exc:
            raise PublicationError("PUB-GROUP-REGEX", f"{group['group_id']}: {exc}") from exc
        matches = sorted(
            path
            for path in tree
            if path.startswith(group["prefix"]) and basename.search(PurePosixPath(path).name)
        )
        if len(matches) != group["expected_count"]:
            raise PublicationError(
                "PUB-GROUP-COUNT",
                f"{group['group_id']} resolved {len(matches)}, expected {group['expected_count']}",
            )
        selected.update(matches)
        group_counts[group["group_id"]] = len(matches)

    forbidden = _compile_patterns(selection["forbidden_path_patterns"], "PUB-PATH-REGEX")
    violations = sorted(path for path in selected if any(pattern.search(path) for pattern in forbidden))
    if violations:
        raise PublicationError("PUB-FORBIDDEN-PATH", f"selected paths violate the boundary: {violations[:5]}")
    return sorted(selected), group_counts


def _classify(path: str) -> str:
    if "/book_strategy/" in path:
        return "book_strategy_record"
    if "/receipts/" in path:
        return "validation_or_completion_receipt"
    name = PurePosixPath(path).name.lower()
    if "/reviews/" in path and any(token in name for token in ("appeal", "dissent", "hold", "failure")):
        return "appeal_hold_dissent_or_failure_evidence"
    if "/reviews/job/" in path.lower():
        return "job_worked_example_pointer"
    if "t544" in path.lower() or "/reviews/ps/" in path.lower():
        return "psalm_failure_and_repair_pointer"
    if "/state/evidence/final/" in path:
        return "final_candidate_evidence_pointer"
    if "role_profiles" in path or "routing_policy" in path or path.endswith("review_contract.yaml"):
        return "role_or_routing_contract"
    return "governance_or_provenance_pointer"


def _validate_coverage(contract: dict[str, Any], entries: dict[str, bytes]) -> dict[str, Any]:
    coverage = contract["coverage"]
    map_path = coverage["candidate_map"]["evidence_path"]
    map_bytes = entries[map_path]
    digest = f"sha256:{_sha256(map_bytes)}"
    if digest != coverage["candidate_map"]["sha256"]:
        raise PublicationError("PUB-MAP-HASH", f"{digest} does not match the contract")
    books: set[str] = set()
    rows = 0
    for line_no, raw in enumerate(map_bytes.decode("utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise PublicationError("PUB-MAP-JSONL", f"line {line_no}: {exc}") from exc
        rows += 1
        books.add(str(row.get("book")))
        if row.get("candidate_only") is not True or row.get("non_authorizing") is not True:
            raise PublicationError("PUB-MAP-AUTHORITY", f"line {line_no} lacks candidate/non-authorizing guards")
    expected_map = coverage["candidate_map"]
    if rows != expected_map["chunk_count"] or len(books) != expected_map["book_count"]:
        raise PublicationError("PUB-MAP-COVERAGE", f"observed {len(books)} books/{rows} rows")
    canonical_path = contract["selection"]["canonical_book_strategies"]["book_list_path"]
    canonical_books = _parse_canonical_books(entries[canonical_path], canonical_path)
    _require_exact_canonical_book_set(books, canonical_books)

    manifest = yaml.safe_load(entries[coverage["corrective_review"]["evidence_path"]].decode("utf-8"))
    if manifest.get("books_completed") != coverage["corrective_review"]["completed"]:
        raise PublicationError("PUB-CORRECTIVE-COUNT", "corrective completion count drifted")
    progress = yaml.safe_load(
        entries[".ai/scratch/multi_model_bible_chunking/M7_sol/marathon_progress.yaml"].decode("utf-8")
    )
    if progress.get("books_completed") != coverage["book_strategy"]["observed"]:
        raise PublicationError("PUB-FIRST-PASS-COUNT", "first-pass progress count drifted")
    return {
        "book_strategy_records": coverage["book_strategy"]["observed"],
        "candidate_map_books": len(books),
        "candidate_map_rows": rows,
        "corrective_review_completed": manifest.get("books_completed"),
        "corrective_review_canonical_total": coverage["corrective_review"]["canonical_total"],
        "corrective_review_campaign_target": coverage["corrective_review"]["campaign_target"],
        "replay_qualified": contract["status"]["replay_qualified"],
        "release_qualified": contract["status"]["release_qualified"],
    }


def build_manifest(contract: dict[str, Any]) -> dict[str, Any]:
    validate_contract(contract)
    _verify_source(contract)
    tree = _tree(contract["source"]["commit_sha"])
    selected, group_counts = select_inventory(contract, tree)
    blobs = _blobs_batch(contract["source"]["commit_sha"], selected)
    coverage = _validate_coverage(contract, blobs)
    inventory = [
        {
            "path": path,
            "git_blob": tree[path]["git_blob"],
            "sha256": f"sha256:{_sha256(blobs[path])}",
            "bytes": len(blobs[path]),
            "classification": _classify(path),
            "payload_embedded": False,
        }
        for path in selected
    ]
    manifest: dict[str, Any] = {
        "schema_version": "candidate_publication_artifact_manifest.v1",
        "publication_id": contract["publication_id"],
        "publication_revision": contract["publication_revision"],
        "source": copy.deepcopy(contract["source"]),
        "status": copy.deepcopy(contract["status"]),
        "authority": copy.deepcopy(contract["authority"]),
        "coverage": coverage,
        "independence": copy.deepcopy(contract["independence"]),
        "licensing": copy.deepcopy(contract["licensing"]),
        "selection_summary": {
            "default_deny": True,
            "selected_pointer_count": len(inventory),
            "selected_pointer_bytes_at_source": sum(item["bytes"] for item in inventory),
            "group_counts_before_deduplication": group_counts,
            "payload_bytes_embedded": 0,
        },
        "inventory": inventory,
        "known_limitations": copy.deepcopy(contract["known_limitations"]),
        "convergence_gate": copy.deepcopy(contract["convergence_gate"]),
        "excluded_surfaces": [
            {"surface": "M8_fable", "reason": "protected active owner lane; no read, copy, comparison, or mutation"},
            {"surface": "_pass1_archive", "reason": "historical duplicate tree"},
            {"surface": "runtime and temporary state", "reason": "local paths, recovery state, and non-public execution debris"},
            {"surface": "raw or copied source corpora", "reason": "file-level redistribution authority is not established"},
            {"surface": "M7 evidence payload bytes", "reason": "metadata-and-hashes-only publication pending provenance approval"},
        ],
        "manifest_digest": "",
    }
    digest_input = copy.deepcopy(manifest)
    digest_input.pop("manifest_digest")
    manifest["manifest_digest"] = f"sha256:{_sha256(_canonical_json(digest_input))}"
    serialized = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    forbidden = _compile_patterns(contract["selection"]["forbidden_content_patterns"], "PUB-CONTENT-REGEX")
    hits = [pattern.pattern for pattern in forbidden if pattern.search(serialized)]
    if hits:
        raise PublicationError("PUB-PUBLIC-CONTENT", f"generated manifest matched forbidden patterns: {hits}")
    return manifest


def validate_manifest_envelope(contract: dict[str, Any], manifest: dict[str, Any]) -> None:
    validate_contract(contract)
    if manifest.get("schema_version") != "candidate_publication_artifact_manifest.v1":
        raise PublicationError("PUB-MANIFEST-SCHEMA", "unexpected artifact manifest schema")
    if manifest.get("publication_id") != contract["publication_id"]:
        raise PublicationError("PUB-MANIFEST-ID", "publication identity mismatch")
    digest_input = copy.deepcopy(manifest)
    recorded_digest = digest_input.pop("manifest_digest", None)
    expected_digest = f"sha256:{_sha256(_canonical_json(digest_input))}"
    if recorded_digest != expected_digest:
        raise PublicationError("PUB-MANIFEST-DIGEST", f"recorded {recorded_digest}, expected {expected_digest}")

    contract_bound_fields = (
        "publication_revision",
        "source",
        "status",
        "authority",
        "independence",
        "licensing",
        "known_limitations",
        "convergence_gate",
    )
    drifted = [field for field in contract_bound_fields if manifest.get(field) != contract.get(field)]
    if drifted:
        raise PublicationError("PUB-MANIFEST-CONTRACT", f"contract-bound fields drifted: {drifted}")
    expected_coverage = {
        "book_strategy_records": contract["coverage"]["book_strategy"]["observed"],
        "candidate_map_books": contract["coverage"]["candidate_map"]["book_count"],
        "candidate_map_rows": contract["coverage"]["candidate_map"]["chunk_count"],
        "corrective_review_completed": contract["coverage"]["corrective_review"]["completed"],
        "corrective_review_canonical_total": contract["coverage"]["corrective_review"]["canonical_total"],
        "corrective_review_campaign_target": contract["coverage"]["corrective_review"]["campaign_target"],
        "replay_qualified": contract["status"]["replay_qualified"],
        "release_qualified": contract["status"]["release_qualified"],
    }
    if manifest.get("coverage") != expected_coverage:
        raise PublicationError("PUB-MANIFEST-COVERAGE", "manifest coverage differs from the publication contract")

    inventory = manifest.get("inventory")
    if not isinstance(inventory, list) or not inventory:
        raise PublicationError("PUB-MANIFEST-INVENTORY", "inventory must be nonempty")
    item_keys = {"path", "git_blob", "sha256", "bytes", "classification", "payload_embedded"}
    paths: list[str] = []
    for index, item in enumerate(inventory):
        if not isinstance(item, dict) or set(item) != item_keys:
            raise PublicationError("PUB-MANIFEST-ITEM", f"inventory item {index} has an invalid envelope")
        path = item.get("path")
        git_blob = item.get("git_blob")
        sha256 = item.get("sha256")
        size = item.get("bytes")
        classification = item.get("classification")
        if not isinstance(path, str) or not path:
            raise PublicationError("PUB-MANIFEST-ITEM", f"inventory item {index} has an invalid path")
        if not isinstance(git_blob, str) or not re.fullmatch(r"[0-9a-f]{40}", git_blob):
            raise PublicationError("PUB-MANIFEST-ITEM", f"inventory item {index} has an invalid Git blob ID")
        if not isinstance(sha256, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", sha256):
            raise PublicationError("PUB-MANIFEST-ITEM", f"inventory item {index} has an invalid SHA-256")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise PublicationError("PUB-MANIFEST-ITEM", f"inventory item {index} has an invalid byte count")
        if not isinstance(classification, str) or not classification or classification != _classify(path):
            raise PublicationError("PUB-MANIFEST-ITEM", f"inventory item {index} has an invalid classification")
        if item.get("payload_embedded") is not False:
            raise PublicationError("PUB-MANIFEST-PAYLOAD", f"inventory item {index} embeds payload")
        paths.append(path)
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise PublicationError("PUB-MANIFEST-INVENTORY", "inventory paths must be unique and sorted")
    forbidden_paths = _compile_patterns(contract["selection"]["forbidden_path_patterns"], "PUB-PATH-REGEX")
    violations = sorted(path for path in paths if any(pattern.search(path) for pattern in forbidden_paths))
    if violations:
        raise PublicationError("PUB-MANIFEST-PATH", f"forbidden inventory paths: {violations[:5]}")

    selection = contract["selection"]
    required_paths = set(str(path) for path in selection["exact_paths"])
    strategy = selection["canonical_book_strategies"]
    canonical_path = strategy["book_list_path"]
    try:
        canonical_data = (ROOT / canonical_path).read_bytes()
    except OSError as exc:
        raise PublicationError("PUB-BOOKS", f"cannot read {canonical_path}: {exc}") from exc
    canonical_books = _parse_canonical_books(canonical_data, canonical_path)
    required_paths.add(canonical_path)
    required_paths.update(strategy["path_template"].format(book=book) for book in canonical_books)
    path_set = set(paths)
    missing_required = sorted(required_paths - path_set)
    group_paths: set[str] = set()
    observed_group_counts: dict[str, int] = {"canonical-book-strategies": len(canonical_books)}
    for group in selection["tree_groups"]:
        try:
            basename = re.compile(group["basename_regex"])
        except re.error as exc:
            raise PublicationError("PUB-GROUP-REGEX", f"{group['group_id']}: {exc}") from exc
        matches = {
            path
            for path in path_set
            if path.startswith(group["prefix"]) and basename.search(PurePosixPath(path).name)
        }
        if len(matches) != group["expected_count"]:
            raise PublicationError(
                "PUB-MANIFEST-GROUP-COUNT",
                f"{group['group_id']} resolved {len(matches)}, expected {group['expected_count']}",
            )
        group_paths.update(matches)
        observed_group_counts[group["group_id"]] = len(matches)
    unexpected = sorted(path_set - required_paths - group_paths)
    if missing_required or unexpected:
        raise PublicationError(
            "PUB-MANIFEST-MEMBERSHIP",
            f"inventory membership drifted; missing={missing_required[:5]}, unexpected={unexpected[:5]}",
        )

    summary = manifest.get("selection_summary", {})
    expected_summary = {
        "default_deny": True,
        "selected_pointer_count": len(inventory),
        "selected_pointer_bytes_at_source": sum(item["bytes"] for item in inventory),
        "group_counts_before_deduplication": observed_group_counts,
        "payload_bytes_embedded": 0,
    }
    if summary != expected_summary:
        raise PublicationError("PUB-MANIFEST-SUMMARY", "selection summary does not match inventory")
    serialized = json.dumps(manifest, ensure_ascii=False, sort_keys=True)
    forbidden_content = _compile_patterns(contract["selection"]["forbidden_content_patterns"], "PUB-CONTENT-REGEX")
    hits = [pattern.pattern for pattern in forbidden_content if pattern.search(serialized)]
    if hits:
        raise PublicationError("PUB-MANIFEST-CONTENT", f"forbidden public content patterns: {hits}")


def render_readme(contract: dict[str, Any], manifest: dict[str, Any]) -> str:
    coverage = manifest["coverage"]
    return f"""# M7 Sol candidate evidence snapshot

This archive is a metadata-only, content-addressed index of immutable M7 candidate
evidence from `{contract['source']['commit_sha']}`. It contains hashes, sizes,
classifications, progress measures, limitations, and source pointers. It deliberately
contains **none of the selected M7 payload bytes**.

- Book-strategy coverage: {coverage['book_strategy_records']}/66
- Candidate-map coverage: {coverage['candidate_map_books']}/66 books,
  {coverage['candidate_map_rows']} candidate rows
- Corrective rereview recorded at the source commit: {coverage['corrective_review_completed']}/66
- Replay qualified: false
- Release qualified: false
- Independent convergence proven: false

The Sol role mesh is one correlated model voice. Appeals, holds, dissent, historical
failures, Job worked-example evidence, and Psalm repair history are indexed rather than
hidden. M8 is absent and protected. Comparison may begin only after a separately
hash-bound M8 publication exists and Lowell authorizes the comparison.

The inventory does not expand repository or source-dataset rights. Underlying payload
publication remains held pending file-level provenance and license approval.
"""


def _tar_member(name: str, data: bytes) -> tuple[tarfile.TarInfo, bytes]:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    return info, data


def package_metadata(contract: dict[str, Any], manifest: dict[str, Any], output_dir: Path) -> tuple[Path, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root_name = contract["artifact"]["root_name"]
    members = [
        _tar_member(
            f"{root_name}/{contract['artifact']['internal_manifest_path']}",
            (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"),
        ),
        _tar_member(f"{root_name}/PUBLICATION_CONTRACT.json", _canonical_json(contract) + b"\n"),
        _tar_member(f"{root_name}/README.md", render_readme(contract, manifest).encode("utf-8")),
    ]
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for info, data in sorted(members, key=lambda item: item[0].name):
                archive.addfile(info, io.BytesIO(data))
    payload = buffer.getvalue()
    digest = _sha256(payload)
    name = f"{contract['artifact']['output_basename']}-{digest}.tar.gz"
    path = output_dir / name
    path.write_bytes(payload)
    (output_dir / f"{name}.sha256").write_text(f"{digest}  {name}\n", encoding="ascii", newline="\n")
    return path, digest


def _compare_manifest(expected: dict[str, Any], path: Path) -> None:
    actual = _load_json(path)
    if actual != expected:
        raise PublicationError("PUB-MANIFEST-STALE", f"{path} does not match immutable source reconstruction")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--check-manifest", type=Path)
    parser.add_argument("--package", type=Path, metavar="OUTPUT_DIR")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        contract = _load_json(args.config)
        manifest = build_manifest(contract)
        if args.write_manifest:
            args.write_manifest.parent.mkdir(parents=True, exist_ok=True)
            args.write_manifest.write_text(
                json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        if args.check_manifest:
            _compare_manifest(manifest, args.check_manifest)
        artifact_path = None
        artifact_sha = None
        if args.package:
            artifact_path, artifact_sha = package_metadata(contract, manifest, args.package)
        result = {
            "status": "pass",
            "publication_id": contract["publication_id"],
            "manifest_digest": manifest["manifest_digest"],
            "selected_pointer_count": manifest["selection_summary"]["selected_pointer_count"],
            "payload_bytes_embedded": 0,
            "artifact_path": str(artifact_path) if artifact_path else None,
            "artifact_sha256": f"sha256:{artifact_sha}" if artifact_sha else None,
        }
        if args.json:
            print(json.dumps(result, sort_keys=True))
        else:
            print(
                "Candidate publication validation passed: "
                f"{result['selected_pointer_count']} immutable pointers, "
                f"manifest {result['manifest_digest']}, payload bytes embedded 0."
            )
        return 0
    except PublicationError as exc:
        print(f"Candidate publication failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
