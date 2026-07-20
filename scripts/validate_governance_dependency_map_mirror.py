#!/usr/bin/env python3
"""Validate the local mirror of the upstream Logos governance dependency map."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / ".ai" / "control" / "governance_dependency_map_mirror.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
README = ROOT / "README.md"
CONTRACT = ROOT / "config" / "governance" / "repository_link_contract.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "mirror_id",
    "owner_repo",
    "upstream_dependency_map",
    "local_enforcement",
    "authority",
    "watched_local_governance_surfaces",
    "required_behavior",
}

REQUIRED_WATCHED = {
    "AI_FRONT_DOOR.md",
    "AI_TABLE_OF_CONTENTS.md",
    "README.md",
    "config/governance/",
    ".ai/control/boundary_material_routing.yaml",
    ".ai/control/governance_dependency_map_mirror.yaml",
    "scripts/validate_governance_dependency_map_mirror.py",
    "scripts/validate_mirror_freshness.py",
    "scripts/validate_repository_link_contract.py",
    "scripts/validate_all.py",
    "tests/test_governance_dependency_map_mirror.py",
    "tests/test_mirror_freshness.py",
}

REQUIRED_SURFACE_PHRASES = {
    FRONT_DOOR: [
        "governance dependency-map mirror",
        ".ai/control/governance_dependency_map_mirror.yaml",
        "logos-governance-architecture/governance/GOVERNANCE_DEPENDENCY_MAP.yaml",
    ],
    TOC: [
        ".ai/control/governance_dependency_map_mirror.yaml",
        "scripts/validate_governance_dependency_map_mirror.py",
        "scripts/validate_mirror_freshness.py",
    ],
    README: [
        ".ai/control/governance_dependency_map_mirror.yaml",
        "upstream governance dependency map",
    ],
    CONTRACT: [
        "governance_dependency_map_mirror",
        "GD-014",
        "governance/GOVERNANCE_DEPENDENCY_MAP.yaml",
    ],
    VALIDATE_ALL: [
        "validate_governance_dependency_map_mirror.py",
        "validate_mirror_freshness.py",
    ],
}


class MirrorValidationError(ValueError):
    """Raised when the local governance dependency-map mirror is invalid."""


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise MirrorValidationError(f"{_rel(path)} unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise MirrorValidationError(f"{_rel(path)} must be a YAML mapping")
    return data


def _require_strings(data: dict[str, Any], key: str, label: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise MirrorValidationError(f"{label}.{key} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise MirrorValidationError(f"{label}.{key} must contain only non-empty strings")
    return value


def validate_governance_dependency_map_mirror(path: Path = MIRROR) -> dict[str, Any]:
    data = _read_yaml(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise MirrorValidationError(f"{_rel(path)} missing keys: {missing}")
    if data["object_type"] != "governance_dependency_map_mirror":
        raise MirrorValidationError(f"{_rel(path)} object_type must be governance_dependency_map_mirror")
    if data["owner_repo"] != "logos-scripture-graph":
        raise MirrorValidationError(f"{_rel(path)} owner_repo must be logos-scripture-graph")

    upstream = data["upstream_dependency_map"]
    if not isinstance(upstream, dict):
        raise MirrorValidationError(f"{_rel(path)} upstream_dependency_map must be a mapping")
    expected_upstream = {
        "repo": "logos-governance-architecture",
        "path": "governance/GOVERNANCE_DEPENDENCY_MAP.yaml",
        "artifact_id": "GD-014",
        "rule": "governance_map_update_gate",
        "source_of_truth": True,
    }
    for key, expected in expected_upstream.items():
        if upstream.get(key) != expected:
            raise MirrorValidationError(f"{_rel(path)} upstream_dependency_map.{key} must be {expected!r}")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise MirrorValidationError(f"{_rel(path)} authority must be a mapping")
    for key in (
        "local_repo_may_override_upstream_dependency_map",
        "local_repo_may_weaken_upstream_governance",
        "local_repo_may_treat_scripture_data_need_as_governance_authority",
    ):
        if authority.get(key) is not False:
            raise MirrorValidationError(f"{_rel(path)} authority.{key} must be false")
    if authority.get("local_repo_must_stop_if_upstream_map_conflicts") is not True:
        raise MirrorValidationError(f"{_rel(path)} authority.local_repo_must_stop_if_upstream_map_conflicts must be true")

    watched = set(_require_strings(data, "watched_local_governance_surfaces", _rel(path)))
    missing_watched = sorted(REQUIRED_WATCHED - watched)
    if missing_watched:
        raise MirrorValidationError(f"{_rel(path)} missing watched surfaces: {missing_watched}")

    enforcement = data["local_enforcement"]
    if not isinstance(enforcement, dict):
        raise MirrorValidationError(f"{_rel(path)} local_enforcement must be a mapping")
    for rel in enforcement.values():
        if isinstance(rel, str) and rel.endswith((".md", ".py", ".yaml")) and not (ROOT / rel).exists():
            raise MirrorValidationError(f"{_rel(path)} references missing local enforcement surface: {rel}")

    for surface, phrases in REQUIRED_SURFACE_PHRASES.items():
        text = surface.read_text(encoding="utf-8")
        missing_phrases = [phrase for phrase in phrases if phrase not in text]
        if missing_phrases:
            raise MirrorValidationError(f"{_rel(surface)} missing phrase(s): {missing_phrases}")

    return data


def main() -> int:
    try:
        validate_governance_dependency_map_mirror()
    except MirrorValidationError as exc:
        print(f"Governance dependency-map mirror validation failed: {exc}", file=sys.stderr)
        return 1
    print("Governance dependency-map mirror validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
