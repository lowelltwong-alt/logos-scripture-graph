from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_wisdom_dialogue_poetry_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "wisdom_dialogue_poetry_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "wisdom_dialogue_poetry_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_wisdom_dialogue_poetry_dossier_queue_validates_current_repo() -> None:
    data = validator.validate_wisdom_dialogue_poetry_dossier_queue()

    assert data["object_type"] == "wisdom_dialogue_poetry_dossier_queue"
    assert set(data["scope"]["lanes"]) >= {"wisdom_dialogue", "poetry_parallelism_stanza"}
    assert data["authority"]["authorizes_wisdom_theology"] is False
    assert data["authority"]["authorizes_speaker_boundary"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False


def test_queue_records_required_wisdom_poetry_dossiers() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "Job.3-Job.42" in dossiers["JOB_DIALOGUE_CYCLES_AND_DIVINE_SPEECHES"]["exact_passage_scope"]
    assert "Song.1-Song.8" in dossiers["SONG_SPEAKER_BOUNDARY_AND_GENRE"]["exact_passage_scope"]
    assert "Lam.1-Lam.5" in dossiers["LAMENTATIONS_ACROSTIC_LAMENT_UNITS"]["exact_passage_scope"]
    assert "Ps.119" in dossiers["PS119_ACROSTIC_TORAH_PSALM"]["exact_passage_scope"]


def test_queue_preserves_review_options_without_selecting_systems() -> None:
    data = load_queue()
    policy = data["preservation_policy"]

    assert validator.REQUIRED_REVIEW_OPTIONS <= set(policy["preserved_review_options"])
    assert "Job theodicy system" in policy["not_selected_by_queue"]
    assert "Song speaker assignment" in policy["not_selected_by_queue"]
    assert "acrostic-as-boundary rule" in policy["not_selected_by_queue"]
    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]


def test_queue_rejects_authorizing_speaker_boundaries(tmp_path: Path) -> None:
    data = load_queue()
    data["authority"]["authorizes_speaker_boundary"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.WisdomDialoguePoetryQueueError, match="authorizes_speaker_boundary must be false"):
        validator.validate_wisdom_dialogue_poetry_dossier_queue(candidate)


def test_queue_rejects_missing_song_dossier(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"] = [
        dossier for dossier in data["dossier_queue"]
        if dossier["dossier_id"] != "SONG_SPEAKER_BOUNDARY_AND_GENRE"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.WisdomDialoguePoetryQueueError, match="missing dossiers"):
        validator.validate_wisdom_dialogue_poetry_dossier_queue(candidate)


def test_queue_rejects_dossier_without_chunk_boundary_non_authorization(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"][0]["non_authorizations"].remove("chunk_boundary")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.WisdomDialoguePoetryQueueError, match="chunk_boundary"):
        validator.validate_wisdom_dialogue_poetry_dossier_queue(candidate)
