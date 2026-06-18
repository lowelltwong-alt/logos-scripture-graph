from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_bible_wide_chunking_research_registry as validator


def test_bible_wide_chunking_research_registry_validates_current_repo() -> None:
    data = validator.validate_research_registry()

    assert data["object_type"] == "bible_wide_chunking_research_registry"
    assert data["scope"]["corpus_scope"] == "canonical_66"
    assert data["scope"]["book_count"] == 66
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_graph_edges"] is False


def test_research_registry_covers_all_66_books_in_order() -> None:
    data = validator.validate_research_registry()
    queue = data["book_research_queue"]

    assert [entry["book_id"] for entry in queue] == validator.CANONICAL_66
    assert [entry["canonical_order"] for entry in queue] == list(range(1, 67))
    assert queue[0]["book_id"] == "Gen"
    assert queue[-1]["book_id"] == "Rev"


def test_research_registry_records_sensitive_research_watchpoints() -> None:
    data = validator.validate_research_registry()
    by_book = {entry["book_id"]: entry for entry in data["book_research_queue"]}

    assert by_book["John"]["research_status"] == "owner_decision_pending"
    assert "wj_markers" in by_book["John"]["metadata_watchpoints"]
    assert "John.3" in by_book["John"]["future_review_packet_candidates"]
    assert by_book["Rev"]["research_status"] == "research_first"
    assert "Rev.12.1-Rev.14.20" in by_book["Rev"]["future_review_packet_candidates"]
    assert "source_metadata_features" in {
        dimension["dimension_id"] for dimension in data["research_dimensions"]
    }
    source_metadata = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "source_metadata_features"
    )
    discourse = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "discourse_argument_flow"
    )
    narrative = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "narrative_scene_pericope"
    )
    legal = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "legal_covenant_formulae"
    )
    poetry = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "poetry_parallelism_stanza"
    )
    assert source_metadata["companion_atlas"] == ".ai/control/source_metadata_research_atlas.yaml"
    assert discourse["companion_dossier_queue"] == ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml"
    assert narrative["companion_dossier_queue"] == ".ai/control/narrative_legal_covenant_dossier_queue.yaml"
    assert legal["companion_dossier_queue"] == ".ai/control/narrative_legal_covenant_dossier_queue.yaml"
    assert poetry["companion_dossier_queue"] == ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml"
    apocalyptic = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "apocalyptic_symbol_intertext"
    )
    prophetic = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "prophetic_oracle_vision"
    )
    assert apocalyptic["companion_dossier_queue"] == ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml"
    assert prophetic["companion_dossier_queue"] == ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml"
    assert prophetic["companion_oracle_dossier_queue"] == ".ai/control/prophetic_oracle_vision_dossier_queue.yaml"
    gospel_wj = next(
        dimension for dimension in data["research_dimensions"]
        if dimension["dimension_id"] == "gospel_discourse_speaker_wj"
    )
    assert gospel_wj["companion_dossier_queue"] == ".ai/control/gospel_wj_discourse_dossier_queue.yaml"
    assert "divine_name_title_capitalization" in {
        dimension["dimension_id"] for dimension in data["research_dimensions"]
    }


def test_research_registry_rejects_missing_book(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_research_registry())
    data["book_research_queue"] = [
        entry for entry in data["book_research_queue"] if entry["book_id"] != "Jude"
    ]
    candidate = tmp_path / "registry.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.ResearchRegistryError, match="66 books"):
        validator.validate_research_registry(candidate)


def test_research_registry_rejects_authorizing_output_change(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_research_registry())
    data["book_research_queue"][0]["output_change_authorized"] = True
    candidate = tmp_path / "registry.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.ResearchRegistryError, match="output_change_authorized"):
        validator.validate_research_registry(candidate)
