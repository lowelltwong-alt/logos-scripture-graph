from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_multi_agent_review_cadence_files_exist() -> None:
    assert (ROOT / ".ai/control/multi_agent_review_cadence.yaml").is_file()
    assert (ROOT / ".ai/control/agent_review_ledger.jsonl").is_file()
    assert (ROOT / ".ai/prompts/codex_daily_prep_review_prompt.md").is_file()
    assert (ROOT / ".ai/prompts/claude_weekly_architecture_chunking_audit_prompt.md").is_file()
    assert (ROOT / "scripts/validate_multi_agent_review_cadence.py").is_file()


def test_multi_agent_review_cadence_validator_passes() -> None:
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_multi_agent_review_cadence.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
