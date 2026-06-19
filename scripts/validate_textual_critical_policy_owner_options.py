#!/usr/bin/env python3
"""Validate the textual-critical policy owner options docket."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
OPTIONS = ROOT / ".ai" / "control" / "textual_critical_policy_owner_options.yaml"
REQUIREMENT = ROOT / ".ai" / "control" / "textual_critical_policy_docket.yaml"
CASE_POLICY = ROOT / ".ai" / "control" / "textual_critical_case_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_textual_critical_policy",
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
    "authorizes_output_change",
}

REQUIRED_OPTIONS = {"TCP-T378-A", "TCP-T378-B", "TCP-T378-C", "TCP-T378-D"}

REQUIRED_NON_AUTHORIZATIONS = {
    "additional_textual_critical_policy_selection_without_owner",
    "preferred_reading_selection",
    "current_source_as_hidden_textual_policy",
    "critical_text_default",
    "majority_text_default",
    "textus_receptus_default",
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
    "output_change",
}


class TextualCriticalOptionsError(ValueError):
    """Raised when the textual-critical owner options docket is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TextualCriticalOptionsError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _read_text(path)
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise TextualCriticalOptionsError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise TextualCriticalOptionsError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise TextualCriticalOptionsError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise TextualCriticalOptionsError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise TextualCriticalOptionsError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    actual_items = set(_require_string_list(actual, label))
    missing = sorted(required - actual_items)
    if missing:
        raise TextualCriticalOptionsError(f"{label} missing {missing}")


def validate_textual_critical_policy_owner_options(path: Path = OPTIONS) -> dict[str, Any]:
    data = _read_yaml(path)

    if data.get("object_type") != "textual_critical_policy_owner_options_docket":
        raise TextualCriticalOptionsError(f"{_rel(path)}: object_type is wrong")
    if data.get("trust_zone") != "canonical":
        raise TextualCriticalOptionsError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise TextualCriticalOptionsError(f"{_rel(path)}: lifecycle_status must be active")
    if data.get("schema_version") != "textual_critical_policy_owner_options.v1":
        raise TextualCriticalOptionsError(f"{_rel(path)}: schema_version is wrong")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise TextualCriticalOptionsError(f"{_rel(path)}: authority must be a mapping")
    for key in (
        "records_policy_options",
        "records_recommendation",
        "records_owner_selection",
        "may_surface_for_owner_decision",
    ):
        if authority.get(key) is not True:
            raise TextualCriticalOptionsError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise TextualCriticalOptionsError(f"{_rel(path)}: authority.{key} must be false")

    status = data.get("policy_status")
    if not isinstance(status, dict):
        raise TextualCriticalOptionsError(f"{_rel(path)}: policy_status must be a mapping")
    if status.get("textual_critical_policy_selected") is not True:
        raise TextualCriticalOptionsError(f"{_rel(path)}: textual_critical_policy_selected must be true")
    if status.get("selected_policy") != "TCP-T378-B":
        raise TextualCriticalOptionsError(f"{_rel(path)}: selected_policy must be TCP-T378-B")
    if status.get("owner_decision_required") is not False:
        raise TextualCriticalOptionsError(f"{_rel(path)}: owner_decision_required must be false")
    if status.get("blocks_t371_until_selected") is not False:
        raise TextualCriticalOptionsError(f"{_rel(path)}: blocks_t371_until_selected must be false")
    if status.get("owner_selection_task") != "T379":
        raise TextualCriticalOptionsError(f"{_rel(path)}: owner_selection_task must be T379")
    if status.get("selection_record") != ".ai/control/textual_critical_case_policy.yaml":
        raise TextualCriticalOptionsError(f"{_rel(path)}: selection_record is stale")

    relation = data.get("relation_to_existing_docket")
    if not isinstance(relation, dict):
        raise TextualCriticalOptionsError(f"{_rel(path)}: relation_to_existing_docket must be a mapping")
    if relation.get("requirement_docket") != ".ai/control/textual_critical_policy_docket.yaml":
        raise TextualCriticalOptionsError(f"{_rel(path)}: requirement_docket is stale")
    if relation.get("requirement_preserved") is not True:
        raise TextualCriticalOptionsError(f"{_rel(path)}: requirement_preserved must be true")
    relation_to_t371 = str(relation.get("relation_to_t371", ""))
    for phrase in ("T379", "T371", "dependency", "promotion"):
        if phrase not in relation_to_t371:
            raise TextualCriticalOptionsError(f"{_rel(path)}: relation_to_t371 must name {phrase}")
    if "T371" not in relation_to_t371:
        raise TextualCriticalOptionsError(f"{_rel(path)}: relation_to_t371 must name T371")

    triggers = data.get("variant_sensitive_trigger_examples")
    if not isinstance(triggers, list) or len(triggers) < 2:
        raise TextualCriticalOptionsError(f"{_rel(path)}: variant_sensitive_trigger_examples must list T371 triggers")
    trigger_passages = {str(item.get("passage")) for item in triggers if isinstance(item, dict)}
    for passage in ("1Cor.9.20", "1Cor.10.9"):
        if passage not in trigger_passages:
            raise TextualCriticalOptionsError(f"{_rel(path)}: missing trigger {passage}")
    for trigger in triggers:
        if not isinstance(trigger, dict):
            raise TextualCriticalOptionsError(f"{_rel(path)}: each trigger must be a mapping")
        for key in ("passage", "surface", "issue", "t371_relevance"):
            _require_string(trigger.get(key), f"trigger.{key}")

    options = data.get("owner_options")
    if not isinstance(options, list) or not options:
        raise TextualCriticalOptionsError(f"{_rel(path)}: owner_options must be a non-empty list")
    option_ids: set[str] = set()
    recommended_count = 0
    for option in options:
        if not isinstance(option, dict):
            raise TextualCriticalOptionsError(f"{_rel(path)}: each owner option must be a mapping")
        option_id = str(option.get("option_id", ""))
        option_ids.add(option_id)
        for key in ("title", "summary", "upside", "downside", "downstream_effect_if_selected"):
            _require_string(option.get(key), f"{option_id}.{key}")
        _require_string_list(option.get("non_authorizations"), f"{option_id}.non_authorizations")
        if option.get("recommended_by_agent") is True:
            recommended_count += 1
            if option_id != "TCP-T378-B":
                raise TextualCriticalOptionsError(f"{_rel(path)}: only TCP-T378-B may be recommended")
            for phrase in ("conservative", "source-tradition", "liberal-critical", "current-source"):
                if phrase not in str(option.get("upside", "")) + str(option.get("recommendation_rationale", "")):
                    raise TextualCriticalOptionsError(f"{option_id}: recommendation must name {phrase}")
    missing = sorted(REQUIRED_OPTIONS - option_ids)
    if missing:
        raise TextualCriticalOptionsError(f"{_rel(path)}: owner_options missing {missing}")
    if recommended_count != 1:
        raise TextualCriticalOptionsError(f"{_rel(path)}: exactly one recommendation is required")

    recommendation = data.get("recommended_owner_path")
    if not isinstance(recommendation, dict):
        raise TextualCriticalOptionsError(f"{_rel(path)}: recommended_owner_path must be a mapping")
    if recommendation.get("option_id") != "TCP-T378-B":
        raise TextualCriticalOptionsError(f"{_rel(path)}: recommended option must be TCP-T378-B")
    if recommendation.get("selection_status") != "selected_by_owner":
        raise TextualCriticalOptionsError(f"{_rel(path)}: recommendation must record selected_by_owner")
    if recommendation.get("selection_task") != "T379":
        raise TextualCriticalOptionsError(f"{_rel(path)}: recommendation selection_task must be T379")
    for phrase in ("canonical Scripture", "hidden source-tradition preference", "liberal-critical", "denominational"):
        if phrase not in str(recommendation.get("why_more_faithful", "")):
            raise TextualCriticalOptionsError(f"{_rel(path)}: recommendation missing {phrase}")

    _require_subset(
        {
            "exact_variant_sensitive_refs",
            "source_surface_and_provenance",
            "owner_confirmation",
            "decision_register_update",
            "validator_or_test_update",
        },
        data.get("minimum_future_policy_if_selected"),
        "minimum_future_policy_if_selected",
    )
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")

    t371 = data.get("t371_specific_recommendation")
    if not isinstance(t371, dict):
        raise TextualCriticalOptionsError(f"{_rel(path)}: t371_specific_recommendation must be a mapping")
    for phrase in ("TCP-T378-B is selected", "Do not promote", "variant-non-dependent", "1Cor.9.20", "1Cor.10.9"):
        if phrase not in str(t371.get("recommended_next_owner_decision", "")):
            raise TextualCriticalOptionsError(f"{_rel(path)}: T371 recommendation missing {phrase}")
    for key in ("child_spans_authorized", "implementation_authorized", "output_change_authorized"):
        if t371.get(key) is not False:
            raise TextualCriticalOptionsError(f"{_rel(path)}: t371_specific_recommendation.{key} must be false")

    _validate_links()
    return data


def _validate_links() -> None:
    options_rel = ".ai/control/textual_critical_policy_owner_options.yaml"
    case_policy_rel = ".ai/control/textual_critical_case_policy.yaml"
    if not REQUIREMENT.exists():
        raise TextualCriticalOptionsError(f"{_rel(REQUIREMENT)}: missing requirement docket")
    if not CASE_POLICY.exists():
        raise TextualCriticalOptionsError(f"{_rel(CASE_POLICY)}: missing selected case policy")

    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {str(item.get("path")) for item in preflight.get("mandatory_reading", []) if isinstance(item, dict)}
    if options_rel not in reading_paths:
        raise TextualCriticalOptionsError(f"{_rel(PREFLIGHT)}: options docket must be mandatory reading")

    register_text = _read_text(REGISTER)
    for phrase in ("CD-044", "CD-045", "Textual-critical policy options block variant-sensitive reviewed-gold promotion", "T378", "T379"):
        if phrase not in register_text:
            raise TextualCriticalOptionsError(f"{_rel(REGISTER)}: missing {phrase!r}")

    readiness_text = _read_text(READINESS)
    for phrase in (options_rel, case_policy_rel, "T378", "T379", "T371"):
        if phrase not in readiness_text:
            raise TextualCriticalOptionsError(f"{_rel(READINESS)}: missing {phrase!r}")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    tasks = {item.get("id"): item for item in future if isinstance(item, dict)}
    task = tasks.get("T378")
    if not isinstance(task, dict) or task.get("status") != "complete":
        raise TextualCriticalOptionsError(f"{_rel(ROADMAP)}: T378 must be recorded complete")
    if task.get("policy_options") != options_rel:
        raise TextualCriticalOptionsError(f"{_rel(ROADMAP)}: T378 policy_options is stale")
    if task.get("textual_critical_policy_selected") is not True:
        raise TextualCriticalOptionsError(f"{_rel(ROADMAP)}: T378 must record selected policy after T379")
    if task.get("selected_policy") != "TCP-T378-B":
        raise TextualCriticalOptionsError(f"{_rel(ROADMAP)}: T378 selected_policy is stale")
    t379 = tasks.get("T379")
    if not isinstance(t379, dict) or t379.get("status") != "complete":
        raise TextualCriticalOptionsError(f"{_rel(ROADMAP)}: T379 must be recorded complete")

    for path in (FRONT_DOOR, TOC, ROADMAP_TOC):
        text = _read_text(path)
        for phrase in (options_rel, case_policy_rel, "textual-critical", "owner", "T378", "T379"):
            if phrase not in text:
                raise TextualCriticalOptionsError(f"{_rel(path)}: missing {phrase!r}")


def main() -> int:
    try:
        validate_textual_critical_policy_owner_options()
    except TextualCriticalOptionsError as exc:
        print(f"Textual-critical policy owner options validation failed: {exc}", file=sys.stderr)
        return 1
    print("Textual-critical policy owner options validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
