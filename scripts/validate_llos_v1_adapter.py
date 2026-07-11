#!/usr/bin/env python3
"""Validate the metadata-only Scripture LLOS v1 adapter."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTROL_REL = ".ai/control/llos_v1_adapter.yaml"
CONTROL = ROOT / CONTROL_REL

TEXT_SURFACES = {
    "AI_FRONT_DOOR.md": (
        CONTROL_REL,
        "LOGOS_LEARNING_LOOP_OPERATING_STANDARD.yaml",
        "may never push or write",
    ),
    "AI_TABLE_OF_CONTENTS.md": (
        CONTROL_REL,
        "llos",
        "metadata-only",
    ),
}

EXPECTED_TOP_LEVEL = {
    "object_type": "scripture_llos_v1_adapter",
    "trust_zone": "governance",
    "lifecycle_status": "active",
    "schema_version": "scripture_llos_v1_adapter.v1",
    "adapter_id": "scripture_llos_v1_metadata_only",
    "owner": "Lowell Wong",
    "validator": "scripts/validate_llos_v1_adapter.py",
}


class LlosAdapterError(ValueError):
    """Raised when the LLOS adapter crosses its metadata-only boundary."""


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise LlosAdapterError(f"{path}: unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise LlosAdapterError(f"{path}: expected a YAML mapping")
    return data


def _mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise LlosAdapterError(f"{CONTROL_REL}: {key} must be a mapping")
    return value


def _require_false(mapping: dict[str, Any], fields: tuple[str, ...], label: str) -> None:
    for field in fields:
        if mapping.get(field) is not False:
            raise LlosAdapterError(f"{CONTROL_REL}: {label}.{field} must be false")


def _require_string_list(mapping: dict[str, Any], key: str) -> set[str]:
    value = mapping.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise LlosAdapterError(f"{CONTROL_REL}: {key} must be a list of non-empty strings")
    return set(value)


def _validate_text_surfaces(root: Path) -> None:
    for rel, needles in TEXT_SURFACES.items():
        try:
            text = (root / rel).read_text(encoding="utf-8").lower()
        except OSError as exc:
            raise LlosAdapterError(f"{rel}: unreadable: {exc}") from exc
        for needle in needles:
            if needle.lower() not in text:
                raise LlosAdapterError(f"{rel}: missing LLOS adapter anchor {needle!r}")


def validate_llos_v1_adapter(path: Path = CONTROL, *, root: Path = ROOT) -> dict[str, Any]:
    data = _read_yaml(path)
    for key, expected in EXPECTED_TOP_LEVEL.items():
        if data.get(key) != expected:
            raise LlosAdapterError(f"{CONTROL_REL}: {key} must be {expected!r}")

    upstream = _mapping(data, "upstream_governance")
    expected_upstream = {
        "repository": "logos-governance-architecture",
        "path": "governance/LOGOS_LEARNING_LOOP_OPERATING_STANDARD.yaml",
        "surface_version": "1.0.0",
        "pin_type": "conceptual_surface_version",
        "consumption_mode": "reference_only",
        "source_of_truth_remains_upstream": True,
    }
    for key, expected in expected_upstream.items():
        if upstream.get(key) != expected:
            raise LlosAdapterError(f"{CONTROL_REL}: upstream_governance.{key} must be {expected!r}")

    scope = _mapping(data, "adapter_scope")
    if scope.get("mode") != "metadata_only":
        raise LlosAdapterError(f"{CONTROL_REL}: adapter_scope.mode must be 'metadata_only'")
    _require_false(
        scope,
        (
            "reads_scripture_or_canonical_data",
            "writes_scripture_or_canonical_data",
            "imports_upstream_governance_content",
            "changes_upstream_governance",
            "emits_runtime_or_retrieval_output",
        ),
        "adapter_scope",
    )

    transport = _mapping(data, "asymmetric_transport_boundary")
    logos_local = _mapping(transport, "logos_local_tooling")
    if logos_local.get("may_write_own_outbox") is not True:
        raise LlosAdapterError(f"{CONTROL_REL}: Logos-local tooling must be allowed to write its own outbox")
    if logos_local.get("may_read_or_pull_dad_central_candidates") is not True:
        raise LlosAdapterError(f"{CONTROL_REL}: Logos-local tooling must be allowed to read or pull DAD candidates")
    _require_false(logos_local, ("may_accept_dad_push_into_logos",), "asymmetric_transport_boundary.logos_local_tooling")

    dad_central = _mapping(transport, "dad_central")
    for key in ("may_read_approved_logos_outboxes", "approved_outbox_read_required", "may_write_central_dad_records"):
        if dad_central.get(key) is not True:
            raise LlosAdapterError(f"{CONTROL_REL}: asymmetric_transport_boundary.dad_central.{key} must be true")
    _require_false(
        dad_central,
        ("may_push_or_write_any_file_into_logos", "may_write_logos_inbox"),
        "asymmetric_transport_boundary.dad_central",
    )
    if dad_central.get("current_rollout_or_static_approval_cannot_authorize_dad_write_into_logos") is not True:
        raise LlosAdapterError(f"{CONTROL_REL}: rollout or static approval must not authorize DAD writes into Logos")
    if dad_central.get("future_foreground_scoped_single_use_owner_grant_required") is not True:
        raise LlosAdapterError(f"{CONTROL_REL}: future Logos writes require a scoped single-use owner grant")

    authority = _mapping(data, "authority")
    for key in ("records_adapter_metadata", "records_asymmetric_dad_transport_boundary"):
        if authority.get(key) is not True:
            raise LlosAdapterError(f"{CONTROL_REL}: authority.{key} must be true")
    _require_false(
        authority,
        (
            "authorizes_dad_write_to_logos",
            "authorizes_dad_push_into_logos",
            "authorizes_dad_write_to_logos_inbox",
            "authorizes_local_outbox_change_by_this_adapter",
            "authorizes_upstream_governance_change",
            "authorizes_scripture_data_change",
            "authorizes_canonical_or_source_data_change",
            "authorizes_candidate_promotion",
            "authorizes_runtime_or_retrieval_change",
        ),
        "authority",
    )

    stops = _require_string_list(data, "stop_conditions")
    required_stops = {
        "missing_or_ambiguous_upstream_surface_version",
        "dad_read_of_unapproved_logos_outbox",
        "request_for_dad_push_or_write_of_any_file_into_logos",
        "request_to_change_upstream_governance_from_this_repository",
        "request_to_modify_scripture_or_canonical_source_data",
    }
    if not required_stops <= stops:
        raise LlosAdapterError(f"{CONTROL_REL}: stop_conditions are incomplete")

    non_authorizations = _require_string_list(data, "non_authorizations")
    required_non_authorizations = {
        "dad_push_or_write_of_any_file_into_logos",
        "dad_write_to_logos_inbox",
        "local_outbox_change_by_this_adapter",
        "upstream_governance_change",
        "canonical_or_source_data_change",
        "candidate_promotion",
        "runtime_or_retrieval_output_change",
    }
    if not required_non_authorizations <= non_authorizations:
        raise LlosAdapterError(f"{CONTROL_REL}: non_authorizations are incomplete")

    _validate_text_surfaces(root)
    return data


def main() -> int:
    try:
        validate_llos_v1_adapter()
    except LlosAdapterError as exc:
        print(f"Scripture LLOS v1 adapter validation failed: {exc}")
        return 1
    print("Scripture LLOS v1 adapter validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
