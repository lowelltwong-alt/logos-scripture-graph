#!/usr/bin/env python3
"""Validate the owner decision option-presentation policy."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "owner_decision_option_presentation_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

POLICY_REL = ".ai/control/owner_decision_option_presentation_policy.yaml"
VALIDATOR_REL = "scripts/validate_owner_decision_option_presentation_policy.py"

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_owner_decision_projection",
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_boundary_import",
}

REQUIRED_GATE_FIELDS = {
    "exact_question_being_decided",
    "all_good_options",
    "recommendation",
    "faithfulness_rationale",
    "upside",
    "downside",
    "downstream_effect",
    "theological_or_hermeneutic_risk",
    "engineering_or_audit_risk",
    "what_each_option_authorizes",
    "what_each_option_does_not_authorize",
    "validators_or_tests_needed",
    "next_task_if_selected",
    "stop_conditions",
}

REQUIRED_STOP_CONDITIONS = {
    "options_are_not_materially_understood",
    "prior_owner_decisions_conflict_for_the_target_text",
    "recommendation_would_smuggle_theology",
    "recommendation_would_create_output_authority_without_owner_review",
    "child_spans_speaker_boundaries_textual_policy_or_theological_system_would_be_selected_by_default",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "option_list_as_owner_selection",
    "recommendation_as_owner_selection",
    "projected_decision_as_output_authority",
    "straw_option_framing",
    "hidden_theological_default",
    "child_span_default",
    "source_metadata_as_authority",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "chunk_output_change",
}


class OwnerDecisionOptionPresentationPolicyError(ValueError):
    """Raised when the option-presentation policy is missing or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise OwnerDecisionOptionPresentationPolicyError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise OwnerDecisionOptionPresentationPolicyError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    missing = sorted(required - set(_string_list(actual, label)))
    if missing:
        raise OwnerDecisionOptionPresentationPolicyError(f"{label} missing {missing}")


def validate_owner_decision_option_presentation_policy(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "owner_decision_option_presentation_policy",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "owner_decision_option_presentation_policy.v1",
        "policy_id": "owner_decision_option_presentation_policy",
        "decision_register_entry": "CD-051",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(path)}: {key} must be {value!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_presentation_requirement") is not True:
        raise OwnerDecisionOptionPresentationPolicyError(
            f"{_rel(path)}: authority.records_presentation_requirement must be true"
        )
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(path)}: authority.{key} must be false")

    _require_subset(REQUIRED_GATE_FIELDS, data.get("required_for_future_owner_gates"), "required_for_future_owner_gates")
    _require_subset(REQUIRED_STOP_CONDITIONS, data.get("must_stop_if"), "must_stop_if")
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    _require_subset(
        {VALIDATOR_REL, "tests/test_owner_decision_option_presentation_policy.py"},
        data.get("validators"),
        "validators",
    )
    for key in ("option_quality_rule", "recommendation_rule"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(path)}: {key} must be a non-empty string")

    for linked in (REGISTER, PREFLIGHT, FORECAST, FRONT_DOOR, TOC, ROADMAP_TOC):
        if not linked.exists():
            raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(linked)}: missing linked surface")
    linked_requirements = (
        (REGISTER, ("CD-051", POLICY_REL, "Owner gates must present options and repercussions")),
        (PREFLIGHT, (POLICY_REL, "CD-051", "options, repercussions")),
        (FORECAST, (POLICY_REL, "HDF-014", "owner_decision_option_presentation_policy")),
        (FRONT_DOOR, (POLICY_REL, "serious faithful options")),
        (TOC, (POLICY_REL, "owner-options", VALIDATOR_REL)),
        (ROADMAP_TOC, (POLICY_REL, "decision-presentation", VALIDATOR_REL)),
    )
    for linked, phrases in linked_requirements:
        text = _read_text(linked)
        for phrase in phrases:
            if phrase not in text:
                raise OwnerDecisionOptionPresentationPolicyError(f"{_rel(linked)}: missing {phrase!r}")

    return data


def main() -> int:
    try:
        validate_owner_decision_option_presentation_policy()
    except OwnerDecisionOptionPresentationPolicyError as exc:
        print(f"Owner decision option presentation policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("Owner decision option presentation policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
