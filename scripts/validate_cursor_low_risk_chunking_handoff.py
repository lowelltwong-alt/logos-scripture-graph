#!/usr/bin/env python3
"""Validate the T404 Cursor low-risk chunking handoff contract."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / ".ai" / "control" / "cursor_low_risk_chunking_handoff.yaml"
MULTI_PASS_PLAN = ROOT / ".ai" / "control" / "low_risk_chunking_multi_pass_plan.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T404_CURSOR_LOW_RISK_CHUNKING_HANDOFF.md"
T406_ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T406_LOW_RISK_CHUNKING_MULTI_PASS_PLAN.md"
PROJECT_RULE = ROOT / ".cursor" / "rules" / "logos-scripture-low-risk-chunking.mdc"
COMMANDS = [
    ROOT / ".cursor" / "commands" / "chunking-preflight.md",
    ROOT / ".cursor" / "commands" / "low-risk-chunking-candidate.md",
    ROOT / ".cursor" / "commands" / "codex-review-packet.md",
]
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
SUPPLY_CHAIN = ROOT / "docs" / "methodology" / "CHUNKING_SKILL_SUPPLY_CHAIN.md"
TASK = ROOT / ".ai" / "tasks" / "T404.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T404" / "handoff.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

CONTRACT_REL = ".ai/control/cursor_low_risk_chunking_handoff.yaml"
VALIDATOR_REL = "scripts/validate_cursor_low_risk_chunking_handoff.py"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_cursor_target_selection",
    "authorizes_exact_target_selection",
    "authorizes_review_packet_strengthening_without_owner_selection",
    "authorizes_reviewed_gold_promotion",
    "authorizes_child_spans",
    "authorizes_chunk_output_change",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_boundary_import",
    "authorizes_whole_bible_output_pass",
    "authorizes_preferred_reading_or_source_tradition",
    "authorizes_canon_scope_change",
    "authorizes_source_or_manuscript_row_population",
    "authorizes_theology_authority_change",
}

REQUIRED_MANDATORY_READING = {
    "AI_FRONT_DOOR.md",
    ".ai/control/MASTER_CONTEXT.md",
    ".ai/control/PROJECT_STATUS.md",
    ".ai/control/DATA_MAP.md",
    ".ai/control/RAW_SOURCE_INVENTORY.md",
    ".ai/control/test_runtime_preflight.yaml",
    ".ai/control/chunking_agent_preflight.yaml",
    ".ai/control/chunking_lesson_index.yaml",
    ".ai/control/chunking_theological_decision_register.yaml",
    ".ai/control/bible_chunking_readiness_map.yaml",
    ".ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml",
    ".ai/control/cursor_low_risk_chunking_handoff.yaml",
    ".ai/control/low_risk_chunking_multi_pass_plan.yaml",
}

REQUIRED_DISALLOWED_STATUSES = {
    "needs_context_research",
    "needs_original_language_review",
    "variant_sensitive_hold",
    "theological_risk_hold",
    "not_low_complexity",
    "owner_decision_required",
    "do_not_chunk_now",
}

REQUIRED_STOP_CONDITIONS = {
    "cursor_selected_target",
    "target_status_not_ready_for_review_packet",
    "variant_source_tradition_hold_detected",
    "theological_risk_hold_detected",
    "child_span_requested_or_required",
    "raw_or_canonical_or_processed_or_derived_data_change",
    "graph_edge_generation_requested",
    "retrieval_truth_requested",
    "embedding_or_vector_work_requested",
    "boundary_import_requested",
    "source_or_manuscript_rows_requested",
    "theology_authority_requested",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "cursor_target_selection",
    "exact_target_selection",
    "reviewed_gold_promotion",
    "child_span_selection",
    "chunk_output_change",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "vector_index_build",
    "boundary_import",
    "whole_bible_output_pass",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "source_or_manuscript_row_population",
    "theology_authority_change",
}

TEXT_SURFACE_REQUIREMENTS = {
    ROADMAP_DOC: ["T404 Cursor Low-Risk Chunking Handoff", "Cursor must stop if it has to pick the target", "Research Completion Verdict"],
    T406_ROADMAP_DOC: ["T406 Low-Risk Chunking Multi-Pass Plan", "The low-risk chunking research is complete at T402 triage depth", "T406 is the next future pass"],
    PROJECT_RULE: ["cursor_low_risk_chunking_handoff.yaml", "Cursor must not choose the target"],
    COMMANDS[0]: ["Use Cursor Plan mode first", "Do not edit files during this command"],
    COMMANDS[1]: ["candidate status is `ready_for_review_packet`", "Cursor would need to choose the target"],
    COMMANDS[2]: ["Codex Review Packet", "non-authorizations confirmed"],
    REGISTER: ["CD-078", "Cursor low-risk chunking delegation is compute prep only", CONTRACT_REL],
    LESSON_INDEX: ["LSN-032", "Cursor low-risk chunking handoffs are compute delegation only", CONTRACT_REL],
    PREFLIGHT: ["CD-078", "LSN-032", CONTRACT_REL],
    READINESS: ["parallel_t404_cursor_low_risk_chunking_handoff", "CD-078", "LSN-032"],
    ROADMAP: ["id: T404", "id: T406", "cursor_may_select_target: false", "Cursor Low-Risk Candidate Research Batch 1"],
    PROJECT_STATUS: ["T404 Cursor low-risk", CONTRACT_REL],
    CURRENT_FOCUS: ["current_task: T404", "cursor_low_risk_chunking_handoff"],
    FRONT_DOOR: [CONTRACT_REL, VALIDATOR_REL, "Cursor may not choose the target"],
    MAIN_TOC: ["t404", "cursor", CONTRACT_REL, VALIDATOR_REL],
    ROADMAP_TOC: ["T404", "Cursor low-risk", CONTRACT_REL],
    SUPPLY_CHAIN: ["10p. Cursor low-risk chunking delegation rule", "Cursor may not choose the target"],
    TASK: ["id: T404", "complete_non_output_changing_cursor_delegation_contract", CONTRACT_REL],
    HANDOFF: ["T404 - Cursor Low-Risk Chunking Handoff", "Files changed", CONTRACT_REL],
    VALIDATE_ALL: ["validate_cursor_low_risk_chunking_handoff.py"],
}


class CursorHandoffError(ValueError):
    """Raised when the T404 Cursor handoff contract drifts."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CursorHandoffError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise CursorHandoffError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise CursorHandoffError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise CursorHandoffError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise CursorHandoffError(f"{label} must contain only non-empty strings")
    return value


def _validate_contract(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "cursor_low_risk_chunking_handoff",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "cursor_low_risk_chunking_handoff.v1",
        "handoff_id": "t404_cursor_low_risk_chunking_handoff",
        "task_id": "T404",
        "status": "complete_non_output_changing_cursor_delegation_contract",
        "owner": "Lowell Wong",
        "decision_register_entry": "CD-078",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise CursorHandoffError(f"{CONTRACT_REL}: {key} must be {value!r}")

    lesson = data.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-032":
        raise CursorHandoffError(f"{CONTRACT_REL}: lesson_recorded.lesson_id must be LSN-032")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise CursorHandoffError(f"{CONTRACT_REL}: authority must be a mapping")
    for key in (
        "records_cursor_delegation_contract",
        "records_low_risk_definition",
        "records_cursor_mode_guidance",
        "records_review_handoff_requirements",
    ):
        if authority.get(key) is not True:
            raise CursorHandoffError(f"{CONTRACT_REL}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise CursorHandoffError(f"{CONTRACT_REL}: authority.{key} must be false")

    reading = set(_require_string_list(data.get("mandatory_reading"), f"{CONTRACT_REL}: mandatory_reading"))
    missing_reading = sorted(REQUIRED_MANDATORY_READING - reading)
    if missing_reading:
        raise CursorHandoffError(f"{CONTRACT_REL}: mandatory_reading missing {missing_reading}")
    for item in reading:
        if not (ROOT / item).exists():
            raise CursorHandoffError(f"{CONTRACT_REL}: mandatory_reading target missing: {item}")

    usage = data.get("cursor_usage")
    if not isinstance(usage, dict):
        raise CursorHandoffError(f"{CONTRACT_REL}: cursor_usage must be a mapping")
    modes = usage.get("preferred_modes")
    if not isinstance(modes, list) or {mode.get("mode") for mode in modes if isinstance(mode, dict)} != {"Plan", "Agent", "Ask"}:
        raise CursorHandoffError(f"{CONTRACT_REL}: cursor_usage.preferred_modes must define Plan, Agent, and Ask")
    commands = usage.get("slash_commands")
    if not isinstance(commands, list) or len(commands) != 3:
        raise CursorHandoffError(f"{CONTRACT_REL}: cursor_usage.slash_commands must contain three commands")
    command_paths = {command.get("path") for command in commands if isinstance(command, dict)}
    required_command_paths = {".cursor/commands/chunking-preflight.md", ".cursor/commands/low-risk-chunking-candidate.md", ".cursor/commands/codex-review-packet.md"}
    if command_paths != required_command_paths:
        raise CursorHandoffError(f"{CONTRACT_REL}: cursor_usage.slash_commands paths must be {sorted(required_command_paths)}")

    eligibility = data.get("low_risk_eligibility")
    if not isinstance(eligibility, dict):
        raise CursorHandoffError(f"{CONTRACT_REL}: low_risk_eligibility must be a mapping")
    if eligibility.get("cursor_may_select_target") is not False:
        raise CursorHandoffError(f"{CONTRACT_REL}: low_risk_eligibility.cursor_may_select_target must be false")
    if eligibility.get("requires_exact_target_from_owner_or_codex") is not True:
        raise CursorHandoffError(f"{CONTRACT_REL}: low_risk_eligibility.requires_exact_target_from_owner_or_codex must be true")
    if eligibility.get("candidate_status_allowed") != "ready_for_review_packet":
        raise CursorHandoffError(f"{CONTRACT_REL}: candidate_status_allowed must be ready_for_review_packet")
    disallowed = set(_require_string_list(eligibility.get("disallowed_statuses"), f"{CONTRACT_REL}: low_risk_eligibility.disallowed_statuses"))
    if not REQUIRED_DISALLOWED_STATUSES <= disallowed:
        raise CursorHandoffError(f"{CONTRACT_REL}: disallowed_statuses missing {sorted(REQUIRED_DISALLOWED_STATUSES - disallowed)}")

    stop_conditions = set(_require_string_list(data.get("stop_conditions"), f"{CONTRACT_REL}: stop_conditions"))
    missing_stops = sorted(REQUIRED_STOP_CONDITIONS - stop_conditions)
    if missing_stops:
        raise CursorHandoffError(f"{CONTRACT_REL}: stop_conditions missing {missing_stops}")

    non_auth = set(_require_string_list(data.get("non_authorizations"), f"{CONTRACT_REL}: non_authorizations"))
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing_non_auth:
        raise CursorHandoffError(f"{CONTRACT_REL}: non_authorizations missing {missing_non_auth}")

    for key in ("allowed_work", "required_cursor_outputs", "codex_review_checklist"):
        _require_string_list(data.get(key), f"{CONTRACT_REL}: {key}")
    verdict = data.get("research_completion_verdict")
    if not isinstance(verdict, dict):
        raise CursorHandoffError(f"{CONTRACT_REL}: research_completion_verdict must be a mapping")
    if verdict.get("t402_queue_research_complete_at_depth") != "all_66_book_candidate_triage":
        raise CursorHandoffError(f"{CONTRACT_REL}: T402 research completion depth must be all_66_book_candidate_triage")
    if verdict.get("ready_for_review_packet_candidates") != 38:
        raise CursorHandoffError(f"{CONTRACT_REL}: ready_for_review_packet_candidates must be 38")
    if verdict.get("next_future_roadmap_task") != "T406":
        raise CursorHandoffError(f"{CONTRACT_REL}: next_future_roadmap_task must be T406")
    algorithms = data.get("algorithms")
    if not isinstance(algorithms, dict):
        raise CursorHandoffError(f"{CONTRACT_REL}: algorithms must be a mapping")
    for key in (
        "preflight_algorithm",
        "eligibility_algorithm",
        "baseline_algorithm",
        "candidate_prep_algorithm",
        "route_isolation_algorithm",
        "review_handoff_algorithm",
    ):
        _require_string_list(algorithms.get(key), f"{CONTRACT_REL}: algorithms.{key}")


def _validate_multi_pass_plan() -> None:
    data = _read_yaml(MULTI_PASS_PLAN)
    expected = {
        "object_type": "low_risk_chunking_multi_pass_plan",
        "schema_version": "low_risk_chunking_multi_pass_plan.v1",
        "plan_id": "t404_low_risk_chunking_multi_pass_plan",
        "task_id": "T404",
        "decision_register_entry": "CD-078",
        "lesson_index_entry": "LSN-032",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: {key} must be {value!r}")
    verdict = data.get("research_completion_verdict")
    if not isinstance(verdict, dict):
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: research_completion_verdict must be a mapping")
    if verdict.get("t402_queue_research_complete_at_depth") != "all_66_book_candidate_triage":
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: completion depth must be all_66_book_candidate_triage")
    if verdict.get("ready_for_review_packet_candidates") != 38:
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: ready candidate count must be 38")
    not_complete = set(_require_string_list(verdict.get("not_complete_at_depths"), f"{_rel(MULTI_PASS_PLAN)}: not_complete_at_depths"))
    for required in ("review_packet_strengthening", "reviewed_gold_promotion", "output_pilot", "embedding_or_vector_work", "theology_authority"):
        if required not in not_complete:
            raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: not_complete_at_depths missing {required}")
    passes = data.get("multi_pass_sequence")
    if not isinstance(passes, list) or len(passes) < 5:
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: multi_pass_sequence must contain at least five passes")
    by_task = {item.get("roadmap_task_id"): item for item in passes if isinstance(item, dict)}
    if by_task.get("T406", {}).get("status") != "planned_future":
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: T406 pass must be planned_future")
    if by_task.get("T406", {}).get("batch_size_limit") != 3:
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: T406 batch_size_limit must be 3")
    if by_task.get("T406", {}).get("cursor_may_select_targets") is not False:
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: T406 cursor_may_select_targets must be false")
    future = data.get("future_roadmap_entry")
    if not isinstance(future, dict) or future.get("next_planned_task_id") != "T406":
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: future_roadmap_entry.next_planned_task_id must be T406")
    non_auth = set(_require_string_list(data.get("non_authorizations"), f"{_rel(MULTI_PASS_PLAN)}: non_authorizations"))
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing_non_auth:
        raise CursorHandoffError(f"{_rel(MULTI_PASS_PLAN)}: non_authorizations missing {missing_non_auth}")


def _validate_text_surfaces() -> None:
    for path, phrases in TEXT_SURFACE_REQUIREMENTS.items():
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise CursorHandoffError(f"{_rel(path)}: missing required T404 phrase {phrase!r}")


def validate_cursor_low_risk_chunking_handoff(path: Path = CONTRACT) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_contract(data)
    _validate_multi_pass_plan()
    _validate_text_surfaces()
    return data


def main() -> int:
    try:
        validate_cursor_low_risk_chunking_handoff()
    except CursorHandoffError as exc:
        print(f"T404 Cursor low-risk chunking handoff validation failed: {exc}", file=sys.stderr)
        return 1
    print("T404 Cursor low-risk chunking handoff validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
