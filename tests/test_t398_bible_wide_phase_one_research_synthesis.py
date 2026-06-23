from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t398_bible_wide_phase_one_research_synthesis as validator


ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / ".ai" / "control" / "t398_bible_wide_phase_one_research_synthesis.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t398_phase_one_synthesis_validates_current_repo() -> None:
    data = validator.validate_t398_bible_wide_phase_one_research_synthesis(SYNTHESIS)

    assert data["object_type"] == "bible_wide_phase_one_research_synthesis"
    assert data["task_id"] == "T398"
    assert data["status"] == "complete_phase_one_whole_corpus_research_synthesis"
    assert data["phase_one_definition"]["canonical_book_count"] == 66
    assert data["phase_one_definition"]["canonical_passage_count"] == 31103
    assert data["phase_one_definition"]["every_canonical_passage_accounted_for_at_triage_depth"] is True
    assert data["phase_one_definition"]["every_verse_deeply_researched"] is False
    assert data["phase_one_definition"]["does_not_mean_chunking_ready_for_whole_bible_output"] is True
    assert data["decision_register_entry"] == "CD-072"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-026"


def test_t398_records_human_decision_prompts_and_goal2_prompt() -> None:
    data = validator.validate_t398_bible_wide_phase_one_research_synthesis(SYNTHESIS)

    prompt_ids = {prompt["prompt_id"] for prompt in data["phase_one_human_decision_prompt_queue"]}
    assert validator.REQUIRED_PROMPTS <= prompt_ids
    assert data["phase_two_research_recommendation"]["relation_to_t397"].startswith("T397 remains")
    assert "Goal 2 focused Bible-wide research" in data["phase_two_research_recommendation"]["goal_prompt"]
    assert "Do not select targets" in data["phase_two_research_recommendation"]["goal_prompt"]


def test_t398_keeps_all_authority_flags_closed() -> None:
    data = validator.validate_t398_bible_wide_phase_one_research_synthesis(SYNTHESIS)

    for key in validator.REQUIRED_FALSE_AUTHORITY:
        assert data["authority"][key] is False
    assert validator.REQUIRED_NON_AUTHORIZATIONS <= set(data["non_authorizations"])


def test_t398_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t398_bible_wide_phase_one_research_synthesis(SYNTHESIS))
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "t398.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T398SynthesisError, match="authorizes_chunk_output_change"):
        validator.validate_t398_bible_wide_phase_one_research_synthesis(candidate)


def test_t398_rejects_deep_exegesis_overclaim(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t398_bible_wide_phase_one_research_synthesis(SYNTHESIS))
    data["phase_one_definition"]["every_verse_deeply_researched"] = True
    candidate = tmp_path / "t398.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T398SynthesisError, match="every_verse_deeply_researched"):
        validator.validate_t398_bible_wide_phase_one_research_synthesis(candidate)
