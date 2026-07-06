#!/usr/bin/env python3
"""Validate the compact front door and task-ledger split."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TASK_LEDGER = ROOT / "docs" / "roadmap" / "TASK_LEDGER.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

MAX_FRONT_DOOR_LINES = 250

FRONT_DOOR_REQUIRED = {
    "docs/roadmap/TASK_LEDGER.md",
    "AI_TABLE_OF_CONTENTS.md",
    "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md",
    ".ai/control/chunking_agent_preflight.yaml",
    ".ai/control/test_runtime_preflight.yaml",
    ".ai/audits/README.md",
    ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md",
    "no-context A/B/red-team",
    "governance/LOGOS_REPO_REGISTRY.yaml",
    "Boundary text source intake",
    "must not override, contaminate, or become equal authority",
    "Source metadata is evidence, not authority",
    "Revelation implementation must wait until reviewed gold exists",
    "isolate corpora, routes, skills, objectives, eval sets, default retrieval policy",
    "python scripts/validate_all.py",
    "python -m pytest -q",
    "validate_task_ledger.py",
}

LEDGER_REQUIRED = {
    "object_type: task_ledger",
    "## Current Newest-First Pointers",
    "## Moved Front-Door Task Narrative",
    "## Moved Raw Source Inspection Detail",
    "T461: Scripture front-door decomposition",
    "T460: Rust and DAD stack integration",
    "T459: Rust word-token signal scanner",
    "T401 Eph.1.3-Eph.1.14 output pilot",
    "T398 phase-one whole-corpus research synthesis",
    "T371-A now promotes only `1Cor.8.1-1Cor.10.33`",
    "T374 additive parent overlay implementation manifest",
    "T385 owner decision packet",
    "No chunk output",
    "No reviewed gold",
    "No child spans",
    "No route/evaluator behavior changes",
    "No graph, retrieval, vector, embedding, or index truth",
    "No source rows, canon changes, preferred readings, or theology authority",
}

TOC_REQUIRED = {
    "docs/roadmap/TASK_LEDGER.md",
    "task-ledger",
    "front-door",
}


class TaskLedgerError(ValueError):
    """Raised when the front-door/task-ledger split is invalid."""


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TaskLedgerError(f"{_rel(path)} unreadable: {exc}") from exc


def _require_phrases(path: Path, required: set[str]) -> None:
    text = _read(path)
    missing = sorted(phrase for phrase in required if phrase not in text)
    if missing:
        raise TaskLedgerError(f"{_rel(path)} missing required phrase(s): {missing}")


def _front_door_read_order_numbers(text: str) -> list[int]:
    in_section = False
    numbers: list[int] = []
    for line in text.splitlines():
        if line == "## Mandatory Read Order":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        match = re.match(r"^(\d+)\. ", line)
        if match:
            numbers.append(int(match.group(1)))
    return numbers


def validate_task_ledger() -> None:
    front = _read(FRONT_DOOR)
    ledger = _read(TASK_LEDGER)

    front_lines = front.splitlines()
    if len(front_lines) > MAX_FRONT_DOOR_LINES:
        raise TaskLedgerError(
            f"{_rel(FRONT_DOOR)} has {len(front_lines)} lines; maximum is {MAX_FRONT_DOOR_LINES}"
        )

    numbers = _front_door_read_order_numbers(front)
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        raise TaskLedgerError(f"{_rel(FRONT_DOOR)} read-order numbers must be sequential; got {numbers}")

    if "T351 through T381 prepared the current route" in front:
        raise TaskLedgerError(f"{_rel(FRONT_DOOR)} still contains moved task-history narrative")

    _require_phrases(FRONT_DOOR, FRONT_DOOR_REQUIRED)
    _require_phrases(TASK_LEDGER, LEDGER_REQUIRED)
    _require_phrases(MAIN_TOC, TOC_REQUIRED)
    _require_phrases(ROADMAP_TOC, TOC_REQUIRED)

    order = [ledger.index(f"T{task}:") for task in (461, 460, 459)]
    if order != sorted(order):
        raise TaskLedgerError(f"{_rel(TASK_LEDGER)} current pointers must be newest first")


def main() -> int:
    try:
        validate_task_ledger()
    except TaskLedgerError as exc:
        print(f"Task ledger validation failed: {exc}", file=sys.stderr)
        return 1
    print("Task ledger validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
