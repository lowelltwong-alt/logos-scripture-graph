from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_all
from scripts.validate_t477_baseline_reset import (
    T477BaselineError,
    t477_migration_active,
    validate_baseline_reset,
)


def test_t477_migration_active_requires_focus_and_candidate_counts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    focus = tmp_path / ".ai/control/current_focus.yaml"
    focus.parent.mkdir(parents=True)
    focus.write_text("current_task: T477\n", encoding="utf-8")
    word_tokens = tmp_path / "data/canonical/translations/eng-web/word_tokens.jsonl"
    footnotes = tmp_path / "data/canonical/translations/eng-web/footnotes.jsonl"
    word_tokens.parent.mkdir(parents=True)
    word_tokens.write_bytes(b"{}\n" * 677686)
    footnotes.write_bytes(b"{}\n" * 1130)
    monkeypatch.setattr("scripts.validate_t477_baseline_reset.ROOT", tmp_path)
    assert t477_migration_active(tmp_path) is True


def test_validate_all_defers_gates_under_t477(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(validate_all, "t475_candidate_transition_active", lambda: False)
    monkeypatch.setattr(validate_all, "t477_baseline_reset_active", lambda: True)
    names = [name for name, _ in validate_all.build_gates()]
    assert "validate_t374_additive_parent_overlay.py" not in names
    assert "validate_t477_baseline_reset.py" in names
    assert "validate_t475_generated_transition_state.py" not in names


def test_validate_baseline_reset_rejects_missing_owner_flag(tmp_path: Path) -> None:
    focus = tmp_path / ".ai/control/current_focus.yaml"
    focus.parent.mkdir(parents=True)
    focus.write_text("current_task: T477\n", encoding="utf-8")
    control = {
        "required_evidence": {"independent_audit_status": "PASS"},
        "execution_state": {
            "independent_audit_complete": True,
            "evidence_ready_for_T476": True,
            "t476_owner_authorized_T477": False,
            "t477_baseline_reset_complete": True,
        },
        "ci_generated_transition_policy": {
            "superseded_by": "T477",
            "authorizes_baseline_update": True,
            "authorizes_gold_or_output_change": False,
            "deferred_legacy_generated_validators": [],
            "deferred_pytest_nodes": [],
        },
    }
    gate = tmp_path / ".ai/control/t475_usfm_shadow_delta_gate.yaml"
    gate.write_text(yaml.safe_dump(control), encoding="utf-8")
    word_tokens = tmp_path / "data/canonical/translations/eng-web/word_tokens.jsonl"
    footnotes = tmp_path / "data/canonical/translations/eng-web/footnotes.jsonl"
    word_tokens.parent.mkdir(parents=True)
    word_tokens.write_bytes(b"{}\n" * 677686)
    footnotes.write_bytes(b"{}\n" * 1130)
    with pytest.raises(T477BaselineError, match="t476_owner_authorized_T477"):
        validate_baseline_reset(tmp_path)
