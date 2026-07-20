from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

import pytest
import yaml

from scripts.generated_data_lifecycle import (
    load_generated_data_gates,
    missing_declared_inputs,
    runnable_generated_data_gates,
    skipped_generated_data_gates,
)

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
    gate_ids = {gate["gate_id"] for gate in data["tracked_gates"]}
    assert "build_t433_phlm_alignment_pilot_currentness" in gate_ids
    assert "build_t439_phlm_alignment_bridge_expansion_currentness" in gate_ids
    assert "validate_fast_canonical_scope" in gate_ids
    assert "validate_fast_jsonl_canonical" in gate_ids


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


def test_generated_data_gate_rejects_path_escape() -> None:
    data = validate_validation_gate_lifecycle()
    gate = deepcopy(data["tracked_gates"][0])
    gate["required_inputs"] = ["data/canonical/../../scripts/validate_all.py"]

    with pytest.raises(ValidationGateLifecycleError, match="repository-relative generated canonical"):
        _validate_gate(gate, set(), validate_validation_gate_lifecycle.__defaults__[0])


def _write_test_registry(root: Path) -> Path:
    command = root / "scripts" / "dummy_generated_gate.py"
    command.parent.mkdir(parents=True)
    command.write_text("raise SystemExit(0)\n", encoding="utf-8")
    registry = root / ".ai" / "control" / "validation_gate_lifecycle.yaml"
    registry.parent.mkdir(parents=True)
    registry.write_text(
        yaml.safe_dump(
            {
                "tracked_gates": [
                    {
                        "gate_id": "dummy_generated_gate",
                        "command": "scripts/dummy_generated_gate.py",
                        "args": ["--check"],
                        "status": "active_generated_data",
                        "required_inputs": ["data/canonical/example.jsonl"],
                        "missing_input_behavior": "skip_when_ignored_generated_data_absent",
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return registry


def test_registry_scheduler_skips_missing_and_runs_present(tmp_path: Path) -> None:
    registry = _write_test_registry(tmp_path)
    missing = tmp_path / "data" / "canonical" / "example.jsonl"

    assert missing_declared_inputs(tmp_path, registry) == (missing,)
    assert runnable_generated_data_gates(sys.executable, tmp_path, registry) == []
    assert skipped_generated_data_gates(tmp_path, registry) == {"dummy_generated_gate": (missing,)}

    missing.parent.mkdir(parents=True)
    missing.write_text("{}\n", encoding="utf-8")
    gates = load_generated_data_gates(tmp_path, registry)
    assert gates[0].args == ("--check",)
    assert runnable_generated_data_gates(sys.executable, tmp_path, registry) == [
        (
            "dummy_generated_gate.py",
            [sys.executable, str(tmp_path / "scripts" / "dummy_generated_gate.py"), "--check"],
        )
    ]


def test_validate_all_clean_mode_reports_skip_but_passes(monkeypatch, capsys) -> None:
    from scripts import validate_all

    missing = validate_all.ROOT / "data" / "canonical" / "missing.jsonl"
    monkeypatch.setattr(validate_all, "missing_declared_inputs", lambda _root: (missing,))
    monkeypatch.setattr(validate_all, "skipped_generated_data_gates", lambda _root: {"dummy": (missing,)})
    monkeypatch.setattr(validate_all, "build_gates", lambda: [])

    assert validate_all.main([]) == 0
    output = capsys.readouterr().out
    assert "skipping lifecycle-declared" in output
    assert "dummy" in output


def test_validate_all_release_mode_fails_before_gates(monkeypatch, capsys) -> None:
    from scripts import validate_all

    missing = validate_all.ROOT / "data" / "canonical" / "missing.jsonl"
    monkeypatch.setattr(validate_all, "missing_declared_inputs", lambda _root: (missing,))
    monkeypatch.setattr(
        validate_all,
        "build_gates",
        lambda: pytest.fail("release mode must stop before executing gates"),
    )

    assert validate_all.main(["--require-generated-data"]) == 1
    assert "requires every lifecycle-declared" in capsys.readouterr().err


def test_validate_all_present_but_failing_gate_remains_red(monkeypatch) -> None:
    from scripts import validate_all

    monkeypatch.setattr(validate_all, "missing_declared_inputs", lambda _root: ())
    monkeypatch.setattr(
        validate_all,
        "build_gates",
        lambda: [("failing-generated-gate", [sys.executable, "-c", "raise SystemExit(7)"])],
    )

    assert validate_all.main([]) == 1
