#!/usr/bin/env python3
"""Validate the T441 Rust no-text alignment coverage/index contract and generated ledgers."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "t441_rust_alignment_coverage_index.yaml"
TASK = ROOT / ".ai" / "tasks" / "T441.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T441" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T441" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T441_RUST_ALIGNMENT_COVERAGE_INDEX.md"
SUBSTRATE = ROOT / ".ai" / "control" / "original_language_evidence_substrate.yaml"
RUST_BIN = ROOT / "tools" / "original_language_observation_scanner" / "src" / "bin" / "t441_alignment_coverage.rs"
CARGO = ROOT / "tools" / "original_language_observation_scanner" / "Cargo.toml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
T439_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "pilots" / "T439_phlm_alignment_bridge_expansion"
T436_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "pilots" / "T436_jonah_hebrew_observation_parity"
T440_CONTROL = ROOT / ".ai" / "control" / "t440_jonah_hebrew_parser_contract.yaml"

EXPECTED_OUTPUT_FILES = {
    "coverage_manifest.json",
    "source_ref_coverage.jsonl",
    "alignment_coverage_index.jsonl",
    "semantic_guardrail_index.jsonl",
    "negative_fixture_summary.json",
}
EXPECTED_NEGATIVE_FIXTURES = {
    "reject_raw_archive_direct_consumption",
    "reject_visible_hebrew_text_storage",
    "reject_oshb_lemma_as_local_lemma",
    "reject_oshb_morph_as_local_morphology_row",
    "reject_strong_population_from_oshb_lemma",
    "reject_metadata_value_hash_as_value_authority",
    "reject_count_match_as_semantic_parity",
    "reject_production_root_opening",
    "reject_preferred_reading_or_source_tradition",
}
FORBIDDEN_ROW_KEYS = {
    "surface_text",
    "normalized_text",
    "source_text",
    "translation_text",
    "visible_text",
    "full_text",
    "manuscript_text",
    "manuscript_transcription",
    "lemma_value_hash",
    "morph_value_hash",
    "morphology_value_hash",
    "strong_value_hash",
    "strongs_value_hash",
}
FORBIDDEN_AUTH_TRUE_PREFIXES = ("authorizes_", "creates_", "changes_", "runs_", "selects_", "opens_")
ALLOWED_AUTH_TRUE = {
    "records_rust_alignment_coverage_index",
    "records_python_validation_contract",
    "records_t439_t440_shadow_coverage_gate",
}
GREEK_HEBREW_RE = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff]")
PRODUCTION_ROOTS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)


class T441ValidationError(ValueError):
    """Raised when T441 scanner artifacts violate the contract."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T441ValidationError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T441ValidationError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T441ValidationError(f"{_rel(path)} unreadable JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise T441ValidationError(f"{_rel(path)} must be a JSON object")
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
                    raise T441ValidationError(f"{_rel(path)}:{line_no} must be a JSON object")
                rows.append(row)
    except (OSError, json.JSONDecodeError) as exc:
        raise T441ValidationError(f"{_rel(path)} unreadable JSONL: {exc}") from exc
    return rows


def _walk(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        found.append(value)
        for child in value.values():
            found.extend(_walk(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_walk(child))
    return found


def _reject_text_leak(row: dict[str, Any], label: str) -> None:
    for mapping in _walk(row):
        for key, value in mapping.items():
            if key in FORBIDDEN_ROW_KEYS:
                raise T441ValidationError(f"{label}: forbidden text/metadata key {key!r}")
            if isinstance(value, str) and GREEK_HEBREW_RE.search(value):
                raise T441ValidationError(f"{label}.{key} appears to leak Greek/Hebrew text")


def _require_authority_false(row: dict[str, Any], label: str) -> None:
    authority = row.get("authority")
    if not isinstance(authority, dict):
        raise T441ValidationError(f"{label}: authority must be a mapping")
    for key, value in authority.items():
        if key in ALLOWED_AUTH_TRUE:
            continue
        if key.startswith(FORBIDDEN_AUTH_TRUE_PREFIXES) and value is not False:
            raise T441ValidationError(f"{label}.authority.{key} must be false")


def _require_no_text_policy(row: dict[str, Any], label: str) -> None:
    policy = row.get("text_storage_policy")
    if not isinstance(policy, dict):
        raise T441ValidationError(f"{label}: text_storage_policy must be present")
    for key in ("stores_source_text", "stores_translation_text", "stores_manuscript_transcription", "stores_manuscript_image"):
        if policy.get(key) is not False:
            raise T441ValidationError(f"{label}: text_storage_policy.{key} must be false")
    if policy.get("no_text") is not True:
        raise T441ValidationError(f"{label}: text_storage_policy.no_text must be true")


def _require_common_row(row: dict[str, Any], label: str) -> None:
    _reject_text_leak(row, label)
    _require_authority_false(row, label)
    _require_no_text_policy(row, label)
    if row.get("task_id") != "T441":
        raise T441ValidationError(f"{label}: task_id must be T441")
    if row.get("trust_zone") != "candidate" or row.get("status") != "coverage_shadow":
        raise T441ValidationError(f"{label}: must remain candidate coverage_shadow")


def _require_false(mapping: dict[str, Any], label: str) -> None:
    for key, value in mapping.items():
        if key in ALLOWED_AUTH_TRUE:
            continue
        if key.startswith(FORBIDDEN_AUTH_TRUE_PREFIXES) and value is not False:
            raise T441ValidationError(f"{label}.{key} must be false")


def _validate_no_production_outputs(root: Path = ROOT) -> None:
    for directory in PRODUCTION_ROOTS:
        path = root / directory.relative_to(ROOT)
        if path.exists() and any(path.rglob("*")):
            raise T441ValidationError(f"{_rel(path)} must stay empty until a later production-population task")


def validate_generated(input_dir: Path) -> dict[str, Any]:
    if not input_dir.exists():
        raise T441ValidationError(f"{_rel(input_dir)} is missing")
    files = {path.name for path in input_dir.iterdir() if path.is_file()}
    missing = EXPECTED_OUTPUT_FILES - files
    if missing:
        raise T441ValidationError(f"{_rel(input_dir)} missing output files: {sorted(missing)}")
    try:
        rel = input_dir.resolve().relative_to(ROOT)
    except ValueError:
        rel = None
    if rel is not None and not rel.as_posix().startswith("build/original_language_observation/T441/"):
        raise T441ValidationError("generated T441 outputs must stay under build/original_language_observation/T441/")

    manifest = _read_json(input_dir / "coverage_manifest.json")
    if manifest.get("object_type") != "t441_rust_alignment_coverage_manifest":
        raise T441ValidationError("coverage_manifest object_type mismatch")
    _require_common_row(manifest, "coverage_manifest")
    if manifest.get("no_authority") is not True or manifest.get("no_text") is not True:
        raise T441ValidationError("coverage_manifest must record no_authority and no_text")
    if set(manifest.get("output_files", [])) != EXPECTED_OUTPUT_FILES:
        raise T441ValidationError("coverage_manifest output_files mismatch")
    if manifest.get("evidence_mode") != "deterministic_no_text_coverage_index":
        raise T441ValidationError("coverage_manifest evidence_mode mismatch")
    scope = manifest.get("coverage_scope")
    if not isinstance(scope, dict):
        raise T441ValidationError("coverage_manifest.coverage_scope missing")
    expected_scope = {
        "philemon_refs": 25,
        "philemon_source_tokens": 334,
        "philemon_alignment_records": 25,
        "philemon_editorial_layers": 98,
        "jonah_refs_per_source": 48,
        "jonah_tokens_all_sources": 1376,
        "count_parity_is_semantic_authority": False,
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            raise T441ValidationError(f"coverage_manifest.coverage_scope.{key} drifted")
    if scope.get("jonah_sources") != ["openscriptures_oshb", "tanach_us_uxlc"]:
        raise T441ValidationError("coverage_manifest Jonah sources/order drifted")

    source_rows = _read_jsonl(input_dir / "source_ref_coverage.jsonl")
    coverage_rows = _read_jsonl(input_dir / "alignment_coverage_index.jsonl")
    guardrail_rows = _read_jsonl(input_dir / "semantic_guardrail_index.jsonl")
    negative = _read_json(input_dir / "negative_fixture_summary.json")
    counts = {
        "source_ref_coverage": len(source_rows),
        "alignment_coverage_index": len(coverage_rows),
        "semantic_guardrail_index": len(guardrail_rows),
        "negative_fixture_summary": negative.get("negative_fixture_count"),
    }
    if manifest.get("row_counts") != counts:
        raise T441ValidationError(f"manifest row_counts mismatch: {manifest.get('row_counts')} != {counts}")

    validate_source_rows(source_rows)
    validate_coverage_rows(coverage_rows)
    validate_guardrail_rows(guardrail_rows)
    validate_negative_summary(negative)
    return manifest


def validate_source_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) != 3:
        raise T441ValidationError(f"expected 3 source coverage rows, got {len(rows)}")
    by_source = {str(row.get("source_id")): row for row in rows}
    if set(by_source) != {"sblgnt", "openscriptures_oshb", "tanach_us_uxlc"}:
        raise T441ValidationError(f"source coverage rows have wrong sources: {sorted(by_source)}")
    for row in rows:
        _require_common_row(row, f"source_ref_coverage:{row.get('id')}")
        if row.get("type") != "T441SourceRefCoverage":
            raise T441ValidationError("source_ref_coverage row type mismatch")
        if str(row.get("source_view_path", "")).startswith("data/raw/"):
            raise T441ValidationError("T441 source coverage must not consume raw archives directly")
    phlm = by_source["sblgnt"]
    if phlm.get("ref_count") != 25 or phlm.get("source_token_count") != 334 or phlm.get("alignment_record_count") != 25:
        raise T441ValidationError("Philemon source coverage counts drifted")
    oshb = by_source["openscriptures_oshb"]
    if oshb.get("ref_count") != 48 or oshb.get("source_token_count") != 688:
        raise T441ValidationError("OSHB Jonah coverage counts drifted")
    if oshb.get("lemma_attr_count") != 688 or oshb.get("morph_attr_count") != 688 or oshb.get("strong_attr_count") != 0:
        raise T441ValidationError("OSHB lemma/morph/Strong attribute coverage drifted")
    uxlc = by_source["tanach_us_uxlc"]
    if uxlc.get("ref_count") != 48 or uxlc.get("source_token_count") != 688:
        raise T441ValidationError("UXLC Jonah coverage counts drifted")
    if uxlc.get("lemma_attr_count") != 0 or uxlc.get("morph_attr_count") != 0 or uxlc.get("strong_attr_count") != 0:
        raise T441ValidationError("UXLC must stay no lemma/morph/Strong")


def validate_coverage_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) != 121:
        raise T441ValidationError(f"expected 121 coverage rows, got {len(rows)}")
    ids: set[str] = set()
    phlm_refs: list[str] = []
    jonah_sources: dict[str, int] = {"openscriptures_oshb": 0, "tanach_us_uxlc": 0}
    for row in rows:
        label = f"alignment_coverage_index:{row.get('id')}"
        _require_common_row(row, label)
        if row.get("type") != "T441AlignmentCoverageObservation":
            raise T441ValidationError(f"{label}: wrong type")
        row_id = str(row.get("id"))
        if row_id in ids:
            raise T441ValidationError(f"duplicate coverage row id {row_id}")
        ids.add(row_id)
        if row.get("word_level_alignment_truth") is not False or row.get("translation_judgment") is not False:
            raise T441ValidationError(f"{label}: semantic truth flags must stay false")
        source = str(row.get("source_id"))
        if row.get("book_id") == "Phlm":
            if row.get("confidence") != "low" or row.get("review_status") != "unreviewed":
                raise T441ValidationError(f"{label}: Philemon coverage must stay low/unreviewed")
            if row.get("translation_side_strong_hints_are_source_text") is not False:
                raise T441ValidationError(f"{label}: translation Strong hints must not be source text")
            phlm_refs.append(str(row.get("osis_ref")))
        elif row.get("book_id") == "Jonah":
            if row.get("count_parity_is_semantic_authority") is not False:
                raise T441ValidationError(f"{label}: count parity must not be semantic authority")
            if row.get("preferred_source_tradition") is not False:
                raise T441ValidationError(f"{label}: preferred_source_tradition must be false")
            if source not in jonah_sources:
                raise T441ValidationError(f"{label}: unexpected Jonah source {source}")
            jonah_sources[source] += 1
        else:
            raise T441ValidationError(f"{label}: unexpected book {row.get('book_id')}")
    expected_phlm = [f"Phlm.1.{index}" for index in range(1, 26)]
    if phlm_refs != expected_phlm:
        raise T441ValidationError("Philemon alignment coverage refs/order drifted")
    if jonah_sources != {"openscriptures_oshb": 48, "tanach_us_uxlc": 48}:
        raise T441ValidationError(f"Jonah coverage row counts drifted: {jonah_sources}")


def validate_guardrail_rows(rows: list[dict[str, Any]]) -> None:
    expected = {
        "no_visible_biblical_text",
        "generated_build_outputs_only",
        "python_authority_validator",
        "t439_bridge_low_confidence",
        "count_parity_not_semantic_parity",
        "oshb_lemma_lookup_hint_only",
        "oshb_morph_metadata_only",
        "no_production_roots_opened",
        "t440_negative_fixtures_carried_forward",
    }
    seen = set()
    for row in rows:
        _require_common_row(row, f"semantic_guardrail_index:{row.get('id')}")
        if row.get("type") != "T441SemanticGuardrail":
            raise T441ValidationError("semantic guardrail row type mismatch")
        seen.add(str(row.get("guardrail_id")))
    if seen != expected:
        raise T441ValidationError(f"semantic guardrails drifted: {sorted(seen)}")


def validate_negative_summary(row: dict[str, Any]) -> None:
    _require_authority_false(row, "negative_fixture_summary")
    _require_no_text_policy(row, "negative_fixture_summary")
    _reject_text_leak(row, "negative_fixture_summary")
    if set(row.get("negative_fixture_ids", [])) != EXPECTED_NEGATIVE_FIXTURES:
        raise T441ValidationError("negative fixture ids drifted")
    if row.get("negative_fixture_count") != len(EXPECTED_NEGATIVE_FIXTURES):
        raise T441ValidationError("negative fixture count drifted")


def validate_contract() -> None:
    required = (
        CONTROL,
        TASK,
        HANDOFF,
        DAD_PREFLIGHT,
        ROADMAP,
        SUBSTRATE,
        RUST_BIN,
        CARGO,
        T439_ROOT / "manifest.yaml",
        T436_ROOT / "manifest.yaml",
        T436_ROOT / "parity_summary.json",
        T440_CONTROL,
    )
    for path in required:
        if not path.exists():
            raise T441ValidationError(f"{_rel(path)} is missing")

    control = _read_yaml(CONTROL)
    if control.get("object_type") != "t441_rust_alignment_coverage_index":
        raise T441ValidationError("T441 control object_type mismatch")
    if control.get("task_id") != "T441":
        raise T441ValidationError("T441 control task_id mismatch")
    _require_false(control.get("authority", {}), "control.authority")
    if control.get("authority", {}).get("records_rust_alignment_coverage_index") is not True:
        raise T441ValidationError("T441 control must record Rust alignment coverage index")
    scope = control.get("scanner_scope")
    if not isinstance(scope, dict):
        raise T441ValidationError("T441 scanner_scope missing")
    if scope.get("writes_generated_build_outputs_only") is not True:
        raise T441ValidationError("T441 must write generated build outputs only")
    if scope.get("opens_production_candidate_roots") is not False:
        raise T441ValidationError("T441 must not open production candidate roots")

    task = _read_yaml(TASK)
    if task.get("id") != "T441" or task.get("mode") != "rust_no_text_coverage_index_non_authorizing":
        raise T441ValidationError("T441 task id/mode mismatch")
    _require_false(task.get("authorization", {}), "task.authorization")
    allowed_paths = "\n".join(task.get("scope", {}).get("allowed_paths", []))
    for required_path in (
        "tools/original_language_observation_scanner/src/bin/t441_alignment_coverage.rs",
        "scripts/validate_t441_rust_alignment_coverage_index.py",
        "tests/test_t441_rust_alignment_coverage_index.py",
        ".digital-asset/mail/outbox.jsonl",
    ):
        if required_path not in allowed_paths:
            raise T441ValidationError(f"T441 task allowed_paths missing {required_path}")

    cargo_text = CARGO.read_text(encoding="utf-8")
    for dep in ("serde_json", "serde_yaml"):
        if dep not in cargo_text:
            raise T441ValidationError(f"Cargo.toml missing dependency {dep}")
    rust_text = RUST_BIN.read_text(encoding="utf-8")
    for phrase in ("--no-authority", "--no-text", "count_parity_is_semantic_authority", "lemma_value_hash"):
        if phrase not in rust_text:
            raise T441ValidationError(f"T441 Rust binary missing guardrail phrase {phrase!r}")

    validate_all_text = VALIDATE_ALL.read_text(encoding="utf-8")
    if "validate_t441_rust_alignment_coverage_index.py" not in validate_all_text:
        raise T441ValidationError("validate_all.py must run T441 contract validator")
    if "cargo run" in validate_all_text and "t441_alignment_coverage" in validate_all_text:
        raise T441ValidationError("validate_all.py must not run the T441 Rust generated scan")

    substrate = _read_yaml(SUBSTRATE)
    lanes = substrate.get("pilot_lanes")
    if not isinstance(lanes, list) or not any(isinstance(lane, dict) and lane.get("task_id") == "T441" for lane in lanes):
        raise T441ValidationError("original_language_evidence_substrate must include T441 lane")

    roadmap_text = ROADMAP.read_text(encoding="utf-8").lower()
    for phrase in ("no-text", "coverage ledger", "not a retrieval index", "count parity is not semantic authority"):
        if phrase not in roadmap_text:
            raise T441ValidationError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")
    dad_text = DAD_PREFLIGHT.read_text(encoding="utf-8").lower()
    for phrase in ("dad", "rust", "python remains the authority validator", "count parity is coverage evidence only"):
        if phrase not in dad_text:
            raise T441ValidationError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")
    _validate_no_production_outputs()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=None, help="Generated T441 build output directory to validate.")
    args = parser.parse_args(argv)
    try:
        validate_contract()
        if args.input is not None:
            validate_generated(args.input.resolve())
    except T441ValidationError as exc:
        print(f"T441 Rust alignment coverage validation failed: {exc}", file=sys.stderr)
        return 1
    print("T441 Rust alignment coverage validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
