from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_wj_speaker_discourse_policy as validator


def test_wj_speaker_discourse_policy_passes_current_repo() -> None:
    data = validator.validate_wj_speaker_discourse_policy()

    assert data["authority"]["selects_review_target"] is True
    assert data["authority"]["authorizes_speaker_boundary"] is False
    assert data["authority"]["authorizes_discourse_boundary"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False


def test_wj_speaker_discourse_policy_selects_john3_without_output_change() -> None:
    data = validator.validate_wj_speaker_discourse_policy()
    selected = data["selected_first_review_target"]

    assert selected["target_id"] == "john3_wj_speaker_boundary"
    assert selected["passage"] == "John.3.1-John.3.36"
    assert selected["selection_status"] == "selected_for_next_owner_review"
    assert selected["review_packet"] == "eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md"
    assert selected["implementation_allowed"] is False
    assert selected["output_change_authorized"] is False
    assert selected["reviewed_gold_promoted"] is False


def test_wj_speaker_discourse_policy_preserves_candidate_queue() -> None:
    data = validator.validate_wj_speaker_discourse_policy()
    candidates = {item["target_id"]: item for item in data["candidate_target_queue"]}

    assert candidates["matt5_7_sermon_on_mount_wj_discourse"]["status"] == "pending_after_john3"
    assert candidates["john13_17_wj_farewell_discourse_marker_focus"]["status"] == "needs_review_packet_after_policy"
    assert candidates["matt24_25_olivet_discourse"]["status"] == "needs_review_packet_after_policy"
    assert candidates["john7_53_8_11_wj_variant_speech"]["status"] == "variant_policy_first"
    assert candidates["revelation_wj_voice_shifts"]["status"] == "revelation_research_first"
    assert all(candidate["implementation_allowed"] is False for candidate in candidates.values())


def test_wj_speaker_discourse_policy_rejects_authorizing_speaker_boundary(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_wj_speaker_discourse_policy())
    data["authority"]["authorizes_speaker_boundary"] = True
    candidate = tmp_path / "policy.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.WJSpeakerPolicyError, match="authorizes_speaker_boundary"):
        validator.validate_wj_speaker_discourse_policy(candidate)


def test_wj_speaker_discourse_policy_rejects_target_output_change(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_wj_speaker_discourse_policy())
    data["selected_first_review_target"]["output_change_authorized"] = True
    candidate = tmp_path / "policy.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.WJSpeakerPolicyError, match="output_change_authorized"):
        validator.validate_wj_speaker_discourse_policy(candidate)
