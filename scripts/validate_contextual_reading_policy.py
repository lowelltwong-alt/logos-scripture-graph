#!/usr/bin/env python3
"""Validate the contextual reading policy."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "contextual_reading_policy.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

POLICY_REL = ".ai/control/contextual_reading_policy.yaml"
VALIDATOR_REL = "scripts/validate_contextual_reading_policy.py"

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
    "context_window_defaults",
    "future_history_sidecar_policy",
    "required_future_review_packet_fields",
    "contextual_reading_lessons",
    "non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_scripture_truth",
    "authorizes_doctrinal_system",
    "authorizes_historical_context_as_authority",
    "authorizes_cultural_background_as_authority",
    "authorizes_canonical_intertext_truth",
    "authorizes_original_language_truth",
    "authorizes_source_metadata_truth",
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
    "immediate_discourse_context",
    "paragraph_section_context",
    "chapter_book_context",
    "canonical_context",
    "original_language_context",
    "historical_cultural_context",
    "source_metadata_context",
}

REQUIRED_PACKET_FIELDS = {
    "exact_passage_scope",
    "immediate_previous_context",
    "immediate_following_context",
    "paragraph_or_section_context",
    "chapter_context",
    "book_argument_or_narrative_context",
    "canonical_context_links_considered",
    "original_language_context_if_used",
    "historical_cultural_context_if_used",
    "source_metadata_context_if_used",
    "context_needed_to_avoid_prooftexting",
    "assumptions_avoided",
    "orthodox_options_preserved",
    "theological_downstream_risks",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
}

REQUIRED_LESSON_IDS = {
    "context_before_boundary",
    "immediate_neighbors_matter",
    "chapter_book_argument_matter",
    "canonical_context_preserves_interpretive_scope",
    "history_serves_scripture_not_governs_it",
    "context_does_not_authorize_output",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "prooftexting_from_isolated_verse",
    "context_as_doctrinal_system",
    "context_as_chunk_boundary_authority",
    "context_as_reviewed_gold",
    "context_as_route_behavior",
    "context_as_evaluator_change",
    "context_as_graph_edge",
    "context_as_retrieval_truth",
    "historical_background_as_scripture_authority",
    "cultural_background_as_doctrine_authority",
    "anti_supernatural_default",
    "liberal_critical_default",
    "editorial_cross_reference_as_canonical_intertext_truth",
    "model_inferred_context_as_truth",
    "metadata_as_context_authority",
    "history_sidecar_as_canonical_repo",
    "boundary_import",
    "chunk_output_change",
}

REQUIRED_VALIDATORS = {
    VALIDATOR_REL,
    "tests/test_contextual_reading_policy.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_chunking_lesson_index.py",
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_bible_chunking_readiness_map.py",
    "scripts/validate_all.py",
}


class ContextualReadingPolicyError(ValueError):
    """Raised when the contextual reading policy is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContextualReadingPolicyError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _read_text(path)
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ContextualReadingPolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ContextualReadingPolicyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_non_empty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContextualReadingPolicyError(f"{label} must be a non-empty string")


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise ContextualReadingPolicyError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise ContextualReadingPolicyError(f"{label} missing {missing}")


def validate_contextual_reading_policy(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise ContextualReadingPolicyError(f"{_rel(path)}: missing top-level keys {missing}")

    if data["object_type"] != "contextual_reading_policy":
        raise ContextualReadingPolicyError(f"{_rel(path)}: object_type is wrong")
    if data["trust_zone"] != "canonical":
        raise ContextualReadingPolicyError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise ContextualReadingPolicyError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "contextual_reading_policy.v1":
        raise ContextualReadingPolicyError(f"{_rel(path)}: schema_version is wrong")

    assessment = data["research_assessment"]
    if not isinstance(assessment, dict):
        raise ContextualReadingPolicyError(f"{_rel(path)}: research_assessment must be a mapping")
    for key in ("short_answer", "refined_rule", "why_this_matters"):
        _require_non_empty_string(assessment.get(key), f"research_assessment.{key}")
    refined = assessment["refined_rule"].lower()
    for phrase in ("immediate discourse", "chapter/book", "canonical", "historical/cultural"):
        if phrase not in refined:
            raise ContextualReadingPolicyError(f"{_rel(path)}: refined_rule missing {phrase!r}")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise ContextualReadingPolicyError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_contextual_reading_policy") is not True:
        raise ContextualReadingPolicyError(f"{_rel(path)}: records flag must be true")
    if authority.get("may_surface_context_evidence_for_review") is not True:
        raise ContextualReadingPolicyError(f"{_rel(path)}: review evidence flag must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ContextualReadingPolicyError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise ContextualReadingPolicyError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise ContextualReadingPolicyError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("research_mode") != "non_output_changing":
        raise ContextualReadingPolicyError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    for key in ("relation_to_t382", "relation_to_t376", "relation_to_history_repo"):
        _require_non_empty_string(scope.get(key), f"scope.{key}")
    if "does not supersede" not in scope["relation_to_t376"]:
        raise ContextualReadingPolicyError(f"{_rel(path)}: relation_to_t376 must preserve owner gate")
    if "Do not create a separate history repo" not in scope["relation_to_history_repo"]:
        raise ContextualReadingPolicyError(f"{_rel(path)}: history repo policy must block current repo creation")

    layers = data["context_layers_required"]
    if not isinstance(layers, list) or not layers:
        raise ContextualReadingPolicyError(f"{_rel(path)}: context_layers_required must be a list")
    layer_ids = set()
    for layer in layers:
        if not isinstance(layer, dict):
            raise ContextualReadingPolicyError(f"{_rel(path)}: each context layer must be a mapping")
        layer_id = str(layer.get("layer_id", ""))
        _require_non_empty_string(layer_id, "context_layers_required.layer_id")
        layer_ids.add(layer_id)
        _require_non_empty_string(layer.get("required_when"), f"{layer_id}.required_when")
        _require_subset(set(layer.get("must_record", [])), layer.get("must_record"), f"{layer_id}.must_record")
        _require_non_empty_string(layer.get("non_authorization"), f"{layer_id}.non_authorization")
        lowered = str(layer["non_authorization"]).lower()
        if "evidence only" not in lowered or ("authorize" not in lowered and "authority" not in lowered):
            raise ContextualReadingPolicyError(f"{layer_id}.non_authorization must deny authority")
    missing_layers = sorted(REQUIRED_CONTEXT_LAYERS - layer_ids)
    if missing_layers:
        raise ContextualReadingPolicyError(f"{_rel(path)}: missing context layers {missing_layers}")

    defaults = data["context_window_defaults"]
    if not isinstance(defaults, dict):
        raise ContextualReadingPolicyError(f"{_rel(path)}: context_window_defaults must be a mapping")
    minimum = defaults.get("review_packet_minimum")
    if not isinstance(minimum, dict):
        raise ContextualReadingPolicyError(f"{_rel(path)}: review_packet_minimum must be a mapping")
    for key in ("previous_context", "following_context", "broader_context", "history_context"):
        _require_non_empty_string(minimum.get(key), f"review_packet_minimum.{key}")
    output_prereq = defaults.get("output_changing_prerequisite")
    if not isinstance(output_prereq, dict) or output_prereq.get("required") is not True:
        raise ContextualReadingPolicyError(f"{_rel(path)}: output_changing_prerequisite.required must be true")

    sidecar = data["future_history_sidecar_policy"]
    if not isinstance(sidecar, dict):
        raise ContextualReadingPolicyError(f"{_rel(path)}: future_history_sidecar_policy must be a mapping")
    if sidecar.get("create_history_repo_now") is not False:
        raise ContextualReadingPolicyError(f"{_rel(path)}: create_history_repo_now must be false")
    _require_subset({"learning-sidecar", "proposed"}, sidecar.get("allowed_trust_zones"), "allowed_trust_zones")
    _require_subset(
        {
            "scripture_authority",
            "doctrine_authority",
            "chunk_boundary_authority",
            "graph_edge_authority",
            "retrieval_truth_authority",
            "anti_supernatural_default",
            "liberal_critical_default",
            "source_of_canon_scope_change",
        },
        sidecar.get("disallowed_roles"),
        "future_history_sidecar_policy.disallowed_roles",
    )

    _require_subset(REQUIRED_PACKET_FIELDS, data["required_future_review_packet_fields"], "required_future_review_packet_fields")

    lessons = data["contextual_reading_lessons"]
    if not isinstance(lessons, list) or not lessons:
        raise ContextualReadingPolicyError(f"{_rel(path)}: contextual_reading_lessons must be a list")
    lesson_ids = set()
    for lesson in lessons:
        if not isinstance(lesson, dict):
            raise ContextualReadingPolicyError(f"{_rel(path)}: each lesson must be a mapping")
        lesson_id = str(lesson.get("lesson_id", ""))
        _require_non_empty_string(lesson_id, "contextual_reading_lessons.lesson_id")
        lesson_ids.add(lesson_id)
        for key in ("rule", "use_when", "non_authorization"):
            _require_non_empty_string(lesson.get(key), f"{lesson_id}.{key}")
        lowered = str(lesson["non_authorization"]).lower()
        if "authorize" not in lowered and "authority" not in lowered:
            raise ContextualReadingPolicyError(f"{lesson_id}.non_authorization must deny authority")
    missing_lessons = sorted(REQUIRED_LESSON_IDS - lesson_ids)
    if missing_lessons:
        raise ContextualReadingPolicyError(f"{_rel(path)}: missing lessons {missing_lessons}")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data["non_authorizations"], "non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")
    _validate_linked_surfaces()
    return data


def _validate_linked_surfaces() -> None:
    preflight = _read_yaml(PREFLIGHT)
    reading = {
        str(item.get("path")): item
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    if POLICY_REL not in reading:
        raise ContextualReadingPolicyError(f"{_rel(PREFLIGHT)}: contextual policy must be mandatory reading")
    decision_entry = reading.get(".ai/control/chunking_theological_decision_register.yaml", {})
    if "CD-059" not in decision_entry.get("required_decision_ids", []):
        raise ContextualReadingPolicyError(f"{_rel(PREFLIGHT)}: CD-059 must be required")
    lesson_entry = reading.get(".ai/control/chunking_lesson_index.yaml", {})
    if "LSN-011" not in lesson_entry.get("required_lesson_ids", []):
        raise ContextualReadingPolicyError(f"{_rel(PREFLIGHT)}: LSN-011 must be required")
    if "contextual_reading_review" not in preflight.get("future_output_changing_use_requires", []):
        raise ContextualReadingPolicyError(f"{_rel(PREFLIGHT)}: contextual review must be required before output changes")

    lesson_text = _read_text(LESSON_INDEX)
    for phrase in ("LSN-011", "Context always matters", POLICY_REL, "historical-context", "chapter-context"):
        if phrase not in lesson_text:
            raise ContextualReadingPolicyError(f"{_rel(LESSON_INDEX)}: missing {phrase!r}")

    register_text = _read_text(REGISTER)
    for phrase in ("CD-059", "Contextual reading discipline", "T383", POLICY_REL):
        if phrase not in register_text:
            raise ContextualReadingPolicyError(f"{_rel(REGISTER)}: missing {phrase!r}")

    readiness_text = _read_text(READINESS_MAP)
    for phrase in (POLICY_REL, "contextual_reading_policy_change"):
        if phrase not in readiness_text:
            raise ContextualReadingPolicyError(f"{_rel(READINESS_MAP)}: missing {phrase!r}")

    for path in (FRONT_DOOR, TOC, ROADMAP_TOC):
        text = _read_text(path)
        for phrase in (POLICY_REL, "contextual-reading", "historical-context", "chapter-context"):
            if phrase not in text:
                raise ContextualReadingPolicyError(f"{_rel(path)}: missing {phrase!r}")


def main() -> int:
    try:
        validate_contextual_reading_policy()
    except ContextualReadingPolicyError as exc:
        print(f"Contextual reading policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("Contextual reading policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
