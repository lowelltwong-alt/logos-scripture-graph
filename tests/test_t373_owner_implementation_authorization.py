from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t373_owner_implementation_authorization as validator


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t373_authorization_validates_current_repo() -> None:
    data = validator.validate_t373_owner_implementation_authorization()

    assert data["object_type"] == "owner_implementation_authorization_record"
    assert data["task_id"] == "T373"
    assert data["owner_decision"]["selected_option"] == "T373-A"
    assert data["scope"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["scope"]["selected_children"] == []
    assert data["authority"]["authorizes_exact_t374_pilot"] is True
    assert data["authority"]["authorizes_child_spans"] is False


def test_t373_authorization_keeps_child_spans_disallowed() -> None:
    data = validator.validate_t373_owner_implementation_authorization()

    assert data["child_span_policy"]["for_t374"] == "disallowed"
    assert "owner_explicitly_promotes_the_child_spans" in data["child_span_policy"]["future_allowed_only_if"]
    assert "child_span_selection" in data["non_authorizations"]
    assert "child_spans_are_added_without_later_owner_promotion" in data["t374_must_fail_if"]


def test_t373_authorization_requires_t374_audit_proof() -> None:
    data = validator.validate_t373_owner_implementation_authorization()

    requirements = set(data["t374_requirements_before_merge"])
    assert "non_target_identity_proof" in requirements
    assert "same_baseline_evaluation" in requirements
    assert "changed_output_manifest" in requirements
    assert "no_context_audit_surface" in requirements


def test_t373_authorization_rejects_child_span_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t373_owner_implementation_authorization())
    data["authority"]["authorizes_child_spans"] = True
    candidate = tmp_path / "t373.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T373AuthorizationError, match="authorizes_child_spans"):
        validator.validate_t373_owner_implementation_authorization(candidate)


def test_t373_authorization_rejects_missing_no_context_audit(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t373_owner_implementation_authorization())
    data["t374_requirements_before_merge"].remove("no_context_audit_surface")
    candidate = tmp_path / "t373.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T373AuthorizationError, match="no_context_audit_surface"):
        validator.validate_t373_owner_implementation_authorization(candidate)
