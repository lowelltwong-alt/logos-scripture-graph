from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_chunking_theological_decision_register as validator


ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"


def load_register() -> dict:
    return validator.validate_register(REGISTER)


def test_register_validates_and_is_non_authorizing() -> None:
    data = validator.validate_register(REGISTER)

    assert data["object_type"] == "chunking_theological_decision_register"
    assert data["trust_zone"] == "canonical"
    assert data["default_orthodoxy_boundary"] == "nicene_chalcedonian_core"
    assert data["register_authority"]["records_decisions"] is True
    assert data["register_authority"]["authorizes_chunk_output_change"] is False
    assert data["register_authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["register_authority"]["authorizes_skill_lifecycle_promotion"] is False
    assert data["register_authority"]["authorizes_boundary_import"] is False


def test_required_seed_decisions_are_backfilled() -> None:
    data = load_register()
    by_id = {entry["decision_id"]: entry for entry in data["decisions"]}

    assert by_id["CD-004"]["classification"] == "canon_scope"
    assert "canonical_66" in by_id["CD-004"]["affected_scope"]["books"]
    assert by_id["CD-006"]["affected_scope"]["passages"] == ["Ps.78.1-Ps.78.72"]
    assert by_id["CD-008"]["affected_scope"]["passages"] == ["Ps.89.1-Ps.89.52"]
    assert by_id["CD-002"]["classification"] == "interpretive_boundary"
    assert by_id["CD-010"]["classification"] == "non_authorizing_review"
    assert by_id["CD-009"]["classification"] == "non_authorizing_review"
    assert by_id["CD-011"]["classification"] == "theological_risk"


def test_full_backfill_coverage_has_no_missing_task_ids() -> None:
    data = validator.validate_register(REGISTER)
    required = set(data["backfill_coverage"]["required_task_ids"])
    covered = set()
    for decision in data["decisions"]:
        covered.update(decision["task_ids"])
    for marker in data["no_impact_markers"]:
        covered.update(marker["task_ids"])

    assert required <= covered
    assert "T348" in covered
    assert "T341" in covered
    assert "T327D" in covered
    assert "T398" in covered


def test_t398_phase_one_research_decision_is_backfilled() -> None:
    data = load_register()
    by_id = {entry["decision_id"]: entry for entry in data["decisions"]}

    decision = by_id["CD-072"]
    assert decision["classification"] == "non_authorizing_review"
    assert decision["task_ids"] == ["T398"]
    assert decision["affected_scope"]["books"] == ["canonical_66"]
    assert ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml" in decision["affected_scope"]["surfaces"]
    assert "every verse has not been deeply exegeted" in decision["decision"]
    assert "chunk_output_change" in decision["non_authorizations"]
    assert "whole_bible_output_pass" in decision["non_authorizations"]


def test_changed_path_gate_requires_register_update_for_chunking_paths() -> None:
    with pytest.raises(validator.RegisterError, match="must be updated"):
        validator.validate_changed_path_gate(
            changed_files=["pipelines/chunking/chunker.py"],
            register_updated=False,
        )


def test_changed_path_gate_passes_when_register_is_updated() -> None:
    validator.validate_changed_path_gate(
        changed_files=[
            "pipelines/chunking/chunker.py",
            ".ai/control/chunking_theological_decision_register.yaml",
        ],
        register_updated=None,
    )


def test_changed_path_gate_ignores_unwatched_paths() -> None:
    validator.validate_changed_path_gate(
        changed_files=["README.md", "scripts/validate_all.py"],
        register_updated=False,
    )
