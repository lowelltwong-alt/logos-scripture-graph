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
LIVE_SAFETY = ROOT / "scripts" / "validate_parallel_execution_safety.py"

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

REQUIRED_BATCH_START_GATES = {
    "one_task_one_branch_one_worktree_claim_recorded",
    "git_status_clean_or_only_current_task_allowed_paths_dirty",
    "no_merge_rebase_cherry_pick_or_bisect_state",
    "no_untracked_artifacts_from_another_task_id_present",
    "shared_control_file_edit_claim_absent_or_owned_by_current_codex_integrator",
    "preflight_result_recorded_in_audit_log",
}

REQUIRED_STOP_WHEN = {
    "untracked_artifacts_from_another_task_id_present",
    "dirty_files_outside_current_task_allowed_paths",
    "shared_control_file_claim_conflict",
    "merge_rebase_cherry_pick_or_bisect_state_detected",
}

REQUIRED_VALIDATION_TIERS = {
    "research",
    "control_plane_or_schema",
    "data_pipeline",
    "output_changing",
    "merge_or_release",
}

REQUIRED_SHARED_CONTROL_FILES = {
    ".ai/control/PROJECT_STATUS.md",
    ".ai/control/current_focus.yaml",
    ".ai/control/handoff_ledger.jsonl",
    ".ai/control/chunking_phase_completion_plan.yaml",
    ".ai/control/bible_chunking_readiness_map.yaml",
    "ROADMAP_STATE.yaml",
    "AI_FRONT_DOOR.md",
    "AI_TABLE_OF_CONTENTS.md",
    "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md",
}

REQUIRED_T411_STARTS_AFTER = {
    "T410_committed_and_merged_to_main",
    "t410_parallel_execution_safety_validates",
    "clean_branch_or_worktree_claimed_for_T411",
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
    ROADMAP_DOC: [
        "T410 Research-To-Chunking Phase One Roadmap",
        "Phase 1 closes only when all 66",
        "Cursor Batch Prompt",
        "Parallel Safety",
        "Validation Tiers",
    ],
    TASK: [
        "id: T410",
        "parallel_chunking_research_program.yaml",
        "cursor_to_codex_transparency_contract.yaml",
        "validate_parallel_execution_safety.py",
    ],
    HANDOFF: ["task_id: T410", "stage:", "Next agent instruction"],
    PROJECT_STATUS: ["T410", "research-to-chunking", "Phase 1"],
    CURRENT_FOCUS: ["current_task: T411", "parallel_chunking_research_program"],
    READINESS: ["parallel_t410_research_to_chunking_phase_one", "chunking_phase_completion_plan.yaml"],
    LOW_RISK_PLAN: ["T410", "research-to-chunking", "Phase 1"],
    HUMAN_FORECAST: ["T410", "chunking_phase_completion_plan.yaml"],
    FRONT_DOOR: ["parallel_chunking_research_program.yaml", "validate_parallel_chunking_prompt_pack.py"],
    MAIN_TOC: ["t410", "research-to-chunking", "parallel_chunking_research_program.yaml"],
    ROADMAP_TOC: ["T410", "Research-to-chunking", "chunking_phase_completion_plan.yaml"],
    ROADMAP_STATE: ["id: T410", "Research-To-Chunking Phase One Roadmap"],
    VALIDATE_ALL: ["validate_parallel_chunking_prompt_pack.py", "validate_parallel_execution_safety.py"],
    LIVE_SAFETY: ["Validate live branch/worktree safety", "allow-current-task-dirty", "require-task-branch"],
    CURSOR_RULE: ["T410", "Cursor is a research and prep workhorse only", "one task id, one branch, and one worktree"],
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
        "live_safety_validator": "scripts/validate_parallel_execution_safety.py",
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
    for key in ("required_before_batch_start", "required_before_next_book", "must_stop_before", "must_stop_when"):
        _string_list(advance.get(key), f"{_rel(path)}: cursor_advance_gate.{key}")
    batch_start = set(advance.get("required_before_batch_start", []))
    missing_batch = sorted(REQUIRED_BATCH_START_GATES - batch_start)
    if missing_batch:
        raise PromptPackError(f"{_rel(path)}: cursor_advance_gate.required_before_batch_start missing {missing_batch}")
    stop_when = set(advance.get("must_stop_when", []))
    missing_stop = sorted(REQUIRED_STOP_WHEN - stop_when)
    if missing_stop:
        raise PromptPackError(f"{_rel(path)}: cursor_advance_gate.must_stop_when missing {missing_stop}")
    safety = data.get("parallel_execution_safety")
    if not isinstance(safety, dict):
        raise PromptPackError(f"{_rel(path)}: parallel_execution_safety must be a mapping")
    branch_rule = str(safety.get("branch_worktree_rule", "")).lower()
    if "one task" not in branch_rule or "one branch" not in branch_rule or "one worktree" not in branch_rule:
        raise PromptPackError(f"{_rel(path)}: parallel_execution_safety.branch_worktree_rule must require one task, one branch, and one worktree")
    clean = safety.get("clean_status_preflight")
    if not isinstance(clean, dict) or clean.get("required") is not True or clean.get("command") != "git status --short --branch":
        raise PromptPackError(f"{_rel(path)}: clean_status_preflight must require git status --short --branch")
    merge = safety.get("merge_state_preflight")
    if not isinstance(merge, dict) or merge.get("required") is not True:
        raise PromptPackError(f"{_rel(path)}: merge_state_preflight must be required")
    forbidden_states = set(_string_list(merge.get("forbidden_states"), f"{_rel(path)}: merge_state_preflight.forbidden_states"))
    if forbidden_states != {"merge", "rebase", "cherry_pick", "bisect"}:
        raise PromptPackError(f"{_rel(path)}: merge_state_preflight.forbidden_states must cover merge/rebase/cherry_pick/bisect")
    isolation = safety.get("task_artifact_isolation")
    if not isinstance(isolation, dict) or isolation.get("cursor_must_not_write_shared_control_plane") is not True:
        raise PromptPackError(f"{_rel(path)}: task_artifact_isolation must block Cursor shared control-plane writes")
    roots = set(_string_list(isolation.get("cursor_allowed_write_roots"), f"{_rel(path)}: task_artifact_isolation.cursor_allowed_write_roots"))
    if roots != {".ai/context/agent_work/<TASK_ID>/", ".ai/handoffs/<TASK_ID>/"}:
        raise PromptPackError(f"{_rel(path)}: Cursor write roots must be task-scoped agent_work and handoffs only")
    shared = safety.get("shared_control_file_serialization")
    if not isinstance(shared, dict) or shared.get("integrator_role") != "Codex" or shared.get("merge_order_required") is not True:
        raise PromptPackError(f"{_rel(path)}: shared_control_file_serialization must require Codex integrator merge order")
    shared_files = set(_string_list(shared.get("shared_files"), f"{_rel(path)}: shared_control_file_serialization.shared_files"))
    missing_shared = sorted(REQUIRED_SHARED_CONTROL_FILES - shared_files)
    if missing_shared:
        raise PromptPackError(f"{_rel(path)}: shared_control_file_serialization.shared_files missing {missing_shared}")
    file_claim = safety.get("file_claim_rule")
    if not isinstance(file_claim, dict) or file_claim.get("cursor_batches_claim_task_roots_only") is not True:
        raise PromptPackError(f"{_rel(path)}: file_claim_rule must limit Cursor claims to task roots")
    stop_conditions = set(_string_list(safety.get("stop_conditions"), f"{_rel(path)}: parallel_execution_safety.stop_conditions"))
    missing_safety_stop = sorted(REQUIRED_STOP_WHEN - stop_conditions)
    if missing_safety_stop:
        raise PromptPackError(f"{_rel(path)}: parallel_execution_safety.stop_conditions missing {missing_safety_stop}")
    sequence = data.get("phase_one_task_sequence")
    if not isinstance(sequence, list):
        raise PromptPackError(f"{_rel(path)}: phase_one_task_sequence must be a list")
    t411 = next((item for item in sequence if isinstance(item, dict) and item.get("task_id") == "T411"), None)
    if not isinstance(t411, dict):
        raise PromptPackError(f"{_rel(path)}: phase_one_task_sequence must include T411")
    starts_after = set(_string_list(t411.get("starts_after"), f"{_rel(path)}: T411.starts_after"))
    missing_starts_after = sorted(REQUIRED_T411_STARTS_AFTER - starts_after)
    if missing_starts_after:
        raise PromptPackError(f"{_rel(path)}: T411.starts_after missing {missing_starts_after}")
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
    if "git_status_preflight" not in data.get("audit_log_fields", []):
        raise PromptPackError(f"{_rel(path)}: audit_log_fields must include git_status_preflight")
    if set(_string_list(data.get("confidence_values"), f"{_rel(path)}: confidence_values")) != {"high", "medium", "low", "blocked"}:
        raise PromptPackError(f"{_rel(path)}: confidence_values must be high/medium/low/blocked")
    tiers = data.get("validation_tiers")
    if not isinstance(tiers, dict):
        raise PromptPackError(f"{_rel(path)}: validation_tiers must be a mapping")
    missing_tiers = sorted(REQUIRED_VALIDATION_TIERS - set(tiers))
    if missing_tiers:
        raise PromptPackError(f"{_rel(path)}: validation_tiers missing {missing_tiers}")
    for tier_name in REQUIRED_VALIDATION_TIERS:
        tier = tiers.get(tier_name)
        if not isinstance(tier, dict):
            raise PromptPackError(f"{_rel(path)}: validation_tiers.{tier_name} must be a mapping")
        _string_list(tier.get("applies_to"), f"{_rel(path)}: validation_tiers.{tier_name}.applies_to")
        _string_list(tier.get("required_gates"), f"{_rel(path)}: validation_tiers.{tier_name}.required_gates")
    research_gates = set(tiers["research"].get("required_gates", []))
    if "python scripts/validate_parallel_execution_safety.py --task-id <TASK_ID> --require-task-branch" not in research_gates:
        raise PromptPackError(f"{_rel(path)}: validation_tiers.research must require live parallel execution safety preflight")
    if tiers["research"].get("full_pytest_required_before_merge") is not False:
        raise PromptPackError(f"{_rel(path)}: validation_tiers.research must not require full pytest before merge")
    for tier_name in ("control_plane_or_schema", "data_pipeline", "output_changing", "merge_or_release"):
        if tiers[tier_name].get("validate_all_required_before_merge") is not True:
            raise PromptPackError(f"{_rel(path)}: validation_tiers.{tier_name} must require validate_all before merge")
    for tier_name in ("control_plane_or_schema", "data_pipeline", "output_changing"):
        gates = set(tiers[tier_name].get("required_gates", []))
        if "python scripts/validate_parallel_execution_safety.py --task-id <TASK_ID> --allow-current-task-dirty --require-task-branch" not in gates:
            raise PromptPackError(f"{_rel(path)}: validation_tiers.{tier_name} must require in-progress live safety validation")
        if "python -m pytest -q" not in gates:
            raise PromptPackError(f"{_rel(path)}: validation_tiers.{tier_name} must require full pytest")
    output_gates = set(tiers["output_changing"].get("required_gates", []))
    for required_gate in ("owner_authorization_record", "route_isolation_harness", "non_target_identity_proof"):
        if required_gate not in output_gates:
            raise PromptPackError(f"{_rel(path)}: validation_tiers.output_changing.required_gates missing {required_gate}")
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
