from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_t442_production_candidate_root_decision_packet import (
    PACKET,
    T442ValidationError,
    validate_t442_packet,
)


def test_t442_packet_validates_current_repo() -> None:
    data = validate_t442_packet(PACKET)

    assert data["task_id"] == "T442"
    assert data["status"] == "pending_owner_decision"
    assert data["owner_selection"]["owner_selection_status"] == "pending"
    assert data["owner_selection"]["opens_production_candidate_roots"] is False
    assert data["recommended_option_id"] == "T442-A"


def test_t442_options_are_non_implementing() -> None:
    data = validate_t442_packet(PACKET)
    options = {option["option_id"]: option for option in data["owner_options"]}

    assert set(options) == {"T442-A", "T442-B", "T442-C", "T442-D"}
    assert options["T442-A"]["requires_future_rust_admission_checker"] is True
    for option in options.values():
        assert option["if_selected_authorizes_immediate_root_creation"] is False
        assert option["if_selected_authorizes_row_population_now"] is False


def test_t442_rejects_root_opening_authority(tmp_path: Path) -> None:
    candidate = tmp_path / "t442.yaml"
    text = PACKET.read_text(encoding="utf-8").replace(
        "opens_production_candidate_roots: false",
        "opens_production_candidate_roots: true",
        1,
    )
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(T442ValidationError, match="opens_production_candidate_roots"):
        validate_t442_packet(candidate)


def test_t442_rejects_recommendation_as_selection(tmp_path: Path) -> None:
    candidate = tmp_path / "t442.yaml"
    text = PACKET.read_text(encoding="utf-8").replace(
        "owner_selection_status: pending",
        "owner_selection_status: selected",
        1,
    )
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(T442ValidationError, match="owner_selection_status"):
        validate_t442_packet(candidate)


def test_t442_keeps_rust_as_future_admission_checker() -> None:
    data = validate_t442_packet(PACKET)
    future = data["future_rust_slice_if_t442_a_selected"]

    assert future["task_shape"] == "production_candidate_root_admission_checker"
    assert "duplicate ID rejection" in future["responsibilities"]
    assert "theology and translation-faithfulness non-authority" in future["python_retained_authority"]
