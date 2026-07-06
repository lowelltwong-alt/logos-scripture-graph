from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_ai_pr_lifecycle_policy as validator


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ai" / "control" / "ai_pr_lifecycle_policy.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_ai_pr_lifecycle_policy_validates_current_repo() -> None:
    data = validator.validate_ai_pr_lifecycle_policy(POLICY)

    assert data["policy"]["ai_created_drafts_must_not_stall_below_pr_stage"] is True
    assert "pr_open_owner_approval_requested" in data["required_terminal_or_visible_states"]


def test_ai_pr_lifecycle_policy_requires_pr_or_owner_visible_exit(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_ai_pr_lifecycle_policy(POLICY))
    data["required_terminal_or_visible_states"].remove("pr_open_owner_approval_requested")
    candidate = tmp_path / "ai_pr_lifecycle_policy.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.AiPrLifecyclePolicyError, match="pr_open_owner_approval_requested"):
        validator.validate_ai_pr_lifecycle_policy(candidate)


def test_ai_pr_lifecycle_policy_rejects_merge_without_permission_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_ai_pr_lifecycle_policy(POLICY))
    data["authority"]["authorizes_merge_without_permission"] = True
    candidate = tmp_path / "ai_pr_lifecycle_policy.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.AiPrLifecyclePolicyError, match="authorizes_merge_without_permission"):
        validator.validate_ai_pr_lifecycle_policy(candidate)


def test_ai_pr_lifecycle_policy_requires_owner_alert_exit_field(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_ai_pr_lifecycle_policy(POLICY))
    data["draft_exit_requirements"].remove("owner_or_integrator_alert")
    candidate = tmp_path / "ai_pr_lifecycle_policy.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.AiPrLifecyclePolicyError, match="owner_or_integrator_alert"):
        validator.validate_ai_pr_lifecycle_policy(candidate)
