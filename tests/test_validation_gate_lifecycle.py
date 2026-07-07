from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.validate_validation_gate_lifecycle import (
    ValidationGateLifecycleError,
    _validate_gate,
    validate_lifecycle_expansion_candidates,
    validate_validation_gate_lifecycle,
)


def test_validation_gate_lifecycle_passes() -> None:
    data = validate_validation_gate_lifecycle()

    assert data["object_type"] == "validation_gate_lifecycle"
    statuses = {gate["status"] for gate in data["tracked_gates"]}
    assert "active_generated_data" in statuses


def test_lifecycle_expansion_candidates_pass() -> None:
    data = validate_lifecycle_expansion_candidates()

    surface_ids = {surface["surface_id"] for surface in data["recommended_lifecycle_surfaces"]}
    assert "generated_artifacts" in surface_ids
    assert "dad_messages_and_lessons" in surface_ids


def test_generated_data_gate_requires_required_inputs() -> None:
    data = validate_validation_gate_lifecycle()
    gate = deepcopy(data["tracked_gates"][0])
    gate["required_inputs"] = []

    with pytest.raises(ValidationGateLifecycleError, match="required_inputs"):
        _validate_gate(gate, set(), validate_validation_gate_lifecycle.__defaults__[0])


def test_retired_gate_requires_replacement() -> None:
    data = validate_validation_gate_lifecycle()
    gate = deepcopy(data["tracked_gates"][0])
    gate["status"] = "retired"
    gate["missing_input_behavior"] = "not_applicable"
    gate["replacement_gate"] = None

    with pytest.raises(ValidationGateLifecycleError, match="replacement_gate"):
        _validate_gate(gate, set(), validate_validation_gate_lifecycle.__defaults__[0])


def test_validate_all_skips_generated_data_gates_when_sidecars_are_absent(tmp_path, monkeypatch) -> None:
    from scripts import validate_all

    missing = tmp_path / "data" / "canonical" / "missing.jsonl"
    monkeypatch.setattr(validate_all, "GENERATED_CANONICAL_REQUIRED", [missing])

    assert validate_all.generated_canonical_missing() == [missing]
    assert validate_all.generated_data_gates() == []
