#!/usr/bin/env python3
"""Validate the original-language phrase/context policy."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "original_language_phrase_context_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
SOURCE_METADATA_ATLAS = ROOT / ".ai" / "control" / "source_metadata_research_atlas.yaml"
ORTHODOX_LANGUAGE_QUEUE = ROOT / ".ai" / "control" / "orthodox_original_language_pressure_dossier_queue.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

POLICY_REL = ".ai/control/original_language_phrase_context_policy.yaml"
VALIDATOR_REL = "scripts/validate_original_language_phrase_context_policy.py"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "policy_id",
    "owner",
    "status",
    "research_assessment",
    "authority",
    "scope",
    "context_layers_required",
    "handling_when_including_greek_words",
    "required_future_original_language_packet_fields",
    "non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_original_language_truth",
    "authorizes_lexical_truth",
    "authorizes_doctrinal_system",
    "authorizes_translation_preference",
    "authorizes_textual_critical_decision",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_nonorthodox_source_authority",
    "authorizes_extra_canonical_source_authority",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_chunk_output_change",
}

REQUIRED_CONTEXT_LAYERS = {
    "surface_word_or_phrase",
    "lemma_and_morphology",
    "phrase_clause_syntax",
    "discourse_and_argument_context",
    "canonical_and_orthodox_context",
}

REQUIRED_PACKET_FIELDS = {
    "exact_passage_scope",
    "exact_surface_word_or_phrase",
    "lemma_or_strongs_tag_if_available",
    "morphology_or_parsing_if_available",
    "phrase_or_clause_scope",
    "syntax_role",
    "immediate_discourse_context",
    "author_book_genre_context",
    "canonical_context_needed_to_avoid_prooftexting",
    "semantic_range_not_single_gloss",
    "theological_downstream_risks",
    "assumptions_avoided",
    "orthodox_options_preserved",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
    "non_target_identity_plan",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "isolated_word_as_theological_truth",
    "isolated_lemma_as_doctrine",
    "single_gloss_as_meaning",
    "strongs_number_as_lexical_truth",
    "lexical_rarity_as_intertext_truth",
    "grammar_label_as_doctrine",
    "phrase_context_as_automatic_chunk_boundary",
    "discourse_context_as_route_authority",
    "original_language_as_graph_edge",
    "original_language_as_retrieval_truth",
    "source_language_as_automatic_truth",
    "translation_preference",
    "textual_critical_decision",
    "doctrinal_system_selection",
    "nonorthodox_source_authority",
    "extra_canonical_source_authority",
    "canon_scope_change",
    "boundary_import",
    "reviewed_gold_promotion",
    "route_behavior_change",
    "evaluator_change",
    "chunk_output_change",
}

REQUIRED_VALIDATORS = {
    VALIDATOR_REL,
    "tests/test_original_language_phrase_context_policy.py",
    "scripts/validate_source_metadata_research_atlas.py",
    "scripts/validate_orthodox_original_language_pressure_dossier_queue.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_all.py",
}


class OriginalLanguagePhraseContextPolicyError(ValueError):
    """Raised when the original-language phrase/context policy is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _read_text(path)
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise OriginalLanguagePhraseContextPolicyError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise OriginalLanguagePhraseContextPolicyError(f"{label} missing {missing}")


def _require_non_empty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise OriginalLanguagePhraseContextPolicyError(f"{label} must be a non-empty string")


def validate_original_language_phrase_context_policy(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "original_language_phrase_context_policy":
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: object_type is wrong")
    if data["trust_zone"] != "canonical":
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "original_language_phrase_context_policy.v1":
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: schema_version is wrong")

    assessment = data["research_assessment"]
    if not isinstance(assessment, dict):
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: research_assessment must be a mapping")
    for key in ("short_answer", "refined_rule", "why_this_matters"):
        _require_non_empty_string(assessment.get(key), f"research_assessment.{key}")
    refined = assessment["refined_rule"].lower()
    for phrase in ("phrase", "clause", "syntax", "discourse", "canonical context"):
        if phrase not in refined:
            raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: refined_rule missing {phrase!r}")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_original_language_phrase_context_policy") is not True:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: records flag must be true")
    if authority.get("may_surface_original_language_evidence_for_review") is not True:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: review surfacing flag must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("research_mode") != "non_output_changing":
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    _require_subset({"greek", "hebrew"}, scope.get("language_scope"), "scope.language_scope")
    for key in ("relation_to_t359", "relation_to_t377", "relation_to_t373"):
        _require_non_empty_string(scope.get(key), f"scope.{key}")
    if "does not supersede" not in str(scope["relation_to_t373"]):
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: relation_to_t373 must preserve the T373 gate")

    layers = data["context_layers_required"]
    if not isinstance(layers, list) or not layers:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: context_layers_required must be a list")
    layer_ids = set()
    for layer in layers:
        if not isinstance(layer, dict):
            raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: each context layer must be a mapping")
        layer_id = str(layer.get("layer_id", ""))
        _require_non_empty_string(layer_id, "context_layers_required.layer_id")
        layer_ids.add(layer_id)
        _require_non_empty_string(layer.get("required_when"), f"{layer_id}.required_when")
        _require_subset(set(layer.get("must_record", [])), layer.get("must_record"), f"{layer_id}.must_record")
        _require_non_empty_string(layer.get("non_authorization"), f"{layer_id}.non_authorization")
        lowered = str(layer["non_authorization"]).lower()
        if "evidence only" not in lowered or ("authorize" not in lowered and "authority" not in lowered):
            raise OriginalLanguagePhraseContextPolicyError(f"{layer_id}.non_authorization must deny authority")
    missing_layers = sorted(REQUIRED_CONTEXT_LAYERS - layer_ids)
    if missing_layers:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: missing context layers {missing_layers}")

    handling = data["handling_when_including_greek_words"]
    if not isinstance(handling, list) or not handling:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: handling_when_including_greek_words must be a list")
    handling_text = " ".join(str(item) for item in handling)
    for phrase in ("phrase", "clause", "discourse", "Strong's-style", "Stop for owner review"):
        if phrase not in handling_text:
            raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: handling list missing {phrase!r}")

    _require_subset(REQUIRED_PACKET_FIELDS, data["required_future_original_language_packet_fields"], "required_future_original_language_packet_fields")
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data["non_authorizations"], "non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    _validate_linked_surfaces()
    return data


def _validate_linked_surfaces() -> None:
    register_text = _read_text(REGISTER)
    for phrase in ("CD-049", "Original-language word evidence requires phrase and discourse context", "T381", POLICY_REL):
        if phrase not in register_text:
            raise OriginalLanguagePhraseContextPolicyError(f"{_rel(REGISTER)}: missing {phrase!r}")

    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {str(item.get("path")) for item in preflight.get("mandatory_reading", []) if isinstance(item, dict)}
    if POLICY_REL not in reading_paths:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(PREFLIGHT)}: policy must be mandatory reading")
    decision_entry = next(
        (item for item in preflight.get("mandatory_reading", []) if isinstance(item, dict) and item.get("path") == ".ai/control/chunking_theological_decision_register.yaml"),
        {},
    )
    if "CD-049" not in decision_entry.get("required_decision_ids", []):
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(PREFLIGHT)}: CD-049 must be required")
    if "original_language_phrase_clause_context" not in preflight.get("non_authorizing_metadata_types", []):
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(PREFLIGHT)}: missing original_language_phrase_clause_context metadata type")

    atlas_text = _read_text(SOURCE_METADATA_ATLAS)
    for phrase in (
        "phrase_clause_discourse_context",
        "syntax_role_if_original_language",
        "semantic_range_not_single_gloss",
        "isolated_word_as_theological_truth",
        "isolated_lemma_as_doctrine",
    ):
        if phrase not in atlas_text:
            raise OriginalLanguagePhraseContextPolicyError(f"{_rel(SOURCE_METADATA_ATLAS)}: missing {phrase!r}")

    queue_text = _read_text(ORTHODOX_LANGUAGE_QUEUE)
    for phrase in (
        "phrase_context_rule",
        "phrase_clause_discourse_context_review",
        "isolated_word_as_theological_truth",
        "single_gloss_as_meaning",
    ):
        if phrase not in queue_text:
            raise OriginalLanguagePhraseContextPolicyError(f"{_rel(ORTHODOX_LANGUAGE_QUEUE)}: missing {phrase!r}")

    roadmap = _read_yaml(ROADMAP)
    phase_4 = roadmap.get("phases", {}).get("phase_4", {})
    tasks = {item.get("id"): item for item in phase_4.get("tasks", []) if isinstance(item, dict)}
    future = {item.get("id"): item for item in phase_4.get("future_sequence", []) if isinstance(item, dict)}
    task = tasks.get("T381") or future.get("T381")
    if not isinstance(task, dict) or task.get("status") != "complete":
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(ROADMAP)}: T381 must be complete")
    if task.get("policy") != POLICY_REL:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(ROADMAP)}: T381 policy path is stale")
    if task.get("output_change_authorized") is not False or task.get("implementation_authorized") is not False:
        raise OriginalLanguagePhraseContextPolicyError(f"{_rel(ROADMAP)}: T381 must be non-output-changing")

    for path in (FRONT_DOOR, TOC, ROADMAP_TOC):
        text = _read_text(path)
        for phrase in (POLICY_REL, "phrase/context", "original-language", "isolated word"):
            if phrase not in text:
                raise OriginalLanguagePhraseContextPolicyError(f"{_rel(path)}: missing {phrase!r}")


def main() -> int:
    try:
        validate_original_language_phrase_context_policy()
    except OriginalLanguagePhraseContextPolicyError as exc:
        print(f"Original-language phrase/context policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("Original-language phrase/context policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
