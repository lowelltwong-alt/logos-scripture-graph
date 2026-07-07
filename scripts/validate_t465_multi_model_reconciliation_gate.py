#!/usr/bin/env python3
"""Validate T465 reconciliation packets and Mark 16 specialist gate."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

EXPECTED_CANDIDATE_IDS = {
    "DELTA-1Chr-012",
    "DELTA-1Chr-015",
    "DELTA-1Chr-025",
    "DELTA-1Chr-026",
    "DELTA-1Chr-027",
    "DELTA-1Sam-030",
    "DELTA-2Chr-029",
    "DELTA-2Chr-034",
    "DELTA-2John-001",
    "DELTA-2Kgs-019",
    "DELTA-2Sam-015",
    "DELTA-2Tim-004",
    "DELTA-Exod-034",
    "DELTA-Josh-013",
    "DELTA-Josh-018",
    "DELTA-Neh-011",
    "DELTA-Num-029",
    "DELTA-Num-032",
    "DELTA-Num-036",
}

FORBIDDEN_AUTHORIZATION_FIELDS = {
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "authorizes_target_selection",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_truth",
    "creates_retrieval_truth",
    "creates_vector_truth",
    "selects_preferred_reading",
    "selects_source_tradition",
    "changes_canon_scope",
    "decides_mark16_inspiration_status",
    "authorizes_theology_authority",
}

REQUIRED_FILES = {
    "task": ".ai/tasks/T465.task.yaml",
    "control": ".ai/control/t465_multi_model_reconciliation_gate.yaml",
    "roadmap": "docs/roadmap/T465_MULTI_MODEL_CHUNKING_RECONCILIATION_GATE.md",
    "handoff": ".ai/handoffs/T465/handoff.md",
    "harness": ".ai/context/agent_work/T465/harness_triage.md",
    "mark16": ".ai/context/agent_work/T465/mark16_specialist_packet.md",
    "docket": ".ai/context/agent_work/T465/owner_candidate_docket.yaml",
    "prompt": ".ai/prompts/t465_mark16_frontier_specialist_review_prompt.md",
}

TEXT_REQUIRED = {
    "harness": [
        "78 `harness_fix_or_rerun_required` rows",
        "M1_cursor",
        "M5_gemini_thinking",
        "M2_claude_sonnet5",
        "M3_claude_frontier",
        "M4_codex_gpt55",
        "M6_fable5",
        "No reviewed gold",
        "chunk output",
    ],
    "mark16": [
        "DELTA-Mark-016",
        "Mark.16.9-Mark.16.20",
        "Codex Vaticanus layout",
        "Codex Sinaiticus ending",
        "letters-per-line",
        "letters-per-column",
        "blank-space",
        "Patristic evidence",
        "Research-Needed Fields",
        "Non-Authorizations",
    ],
    "prompt": [
        "Claude/frontier",
        "not make a chunk-output task",
        "Do not select a preferred reading",
        "Codex Vaticanus blank-space/layout",
        "Codex Sinaiticus ending",
        "letters-per-line",
        "letters-per-column",
        "no chunk output",
        "reviewed gold",
    ],
    "roadmap": [
        "T465",
        "19",
        "M4_codex_gpt55",
        "M6_fable5",
        "Mark 16",
        "Non-Authorizations",
    ],
}


class ValidationError(Exception):
    """Raised when the T465 package fails validation."""


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(_strip_front_matter(path.read_text(encoding="utf-8")))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: expected YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            row = json.loads(stripped)
            if not isinstance(row, dict):
                raise ValidationError(f"{path}:{line_no}: expected JSON object")
            rows.append(row)
    return rows


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _validate_authorization_block(block: dict[str, Any], label: str, errors: list[str]) -> None:
    for field in FORBIDDEN_AUTHORIZATION_FIELDS:
        if block.get(field) is not False:
            errors.append(f"{label}: {field} must be false")


def _validate_required_text(paths: dict[str, Path], errors: list[str]) -> None:
    for key, needles in TEXT_REQUIRED.items():
        text = paths[key].read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{paths[key]}: missing required text {needle!r}")
        lower = text.lower()
        forbidden_phrases = [
            "authorizes reviewed gold",
            "authorizes chunk output",
            "selects the preferred reading",
            "decides mark 16 inspiration",
            "changes canon scope",
        ]
        for phrase in forbidden_phrases:
            index = lower.find(phrase)
            if index != -1 and "no " not in lower[max(0, index - 8):index]:
                errors.append(f"{paths[key]}: suspicious authority phrase {phrase!r}")


def _validate_owner_docket(docket: dict[str, Any], t464_docket: dict[str, Any], errors: list[str]) -> None:
    _require(docket.get("object_type") == "t465_owner_candidate_docket", "owner docket object_type mismatch", errors)
    _require(docket.get("task_id") == "T465", "owner docket task_id must be T465", errors)
    _require(docket.get("source_task_id") == "T464", "owner docket source_task_id must be T464", errors)
    _require(docket.get("candidate_count") == 19, "owner docket candidate_count must be 19", errors)
    _require(docket.get("non_authorizing") is True, "owner docket must be non_authorizing", errors)
    _require(docket.get("promotion_authority") in {"none", None}, "owner docket promotion_authority must be none", errors)
    _require(docket.get("owner_gate_required_before_any_promotion") is True, "owner gate required flag missing", errors)

    candidates = docket.get("candidates")
    if not isinstance(candidates, list):
        errors.append("owner docket candidates must be a list")
        return
    candidate_ids = {str(row.get("source_id")) for row in candidates if isinstance(row, dict)}
    if candidate_ids != EXPECTED_CANDIDATE_IDS:
        errors.append(f"owner docket candidate IDs mismatch: missing {sorted(EXPECTED_CANDIDATE_IDS - candidate_ids)}, extra {sorted(candidate_ids - EXPECTED_CANDIDATE_IDS)}")
    if len(candidates) != 19:
        errors.append("owner docket must contain 19 candidates")

    statuses = t464_docket.get("statuses", {})
    expected_rows = statuses.get("codex_fable_recommended_candidate", []) if isinstance(statuses, dict) else []
    expected_from_t464 = {str(row.get("source_id")) for row in expected_rows if isinstance(row, dict)}
    if expected_from_t464 and candidate_ids != expected_from_t464:
        errors.append("owner docket must mirror T464 codex_fable_recommended_candidate IDs")

    for index, row in enumerate(candidates, start=1):
        label = f"owner candidate {index}"
        if not isinstance(row, dict):
            errors.append(f"{label}: must be mapping")
            continue
        _require(row.get("recommended_candidate_basis") == "codex_fable_alignment", f"{label}: basis must be codex_fable_alignment", errors)
        _require(row.get("non_authorizing") is True, f"{label}: non_authorizing must be true", errors)
        _require(row.get("promotion_authority") in {"none", None}, f"{label}: promotion_authority must be none", errors)
        risk_flags = row.get("risk_flags", [])
        _require(risk_flags == ["strongs_original_language_metadata"], f"{label}: only Strong's metadata risk expected", errors)
        next_gate = str(row.get("next_gate", ""))
        _require("promotion" not in next_gate and "output" not in next_gate, f"{label}: next_gate must not imply promotion/output", errors)


def _validate_control(control: dict[str, Any], task: dict[str, Any], errors: list[str]) -> None:
    _require(control.get("object_type") == "t465_multi_model_reconciliation_gate", "control object_type mismatch", errors)
    _require(control.get("task_id") == "T465", "control task_id must be T465", errors)
    _require(control.get("source_task_id") == "T464", "control source_task_id must be T464", errors)
    auth = control.get("authorization", {})
    if not isinstance(auth, dict):
        errors.append("control authorization must be mapping")
    else:
        _validate_authorization_block(auth, "control.authorization", errors)
        _require(auth.get("records_reconciliation_next_actions") is True, "control must record reconciliation next actions", errors)
    mark16 = control.get("mark16_gate", {})
    if not isinstance(mark16, dict):
        errors.append("control mark16_gate must be mapping")
    else:
        _require(mark16.get("source_id") == "DELTA-Mark-016", "mark16 source_id mismatch", errors)
        _require(mark16.get("packet_status") == "frontier_specialist_review_needed", "mark16 packet_status mismatch", errors)
        lanes = set(mark16.get("specialist_lanes", []))
        for lane in {
            "codex_vaticanus_layout_blank_space_review",
            "codex_sinaiticus_ending_review",
            "scribal_letters_per_line_and_column_capacity_review",
            "patristic_evidence_review",
        }:
            _require(lane in lanes, f"mark16 specialist lane missing {lane}", errors)

    task_auth = task.get("authorization", {})
    if not isinstance(task_auth, dict):
        errors.append("task authorization must be mapping")
    else:
        task_field_map = {
            "authorizes_reviewed_gold": "authorizes_reviewed_gold",
            "authorizes_chunk_output": "authorizes_chunk_output",
            "authorizes_child_spans": "authorizes_child_spans",
            "authorizes_target_selection": "authorizes_target_selection",
            "changes_route_behavior": "changes_route_behavior",
            "changes_evaluator_behavior": "changes_evaluator_behavior",
            "creates_graph_truth": "creates_graph_or_retrieval_truth",
            "creates_retrieval_truth": "creates_graph_or_retrieval_truth",
            "creates_vector_truth": "creates_graph_or_retrieval_truth",
            "selects_preferred_reading": "selects_preferred_reading_or_source_tradition",
            "selects_source_tradition": "selects_preferred_reading_or_source_tradition",
            "changes_canon_scope": "changes_canon_scope",
            "decides_mark16_inspiration_status": "decides_mark16_inspiration_or_canon_status",
            "authorizes_theology_authority": "authorizes_theology_authority",
        }
        for task_field in task_field_map.values():
            if task_auth.get(task_field) is not False:
                errors.append(f"task.authorization: {task_field} must be false")


def _validate_mark16_source_row(root: Path, errors: list[str]) -> None:
    frontier_path = root / ".ai" / "scratch" / "multi_model_bible_chunking" / "comparison" / "frontier_review_queue.jsonl"
    if not frontier_path.is_file():
        errors.append("missing T464 frontier_review_queue.jsonl")
        return
    mark_rows = [row for row in _read_jsonl(frontier_path) if row.get("source_id") == "DELTA-Mark-016"]
    _require(len(mark_rows) == 1, "frontier queue must contain exactly one DELTA-Mark-016 row", errors)
    if not mark_rows:
        return
    row = mark_rows[0]
    risk_flags = set(row.get("risk_flags", []))
    for flag in {"variant_hot_zone", "wj_or_red_letter", "low_confidence", "high_risk_book"}:
        _require(flag in risk_flags, f"DELTA-Mark-016 missing risk flag {flag}", errors)
    lanes = set(row.get("expert_review_lanes", []))
    for lane in {"codex_vaticanus_layout_review", "codex_sinaiticus_ending_review", "mark16_longer_ending_specialist_packet"}:
        _require(lane in lanes, f"DELTA-Mark-016 missing expert lane {lane}", errors)
    _require(row.get("non_authorizing") is True, "DELTA-Mark-016 must be non_authorizing in T464 queue", errors)


def validate_t465_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {key: root / rel for key, rel in REQUIRED_FILES.items()}
    for key, path in paths.items():
        if not path.is_file():
            errors.append(f"missing required T465 file {REQUIRED_FILES[key]}")
    if errors:
        return errors

    control = _read_yaml(paths["control"])
    task = _read_yaml(paths["task"])
    docket = _read_yaml(paths["docket"])
    t464_docket_path = root / ".ai" / "scratch" / "multi_model_bible_chunking" / "comparison" / "owner_decision_docket.yaml"
    if not t464_docket_path.is_file():
        errors.append("missing T464 owner_decision_docket.yaml")
        t464_docket: dict[str, Any] = {}
    else:
        t464_docket = _read_yaml(t464_docket_path)

    _validate_control(control, task, errors)
    _validate_owner_docket(docket, t464_docket, errors)
    _validate_required_text(paths, errors)
    _validate_mark16_source_row(root, errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate_t465_package(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T465 reconciliation gate validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
