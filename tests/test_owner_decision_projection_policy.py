from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_owner_decision_projection_policy as validator


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ai" / "control" / "owner_decision_projection_policy.yaml"


def test_owner_decision_projection_policy_validates_current_repo() -> None:
    data = validator.validate_owner_decision_projection_policy(POLICY)

    assert data["object_type"] == "owner_decision_projection_policy"
    assert data["authority"]["records_projection_policy"] is True
    assert data["authority"]["records_projected_owner_pattern_decisions"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False


def test_projection_policy_requires_conflict_scan_and_stop_for_conflicts() -> None:
    data = validator.validate_owner_decision_projection_policy(POLICY)
    conflict = data["conflict_policy"]

    assert conflict["conflict_scan_required_for_every_projected_decision"] is True
    assert conflict["if_conflict_detected"] == "stop_and_surface_to_owner_before_work_continues"
    assert "prior_owner_decisions_conflict_for_the_target_text" in data["projection_must_stop_when"]
    assert "conflict_scan_finds_no_conflicting_owner_decisions_for_the_target_text" in data["projection_allowed_when"]


def test_1cor8_10_projection_is_parent_only_and_non_authorizing() -> None:
    data = validator.validate_owner_decision_projection_policy(POLICY)
    projected = {
        item["projection_id"]: item
        for item in data["current_projected_decisions"]
    }
    onecor = projected["ODP-20260618-1COR8-10-PARENT"]

    assert onecor["selected_option"] == "1COR8-10-T369-B"
    assert onecor["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert onecor["selected_children"] == []
    assert onecor["conflict_scan_result"] == "no_conflict_detected"
    assert "child_span_projection" in onecor["non_authorizations"]
    assert "chunk_output_change" in onecor["non_authorizations"]


def test_projection_policy_rejects_missing_conflict_scan(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_owner_decision_projection_policy(POLICY))
    data["current_projected_decisions"][0]["conflict_scan_result"] = "not_checked"
    candidate = tmp_path / "projection.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.ProjectionPolicyError, match="no-conflict scan"):
        validator.validate_owner_decision_projection_policy(candidate)
