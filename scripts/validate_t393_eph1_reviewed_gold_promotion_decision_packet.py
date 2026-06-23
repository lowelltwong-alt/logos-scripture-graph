#!/usr/bin/env python3
"""Validate the T393 Eph.1.3-Eph.1.14 reviewed-gold promotion decision packet."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / ".ai" / "control" / "t393_eph1_reviewed_gold_promotion_decision_packet.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md"
TASK = ROOT / ".ai" / "tasks" / "T393.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T393" / "handoff.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260623-T393-eph1-reviewed-gold-promotion-decision-packet.md"
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
PROMOTION_RECORD = ROOT / ".ai" / "control" / "t394_eph1_parent_only_reviewed_gold_promotion.yaml"

PACKET_REL = ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml"
PROMOTION_REL = ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml"
DOC_REL = "docs/roadmap/T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md"
VALIDATOR_REL = "scripts/validate_t393_eph1_reviewed_gold_promotion_decision_packet.py"
REVIEW_PACKET_REL = "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md"

REQUIRED_OPTION_IDS = {"T393-A", "T393-B", "T393-C", "T393-D", "T393-E"}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_owner_selection",
    "authorizes_reviewed_gold_promotion",
    "authorizes_parent_span_as_chunk_boundary",
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
    "owner_selection",
    "reviewed_gold_promotion",
    "parent_span_as_chunk_boundary",
    "child_span_selection",
    "child_span_reviewed_gold_promotion",
    "chunk_output_change",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "boundary_import",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "denominational_systematic_theology_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
    "recommendation_as_owner_selection",
    "current_sidecar_silence_as_universal_variant_claim",
    "source_metadata_as_boundary_authority",
    "original_language_word_as_boundary_authority",
}


class T393PacketError(ValueError):
    """Raised when T393 loses owner-gate, promotion, or non-authorization controls."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T393PacketError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T393PacketError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T393PacketError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T393PacketError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T393PacketError(f"{label} missing {missing}")


def _validate_packet(packet: dict[str, Any]) -> None:
    expected = {
        "object_type": "reviewed_gold_promotion_owner_decision_packet",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t393_reviewed_gold_promotion_owner_decision_packet.v1",
        "packet_id": "t393_eph1_reviewed_gold_promotion_decision_packet",
        "task_id": "T393",
        "status": "resolved_by_t393_a",
        "owner": "Lowell Wong",
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            raise T393PacketError(f"{PACKET_REL}: {key} must be {value!r}")

    boundary = packet.get("orthodoxy_boundary")
    if not isinstance(boundary, dict):
        raise T393PacketError(f"{PACKET_REL}: orthodoxy_boundary must be a mapping")
    if boundary.get("default") != "nicene_chalcedonian_core":
        raise T393PacketError(f"{PACKET_REL}: orthodoxy boundary must be Nicene/Chalcedonian")
    if boundary.get("canonical_scripture_authority") is not True:
        raise T393PacketError(f"{PACKET_REL}: canonical Scripture authority must stay true")

    authority = packet.get("authority")
    if not isinstance(authority, dict):
        raise T393PacketError(f"{PACKET_REL}: authority must be a mapping")
    for key in (
        "records_owner_options",
        "records_recommendation",
        "records_repercussions",
        "records_variant_dependency_assessment",
        "records_child_span_necessity_assessment",
    ):
        if authority.get(key) is not True:
            raise T393PacketError(f"{PACKET_REL}: authority.{key} must be true")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise T393PacketError(f"{PACKET_REL}: authority.{key} must be false")

    scope = packet.get("scope")
    if not isinstance(scope, dict):
        raise T393PacketError(f"{PACKET_REL}: scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "translation_scope": "eng-web",
        "lane": "epistle_argument",
        "target_id": "eph1_3_14_argument",
        "selected_option_from_t385": "T385-A",
        "strengthening_task": "T392",
        "review_packet": REVIEW_PACKET_REL,
        "selected_parent_candidate": "Eph.1.3-Eph.1.14",
        "prior_owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
        "prior_strengthening_report": "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md",
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T393PacketError(f"{PACKET_REL}: scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T393PacketError(f"{PACKET_REL}: scope.selected_children must be []")

    selection = packet.get("owner_selection")
    if not isinstance(selection, dict):
        raise T393PacketError(f"{PACKET_REL}: owner_selection must be a mapping")
    expected_selection = {
        "owner_selection_status": "selected",
        "selected_option": "T393-A",
        "selected_parent": "Eph.1.3-Eph.1.14",
        "selected_children": [],
        "reviewed_gold_promoted": False,
        "recommendation_is_owner_selection": False,
        "owner_response_record": PROMOTION_REL,
    }
    for key, value in expected_selection.items():
        if selection.get(key) != value:
            raise T393PacketError(f"{PACKET_REL}: owner_selection.{key} must be {value!r}")

    response = packet.get("owner_response")
    if not isinstance(response, dict):
        raise T393PacketError(f"{PACKET_REL}: owner_response must be a mapping")
    expected_response = {
        "response_status": "selected",
        "task_id": "T394",
        "selected_option": "T393-A",
        "owner_response_record": PROMOTION_REL,
        "exact_parent": "Eph.1.3-Eph.1.14",
        "selected_children": [],
        "exact_internal_variant_refs": [],
        "boundary_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "source_tradition_dependency_or_non_dependency": "current_repo_source_tradition_non_dependent",
        "child_span_necessity_or_denial": "child_spans_not_necessary_now_and_not_authorized",
        "parent_only_reviewed_gold_authorized_or_held": "authorized_parent_only_reviewed_gold",
        "decision_register_update": "CD-071",
    }
    for key, value in expected_response.items():
        if response.get(key) != value:
            raise T393PacketError(f"{PACKET_REL}: owner_response.{key} must be {value!r}")
    _require_subset(
        {
            "parent_span_as_chunk_boundary",
            "child_span_selection",
            "chunk_output_change",
            "route_behavior_change",
            "evaluator_change",
            "graph_edge_generation",
            "retrieval_truth",
            "embedding_or_vector_work",
            "boundary_import",
            "preferred_reading_selection",
            "source_tradition_preference",
            "canon_scope_change",
            "source_or_manuscript_row_population",
            "theology_authority_change",
        },
        response.get("explicit_non_authorizations"),
        "owner_response.explicit_non_authorizations",
    )

    evidence = packet.get("packet_evidence_summary")
    if not isinstance(evidence, dict):
        raise T393PacketError(f"{PACKET_REL}: packet_evidence_summary must be a mapping")
    expected_evidence = {
        "review_packet_status": "pending_human_review",
        "strengthened_by_task": "T392",
        "exact_passage_scope": "Eph.1.3-Eph.1.14",
        "contextual_reading_complete_for_current_packet": True,
        "premortem_red_team_complete": True,
        "exact_internal_variant_refs": [],
        "variant_dependency_non_authorizing_assessment": "current_repo_variant_non_dependent_for_parent_boundary_and_reviewed_gold_claim",
        "child_span_necessity_non_authorizing_assessment": "child_spans_not_necessary_for_parent_only_reviewed_gold_now",
    }
    for key, value in expected_evidence.items():
        if evidence.get(key) != value:
            raise T393PacketError(f"{PACKET_REL}: packet_evidence_summary.{key} must be {value!r}")

    question = packet.get("owner_question")
    if not isinstance(question, dict):
        raise T393PacketError(f"{PACKET_REL}: owner_question must be a mapping")
    if question.get("decision_id") != "T393_EPH1_REVIEWED_GOLD_PROMOTION":
        raise T393PacketError(f"{PACKET_REL}: owner_question.decision_id is wrong")
    _require_subset(
        {
            "selected_option",
            "exact_parent",
            "selected_children",
            "boundary_dependency_or_non_dependency",
            "reviewed_gold_dependency_or_non_dependency",
            "child_span_necessity_or_denial",
            "parent_only_reviewed_gold_authorized_or_held",
            "explicit_non_authorizations",
            "decision_register_update",
            "validators_tests",
        },
        question.get("owner_response_must_record"),
        "owner_question.owner_response_must_record",
    )
    if question.get("must_stop_if_owner_response_is_ambiguous") is not True:
        raise T393PacketError(f"{PACKET_REL}: ambiguous owner response must stop")

    options = packet.get("owner_options")
    if not isinstance(options, list):
        raise T393PacketError(f"{PACKET_REL}: owner_options must be a list")
    option_ids = {option.get("option_id") for option in options if isinstance(option, dict)}
    missing_options = sorted(REQUIRED_OPTION_IDS - option_ids)
    if missing_options:
        raise T393PacketError(f"{PACKET_REL}: missing options {missing_options}")
    for option in options:
        if not isinstance(option, dict):
            raise T393PacketError(f"{PACKET_REL}: each owner option must be a mapping")
        label = f"{PACKET_REL}:{option.get('option_id')}"
        for key in (
            "label",
            "owner_action",
            "downstream_effect_if_selected",
            "theological_risk_if_selected",
            "variant_dependency_if_selected",
            "child_span_decision_if_selected",
        ):
            if not isinstance(option.get(key), str) or not option[key].strip():
                raise T393PacketError(f"{label}: {key} must be a non-empty string")
        for key in ("if_selected_authorizes_child_spans", "if_selected_authorizes_output_change", "if_selected_authorizes_route_behavior"):
            if option.get(key) is not False:
                raise T393PacketError(f"{label}: {key} must be false")

    by_id = {option["option_id"]: option for option in options}
    if by_id["T393-A"].get("if_selected_authorizes_parent_only_reviewed_gold") is not True:
        raise T393PacketError(f"{PACKET_REL}: T393-A must be the only promotion option")
    for option_id in REQUIRED_OPTION_IDS - {"T393-A"}:
        if by_id[option_id].get("if_selected_authorizes_parent_only_reviewed_gold") is not False:
            raise T393PacketError(f"{PACKET_REL}: {option_id} must not authorize reviewed gold")

    recommendation = packet.get("recommendation_for_owner_review")
    if not isinstance(recommendation, dict):
        raise T393PacketError(f"{PACKET_REL}: recommendation_for_owner_review must be a mapping")
    if recommendation.get("recommended_option_id") != "T393-A":
        raise T393PacketError(f"{PACKET_REL}: recommended option must be T393-A")
    if "not an owner decision" not in str(recommendation.get("why_not_auto_select", "")):
        raise T393PacketError(f"{PACKET_REL}: recommendation must deny owner selection")

    if not isinstance(packet.get("premortem_red_team"), list) or len(packet["premortem_red_team"]) < 5:
        raise T393PacketError(f"{PACKET_REL}: premortem_red_team must include at least five failure modes")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, packet.get("non_authorizations"), "non_authorizations")
    if packet.get("decision_register_entry") != "CD-068":
        raise T393PacketError(f"{PACKET_REL}: decision_register_entry must be CD-068")
    lesson = packet.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-022":
        raise T393PacketError(f"{PACKET_REL}: lesson_recorded.lesson_id must be LSN-022")
    _require_subset({VALIDATOR_REL, "tests/test_t393_eph1_reviewed_gold_promotion_decision_packet.py"}, packet.get("validators"), "validators")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-068", "T393 promotion decision packet does not promote reviewed gold", PACKET_REL)),
        (LESSON_INDEX, ("LSN-022", "Reviewed-gold promotion packets are not promotions", "related_decision_ids: [CD-068]")),
        (PREFLIGHT, (PACKET_REL, "CD-068", "LSN-022")),
        (READINESS, ("task_id: T393", PACKET_REL, "recommended_option: T393-A", "owner_selection_status: selected", PROMOTION_REL)),
        (ROADMAP, ("id: T393", "resolved_by_t393_a", PACKET_REL, PROMOTION_REL)),
        (FRONT_DOOR, ("T393", "Eph.1.3-Eph.1.14", "Goal 5", VALIDATOR_REL)),
        (MAIN_TOC, ("t393", "reviewed-gold-promotion-decision", PACKET_REL)),
        (ROADMAP_TOC, ("T393 | Eph.1.3-Eph.1.14 reviewed-gold promotion decision packet", DOC_REL)),
        (ROADMAP_DOC, ("Recommended option", "T393-A", "Resolved by T394")),
        (TASK, ("id: T393", "CD-068", "LSN-022")),
        (HANDOFF, ("task_id: T393", "T393-A", PACKET_REL)),
        (AUDIT, ("T393", "No reviewed gold is promoted", "No chunk output is implemented")),
        (PROJECT_STATUS, ("T393 Eph.1.3-Eph.1.14 reviewed-gold promotion decision packet", "Goal 5")),
        (CURRENT_FOCUS, ("current_task: T394", PROMOTION_REL)),
        (VALIDATE_ALL, ("validate_t393_eph1_reviewed_gold_promotion_decision_packet.py",)),
        (PROMOTION_RECORD, ("task_id: T394", "selected_option: T393-A", PACKET_REL)),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T393PacketError(f"{_rel(path)}: missing {phrase!r}")


def validate_t393_owner_decision_packet(path: Path = PACKET) -> dict[str, Any]:
    packet = _read_yaml(path)
    _validate_packet(packet)
    _validate_links()
    return packet


def main() -> int:
    try:
        validate_t393_owner_decision_packet()
    except T393PacketError as exc:
        print(f"T393 reviewed-gold promotion decision packet validation failed: {exc}", file=sys.stderr)
        return 1
    print("T393 reviewed-gold promotion decision packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
