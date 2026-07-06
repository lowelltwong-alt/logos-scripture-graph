#!/usr/bin/env python3
"""Validate the T433 Philemon original-language alignment pilot."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PILOT_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "pilots" / "T433_phlm_alignment_bridge"
CONTROL = ROOT / ".ai" / "control" / "t433_phlm_original_language_evidence_pilot.yaml"
TASK = ROOT / ".ai" / "tasks" / "T433.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T433" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T433" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T433_PHLM_ORIGINAL_LANGUAGE_EVIDENCE_PILOT.md"
BUILD_SCRIPT = ROOT / "scripts" / "build_t433_phlm_alignment_pilot.py"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

TARGET_REFS = {"Phlm.1.1", "Phlm.1.2", "Phlm.1.3"}
TARGET_SPAN = "Phlm.1.1-Phlm.1.3"
PRODUCTION_ROOTS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)

FORBIDDEN_AUTH_TRUE = {
    "authorizes_source_language_truth",
    "authorizes_lexical_truth",
    "authorizes_strongs_as_source_text",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_canon_scope_change",
    "authorizes_translation_judgment",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_route_behavior",
    "authorizes_evaluator_behavior",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embeddings_or_indexes",
    "authorizes_theology_authority",
}


class T433PilotError(ValueError):
    """Raised when the T433 pilot is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T433PilotError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T433PilotError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        rows = []
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if line.strip():
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise T433PilotError(f"{_rel(path)}:{line_no} must be a JSON object")
                    rows.append(row)
        return rows
    except (OSError, json.JSONDecodeError) as exc:
        raise T433PilotError(f"{_rel(path)} unreadable JSONL: {exc}") from exc


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if key in mapping and mapping.get(key) is not False:
            raise T433PilotError(f"{label}.{key} must be false")


def _require_all_false(mapping: dict[str, Any], label: str) -> None:
    for key, value in mapping.items():
        if key.startswith("authorizes_") and value is not False:
            raise T433PilotError(f"{label}.{key} must be false")


def validate_source_tokens(rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise T433PilotError("source token rows are missing")
    refs = {str(row.get("osis_ref")) for row in rows}
    if refs != TARGET_REFS:
        raise T433PilotError(f"source token refs must be {sorted(TARGET_REFS)}, got {sorted(refs)}")
    ids: set[str] = set()
    for row in rows:
        label = str(row.get("id", "<missing-token-id>"))
        if label in ids:
            raise T433PilotError(f"duplicate source token id {label}")
        ids.add(label)
        if row.get("type") != "SourceLanguageToken":
            raise T433PilotError(f"{label}: type must be SourceLanguageToken")
        if row.get("source_id") != "sblgnt" or row.get("language") != "greek" or row.get("book_id") != "Phlm":
            raise T433PilotError(f"{label}: wrong source/language/book")
        if row.get("strong_id") is not None or row.get("lemma") is not None or row.get("morphology") is not None:
            raise T433PilotError(f"{label}: SBLGNT pilot must not populate Strong's, lemma, or morphology fields")
        if row.get("evidence_mode") != "observed_source_view" or row.get("inferred_vs_observed") != "observed":
            raise T433PilotError(f"{label}: source tokens must be observed source-view evidence")
        if row.get("trust_zone") != "candidate" or row.get("status") != "candidate":
            raise T433PilotError(f"{label}: source tokens must remain candidate")
        if row.get("confidence") != "high":
            raise T433PilotError(f"{label}: observed token confidence must be high")
        if row.get("source_view_path") != "data/candidate/original_language_evidence/canonical_source_views/sblgnt/files/Phlm.xml":
            raise T433PilotError(f"{label}: wrong source view path")
        storage = row.get("text_storage_policy")
        if not isinstance(storage, dict) or storage.get("license_authorized_for_storage") is not True:
            raise T433PilotError(f"{label}: text storage policy must be license-authorized")
        authority = row.get("authority")
        if not isinstance(authority, dict):
            raise T433PilotError(f"{label}: authority must be a mapping")
        _require_all_false(authority, f"{label}.authority")


def validate_editorial_layers(rows: list[dict[str, Any]], token_ids: set[str]) -> None:
    if len(rows) < 5:
        raise T433PilotError("expected paragraphing, three versification rows, and punctuation/sigla editorial rows")
    kinds = {str(row.get("layer_kind")) for row in rows}
    if not {"paragraphing", "versification", "punctuation"} <= kinds:
        raise T433PilotError(f"editorial layer kinds missing required classes: {sorted(kinds)}")
    for row in rows:
        label = str(row.get("id", "<missing-editorial-id>"))
        if row.get("type") != "EditorialLayer":
            raise T433PilotError(f"{label}: type must be EditorialLayer")
        if row.get("is_editorial_not_autograph_certainty") is not True:
            raise T433PilotError(f"{label}: must be editorial-not-autograph certainty")
        if row.get("editorial_origin") != "source_edition":
            raise T433PilotError(f"{label}: editorial origin must be source_edition")
        if row.get("evidence_mode") != "observed_source_view":
            raise T433PilotError(f"{label}: editorial rows must be observed source-view evidence")
        for token_id in row.get("applies_to_source_token_ids", []):
            if token_id not in token_ids:
                raise T433PilotError(f"{label}: applies to unknown source token {token_id}")
        authority = row.get("authority")
        if not isinstance(authority, dict):
            raise T433PilotError(f"{label}: authority must be a mapping")
        _require_all_false(authority, f"{label}.authority")


def validate_alignments(rows: list[dict[str, Any]], token_ids: set[str]) -> None:
    if len(rows) != 3:
        raise T433PilotError("expected exactly three verse-level alignment records")
    refs = {str(row.get("osis_ref")) for row in rows}
    if refs != TARGET_REFS:
        raise T433PilotError(f"alignment refs must be {sorted(TARGET_REFS)}, got {sorted(refs)}")
    for row in rows:
        label = str(row.get("id", "<missing-alignment-id>"))
        if row.get("type") != "AlignmentRecord":
            raise T433PilotError(f"{label}: type must be AlignmentRecord")
        if row.get("alignment_type") != "many_to_many":
            raise T433PilotError(f"{label}: alignment_type must be many_to_many")
        if row.get("alignment_basis") != "source_token_order" or row.get("method") != "source_view_bridge":
            raise T433PilotError(f"{label}: wrong alignment basis/method")
        if row.get("evidence_mode") != "inferred" or row.get("inferred_vs_observed") != "inferred":
            raise T433PilotError(f"{label}: alignments must be inferred bridge evidence")
        if row.get("confidence") != "low":
            raise T433PilotError(f"{label}: alignment confidence must stay low")
        if row.get("review_status") != "unreviewed" or row.get("status") != "candidate":
            raise T433PilotError(f"{label}: alignment must stay unreviewed candidate")
        if row.get("translation_strong_hints_are_source_text") is not False:
            raise T433PilotError(f"{label}: WEB Strong's hints must not be source text")
        if not row.get("translation_side_strong_hints"):
            raise T433PilotError(f"{label}: expected translation-side Strong's hints")
        source = row.get("source")
        if not isinstance(source, dict) or source.get("source_id") != "sblgnt":
            raise T433PilotError(f"{label}: source must be sblgnt")
        if source.get("strong") is not None:
            raise T433PilotError(f"{label}: source.strong must be null")
        for token_id in source.get("source_token_ids", []):
            if token_id not in token_ids:
                raise T433PilotError(f"{label}: references unknown source token {token_id}")
        authority = row.get("authority")
        if not isinstance(authority, dict):
            raise T433PilotError(f"{label}: authority must be a mapping")
        _require_all_false(authority, f"{label}.authority")


def _validate_schema_records(paths: list[Path]) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return
    schema_paths = {
        "SourceLanguageToken": ROOT / "schemas" / "source_language_token.schema.json",
        "EditorialLayer": ROOT / "schemas" / "editorial_layer.schema.json",
        "AlignmentRecord": ROOT / "schemas" / "alignment_record.schema.json",
    }
    validators = {
        rec_type: Draft202012Validator(json.loads(path.read_text(encoding="utf-8")))
        for rec_type, path in schema_paths.items()
    }
    failures: list[str] = []
    for path in paths:
        for line_no, row in enumerate(_read_jsonl(path), start=1):
            validator = validators.get(str(row.get("type")))
            if validator is None:
                failures.append(f"{_rel(path)}:{line_no}: unknown type {row.get('type')}")
                continue
            for error in validator.iter_errors(row):
                failures.append(f"{_rel(path)}:{line_no}: {error.message}")
    if failures:
        raise T433PilotError("schema validation failed: " + "; ".join(failures[:20]))


def _validate_no_production_outputs(root: Path) -> None:
    for directory in PRODUCTION_ROOTS:
        path = root / directory.relative_to(ROOT)
        if path.exists() and any(path.rglob("*")):
            raise T433PilotError(f"{_rel(path)} must stay empty until a later production-population task")


def validate_t433_phlm_alignment_pilot(root: Path = ROOT) -> dict[str, Any]:
    pilot_root = root / PILOT_ROOT.relative_to(ROOT)
    manifest_path = pilot_root / "manifest.yaml"
    tokens_path = pilot_root / "source_language_tokens.jsonl"
    editorial_path = pilot_root / "editorial_layers.jsonl"
    alignments_path = pilot_root / "alignment_records.jsonl"

    for relative in (
        CONTROL,
        TASK,
        HANDOFF,
        DAD_PREFLIGHT,
        ROADMAP,
        BUILD_SCRIPT,
        manifest_path,
        tokens_path,
        editorial_path,
        alignments_path,
    ):
        path = relative if relative.is_absolute() else root / relative.relative_to(ROOT)
        if not path.exists():
            raise T433PilotError(f"{_rel(path)} is missing")

    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "t433_phlm_original_language_evidence_pilot":
        raise T433PilotError("T433 control object_type is wrong")
    _require_false(control.get("authority", {}), FORBIDDEN_AUTH_TRUE, "control.authority")
    if control.get("rust_policy", {}).get("rust_added_in_t433") is not False:
        raise T433PilotError("T433 rust_policy.rust_added_in_t433 must be false")

    manifest = _read_yaml(manifest_path)
    if manifest.get("pilot_span") != TARGET_SPAN:
        raise T433PilotError("manifest pilot_span mismatch")
    if set(manifest.get("exact_refs", [])) != TARGET_REFS:
        raise T433PilotError("manifest exact_refs mismatch")
    if manifest.get("source_id") != "sblgnt":
        raise T433PilotError("manifest source_id must be sblgnt")
    _require_false(manifest.get("authority", {}), FORBIDDEN_AUTH_TRUE, "manifest.authority")
    if "translation-side hints" not in str(manifest.get("web_strongs_policy", "")):
        raise T433PilotError("manifest must keep WEB Strong's as translation-side hints")

    tokens = _read_jsonl(tokens_path)
    editorial_layers = _read_jsonl(editorial_path)
    alignments = _read_jsonl(alignments_path)
    validate_source_tokens(tokens)
    token_ids = {str(row["source_token_id"]) for row in tokens}
    validate_editorial_layers(editorial_layers, token_ids)
    validate_alignments(alignments, token_ids)

    counts = manifest.get("counts")
    expected_counts = {
        "source_language_tokens": len(tokens),
        "editorial_layers": len(editorial_layers),
        "alignment_records": len(alignments),
    }
    if counts != expected_counts:
        raise T433PilotError(f"manifest counts mismatch: {counts} != {expected_counts}")

    _validate_schema_records([tokens_path, editorial_path, alignments_path])
    _validate_no_production_outputs(root)

    validate_all_text = (root / VALIDATE_ALL.relative_to(ROOT)).read_text(encoding="utf-8")
    if "validate_t433_phlm_alignment_pilot.py" not in validate_all_text:
        raise T433PilotError("validate_all.py must run the T433 validator")

    dad_text = (root / DAD_PREFLIGHT.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("manifest-level metadata is not enough", "ugnt", "t435", "rust"):
        if phrase not in dad_text:
            raise T433PilotError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")

    roadmap_text = (root / ROADMAP.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("translation-side hints", "preferred reading", "rust", "ugnt is deferred"):
        if phrase not in roadmap_text:
            raise T433PilotError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")

    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t433_phlm_alignment_pilot(args.root.resolve())
    except T433PilotError as exc:
        print(f"T433 Philemon alignment pilot validation failed: {exc}", file=sys.stderr)
        return 1
    print("T433 Philemon alignment pilot validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
