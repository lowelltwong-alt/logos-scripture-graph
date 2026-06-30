#!/usr/bin/env python3
"""Validate the T412 Rust-first no-text observation substrate contract.

Default mode is contract-only so validate_all.py stays fast and never reruns the
full Bible scan. Use --input build/observation_substrate/current after running
the Rust scanner to validate generated ledgers.

No-text enforcement is intentionally key-name based plus scanner-contract based:
rows must set no_text=true and must not expose known text-bearing keys, while
free-text note fields such as anomaly reasons are not length-scanned.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
TASK_ID = "T412"
CONTROL = ROOT / ".ai" / "control" / "rust_first_observation_substrate.yaml"
TASK = ROOT / ".ai" / "tasks" / "T412.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T412" / "handoff.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T412_RUST_FIRST_OBSERVATION_SUBSTRATE.md"
RUST_CARGO = ROOT / "tools" / "usfm_observation_scanner" / "Cargo.toml"
RUST_MAIN = ROOT / "tools" / "usfm_observation_scanner" / "src" / "main.rs"
CANON = ROOT / "config" / "canon" / "canonical_66_books.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_OUTPUTS = [
    "scan_manifest.json",
    "book_observations.jsonl",
    "verse_observations.jsonl",
    "span_observation_features.jsonl",
    "risk_signal_index.jsonl",
    "strong_occurrence_index.jsonl",
    "marker_anomalies.jsonl",
]

FORBIDDEN_TRUE_FIELDS = {
    "authorizes_cursor_raw_whole_bible_reread",
    "authorizes_cursor_target_selection",
    "authorizes_exact_target_selection",
    "authorizes_reviewed_gold_promotion",
    "authorizes_child_spans",
    "authorizes_chunk_output_change",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_boundary_import",
    "authorizes_whole_bible_output_pass",
    "authorizes_backend_choice",
    "authorizes_retrieval_profile_promotion",
    "authorizes_preferred_reading_or_source_tradition",
    "authorizes_canon_scope_change",
    "authorizes_source_or_manuscript_row_population",
    "authorizes_theology_authority_change",
    "cursor_may_select_target",
    "promotes_reviewed_gold",
    "implements_chunk_output",
    "adds_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "chooses_backend",
    "promotes_retrieval_profile",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_source_or_manuscript_rows",
    "authorizes_theology_authority",
}

FORBIDDEN_TEXT_KEYS = {"text", "raw_text", "verse_text", "full_text", "content", "body"}
FORBIDDEN_TEXT = [
    re.compile(r"\b(authorizes?_(?:reviewed_gold|chunk_output|child_span|route|evaluator|graph|retrieval|embedding|vector|boundary|theology)[\w-]*)\s*:\s*true\b", re.I),
    re.compile(r"\b(reviewed gold promoted|chunk output created|child span created|embedding run|vector index built)\b", re.I),
]


class RustObservationSubstrateError(ValueError):
    """Raised when T412 contract or generated substrate artifacts are invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _strip_front_matter(path.read_text(encoding="utf-8"))
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise RustObservationSubstrateError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise RustObservationSubstrateError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise RustObservationSubstrateError(f"{_rel(path)}: required file is missing")


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise RustObservationSubstrateError(f"{label} must be a list of non-empty strings")
    return value


def _canonical_books() -> list[str]:
    data = _read_yaml(CANON)
    books = _string_list(data.get("canonical_66_books"), f"{_rel(CANON)} canonical_66_books")
    if len(books) != 66:
        raise RustObservationSubstrateError(f"{_rel(CANON)}: expected 66 canonical books")
    return books


def _require_false_authority(mapping: Any, label: str) -> None:
    if not isinstance(mapping, dict):
        raise RustObservationSubstrateError(f"{label}: authority mapping is required")
    true_fields = sorted(field for field in FORBIDDEN_TRUE_FIELDS if mapping.get(field) is True)
    if true_fields:
        raise RustObservationSubstrateError(f"{label}: forbidden authority field(s) true: {true_fields}")


def _walk_values(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text.lower() in FORBIDDEN_TEXT_KEYS:
                raise RustObservationSubstrateError(f"{label}: forbidden text-bearing key {key_text!r}")
            if key_text in FORBIDDEN_TRUE_FIELDS and child is True:
                raise RustObservationSubstrateError(f"{label}: forbidden authority field {key_text!r} is true")
            _walk_values(child, f"{label}.{key_text}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_values(child, f"{label}[{index}]")


def _require_non_authorizing_row(row: dict[str, Any], path: Path, line_number: int | None = None) -> None:
    label = f"{_rel(path)}:{line_number}" if line_number else _rel(path)
    if row.get("non_authorizing") is not True:
        raise RustObservationSubstrateError(f"{label}: non_authorizing must be true")
    if row.get("no_text") is not True:
        raise RustObservationSubstrateError(f"{label}: no_text must be true")
    _walk_values(row, label)


def _read_jsonl(path: Path, *, allow_empty: bool = False) -> list[dict[str, Any]]:
    _require_file(path)
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RustObservationSubstrateError(f"{_rel(path)}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise RustObservationSubstrateError(f"{_rel(path)}:{line_number}: expected JSON object")
        _require_non_authorizing_row(row, path, line_number)
        rows.append(row)
    if not rows and not allow_empty:
        raise RustObservationSubstrateError(f"{_rel(path)}: must contain at least one JSONL row")
    return rows


def _require_fields(row: dict[str, Any], fields: set[str], path: Path, line_number: int) -> None:
    missing = sorted(field for field in fields if field not in row)
    if missing:
        raise RustObservationSubstrateError(f"{_rel(path)}:{line_number}: missing required field(s) {missing}")


def _require_non_negative_int(row: dict[str, Any], field: str, path: Path, line_number: int) -> None:
    value = row.get(field)
    if not isinstance(value, int) or value < 0:
        raise RustObservationSubstrateError(f"{_rel(path)}:{line_number}: {field} must be a non-negative integer")


def validate_contract() -> dict[str, Any]:
    for path in (CONTROL, TASK, HANDOFF, ROADMAP, RUST_CARGO, RUST_MAIN):
        _require_file(path)

    control = _read_yaml(CONTROL)
    if control.get("object_type") != "rust_first_observation_substrate" or control.get("task_id") != TASK_ID:
        raise RustObservationSubstrateError(f"{_rel(CONTROL)}: must declare T412 rust_first_observation_substrate")
    _require_false_authority(control.get("authority"), _rel(CONTROL))
    required_files = _string_list(control.get("generated_artifacts", {}).get("required_files"), "generated_artifacts.required_files")
    if required_files != REQUIRED_OUTPUTS:
        raise RustObservationSubstrateError(f"{_rel(CONTROL)}: generated_artifacts.required_files must match T412 output contract")
    validation = control.get("validation")
    if not isinstance(validation, dict):
        raise RustObservationSubstrateError(f"{_rel(CONTROL)}: validation mapping is required")
    validate_all_policy = validation.get("validate_all_policy")
    if not isinstance(validate_all_policy, str):
        raise RustObservationSubstrateError(f"{_rel(CONTROL)}: validate_all_policy must forbid full scan in validate_all.py")
    normalized_policy = validate_all_policy.lower()
    for phrase in ("validate_all.py", "t412 contract validator", "must not run the full rust scan", "focused task"):
        if phrase not in normalized_policy:
            raise RustObservationSubstrateError(f"{_rel(CONTROL)}: validate_all_policy missing required policy phrase {phrase!r}")

    task = _read_yaml(TASK)
    if task.get("id") != TASK_ID or task.get("branch") != "codex/t412-rust-observation-substrate":
        raise RustObservationSubstrateError(f"{_rel(TASK)}: must declare T412 and the codex/t412 branch")
    _require_false_authority(task.get("authorization"), _rel(TASK))
    allowed = _string_list(task.get("scope", {}).get("allowed_paths"), f"{_rel(TASK)} scope.allowed_paths")
    for required in ("tools/usfm_observation_scanner/", "scripts/validate_rust_observation_substrate.py", "scripts/build_cursor_observation_pack.py"):
        if required not in allowed:
            raise RustObservationSubstrateError(f"{_rel(TASK)}: scope.allowed_paths missing {required}")

    cargo = RUST_CARGO.read_text(encoding="utf-8")
    for phrase in ('name = "usfm_observation_scanner"', 'hex =', 'serde_json', 'serde_yaml', 'sha2 =', 'zip ='):
        if phrase not in cargo:
            raise RustObservationSubstrateError(f"{_rel(RUST_CARGO)}: missing required Rust dependency or package phrase {phrase!r}")

    rust = RUST_MAIN.read_text(encoding="utf-8")
    for phrase in ("--no-text is required", "non_authorizing", "no_text", "RustObservationScanManifest"):
        if phrase not in rust:
            raise RustObservationSubstrateError(f"{_rel(RUST_MAIN)}: missing required scanner phrase {phrase!r}")
    for pattern in FORBIDDEN_TEXT:
        if pattern.search(rust):
            raise RustObservationSubstrateError(f"{_rel(RUST_MAIN)}: forbidden authority claim pattern detected")

    validate_all = VALIDATE_ALL.read_text(encoding="utf-8")
    if "validate_rust_observation_substrate.py" not in validate_all:
        raise RustObservationSubstrateError(f"{_rel(VALIDATE_ALL)}: missing T412 validator gate")
    if "cargo run --manifest-path tools/usfm_observation_scanner/Cargo.toml" in validate_all:
        raise RustObservationSubstrateError(f"{_rel(VALIDATE_ALL)}: validate_all.py must not run the full Rust scan")

    roadmap = ROADMAP.read_text(encoding="utf-8")
    for phrase in ("Rust scan -> Python validate -> Cursor compressed packet", "T411 remains frozen", "Claude Audit Prompt"):
        if phrase not in roadmap:
            raise RustObservationSubstrateError(f"{_rel(ROADMAP)}: missing required roadmap phrase {phrase!r}")

    return {"mode": "contract", "task_id": TASK_ID}


def validate_generated_substrate(input_dir: Path) -> dict[str, Any]:
    if not input_dir.is_dir():
        raise RustObservationSubstrateError(f"{input_dir}: input directory is missing")

    paths = {name: input_dir / name for name in REQUIRED_OUTPUTS}
    for path in paths.values():
        _require_file(path)

    try:
        manifest = json.loads(paths["scan_manifest.json"].read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RustObservationSubstrateError(f"{paths['scan_manifest.json']}: invalid JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise RustObservationSubstrateError(f"{paths['scan_manifest.json']}: expected JSON object")
    _require_non_authorizing_row(manifest, paths["scan_manifest.json"])
    if manifest.get("output_files") != REQUIRED_OUTPUTS:
        raise RustObservationSubstrateError("scan_manifest.json: output_files must match required T412 output list")
    if manifest.get("canonical_book_count") != 66:
        raise RustObservationSubstrateError("scan_manifest.json: canonical_book_count must be 66")

    book_rows = _read_jsonl(paths["book_observations.jsonl"])
    canonical_books = _canonical_books()
    canonical_seen = [
        row.get("book_id")
        for row in book_rows
        if row.get("source_class") == "canonical_66"
    ]
    if canonical_seen != canonical_books:
        raise RustObservationSubstrateError("book_observations.jsonl: canonical_66 book order must match config/canon/canonical_66_books.yaml")
    for index, row in enumerate(book_rows, start=1):
        _require_fields(
            row,
            {
                "type",
                "schema_version",
                "book_id",
                "usfm_code",
                "source_entry",
                "source_class",
                "sha256_short",
                "bytes_read",
                "char_count",
                "line_count",
                "chapter_count",
                "verse_count",
                "marker_counts",
                "strong_h_count",
                "strong_g_count",
                "feature_flags",
            },
            paths["book_observations.jsonl"],
            index,
        )
        for field in ("bytes_read", "char_count", "line_count", "chapter_count", "verse_count", "strong_h_count", "strong_g_count"):
            _require_non_negative_int(row, field, paths["book_observations.jsonl"], index)
        if not isinstance(row.get("marker_counts"), dict):
            raise RustObservationSubstrateError(f"{paths['book_observations.jsonl']}:{index}: marker_counts must be an object")

    verse_rows = _read_jsonl(paths["verse_observations.jsonl"])
    for index, row in enumerate(verse_rows, start=1):
        _require_fields(
            row,
            {
                "type",
                "schema_version",
                "book_id",
                "osis_ref",
                "chapter",
                "verse",
                "source_line_start",
                "source_line_end",
                "marker_counts",
                "strong_ids",
                "feature_flags",
            },
            paths["verse_observations.jsonl"],
            index,
        )
        for field in ("chapter", "verse", "source_line_start", "source_line_end"):
            _require_non_negative_int(row, field, paths["verse_observations.jsonl"], index)
        if row["source_line_end"] < row["source_line_start"]:
            raise RustObservationSubstrateError(f"{paths['verse_observations.jsonl']}:{index}: source_line_end before source_line_start")
        if not isinstance(row.get("strong_ids"), list):
            raise RustObservationSubstrateError(f"{paths['verse_observations.jsonl']}:{index}: strong_ids must be a list")

    span_rows = _read_jsonl(paths["span_observation_features.jsonl"])
    for index, row in enumerate(span_rows, start=1):
        _require_fields(
            row,
            {"span_id", "book_id", "osis_start", "osis_end", "span_kind", "verse_count", "marker_counts", "risk_flags"},
            paths["span_observation_features.jsonl"],
            index,
        )
        _require_non_negative_int(row, "verse_count", paths["span_observation_features.jsonl"], index)

    _read_jsonl(paths["risk_signal_index.jsonl"], allow_empty=True)
    _read_jsonl(paths["strong_occurrence_index.jsonl"], allow_empty=True)
    _read_jsonl(paths["marker_anomalies.jsonl"], allow_empty=True)

    return {
        "mode": "generated",
        "books": len(book_rows),
        "canonical_books": len(canonical_seen),
        "verses": len(verse_rows),
        "spans": len(span_rows),
    }


def validate_rust_observation_substrate(input_dir: Path | None = None) -> dict[str, Any]:
    contract = validate_contract()
    if input_dir is None:
        return contract
    generated = validate_generated_substrate(input_dir)
    return {"contract": contract, "generated": generated}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=None, help="Generated observation substrate directory.")
    args = parser.parse_args(argv)
    try:
        result = validate_rust_observation_substrate(args.input)
    except RustObservationSubstrateError as exc:
        print(f"T412 Rust observation substrate validation failed: {exc}", file=sys.stderr)
        return 1
    mode = "generated" if args.input else "contract"
    print(f"T412 Rust observation substrate validation passed ({mode} mode).")
    if args.input:
        print(json.dumps(result["generated"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
