from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_textual_variant_source_tradition_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "textual_variant_source_tradition_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "textual_variant_source_tradition_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_textual_variant_source_tradition_dossier_queue_validates_current_repo() -> None:
    data = validator.validate_textual_variant_source_tradition_dossier_queue()

    assert data["object_type"] == "textual_variant_source_tradition_dossier_queue"
    assert set(data["scope"]["lanes"]) >= {"textual_variant_source_tradition"}
    assert data["authority"]["authorizes_textual_critical_decision"] is False
    assert data["authority"]["authorizes_canon_scope_change"] is False
    assert data["authority"]["authorizes_boundary_import"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False


def test_queue_records_required_variant_source_dossiers() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "Mark.16.9-Mark.16.20" in dossiers["MARK16_LONGER_ENDING"]["exact_passage_scope"]
    assert "John.7.53-John.8.11" in dossiers["JOHN7_53_8_11_PERICOPE_ADULTERAE"]["exact_passage_scope"]
    assert "Deut.32.8-Deut.32.9" in dossiers["DEUT32_8_9_SONS_OF_GOD_VARIANT"]["exact_passage_scope"]
    assert "1John.5.6-1John.5.8" in dossiers["ONEJOHN5_7_COMMA_JOHANNEUM"]["exact_passage_scope"]


def test_queue_preserves_options_without_selecting_textual_or_canon_policy() -> None:
    data = load_queue()
    policy = data["preservation_policy"]

    assert validator.REQUIRED_REVIEW_OPTIONS <= set(policy["preserved_review_options"])
    assert "textual-critical preferred reading" in policy["not_selected_by_queue"]
    assert "canon-scope expansion or contraction" in policy["not_selected_by_queue"]
    assert "Daniel or Esther additions import" in policy["not_selected_by_queue"]
    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]


def test_queue_rejects_authorizing_textual_decision(tmp_path: Path) -> None:
    data = load_queue()
    data["authority"]["authorizes_textual_critical_decision"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualVariantSourceTraditionQueueError, match="authorizes_textual_critical_decision must be false"):
        validator.validate_textual_variant_source_tradition_dossier_queue(candidate)


def test_queue_rejects_missing_mark_longer_ending_dossier(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"] = [
        dossier for dossier in data["dossier_queue"]
        if dossier["dossier_id"] != "MARK16_LONGER_ENDING"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualVariantSourceTraditionQueueError, match="missing dossiers"):
        validator.validate_textual_variant_source_tradition_dossier_queue(candidate)


def test_queue_rejects_dossier_without_boundary_import_non_authorization(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"][0]["non_authorizations"].remove("boundary_import")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualVariantSourceTraditionQueueError, match="boundary_import"):
        validator.validate_textual_variant_source_tradition_dossier_queue(candidate)
