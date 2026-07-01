#!/usr/bin/env python3
"""Validate autonomous run queue and optional package completion markers."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "autonomous_run_queue.yaml"
TASK = ROOT / ".ai" / "tasks" / "T417.task.yaml"


class AutonomousRunQueueError(ValueError):
    """Raised when autonomous run queue state is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise AutonomousRunQueueError(f"{_rel(path)}: expected YAML mapping")
    return data


def _validate_queue(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("active_task_id") != "T417":
        errors.append("active_task_id must be T417")
    if not data.get("kickoff_prompt"):
        errors.append("kickoff_prompt is required")
    packages = data.get("work_packages")
    if not isinstance(packages, list) or not packages:
        errors.append("work_packages must be a non-empty list")
        return errors
    seen: set[str] = set()
    for pkg in packages:
        if not isinstance(pkg, dict):
            errors.append("each work package must be a mapping")
            continue
        pkg_id = pkg.get("package_id")
        if not isinstance(pkg_id, str) or not pkg_id:
            errors.append("work package missing package_id")
            continue
        if pkg_id in seen:
            errors.append(f"duplicate package_id: {pkg_id}")
        seen.add(pkg_id)
        for key in ("title", "estimated_minutes", "deliverables", "validations", "commit_message"):
            if key not in pkg:
                errors.append(f"{pkg_id}: missing {key}")
        deliverables = pkg.get("deliverables")
        if not isinstance(deliverables, list) or not deliverables:
            errors.append(f"{pkg_id}: deliverables must be a non-empty list")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority mapping required")
    elif authority.get("authorizes_chunk_output_change"):
        errors.append("autonomous queue must not authorize chunk output")
    return errors


def _validate_package_deliverables(data: dict[str, Any], package_id: str) -> list[str]:
    errors: list[str] = []
    packages = data.get("work_packages", [])
    pkg = next((p for p in packages if isinstance(p, dict) and p.get("package_id") == package_id), None)
    if pkg is None:
        return [f"unknown package_id: {package_id}"]
    deliverables = pkg.get("deliverables", [])
    if not isinstance(deliverables, list):
        return [f"{package_id}: deliverables not a list"]
    for rel in deliverables:
        if not isinstance(rel, str):
            errors.append(f"{package_id}: invalid deliverable entry")
            continue
        path = ROOT / rel
        if not path.exists():
            errors.append(f"{package_id}: missing deliverable {_rel(path)}")
    return errors


def _validate_task_alignment() -> list[str]:
    errors: list[str] = []
    if not TASK.exists():
        return ["missing .ai/tasks/T417.task.yaml"]
    task = _read_yaml(TASK)
    if task.get("id") != "T417":
        errors.append("T417.task.yaml id must be T417")
    if task.get("autonomous_run_queue") != ".ai/control/autonomous_run_queue.yaml":
        errors.append("T417.task.yaml must reference autonomous_run_queue.yaml")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", help="Validate deliverables exist for one work package id")
    args = parser.parse_args()
    try:
        if not QUEUE.exists():
            raise AutonomousRunQueueError(f"missing {_rel(QUEUE)}")
        data = _read_yaml(QUEUE)
        errors = _validate_queue(data)
        errors.extend(_validate_task_alignment())
        if args.package:
            errors.extend(_validate_package_deliverables(data, args.package))
        if errors:
            raise AutonomousRunQueueError("; ".join(errors))
        print("autonomous run queue: OK")
        return 0
    except AutonomousRunQueueError as exc:
        print(f"autonomous run queue: FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
