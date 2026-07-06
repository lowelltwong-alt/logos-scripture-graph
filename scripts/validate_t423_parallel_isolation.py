#!/usr/bin/env python3
"""Validate T423 parallel-path isolation (one model, own folder, no T417 bleed)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import SCRATCH_ROOT, load_fork_policy
T417_FORBIDDEN_PREFIXES = (
    ".ai/context/agent_work/T417/model_layers/batch2/",
)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _normalize(path: str) -> str:
    normalized = path.replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _git_branch() -> str:
    try:
        return subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _git_changed_files() -> list[str]:
    paths: list[str] = []
    for args in (
        ["diff", "--cached", "--name-only"],
        ["diff", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        try:
            out = subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
            paths.extend(line.strip() for line in out.splitlines() if line.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    seen: set[str] = set()
    result: list[str] = []
    for path in paths:
        norm = _normalize(path)
        if norm not in seen:
            seen.add(norm)
            result.append(norm)
    return result


def validate_parallel_isolation(
    *,
    branch: str | None = None,
    changed_files: list[str] | None = None,
    model_folder: Path | None = None,
    policy: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    policy = policy or load_fork_policy()
    isolation = policy.get("parallel_path_isolation", {})

    if not isolation.get("worktree_required"):
        errors.append("parallel_path_isolation.worktree_required must be true")

    branch = branch or _git_branch()
    allowed_branch = branch.startswith("scratch/t423-") or (
        model_folder is None and branch.startswith("codex/t423-")
    )
    if branch and not allowed_branch:
        errors.append(
            f"branch {branch!r} should start with scratch/t423- for model marathon work "
            "or codex/t423- for integration review"
        )

    files = [_normalize(p) for p in (changed_files if changed_files is not None else _git_changed_files())]
    for path in files:
        for prefix in T417_FORBIDDEN_PREFIXES:
            if path.startswith(prefix) or fnmatch(path, prefix.rstrip("/") + "/**"):
                errors.append(f"T417 batch2 path touched in T423 worktree: {path}")

    forbidden = isolation.get("forbidden_reads", [])
    for path in files:
        for rule in forbidden:
            rule_norm = _normalize(str(rule)).rstrip("/")
            if path.startswith(rule_norm) or fnmatch(path, rule_norm + "/**"):
                errors.append(f"forbidden path modified: {path}")

    if model_folder and model_folder.is_dir():
        manifest_path = model_folder / "model_manifest.yaml"
        if manifest_path.is_file():
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                errors.append(f"{_rel(manifest_path)}: expected mapping")
            else:
                iso = data.get("isolation", {})
                if not iso.get("forbidden_reads_ack"):
                    errors.append(f"{_rel(manifest_path)}: isolation.forbidden_reads_ack must be true")
                if isolation.get("worktree_required") and not iso.get("worktree_path"):
                    errors.append(f"{_rel(manifest_path)}: isolation.worktree_path required")

        try:
            allowed_prefix = _normalize(str(model_folder.relative_to(ROOT))) + "/"
        except ValueError:
            allowed_prefix = ""
            errors.append(f"model_folder outside repository: {_rel(model_folder)}")
        for path in files:
            if allowed_prefix and path.startswith(".ai/scratch/multi_model_bible_chunking/") and not path.startswith(allowed_prefix):
                if not path.startswith(".ai/scratch/multi_model_bible_chunking/comparison/"):
                    errors.append(f"change outside model folder: {path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy-only", action="store_true", help="Check fork policy fields only (for validate_all)")
    parser.add_argument("--branch", help="Override git branch")
    parser.add_argument("--file", action="append", dest="files")
    parser.add_argument("--model-folder", type=Path, help="Model folder e.g. .ai/scratch/.../M1_cursor")
    args = parser.parse_args()

    if args.policy_only:
        policy = load_fork_policy()
        errors: list[str] = []
        if not policy.get("parallel_path_isolation", {}).get("worktree_required"):
            errors.append("parallel_path_isolation.worktree_required must be true")
        if not policy.get("pilot_gate"):
            errors.append("pilot_gate section required")
        exec_mode = policy.get("execution_mode", {})
        if exec_mode.get("compare_when") != "all_models_complete_batch_offline_only":
            errors.append("execution_mode.compare_when must be all_models_complete_batch_offline_only")
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        print("T423 parallel isolation policy: OK")
        return 0

    errors = validate_parallel_isolation(
        branch=args.branch,
        changed_files=args.files,
        model_folder=args.model_folder,
    )
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("T423 parallel isolation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
