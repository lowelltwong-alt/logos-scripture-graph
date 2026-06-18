from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_gospel_wj_discourse_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "gospel_wj_discourse_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "gospel_wj_discourse_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_gospel_wj_discourse_dossier_queue_validates_current_repo() -> None:
    data = validator.validate_gospel_wj_discourse_dossier_queue()

    assert data["object_type"] == "gospel_wj_discourse_dossier_queue"
    assert data["scope"]["lane"] == "gospel_discourse_wj"
    assert data["authority"]["authorizes_jesus_speaker_attribution"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["authority"]["authorizes_output_change"] is False


def test_queue_records_wj_inventory_counts_and_non_gospel_books() -> None:
    data = validator.validate_gospel_wj_discourse_dossier_queue()
    metadata = data["observed_wj_metadata"]

    assert metadata["wj_word_tokens"] == 38094
    assert metadata["wj_token_runs"] == 675
    assert metadata["books_with_wj"] == ["Matt", "Mark", "Luke", "John", "Acts", "1Cor", "2Cor", "1Tim", "Rev"]
    assert metadata["books_outside_four_gospels_with_wj"] == ["Acts", "1Cor", "2Cor", "1Tim", "Rev"]
    assert "presence is not Jesus speaker authority" in metadata["warning"]


def test_queue_records_required_wj_dossiers() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "John.3.1-John.3.36" in dossiers["JOHN3_WJ_SPEAKER_BOUNDARY"]["exact_passage_scope"]
    assert "Matt.5.1-Matt.7.29" in dossiers["MATT5_7_SERMON_ON_MOUNT_WJ_DISCOURSE"]["exact_passage_scope"]
    assert "John.13-John.17" in dossiers["JOHN13_17_FAREWELL_DISCOURSE"]["exact_passage_scope"]
    assert "Matt.24-Matt.25" in dossiers["SYNOPTIC_OLIVET_WJ_APOCALYPTIC_DISCOURSE"]["exact_passage_scope"]
    assert "Rev.1-Rev.3" in dossiers["REVELATION_WJ_VOICE_SHIFTS"]["exact_passage_scope"]
    assert "Acts" in dossiers["ACTS_EPISTLE_WJ_DOMINICAL_QUOTES"]["exact_passage_scope"]


def test_queue_preserves_review_options_without_selecting_speaker_boundaries() -> None:
    data = load_queue()
    policy = data["wj_discourse_preservation_policy"]

    assert validator.REQUIRED_REVIEW_OPTIONS <= set(policy["preserved_review_options"])
    assert "John 3 Jesus/narrator boundary" in policy["not_selected_by_queue"]
    assert "Revelation voice identity" in policy["not_selected_by_queue"]
    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]


def test_queue_rejects_authorizing_jesus_speaker_attribution(tmp_path: Path) -> None:
    data = load_queue()
    data["authority"]["authorizes_jesus_speaker_attribution"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.GospelWJDossierQueueError, match="authorizes_jesus_speaker_attribution must be false"):
        validator.validate_gospel_wj_discourse_dossier_queue(candidate)


def test_queue_rejects_missing_john3_pending_packet(tmp_path: Path) -> None:
    data = load_queue()
    data["existing_packet_state"]["required_pending_packets"] = [
        packet for packet in data["existing_packet_state"]["required_pending_packets"]
        if packet["entry_id"] != "packet_john3_wj_speaker_boundary_review"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.GospelWJDossierQueueError, match="required_pending_packets"):
        validator.validate_gospel_wj_discourse_dossier_queue(candidate)


def test_queue_rejects_dossier_without_speaker_boundary_non_authorization(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"][0]["non_authorizations"].remove("speaker_boundary")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.GospelWJDossierQueueError, match="speaker_boundary"):
        validator.validate_gospel_wj_discourse_dossier_queue(candidate)
