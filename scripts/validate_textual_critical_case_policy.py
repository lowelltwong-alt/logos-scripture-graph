#!/usr/bin/env python3
"""Validate the selected textual-critical case-by-case policy."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "textual_critical_case_policy.yaml"
OPTIONS = ROOT / ".ai" / "control" / "textual_critical_policy_owner_options.yaml"
DOCKET = ROOT / ".ai" / "control" / "textual_critical_policy_docket.yaml"
PROJECTION = ROOT / ".ai" / "control" / "owner_decision_projection_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_noncanonical_source_authority",
    "authorizes_reviewed_gold",
    "authorizes_chunk_boundaries",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_chunk_output_change",
    "authorizes_implementation",
}

REQUIRED_CASE_FIELDS = {
    "exact_variant_sensitive_refs",
    "source_surface_and_provenance",
    "boundary_dependency_or_non_dependency",
    "reviewed_gold_dependency_or_non_dependency",
    "owner_confirmation",
    "decision_register_update",
    "validators_tests",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "preferred_reading_selection",
    "critical_text_default",
    "majority_text_default",
    "textus_receptus_default",
    "current_source_as_hidden_textual_policy",
    "source_tradition_preference",
    "canon_scope_change",
    "boundary_import",
    "noncanonical_source_authority",
    "reviewed_gold_promotion",
    "chunk_boundary_authority",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "chunk_output_change",
    "implementation_authority",
}


class TextualCriticalCasePolicyError(ValueError):
    """Raised when the selected textual-critical case policy is unsafe or stale."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise TextualCriticalCasePolicyError(f"{label} must be a non-empty string")


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise TextualCriticalCasePolicyError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise TextualCriticalCasePolicyError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    actual_set = set(_string_list(actual, label))
    missing = sorted(required - actual_set)
    if missing:
        raise TextualCriticalCasePolicyError(f"{label} missing {missing}")


def validate_textual_critical_case_policy(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)

    expected = {
        "object_type": "textual_critical_case_policy",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "textual_critical_case_policy.v1",
        "policy_id": "tcp_t378_b_case_by_case_variant_sensitive_promotion",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: {key} must be {value!r}")

    auth = data.get("owner_authorization")
    if not isinstance(auth, dict):
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: owner_authorization must be a mapping")
    if auth.get("task_id") != "T379":
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: owner_authorization.task_id must be T379")
    if auth.get("selected_option") != "TCP-T378-B":
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: selected option must be TCP-T378-B")
    if auth.get("source_options_docket") != ".ai/control/textual_critical_policy_owner_options.yaml":
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: source_options_docket is stale")
    for phrase in (
        "case-by-case owner policy",
        "exact variants",
        "boundary dependency or non-dependency",
        "reviewed-gold dependency or non-dependency",
        "owner confirmation",
        "validators/tests",
        "does not authorize preferred readings",
    ):
        if phrase not in str(auth.get("exact_authorization", "")):
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: exact_authorization missing {phrase!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: authority must be a mapping")
    for key in (
        "records_owner_textual_critical_policy_selection",
        "selects_case_by_case_process_policy",
        "may_be_used_as_future_pattern_for_process_only",
    ):
        if authority.get(key) is not True:
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: authority.{key} must be false")

    policy = data.get("case_by_case_policy")
    if not isinstance(policy, dict):
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: case_by_case_policy must be a mapping")
    _require_subset(
        {
            "variant_sensitive_reviewed_gold_promotion",
            "variant_sensitive_chunk_implementation",
            "variant_sensitive_reviewed_gold_use",
            "variant_sensitive_boundary_or_canon_source_tradition_decision",
            "variant_sensitive_graph_or_retrieval_truth_use",
        },
        policy.get("applies_to"),
        "case_by_case_policy.applies_to",
    )
    _require_subset(
        REQUIRED_CASE_FIELDS,
        policy.get("required_before_each_variant_sensitive_promotion"),
        "case_by_case_policy.required_before_each_variant_sensitive_promotion",
    )
    for phrase in ("standing process rule", "must not re-litigate", "owner confirmation"):
        if phrase not in str(policy.get("future_pattern_rule", "")):
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: future_pattern_rule missing {phrase!r}")
    _require_subset(
        {
            "preferred_reading_needed",
            "source_tradition_preference_needed",
            "owner_confirmation_missing",
            "decision_register_update_missing",
            "validators_tests_missing",
        },
        policy.get("stop_conditions"),
        "case_by_case_policy.stop_conditions",
    )

    t371 = data.get("t371_implication")
    if not isinstance(t371, dict):
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: t371_implication must be a mapping")
    if t371.get("policy_blocker_resolved") is not True:
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: T371 policy_blocker_resolved must be true")
    if t371.get("t371_may_proceed_to_variant_dependency_review") is not True:
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: T371 dependency review must be allowed")
    if t371.get("t371_reviewed_gold_promotion_authorized") is not False:
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: T371 promotion must remain false")
    refs = set(_string_list(t371.get("exact_variant_refs_requiring_dependency_assessment"), "T371 refs"))
    if refs != {"1Cor.9.20", "1Cor.10.9"}:
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: T371 refs must be 1Cor.9.20 and 1Cor.10.9")
    for phrase in ("parent-only", "variant-non-dependent", "1Cor.9.20", "1Cor.10.9"):
        if phrase not in str(t371.get("next_owner_decision_required", "")):
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: T371 next decision missing {phrase!r}")

    projection = data.get("future_projection_memory")
    if not isinstance(projection, dict):
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: future_projection_memory must be a mapping")
    if projection.get("projectable_pattern_id") != "ODP-005":
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: projectable_pattern_id must be ODP-005")
    if projection.get("can_project_process_rule") is not True:
        raise TextualCriticalCasePolicyError(f"{_rel(path)}: process rule must be projectable")
    for key in ("cannot_project_specific_promotion", "cannot_project_variant_dependency_claim", "cannot_project_preferred_reading"):
        if projection.get(key) is not True:
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: future_projection_memory.{key} must be true")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    _validate_links()
    return data


def _validate_links() -> None:
    policy_rel = ".ai/control/textual_critical_case_policy.yaml"
    for path in (OPTIONS, DOCKET, PROJECTION, REGISTER, PREFLIGHT, READINESS, FORECAST, ROADMAP):
        if not path.exists():
            raise TextualCriticalCasePolicyError(f"{_rel(path)}: missing linked surface")

    options = _read_yaml(OPTIONS)
    options_status = options.get("policy_status", {})
    if options_status.get("selected_policy") != "TCP-T378-B":
        raise TextualCriticalCasePolicyError(f"{_rel(OPTIONS)}: selected_policy must be TCP-T378-B")
    if options_status.get("selection_record") != policy_rel:
        raise TextualCriticalCasePolicyError(f"{_rel(OPTIONS)}: selection_record must link case policy")

    docket = _read_yaml(DOCKET)
    status = docket.get("policy_status", {})
    if status.get("selected_policy") != "TCP-T378-B":
        raise TextualCriticalCasePolicyError(f"{_rel(DOCKET)}: selected_policy must be TCP-T378-B")
    if status.get("selected_policy_record") != policy_rel:
        raise TextualCriticalCasePolicyError(f"{_rel(DOCKET)}: selected_policy_record must link case policy")

    for path, phrases in (
        (PROJECTION, ("ODP-005", "TCP-T378-B", "process rule")),
        (REGISTER, ("CD-045", "TCP-T378-B", "case-by-case")),
        (PREFLIGHT, (policy_rel, "CD-045", "TCP-T378-B")),
        (READINESS, (policy_rel, "T379", "variant_dependency_owner_decision_required")),
        (FORECAST, ("HDF-002", "selected_case_by_case_policy", "TCP-T378-B")),
    ):
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise TextualCriticalCasePolicyError(f"{_rel(path)}: missing {phrase!r}")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    tasks = {item.get("id"): item for item in future if isinstance(item, dict)}
    t379 = tasks.get("T379")
    if not isinstance(t379, dict) or t379.get("status") != "complete":
        raise TextualCriticalCasePolicyError(f"{_rel(ROADMAP)}: T379 must be complete")
    if t379.get("selected_policy") != "TCP-T378-B":
        raise TextualCriticalCasePolicyError(f"{_rel(ROADMAP)}: T379 selected_policy is stale")

    for path in (FRONT_DOOR, TOC, ROADMAP_TOC):
        text = _read_text(path)
        for phrase in (policy_rel, "TCP-T378-B", "case-by-case"):
            if phrase not in text:
                raise TextualCriticalCasePolicyError(f"{_rel(path)}: missing {phrase!r}")


def main() -> int:
    try:
        validate_textual_critical_case_policy()
    except TextualCriticalCasePolicyError as exc:
        print(f"Textual-critical case policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("Textual-critical case policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
