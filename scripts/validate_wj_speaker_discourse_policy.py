#!/usr/bin/env python3
"""Validate the WJ speaker/discourse policy selection."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "wj_speaker_discourse_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
T355_TASK = ROOT / ".ai" / "tasks" / "T355.task.yaml"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_jesus_speaker_attribution",
    "authorizes_speaker_boundary",
    "authorizes_discourse_boundary",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_output_change",
}

REQUIRED_TRUE_AUTHORITY = {
    "records_policy",
    "selects_review_target",
    "may_surface_for_review",
}

REQUIRED_RULE_IDS = {
    "WJ-SPK-001",
    "WJ-SPK-002",
    "WJ-SPK-003",
    "WJ-SPK-004",
    "WJ-SPK-005",
}

REQUIRED_CANDIDATES = {
    "matt5_7_sermon_on_mount_wj_discourse",
    "john13_17_wj_farewell_discourse_marker_focus",
    "matt24_25_olivet_discourse",
    "john7_53_8_11_wj_variant_speech",
    "revelation_wj_voice_shifts",
}

REQUIRED_REQUIREMENTS = {
    "owner_review",
    "exact_scope",
    "reviewed_speaker_discourse_gold_or_equivalent_governed_evidence",
    "decision_register_update",
    "executable_tests",
    "non_target_identity_proof",
    "same_baseline_evaluation",
    "later_implementation_authorization",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "wj_marker_as_speaker_authority",
    "wj_marker_as_jesus_speaker_attribution",
    "wj_marker_as_speaker_boundary",
    "wj_marker_as_discourse_boundary",
    "wj_marker_as_chunk_boundary",
    "wj_marker_as_reviewed_gold",
    "wj_marker_as_graph_edge",
    "wj_marker_as_retrieval_truth",
    "wj_marker_as_output_change",
    "red_letter_markup_as_theological_truth",
}


class WJSpeakerPolicyError(ValueError):
    """Raised when the WJ speaker/discourse policy is missing or authorizing."""


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
        raise WJSpeakerPolicyError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise WJSpeakerPolicyError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise WJSpeakerPolicyError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise WJSpeakerPolicyError(f"{label} missing {missing}")


def _validate_policy_shape(data: dict[str, Any], path: Path) -> None:
    if data.get("object_type") != "wj_speaker_discourse_policy":
        raise WJSpeakerPolicyError(f"{_rel(path)}: object_type must be wj_speaker_discourse_policy")
    if data.get("trust_zone") != "canonical":
        raise WJSpeakerPolicyError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise WJSpeakerPolicyError(f"{_rel(path)}: lifecycle_status must be active")
    if data.get("schema_version") != "wj_speaker_discourse_policy.v1":
        raise WJSpeakerPolicyError(f"{_rel(path)}: schema_version must be wj_speaker_discourse_policy.v1")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise WJSpeakerPolicyError(f"{_rel(path)}: authority must be a mapping")
    for key in REQUIRED_TRUE_AUTHORITY:
        if authority.get(key) is not True:
            raise WJSpeakerPolicyError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise WJSpeakerPolicyError(f"{_rel(path)}: authority.{key} must be false")

    rule_ids = {
        str(item.get("rule_id"))
        for item in data.get("policy_rules", [])
        if isinstance(item, dict)
    }
    missing_rules = sorted(REQUIRED_RULE_IDS - rule_ids)
    if missing_rules:
        raise WJSpeakerPolicyError(f"{_rel(path)}: missing policy rules {missing_rules}")

    _require_subset(
        REQUIRED_REQUIREMENTS,
        data.get("future_output_changing_use_requires"),
        "future_output_changing_use_requires",
    )
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")


def _validate_selected_target(data: dict[str, Any], path: Path) -> None:
    selected = data.get("selected_first_review_target")
    if not isinstance(selected, dict):
        raise WJSpeakerPolicyError(f"{_rel(path)}: selected_first_review_target must be a mapping")
    expected = {
        "target_id": "john3_wj_speaker_boundary",
        "passage": "John.3.1-John.3.36",
        "selection_status": "selected_for_next_owner_review",
        "selected_in_task": "T355",
        "review_packet": "eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md",
    }
    for key, value in expected.items():
        if selected.get(key) != value:
            raise WJSpeakerPolicyError(f"{_rel(path)}: selected_first_review_target.{key} must be {value}")
    for key in ("implementation_allowed", "output_change_authorized", "reviewed_gold_promoted"):
        if selected.get(key) is not False:
            raise WJSpeakerPolicyError(f"{_rel(path)}: selected_first_review_target.{key} must be false")
    if not (ROOT / selected["review_packet"]).exists():
        raise WJSpeakerPolicyError(f"{_rel(path)}: selected review packet is missing")

    candidates = {
        str(item.get("target_id"))
        for item in data.get("candidate_target_queue", [])
        if isinstance(item, dict)
    }
    missing_candidates = sorted(REQUIRED_CANDIDATES - candidates)
    if missing_candidates:
        raise WJSpeakerPolicyError(f"{_rel(path)}: missing candidate targets {missing_candidates}")


def _validate_governed_links() -> None:
    register = _read_yaml(REGISTER)
    decisions = register.get("decisions")
    if not isinstance(decisions, list):
        raise WJSpeakerPolicyError(f"{_rel(REGISTER)}: decisions must be a list")
    cd022 = next((item for item in decisions if isinstance(item, dict) and item.get("decision_id") == "CD-022"), None)
    if not isinstance(cd022, dict):
        raise WJSpeakerPolicyError(f"{_rel(REGISTER)}: missing CD-022")
    if "T355" not in cd022.get("task_ids", []):
        raise WJSpeakerPolicyError(f"{_rel(REGISTER)}: CD-022 must cover T355")
    for validator in ("scripts/validate_wj_speaker_discourse_policy.py", "tests/test_wj_speaker_discourse_policy.py"):
        if validator not in cd022.get("validators", []):
            raise WJSpeakerPolicyError(f"{_rel(REGISTER)}: CD-022 validators missing {validator}")

    preflight = _read_yaml(PREFLIGHT)
    reading_by_path = {
        str(item.get("path")): item
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    policy_entry = reading_by_path.get(".ai/control/wj_speaker_discourse_policy.yaml")
    if not isinstance(policy_entry, dict):
        raise WJSpeakerPolicyError(f"{_rel(PREFLIGHT)}: WJ speaker policy must be mandatory reading")
    if "CD-022" not in reading_by_path.get(".ai/control/chunking_theological_decision_register.yaml", {}).get(
        "required_decision_ids", []
    ):
        raise WJSpeakerPolicyError(f"{_rel(PREFLIGHT)}: decision register reading must require CD-022")

    readiness = _read_yaml(READINESS_MAP)
    lanes = readiness.get("lane_sequence")
    if not isinstance(lanes, list):
        raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: lane_sequence must be a list")
    gospel_lane = next(
        (item for item in lanes if isinstance(item, dict) and item.get("lane_id") == "gospel_discourse_wj"),
        None,
    )
    if not isinstance(gospel_lane, dict):
        raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: missing gospel_discourse_wj lane")

    policy_surface = gospel_lane.get("speaker_discourse_policy")
    if not isinstance(policy_surface, dict):
        raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: gospel_discourse_wj.speaker_discourse_policy must be a mapping")
    expected_policy = {
        "task_id": "T355",
        "path": ".ai/control/wj_speaker_discourse_policy.yaml",
        "status": "selected_for_next_owner_review",
        "selected_target": "john3_wj_speaker_boundary",
        "selected_passage": "John.3.1-John.3.36",
        "review_packet": "eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md",
    }
    for key, value in expected_policy.items():
        if policy_surface.get(key) != value:
            raise WJSpeakerPolicyError(
                f"{_rel(READINESS_MAP)}: speaker_discourse_policy.{key} must be {value}"
            )
    for key in ("output_change_authorized", "implementation_authorized", "reviewed_gold_promoted"):
        if policy_surface.get(key) is not False:
            raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: speaker_discourse_policy.{key} must be false")

    docket_surface = gospel_lane.get("owner_review_docket")
    if not isinstance(docket_surface, dict):
        raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: gospel_discourse_wj.owner_review_docket must be a mapping")
    expected_docket = {
        "task_id": "T356",
        "path": ".ai/control/john3_wj_owner_review_docket.yaml",
        "status": "parent_only_review_target_selected",
        "selected_target": "john3_wj_speaker_boundary",
        "selected_passage": "John.3.1-John.3.36",
        "selected_option": "JOHN3-T356-B",
        "selected_parent": "John.3.1-John.3.36",
    }
    for key, value in expected_docket.items():
        if docket_surface.get(key) != value:
            raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: owner_review_docket.{key} must be {value}")
    for key in ("output_change_authorized", "implementation_authorized", "reviewed_gold_promoted"):
        if docket_surface.get(key) is not False:
            raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: owner_review_docket.{key} must be false")

    next_route = readiness.get("next_route")
    if isinstance(next_route, dict):
        if next_route.get("task_id") == "T374":
            if next_route.get("authorization_record") != ".ai/control/t373_owner_implementation_authorization.yaml":
                raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: T374 authorization_record is stale")
            if next_route.get("selected_children") != []:
                raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: T374 selected_children must be []")
            for key in ("evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
                if next_route.get(key) is not False:
                    raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: T374 next_route.{key} must be false")
        else:
            for key in ("output_change_authorized", "implementation_authorized"):
                if next_route.get(key) is not False:
                    raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: next_route.{key} must be false")
            if next_route.get("task_id") not in {"T372", "T373", "T374", "T375"} and next_route.get("reviewed_gold_promoted") is not False:
                raise WJSpeakerPolicyError(f"{_rel(READINESS_MAP)}: next_route.reviewed_gold_promoted must be false outside T372/T373/T374/T375")

    if not T355_TASK.exists():
        raise WJSpeakerPolicyError(f"{_rel(T355_TASK)}: T355 task file is missing")


def validate_wj_speaker_discourse_policy(path: Path = POLICY) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_policy_shape(data, path)
    _validate_selected_target(data, path)
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_wj_speaker_discourse_policy()
    except WJSpeakerPolicyError as exc:
        print(f"WJ speaker/discourse policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("WJ speaker/discourse policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
