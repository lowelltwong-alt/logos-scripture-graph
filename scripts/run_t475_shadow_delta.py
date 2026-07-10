#!/usr/bin/env python3
"""Run pinned pre/post-T474 importer shadows and emit exact no-text delta evidence."""
from __future__ import annotations

import argparse
import gzip
from collections import Counter, defaultdict
import hashlib
import json
import os
import platform
import shutil
import sqlite3
import statistics
import subprocess
import sys
import stat
import zipfile
import time
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL_PATH = ROOT / ".ai" / "control" / "t475_usfm_shadow_delta_gate.yaml"
SAFE_VISIBLE_FIELDS = {
    "id",
    "osis_ref",
    "anchor_osis_ref",
    "prior_osis_ref",
    "next_osis_ref",
    "source_file",
    "source_line",
    "marker",
    "anchor_kind",
    "body_disposition",
    "anchor_resolved",
}
SENSITIVE_PREFIXES = ("Ps.119.", "Ps.78.", "Song.", "Gen.1.")
CHUNK_INPUT_SURFACES = {
    "canonical/translations/eng-web/translation_witnesses.jsonl",
    "canonical/translations/eng-web/word_tokens.jsonl",
    "canonical/translations/eng-web/boundary_claims.jsonl",
    "canonical/translations/eng-web/section_headings.jsonl",
}


class ShadowDeltaError(ValueError):
    """Raised when a shadow run or comparison cannot fail closed."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest_value(value: Any) -> str:
    return digest_bytes(canonical_json(value).encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_control(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    data = yaml.safe_load(parts[2] if len(parts) == 3 else text)
    if not isinstance(data, dict):
        raise ShadowDeltaError("T475 control must be a YAML mapping")
    return data


def resolve_under(root: Path, path: Path) -> Path:
    root = root.resolve()
    path = path.resolve()
    if path != root and root not in path.parents:
        raise ShadowDeltaError(f"path escapes {root}: {path}")
    return path


def _remove_readonly(func, path, _exc_info) -> None:
    os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
    func(path)


def clean_dir(work_root: Path, path: Path) -> None:
    target = resolve_under(work_root, path)
    if target.exists():
        shutil.rmtree(target, onerror=_remove_readonly)
    target.mkdir(parents=True, exist_ok=True)


def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def git_blob(root: Path, ref: str, rel: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{rel}"], cwd=root)


def extract_source_snapshot(root: Path, work_root: Path, ref: str, destination: Path) -> None:
    clean_dir(work_root, destination)
    zip_path = resolve_under(work_root, work_root / f"{destination.name}.zip")
    if zip_path.exists():
        zip_path.unlink()
    subprocess.run(
        ["git", "archive", "--format=zip", f"--output={zip_path}", ref, "pipelines", "config/canon"],
        cwd=root,
        check=True,
    )
    destination_resolved = destination.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            member_path = (destination / member.filename).resolve()
            if member_path != destination_resolved and destination_resolved not in member_path.parents:
                raise ShadowDeltaError(f"unsafe Git archive member: {member.filename}")
            if member.is_dir():
                member_path.mkdir(parents=True, exist_ok=True)
                continue
            member_path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, member_path.open("wb") as target:
                shutil.copyfileobj(source, target)
    zip_path.unlink()


def source_hashes(root: Path, ref: str, paths: Iterable[str]) -> dict[str, str]:
    return {path: digest_bytes(git_blob(root, ref, path)) for path in paths}


def stable_key(record: dict[str, Any], surface: str) -> str:
    record_id = record.get("id")
    if isinstance(record_id, str) and record_id:
        return record_id
    values = [record.get(name) for name in ("osis_ref", "source_file", "source_line", "marker")]
    if any(value not in (None, "") for value in values):
        return canonical_json(values)
    raise ShadowDeltaError(f"{surface}: row lacks stable id or provenance key")


def safe_metadata(record: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in sorted(SAFE_VISIBLE_FIELDS):
        value = record.get(key)
        if isinstance(value, (str, int, float, bool)) or value is None:
            if key in record:
                result[key] = value
    return result


def changed_paths(before: Any, after: Any, prefix: str = "") -> list[str]:
    if isinstance(before, dict) and isinstance(after, dict):
        paths: list[str] = []
        for key in sorted(set(before) | set(after)):
            path = f"{prefix}.{key}" if prefix else str(key)
            if key not in before or key not in after:
                paths.append(path)
            else:
                paths.extend(changed_paths(before[key], after[key], path))
        return paths
    if isinstance(before, list) and isinstance(after, list):
        if before == after:
            return []
        return [prefix or "$"]
    return [] if before == after else [prefix or "$"]


def value_at_path(record: Any, path: str) -> Any:
    current = record
    if path == "$":
        return current
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def field_change_rows(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in changed_paths(before, after):
        old = value_at_path(before, path)
        new = value_at_path(after, path)
        item: dict[str, Any] = {
            "path": path,
            "before_sha256": digest_value(old),
            "after_sha256": digest_value(new),
        }
        leaf = path.rsplit(".", 1)[-1]
        if leaf in SAFE_VISIBLE_FIELDS:
            if isinstance(old, (str, int, float, bool)) or old is None:
                item["before"] = old
            if isinstance(new, (str, int, float, bool)) or new is None:
                item["after"] = new
        rows.append(item)
    return rows


def jsonl_stats(path: Path, surface: str) -> tuple[int, str]:
    count = 0
    digest = hashlib.sha256()
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ShadowDeltaError(f"{surface}:{line_no}: malformed JSON") from exc
            if not isinstance(record, dict):
                raise ShadowDeltaError(f"{surface}:{line_no}: expected object")
            key = stable_key(record, surface)
            if key in seen:
                raise ShadowDeltaError(f"{surface}:{line_no}: duplicate stable key {key}")
            seen.add(key)
            row_hash = digest_value(record)
            digest.update(key.encode("utf-8"))
            digest.update(b"\0")
            digest.update(row_hash.encode("ascii"))
            digest.update(b"\n")
            count += 1
    return count, digest.hexdigest()


def output_manifest(side_root: Path, ref: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for file_path in sorted(path for path in side_root.rglob("*") if path.is_file()):
        rel = file_path.relative_to(side_root).as_posix()
        item: dict[str, Any] = {
            "path": rel,
            "bytes": file_path.stat().st_size,
            "sha256": sha256_file(file_path),
            "row_count": None,
            "stable_key_digest": None,
        }
        if file_path.suffix == ".jsonl":
            item["row_count"], item["stable_key_digest"] = jsonl_stats(file_path, rel)
        rows.append(item)
    aggregate = digest_value(rows)
    return {"ref": ref, "aggregate_sha256": aggregate, "files": rows}


def run_import(
    *,
    source_root: Path,
    archive: Path,
    manifest: Path,
    side_root: Path,
    work_root: Path,
) -> tuple[float, list[str]]:
    canonical = side_root / "canonical"
    processed = side_root / "processed"
    clean_dir(work_root, side_root)
    command = [
        sys.executable,
        str(source_root / "pipelines" / "ingest" / "usfm_importer.py"),
        "--archive",
        str(archive),
        "--manifest",
        str(manifest),
        "--canonical-root",
        str(canonical),
        "--processed-root",
        str(processed),
        "--canonical-66-filter",
    ]
    started = time.perf_counter()
    result = subprocess.run(command, cwd=source_root, capture_output=True, text=True)
    elapsed = time.perf_counter() - started
    if result.returncode != 0:
        raise ShadowDeltaError(
            f"import failed ({result.returncode}): {result.stdout[-1000:]} {result.stderr[-1000:]}"
        )
    return elapsed, command


def manifest_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["path"]): row for row in manifest["files"]}


def compare_jsonl(
    *,
    baseline: Path,
    candidate: Path,
    surface: str,
    db_path: Path,
    ledger,
    sensitive: dict[str, Counter[str]],
    affected_refs: set[str],
) -> dict[str, int]:
    # Keep only stable keys, row hashes, and byte offsets in memory. Full rows stay
    # in the source files and are sought only for actual mismatches.
    del db_path
    counts = Counter({"added": 0, "removed": 0, "modified": 0, "unchanged": 0})
    baseline_index: dict[str, tuple[str, int]] = {}
    with baseline.open("rb") as handle:
        while True:
            offset = handle.tell()
            raw = handle.readline()
            if not raw:
                break
            if not raw.strip():
                continue
            before = json.loads(raw.decode("utf-8"))
            key = stable_key(before, surface)
            if key in baseline_index:
                raise ShadowDeltaError(f"{surface}: duplicate baseline key {key}")
            baseline_index[key] = (digest_value(before), offset)

    candidate_seen: set[str] = set()
    with baseline.open("rb") as baseline_handle, candidate.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            after = json.loads(line)
            key = stable_key(after, surface)
            if key in candidate_seen:
                raise ShadowDeltaError(f"{surface}:{line_no}: duplicate candidate key {key}")
            candidate_seen.add(key)
            found = baseline_index.pop(key, None)
            after_hash = digest_value(after)
            if found is None:
                counts["added"] += 1
                row = {
                    "surface": surface,
                    "class": "added",
                    "stable_key": key,
                    "before_sha256": None,
                    "after_sha256": after_hash,
                    "safe_metadata": safe_metadata(after),
                    "field_changes": [],
                }
            else:
                before_hash, offset = found
                if before_hash == after_hash:
                    counts["unchanged"] += 1
                    continue
                baseline_handle.seek(offset)
                before = json.loads(baseline_handle.readline().decode("utf-8"))
                counts["modified"] += 1
                row = {
                    "surface": surface,
                    "class": "modified",
                    "stable_key": key,
                    "before_sha256": before_hash,
                    "after_sha256": after_hash,
                    "safe_metadata": {**safe_metadata(before), **safe_metadata(after)},
                    "field_changes": field_change_rows(before, after),
                }
                before_anchor = str(before.get("anchor_kind", "<missing>"))
                after_anchor = str(after.get("anchor_kind", "<missing>"))
                marker = str(after.get("marker", before.get("marker", "<missing>")))
                sensitive["anchor_transitions"][f"{marker}:{before_anchor}->{after_anchor}"] += 1
            ledger.write(canonical_json(row) + "\n")
            ref = row["safe_metadata"].get("osis_ref") or row["safe_metadata"].get("anchor_osis_ref")
            if isinstance(ref, str):
                if surface in CHUNK_INPUT_SURFACES:
                    affected_refs.add(ref)
                for prefix in SENSITIVE_PREFIXES:
                    if ref.startswith(prefix):
                        sensitive[prefix][row["class"]] += 1

        for key, (before_hash, offset) in sorted(baseline_index.items(), key=lambda item: item[1][1]):
            baseline_handle.seek(offset)
            before = json.loads(baseline_handle.readline().decode("utf-8"))
            counts["removed"] += 1
            row = {
                "surface": surface,
                "class": "removed",
                "stable_key": key,
                "before_sha256": before_hash,
                "after_sha256": None,
                "safe_metadata": safe_metadata(before),
                "field_changes": [],
            }
            ledger.write(canonical_json(row) + "\n")
            ref = row["safe_metadata"].get("osis_ref") or row["safe_metadata"].get("anchor_osis_ref")
            if isinstance(ref, str):
                if surface in CHUNK_INPUT_SURFACES:
                    affected_refs.add(ref)
                for prefix in SENSITIVE_PREFIXES:
                    if ref.startswith(prefix):
                        sensitive[prefix]["removed"] += 1
    return dict(counts)


def compare_outputs(
    *,
    baseline_root: Path,
    candidate_root: Path,
    baseline_manifest: dict[str, Any],
    candidate_manifest: dict[str, Any],
    report_root: Path,
    work_root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    baseline_index = manifest_index(baseline_manifest)
    candidate_index = manifest_index(candidate_manifest)
    summary: dict[str, Any] = {"files": {}, "totals": Counter()}
    sensitive: dict[str, Counter[str]] = defaultdict(Counter)
    affected_refs: set[str] = set()
    ledger_path = report_root / "mismatch_ledger.jsonl"
    db_path = work_root / "delta_index.sqlite"
    with ledger_path.open("w", encoding="utf-8", newline="\n") as ledger:
        for surface in sorted(set(baseline_index) | set(candidate_index)):
            before_meta = baseline_index.get(surface)
            after_meta = candidate_index.get(surface)
            if before_meta is None or after_meta is None:
                cls = "added_file" if before_meta is None else "removed_file"
                row = {
                    "surface": surface,
                    "class": cls,
                    "stable_key": None,
                    "before_sha256": before_meta and before_meta["sha256"],
                    "after_sha256": after_meta and after_meta["sha256"],
                    "safe_metadata": {},
                    "field_changes": [],
                }
                ledger.write(canonical_json(row) + "\n")
                summary["files"][surface] = {cls: 1}
                summary["totals"][cls] += 1
                continue
            if before_meta["sha256"] == after_meta["sha256"]:
                count = before_meta["row_count"]
                summary["files"][surface] = {
                    "added": 0,
                    "removed": 0,
                    "modified": 0,
                    "unchanged": count if count is not None else 1,
                }
                summary["totals"]["unchanged"] += count if count is not None else 1
                continue
            before_path = baseline_root / surface
            after_path = candidate_root / surface
            if before_path.suffix == ".jsonl" and after_path.suffix == ".jsonl":
                counts = compare_jsonl(
                    baseline=before_path,
                    candidate=after_path,
                    surface=surface,
                    db_path=db_path,
                    ledger=ledger,
                    sensitive=sensitive,
                    affected_refs=affected_refs,
                )
                summary["files"][surface] = counts
                summary["totals"].update(counts)
            else:
                row = {
                    "surface": surface,
                    "class": "modified_file",
                    "stable_key": None,
                    "before_sha256": before_meta["sha256"],
                    "after_sha256": after_meta["sha256"],
                    "safe_metadata": {},
                    "field_changes": [],
                }
                ledger.write(canonical_json(row) + "\n")
                summary["files"][surface] = {"modified_file": 1}
                summary["totals"]["modified_file"] += 1
    summary["totals"] = dict(summary["totals"])
    sensitive_summary = {
        "scopes": {key: dict(value) for key, value in sorted(sensitive.items()) if key != "anchor_transitions"},
        "anchor_transition_matrix": dict(sorted(sensitive["anchor_transitions"].items())),
        "contains_visible_scripture_text": False,
    }
    chunk_impact = {
        "chunker_executed": False,
        "chunk_output_emitted": False,
        "affected_osis_ref_count": len(affected_refs),
        "affected_osis_refs": sorted(affected_refs),
        "interpretation_authorized": False,
    }
    return summary, sensitive_summary, chunk_impact


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def finalize_ledger(report_root: Path) -> Path:
    source = report_root / "mismatch_ledger.jsonl"
    target = report_root / "mismatch_ledger.jsonl.gz"
    if not source.is_file():
        if target.is_file():
            return target
        raise ShadowDeltaError("mismatch ledger is missing")
    with source.open("rb") as src, target.open("wb") as raw_target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_target, mtime=0, compresslevel=9) as compressed:
            shutil.copyfileobj(src, compressed, length=1024 * 1024)
    for attempt in range(20):
        try:
            source.unlink()
            break
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(0.25)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control", type=Path, default=CONTROL_PATH)
    parser.add_argument("--work-root", type=Path, default=ROOT / "build" / "T475")
    parser.add_argument("--report-root", type=Path, default=ROOT / ".ai" / "context" / "agent_work" / "T475")
    parser.add_argument("--trials", type=int, default=None)
    parser.add_argument(
        "--compare-existing",
        action="store_true",
        help="Reuse completed shadow roots/manifests and run only the bounded comparison.",
    )
    args = parser.parse_args(argv)

    control_path = args.control if args.control.is_absolute() else ROOT / args.control
    control = load_control(control_path)
    work_root = args.work_root if args.work_root.is_absolute() else ROOT / args.work_root
    report_root = args.report_root if args.report_root.is_absolute() else ROOT / args.report_root
    work_root = work_root.resolve()
    report_root = report_root.resolve()
    expected_work = (ROOT / "build" / "T475").resolve()
    if work_root != expected_work:
        raise ShadowDeltaError(f"work root must be exactly {expected_work}")
    work_root.mkdir(parents=True, exist_ok=True)
    if report_root != (ROOT / ".ai" / "context" / "agent_work" / "T475").resolve():
        raise ShadowDeltaError("report root must be the declared T475 agent-work root")

    if args.compare_existing:
        required = [
            report_root / "input_manifest.json",
            report_root / "baseline_manifest.json",
            report_root / "candidate_manifest.json",
            report_root / "repeatability_and_benchmark.json",
            work_root / "baseline",
            work_root / "candidate",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise ShadowDeltaError(f"existing comparison inputs missing: {missing}")
        baseline_manifest = json.loads((report_root / "baseline_manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads((report_root / "candidate_manifest.json").read_text(encoding="utf-8"))
        current_baseline = output_manifest(work_root / "baseline", str(baseline_manifest["ref"]))
        current_candidate = output_manifest(work_root / "candidate", str(candidate_manifest["ref"]))
        if current_baseline["aggregate_sha256"] != baseline_manifest["aggregate_sha256"]:
            raise ShadowDeltaError("retained baseline root no longer matches its frozen manifest")
        if current_candidate["aggregate_sha256"] != candidate_manifest["aggregate_sha256"]:
            raise ShadowDeltaError("retained candidate root no longer matches its frozen manifest")
        summary, sensitive, chunk_impact = compare_outputs(
            baseline_root=work_root / "baseline",
            candidate_root=work_root / "candidate",
            baseline_manifest=baseline_manifest,
            candidate_manifest=candidate_manifest,
            report_root=report_root,
            work_root=work_root,
        )
        chunk_impact["chunker_input_source_hashes"] = {
            path: sha256_file(ROOT / path)
            for path in ("pipelines/chunking/chunker.py", "config/chunking/book_genres.yaml")
            if (ROOT / path).is_file()
        }
        finalize_ledger(report_root)
        write_json(report_root / "delta_summary.json", summary)
        write_json(report_root / "sensitive_scope_summary.json", sensitive)
        write_json(report_root / "chunk_input_impact.json", chunk_impact)
        benchmark = json.loads((report_root / "repeatability_and_benchmark.json").read_text(encoding="utf-8"))
        lines = [
            "# Luna T475 Trial Log",
            "",
            "Bounded execution only. No ambiguity was resolved and no chunker was run.",
            "",
            f"- trials: {benchmark['repetitions']}",
            f"- deterministic: {str(benchmark['deterministic']).lower()}",
            f"- baseline median seconds: {benchmark['baseline_median_seconds']}",
            f"- candidate median seconds: {benchmark['candidate_median_seconds']}",
            f"- baseline output hash: {baseline_manifest['aggregate_sha256']}",
            f"- candidate output hash: {candidate_manifest['aggregate_sha256']}",
            "- comparison resumed from frozen final roots after the initial full-row SQLite index exhausted scratch disk",
            "- bounded comparator stores only keys, hashes, and byte offsets; full rows remain in shadow files",
            "- outputs retained: build/T475/baseline and build/T475/candidate",
            "- visible Scripture text in reports: false",
            "- unresolved items: semantic acceptability of measured deltas belongs to Terra/Sol",
        ]
        (report_root / "luna_trial_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"T475 existing-shadow comparison complete: {summary['totals']}")
        return 0

    if report_root.exists():
        shutil.rmtree(report_root)
    report_root.mkdir(parents=True)

    revisions = control["source_revisions"]
    baseline_ref = run_git(ROOT, "rev-parse", revisions["baseline_ref"])
    candidate_ref = run_git(ROOT, "rev-parse", revisions["candidate_ref"])
    inputs = control["identical_input_contract"]
    archive = (ROOT / inputs["raw_archive"]).resolve()
    manifest = (ROOT / inputs["source_manifest"]).resolve()
    for path in (archive, manifest, ROOT / inputs["canon_config"], ROOT / inputs["marker_coverage"]):
        if not path.is_file():
            raise ShadowDeltaError(f"input missing: {path}")

    source_root = work_root / "source"
    baseline_source = source_root / "baseline"
    candidate_source = source_root / "candidate"
    clean_dir(work_root, source_root)
    extract_source_snapshot(ROOT, work_root, baseline_ref, baseline_source)
    extract_source_snapshot(ROOT, work_root, candidate_ref, candidate_source)

    pin_paths = list(inputs["pin_source_files"])
    input_manifest = {
        "schema_version": "t475_input_manifest.v1",
        "task_id": "T475",
        "baseline_ref": baseline_ref,
        "candidate_ref": candidate_ref,
        "raw_archive": {"path": inputs["raw_archive"], "sha256": sha256_file(archive), "bytes": archive.stat().st_size},
        "source_manifest": {"path": inputs["source_manifest"], "sha256": sha256_file(manifest)},
        "canon_config": {"path": inputs["canon_config"], "sha256": sha256_file(ROOT / inputs["canon_config"])},
        "marker_coverage": {"path": inputs["marker_coverage"], "sha256": sha256_file(ROOT / inputs["marker_coverage"])},
        "baseline_source_hashes": source_hashes(ROOT, baseline_ref, pin_paths),
        "candidate_source_hashes": source_hashes(ROOT, candidate_ref, pin_paths),
        "required_flag": "--canonical-66-filter",
        "sha_bypass_used": False,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
        },
        "non_authorizing": True,
    }
    write_json(report_root / "input_manifest.json", input_manifest)

    repetitions = args.trials or int(control["trial_contract"]["repetitions"])
    if repetitions < 3:
        raise ShadowDeltaError("at least three trials are required")
    baseline_root = work_root / "baseline"
    candidate_root = work_root / "candidate"
    receipts: list[dict[str, Any]] = []
    baseline_manifests: list[dict[str, Any]] = []
    candidate_manifests: list[dict[str, Any]] = []
    for trial in range(1, repetitions + 1):
        baseline_seconds, baseline_command = run_import(
            source_root=baseline_source,
            archive=archive,
            manifest=manifest,
            side_root=baseline_root,
            work_root=work_root,
        )
        baseline_output = output_manifest(baseline_root, baseline_ref)
        candidate_seconds, candidate_command = run_import(
            source_root=candidate_source,
            archive=archive,
            manifest=manifest,
            side_root=candidate_root,
            work_root=work_root,
        )
        candidate_output = output_manifest(candidate_root, candidate_ref)
        baseline_manifests.append(baseline_output)
        candidate_manifests.append(candidate_output)
        receipts.append(
            {
                "trial": trial,
                "warmup_class": "cold_recorded" if trial == 1 else "warm",
                "baseline_seconds": round(baseline_seconds, 6),
                "candidate_seconds": round(candidate_seconds, 6),
                "baseline_manifest_sha256": baseline_output["aggregate_sha256"],
                "candidate_manifest_sha256": candidate_output["aggregate_sha256"],
                "baseline_command": baseline_command,
                "candidate_command": candidate_command,
            }
        )

    baseline_hashes = {item["aggregate_sha256"] for item in baseline_manifests}
    candidate_hashes = {item["aggregate_sha256"] for item in candidate_manifests}
    deterministic = len(baseline_hashes) == 1 and len(candidate_hashes) == 1
    if not deterministic:
        raise ShadowDeltaError("repeated shadow outputs are not byte-identical")
    baseline_manifest = baseline_manifests[-1]
    candidate_manifest = candidate_manifests[-1]
    write_json(report_root / "baseline_manifest.json", baseline_manifest)
    write_json(report_root / "candidate_manifest.json", candidate_manifest)

    benchmark = {
        "schema_version": "t475_repeatability_and_benchmark.v1",
        "repetitions": repetitions,
        "warmup_policy": control["trial_contract"]["warmup_policy"],
        "deterministic": deterministic,
        "baseline_median_seconds": round(statistics.median(row["baseline_seconds"] for row in receipts), 6),
        "candidate_median_seconds": round(statistics.median(row["candidate_seconds"] for row in receipts), 6),
        "receipts": receipts,
        "performance_alone_may_advance": False,
    }
    write_json(report_root / "repeatability_and_benchmark.json", benchmark)

    summary, sensitive, chunk_impact = compare_outputs(
        baseline_root=baseline_root,
        candidate_root=candidate_root,
        baseline_manifest=baseline_manifest,
        candidate_manifest=candidate_manifest,
        report_root=report_root,
        work_root=work_root,
    )
    chunk_impact["chunker_input_source_hashes"] = {
        path: sha256_file(ROOT / path)
        for path in (
            "pipelines/chunking/chunker.py",
            "config/chunking/book_genres.yaml",
        )
        if (ROOT / path).is_file()
    }
    finalize_ledger(report_root)
    write_json(report_root / "delta_summary.json", summary)
    write_json(report_root / "sensitive_scope_summary.json", sensitive)
    write_json(report_root / "chunk_input_impact.json", chunk_impact)

    lines = [
        "# Luna T475 Trial Log",
        "",
        "Bounded execution only. No ambiguity was resolved and no chunker was run.",
        "",
        f"- trials: {repetitions}",
        f"- deterministic: {str(deterministic).lower()}",
        f"- baseline median seconds: {benchmark['baseline_median_seconds']}",
        f"- candidate median seconds: {benchmark['candidate_median_seconds']}",
        f"- baseline output hash: {baseline_manifest['aggregate_sha256']}",
        f"- candidate output hash: {candidate_manifest['aggregate_sha256']}",
        "- outputs retained: build/T475/baseline and build/T475/candidate",
        "- visible Scripture text in reports: false",
        "- unresolved items: semantic acceptability of measured deltas belongs to Terra/Sol",
    ]
    (report_root / "luna_trial_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"T475 shadow delta complete: {summary['totals']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ShadowDeltaError as exc:
        print(f"T475 shadow delta failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
