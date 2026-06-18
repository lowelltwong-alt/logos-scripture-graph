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
}

REQUIRED_NON_AUTHORIZATIONS = {
    "raw_or_canonical_mutation",
    "chunk_output_change",
    "revelation_implementation",
    "reviewed_gold_promotion",
    "skill_lifecycle_promotion",
    "boundary_import",
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
        if lane.get("new_algorithm_work_ready") is not False:
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
