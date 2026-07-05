#!/usr/bin/env python3
"""Validate the T436 Jonah Hebrew no-text observation/parity pilot."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PILOT_ROOT = (
    ROOT
    / "data"
    / "candidate"
    / "original_language_evidence"
    / "pilots"
    / "T436_jonah_hebrew_observation_parity"
)
CONTROL = ROOT / ".ai" / "control" / "t436_jonah_hebrew_metadata_pilot.yaml"
TASK = ROOT / ".ai" / "tasks" / "T436.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T436" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T436" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T436_JONAH_HEBREW_METADATA_PILOT.md"
BUILD_SCRIPT = ROOT / "scripts" / "build_t436_jonah_hebrew_metadata_pilot.py"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

EXPECTED_SOURCES = {"tanach_us_uxlc", "openscriptures_oshb"}
EXPECTED_VERSES_PER_SOURCE = 48
EXPECTED_TOKENS_PER_SOURCE = 688
EXPECTED_TOKEN_ROWS = 1376
EXPECTED_VERSE_ROWS = 96
EXPECTED_FILE_ROWS = 2
HEBREW_OR_GREEK_RE = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")

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
    "authorizes_word_level_alignment_truth",
    "authorizes_lemma_or_morphology_population",
    "authorizes_strongs_as_source_text",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_manuscript_witness_support",
    "authorizes_canon_scope_change",
    "authorizes_translation_judgment",
    "authorizes_chunk_boundary",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_route_behavior",
    "authorizes_evaluator_behavior",
    "authorizes_graph_edges",
    "authorizes_graph_or_retrieval_truth",
    "authorizes_retrieval_truth",
    "authorizes_embeddings_or_indexes",
    "authorizes_theology_authority",
}

FORBIDDEN_TEXT_KEYS = {
    "surface_text",
    "normalized_text",
    "raw_text",
    "source_text",
    "lemma",
    "lemma_value",
    "morphology",
    "morph",
    "morphology_value",
    "strong_id",
    "strong",
}


class T436PilotError(ValueError):
    """Raised when the T436 pilot is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T436PilotError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T436PilotError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T436PilotError(f"{_rel(path)} unreadable JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise T436PilotError(f"{_rel(path)} must be a JSON object")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        rows = []
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if line.strip():
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise T436PilotError(f"{_rel(path)}:{line_no} must be a JSON object")
                    rows.append(row)
        return rows
    except (OSError, json.JSONDecodeError) as exc:
        raise T436PilotError(f"{_rel(path)} unreadable JSONL: {exc}") from exc


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if key in mapping and mapping.get(key) is not False:
            raise T436PilotError(f"{label}.{key} must be false")


def _require_all_authority_false(row: dict[str, Any], label: str) -> None:
    authority = row.get("authority")
    if not isinstance(authority, dict):
        raise T436PilotError(f"{label}: authority must be a mapping")
    for key, value in authority.items():
        if key.startswith("authorizes_") and value is not False:
            raise T436PilotError(f"{label}.authority.{key} must be false")


def _walk_dict(value: Any, path: str = "$") -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            rows.append((f"{path}.{key}", child))
            rows.extend(_walk_dict(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.append((f"{path}[{index}]", child))
            rows.extend(_walk_dict(child, f"{path}[{index}]"))
    return rows


def _validate_no_text_payload(row: dict[str, Any], label: str) -> None:
    if row.get("stores_source_text") is not False:
        raise T436PilotError(f"{label}: stores_source_text must be false")
    for path, value in _walk_dict(row):
        key = path.rsplit(".", 1)[-1]
        if key in FORBIDDEN_TEXT_KEYS:
            raise T436PilotError(f"{label}: forbidden text/value key {key}")
        if isinstance(value, str) and HEBREW_OR_GREEK_RE.search(value):
            raise T436PilotError(f"{label}: no-text ledgers must not contain Hebrew or Greek characters at {path}")


def validate_file_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) != EXPECTED_FILE_ROWS:
        raise T436PilotError(f"expected {EXPECTED_FILE_ROWS} source-view file rows")
    seen = {str(row.get("source_id")) for row in rows}
    if seen != EXPECTED_SOURCES:
        raise T436PilotError(f"source-view file rows must cover {sorted(EXPECTED_SOURCES)}, got {sorted(seen)}")
    for row in rows:
        label = str(row.get("id", "<missing-file-id>"))
        if row.get("object_type") != "t436_source_view_file_observation":
            raise T436PilotError(f"{label}: wrong object_type")
        if row.get("consumes_raw_archive_directly") is not False:
            raise T436PilotError(f"{label}: must not consume raw archive directly")
        if str(row.get("source_view_path", "")).startswith("data/raw/"):
            raise T436PilotError(f"{label}: source_view_path must use canonical source view, not raw")
        flags = row.get("manifest_flags")
        if not isinstance(flags, dict):
            raise T436PilotError(f"{label}: manifest_flags missing")
        if row.get("source_id") == "tanach_us_uxlc":
            for field in ("contains_source_provided_morphology", "contains_source_provided_lemmas", "contains_source_provided_strongs"):
                if flags.get(field) is not False:
                    raise T436PilotError(f"{label}: UXLC {field} must be false")
        if row.get("source_id") == "openscriptures_oshb":
            if flags.get("contains_source_provided_morphology") is not True:
                raise T436PilotError(f"{label}: OSHB morphology flag must be true")
            if flags.get("contains_source_provided_lemmas") is not False:
                raise T436PilotError(f"{label}: OSHB lemma manifest flag drift expects false before policy fix")
            if flags.get("contains_source_provided_strongs") is not False:
                raise T436PilotError(f"{label}: OSHB Strong's flag must be false")
        _validate_no_text_payload(row, label)
        _require_all_authority_false(row, label)


def validate_token_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) != EXPECTED_TOKEN_ROWS:
        raise T436PilotError(f"expected {EXPECTED_TOKEN_ROWS} token-shape rows")
    by_source: dict[str, list[dict[str, Any]]] = {source: [] for source in EXPECTED_SOURCES}
    ids: set[str] = set()
    for row in rows:
        label = str(row.get("id", "<missing-token-id>"))
        if label in ids:
            raise T436PilotError(f"duplicate token row {label}")
        ids.add(label)
        if row.get("object_type") != "t436_token_shape_observation":
            raise T436PilotError(f"{label}: wrong object_type")
        source_id = str(row.get("source_id"))
        if source_id not in by_source:
            raise T436PilotError(f"{label}: unexpected source {source_id}")
        by_source[source_id].append(row)
        if row.get("book_id") != "Jonah" or row.get("language") != "hebrew":
            raise T436PilotError(f"{label}: wrong book/language")
        if not re.fullmatch(r"[0-9a-f]{64}", str(row.get("token_text_sha256", ""))):
            raise T436PilotError(f"{label}: token_text_sha256 must be sha256")
        if row.get("stores_morphology_value") is not False or row.get("stores_lemma_value") is not False:
            raise T436PilotError(f"{label}: lemma/morphology values must not be stored")
        if row.get("stores_strongs_value") is not False:
            raise T436PilotError(f"{label}: Strong's values must not be stored")
        if source_id == "tanach_us_uxlc":
            if row.get("has_morph_attr") or row.get("has_lemma_attr") or row.get("has_strong_attr"):
                raise T436PilotError(f"{label}: UXLC must not expose lemma/morph/Strong attrs")
            if row.get("attribute_keys") != []:
                raise T436PilotError(f"{label}: UXLC token attribute keys must be empty")
        if source_id == "openscriptures_oshb":
            if row.get("has_morph_attr") is not True:
                raise T436PilotError(f"{label}: OSHB must expose morphology attr presence")
            if row.get("has_lemma_attr") is not True:
                raise T436PilotError(f"{label}: OSHB lemma attr presence must be detected")
            if row.get("has_strong_attr") is not False:
                raise T436PilotError(f"{label}: OSHB must not expose Strong's attrs")
            attr_keys = set(row.get("attribute_keys", []))
            if not {"id", "lemma", "morph"} <= attr_keys:
                raise T436PilotError(f"{label}: OSHB expected id/lemma/morph attribute keys")
        _validate_no_text_payload(row, label)
        _require_all_authority_false(row, label)
    for source_id, source_rows in by_source.items():
        if len(source_rows) != EXPECTED_TOKENS_PER_SOURCE:
            raise T436PilotError(f"{source_id} token rows must be {EXPECTED_TOKENS_PER_SOURCE}")


def validate_verse_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) != EXPECTED_VERSE_ROWS:
        raise T436PilotError(f"expected {EXPECTED_VERSE_ROWS} verse rows")
    by_source: dict[str, dict[str, dict[str, Any]]] = {source: {} for source in EXPECTED_SOURCES}
    for row in rows:
        label = str(row.get("id", "<missing-verse-id>"))
        if row.get("object_type") != "t436_verse_token_observation":
            raise T436PilotError(f"{label}: wrong object_type")
        source_id = str(row.get("source_id"))
        if source_id not in by_source:
            raise T436PilotError(f"{label}: unexpected source {source_id}")
        by_source[source_id][str(row.get("osis_ref"))] = row
        if not isinstance(row.get("source_token_ids"), list) or len(row["source_token_ids"]) != row.get("token_count"):
            raise T436PilotError(f"{label}: source_token_ids must match token_count")
        _validate_no_text_payload(row, label)
        _require_all_authority_false(row, label)
    if set(by_source["tanach_us_uxlc"]) != set(by_source["openscriptures_oshb"]):
        raise T436PilotError("UXLC/OSHB verse refs must match")
    for ref in by_source["tanach_us_uxlc"]:
        if by_source["tanach_us_uxlc"][ref]["token_count"] != by_source["openscriptures_oshb"][ref]["token_count"]:
            raise T436PilotError(f"UXLC/OSHB per-verse token-count drift at {ref}")


def validate_editorial_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) < 10:
        raise T436PilotError("expected editorial/metadata shape rows for both sources")
    by_source_kind = {(str(row.get("source_id")), str(row.get("marker_kind"))) for row in rows}
    required = {
        ("tanach_us_uxlc", "samekh"),
        ("tanach_us_uxlc", "pe"),
        ("tanach_us_uxlc", "vs"),
        ("tanach_us_uxlc", "nested_token_markup"),
        ("openscriptures_oshb", "seg:x-maqqef"),
        ("openscriptures_oshb", "seg:x-sof-pasuq"),
        ("openscriptures_oshb", "morph_attr_presence"),
        ("openscriptures_oshb", "lemma_attr_presence"),
        ("openscriptures_oshb", "strong_attr_presence"),
    }
    missing = required - by_source_kind
    if missing:
        raise T436PilotError(f"missing editorial/metadata markers: {sorted(missing)}")
    for row in rows:
        label = str(row.get("id", "<missing-editorial-id>"))
        if row.get("object_type") != "t436_editorial_metadata_shape_observation":
            raise T436PilotError(f"{label}: wrong object_type")
        if row.get("is_editorial_not_autograph_certainty") is not True:
            raise T436PilotError(f"{label}: must be editorial-not-autograph certainty")
        if row.get("source_id") == "openscriptures_oshb" and row.get("marker_kind") == "strong_attr_presence":
            if row.get("count") != 0:
                raise T436PilotError(f"{label}: OSHB strong_attr_presence must be 0")
        _validate_no_text_payload(row, label)
        _require_all_authority_false(row, label)


def validate_parity_summary(summary: dict[str, Any]) -> None:
    if summary.get("object_type") != "t436_jonah_hebrew_observation_parity_summary":
        raise T436PilotError("parity summary object_type mismatch")
    if summary.get("refs_match") is not True:
        raise T436PilotError("parity summary refs_match must be true")
    if summary.get("per_verse_token_counts_match") is not True:
        raise T436PilotError("parity summary per_verse_token_counts_match must be true")
    counts = summary.get("observed_counts")
    expected = {
        "uxlc_verses": 48,
        "oshb_verses": 48,
        "uxlc_tokens": 688,
        "oshb_tokens": 688,
        "oshb_morph_attr_count": 688,
        "oshb_lemma_attr_count": 688,
        "oshb_strong_attr_count": 0,
    }
    if counts != expected:
        raise T436PilotError(f"parity summary observed_counts mismatch: {counts} != {expected}")
    drift = summary.get("metadata_flag_drift")
    if not isinstance(drift, dict):
        raise T436PilotError("parity summary metadata_flag_drift missing")
    if drift.get("manifest_contains_source_provided_lemmas") is not False:
        raise T436PilotError("OSHB lemma manifest flag must remain false until policy fix")
    if drift.get("observed_lemma_attr_count") != 688:
        raise T436PilotError("OSHB lemma attr count must be 688")
    if drift.get("requires_policy_before_rust_expansion") is not True:
        raise T436PilotError("OSHB lemma drift must block Rust expansion")
    if summary.get("rust_expansion_allowed") is not False:
        raise T436PilotError("T436 must not allow Rust expansion")
    _validate_no_text_payload(summary, "parity_summary")
    _require_all_authority_false(summary, "parity_summary")


def _validate_no_production_outputs(root: Path) -> None:
    for directory in PRODUCTION_ROOTS:
        path = root / directory.relative_to(ROOT)
        if path.exists() and any(path.rglob("*")):
            raise T436PilotError(f"{_rel(path)} must stay empty until a later production-population task")


def _validate_output_files_no_text(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if HEBREW_OR_GREEK_RE.search(text):
            raise T436PilotError(f"{_rel(path)} contains Hebrew/Greek text despite no-text policy")
        for forbidden in ('"surface_text"', '"normalized_text"', '"lemma_value"', '"morphology_value"', '"strong_id"'):
            if forbidden in text:
                raise T436PilotError(f"{_rel(path)} contains forbidden key {forbidden}")


def validate_t436_jonah_hebrew_metadata_pilot(root: Path = ROOT) -> dict[str, Any]:
    pilot_root = root / PILOT_ROOT.relative_to(ROOT)
    manifest_path = pilot_root / "manifest.yaml"
    file_rows_path = pilot_root / "source_view_file_observations.jsonl"
    verse_rows_path = pilot_root / "verse_token_observations.jsonl"
    token_rows_path = pilot_root / "token_shape_index.jsonl"
    editorial_rows_path = pilot_root / "editorial_metadata_shape_index.jsonl"
    parity_path = pilot_root / "parity_summary.json"

    required_paths = (
        CONTROL,
        TASK,
        HANDOFF,
        DAD_PREFLIGHT,
        ROADMAP,
        BUILD_SCRIPT,
        manifest_path,
        file_rows_path,
        verse_rows_path,
        token_rows_path,
        editorial_rows_path,
        parity_path,
    )
    for path in required_paths:
        local = path if path.is_absolute() else root / path.relative_to(ROOT)
        if not local.exists():
            raise T436PilotError(f"{_rel(local)} is missing")

    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "t436_jonah_hebrew_metadata_pilot":
        raise T436PilotError("T436 control object_type is wrong")
    _require_false(control.get("authority", {}), FORBIDDEN_AUTH_TRUE, "control.authority")
    if control.get("rust_policy", {}).get("rust_added_in_t436") is not False:
        raise T436PilotError("T436 rust_policy.rust_added_in_t436 must be false")

    task = _read_yaml(root / TASK.relative_to(ROOT))
    if task.get("mode") != "no_text_observation_parity_pilot_non_authorizing":
        raise T436PilotError("T436 task mode must be no-text observation parity")
    _require_false(task.get("authorization", {}), FORBIDDEN_AUTH_TRUE, "task.authorization")

    manifest = _read_yaml(manifest_path)
    if manifest.get("object_type") != "t436_jonah_hebrew_observation_parity_manifest":
        raise T436PilotError("manifest object_type mismatch")
    if manifest.get("no_text_ledgers") is not True:
        raise T436PilotError("manifest no_text_ledgers must be true")
    if manifest.get("consumes_raw_archives_directly") is not False:
        raise T436PilotError("manifest must not consume raw archives directly")
    _require_false(manifest.get("authority", {}), FORBIDDEN_AUTH_TRUE, "manifest.authority")

    file_rows = _read_jsonl(file_rows_path)
    verse_rows = _read_jsonl(verse_rows_path)
    token_rows = _read_jsonl(token_rows_path)
    editorial_rows = _read_jsonl(editorial_rows_path)
    parity = _read_json(parity_path)

    validate_file_rows(file_rows)
    validate_token_rows(token_rows)
    validate_verse_rows(verse_rows)
    validate_editorial_rows(editorial_rows)
    validate_parity_summary(parity)

    counts = manifest.get("counts")
    expected_counts = {
        "source_view_file_observations": len(file_rows),
        "verse_token_observations": len(verse_rows),
        "token_shape_index": len(token_rows),
        "editorial_metadata_shape_index": len(editorial_rows),
    }
    if counts != expected_counts:
        raise T436PilotError(f"manifest counts mismatch: {counts} != {expected_counts}")

    _validate_output_files_no_text([manifest_path, file_rows_path, verse_rows_path, token_rows_path, editorial_rows_path, parity_path])
    _validate_no_production_outputs(root)

    validate_all_text = (root / VALIDATE_ALL.relative_to(ROOT)).read_text(encoding="utf-8")
    if "validate_t436_jonah_hebrew_metadata_pilot.py" not in validate_all_text:
        raise T436PilotError("validate_all.py must run the T436 validator")
    if "cargo run" in validate_all_text and "scan-uxlc" in validate_all_text:
        raise T436PilotError("validate_all.py must not run a Hebrew Rust scan in T436")

    dad_text = (root / DAD_PREFLIGHT.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("no-text", "oshb", "lemma", "rust"):
        if phrase not in dad_text:
            raise T436PilotError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")

    roadmap_text = (root / ROADMAP.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("no-text", "metadata-flag drift", "rust expansion is blocked", "strong"):
        if phrase not in roadmap_text:
            raise T436PilotError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")

    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t436_jonah_hebrew_metadata_pilot(args.root.resolve())
    except T436PilotError as exc:
        print(f"T436 Jonah Hebrew observation parity validation failed: {exc}", file=sys.stderr)
        return 1
    print("T436 Jonah Hebrew observation parity validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
