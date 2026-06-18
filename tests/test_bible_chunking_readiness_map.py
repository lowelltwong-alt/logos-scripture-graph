from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_bible_chunking_readiness_map as validator


ROOT = Path(__file__).resolve().parents[1]
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"


def test_readiness_map_validates_and_is_non_authorizing() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    assert data["object_type"] == "bible_chunking_readiness_map"
    assert data["trust_zone"] == "canonical"
    assert data["authority"]["records_readiness"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_new_algorithm_work"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_skill_lifecycle_promotion"] is False
    assert data["authority"]["authorizes_boundary_import"] is False


def test_faithful_route_is_one_lane_at_a_time() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    assert data["faithful_execution_model"]["route"] == "one_lane_at_a_time_under_bible_wide_map"
    assert data["current_baseline"]["corpus_scope"] == "canonical_66"
    assert data["current_baseline"]["improvement_claim_allowed"] is False


def test_required_lanes_are_present_and_block_new_algorithm_work() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    by_lane = {lane["lane_id"]: lane for lane in data["lane_sequence"]}

    assert set(by_lane) >= validator.REQUIRED_LANES
    assert by_lane["revelation_apocalyptic"]["review_order"] == 1
    assert by_lane["bible_wide_orchestration"]["implementation_order"] == 8
    assert all(lane["new_algorithm_work_ready"] is False for lane in by_lane.values())


def test_lessons_are_stored_in_first_class_surfaces() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    surfaces = set(data["lessons_storage"]["surfaces"])
    assert validator.REQUIRED_LESSON_SURFACES <= surfaces
    assert ".ai/control/chunking_theological_decision_register.yaml" in surfaces
    assert ".ai/control/john3_wj_owner_review_docket.yaml" in surfaces
    assert ".ai/control/bible_wide_chunking_research_registry.yaml" in surfaces
    assert ".ai/control/source_metadata_research_atlas.yaml" in surfaces
    assert ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml" in surfaces
    assert ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml" in surfaces
    assert ".ai/control/gospel_wj_discourse_dossier_queue.yaml" in surfaces
    assert ".ai/control/narrative_legal_covenant_dossier_queue.yaml" in surfaces
    assert ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml" in surfaces
    assert ".ai/control/prophetic_oracle_vision_dossier_queue.yaml" in surfaces


def test_prophetic_oracle_lane_records_t365_without_algorithm_authority() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    by_lane = {lane["lane_id"]: lane for lane in data["lane_sequence"]}
    prophetic = by_lane["prophetic_oracle"]

    assert prophetic["current_state"] == "t365_research_dossier_queue_seeded_needs_review_packets"
    assert prophetic["new_algorithm_work_ready"] is False
    assert prophetic["dossier_queue"]["task_id"] == "T365"
    assert prophetic["dossier_queue"]["path"] == ".ai/control/prophetic_oracle_vision_dossier_queue.yaml"
    assert prophetic["dossier_queue"]["output_change_authorized"] is False
    assert prophetic["dossier_queue"]["implementation_authorized"] is False
    assert prophetic["dossier_queue"]["reviewed_gold_promoted"] is False


def test_parallel_research_queue_records_t358_without_replacing_john3_route() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    queue = data["parallel_research_queue"]

    assert data["next_route"]["task_id"] == "T356"
    assert queue["task_id"] == "T358"
    assert queue["route_type"] == "whole_bible_research_registry"
    assert queue["path"] == ".ai/control/bible_wide_chunking_research_registry.yaml"
    assert queue["corpus_scope"] == "canonical_66"
    assert queue["book_count"] == 66
    assert queue["output_change_authorized"] is False
    assert queue["implementation_authorized"] is False
    assert queue["reviewed_gold_promoted"] is False


def test_next_route_advances_to_t356_john3_owner_review_docket() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    assert data["next_route"]["task_id"] == "T356"
    assert data["next_route"]["route_type"] == "john3_wj_owner_review_docket"
    assert data["next_route"]["recommended_target"] == "gospel_discourse_wj"
    assert data["next_route"]["owner_selection_status"] == "selected"
    assert data["next_route"]["selected_option"] == "REV-T344-E"
    assert data["next_route"]["selection_docket"] == "docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md"
    assert data["next_route"]["triage_map"] == ".ai/control/bible_chunking_research_triage_map.yaml"
    assert data["next_route"]["prior_triage_task"] == "T351"
    assert data["next_route"]["prior_inventory_task"] == "T354"
    assert data["next_route"]["prior_policy_task"] == "T355"
    assert data["next_route"]["review_packet_lane"] == "gospel_discourse_wj"
    assert data["next_route"]["policy"] == ".ai/control/wj_speaker_discourse_policy.yaml"
    assert data["next_route"]["docket"] == ".ai/control/john3_wj_owner_review_docket.yaml"
    assert data["next_route"]["selected_target"] == "john3_wj_speaker_boundary"
    assert data["next_route"]["selected_passage"] == "John.3.1-John.3.36"
    assert data["next_route"]["selected_target_status"] == "owner_selection_pending"
    assert data["next_route"]["john3_owner_selection_status"] == "pending"
    assert data["next_route"]["john3_selected_option"] == "pending"
    assert data["next_route"]["output_change_authorized"] is False
    assert data["next_route"]["implementation_authorized"] is False
    assert data["next_route"]["reviewed_gold_promoted"] is False


def test_validator_rejects_missing_required_lane(tmp_path: Path) -> None:
    text = READINESS_MAP.read_text(encoding="utf-8")
    text = text.replace("lane_id: gospel_discourse_wj", "lane_id: gospel_discourse_missing")
    candidate = tmp_path / "readiness.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(validator.ReadinessMapError, match="lane_sequence missing"):
        validator.validate_readiness_map(candidate)
