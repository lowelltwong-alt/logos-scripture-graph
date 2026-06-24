#!/usr/bin/env python3
"""Validate the T372 route-isolation harness and non-target identity plan."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / ".ai" / "control" / "t372_route_isolation_harness_plan.yaml"
PROMOTION = ROOT / ".ai" / "control" / "t371_parent_only_reviewed_gold_promotion.yaml"
MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "epistle_argument_gold_manifest.json"
EVIDENCE = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_parent_only_evidence_packet.yaml"
REVIEW_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_food_offered_to_idols_review.md"
OWNER_DOCKET = ROOT / ".ai" / "control" / "1cor8_10_epistle_owner_review_docket.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
TASK = ROOT / ".ai" / "tasks" / "T372.task.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T372_ROUTE_ISOLATION_HARNESS_PLAN.md"

PLAN_REL = ".ai/control/t372_route_isolation_harness_plan.yaml"
PROMOTION_REL = ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
MANIFEST_REL = "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_parent_only_reviewed_gold_promotion",
    "authorizes_parent_span_as_chunk_boundary",
    "authorizes_child_spans",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_chunk_output_change",
    "authorizes_implementation",
}

REQUIRED_HARNESSES = {
    "T372-HARN-001",
    "T372-HARN-002",
    "T372-HARN-003",
    "T372-HARN-004",
    "T372-HARN-005",
    "T372-HARN-006",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "parent_only_gold_as_chunk_boundary",
    "child_span_selection",
    "argument_outline_as_child_boundary",
    "paragraph_marker_as_chunk_boundary",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "boundary_import",
    "noncanonical_source_authority",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "implementation_authority",
    "chunk_output_change",
    "improvement_claim",
    "leaderboard_update",
}

REQUIRED_BEFORE_T374 = {
    "T373_owner_implementation_authorization",
    "exact_scope_recorded",
    "decision_register_update_for_any_output_or_route_authority",
    "non_target_identity_proof",
    "same_baseline_evaluation_plan",
    "task_scope_for_any_output_changing_paths",
    "no_context_audit_surface_if_output_changes",
}


class T372HarnessPlanError(ValueError):
    """Raised when T372 harness planning is unsafe or stale."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T372HarnessPlanError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T372HarnessPlanError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T372HarnessPlanError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise T372HarnessPlanError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T372HarnessPlanError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    missing = sorted(required - set(_string_list(actual, label)))
    if missing:
        raise T372HarnessPlanError(f"{label} missing {missing}")


def _validate_plan(path: Path) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "route_isolation_harness_plan",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "route_isolation_harness_plan.v1",
        "plan_id": "t372_1cor8_10_route_isolation_harness_plan",
        "task_id": "T372",
        "status": "complete_non_output_changing_plan",
        "lane": "epistle_argument",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T372HarnessPlanError(f"{_rel(path)}: {key} must be {value!r}")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise T372HarnessPlanError(f"{_rel(path)}: scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "translation_scope": "eng-web",
        "target_id": "1cor8_10_food_offered_to_idols",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "reviewed_gold_kind": "parent_only_span",
        "promotion_record": PROMOTION_REL,
        "reviewed_gold_manifest": MANIFEST_REL,
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
        "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
        "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T372HarnessPlanError(f"{_rel(path)}: scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T372HarnessPlanError(f"{_rel(path)}: scope.selected_children must be []")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T372HarnessPlanError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_harness_plan") is not True:
        raise T372HarnessPlanError(f"{_rel(path)}: authority.records_harness_plan must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T372HarnessPlanError(f"{_rel(path)}: authority.{key} must be false")

    limits = data.get("reviewed_gold_input_limits")
    if not isinstance(limits, dict):
        raise T372HarnessPlanError(f"{_rel(path)}: reviewed_gold_input_limits must be a mapping")
    if limits.get("may_cite_parent_only_reviewed_gold_as_input") is not True:
        raise T372HarnessPlanError(f"{_rel(path)}: parent-only gold may be cited only as input")
    for key in (
        "may_treat_parent_span_as_output_chunk_boundary",
        "may_infer_child_spans",
        "may_use_argument_outline_as_child_boundary",
        "may_use_paragraph_markers_as_chunk_boundaries",
        "may_use_source_metadata_as_authority",
        "may_select_preferred_readings",
    ):
        if limits.get(key) is not False:
            raise T372HarnessPlanError(f"{_rel(path)}: reviewed_gold_input_limits.{key} must be false")
    if set(limits.get("exact_variant_refs", [])) != {"1Cor.9.20", "1Cor.10.9"}:
        raise T372HarnessPlanError(f"{_rel(path)}: exact_variant_refs must remain T371 refs")

    harnesses = data.get("planned_harnesses")
    if not isinstance(harnesses, list):
        raise T372HarnessPlanError(f"{_rel(path)}: planned_harnesses must be a list")
    by_id = {item.get("harness_id"): item for item in harnesses if isinstance(item, dict)}
    if set(by_id) != REQUIRED_HARNESSES:
        raise T372HarnessPlanError(f"{_rel(path)}: planned_harnesses must be {sorted(REQUIRED_HARNESSES)}")
    for harness_id, harness in by_id.items():
        if not str(harness.get("status", "")).startswith("planned_for_"):
            raise T372HarnessPlanError(f"{_rel(path)}: {harness_id}.status must be planned_for_*")
        _string_list(harness.get("must_fail_if"), f"{harness_id}.must_fail_if")

    gate = data.get("t373_owner_gate")
    if not isinstance(gate, dict):
        raise T372HarnessPlanError(f"{_rel(path)}: t373_owner_gate must be a mapping")
    if gate.get("next_task_id") != "T373":
        raise T372HarnessPlanError(f"{_rel(path)}: t373_owner_gate.next_task_id must be T373")
    if gate.get("owner_decision_required") is not True:
        raise T372HarnessPlanError(f"{_rel(path)}: T373 owner decision must be required")
    if gate.get("default_if_owner_unavailable") != "stop_before_implementation_or_output_change":
        raise T372HarnessPlanError(f"{_rel(path)}: T373 default must stop before implementation")
    _string_list(gate.get("owner_must_decide_before_any_implementation"), "t373_owner_gate.owner_must_decide")

    _require_subset(REQUIRED_BEFORE_T374, data.get("required_before_t374"), "required_before_t374")
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    _require_subset(
        {
            "scripts/validate_t372_route_isolation_harness_plan.py",
            "tests/test_t372_route_isolation_harness_plan.py",
            "scripts/validate_task_scope.py --task-id T372",
        },
        data.get("validators"),
        "validators",
    )
    return data


def _validate_links() -> None:
    for path in (
        PROMOTION,
        MANIFEST,
        EVIDENCE,
        REVIEW_PACKET,
        OWNER_DOCKET,
        REGISTER,
        PREFLIGHT,
        READINESS,
        FORECAST,
        ROADMAP,
        FRONT_DOOR,
        TOC,
        ROADMAP_TOC,
        TASK,
        ROADMAP_DOC,
    ):
        if not path.exists():
            raise T372HarnessPlanError(f"{_rel(path)}: missing linked surface")

    for path, phrases in (
        (REGISTER, ("CD-048", PLAN_REL, "T372 route-isolation harness plan is non-authorizing")),
        (PREFLIGHT, (PLAN_REL, "CD-048", "T372 route-isolation harness plan")),
        (READINESS, (PLAN_REL, "task_id: T375", "parallel_t372_route_isolation_harness_plan", "parallel_t373_owner_implementation_authorization")),
        (FORECAST, ("HDF-013", PLAN_REL, "T373")),
        (ROADMAP, ("id: T372", "status: complete", PLAN_REL, "starts_only_if: T372_route_isolation_harness_plan_complete")),
        (FRONT_DOOR, (PLAN_REL, "T372 route-isolation harness plan", "T373 owner implementation authorization")),
        (TOC, (PLAN_REL, "t372", "route-isolation", "non-target-identity")),
        (ROADMAP_TOC, ("T372", PLAN_REL, "Route-isolation harness plan")),
        (TASK, ("id: T372", PLAN_REL, "chunk_output_authorized: false")),
        (ROADMAP_DOC, ("T372 Route-Isolation Harness Plan", "T373 - Owner Implementation Authorization Gate")),
    ):
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T372HarnessPlanError(f"{_rel(path)}: missing {phrase!r}")

    readiness = _read_yaml(READINESS)
    next_route = readiness.get("next_route")
    if not isinstance(next_route, dict) or next_route.get("task_id") not in {"T373", "T374", "T375", "T376", "T384", "T385", "T392", "T393", "T397"}:
        raise T372HarnessPlanError(f"{_rel(READINESS)}: next_route.task_id must be T373, T374, T375, T376, T384, T385, T392, T393, or T397 after T372")
    if next_route.get("task_id") == "T373" and next_route.get("starts_only_if") != "T372_route_isolation_harness_plan_complete":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T373 starts_only_if is stale")
    if next_route.get("task_id") == "T374" and next_route.get("starts_only_if") != "T373_A_authorizes_exact_parent_only_output_pilot":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T374 starts_only_if is stale")
    if next_route.get("task_id") == "T375" and next_route.get("starts_only_if") != "T374_additive_parent_overlay_implemented":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T375 starts_only_if is stale")
    if next_route.get("task_id") == "T376" and next_route.get("starts_only_if") != "T375_post_pilot_review_complete":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T376 starts_only_if is stale")
    if next_route.get("task_id") == "T384" and next_route.get("starts_only_if") != "T376_A_epistle_argument_research_runway_selected":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T384 starts_only_if is stale")
    if next_route.get("task_id") == "T385" and next_route.get("starts_only_if") != "T384_bible_wide_research_readiness_synthesis_complete_and_T386_coverage_complete":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T385 starts_only_if is stale")
    if next_route.get("task_id") == "T392" and next_route.get("starts_only_if") != "explicit_owner_selection_of_T385_A":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T392 starts_only_if is stale")
    if next_route.get("task_id") == "T393" and next_route.get("starts_only_if") != "T392_eph1_review_packet_strengthening_complete":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T393 starts_only_if is stale")
    if next_route.get("task_id") == "T397" and next_route.get("starts_only_if") != "T394_eph1_parent_only_reviewed_gold_promoted":
        raise T372HarnessPlanError(f"{_rel(READINESS)}: T397 starts_only_if is stale")
    if next_route.get("task_id") in {"T373", "T374", "T375"} and next_route.get("harness_plan") != PLAN_REL:
        raise T372HarnessPlanError(f"{_rel(READINESS)}: next_route.harness_plan is stale")
    if next_route.get("task_id") == "T373":
        if next_route.get("owner_decision_required") is not True:
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T373 owner_decision_required must be true")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T373 next_route.{key} must be false")
    if next_route.get("task_id") == "T374":
        if next_route.get("authorization_record") != ".ai/control/t373_owner_implementation_authorization.yaml":
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T374 authorization_record is stale")
        if next_route.get("selected_children") != []:
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T374 selected_children must be []")
        for key in ("evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T374 next_route.{key} must be false")
    if next_route.get("task_id") == "T375":
        if next_route.get("implementation_manifest") != ".ai/control/t374_additive_parent_overlay_manifest.yaml":
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T375 implementation_manifest is stale")
        if next_route.get("selected_children") != []:
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T375 selected_children must be []")
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized", "evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T375 next_route.{key} must be false")
    if next_route.get("task_id") == "T376":
        if next_route.get("prior_post_pilot_review") != ".ai/control/t375_post_pilot_review.yaml":
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T376 prior_post_pilot_review is stale")
        result = next_route.get("t375_result", {})
        if result.get("child_span_result") != "child_spans_not_necessary_now":
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T376 t375_result.child_span_result is stale")
        if result.get("selected_children") != []:
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T376 t375_result.selected_children must be []")
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized", "evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T376 next_route.{key} must be false")
    if next_route.get("task_id") == "T384":
        expected_t384 = {
            "route_type": "bible_wide_research_readiness_synthesis",
            "prior_lane_selection": ".ai/control/t376_epistle_research_runway.yaml",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "selected_t376_option": "T376-A",
            "selected_lane": "epistle_argument",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected": False,
            "reviewed_gold_promoted": False,
            "child_spans_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t384.items():
            if next_route.get(key) != value:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T384 next_route.{key} must be {value!r}")
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized", "evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T384 next_route.{key} must be false")
    if next_route.get("task_id") == "T385":
        expected_t385 = {
            "route_type": "owner_decision_packet_only",
            "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
            "completion_status": "complete_owner_decision_packet_only",
            "owner_selection_status": "pending",
            "recommended_option": "T385-A",
            "recommendation_is_owner_selection": False,
            "reviewed_gold_promoted": False,
            "child_spans_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t385.items():
            if next_route.get(key) != value:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T385 next_route.{key} must be {value!r}")
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized", "evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T385 next_route.{key} must be false")
    if next_route.get("task_id") == "T392":
        expected_t392 = {
            "route_type": "epistle_argument_review_packet_strengthening",
            "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
            "completion_status": "complete_review_packet_strengthening_only",
            "selected_option": "T385-A",
            "review_packet_strengthened": True,
            "exact_next_owner_action": "Goal5_owner_reviewed_gold_promotion_decision_packet",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected_for_promotion_or_implementation": False,
            "reviewed_gold_promoted": False,
            "child_spans_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t392.items():
            if next_route.get(key) != value:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T392 next_route.{key} must be {value!r}")
        if "CD-067" not in next_route.get("prior_decision_register_entries", []):
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T392 must reference CD-067")
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized", "evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T392 next_route.{key} must be false")
    if next_route.get("task_id") == "T393":
        expected_t393 = {
            "route_type": "epistle_argument_owner_reviewed_gold_promotion_decision_packet",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "completion_status": "pending_owner_reviewed_gold_promotion_decision",
            "owner_selection_status": "pending",
            "recommended_option": "T393-A",
            "recommendation_is_owner_selection": False,
            "reviewed_gold_promoted": False,
            "child_spans_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t393.items():
            if next_route.get(key) != value:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T393 next_route.{key} must be {value!r}")
        if "CD-068" not in next_route.get("prior_decision_register_entries", []):
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T393 must reference CD-068")
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized", "evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T393 next_route.{key} must be false")
    if next_route.get("task_id") == "T397":
        expected_t397 = {
            "route_type": "epistle_argument_goal6_route_isolation_harness_prep",
            "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "completion_status": "complete_non_output_changing_route_isolation_harness_prep",
            "owner_selection_status": "selected",
            "selected_option": "T393-A",
            "reviewed_gold_promoted": True,
            "child_spans_authorized": False,
            "embedding_or_vector_work_allowed": False,
            "source_or_manuscript_rows_authorized": False,
        }
        for key, value in expected_t397.items():
            if next_route.get(key) != value:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T397 next_route.{key} must be {value!r}")
        if "CD-071" not in next_route.get("prior_decision_register_entries", []):
            raise T372HarnessPlanError(f"{_rel(READINESS)}: T397 must reference CD-071")
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized", "evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise T372HarnessPlanError(f"{_rel(READINESS)}: T397 next_route.{key} must be false")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    by_id = {item.get("id"): item for item in future if isinstance(item, dict)}
    t372 = by_id.get("T372")
    if not isinstance(t372, dict) or t372.get("status") != "complete":
        raise T372HarnessPlanError(f"{_rel(ROADMAP)}: T372 must be complete")
    if t372.get("harness_plan") != PLAN_REL:
        raise T372HarnessPlanError(f"{_rel(ROADMAP)}: T372 harness_plan is stale")
    t373 = by_id.get("T373")
    if not isinstance(t373, dict) or t373.get("starts_only_if") != "T372_route_isolation_harness_plan_complete":
        raise T372HarnessPlanError(f"{_rel(ROADMAP)}: T373 starts_only_if is stale")
    if t373.get("owner_decision_required") is not False:
        raise T372HarnessPlanError(f"{_rel(ROADMAP)}: T373 owner decision must be recorded after T373-A")
    if t373.get("authorization_record") != ".ai/control/t373_owner_implementation_authorization.yaml":
        raise T372HarnessPlanError(f"{_rel(ROADMAP)}: T373 authorization_record is stale")


def validate_t372_route_isolation_harness_plan(path: Path = PLAN) -> dict[str, Any]:
    data = _validate_plan(path)
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t372_route_isolation_harness_plan()
    except T372HarnessPlanError as exc:
        print(f"T372 route-isolation harness plan validation failed: {exc}", file=sys.stderr)
        return 1
    print("T372 route-isolation harness plan validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
