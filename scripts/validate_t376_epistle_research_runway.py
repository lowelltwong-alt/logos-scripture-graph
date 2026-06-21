#!/usr/bin/env python3
"""Validate the T376 epistle argument research-first runway."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
RUNWAY = ROOT / ".ai" / "control" / "t376_epistle_research_runway.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T376_EPISTLE_RESEARCH_RUNWAY.md"
TASK = ROOT / ".ai" / "tasks" / "T376.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T376" / "handoff.md"
AUDIT_README = ROOT / ".ai" / "audits" / "reports" / "README.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260621-T376-epistle-research-runway.md"

RUNWAY_REL = ".ai/control/t376_epistle_research_runway.yaml"
VALIDATOR_REL = "scripts/validate_t376_epistle_research_runway.py"
DOC_REL = "docs/roadmap/T376_EPISTLE_RESEARCH_RUNWAY.md"

REQUIRED_AUTHORITY_FALSE = {
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
    "authorizes_denominational_systematic_theology_as_chunk_authority",
}

REQUIRED_MAY_CONTINUE = {
    "compile_epistle_argument_target_options",
    "inspect_existing_pending_review_packets",
    "inspect_epistle_argument_dossier_queue",
    "identify_contextual_reading_requirements",
    "identify_source_metadata_watchpoints",
    "identify_original_language_phrase_context_needs",
    "identify_textual_variant_or_source_tradition_sensitivities",
    "identify_orthodox_hermeneutic_firewall_risks",
    "create_non_authorizing_research_dockets_or_review_packet_drafts",
    "update_decision_register_readiness_map_preflight_tocs_audit_and_handoff",
    "add_validators_and_tests_for_non_authorizing_research_surfaces",
}

REQUIRED_STOP_FOR_OWNER = {
    "exact_epistle_target_selection_for_promotion_or_implementation",
    "reviewed_gold_promotion",
    "child_span_selection_or_child_span_reviewed_gold",
    "chunk_output_change",
    "route_behavior_change",
    "evaluator_behavior_or_formula_change",
    "graph_edge_generation",
    "retrieval_truth_or_vector_output",
    "boundary_import",
    "whole_bible_output_pass",
    "preferred_reading_or_source_tradition_preference",
    "canon_scope_change",
    "denominational_systematic_theology_as_chunk_authority",
}

REQUIRED_TARGET_OPTIONS = {
    "T384-A",
    "T384-B",
    "T384-C",
    "T384-D",
    "T384-E",
    "T384-F",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "exact_target_selection",
    "child_span_selection",
    "child_span_reviewed_gold_promotion",
    "reviewed_gold_promotion",
    "chunk_output_change",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "boundary_import",
    "whole_bible_output_pass",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "denominational_systematic_theology_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
}


class T376RunwayError(ValueError):
    """Raised when the T376 runway drifts into authority or loses required context."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T376RunwayError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T376RunwayError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T376RunwayError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T376RunwayError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T376RunwayError(f"{label} missing {missing}")


def _validate_static(runway: dict[str, Any]) -> None:
    expected = {
        "object_type": "epistle_argument_research_runway_selection",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t376_epistle_research_runway.v1",
        "selection_id": "t376_epistle_argument_research_first_runway",
        "task_id": "T376",
        "status": "complete_selected_research_first_epistle_argument_runway",
        "selected_option": "T376-A",
        "selected_lane": "epistle_argument",
        "selected_lane_mode": "research_and_prep_only",
    }
    for key, value in expected.items():
        if runway.get(key) != value:
            raise T376RunwayError(f"{RUNWAY_REL}: {key} must be {value!r}")

    authority = runway.get("authority")
    if not isinstance(authority, dict):
        raise T376RunwayError(f"{RUNWAY_REL}: authority must be a mapping")
    if authority.get("records_owner_lane_selection") is not True:
        raise T376RunwayError(f"{RUNWAY_REL}: authority.records_owner_lane_selection must be true")
    if authority.get("authorizes_non_output_changing_research_prep") is not True:
        raise T376RunwayError(f"{RUNWAY_REL}: authority must allow non-output research/prep")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise T376RunwayError(f"{RUNWAY_REL}: authority.{key} must be false")

    boundary = runway.get("research_autonomy_boundary")
    if not isinstance(boundary, dict):
        raise T376RunwayError(f"{RUNWAY_REL}: research_autonomy_boundary must be a mapping")
    _require_subset(
        REQUIRED_MAY_CONTINUE,
        boundary.get("may_continue_without_new_owner_decision"),
        "research_autonomy_boundary.may_continue_without_new_owner_decision",
    )
    _require_subset(
        REQUIRED_STOP_FOR_OWNER,
        boundary.get("must_stop_for_owner_decision_before"),
        "research_autonomy_boundary.must_stop_for_owner_decision_before",
    )

    policies = runway.get("required_policy_fields")
    if not isinstance(policies, dict):
        raise T376RunwayError(f"{RUNWAY_REL}: required_policy_fields must be a mapping")
    expected_paths = {
        "contextual_reading_policy": ".ai/control/contextual_reading_policy.yaml",
        "source_metadata_evidence_only": ".ai/control/source_metadata_research_atlas.yaml",
        "original_language_phrase_context": ".ai/control/original_language_phrase_context_policy.yaml",
        "orthodox_hermeneutic_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
        "textual_critical_case_policy": ".ai/control/textual_critical_case_policy.yaml",
    }
    for key, expected_path in expected_paths.items():
        if not isinstance(policies.get(key), dict) or policies[key].get("path") != expected_path:
            raise T376RunwayError(f"{RUNWAY_REL}: required_policy_fields.{key}.path must be {expected_path}")

    _require_subset(
        {
            "immediate_discourse_context",
            "paragraph_section_context",
            "chapter_book_context",
            "canonical_context",
            "original_language_context_if_used",
            "historical_cultural_context_if_relevant",
            "source_metadata_context_if_cited",
        },
        policies["contextual_reading_policy"].get("required_layers"),
        "required_policy_fields.contextual_reading_policy.required_layers",
    )

    options = runway.get("target_options_to_research_before_owner_selection")
    if not isinstance(options, list) or len(options) < len(REQUIRED_TARGET_OPTIONS):
        raise T376RunwayError(f"{RUNWAY_REL}: target options are incomplete")
    option_ids = {option.get("option_id") for option in options if isinstance(option, dict)}
    if REQUIRED_TARGET_OPTIONS - option_ids:
        raise T376RunwayError(f"{RUNWAY_REL}: target options missing {sorted(REQUIRED_TARGET_OPTIONS - option_ids)}")
    for option in options:
        if not isinstance(option, dict):
            raise T376RunwayError(f"{RUNWAY_REL}: each target option must be a mapping")
        label = f"{RUNWAY_REL}:{option.get('option_id')}"
        for key in ("passage", "label", "why_serious"):
            if not isinstance(option.get(key), str) or not option[key].strip():
                raise T376RunwayError(f"{label}: {key} must be a non-empty string")
        _require_subset({"all_good_options_and_repercussions"}, option.get("required_research"), f"{label}.required_research")
        if not isinstance(option.get("repercussions"), list) or len(option["repercussions"]) < 2:
            raise T376RunwayError(f"{label}: repercussions must be a non-empty list")
        if option.get("exact_target_selected") is not False:
            raise T376RunwayError(f"{label}: exact_target_selected must be false")
        if option.get("promotion_authorized") is not False:
            raise T376RunwayError(f"{label}: promotion_authorized must be false")

    recommendation = runway.get("recommendation")
    if not isinstance(recommendation, dict):
        raise T376RunwayError(f"{RUNWAY_REL}: recommendation must be a mapping")
    if recommendation.get("likely_first_option_to_compare_later") != "T384-A":
        raise T376RunwayError(f"{RUNWAY_REL}: likely first comparison option must be T384-A")
    if "not an owner selection" not in str(recommendation.get("why_not_selection", "")):
        raise T376RunwayError(f"{RUNWAY_REL}: recommendation must deny owner selection")

    next_route = runway.get("next_route")
    if not isinstance(next_route, dict):
        raise T376RunwayError(f"{RUNWAY_REL}: next_route must be a mapping")
    expected_next = {
        "task_id": "T384",
        "title": "Epistle Argument Research Runway And Target Options Matrix",
        "route_type": "epistle_argument_research_runway",
        "starts_only_if": "T376_A_epistle_argument_research_runway_selected",
        "owner_decision_required_before_promotion_or_implementation": True,
        "output_change_authorized": False,
        "implementation_authorized": False,
        "reviewed_gold_promoted": False,
        "child_spans_authorized": False,
        "route_behavior_authorized": False,
        "evaluator_change_authorized": False,
        "graph_edge_generation_allowed": False,
        "retrieval_truth_authorized": False,
        "embedding_or_vector_work_allowed": False,
    }
    for key, value in expected_next.items():
        if next_route.get(key) != value:
            raise T376RunwayError(f"{RUNWAY_REL}: next_route.{key} must be {value!r}")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, runway.get("non_authorizations"), "non_authorizations")
    lesson = runway.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-012":
        raise T376RunwayError(f"{RUNWAY_REL}: lesson_recorded.lesson_id must be LSN-012")
    if runway.get("decision_register_entry") != "CD-060":
        raise T376RunwayError(f"{RUNWAY_REL}: decision_register_entry must be CD-060")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-060", "T376-A selects epistle argument research/prep runway", RUNWAY_REL)),
        (PREFLIGHT, ("CD-060", "LSN-012", RUNWAY_REL, "Research autonomy is not authority autonomy")),
        (LESSON_INDEX, ("LSN-012", "Research autonomy is not authority autonomy", "T376")),
        (READINESS, ("task_id: T384", RUNWAY_REL, "research_autonomy_is_not_authority_autonomy")),
        (ROADMAP, ("id: T376", "complete_selected_research_first_epistle_argument_runway", "id: T384")),
        (FRONT_DOOR, (RUNWAY_REL, VALIDATOR_REL, "T384 epistle argument research/options matrix")),
        (MAIN_TOC, (RUNWAY_REL, VALIDATOR_REL, "research-runway")),
        (ROADMAP_TOC, (RUNWAY_REL, DOC_REL, "T376 | Epistle research runway")),
        (ROADMAP_DOC, (RUNWAY_REL, "Research autonomy is not authority autonomy", "T384")),
        (TASK, ("id: T376", "CD-060", "LSN-012")),
        (HANDOFF, ("task_id: T376", "CD-060", "T384")),
        (AUDIT_README, ("20260621-T376-epistle-research-runway.md", "T376")),
        (AUDIT, ("T376 No-Context Audit Surface", "Research autonomy is not authority autonomy", "T384")),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T376RunwayError(f"{_rel(path)}: missing {phrase!r}")


def validate_t376_epistle_research_runway(path: Path = RUNWAY) -> dict[str, Any]:
    runway = _read_yaml(path)
    _validate_static(runway)
    _validate_links()
    return runway


def main() -> int:
    try:
        validate_t376_epistle_research_runway()
    except T376RunwayError as exc:
        print(f"T376 epistle research runway validation failed: {exc}", file=sys.stderr)
        return 1
    print("T376 epistle research runway validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
