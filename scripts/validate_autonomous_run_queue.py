#!/usr/bin/env python3
"""Validate autonomous run queue and optional work-unit completion markers."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "autonomous_run_queue.yaml"
PROCESSOR = ROOT / ".ai" / "control" / "autonomous_corpus_processor.yaml"
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


def _validate_processor() -> list[str]:
    errors: list[str] = []
    if not PROCESSOR.exists():
        return [f"missing {_rel(PROCESSOR)}"]
    data = _read_yaml(PROCESSOR)
    policy = data.get("efficiency_policy")
    if not isinstance(policy, dict):
        errors.append("autonomous_corpus_processor: efficiency_policy required")
    elif "work_unit_definition" not in policy:
        errors.append("autonomous_corpus_processor: work_unit_definition required")
    stop = data.get("efficiency_policy", {}).get("stop_conditions")
    if not isinstance(stop, list) or "backlog_exhausted_for_current_lane" not in stop:
        errors.append("processor must stop on backlog exhaustion")
    return errors


def _validate_queue(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("active_task_id") != "T417":
        errors.append("active_task_id must be T417")
    if not data.get("kickoff_prompt"):
        errors.append("kickoff_prompt is required")
    if not data.get("session_stop_when"):
        errors.append("session_stop_when is required for outcome-based queues")
    units = data.get("work_units")
    legacy = data.get("work_packages")
    if units is None and legacy is not None:
        units = legacy
    if not isinstance(units, list) or not units:
        errors.append("work_units must be a non-empty list")
        return errors
    seen: set[str] = set()
    for unit in units:
        if not isinstance(unit, dict):
            errors.append("each work unit must be a mapping")
            continue
        unit_id = unit.get("unit_id") or unit.get("package_id")
        if not isinstance(unit_id, str) or not unit_id:
            errors.append("work unit missing unit_id")
            continue
        if unit_id in seen:
            errors.append(f"duplicate unit_id: {unit_id}")
        seen.add(unit_id)
        for key in ("title", "deliverables", "validations", "commit_message"):
            if key not in unit:
                errors.append(f"{unit_id}: missing {key}")
        deliverables = unit.get("deliverables")
        if not isinstance(deliverables, list) or not deliverables:
            errors.append(f"{unit_id}: deliverables must be a non-empty list")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority mapping required")
    elif authority.get("authorizes_chunk_output_change"):
        errors.append("autonomous queue must not authorize chunk output")
    return errors


def _validate_unit_deliverables(data: dict[str, Any], unit_id: str) -> list[str]:
    errors: list[str] = []
    units = data.get("work_units") or data.get("work_packages") or []
    unit = next(
        (
            u
            for u in units
            if isinstance(u, dict) and (u.get("unit_id") == unit_id or u.get("package_id") == unit_id)
        ),
        None,
    )
    if unit is None:
        return [f"unknown unit_id: {unit_id}"]
    if unit.get("status") == "complete":
        return []
    if unit.get("optional") and unit.get("status") == "skipped":
        return []
    deliverables = unit.get("deliverables", [])
    if not isinstance(deliverables, list):
        return [f"{unit_id}: deliverables not a list"]
    for rel in deliverables:
        if not isinstance(rel, str):
            errors.append(f"{unit_id}: invalid deliverable entry")
            continue
        path = ROOT / rel
        if not path.exists():
            errors.append(f"{unit_id}: missing deliverable {_rel(path)}")
    return errors


def _validate_task_alignment() -> list[str]:
    errors: list[str] = []
    if not TASK.exists():
        return ["missing .ai/tasks/T417.task.yaml"]
    task = _read_yaml(TASK)
    if task.get("id") != "T417":
        errors.append("T417.task.yaml id must be T417")
    queue_ref = task.get("autonomous_run_queue")
    if queue_ref not in (".ai/control/autonomous_run_queue.yaml", None):
        errors.append("T417.task.yaml must reference autonomous_run_queue.yaml")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unit", help="Validate deliverables exist for one work unit id")
    parser.add_argument("--package", help="Deprecated alias for --unit")
    args = parser.parse_args()
    unit_id = args.unit or args.package
    try:
        if not QUEUE.exists():
            raise AutonomousRunQueueError(f"missing {_rel(QUEUE)}")
        data = _read_yaml(QUEUE)
        errors = _validate_queue(data)
        errors.extend(_validate_processor())
        errors.extend(_validate_task_alignment())
        if unit_id:
            errors.extend(_validate_unit_deliverables(data, unit_id))
        if errors:
            raise AutonomousRunQueueError("; ".join(errors))
        print("autonomous run queue: OK")
        return 0
    except AutonomousRunQueueError as exc:
        print(f"autonomous run queue: FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
