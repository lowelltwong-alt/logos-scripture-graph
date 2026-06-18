from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_apocalyptic_prophetic_intertext_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "apocalyptic_prophetic_intertext_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "apocalyptic_prophetic_intertext_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_apocalyptic_prophetic_intertext_dossier_queue_validates_current_repo() -> None:
    data = validator.validate_apocalyptic_prophetic_intertext_dossier_queue()

    assert data["object_type"] == "apocalyptic_prophetic_intertext_dossier_queue"
    assert data["scope"]["corpus_scope"] == "canonical_66"
    assert data["authority"]["authorizes_intertext_truth"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False


def test_queue_preserves_orthodox_hermeneutic_options_without_selecting_one() -> None:
    data = load_queue()
    policy = data["hermeneutic_preservation_policy"]

    assert validator.REQUIRED_HERMENEUTIC_OPTIONS <= set(policy["preserved_orthodox_options"])
    assert "Revelation chronology" in policy["not_selected_by_queue"]
    assert "millennium view" in policy["not_selected_by_queue"]
    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]


def test_queue_records_required_dossiers_and_priority_cases() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "Dan.7.13-Dan.7.14" in dossiers["REV_DAN_SON_OF_MAN"]["candidate_intertexts"]
    assert "Ps.2.9" in dossiers["REV_PS2_ROD_OF_IRON"]["candidate_intertexts"]
    assert "Dan.9.27" in dossiers["OLIVET_DANIEL_ABOMINATION"]["candidate_intertexts"]
    assert "Ezek.40-Ezek.48" in dossiers["EZEKIEL_TEMPLE_CITY_REVELATION_NEW_CREATION"]["candidate_intertexts"]
    assert "Zech.12.10" in dossiers["ZECHARIAH_PIERCED_MOURNING_AND_REVELATION"]["candidate_intertexts"]


def test_queue_records_source_metadata_limits_from_current_sidecar() -> None:
    data = validator.validate_apocalyptic_prophetic_intertext_dossier_queue()
    limits = data["observed_source_metadata_limits"]

    assert limits["canonical_cross_reference_records"] == 340
    assert limits["revelation_origin_cross_reference_records"] == 5
    assert limits["daniel_origin_cross_reference_records"] == 0
    assert "absence of a source cross-reference is not absence" in limits["warning"]


def test_queue_rejects_authorizing_intertext_truth(tmp_path: Path) -> None:
    data = load_queue()
    data["authority"]["authorizes_intertext_truth"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.ApocalypticIntertextQueueError, match="authorizes_intertext_truth must be false"):
        validator.validate_apocalyptic_prophetic_intertext_dossier_queue(candidate)


def test_queue_rejects_missing_hermeneutic_option(tmp_path: Path) -> None:
    data = load_queue()
    data["hermeneutic_preservation_policy"]["preserved_orthodox_options"].remove("preterist")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.ApocalypticIntertextQueueError, match="preserved_orthodox_options"):
        validator.validate_apocalyptic_prophetic_intertext_dossier_queue(candidate)


def test_queue_rejects_dossier_without_output_non_authorization(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"][0]["non_authorizations"].remove("output_change")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.ApocalypticIntertextQueueError, match="output_change"):
        validator.validate_apocalyptic_prophetic_intertext_dossier_queue(candidate)
