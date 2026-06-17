#!/usr/bin/env python3
"""Validate the Scripture chunking theological decision register."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"

ALLOWED_CLASSIFICATIONS = {
    "text_neutral",
    "theological_risk",
    "interpretive_boundary",
    "canon_scope",
    "non_authorizing_review",
}

REQUIRED_SEED_DECISIONS = {
    "canonical 66 scope": "CD-004",
    "Psalm 78 parent/child": "CD-006",
    "Psalm 89 Option C": "CD-008",
    "WJ marker limits": "CD-002",
    "Revelation non-implementation": "CD-010",
    "Psalm candidate non-promotion": "CD-009",
    "Vector/edge never truth": "CD-011",
}

WATCHED_PREFIXES = (
    "pipelines/chunking/",
    "config/chunking/",
    "registry/chunking/",
    "eval/chunking_gold/",
    "data/derived/chunks/",
    "docs/roadmap/",
)

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "register_id",
    "owner",
    "default_orthodoxy_boundary",
    "register_authority",
    "update_policy",
    "allowed_classifications",
    "decisions",
    "no_impact_markers",
    "backfill_coverage",
}

REQUIRED_DECISION_FIELDS = {
    "decision_id",
    "title",
    "classification",
    "task_ids",
    "owner_decision_ref",
    "pr_refs",
    "affected_scope",
    "decision",
    "downstream_risk",
    "theological_assumptions_avoided",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validators",
    "lifecycle_status",
    "supersedes",
    "deprecated_by",
}


class RegisterError(ValueError):
    """Raised when the decision register is invalid."""


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
        raise RegisterError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise RegisterError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_nonempty_string(container: dict[str, Any], key: str, label: str) -> None:
    if not isinstance(container.get(key), str) or not container[key].strip():
        raise RegisterError(f"{label}: {key} must be a non-empty string")


def _require_string_list(container: dict[str, Any], key: str, label: str, *, allow_empty: bool = False) -> None:
    value = container.get(key)
    if not isinstance(value, list) or (not allow_empty and not value):
        raise RegisterError(f"{label}: {key} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise RegisterError(f"{label}: {key} must contain only non-empty strings")


def _normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith("./"):
        return normalized[2:]
    return normalized


def _git_changed_files(base_ref: str) -> list[str]:
    try:
        merge_base = subprocess.check_output(
            ["git", "merge-base", "HEAD", base_ref],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        output = subprocess.check_output(
            ["git", "diff", "--name-only", f"{merge_base}...HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [_normalize_path(line) for line in output.splitlines() if line.strip()]


def validate_register(path: Path = REGISTER) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise RegisterError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "chunking_theological_decision_register":
        raise RegisterError(f"{_rel(path)}: object_type must be chunking_theological_decision_register")
    if data["trust_zone"] != "canonical":
        raise RegisterError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise RegisterError(f"{_rel(path)}: lifecycle_status must be active")
    if data["default_orthodoxy_boundary"] != "nicene_chalcedonian_core":
        raise RegisterError(f"{_rel(path)}: default_orthodoxy_boundary must be nicene_chalcedonian_core")

    authority = data["register_authority"]
    if not isinstance(authority, dict):
        raise RegisterError(f"{_rel(path)}: register_authority must be a mapping")
    if authority.get("records_decisions") is not True:
        raise RegisterError(f"{_rel(path)}: register_authority.records_decisions must be true")
    for forbidden in (
        "authorizes_chunk_output_change",
        "authorizes_reviewed_gold_promotion",
        "authorizes_skill_lifecycle_promotion",
        "authorizes_boundary_import",
    ):
        if authority.get(forbidden) is not False:
            raise RegisterError(f"{_rel(path)}: register_authority.{forbidden} must be false")

    classifications = data["allowed_classifications"]
    if set(classifications) != ALLOWED_CLASSIFICATIONS:
        raise RegisterError(
            f"{_rel(path)}: allowed_classifications must match {sorted(ALLOWED_CLASSIFICATIONS)}"
        )

    decisions = data["decisions"]
    if not isinstance(decisions, list) or not decisions:
        raise RegisterError(f"{_rel(path)}: decisions must be a non-empty list")

    decision_ids: set[str] = set()
    covered_tasks: set[str] = set()
    for decision in decisions:
        if not isinstance(decision, dict):
            raise RegisterError(f"{_rel(path)}: each decision must be a mapping")
        decision_id = str(decision.get("decision_id", "<missing>"))
        label = f"{_rel(path)}:{decision_id}"
        missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
        if missing:
            raise RegisterError(f"{label}: missing keys {missing}")
        if decision_id in decision_ids:
            raise RegisterError(f"{label}: duplicate decision_id")
        decision_ids.add(decision_id)
        if decision.get("classification") not in ALLOWED_CLASSIFICATIONS:
            raise RegisterError(f"{label}: invalid classification {decision.get('classification')!r}")
        for key in ("title", "owner_decision_ref", "decision", "downstream_risk", "reviewed_gold_dependency", "lifecycle_status"):
            _require_nonempty_string(decision, key, label)
        for key in ("task_ids", "theological_assumptions_avoided", "non_authorizations", "validators"):
            _require_string_list(decision, key, label)
        _require_string_list(decision, "supersedes", label, allow_empty=True)
        _require_string_list(decision, "pr_refs", label, allow_empty=True)
        scope = decision["affected_scope"]
        if not isinstance(scope, dict):
            raise RegisterError(f"{label}: affected_scope must be a mapping")
        for key in ("books", "passages", "routes", "surfaces"):
            _require_string_list(scope, key, f"{label}.affected_scope", allow_empty=True)
        covered_tasks.update(decision["task_ids"])

    for seed_name, decision_id in REQUIRED_SEED_DECISIONS.items():
        if decision_id not in decision_ids:
            raise RegisterError(f"{_rel(path)}: missing required seed decision for {seed_name}: {decision_id}")

    markers = data["no_impact_markers"]
    if not isinstance(markers, list):
        raise RegisterError(f"{_rel(path)}: no_impact_markers must be a list")
    for marker in markers:
        if not isinstance(marker, dict):
            raise RegisterError(f"{_rel(path)}: each no_impact_marker must be a mapping")
        label = f"{_rel(path)}:{marker.get('marker_id', '<missing-marker>')}"
        _require_nonempty_string(marker, "marker_id", label)
        _require_nonempty_string(marker, "rationale", label)
        _require_string_list(marker, "task_ids", label)
        _require_string_list(marker, "validators", label)
        covered_tasks.update(marker["task_ids"])

    coverage = data["backfill_coverage"]
    if not isinstance(coverage, dict):
        raise RegisterError(f"{_rel(path)}: backfill_coverage must be a mapping")
    required = coverage.get("required_task_ids")
    if not isinstance(required, list) or not required:
        raise RegisterError(f"{_rel(path)}: backfill_coverage.required_task_ids must be a non-empty list")
    missing_tasks = sorted(set(required) - covered_tasks)
    if missing_tasks:
        raise RegisterError(f"{_rel(path)}: required task ids missing coverage {missing_tasks}")

    return data


def validate_changed_path_gate(
    *,
    changed_files: list[str],
    register_path: Path = REGISTER,
    register_updated: bool | None = None,
) -> None:
    normalized = [_normalize_path(path) for path in changed_files]
    watched_changed = [
        path for path in normalized
        if any(path.startswith(prefix) for prefix in WATCHED_PREFIXES)
    ]
    if register_updated is None:
        register_rel = _rel(register_path)
        register_updated = register_rel in normalized
    if watched_changed and not register_updated:
        raise RegisterError(
            "chunking theological decision register must be updated when watched paths change: "
            + ", ".join(watched_changed)
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=REGISTER)
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--register-updated", choices=["true", "false"], default=None)
    args = parser.parse_args(argv)

    try:
        validate_register(args.register)
        changed_files = args.changed_file or _git_changed_files(args.base_ref)
        register_updated = None
        if args.register_updated is not None:
            register_updated = args.register_updated == "true"
        validate_changed_path_gate(
            changed_files=changed_files,
            register_path=args.register,
            register_updated=register_updated,
        )
    except RegisterError as exc:
        print(f"Chunking theological decision register validation failed: {exc}", file=sys.stderr)
        return 1

    print("Chunking theological decision register validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
