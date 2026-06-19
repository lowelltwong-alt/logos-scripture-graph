from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t372_route_isolation_harness_plan as validator


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t372_route_isolation_harness_plan_validates_current_repo() -> None:
    data = validator.validate_t372_route_isolation_harness_plan()

    assert data["object_type"] == "route_isolation_harness_plan"
    assert data["task_id"] == "T372"
    assert data["status"] == "complete_non_output_changing_plan"
    assert data["scope"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["scope"]["selected_children"] == []
    assert data["authority"]["records_harness_plan"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_implementation"] is False


def test_t372_plan_keeps_parent_only_gold_from_becoming_boundary() -> None:
    data = validator.validate_t372_route_isolation_harness_plan()
    limits = data["reviewed_gold_input_limits"]

    assert limits["may_cite_parent_only_reviewed_gold_as_input"] is True
    assert limits["may_treat_parent_span_as_output_chunk_boundary"] is False
    assert limits["may_infer_child_spans"] is False
    assert "parent_only_gold_as_chunk_boundary" in data["non_authorizations"]
    assert "child_span_selection" in data["non_authorizations"]


def test_t372_plan_requires_t373_before_implementation() -> None:
    data = validator.validate_t372_route_isolation_harness_plan()

    assert data["t373_owner_gate"]["next_task_id"] == "T373"
    assert data["t373_owner_gate"]["owner_decision_required"] is True
    assert data["t373_owner_gate"]["default_if_owner_unavailable"] == "stop_before_implementation_or_output_change"
    assert "T373_owner_implementation_authorization" in data["required_before_t374"]
    assert "non_target_identity_proof" in data["required_before_t374"]


def test_t372_plan_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t372_route_isolation_harness_plan())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "t372.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T372HarnessPlanError, match="authorizes_chunk_output_change"):
        validator.validate_t372_route_isolation_harness_plan(candidate)


def test_t372_plan_rejects_child_span_inference(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t372_route_isolation_harness_plan())
    data["reviewed_gold_input_limits"]["may_infer_child_spans"] = True
    candidate = tmp_path / "t372.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T372HarnessPlanError, match="may_infer_child_spans"):
        validator.validate_t372_route_isolation_harness_plan(candidate)
