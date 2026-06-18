from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_narrative_legal_covenant_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "narrative_legal_covenant_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "narrative_legal_covenant_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_narrative_legal_covenant_dossier_queue_validates_current_repo() -> None:
    data = validator.validate_narrative_legal_covenant_dossier_queue()

    assert data["object_type"] == "narrative_legal_covenant_dossier_queue"
    assert set(data["scope"]["lanes"]) >= {"narrative_pericope", "legal_covenant_formulae"}
    assert data["authority"]["authorizes_covenant_theology"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["authority"]["authorizes_output_change"] is False


def test_queue_records_required_narrative_legal_dossiers() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "Gen.1-Gen.11" in dossiers["GEN1_11_PRIMEVAL_NARRATIVE_GENEALOGY"]["exact_passage_scope"]
    assert "Exod.19-Exod.24" in dossiers["EXOD19_24_SINAI_COVENANT_NARRATIVE_LAW"]["exact_passage_scope"]
    assert "Lev.1-Lev.7" in dossiers["LEV1_7_SACRIFICE_RITUAL_LAW"]["exact_passage_scope"]
    assert "Josh.13-Josh.21" in dossiers["JOSH13_21_LAND_ALLOTMENT_LISTS"]["exact_passage_scope"]
    assert "Matt.1-Matt.2" in dossiers["MATT_LUKE_GENEALOGY_BIRTH_NARRATIVE"]["exact_passage_scope"]


def test_queue_preserves_review_options_without_selecting_covenant_systems() -> None:
    data = load_queue()
    policy = data["preservation_policy"]

    assert validator.REQUIRED_REVIEW_OPTIONS <= set(policy["preserved_review_options"])
    assert "covenant theology system" in policy["not_selected_by_queue"]
    assert "law/gospel framework" in policy["not_selected_by_queue"]
    assert "typological fulfillment boundary" in policy["not_selected_by_queue"]
    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]


def test_queue_rejects_authorizing_covenant_theology(tmp_path: Path) -> None:
    data = load_queue()
    data["authority"]["authorizes_covenant_theology"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.NarrativeLegalCovenantQueueError, match="authorizes_covenant_theology must be false"):
        validator.validate_narrative_legal_covenant_dossier_queue(candidate)


def test_queue_rejects_missing_sinai_dossier(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"] = [
        dossier for dossier in data["dossier_queue"]
        if dossier["dossier_id"] != "EXOD19_24_SINAI_COVENANT_NARRATIVE_LAW"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.NarrativeLegalCovenantQueueError, match="missing dossiers"):
        validator.validate_narrative_legal_covenant_dossier_queue(candidate)


def test_queue_rejects_dossier_without_chunk_boundary_non_authorization(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"][0]["non_authorizations"].remove("chunk_boundary")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.NarrativeLegalCovenantQueueError, match="chunk_boundary"):
        validator.validate_narrative_legal_covenant_dossier_queue(candidate)
