#!/usr/bin/env python3
"""Validate that changed files stay inside the active task's declared scope."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
TASK_ROOT = ROOT / ".ai" / "tasks"

HARD_FORBIDDEN_PATHS = {
    ".ai/control/MASTER_CONTEXT.md",
    ".ai/control/MASTER_CONTEXT.lock.yaml",
}

PROTECTED_PREFIXES = (
    "data/raw/",
    "data/canonical/",
    "data/processed/",
    "data/derived/",
    "pipelines/chunking/",
    "registry/chunking/",
    "eval/chunking_gold/per_form/",
    "eval/chunking_runs/",
    "eval/LEADERBOARD.md",
    ".github/workflows/",
    ".ai/control/chunking_theological_decision_register.yaml",
    ".ai/control/governance_memory_durability_policy.yaml",
    ".ai/control/owner_decision_projection_policy.yaml",
)

RUNTIME_PREFLIGHT_SURFACES = (
    "scripts/validate_",
    "scripts/build_",
    "scripts/scan_",
    "scripts/download_",
    "scripts/generate_",
    "scripts/qa_",
    "tools/",
    "pipelines/",
    ".github/workflows/",
)

RUNTIME_PREFLIGHT_DECISIONS = {
    "rust_fast_path_with_python_wrapper",
    "python_orchestration_with_rust_leaf_worker",
    "python_only_below_threshold",
    "python_only_due_to_semantic_policy_complexity",
    "defer_rust_until_measurement",
}

RUNTIME_PREFLIGHT_REQUIRED_FIELDS = {
    "task_id",
    "touched_paths",
    "expected_input_size_or_record_count",
    "expected_runtime_or_memory_pressure",
    "rust_trigger_match",
    "chosen_language",
    "expected_rust_time_saved_or_reason_not_applicable",
    "interop_boundary",
    "python_fallback_or_wrapper_plan",
    "validation_plan",
    "maintenance_tradeoffs",
}


class TaskScopeError(ValueError):
    """Raised when a changed path violates task scope."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/").strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    candidate = Path(normalized)
    if candidate.is_absolute():
        try:
            normalized = candidate.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            normalized = candidate.as_posix()
    return normalized


def _dedupe(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for path in paths:
        normalized = _normalize_path(path)
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def _run_git(args: list[str]) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def _git_names(args: list[str]) -> list[str]:
    output = _run_git(args)
    return [line.strip() for line in output.splitlines() if line.strip()]


def git_changed_files(base_ref: str) -> list[str]:
    """Return committed and working-tree changed files, best-effort."""

    paths: list[str] = []
    base_candidates: list[str] = []
    github_base = os.environ.get("GITHUB_BASE_REF")
    if github_base and base_ref == "origin/main":
        base_candidates.append(f"origin/{github_base}")
    if base_ref:
        base_candidates.append(base_ref)
    if base_ref == "origin/main":
        try:
            upstream = _run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])
            current_branch = _run_git(["branch", "--show-current"])
            if upstream and not upstream.endswith(f"/{current_branch}"):
                base_candidates.insert(0, upstream)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    for candidate in base_candidates:
        try:
            merge_base = _run_git(["merge-base", "HEAD", candidate])
            paths.extend(_git_names(["diff", "--name-only", f"{merge_base}...HEAD"]))
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    else:
        try:
            paths.extend(_git_names(["diff", "--name-only", "HEAD^1...HEAD"]))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    for args in (
        ["diff", "--cached", "--name-only"],
        ["diff", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        try:
            paths.extend(_git_names(args))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    return _dedupe(paths)


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise TaskScopeError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise TaskScopeError(f"{_rel(path)}: expected a YAML mapping")
    return data


def default_task_id(path: Path = CURRENT_FOCUS) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TaskScopeError(f"{_rel(path)}: unreadable: {exc}") from exc
    match = re.search(r"^current_task:\s*([^\n#]+)", text, flags=re.MULTILINE)
    task_id = match.group(1).strip().strip('"').strip("'") if match else ""
    if not task_id:
        raise TaskScopeError(f"{_rel(path)}: current_task must be a non-empty string")
    return task_id


def _task_file_for(task_id: str) -> Path:
    return TASK_ROOT / f"{task_id}.task.yaml"


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise TaskScopeError(f"{label} must be a list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise TaskScopeError(f"{label} must contain only non-empty strings")
    return [_normalize_path(item) for item in value]


def load_task_scope(task_file: Path) -> dict[str, Any]:
    data = _read_yaml(task_file)
    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise TaskScopeError(f"{_rel(task_file)}: scope must be a mapping")
    allowed = _string_list(scope.get("allowed_paths"), f"{_rel(task_file)}: scope.allowed_paths")
    forbidden = _string_list(scope.get("forbidden_paths"), f"{_rel(task_file)}: scope.forbidden_paths")
    if not allowed:
        raise TaskScopeError(f"{_rel(task_file)}: scope.allowed_paths must not be empty")
    return {"task": data, "allowed_paths": allowed, "forbidden_paths": forbidden}


def _matches_rule(path: str, rule: str) -> bool:
    path = _normalize_path(path)
    rule = _normalize_path(rule)
    if "*" in rule:
        return fnmatch(path, rule)
    if rule.endswith("/"):
        return path.startswith(rule)
    return path == rule


def _matches_any(path: str, rules: list[str] | tuple[str, ...] | set[str]) -> bool:
    return any(_matches_rule(path, rule) for rule in rules)


def _task_number(task: dict[str, Any]) -> int | None:
    task_id = str(task.get("id", ""))
    match = re.match(r"^T(\d+)", task_id)
    return int(match.group(1)) if match else None


def _is_runtime_preflight_surface(path: str) -> bool:
    normalized = _normalize_path(path)
    return any(normalized.startswith(prefix) for prefix in RUNTIME_PREFLIGHT_SURFACES)


def _requires_runtime_language_preflight(task: dict[str, Any], task_file: Path, changed_files: list[str]) -> bool:
    task_no = _task_number(task)
    if task_no is None or task_no < 425:
        return False
    task_file_rel = _rel(task_file)
    task_id = str(task.get("id", ""))
    task_contract_changed = (
        task_file_rel in changed_files
        or f".ai/tasks/{task_id}.task.yaml" in changed_files
        or any(Path(path).name == f"{task_id}.task.yaml" for path in changed_files)
    )
    if not task_contract_changed:
        return False
    return any(_is_runtime_preflight_surface(path) for path in changed_files)


def _validate_runtime_language_preflight(task: dict[str, Any], changed_files: list[str], task_file: Path) -> None:
    block = task.get("runtime_language_preflight")
    if not isinstance(block, dict):
        raise TaskScopeError(
            f"{_rel(task_file)}: runtime_language_preflight is required when post-T424 tasks touch "
            "validator, scanner, pipeline, workflow, generated-data, Rust, or CI hot-path surfaces"
        )
    missing = sorted(RUNTIME_PREFLIGHT_REQUIRED_FIELDS - set(block))
    if missing:
        raise TaskScopeError(f"{_rel(task_file)}: runtime_language_preflight missing field(s) {missing}")
    if block.get("task_id") != task.get("id"):
        raise TaskScopeError(f"{_rel(task_file)}: runtime_language_preflight.task_id must match task id")
    touched = _string_list(block.get("touched_paths"), f"{_rel(task_file)}: runtime_language_preflight.touched_paths")
    runtime_paths = [path for path in changed_files if _is_runtime_preflight_surface(path)]
    missing_runtime_paths = [path for path in runtime_paths if not _matches_any(path, touched)]
    if missing_runtime_paths:
        raise TaskScopeError(
            f"{_rel(task_file)}: runtime_language_preflight.touched_paths missing runtime-sensitive path(s): "
            + ", ".join(missing_runtime_paths)
        )
    triggers = _string_list(
        block.get("rust_trigger_match"),
        f"{_rel(task_file)}: runtime_language_preflight.rust_trigger_match",
    )
    if not triggers:
        raise TaskScopeError(f"{_rel(task_file)}: runtime_language_preflight.rust_trigger_match must not be empty")
    chosen = block.get("chosen_language")
    if chosen not in RUNTIME_PREFLIGHT_DECISIONS:
        raise TaskScopeError(
            f"{_rel(task_file)}: runtime_language_preflight.chosen_language must be one of "
            + ", ".join(sorted(RUNTIME_PREFLIGHT_DECISIONS))
        )
    for key in (
        "expected_input_size_or_record_count",
        "expected_runtime_or_memory_pressure",
        "expected_rust_time_saved_or_reason_not_applicable",
        "interop_boundary",
        "python_fallback_or_wrapper_plan",
        "validation_plan",
        "maintenance_tradeoffs",
    ):
        value = block.get(key)
        if isinstance(value, str) and value.strip():
            continue
        if isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value) and value:
            continue
        raise TaskScopeError(f"{_rel(task_file)}: runtime_language_preflight.{key} must be non-empty text or string list")


def validate_task_scope(
    *,
    task_file: Path,
    changed_files: list[str],
) -> dict[str, Any]:
    scope = load_task_scope(task_file)
    task = scope["task"]
    normalized = _dedupe(changed_files)
    allowed = scope["allowed_paths"]
    forbidden = scope["forbidden_paths"]

    hard_forbidden = [path for path in normalized if _matches_any(path, HARD_FORBIDDEN_PATHS)]
    if hard_forbidden:
        raise TaskScopeError(
            "hard-forbidden human-gated paths changed: " + ", ".join(hard_forbidden)
        )

    forbidden_changed = [path for path in normalized if _matches_any(path, forbidden)]
    if forbidden_changed:
        raise TaskScopeError(
            f"{_rel(task_file)} forbids changed path(s): " + ", ".join(forbidden_changed)
        )

    outside_allowed = [path for path in normalized if not _matches_any(path, allowed)]
    if outside_allowed:
        raise TaskScopeError(
            f"{_rel(task_file)} does not allow changed path(s): " + ", ".join(outside_allowed)
        )

    protected_changed = [path for path in normalized if _matches_any(path, PROTECTED_PREFIXES)]
    protected_without_explicit_scope = [
        path for path in protected_changed
        if not _matches_any(path, allowed)
    ]
    if protected_without_explicit_scope:
        raise TaskScopeError(
            "protected changed path(s) lack explicit task scope: "
            + ", ".join(protected_without_explicit_scope)
        )

    if _requires_runtime_language_preflight(task, task_file, normalized):
        _validate_runtime_language_preflight(task, normalized, task_file)

    return {
        "task_file": _rel(task_file),
        "changed_files": normalized,
        "protected_changed": protected_changed,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", default=None)
    parser.add_argument("--task-file", type=Path, default=None)
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--changed-file", action="append", default=[])
    args = parser.parse_args(argv)

    try:
        task_file = args.task_file
        if task_file is None:
            task_id = args.task_id or default_task_id()
            task_file = _task_file_for(task_id)
        if not task_file.is_absolute():
            task_file = ROOT / task_file
        base_ref = args.base_ref
        if base_ref == "origin/main":
            task_data = _read_yaml(task_file)
            task_base_ref = task_data.get("base_ref")
            if isinstance(task_base_ref, str) and task_base_ref.strip():
                base_ref = task_base_ref.strip()
        changed_files = args.changed_file or git_changed_files(base_ref)
        validate_task_scope(task_file=task_file, changed_files=changed_files)
    except TaskScopeError as exc:
        print(f"Task scope validation failed: {exc}", file=sys.stderr)
        return 1

    print("Task scope validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
