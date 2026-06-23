from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t385_owner_decision_packet as validator


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / ".ai" / "control" / "t385_owner_decision_packet.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t385_owner_decision_packet_validates_current_repo() -> None:
    data = validator.validate_t385_owner_decision_packet(PACKET)

    assert data["object_type"] == "chunking_owner_decision_packet"
    assert data["task_id"] == "T385"
    assert data["status"] == "pending_owner_decision"
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_graph_edges"] is False
    assert data["owner_selection"]["owner_selection_status"] == "pending"
    assert data["owner_selection"]["exact_target_selected"] is False
    assert data["decision_register_entry"] == "CD-066"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-020"


def test_t385_presents_all_serious_options_and_recommends_ephesians_without_selecting() -> None:
    data = validator.validate_t385_owner_decision_packet(PACKET)

    options = {option["option_id"]: option for option in data["serious_faithful_options"]}
    assert validator.REQUIRED_OPTION_IDS <= set(options)
    assert options["T385-A"]["passage"] == "Eph.1.3-Eph.1.14"
    assert options["T385-A"]["recommendation_status"] == "recommended_next_owner_choice"
    assert options["T385-G"]["passage"] == "John.3.1-John.3.36"
    assert options["T385-H"]["lane"] == "revelation_apocalyptic"
    assert data["recommendation"]["recommended_option_id"] == "T385-A"
    assert data["recommendation"]["recommended_passage"] == "Eph.1.3-Eph.1.14"
    assert "not an owner decision" in data["recommendation"]["why_this_is_not_selection"]
    assert data["owner_selection"]["selected_option"] is None


def test_t385_blocks_goal4_until_owner_selection() -> None:
    data = validator.validate_t385_owner_decision_packet(PACKET)

    assert data["next_goal_gate"]["goal_4_can_run_after"] == "explicit_owner_selection_of_one_T385_option"
    assert "explicitly selects" in data["next_goal_gate"]["if_no_owner_selection"]
    assert "recommendation_as_owner_selection" in data["non_authorizations"]
    assert "review_packet_strengthening_without_owner_selection" in data["non_authorizations"]


def test_t385_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t385_owner_decision_packet(PACKET))
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "packet.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T385PacketError, match="authorizes_chunk_output_change"):
        validator.validate_t385_owner_decision_packet(candidate)


def test_t385_rejects_missing_option(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t385_owner_decision_packet(PACKET))
    data["serious_faithful_options"] = [
        option for option in data["serious_faithful_options"] if option["option_id"] != "T385-H"
    ]
    candidate = tmp_path / "packet.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T385PacketError, match="T385-H"):
        validator.validate_t385_owner_decision_packet(candidate)
