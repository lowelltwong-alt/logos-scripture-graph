#!/usr/bin/env python3
"""Validate deterministic runtime guidance for long test/validation commands."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFLIGHT = ROOT / ".ai" / "control" / "test_runtime_preflight.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
WORKFLOW_LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"

REQUIRED_PROFILES = {
    "pytest_full_suite": {
        "command": "python -m pytest -q",
        "minimum_timeout_ms": 600000,
        "required_phrases": ["5-minute tool timeout", "7 minutes"],
    },
    "validate_all": {
        "command": "python scripts/validate_all.py",
        "minimum_timeout_ms": 900000,
        "required_phrases": ["240000 ms", "900000 ms", "477.5 seconds"],
    },
    "pytest_full_suite_local_desktop_t398": {
        "command": "python -m pytest -q",
        "minimum_timeout_ms": 1200000,
        "required_phrases": ["900000 ms", "nested pytest/validate_all"],
    },
}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_skipping_tests",
    "authorizes_ignoring_failures",
    "authorizes_output_change",
    "authorizes_validation_bypass",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "skip_test_due_to_runtime",
    "ignore_timeout",
    "treat_timeout_as_green",
    "validation_bypass",
    "output_change",
}

REQUIRED_WIRING = {
    FRONT_DOOR: ["test_runtime_preflight.yaml", "python scripts/validate_all.py", "900000", "python -m pytest -q"],
    MAIN_TOC: ["test-runtime", "pytest-timeout", "test_runtime_preflight.yaml"],
    WORKFLOW_LESSONS: ["WORKFLOW-LESSON-010", "Test Runtime Preflight"],
    LESSON_INDEX: ["LSN-015", "test-runtime", "test_runtime_preflight.yaml"],
}


class TestRuntimePreflightError(ValueError):
    """Raised when test runtime preflight memory is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TestRuntimePreflightError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise TestRuntimePreflightError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise TestRuntimePreflightError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise TestRuntimePreflightError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise TestRuntimePreflightError(f"{label} must contain only non-empty strings")
    return [str(item) for item in value]


def validate_test_runtime_preflight(path: Path = PREFLIGHT) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "test_runtime_preflight",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "test_runtime_preflight.v1",
        "preflight_id": "repo_test_runtime_preflight",
        "validator": "scripts/validate_test_runtime_preflight.py",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise TestRuntimePreflightError(f"{_rel(path)}: {key} must be {value!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise TestRuntimePreflightError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_runtime_observations") is not True:
        raise TestRuntimePreflightError(f"{_rel(path)}: authority.records_runtime_observations must be true")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise TestRuntimePreflightError(f"{_rel(path)}: authority.{key} must be false")

    non_auth = set(_require_string_list(data.get("non_authorizations"), f"{_rel(path)}.non_authorizations"))
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing_non_auth:
        raise TestRuntimePreflightError(f"{_rel(path)}: missing non_authorizations {missing_non_auth}")

    profiles = data.get("runtime_profiles")
    if not isinstance(profiles, list) or not profiles:
        raise TestRuntimePreflightError(f"{_rel(path)}: runtime_profiles must be a non-empty list")
    by_id = {profile.get("command_id"): profile for profile in profiles if isinstance(profile, dict)}
    missing_profiles = sorted(set(REQUIRED_PROFILES) - set(by_id))
    if missing_profiles:
        raise TestRuntimePreflightError(f"{_rel(path)}: missing runtime profiles {missing_profiles}")

    for command_id, requirements in REQUIRED_PROFILES.items():
        profile = by_id[command_id]
        label = f"{_rel(path)}:{command_id}"
        if profile.get("command") != requirements["command"]:
            raise TestRuntimePreflightError(f"{label}: command must be {requirements['command']!r}")
        timeout = profile.get("recommended_timeout_ms")
        if not isinstance(timeout, int) or timeout < requirements["minimum_timeout_ms"]:
            raise TestRuntimePreflightError(f"{label}: recommended_timeout_ms must be at least {requirements['minimum_timeout_ms']}")
        _require_string_list(profile.get("recommended_strategy"), f"{label}.recommended_strategy")
        do_not = set(_require_string_list(profile.get("do_not"), f"{label}.do_not"))
        if "treat_timeout_as_test_pass" not in do_not and "treat_timeout_as_green" not in do_not:
            raise TestRuntimePreflightError(f"{label}: do_not must deny treating timeout as green")
        observed_result = str(profile.get("observed_result", ""))
        for phrase in requirements["required_phrases"]:
            if phrase not in observed_result and phrase not in str(profile.get("observed_context", "")):
                raise TestRuntimePreflightError(f"{label}: missing observed phrase {phrase!r}")

    update_policy = data.get("update_policy")
    if not isinstance(update_policy, dict) or update_policy.get("status") != "required":
        raise TestRuntimePreflightError(f"{_rel(path)}: update_policy.status must be required")
    for key in ("update_required_when", "required_fields_for_new_profile"):
        _require_string_list(update_policy.get(key), f"{_rel(path)}.update_policy.{key}")

    for wired_path, needles in REQUIRED_WIRING.items():
        text = _read_text(wired_path)
        for needle in needles:
            if needle not in text:
                raise TestRuntimePreflightError(f"{_rel(wired_path)}: missing runtime preflight wiring string {needle!r}")

    return data


def main() -> int:
    try:
        validate_test_runtime_preflight()
    except TestRuntimePreflightError as exc:
        print(f"Test runtime preflight validation failed: {exc}", file=sys.stderr)
        return 1
    print("Test runtime preflight validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
