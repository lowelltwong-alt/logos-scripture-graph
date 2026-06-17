from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_task_scope as validator


ROOT = Path(__file__).resolve().parents[1]
T344_TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"
T351_TASK = ROOT / ".ai" / "tasks" / "T351.task.yaml"


def test_t344_scope_accepts_harn_001_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T344_TASK,
        changed_files=[
            "scripts/validate_task_scope.py",
            "tests/test_task_scope_validator.py",
            "scripts/validate_all.py",
            ".github/workflows/validate.yml",
            ".ai/control/harness_upgrade_roadmap.yaml",
            ".ai/tasks/T344.task.yaml",
            ".ai/handoffs/T344/handoff.md",
            ".ai/control/PROJECT_STATUS.md",
            ".ai/control/current_focus.yaml",
            ".ai/control/roadmap_events.jsonl",
            ".ai/control/handoff_ledger.jsonl",
            "AI_FRONT_DOOR.md",
            "AI_TABLE_OF_CONTENTS.md",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T344.task.yaml"
    assert ".github/workflows/validate.yml" in result["protected_changed"]


def test_scope_rejects_forbidden_raw_or_chunking_paths() -> None:
    with pytest.raises(validator.TaskScopeError, match="forbids changed path"):
        validator.validate_task_scope(
            task_file=T344_TASK,
            changed_files=["data/raw/bible/eng-web/file.usfm"],
        )

    with pytest.raises(validator.TaskScopeError, match="forbids changed path"):
        validator.validate_task_scope(
            task_file=T344_TASK,
            changed_files=["pipelines/chunking/chunker.py"],
        )


def test_t351_scope_accepts_bible_wide_triage_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T351_TASK,
        changed_files=[
            ".ai/control/bible_chunking_research_triage_map.yaml",
            "docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md",
            "scripts/validate_bible_chunking_research_triage.py",
            "tests/test_t351_bible_wide_research_triage.py",
            ".ai/tasks/T344R.task.yaml",
            ".ai/handoffs/T344R/handoff.md",
            ".ai/tasks/T351.task.yaml",
            ".ai/handoffs/T351/handoff.md",
            "ROADMAP_STATE.yaml",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T351.task.yaml"


def test_scope_rejects_paths_outside_allowed_scope() -> None:
    with pytest.raises(validator.TaskScopeError, match="does not allow"):
        validator.validate_task_scope(
            task_file=T344_TASK,
            changed_files=["README.md"],
        )


def test_scope_rejects_master_context_even_if_task_allows_it(tmp_path: Path) -> None:
    task_file = tmp_path / "T999.task.yaml"
    task_file.write_text(
        "\n".join(
            [
                "id: T999",
                "scope:",
                "  allowed_paths:",
                "    - .ai/control/MASTER_CONTEXT.md",
                "  forbidden_paths: []",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(validator.TaskScopeError, match="hard-forbidden"):
        validator.validate_task_scope(
            task_file=task_file,
            changed_files=[".ai/control/MASTER_CONTEXT.md"],
        )


def test_scope_accepts_directory_prefixes() -> None:
    validator.validate_task_scope(
        task_file=T344_TASK,
        changed_files=[".ai/audits/reports/example.md"],
    )


def test_default_task_id_reads_current_task_without_strict_yaml(tmp_path: Path) -> None:
    focus = tmp_path / "current_focus.yaml"
    focus.write_text(
        "current_task: T344\nnext_sprint: Owner chooses exactly one T344 option: REV-T344-A\n",
        encoding="utf-8",
    )

    assert validator.default_task_id(focus) == "T344"
