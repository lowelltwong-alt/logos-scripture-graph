from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_orthodox_original_language_pressure_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "orthodox_original_language_pressure_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "orthodox_original_language_pressure_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_orthodox_original_language_pressure_queue_validates_current_repo() -> None:
    data = validator.validate_orthodox_original_language_pressure_dossier_queue()

    assert data["object_type"] == "orthodox_original_language_pressure_dossier_queue"
    assert data["trust_zone"] == "canonical"
    assert data["authority"]["records_original_language_pressure_queue"] is True
    assert data["authority"]["authorizes_nonorthodox_source_authority"] is False
    assert data["authority"]["authorizes_extra_canonical_source_authority"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["authority"]["authorizes_output_change"] is False


def test_queue_records_required_pressure_dossiers() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "John.1.1-John.1.18" in dossiers["JOHN1_1_LOGOS_THEOS_GRAMMAR"]["exact_passage_scope"]
    assert "Col.1.15-Col.1.20" in dossiers["COL1_15_20_FIRSTBORN_ALL_THINGS"]["exact_passage_scope"]
    assert "Gen.1.26-Gen.1.27" in dossiers["GEN1_26_ELOHIM_US_IMAGE"]["exact_passage_scope"]
    assert "Isa.44.6-Isa.44.8" in dossiers["ISA43_44_ONE_GOD_LDS_POLYTHEISM"]["exact_passage_scope"]
    assert "1Cor.15.12-1Cor.15.34" in dossiers["ONECOR15_29_BAPTISM_FOR_DEAD"]["exact_passage_scope"]


def test_queue_preserves_orthodox_boundary_without_selecting_pressure_authority() -> None:
    data = load_queue()
    policy = data["preservation_policy"]

    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]
    assert "LDS extra-canonical authority" in policy["orthodox_boundary"]
    assert "Watch Tower/New World Translation authority" in policy["orthodox_boundary"]
    assert "Watch Tower/New World Translation authority" in policy["not_selected_by_queue"]
    assert "LDS extra-canonical authority" in policy["not_selected_by_queue"]
    assert "automatic proof-text conclusion from one lemma or grammar label" in policy["not_selected_by_queue"]


def test_queue_rejects_nonorthodox_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(load_queue())
    data["authority"]["authorizes_nonorthodox_source_authority"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.OrthodoxLanguagePressureQueueError, match="authorizes_nonorthodox_source_authority"):
        validator.validate_orthodox_original_language_pressure_dossier_queue(candidate)


def test_queue_rejects_missing_john1_pressure_dossier(tmp_path: Path) -> None:
    data = copy.deepcopy(load_queue())
    data["dossier_queue"] = [
        dossier for dossier in data["dossier_queue"]
        if dossier["dossier_id"] != "JOHN1_1_LOGOS_THEOS_GRAMMAR"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.OrthodoxLanguagePressureQueueError, match="missing dossiers"):
        validator.validate_orthodox_original_language_pressure_dossier_queue(candidate)


def test_queue_rejects_dossier_without_graph_denial(tmp_path: Path) -> None:
    data = copy.deepcopy(load_queue())
    data["dossier_queue"][0]["non_authorizations"].remove("graph_edge")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.OrthodoxLanguagePressureQueueError, match="graph_edge"):
        validator.validate_orthodox_original_language_pressure_dossier_queue(candidate)
