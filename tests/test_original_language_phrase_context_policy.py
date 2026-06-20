from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_original_language_phrase_context_policy as validator


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ai" / "control" / "original_language_phrase_context_policy.yaml"


def load_policy() -> dict:
    text = POLICY.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "original_language_phrase_context_policy.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_original_language_phrase_context_policy_validates_current_repo() -> None:
    data = validator.validate_original_language_phrase_context_policy()

    assert data["object_type"] == "original_language_phrase_context_policy"
    assert data["trust_zone"] == "canonical"
    assert data["authority"]["authorizes_original_language_truth"] is False
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert "phrase" in data["research_assessment"]["refined_rule"].lower()
    assert "discourse" in data["research_assessment"]["refined_rule"].lower()


def test_policy_requires_context_layers_and_packet_fields() -> None:
    data = load_policy()
    layers = {layer["layer_id"] for layer in data["context_layers_required"]}

    assert validator.REQUIRED_CONTEXT_LAYERS <= layers
    assert "phrase_or_clause_scope" in data["required_future_original_language_packet_fields"]
    assert "syntax_role" in data["required_future_original_language_packet_fields"]
    assert "immediate_discourse_context" in data["required_future_original_language_packet_fields"]
    assert "semantic_range_not_single_gloss" in data["required_future_original_language_packet_fields"]
    assert "textual_variant_dependency_if_any" in data["required_future_original_language_packet_fields"]
    assert "poetry_parallelism_or_structural_feature_if_relevant" in data["required_future_original_language_packet_fields"]


def test_policy_records_greek_hebrew_chunking_lessons() -> None:
    data = validator.validate_original_language_phrase_context_policy()
    lesson_ids = {lesson["lesson_id"] for lesson in data["original_language_chunking_lessons"]}

    assert validator.REQUIRED_LESSON_IDS <= lesson_ids
    assert "root_fallacy_guard" in lesson_ids
    assert "semantic_range_not_totality" in lesson_ids
    assert "greek_article_predication_guard" in lesson_ids
    assert "hebrew_plural_form_guard" in lesson_ids
    assert "lxx_nt_quotation_guard" in lesson_ids
    assert "textual_variant_gate" in lesson_ids
    assert "punctuation_capitalization_editorial_guard" in lesson_ids
    assert "discourse_markers_and_poetry_need_context" in lesson_ids


def test_policy_rejects_original_language_truth_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["authority"]["authorizes_original_language_truth"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.OriginalLanguagePhraseContextPolicyError, match="authorizes_original_language_truth"):
        validator.validate_original_language_phrase_context_policy(candidate)


def test_policy_rejects_missing_phrase_clause_syntax_layer(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["context_layers_required"] = [
        layer for layer in data["context_layers_required"]
        if layer["layer_id"] != "phrase_clause_syntax"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.OriginalLanguagePhraseContextPolicyError, match="phrase_clause_syntax"):
        validator.validate_original_language_phrase_context_policy(candidate)


def test_policy_rejects_isolated_word_authorization_loss(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["non_authorizations"].remove("isolated_word_as_theological_truth")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.OriginalLanguagePhraseContextPolicyError, match="isolated_word_as_theological_truth"):
        validator.validate_original_language_phrase_context_policy(candidate)


def test_policy_rejects_missing_root_fallacy_guard(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["original_language_chunking_lessons"] = [
        lesson for lesson in data["original_language_chunking_lessons"]
        if lesson["lesson_id"] != "root_fallacy_guard"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.OriginalLanguagePhraseContextPolicyError, match="root_fallacy_guard"):
        validator.validate_original_language_phrase_context_policy(candidate)
