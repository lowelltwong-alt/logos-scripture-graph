from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "agent" / "post_merge_verify.py"
WORKFLOW = ROOT / "docs" / "workflows" / "POST_MERGE_VERIFICATION_WORKFLOW.md"
PROMPT_TEMPLATE = ROOT / ".ai" / "templates" / "POST_MERGE_AND_NEXT_TASK_PROMPT.md"
CHECKLIST = ROOT / ".ai" / "templates" / "NEXT_TASK_HANDOFF_CHECKLIST.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def squish(text: str) -> str:
    return " ".join(text.split())


def test_post_merge_verify_script_exposes_required_cli_flags() -> None:
    assert SCRIPT.exists()

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    help_text = result.stdout

    for flag in ["--pr", "--expected-commit", "--next-task", "--skip-pytest", "--json"]:
        assert flag in help_text


def test_post_merge_workflow_templates_and_toc_are_discoverable() -> None:
    assert WORKFLOW.exists()
    assert PROMPT_TEMPLATE.exists()
    assert CHECKLIST.exists()

    toc = read(TOC)
    assert "docs/workflows/POST_MERGE_VERIFICATION_WORKFLOW.md" in toc
    assert ".ai/templates/POST_MERGE_AND_NEXT_TASK_PROMPT.md" in toc
    assert ".ai/templates/NEXT_TASK_HANDOFF_CHECKLIST.md" in toc


def test_workflow_locks_non_authorizing_post_merge_rules() -> None:
    workflow = squish(read(WORKFLOW))
    prompt = read(PROMPT_TEMPLATE)
    checklist = read(CHECKLIST)

    assert "Post-merge verification is the mandatory checkpoint" in workflow
    assert "It does not start the next task" in workflow
    assert "does not by itself authorize implementation" in workflow
    assert "High-risk tasks still require RISK-GATE-001" in workflow
    assert "Output-changing tasks still require reviewed gold and explicit authorization" in workflow
    assert "If verification fails:" in prompt
    assert "do not create a branch" in prompt
    assert "No implementation authorization inferred from planning docs" in checklist
