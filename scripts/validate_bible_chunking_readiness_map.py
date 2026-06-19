#!/usr/bin/env python3
"""Validate the Bible-wide chunking readiness map."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "map_id",
    "owner",
    "authority",
    "faithful_execution_model",
    "lessons_storage",
    "current_baseline",
    "algorithm_readiness",
    "lane_sequence",
    "next_route",
    "update_triggers",
    "explicit_non_authorizations",
}

REQUIRED_LANES = {
    "psalms_poetry",
    "revelation_apocalyptic",
    "epistle_argument",
    "narrative_pericope",
    "wisdom_dialogue",
    "prophetic_oracle",
    "gospel_discourse_wj",
    "textual_variant_source_tradition",
    "bible_wide_orchestration",
}

REQUIRED_ALGORITHMS = {
    "monolith_fallback",
    "form_detector",
    "orchestrator",
    "psalm_candidate_skill",
    "revelation_skill",
}

REQUIRED_LESSON_SURFACES = {
    ".ai/control/chunking_theological_decision_register.yaml",
    "docs/methodology/WORKFLOW_LESSONS.md",
    "docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md",
    "docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md",
    ".ai/control/bible_wide_chunking_research_registry.yaml",
    ".ai/control/source_metadata_research_atlas.yaml",
    ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml",
    ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml",
    ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
    ".ai/control/gospel_wj_discourse_dossier_queue.yaml",
    ".ai/control/narrative_legal_covenant_dossier_queue.yaml",
    ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml",
    ".ai/control/prophetic_oracle_vision_dossier_queue.yaml",
    ".ai/control/textual_variant_source_tradition_dossier_queue.yaml",
    ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml",
    ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
    ".ai/control/textual_critical_policy_docket.yaml",
    ".ai/control/textual_critical_policy_owner_options.yaml",
    ".ai/control/textual_critical_case_policy.yaml",
    ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
    ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
    ".ai/control/t372_route_isolation_harness_plan.yaml",
    ".ai/control/t373_owner_implementation_authorization.yaml",
    ".ai/control/owner_decision_option_presentation_policy.yaml",
    ".ai/control/chunking_human_decision_forecast.yaml",
    ".ai/control/governance_memory_durability_policy.yaml",
    ".ai/control/owner_decision_projection_policy.yaml",
    "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "raw_or_canonical_mutation",
    "chunk_output_change",
    "revelation_implementation",
    "reviewed_gold_promotion",
    "skill_lifecycle_promotion",
    "boundary_import",
    "parent_only_gold_as_chunk_boundary_outside_exact_t373_t374_pilot",
    "child_span_selection_without_later_owner_promotion",
    "t327g",
    "master_chunker_global_objective",
}

ALLOWED_NEXT_ROUTES = {
    "T342": {
        "route_type": "review_selection_only",
        "title": "Revelation Review-Packet Candidate Selection",
    },
    "T343": {
        "route_type": "review_packet_and_gold_candidate_creation",
        "title": "Revelation Review Packets and Gold Candidates",
    },
    "T344": {
        "route_type": "owner_target_selection",
        "title": "Select One Revelation Behavior Target",
    },
    "T351": {
        "route_type": "bible_wide_research_triage",
        "title": "Bible-Wide Chunking Research Triage Atlas",
    },
    "T352": {
        "route_type": "epistle_argument_review_packet_prep",
        "title": "Epistle Argument Review Packets",
    },
    "T354": {
        "route_type": "gospel_wj_marker_inventory_harness",
        "title": "WJ Marker Inventory Harness",
    },
    "T355": {
        "route_type": "wj_speaker_discourse_policy_and_target_selection",
        "title": "WJ Speaker/Discourse Policy And Target Selection",
    },
    "T356": {
        "route_type": "john3_wj_owner_review_docket",
        "title": "John 3 WJ Owner Review Docket",
    },
    "T368": {
        "route_type": "epistle_argument_review_packet_strengthening",
        "title": "1 Corinthians 8-10 Epistle Argument Packet Strengthening",
    },
    "T369": {
        "route_type": "epistle_argument_owner_review_gate",
        "title": "1 Corinthians 8-10 Owner Review Docket",
    },
    "T370": {
        "route_type": "epistle_argument_parent_only_evidence_prep",
        "title": "Build Selected 1 Corinthians 8-10 Reviewed-Gold Evidence Packet",
    },
    "T371": {
        "route_type": "epistle_argument_owner_reviewed_gold_promotion_gate",
        "title": "Owner Reviewed-Gold Promotion Decision",
    },
    "T372": {
        "route_type": "epistle_argument_route_isolation_harness",
        "title": "Route-Isolated Implementation Harness And Non-Target Identity Plan",
    },
    "T373": {
        "route_type": "epistle_argument_owner_implementation_authorization_gate",
        "title": "Owner Implementation Authorization Gate",
    },
    "T374": {
        "route_type": "epistle_argument_route_isolated_output_pilot",
        "title": "First Route-Isolated 1 Corinthians 8-10 Implementation",
    },
}


class ReadinessMapError(ValueError):
    """Raised when the readiness map is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise ReadinessMapError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ReadinessMapError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReadinessMapError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ReadinessMapError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ReadinessMapError(f"{label} must contain only non-empty strings")
    return value


def validate_readiness_map(path: Path = READINESS_MAP) -> dict[str, Any]:
    data = _read_yaml(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise ReadinessMapError(f"{_rel(path)}: missing top-level keys {missing}")

    if data["object_type"] != "bible_chunking_readiness_map":
        raise ReadinessMapError(f"{_rel(path)}: object_type must be bible_chunking_readiness_map")
    if data["trust_zone"] != "canonical":
        raise ReadinessMapError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise ReadinessMapError(f"{_rel(path)}: lifecycle_status must be active")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise ReadinessMapError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_readiness") is not True:
        raise ReadinessMapError(f"{_rel(path)}: authority.records_readiness must be true")
    for forbidden in (
        "authorizes_chunk_output_change",
        "authorizes_new_algorithm_work",
        "authorizes_reviewed_gold_promotion",
        "authorizes_skill_lifecycle_promotion",
        "authorizes_boundary_import",
    ):
        if authority.get(forbidden) is not False:
            raise ReadinessMapError(f"{_rel(path)}: authority.{forbidden} must be false")

    model = data["faithful_execution_model"]
    if not isinstance(model, dict):
        raise ReadinessMapError(f"{_rel(path)}: faithful_execution_model must be a mapping")
    if model.get("route") != "one_lane_at_a_time_under_bible_wide_map":
        raise ReadinessMapError(f"{_rel(path)}: faithful route must stay one lane at a time")
    _require_string(model.get("rationale"), "faithful_execution_model.rationale")
    _require_string(model.get("bible_wide_goal"), "faithful_execution_model.bible_wide_goal")

    lessons = data["lessons_storage"]
    if not isinstance(lessons, dict):
        raise ReadinessMapError(f"{_rel(path)}: lessons_storage must be a mapping")
    surfaces = set(_require_string_list(lessons.get("surfaces"), "lessons_storage.surfaces"))
    missing_surfaces = sorted(REQUIRED_LESSON_SURFACES - surfaces)
    if missing_surfaces:
        raise ReadinessMapError(f"{_rel(path)}: lessons_storage missing {missing_surfaces}")
    _require_string(lessons.get("rule"), "lessons_storage.rule")

    algorithms = data["algorithm_readiness"]
    if not isinstance(algorithms, dict):
        raise ReadinessMapError(f"{_rel(path)}: algorithm_readiness must be a mapping")
    missing_algorithms = sorted(REQUIRED_ALGORITHMS - set(algorithms))
    if missing_algorithms:
        raise ReadinessMapError(f"{_rel(path)}: algorithm_readiness missing {missing_algorithms}")
    for algorithm_id, algorithm in algorithms.items():
        if not isinstance(algorithm, dict):
            raise ReadinessMapError(f"{_rel(path)}:{algorithm_id}: algorithm entry must be a mapping")
        _require_string(algorithm.get("status"), f"algorithm_readiness.{algorithm_id}.status")
        _require_string(algorithm.get("role"), f"algorithm_readiness.{algorithm_id}.role")
        if algorithm.get("output_change_authorized") is not False:
            raise ReadinessMapError(f"{_rel(path)}:{algorithm_id}: output_change_authorized must be false")

    lanes = data["lane_sequence"]
    if not isinstance(lanes, list) or not lanes:
        raise ReadinessMapError(f"{_rel(path)}: lane_sequence must be a non-empty list")
    lane_ids: set[str] = set()
    implementation_orders: list[int] = []
    for lane in lanes:
        if not isinstance(lane, dict):
            raise ReadinessMapError(f"{_rel(path)}: each lane must be a mapping")
        lane_id = lane.get("lane_id")
        _require_string(lane_id, "lane_sequence.lane_id")
        if lane_id in lane_ids:
            raise ReadinessMapError(f"{_rel(path)}:{lane_id}: duplicate lane_id")
        lane_ids.add(lane_id)
        if not isinstance(lane.get("implementation_order"), int):
            raise ReadinessMapError(f"{_rel(path)}:{lane_id}: implementation_order must be an integer")
        implementation_orders.append(lane["implementation_order"])
        _require_string(lane.get("current_state"), f"lane_sequence.{lane_id}.current_state")
        _require_string(lane.get("theological_risk"), f"lane_sequence.{lane_id}.theological_risk")
        if lane_id == "epistle_argument" and lane.get("current_state") == "t373_a_authorized_exact_parent_only_t374_pilot_next":
            if lane.get("new_algorithm_work_ready") is not True:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be true after T373-A")
        elif lane.get("new_algorithm_work_ready") is not False:
            raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be false")

    missing_lanes = sorted(REQUIRED_LANES - lane_ids)
    if missing_lanes:
        raise ReadinessMapError(f"{_rel(path)}: lane_sequence missing {missing_lanes}")
    if sorted(implementation_orders) != list(range(1, len(implementation_orders) + 1)):
        raise ReadinessMapError(f"{_rel(path)}: implementation_order values must be contiguous")

    next_route = data["next_route"]
    if not isinstance(next_route, dict):
        raise ReadinessMapError(f"{_rel(path)}: next_route must be a mapping")
    task_id = next_route.get("task_id")
    if task_id not in ALLOWED_NEXT_ROUTES:
        raise ReadinessMapError(
            f"{_rel(path)}: next_route.task_id must be one of {sorted(ALLOWED_NEXT_ROUTES)}"
        )
    expected_route_type = ALLOWED_NEXT_ROUTES[task_id]["route_type"]
    if next_route.get("route_type") != expected_route_type:
        raise ReadinessMapError(
            f"{_rel(path)}: next_route.route_type must be {expected_route_type} for {task_id}"
        )
    if task_id == "T374":
        if next_route.get("output_change_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 next_route.output_change_authorized must be true")
        if next_route.get("implementation_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 next_route.implementation_authorized must be true")
    else:
        if next_route.get("output_change_authorized") is not False:
            raise ReadinessMapError(f"{_rel(path)}: next_route.output_change_authorized must be false")
        if next_route.get("implementation_authorized") is not False:
            raise ReadinessMapError(f"{_rel(path)}: next_route.implementation_authorized must be false")
    if task_id == "T352":
        if next_route.get("review_packet_lane") != "epistle_argument":
            raise ReadinessMapError(f"{_rel(path)}: T352 next_route.review_packet_lane must be epistle_argument")
        if next_route.get("packet_status") != "pending_human_review":
            raise ReadinessMapError(f"{_rel(path)}: T352 next_route.packet_status must be pending_human_review")
        if next_route.get("prior_triage_task") != "T351":
            raise ReadinessMapError(f"{_rel(path)}: T352 next_route.prior_triage_task must be T351")
    if task_id == "T354":
        if next_route.get("review_packet_lane") != "gospel_discourse_wj":
            raise ReadinessMapError(f"{_rel(path)}: T354 next_route.review_packet_lane must be gospel_discourse_wj")
        if next_route.get("prior_inventory_task") != "T353":
            raise ReadinessMapError(f"{_rel(path)}: T354 next_route.prior_inventory_task must be T353")
        if next_route.get("inventory_status") != "generated_non_authorizing":
            raise ReadinessMapError(f"{_rel(path)}: T354 next_route.inventory_status must be generated_non_authorizing")
    if task_id == "T355":
        if next_route.get("review_packet_lane") != "gospel_discourse_wj":
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.review_packet_lane must be gospel_discourse_wj")
        if next_route.get("prior_inventory_task") != "T354":
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.prior_inventory_task must be T354")
        if next_route.get("selected_target") != "john3_wj_speaker_boundary":
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.selected_target must be john3_wj_speaker_boundary")
        if next_route.get("selected_target_status") != "selected_for_next_owner_review":
            raise ReadinessMapError(
                f"{_rel(path)}: T355 next_route.selected_target_status must be selected_for_next_owner_review"
            )
        if next_route.get("policy") != ".ai/control/wj_speaker_discourse_policy.yaml":
            raise ReadinessMapError(
                f"{_rel(path)}: T355 next_route.policy must be .ai/control/wj_speaker_discourse_policy.yaml"
            )
        if next_route.get("reviewed_gold_promoted") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.reviewed_gold_promoted must be false")
    if task_id == "T356":
        if next_route.get("review_packet_lane") != "gospel_discourse_wj":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.review_packet_lane must be gospel_discourse_wj")
        if next_route.get("prior_policy_task") != "T355":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.prior_policy_task must be T355")
        if next_route.get("selected_target") != "john3_wj_speaker_boundary":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.selected_target must be john3_wj_speaker_boundary")
        if next_route.get("john3_owner_selection_status") != "pending":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.john3_owner_selection_status must be pending")
        if next_route.get("john3_selected_option") != "pending":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.john3_selected_option must be pending")
        if next_route.get("docket") != ".ai/control/john3_wj_owner_review_docket.yaml":
            raise ReadinessMapError(
                f"{_rel(path)}: T356 next_route.docket must be .ai/control/john3_wj_owner_review_docket.yaml"
            )
        if next_route.get("reviewed_gold_promoted") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.reviewed_gold_promoted must be false")
    if task_id == "T368":
        expected_t368 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "packet_status": "pending_human_review",
            "prior_owner_decision_task": "T367",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
            "john3_owner_selection_status": "selected",
            "john3_selected_option": "JOHN3-T356-B",
            "john3_selected_parent": "John.3.1-John.3.36",
        }
        for key, value in expected_t368.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T368 next_route.{key} must be {value}")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T368 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T368 next_route.{key} must be false")
    if task_id == "T369":
        expected_t369 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "pending_human_review",
            "owner_selection_status": "pending_owner_decision",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
            "textual_critical_policy_owner_options": ".ai/control/textual_critical_policy_owner_options.yaml",
            "textual_critical_case_policy": ".ai/control/textual_critical_case_policy.yaml",
        }
        for key, value in expected_t369.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T369 next_route.{key} must be {value}")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T369 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T369 next_route.{key} must be false")
    if task_id == "T370":
        expected_t370 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_evidence_prep_allowed",
            "owner_selection_status": "selected",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t370.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T370 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T370 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T369_parent_only_projected_selection":
            raise ReadinessMapError(f"{_rel(path)}: T370 next_route.starts_only_if is stale")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T370 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T370 next_route.{key} must be false")
    if task_id == "T371":
        expected_t371 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_evidence_packet_ready_for_owner_review",
            "owner_selection_status": "selected",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "evidence_prep_task": "T370",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t371.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T371 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T370_builds_governed_evidence_and_T379_selects_case_policy":
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.starts_only_if is stale")
        if next_route.get("owner_decision_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.owner_decision_required must be true")
        if next_route.get("variant_sensitive_policy_gate_task") != "T379":
            raise ReadinessMapError(f"{_rel(path)}: T371 variant_sensitive_policy_gate_task must be T379")
        if next_route.get("variant_sensitive_policy_selected") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 variant_sensitive_policy_selected must be true")
        if next_route.get("selected_textual_critical_policy") != "TCP-T378-B":
            raise ReadinessMapError(f"{_rel(path)}: T371 selected_textual_critical_policy must be TCP-T378-B")
        if next_route.get("t371_promotion_blocked_until_textual_policy") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T371 textual-policy blocker must be resolved")
        if next_route.get("variant_dependency_owner_decision_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 variant dependency owner decision must be required")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T371 next_route.{key} must be false")
    if task_id == "T372":
        expected_t372 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "promotion_record": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
            "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_reviewed_gold_promoted",
            "owner_selection_status": "selected",
            "selected_t371_option": "T371-A",
            "parent_gold_promotion_task": "T371",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "evidence_prep_task": "T370",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t372.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T372 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T372 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T371_A_parent_only_reviewed_gold_promoted":
            raise ReadinessMapError(f"{_rel(path)}: T372 starts_only_if is stale")
        if next_route.get("reviewed_gold_promoted") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T372 reviewed_gold_promoted must be true")
        if next_route.get("variant_dependency_result") != "variant_non_dependent":
            raise ReadinessMapError(f"{_rel(path)}: T372 variant_dependency_result is stale")
        if next_route.get("variant_dependency_owner_decision_required") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T372 variant dependency owner decision must be resolved")
        if next_route.get("harness_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T372 next_route.harness_only must be true")
        if next_route.get("owner_implementation_authorization_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T372 implementation owner gate must be required")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T372 next_route.{key} must be false")
    if task_id == "T373":
        expected_t373 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "promotion_record": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
            "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
            "harness_plan": ".ai/control/t372_route_isolation_harness_plan.yaml",
            "harness_plan_status": "complete_non_output_changing_plan",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_reviewed_gold_promoted",
            "owner_selection_status": "selected",
            "selected_t371_option": "T371-A",
            "parent_gold_promotion_task": "T371",
            "prior_harness_task": "T372",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "evidence_prep_task": "T370",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t373.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T373 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T373 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T372_route_isolation_harness_plan_complete":
            raise ReadinessMapError(f"{_rel(path)}: T373 starts_only_if is stale")
        if next_route.get("owner_decision_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T373 owner_decision_required must be true")
        if next_route.get("reviewed_gold_promoted") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T373 reviewed_gold_promoted must be true")
        if next_route.get("harness_only") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T373 next_route.harness_only must be false")
        if next_route.get("owner_implementation_authorization_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T373 implementation owner gate must be required")
        if next_route.get("next_task_if_authorized") != "T374":
            raise ReadinessMapError(f"{_rel(path)}: T373 next_task_if_authorized must be T374")
        required_owner = set(_require_string_list(
            next_route.get("required_owner_decision_must_record"),
            "T373 required_owner_decision_must_record",
        ))
        for item in (
            "exact_output_or_implementation_authorization_or_hold",
            "whether_parent_span_may_be_used_as_output_chunk_boundary",
            "whether_child_spans_remain_disallowed_or_are_separately_selected",
            "non_target_identity_proof_requirement",
            "same_baseline_evaluation_requirement",
            "decision_register_update_requirement",
        ):
            if item not in required_owner:
                raise ReadinessMapError(f"{_rel(path)}: T373 required owner decision missing {item}")
        if next_route.get("default_if_owner_unavailable") != "stop_before_implementation_or_output_change":
            raise ReadinessMapError(f"{_rel(path)}: T373 default_if_owner_unavailable must stop")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T373 next_route.{key} must be false")
    if task_id == "T374":
        expected_t374 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "T373-A",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "explicit_owner_authorization",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "promotion_record": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
            "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
            "harness_plan": ".ai/control/t372_route_isolation_harness_plan.yaml",
            "authorization_record": ".ai/control/t373_owner_implementation_authorization.yaml",
            "option_presentation_policy": ".ai/control/owner_decision_option_presentation_policy.yaml",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_reviewed_gold_promoted",
            "owner_selection_status": "selected",
            "selected_t371_option": "T371-A",
            "selected_t373_option": "T373-A",
            "implementation_authorization_task": "T373",
            "prior_harness_task": "T372",
            "variant_dependency_result": "variant_non_dependent",
            "general_parent_first_pilot_pattern": "parent_first_pilot_then_child_necessity_review",
            "post_pilot_child_necessity_review_required": True,
            "child_span_work_requires_later_owner_promotion": True,
        }
        for key, value in expected_t374.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T374 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T374 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T373_A_authorizes_exact_parent_only_output_pilot":
            raise ReadinessMapError(f"{_rel(path)}: T374 starts_only_if is stale")
        if next_route.get("owner_decision_required") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T374 owner_decision_required must be false")
        if next_route.get("owner_implementation_authorization_recorded") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 owner implementation authorization must be recorded")
        if next_route.get("parent_span_as_chunk_boundary_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 parent span must be authorized")
        if next_route.get("parent_span_authorization_scope") != "exact_t374_pilot_only":
            raise ReadinessMapError(f"{_rel(path)}: T374 parent authorization scope must be exact")
        if next_route.get("route_behavior_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 route behavior must be authorized")
        if next_route.get("route_behavior_authorization_scope") != "exact_t374_target_only":
            raise ReadinessMapError(f"{_rel(path)}: T374 route scope must be exact")
        required_t374 = set(_require_string_list(
            next_route.get("required_t374_work_must_record"),
            "T374 required_t374_work_must_record",
        ))
        for item in (
            "parent_only_scope_proof",
            "selected_children_must_be_empty",
            "non_target_identity_proof",
            "same_baseline_evaluation",
            "changed_output_manifest",
            "decision_register_update",
            "validators_and_tests",
            "no_context_audit_surface",
            "post_pilot_child_necessity_review_gate",
        ):
            if item not in required_t374:
                raise ReadinessMapError(f"{_rel(path)}: T374 required work missing {item}")
        must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T374 must_fail_if"))
        for item in (
            "child_spans_are_added_without_later_owner_promotion",
            "child_spans_are_added_without_post_pilot_review",
            "route_behavior_applies_outside_1cor8_10",
            "graph_or_retrieval_truth_is_generated",
            "non_target_output_diff_is_detected",
        ):
            if item not in must_fail:
                raise ReadinessMapError(f"{_rel(path)}: T374 must_fail_if missing {item}")
        for key in ("evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T374 next_route.{key} must be false")

    parallel_research = data.get("parallel_research_queue")
    if isinstance(parallel_research, dict):
        expected_parallel = {
            "task_id": "T358",
            "route_type": "whole_bible_research_registry",
            "path": ".ai/control/bible_wide_chunking_research_registry.yaml",
            "status": "complete_non_authorizing",
            "corpus_scope": "canonical_66",
            "book_count": 66,
        }
        for key, value in expected_parallel.items():
            if parallel_research.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: parallel_research_queue.{key} must be {value}")
        for key in ("output_change_authorized", "implementation_authorized", "reviewed_gold_promoted"):
            if parallel_research.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: parallel_research_queue.{key} must be false")

    options = data.get("parallel_textual_critical_policy_options")
    if not isinstance(options, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_policy_options must be a mapping")
    if options.get("task_id") != "T378":
        raise ReadinessMapError(f"{_rel(path)}: textual-critical options task_id must be T378")
    if options.get("textual_critical_policy_selected") is not True:
        raise ReadinessMapError(f"{_rel(path)}: textual-critical options must record selected policy")
    if options.get("selected_policy") != "TCP-T378-B":
        raise ReadinessMapError(f"{_rel(path)}: textual-critical selected_policy must be TCP-T378-B")
    if options.get("selection_record") != ".ai/control/textual_critical_case_policy.yaml":
        raise ReadinessMapError(f"{_rel(path)}: textual-critical selection_record is stale")

    case_policy = data.get("parallel_textual_critical_case_policy")
    if not isinstance(case_policy, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_case_policy must be a mapping")
    expected_case = {
        "task_id": "T379",
        "path": ".ai/control/textual_critical_case_policy.yaml",
        "selected_policy": "TCP-T378-B",
        "projectable_pattern": "ODP-005",
    }
    for key, value in expected_case.items():
        if case_policy.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_case_policy.{key} must be {value}")
    if case_policy.get("variant_dependency_owner_decision_required") is not True:
        raise ReadinessMapError(f"{_rel(path)}: variant dependency owner decision must be required")
    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "reviewed_gold_promoted",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if case_policy.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_case_policy.{key} must be false")

    t371_packet = data.get("parallel_t371_owner_decision_packet")
    if not isinstance(t371_packet, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet must be a mapping")
    expected_t371_packet = {
        "task_id": "T380",
        "path": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
        "target_owner_task": "T371",
        "recommended_if_owner_agrees_with_variant_non_dependency": "T371-A",
        "conservative_hold_if_any_doubt": "T371-B",
    }
    for key, value in expected_t371_packet.items():
        if t371_packet.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet.{key} must be {value}")
    if set(t371_packet.get("exact_variant_refs", [])) != {"1Cor.9.20", "1Cor.10.9"}:
        raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet refs are stale")
    if t371_packet.get("owner_decision_required") is not False:
        raise ReadinessMapError(f"{_rel(path)}: T371 packet owner_decision_required must be false after T371-A")
    if t371_packet.get("owner_response_record") != ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml":
        raise ReadinessMapError(f"{_rel(path)}: T371 packet owner_response_record is stale")
    if t371_packet.get("selected_option") != "T371-A":
        raise ReadinessMapError(f"{_rel(path)}: T371 packet selected_option must be T371-A")
    for key in (
        "variant_dependency_finding_authorized",
        "variant_non_dependency_finding_authorized",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "reviewed_gold_promoted",
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if t371_packet.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet.{key} must be false")

    promotion = data.get("parallel_t371_parent_only_promotion_record")
    if not isinstance(promotion, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t371_parent_only_promotion_record must be a mapping")
    expected_promotion = {
        "task_id": "T371",
        "path": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "status": "complete_parent_only_reviewed_gold_promoted",
        "selected_option": "T371-A",
        "boundary_dependency_or_non_dependency": "variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency": "variant_non_dependent",
    }
    for key, value in expected_promotion.items():
        if promotion.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_parent_only_promotion_record.{key} must be {value}")
    if set(promotion.get("exact_variant_refs", [])) != {"1Cor.9.20", "1Cor.10.9"}:
        raise ReadinessMapError(f"{_rel(path)}: T371 promotion refs are stale")
    if promotion.get("reviewed_gold_promoted") is not True:
        raise ReadinessMapError(f"{_rel(path)}: T371 promotion must record reviewed_gold_promoted true")
    for key in (
        "parent_span_as_chunk_boundary_authorized",
        "child_spans_authorized",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if promotion.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_parent_only_promotion_record.{key} must be false")

    t372_plan = data.get("parallel_t372_route_isolation_harness_plan")
    if not isinstance(t372_plan, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t372_route_isolation_harness_plan must be a mapping")
    expected_t372_plan = {
        "task_id": "T372",
        "path": ".ai/control/t372_route_isolation_harness_plan.yaml",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "status": "complete_non_output_changing_plan",
        "next_owner_gate": "T373",
    }
    for key, value in expected_t372_plan.items():
        if t372_plan.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t372_route_isolation_harness_plan.{key} must be {value}")
    if t372_plan.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise ReadinessMapError(f"{_rel(path)}: T372 plan selected_parent is stale")
    if t372_plan.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T372 plan selected_children must be []")
    if t372_plan.get("owner_implementation_authorization_required") is not True:
        raise ReadinessMapError(f"{_rel(path)}: T372 plan must require T373 owner authorization")
    for key in (
        "parent_span_as_chunk_boundary_authorized",
        "child_spans_authorized",
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if t372_plan.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t372_route_isolation_harness_plan.{key} must be false")

    t373_auth = data.get("parallel_t373_owner_implementation_authorization")
    if not isinstance(t373_auth, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t373_owner_implementation_authorization must be a mapping")
    expected_t373_auth = {
        "task_id": "T373",
        "path": ".ai/control/t373_owner_implementation_authorization.yaml",
        "option_presentation_policy": ".ai/control/owner_decision_option_presentation_policy.yaml",
        "status": "complete_owner_authorized_exact_parent_only_pilot",
        "selected_option": "T373-A",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "general_parent_first_pilot_pattern": "parent_first_pilot_then_child_necessity_review",
        "post_pilot_child_necessity_review_required": True,
        "child_span_work_requires_later_owner_promotion": True,
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "parent_span_as_chunk_boundary_authorized": True,
        "child_spans_authorized": False,
        "output_change_authorized": True,
        "implementation_authorized": True,
        "route_behavior_authorized": True,
        "evaluator_change_authorized": False,
        "graph_edge_generation_allowed": False,
        "retrieval_truth_authorized": False,
    }
    for key, value in expected_t373_auth.items():
        if t373_auth.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t373_owner_implementation_authorization.{key} must be {value!r}")
    if t373_auth.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T373 parallel selected_children must be []")

    non_authorizations = set(
        _require_string_list(data["explicit_non_authorizations"], "explicit_non_authorizations")
    )
    missing_non_authorizations = sorted(REQUIRED_NON_AUTHORIZATIONS - non_authorizations)
    if missing_non_authorizations:
        raise ReadinessMapError(
            f"{_rel(path)}: explicit_non_authorizations missing {missing_non_authorizations}"
        )

    return data


def main() -> int:
    try:
        validate_readiness_map()
    except ReadinessMapError as exc:
        print(f"Bible chunking readiness map validation failed: {exc}", file=sys.stderr)
        return 1
    print("Bible chunking readiness map validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
