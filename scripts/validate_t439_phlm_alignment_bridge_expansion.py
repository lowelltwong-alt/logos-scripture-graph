#!/usr/bin/env python3
"""Validate the T439 no-text full-Philemon alignment bridge pilot."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PILOT_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "pilots" / "T439_phlm_alignment_bridge_expansion"
CONTROL = ROOT / ".ai" / "control" / "t439_phlm_alignment_bridge_expansion.yaml"
TASK = ROOT / ".ai" / "tasks" / "T439.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T439" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T439" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T439_PHLM_ALIGNMENT_BRIDGE_EXPANSION.md"
BUILD_SCRIPT = ROOT / "scripts" / "build_t439_phlm_alignment_bridge_expansion.py"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
WEB_WORD_TOKENS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "word_tokens.jsonl"

TARGET_REFS = [f"Phlm.1.{index}" for index in range(1, 26)]
EXPECTED_COUNTS = {
    "source_language_tokens": 334,
    "editorial_layers": 98,
    "alignment_records": 25,
    "refs": 25,
}
TEXT_LEAK_KEYS = {
    "surface_text",
    "normalized_text",
    "source_text",
    "translation_text",
    "visible_text",
    "manuscript_text",
}
PRODUCTION_ROOTS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)
GREEK_RE = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")


class T439PilotError(ValueError):
    """Raised when the T439 pilot is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T439PilotError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T439PilotError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if line.strip():
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise T439PilotError(f"{_rel(path)}:{line_no} must be a JSON object")
                    rows.append(row)
    except (OSError, json.JSONDecodeError) as exc:
        raise T439PilotError(f"{_rel(path)} unreadable JSONL: {exc}") from exc
    return rows


def _require_all_authority_false(mapping: dict[str, Any], label: str) -> None:
    for key, value in mapping.items():
        if key.startswith(("authorizes_", "creates_", "changes_", "runs_", "selects_")) and value is not False:
            if key not in {"records_candidate_pilot", "creates_task_scoped_candidate_rows"}:
                raise T439PilotError(f"{label}.{key} must be false")


def _reject_text_leak(row: dict[str, Any], label: str) -> None:
    for key in TEXT_LEAK_KEYS:
        if key in row and row[key] not in (None, "", False):
            raise T439PilotError(f"{label} must not store visible text key {key}")
    for key, value in row.items():
        if isinstance(value, str) and GREEK_RE.search(value) and key not in {"id", "source_token_id"}:
            raise T439PilotError(f"{label}.{key} appears to leak Greek text")


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
        raise T439PilotError("schema validation failed: " + "; ".join(failures[:20]))


def _web_token_ids() -> set[str]:
    ids: set[str] = set()
    with WEB_WORD_TOKENS.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("osis_ref") in TARGET_REFS:
                ids.add(str(row["id"]))
    return ids


def _validate_no_production_outputs(root: Path) -> None:
    for directory in PRODUCTION_ROOTS:
        path = root / directory.relative_to(ROOT)
        if path.exists() and any(path.rglob("*")):
            raise T439PilotError(f"{_rel(path)} must stay empty until a later production task")


def validate_source_tokens(rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    if len(rows) != EXPECTED_COUNTS["source_language_tokens"]:
        raise T439PilotError(f"expected 334 source token rows, got {len(rows)}")
    ids: set[str] = set()
    by_ref: dict[str, list[str]] = {ref: [] for ref in TARGET_REFS}
    verse_positions: set[tuple[str, int]] = set()
    for row in rows:
        label = str(row.get("id", "<missing-token-id>"))
        if label in ids:
            raise T439PilotError(f"duplicate source token row id {label}")
        ids.add(label)
        _reject_text_leak(row, label)
        if row.get("type") != "SourceLanguageToken":
            raise T439PilotError(f"{label}: type must be SourceLanguageToken")
        ref = str(row.get("osis_ref"))
        if ref not in by_ref:
            raise T439PilotError(f"{label}: unexpected ref {ref}")
        if row.get("source_id") != "sblgnt" or row.get("language") != "greek" or row.get("book_id") != "Phlm":
            raise T439PilotError(f"{label}: wrong source/language/book")
        if row.get("strong_id") is not None or row.get("lemma") is not None or row.get("morphology") is not None:
            raise T439PilotError(f"{label}: T439 must not populate Strong's, lemma, or morphology")
        if row.get("evidence_mode") != "observed_source_view" or row.get("inferred_vs_observed") != "observed":
            raise T439PilotError(f"{label}: source tokens must be observed source-view evidence")
        if row.get("trust_zone") != "candidate" or row.get("status") != "candidate":
            raise T439PilotError(f"{label}: source tokens must remain candidate")
        storage = row.get("text_storage_policy")
        if not isinstance(storage, dict) or storage.get("stores_source_text") is not False:
            raise T439PilotError(f"{label}: stores_source_text must be false")
        if not isinstance(row.get("token_text_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", row["token_text_sha256"]):
            raise T439PilotError(f"{label}: token_text_sha256 must be a SHA-256 hex digest")
        position = (ref, int(row.get("verse_token_index", -1)))
        if position in verse_positions:
            raise T439PilotError(f"{label}: duplicate verse token position {position}")
        verse_positions.add(position)
        source_token_id = str(row.get("source_token_id"))
        by_ref[ref].append(source_token_id)
        authority = row.get("authority")
        if not isinstance(authority, dict):
            raise T439PilotError(f"{label}: authority must be a mapping")
        _require_all_authority_false(authority, f"{label}.authority")
    if set(by_ref) != set(TARGET_REFS) or any(not ids for ids in by_ref.values()):
        raise T439PilotError("source token rows must cover all 25 Philemon refs")
    return by_ref


def validate_editorial_layers(rows: list[dict[str, Any]], source_token_ids: set[str]) -> None:
    if len(rows) != EXPECTED_COUNTS["editorial_layers"]:
        raise T439PilotError(f"expected 98 editorial rows, got {len(rows)}")
    ids: set[str] = set()
    kinds: dict[str, int] = {}
    for row in rows:
        label = str(row.get("id", "<missing-editorial-id>"))
        if label in ids:
            raise T439PilotError(f"duplicate editorial row id {label}")
        ids.add(label)
        _reject_text_leak(row, label)
        if row.get("type") != "EditorialLayer":
            raise T439PilotError(f"{label}: type must be EditorialLayer")
        if row.get("observed_value") != "redacted_no_text_value_present":
            raise T439PilotError(f"{label}: observed_value must stay redacted")
        if row.get("is_editorial_not_autograph_certainty") is not True:
            raise T439PilotError(f"{label}: must be editorial-not-autograph certainty")
        for token_id in row.get("applies_to_source_token_ids", []):
            if token_id not in source_token_ids:
                raise T439PilotError(f"{label}: applies to unknown source token {token_id}")
        kinds[str(row.get("layer_kind"))] = kinds.get(str(row.get("layer_kind")), 0) + 1
        authority = row.get("authority")
        if not isinstance(authority, dict):
            raise T439PilotError(f"{label}: authority must be a mapping")
        _require_all_authority_false(authority, f"{label}.authority")
    if kinds.get("paragraphing") != 6 or kinds.get("versification") != 25 or kinds.get("punctuation") != 67:
        raise T439PilotError(f"unexpected editorial layer kind counts: {kinds}")


def validate_alignments(rows: list[dict[str, Any]], by_ref: dict[str, list[str]]) -> None:
    if len(rows) != EXPECTED_COUNTS["alignment_records"]:
        raise T439PilotError(f"expected 25 alignment rows, got {len(rows)}")
    refs = [str(row.get("osis_ref")) for row in rows]
    if refs != TARGET_REFS:
        raise T439PilotError(f"alignment refs must be {TARGET_REFS}, got {refs}")
    seen_web_ids: set[str] = set()
    for row in rows:
        label = str(row.get("id", "<missing-alignment-id>"))
        _reject_text_leak(row, label)
        if row.get("type") != "AlignmentRecord":
            raise T439PilotError(f"{label}: type must be AlignmentRecord")
        if row.get("alignment_type") != "many_to_many":
            raise T439PilotError(f"{label}: alignment_type must remain many_to_many")
        if row.get("alignment_basis") != "source_token_order" or row.get("method") != "source_view_bridge":
            raise T439PilotError(f"{label}: wrong alignment basis/method")
        if row.get("evidence_mode") != "inferred" or row.get("inferred_vs_observed") != "inferred":
            raise T439PilotError(f"{label}: alignments must be inferred bridge evidence")
        if row.get("confidence") != "low" or row.get("review_status") != "unreviewed":
            raise T439PilotError(f"{label}: alignment must stay low-confidence and unreviewed")
        if row.get("translation_strong_hints_are_source_text") is not False:
            raise T439PilotError(f"{label}: WEB Strong's hints must not be source text")
        if row.get("translation_text_stored") is not False:
            raise T439PilotError(f"{label}: translation_text_stored must be false")
        source = row.get("source")
        if not isinstance(source, dict) or source.get("source_id") != "sblgnt":
            raise T439PilotError(f"{label}: source must be sblgnt")
        if source.get("strong") is not None:
            raise T439PilotError(f"{label}: source.strong must be null")
        ref = str(row["osis_ref"])
        if source.get("source_token_ids") != by_ref[ref]:
            raise T439PilotError(f"{label}: source token IDs do not match source-token rows")
        token_ids = row.get("translation_token_ids")
        if not isinstance(token_ids, list) or not token_ids:
            raise T439PilotError(f"{label}: translation token IDs must be non-empty")
        for token_id in token_ids:
            seen_web_ids.add(str(token_id))
        authority = row.get("authority")
        if not isinstance(authority, dict):
            raise T439PilotError(f"{label}: authority must be a mapping")
        _require_all_authority_false(authority, f"{label}.authority")
    expected_web = _web_token_ids()
    if seen_web_ids != expected_web:
        missing = sorted(expected_web - seen_web_ids)[:10]
        extra = sorted(seen_web_ids - expected_web)[:10]
        raise T439PilotError(f"WEB token coverage mismatch: missing={missing}, extra={extra}")


def validate_t439_phlm_alignment_bridge_expansion(root: Path = ROOT) -> dict[str, Any]:
    manifest_path = root / PILOT_ROOT.relative_to(ROOT) / "manifest.yaml"
    tokens_path = root / PILOT_ROOT.relative_to(ROOT) / "source_language_tokens.jsonl"
    editorial_path = root / PILOT_ROOT.relative_to(ROOT) / "editorial_layers.jsonl"
    alignments_path = root / PILOT_ROOT.relative_to(ROOT) / "alignment_records.jsonl"
    for path in (
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
        local = path if path.is_absolute() and str(path).startswith(str(root)) else root / path.relative_to(ROOT)
        if not local.exists():
            raise T439PilotError(f"{_rel(local)} is missing")

    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "t439_phlm_alignment_bridge_expansion":
        raise T439PilotError("T439 control object_type is wrong")
    _require_all_authority_false(control.get("authority", {}), "control.authority")
    if control.get("rust_policy", {}).get("rust_added_in_t439") is not False:
        raise T439PilotError("T439 must not add Rust")

    task = _read_yaml(root / TASK.relative_to(ROOT))
    if task.get("authorization", {}).get("creates_task_scoped_candidate_rows") is not True:
        raise T439PilotError("T439 task must record task-scoped candidate rows")
    if task.get("authorization", {}).get("opens_production_candidate_roots") is not False:
        raise T439PilotError("T439 must not open production candidate roots")

    manifest = _read_yaml(manifest_path)
    if manifest.get("pilot_span") != "Phlm.1.1-Phlm.1.25":
        raise T439PilotError("manifest pilot_span mismatch")
    if manifest.get("exact_refs") != TARGET_REFS:
        raise T439PilotError("manifest exact_refs mismatch")
    if manifest.get("counts") != EXPECTED_COUNTS:
        raise T439PilotError(f"manifest counts mismatch: {manifest.get('counts')} != {EXPECTED_COUNTS}")
    no_text = manifest.get("no_text_policy")
    if not isinstance(no_text, dict) or no_text.get("stores_source_text") is not False or no_text.get("stores_translation_text") is not False:
        raise T439PilotError("manifest no_text_policy must forbid source and translation text storage")
    _require_all_authority_false(manifest.get("authority", {}), "manifest.authority")

    tokens = _read_jsonl(tokens_path)
    editorial = _read_jsonl(editorial_path)
    alignments = _read_jsonl(alignments_path)
    by_ref = validate_source_tokens(tokens)
    source_token_ids = {token_id for token_ids in by_ref.values() for token_id in token_ids}
    validate_editorial_layers(editorial, source_token_ids)
    validate_alignments(alignments, by_ref)
    _validate_schema_records([tokens_path, editorial_path, alignments_path])
    _validate_no_production_outputs(root)

    validate_all_text = (root / VALIDATE_ALL.relative_to(ROOT)).read_text(encoding="utf-8")
    if "validate_t439_phlm_alignment_bridge_expansion.py" not in validate_all_text:
        raise T439PilotError("validate_all.py must run the T439 validator")

    roadmap_text = (root / ROADMAP.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("no-text", "full philemon", "rust", "strong's-as-source-text"):
        if phrase not in roadmap_text:
            raise T439PilotError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")
    dad_text = (root / DAD_PREFLIGHT.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("no-text python pilot fixture", "future rust", "production roots"):
        if phrase not in dad_text:
            raise T439PilotError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t439_phlm_alignment_bridge_expansion(args.root.resolve())
    except T439PilotError as exc:
        print(f"T439 Philemon alignment bridge expansion validation failed: {exc}", file=sys.stderr)
        return 1
    print("T439 Philemon alignment bridge expansion validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
