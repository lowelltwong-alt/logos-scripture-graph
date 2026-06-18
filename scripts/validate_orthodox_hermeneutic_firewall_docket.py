#!/usr/bin/env python3
"""Validate the Orthodox Hermeneutic Firewall / Anti-Smuggling Docket."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCKET = ROOT / ".ai" / "control" / "orthodox_hermeneutic_firewall_docket.yaml"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_denominational_system_as_chunk_authority",
    "authorizes_liberal_critical_default",
    "authorizes_anti_supernatural_default",
    "authorizes_anti_canonical_default",
    "authorizes_heterodox_default",
    "authorizes_doctrinal_system_selection",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_output_change",
}

REQUIRED_RULES = {
    "FIREWALL-ORTH-001",
    "FIREWALL-ORTH-002",
    "FIREWALL-ORTH-003",
    "FIREWALL-ORTH-004",
    "FIREWALL-ORTH-005",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "denominational_system_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
    "anti_canonical_default",
    "heterodox_default",
    "doctrinal_system_selection",
    "reviewed_gold_promotion",
    "route_behavior_change",
    "evaluator_change",
    "chunk_output_change",
}


class OrthodoxFirewallError(ValueError):
    """Raised when the orthodox firewall docket is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise OrthodoxFirewallError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise OrthodoxFirewallError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise OrthodoxFirewallError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise OrthodoxFirewallError(f"{label} missing {missing}")


def validate_orthodox_firewall(path: Path = DOCKET) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "orthodox_hermeneutic_firewall_docket":
        raise OrthodoxFirewallError(f"{_rel(path)}: object_type must be orthodox_hermeneutic_firewall_docket")
    if data.get("trust_zone") != "canonical":
        raise OrthodoxFirewallError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise OrthodoxFirewallError(f"{_rel(path)}: lifecycle_status must be active")
    if data.get("schema_version") != "orthodox_hermeneutic_firewall_docket.v1":
        raise OrthodoxFirewallError(f"{_rel(path)}: schema_version must be orthodox_hermeneutic_firewall_docket.v1")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise OrthodoxFirewallError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_orthodox_firewall", "records_anti_smuggling_rules", "may_surface_for_review"):
        if authority.get(key) is not True:
            raise OrthodoxFirewallError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise OrthodoxFirewallError(f"{_rel(path)}: authority.{key} must be false")

    affirmations = data.get("affirmations")
    if not isinstance(affirmations, dict):
        raise OrthodoxFirewallError(f"{_rel(path)}: affirmations must be a mapping")
    if affirmations.get("orthodoxy_boundary") != "Nicene/Chalcedonian orthodox Christianity":
        raise OrthodoxFirewallError(f"{_rel(path)}: orthodoxy_boundary must be Nicene/Chalcedonian orthodox Christianity")
    scripture_authority = str(affirmations.get("scripture_authority", ""))
    if "Canonical Scripture" not in scripture_authority or "authority" not in scripture_authority:
        raise OrthodoxFirewallError(f"{_rel(path)}: scripture_authority must affirm canonical Scripture authority")

    rule_ids = {
        str(item.get("rule_id"))
        for item in data.get("anti_smuggling_rules", [])
        if isinstance(item, dict)
    }
    missing_rules = sorted(REQUIRED_RULES - rule_ids)
    if missing_rules:
        raise OrthodoxFirewallError(f"{_rel(path)}: missing anti-smuggling rules {missing_rules}")
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")

    preserved = set(str(item) for item in data.get("preserved_options", []))
    if "orthodox_reformed_readings" not in preserved or "orthodox_arminian_wesleyan_readings" not in preserved:
        raise OrthodoxFirewallError(f"{_rel(path)}: preserved_options must include multiple orthodox options")
    return data


def main() -> int:
    try:
        validate_orthodox_firewall()
    except OrthodoxFirewallError as exc:
        print(f"Orthodox firewall validation failed: {exc}", file=sys.stderr)
        return 1
    print("Orthodox firewall validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
