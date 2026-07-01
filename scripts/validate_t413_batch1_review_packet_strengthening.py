#!/usr/bin/env python3
"""Validate T413 batch1 review-packet strengthening."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "t413_batch1_review_packet_strengthening.yaml"
TASK = ROOT / ".ai" / "tasks" / "T415.task.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"

PACKETS = (
    ("T402-LC-064", "3John.1.1-3John.1.4", ROOT / "eval/chunking_gold/review_packets/t411_batch1_3john_opening_review.md"),
    ("T402-LC-047", "2Cor.1.1-2Cor.1.2", ROOT / "eval/chunking_gold/review_packets/t411_batch1_2cor_opening_review.md"),
    ("T402-LC-054", "1Tim.1.1-1Tim.1.2", ROOT / "eval/chunking_gold/review_packets/t411_batch1_1tim_opening_review.md"),
    ("T402-LC-059", "Jas.1.1-Jas.1.1", ROOT / "eval/chunking_gold/review_packets/t411_batch1_jas_opening_review.md"),
    ("T402-LC-063", "2John.1.1-2John.1.3", ROOT / "eval/chunking_gold/review_packets/t411_batch1_2john_opening_review.md"),
)

REQUIRED_STATUS_PHRASES = (
    "Status: `pending_human_review`",
    "Decision: pending",
    "Implementation allowed: false",
    "Output change authorized: false",
    "Reviewed gold promoted: false",
    "T413 batch1 strengthened packet: true",
    "Review-only strengthening: true",
    "Contextual Reading Fields",
    "non_authorizations:",
    "No option above is approved. No reviewed gold is promoted.",
)

FORBIDDEN_PHRASES = (
    "Reviewed gold promoted: true",
    "Implementation allowed: true",
    "Output change authorized: true",
)


class T413Batch1Error(ValueError):
    """Raised when T413 batch1 strengthening state is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise T413Batch1Error(f"{_rel(path)}: expected YAML mapping")
    return data


def _validate_control() -> None:
    data = _read_yaml(CONTROL)
    if data.get("task_id") != "T413-B":
        raise T413Batch1Error("control task_id must be T413-B (phase A of T415)")
    if data.get("decision_register_entry") != "CD-080":
        raise T413Batch1Error("control decision_register_entry must be CD-080")
    docket = data.get("docket")
    if not isinstance(docket, list) or len(docket) != 5:
        raise T413Batch1Error("control docket must list five candidates")
    auth = data.get("authorization", {})
    if auth.get("authorizes_review_packet_strengthening") is not True:
        raise T413Batch1Error("control must authorize review-packet strengthening only")
    for key in ("authorizes_reviewed_gold_promotion", "authorizes_chunk_output_change", "authorizes_child_spans"):
        if auth.get(key) is not False:
            raise T413Batch1Error(f"control authorization.{key} must be false")


def _validate_packets() -> None:
    for candidate_id, span, path in PACKETS:
        if not path.exists():
            raise T413Batch1Error(f"missing review packet {_rel(path)}")
        text = _read_text(path)
        if f"`{candidate_id}`" not in text:
            raise T413Batch1Error(f"{_rel(path)} must reference {candidate_id}")
        if f"`{span}`" not in text:
            raise T413Batch1Error(f"{_rel(path)} must reference {span}")
        for phrase in REQUIRED_STATUS_PHRASES:
            if phrase not in text:
                raise T413Batch1Error(f"{_rel(path)} missing {phrase!r}")
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                raise T413Batch1Error(f"{_rel(path)} contains forbidden {phrase!r}")


def _validate_surfaces() -> None:
    surface_checks = (
        (REGISTER, ("decision_id: CD-080", "T413 batch1", "task_ids: [T413, T415]")),
        (LESSON_INDEX, ("lesson_id: LSN-035", "CD-080")),
        (PREFLIGHT, ("CD-080", "LSN-035", "t413_batch1_review_packet_strengthening.yaml")),
        (READINESS, ("task_id: T413", "batch1_review_packet_strengthening", "CD-080")),
        (ROADMAP_STATE, ("id: T413", "CD-080")),
        (PROJECT_STATUS, ("T413 batch1", "CD-080", "LSN-035")),
        (CURRENT_FOCUS, ("T415", "t413_batch1_review_packet_strengthening.yaml")),
        (TASK, ("id: T415", "T413 batch1", "authorizes_review_packet_strengthening: true", "phases:")),
    )
    for path, phrases in surface_checks:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T413Batch1Error(f"{_rel(path)} missing {phrase!r}")


def validate_t413_batch1() -> None:
    _validate_control()
    _validate_packets()
    _validate_surfaces()


def main() -> int:
    try:
        validate_t413_batch1()
    except T413Batch1Error as exc:
        print(f"T413 batch1 review-packet strengthening validation failed: {exc}", file=sys.stderr)
        return 1
    print("T413 batch1 review-packet strengthening validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
