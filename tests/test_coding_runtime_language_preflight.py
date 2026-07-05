from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_coding_runtime_language_preflight as validator


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / ".ai" / "control" / "coding_runtime_language_preflight.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_coding_runtime_language_preflight_validates_current_repo() -> None:
    data = validator.validate_coding_runtime_language_preflight(PREFLIGHT)

    assert data["object_type"] == "coding_runtime_language_preflight"
    assert data["policy"]["rust_preferred_for_high_resource_deterministic_code"] is True
    assert data["policy"]["python_pytest_remain_governance_orchestrator"] is True
    assert data["rust_preferred_cutoffs"]["rust_preferred_when_estimated_savings_seconds_at_least"] >= 30


def test_coding_runtime_language_preflight_rejects_disabling_rust_preference(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_coding_runtime_language_preflight(PREFLIGHT))
    data["policy"]["rust_preferred_for_high_resource_deterministic_code"] = False
    candidate = tmp_path / "coding-runtime-language-preflight.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.CodingRuntimeLanguagePreflightError, match="rust_preferred"):
        validator.validate_coding_runtime_language_preflight(candidate)


def test_coding_runtime_language_preflight_rejects_weak_savings_cutoff(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_coding_runtime_language_preflight(PREFLIGHT))
    data["rust_preferred_cutoffs"]["rust_preferred_when_estimated_savings_seconds_at_least"] = 5
    candidate = tmp_path / "coding-runtime-language-preflight.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.CodingRuntimeLanguagePreflightError, match="30 seconds"):
        validator.validate_coding_runtime_language_preflight(candidate)


def test_coding_runtime_language_preflight_requires_decision_traceability(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_coding_runtime_language_preflight(PREFLIGHT))
    data["decision_record_required_fields"].remove("maintenance_tradeoffs")
    candidate = tmp_path / "coding-runtime-language-preflight.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.CodingRuntimeLanguagePreflightError, match="maintenance_tradeoffs"):
        validator.validate_coding_runtime_language_preflight(candidate)
