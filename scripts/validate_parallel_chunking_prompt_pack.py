#!/usr/bin/env python3
"""Validate the T410 parallel chunking prompt-pack and Phase 1 plan."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

PROGRAM = ROOT / ".ai" / "control" / "parallel_chunking_research_program.yaml"
BOOK_HINTS = ROOT / ".ai" / "control" / "bible_book_literature_prompt_hints.yaml"
TRANSPARENCY = ROOT / ".ai" / "control" / "cursor_to_codex_transparency_contract.yaml"
FRONTIER = ROOT / ".ai" / "control" / "frontier_chunking_escalation_policy.yaml"
COMPLETION = ROOT / ".ai" / "control" / "chunking_phase_completion_plan.yaml"
CANON = ROOT / "config" / "canon" / "canonical_66_books.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T410_RESEARCH_TO_CHUNKING_PHASE_ONE_ROADMAP.md"
TASK = ROOT / ".ai" / "tasks" / "T410.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T410" / "handoff.md"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
LOW_RISK_PLAN = ROOT / ".ai" / "control" / "low_risk_chunking_multi_pass_plan.yaml"
HUMAN_FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

COMMANDS = [
    ROOT / ".cursor" / "commands" / "verse-ledger-batch.md",
    ROOT / ".cursor" / "commands" / "review-packet-batch.md",
    ROOT / ".cursor" / "commands" / "next-book-or-stop.md",
    ROOT / ".cursor" / "commands" / "frontier-escalation-packet.md",
    ROOT / ".cursor" / "commands" / "codex-prompt-pack-review.md",
]
CURSOR_RULE = ROOT / ".cursor" / "rules" / "logos-scripture-parallel-verse-research.mdc"

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
    "authorizes_backend_choice",
    "authorizes_retrieval_profile_promotion",
    "authorizes_preferred_reading_or_source_tradition",
    "authorizes_canon_scope_change",
    "authorizes_source_or_manuscript_row_population",
    "authorizes_theology_authority_change",
}

REQUIRED_NON_AUTHORIZATIONS = {
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
    "theology_authority_change",
}

PHASE_LADDER = [
    "research",
    "review_packet_prep",
    "codex_review",
    "frontier_escalation",
    "owner_gate",
    "reviewed_gold_promotion",
    "route_isolated_harness",
    "output_changing_pr",
    "post_pilot_review",
]

REQUIRED_TRANSPARENCY_FILES = {
    "source_size_manifest.jsonl",
    "confidence_register.jsonl",
    "audit_log.jsonl",
    "claim_traceability_matrix.md",
}

REQUIRED_FRONTIER_TRIGGERS = {
    "prophecy_or_oracle_boundary",
    "apocalyptic_or_vision_cycle",
    "dense_epistle_argument",
    "gospel_wj_or_speaker_boundary",
    "textual_variant_or_source_tradition_pressure",
    "doxology_or_benediction_boundary",
    "christology_or_trinity_pressure",
    "law_gospel_or_covenant_system_pressure",
    "ecclesiology_or_office_pressure",
    "original_language_claim_controls_boundary",
    "source_metadata_would_become_boundary_authority",
    "low_confidence_or_blocked_claim",
}

TEXT_REQUIREMENTS = {
    ROADMAP_DOC: ["T410 Research-To-Chunking Phase One Roadmap", "Phase 1 closes only when all 66", "Cursor Batch Prompt"],
    TASK: ["id: T410", "parallel_chunking_research_program.yaml", "cursor_to_codex_transparency_contract.yaml"],
    HANDOFF: ["task_id: T410", "stage:", "Next agent instruction"],
    PROJECT_STATUS: ["T410", "research-to-chunking", "Phase 1"],
    CURRENT_FOCUS: ["current_task: T410", "parallel_chunking_research_program"],
    READINESS: ["parallel_t410_research_to_chunking_phase_one", "chunking_phase_completion_plan.yaml"],
    LOW_RISK_PLAN: ["T410", "research-to-chunking", "Phase 1"],
    HUMAN_FORECAST: ["T410", "chunking_phase_completion_plan.yaml"],
    FRONT_DOOR: ["parallel_chunking_research_program.yaml", "validate_parallel_chunking_prompt_pack.py"],
    MAIN_TOC: ["t410", "research-to-chunking", "parallel_chunking_research_program.yaml"],
    ROADMAP_TOC: ["T410", "Research-to-chunking", "chunking_phase_completion_plan.yaml"],
    ROADMAP_STATE: ["id: T410", "Research-To-Chunking Phase One Roadmap"],
    VALIDATE_ALL: ["validate_parallel_chunking_prompt_pack.py"],
    CURSOR_RULE: ["T410", "Cursor is a research and prep workhorse only"],
}


class PromptPackError(ValueError):
    """Raised when the T410 prompt-pack program drifts."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PromptPackError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise PromptPackError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise PromptPackError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise PromptPackError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise PromptPackError(f"{label} must contain only non-empty strings")
    return value


def _canonical_books() -> list[str]:
    data = _read_yaml(CANON)
    books = data.get("canonical_66_books")
    if not isinstance(books, list) or len(books) != 66:
        raise PromptPackError("canonical_66_books.yaml must define exactly 66 books")
    return [str(book) for book in books]


def _require_false_authority(authority: Any, path: Path, required: set[str] = REQUIRED_FALSE_AUTHORITY) -> None:
    if not isinstance(authority, dict):
        raise PromptPackError(f"{_rel(path)}: authority must be a mapping")
    for key in required:
        if authority.get(key) is not False:
            raise PromptPackError(f"{_rel(path)}: authority.{key} must be false")


def _require_non_authorizations(data: dict[str, Any], path: Path, required: set[str] = REQUIRED_NON_AUTHORIZATIONS) -> None:
    non_auth = set(_string_list(data.get("non_authorizations"), f"{_rel(path)}: non_authorizations"))
    missing = sorted(required - non_auth)
    if missing:
        raise PromptPackError(f"{_rel(path)}: non_authorizations missing {missing}")


def validate_program(path: Path = PROGRAM) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "parallel_chunking_research_program",
        "schema_version": "parallel_chunking_research_program.v1",
        "program_id": "t410_parallel_chunking_research_program",
        "task_id": "T410",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise PromptPackError(f"{_rel(path)}: {key} must be {value!r}")
    _require_false_authority(data.get("authority"), path)
    ladder = data.get("phase_ladder")
    if not isinstance(ladder, list) or [item.get("step_id") for item in ladder if isinstance(item, dict)] != PHASE_LADDER:
        raise PromptPackError(f"{_rel(path)}: phase_ladder must define the T410 nine-step ladder in order")
    if [item.get("order") for item in ladder if isinstance(item, dict)] != list(range(1, 10)):
        raise PromptPackError(f"{_rel(path)}: phase_ladder order values must be 1 through 9")
    phase_one = data.get("phase_one_definition")
    if not isinstance(phase_one, dict) or "66" not in phase_one.get("completion_rule", ""):
        raise PromptPackError(f"{_rel(path)}: phase_one_definition.completion_rule must mention all 66 books")
    future = data.get("future_phases")
    if not isinstance(future, list) or [item.get("phase") for item in future if isinstance(item, dict)] != [2, 3, 4, 5, 6]:
        raise PromptPackError(f"{_rel(path)}: future_phases must define phases 2 through 6")
    advance = data.get("cursor_advance_gate")
    if not isinstance(advance, dict):
        raise PromptPackError(f"{_rel(path)}: cursor_advance_gate must be a mapping")
    for key in ("required_before_next_book", "must_stop_before"):
        _string_list(advance.get(key), f"{_rel(path)}: cursor_advance_gate.{key}")
    _require_non_authorizations(data, path, REQUIRED_NON_AUTHORIZATIONS | {"cursor_target_selection", "exact_target_selection"})
    return data


def validate_transparency(path: Path = TRANSPARENCY) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "cursor_to_codex_transparency_contract" or data.get("task_id") != "T410":
        raise PromptPackError(f"{_rel(path)}: must be the T410 transparency contract")
    _require_false_authority(
        data.get("authority"),
        path,
        {
            "authorizes_chunk_output_change",
            "authorizes_reviewed_gold_promotion",
            "authorizes_graph_edges",
            "authorizes_retrieval_truth",
            "authorizes_embedding_or_vector_work",
            "authorizes_theology_authority_change",
        },
    )
    note = data.get("required_handoff_note")
    if not isinstance(note, dict) or note.get("path_template") != ".ai/handoffs/<TASK_ID>/cursor_notes_to_codex.md":
        raise PromptPackError(f"{_rel(path)}: required_handoff_note.path_template is wrong")
    logs = data.get("required_machine_logs")
    if not isinstance(logs, dict):
        raise PromptPackError(f"{_rel(path)}: required_machine_logs must be a mapping")
    files = set(_string_list(logs.get("files"), f"{_rel(path)}: required_machine_logs.files"))
    missing = sorted(REQUIRED_TRANSPARENCY_FILES - files)
    if missing:
        raise PromptPackError(f"{_rel(path)}: required_machine_logs.files missing {missing}")
    for key in ("source_size_manifest_fields", "confidence_register_fields", "audit_log_fields", "claim_rules"):
        _string_list(data.get(key), f"{_rel(path)}: {key}")
    if set(_string_list(data.get("confidence_values"), f"{_rel(path)}: confidence_values")) != {"high", "medium", "low", "blocked"}:
        raise PromptPackError(f"{_rel(path)}: confidence_values must be high/medium/low/blocked")
    _require_non_authorizations(data, path)
    return data


def validate_frontier_policy(path: Path = FRONTIER) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "frontier_chunking_escalation_policy" or data.get("task_id") != "T410":
        raise PromptPackError(f"{_rel(path)}: must be the T410 frontier escalation policy")
    _require_false_authority(
        data.get("authority"),
        path,
        {
            "authorizes_exact_target_selection",
            "authorizes_reviewed_gold_promotion",
            "authorizes_chunk_output_change",
            "authorizes_route_behavior_change",
            "authorizes_evaluator_change",
            "authorizes_graph_edges",
            "authorizes_retrieval_truth",
            "authorizes_embedding_or_vector_work",
            "authorizes_theology_authority_change",
        },
    )
    triggers = set(_string_list(data.get("mandatory_escalation_triggers"), f"{_rel(path)}: mandatory_escalation_triggers"))
    missing = sorted(REQUIRED_FRONTIER_TRIGGERS - triggers)
    if missing:
        raise PromptPackError(f"{_rel(path)}: mandatory_escalation_triggers missing {missing}")
    _string_list(data.get("frontier_default_books"), f"{_rel(path)}: frontier_default_books")
    _string_list(data.get("escalation_packet_required_fields"), f"{_rel(path)}: escalation_packet_required_fields")
    _require_non_authorizations(data, path)
    return data


def validate_book_hints(path: Path = BOOK_HINTS) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "bible_book_literature_prompt_hints" or data.get("task_id") != "T410":
        raise PromptPackError(f"{_rel(path)}: must be the T410 book prompt hints")
    required_fields = set(_string_list(data.get("required_fields"), f"{_rel(path)}: required_fields"))
    for field in (
        "book_id",
        "testament",
        "primary_language_layer",
        "primary_genre",
        "literary_modes",
        "t409_risk",
        "phase_one_default",
        "frontier_required_by_default",
        "chunking_ramifications",
        "escalation_triggers",
    ):
        if field not in required_fields:
            raise PromptPackError(f"{_rel(path)}: required_fields missing {field}")
    hints = data.get("book_hints")
    if not isinstance(hints, list):
        raise PromptPackError(f"{_rel(path)}: book_hints must be a list")
    canonical = _canonical_books()
    ids = [item.get("book_id") for item in hints if isinstance(item, dict)]
    if ids != canonical:
        raise PromptPackError(f"{_rel(path)}: book_hints must match canonical 66 order")
    allowed_risks = {"low", "medium", "high"}
    for item in hints:
        if not isinstance(item, dict):
            raise PromptPackError(f"{_rel(path)}: each book hint must be a mapping")
        for field in required_fields:
            if field not in item:
                raise PromptPackError(f"{_rel(path)}: {item.get('book_id')}: missing {field}")
        if item["t409_risk"] not in allowed_risks:
            raise PromptPackError(f"{_rel(path)}: {item['book_id']}: invalid t409_risk")
        if not isinstance(item["frontier_required_by_default"], bool):
            raise PromptPackError(f"{_rel(path)}: {item['book_id']}: frontier_required_by_default must be bool")
        for key in ("literary_modes", "chunking_ramifications", "escalation_triggers"):
            _string_list(item.get(key), f"{_rel(path)}: {item['book_id']}.{key}")
    default_books = set(validate_frontier_policy().get("frontier_default_books", []))
    hint_map = {item["book_id"]: item for item in hints}
    for book in default_books:
        if book not in hint_map:
            raise PromptPackError(f"{_rel(path)}: frontier default book {book} missing from hints")
        if hint_map[book].get("frontier_required_by_default") is not True:
            raise PromptPackError(f"{_rel(path)}: frontier default book {book} must require frontier by default")
    _require_non_authorizations(data, path, {"chunk_output_change", "reviewed_gold_promotion", "child_span_selection", "theology_authority_change"})
    return data


def validate_completion_plan(path: Path = COMPLETION) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "chunking_phase_completion_plan" or data.get("task_id") != "T410":
        raise PromptPackError(f"{_rel(path)}: must be the T410 phase completion plan")
    _require_false_authority(
        data.get("authority"),
        path,
        {
            "authorizes_chunk_output_change",
            "authorizes_reviewed_gold_promotion",
            "authorizes_child_spans",
            "authorizes_route_behavior_change",
            "authorizes_evaluator_change",
            "authorizes_whole_bible_output_pass",
            "authorizes_theology_authority_change",
        },
    )
    statuses = data.get("initial_phase_one_statuses")
    if not isinstance(statuses, list):
        raise PromptPackError(f"{_rel(path)}: initial_phase_one_statuses must be a list")
    canonical = _canonical_books()
    ids = [item.get("book_id") for item in statuses if isinstance(item, dict)]
    if ids != canonical:
        raise PromptPackError(f"{_rel(path)}: initial_phase_one_statuses must match canonical 66 order")
    allowed = set((data.get("status_values") or {}).keys())
    if not allowed:
        raise PromptPackError(f"{_rel(path)}: status_values must be a non-empty mapping")
    used: set[str] = set()
    for item in statuses:
        if not isinstance(item, dict) or item.get("status") not in allowed or not item.get("route"):
            raise PromptPackError(f"{_rel(path)}: each initial status needs a valid status and route")
        used.add(item["status"])
    for required in ("implemented_existing_pilot", "pending_phase_one_gate", "deferred_phase_two_or_frontier_default"):
        if required not in used:
            raise PromptPackError(f"{_rel(path)}: initial statuses must include {required}")
    routes = data.get("future_phase_routes")
    if not isinstance(routes, dict) or sorted(routes.keys()) != ["phase_2", "phase_3", "phase_4", "phase_5", "phase_6"]:
        raise PromptPackError(f"{_rel(path)}: future_phase_routes must define phase_2 through phase_6")
    _require_non_authorizations(data, path)
    return data


def validate_text_surfaces() -> None:
    for command in COMMANDS:
        text = _read_text(command)
        for phrase in ("Cursor", "Stop", "non-authorizing"):
            if phrase not in text:
                raise PromptPackError(f"{_rel(command)}: missing required phrase {phrase!r}")
    for path, phrases in TEXT_REQUIREMENTS.items():
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise PromptPackError(f"{_rel(path)}: missing required T410 phrase {phrase!r}")


def validate_parallel_chunking_prompt_pack() -> dict[str, Any]:
    program = validate_program()
    validate_transparency()
    validate_frontier_policy()
    validate_book_hints()
    validate_completion_plan()
    validate_text_surfaces()
    return program


def main() -> int:
    try:
        validate_parallel_chunking_prompt_pack()
    except PromptPackError as exc:
        print(f"T410 parallel chunking prompt-pack validation failed: {exc}", file=sys.stderr)
        return 1
    print("T410 parallel chunking prompt-pack validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
