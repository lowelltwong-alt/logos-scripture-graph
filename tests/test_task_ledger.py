from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.validate_task_ledger import (
    FRONT_DOOR,
    MAX_FRONT_DOOR_LINES,
    TASK_LEDGER,
    validate_task_ledger,
)


ROOT = Path(__file__).resolve().parents[1]


def test_task_ledger_validator_passes() -> None:
    validate_task_ledger()


def test_task_ledger_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_task_ledger.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Task ledger validation passed." in result.stdout


def test_front_door_is_compact_and_points_to_task_ledger() -> None:
    front = FRONT_DOOR.read_text(encoding="utf-8")
    assert len(front.splitlines()) <= MAX_FRONT_DOOR_LINES
    assert "docs/roadmap/TASK_LEDGER.md" in front
    assert "T351 through T381 prepared the current route" not in front


def test_task_ledger_preserves_moved_task_history() -> None:
    ledger = TASK_LEDGER.read_text(encoding="utf-8")
    for phrase in [
        "T371-A now promotes only `1Cor.8.1-1Cor.10.33`",
        "T401 Eph.1.3-Eph.1.14 output pilot",
        "T398 phase-one whole-corpus research synthesis",
        "No graph, retrieval, vector, embedding, or index truth",
    ]:
        assert phrase in ledger
