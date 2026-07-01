#!/usr/bin/env python3
"""Validate the T373 owner implementation authorization record."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
AUTH = ROOT / ".ai" / "control" / "t373_owner_implementation_authorization.yaml"
OPTION_POLICY = ROOT / ".ai" / "control" / "owner_decision_option_presentation_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
TASK = ROOT / ".ai" / "tasks" / "T373.task.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T373_OWNER_IMPLEMENTATION_AUTHORIZATION.md"

AUTH_REL = ".ai/control/t373_owner_implementation_authorization.yaml"
OPTION_POLICY_REL = ".ai/control/owner_decision_option_presentation_policy.yaml"
PROMOTION_REL = ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
PLAN_REL = ".ai/control/t372_route_isolation_harness_plan.yaml"
MANIFEST_REL = "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
VALIDATOR_REL = "scripts/validate_t373_owner_implementation_authorization.py"

REQUIRED_TRUE_AUTHORITY = {
    "records_owner_implementation_authorization",
    "authorizes_exact_t374_pilot",
    "authorizes_parent_span_as_chunk_boundary_for_exact_t374_pilot",
    "authorizes_parent_first_pilot_then_child_necessity_review_pattern",
    "authorizes_route_behavior_for_exact_t374_target_only",
    "authorizes_chunk_output_change_for_exact_t374_target_only",
    "authorizes_implementation_for_exact_t374_target_only",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_child_spans",
    "authorizes_child_span_after_pilot_without_review",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_broader_epistle_generalization",
    "authorizes_whole_bible_output_pass",
}

REQUIRED_T374_REQUIREMENTS = {
    "exact_t373_authorization_record_present",
    "task_scope_for_output_changing_paths",
    "parent_only_scope_proof",
    "selected_children_must_be_empty",
    "non_target_identity_proof",
    "same_baseline_evaluation",
    "changed_output_manifest",
    "decision_register_update",
    "validators_and_tests",
    "no_context_audit_surface",
    "handoff_validates",
    "post_pilot_child_necessity_review_gate",
}

REQUIRED_T374_FAILS = {
    "child_spans_are_added_without_later_owner_promotion",
    "route_behavior_applies_outside_1cor8_10",
    "parent_span_generalizes_to_other_epistles",
    "evaluator_formula_changes_inside_implementation_pr",
    "graph_or_retrieval_truth_is_generated",
    "embedding_or_vector_output_is_generated",
    "preferred_reading_is_selected",
    "source_tradition_preference_is_selected",
    "source_metadata_becomes_chunk_authority",
    "non_target_output_diff_is_detected",
    "improvement_claim_without_same_baseline",
    "no_context_audit_surface_is_missing",
}

REQUIRED_CHILD_FUTURE = {
    "parent_first_pilot_has_been_reviewed_when_this_pattern_is_used",
    "post_parent_pilot_review_finds_child_span_is_necessary",
    "exact_child_spans_are_proposed",
    "reviewed_child_span_gold_or_equivalent_governed_evidence_exists",
    "necessity_rationale_is_recorded",
    "theological_assumptions_avoided_are_recorded",
    "owner_explicitly_promotes_the_child_spans",
    "decision_register_is_updated",
    "validators_and_tests_cover_child_span_non_smuggling",
    "non_target_identity_proof_is_kept",
}

REQUIRED_GENERAL_PATTERN_APPLIES = {
    "exact_parent_candidate_has_reviewed_gold_or_equivalent_governed_evidence",
    "pilot_is_route_isolated_and_exact_scope",
    "owner_or_projected_owner_authorization_records_it_as_pilot",
    "child_span_need_is_uncertain_or_not_strong_enough_before_the_pilot",
    "future_case_matches_this_owner_pattern_without_conflict",
}

REQUIRED_GENERAL_PATTERN_SEQUENCE = {
    "authorize_exact_parent_only_pilot",
    "implement_parent_only_pilot_first",
    "run_same_baseline_evaluation",
    "produce_no_context_audit_surface",
    "perform_post_pilot_child_necessity_review",
    "owner_decides_whether_child_span_work_is_needed",
}

REQUIRED_GENERAL_PATTERN_REVIEW = {
    "whether_parent_only_chunk_faithfully_serves_the_passage",
    "whether_absence_of_child_spans_hides_material_discourse_or_theological_distinctions",
    "whether_child_spans_would_smuggle_theology_or_a_systematic_framework",
    "whether_reviewed_child_span_evidence_exists",
    "whether_non_target_identity_and_route_isolation_remain_protected",
}

REQUIRED_GENERAL_PATTERN_NON_AUTHS = {
    "automatic_child_spans_after_parent_pilot",
    "child_span_without_post_pilot_review",
    "child_span_without_owner_promotion",
    "treating_pilot_success_as_general_algorithm_authority",
    "denominational_system_as_child_boundary",
    "parent_pilot_as_whole_bible_authority",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "child_span_selection",
    "argument_outline_as_child_boundary",
    "paragraph_marker_as_child_boundary",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "boundary_import",
    "source_metadata_as_authority",
    "cross_reference_as_graph_edge",
    "strong_number_as_lexical_truth",
    "isolated_word_as_theological_truth",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "broader_epistle_generalization",
    "whole_bible_output_pass",
}


class T373AuthorizationError(ValueError):
    """Raised when T373 authorization is unsafe or stale."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T373AuthorizationError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T373AuthorizationError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T373AuthorizationError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise T373AuthorizationError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T373AuthorizationError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    missing = sorted(required - set(_string_list(actual, label)))
    if missing:
        raise T373AuthorizationError(f"{label} missing {missing}")


def _validate_auth(path: Path) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "owner_implementation_authorization_record",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "owner_implementation_authorization_record.v1",
        "record_id": "t373_1cor8_10_owner_implementation_authorization",
        "task_id": "T373",
        "status": "complete_owner_authorized_exact_parent_only_pilot",
        "lane": "epistle_argument",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T373AuthorizationError(f"{_rel(path)}: {key} must be {value!r}")

    owner_decision = data.get("owner_decision")
    if not isinstance(owner_decision, dict):
        raise T373AuthorizationError(f"{_rel(path)}: owner_decision must be a mapping")
    expected_owner = {
        "selected_option": "T373-A",
        "option_presentation_policy": OPTION_POLICY_REL,
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "parent_span_as_output_chunk_boundary": "authorized_for_exact_t374_pilot_only",
        "output_change_authorized": "authorized_for_exact_t374_pilot_only",
        "implementation_authorized": "authorized_for_exact_t374_pilot_only",
        "route_behavior_authorized": "authorized_for_exact_t374_target_only",
        "decision_register_update": "CD-050",
        "general_parent_first_pilot_pattern_authorized": True,
        "pilot_pattern_decision_register_update": "CD-052",
    }
    for key, value in expected_owner.items():
        if owner_decision.get(key) != value:
            raise T373AuthorizationError(f"{_rel(path)}: owner_decision.{key} must be {value!r}")
    if owner_decision.get("selected_children") != []:
        raise T373AuthorizationError(f"{_rel(path)}: owner_decision.selected_children must be []")
    if owner_decision.get("option_set_required_for_future_owner_gates") is not True:
        raise T373AuthorizationError(f"{_rel(path)}: future owner gates must require option sets")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise T373AuthorizationError(f"{_rel(path)}: scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "translation_scope": "eng-web",
        "target_id": "1cor8_10_food_offered_to_idols",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "reviewed_gold_kind": "parent_only_span",
        "promotion_record": PROMOTION_REL,
        "reviewed_gold_manifest": MANIFEST_REL,
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "harness_plan": PLAN_REL,
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T373AuthorizationError(f"{_rel(path)}: scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T373AuthorizationError(f"{_rel(path)}: scope.selected_children must be []")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T373AuthorizationError(f"{_rel(path)}: authority must be a mapping")
    for key in REQUIRED_TRUE_AUTHORITY:
        if authority.get(key) is not True:
            raise T373AuthorizationError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T373AuthorizationError(f"{_rel(path)}: authority.{key} must be false")

    selected = data.get("selected_option")
    if not isinstance(selected, dict) or selected.get("option_id") != "T373-A":
        raise T373AuthorizationError(f"{_rel(path)}: selected_option.option_id must be T373-A")
    for key in ("upside", "downside", "downstream_risk", "faithfulness_rationale"):
        if not isinstance(selected.get(key), str) or not selected[key].strip():
            raise T373AuthorizationError(f"{_rel(path)}: selected_option.{key} must be present")
    alternatives = data.get("alternatives_reviewed")
    if not isinstance(alternatives, list):
        raise T373AuthorizationError(f"{_rel(path)}: alternatives_reviewed must be a list")
    option_ids = {item.get("option_id") for item in alternatives if isinstance(item, dict)}
    if option_ids != {"T373-B", "T373-C", "T373-D", "T373-E", "T373-F", "T373-G"}:
        raise T373AuthorizationError(f"{_rel(path)}: alternatives_reviewed must include T373-B through T373-G")

    _require_subset(REQUIRED_T374_REQUIREMENTS, data.get("t374_requirements_before_merge"), "t374_requirements_before_merge")
    _require_subset(REQUIRED_T374_FAILS, data.get("t374_must_fail_if"), "t374_must_fail_if")
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")

    child = data.get("child_span_policy")
    if not isinstance(child, dict):
        raise T373AuthorizationError(f"{_rel(path)}: child_span_policy must be a mapping")
    if child.get("for_t374") != "disallowed":
        raise T373AuthorizationError(f"{_rel(path)}: child_span_policy.for_t374 must be disallowed")
    _require_subset(REQUIRED_CHILD_FUTURE, child.get("future_allowed_only_if"), "child_span_policy.future_allowed_only_if")

    pattern = data.get("general_parent_first_pilot_pattern")
    if not isinstance(pattern, dict):
        raise T373AuthorizationError(f"{_rel(path)}: general_parent_first_pilot_pattern must be a mapping")
    expected_pattern = {
        "pattern_id": "parent_first_pilot_then_child_necessity_review",
        "status": "owner_authorized_general_pattern",
        "decision_register_entry": "CD-052",
    }
    for key, value in expected_pattern.items():
        if pattern.get(key) != value:
            raise T373AuthorizationError(f"{_rel(path)}: general_parent_first_pilot_pattern.{key} must be {value!r}")
    if not isinstance(pattern.get("owner_authorization"), str) or "parent-only pilot" not in pattern["owner_authorization"]:
        raise T373AuthorizationError(f"{_rel(path)}: general_parent_first_pilot_pattern.owner_authorization must record the owner pilot pattern")
    _require_subset(REQUIRED_GENERAL_PATTERN_APPLIES, pattern.get("applies_when"), "general_parent_first_pilot_pattern.applies_when")
    _require_subset(REQUIRED_GENERAL_PATTERN_SEQUENCE, pattern.get("required_sequence"), "general_parent_first_pilot_pattern.required_sequence")
    _require_subset(REQUIRED_GENERAL_PATTERN_REVIEW, pattern.get("post_pilot_review_must_assess"), "general_parent_first_pilot_pattern.post_pilot_review_must_assess")
    _require_subset(REQUIRED_GENERAL_PATTERN_NON_AUTHS, pattern.get("non_authorizations"), "general_parent_first_pilot_pattern.non_authorizations")

    next_task = data.get("next_task")
    if not isinstance(next_task, dict) or next_task.get("task_id") != "T374":
        raise T373AuthorizationError(f"{_rel(path)}: next_task.task_id must be T374")
    if next_task.get("starts_only_if") != "T373_A_authorizes_exact_parent_only_output_pilot":
        raise T373AuthorizationError(f"{_rel(path)}: next_task.starts_only_if is stale")
    if next_task.get("output_change_authorized") is not True:
        raise T373AuthorizationError(f"{_rel(path)}: next_task.output_change_authorized must be true")
    if next_task.get("implementation_authorized") is not True:
        raise T373AuthorizationError(f"{_rel(path)}: next_task.implementation_authorized must be true")

    _require_subset(
        {VALIDATOR_REL, "tests/test_t373_owner_implementation_authorization.py", "scripts/validate_task_scope.py --task-id T373"},
        data.get("validators"),
        "validators",
    )
    return data


def _validate_links() -> None:
    for linked in (
        OPTION_POLICY,
        REGISTER,
        PREFLIGHT,
        READINESS,
        FORECAST,
        ROADMAP,
        FRONT_DOOR,
        TOC,
        ROADMAP_TOC,
        TASK,
        ROADMAP_DOC,
    ):
        if not linked.exists():
            raise T373AuthorizationError(f"{_rel(linked)}: missing linked surface")

    linked_requirements = (
        (REGISTER, ("CD-050", AUTH_REL, "T373-A authorizes exact parent-only")),
        (REGISTER, ("CD-051", OPTION_POLICY_REL, "Owner gates must present options and repercussions")),
        (REGISTER, ("CD-052", "Parent-first pilot then child-necessity review")),
        (PREFLIGHT, (AUTH_REL, OPTION_POLICY_REL, "CD-050", "CD-051", "CD-052")),
        (READINESS, ("task_id: T375", AUTH_REL, "parallel_t373_owner_implementation_authorization")),
        (FORECAST, ("HDF-014", AUTH_REL, "T373-A")),
        (ROADMAP, ("id: T373", "status: complete", AUTH_REL, "id: T374")),
        (FRONT_DOOR, (AUTH_REL, "T373-A", "post-pilot child-necessity review gate")),
        (TOC, (AUTH_REL, "parent-first-pilot", VALIDATOR_REL)),
        (ROADMAP_TOC, ("T373 | Owner implementation authorization", AUTH_REL, "post-pilot child review gate", VALIDATOR_REL)),
        (TASK, ("id: T373", AUTH_REL, "decision_register_entries: [CD-050, CD-051, CD-052, CD-053]")),
        (ROADMAP_DOC, ("T373 Owner Implementation Authorization", AUTH_REL, "parent-first pilot", "post-pilot child-necessity review gate")),
    )
    for linked, phrases in linked_requirements:
        text = _read_text(linked)
        for phrase in phrases:
            if phrase not in text:
                raise T373AuthorizationError(f"{_rel(linked)}: missing {phrase!r}")

    readiness = _read_yaml(READINESS)
    next_route = readiness.get("next_route")
    if not isinstance(next_route, dict) or next_route.get("task_id") not in {"T374", "T375", "T376", "T384", "T385", "T392", "T393", "T397", "T401", "T415"}:
        raise T373AuthorizationError(f"{_rel(READINESS)}: next_route.task_id must be T374, T375, T376, T384, T385, T392, T393, T397, T401, or T415")
    if next_route.get("task_id") == "T374":
        expected_next = {
            "starts_only_if": "T373_A_authorizes_exact_parent_only_output_pilot",
            "authorization_record": AUTH_REL,
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selected_option": "T373-A",
            "owner_decision_required": False,
            "owner_implementation_authorization_recorded": True,
            "parent_span_as_chunk_boundary_authorized": True,
            "output_change_authorized": True,
            "implementation_authorized": True,
            "route_behavior_authorized": True,
            "general_parent_first_pilot_pattern": "parent_first_pilot_then_child_necessity_review",
            "post_pilot_child_necessity_review_required": True,
            "child_span_work_requires_later_owner_promotion": True,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
        }
    elif next_route.get("task_id") == "T375":
        expected_next = {
            "starts_only_if": "T374_additive_parent_overlay_implemented",
            "authorization_record": AUTH_REL,
            "implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selected_option": "T374-OVERLAP-B",
            "selected_t373_option": "T373-A",
            "owner_implementation_authorization_recorded": True,
            "additive_parent_overlay_implemented": True,
            "parent_span_as_chunk_boundary_authorized": True,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "general_parent_first_pilot_pattern": "parent_first_pilot_then_child_necessity_review",
            "post_pilot_child_necessity_review_required": True,
            "child_span_work_requires_later_owner_promotion": True,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
        }
    elif next_route.get("task_id") == "T376":
        expected_next = {
            "starts_only_if": "T375_post_pilot_review_complete",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "route_type": "next_genre_selection",
            "owner_decision_required": True,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
        }
    elif next_route.get("task_id") == "T384":
        expected_next = {
            "starts_only_if": "T376_A_epistle_argument_research_runway_selected",
            "prior_lane_selection": ".ai/control/t376_epistle_research_runway.yaml",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "route_type": "bible_wide_research_readiness_synthesis",
            "selected_t376_option": "T376-A",
            "selected_lane": "epistle_argument",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
    elif next_route.get("task_id") == "T392":
        expected_next = {
            "starts_only_if": "explicit_owner_selection_of_T385_A",
            "route_type": "epistle_argument_review_packet_strengthening",
            "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
            "completion_status": "complete_review_packet_strengthening_only",
            "selected_option": "T385-A",
            "review_packet_strengthened": True,
            "exact_next_owner_action": "Goal5_owner_reviewed_gold_promotion_decision_packet",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected_for_promotion_or_implementation": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
    elif next_route.get("task_id") == "T393":
        expected_next = {
            "starts_only_if": "T392_eph1_review_packet_strengthening_complete",
            "route_type": "epistle_argument_owner_reviewed_gold_promotion_decision_packet",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "completion_status": "pending_owner_reviewed_gold_promotion_decision",
            "owner_selection_status": "pending",
            "recommended_option": "T393-A",
            "recommendation_is_owner_selection": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
    elif next_route.get("task_id") == "T397":
        expected_next = {
            "starts_only_if": "T394_eph1_parent_only_reviewed_gold_promoted",
            "route_type": "epistle_argument_goal6_route_isolation_harness_prep",
            "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "completion_status": "complete_non_output_changing_route_isolation_harness_prep",
            "owner_selection_status": "selected",
            "selected_option": "T393-A",
            "reviewed_gold_promoted": True,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
            "source_or_manuscript_rows_authorized": False,
        }
    elif next_route.get("task_id") == "T401":
        expected_next = {
            "starts_only_if": "T397_route_isolation_harness_complete_and_owner_authorized_exact_output_pilot",
            "route_type": "epistle_argument_goal7_exact_output_pilot",
            "completion_status": "complete_output_changed_eph1_parent_overlay",
            "output_manifest": ".ai/control/t401_eph1_output_pilot_manifest.yaml",
            "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
            "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
            "reviewed_gold_promoted": True,
            "output_change_authorized": True,
            "implementation_authorized": True,
            "route_behavior_authorized": True,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
            "source_or_manuscript_rows_authorized": False,
            "exact_next_owner_action": "T402_post_pilot_review_before_child_spans_or_broader_behavior",
        }
    elif next_route.get("task_id") == "T415":
        expected_next = {
            "route_type": "epistle_opening_goal7_exact_output_pilot",
            "completion_status": "complete_output_changed_batch1_parent_overlays",
            "output_manifest": ".ai/control/t415_batch1_output_pilot_manifest.yaml",
            "promotion_record": ".ai/control/t414_batch1_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_promoted": True,
            "output_change_authorized": True,
            "implementation_authorized": True,
            "route_behavior_authorized": True,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
        }
    else:
        expected_next = {
            "starts_only_if": "T384_bible_wide_research_readiness_synthesis_complete_and_T386_coverage_complete",
            "route_type": "owner_decision_packet_only",
            "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
            "completion_status": "complete_owner_decision_packet_only",
            "owner_selection_status": "pending",
            "recommended_option": "T385-A",
            "recommendation_is_owner_selection": False,
            "exact_target_selected": False,
            "reviewed_gold_promoted": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
            "route_behavior_authorized": False,
            "child_spans_authorized": False,
            "evaluator_change_authorized": False,
            "graph_edge_generation_allowed": False,
            "retrieval_truth_authorized": False,
            "embedding_or_vector_work_allowed": False,
        }
    for key, value in expected_next.items():
        if next_route.get(key) != value:
            raise T373AuthorizationError(f"{_rel(READINESS)}: next_route.{key} must be {value!r}")
    if next_route.get("task_id") in {"T374", "T375"} and next_route.get("selected_children") != []:
        raise T373AuthorizationError(f"{_rel(READINESS)}: {next_route.get('task_id')} selected_children must be []")
    if next_route.get("task_id") == "T376":
        result = next_route.get("t375_result", {})
        if result.get("child_span_result") != "child_spans_not_necessary_now":
            raise T373AuthorizationError(f"{_rel(READINESS)}: T376 t375_result.child_span_result is stale")
        if result.get("selected_children") != []:
            raise T373AuthorizationError(f"{_rel(READINESS)}: T376 t375_result.selected_children must be []")
    if next_route.get("task_id") == "T384" and "CD-060" not in next_route.get("prior_decision_register_entries", []):
        raise T373AuthorizationError(f"{_rel(READINESS)}: T384 must reference CD-060")
    if next_route.get("task_id") == "T385" and "CD-066" not in next_route.get("prior_decision_register_entries", []):
        raise T373AuthorizationError(f"{_rel(READINESS)}: T385 must reference CD-066")
    if next_route.get("task_id") == "T392" and "CD-067" not in next_route.get("prior_decision_register_entries", []):
        raise T373AuthorizationError(f"{_rel(READINESS)}: T392 must reference CD-067")
    if next_route.get("task_id") == "T393" and "CD-068" not in next_route.get("prior_decision_register_entries", []):
        raise T373AuthorizationError(f"{_rel(READINESS)}: T393 must reference CD-068")
    if next_route.get("task_id") == "T397" and "CD-071" not in next_route.get("prior_decision_register_entries", []):
        raise T373AuthorizationError(f"{_rel(READINESS)}: T397 must reference CD-071")
    if next_route.get("task_id") == "T401":
        for required in ("CD-071", "CD-074", "CD-076"):
            if required not in next_route.get("prior_decision_register_entries", []):
                raise T373AuthorizationError(f"{_rel(READINESS)}: T401 must reference {required}")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    by_id = {item.get("id"): item for item in future if isinstance(item, dict)}
    t373 = by_id.get("T373")
    if not isinstance(t373, dict) or t373.get("status") != "complete":
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T373 must be complete")
    if t373.get("authorization_record") != AUTH_REL:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T373 authorization_record is stale")
    if "CD-052" not in t373.get("decision_register_entries", []):
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T373 decision_register_entries must include CD-052")
    if t373.get("general_parent_first_pilot_pattern") != "parent_first_pilot_then_child_necessity_review":
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T373 general_parent_first_pilot_pattern is stale")
    if t373.get("post_pilot_child_necessity_review_required") is not True:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T373 post_pilot_child_necessity_review_required must be true")
    if t373.get("child_spans_authorized") is not False:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T373 child_spans_authorized must be false")
    t374 = by_id.get("T374")
    if not isinstance(t374, dict) or t374.get("starts_only_if") != "T373_A_authorizes_exact_parent_only_output_pilot":
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T374 starts_only_if is stale")
    if t374.get("output_change_authorized") is not True:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T374 output_change_authorized must be true")
    if t374.get("implementation_authorized") is not True:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T374 implementation_authorized must be true")
    if t374.get("child_spans_authorized") is not False:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T374 child_spans_authorized must be false")
    if t374.get("requires_post_pilot_child_necessity_review_gate") is not True:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T374 requires_post_pilot_child_necessity_review_gate must be true")
    t375 = by_id.get("T375")
    if not isinstance(t375, dict) or t375.get("post_pilot_child_necessity_review_required") is not True:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T375 must require post-pilot child-necessity review")
    if t375.get("child_span_work_requires_later_owner_promotion") is not True:
        raise T373AuthorizationError(f"{_rel(ROADMAP)}: T375 child_span_work_requires_later_owner_promotion must be true")


def validate_t373_owner_implementation_authorization(path: Path = AUTH) -> dict[str, Any]:
    data = _validate_auth(path)
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t373_owner_implementation_authorization()
    except T373AuthorizationError as exc:
        print(f"T373 owner implementation authorization validation failed: {exc}", file=sys.stderr)
        return 1
    print("T373 owner implementation authorization validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
