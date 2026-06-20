from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t375_post_pilot_review as validator


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / ".ai" / "control" / "t375_post_pilot_review.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t375_post_pilot_review_validates_current_repo() -> None:
    data = validator.validate_t375_post_pilot_review(REVIEW)

    assert data["object_type"] == "t375_post_pilot_review"
    assert data["task_id"] == "T375"
    assert data["status"] == "complete_review_only_child_spans_not_necessary_now"
    assert data["scope"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["scope"]["selected_children"] == []
    assert data["scope"]["decision_register_entry"] == "CD-057"
    assert data["next_route"]["task_id"] == "T376"
    assert data["next_route"]["owner_decision_required"] is True


def test_t375_same_baseline_review_is_non_output_changing() -> None:
    data = validator.validate_t375_post_pilot_review(REVIEW)
    same = data["same_baseline_review"]

    assert same["baseline_chunk_count"] == 1136
    assert same["candidate_chunk_count"] == 1137
    assert same["added_overlay_count"] == 1
    assert same["baseline_prefix_matches_pre_t374_bytes"] is True
    assert same["non_target_output_diff_detected"] is False
    assert same["evaluator_formula_changed"] is False
    assert same["improvement_claim_allowed"] is False
    assert data["authority"]["authorizes_new_chunk_output"] is False


def test_t375_child_spans_are_not_promoted() -> None:
    data = validator.validate_t375_post_pilot_review(REVIEW)
    child = data["child_necessity_review"]

    assert child["finding"] == "child_spans_not_necessary_now"
    assert child["current_child_span_authority"] == "none"
    assert child["selected_children"] == []
    assert len(child["child_span_candidates_not_promoted"]) == 6
    assert data["authority"]["authorizes_child_spans"] is False
    assert "child_span_selection" in data["non_authorizations"]


def test_t375_review_rejects_child_span_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t375_post_pilot_review(REVIEW))
    data["authority"]["authorizes_child_spans"] = True
    candidate = tmp_path / "review.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T375ReviewError, match="authorizes_child_spans"):
        validator.validate_t375_post_pilot_review(candidate)


def test_t375_review_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t375_post_pilot_review(REVIEW))
    data["authority"]["authorizes_new_chunk_output"] = True
    candidate = tmp_path / "review.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T375ReviewError, match="authorizes_new_chunk_output"):
        validator.validate_t375_post_pilot_review(candidate)
