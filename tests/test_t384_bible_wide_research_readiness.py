from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t384_bible_wide_research_readiness as validator


ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / ".ai" / "control" / "t384_bible_wide_research_readiness_synthesis.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t384_bible_wide_research_readiness_validates_current_repo() -> None:
    data = validator.validate_t384_bible_wide_research_readiness(SYNTHESIS)

    assert data["object_type"] == "bible_wide_chunking_research_readiness_synthesis"
    assert data["task_id"] == "T384"
    assert data["status"] == "complete_bible_wide_research_readiness_synthesis"
    assert data["goal_completed"]["completed_as_non_output_changing_research_readiness"] is True
    assert data["goal_completed"]["does_not_mean_chunking_ready_for_output"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_graph_edges"] is False
    assert data["coverage"]["corpus_scope"] == "canonical_66"
    assert data["coverage"]["bible_wide_research_registry_book_count"] == 66
    assert data["decision_register_entry"] == "CD-061"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-013"


def test_t384_maps_ready_lanes_research_gaps_blockers_and_owner_decisions() -> None:
    data = validator.validate_t384_bible_wide_research_readiness(SYNTHESIS)

    ready = {lane["lane_id"] for lane in data["what_is_ready_for_review_packet_strengthening"]}
    needs_more = {lane["lane_id"] for lane in data["what_needs_more_research"]}
    blockers = {blocker["blocker_id"] for blocker in data["what_must_remain_blocked"]}
    decisions = {decision["decision_id"] for decision in data["human_decisions_required"]}

    assert validator.REQUIRED_READY_LANES <= ready
    assert validator.REQUIRED_MORE_RESEARCH_LANES <= needs_more
    assert validator.REQUIRED_BLOCKERS <= blockers
    assert validator.REQUIRED_HUMAN_DECISIONS <= decisions

    hdm001 = next(decision for decision in data["human_decisions_required"] if decision["decision_id"] == "HDM-001")
    option_ids = {option["option_id"] for option in hdm001["faithful_options"]}
    assert validator.REQUIRED_T384_OPTIONS <= option_ids
    assert "selection_by_this_synthesis" in hdm001["non_authorizations"]


def test_t384_points_to_t385_owner_packet_without_authorizing_output() -> None:
    data = validator.validate_t384_bible_wide_research_readiness(SYNTHESIS)
    next_step = data["exact_next_non_output_step"]

    assert next_step["task_id"] == "T385"
    assert next_step["route_type"] == "owner_decision_packet_only"
    assert next_step["required_input"] == ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml"
    assert next_step["owner_decision_required_before_promotion_or_implementation"] is True
    for key in validator.REQUIRED_NEXT_FALSE:
        assert next_step[key] is False


def test_t384_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t384_bible_wide_research_readiness(SYNTHESIS))
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "synthesis.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T384ReadinessError, match="authorizes_chunk_output_change"):
        validator.validate_t384_bible_wide_research_readiness(candidate)


def test_t384_rejects_missing_human_decision(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t384_bible_wide_research_readiness(SYNTHESIS))
    data["human_decisions_required"] = [
        decision for decision in data["human_decisions_required"] if decision["decision_id"] != "HDM-005"
    ]
    candidate = tmp_path / "synthesis.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T384ReadinessError, match="HDM-005"):
        validator.validate_t384_bible_wide_research_readiness(candidate)
