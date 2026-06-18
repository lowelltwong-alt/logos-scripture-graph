#!/usr/bin/env python3
"""Validate no-context audit surfaces and harness entry points."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / ".ai" / "control" / "audit_surface_map.yaml"
HARNESS_ROADMAP = ROOT / ".ai" / "control" / "harness_upgrade_roadmap.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "map_id",
    "owner",
    "authority",
    "required_entrypoints",
    "required_changelogs",
    "required_decision_surfaces",
    "required_harness",
    "future_harness_roadmap",
    "audit_dimensions",
    "stop_conditions",
    "validator",
}

REQUIRED_ENTRYPOINTS = {
    "AI_FRONT_DOOR.md",
    ".ai/audits/README.md",
    ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md",
    ".ai/audits/templates/REVIEW_REPORT_TEMPLATE.md",
    ".ai/audits/reports/README.md",
}

REQUIRED_CHANGELOGS = {
    ".ai/control/roadmap_events.jsonl",
    ".ai/control/handoff_ledger.jsonl",
    ".ai/control/PROJECT_STATUS.md",
    "ROADMAP_STATE.yaml",
}

REQUIRED_DECISION_SURFACES = {
    ".ai/control/chunking_theological_decision_register.yaml",
    ".ai/control/governance_memory_durability_policy.yaml",
    ".ai/control/owner_decision_projection_policy.yaml",
    ".ai/control/bible_chunking_readiness_map.yaml",
    ".ai/control/chunking_agent_preflight.yaml",
    "eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md",
}

REQUIRED_HARNESS = {
    "scripts/validate_audit_surface_map.py",
    "scripts/agent/no_context_audit_harness.py",
}

REQUIRED_HARNESS_CANDIDATES = {
    "HARN-001",
    "HARN-002",
    "HARN-003",
    "HARN-004",
    "HARN-005",
    "HARN-006",
    "HARN-007",
    "HARN-008",
    "HARN-009",
    "HARN-010",
    "HARN-011",
    "HARN-012",
}

REQUIRED_DIMENSIONS = {
    "task_intent",
    "changed_files",
    "scope_boundaries",
    "protected_paths",
    "owner_decisions",
    "theological_downstream_decisions",
    "dependency_and_readiness_state",
    "lesson_capture",
    "non_authorizations",
    "validation_evidence",
    "next_action",
}

REQUIRED_STOP_CONDITIONS = {
    "chat_only_claim",
    "raw_or_canonical_mutation_without_authorization",
    "generated_chunk_or_evaluator_change_without_authorization",
    "pending_packet_treated_as_reviewed_gold",
    "owner_selection_docket_treated_as_owner_decision",
    "theological_downstream_decision_missing_register_entry",
    "master_context_changed_without_human_lock",
}


class AuditSurfaceError(ValueError):
    """Raised when audit-surface governance is invalid."""


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
        raise AuditSurfaceError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise AuditSurfaceError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AuditSurfaceError(f"{_rel(path)}: unreadable: {exc}") from exc


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise AuditSurfaceError(f"{label} must be a list")
    actual_set = {str(item) for item in actual}
    missing = sorted(required - actual_set)
    if missing:
        raise AuditSurfaceError(f"{label} missing {missing}")


def _require_paths(paths: set[str]) -> None:
    missing = sorted(path for path in paths if not (ROOT / path).exists())
    if missing:
        raise AuditSurfaceError(f"required audit paths missing {missing}")


def _validate_harness_roadmap(path: Path = HARNESS_ROADMAP) -> None:
    data = _read_yaml(path)
    for key in (
        "object_type",
        "trust_zone",
        "lifecycle_status",
        "schema_version",
        "map_id",
        "authority",
        "upgrade_policy",
        "candidate_harnesses",
        "watchlist",
    ):
        if key not in data:
            raise AuditSurfaceError(f"{_rel(path)}: missing {key}")
    if data["object_type"] != "harness_upgrade_roadmap":
        raise AuditSurfaceError(f"{_rel(path)}: object_type must be harness_upgrade_roadmap")
    if data["trust_zone"] != "canonical":
        raise AuditSurfaceError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise AuditSurfaceError(f"{_rel(path)}: lifecycle_status must be active")
    authority = data["authority"]
    if not isinstance(authority, dict):
        raise AuditSurfaceError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_future_harness_needs") is not True:
        raise AuditSurfaceError(f"{_rel(path)}: authority.records_future_harness_needs must be true")
    for key in (
        "authorizes_harness_implementation",
        "authorizes_chunk_output_change",
        "authorizes_reviewed_gold_promotion",
        "authorizes_owner_decision",
    ):
        if authority.get(key) is not False:
            raise AuditSurfaceError(f"{_rel(path)}: authority.{key} must be false")
    candidates = data["candidate_harnesses"]
    if not isinstance(candidates, list) or not candidates:
        raise AuditSurfaceError(f"{_rel(path)}: candidate_harnesses must be a non-empty list")
    candidate_ids = {str(item.get("harness_id")) for item in candidates if isinstance(item, dict)}
    missing = sorted(REQUIRED_HARNESS_CANDIDATES - candidate_ids)
    if missing:
        raise AuditSurfaceError(f"{_rel(path)}: missing candidate harnesses {missing}")
    for item in candidates:
        if not isinstance(item, dict):
            raise AuditSurfaceError(f"{_rel(path)}: each candidate harness must be a mapping")
        label = f"{_rel(path)}:{item.get('harness_id', '<missing>')}"
        for key in ("harness_id", "title", "status", "trigger", "purpose", "non_authorizations"):
            if key not in item:
                raise AuditSurfaceError(f"{label}: missing {key}")
        if not isinstance(item["non_authorizations"], list) or not item["non_authorizations"]:
            raise AuditSurfaceError(f"{label}: non_authorizations must be a non-empty list")
        if str(item["status"]).startswith("implemented"):
            surfaces = item.get("implemented_surfaces")
            if not isinstance(surfaces, list) or not surfaces:
                raise AuditSurfaceError(f"{label}: implemented_surfaces must be a non-empty list")
            missing = sorted(str(surface) for surface in surfaces if not (ROOT / str(surface)).exists())
            if missing:
                raise AuditSurfaceError(f"{label}: implemented_surfaces missing paths {missing}")
    if not isinstance(data["watchlist"], list) or not data["watchlist"]:
        raise AuditSurfaceError(f"{_rel(path)}: watchlist must be a non-empty list")


def validate_audit_surface_map(path: Path = MAP) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise AuditSurfaceError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "audit_surface_map":
        raise AuditSurfaceError(f"{_rel(path)}: object_type must be audit_surface_map")
    if data["trust_zone"] != "canonical":
        raise AuditSurfaceError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise AuditSurfaceError(f"{_rel(path)}: lifecycle_status must be active")
    if data["validator"] != "scripts/validate_audit_surface_map.py":
        raise AuditSurfaceError(f"{_rel(path)}: validator path is wrong")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise AuditSurfaceError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_audit_surfaces") is not True:
        raise AuditSurfaceError(f"{_rel(path)}: authority.records_audit_surfaces must be true")
    for key in (
        "authorizes_code_change",
        "authorizes_chunk_output_change",
        "authorizes_reviewed_gold_promotion",
        "authorizes_owner_decision",
    ):
        if authority.get(key) is not False:
            raise AuditSurfaceError(f"{_rel(path)}: authority.{key} must be false")

    _require_subset(REQUIRED_ENTRYPOINTS, data["required_entrypoints"], "required_entrypoints")
    _require_subset(REQUIRED_CHANGELOGS, data["required_changelogs"], "required_changelogs")
    _require_subset(REQUIRED_DECISION_SURFACES, data["required_decision_surfaces"], "required_decision_surfaces")
    _require_subset(REQUIRED_HARNESS, data["required_harness"], "required_harness")
    _require_subset(REQUIRED_DIMENSIONS, data["audit_dimensions"], "audit_dimensions")
    _require_subset(REQUIRED_STOP_CONDITIONS, data["stop_conditions"], "stop_conditions")

    roadmap_rel = str(data["future_harness_roadmap"])
    if roadmap_rel != ".ai/control/harness_upgrade_roadmap.yaml":
        raise AuditSurfaceError(f"{_rel(path)}: future_harness_roadmap path is wrong")
    _require_paths(
        REQUIRED_ENTRYPOINTS
        | REQUIRED_CHANGELOGS
        | REQUIRED_DECISION_SURFACES
        | REQUIRED_HARNESS
        | {roadmap_rel}
    )
    _validate_harness_roadmap(ROOT / roadmap_rel)

    front_door = _read_text(FRONT_DOOR)
    for phrase in (
        ".ai/audits/README.md",
        ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md",
        "no-context",
    ):
        if phrase not in front_door:
            raise AuditSurfaceError(f"{_rel(FRONT_DOOR)}: missing audit phrase {phrase!r}")

    toc = _read_text(TOC)
    for phrase in (
        ".ai/audits/README.md",
        ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md",
        ".ai/audits/templates/REVIEW_REPORT_TEMPLATE.md",
        ".ai/control/harness_upgrade_roadmap.yaml",
    ):
        if phrase not in toc:
            raise AuditSurfaceError(f"{_rel(TOC)}: missing audit TOC phrase {phrase!r}")

    lessons = _read_text(LESSONS)
    if "WORKFLOW-LESSON-003 - No-Context Review Requires A Repo-Resident Audit Path" not in lessons:
        raise AuditSurfaceError(f"{_rel(LESSONS)}: missing no-context audit workflow lesson")

    return data


def main() -> int:
    try:
        validate_audit_surface_map()
    except AuditSurfaceError as exc:
        print(f"Audit surface map validation failed: {exc}", file=sys.stderr)
        return 1
    print("Audit surface map validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
