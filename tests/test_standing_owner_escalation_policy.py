"""Tests for standing owner escalation policy validator."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts.validate_standing_owner_escalation_policy import (
    StandingEscalationPolicyError,
    validate_policy,
)

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "standing_owner_escalation_policy.yaml"


def _load_policy() -> dict:
    text = POLICY.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    assert isinstance(data, dict)
    return data


def test_policy_file_validates_clean() -> None:
    errors = validate_policy()
    assert errors == []


def test_all_packet_suffixes_covered() -> None:
    data = _load_policy()
    suffixes = {r["issue_suffix"] for r in data["escalation_packet_issue_rules"]}
    assert "theology_pressure" in suffixes
    assert "slavery_social_ethics" in suffixes
    assert len(suffixes) == 14


def test_draft_status_blocks_ladder_until_approval() -> None:
    data = _load_policy()
    assert data["status"] == "draft_pending_owner_approval"
    blocked = data["owner_one_time_approval"]["until_approved"]["blocked_without_approval"]
    assert "standing_ladder_authorization" in blocked


def test_active_policy_requires_lifecycle_active() -> None:
    data = _load_policy()
    data["status"] = "active"
    data["lifecycle_status"] = "draft_pending_owner_approval"
    errors = validate_policy(data)
    assert any("lifecycle_status active" in e for e in errors)


def test_missing_issue_suffix_fails() -> None:
    data = _load_policy()
    data["escalation_packet_issue_rules"] = [
        r for r in data["escalation_packet_issue_rules"] if r["issue_suffix"] != "theology_pressure"
    ]
    errors = validate_policy(data)
    assert any("theology_pressure" in e for e in errors)
