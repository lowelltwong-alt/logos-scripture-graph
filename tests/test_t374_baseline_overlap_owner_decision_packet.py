from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t374_baseline_overlap_owner_decision_packet as validator


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t374_baseline_overlap_packet_validates_current_repo() -> None:
    data = validator.validate_t374_baseline_overlap_owner_decision_packet()

    assert data["object_type"] == "t374_baseline_overlap_owner_decision_packet"
    assert data["task_id"] == "T374"
    assert data["status"] == "blocked_pending_owner_decision"
    assert data["target"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["target"]["selected_children"] == []
    assert data["finding"]["replacement_style_implementation_paused"] is True
    assert data["finding"]["replacement_safe_without_new_owner_decision"] is False
    assert data["authority"]["authorizes_chunk_output_change"] is False


def test_t374_packet_records_exact_overlap_window_and_spills() -> None:
    data = validator.validate_t374_baseline_overlap_owner_decision_packet()
    observed = [(item["osis_start"], item["osis_end"]) for item in data["baseline_inspection"]["observed_window"]]

    assert observed == validator.EXPECTED_OBSERVED_WINDOW
    assert "1Cor.7.25-1Cor.7.40" in data["finding"]["reason"]
    assert "1Cor.11.1-1Cor.11.10" in data["finding"]["reason"]


def test_t374_packet_presents_all_owner_options_without_selection() -> None:
    data = validator.validate_t374_baseline_overlap_owner_decision_packet()
    option_ids = {item["option_id"] for item in data["owner_options"]}

    assert option_ids == validator.EXPECTED_OPTIONS
    assert data["recommendation"]["recommended_if_owner_wants_output"] == "T374-OVERLAP-B"
    assert data["recommendation"]["conservative_recommendation_if_any_doubt"] == "T374-OVERLAP-A"
    assert data["recommendation"]["recommendation_is_owner_selection"] is False
    assert data["required_owner_selection_record"]["selected_option"] == "pending_owner_selection"


def test_t374_packet_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t374_baseline_overlap_owner_decision_packet())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "t374.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T374BaselineOverlapError, match="authorizes_chunk_output_change"):
        validator.validate_t374_baseline_overlap_owner_decision_packet(candidate)


def test_t374_packet_rejects_missing_additive_overlay_option(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t374_baseline_overlap_owner_decision_packet())
    data["owner_options"] = [item for item in data["owner_options"] if item["option_id"] != "T374-OVERLAP-B"]
    candidate = tmp_path / "t374.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T374BaselineOverlapError, match="owner_options"):
        validator.validate_t374_baseline_overlap_owner_decision_packet(candidate)
