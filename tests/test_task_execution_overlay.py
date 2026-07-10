from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from scripts.validate_task_execution_overlay import ExecutionOverlayError, validate_execution_overlay

ROOT = Path(__file__).resolve().parent.parent


def _copy_contract(tmp_path: Path) -> Path:
    for rel in (
        ".ai/tasks/T475.task.yaml",
        ".ai/control/ai_agnostic_rust_subagent_charter.yaml",
        ".ai/control/t474_usfm_marker_anchor_contract.yaml",
        "config/agents/model_routing.yaml",
        "config/agents/agent_roles.yaml",
    ):
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    return tmp_path


def _mutate_task(root: Path, mutate) -> None:
    path = root / ".ai/tasks/T475.task.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t475_execution_overlay_passes() -> None:
    result = validate_execution_overlay(ROOT, "T475")
    assert result["stage_count"] == 6
    assert result["aliases"] == ["Claude", "Luna", "Sol", "Terra"]


def test_luna_cannot_inherit_reasoner_profile(tmp_path: Path) -> None:
    root = _copy_contract(tmp_path)
    _mutate_task(root, lambda data: data["execution_overlay"]["task_local_roster_binding"]["Luna"].update(profile="reasoner"))
    with pytest.raises(ExecutionOverlayError, match="Luna"):
        validate_execution_overlay(root, "T475")


def test_performance_alone_cannot_advance(tmp_path: Path) -> None:
    root = _copy_contract(tmp_path)
    _mutate_task(root, lambda data: data["execution_overlay"]["rust_continuation_gate"].update(performance_alone_may_advance=True))
    with pytest.raises(ExecutionOverlayError, match="performance alone"):
        validate_execution_overlay(root, "T475")


def test_independent_auditor_cannot_edit(tmp_path: Path) -> None:
    root = _copy_contract(tmp_path)
    _mutate_task(root, lambda data: data["execution_overlay"]["independent_audit"].update(may_edit_or_regenerate=True))
    with pytest.raises(ExecutionOverlayError, match="may not edit"):
        validate_execution_overlay(root, "T475")


def test_model_id_cannot_leak_into_durable_routing(tmp_path: Path) -> None:
    root = _copy_contract(tmp_path)
    routing = root / "config/agents/model_routing.yaml"
    routing.write_text(routing.read_text(encoding="utf-8") + "\n# gpt-5.6-sol\n", encoding="utf-8")
    with pytest.raises(ExecutionOverlayError, match="leaked"):
        validate_execution_overlay(root, "T475")
