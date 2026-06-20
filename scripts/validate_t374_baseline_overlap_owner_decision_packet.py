#!/usr/bin/env python3
"""Validate the T374 baseline-overlap owner decision packet."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / ".ai" / "control" / "t374_baseline_overlap_owner_decision_packet.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
TASK = ROOT / ".ai" / "tasks" / "T374.task.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T374_BASELINE_OVERLAP_OWNER_DECISION_PACKET.md"

PACKET_REL = ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml"
VALIDATOR_REL = "scripts/validate_t374_baseline_overlap_owner_decision_packet.py"

EXPECTED_OBSERVED_WINDOW = [
    ("1Cor.4.6", "1Cor.6.8"),
    ("1Cor.6.9", "1Cor.7.24"),
    ("1Cor.7.25", "1Cor.9.2"),
    ("1Cor.9.3", "1Cor.10.5"),
    ("1Cor.10.6", "1Cor.11.10"),
    ("1Cor.11.11", "1Cor.12.11"),
    ("1Cor.12.12", "1Cor.14.5"),
]

EXPECTED_OPTIONS = {
    "T374-OVERLAP-A",
    "T374-OVERLAP-B",
    "T374-OVERLAP-C",
    "T374-OVERLAP-D",
    "T374-OVERLAP-E",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_chunk_output_change",
    "authorizes_implementation",
    "authorizes_route_behavior",
    "authorizes_child_spans",
    "authorizes_additive_overlay",
    "authorizes_replacement_split",
    "authorizes_target_widening",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_boundary_import",
    "authorizes_whole_bible_output_pass",
}

REQUIRED_SELECTION_FIELDS = {
    "exact_selected_option",
    "what_output_semantics_are_authorized",
    "what_non_target_identity_rule_applies",
    "whether_duplicate_parent_coverage_is_allowed",
    "whether_adjacent_spill_splits_are_allowed",
    "decision_register_update",
    "validators_and_tests",
}

REQUIRED_NON_AUTHS = {
    "option_packet_as_owner_selection",
    "recommendation_as_owner_selection",
    "output_change_without_selected_overlap_option",
    "implementation_without_selected_overlap_option",
    "additive_overlay_without_owner_selection",
    "replacement_split_without_owner_selection",
    "target_widening_without_new_reviewed_gold",
    "child_span_selection",
    "adjacent_spill_as_theological_boundary",
    "graph_edge_generation",
    "retrieval_truth",
    "whole_bible_output_pass",
}


class T374BaselineOverlapError(ValueError):
    """Raised when T374 baseline-overlap governance is stale or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T374BaselineOverlapError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T374BaselineOverlapError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise T374BaselineOverlapError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T374BaselineOverlapError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    missing = sorted(required - set(_string_list(actual, label)))
    if missing:
        raise T374BaselineOverlapError(f"{label} missing {missing}")


def _validate_packet(path: Path) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "t374_baseline_overlap_owner_decision_packet",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t374_baseline_overlap_owner_decision_packet.v1",
        "packet_id": "t374_1cor8_10_baseline_overlap_owner_decision_packet",
        "task_id": "T374",
        "status": "blocked_pending_owner_decision",
        "lane": "epistle_argument",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T374BaselineOverlapError(f"{_rel(path)}: {key} must be {value!r}")

    target = data.get("target")
    if not isinstance(target, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: target must be a mapping")
    if target.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise T374BaselineOverlapError(f"{_rel(path)}: target.selected_parent is stale")
    if target.get("selected_children") != []:
        raise T374BaselineOverlapError(f"{_rel(path)}: target.selected_children must be []")

    inspection = data.get("baseline_inspection")
    if not isinstance(inspection, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: baseline_inspection must be a mapping")
    if inspection.get("observed_chunk_count") != 1136:
        raise T374BaselineOverlapError(f"{_rel(path)}: observed_chunk_count must be 1136")
    observed = inspection.get("observed_window")
    if not isinstance(observed, list):
        raise T374BaselineOverlapError(f"{_rel(path)}: observed_window must be a list")
    observed_pairs = [(item.get("osis_start"), item.get("osis_end")) for item in observed if isinstance(item, dict)]
    if observed_pairs != EXPECTED_OBSERVED_WINDOW:
        raise T374BaselineOverlapError(f"{_rel(path)}: observed_window is stale")
    overlap_kinds = {item.get("overlap_kind") for item in inspection.get("target_overlap_chunks", []) if isinstance(item, dict)}
    if overlap_kinds != {"crosses_target_start", "fully_inside_target", "crosses_target_end"}:
        raise T374BaselineOverlapError(f"{_rel(path)}: target_overlap_chunks must record start, inside, and end overlap")

    finding = data.get("finding")
    if not isinstance(finding, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: finding must be a mapping")
    expected_finding = {
        "replacement_style_implementation_paused": True,
        "replacement_safe_without_new_owner_decision": False,
        "additive_overlay_requires_owner_decision": True,
        "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
    }
    for key, value in expected_finding.items():
        if finding.get(key) != value:
            raise T374BaselineOverlapError(f"{_rel(path)}: finding.{key} must be {value!r}")
    if "1Cor.7.25-1Cor.7.40" not in str(finding.get("reason", "")):
        raise T374BaselineOverlapError(f"{_rel(path)}: finding.reason must mention the 1Cor.7 spill")
    if "1Cor.11.1-1Cor.11.10" not in str(finding.get("reason", "")):
        raise T374BaselineOverlapError(f"{_rel(path)}: finding.reason must mention the 1Cor.11 spill")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_owner_options") is not True:
        raise T374BaselineOverlapError(f"{_rel(path)}: authority.records_owner_options must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T374BaselineOverlapError(f"{_rel(path)}: authority.{key} must be false")

    options = data.get("owner_options")
    if not isinstance(options, list):
        raise T374BaselineOverlapError(f"{_rel(path)}: owner_options must be a list")
    option_ids = {item.get("option_id") for item in options if isinstance(item, dict)}
    if option_ids != EXPECTED_OPTIONS:
        raise T374BaselineOverlapError(f"{_rel(path)}: owner_options must be {sorted(EXPECTED_OPTIONS)}")
    for option in options:
        if not isinstance(option, dict):
            raise T374BaselineOverlapError(f"{_rel(path)}: each option must be a mapping")
        for key in ("label", "upside", "downside", "downstream_effect", "theological_or_hermeneutic_risk", "faithfulness_rationale"):
            if not isinstance(option.get(key), str) or not option[key].strip():
                raise T374BaselineOverlapError(f"{_rel(path)}: {option.get('option_id')}.{key} is required")
        _string_list(option.get("what_it_would_authorize"), f"{option.get('option_id')}.what_it_would_authorize")
        _string_list(option.get("what_it_does_not_authorize"), f"{option.get('option_id')}.what_it_does_not_authorize")

    recommendation = data.get("recommendation")
    if not isinstance(recommendation, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: recommendation must be a mapping")
    if recommendation.get("recommended_if_owner_wants_output") != "T374-OVERLAP-B":
        raise T374BaselineOverlapError(f"{_rel(path)}: additive overlay must remain the conditional output recommendation")
    if recommendation.get("conservative_recommendation_if_any_doubt") != "T374-OVERLAP-A":
        raise T374BaselineOverlapError(f"{_rel(path)}: conservative hold must remain the doubt recommendation")
    if recommendation.get("recommendation_is_owner_selection") is not False:
        raise T374BaselineOverlapError(f"{_rel(path)}: recommendation must not be owner selection")

    selection = data.get("required_owner_selection_record")
    if not isinstance(selection, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: required_owner_selection_record must be a mapping")
    if selection.get("selected_option") != "pending_owner_selection":
        raise T374BaselineOverlapError(f"{_rel(path)}: selected_option must remain pending")
    if set(selection.get("allowed_option_ids", [])) != EXPECTED_OPTIONS:
        raise T374BaselineOverlapError(f"{_rel(path)}: allowed_option_ids are stale")
    _require_subset(REQUIRED_SELECTION_FIELDS, selection.get("must_record_before_implementation_resumes"), "must_record_before_implementation_resumes")
    _require_subset(REQUIRED_NON_AUTHS, data.get("non_authorizations"), "non_authorizations")
    _require_subset({VALIDATOR_REL, "tests/test_t374_baseline_overlap_owner_decision_packet.py"}, data.get("validators"), "validators")

    links = data.get("links")
    if not isinstance(links, dict) or links.get("decision_register_entry") != "CD-054":
        raise T374BaselineOverlapError(f"{_rel(path)}: links.decision_register_entry must be CD-054")

    return data


def _validate_links() -> None:
    for linked in (REGISTER, PREFLIGHT, READINESS, ROADMAP, FRONT_DOOR, TOC, ROADMAP_TOC, TASK, ROADMAP_DOC):
        if not linked.exists():
            raise T374BaselineOverlapError(f"{_rel(linked)}: missing linked surface")

    linked_requirements = (
        (REGISTER, ("CD-054", PACKET_REL, "T374 baseline-overlap output semantics require owner selection")),
        (PREFLIGHT, (PACKET_REL, "CD-054", "baseline-overlap")),
        (READINESS, (PACKET_REL, "implementation_paused_until_owner_selects_baseline_overlap_option: true", "selected_baseline_overlap_option: pending_owner_selection")),
        (ROADMAP, ("id: T374", "status: blocked_pending_owner_decision", PACKET_REL)),
        (FRONT_DOOR, (PACKET_REL, "baseline overlap", "Do not implement chunks until Lowell selects")),
        (TOC, (PACKET_REL, "baseline-overlap", VALIDATOR_REL)),
        (ROADMAP_TOC, ("T374 | Baseline-overlap owner decision packet", PACKET_REL, "baseline-overlap", VALIDATOR_REL)),
        (TASK, ("id: T374", PACKET_REL, "blocked_pending_owner_decision")),
        (ROADMAP_DOC, ("T374 Baseline-Overlap Owner Decision Packet", PACKET_REL, "T374-OVERLAP-B")),
    )
    for linked, phrases in linked_requirements:
        text = _read_text(linked)
        for phrase in phrases:
            if phrase not in text:
                raise T374BaselineOverlapError(f"{_rel(linked)}: missing {phrase!r}")

    readiness = _read_yaml(READINESS)
    next_route = readiness.get("next_route")
    if not isinstance(next_route, dict) or next_route.get("task_id") != "T374":
        raise T374BaselineOverlapError(f"{_rel(READINESS)}: next_route.task_id must be T374")
    expected_next = {
        "baseline_overlap_decision_packet": PACKET_REL,
        "baseline_overlap_status": "blocked_pending_owner_decision",
        "implementation_paused_until_owner_selects_baseline_overlap_option": True,
        "selected_baseline_overlap_option": "pending_owner_selection",
        "replacement_style_implementation_paused": True,
        "replacement_safe_without_new_owner_decision": False,
        "additive_overlay_requires_owner_decision": True,
    }
    for key, value in expected_next.items():
        if next_route.get(key) != value:
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: next_route.{key} must be {value!r}")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    by_id = {item.get("id"): item for item in future if isinstance(item, dict)}
    t374 = by_id.get("T374")
    if not isinstance(t374, dict):
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 roadmap entry missing")
    if t374.get("status") != "blocked_pending_owner_decision":
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 status must be blocked_pending_owner_decision")
    if t374.get("baseline_overlap_decision_packet") != PACKET_REL:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 baseline packet is stale")
    if t374.get("implementation_paused_until_owner_selects_baseline_overlap_option") is not True:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 must pause implementation")
    if t374.get("chunk_output_changed_in_this_task") is not False:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 packet task must not change chunk output")


def validate_t374_baseline_overlap_owner_decision_packet(path: Path = PACKET) -> dict[str, Any]:
    data = _validate_packet(path)
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t374_baseline_overlap_owner_decision_packet()
    except T374BaselineOverlapError as exc:
        print(f"T374 baseline-overlap owner decision packet validation failed: {exc}", file=sys.stderr)
        return 1
    print("T374 baseline-overlap owner decision packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
