#!/usr/bin/env python3
"""Validate protected governance memory surfaces."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.validate_chunking_theological_decision_register import validate_register  # noqa: E402

POLICY = ROOT / ".ai" / "control" / "governance_memory_durability_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
AUDIT_MAP = ROOT / ".ai" / "control" / "audit_surface_map.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
TASK_SCOPE = ROOT / "scripts" / "validate_task_scope.py"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "policy_id",
    "owner",
    "authority",
    "protected_memory_surfaces",
    "required_task_scope_protection",
    "non_authorizations",
    "validators",
}

REQUIRED_DISCOVERY = {
    "AI_FRONT_DOOR.md": FRONT_DOOR,
    "AI_TABLE_OF_CONTENTS.md": TOC,
    "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md": ROADMAP_TOC,
    ".ai/control/audit_surface_map.yaml": AUDIT_MAP,
    ".ai/control/chunking_agent_preflight.yaml": PREFLIGHT,
    ".ai/control/bible_chunking_readiness_map.yaml": READINESS,
}

REQUIRED_VALIDATORS = {
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_governance_memory_durability.py",
    "scripts/validate_task_scope.py",
    "scripts/validate_all.py",
}


class GovernanceMemoryError(ValueError):
    """Raised when protected governance memory is not durable."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GovernanceMemoryError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise GovernanceMemoryError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise GovernanceMemoryError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise GovernanceMemoryError(f"{label} must be a list")
    actual_set = {str(item) for item in actual}
    missing = sorted(required - actual_set)
    if missing:
        raise GovernanceMemoryError(f"{label} missing {missing}")


def validate_governance_memory_durability(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise GovernanceMemoryError(f"{_rel(path)}: missing top-level keys {missing}")

    if data["object_type"] != "governance_memory_durability_policy":
        raise GovernanceMemoryError(f"{_rel(path)}: object_type must be governance_memory_durability_policy")
    if data["trust_zone"] != "canonical":
        raise GovernanceMemoryError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise GovernanceMemoryError(f"{_rel(path)}: lifecycle_status must be active")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise GovernanceMemoryError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_protected_memory_surfaces") is not True:
        raise GovernanceMemoryError(f"{_rel(path)}: authority.records_protected_memory_surfaces must be true")
    for key in (
        "authorizes_register_deletion",
        "authorizes_register_downgrade",
        "authorizes_chunk_output_change",
        "authorizes_reviewed_gold_promotion",
        "authorizes_owner_decision",
    ):
        if authority.get(key) is not False:
            raise GovernanceMemoryError(f"{_rel(path)}: authority.{key} must be false")

    surfaces = data["protected_memory_surfaces"]
    if not isinstance(surfaces, list) or not surfaces:
        raise GovernanceMemoryError(f"{_rel(path)}: protected_memory_surfaces must be a non-empty list")
    by_id = {surface.get("surface_id"): surface for surface in surfaces if isinstance(surface, dict)}
    register_surface = by_id.get("chunking_theological_decision_register")
    if not isinstance(register_surface, dict):
        raise GovernanceMemoryError(f"{_rel(path)}: missing chunking_theological_decision_register surface")
    if register_surface.get("path") != ".ai/control/chunking_theological_decision_register.yaml":
        raise GovernanceMemoryError(f"{_rel(path)}: register path is wrong")
    if register_surface.get("protection_level") != "critical_non_deletable_governance_memory":
        raise GovernanceMemoryError(f"{_rel(path)}: register protection_level is wrong")
    _require_subset(set(REQUIRED_DISCOVERY), register_surface.get("must_be_discoverable_from"), "must_be_discoverable_from")
    _require_subset(REQUIRED_VALIDATORS, register_surface.get("required_validators"), "required_validators")

    if not REGISTER.exists():
        raise GovernanceMemoryError(f"{_rel(REGISTER)}: protected decision register is missing")
    register = validate_register(REGISTER)
    if register["object_type"] != "chunking_theological_decision_register":
        raise GovernanceMemoryError(f"{_rel(REGISTER)}: wrong object_type")
    if register["trust_zone"] != "canonical" or register["lifecycle_status"] != "active":
        raise GovernanceMemoryError(f"{_rel(REGISTER)}: register must remain canonical and active")

    register_rel = ".ai/control/chunking_theological_decision_register.yaml"
    for label, target in REQUIRED_DISCOVERY.items():
        text = _read_text(target)
        if register_rel not in text:
            raise GovernanceMemoryError(f"{label}: missing protected register reference")

    validate_all_text = _read_text(VALIDATE_ALL)
    for validator in (
        "validate_chunking_theological_decision_register.py",
        "validate_governance_memory_durability.py",
    ):
        if validator not in validate_all_text:
            raise GovernanceMemoryError(f"{_rel(VALIDATE_ALL)}: missing {validator}")

    task_scope_text = _read_text(TASK_SCOPE)
    for protected_path in (
        ".ai/control/chunking_theological_decision_register.yaml",
        ".ai/control/governance_memory_durability_policy.yaml",
        ".ai/control/owner_decision_projection_policy.yaml",
    ):
        if protected_path not in task_scope_text:
            raise GovernanceMemoryError(f"{_rel(TASK_SCOPE)}: missing protected path {protected_path}")

    _require_subset(
        {
            "register_deletion",
            "register_rename_without_supersession",
            "register_trust_zone_downgrade",
            "hiding_register_from_front_door_or_toc",
            "bypassing_register_validator",
        },
        data["non_authorizations"],
        "non_authorizations",
    )
    return data


def main() -> int:
    try:
        validate_governance_memory_durability()
    except GovernanceMemoryError as exc:
        print(f"Governance memory durability validation failed: {exc}", file=sys.stderr)
        return 1
    print("Governance memory durability validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
