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
    assert data["authority"]["authorizes_parent_first_pilot_then_child_necessity_review_pattern"] is True
    assert data["owner_decision"]["pilot_pattern_decision_register_update"] == "CD-052"


def test_t373_authorization_keeps_child_spans_disallowed() -> None:
    data = validator.validate_t373_owner_implementation_authorization()

    assert data["child_span_policy"]["for_t374"] == "disallowed"
    assert "owner_explicitly_promotes_the_child_spans" in data["child_span_policy"]["future_allowed_only_if"]
    assert "post_parent_pilot_review_finds_child_span_is_necessary" in data["child_span_policy"]["future_allowed_only_if"]
    assert "child_span_selection" in data["non_authorizations"]
    assert "child_span_without_post_pilot_review" in data["non_authorizations"]
    assert "child_spans_are_added_without_later_owner_promotion" in data["t374_must_fail_if"]


def test_t373_authorization_records_parent_first_pilot_pattern() -> None:
    data = validator.validate_t373_owner_implementation_authorization()
    pattern = data["general_parent_first_pilot_pattern"]

    assert pattern["pattern_id"] == "parent_first_pilot_then_child_necessity_review"
    assert pattern["decision_register_entry"] == "CD-052"
    assert "authorize_exact_parent_only_pilot" in pattern["required_sequence"]
    assert "perform_post_pilot_child_necessity_review" in pattern["required_sequence"]
    assert "owner_decides_whether_child_span_work_is_needed" in pattern["required_sequence"]
    assert "automatic_child_spans_after_parent_pilot" in pattern["non_authorizations"]
    assert "treating_pilot_success_as_general_algorithm_authority" in pattern["non_authorizations"]


def test_t373_authorization_requires_t374_audit_proof() -> None:
    data = validator.validate_t373_owner_implementation_authorization()

    requirements = set(data["t374_requirements_before_merge"])
    assert "non_target_identity_proof" in requirements
    assert "same_baseline_evaluation" in requirements
    assert "changed_output_manifest" in requirements
    assert "no_context_audit_surface" in requirements
    assert "post_pilot_child_necessity_review_gate" in requirements


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


def test_t373_authorization_rejects_missing_post_pilot_review(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t373_owner_implementation_authorization())
    data["general_parent_first_pilot_pattern"]["required_sequence"].remove("perform_post_pilot_child_necessity_review")
    candidate = tmp_path / "t373.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T373AuthorizationError, match="perform_post_pilot_child_necessity_review"):
        validator.validate_t373_owner_implementation_authorization(candidate)
