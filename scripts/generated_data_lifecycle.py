#!/usr/bin/env python3
"""Resolve generated-data validation gates from the governed lifecycle registry.

This module performs orchestration only. It never reads, writes, copies, links, or
regenerates canonical sidecars. Missing ignored artifacts are a clean-checkout
availability state; present artifacts remain subject to their existing validators.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
LIFECYCLE = ROOT / ".ai" / "control" / "validation_gate_lifecycle.yaml"


class GeneratedDataLifecycleError(ValueError):
    """Raised when generated-data lifecycle metadata cannot be scheduled safely."""


def _canonical_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and path.parts[:2] == ("data", "canonical")
        and ".." not in path.parts
        and "\\" not in value
    )


@dataclass(frozen=True)
class GeneratedDataGate:
    gate_id: str
    command: str
    args: tuple[str, ...]
    required_inputs: tuple[str, ...]
    missing_input_behavior: str

    def missing_inputs(self, root: Path = ROOT) -> tuple[Path, ...]:
        return tuple(root / item for item in self.required_inputs if not (root / item).is_file())

    def argv(self, python: str, root: Path = ROOT) -> list[str]:
        return [python, str(root / self.command), *self.args]

    @property
    def display_name(self) -> str:
        return Path(self.command).name


def _read_registry(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise GeneratedDataLifecycleError(f"generated-data lifecycle registry is unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise GeneratedDataLifecycleError("generated-data lifecycle registry must be a YAML mapping")
    return data


def load_generated_data_gates(
    root: Path = ROOT,
    lifecycle_path: Path | None = None,
) -> tuple[GeneratedDataGate, ...]:
    path = lifecycle_path or root / ".ai" / "control" / "validation_gate_lifecycle.yaml"
    data = _read_registry(path)
    rows = data.get("tracked_gates")
    if not isinstance(rows, list):
        raise GeneratedDataLifecycleError("tracked_gates must be a list")

    gates: list[GeneratedDataGate] = []
    seen_ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or row.get("status") != "active_generated_data":
            continue
        gate_id = row.get("gate_id")
        command = row.get("command")
        args = row.get("args", [])
        required_inputs = row.get("required_inputs")
        behavior = row.get("missing_input_behavior")
        if not isinstance(gate_id, str) or not gate_id or gate_id in seen_ids:
            raise GeneratedDataLifecycleError(f"invalid or duplicate generated-data gate ID: {gate_id!r}")
        command_path = (root / command).resolve() if isinstance(command, str) else None
        scripts_root = (root / "scripts").resolve()
        if (
            not isinstance(command, str)
            or command_path is None
            or not command_path.is_relative_to(scripts_root)
            or not command_path.is_file()
        ):
            raise GeneratedDataLifecycleError(f"{gate_id}: command is missing or outside scripts/: {command!r}")
        if not isinstance(args, list) or not all(isinstance(item, str) and item for item in args):
            raise GeneratedDataLifecycleError(f"{gate_id}: args must contain only non-empty strings")
        if not isinstance(required_inputs, list) or not required_inputs:
            raise GeneratedDataLifecycleError(f"{gate_id}: required_inputs must be a non-empty list")
        if not all(isinstance(item, str) and _canonical_relative_path(item) for item in required_inputs):
            raise GeneratedDataLifecycleError(f"{gate_id}: every required input must be under data/canonical/")
        if behavior not in {"skip_when_ignored_generated_data_absent", "require_before_release"}:
            raise GeneratedDataLifecycleError(f"{gate_id}: unsupported missing_input_behavior {behavior!r}")
        seen_ids.add(gate_id)
        gates.append(
            GeneratedDataGate(
                gate_id=gate_id,
                command=command,
                args=tuple(args),
                required_inputs=tuple(required_inputs),
                missing_input_behavior=str(behavior),
            )
        )
    if not gates:
        raise GeneratedDataLifecycleError("no active generated-data gates are declared")
    return tuple(gates)


def declared_generated_inputs(
    root: Path = ROOT,
    lifecycle_path: Path | None = None,
) -> tuple[Path, ...]:
    inputs = {
        root / item
        for gate in load_generated_data_gates(root, lifecycle_path)
        for item in gate.required_inputs
    }
    return tuple(sorted(inputs, key=lambda path: path.as_posix()))


def missing_declared_inputs(
    root: Path = ROOT,
    lifecycle_path: Path | None = None,
) -> tuple[Path, ...]:
    return tuple(path for path in declared_generated_inputs(root, lifecycle_path) if not path.is_file())


def runnable_generated_data_gates(
    python: str,
    root: Path = ROOT,
    lifecycle_path: Path | None = None,
) -> list[tuple[str, list[str]]]:
    return [
        (gate.display_name, gate.argv(python, root))
        for gate in load_generated_data_gates(root, lifecycle_path)
        if not gate.missing_inputs(root)
    ]


def skipped_generated_data_gates(
    root: Path = ROOT,
    lifecycle_path: Path | None = None,
) -> dict[str, tuple[Path, ...]]:
    return {
        gate.gate_id: gate.missing_inputs(root)
        for gate in load_generated_data_gates(root, lifecycle_path)
        if gate.missing_inputs(root)
    }
