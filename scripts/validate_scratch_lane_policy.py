#!/usr/bin/env python3
"""Validate scratch lane policy contract and cross-links."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "scratch_lane_policy.yaml"
TEMPLATE = ROOT / ".ai" / "scratch" / "submissions" / "_template" / "promotion_packet.yaml"
TASK = ROOT / ".ai" / "tasks" / "T422.task.yaml"
CODEX_PROMPT = ROOT / ".ai" / "prompts" / "codex_promotion_packet_review_prompt.md"

REQUIRED_TOP = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "policy_id",
    "task_id",
    "status",
    "owner",
    "lanes",
    "allowed_paths",
    "hard_forbidden_paths",
    "promotion_packet",
    "authority",
    "non_authorizations",
    "validators",
}


class ScratchLanePolicyError(ValueError):
    """Raised when scratch lane policy is incomplete or unsafe."""


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
        raise ScratchLanePolicyError(f"{_rel(path)}: expected YAML mapping")
    return data


def validate_policy(data: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if data is None:
        if not POLICY.is_file():
            return [f"missing {_rel(POLICY)}"]
        data = _read_yaml(POLICY)

    missing = REQUIRED_TOP - set(data)
    if missing:
        errors.append(f"policy missing keys: {sorted(missing)}")

    if data.get("object_type") != "scratch_lane_policy":
        errors.append("object_type must be scratch_lane_policy")

    authority = data.get("authority", {})
    if authority.get("authorizes_reviewed_gold_promotion"):
        errors.append("scratch policy must not authorize reviewed gold")

    scratch = data.get("lanes", {}).get("scratch_lane", {})
    if scratch.get("branch_name_prefix") != "scratch/":
        errors.append("scratch_lane.branch_name_prefix must be scratch/")

    if not TEMPLATE.is_file():
        errors.append(f"missing promotion template {_rel(TEMPLATE)}")

    packet = data.get("promotion_packet", {})
    for field in (
        "submission_id",
        "risk_summary",
        "decisions",
        "requested_promotion",
        "non_authorizations",
    ):
        if field not in packet.get("required_top_level_fields", []):
            errors.append(f"promotion_packet missing required field {field}")

    if not CODEX_PROMPT.is_file():
        errors.append(f"missing {_rel(CODEX_PROMPT)}")

    return errors


def main() -> int:
    errors = validate_policy()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: {_rel(POLICY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
