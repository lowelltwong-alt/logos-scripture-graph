from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_textual_critical_policy_docket as validator


def test_textual_critical_policy_docket_validates_current_repo() -> None:
    data = validator.validate_textual_critical_policy()

    assert data["object_type"] == "textual_critical_policy_docket"
    assert data["authority"]["requires_policy_before_variant_sensitive_promotion"] is True
    assert data["policy_status"]["textual_critical_policy_selected"] is False
    assert data["policy_status"]["selected_policy"] == "pending_owner_decision"
    assert data["authority"]["authorizes_textual_critical_decision"] is False
    assert "John.7.53-John.8.11" in data["variant_sensitive_surfaces"]


def test_textual_critical_policy_rejects_hidden_selected_policy(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_textual_critical_policy())
    data["policy_status"]["textual_critical_policy_selected"] = True
    data["policy_status"]["selected_policy"] = "secret_preference"
    candidate = tmp_path / "textual.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.TextualCriticalPolicyError, match="textual_critical_policy_selected"):
        validator.validate_textual_critical_policy(candidate)


def test_textual_critical_policy_rejects_authorizing_preferred_reading(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_textual_critical_policy())
    data["authority"]["authorizes_preferred_reading"] = True
    candidate = tmp_path / "textual.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.TextualCriticalPolicyError, match="authorizes_preferred_reading"):
        validator.validate_textual_critical_policy(candidate)
