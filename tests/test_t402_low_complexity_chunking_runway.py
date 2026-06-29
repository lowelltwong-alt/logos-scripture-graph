from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t402_low_complexity_chunking_runway as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "whole_bible_low_complexity_chunking_candidate_queue.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t402_runway_validates_current_repo() -> None:
    data = validator.validate_t402_low_complexity_chunking_runway(QUEUE)

    assert data["object_type"] == "whole_bible_low_complexity_chunking_candidate_queue"
    assert data["task_id"] == "T402"
    assert data["status"] == "complete_review_research_only_candidate_runway"
    assert data["decision_register_entry"] == "CD-077"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-031"


def test_t402_queue_covers_all_66_books_and_expected_statuses() -> None:
    data = validator.validate_t402_low_complexity_chunking_runway(QUEUE)

    books = [entry["book"] for entry in data["candidate_queue"]]
    assert books == validator.CANONICAL_BOOKS
    assert data["summary_counts"]["canonical_book_count"] == 66
    assert data["summary_counts"]["candidate_count"] == 66
    for key, value in validator.EXPECTED_STATUS_COUNTS.items():
        assert data["summary_counts"][key] == value


def test_t402_queue_keeps_all_authority_flags_closed() -> None:
    data = validator.validate_t402_low_complexity_chunking_runway(QUEUE)

    for key in validator.REQUIRED_FALSE_AUTHORITY:
        assert data["authority"][key] is False
    assert set(data["common_non_authorizations"]) >= validator.REQUIRED_NON_AUTHORIZATIONS
    for candidate in data["candidate_queue"]:
        assert set(candidate["non_authorizations"]) >= validator.REQUIRED_NON_AUTHORIZATIONS
        assert candidate["child_span_policy"] == "parent_only_assumed_no_children_authorized"


def test_t402_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t402_low_complexity_chunking_runway(QUEUE))
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "t402.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T402RunwayError, match="authorizes_chunk_output_change"):
        validator.validate_t402_low_complexity_chunking_runway(candidate)


def test_t402_rejects_missing_canonical_book(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t402_low_complexity_chunking_runway(QUEUE))
    data["candidate_queue"] = data["candidate_queue"][:-1]
    data["summary_counts"]["candidate_count"] = 65
    candidate = tmp_path / "t402.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T402RunwayError, match="66 candidates"):
        validator.validate_t402_low_complexity_chunking_runway(candidate)


def test_t402_rejects_metadata_as_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t402_low_complexity_chunking_runway(QUEUE))
    data["candidate_queue"][0]["source_metadata_evidence"] = ["paragraph_markers_boundary_authority"]
    candidate = tmp_path / "t402.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T402RunwayError, match="evidence_only"):
        validator.validate_t402_low_complexity_chunking_runway(candidate)


def test_t402_rejects_ready_candidate_without_owner_gate(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t402_low_complexity_chunking_runway(QUEUE))
    data["candidate_queue"][0]["non_authorizations"].remove("exact_target_selection")
    candidate = tmp_path / "t402.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T402RunwayError, match="exact_target_selection"):
        validator.validate_t402_low_complexity_chunking_runway(candidate)
