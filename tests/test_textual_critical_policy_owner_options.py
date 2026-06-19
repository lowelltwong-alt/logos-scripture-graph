from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_textual_critical_policy_owner_options as validator


ROOT = Path(__file__).resolve().parents[1]
OPTIONS = ROOT / ".ai" / "control" / "textual_critical_policy_owner_options.yaml"


def load_options() -> dict:
    text = OPTIONS.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "textual_critical_policy_owner_options.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_textual_critical_policy_owner_options_validate_current_repo() -> None:
    data = validator.validate_textual_critical_policy_owner_options()

    assert data["object_type"] == "textual_critical_policy_owner_options_docket"
    assert data["policy_status"]["textual_critical_policy_selected"] is True
    assert data["policy_status"]["selected_policy"] == "TCP-T378-B"
    assert data["policy_status"]["owner_decision_required"] is False
    assert data["policy_status"]["blocks_t371_until_selected"] is False
    assert data["policy_status"]["owner_selection_task"] == "T379"
    assert data["policy_status"]["selection_record"] == ".ai/control/textual_critical_case_policy.yaml"
    assert data["authority"]["authorizes_textual_critical_policy"] is False
    assert data["authority"]["authorizes_preferred_reading"] is False
    assert data["authority"]["authorizes_reviewed_gold"] is False
    assert data["recommended_owner_path"]["option_id"] == "TCP-T378-B"
    assert data["recommended_owner_path"]["selection_status"] == "selected_by_owner"


def test_t371_variant_triggers_are_recorded() -> None:
    data = load_options()
    triggers = {item["passage"]: item for item in data["variant_sensitive_trigger_examples"]}

    assert "1Cor.9.20" in triggers
    assert "1Cor.10.9" in triggers
    assert "parent span" in triggers["1Cor.9.20"]["t371_relevance"]
    assert "Christological" in triggers["1Cor.10.9"]["t371_relevance"]


def test_owner_options_include_recommended_case_by_case_policy() -> None:
    data = load_options()
    options = {item["option_id"]: item for item in data["owner_options"]}

    assert validator.REQUIRED_OPTIONS <= set(options)
    assert options["TCP-T378-B"]["recommended_by_agent"] is True
    assert "case-by-case" in options["TCP-T378-B"]["title"].lower()
    assert "liberal-critical" in options["TCP-T378-B"]["upside"]
    assert "current-source" in options["TCP-T378-B"]["recommendation_rationale"]


def test_options_reject_hidden_policy_selection(tmp_path: Path) -> None:
    data = copy.deepcopy(load_options())
    data["policy_status"]["selected_policy"] = "critical_text_default"
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualCriticalOptionsError, match="selected_policy"):
        validator.validate_textual_critical_policy_owner_options(candidate)


def test_options_reject_preferred_reading_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(load_options())
    data["authority"]["authorizes_preferred_reading"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualCriticalOptionsError, match="authorizes_preferred_reading"):
        validator.validate_textual_critical_policy_owner_options(candidate)


def test_options_reject_recommendation_drift(tmp_path: Path) -> None:
    data = copy.deepcopy(load_options())
    data["recommended_owner_path"]["option_id"] = "TCP-T378-C"
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.TextualCriticalOptionsError, match="recommended option"):
        validator.validate_textual_critical_policy_owner_options(candidate)
