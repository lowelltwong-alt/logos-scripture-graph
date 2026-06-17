from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_owner_selection_implementation_gate as gate


ROOT = Path(__file__).resolve().parents[1]
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
HARNESS_ROADMAP = ROOT / ".ai" / "control" / "harness_upgrade_roadmap.yaml"
T344_TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"


def test_owner_selection_gate_validates_current_pending_state() -> None:
    data = gate.validate_owner_selection_implementation_gate()

    assert data["gate_id"] == "HARN-012"
    assert data["owner_selection_status"] == "pending"
    assert data["selected_option"] == "pending"
    assert data["t345_status"] == "planned"
    assert data["implementation_allowed"] is False


def test_gate_rejects_t345_start_while_owner_selection_pending(tmp_path: Path) -> None:
    text = ROADMAP_STATE.read_text(encoding="utf-8")
    text = text.replace("status: planned\n        lane: revelation_implementation", "status: in_progress\n        lane: revelation_implementation")
    candidate = tmp_path / "ROADMAP_STATE.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(gate.OwnerSelectionGateError, match="ROADMAP_STATE.T345.status"):
        gate.validate_owner_selection_implementation_gate(roadmap_state=candidate)


def test_gate_rejects_t345_task_file_before_owner_selection(tmp_path: Path) -> None:
    t345_task = tmp_path / "T345.task.yaml"
    t345_task.write_text("id: T345\nstatus: in_progress\n", encoding="utf-8")

    with pytest.raises(gate.OwnerSelectionGateError, match="T345 implementation cannot start"):
        gate.validate_owner_selection_implementation_gate(t345_task=t345_task)


def test_gate_rejects_selected_option_drift(tmp_path: Path) -> None:
    text = T344_TASK.read_text(encoding="utf-8").replace("selected_option: pending", "selected_option: REV-T344-C")
    candidate = tmp_path / "T344.task.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(gate.OwnerSelectionGateError, match="selected_option surfaces disagree"):
        gate.validate_owner_selection_implementation_gate(t344_task=candidate)


def test_gate_requires_harn_012_to_be_marked_implemented(tmp_path: Path) -> None:
    text = HARNESS_ROADMAP.read_text(encoding="utf-8")
    text = text.replace(
        "  - harness_id: HARN-012\n"
        "    title: Owner-selection-to-implementation gate harness\n"
        "    status: implemented_v1",
        "  - harness_id: HARN-012\n"
        "    title: Owner-selection-to-implementation gate harness\n"
        "    status: candidate_not_started",
    )
    candidate = tmp_path / "harness_upgrade_roadmap.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(gate.OwnerSelectionGateError, match="HARN-012.status"):
        gate.validate_owner_selection_implementation_gate(harness_roadmap=candidate)
