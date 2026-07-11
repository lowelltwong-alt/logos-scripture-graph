#!/usr/bin/env python3
"""Validate the T442 original-language production candidate-root decision packet."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / ".ai" / "control" / "t442_production_candidate_root_decision_packet.yaml"
TASK = ROOT / ".ai" / "tasks" / "T442.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T442" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T442" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T442_PRODUCTION_CANDIDATE_ROOT_DECISION_PACKET.md"
SUBSTRATE = ROOT / ".ai" / "control" / "original_language_evidence_substrate.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
DECISION_REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
OUTBOX = ROOT / "tests" / "fixtures" / "dad" / "candidate_messages.jsonl"

EXPECTED_OPTION_IDS = {"T442-A", "T442-B", "T442-C", "T442-D"}
EXPECTED_REQUIRED_TASKS = {"T431", "T432", "T433", "T435", "T436", "T437", "T438", "T439", "T440", "T441"}
ALLOWED_TRUE_AUTHORITY = {
    "records_owner_options",
    "records_recommendation",
    "records_future_rust_admission_checker_option",
}
FORBIDDEN_TRUE_PREFIXES = ("opens_", "creates_", "stores_", "selects_", "changes_", "runs_", "authorizes_")
PRODUCTION_ROOTS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "alignment_records",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)
REQUIRED_NON_AUTHORIZATIONS = {
    "production_root_opening_now",
    "source_token_row_creation_now",
    "alignment_row_creation_now",
    "editorial_layer_row_creation_now",
    "strongs_overlay_population",
    "lemma_or_morphology_population",
    "source_language_truth",
    "lexical_truth",
    "word_level_alignment_truth",
    "preferred_reading",
    "source_tradition_preference",
    "textual_critical_decision",
    "manuscript_witness_support",
    "translation_faithfulness_judgment",
    "chunk_boundary",
    "reviewed_gold",
    "chunk_output",
    "graph_or_retrieval_truth",
    "retrieval_or_vector_index",
    "theology_authority",
}


class T442ValidationError(ValueError):
    """Raised when T442 loses owner-gate or non-authority controls."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T442ValidationError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T442ValidationError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T442ValidationError(f"{_rel(path)} unreadable: {exc}") from exc


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T442ValidationError(f"{label} must be a list")
    got = {str(item) for item in actual}
    missing = sorted(required - got)
    if missing:
        raise T442ValidationError(f"{label} missing {missing}")


def _require_authority_false(authority: Any, label: str) -> None:
    if not isinstance(authority, dict):
        raise T442ValidationError(f"{label} must be a mapping")
    for key, value in authority.items():
        if key in ALLOWED_TRUE_AUTHORITY:
            if value is not True:
                raise T442ValidationError(f"{label}.{key} must be true")
            continue
        if key.startswith(FORBIDDEN_TRUE_PREFIXES) and value is not False:
            raise T442ValidationError(f"{label}.{key} must be false")


def _validate_packet(packet: dict[str, Any]) -> None:
    expected = {
        "object_type": "t442_production_candidate_root_decision_packet",
        "schema_version": "t442_production_candidate_root_decision_packet.v1",
        "task_id": "T442",
        "owner": "Lowell Wong",
        "status": "pending_owner_decision",
        "trust_zone": "control",
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            raise T442ValidationError(f"packet.{key} must be {value!r}")

    preconditions = packet.get("preconditions")
    if not isinstance(preconditions, dict):
        raise T442ValidationError("preconditions must be a mapping")
    if preconditions.get("requires_pr_stack_merge_or_owner_override") is not True:
        raise T442ValidationError("T442 must require stack merge/readiness or explicit owner override")
    _require_subset(EXPECTED_REQUIRED_TASKS, preconditions.get("required_stack_tasks"), "preconditions.required_stack_tasks")

    selection = packet.get("owner_selection")
    if not isinstance(selection, dict):
        raise T442ValidationError("owner_selection must be a mapping")
    if selection.get("owner_selection_status") != "pending":
        raise T442ValidationError("owner_selection_status must remain pending")
    for key in ("opens_production_candidate_roots", "creates_rows", "recommendation_is_owner_selection"):
        if selection.get(key) is not False:
            raise T442ValidationError(f"owner_selection.{key} must be false")
    if selection.get("selected_option") is not None:
        raise T442ValidationError("owner_selection.selected_option must remain null")

    if packet.get("recommended_option_id") != "T442-A":
        raise T442ValidationError("recommended_option_id must be T442-A")
    recommendation = packet.get("recommendation")
    if not isinstance(recommendation, dict):
        raise T442ValidationError("recommendation must be a mapping")
    if "not owner selection" not in str(recommendation.get("why_not_auto_select", "")):
        raise T442ValidationError("recommendation must explicitly deny owner selection")

    question = packet.get("owner_question")
    if not isinstance(question, dict):
        raise T442ValidationError("owner_question must be a mapping")
    if question.get("must_stop_if_owner_response_is_ambiguous") is not True:
        raise T442ValidationError("ambiguous owner response must stop")
    _require_subset(
        {
            "selected_option",
            "exact_allowed_roots",
            "exact_allowed_source_views",
            "exact_allowed_books_or_spans",
            "required_no_text_policy",
            "required_rust_admission_checker",
            "explicit_non_authorizations",
            "next_task_id",
        },
        question.get("owner_response_must_record"),
        "owner_question.owner_response_must_record",
    )

    options = packet.get("owner_options")
    if not isinstance(options, list):
        raise T442ValidationError("owner_options must be a list")
    by_id = {str(option.get("option_id")): option for option in options if isinstance(option, dict)}
    if set(by_id) != EXPECTED_OPTION_IDS:
        raise T442ValidationError(f"owner_options must be exactly {sorted(EXPECTED_OPTION_IDS)}")
    option_a = by_id["T442-A"]
    for root in (
        "data/candidate/original_language_evidence/source_tokens/",
        "data/candidate/original_language_evidence/alignment_records/",
        "data/candidate/original_language_evidence/editorial_layers/",
    ):
        if root not in option_a.get("allowed_roots_if_selected", []):
            raise T442ValidationError(f"T442-A missing allowed root {root}")
    if option_a.get("requires_future_rust_admission_checker") is not True:
        raise T442ValidationError("T442-A must require a future Rust admission checker")
    for option_id, option in by_id.items():
        for key in ("if_selected_authorizes_immediate_root_creation", "if_selected_authorizes_row_population_now"):
            if option.get(key) is not False:
                raise T442ValidationError(f"{option_id}.{key} must be false")

    future_rust = packet.get("future_rust_slice_if_t442_a_selected")
    if not isinstance(future_rust, dict):
        raise T442ValidationError("future_rust_slice_if_t442_a_selected must be a mapping")
    if future_rust.get("task_shape") != "production_candidate_root_admission_checker":
        raise T442ValidationError("future Rust slice must be an admission checker")
    _require_subset(
        {
            "duplicate ID rejection",
            "canonical ref coverage checks",
            "source-view checksum drift checks",
            "no visible source or translation text leakage checks",
            "forbidden authority flag checks",
            "T439/T440/T441 coverage mismatch checks",
        },
        future_rust.get("responsibilities"),
        "future_rust_slice_if_t442_a_selected.responsibilities",
    )

    _require_authority_false(packet.get("authority"), "authority")
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, packet.get("non_authorizations"), "non_authorizations")
    _require_subset(
        {
            "scripts/validate_t442_production_candidate_root_decision_packet.py",
            "tests/test_t442_production_candidate_root_decision_packet.py",
        },
        packet.get("validators"),
        "validators",
    )


def _validate_no_production_outputs() -> None:
    for path in PRODUCTION_ROOTS:
        if path.exists() and any(path.rglob("*")):
            raise T442ValidationError(f"{_rel(path)} must remain empty until owner-gated implementation")


def _validate_links() -> None:
    required = (PACKET, TASK, HANDOFF, DAD_PREFLIGHT, ROADMAP, SUBSTRATE)
    for path in required:
        if not path.exists():
            raise T442ValidationError(f"{_rel(path)} is missing")

    task = _read_yaml(TASK)
    if task.get("id") != "T442":
        raise T442ValidationError("T442 task id mismatch")
    _require_authority_false(task.get("authorization"), "task.authorization")
    allowed = "\n".join(task.get("scope", {}).get("allowed_paths", []))
    for required_path in (
        ".ai/control/t442_production_candidate_root_decision_packet.yaml",
        "scripts/validate_t442_production_candidate_root_decision_packet.py",
        "tests/test_t442_production_candidate_root_decision_packet.py",
        ".digital-asset/mail/outbox.jsonl",
    ):
        if required_path not in allowed:
            raise T442ValidationError(f"T442 task allowed_paths missing {required_path}")

    substrate = _read_yaml(SUBSTRATE)
    lanes = substrate.get("pilot_lanes")
    if not isinstance(lanes, list) or not any(isinstance(lane, dict) and lane.get("task_id") == "T442" for lane in lanes):
        raise T442ValidationError("original_language_evidence_substrate must include T442 lane")

    text_requirements = (
        (ROADMAP, ("T442-A", "not owner selection", "production-root admission checker", "No production root opening")),
        (HANDOFF, ("Task id: T442", "owner decision packet", "python scripts/validate_all.py")),
        (DAD_PREFLIGHT, ("pilot fixture -> parser contract -> Rust coverage shadow -> owner gate", "future Rust admission checker")),
        (PROJECT_STATUS, ("T442 production candidate-root decision packet", "owner decision packet")),
        (CURRENT_FOCUS, ("current_task: T442", "production candidate-root decision packet")),
        (DECISION_REGISTER, ("CD-098", "T442 production candidate-root decision packet")),
        (VALIDATE_ALL, ("validate_t442_production_candidate_root_decision_packet.py",)),
        (OUTBOX, ("msg-20260705-t442-production-root-gate-lesson", "owner gate -> future Rust admission checker")),
    )
    for path, phrases in text_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T442ValidationError(f"{_rel(path)} missing {phrase!r}")


def validate_t442_packet(path: Path = PACKET) -> dict[str, Any]:
    packet = _read_yaml(path)
    _validate_packet(packet)
    _validate_links()
    _validate_no_production_outputs()
    return packet


def main() -> int:
    try:
        validate_t442_packet()
    except T442ValidationError as exc:
        print(f"T442 production candidate-root decision packet validation failed: {exc}", file=sys.stderr)
        return 1
    print("T442 production candidate-root decision packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
