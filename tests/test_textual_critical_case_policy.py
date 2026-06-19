from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_textual_critical_case_policy as validator


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ai" / "control" / "textual_critical_case_policy.yaml"


def load_policy() -> dict:
    text = POLICY.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "textual_critical_case_policy.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_textual_critical_case_policy_validates_current_repo() -> None:
    data = validator.validate_textual_critical_case_policy()

    assert data["object_type"] == "textual_critical_case_policy"
    assert data["owner_authorization"]["selected_option"] == "TCP-T378-B"
    assert data["authority"]["selects_case_by_case_process_policy"] is True
    assert data["authority"]["authorizes_preferred_reading"] is False
    assert data["authority"]["authorizes_reviewed_gold"] is False
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["t371_implication"]["t371_reviewed_gold_promotion_authorized"] is False


def test_case_policy_requires_exact_future_promotion_fields() -> None:
    data = load_policy()
    required = set(data["case_by_case_policy"]["required_before_each_variant_sensitive_promotion"])

    assert validator.REQUIRED_CASE_FIELDS <= required
    assert "owner_confirmation" in required
    assert "decision_register_update" in required
    assert "validators_tests" in required


def test_case_policy_records_future_pattern_without_promotion_authority() -> None:
    data = load_policy()
    projection = data["future_projection_memory"]

    assert projection["projectable_pattern_id"] == "ODP-005"
    assert projection["can_project_process_rule"] is True
    assert projection["cannot_project_specific_promotion"] is True
    assert projection["cannot_project_variant_dependency_claim"] is True
    assert projection["cannot_project_preferred_reading"] is True


def test_case_policy_rejects_preferred_reading_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["authority"]["authorizes_preferred_reading"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualCriticalCasePolicyError, match="authorizes_preferred_reading"):
        validator.validate_textual_critical_case_policy(candidate)


def test_case_policy_rejects_missing_owner_confirmation_requirement(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["case_by_case_policy"]["required_before_each_variant_sensitive_promotion"].remove(
        "owner_confirmation"
    )
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualCriticalCasePolicyError, match="owner_confirmation"):
        validator.validate_textual_critical_case_policy(candidate)


def test_case_policy_rejects_projection_drift(tmp_path: Path) -> None:
    data = copy.deepcopy(load_policy())
    data["future_projection_memory"]["projectable_pattern_id"] = "ODP-999"
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualCriticalCasePolicyError, match="ODP-005"):
        validator.validate_textual_critical_case_policy(candidate)
