#!/usr/bin/env python3
"""Validate the textual-critical policy requirement docket."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCKET = ROOT / ".ai" / "control" / "textual_critical_policy_docket.yaml"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_textual_critical_decision",
    "authorizes_preferred_reading",
    "authorizes_canon_scope_change",
    "authorizes_source_tradition_preference",
    "authorizes_noncanonical_source_authority",
    "authorizes_boundary_import",
    "authorizes_reviewed_gold",
    "authorizes_chunk_boundaries",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_output_change",
}

REQUIRED_SURFACES = {
    "Mark.16.9-Mark.16.20",
    "John.7.53-John.8.11",
    "Deut.32.8-Deut.32.9",
    "Jude noncanonical references",
    "1John.5.6-1John.5.8",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "textual_critical_preferred_reading",
    "canon_scope_change",
    "source_tradition_preference",
    "noncanonical_source_authority",
    "boundary_import",
    "variant_packet_as_reviewed_gold",
    "graph_edge_generation",
    "retrieval_truth",
    "chunk_output_change",
}


class TextualCriticalPolicyError(ValueError):
    """Raised when the textual-critical policy docket is invalid."""


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
        raise TextualCriticalPolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise TextualCriticalPolicyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise TextualCriticalPolicyError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise TextualCriticalPolicyError(f"{label} missing {missing}")


def validate_textual_critical_policy(path: Path = DOCKET) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "textual_critical_policy_docket":
        raise TextualCriticalPolicyError(f"{_rel(path)}: object_type must be textual_critical_policy_docket")
    if data.get("trust_zone") != "canonical":
        raise TextualCriticalPolicyError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise TextualCriticalPolicyError(f"{_rel(path)}: lifecycle_status must be active")
    if data.get("schema_version") != "textual_critical_policy_docket.v1":
        raise TextualCriticalPolicyError(f"{_rel(path)}: schema_version must be textual_critical_policy_docket.v1")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise TextualCriticalPolicyError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_policy_requirement", "may_surface_for_review", "requires_policy_before_variant_sensitive_promotion"):
        if authority.get(key) is not True:
            raise TextualCriticalPolicyError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise TextualCriticalPolicyError(f"{_rel(path)}: authority.{key} must be false")

    policy_status = data.get("policy_status")
    if not isinstance(policy_status, dict):
        raise TextualCriticalPolicyError(f"{_rel(path)}: policy_status must be a mapping")
    if policy_status.get("textual_critical_policy_selected") is not False:
        raise TextualCriticalPolicyError(f"{_rel(path)}: textual_critical_policy_selected must be false")
    if policy_status.get("selected_policy") != "pending_owner_decision":
        raise TextualCriticalPolicyError(f"{_rel(path)}: selected_policy must be pending_owner_decision")
    if policy_status.get("owner_decision_required") is not True:
        raise TextualCriticalPolicyError(f"{_rel(path)}: owner_decision_required must be true")

    _require_subset(REQUIRED_SURFACES, data.get("variant_sensitive_surfaces"), "variant_sensitive_surfaces")
    _require_subset(
        {"explicit_owner_textual_critical_policy", "exact_scope", "decision_register_update"},
        data.get("required_before_use"),
        "required_before_use",
    )
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    return data


def main() -> int:
    try:
        validate_textual_critical_policy()
    except TextualCriticalPolicyError as exc:
        print(f"Textual-critical policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("Textual-critical policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
