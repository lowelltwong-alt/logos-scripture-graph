#!/usr/bin/env python3
"""Validate the T440 Jonah Hebrew source-specific parser contract."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "t440_jonah_hebrew_parser_contract.yaml"
TASK = ROOT / ".ai" / "tasks" / "T440.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T440" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T440" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T440_JONAH_HEBREW_PARSER_CONTRACT.md"
SUBSTRATE = ROOT / ".ai" / "control" / "original_language_evidence_substrate.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
T436_MANIFEST = ROOT / "data" / "candidate" / "original_language_evidence" / "pilots" / "T436_jonah_hebrew_observation_parity" / "manifest.yaml"
T436_PARITY = ROOT / "data" / "candidate" / "original_language_evidence" / "pilots" / "T436_jonah_hebrew_observation_parity" / "parity_summary.json"
T437_POLICY = ROOT / ".ai" / "control" / "t437_oshb_lemma_attribute_policy.yaml"

EXPECTED_SOURCES = {"tanach_us_uxlc", "openscriptures_oshb"}
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
EXPECTED_MARKERS = {
    "tanach_us_uxlc": {
        "chaptering",
        "correction",
        "nested_token_markup",
        "note",
        "pe",
        "samekh",
        "versification",
        "vowel_or_accent_presence",
        "vs",
    },
    "openscriptures_oshb": {
        "chaptering",
        "lemma_attr_presence",
        "morph_attr_presence",
        "seg:x-maqqef",
        "seg:x-pe",
        "seg:x-paseq",
        "seg:x-reversednun",
        "seg:x-samekh",
        "seg:x-sof-pasuq",
        "strong_attr_presence",
        "versification",
        "vowel_or_accent_presence",
    },
}
HEBREW_OR_GREEK_RE = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")
FORBIDDEN_METADATA_VALUE_KEYS = {
    "lemma_value_hash",
    "morph_value_hash",
    "morphology_value_hash",
    "strong_value_hash",
    "strongs_value_hash",
}

PRODUCTION_ROOTS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)

FORBIDDEN_AUTH_TRUE = {
    "opens_production_candidate_roots",
    "creates_source_token_rows",
    "creates_alignment_rows",
    "creates_strongs_overlay_rows",
    "creates_lexeme_or_morphology_rows",
    "creates_textual_variant_rows",
    "creates_witness_support_rows",
    "stores_visible_source_text",
    "stores_visible_translation_text",
    "selects_preferred_reading",
    "selects_source_tradition",
    "changes_canon_scope",
    "creates_translation_faithfulness_judgment",
    "authorizes_source_language_truth",
    "authorizes_lexical_truth",
    "authorizes_word_level_alignment_truth",
    "authorizes_strongs_as_source_text",
    "authorizes_lemma_or_morphology_population",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_manuscript_witness_support",
    "authorizes_canon_scope_change",
    "authorizes_translation_judgment",
    "authorizes_chunk_boundary",
    "creates_reviewed_gold",
    "creates_chunk_output",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "authorizes_theology_authority",
}


class T440ParserContractError(ValueError):
    """Raised when the T440 parser contract is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T440ParserContractError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T440ParserContractError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T440ParserContractError(f"{_rel(path)} unreadable JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise T440ParserContractError(f"{_rel(path)} must be a JSON object")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if line.strip():
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise T440ParserContractError(f"{_rel(path)}:{line_no} must be a JSON object")
                    rows.append(row)
    except (OSError, json.JSONDecodeError) as exc:
        raise T440ParserContractError(f"{_rel(path)} unreadable JSONL: {exc}") from exc
    return rows


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if key in mapping and mapping.get(key) is not False:
            raise T440ParserContractError(f"{label}.{key} must be false")


def _reject_visible_biblical_text(mapping: Any, label: str) -> None:
    if isinstance(mapping, dict):
        for key, value in mapping.items():
            if key in FORBIDDEN_METADATA_VALUE_KEYS:
                raise T440ParserContractError(f"{label}.{key} is a forbidden metadata-value authority key")
            if isinstance(value, str) and HEBREW_OR_GREEK_RE.search(value):
                raise T440ParserContractError(f"{label}.{key} contains visible Greek/Hebrew text")
            _reject_visible_biblical_text(value, f"{label}.{key}")
    elif isinstance(mapping, list):
        for index, value in enumerate(mapping):
            _reject_visible_biblical_text(value, f"{label}[{index}]")


def _included_row(path: Path, view_path: str) -> dict[str, Any]:
    rows = [row for row in _read_jsonl(path) if row.get("view_path") == view_path]
    if len(rows) != 1:
        raise T440ParserContractError(f"{_rel(path)} must contain exactly one included row for {view_path}")
    return rows[0]


def _validate_t436_inputs(control: dict[str, Any]) -> None:
    manifest = _read_yaml(T436_MANIFEST)
    parity = _read_json(T436_PARITY)

    if manifest.get("task_id") != "T436" or manifest.get("no_text_ledgers") is not True:
        raise T440ParserContractError("T436 manifest must be a no-text T436 manifest")
    if manifest.get("consumes_raw_archives_directly") is not False:
        raise T440ParserContractError("T436 manifest must not consume raw archives directly")
    counts = manifest.get("counts")
    if not isinstance(counts, dict) or counts.get("token_shape_index") != 1376:
        raise T440ParserContractError("T436 manifest token_shape_index count must remain 1376")

    expected_counts = parity.get("expected_counts")
    observed_counts = parity.get("observed_counts")
    if expected_counts != {"chapters": 4, "tokens_per_source": 688, "verses_per_source": 48}:
        raise T440ParserContractError("T436 expected_counts drifted")
    if not isinstance(observed_counts, dict):
        raise T440ParserContractError("T436 observed_counts missing")
    for key in ("uxlc_verses", "oshb_verses"):
        if observed_counts.get(key) != 48:
            raise T440ParserContractError(f"T436 observed_counts.{key} must be 48")
    for key in ("uxlc_tokens", "oshb_tokens"):
        if observed_counts.get(key) != 688:
            raise T440ParserContractError(f"T436 observed_counts.{key} must be 688")
    if parity.get("refs_match") is not True or parity.get("per_verse_token_counts_match") is not True:
        raise T440ParserContractError("T436 ref/token parity must remain true")
    if parity.get("exact_token_hashes_all_match") is not False:
        raise T440ParserContractError("T436 exact token hashes must remain recorded as non-matching")
    if parity.get("rust_expansion_allowed") is not False:
        raise T440ParserContractError("T436 still must not allow Rust expansion")

    parity_req = control.get("parity_requirements")
    if not isinstance(parity_req, dict):
        raise T440ParserContractError("T440 parity_requirements missing")
    for key in ("refs_match", "per_verse_token_counts_match"):
        if parity_req.get(key) is not True:
            raise T440ParserContractError(f"T440 parity_requirements.{key} must be true")
    if parity_req.get("exact_token_hashes_all_match") is not False:
        raise T440ParserContractError("T440 must preserve exact_token_hashes_all_match=false")
    if parity_req.get("t436_rust_expansion_allowed_must_remain") is not False:
        raise T440ParserContractError("T440 must keep T436 rust expansion false")


def validate_source_contracts(control: dict[str, Any], root: Path = ROOT) -> dict[str, dict[str, Any]]:
    contracts = control.get("parser_contracts")
    if not isinstance(contracts, list) or len(contracts) != 2:
        raise T440ParserContractError("T440 must define exactly two parser contracts")
    by_source = {str(contract.get("source_id")): contract for contract in contracts}
    if set(by_source) != EXPECTED_SOURCES:
        raise T440ParserContractError(f"T440 parser contracts must cover {sorted(EXPECTED_SOURCES)}")

    parity = _read_json(root / T436_PARITY.relative_to(ROOT))
    checksums = parity.get("source_view_checksums")
    if not isinstance(checksums, dict):
        raise T440ParserContractError("T436 parity source_view_checksums missing")

    for source_id, contract in by_source.items():
        label = f"parser_contracts.{source_id}"
        if contract.get("consumes_raw_archives_directly") is not False:
            raise T440ParserContractError(f"{label}.consumes_raw_archives_directly must be false")
        if contract.get("stores_visible_source_text") is not False:
            raise T440ParserContractError(f"{label}.stores_visible_source_text must be false")

        source_view_path = str(contract.get("source_view_path", ""))
        if not source_view_path.startswith("data/candidate/original_language_evidence/canonical_source_views/"):
            raise T440ParserContractError(f"{label}.source_view_path must consume canonical source views only")
        if source_view_path.startswith("data/raw/"):
            raise T440ParserContractError(f"{label}.source_view_path must not use raw archives")
        local_view = root / source_view_path
        if not local_view.exists():
            raise T440ParserContractError(f"{label}.source_view_path missing: {source_view_path}")

        source_manifest_path = root / str(contract.get("source_manifest", ""))
        manifest_path = root / str(contract.get("canonical_source_view_manifest", ""))
        included_path = root / str(contract.get("included_files_ledger", ""))
        source_manifest = _read_yaml(source_manifest_path)
        manifest = _read_yaml(manifest_path)
        included = _included_row(included_path, source_view_path)
        if str(contract.get("source_view_sha256")) != str(checksums.get(source_id)):
            raise T440ParserContractError(f"{label}.source_view_sha256 must match T436 parity summary")
        if included.get("sha256") != contract.get("source_view_sha256"):
            raise T440ParserContractError(f"{label}.source_view_sha256 must match included-files ledger")
        if included.get("source_archive_path") != contract.get("source_archive_path"):
            raise T440ParserContractError(f"{label}.source_archive_path must match included-files ledger")
        if manifest.get("source_id") != source_id:
            raise T440ParserContractError(f"{label} manifest source_id mismatch")
        if source_manifest.get("id") != source_id:
            raise T440ParserContractError(f"{label} source manifest id mismatch")
        if source_manifest.get("license") != contract.get("license"):
            raise T440ParserContractError(f"{label}.license must match source manifest")

        counts = contract.get("expected_counts")
        if not isinstance(counts, dict):
            raise T440ParserContractError(f"{label}.expected_counts missing")
        for key, expected in {"chapters": 4, "verses": 48, "tokens": 688}.items():
            if counts.get(key) != expected:
                raise T440ParserContractError(f"{label}.expected_counts.{key} must be {expected}")

        token_semantics = contract.get("token_attribute_semantics")
        if not isinstance(token_semantics, dict):
            raise T440ParserContractError(f"{label}.token_attribute_semantics missing")
        for field in (
            "local_lemma_population_allowed",
            "local_morphology_population_allowed",
            "local_strongs_population_allowed",
        ):
            if token_semantics.get(field) is not False:
                raise T440ParserContractError(f"{label}.token_attribute_semantics.{field} must be false")

        markers = set(contract.get("editorial_metadata_semantics", {}).get("observed_marker_kinds", []))
        if markers != EXPECTED_MARKERS[source_id]:
            raise T440ParserContractError(f"{label}.editorial markers drifted")
        if contract.get("editorial_metadata_semantics", {}).get("editorial_not_autograph_certainty") is not True:
            raise T440ParserContractError(f"{label}.editorial_not_autograph_certainty must be true")

        if source_id == "tanach_us_uxlc":
            if contract.get("parser_profile") != "uxlc_tanach_xml":
                raise T440ParserContractError("UXLC parser_profile mismatch")
            if token_semantics.get("allowed_source_attribute_keys") != []:
                raise T440ParserContractError("UXLC must not allow token attributes")
            for key in ("morph_attr_count", "lemma_attr_count", "strong_attr_count"):
                if counts.get(key) != 0:
                    raise T440ParserContractError(f"UXLC expected_counts.{key} must be 0")
            for key in (
                "contains_source_provided_morphology",
                "contains_source_provided_lemmas",
                "contains_source_provided_lemma_attributes",
                "contains_source_provided_strong_lookup_hints",
                "contains_source_provided_strongs",
            ):
                if token_semantics.get(key) is not False:
                    raise T440ParserContractError(f"UXLC {key} must be false")
                if manifest.get(key) is not False:
                    raise T440ParserContractError(f"UXLC manifest {key} must be false")

        if source_id == "openscriptures_oshb":
            if contract.get("parser_profile") != "oshb_osis_xml":
                raise T440ParserContractError("OSHB parser_profile mismatch")
            if set(token_semantics.get("allowed_source_attribute_keys", [])) != {"id", "lemma", "morph"}:
                raise T440ParserContractError("OSHB allowed_source_attribute_keys must be id/lemma/morph")
            if counts.get("morph_attr_count") != 688:
                raise T440ParserContractError("OSHB expected_counts.morph_attr_count must be 688")
            if counts.get("lemma_attr_count") != 688:
                raise T440ParserContractError("OSHB expected_counts.lemma_attr_count must be 688")
            if counts.get("strong_attr_count") != 0:
                raise T440ParserContractError("OSHB expected_counts.strong_attr_count must be 0")
            expected_policy = {
                "contains_source_provided_morphology": True,
                "contains_source_provided_lemmas": False,
                "contains_source_provided_lemma_attributes": True,
                "contains_source_provided_strong_lookup_hints": True,
                "contains_source_provided_strongs": False,
                "lemma_attribute_interpretation": "strong_lookup_hint",
                "lemma_attribute_authority": "metadata_only_not_local_lemma_or_strong_authority",
            }
            for key, expected in expected_policy.items():
                if token_semantics.get(key) != expected:
                    raise T440ParserContractError(f"OSHB token semantics {key} must be {expected!r}")
                if manifest.get(key) != expected:
                    raise T440ParserContractError(f"OSHB manifest {key} must be {expected!r}")
            if token_semantics.get("morph_attribute_authority") != "source_morphology_metadata_not_local_morphology_row_authority":
                raise T440ParserContractError("OSHB morph_attribute_authority mismatch")

        _reject_visible_biblical_text(contract, label)
    return by_source


def validate_negative_fixture_requirements(control: dict[str, Any]) -> None:
    rows = control.get("negative_fixture_requirements")
    if not isinstance(rows, list):
        raise T440ParserContractError("negative_fixture_requirements must be a list")
    seen = {str(row.get("id")) for row in rows if isinstance(row, dict)}
    missing = EXPECTED_NEGATIVE_FIXTURES - seen
    if missing:
        raise T440ParserContractError(f"missing negative fixture requirements: {sorted(missing)}")
    for row in rows:
        if not isinstance(row, dict) or not str(row.get("must_fail_if", "")).strip():
            raise T440ParserContractError("each negative fixture requirement needs must_fail_if")


def validate_rust_policy(control: dict[str, Any]) -> None:
    rust = control.get("rust_policy")
    if not isinstance(rust, dict):
        raise T440ParserContractError("rust_policy missing")
    expected = {
        "rust_added_in_t440": False,
        "source_specific_parser_contracts_defined": True,
        "negative_fixture_expectations_defined": True,
        "t441_may_design_no_text_rust_checker_after_t440": True,
        "t441_requires_separate_task_and_pr": True,
        "rust_scanner_allowed_inside_t440": False,
    }
    for key, value in expected.items():
        if rust.get(key) != value:
            raise T440ParserContractError(f"rust_policy.{key} must be {value!r}")


def _validate_no_production_outputs(root: Path) -> None:
    for directory in PRODUCTION_ROOTS:
        path = root / directory.relative_to(ROOT)
        if path.exists() and any(path.rglob("*")):
            raise T440ParserContractError(f"{_rel(path)} must stay empty until a later production-population task")


def validate_t440_jonah_hebrew_parser_contract(root: Path = ROOT) -> dict[str, Any]:
    required = (CONTROL, TASK, HANDOFF, DAD_PREFLIGHT, ROADMAP, SUBSTRATE, T436_MANIFEST, T436_PARITY, T437_POLICY)
    for path in required:
        local = root / path.relative_to(ROOT)
        if not local.exists():
            raise T440ParserContractError(f"{_rel(local)} is missing")

    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "t440_jonah_hebrew_parser_contract":
        raise T440ParserContractError("T440 control object_type is wrong")
    if control.get("schema_version") != "t440_jonah_hebrew_parser_contract.v1":
        raise T440ParserContractError("T440 schema_version is wrong")
    if control.get("task_id") != "T440":
        raise T440ParserContractError("T440 task_id is wrong")
    _require_false(control.get("authority", {}), FORBIDDEN_AUTH_TRUE, "control.authority")
    if control.get("authority", {}).get("records_source_specific_parser_contract") is not True:
        raise T440ParserContractError("T440 must record source-specific parser contract")
    if control.get("authority", {}).get("authorizes_t441_design") is not True:
        raise T440ParserContractError("T440 should authorize only T441 design")

    span = control.get("span")
    required_span = {
        "book_id": "Jonah",
        "start_osis_ref": "Jonah.1.1",
        "end_osis_ref": "Jonah.4.11",
        "expected_chapters": 4,
        "expected_verses_per_source": 48,
        "expected_tokens_per_source": 688,
        "spotlight_refs": ["Jonah.1.1", "Jonah.1.2", "Jonah.1.3"],
    }
    if span != required_span:
        raise T440ParserContractError("T440 span/count contract drifted")

    _validate_t436_inputs(control)
    validate_source_contracts(control, root)
    validate_negative_fixture_requirements(control)
    validate_rust_policy(control)
    _reject_visible_biblical_text(control, "control")

    t437 = _read_yaml(root / T437_POLICY.relative_to(ROOT))
    if t437.get("policy", {}).get("lemma_attribute_interpretation") != "strong_lookup_hint":
        raise T440ParserContractError("T437 OSHB lemma policy must remain strong_lookup_hint")
    if t437.get("policy", {}).get("lemma_attribute_authority") != "metadata_only_not_local_lemma_or_strong_authority":
        raise T440ParserContractError("T437 OSHB lemma authority policy drifted")

    task = _read_yaml(root / TASK.relative_to(ROOT))
    if task.get("mode") != "source_specific_parser_contract_non_authorizing":
        raise T440ParserContractError("T440 task mode mismatch")
    _require_false(task.get("authorization", {}), FORBIDDEN_AUTH_TRUE, "task.authorization")

    substrate = _read_yaml(root / SUBSTRATE.relative_to(ROOT))
    lanes = substrate.get("pilot_lanes")
    if not isinstance(lanes, list) or not any(lane.get("task_id") == "T440" for lane in lanes if isinstance(lane, dict)):
        raise T440ParserContractError("original_language_evidence_substrate must include T440 lane")

    validate_all_text = (root / VALIDATE_ALL.relative_to(ROOT)).read_text(encoding="utf-8")
    if "validate_t440_jonah_hebrew_parser_contract.py" not in validate_all_text:
        raise T440ParserContractError("validate_all.py must run the T440 validator")

    roadmap_text = (root / ROADMAP.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("source-specific", "count parity is not enough", "no rust is added in t440", "strong lookup"):
        if phrase not in roadmap_text:
            raise T440ParserContractError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")

    dad_text = (root / DAD_PREFLIGHT.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("dad", "count parity", "source-specific", "rust"):
        if phrase not in dad_text:
            raise T440ParserContractError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")

    _validate_no_production_outputs(root)
    return control


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t440_jonah_hebrew_parser_contract(args.root.resolve())
    except T440ParserContractError as exc:
        print(f"T440 Jonah Hebrew parser contract validation failed: {exc}", file=sys.stderr)
        return 1
    print("T440 Jonah Hebrew parser contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
