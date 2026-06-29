from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_cursor_low_risk_chunking_handoff as validator


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".ai" / "control" / "cursor_low_risk_chunking_handoff.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t404_cursor_handoff_validates_current_repo() -> None:
    data = validator.validate_cursor_low_risk_chunking_handoff(CONTRACT)

    assert data["object_type"] == "cursor_low_risk_chunking_handoff"
    assert data["task_id"] == "T404"
    assert data["decision_register_entry"] == "CD-078"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-032"
    assert data["research_completion_verdict"]["t402_queue_research_complete_at_depth"] == "all_66_book_candidate_triage"
    assert data["research_completion_verdict"]["next_future_roadmap_task"] == "T406"


def test_t404_rejects_cursor_target_selection(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_cursor_low_risk_chunking_handoff(CONTRACT))
    data["low_risk_eligibility"]["cursor_may_select_target"] = True
    candidate = tmp_path / "t404.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.CursorHandoffError, match="cursor_may_select_target"):
        validator.validate_cursor_low_risk_chunking_handoff(candidate)


def test_t404_rejects_embedding_stop_condition_removal(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_cursor_low_risk_chunking_handoff(CONTRACT))
    data["stop_conditions"].remove("embedding_or_vector_work_requested")
    candidate = tmp_path / "t404.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.CursorHandoffError, match="embedding_or_vector_work_requested"):
        validator.validate_cursor_low_risk_chunking_handoff(candidate)


def test_t404_rejects_chunk_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_cursor_low_risk_chunking_handoff(CONTRACT))
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "t404.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.CursorHandoffError, match="authorizes_chunk_output_change"):
        validator.validate_cursor_low_risk_chunking_handoff(candidate)


def test_t404_rejects_missing_cursor_slash_command(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_cursor_low_risk_chunking_handoff(CONTRACT))
    data["cursor_usage"]["slash_commands"] = data["cursor_usage"]["slash_commands"][:2]
    candidate = tmp_path / "t404.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.CursorHandoffError, match="slash_commands"):
        validator.validate_cursor_low_risk_chunking_handoff(candidate)


def test_t404_multi_pass_plan_records_future_t406() -> None:
    data = validator.validate_cursor_low_risk_chunking_handoff(CONTRACT)

    assert ".ai/control/low_risk_chunking_multi_pass_plan.yaml" in data["mandatory_reading"]
