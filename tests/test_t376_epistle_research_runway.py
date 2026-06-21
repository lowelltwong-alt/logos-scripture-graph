from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t376_epistle_research_runway as validator


ROOT = Path(__file__).resolve().parents[1]
RUNWAY = ROOT / ".ai" / "control" / "t376_epistle_research_runway.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t376_epistle_research_runway_validates_current_repo() -> None:
    data = validator.validate_t376_epistle_research_runway(RUNWAY)

    assert data["object_type"] == "epistle_argument_research_runway_selection"
    assert data["task_id"] == "T376"
    assert data["status"] == "complete_selected_research_first_epistle_argument_runway"
    assert data["selected_option"] == "T376-A"
    assert data["selected_lane"] == "epistle_argument"
    assert data["authority"]["authorizes_non_output_changing_research_prep"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_exact_target_selection"] is False
    assert data["next_route"]["task_id"] == "T384"
    assert data["decision_register_entry"] == "CD-060"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-012"


def test_t376_research_autonomy_boundary_stops_before_authority_changes() -> None:
    data = validator.validate_t376_epistle_research_runway(RUNWAY)
    boundary = data["research_autonomy_boundary"]

    assert "compile_epistle_argument_target_options" in boundary["may_continue_without_new_owner_decision"]
    assert "create_non_authorizing_research_dockets_or_review_packet_drafts" in boundary["may_continue_without_new_owner_decision"]
    assert "exact_epistle_target_selection_for_promotion_or_implementation" in boundary["must_stop_for_owner_decision_before"]
    assert "chunk_output_change" in boundary["must_stop_for_owner_decision_before"]
    assert "graph_edge_generation" in boundary["must_stop_for_owner_decision_before"]
    assert "denominational_systematic_theology_as_chunk_authority" in boundary["must_stop_for_owner_decision_before"]


def test_t376_lists_serious_target_options_without_selecting_one() -> None:
    data = validator.validate_t376_epistle_research_runway(RUNWAY)
    options = {option["option_id"]: option for option in data["target_options_to_research_before_owner_selection"]}

    assert set(options) >= validator.REQUIRED_TARGET_OPTIONS
    assert options["T384-A"]["passage"] == "Eph.1.3-Eph.1.14"
    assert options["T384-B"]["passage"] == "Rom.9.1-Rom.11.36"
    assert options["T384-C"]["passage"] == "Heb.7.1-Heb.10.39"
    assert options["T384-D"]["passage"] == "Gal.2.15-Gal.3.29"
    assert options["T384-E"]["passage"] == "Jas.2.14-Jas.2.26"
    assert options["T384-F"]["passage"] == "1Cor.11.17-1Cor.14.40"
    assert all(option["exact_target_selected"] is False for option in options.values())
    assert all(option["promotion_authorized"] is False for option in options.values())
    assert data["recommendation"]["likely_first_option_to_compare_later"] == "T384-A"
    assert "not an owner selection" in data["recommendation"]["why_not_selection"]


def test_t376_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t376_epistle_research_runway(RUNWAY))
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "runway.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T376RunwayError, match="authorizes_chunk_output_change"):
        validator.validate_t376_epistle_research_runway(candidate)


def test_t376_rejects_hidden_target_selection(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t376_epistle_research_runway(RUNWAY))
    data["target_options_to_research_before_owner_selection"][0]["exact_target_selected"] = True
    candidate = tmp_path / "runway.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T376RunwayError, match="exact_target_selected"):
        validator.validate_t376_epistle_research_runway(candidate)
