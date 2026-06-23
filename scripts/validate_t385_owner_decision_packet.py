#!/usr/bin/env python3
"""Validate the T385 owner decision packet."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / ".ai" / "control" / "t385_owner_decision_packet.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T385_OWNER_DECISION_PACKET.md"
TASK = ROOT / ".ai" / "tasks" / "T385.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T385" / "handoff.md"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

PACKET_REL = ".ai/control/t385_owner_decision_packet.yaml"
DOC_REL = "docs/roadmap/T385_OWNER_DECISION_PACKET.md"
VALIDATOR_REL = "scripts/validate_t385_owner_decision_packet.py"

REQUIRED_OPTION_IDS = {
    "T385-A",
    "T385-B",
    "T385-C",
    "T385-D",
    "T385-E",
    "T385-F",
    "T385-G",
    "T385-H",
    "T385-I",
}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_exact_target_selection",
    "authorizes_review_packet_strengthening",
    "authorizes_reviewed_gold_promotion",
    "authorizes_child_spans",
    "authorizes_chunk_output_change",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_boundary_import",
    "authorizes_preferred_reading_or_source_tradition",
    "authorizes_canon_scope_change",
    "authorizes_denominational_systematic_theology_as_chunk_authority",
    "authorizes_sqlite_database_creation",
    "authorizes_metadata_row_population",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "exact_target_selection",
    "review_packet_strengthening_without_owner_selection",
    "reviewed_gold_promotion",
    "child_span_selection",
    "child_span_reviewed_gold_promotion",
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
    "recommendation_as_owner_selection",
    "coverage_status_as_output_authority",
    "manuscript_metadata_as_preferred_reading_authority",
}


class T385PacketError(ValueError):
    """Raised when the T385 packet loses option, recommendation, or authority boundaries."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T385PacketError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T385PacketError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T385PacketError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T385PacketError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T385PacketError(f"{label} missing {missing}")


def _validate_static(packet: dict[str, Any]) -> None:
    expected = {
        "object_type": "chunking_owner_decision_packet",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t385_owner_decision_packet.v1",
        "packet_id": "t385_owner_decision_packet_from_readiness",
        "task_id": "T385",
        "status": "pending_owner_decision",
        "owner": "Lowell Wong",
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            raise T385PacketError(f"{PACKET_REL}: {key} must be {value!r}")

    boundary = packet.get("orthodoxy_boundary")
    if not isinstance(boundary, dict):
        raise T385PacketError(f"{PACKET_REL}: orthodoxy_boundary must be a mapping")
    if boundary.get("default") != "nicene_chalcedonian_core":
        raise T385PacketError(f"{PACKET_REL}: orthodoxy boundary must be Nicene/Chalcedonian")
    if boundary.get("canonical_scripture_authority") is not True:
        raise T385PacketError(f"{PACKET_REL}: canonical Scripture authority must stay true")

    authority = packet.get("authority")
    if not isinstance(authority, dict):
        raise T385PacketError(f"{PACKET_REL}: authority must be a mapping")
    for key in ("records_owner_options", "records_recommendation", "records_repercussions", "records_readiness_inputs"):
        if authority.get(key) is not True:
            raise T385PacketError(f"{PACKET_REL}: authority.{key} must be true")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise T385PacketError(f"{PACKET_REL}: authority.{key} must be false")

    selection = packet.get("owner_selection")
    if not isinstance(selection, dict):
        raise T385PacketError(f"{PACKET_REL}: owner_selection must be a mapping")
    expected_selection = {
        "owner_selection_status": "pending",
        "selected_option": None,
        "selected_passage": None,
        "selected_lane": None,
        "selected_children": [],
        "exact_target_selected": False,
        "recommendation_is_owner_selection": False,
    }
    for key, value in expected_selection.items():
        if selection.get(key) != value:
            raise T385PacketError(f"{PACKET_REL}: owner_selection.{key} must be {value!r}")

    inputs = packet.get("readiness_inputs")
    if not isinstance(inputs, list):
        raise T385PacketError(f"{PACKET_REL}: readiness_inputs must be a list")
    input_ids = {item.get("input_id") for item in inputs if isinstance(item, dict)}
    for required in {"T384", "T386-summary", "T386-docket", "T387", "T388", "T389", "T390"}:
        if required not in input_ids:
            raise T385PacketError(f"{PACKET_REL}: readiness_inputs missing {required}")

    coverage = packet.get("coverage_basis")
    if not isinstance(coverage, dict):
        raise T385PacketError(f"{PACKET_REL}: coverage_basis must be a mapping")
    if coverage.get("canonical_scope") != "canonical_66":
        raise T385PacketError(f"{PACKET_REL}: coverage_basis.canonical_scope must be canonical_66")
    if coverage.get("canonical_passage_count") != 31103:
        raise T385PacketError(f"{PACKET_REL}: coverage_basis.canonical_passage_count must be 31103")
    if coverage.get("target_passage_lookup_required_before_strengthening") is not True:
        raise T385PacketError(f"{PACKET_REL}: target passage lookup must be required")

    options = packet.get("serious_faithful_options")
    if not isinstance(options, list):
        raise T385PacketError(f"{PACKET_REL}: serious_faithful_options must be a list")
    option_ids = {option.get("option_id") for option in options if isinstance(option, dict)}
    missing_options = sorted(REQUIRED_OPTION_IDS - option_ids)
    if missing_options:
        raise T385PacketError(f"{PACKET_REL}: missing options {missing_options}")
    for option in options:
        if not isinstance(option, dict):
            raise T385PacketError(f"{PACKET_REL}: each option must be a mapping")
        label = f"{PACKET_REL}:{option.get('option_id')}"
        for key in ("lane", "label", "why_serious", "upside", "downside_risk", "what_it_authorizes_if_owner_selects"):
            if not isinstance(option.get(key), str) or not option[key].strip():
                raise T385PacketError(f"{label}: {key} must be a non-empty string")
        if option.get("owner_selection_status") != "pending":
            raise T385PacketError(f"{label}: owner_selection_status must be pending")
        _require_subset({"source_metadata_sensitive"}, option.get("coverage_flags"), f"{label}.coverage_flags")
        _require_subset({"contextual_reading_policy_fields"} if option["option_id"] != "T385-I" else set(), option.get("required_controls_if_selected"), f"{label}.required_controls_if_selected")

    recommendation = packet.get("recommendation")
    if not isinstance(recommendation, dict):
        raise T385PacketError(f"{PACKET_REL}: recommendation must be a mapping")
    if recommendation.get("recommended_option_id") != "T385-A":
        raise T385PacketError(f"{PACKET_REL}: recommendation.recommended_option_id must be T385-A")
    if recommendation.get("recommended_passage") != "Eph.1.3-Eph.1.14":
        raise T385PacketError(f"{PACKET_REL}: recommendation.recommended_passage must be Eph.1.3-Eph.1.14")
    if "not an owner decision" not in str(recommendation.get("why_this_is_not_selection", "")):
        raise T385PacketError(f"{PACKET_REL}: recommendation must deny owner selection")

    next_gate = packet.get("next_goal_gate")
    if not isinstance(next_gate, dict):
        raise T385PacketError(f"{PACKET_REL}: next_goal_gate must be a mapping")
    if next_gate.get("goal_4_can_run_after") != "explicit_owner_selection_of_one_T385_option":
        raise T385PacketError(f"{PACKET_REL}: Goal 4 gate must require explicit owner selection")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, packet.get("non_authorizations"), "non_authorizations")
    if packet.get("decision_register_entry") != "CD-066":
        raise T385PacketError(f"{PACKET_REL}: decision_register_entry must be CD-066")
    lesson = packet.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-020":
        raise T385PacketError(f"{PACKET_REL}: lesson_recorded.lesson_id must be LSN-020")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-066", "T385 owner decision packet recommends but does not select", PACKET_REL)),
        (LESSON_INDEX, ("LSN-020", "Owner packet recommendation is not owner selection", "T385", PACKET_REL)),
        (PREFLIGHT, (PACKET_REL, "CD-066", "LSN-020")),
        (READINESS, ("prior_owner_packet:", "task_id: T385", PACKET_REL, "owner_selection_status: pending")),
        (ROADMAP, ("id: T385", "complete_owner_decision_packet_only", PACKET_REL)),
        (FRONT_DOOR, (PACKET_REL, VALIDATOR_REL, "T385 owner decision packet is complete")),
        (MAIN_TOC, (PACKET_REL, VALIDATOR_REL, "owner-decision-packet")),
        (ROADMAP_TOC, (PACKET_REL, DOC_REL, "T385 | Owner decision packet")),
        (ROADMAP_DOC, ("Recommended owner choice", "T385-A", "does not select a target")),
        (TASK, ("id: T385", "CD-066", "LSN-020")),
        (HANDOFF, ("task_id: T385", "CD-066", "T385-A")),
        (PROJECT_STATUS, ("T385 owner decision packet", "T385-A")),
        (CURRENT_FOCUS, ("current_task: T392", PACKET_REL)),
        (VALIDATE_ALL, ("validate_t385_owner_decision_packet.py",)),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T385PacketError(f"{_rel(path)}: missing {phrase!r}")


def validate_t385_owner_decision_packet(path: Path = PACKET) -> dict[str, Any]:
    packet = _read_yaml(path)
    _validate_static(packet)
    _validate_links()
    return packet


def main() -> int:
    try:
        validate_t385_owner_decision_packet()
    except T385PacketError as exc:
        print(f"T385 owner decision packet validation failed: {exc}", file=sys.stderr)
        return 1
    print("T385 owner decision packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
