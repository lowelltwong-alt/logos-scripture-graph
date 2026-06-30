from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_parallel_execution_safety as validator


def _patch_common_git(monkeypatch: pytest.MonkeyPatch, *, status: str = "", branch: str = "codex/t410-live-execution-safety-validator") -> None:
    def fake_run_git(args: list[str]) -> str:
        if args == ["status", "--porcelain=v1"]:
            return status
        if args == ["branch", "--show-current"]:
            return branch
        if args == ["worktree", "list", "--porcelain"]:
            return f"worktree /repo\nHEAD abc\nbranch refs/heads/{branch}\n"
        raise AssertionError(f"unexpected git args: {args}")

    monkeypatch.setattr(validator, "run_git", fake_run_git)
    monkeypatch.setattr(validator, "active_merge_states", lambda: [])


def test_parallel_safety_passes_clean_task_branch(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_common_git(monkeypatch)

    result = validator.validate_parallel_execution_safety(task_id="T410", require_task_branch=True)

    assert result["task_id"] == "T410"
    assert result["dirty_paths"] == []


def test_parallel_safety_rejects_dirty_worktree_without_allowance(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_common_git(monkeypatch, status=" M scripts/validate_parallel_execution_safety.py")

    with pytest.raises(validator.ParallelSafetyError, match="worktree is not clean"):
        validator.validate_parallel_execution_safety(task_id="T410")


def test_parallel_safety_allows_only_current_task_dirty_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_common_git(
        monkeypatch,
        status=" M scripts/validate_parallel_execution_safety.py\n?? tests/test_parallel_execution_safety.py",
    )

    result = validator.validate_parallel_execution_safety(task_id="T410", allow_current_task_dirty=True)

    assert "scripts/validate_parallel_execution_safety.py" in result["dirty_paths"]


def test_parallel_safety_rejects_dirty_paths_outside_task_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_common_git(monkeypatch, status=" M data/raw/bible/eng-web/source_manifest.yaml")

    with pytest.raises(validator.ParallelSafetyError, match="outside current task allowed paths"):
        validator.validate_parallel_execution_safety(task_id="T410", allow_current_task_dirty=True)


def test_parallel_safety_rejects_cross_task_untracked_artifacts(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_common_git(monkeypatch, status="?? .ai/context/agent_work/T999/audit_log.jsonl")

    with pytest.raises(validator.ParallelSafetyError, match="another task id"):
        validator.validate_parallel_execution_safety(task_id="T410", allow_current_task_dirty=True)


def test_parallel_safety_rejects_merge_state(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_common_git(monkeypatch)
    monkeypatch.setattr(validator, "active_merge_states", lambda: ["MERGE_HEAD"])

    with pytest.raises(validator.ParallelSafetyError, match="merge/rebase"):
        validator.validate_parallel_execution_safety(task_id="T410")


def test_parallel_safety_rejects_wrong_branch(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_common_git(monkeypatch, branch="codex/not-this-task")

    with pytest.raises(validator.ParallelSafetyError, match="does not match task branch"):
        validator.validate_parallel_execution_safety(task_id="T410", require_task_branch=True)


def test_parse_porcelain_status_uses_renamed_destination() -> None:
    entries = validator.parse_porcelain_status("R  old/path.txt -> new/path.txt\n")

    assert entries == [validator.StatusEntry(code="R ", path="new/path.txt")]


def test_parse_porcelain_status_preserves_dot_prefixed_paths() -> None:
    entries = validator.parse_porcelain_status(" M .ai/control/PROJECT_STATUS.md\n")

    assert entries == [validator.StatusEntry(code=" M", path=".ai/control/PROJECT_STATUS.md")]
