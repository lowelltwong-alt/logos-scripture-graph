from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_test_runtime_preflight as validator


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / ".ai" / "control" / "test_runtime_preflight.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_test_runtime_preflight_validates_current_repo() -> None:
    data = validator.validate_test_runtime_preflight(PREFLIGHT)
    profiles = {profile["command_id"]: profile for profile in data["runtime_profiles"]}

    assert data["object_type"] == "test_runtime_preflight"
    assert data["authority"]["authorizes_skipping_tests"] is False
    assert data["authority"]["authorizes_validation_bypass"] is False
    assert profiles["pytest_full_suite"]["recommended_timeout_ms"] >= 600000
    assert profiles["pytest_full_suite_local_desktop_t398"]["recommended_timeout_ms"] >= 1200000
    assert "nested pytest/validate_all" in profiles["pytest_full_suite_local_desktop_t398"]["observed_result"]
    assert profiles["validate_all"]["recommended_timeout_ms"] >= 300000


def test_test_runtime_preflight_rejects_short_pytest_timeout(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_test_runtime_preflight(PREFLIGHT))
    for profile in data["runtime_profiles"]:
        if profile["command_id"] == "pytest_full_suite":
            profile["recommended_timeout_ms"] = 300000
    candidate = tmp_path / "test-runtime-preflight.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.TestRuntimePreflightError, match="recommended_timeout_ms"):
        validator.validate_test_runtime_preflight(candidate)


def test_test_runtime_preflight_rejects_timeout_as_green(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_test_runtime_preflight(PREFLIGHT))
    for profile in data["runtime_profiles"]:
        if profile["command_id"] == "pytest_full_suite":
            profile["do_not"] = ["hide_timeout_from_handoff"]
    candidate = tmp_path / "test-runtime-preflight.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.TestRuntimePreflightError, match="timeout as green"):
        validator.validate_test_runtime_preflight(candidate)
