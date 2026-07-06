#!/usr/bin/env python3
"""Validate the T435-A SBLGNT original-language observation scanner contract and generated ledgers."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
TASK = ROOT / ".ai" / "tasks" / "T435.task.yaml"
CONTROL = ROOT / ".ai" / "control" / "original_language_observation_scanner.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T435" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T435" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T435_ORIGINAL_LANGUAGE_OBSERVATION_SCANNER.md"
SCANNER = ROOT / "tools" / "original_language_observation_scanner"
CARGO = SCANNER / "Cargo.toml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
SBLGNT_MANIFEST = (
    ROOT
    / "data"
    / "candidate"
    / "original_language_evidence"
    / "canonical_source_views"
    / "sblgnt"
    / "canonical_source_view_manifest.yaml"
)
SBLGNT_INCLUDED = SBLGNT_MANIFEST.parent / "included_files.jsonl"
T433_PILOT = (
    ROOT
    / "data"
    / "candidate"
    / "original_language_evidence"
    / "pilots"
    / "T433_phlm_alignment_bridge"
)

EXPECTED_OUTPUT_FILES = {
    "scan_manifest.json",
    "source_view_file_observations.jsonl",
    "verse_token_observations.jsonl",
    "source_token_shape_index.jsonl",
    "editorial_layer_shape_index.jsonl",
    "t433_shadow_parity.json",
}

FORBIDDEN_ROW_KEYS = {
    "surface_text",
    "normalized_text",
    "observed_value",
    "full_text",
    "source_text",
    "manuscript_transcription",
    "manuscript_image",
    "preferred_reading",
}

FORBIDDEN_AUTH_TRUE = {
    "authorizes_source_language_truth",
    "authorizes_lexical_truth",
    "authorizes_word_level_alignment_truth",
    "authorizes_strongs_as_source_text",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_canon_scope_change",
    "authorizes_translation_judgment",
    "authorizes_chunk_boundary",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_route_behavior",
    "authorizes_evaluator_behavior",
    "authorizes_graph_or_retrieval_truth",
    "authorizes_embeddings_or_indexes",
    "authorizes_theology_authority",
}

PRODUCTION_ROOTS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)


class T435ValidationError(ValueError):
    """Raised when T435-A scanner artifacts violate the contract."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T435ValidationError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T435ValidationError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T435ValidationError(f"{_rel(path)} unreadable JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise T435ValidationError(f"{_rel(path)} must be a JSON object")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise T435ValidationError(f"{_rel(path)}:{line_no} must be a JSON object")
                rows.append(row)
    except (OSError, json.JSONDecodeError) as exc:
        raise T435ValidationError(f"{_rel(path)} unreadable JSONL: {exc}") from exc
    return rows


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if key in mapping and mapping.get(key) is not False:
            raise T435ValidationError(f"{label}.{key} must be false")


def _require_authority_false(row: dict[str, Any], label: str) -> None:
    authority = row.get("authority")
    if not isinstance(authority, dict):
        raise T435ValidationError(f"{label}: authority must be a mapping")
    _require_false(authority, FORBIDDEN_AUTH_TRUE, f"{label}.authority")
    for key, value in authority.items():
        if key.startswith("authorizes_") and value is not False:
            raise T435ValidationError(f"{label}.authority.{key} must be false")


def _walk_dicts(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        found.append(value)
        for child in value.values():
            found.extend(_walk_dicts(child))
    elif isinstance(value, list):
        for item in value:
            found.extend(_walk_dicts(item))
    return found


def _require_no_forbidden_keys(row: dict[str, Any], label: str) -> None:
    for mapping in _walk_dicts(row):
        for key in mapping:
            if key in FORBIDDEN_ROW_KEYS:
                raise T435ValidationError(f"{label}: forbidden text/authority key {key!r}")


def _require_no_text_policy(row: dict[str, Any], label: str) -> None:
    policy = row.get("text_storage_policy")
    if not isinstance(policy, dict):
        raise T435ValidationError(f"{label}: text_storage_policy must be present")
    if policy.get("no_text") is not True or policy.get("stores_source_text") is not False:
        raise T435ValidationError(f"{label}: no-text policy must be explicit")


def _require_candidate_shadow(row: dict[str, Any], label: str) -> None:
    if row.get("trust_zone") != "candidate":
        raise T435ValidationError(f"{label}: trust_zone must be candidate")
    if row.get("status") != "observation_shadow":
        raise T435ValidationError(f"{label}: status must be observation_shadow")
    if row.get("evidence_mode") != "observed_source_view_shape":
        raise T435ValidationError(f"{label}: evidence_mode must be observed_source_view_shape")
    if row.get("inferred_vs_observed") != "observed":
        raise T435ValidationError(f"{label}: inferred_vs_observed must be observed")


def _included_by_view_path() -> dict[str, dict[str, Any]]:
    rows = _read_jsonl(SBLGNT_INCLUDED)
    return {str(row["view_path"]): row for row in rows}


def _validate_common_row(row: dict[str, Any], included: dict[str, dict[str, Any]], label: str) -> None:
    _require_no_forbidden_keys(row, label)
    _require_authority_false(row, label)
    _require_no_text_policy(row, label)
    _require_candidate_shadow(row, label)
    if row.get("task_id") != "T435" or row.get("source_id") != "sblgnt":
        raise T435ValidationError(f"{label}: wrong task/source")
    if row.get("language") not in (None, "greek"):
        raise T435ValidationError(f"{label}: language must be greek when present")
    view_path = str(row.get("source_view_path", ""))
    if view_path not in included:
        raise T435ValidationError(f"{label}: source_view_path not present in SBLGNT included ledger")
    included_row = included[view_path]
    if row.get("source_file_sha256") != included_row.get("sha256"):
        raise T435ValidationError(f"{label}: stale source_file_sha256")
    if row.get("source_archive_path") != included_row.get("source_archive_path"):
        raise T435ValidationError(f"{label}: source_archive_path mismatch")
    for key in ("contains_source_provided_lemmas", "contains_source_provided_morphology", "contains_source_provided_strongs"):
        if row.get(key) not in (None, False):
            raise T435ValidationError(f"{label}: {key} must remain false for SBLGNT")


def _validate_tokens(rows: list[dict[str, Any]], included: dict[str, dict[str, Any]]) -> None:
    ids: set[str] = set()
    by_ref: dict[str, set[int]] = {}
    for index, row in enumerate(rows, start=1):
        label = f"source_token_shape_index:{index}"
        _validate_common_row(row, included, label)
        if row.get("type") != "SblgntSourceTokenShapeObservation":
            raise T435ValidationError(f"{label}: wrong type")
        for field in ("lemma", "morphology", "strong_id"):
            if row.get(field) is not None:
                raise T435ValidationError(f"{label}: {field} must be null for SBLGNT")
        row_id = str(row.get("id"))
        if row_id in ids:
            raise T435ValidationError(f"duplicate token observation id {row_id}")
        ids.add(row_id)
        ref = str(row.get("osis_ref"))
        verse_index = row.get("verse_token_index")
        if not isinstance(verse_index, int) or verse_index < 1:
            raise T435ValidationError(f"{label}: verse_token_index must be a positive integer")
        indexes = by_ref.setdefault(ref, set())
        if verse_index in indexes:
            raise T435ValidationError(f"{label}: duplicate verse token index for {ref}")
        indexes.add(verse_index)
        if not row.get("content_sha256_short") or row.get("content_char_count", 0) < 1:
            raise T435ValidationError(f"{label}: content hash/count observations are required")


def _validate_editorial(rows: list[dict[str, Any]], included: dict[str, dict[str, Any]]) -> None:
    ids: set[str] = set()
    required_kinds = {"paragraphing", "versification", "punctuation"}
    seen_kinds: set[str] = set()
    for index, row in enumerate(rows, start=1):
        label = f"editorial_layer_shape_index:{index}"
        _validate_common_row(row, included, label)
        if row.get("type") != "SblgntEditorialShapeObservation":
            raise T435ValidationError(f"{label}: wrong type")
        row_id = str(row.get("id"))
        if row_id in ids:
            raise T435ValidationError(f"duplicate editorial observation id {row_id}")
        ids.add(row_id)
        kind = str(row.get("layer_kind"))
        seen_kinds.add(kind)
        if row.get("is_editorial_not_autograph_certainty") is not True:
            raise T435ValidationError(f"{label}: must be editorial-not-autograph certainty")
        if kind == "punctuation" and not row.get("marker_content_sha256_short"):
            raise T435ValidationError(f"{label}: punctuation rows require content hash")
    if not required_kinds <= seen_kinds:
        raise T435ValidationError(f"editorial rows missing required kinds: {sorted(required_kinds - seen_kinds)}")


def _validate_verses(rows: list[dict[str, Any]], included: dict[str, dict[str, Any]]) -> None:
    refs: set[str] = set()
    for index, row in enumerate(rows, start=1):
        label = f"verse_token_observations:{index}"
        _validate_common_row(row, included, label)
        if row.get("type") != "SblgntVerseTokenObservation":
            raise T435ValidationError(f"{label}: wrong type")
        ref = str(row.get("osis_ref"))
        if ref in refs:
            raise T435ValidationError(f"duplicate verse observation {ref}")
        refs.add(ref)
        if row.get("token_shape_count", 0) < 1:
            raise T435ValidationError(f"{label}: token_shape_count must be positive")


def _validate_files(rows: list[dict[str, Any]], included: dict[str, dict[str, Any]]) -> None:
    books: set[str] = set()
    for index, row in enumerate(rows, start=1):
        label = f"source_view_file_observations:{index}"
        _validate_common_row(row, included, label)
        if row.get("type") != "SblgntSourceViewFileObservation":
            raise T435ValidationError(f"{label}: wrong type")
        book = str(row.get("book_id"))
        if book in books:
            raise T435ValidationError(f"duplicate file observation book {book}")
        books.add(book)
        if row.get("bytes_read") != row.get("size_bytes_from_included_ledger"):
            raise T435ValidationError(f"{label}: bytes_read must match included ledger size")


def _validate_parity(path: Path) -> dict[str, Any]:
    parity = _read_json(path)
    _require_authority_false(parity, "t433_shadow_parity")
    if parity.get("status") != "pass":
        raise T435ValidationError("t433_shadow_parity.json must pass when generated-mode validation runs")
    if parity.get("rust_source_token_shapes") != 41 or parity.get("t433_source_language_tokens") != 41:
        raise T435ValidationError("T433 token parity must be 41 vs 41")
    if parity.get("rust_editorial_shapes") != 7 or parity.get("t433_editorial_layers") != 7:
        raise T435ValidationError("T433 editorial parity must be 7 vs 7")
    return parity


def validate_generated(input_dir: Path) -> dict[str, Any]:
    files = {path.name for path in input_dir.iterdir() if path.is_file()}
    missing = EXPECTED_OUTPUT_FILES - files
    if missing:
        raise T435ValidationError(f"{_rel(input_dir)} missing output files: {sorted(missing)}")

    try:
        rel = input_dir.resolve().relative_to(ROOT)
    except ValueError:
        rel = None
    if rel is not None and not rel.as_posix().startswith("build/"):
        raise T435ValidationError("generated T435-A scanner outputs must stay under build/")

    manifest = _read_json(input_dir / "scan_manifest.json")
    if manifest.get("object_type") != "t435_sblgnt_observation_scan_manifest":
        raise T435ValidationError("scan_manifest object_type mismatch")
    if manifest.get("no_authority") is not True or manifest.get("no_text") is not True:
        raise T435ValidationError("scan_manifest must record no_authority and no_text")
    _require_authority_false(manifest, "scan_manifest")
    _require_no_text_policy(manifest, "scan_manifest")
    if manifest.get("source_id") != "sblgnt" or manifest.get("language") != "greek":
        raise T435ValidationError("scan_manifest source/language mismatch")
    if set(manifest.get("output_files", [])) != EXPECTED_OUTPUT_FILES:
        raise T435ValidationError("scan_manifest output_files mismatch")

    included = _included_by_view_path()
    file_rows = _read_jsonl(input_dir / "source_view_file_observations.jsonl")
    verse_rows = _read_jsonl(input_dir / "verse_token_observations.jsonl")
    token_rows = _read_jsonl(input_dir / "source_token_shape_index.jsonl")
    editorial_rows = _read_jsonl(input_dir / "editorial_layer_shape_index.jsonl")
    _validate_files(file_rows, included)
    _validate_verses(verse_rows, included)
    _validate_tokens(token_rows, included)
    _validate_editorial(editorial_rows, included)

    counts = manifest.get("row_counts")
    expected_counts = {
        "source_view_file_observations": len(file_rows),
        "verse_token_observations": len(verse_rows),
        "source_token_shape_index": len(token_rows),
        "editorial_layer_shape_index": len(editorial_rows),
    }
    if counts != expected_counts:
        raise T435ValidationError(f"scan_manifest row_counts mismatch: {counts} != {expected_counts}")
    if len(file_rows) == 27 and manifest.get("scanned_book_count") != 27:
        raise T435ValidationError("full SBLGNT scan must report 27 scanned books")
    parity = _validate_parity(input_dir / "t433_shadow_parity.json")
    if manifest.get("t433_shadow_parity_status") != parity.get("status"):
        raise T435ValidationError("manifest parity status mismatch")
    return manifest


def _validate_no_production_outputs() -> None:
    for root in PRODUCTION_ROOTS:
        if root.exists() and any(root.rglob("*")):
            raise T435ValidationError(f"{_rel(root)} must stay empty until a later production-population task")


def validate_contract() -> None:
    for path in (
        TASK,
        CONTROL,
        HANDOFF,
        DAD_PREFLIGHT,
        ROADMAP,
        CARGO,
        SCANNER / "src" / "main.rs",
        SBLGNT_MANIFEST,
        SBLGNT_INCLUDED,
        T433_PILOT / "manifest.yaml",
    ):
        if not path.exists():
            raise T435ValidationError(f"{_rel(path)} is missing")

    task = _read_yaml(TASK)
    if task.get("id") != "T435":
        raise T435ValidationError("T435 task id mismatch")
    auth = task.get("authorization", {})
    if auth.get("records_rust_sblgnt_observation_scanner") is not True:
        raise T435ValidationError("T435 task must record Rust SBLGNT observation scanner")
    _require_false(auth, FORBIDDEN_AUTH_TRUE, "task.authorization")
    allowed_paths = "\n".join(task.get("scope", {}).get("allowed_paths", []))
    for required in (
        "tools/original_language_observation_scanner/",
        "scripts/validate_t435_original_language_observation_scanner.py",
        "tests/test_t435_original_language_observation_scanner.py",
    ):
        if required not in allowed_paths:
            raise T435ValidationError(f"T435 task allowed_paths missing {required}")

    control = _read_yaml(CONTROL)
    if control.get("object_type") != "original_language_observation_scanner":
        raise T435ValidationError("T435 control object_type mismatch")
    _require_false(control.get("authority", {}), FORBIDDEN_AUTH_TRUE, "control.authority")
    if control.get("scanner_scope", {}).get("source_id") != "sblgnt":
        raise T435ValidationError("T435-A scanner scope must be SBLGNT")
    if control.get("scanner_scope", {}).get("writes_generated_build_outputs_only") is not True:
        raise T435ValidationError("T435-A scanner must write generated build outputs only")

    cargo_text = CARGO.read_text(encoding="utf-8")
    for dep in ("hex", "roxmltree", "serde_json", "serde_yaml", "sha2"):
        if dep not in cargo_text:
            raise T435ValidationError(f"Cargo.toml missing dependency {dep}")
    gitignore_text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "tools/original_language_observation_scanner/target/" not in gitignore_text:
        raise T435ValidationError(".gitignore must ignore the T435 Rust target directory")
    validate_all_text = VALIDATE_ALL.read_text(encoding="utf-8")
    if "validate_t435_original_language_observation_scanner.py" not in validate_all_text:
        raise T435ValidationError("validate_all.py must run the T435 contract validator")
    if "cargo run --manifest-path tools/original_language_observation_scanner" in validate_all_text:
        raise T435ValidationError("validate_all.py must not run the full T435 Rust scan")

    dad_text = DAD_PREFLIGHT.read_text(encoding="utf-8").lower()
    for phrase in ("rust", "shadow parity", "python remains the authority validator", "no source wording"):
        if phrase not in dad_text:
            raise T435ValidationError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")
    roadmap_text = ROADMAP.read_text(encoding="utf-8").lower()
    for phrase in ("sblgnt", "t433", "no-text", "hebrew jonah"):
        if phrase not in roadmap_text:
            raise T435ValidationError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")
    _validate_no_production_outputs()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=None, help="Generated build output directory to validate.")
    args = parser.parse_args(argv)
    try:
        validate_contract()
        if args.input is not None:
            validate_generated(args.input.resolve())
    except T435ValidationError as exc:
        print(f"T435 original-language observation scanner validation failed: {exc}", file=sys.stderr)
        return 1
    print("T435 original-language observation scanner validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
