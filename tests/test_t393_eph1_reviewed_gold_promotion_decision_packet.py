from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_t393_eph1_reviewed_gold_promotion_decision_packet import (
    PACKET,
    T393PacketError,
    validate_t393_owner_decision_packet,
)


def test_t393_owner_decision_packet_validates() -> None:
    data = validate_t393_owner_decision_packet(PACKET)

    assert data["task_id"] == "T393"
    assert data["status"] == "resolved_by_t393_a"
    assert data["owner_selection"]["owner_selection_status"] == "selected"
    assert data["owner_selection"]["selected_option"] == "T393-A"
    assert data["owner_selection"]["owner_response_record"] == ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml"
    assert data["owner_selection"]["reviewed_gold_promoted"] is False


def test_t393_presents_options_and_recommendation_without_selection() -> None:
    data = validate_t393_owner_decision_packet(PACKET)
    options = {option["option_id"]: option for option in data["owner_options"]}

    assert set(options) == {"T393-A", "T393-B", "T393-C", "T393-D", "T393-E"}
    assert options["T393-A"]["if_selected_authorizes_parent_only_reviewed_gold"] is True
    assert options["T393-A"]["if_selected_authorizes_child_spans"] is False
    assert options["T393-A"]["if_selected_authorizes_output_change"] is False
    assert data["recommendation_for_owner_review"]["recommended_option_id"] == "T393-A"
    assert "not an owner decision" in data["recommendation_for_owner_review"]["why_not_auto_select"]
    assert data["owner_response"]["task_id"] == "T394"
    assert data["owner_response"]["selected_option"] == "T393-A"


def test_t393_records_variant_child_span_and_premortem_controls() -> None:
    data = validate_t393_owner_decision_packet(PACKET)
    evidence = data["packet_evidence_summary"]

    assert evidence["exact_internal_variant_refs"] == []
    assert evidence["variant_dependency_non_authorizing_assessment"] == "current_repo_variant_non_dependent_for_parent_boundary_and_reviewed_gold_claim"
    assert evidence["child_span_necessity_non_authorizing_assessment"] == "child_spans_not_necessary_for_parent_only_reviewed_gold_now"
    assert data["owner_response"]["exact_internal_variant_refs"] == []
    assert data["owner_response"]["child_span_necessity_or_denial"] == "child_spans_not_necessary_now_and_not_authorized"
    assert len(data["premortem_red_team"]) >= 5


def test_t393_validator_rejects_reviewed_gold_authority(tmp_path: Path) -> None:
    candidate = tmp_path / "t393.yaml"
    text = PACKET.read_text(encoding="utf-8").replace(
        "authorizes_reviewed_gold_promotion: false",
        "authorizes_reviewed_gold_promotion: true",
        1,
    )
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(T393PacketError, match="authorizes_reviewed_gold_promotion"):
        validate_t393_owner_decision_packet(candidate)
