#!/usr/bin/env python3
"""Validate owner-decision projection policy and current projected decisions."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "owner_decision_projection_policy.yaml"
CASE_POLICY = ROOT / ".ai" / "control" / "textual_critical_case_policy.yaml"
DOCKET = ROOT / ".ai" / "control" / "1cor8_10_epistle_owner_review_docket.yaml"
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "policy_id",
    "owner",
    "authority",
    "projection_allowed_when",
    "projection_must_stop_when",
    "conflict_policy",
    "projectable_owner_patterns",
    "current_projected_decisions",
    "validators",
}

REQUIRED_PATTERNS = {"ODP-001", "ODP-002", "ODP-003", "ODP-004", "ODP-005"}
REQUIRED_ONECOR_PATTERNS = {"ODP-001", "ODP-002", "ODP-003", "ODP-004"}
REQUIRED_FALSE_AUTHORITY = {
    "authorizes_real_time_owner_decision_replacement",
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edge_generation",
    "authorizes_retrieval_truth",
    "authorizes_textual_critical_policy",
    "authorizes_boundary_import",
}


class ProjectionPolicyError(ValueError):
    """Raised when owner-decision projection policy is stale or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProjectionPolicyError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ProjectionPolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ProjectionPolicyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise ProjectionPolicyError(f"{label} must be a list")
    actual_set = {str(item) for item in actual}
    missing = sorted(required - actual_set)
    if missing:
        raise ProjectionPolicyError(f"{label} missing {missing}")


def _validate_policy(data: dict[str, Any], path: Path) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise ProjectionPolicyError(f"{_rel(path)}: missing top-level keys {missing}")
    if data["object_type"] != "owner_decision_projection_policy":
        raise ProjectionPolicyError(f"{_rel(path)}: object_type must be owner_decision_projection_policy")
    if data["trust_zone"] != "canonical":
        raise ProjectionPolicyError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise ProjectionPolicyError(f"{_rel(path)}: lifecycle_status must be active")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise ProjectionPolicyError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_projection_policy") is not True:
        raise ProjectionPolicyError(f"{_rel(path)}: authority.records_projection_policy must be true")
    if authority.get("records_projected_owner_pattern_decisions") is not True:
        raise ProjectionPolicyError(
            f"{_rel(path)}: authority.records_projected_owner_pattern_decisions must be true"
        )
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ProjectionPolicyError(f"{_rel(path)}: authority.{key} must be false")

    _require_subset(
        {
            "prior_owner_decisions_are_materially_same_shape",
            "projected_default_is_conservative_and_fail_closed",
            "projection_keeps_metadata_evidence_only",
            "projection_applies_textual_critical_case_policy_as_process_not_reading_preference",
            "projection_does_not_promote_reviewed_gold",
            "projection_does_not_change_chunks_routes_evaluators_graph_retrieval_vectors_or_outputs",
            "conflict_scan_finds_no_conflicting_owner_decisions_for_the_target_text",
        },
        data["projection_allowed_when"],
        "projection_allowed_when",
    )
    _require_subset(
        {
            "decision_pattern_is_new_or_not_materially_same_shape",
            "prior_owner_decisions_conflict_for_the_target_text",
            "projection_would_choose_child_spans_without_exact_owner_selection",
            "projection_would_select_textual_critical_policy_or_preferred_reading",
            "projection_would_skip_owner_confirmation_for_variant_sensitive_promotion",
            "projection_would_project_variant_dependency_or_non_dependency_for_a_specific_packet",
            "projection_would_change_any_output_or_default_runtime_behavior",
        },
        data["projection_must_stop_when"],
        "projection_must_stop_when",
    )

    conflict = data["conflict_policy"]
    if not isinstance(conflict, dict):
        raise ProjectionPolicyError(f"{_rel(path)}: conflict_policy must be a mapping")
    if conflict.get("conflict_scan_required_for_every_projected_decision") is not True:
        raise ProjectionPolicyError(f"{_rel(path)}: conflict scan must be required")
    if conflict.get("if_conflict_detected") != "stop_and_surface_to_owner_before_work_continues":
        raise ProjectionPolicyError(f"{_rel(path)}: conflicts must stop for owner review")
    _require_subset(
        {
            "target_text_or_passage",
            "prior_decisions_considered",
            "projected_pattern",
            "possible_conflicts_checked",
            "conflict_scan_result",
            "stop_or_continue_rationale",
        },
        conflict.get("required_conflict_report_fields"),
        "conflict_policy.required_conflict_report_fields",
    )

    patterns = data["projectable_owner_patterns"]
    if not isinstance(patterns, list) or not patterns:
        raise ProjectionPolicyError(f"{_rel(path)}: projectable_owner_patterns must be a non-empty list")
    pattern_ids = {str(item.get("pattern_id")) for item in patterns if isinstance(item, dict)}
    missing_patterns = sorted(REQUIRED_PATTERNS - pattern_ids)
    if missing_patterns:
        raise ProjectionPolicyError(f"{_rel(path)}: missing projectable patterns {missing_patterns}")
    odp_005 = next((item for item in patterns if isinstance(item, dict) and item.get("pattern_id") == "ODP-005"), None)
    if not isinstance(odp_005, dict):
        raise ProjectionPolicyError(f"{_rel(path)}: missing ODP-005")
    for phrase in ("TCP-T378-B", "case-by-case process rule", "owner confirmation", "validators/tests"):
        if phrase not in str(odp_005.get("rule", "")):
            raise ProjectionPolicyError(f"{_rel(path)}: ODP-005 rule missing {phrase!r}")
    for phrase in ("preferred reading", "source-tradition preference", "variant dependency", "reviewed-gold promotion"):
        if phrase not in str(odp_005.get("forbidden_projection", "")):
            raise ProjectionPolicyError(f"{_rel(path)}: ODP-005 forbidden_projection missing {phrase!r}")

    projected = data["current_projected_decisions"]
    if not isinstance(projected, list) or not projected:
        raise ProjectionPolicyError(f"{_rel(path)}: current_projected_decisions must be a non-empty list")
    by_id = {str(item.get("projection_id")): item for item in projected if isinstance(item, dict)}
    onecor = by_id.get("ODP-20260618-1COR8-10-PARENT")
    if not isinstance(onecor, dict):
        raise ProjectionPolicyError(f"{_rel(path)}: missing 1Cor.8-10 projected decision")
    if onecor.get("selected_option") != "1COR8-10-T369-B":
        raise ProjectionPolicyError(f"{_rel(path)}: 1Cor projection must select option B")
    if onecor.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise ProjectionPolicyError(f"{_rel(path)}: 1Cor projection parent is wrong")
    if onecor.get("selected_children") != []:
        raise ProjectionPolicyError(f"{_rel(path)}: 1Cor projection must not select child spans")
    if onecor.get("confidence") != "high":
        raise ProjectionPolicyError(f"{_rel(path)}: 1Cor projection confidence must be high")
    if onecor.get("conflict_scan_result") != "no_conflict_detected":
        raise ProjectionPolicyError(f"{_rel(path)}: 1Cor projection must have no-conflict scan")
    _require_subset(REQUIRED_ONECOR_PATTERNS, onecor.get("projected_pattern_ids"), "projected_pattern_ids")
    _require_subset(
        {
            "1cor8_10_parent_span_as_reviewed_gold",
            "1cor8_10_child_span_approval",
            "child_span_projection",
            "reviewed_gold_promotion",
            "chunk_output_change",
        },
        onecor.get("non_authorizations"),
        "1Cor projection non_authorizations",
    )


def _validate_governed_links() -> None:
    docket = _read_yaml(DOCKET)
    selection = docket.get("owner_selection", {})
    if selection.get("selection_mode") != "projected_owner_pattern":
        raise ProjectionPolicyError(f"{_rel(DOCKET)}: selection_mode must be projected_owner_pattern")
    if selection.get("selected_option") != "1COR8-10-T369-B":
        raise ProjectionPolicyError(f"{_rel(DOCKET)}: selected option must be 1COR8-10-T369-B")
    if selection.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise ProjectionPolicyError(f"{_rel(DOCKET)}: selected_parent is wrong")
    if selection.get("selected_children") != []:
        raise ProjectionPolicyError(f"{_rel(DOCKET)}: child spans must remain unselected")
    for key in ("implementation_allowed", "output_change_authorized", "reviewed_gold_promoted"):
        if selection.get(key) is not False:
            raise ProjectionPolicyError(f"{_rel(DOCKET)}: owner_selection.{key} must be false")

    forecast = _read_yaml(FORECAST)
    by_id = {
        item.get("decision_id"): item
        for item in forecast.get("front_loaded_decisions", [])
        if isinstance(item, dict)
    }
    hdf_001 = by_id.get("HDF-001")
    if not isinstance(hdf_001, dict):
        raise ProjectionPolicyError(f"{_rel(FORECAST)}: missing HDF-001")
    if hdf_001.get("status") != "projected_owner_pattern_selected":
        raise ProjectionPolicyError(f"{_rel(FORECAST)}: HDF-001 must be projected_owner_pattern_selected")
    if hdf_001.get("selected_option") != "1COR8-10-T369-B":
        raise ProjectionPolicyError(f"{_rel(FORECAST)}: HDF-001 selected_option is wrong")
    if hdf_001.get("conflict_scan_result") != "no_conflict_detected":
        raise ProjectionPolicyError(f"{_rel(FORECAST)}: HDF-001 conflict scan missing")

    readiness = _read_yaml(READINESS)
    next_route = readiness.get("next_route", {})
    next_task_id = next_route.get("task_id")
    if next_task_id not in {"T372", "T373", "T374", "T375", "T376", "T384", "T385", "T392"}:
        raise ProjectionPolicyError(f"{_rel(READINESS)}: next_route must be T372, T373, T374, T375, T376, T384, T385, or T392 after T371-A promotion")
    if next_task_id == "T372" and next_route.get("starts_only_if") != "T371_A_parent_only_reviewed_gold_promoted":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T372 starts_only_if is wrong")
    if next_task_id == "T373" and next_route.get("starts_only_if") != "T372_route_isolation_harness_plan_complete":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T373 starts_only_if is wrong")
    if next_task_id == "T374" and next_route.get("starts_only_if") != "T373_A_authorizes_exact_parent_only_output_pilot":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T374 starts_only_if is wrong")
    if next_task_id == "T375" and next_route.get("starts_only_if") != "T374_additive_parent_overlay_implemented":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T375 starts_only_if is wrong")
    if next_task_id == "T376" and next_route.get("starts_only_if") != "T375_post_pilot_review_complete":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T376 starts_only_if is wrong")
    if next_task_id == "T384" and next_route.get("starts_only_if") != "T376_A_epistle_argument_research_runway_selected":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T384 starts_only_if is wrong")
    if next_task_id == "T385" and next_route.get("starts_only_if") != "T384_bible_wide_research_readiness_synthesis_complete_and_T386_coverage_complete":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T385 starts_only_if is wrong")
    if next_task_id == "T392" and next_route.get("starts_only_if") != "explicit_owner_selection_of_T385_A":
        raise ProjectionPolicyError(f"{_rel(READINESS)}: T392 starts_only_if is wrong")
    if next_task_id not in {"T376", "T384", "T385", "T392"}:
        if (
            next_route.get("evidence_packet")
            != "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml"
        ):
            raise ProjectionPolicyError(f"{_rel(READINESS)}: {next_task_id} evidence_packet is stale")
        if next_route.get("promotion_record") != ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml":
            raise ProjectionPolicyError(f"{_rel(READINESS)}: {next_task_id} promotion_record is stale")
        if next_route.get("reviewed_gold_manifest") != "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json":
            raise ProjectionPolicyError(f"{_rel(READINESS)}: {next_task_id} reviewed_gold_manifest is stale")
    if next_task_id == "T372":
        if next_route.get("owner_decision_required") is not False:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T372 owner_decision_required must be false")
        if next_route.get("harness_only") is not True:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T372 harness_only must be true")
    if next_task_id == "T373":
        if next_route.get("owner_decision_required") is not True:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T373 owner_decision_required must be true")
        if next_route.get("harness_only") is not False:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T373 harness_only must be false")
        if next_route.get("harness_plan") != ".ai/control/t372_route_isolation_harness_plan.yaml":
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T373 harness_plan is stale")
    if next_task_id == "T374":
        if next_route.get("owner_decision_required") is not False:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T374 owner_decision_required must be false")
        if next_route.get("authorization_record") != ".ai/control/t373_owner_implementation_authorization.yaml":
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T374 authorization_record is stale")
        if next_route.get("selected_children") != []:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T374 selected_children must be []")
    if next_task_id == "T375":
        if next_route.get("implementation_manifest") != ".ai/control/t374_additive_parent_overlay_manifest.yaml":
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T375 implementation_manifest is stale")
        if next_route.get("additive_parent_overlay_implemented") is not True:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T375 additive_parent_overlay_implemented must be true")
        if next_route.get("selected_children") != []:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T375 selected_children must be []")
    if next_task_id == "T376":
        if next_route.get("prior_post_pilot_review") != ".ai/control/t375_post_pilot_review.yaml":
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T376 prior_post_pilot_review is stale")
        if next_route.get("owner_decision_required") is not True:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T376 owner_decision_required must be true")
        result = next_route.get("t375_result", {})
        if result.get("child_span_result") != "child_spans_not_necessary_now":
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T376 t375_result.child_span_result is stale")
        if result.get("selected_children") != []:
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T376 t375_result.selected_children must be []")
    if next_task_id == "T384":
        expected_t384 = {
            "route_type": "bible_wide_research_readiness_synthesis",
            "prior_lane_selection": ".ai/control/t376_epistle_research_runway.yaml",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "selected_t376_option": "T376-A",
            "selected_lane": "epistle_argument",
            "selection_mode": "bible_wide_research_readiness_complete_non_authorizing",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected": False,
            "reviewed_gold_promoted": False,
            "child_spans_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t384.items():
            if next_route.get(key) != value:
                raise ProjectionPolicyError(f"{_rel(READINESS)}: T384 {key} must be {value!r}")
        if "CD-060" not in next_route.get("prior_decision_register_entries", []):
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T384 must reference CD-060")
    if next_task_id == "T385":
        expected_t385 = {
            "route_type": "owner_decision_packet_only",
            "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
            "completion_status": "complete_owner_decision_packet_only",
            "owner_selection_status": "pending",
            "recommended_option": "T385-A",
            "recommendation_is_owner_selection": False,
            "exact_target_selected": False,
            "reviewed_gold_promoted": False,
            "child_spans_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
        for key, value in expected_t385.items():
            if next_route.get(key) != value:
                raise ProjectionPolicyError(f"{_rel(READINESS)}: T385 {key} must be {value!r}")
        if "CD-066" not in next_route.get("prior_decision_register_entries", []):
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T385 must reference CD-066")
    if next_task_id == "T392":
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
                raise ProjectionPolicyError(f"{_rel(READINESS)}: T392 {key} must be {value!r}")
        if "CD-067" not in next_route.get("prior_decision_register_entries", []):
            raise ProjectionPolicyError(f"{_rel(READINESS)}: T392 must reference CD-067")
    if next_task_id not in {"T376", "T384", "T385", "T392"} and next_route.get("reviewed_gold_promoted") is not True:
        raise ProjectionPolicyError(f"{_rel(READINESS)}: {next_task_id} reviewed_gold_promoted must be true")
    if next_task_id == "T374":
        for key in ("output_change_authorized", "implementation_authorized", "route_behavior_authorized"):
            if next_route.get(key) is not True:
                raise ProjectionPolicyError(f"{_rel(READINESS)}: T374 {key} must be true after explicit owner authorization")
        for key in ("evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise ProjectionPolicyError(f"{_rel(READINESS)}: T374 {key} must remain false")
    else:
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ProjectionPolicyError(f"{_rel(READINESS)}: {next_task_id} {key} must remain false")

    register_text = _read_text(REGISTER)
    for phrase in (
        "CD-039",
        "CD-040",
        "CD-041",
        "CD-042",
        "Owner decision projection policy allows conservative repeated-pattern decisions",
        "1 Corinthians 8-10 parent-only review target selected by projected owner pattern",
        "1 Corinthians 8-10 parent-only evidence packet remains non-authorizing",
    ):
        if phrase not in register_text:
            raise ProjectionPolicyError(f"{_rel(REGISTER)}: missing {phrase!r}")

    for path in (FRONT_DOOR, TOC):
        text = _read_text(path)
        for phrase in (
            "owner_decision_projection_policy.yaml",
            "conflict",
            "projected owner pattern",
            "ODP-005",
        ):
            if phrase not in text:
                raise ProjectionPolicyError(f"{_rel(path)}: missing {phrase!r}")

    case_policy = _read_yaml(CASE_POLICY)
    projection = case_policy.get("future_projection_memory", {})
    if projection.get("projectable_pattern_id") != "ODP-005":
        raise ProjectionPolicyError(f"{_rel(CASE_POLICY)}: projectable_pattern_id must be ODP-005")
    if projection.get("can_project_process_rule") is not True:
        raise ProjectionPolicyError(f"{_rel(CASE_POLICY)}: can_project_process_rule must be true")


def validate_owner_decision_projection_policy(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_policy(data, path)
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_owner_decision_projection_policy()
    except ProjectionPolicyError as exc:
        print(f"Owner decision projection policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("Owner decision projection policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
