from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t371_parent_only_reviewed_gold_promotion as validator


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t371_parent_only_reviewed_gold_promotion_validates_current_repo() -> None:
    data = validator.validate_t371_parent_only_reviewed_gold_promotion()

    assert data["object_type"] == "parent_only_reviewed_gold_promotion_record"
    assert data["task_id"] == "T371"
    assert data["owner_decision"]["selected_option"] == "T371-A"
    assert data["owner_decision"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["owner_decision"]["selected_children"] == []
    assert data["authority"]["authorizes_parent_only_reviewed_gold_promotion"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False


def test_t371_promotion_keeps_variant_non_dependency_narrow() -> None:
    data = validator.validate_t371_parent_only_reviewed_gold_promotion()
    findings = {item["ref"]: item for item in data["variant_non_dependency_findings"]}

    assert set(findings) == {"1Cor.9.20", "1Cor.10.9"}
    assert findings["1Cor.9.20"]["finding"] == "non_dependent_for_parent_boundary_and_parent_only_reviewed_gold_claim"
    assert findings["1Cor.10.9"]["finding"] == "non_dependent_for_parent_boundary_and_parent_only_reviewed_gold_claim"
    assert "source_tradition_preference" in data["non_authorizations"]
    assert "child_span_selection" in data["non_authorizations"]


def test_t371_promotion_rejects_child_spans(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t371_parent_only_reviewed_gold_promotion())
    data["owner_decision"]["selected_children"] = ["1Cor.8.1-1Cor.8.13"]
    candidate = tmp_path / "promotion.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T371PromotionError, match="selected_children"):
        validator.validate_t371_parent_only_reviewed_gold_promotion(candidate)


def test_t371_promotion_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t371_parent_only_reviewed_gold_promotion())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "promotion.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T371PromotionError, match="authorizes_chunk_output_change"):
        validator.validate_t371_parent_only_reviewed_gold_promotion(candidate)
