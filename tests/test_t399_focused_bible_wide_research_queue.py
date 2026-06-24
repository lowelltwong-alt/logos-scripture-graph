from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t399_focused_bible_wide_research_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "t399_focused_bible_wide_research_queue.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t399_queue_validates_current_repo() -> None:
    data = validator.validate_t399_focused_bible_wide_research_queue(QUEUE)

    assert data["object_type"] == "focused_bible_wide_research_queue"
    assert data["task_id"] == "T399"
    assert data["status"] == "complete_goal2_focused_research_queue"
    assert data["goal2_scope"]["final_target_selected"] is False
    assert data["goal2_scope"]["reviewed_gold_promoted"] is False
    assert data["decision_register_entry"] == "CD-073"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-027"


def test_t399_queue_covers_required_candidates_and_lanes() -> None:
    data = validator.validate_t399_focused_bible_wide_research_queue(QUEUE)

    candidate_ids = {entry["candidate_id"] for entry in data["focused_research_queue"]}
    lanes = {entry["lane_id"] for entry in data["focused_research_queue"]}
    assert validator.REQUIRED_CANDIDATES <= candidate_ids
    assert validator.REQUIRED_LANES <= lanes
    assert data["focused_research_queue"][0]["candidate_id"] == "T399-Q001"
    assert data["focused_research_queue"][0]["score"] == 91


def test_t399_queue_blocks_variant_source_tradition_candidates() -> None:
    data = validator.validate_t399_focused_bible_wide_research_queue(QUEUE)
    by_id = {entry["candidate_id"]: entry for entry in data["focused_research_queue"]}

    for candidate_id in validator.BLOCKED_CANDIDATES:
        assert by_id[candidate_id]["safe_for_review_only_strengthening_now"] is False
        assert by_id[candidate_id]["review_only_safety_status"] == "blocked_until_case_policy_or_owner_decision"


def test_t399_queue_keeps_all_authority_flags_closed() -> None:
    data = validator.validate_t399_focused_bible_wide_research_queue(QUEUE)

    for key in validator.REQUIRED_FALSE_AUTHORITY:
        assert data["authority"][key] is False
    assert validator.REQUIRED_NON_AUTHORIZATIONS <= set(data["non_authorizations"])
    assert all(decision["recommendation_is_owner_selection"] is False for decision in data["owner_decision_map"])


def test_t399_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t399_focused_bible_wide_research_queue(QUEUE))
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "t399.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T399QueueError, match="authorizes_chunk_output_change"):
        validator.validate_t399_focused_bible_wide_research_queue(candidate)


def test_t399_rejects_owner_recommendation_as_selection(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t399_focused_bible_wide_research_queue(QUEUE))
    data["owner_decision_map"][0]["recommendation_is_owner_selection"] = True
    candidate = tmp_path / "t399.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T399QueueError, match="recommendation_is_owner_selection"):
        validator.validate_t399_focused_bible_wide_research_queue(candidate)
