"""Tests for T423 parallel-path isolation validator."""
from __future__ import annotations

import pytest

from scripts.validate_t423_parallel_isolation import _normalize, validate_parallel_isolation


def test_normalize_preserves_dot_ai_root() -> None:
    assert _normalize(".ai/context/foo.md") == ".ai/context/foo.md"
    assert _normalize("./.ai/context/foo.md") == ".ai/context/foo.md"
    assert _normalize(r".ai\context\foo.md") == ".ai/context/foo.md"


def test_main_branch_fails_closed_for_marathon_work() -> None:
    errors = validate_parallel_isolation(branch="main", changed_files=[])
    assert any("should start with scratch/t423-" in error for error in errors)


def test_codex_t423_branch_allows_integration_review() -> None:
    assert validate_parallel_isolation(branch="codex/t423-six-model-marathon-complete", changed_files=[]) == []


def test_codex_t423_branch_does_not_allow_single_model_marathon_mode(tmp_path) -> None:
    model_folder = tmp_path / "M1_cursor"
    model_folder.mkdir()
    errors = validate_parallel_isolation(
        branch="codex/t423-six-model-marathon-complete",
        changed_files=[],
        model_folder=model_folder,
    )
    assert any("should start with scratch/t423-" in error for error in errors)


def test_scratch_t423_branch_allows_empty_change_set() -> None:
    assert validate_parallel_isolation(branch="scratch/t423-M1-cursor", changed_files=[]) == []


@pytest.mark.parametrize(
    "path",
    [
        ".ai/context/agent_work/T417/model_layers/batch2/root_note.md",
        ".ai/context/agent_work/T417/model_layers/batch2/L4_gemini/foo.md",
        "./.ai/context/agent_work/T417/model_layers/batch2/L5_hostile/foo.md",
    ],
)
def test_t417_batch2_root_and_future_layers_are_forbidden(path: str) -> None:
    errors = validate_parallel_isolation(
        branch="scratch/t423-M1-cursor",
        changed_files=[path],
    )
    assert any("T417 batch2 path touched" in error for error in errors)


def test_policy_listed_forbidden_paths_are_forbidden() -> None:
    errors = validate_parallel_isolation(
        branch="scratch/t423-M1-cursor",
        changed_files=[".ai/scratch/multi_model_bible_chunking/comparison/delta_summary.md"],
    )
    assert any("forbidden path modified" in error for error in errors)
