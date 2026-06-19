#!/usr/bin/env python3
"""Validate the chunking human decision forecast."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T369_HUMAN_DECISION_FORECAST_AND_CHUNKING_READY_ROADMAP.md"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"

REQUIRED_DECISIONS = {
    "HDF-001",
    "HDF-002",
    "HDF-003",
    "HDF-004",
    "HDF-005",
    "HDF-006",
    "HDF-007",
    "HDF-008",
    "HDF-009",
    "HDF-010",
    "HDF-011",
    "HDF-012",
}

REQUIRED_FALSE_AUTHORITY_FLAGS = {
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edge_generation",
    "authorizes_retrieval_truth",
    "authorizes_textual_critical_policy",
    "authorizes_boundary_import",
}


class ForecastError(ValueError):
    """Raised when the human decision forecast is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ForecastError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _read_text(path)
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ForecastError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ForecastError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_false(mapping: dict[str, Any], key: str, label: str) -> None:
    if mapping.get(key) is not False:
        raise ForecastError(f"{label}.{key} must be false")


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ForecastError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ForecastError(f"{label} must contain only non-empty strings")
    return value


def _validate_forecast(data: dict[str, Any], path: Path) -> None:
    expected = {
        "object_type": "chunking_human_decision_forecast",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "chunking_human_decision_forecast.v1",
        "forecast_id": "chunking_ready_owner_decision_forecast",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise ForecastError(f"{_rel(path)}: {key} must be {value!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise ForecastError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_anticipated_decisions") is not True:
        raise ForecastError(f"{_rel(path)}: authority.records_anticipated_decisions must be true")
    for key in REQUIRED_FALSE_AUTHORITY_FLAGS:
        _require_false(authority, key, "authority")

    blocked = data.get("goal_blocked_explanation")
    if not isinstance(blocked, dict) or blocked.get("thread_goal_status") != "blocked":
        raise ForecastError(f"{_rel(path)}: goal_blocked_explanation.thread_goal_status must be blocked")
    if "owner decisions" not in str(blocked.get("reason", "")):
        raise ForecastError(f"{_rel(path)}: goal_blocked_explanation.reason must mention owner decisions")

    policy = data.get("decision_policy")
    if not isinstance(policy, dict):
        raise ForecastError(f"{_rel(path)}: decision_policy must be a mapping")
    if policy.get("owner_pattern_projection_policy") != ".ai/control/owner_decision_projection_policy.yaml":
        raise ForecastError(f"{_rel(path)}: decision_policy.owner_pattern_projection_policy is stale")
    _string_list(policy.get("projected_decisions_allowed_when"), "decision_policy.projected_decisions_allowed_when")
    owner_must_be_told = set(_string_list(policy.get("owner_must_be_told_when"), "decision_policy.owner_must_be_told_when"))
    if "prior_owner_decisions_conflict_for_the_text_under_review" not in owner_must_be_told:
        raise ForecastError(f"{_rel(path)}: owner_must_be_told_when must include conflict stop")
    required_owner = set(_string_list(policy.get("owner_decision_required_for"), "decision_policy.owner_decision_required_for"))
    for item in (
        "reviewed_gold_promotion",
        "chunk_output_change",
        "route_behavior_change",
        "evaluator_behavior_change",
        "new_textual_critical_policy_selection",
        "variant_sensitive_promotion_owner_confirmation",
        "boundary_import",
    ):
        if item not in required_owner:
            raise ForecastError(f"{_rel(path)}: owner_decision_required_for missing {item}")
    if policy.get("if_owner_unavailable") != "stop_before_authority_change":
        raise ForecastError(f"{_rel(path)}: decision_policy.if_owner_unavailable must stop before authority change")

    decisions = data.get("front_loaded_decisions")
    if not isinstance(decisions, list):
        raise ForecastError(f"{_rel(path)}: front_loaded_decisions must be a list")
    by_id = {item.get("decision_id"): item for item in decisions if isinstance(item, dict)}
    missing = sorted(REQUIRED_DECISIONS - set(by_id))
    if missing:
        raise ForecastError(f"{_rel(path)}: missing front-loaded decisions {missing}")

    hdf_001 = by_id["HDF-001"]
    if hdf_001.get("status") != "projected_owner_pattern_selected":
        raise ForecastError(f"{_rel(path)}: HDF-001 must be projected_owner_pattern_selected")
    if hdf_001.get("earliest_task") != "T369":
        raise ForecastError(f"{_rel(path)}: HDF-001 earliest_task must be T369")
    if hdf_001.get("selected_option") != "1COR8-10-T369-B":
        raise ForecastError(f"{_rel(path)}: HDF-001 selected_option must be 1COR8-10-T369-B")
    if hdf_001.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise ForecastError(f"{_rel(path)}: HDF-001 selected_parent is wrong")
    if hdf_001.get("selected_children") != []:
        raise ForecastError(f"{_rel(path)}: HDF-001 selected_children must remain empty")
    if hdf_001.get("selection_mode") != "projected_owner_pattern":
        raise ForecastError(f"{_rel(path)}: HDF-001 selection_mode must be projected_owner_pattern")
    if hdf_001.get("conflict_scan_result") != "no_conflict_detected":
        raise ForecastError(f"{_rel(path)}: HDF-001 conflict_scan_result must be no_conflict_detected")
    option_ids = {
        option.get("option_id")
        for option in hdf_001.get("options", [])
        if isinstance(option, dict)
    }
    expected_options = {
        "1COR8-10-T369-A",
        "1COR8-10-T369-B",
        "1COR8-10-T369-C",
        "1COR8-10-T369-D",
        "1COR8-10-T369-E",
    }
    if option_ids != expected_options:
        raise ForecastError(f"{_rel(path)}: HDF-001 options must match {sorted(expected_options)}")

    hdf_002 = by_id["HDF-002"]
    if hdf_002.get("status") != "selected_case_by_case_policy":
        raise ForecastError(f"{_rel(path)}: HDF-002 must be selected_case_by_case_policy")
    if hdf_002.get("selected_policy") != "TCP-T378-B":
        raise ForecastError(f"{_rel(path)}: HDF-002 selected_policy must be TCP-T378-B")
    if hdf_002.get("owner_selection_task") != "T379":
        raise ForecastError(f"{_rel(path)}: HDF-002 owner_selection_task must be T379")
    if hdf_002.get("policy_record") != ".ai/control/textual_critical_case_policy.yaml":
        raise ForecastError(f"{_rel(path)}: HDF-002 policy_record is stale")
    if hdf_002.get("projection_policy_pattern") != "ODP-005":
        raise ForecastError(f"{_rel(path)}: HDF-002 projection policy must be ODP-005")
    for phrase in ("exact variants", "owner confirmation", "validators/tests"):
        if phrase not in str(hdf_002.get("current_authorization", "")):
            raise ForecastError(f"{_rel(path)}: HDF-002 current_authorization missing {phrase!r}")
    if "preferred_reading_selection" not in hdf_002.get("non_authorizations", []):
        raise ForecastError(f"{_rel(path)}: HDF-002 must deny preferred_reading_selection")
    if "variant_dependency_projection" not in hdf_002.get("non_authorizations", []):
        raise ForecastError(f"{_rel(path)}: HDF-002 must deny variant_dependency_projection")

    hdf_003 = by_id["HDF-003"]
    if hdf_003.get("status") != "t371_owner_decision_packet_prepared":
        raise ForecastError(f"{_rel(path)}: HDF-003 must record T371 packet preparation")
    if hdf_003.get("current_decision_packet") != ".ai/control/t371_variant_dependency_owner_decision_packet.yaml":
        raise ForecastError(f"{_rel(path)}: HDF-003 current_decision_packet is stale")
    if hdf_003.get("next_owner_gate") != "T371":
        raise ForecastError(f"{_rel(path)}: HDF-003 next_owner_gate must be T371")

    hdf_004 = by_id["HDF-004"]
    if "chunk_output_change" not in hdf_004.get("must_stop_for", []):
        raise ForecastError(f"{_rel(path)}: HDF-004 must stop for chunk_output_change")

    ready = data.get("chunking_ready_definition")
    if not isinstance(ready, dict):
        raise ForecastError(f"{_rel(path)}: chunking_ready_definition must be a mapping")
    ready_required = set(_string_list(
        ready.get("ready_for_first_output_changing_chunk_pr_requires"),
        "chunking_ready_definition.ready_for_first_output_changing_chunk_pr_requires",
    ))
    for item in (
        "owner_selected_exact_target",
        "reviewed_gold_or_equivalent_governed_evidence_promoted_by_owner",
        "non_target_identity_proof",
        "same_baseline_evaluation_plan",
        "explicit_owner_implementation_authorization",
    ):
        if item not in ready_required:
            raise ForecastError(f"{_rel(path)}: chunking-ready definition missing {item}")

    for item in (
        "source_metadata_would_become_authority",
        "missing_reviewed_gold",
        "non_target_output_diff",
        "graph_retrieval_vector_output_requested",
    ):
        if item not in data.get("stop_conditions", []):
            raise ForecastError(f"{_rel(path)}: stop_conditions missing {item}")

    for item in (
        "do_not_treat_this_forecast_as_authorization",
        "do_not_implement_chunks_from_pending_packets",
        "do_not_merge_output_changing_work_without_owner_authorization",
        "do_not_project_owner_decisions_when_prior_decisions_conflict_for_the_target_text",
    ):
        if item not in data.get("what_not_to_do", []):
            raise ForecastError(f"{_rel(path)}: what_not_to_do missing {item}")

    steps = data.get("next_roadmap_steps")
    if not isinstance(steps, list):
        raise ForecastError(f"{_rel(path)}: next_roadmap_steps must be a list")
    step_ids = [step.get("task_id") for step in steps if isinstance(step, dict)]
    for expected in ("T369", "T370", "T379", "T380", "T371", "T372", "T373", "T374", "T375", "T376"):
        if expected not in step_ids:
            raise ForecastError(f"{_rel(path)}: next_roadmap_steps missing {expected}")


def _validate_governed_links() -> None:
    roadmap = _read_text(ROADMAP_DOC)
    for phrase in (
        "Why The Goal Looked Blocked",
        "Front-Loaded Human Decisions",
        "HDF-001 - 1 Corinthians 8-10 Owner Option",
        "Roadmap From Here",
        "What Not To Do",
        "Stop Conditions",
    ):
        if phrase not in roadmap:
            raise ForecastError(f"{_rel(ROADMAP_DOC)}: missing phrase {phrase!r}")

    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {
        str(item.get("path"))
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    if ".ai/control/chunking_human_decision_forecast.yaml" not in reading_paths:
        raise ForecastError(f"{_rel(PREFLIGHT)}: human decision forecast must be mandatory reading")

    readiness = _read_yaml(READINESS_MAP)
    surfaces = set(readiness.get("lessons_storage", {}).get("surfaces", []))
    if ".ai/control/chunking_human_decision_forecast.yaml" not in surfaces:
        raise ForecastError(f"{_rel(READINESS_MAP)}: lessons_storage must include human decision forecast")

    register = _read_text(REGISTER)
    for phrase in ("CD-038", "CD-042", "CD-046", "Human decision forecast front-loads chunking gates", "T368", "T370", "T380"):
        if phrase not in register:
            raise ForecastError(f"{_rel(REGISTER)}: missing {phrase!r}")

    roadmap_state = _read_yaml(ROADMAP_STATE)
    future = roadmap_state.get("phases", {}).get("phase_4", {}).get("future_sequence")
    if not isinstance(future, list):
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: phase_4.future_sequence must be a list")
    by_id = {item.get("id"): item for item in future if isinstance(item, dict)}
    for task_id in ("T369", "T370", "T379", "T380", "T371", "T372", "T373", "T374", "T375", "T376"):
        if task_id not in by_id:
            raise ForecastError(f"{_rel(ROADMAP_STATE)}: future_sequence missing {task_id}")
    if by_id["T369"].get("status") != "complete":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T369 must be complete after projection")
    if by_id["T369"].get("selected_option") != "1COR8-10-T369-B":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T369 selected_option is wrong")
    if by_id["T370"].get("starts_only_if") != "T369_parent_only_projected_selection":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T370 starts_only_if is stale")
    if by_id["T370"].get("status") != "complete":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T370 must be complete after evidence prep")
    if by_id["T370"].get("evidence_packet") != "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T370 evidence_packet is stale")
    if by_id["T371"].get("starts_only_if") != "T370_builds_governed_evidence_and_T379_selects_case_policy":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T371 starts_only_if is stale")
    if by_id["T371"].get("owner_decision_required") is not True:
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T371 owner_decision_required must be true")
    if by_id["T379"].get("selected_policy") != "TCP-T378-B":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T379 selected_policy is stale")
    if by_id["T380"].get("owner_decision_packet") != ".ai/control/t371_variant_dependency_owner_decision_packet.yaml":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T380 owner_decision_packet is stale")
    if by_id["T380"].get("status") != "complete":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T380 must be complete")
    if by_id["T369"].get("human_decision_forecast") != ".ai/control/chunking_human_decision_forecast.yaml":
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T369 must link the human decision forecast")
    if by_id["T374"].get("output_change_authorized") is not False:
        raise ForecastError(f"{_rel(ROADMAP_STATE)}: T374 must not be pre-authorized for output change")

    front_door = _read_text(FRONT_DOOR)
    for phrase in (
        "chunking_human_decision_forecast.yaml",
        "predictable owner decisions",
        "ready for the first new output-changing chunk PR",
    ):
        if phrase not in front_door:
            raise ForecastError(f"{_rel(FRONT_DOOR)}: missing {phrase!r}")


def validate_chunking_human_decision_forecast(path: Path = FORECAST) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_forecast(data, path)
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_chunking_human_decision_forecast()
    except ForecastError as exc:
        print(f"Chunking human decision forecast validation failed: {exc}", file=sys.stderr)
        return 1
    print("Chunking human decision forecast validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
