from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_owner_decision_option_presentation_policy as validator


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_owner_decision_option_presentation_policy_validates_current_repo() -> None:
    data = validator.validate_owner_decision_option_presentation_policy()

    assert data["object_type"] == "owner_decision_option_presentation_policy"
    assert data["decision_register_entry"] == "CD-051"
    assert data["authority"]["records_presentation_requirement"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False


def test_owner_decision_policy_requires_repercussions_and_non_authorizations() -> None:
    data = validator.validate_owner_decision_option_presentation_policy()

    required = set(data["required_for_future_owner_gates"])
    assert "all_good_options" in required
    assert "downstream_effect" in required
    assert "what_each_option_does_not_authorize" in required
    assert "stop_conditions" in required
    assert "recommendation_as_owner_selection" in data["non_authorizations"]


def test_owner_decision_policy_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_owner_decision_option_presentation_policy())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "owner_options.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.OwnerDecisionOptionPresentationPolicyError, match="authorizes_chunk_output_change"):
        validator.validate_owner_decision_option_presentation_policy(candidate)


def test_owner_decision_policy_rejects_missing_downstream_effect(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_owner_decision_option_presentation_policy())
    data["required_for_future_owner_gates"].remove("downstream_effect")
    candidate = tmp_path / "owner_options.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.OwnerDecisionOptionPresentationPolicyError, match="downstream_effect"):
        validator.validate_owner_decision_option_presentation_policy(candidate)
