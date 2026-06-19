from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t371_variant_dependency_owner_decision_packet as validator


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / ".ai" / "control" / "t371_variant_dependency_owner_decision_packet.yaml"


def load_packet() -> dict:
    text = PACKET.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "t371_variant_dependency_owner_decision_packet.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_t371_variant_dependency_packet_validates_current_repo() -> None:
    data = validator.validate_t371_variant_dependency_owner_decision_packet()

    assert data["object_type"] == "variant_dependency_owner_decision_packet"
    assert data["prepared_by_task"] == "T380"
    assert data["target_owner_task"] == "T371"
    assert data["status"] == "pending_owner_decision"
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_variant_non_dependency_finding"] is False
    assert data["authority"]["authorizes_chunk_output_change"] is False


def test_packet_names_exact_variant_refs_and_owner_response_fields() -> None:
    data = load_packet()
    refs = {item["ref"] for item in data["variant_dependency_review"]}

    assert refs == {"1Cor.9.20", "1Cor.10.9"}
    required = set(data["owner_question"]["owner_response_must_record"])
    assert validator.REQUIRED_OWNER_RESPONSE_FIELDS <= required
    assert "boundary_dependency_or_non_dependency" in required
    assert "reviewed_gold_dependency_or_non_dependency" in required
    assert "decision_register_update" in required


def test_packet_keeps_t371_a_conditional_not_selected() -> None:
    data = load_packet()
    options = {item["option_id"]: item for item in data["owner_options"]}

    assert data["recommendation_for_owner_review"]["recommended_if_owner_agrees_with_variant_non_dependency"] == "T371-A"
    assert data["recommendation_for_owner_review"]["conservative_hold_if_any_doubt"] == "T371-B"
    assert options["T371-A"]["if_selected_authorizes_parent_only_reviewed_gold"] is True
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["owner_question"]["must_stop_if_owner_response_is_ambiguous"] is True


def test_packet_rejects_promotion_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(load_packet())
    data["authority"]["authorizes_reviewed_gold_promotion"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.T371PacketError, match="authorizes_reviewed_gold_promotion"):
        validator.validate_t371_variant_dependency_owner_decision_packet(candidate)


def test_packet_rejects_missing_variant_ref(tmp_path: Path) -> None:
    data = copy.deepcopy(load_packet())
    data["variant_dependency_review"] = [
        item for item in data["variant_dependency_review"] if item["ref"] != "1Cor.10.9"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.T371PacketError, match="exact variant refs"):
        validator.validate_t371_variant_dependency_owner_decision_packet(candidate)


def test_packet_rejects_output_authorizing_option(tmp_path: Path) -> None:
    data = copy.deepcopy(load_packet())
    data["owner_options"][0]["if_selected_authorizes_output_change"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.T371PacketError, match="output change"):
        validator.validate_t371_variant_dependency_owner_decision_packet(candidate)
