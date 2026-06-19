#!/usr/bin/env python3
"""Validate the T371 variant-dependency owner decision packet."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / ".ai" / "control" / "t371_variant_dependency_owner_decision_packet.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
EVIDENCE_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_parent_only_evidence_packet.yaml"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_variant_dependency_finding",
    "authorizes_variant_non_dependency_finding",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_noncanonical_source_authority",
    "authorizes_reviewed_gold_promotion",
    "authorizes_parent_span_as_chunk_boundary",
    "authorizes_child_spans",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_chunk_output_change",
    "authorizes_implementation",
}

REQUIRED_OWNER_RESPONSE_FIELDS = {
    "selected_option",
    "exact_variant_refs",
    "boundary_dependency_or_non_dependency",
    "reviewed_gold_dependency_or_non_dependency",
    "parent_only_promotion_authorized_or_held",
    "explicit_non_authorizations",
    "decision_register_update",
    "validators_tests",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "variant_dependency_finding",
    "variant_non_dependency_finding",
    "preferred_reading_selection",
    "critical_text_default",
    "majority_text_default",
    "textus_receptus_default",
    "current_source_as_hidden_textual_policy",
    "source_tradition_preference",
    "canon_scope_change",
    "boundary_import",
    "noncanonical_source_authority",
    "reviewed_gold_promotion",
    "parent_span_as_chunk_boundary",
    "child_span_selection",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "chunk_output_change",
    "implementation_authority",
}


class T371PacketError(ValueError):
    """Raised when the T371 decision packet becomes unsafe or stale."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T371PacketError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T371PacketError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T371PacketError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise T371PacketError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T371PacketError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    actual_set = set(_string_list(actual, label))
    missing = sorted(required - actual_set)
    if missing:
        raise T371PacketError(f"{label} missing {missing}")


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise T371PacketError(f"{label} must be a non-empty string")


def validate_t371_variant_dependency_owner_decision_packet(path: Path = PACKET) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "variant_dependency_owner_decision_packet",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "variant_dependency_owner_decision_packet.v1",
        "packet_id": "t371_1cor8_10_variant_dependency_owner_decision_packet",
        "prepared_by_task": "T380",
        "target_owner_task": "T371",
        "status": "pending_owner_decision",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T371PacketError(f"{_rel(path)}: {key} must be {value!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T371PacketError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_owner_decision_options", "records_non_authorizing_agent_assessment"):
        if authority.get(key) is not True:
            raise T371PacketError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T371PacketError(f"{_rel(path)}: authority.{key} must be false")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise T371PacketError(f"{_rel(path)}: scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "translation_scope": "eng-web",
        "lane": "epistle_argument",
        "target_id": "1cor8_10_food_offered_to_idols",
        "selected_option_from_t369": "1COR8-10-T369-B",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "evidence_scope": "parent_only",
        "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
        "textual_critical_case_policy": ".ai/control/textual_critical_case_policy.yaml",
        "selected_textual_critical_policy": "TCP-T378-B",
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T371PacketError(f"{_rel(path)}: scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T371PacketError(f"{_rel(path)}: selected_children must remain empty")

    question = data.get("owner_question")
    if not isinstance(question, dict):
        raise T371PacketError(f"{_rel(path)}: owner_question must be a mapping")
    if question.get("decision_id") != "T371_VARIANT_DEPENDENCY_AND_PARENT_PROMOTION":
        raise T371PacketError(f"{_rel(path)}: owner_question.decision_id is stale")
    exact_question = str(question.get("exact_question", ""))
    for phrase in ("variant-non-dependent", "1Cor.9.20", "1Cor.10.9", "parent-only", "no output change"):
        if phrase not in exact_question:
            raise T371PacketError(f"{_rel(path)}: exact_question missing {phrase!r}")
    _require_subset(REQUIRED_OWNER_RESPONSE_FIELDS, question.get("owner_response_must_record"), "owner_response_must_record")
    if question.get("must_stop_if_owner_response_is_ambiguous") is not True:
        raise T371PacketError(f"{_rel(path)}: ambiguous owner response must stop")

    variants = data.get("variant_dependency_review")
    if not isinstance(variants, list):
        raise T371PacketError(f"{_rel(path)}: variant_dependency_review must be a list")
    by_ref = {item.get("ref"): item for item in variants if isinstance(item, dict)}
    if set(by_ref) != {"1Cor.9.20", "1Cor.10.9"}:
        raise T371PacketError(f"{_rel(path)}: exact variant refs must be 1Cor.9.20 and 1Cor.10.9")
    for ref, item in by_ref.items():
        for key in (
            "source_surface",
            "variant_note_summary",
            "theological_or_boundary_risk",
            "owner_dependency_question",
            "non_authorizing_agent_assessment",
        ):
            _require_string(item.get(key), f"{ref}.{key}")
        if item.get("still_requires_owner_confirmation") is not True:
            raise T371PacketError(f"{_rel(path)}: {ref} still_requires_owner_confirmation must be true")

    options = data.get("owner_options")
    if not isinstance(options, list):
        raise T371PacketError(f"{_rel(path)}: owner_options must be a list")
    by_option = {item.get("option_id"): item for item in options if isinstance(item, dict)}
    if set(by_option) != {"T371-A", "T371-B", "T371-C", "T371-D"}:
        raise T371PacketError(f"{_rel(path)}: owner_options must be exactly T371-A through T371-D")
    if by_option["T371-A"].get("if_selected_authorizes_parent_only_reviewed_gold") is not True:
        raise T371PacketError(f"{_rel(path)}: T371-A must be the only parent-only promotion option")
    for option_id, option in by_option.items():
        if option.get("if_selected_authorizes_child_spans") is not False:
            raise T371PacketError(f"{_rel(path)}: {option_id} must not authorize child spans")
        if option.get("if_selected_authorizes_output_change") is not False:
            raise T371PacketError(f"{_rel(path)}: {option_id} must not authorize output change")
        if option_id != "T371-A" and option.get("if_selected_authorizes_parent_only_reviewed_gold") is not False:
            raise T371PacketError(f"{_rel(path)}: {option_id} must not authorize reviewed gold")

    recommendation = data.get("recommendation_for_owner_review")
    if not isinstance(recommendation, dict):
        raise T371PacketError(f"{_rel(path)}: recommendation_for_owner_review must be a mapping")
    if recommendation.get("recommended_if_owner_agrees_with_variant_non_dependency") != "T371-A":
        raise T371PacketError(f"{_rel(path)}: recommendation must point to T371-A conditionally")
    if recommendation.get("conservative_hold_if_any_doubt") != "T371-B":
        raise T371PacketError(f"{_rel(path)}: conservative hold must be T371-B")
    for phrase in ("narrowest progress path", "if the owner confirms", "denying preferred readings"):
        if phrase not in str(recommendation.get("rationale", "")):
            raise T371PacketError(f"{_rel(path)}: recommendation rationale missing {phrase!r}")
    if "forbids projecting" not in str(recommendation.get("why_not_auto_select", "")):
        raise T371PacketError(f"{_rel(path)}: why_not_auto_select must mention projection limits")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    _validate_links()
    return data


def _validate_links() -> None:
    packet_rel = ".ai/control/t371_variant_dependency_owner_decision_packet.yaml"
    for path in (REGISTER, PREFLIGHT, READINESS, FORECAST, ROADMAP, FRONT_DOOR, TOC, ROADMAP_TOC, EVIDENCE_PACKET):
        if not path.exists():
            raise T371PacketError(f"{_rel(path)}: missing linked surface")

    evidence_text = _read_text(EVIDENCE_PACKET)
    for phrase in ("1Cor.9.20", "1Cor.10.9", "review_status: ready_for_owner_promotion_review"):
        if phrase not in evidence_text:
            raise T371PacketError(f"{_rel(EVIDENCE_PACKET)}: missing {phrase!r}")

    for path, phrases in (
        (REGISTER, ("CD-046", "T380", packet_rel)),
        (PREFLIGHT, (packet_rel, "CD-046")),
        (READINESS, (packet_rel, "owner_decision_packet", "T371")),
        (FORECAST, ("T380", packet_rel, "T371")),
        (FRONT_DOOR, (packet_rel, "T371 owner-decision packet")),
        (TOC, (packet_rel, "variant-dependency", "owner-decision")),
        (ROADMAP_TOC, ("T380", packet_rel, "T371 owner decision packet")),
    ):
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T371PacketError(f"{_rel(path)}: missing {phrase!r}")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    by_id = {item.get("id"): item for item in future if isinstance(item, dict)}
    t380 = by_id.get("T380")
    if not isinstance(t380, dict) or t380.get("status") != "complete":
        raise T371PacketError(f"{_rel(ROADMAP)}: T380 must be complete")
    if t380.get("owner_decision_packet") != packet_rel:
        raise T371PacketError(f"{_rel(ROADMAP)}: T380 owner_decision_packet is stale")
    t371 = by_id.get("T371")
    if not isinstance(t371, dict) or t371.get("blocked_until") != "T371_owner_variant_dependency_and_parent_promotion_decision":
        raise T371PacketError(f"{_rel(ROADMAP)}: T371 must remain blocked until owner decision")
    if t371.get("owner_decision_packet") != packet_rel:
        raise T371PacketError(f"{_rel(ROADMAP)}: T371 must link owner decision packet")


def main() -> int:
    try:
        validate_t371_variant_dependency_owner_decision_packet()
    except T371PacketError as exc:
        print(f"T371 variant-dependency owner decision packet validation failed: {exc}", file=sys.stderr)
        return 1
    print("T371 variant-dependency owner decision packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
