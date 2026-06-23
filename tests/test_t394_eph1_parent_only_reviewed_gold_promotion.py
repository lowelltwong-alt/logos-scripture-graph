from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t394_eph1_parent_only_reviewed_gold_promotion as validator


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t394_eph1_parent_only_reviewed_gold_promotion_validates_current_repo() -> None:
    data = validator.validate_t394_eph1_parent_only_reviewed_gold_promotion()

    assert data["object_type"] == "parent_only_reviewed_gold_promotion_record"
    assert data["task_id"] == "T394"
    assert data["owner_decision"]["selected_option"] == "T393-A"
    assert data["owner_decision"]["selected_parent"] == "Eph.1.3-Eph.1.14"
    assert data["owner_decision"]["selected_children"] == []
    assert data["owner_decision"]["exact_internal_variant_refs"] == []
    assert data["authority"]["authorizes_parent_only_reviewed_gold_promotion"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False


def test_t394_promotion_keeps_variant_source_tradition_and_child_span_limits() -> None:
    data = validator.validate_t394_eph1_parent_only_reviewed_gold_promotion()
    finding = data["variant_and_source_tradition_findings"]
    child = data["child_span_finding"]

    assert finding["exact_internal_variant_refs"] == []
    assert finding["finding"] == "current_repo_non_dependent_for_parent_boundary_and_parent_only_reviewed_gold_claim"
    assert finding["source_tradition_finding"] == "current_repo_source_tradition_non_dependent_for_parent_boundary_and_parent_only_reviewed_gold_claim"
    assert child["child_spans_necessary_now"] is False
    assert child["child_spans_authorized"] is False
    assert child["permanent_child_span_denial"] is False
    assert "source_tradition_preference" in data["non_authorizations"]
    assert "child_span_selection" in data["non_authorizations"]


def test_t394_promotion_rejects_child_spans(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t394_eph1_parent_only_reviewed_gold_promotion())
    data["owner_decision"]["selected_children"] = ["Eph.1.3-Eph.1.6"]
    candidate = tmp_path / "promotion.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T394PromotionError, match="selected_children"):
        validator.validate_t394_eph1_parent_only_reviewed_gold_promotion(candidate)


def test_t394_promotion_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t394_eph1_parent_only_reviewed_gold_promotion())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "promotion.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T394PromotionError, match="authorizes_chunk_output_change"):
        validator.validate_t394_eph1_parent_only_reviewed_gold_promotion(candidate)
