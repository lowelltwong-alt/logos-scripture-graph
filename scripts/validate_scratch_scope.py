#!/usr/bin/env python3
"""Fast scope check for scratch-lane branches (no full validate_all)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "scratch_lane_policy.yaml"


class ScratchScopeError(ValueError):
    """Raised when scratch scope is violated."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _normalize(path: str) -> str:
    normalized = path.replace("\\", "/").strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _read_policy() -> dict[str, Any]:
    text = POLICY.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ScratchScopeError("scratch_lane_policy.yaml must be a mapping")
    return data


def _matches_rule(path: str, rule: str) -> bool:
    path = _normalize(path)
    rule = _normalize(rule)
    if "*" in rule:
        return fnmatch(path, rule)
    if rule.endswith("/"):
        return path.startswith(rule)
    return path == rule


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


def validate_scratch_scope(
    *,
    branch: str | None = None,
    changed_files: list[str] | None = None,
    policy: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if policy is None:
        if not POLICY.is_file():
            return [f"missing {_rel(POLICY)}"]
        policy = _read_policy()

    branch = branch or _git_branch()
    prefix = policy.get("lanes", {}).get("scratch_lane", {}).get("branch_name_prefix", "scratch/")
    if not branch.startswith(prefix):
        errors.append(f"branch {branch!r} must start with {prefix!r} for scratch lane commits")

    allowed = policy.get("allowed_paths", [])
    forbidden = policy.get("hard_forbidden_paths", [])
    files = [_normalize(p) for p in (changed_files if changed_files is not None else _git_changed_files())]

    for path in files:
        if any(_matches_rule(path, rule) for rule in forbidden):
            errors.append(f"hard-forbidden path in scratch lane: {path}")
        if not any(_matches_rule(path, rule) for rule in allowed):
            errors.append(f"path not allowed in scratch lane: {path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", help="Override detected git branch")
    parser.add_argument("--file", action="append", dest="files", help="Check specific path(s)")
    args = parser.parse_args()

    errors = validate_scratch_scope(branch=args.branch, changed_files=args.files)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("scratch scope: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
