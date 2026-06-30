from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_parallel_chunking_prompt_pack as validator


ROOT = Path(__file__).resolve().parents[1]


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t410_prompt_pack_validates_current_repo() -> None:
    data = validator.validate_parallel_chunking_prompt_pack()

    assert data["object_type"] == "parallel_chunking_research_program"
    assert data["task_id"] == "T410"
    assert data["phase_one_definition"]["implementation_shape"] == "parent_only_additive_overlay"


def test_t410_rejects_chunk_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_program())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "program.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.PromptPackError, match="authorizes_chunk_output_change"):
        validator.validate_program(candidate)


def test_t410_rejects_missing_book_hint(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_book_hints())
    data["book_hints"] = data["book_hints"][:-1]
    candidate = tmp_path / "hints.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.PromptPackError, match="canonical 66 order"):
        validator.validate_book_hints(candidate)


def test_t410_rejects_missing_transparency_log(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_transparency())
    data["required_machine_logs"]["files"].remove("audit_log.jsonl")
    candidate = tmp_path / "transparency.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.PromptPackError, match="audit_log.jsonl"):
        validator.validate_transparency(candidate)


def test_t410_rejects_missing_frontier_trigger(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_frontier_policy())
    data["mandatory_escalation_triggers"].remove("apocalyptic_or_vision_cycle")
    candidate = tmp_path / "frontier.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.PromptPackError, match="apocalyptic_or_vision_cycle"):
        validator.validate_frontier_policy(candidate)


def test_t410_phase_one_statuses_cover_all_66_books(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_completion_plan())
    data["initial_phase_one_statuses"][0]["book_id"] = "Rev"
    candidate = tmp_path / "completion.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.PromptPackError, match="canonical 66 order"):
        validator.validate_completion_plan(candidate)
