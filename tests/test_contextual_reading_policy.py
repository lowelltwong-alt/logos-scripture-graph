from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_contextual_reading_policy as validator


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ai" / "control" / "contextual_reading_policy.yaml"


def load_policy() -> dict:
    text = POLICY.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "contextual_reading_policy.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_contextual_reading_policy_validates_current_repo() -> None:
    data = validator.validate_contextual_reading_policy()

    assert data["object_type"] == "contextual_reading_policy"
    assert data["trust_zone"] == "canonical"
    assert data["authority"]["records_contextual_reading_policy"] is True
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["authority"]["authorizes_chunk_output_change"] is False


def test_policy_requires_context_layers_and_packet_fields() -> None:
    data = validator.validate_contextual_reading_policy()
    layers = {layer["layer_id"] for layer in data["context_layers_required"]}

    assert validator.REQUIRED_CONTEXT_LAYERS <= layers
    assert "immediate_previous_context" in data["required_future_review_packet_fields"]
    assert "immediate_following_context" in data["required_future_review_packet_fields"]
    assert "chapter_context" in data["required_future_review_packet_fields"]
    assert "book_argument_or_narrative_context" in data["required_future_review_packet_fields"]
    assert "canonical_context_links_considered" in data["required_future_review_packet_fields"]
    assert "historical_cultural_context_if_used" in data["required_future_review_packet_fields"]


def test_policy_keeps_history_sidecar_lower_trust_and_not_created_now() -> None:
    data = validator.validate_contextual_reading_policy()
    sidecar = data["future_history_sidecar_policy"]

    assert sidecar["create_history_repo_now"] is False
    assert set(sidecar["allowed_trust_zones"]) == {"learning-sidecar", "proposed"}
    assert "scripture_authority" in sidecar["disallowed_roles"]
    assert "chunk_boundary_authority" in sidecar["disallowed_roles"]
    assert "liberal_critical_default" in sidecar["disallowed_roles"]


def test_policy_rejects_historical_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["authority"]["authorizes_historical_context_as_authority"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.ContextualReadingPolicyError, match="authorizes_historical_context_as_authority"):
        validator.validate_contextual_reading_policy(candidate)


def test_policy_rejects_missing_chapter_book_context(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["context_layers_required"] = [
        layer for layer in data["context_layers_required"]
        if layer["layer_id"] != "chapter_book_context"
    ]
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.ContextualReadingPolicyError, match="chapter_book_context"):
        validator.validate_contextual_reading_policy(candidate)


def test_policy_rejects_context_as_output_authority_loss(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["non_authorizations"].remove("context_as_chunk_boundary_authority")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.ContextualReadingPolicyError, match="context_as_chunk_boundary_authority"):
        validator.validate_contextual_reading_policy(candidate)
