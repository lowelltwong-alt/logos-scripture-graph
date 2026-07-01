from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_autonomous_run_queue_files_exist() -> None:
    assert (ROOT / ".ai/control/autonomous_run_queue.yaml").is_file()
    assert (ROOT / ".ai/tasks/T417.task.yaml").is_file()
    assert (ROOT / "scripts/validate_autonomous_run_queue.py").is_file()


def test_autonomous_run_queue_validator_passes() -> None:
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_autonomous_run_queue.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
