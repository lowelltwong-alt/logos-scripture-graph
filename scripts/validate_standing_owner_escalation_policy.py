#!/usr/bin/env python3
"""Validate standing owner escalation policy coverage and cross-links."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "standing_owner_escalation_policy.yaml"
PACKETS_DIR = ROOT / ".ai" / "context" / "agent_work" / "T411" / "escalation_packets"
QUEUE = ROOT / ".ai" / "control" / "whole_bible_low_complexity_chunking_candidate_queue.yaml"
FRONTIER = ROOT / ".ai" / "control" / "frontier_chunking_escalation_policy.yaml"
AUTONOMOUS_QUEUE = ROOT / ".ai" / "control" / "autonomous_run_queue.yaml"

REQUIRED_TOP = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "policy_id",
    "status",
    "owner",
    "authority",
    "owner_one_time_approval",
    "standing_ladder_authorization",
    "disposition_definitions",
    "escalation_packet_issue_rules",
    "queue_status_rules",
    "application_rules",
    "must_stop_even_when_policy_active",
    "validators",
}

REQUIRED_ISSUE_SUFFIXES = {
    "theology_pressure",
    "context_research_hold",
    "variant_sensitive_hold",
    "theological_risk_hold",
    "owner_decision_hold",
    "do_not_chunk_hold",
    "apostolic_authority",
    "slavery_social_ethics",
    "elect_lady_ecclesiology",
    "faith_works_theology",
    "prophetic_typology",
    "noncanonical_context",
    "church_office",
    "church_authority",
}

REQUIRED_QUEUE_STATUSES = {
    "ready_for_review_packet",
    "needs_context_research",
    "needs_original_language_review",
    "variant_sensitive_hold",
    "theological_risk_hold",
    "not_low_complexity",
    "owner_decision_required",
    "do_not_chunk_now",
}

REQUIRED_DISPOSITIONS = {
    "proceed_parent_only_through_ladder",
    "proceed_parent_only_with_frontier_note",
    "proceed_prep_and_draft_only",
    "hold_no_strengthening",
    "defer_until_frontier_review",
    "stop_escalate_owner",
    "no_pipeline",
}

SUFFIX_RE = re.compile(r"^T402-LC-\d+_(.+)\.md$")


class StandingEscalationPolicyError(ValueError):
    """Raised when standing escalation policy is incomplete or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise StandingEscalationPolicyError(f"{_rel(path)}: expected YAML mapping")
    return data


def _packet_suffixes_on_disk() -> set[str]:
    if not PACKETS_DIR.is_dir():
        raise StandingEscalationPolicyError(f"missing {_rel(PACKETS_DIR)}")
    found: set[str] = set()
    for path in PACKETS_DIR.glob("T402-LC-*.md"):
        match = SUFFIX_RE.match(path.name)
        if match:
            found.add(match.group(1))
    return found


def validate_policy(data: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if data is None:
        if not POLICY.is_file():
            return [f"missing {_rel(POLICY)}"]
        data = _read_yaml(POLICY)

    missing_top = REQUIRED_TOP - set(data)
    if missing_top:
        errors.append(f"policy missing keys: {sorted(missing_top)}")

    if data.get("object_type") != "standing_owner_escalation_policy":
        errors.append("object_type must be standing_owner_escalation_policy")

    status = data.get("status")
    if status not in {"draft_pending_owner_approval", "active"}:
        errors.append("status must be draft_pending_owner_approval or active")

    authority = data.get("authority", {})
    if not isinstance(authority, dict):
        errors.append("authority must be a mapping")
    else:
        for key, expected in (
            ("authorizes_review_packet_strengthening", False),
            ("authorizes_reviewed_gold_promotion", False),
            ("authorizes_chunk_output_change", False),
            ("authorizes_hold_clearing", False),
            ("authorizes_theology_authority_change", False),
        ):
            if authority.get(key) is not expected:
                errors.append(f"authority.{key} must be {expected}")

    defs = data.get("disposition_definitions", {})
    if not isinstance(defs, dict):
        errors.append("disposition_definitions must be a mapping")
    else:
        missing_defs = REQUIRED_DISPOSITIONS - set(defs)
        if missing_defs:
            errors.append(f"disposition_definitions missing: {sorted(missing_defs)}")

    issue_rules = data.get("escalation_packet_issue_rules", [])
    if not isinstance(issue_rules, list):
        errors.append("escalation_packet_issue_rules must be a list")
        covered_suffixes: set[str] = set()
    else:
        covered_suffixes = set()
        for idx, rule in enumerate(issue_rules):
            if not isinstance(rule, dict):
                errors.append(f"escalation_packet_issue_rules[{idx}] must be a mapping")
                continue
            suffix = rule.get("issue_suffix")
            disposition = rule.get("disposition")
            if not suffix:
                errors.append(f"escalation_packet_issue_rules[{idx}] missing issue_suffix")
                continue
            covered_suffixes.add(str(suffix))
            if disposition not in REQUIRED_DISPOSITIONS:
                errors.append(f"unknown disposition for {suffix}: {disposition}")

    missing_suffix_rules = REQUIRED_ISSUE_SUFFIXES - covered_suffixes
    if missing_suffix_rules:
        errors.append(f"escalation_packet_issue_rules missing suffixes: {sorted(missing_suffix_rules)}")

    extra_suffix_rules = covered_suffixes - REQUIRED_ISSUE_SUFFIXES
    if extra_suffix_rules:
        errors.append(f"unexpected issue_suffix entries: {sorted(extra_suffix_rules)}")

    on_disk = _packet_suffixes_on_disk()
    if on_disk != REQUIRED_ISSUE_SUFFIXES:
        only_disk = sorted(on_disk - REQUIRED_ISSUE_SUFFIXES)
        only_required = sorted(REQUIRED_ISSUE_SUFFIXES - on_disk)
        if only_disk:
            errors.append(f"packet files on disk not in REQUIRED_ISSUE_SUFFIXES: {only_disk}")
        if only_required:
            errors.append(f"REQUIRED_ISSUE_SUFFIXES missing packet files: {only_required}")

    queue_rules = data.get("queue_status_rules", [])
    if not isinstance(queue_rules, list):
        errors.append("queue_status_rules must be a list")
        covered_statuses: set[str] = set()
    else:
        covered_statuses = set()
        for idx, rule in enumerate(queue_rules):
            if not isinstance(rule, dict):
                errors.append(f"queue_status_rules[{idx}] must be a mapping")
                continue
            qstatus = rule.get("queue_status")
            disposition = rule.get("disposition") or rule.get("default_disposition")
            if not qstatus:
                errors.append(f"queue_status_rules[{idx}] missing queue_status")
                continue
            covered_statuses.add(str(qstatus))
            if disposition not in REQUIRED_DISPOSITIONS:
                errors.append(f"unknown disposition for queue {qstatus}: {disposition}")

    missing_queue = REQUIRED_QUEUE_STATUSES - covered_statuses
    if missing_queue:
        errors.append(f"queue_status_rules missing statuses: {sorted(missing_queue)}")

    if QUEUE.is_file():
        queue_data = _read_yaml(QUEUE)
        declared = queue_data.get("status_values", [])
        if isinstance(declared, list):
            declared_set = {str(v) for v in declared}
            if declared_set != REQUIRED_QUEUE_STATUSES:
                errors.append("queue status_values in candidate queue drifted from policy coverage")

    ladder = data.get("standing_ladder_authorization", {})
    if not isinstance(ladder, dict):
        errors.append("standing_ladder_authorization must be a mapping")
    else:
        for batch_key in ("batch2", "batch3"):
            batches = ladder.get("in_scope_when_active", {}).get("initial_batches", [])
            if not any(b.get("batch_id") == batch_key for b in batches if isinstance(b, dict)):
                errors.append(f"standing_ladder_authorization missing initial_batches {batch_key}")

    approval = data.get("owner_one_time_approval", {})
    if not isinstance(approval, dict) or not approval.get("approval_phrase"):
        errors.append("owner_one_time_approval.approval_phrase required")

    if status == "active":
        if data.get("lifecycle_status") != "active":
            errors.append("active policy requires lifecycle_status active")
        if not approval.get("on_approval", {}).get("decision_register_entry"):
            errors.append("active policy requires decision_register_entry on approval block")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate_policy()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: {_rel(POLICY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
