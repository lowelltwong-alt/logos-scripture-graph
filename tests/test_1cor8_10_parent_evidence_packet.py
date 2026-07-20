from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_1cor8_10_parent_evidence_packet as validator

pytestmark = pytest.mark.generated_data(
    "data/canonical/translations/eng-web/translation_witnesses.jsonl"
)


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_1cor8_10_parent_evidence_packet_validates_current_repo() -> None:
    data = validator.validate_1cor8_10_parent_evidence_packet()

    assert data["object_type"] == "parent_only_review_evidence_packet"
    assert data["trust_zone"] == "canonical"
    assert data["scope"]["selected_option"] == "1COR8-10-T369-B"
    assert data["scope"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["scope"]["selected_children"] == []
    assert data["scope"]["review_status"] == "ready_for_owner_promotion_review"
    assert data["scope"]["reviewed_gold_promoted"] is False
    assert data["authority"]["records_parent_only_evidence"] is True
    assert data["authority"]["authorizes_output_change"] is False


def test_1cor8_10_parent_evidence_packet_preserves_metadata_as_evidence_only() -> None:
    data = validator.validate_1cor8_10_parent_evidence_packet()
    metadata = data["source_metadata_evidence"]

    assert metadata["strong_style_authority_limit"] == "strong_style_numbers_are_metadata_not_lexical_or_theological_truth"
    assert (
        metadata["capitalization_authority_limit"]
        == "capitalization_is_translation_evidence_not_divine_identity_or_chunk_authority"
    )
    assert "cross_reference_as_graph_edge" in data["non_authorizations"]
    assert "strong_number_as_lexical_truth" in data["non_authorizations"]
    assert "capitalization_as_divine_identity" in data["non_authorizations"]


def test_1cor8_10_parent_evidence_packet_requires_conflict_stop_rule() -> None:
    data = validator.validate_1cor8_10_parent_evidence_packet()
    conflict = data["conflict_scan"]

    assert conflict["result"] == "no_conflict_detected_for_parent_only_evidence_prep"
    assert "JOHN3-T356-B" in conflict["prior_decisions_considered"]
    assert "REV-T344-E" in conflict["prior_decisions_considered"]
    assert "stop and surface the conflict" in conflict["stop_rule"]


def test_1cor8_10_parent_evidence_packet_rejects_reviewed_gold_promotion(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_1cor8_10_parent_evidence_packet())
    data["scope"]["reviewed_gold_promoted"] = True
    candidate = tmp_path / "packet.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.ParentEvidenceError, match="reviewed_gold_promoted"):
        validator.validate_1cor8_10_parent_evidence_packet(candidate)


def test_1cor8_10_parent_evidence_packet_rejects_missing_conflict_stop(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_1cor8_10_parent_evidence_packet())
    data["conflict_scan"]["stop_rule"] = "continue"
    candidate = tmp_path / "packet.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.ParentEvidenceError, match="conflict stop rule"):
        validator.validate_1cor8_10_parent_evidence_packet(candidate)
