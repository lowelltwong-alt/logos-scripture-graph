#!/usr/bin/env python3
"""Validate AI-created branch/PR lifecycle policy."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "ai_pr_lifecycle_policy.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
WORKFLOW_LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_STATES = {
    "pr_open_owner_approval_requested",
    "pr_open_green_merge_permission_already_granted",
    "merged_with_recorded_permission",
    "hold_with_findings_owner_visible",
    "closed_superseded_with_rationale",
    "abandoned_not_value_add_with_rationale",
    "escalated_to_owner_or_integrator",
}

REQUIRED_EXIT_FIELDS = {
    "branch_name",
    "task_id",
    "pr_url_or_reason_no_pr",
    "validation_status",
    "merge_permission_status",
    "next_action_state",
    "owner_or_integrator_alert",
    "superseded_or_not_value_add_rationale_when_applicable",
}

REQUIRED_NON_AUTHS = {
    "merge_without_green_checks",
    "merge_without_owner_or_prior_permission",
    "delete_user_work_without_instruction",
    "close_pr_without_review_or_rationale",
    "skip_owner_or_integrator_escalation",
    "treat_staged_work_as_complete",
    "dad_override_local_authority",
}


class AiPrLifecyclePolicyError(ValueError):
    """Raised when AI PR lifecycle policy is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: expected mapping")
    return data


def _string_set(value: Any, label: str) -> set[str]:
    if not isinstance(value, list) or not value:
        raise AiPrLifecyclePolicyError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise AiPrLifecyclePolicyError(f"{label} must contain only non-empty strings")
    return {str(item).strip() for item in value}


def validate_ai_pr_lifecycle_policy(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "ai_pr_lifecycle_policy",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "ai_pr_lifecycle_policy.v1",
        "policy_id": "repo_ai_pr_lifecycle_policy",
        "validator": "scripts/validate_ai_pr_lifecycle_policy.py",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise AiPrLifecyclePolicyError(f"{_rel(path)}: {key} must be {value!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_workflow_policy") is not True:
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: authority.records_workflow_policy must be true")
    for key in (
        "authorizes_merge_without_permission",
        "authorizes_delete_user_work",
        "authorizes_close_pr_without_review",
        "authorizes_skip_validation",
        "authorizes_dad_override_local_authority",
    ):
        if authority.get(key) is not False:
            raise AiPrLifecyclePolicyError(f"{_rel(path)}: authority.{key} must be false")

    policy = data.get("policy")
    if not isinstance(policy, dict):
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: policy must be a mapping")
    for key in (
        "ai_created_drafts_must_not_stall_below_pr_stage",
        "owner_visible_next_action_required",
        "merge_allowed_only_when_permission_already_given_or_owner_approves",
        "stale_branch_cleanup_requires_superseded_or_not_value_add_rationale",
        "integration_branch_required_for_stacked_or_dependent_prs",
    ):
        if policy.get(key) is not True:
            raise AiPrLifecyclePolicyError(f"{_rel(path)}: policy.{key} must be true")

    states = _string_set(data.get("required_terminal_or_visible_states"), f"{_rel(path)}.required_terminal_or_visible_states")
    missing_states = sorted(REQUIRED_STATES - states)
    if missing_states:
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: missing states {missing_states}")

    exit_fields = _string_set(data.get("draft_exit_requirements"), f"{_rel(path)}.draft_exit_requirements")
    missing_fields = sorted(REQUIRED_EXIT_FIELDS - exit_fields)
    if missing_fields:
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: missing draft exit fields {missing_fields}")

    obligations = _string_set(data.get("agent_obligations"), f"{_rel(path)}.agent_obligations")
    obligation_text = " ".join(obligations).lower()
    for needle in ("open a pr", "alert", "superseded", "dependent work"):
        if needle not in obligation_text:
            raise AiPrLifecyclePolicyError(f"{_rel(path)}: agent_obligations must mention {needle!r}")

    non_auths = _string_set(data.get("non_authorizations"), f"{_rel(path)}.non_authorizations")
    missing_non_auths = sorted(REQUIRED_NON_AUTHS - non_auths)
    if missing_non_auths:
        raise AiPrLifecyclePolicyError(f"{_rel(path)}: missing non_authorizations {missing_non_auths}")

    for wired_path, needles in {
        FRONT_DOOR: ["ai_pr_lifecycle_policy.yaml", "draft branch", "PR"],
        WORKFLOW_LESSONS: ["WORKFLOW-LESSON-011", "pr_open_owner_approval_requested"],
        LESSON_INDEX: ["LSN-045", "ai_pr_lifecycle_policy.yaml"],
        VALIDATE_ALL: ["validate_ai_pr_lifecycle_policy.py"],
    }.items():
        text = _read_text(wired_path)
        for needle in needles:
            if needle not in text:
                raise AiPrLifecyclePolicyError(f"{_rel(wired_path)}: missing policy wiring string {needle!r}")

    return data


def main() -> int:
    try:
        validate_ai_pr_lifecycle_policy()
    except AiPrLifecyclePolicyError as exc:
        print(f"AI PR lifecycle policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("AI PR lifecycle policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
