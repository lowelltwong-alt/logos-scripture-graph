#!/usr/bin/env python3
"""Validate the source-metadata research atlas."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ATLAS = ROOT / ".ai" / "control" / "source_metadata_research_atlas.yaml"
WJ_INVENTORY = ROOT / ".ai" / "control" / "wj_marker_inventory.yaml"
CAPITALIZATION_INVENTORY = ROOT / ".ai" / "control" / "divine_capitalization_inventory.yaml"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "atlas_id",
    "owner",
    "authority",
    "scope",
    "observed_source_surfaces",
    "metadata_families",
    "required_future_metadata_packet_fields",
    "priority_research_cases",
    "global_non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_scripture_truth",
    "authorizes_lexical_truth",
    "authorizes_intertext_truth",
    "authorizes_speaker_attribution",
    "authorizes_graph_edges",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_output_change",
    "authorizes_boundary_import",
    "authorizes_new_algorithm_work",
}

REQUIRED_SURFACES = {
    "canonical_word_tokens",
    "editorial_cross_references",
    "footnotes",
    "section_headings",
    "boundary_claims",
    "wj_marker_inventory",
    "divine_capitalization_inventory",
    "raw_source_inventory",
}

REQUIRED_FAMILIES = {
    "editorial_cross_references",
    "strongs_style_word_numbers",
    "lexical_rarity_and_shared_lemmas",
    "footnotes_and_alternate_readings",
    "section_headings_and_titles",
    "paragraph_poetry_and_boundary_markers",
    "wj_red_letter_markers",
    "divine_name_title_capitalization",
    "speaker_labels_and_dialogue_markers",
    "edition_formatting_and_layout",
}

REQUIRED_PACKET_FIELDS = {
    "exact_passage_scope",
    "metadata_family_ids",
    "observed_source_surfaces",
    "raw_or_canonical_paths_consulted",
    "source_feature_summary",
    "phrase_clause_discourse_context",
    "syntax_role_if_original_language",
    "semantic_range_not_single_gloss",
    "theological_downstream_risks",
    "assumptions_avoided",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
    "non_target_identity_plan",
}

REQUIRED_GLOBAL_NON_AUTHORIZATIONS = {
    "metadata_as_scripture_truth",
    "metadata_as_lexical_truth",
    "metadata_as_intertext_truth",
    "metadata_as_speaker_attribution",
    "metadata_as_graph_edge",
    "metadata_as_chunk_boundary",
    "metadata_as_reviewed_gold",
    "metadata_as_retrieval_truth",
    "metadata_as_output_change",
    "metadata_as_algorithm_permission",
    "isolated_word_as_theological_truth",
    "isolated_lemma_as_doctrine",
    "single_gloss_as_meaning",
    "boundary_import",
    "t345",
}

REQUIRED_VALIDATORS = {
    "scripts/validate_source_metadata_research_atlas.py",
    "tests/test_source_metadata_research_atlas.py",
    "scripts/validate_original_language_phrase_context_policy.py",
    "tests/test_original_language_phrase_context_policy.py",
    "scripts/validate_source_metadata_authority.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_all.py",
}

REQUIRED_FAMILY_NON_AUTHORIZATIONS = {
    "editorial_cross_references": "automatic_cross_reference_edge",
    "strongs_style_word_numbers": "automatic_strongs_lexical_authority",
    "lexical_rarity_and_shared_lemmas": "lexical_rarity_as_theological_truth",
    "footnotes_and_alternate_readings": "alternate_reading_as_canonical_preference",
    "section_headings_and_titles": "section_heading_as_boundary_authority",
    "paragraph_poetry_and_boundary_markers": "formatting_marker_as_boundary_authority",
    "wj_red_letter_markers": "wj_marker_as_speaker_attribution",
    "divine_name_title_capitalization": "capitalization_as_theological_truth",
    "speaker_labels_and_dialogue_markers": "speaker_label_as_attribution_authority",
    "edition_formatting_and_layout": "edition_formatting_as_canonical_structure",
}

REQUIRED_CASES = {
    "revelation_crossrefs_wj_and_symbolic_intertexts",
    "john3_wj_speaker_boundary_metadata",
    "romans_9_11_argument_and_crossrefs",
    "psalms_messianic_headings_and_lexemes",
    "jude_noncanonical_reference_metadata",
}


class SourceMetadataResearchAtlasError(ValueError):
    """Raised when the source-metadata research atlas is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _line_count(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return sum(1 for _ in handle)
    except OSError as exc:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: unreadable for line count: {exc}") from exc


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SourceMetadataResearchAtlasError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise SourceMetadataResearchAtlasError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise SourceMetadataResearchAtlasError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise SourceMetadataResearchAtlasError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise SourceMetadataResearchAtlasError(f"{label} missing {missing}")


def _require_evidence_only(text: str, label: str) -> None:
    lowered = text.lower()
    if "evidence only" not in lowered:
        raise SourceMetadataResearchAtlasError(f"{label} must say evidence only")
    if "does not authorize" not in lowered and "not authorize" not in lowered:
        raise SourceMetadataResearchAtlasError(f"{label} must explicitly deny authorization")


def validate_source_metadata_research_atlas(path: Path = ATLAS) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "source_metadata_research_atlas":
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: object_type must be source_metadata_research_atlas")
    if data["trust_zone"] != "canonical":
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "source_metadata_research_atlas.v1":
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: schema_version must be source_metadata_research_atlas.v1")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_source_metadata_research_atlas", "records_observed_canonical_surfaces", "may_surface_for_review"):
        if authority.get(key) is not True:
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("translation_scope") != "eng-web":
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: scope.translation_scope must be eng-web")
    if scope.get("research_mode") != "non_output_changing":
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    relation_to_t358 = str(scope.get("relation_to_t358", "")).lower()
    for phrase in ("companion atlas", "without authorizing", "chunk", "gold", "graph", "retrieval", "implementation"):
        if phrase not in relation_to_t358:
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: scope.relation_to_t358 missing {phrase!r}")

    surfaces = data["observed_source_surfaces"]
    if not isinstance(surfaces, list) or not surfaces:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: observed_source_surfaces must be a non-empty list")
    surface_ids: set[str] = set()
    for surface in surfaces:
        if not isinstance(surface, dict):
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: each observed source surface must be a mapping")
        surface_id = str(surface.get("surface_id", ""))
        _require_string(surface_id, "observed_source_surfaces.surface_id")
        if surface_id in surface_ids:
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: duplicate surface_id {surface_id}")
        surface_ids.add(surface_id)
        _require_string(surface.get("path"), f"{surface_id}.path")
        target = ROOT / str(surface["path"])
        if not target.exists():
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}:{surface_id}: missing target {_rel(target)}")
        _require_string_list(surface.get("observed_features"), f"{surface_id}.observed_features")
        _require_string(surface.get("use_when"), f"{surface_id}.use_when")
        _require_string(surface.get("non_authorization"), f"{surface_id}.non_authorization")
        _require_evidence_only(surface["non_authorization"], f"{surface_id}.non_authorization")
        if "record_count" in surface:
            actual_count = _line_count(target)
            if surface["record_count"] != actual_count:
                raise SourceMetadataResearchAtlasError(
                    f"{_rel(path)}:{surface_id}: record_count {surface['record_count']} != actual {actual_count}"
                )
    missing_surfaces = sorted(REQUIRED_SURFACES - surface_ids)
    if missing_surfaces:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: missing observed source surfaces {missing_surfaces}")

    wj_surface = next(surface for surface in surfaces if surface["surface_id"] == "wj_marker_inventory")
    wj_counts = wj_surface.get("observed_counts")
    wj_data = _read_yaml(WJ_INVENTORY)
    if not isinstance(wj_counts, dict):
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: wj_marker_inventory.observed_counts must be a mapping")
    for key in ("wj_word_tokens", "wj_token_runs", "books_with_wj"):
        if wj_counts.get(key) != wj_data.get("summary", {}).get(key):
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: WJ observed count mismatch for {key}")

    capitalization = _read_yaml(CAPITALIZATION_INVENTORY)
    if capitalization.get("object_type") != "divine_capitalization_inventory":
        raise SourceMetadataResearchAtlasError(f"{_rel(CAPITALIZATION_INVENTORY)}: unexpected object_type")

    families = data["metadata_families"]
    if not isinstance(families, list) or not families:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: metadata_families must be a non-empty list")
    family_ids: set[str] = set()
    for family in families:
        if not isinstance(family, dict):
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: each metadata family must be a mapping")
        family_id = str(family.get("family_id", ""))
        _require_string(family_id, "metadata_families.family_id")
        if family_id in family_ids:
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: duplicate family_id {family_id}")
        family_ids.add(family_id)
        _require_string_list(family.get("tags"), f"{family_id}.tags")
        family_surfaces = set(_require_string_list(family.get("source_surfaces"), f"{family_id}.source_surfaces"))
        unknown_surfaces = sorted(family_surfaces - surface_ids)
        if unknown_surfaces:
            raise SourceMetadataResearchAtlasError(f"{family_id}.source_surfaces unknown {unknown_surfaces}")
        _require_string(family.get("use_when"), f"{family_id}.use_when")
        _require_string_list(family.get("required_review_questions"), f"{family_id}.required_review_questions")
        _require_string_list(family.get("theological_downstream_risks"), f"{family_id}.theological_downstream_risks")
        _require_string(family.get("authority_boundary"), f"{family_id}.authority_boundary")
        _require_evidence_only(family["authority_boundary"], f"{family_id}.authority_boundary")
        if family_id in {"strongs_style_word_numbers", "lexical_rarity_and_shared_lemmas"}:
            family_text = " ".join(str(value) for value in family.values()).lower()
            for phrase in ("phrase", "clause", "discourse"):
                if phrase not in family_text:
                    raise SourceMetadataResearchAtlasError(f"{family_id} missing original-language context phrase {phrase!r}")
        non_authorizations = set(_require_string_list(family.get("non_authorizations"), f"{family_id}.non_authorizations"))
        required_non_authorization = REQUIRED_FAMILY_NON_AUTHORIZATIONS.get(family_id)
        if required_non_authorization and required_non_authorization not in non_authorizations:
            raise SourceMetadataResearchAtlasError(
                f"{family_id}.non_authorizations missing {required_non_authorization}"
            )
    missing_families = sorted(REQUIRED_FAMILIES - family_ids)
    if missing_families:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: missing metadata families {missing_families}")

    _require_subset(REQUIRED_PACKET_FIELDS, data["required_future_metadata_packet_fields"], "required_future_metadata_packet_fields")
    _require_subset(REQUIRED_GLOBAL_NON_AUTHORIZATIONS, data["global_non_authorizations"], "global_non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    cases = data["priority_research_cases"]
    if not isinstance(cases, list) or not cases:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: priority_research_cases must be a non-empty list")
    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise SourceMetadataResearchAtlasError(f"{_rel(path)}: each priority case must be a mapping")
        case_id = str(case.get("case_id", ""))
        _require_string(case_id, "priority_research_cases.case_id")
        case_ids.add(case_id)
        _require_string_list(case.get("passages"), f"{case_id}.passages")
        case_families = set(_require_string_list(case.get("metadata_families"), f"{case_id}.metadata_families"))
        unknown_families = sorted(case_families - family_ids)
        if unknown_families:
            raise SourceMetadataResearchAtlasError(f"{case_id}.metadata_families unknown {unknown_families}")
        if case.get("status") not in {"research_only", "owner_review_pending", "governed_hold_existing_gold"}:
            raise SourceMetadataResearchAtlasError(f"{case_id}.status is invalid")
        _require_string(case.get("reason"), f"{case_id}.reason")
    missing_cases = sorted(REQUIRED_CASES - case_ids)
    if missing_cases:
        raise SourceMetadataResearchAtlasError(f"{_rel(path)}: missing priority cases {missing_cases}")

    return data


def main() -> int:
    try:
        validate_source_metadata_research_atlas()
    except SourceMetadataResearchAtlasError as exc:
        print(f"Source-metadata research atlas validation failed: {exc}", file=sys.stderr)
        return 1
    print("Source-metadata research atlas validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
