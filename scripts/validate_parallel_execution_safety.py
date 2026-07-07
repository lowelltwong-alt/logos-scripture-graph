#!/usr/bin/env python3
"""Validate live branch/worktree safety for parallel AI task execution."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts.validate_task_scope import _matches_any, _normalize_path, default_task_id, load_task_scope
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from validate_task_scope import _matches_any, _normalize_path, default_task_id, load_task_scope

ROOT = Path(__file__).resolve().parent.parent
TASK_ROOT = ROOT / ".ai" / "tasks"

MERGE_STATE_KEYS = (
    "MERGE_HEAD",
    "REBASE_HEAD",
    "CHERRY_PICK_HEAD",
    "BISECT_LOG",
    "rebase-merge",
    "rebase-apply",
)

TASK_ARTIFACT_RE = re.compile(
    r"^(?:\.ai/context/agent_work/(?P<agent_work>[^/]+)/|"
    r"\.ai/handoffs/(?P<handoff>[^/]+)/|"
    r"\.ai/tasks/(?P<task_file>[^/]+)\.task\.yaml$)"
)


class ParallelSafetyError(ValueError):
    """Raised when live branch/worktree state is unsafe for parallel work."""


@dataclass(frozen=True)
class StatusEntry:
    code: str
    path: str


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).rstrip("\n")


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ParallelSafetyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ParallelSafetyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def task_file_for(task_id: str) -> Path:
    return TASK_ROOT / f"{task_id}.task.yaml"


def parse_porcelain_status(output: str) -> list[StatusEntry]:
    entries: list[StatusEntry] = []
    for raw in output.splitlines():
        line = raw.rstrip()
        if not line:
            continue
        code = line[:2]
        path_text = line[3:] if len(line) > 3 else ""
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        entries.append(StatusEntry(code=code, path=_normalize_path(path_text.strip('"'))))
    return entries


def git_status_entries() -> list[StatusEntry]:
    return parse_porcelain_status(run_git(["status", "--porcelain=v1"]))


def git_path_exists(path_key: str) -> bool:
    try:
        path = run_git(["rev-parse", "--git-path", path_key])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return (ROOT / path).exists() if not Path(path).is_absolute() else Path(path).exists()


def active_merge_states() -> list[str]:
    return [key for key in MERGE_STATE_KEYS if git_path_exists(key)]


def current_branch() -> str:
    return run_git(["branch", "--show-current"])


def worktree_branch_counts() -> dict[str, int]:
    try:
        output = run_git(["worktree", "list", "--porcelain"])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    counts: dict[str, int] = {}
    for line in output.splitlines():
        if not line.startswith("branch refs/heads/"):
            continue
        branch = line.removeprefix("branch refs/heads/").strip()
        if branch:
            counts[branch] = counts.get(branch, 0) + 1
    return counts


def _task_id_from_artifact(path: str) -> str | None:
    match = TASK_ARTIFACT_RE.match(_normalize_path(path))
    if not match:
        return None
    return next((value for value in match.groupdict().values() if value), None)


def _branch_matches_task(*, branch: str, task_id: str, expected_branch: str | None) -> bool:
    if not branch:
        return False
    if expected_branch:
        return branch == expected_branch
    return task_id.lower().replace("_", "-") in branch.lower().replace("_", "-")


def _artifact_task_allowed_for_current_task(*, task_id: str, artifact_task: str) -> bool:
    """Allow only declared integration tasks to carry related task artifacts."""
    if artifact_task == task_id:
        return True
    related_task_sets = [
        {"T417", "T420"},
        {"T423", "T424", "T464"},
    ]
    return any(task_id in task_set and artifact_task in task_set for task_set in related_task_sets)


def validate_parallel_execution_safety(
    *,
    task_id: str,
    allow_current_task_dirty: bool = False,
    require_task_branch: bool = False,
) -> dict[str, Any]:
    task_file = task_file_for(task_id)
    if not task_file.exists():
        raise ParallelSafetyError(f"{_rel(task_file)}: task file is required")

    merge_states = active_merge_states()
    if merge_states:
        raise ParallelSafetyError("merge/rebase/cherry-pick/bisect state present: " + ", ".join(merge_states))

    branch = current_branch()
    task_data = _read_yaml(task_file)
    expected_branch = task_data.get("branch") if isinstance(task_data.get("branch"), str) else None
    if require_task_branch and not _branch_matches_task(branch=branch, task_id=task_id, expected_branch=expected_branch):
        expected = expected_branch or f"a branch name containing {task_id.lower()}"
        raise ParallelSafetyError(f"current branch {branch!r} does not match task branch requirement {expected!r}")

    branch_counts = worktree_branch_counts()
    if branch and branch_counts.get(branch, 0) > 1:
        raise ParallelSafetyError(f"branch {branch!r} is checked out in multiple worktrees")

    entries = git_status_entries()
    other_task_artifacts = [
        entry.path
        for entry in entries
        if entry.code == "??"
        for artifact_task in [_task_id_from_artifact(entry.path)]
        if artifact_task
        and not _artifact_task_allowed_for_current_task(task_id=task_id, artifact_task=artifact_task)
    ]
    if other_task_artifacts:
        raise ParallelSafetyError("untracked artifacts from another task id present: " + ", ".join(other_task_artifacts))

    dirty_paths = [entry.path for entry in entries]
    if dirty_paths and not allow_current_task_dirty:
        raise ParallelSafetyError("worktree is not clean: " + ", ".join(dirty_paths))

    outside_allowed: list[str] = []
    if dirty_paths and allow_current_task_dirty:
        scope = load_task_scope(task_file)
        allowed = scope["allowed_paths"]
        outside_allowed = [path for path in dirty_paths if not _matches_any(path, allowed)]
        if outside_allowed:
            raise ParallelSafetyError("dirty path(s) outside current task allowed paths: " + ", ".join(outside_allowed))

    return {
        "task_id": task_id,
        "branch": branch,
        "dirty_paths": dirty_paths,
        "allow_current_task_dirty": allow_current_task_dirty,
        "require_task_branch": require_task_branch,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", default=None)
    parser.add_argument(
        "--allow-current-task-dirty",
        action="store_true",
        help="Allow dirty files only when every dirty path is inside the task's declared allowed paths.",
    )
    parser.add_argument(
        "--require-task-branch",
        action="store_true",
        help="Require the current branch to match the task file branch or contain the task id.",
    )
    args = parser.parse_args(argv)

    try:
        task_id = args.task_id or default_task_id()
        validate_parallel_execution_safety(
            task_id=task_id,
            allow_current_task_dirty=args.allow_current_task_dirty,
            require_task_branch=args.require_task_branch,
        )
    except (ParallelSafetyError, subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Parallel execution safety validation failed: {exc}", file=sys.stderr)
        return 1

    print("Parallel execution safety validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
