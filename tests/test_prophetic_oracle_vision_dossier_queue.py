from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_prophetic_oracle_vision_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "prophetic_oracle_vision_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "prophetic_oracle_vision_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_prophetic_oracle_vision_dossier_queue_validates_current_repo() -> None:
    data = validator.validate_prophetic_oracle_vision_dossier_queue()

    assert data["object_type"] == "prophetic_oracle_vision_dossier_queue"
    assert set(data["scope"]["lanes"]) >= {"prophetic_oracle", "prophetic_oracle_vision"}
    assert data["authority"]["authorizes_fulfillment_theology"] is False
    assert data["authority"]["authorizes_temple_theology"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False


def test_queue_records_required_prophetic_dossiers() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "Isa.52.13-Isa.53.12" in dossiers["ISA40_55_SERVANT_COMFORT_ORACLES"]["exact_passage_scope"]
    assert "Jer.31.31-Jer.31.34" in dossiers["JER30_33_RESTORATION_NEW_COVENANT"]["exact_passage_scope"]
    assert "Ezek.40-Ezek.48" in dossiers["EZEK40_48_TEMPLE_CITY_VISION"]["exact_passage_scope"]
    assert "Dan.7-Dan.12" in dossiers["DAN7_12_PROPHETIC_APOCALYPTIC_VISIONS"]["exact_passage_scope"]


def test_queue_preserves_options_without_selecting_prophetic_systems() -> None:
    data = load_queue()
    policy = data["preservation_policy"]

    assert validator.REQUIRED_REVIEW_OPTIONS <= set(policy["preserved_review_options"])
    assert "fulfillment theology system" in policy["not_selected_by_queue"]
    assert "millennial temple view" in policy["not_selected_by_queue"]
    assert "servant-song referent system" in policy["not_selected_by_queue"]
    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]


def test_queue_rejects_authorizing_fulfillment_theology(tmp_path: Path) -> None:
    data = load_queue()
    data["authority"]["authorizes_fulfillment_theology"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.PropheticOracleVisionQueueError, match="authorizes_fulfillment_theology must be false"):
        validator.validate_prophetic_oracle_vision_dossier_queue(candidate)


def test_queue_rejects_missing_ezekiel_temple_dossier(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"] = [
        dossier for dossier in data["dossier_queue"]
        if dossier["dossier_id"] != "EZEK40_48_TEMPLE_CITY_VISION"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.PropheticOracleVisionQueueError, match="missing dossiers"):
        validator.validate_prophetic_oracle_vision_dossier_queue(candidate)


def test_queue_rejects_dossier_without_graph_non_authorization(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"][0]["non_authorizations"].remove("graph_edge")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.PropheticOracleVisionQueueError, match="graph_edge"):
        validator.validate_prophetic_oracle_vision_dossier_queue(candidate)
