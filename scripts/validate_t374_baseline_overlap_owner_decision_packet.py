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
        "status": "complete_owner_selected_additive_parent_overlay",
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
        "additive_overlay_owner_decision_recorded": True,
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
        expected_status = "selected_by_owner" if option.get("option_id") == "T374-OVERLAP-B" else "not_selected"
        if option.get("status") != expected_status:
            raise T374BaselineOverlapError(f"{_rel(path)}: {option.get('option_id')}.status must be {expected_status}")
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
    if selection.get("selected_option") != "T374-OVERLAP-B":
        raise T374BaselineOverlapError(f"{_rel(path)}: selected_option must be T374-OVERLAP-B")
    if set(selection.get("allowed_option_ids", [])) != EXPECTED_OPTIONS:
        raise T374BaselineOverlapError(f"{_rel(path)}: allowed_option_ids are stale")
    _require_subset(REQUIRED_SELECTION_FIELDS, selection.get("must_record_before_implementation_resumes"), "must_record_before_implementation_resumes")
    recorded = selection.get("recorded_owner_selection")
    if not isinstance(recorded, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: recorded_owner_selection must be a mapping")
    if recorded.get("selected_option") != "T374-OVERLAP-B":
        raise T374BaselineOverlapError(f"{_rel(path)}: recorded_owner_selection.selected_option must be T374-OVERLAP-B")
    if recorded.get("decision_register_update") != "CD-055":
        raise T374BaselineOverlapError(f"{_rel(path)}: recorded_owner_selection.decision_register_update must be CD-055")

    owner_selection = data.get("owner_selection")
    if not isinstance(owner_selection, dict):
        raise T374BaselineOverlapError(f"{_rel(path)}: owner_selection must be a mapping")
    expected_owner_selection = {
        "selected_option": "T374-OVERLAP-B",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "selected_children": [],
        "output_semantics_authorized_for_future_implementation": "additive_parent_overlay_only",
        "preserve_existing_baseline_chunks_byte_identical": True,
        "delete_or_replace_existing_chunks_authorized": False,
        "duplicate_parent_coverage_allowed_for_exact_pilot": True,
        "adjacent_spill_splits_authorized": False,
        "implementation_must_be_separate_task": True,
        "chunk_output_changed_in_this_task": False,
        "route_behavior_changed_in_this_task": False,
        "decision_register_update": "CD-055",
        "post_pilot_child_necessity_review_required": True,
    }
    for key, value in expected_owner_selection.items():
        if owner_selection.get(key) != value:
            raise T374BaselineOverlapError(f"{_rel(path)}: owner_selection.{key} must be {value!r}")
    _require_subset(REQUIRED_NON_AUTHS, data.get("non_authorizations"), "non_authorizations")
    _require_subset({VALIDATOR_REL, "tests/test_t374_baseline_overlap_owner_decision_packet.py"}, data.get("validators"), "validators")

    links = data.get("links")
    if not isinstance(links, dict) or links.get("decision_register_entry") != "CD-055":
        raise T374BaselineOverlapError(f"{_rel(path)}: links.decision_register_entry must be CD-055")
    if links.get("prior_decision_register_entry") != "CD-054":
        raise T374BaselineOverlapError(f"{_rel(path)}: links.prior_decision_register_entry must be CD-054")

    return data


def _validate_links() -> None:
    for linked in (REGISTER, PREFLIGHT, READINESS, ROADMAP, FRONT_DOOR, TOC, ROADMAP_TOC, TASK, ROADMAP_DOC):
        if not linked.exists():
            raise T374BaselineOverlapError(f"{_rel(linked)}: missing linked surface")

    linked_requirements = (
        (REGISTER, ("CD-054", "CD-055", PACKET_REL, "T374-OVERLAP-B selects additive parent overlay semantics")),
        (PREFLIGHT, (PACKET_REL, "CD-055", "T374-OVERLAP-B")),
        (READINESS, (PACKET_REL, "task_id: T376", "t375_post_pilot_review_complete_next_lane_selection_required")),
        (ROADMAP, ("id: T374", "status: complete_output_changed_additive_parent_overlay", PACKET_REL)),
        (FRONT_DOOR, (PACKET_REL, "baseline overlap", "T374-OVERLAP-B")),
        (TOC, (PACKET_REL, "baseline-overlap", VALIDATOR_REL)),
        (ROADMAP_TOC, ("T374 | Additive parent overlay implementation", PACKET_REL, "owner-selection", VALIDATOR_REL)),
        (TASK, ("id: T374", PACKET_REL, "complete_output_changed_additive_parent_overlay")),
        (ROADMAP_DOC, ("T374 Baseline-Overlap Owner Decision Packet", PACKET_REL, "T374-OVERLAP-B", "preserving all existing baseline chunks byte-identical")),
    )
    for linked, phrases in linked_requirements:
        text = _read_text(linked)
        for phrase in phrases:
            if phrase not in text:
                raise T374BaselineOverlapError(f"{_rel(linked)}: missing {phrase!r}")

    readiness = _read_yaml(READINESS)
    next_route = readiness.get("next_route")
    if not isinstance(next_route, dict) or next_route.get("task_id") not in {"T374", "T375", "T376", "T384", "T385", "T392", "T393", "T397", "T401"}:
        raise T374BaselineOverlapError(f"{_rel(READINESS)}: next_route.task_id must be T374, T375, T376, T384, T385, T392, T393, T397, or T401")
    if next_route.get("task_id") in {"T374", "T375"}:
        expected_next = {
            "baseline_overlap_decision_packet": PACKET_REL,
            "baseline_overlap_status": "complete_owner_selected_additive_parent_overlay",
            "implementation_paused_until_owner_selects_baseline_overlap_option": False,
            "selected_baseline_overlap_option": "T374-OVERLAP-B",
            "additive_parent_overlay_selected": True,
            "preserve_existing_baseline_chunks_byte_identical": True,
            "delete_or_replace_existing_chunks_authorized": False,
            "duplicate_parent_coverage_allowed_for_exact_pilot": True,
            "adjacent_spill_splits_authorized": False,
            "replacement_style_implementation_paused": True,
            "replacement_safe_without_new_owner_decision": False,
            "additive_overlay_requires_owner_decision": True,
            "additive_overlay_owner_decision_recorded": True,
        }
        for key, value in expected_next.items():
            if next_route.get(key) != value:
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: next_route.{key} must be {value!r}")
    if next_route.get("task_id") == "T375":
        if next_route.get("implementation_manifest") != ".ai/control/t374_additive_parent_overlay_manifest.yaml":
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T375 next_route implementation manifest is stale")
        if next_route.get("additive_parent_overlay_implemented") is not True:
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T375 must record the T374 overlay as implemented")
    if next_route.get("task_id") == "T376":
        if next_route.get("starts_only_if") != "T375_post_pilot_review_complete":
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T376 starts_only_if is stale")
        if next_route.get("prior_implementation_manifest") != ".ai/control/t374_additive_parent_overlay_manifest.yaml":
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T376 prior_implementation_manifest is stale")
        if "CD-057" not in next_route.get("prior_decision_register_entries", []):
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T376 must reference CD-057")
        result = next_route.get("t375_result", {})
        if result.get("child_span_result") != "child_spans_not_necessary_now":
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T376 t375_result.child_span_result is stale")
        if result.get("selected_children") != []:
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T376 t375_result.selected_children must be []")
    if next_route.get("task_id") == "T384":
        expected_t384 = {
            "starts_only_if": "T376_A_epistle_argument_research_runway_selected",
            "prior_lane_selection": ".ai/control/t376_epistle_research_runway.yaml",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "route_type": "bible_wide_research_readiness_synthesis",
            "selected_t376_option": "T376-A",
            "selected_lane": "epistle_argument",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t384.items():
            if next_route.get(key) != value:
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: T384 next_route.{key} must be {value!r}")
        if "CD-060" not in next_route.get("prior_decision_register_entries", []):
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T384 must reference CD-060")
    if next_route.get("task_id") == "T385":
        expected_t385 = {
            "starts_only_if": "T384_bible_wide_research_readiness_synthesis_complete_and_T386_coverage_complete",
            "route_type": "owner_decision_packet_only",
            "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
            "completion_status": "complete_owner_decision_packet_only",
            "owner_selection_status": "pending",
            "recommended_option": "T385-A",
            "recommendation_is_owner_selection": False,
            "exact_target_selected": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t385.items():
            if next_route.get(key) != value:
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: T385 next_route.{key} must be {value!r}")
        if "CD-066" not in next_route.get("prior_decision_register_entries", []):
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T385 must reference CD-066")
    if next_route.get("task_id") == "T392":
        expected_t392 = {
            "starts_only_if": "explicit_owner_selection_of_T385_A",
            "route_type": "epistle_argument_review_packet_strengthening",
            "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
            "completion_status": "complete_review_packet_strengthening_only",
            "selected_option": "T385-A",
            "review_packet_strengthened": True,
            "exact_next_owner_action": "Goal5_owner_reviewed_gold_promotion_decision_packet",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected_for_promotion_or_implementation": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t392.items():
            if next_route.get(key) != value:
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: T392 next_route.{key} must be {value!r}")
        if "CD-067" not in next_route.get("prior_decision_register_entries", []):
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T392 must reference CD-067")
    if next_route.get("task_id") == "T393":
        expected_t393 = {
            "starts_only_if": "T392_eph1_review_packet_strengthening_complete",
            "route_type": "epistle_argument_owner_reviewed_gold_promotion_decision_packet",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "completion_status": "pending_owner_reviewed_gold_promotion_decision",
            "owner_selection_status": "pending",
            "recommended_option": "T393-A",
            "recommendation_is_owner_selection": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t393.items():
            if next_route.get(key) != value:
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: T393 next_route.{key} must be {value!r}")
        if "CD-068" not in next_route.get("prior_decision_register_entries", []):
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T393 must reference CD-068")
    if next_route.get("task_id") == "T397":
        expected_t397 = {
            "starts_only_if": "T394_eph1_parent_only_reviewed_gold_promoted",
            "route_type": "epistle_argument_goal6_route_isolation_harness_prep",
            "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "completion_status": "complete_non_output_changing_route_isolation_harness_prep",
            "owner_selection_status": "selected",
            "selected_option": "T393-A",
            "reviewed_gold_promoted": True,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
            "source_or_manuscript_rows_authorized": False,
        }
        for key, value in expected_t397.items():
            if next_route.get(key) != value:
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: T397 next_route.{key} must be {value!r}")
        if "CD-071" not in next_route.get("prior_decision_register_entries", []):
            raise T374BaselineOverlapError(f"{_rel(READINESS)}: T397 must reference CD-071")
    if next_route.get("task_id") == "T401":
        expected_t401 = {
            "starts_only_if": "T397_route_isolation_harness_complete_and_owner_authorized_exact_output_pilot",
            "route_type": "epistle_argument_goal7_exact_output_pilot",
            "completion_status": "complete_output_changed_eph1_parent_overlay",
            "output_manifest": ".ai/control/t401_eph1_output_pilot_manifest.yaml",
            "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "reviewed_gold_promoted": True,
            "output_change_authorized": True,
            "implementation_authorized": True,
            "route_behavior_authorized": True,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
            "source_or_manuscript_rows_authorized": False,
            "exact_next_owner_action": "T402_post_pilot_review_before_child_spans_or_broader_behavior",
        }
        for key, value in expected_t401.items():
            if next_route.get(key) != value:
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: T401 next_route.{key} must be {value!r}")
        for required in ("CD-071", "CD-074", "CD-076"):
            if required not in next_route.get("prior_decision_register_entries", []):
                raise T374BaselineOverlapError(f"{_rel(READINESS)}: T401 must reference {required}")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    by_id = {item.get("id"): item for item in future if isinstance(item, dict)}
    t374 = by_id.get("T374")
    if not isinstance(t374, dict):
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 roadmap entry missing")
    if t374.get("status") not in {"ready_owner_selected_additive_parent_overlay", "complete_output_changed_additive_parent_overlay"}:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 status is stale")
    if t374.get("baseline_overlap_decision_packet") != PACKET_REL:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 baseline packet is stale")
    if t374.get("implementation_paused_until_owner_selects_baseline_overlap_option") is not False:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 owner-selection pause must be resolved")
    if t374.get("selected_baseline_overlap_option") != "T374-OVERLAP-B":
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 selected_baseline_overlap_option must be T374-OVERLAP-B")
    if t374.get("preserve_existing_baseline_chunks_byte_identical") is not True:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 must preserve baseline chunks byte-identical")
    if t374.get("delete_or_replace_existing_chunks_authorized") is not False:
        raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 must not authorize delete/replace")
    if t374.get("status") == "ready_owner_selected_additive_parent_overlay":
        if t374.get("chunk_output_changed_in_this_task") is not False:
            raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: T374 packet task must not change chunk output")
    else:
        if t374.get("chunk_output_changed_in_this_task") is not True:
            raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: implemented T374 must record chunk output change")
        if t374.get("implementation_manifest") != ".ai/control/t374_additive_parent_overlay_manifest.yaml":
            raise T374BaselineOverlapError(f"{_rel(ROADMAP)}: implemented T374 manifest is stale")


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
