#!/usr/bin/env python3
"""Validate the Bible-wide chunking readiness map."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"

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
    "faithful_execution_model",
    "lessons_storage",
    "current_baseline",
    "algorithm_readiness",
    "lane_sequence",
    "next_route",
    "update_triggers",
    "explicit_non_authorizations",
}

REQUIRED_LANES = {
    "psalms_poetry",
    "revelation_apocalyptic",
    "epistle_argument",
    "narrative_pericope",
    "wisdom_dialogue",
    "prophetic_oracle",
    "gospel_discourse_wj",
    "textual_variant_source_tradition",
    "bible_wide_orchestration",
}

REQUIRED_ALGORITHMS = {
    "monolith_fallback",
    "form_detector",
    "orchestrator",
    "psalm_candidate_skill",
    "revelation_skill",
}

REQUIRED_LESSON_SURFACES = {
    ".ai/control/chunking_lesson_index.yaml",
    ".ai/control/chunking_theological_decision_register.yaml",
    "docs/methodology/WORKFLOW_LESSONS.md",
    "docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md",
    "docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md",
    ".ai/control/bible_wide_chunking_research_registry.yaml",
    ".ai/control/source_metadata_research_atlas.yaml",
    ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml",
    ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml",
    ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
    ".ai/control/gospel_wj_discourse_dossier_queue.yaml",
    ".ai/control/narrative_legal_covenant_dossier_queue.yaml",
    ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml",
    ".ai/control/prophetic_oracle_vision_dossier_queue.yaml",
    ".ai/control/textual_variant_source_tradition_dossier_queue.yaml",
    ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml",
    ".ai/control/contextual_reading_policy.yaml",
    ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
    ".ai/control/textual_critical_policy_docket.yaml",
    ".ai/control/textual_critical_policy_owner_options.yaml",
    ".ai/control/textual_critical_case_policy.yaml",
    ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
    ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
    ".ai/control/t372_route_isolation_harness_plan.yaml",
    ".ai/control/t373_owner_implementation_authorization.yaml",
    ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml",
    ".ai/control/t374_additive_parent_overlay_manifest.yaml",
    ".ai/control/t375_post_pilot_review.yaml",
    ".ai/control/t376_epistle_research_runway.yaml",
    ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml",
    ".ai/control/t385_owner_decision_packet.yaml",
    "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
    "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md",
    ".ai/tasks/T392.task.yaml",
    ".ai/audits/reports/20260623-T392-eph1-review-packet-strengthening.md",
    ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
    "docs/roadmap/T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md",
    ".ai/tasks/T393.task.yaml",
    ".ai/audits/reports/20260623-T393-eph1-reviewed-gold-promotion-decision-packet.md",
    ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
    "docs/roadmap/T394_EPH1_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md",
    ".ai/tasks/T394.task.yaml",
    ".ai/audits/reports/20260623-T394-eph1-parent-only-reviewed-gold-promotion.md",
    ".ai/control/t397_eph1_route_isolation_harness.yaml",
    "docs/roadmap/T397_EPH1_ROUTE_ISOLATION_HARNESS.md",
    ".ai/tasks/T397.task.yaml",
    ".ai/handoffs/T397/handoff.md",
    ".ai/audits/reports/20260624-T397-eph1-route-isolation-harness.md",
    "scripts/chunking/route_isolation_harness.py",
    "scripts/validate_t397_eph1_route_isolation_harness.py",
    "tests/test_t397_eph1_route_isolation_harness.py",
    "tests/test_route_isolation_harness.py",
    ".ai/control/t401_eph1_output_pilot_manifest.yaml",
    "docs/roadmap/T401_EPH1_OUTPUT_PILOT.md",
    ".ai/tasks/T401.task.yaml",
    ".ai/handoffs/T401/handoff.md",
    ".ai/audits/reports/20260625-T401-eph1-output-pilot.md",
    "scripts/validate_t401_eph1_output_pilot.py",
    "tests/test_t401_eph1_output_pilot.py",
    ".ai/control/t402_eph1_post_pilot_review.yaml",
    ".ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml",
    "docs/roadmap/T402_LOW_COMPLEXITY_CHUNKING_RUNWAY.md",
    ".ai/tasks/T402.task.yaml",
    ".ai/handoffs/T402/handoff.md",
    ".ai/audits/reports/20260625-T402-low-complexity-runway.md",
    "scripts/validate_t402_low_complexity_chunking_runway.py",
    "tests/test_t402_low_complexity_chunking_runway.py",
    ".ai/control/cursor_low_risk_chunking_handoff.yaml",
    ".ai/control/low_risk_chunking_multi_pass_plan.yaml",
    "docs/roadmap/T404_CURSOR_LOW_RISK_CHUNKING_HANDOFF.md",
    "docs/roadmap/T406_LOW_RISK_CHUNKING_MULTI_PASS_PLAN.md",
    ".ai/tasks/T404.task.yaml",
    ".ai/handoffs/T404/handoff.md",
    ".cursor/commands/chunking-preflight.md",
    ".cursor/commands/low-risk-chunking-candidate.md",
    ".cursor/commands/codex-review-packet.md",
    ".cursor/rules/logos-scripture-low-risk-chunking.mdc",
    "scripts/validate_cursor_low_risk_chunking_handoff.py",
    "tests/test_cursor_low_risk_chunking_handoff.py",
    ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml",
    "docs/roadmap/T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md",
    ".ai/tasks/T398.task.yaml",
    ".ai/audits/reports/20260623-T398-bible-wide-phase-one-research-synthesis.md",
    "scripts/validate_t398_bible_wide_phase_one_research_synthesis.py",
    "tests/test_t398_bible_wide_phase_one_research_synthesis.py",
    ".ai/control/t399_focused_bible_wide_research_queue.yaml",
    "docs/roadmap/T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md",
    ".ai/tasks/T399.task.yaml",
    ".ai/audits/reports/20260624-T399-focused-bible-wide-research-queue.md",
    "scripts/validate_t399_focused_bible_wide_research_queue.py",
    "tests/test_t399_focused_bible_wide_research_queue.py",
    ".ai/control/bible_verse_passage_coverage_inventory.jsonl",
    ".ai/control/bible_verse_passage_coverage_taxonomy.yaml",
    ".ai/control/bible_verse_passage_coverage_summary.yaml",
    ".ai/control/bible_verse_passage_readiness_matrix.yaml",
    ".ai/control/bible_verse_passage_gap_register.yaml",
    ".ai/control/bible_verse_passage_human_review_docket.yaml",
    ".ai/control/owner_decision_option_presentation_policy.yaml",
    ".ai/control/chunking_human_decision_forecast.yaml",
    ".ai/control/governance_memory_durability_policy.yaml",
    ".ai/control/owner_decision_projection_policy.yaml",
    "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "raw_or_canonical_mutation",
    "chunk_output_change",
    "revelation_implementation",
    "unscoped_reviewed_gold_promotion",
    "reviewed_gold_promotion_without_owner_confirmation",
    "skill_lifecycle_promotion",
    "boundary_import",
    "parent_only_gold_as_chunk_boundary_outside_exact_t373_t374_pilot",
    "t374_implementation_without_baseline_overlap_owner_option",
    "child_span_selection_without_later_owner_promotion",
    "context_as_chunk_boundary_authority",
    "historical_background_as_scripture_authority",
    "recommendation_as_owner_selection",
    "route_isolation_harness_as_output_authority",
    "t327g",
    "master_chunker_global_objective",
}

ALLOWED_NEXT_ROUTES = {
    "T342": {
        "route_type": "review_selection_only",
        "title": "Revelation Review-Packet Candidate Selection",
    },
    "T343": {
        "route_type": "review_packet_and_gold_candidate_creation",
        "title": "Revelation Review Packets and Gold Candidates",
    },
    "T344": {
        "route_type": "owner_target_selection",
        "title": "Select One Revelation Behavior Target",
    },
    "T351": {
        "route_type": "bible_wide_research_triage",
        "title": "Bible-Wide Chunking Research Triage Atlas",
    },
    "T352": {
        "route_type": "epistle_argument_review_packet_prep",
        "title": "Epistle Argument Review Packets",
    },
    "T354": {
        "route_type": "gospel_wj_marker_inventory_harness",
        "title": "WJ Marker Inventory Harness",
    },
    "T355": {
        "route_type": "wj_speaker_discourse_policy_and_target_selection",
        "title": "WJ Speaker/Discourse Policy And Target Selection",
    },
    "T356": {
        "route_type": "john3_wj_owner_review_docket",
        "title": "John 3 WJ Owner Review Docket",
    },
    "T368": {
        "route_type": "epistle_argument_review_packet_strengthening",
        "title": "1 Corinthians 8-10 Epistle Argument Packet Strengthening",
    },
    "T369": {
        "route_type": "epistle_argument_owner_review_gate",
        "title": "1 Corinthians 8-10 Owner Review Docket",
    },
    "T370": {
        "route_type": "epistle_argument_parent_only_evidence_prep",
        "title": "Build Selected 1 Corinthians 8-10 Reviewed-Gold Evidence Packet",
    },
    "T371": {
        "route_type": "epistle_argument_owner_reviewed_gold_promotion_gate",
        "title": "Owner Reviewed-Gold Promotion Decision",
    },
    "T372": {
        "route_type": "epistle_argument_route_isolation_harness",
        "title": "Route-Isolated Implementation Harness And Non-Target Identity Plan",
    },
    "T373": {
        "route_type": "epistle_argument_owner_implementation_authorization_gate",
        "title": "Owner Implementation Authorization Gate",
    },
    "T374": {
        "route_type": "epistle_argument_route_isolated_output_pilot",
        "title": "First Route-Isolated 1 Corinthians 8-10 Implementation",
    },
    "T375": {
        "route_type": "epistle_argument_post_pilot_review",
        "title": "Same-Baseline Evaluation, No-Context Audit, And Child-Necessity Review",
    },
    "T376": {
        "route_type": "next_genre_selection",
        "title": "Select Next Chunking Lane From Decision Forecast",
    },
    "T384": {
        "route_type": "bible_wide_research_readiness_synthesis",
        "title": "Bible-Wide Research Readiness Synthesis",
    },
    "T385": {
        "route_type": "owner_decision_packet_only",
        "title": "Owner Decision Packet From T384/T386/T387/T388/T389/T390 Readiness",
    },
    "T392": {
        "route_type": "epistle_argument_review_packet_strengthening",
        "title": "Eph.1.3-Eph.1.14 Review Packet Strengthening",
    },
    "T393": {
        "route_type": "epistle_argument_owner_reviewed_gold_promotion_decision_packet",
        "title": "Eph.1.3-Eph.1.14 Reviewed-Gold Promotion Decision Packet",
    },
    "T397": {
        "route_type": "epistle_argument_goal6_route_isolation_harness_prep",
        "title": "Eph.1.3-Eph.1.14 Route-Isolated Harness Prep",
    },
    "T401": {
        "route_type": "epistle_argument_goal7_exact_output_pilot",
        "title": "Eph.1.3-Eph.1.14 Exact Output Pilot",
    },
    "T415": {
        "route_type": "epistle_opening_goal7_exact_output_pilot",
        "title": "T411 Batch1 Output Pilot",
    },
}


class ReadinessMapError(ValueError):
    """Raised when the readiness map is invalid."""


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
        raise ReadinessMapError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ReadinessMapError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReadinessMapError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ReadinessMapError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ReadinessMapError(f"{label} must contain only non-empty strings")
    return value


def _validate_t385_next_route(next_route: dict[str, Any], path: Path) -> None:
    expected = {
        "title": "Owner Decision Packet From T384/T386/T387/T388/T389/T390 Readiness",
        "starts_only_if": "T384_bible_wide_research_readiness_synthesis_complete_and_T386_coverage_complete",
        "completion_status": "complete_owner_decision_packet_only",
        "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
        "roadmap_doc": "docs/roadmap/T385_OWNER_DECISION_PACKET.md",
        "validator": "scripts/validate_t385_owner_decision_packet.py",
        "required_handoff": ".ai/handoffs/T385/handoff.md",
        "decision_register_entry": "CD-066",
        "lesson_index_entry": "LSN-020",
        "selected_t376_option": "T376-A",
        "selected_lane": "epistle_argument",
        "selection_mode": "owner_packet_complete_non_authorizing",
        "owner_decision_required_before_goal_4": True,
        "owner_decision_required_before_promotion_or_implementation": True,
        "owner_selection_status": "pending",
        "recommended_option": "T385-A",
        "recommended_passage": "Eph.1.3-Eph.1.14",
        "recommendation_is_owner_selection": False,
        "exact_target_selected": False,
        "exact_next_owner_action": "explicit_owner_selection_of_one_T385_option",
        "goal_4_can_run_after": "explicit_owner_selection_of_one_T385_option",
    }
    for key, value in expected.items():
        if next_route.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T385 next_route.{key} must be {value!r}")

    inputs = next_route.get("prior_readiness_inputs")
    if not isinstance(inputs, list):
        raise ReadinessMapError(f"{_rel(path)}: T385 prior_readiness_inputs must be a list")
    input_ids = {item.get("task_id") for item in inputs if isinstance(item, dict)}
    for required in {"T384", "T386", "T386-docket", "T387", "T388", "T389", "T390"}:
        if required not in input_ids:
            raise ReadinessMapError(f"{_rel(path)}: T385 prior_readiness_inputs missing {required}")

    prior_entries = set(
        _require_string_list(next_route.get("prior_decision_register_entries"), "T385 prior_decision_register_entries")
    )
    for required in {"CD-061", "CD-062", "CD-063", "CD-064", "CD-065", "CD-066"}:
        if required not in prior_entries:
            raise ReadinessMapError(f"{_rel(path)}: T385 prior_decision_register_entries missing {required}")

    options = set(_require_string_list(next_route.get("serious_faithful_options"), "T385 serious_faithful_options"))
    for required in {"T385-A", "T385-B", "T385-C", "T385-D", "T385-E", "T385-F", "T385-G", "T385-H", "T385-I"}:
        if required not in options:
            raise ReadinessMapError(f"{_rel(path)}: T385 serious_faithful_options missing {required}")

    required_records = set(
        _require_string_list(next_route.get("required_t385_packet_records"), "T385 required_t385_packet_records")
    )
    for required in (
        "serious_faithful_target_options",
        "repercussions_for_each_option",
        "recommendation",
        "owner_selection_pending",
        "recommendation_is_not_owner_selection",
        "contextual_reading_policy_fields",
        "source_metadata_evidence_only_handling",
        "original_language_phrase_context_review_where_used",
        "textual_variant_or_source_tradition_sensitivity",
        "orthodox_hermeneutic_firewall_compliance",
        "decision_register_update",
        "lesson_index_update",
        "validators_and_tests",
        "handoff_next_owner_gate",
    ):
        if required not in required_records:
            raise ReadinessMapError(f"{_rel(path)}: T385 required_t385_packet_records missing {required}")

    must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T385 must_fail_if"))
    for required in (
        "T385_recommendation_is_treated_as_owner_selection",
        "Goal4_runs_without_explicit_owner_selection",
        "T385_strengthens_review_packet_without_owner_selection",
        "T385_promotes_reviewed_gold",
        "T385_changes_chunk_output",
        "T385_generates_graph_retrieval_or_vector_truth",
        "T385_changes_canon_scope_or_theology_authority",
    ):
        if required not in must_fail:
            raise ReadinessMapError(f"{_rel(path)}: T385 must_fail_if missing {required}")

    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "reviewed_gold_promoted",
        "review_packet_strengthening_authorized",
        "route_behavior_authorized",
        "child_spans_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "theology_authority_change_authorized",
        "sqlite_database_creation_authorized",
        "metadata_row_population_authorized",
    ):
        if next_route.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: T385 next_route.{key} must be false")


def _validate_t392_next_route(next_route: dict[str, Any], path: Path) -> None:
    expected = {
        "title": "Eph.1.3-Eph.1.14 Review Packet Strengthening",
        "starts_only_if": "explicit_owner_selection_of_T385_A",
        "completion_status": "complete_review_packet_strengthening_only",
        "selected_t376_option": "T376-A",
        "selected_lane": "epistle_argument",
        "selected_option": "T385-A",
        "selected_passage": "Eph.1.3-Eph.1.14",
        "selected_parent_candidate": "Eph.1.3-Eph.1.14",
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "review_packet_status": "pending_human_review",
        "review_packet_strengthened": True,
        "roadmap_doc": "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md",
        "validator": "scripts/validate_t392_eph1_review_packet_strengthening.py",
        "required_handoff": ".ai/handoffs/T392/handoff.md",
        "decision_register_entry": "CD-067",
        "lesson_index_entry": "LSN-021",
        "owner_selection_recorded": True,
        "owner_selection_record": ".ai/tasks/T392.task.yaml",
        "selection_mode": "owner_selected_review_packet_strengthening_only",
        "goal_4_completed": True,
        "owner_decision_required_before_promotion_or_implementation": True,
        "exact_target_selected_for_review_packet_strengthening_only": True,
        "exact_target_selected_for_promotion_or_implementation": False,
        "exact_next_owner_action": "Goal5_owner_reviewed_gold_promotion_decision_packet",
        "next_task": "T393",
    }
    for key, value in expected.items():
        if next_route.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T392 next_route.{key} must be {value!r}")
    if next_route.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T392 selected_children must be []")

    prior = next_route.get("prior_owner_packet")
    if not isinstance(prior, dict):
        raise ReadinessMapError(f"{_rel(path)}: T392 prior_owner_packet must be a mapping")
    expected_prior = {
        "task_id": "T385",
        "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
        "roadmap_doc": "docs/roadmap/T385_OWNER_DECISION_PACKET.md",
        "validator": "scripts/validate_t385_owner_decision_packet.py",
        "owner_selection_status": "pending",
        "recommended_option": "T385-A",
        "recommended_passage": "Eph.1.3-Eph.1.14",
        "recommendation_is_owner_selection": False,
        "decision_register_entry": "CD-066",
        "lesson_index_entry": "LSN-020",
    }
    for key, value in expected_prior.items():
        if prior.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T392 prior_owner_packet.{key} must be {value!r}")

    inputs = next_route.get("prior_readiness_inputs")
    if not isinstance(inputs, list):
        raise ReadinessMapError(f"{_rel(path)}: T392 prior_readiness_inputs must be a list")
    input_ids = {item.get("task_id") for item in inputs if isinstance(item, dict)}
    for required in {"T384", "T386", "T386-docket", "T387", "T388", "T389", "T390", "T385"}:
        if required not in input_ids:
            raise ReadinessMapError(f"{_rel(path)}: T392 prior_readiness_inputs missing {required}")

    prior_entries = set(
        _require_string_list(next_route.get("prior_decision_register_entries"), "T392 prior_decision_register_entries")
    )
    for required in {"CD-061", "CD-062", "CD-063", "CD-064", "CD-065", "CD-066", "CD-067"}:
        if required not in prior_entries:
            raise ReadinessMapError(f"{_rel(path)}: T392 prior_decision_register_entries missing {required}")

    must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T392 must_fail_if"))
    for required in (
        "T392_owner_selection_is_treated_as_reviewed_gold",
        "T392_strengthened_packet_is_treated_as_chunk_output_authority",
        "T392_adds_child_spans",
        "T392_changes_chunk_output",
        "T392_changes_route_or_evaluator_behavior",
        "T392_generates_graph_retrieval_or_vector_truth",
        "T392_imports_boundary_or_source_tradition_authority",
        "T392_changes_canon_scope_or_theology_authority",
        "Goal5_promotion_runs_without_owner_decision_packet",
    ):
        if required not in must_fail:
            raise ReadinessMapError(f"{_rel(path)}: T392 must_fail_if missing {required}")

    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "reviewed_gold_promoted",
        "route_behavior_authorized",
        "child_spans_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "theology_authority_change_authorized",
        "sqlite_database_creation_authorized",
        "metadata_row_population_authorized",
    ):
        if next_route.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: T392 next_route.{key} must be false")
    if next_route.get("review_packet_strengthening_authorized") is not True:
        raise ReadinessMapError(f"{_rel(path)}: T392 review_packet_strengthening_authorized must be true")


def _validate_t393_next_route(next_route: dict[str, Any], path: Path) -> None:
    expected = {
        "title": "Eph.1.3-Eph.1.14 Reviewed-Gold Promotion Decision Packet",
        "starts_only_if": "T392_eph1_review_packet_strengthening_complete",
        "completion_status": "pending_owner_reviewed_gold_promotion_decision",
        "selected_t376_option": "T376-A",
        "selected_lane": "epistle_argument",
        "selected_t385_option": "T385-A",
        "selected_passage": "Eph.1.3-Eph.1.14",
        "selected_parent_candidate": "Eph.1.3-Eph.1.14",
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
        "owner_selection_status": "pending",
        "recommended_option": "T393-A",
        "recommendation_is_owner_selection": False,
        "variant_dependency_non_authorizing_assessment": "current_repo_variant_non_dependent_for_parent_boundary_and_reviewed_gold_claim",
        "child_span_necessity_non_authorizing_assessment": "child_spans_not_necessary_for_parent_only_reviewed_gold_now",
        "roadmap_doc": "docs/roadmap/T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md",
        "validator": "scripts/validate_t393_eph1_reviewed_gold_promotion_decision_packet.py",
        "required_handoff": ".ai/handoffs/T393/handoff.md",
        "decision_register_entry": "CD-068",
        "lesson_index_entry": "LSN-022",
        "goal_5_packet_prepared": True,
        "owner_decision_required_before_promotion_or_implementation": True,
        "reviewed_gold_promoted": False,
        "next_task_if_owner_selects_promotion": "T394",
        "exact_next_owner_action": "owner_select_one_T393_option_before_promotion",
    }
    for key, value in expected.items():
        if next_route.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T393 next_route.{key} must be {value!r}")
    if next_route.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T393 selected_children must be []")
    if next_route.get("exact_internal_variant_refs") != []:
        raise ReadinessMapError(f"{_rel(path)}: T393 exact_internal_variant_refs must be []")

    strengthening = next_route.get("prior_strengthening")
    if not isinstance(strengthening, dict):
        raise ReadinessMapError(f"{_rel(path)}: T393 prior_strengthening must be a mapping")
    expected_strengthening = {
        "task_id": "T392",
        "review_packet_strengthened": True,
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "roadmap_doc": "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md",
        "validator": "scripts/validate_t392_eph1_review_packet_strengthening.py",
        "required_handoff": ".ai/handoffs/T392/handoff.md",
        "decision_register_entry": "CD-067",
        "lesson_index_entry": "LSN-021",
        "selected_option": "T385-A",
        "reviewed_gold_promoted": False,
    }
    for key, value in expected_strengthening.items():
        if strengthening.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T393 prior_strengthening.{key} must be {value!r}")
    if strengthening.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T393 prior_strengthening.selected_children must be []")

    prior = next_route.get("prior_owner_packet")
    if not isinstance(prior, dict):
        raise ReadinessMapError(f"{_rel(path)}: T393 prior_owner_packet must be a mapping")
    expected_prior = {
        "task_id": "T385",
        "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
        "roadmap_doc": "docs/roadmap/T385_OWNER_DECISION_PACKET.md",
        "validator": "scripts/validate_t385_owner_decision_packet.py",
        "owner_selection_status": "pending",
        "recommended_option": "T385-A",
        "recommended_passage": "Eph.1.3-Eph.1.14",
        "recommendation_is_owner_selection": False,
        "decision_register_entry": "CD-066",
        "lesson_index_entry": "LSN-020",
    }
    for key, value in expected_prior.items():
        if prior.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T393 prior_owner_packet.{key} must be {value!r}")

    inputs = next_route.get("prior_readiness_inputs")
    if not isinstance(inputs, list):
        raise ReadinessMapError(f"{_rel(path)}: T393 prior_readiness_inputs must be a list")
    input_ids = {item.get("task_id") for item in inputs if isinstance(item, dict)}
    for required in {"T384", "T386", "T386-docket", "T387", "T388", "T389", "T390", "T385", "T392"}:
        if required not in input_ids:
            raise ReadinessMapError(f"{_rel(path)}: T393 prior_readiness_inputs missing {required}")

    prior_entries = set(
        _require_string_list(next_route.get("prior_decision_register_entries"), "T393 prior_decision_register_entries")
    )
    for required in {"CD-061", "CD-062", "CD-063", "CD-064", "CD-065", "CD-066", "CD-067", "CD-068"}:
        if required not in prior_entries:
            raise ReadinessMapError(f"{_rel(path)}: T393 prior_decision_register_entries missing {required}")

    must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T393 must_fail_if"))
    for required in (
        "T393_recommendation_is_treated_as_owner_selection",
        "T393_packet_promotes_reviewed_gold_without_owner_authorization",
        "T393_adds_child_spans",
        "T393_changes_chunk_output",
        "T393_changes_route_or_evaluator_behavior",
        "T393_generates_graph_retrieval_or_vector_truth",
        "T393_imports_boundary_or_source_tradition_authority",
        "T393_changes_canon_scope_or_theology_authority",
        "Goal6_harness_runs_without_owner_promoted_gold",
    ):
        if required not in must_fail:
            raise ReadinessMapError(f"{_rel(path)}: T393 must_fail_if missing {required}")

    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "review_packet_strengthening_authorized",
        "route_behavior_authorized",
        "child_spans_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "theology_authority_change_authorized",
        "sqlite_database_creation_authorized",
        "metadata_row_population_authorized",
    ):
        if next_route.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: T393 next_route.{key} must be false")


def _validate_t397_next_route(next_route: dict[str, Any], path: Path) -> None:
    expected = {
        "title": "Eph.1.3-Eph.1.14 Route-Isolated Harness Prep",
        "starts_only_if": "T394_eph1_parent_only_reviewed_gold_promoted",
        "completion_status": "complete_non_output_changing_route_isolation_harness_prep",
        "completion_surface": ".ai/control/t397_eph1_route_isolation_harness.yaml",
        "selected_t376_option": "T376-A",
        "selected_lane": "epistle_argument",
        "selected_t385_option": "T385-A",
        "selected_passage": "Eph.1.3-Eph.1.14",
        "selected_parent_candidate": "Eph.1.3-Eph.1.14",
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
        "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
        "owner_selection_status": "selected",
        "selected_option": "T393-A",
        "recommendation_is_owner_selection": False,
        "variant_dependency_non_authorizing_assessment": "current_repo_variant_non_dependent_for_parent_boundary_and_reviewed_gold_claim",
        "child_span_necessity_non_authorizing_assessment": "child_spans_not_necessary_for_parent_only_reviewed_gold_now",
        "harness_script": "scripts/chunking/route_isolation_harness.py",
        "roadmap_doc": "docs/roadmap/T397_EPH1_ROUTE_ISOLATION_HARNESS.md",
        "validator": "scripts/validate_t397_eph1_route_isolation_harness.py",
        "required_handoff": ".ai/handoffs/T397/handoff.md",
        "decision_register_entry": "CD-074",
        "lesson_index_entry": "LSN-028",
        "goal_5_packet_prepared": True,
        "owner_decision_required_before_promotion_or_implementation": False,
        "reviewed_gold_promoted": True,
        "route_isolation_harness_ready": True,
        "non_target_identity_harness_ready": True,
        "exact_parent_only_change_shape_harness_ready": True,
        "spillover_denial_harness_ready": True,
        "child_span_denial_harness_ready": True,
        "same_baseline_report_shape_ready": True,
        "future_output_pilot_owner_authorization_required": True,
        "exact_next_owner_action": "future_owner_output_pilot_authorization_gate_for_Eph_1_3_Eph_1_14",
    }
    for key, value in expected.items():
        if next_route.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T397 next_route.{key} must be {value!r}")
    harness_tests = set(_require_string_list(next_route.get("harness_tests"), "T397 harness_tests"))
    for required in {
        "tests/test_route_isolation_harness.py",
        "tests/test_t397_eph1_route_isolation_harness.py",
    }:
        if required not in harness_tests:
            raise ReadinessMapError(f"{_rel(path)}: T397 harness_tests missing {required}")
    if next_route.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T397 selected_children must be []")
    if next_route.get("exact_internal_variant_refs") != []:
        raise ReadinessMapError(f"{_rel(path)}: T397 exact_internal_variant_refs must be []")

    strengthening = next_route.get("prior_strengthening")
    if not isinstance(strengthening, dict):
        raise ReadinessMapError(f"{_rel(path)}: T397 prior_strengthening must be a mapping")
    expected_strengthening = {
        "task_id": "T392",
        "review_packet_strengthened": True,
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "roadmap_doc": "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md",
        "validator": "scripts/validate_t392_eph1_review_packet_strengthening.py",
        "required_handoff": ".ai/handoffs/T392/handoff.md",
        "decision_register_entry": "CD-067",
        "lesson_index_entry": "LSN-021",
        "selected_option": "T385-A",
        "reviewed_gold_promoted": False,
    }
    for key, value in expected_strengthening.items():
        if strengthening.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T397 prior_strengthening.{key} must be {value!r}")
    if strengthening.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T397 prior_strengthening.selected_children must be []")

    prior = next_route.get("prior_owner_packet")
    if not isinstance(prior, dict):
        raise ReadinessMapError(f"{_rel(path)}: T397 prior_owner_packet must be a mapping")
    expected_prior = {
        "task_id": "T385",
        "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
        "roadmap_doc": "docs/roadmap/T385_OWNER_DECISION_PACKET.md",
        "validator": "scripts/validate_t385_owner_decision_packet.py",
        "owner_selection_status": "pending",
        "recommended_option": "T385-A",
        "recommended_passage": "Eph.1.3-Eph.1.14",
        "recommendation_is_owner_selection": False,
        "decision_register_entry": "CD-066",
        "lesson_index_entry": "LSN-020",
    }
    for key, value in expected_prior.items():
        if prior.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T397 prior_owner_packet.{key} must be {value!r}")

    inputs = next_route.get("prior_readiness_inputs")
    if not isinstance(inputs, list):
        raise ReadinessMapError(f"{_rel(path)}: T397 prior_readiness_inputs must be a list")
    input_ids = {item.get("task_id") for item in inputs if isinstance(item, dict)}
    for required in {"T384", "T386", "T386-docket", "T387", "T388", "T389", "T390", "T385", "T392"}:
        if required not in input_ids:
            raise ReadinessMapError(f"{_rel(path)}: T397 prior_readiness_inputs missing {required}")

    prior_entries = set(
        _require_string_list(next_route.get("prior_decision_register_entries"), "T397 prior_decision_register_entries")
    )
    for required in {"CD-061", "CD-062", "CD-063", "CD-064", "CD-065", "CD-066", "CD-067", "CD-068", "CD-071", "CD-074"}:
        if required not in prior_entries:
            raise ReadinessMapError(f"{_rel(path)}: T397 prior_decision_register_entries missing {required}")

    must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T397 must_fail_if"))
    for required in (
        "T397_harness_changes_chunk_output",
        "T397_harness_changes_route_or_evaluator_behavior",
        "T397_harness_generates_graph_retrieval_or_vector_truth",
        "T397_harness_adds_child_spans",
        "T397_harness_imports_boundary_or_source_tradition_authority",
        "T397_harness_changes_canon_scope_or_theology_authority",
        "T397_harness_creates_source_or_manuscript_rows",
        "T397_harness_treats_reviewed_gold_as_output_authority",
        "T397_harness_is_treated_as_output_authority",
        "future_output_pilot_starts_without_explicit_owner_authorization",
    ):
        if required not in must_fail:
            raise ReadinessMapError(f"{_rel(path)}: T397 must_fail_if missing {required}")

    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "review_packet_strengthening_authorized",
        "route_behavior_authorized",
        "child_spans_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "theology_authority_change_authorized",
        "sqlite_database_creation_authorized",
        "metadata_row_population_authorized",
        "source_or_manuscript_rows_authorized",
    ):
        if next_route.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: T397 next_route.{key} must be false")


def _validate_t401_next_route(next_route: dict[str, Any], path: Path) -> None:
    expected = {
        "title": "Eph.1.3-Eph.1.14 Exact Output Pilot",
        "starts_only_if": "T397_route_isolation_harness_complete_and_owner_authorized_exact_output_pilot",
        "completion_status": "complete_output_changed_eph1_parent_overlay",
        "completion_surface": ".ai/control/t401_eph1_output_pilot_manifest.yaml",
        "selected_t376_option": "T376-A",
        "selected_lane": "epistle_argument",
        "selected_t385_option": "T385-A",
        "selected_passage": "Eph.1.3-Eph.1.14",
        "selected_parent_candidate": "Eph.1.3-Eph.1.14",
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
        "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
        "owner_selection_status": "selected",
        "selected_option": "T393-A",
        "recommendation_is_owner_selection": False,
        "variant_dependency_non_authorizing_assessment": "current_repo_variant_non_dependent_for_parent_boundary_and_reviewed_gold_claim",
        "child_span_necessity_non_authorizing_assessment": "child_spans_not_necessary_for_parent_only_reviewed_gold_now",
        "harness_script": "scripts/chunking/route_isolation_harness.py",
        "output_manifest": ".ai/control/t401_eph1_output_pilot_manifest.yaml",
        "roadmap_doc": "docs/roadmap/T401_EPH1_OUTPUT_PILOT.md",
        "validator": "scripts/validate_t401_eph1_output_pilot.py",
        "required_handoff": ".ai/handoffs/T401/handoff.md",
        "decision_register_entry": "CD-076",
        "lesson_index_entry": "LSN-030",
        "goal_5_packet_prepared": True,
        "owner_decision_required_before_promotion_or_implementation": False,
        "reviewed_gold_promoted": True,
        "route_isolation_harness_ready": True,
        "non_target_identity_harness_ready": True,
        "exact_parent_only_change_shape_harness_ready": True,
        "spillover_denial_harness_ready": True,
        "child_span_denial_harness_ready": True,
        "same_baseline_report_shape_ready": True,
        "future_output_pilot_owner_authorization_required": False,
        "exact_next_owner_action": "T402_post_pilot_review_before_child_spans_or_broader_behavior",
        "output_pilot_complete": True,
        "parent_span_as_chunk_boundary_authorized_for_exact_pilot": True,
        "same_baseline_evaluated": True,
        "no_context_audit_surface": ".ai/audits/reports/20260625-T401-eph1-output-pilot.md",
        "baseline_chunk_count": 1137,
        "candidate_chunk_count": 1138,
        "added_overlay_count": 1,
        "baseline_prefix_matches_pre_t401_bytes": True,
        "non_target_output_diff_detected": False,
        "overlay_id": "chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--Eph.1.3--Eph.1.14--T401-EPH1-PILOT",
        "output_change_authorized": True,
        "implementation_authorized": True,
        "route_behavior_authorized": True,
        "route_behavior_authorization_scope": "exact_t401_eph1_parent_overlay_only",
    }
    for key, value in expected.items():
        if next_route.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T401 next_route.{key} must be {value!r}")
    harness_tests = set(_require_string_list(next_route.get("harness_tests"), "T401 harness_tests"))
    for required in {
        "tests/test_route_isolation_harness.py",
        "tests/test_t397_eph1_route_isolation_harness.py",
    }:
        if required not in harness_tests:
            raise ReadinessMapError(f"{_rel(path)}: T401 harness_tests missing {required}")
    if next_route.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T401 selected_children must be []")
    if next_route.get("exact_internal_variant_refs") != []:
        raise ReadinessMapError(f"{_rel(path)}: T401 exact_internal_variant_refs must be []")

    strengthening = next_route.get("prior_strengthening")
    if not isinstance(strengthening, dict):
        raise ReadinessMapError(f"{_rel(path)}: T401 prior_strengthening must be a mapping")
    expected_strengthening = {
        "task_id": "T392",
        "review_packet_strengthened": True,
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "roadmap_doc": "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md",
        "validator": "scripts/validate_t392_eph1_review_packet_strengthening.py",
        "required_handoff": ".ai/handoffs/T392/handoff.md",
        "decision_register_entry": "CD-067",
        "lesson_index_entry": "LSN-021",
        "selected_option": "T385-A",
        "reviewed_gold_promoted": False,
    }
    for key, value in expected_strengthening.items():
        if strengthening.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T401 prior_strengthening.{key} must be {value!r}")
    if strengthening.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T401 prior_strengthening.selected_children must be []")

    prior = next_route.get("prior_owner_packet")
    if not isinstance(prior, dict):
        raise ReadinessMapError(f"{_rel(path)}: T401 prior_owner_packet must be a mapping")
    expected_prior = {
        "task_id": "T385",
        "owner_packet": ".ai/control/t385_owner_decision_packet.yaml",
        "roadmap_doc": "docs/roadmap/T385_OWNER_DECISION_PACKET.md",
        "validator": "scripts/validate_t385_owner_decision_packet.py",
        "owner_selection_status": "pending",
        "recommended_option": "T385-A",
        "recommended_passage": "Eph.1.3-Eph.1.14",
        "recommendation_is_owner_selection": False,
        "decision_register_entry": "CD-066",
        "lesson_index_entry": "LSN-020",
    }
    for key, value in expected_prior.items():
        if prior.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T401 prior_owner_packet.{key} must be {value!r}")

    inputs = next_route.get("prior_readiness_inputs")
    if not isinstance(inputs, list):
        raise ReadinessMapError(f"{_rel(path)}: T401 prior_readiness_inputs must be a list")
    input_ids = {item.get("task_id") for item in inputs if isinstance(item, dict)}
    for required in {"T384", "T386", "T386-docket", "T387", "T388", "T389", "T390", "T385", "T392"}:
        if required not in input_ids:
            raise ReadinessMapError(f"{_rel(path)}: T401 prior_readiness_inputs missing {required}")

    prior_entries = set(
        _require_string_list(next_route.get("prior_decision_register_entries"), "T401 prior_decision_register_entries")
    )
    for required in {"CD-061", "CD-062", "CD-063", "CD-064", "CD-065", "CD-066", "CD-067", "CD-068", "CD-071", "CD-074", "CD-076"}:
        if required not in prior_entries:
            raise ReadinessMapError(f"{_rel(path)}: T401 prior_decision_register_entries missing {required}")

    must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T401 must_fail_if"))
    for required in (
        "T401_changes_any_non_target_output_record",
        "T401_adds_child_spans",
        "T401_deletes_or_replaces_existing_chunks",
        "T401_generates_graph_retrieval_or_vector_truth",
        "T401_changes_evaluator_or_leaderboard",
        "T401_imports_boundary_or_source_tradition_authority",
        "T401_changes_canon_scope_or_theology_authority",
        "T401_creates_source_or_manuscript_rows",
        "T401_overlay_is_treated_as_truth_bearing_hierarchy",
        "future_child_span_work_starts_without_post_pilot_review_and_owner_gate",
    ):
        if required not in must_fail:
            raise ReadinessMapError(f"{_rel(path)}: T401 must_fail_if missing {required}")

    for key in (
        "review_packet_strengthening_authorized",
        "child_spans_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "theology_authority_change_authorized",
        "sqlite_database_creation_authorized",
        "metadata_row_population_authorized",
        "source_or_manuscript_rows_authorized",
    ):
        if next_route.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: T401 next_route.{key} must be false")


def _validate_t415_next_route(next_route: dict[str, Any], path: Path) -> None:
    expected = {
        "title": "T411 Batch1 Output Pilot",
        "route_type": "epistle_opening_goal7_exact_output_pilot",
        "completion_status": "complete_output_changed_batch1_parent_overlays",
        "completion_surface": ".ai/control/t415_batch1_output_pilot_manifest.yaml",
        "output_manifest": ".ai/control/t415_batch1_output_pilot_manifest.yaml",
        "validator": "scripts/validate_t415_batch1_output_pilot.py",
        "decision_register_entry": "CD-082",
        "lesson_index_entry": "LSN-037",
        "baseline_chunk_count": 1138,
        "candidate_chunk_count": 1143,
        "added_overlay_count": 5,
        "output_change_authorized": True,
        "implementation_authorized": True,
        "route_behavior_authorized": True,
        "child_spans_authorized": False,
    }
    for key, value in expected.items():
        if next_route.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: T415 next_route.{key} must be {value!r}")
    prior_strengthening = next_route.get("prior_strengthening")
    if not isinstance(prior_strengthening, dict):
        raise ReadinessMapError(f"{_rel(path)}: T415 prior_strengthening must be a mapping")
    if prior_strengthening.get("task_id") != "T413":
        raise ReadinessMapError(f"{_rel(path)}: T415 prior_strengthening.task_id must be T413")
    prior_promotion = next_route.get("prior_promotion")
    if not isinstance(prior_promotion, dict):
        raise ReadinessMapError(f"{_rel(path)}: T415 prior_promotion must be a mapping")
    if prior_promotion.get("task_id") != "T414":
        raise ReadinessMapError(f"{_rel(path)}: T415 prior_promotion.task_id must be T414")


def validate_readiness_map(path: Path = READINESS_MAP) -> dict[str, Any]:
    data = _read_yaml(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise ReadinessMapError(f"{_rel(path)}: missing top-level keys {missing}")

    if data["object_type"] != "bible_chunking_readiness_map":
        raise ReadinessMapError(f"{_rel(path)}: object_type must be bible_chunking_readiness_map")
    if data["trust_zone"] != "canonical":
        raise ReadinessMapError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise ReadinessMapError(f"{_rel(path)}: lifecycle_status must be active")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise ReadinessMapError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_readiness") is not True:
        raise ReadinessMapError(f"{_rel(path)}: authority.records_readiness must be true")
    for forbidden in (
        "authorizes_chunk_output_change",
        "authorizes_new_algorithm_work",
        "authorizes_reviewed_gold_promotion",
        "authorizes_skill_lifecycle_promotion",
        "authorizes_boundary_import",
    ):
        if authority.get(forbidden) is not False:
            raise ReadinessMapError(f"{_rel(path)}: authority.{forbidden} must be false")

    model = data["faithful_execution_model"]
    if not isinstance(model, dict):
        raise ReadinessMapError(f"{_rel(path)}: faithful_execution_model must be a mapping")
    if model.get("route") != "one_lane_at_a_time_under_bible_wide_map":
        raise ReadinessMapError(f"{_rel(path)}: faithful route must stay one lane at a time")
    _require_string(model.get("rationale"), "faithful_execution_model.rationale")
    _require_string(model.get("bible_wide_goal"), "faithful_execution_model.bible_wide_goal")

    lessons = data["lessons_storage"]
    if not isinstance(lessons, dict):
        raise ReadinessMapError(f"{_rel(path)}: lessons_storage must be a mapping")
    surfaces = set(_require_string_list(lessons.get("surfaces"), "lessons_storage.surfaces"))
    missing_surfaces = sorted(REQUIRED_LESSON_SURFACES - surfaces)
    if missing_surfaces:
        raise ReadinessMapError(f"{_rel(path)}: lessons_storage missing {missing_surfaces}")
    _require_string(lessons.get("rule"), "lessons_storage.rule")

    algorithms = data["algorithm_readiness"]
    if not isinstance(algorithms, dict):
        raise ReadinessMapError(f"{_rel(path)}: algorithm_readiness must be a mapping")
    missing_algorithms = sorted(REQUIRED_ALGORITHMS - set(algorithms))
    if missing_algorithms:
        raise ReadinessMapError(f"{_rel(path)}: algorithm_readiness missing {missing_algorithms}")
    for algorithm_id, algorithm in algorithms.items():
        if not isinstance(algorithm, dict):
            raise ReadinessMapError(f"{_rel(path)}:{algorithm_id}: algorithm entry must be a mapping")
        _require_string(algorithm.get("status"), f"algorithm_readiness.{algorithm_id}.status")
        _require_string(algorithm.get("role"), f"algorithm_readiness.{algorithm_id}.role")
        if algorithm.get("output_change_authorized") is not False:
            raise ReadinessMapError(f"{_rel(path)}:{algorithm_id}: output_change_authorized must be false")

    lanes = data["lane_sequence"]
    if not isinstance(lanes, list) or not lanes:
        raise ReadinessMapError(f"{_rel(path)}: lane_sequence must be a non-empty list")
    lane_ids: set[str] = set()
    implementation_orders: list[int] = []
    for lane in lanes:
        if not isinstance(lane, dict):
            raise ReadinessMapError(f"{_rel(path)}: each lane must be a mapping")
        lane_id = lane.get("lane_id")
        _require_string(lane_id, "lane_sequence.lane_id")
        if lane_id in lane_ids:
            raise ReadinessMapError(f"{_rel(path)}:{lane_id}: duplicate lane_id")
        lane_ids.add(lane_id)
        if not isinstance(lane.get("implementation_order"), int):
            raise ReadinessMapError(f"{_rel(path)}:{lane_id}: implementation_order must be an integer")
        implementation_orders.append(lane["implementation_order"])
        _require_string(lane.get("current_state"), f"lane_sequence.{lane_id}.current_state")
        _require_string(lane.get("theological_risk"), f"lane_sequence.{lane_id}.theological_risk")
        if lane_id == "epistle_argument" and lane.get("current_state") == "t373_a_authorized_exact_parent_only_t374_pilot_next":
            if lane.get("new_algorithm_work_ready") is not True:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be true after T373-A")
        elif lane_id == "epistle_argument" and lane.get("current_state") == "t374_baseline_overlap_owner_decision_required":
            if lane.get("new_algorithm_work_ready") is not False:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be false while T374 overlap owner decision is pending")
        elif lane_id == "epistle_argument" and lane.get("current_state") == "t374_overlap_b_selected_additive_overlay_ready":
            if lane.get("new_algorithm_work_ready") is not True:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be true after T374-OVERLAP-B")
        elif lane_id == "epistle_argument" and lane.get("current_state") == "t374_additive_parent_overlay_implemented_post_pilot_review_next":
            if lane.get("new_algorithm_work_ready") is not False:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be false while T375 review is next")
            implementation = lane.get("additive_parent_overlay_implementation")
            if not isinstance(implementation, dict):
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: additive_parent_overlay_implementation must be present")
            expected_implementation = {
                "task_id": "T374",
                "path": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
                "status": "complete_output_changed_additive_parent_overlay",
                "selected_option": "T374-OVERLAP-B",
                "selected_parent": "1Cor.8.1-1Cor.10.33",
                "baseline_chunk_count": 1136,
                "candidate_chunk_count": 1137,
                "added_overlay_count": 1,
                "baseline_prefix_matches_pre_t374_bytes": True,
                "non_target_output_diff_detected": False,
                "next_review_task": "T375",
            }
            for key, value in expected_implementation.items():
                if implementation.get(key) != value:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: additive_parent_overlay_implementation.{key} must be {value!r}")
            if implementation.get("selected_children") != []:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: additive_parent_overlay_implementation.selected_children must be []")
            for key in (
                "child_spans_authorized",
                "evaluator_change_authorized",
                "graph_edge_generation_allowed",
                "retrieval_truth_authorized",
            ):
                if implementation.get(key) is not False:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: additive_parent_overlay_implementation.{key} must be false")
        elif lane_id == "epistle_argument" and lane.get("current_state") == "t375_post_pilot_review_complete_next_lane_selection_required":
            if lane.get("new_algorithm_work_ready") is not False:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be false while T376 owner lane selection is next")
            implementation = lane.get("additive_parent_overlay_implementation")
            if not isinstance(implementation, dict):
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: additive_parent_overlay_implementation must be present")
            if implementation.get("task_id") != "T374":
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: additive_parent_overlay_implementation.task_id must be T374")
            review = lane.get("post_pilot_review")
            if not isinstance(review, dict):
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: post_pilot_review must be present")
            expected_review = {
                "task_id": "T375",
                "path": ".ai/control/t375_post_pilot_review.yaml",
                "status": "complete_review_only_child_spans_not_necessary_now",
                "selected_parent": "1Cor.8.1-1Cor.10.33",
                "same_baseline_reviewed": True,
                "no_context_audit_reviewed": True,
                "child_necessity_reviewed": True,
                "child_spans_necessary_now": False,
                "child_spans_authorized": False,
                "output_change_authorized": False,
                "implementation_authorized": False,
                "route_behavior_authorized": False,
                "evaluator_change_authorized": False,
                "graph_edge_generation_allowed": False,
                "retrieval_truth_authorized": False,
                "next_route": "T376",
            }
            for key, value in expected_review.items():
                if review.get(key) != value:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: post_pilot_review.{key} must be {value!r}")
            if review.get("selected_children") != []:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: post_pilot_review.selected_children must be []")
        elif lane_id == "epistle_argument" and lane.get("current_state") == "t376_a_epistle_research_runway_selected_next_t384_options_matrix":
            if lane.get("new_algorithm_work_ready") is not False:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be false while T384 research/options is next")
            review = lane.get("post_pilot_review")
            if not isinstance(review, dict) or review.get("task_id") != "T375":
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: T375 post_pilot_review must remain recorded")
            if review.get("next_route") != "T376":
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: T375 post_pilot_review.next_route must remain T376")
            selection = lane.get("research_runway_selection")
            if not isinstance(selection, dict):
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: research_runway_selection must be present")
            expected_selection = {
                "task_id": "T376",
                "path": ".ai/control/t376_epistle_research_runway.yaml",
                "status": "complete_selected_research_first_epistle_argument_runway",
                "selected_option": "T376-A",
                "selected_lane": "epistle_argument",
                "selected_lane_mode": "research_and_prep_only",
                "lesson": "research_autonomy_is_not_authority_autonomy",
                "decision_register_entry": "CD-060",
                "exact_target_selected": False,
                "next_route": "T384",
            }
            for key, value in expected_selection.items():
                if selection.get(key) != value:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: research_runway_selection.{key} must be {value!r}")
            _require_string_list(selection.get("may_continue_without_new_owner_decision"), "research_runway_selection.may_continue_without_new_owner_decision")
            must_stop = set(_require_string_list(selection.get("must_stop_for_owner_decision_before"), "research_runway_selection.must_stop_for_owner_decision_before"))
            for item in (
                "exact_epistle_target_selection_for_promotion_or_implementation",
                "reviewed_gold_promotion",
                "child_span_selection_or_child_span_reviewed_gold",
                "chunk_output_change",
                "graph_edge_generation",
                "denominational_systematic_theology_as_chunk_authority",
            ):
                if item not in must_stop:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: research_runway_selection must_stop missing {item}")
            for key in (
                "output_change_authorized",
                "implementation_authorized",
                "reviewed_gold_promoted",
                "child_spans_authorized",
                "route_behavior_authorized",
                "evaluator_change_authorized",
                "graph_edge_generation_allowed",
                "retrieval_truth_authorized",
            ):
                if selection.get(key) is not False:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: research_runway_selection.{key} must be false")
        elif lane_id == "epistle_argument" and lane.get("current_state") in {
            "t397_eph1_route_isolation_harness_complete_future_owner_gate_next",
            "t401_eph1_output_pilot_complete_post_pilot_review_next",
        }:
            if lane.get("new_algorithm_work_ready") is not False:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be false while the next stop is owner-gated")

            packet = lane.get("eph1_reviewed_gold_promotion_decision_packet")
            if not isinstance(packet, dict):
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_reviewed_gold_promotion_decision_packet must be present")
            expected_packet = {
                "task_id": "T393",
                "path": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
                "status": "resolved_by_t393_a",
                "selected_option_from_t385": "T385-A",
                "selected_passage": "Eph.1.3-Eph.1.14",
                "selected_parent_candidate": "Eph.1.3-Eph.1.14",
                "source_review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
                "strengthening_task": "T392",
                "decision_register_entry": "CD-068",
                "lesson_index_entry": "LSN-022",
                "roadmap_doc": "docs/roadmap/T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md",
                "validator": "scripts/validate_t393_eph1_reviewed_gold_promotion_decision_packet.py",
                "owner_selection_status": "selected",
                "selected_option": "T393-A",
                "owner_response_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
                "recommended_option": "T393-A",
                "recommendation_is_owner_selection": False,
                "variant_dependency_non_authorizing_assessment": "current_repo_variant_non_dependent_for_parent_boundary_and_reviewed_gold_claim",
                "child_span_necessity_non_authorizing_assessment": "child_spans_not_necessary_for_parent_only_reviewed_gold_now",
                "next_owner_gate": "resolved_by_t394",
            }
            for key, value in expected_packet.items():
                if packet.get(key) != value:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_reviewed_gold_promotion_decision_packet.{key} must be {value!r}")
            if packet.get("selected_children") != []:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_reviewed_gold_promotion_decision_packet.selected_children must be []")
            if packet.get("exact_internal_variant_refs") != []:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_reviewed_gold_promotion_decision_packet.exact_internal_variant_refs must be []")
            for key in (
                "output_change_authorized",
                "implementation_authorized",
                "reviewed_gold_promoted",
                "child_spans_authorized",
                "route_behavior_authorized",
                "evaluator_change_authorized",
                "graph_edge_generation_allowed",
                "retrieval_truth_authorized",
                "embedding_or_vector_work_allowed",
                "boundary_import_allowed",
                "preferred_reading_authorized",
                "source_tradition_preference_authorized",
                "canon_scope_change_authorized",
                "theology_authority_change_authorized",
            ):
                if packet.get(key) is not False:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_reviewed_gold_promotion_decision_packet.{key} must be false")

            promotion = lane.get("eph1_parent_only_reviewed_gold_promotion")
            if not isinstance(promotion, dict):
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_parent_only_reviewed_gold_promotion must be present")
            expected_promotion = {
                "task_id": "T394",
                "path": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
                "status": "complete_parent_only_reviewed_gold_promoted",
                "selected_option": "T393-A",
                "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
                "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
                "selected_parent": "Eph.1.3-Eph.1.14",
                "boundary_dependency_or_non_dependency": "current_repo_variant_non_dependent",
                "reviewed_gold_dependency_or_non_dependency": "current_repo_variant_non_dependent",
                "source_tradition_dependency_or_non_dependency": "current_repo_source_tradition_non_dependent",
                "next_task": "T397",
            }
            for key, value in expected_promotion.items():
                if promotion.get(key) != value:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_parent_only_reviewed_gold_promotion.{key} must be {value!r}")
            if promotion.get("selected_children") != []:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_parent_only_reviewed_gold_promotion.selected_children must be []")
            if promotion.get("exact_internal_variant_refs") != []:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_parent_only_reviewed_gold_promotion.exact_internal_variant_refs must be []")
            if promotion.get("reviewed_gold_promoted") is not True:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_parent_only_reviewed_gold_promotion.reviewed_gold_promoted must be true")
            if promotion.get("child_spans_necessary_now") is not False:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_parent_only_reviewed_gold_promotion.child_spans_necessary_now must be false")
            for key in (
                "parent_span_as_chunk_boundary_authorized",
                "output_change_authorized",
                "implementation_authorized",
                "route_behavior_authorized",
                "evaluator_change_authorized",
                "graph_edge_generation_allowed",
                "retrieval_truth_authorized",
                "embedding_or_vector_work_allowed",
                "source_or_manuscript_rows_authorized",
            ):
                if promotion.get(key) is not False:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_parent_only_reviewed_gold_promotion.{key} must be false")

            harness = lane.get("eph1_route_isolation_harness")
            if not isinstance(harness, dict):
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_route_isolation_harness must be present")
            expected_harness = {
                "task_id": "T397",
                "path": ".ai/control/t397_eph1_route_isolation_harness.yaml",
                "status": "complete_non_output_changing_route_isolation_harness_prep",
                "selected_parent": "Eph.1.3-Eph.1.14",
                "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
                "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
                "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
                "harness_script": "scripts/chunking/route_isolation_harness.py",
                "validator": "scripts/validate_t397_eph1_route_isolation_harness.py",
                "decision_register_entry": "CD-074",
                "lesson_index_entry": "LSN-028",
                "reviewed_gold_promoted": True,
                "non_target_identity_harness_ready": True,
                "exact_parent_only_change_shape_harness_ready": True,
                "spillover_denial_harness_ready": True,
                "child_span_denial_harness_ready": True,
                "same_baseline_report_shape_ready": True,
                "future_output_pilot_owner_authorization_required": True,
            }
            for key, value in expected_harness.items():
                if harness.get(key) != value:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_route_isolation_harness.{key} must be {value!r}")
            if harness.get("selected_children") != []:
                raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_route_isolation_harness.selected_children must be []")
            harness_tests = set(_require_string_list(harness.get("tests"), "eph1_route_isolation_harness.tests"))
            for required in {
                "tests/test_route_isolation_harness.py",
                "tests/test_t397_eph1_route_isolation_harness.py",
            }:
                if required not in harness_tests:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_route_isolation_harness.tests missing {required}")
            for key in (
                "parent_span_as_chunk_boundary_authorized",
                "child_spans_authorized",
                "output_change_authorized",
                "implementation_authorized",
                "route_behavior_authorized",
                "evaluator_change_authorized",
                "graph_edge_generation_allowed",
                "retrieval_truth_authorized",
                "embedding_or_vector_work_allowed",
                "boundary_import_allowed",
                "preferred_reading_authorized",
                "source_tradition_preference_authorized",
                "canon_scope_change_authorized",
                "theology_authority_change_authorized",
                "sqlite_database_creation_authorized",
                "metadata_row_population_authorized",
                "source_or_manuscript_rows_authorized",
            ):
                if harness.get(key) is not False:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_route_isolation_harness.{key} must be false")
            if lane.get("current_state") == "t401_eph1_output_pilot_complete_post_pilot_review_next":
                output_pilot = lane.get("eph1_output_pilot")
                if not isinstance(output_pilot, dict):
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_output_pilot must be present")
                expected_output_pilot = {
                    "task_id": "T401",
                    "path": ".ai/control/t401_eph1_output_pilot_manifest.yaml",
                    "status": "complete_output_changed_eph1_parent_overlay",
                    "selected_parent": "Eph.1.3-Eph.1.14",
                    "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
                    "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
                    "promotion_record": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
                    "route_isolation_harness": ".ai/control/t397_eph1_route_isolation_harness.yaml",
                    "output_manifest": ".ai/control/t401_eph1_output_pilot_manifest.yaml",
                    "roadmap_doc": "docs/roadmap/T401_EPH1_OUTPUT_PILOT.md",
                    "validator": "scripts/validate_t401_eph1_output_pilot.py",
                    "decision_register_entry": "CD-076",
                    "lesson_index_entry": "LSN-030",
                    "reviewed_gold_promoted": True,
                    "route_isolation_harness_passed": True,
                    "same_baseline_evaluated": True,
                    "no_context_audit_surface": ".ai/audits/reports/20260625-T401-eph1-output-pilot.md",
                    "parent_span_as_chunk_boundary_authorized_for_exact_pilot": True,
                    "output_change_authorized": True,
                    "implementation_authorized": True,
                    "route_behavior_authorized_for_exact_target_overlay": True,
                    "chunk_output_changed": True,
                    "baseline_chunk_count": 1137,
                    "candidate_chunk_count": 1138,
                    "added_overlay_count": 1,
                    "baseline_prefix_matches_pre_t401_bytes": True,
                    "non_target_output_diff_detected": False,
                    "overlay_id": "chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--Eph.1.3--Eph.1.14--T401-EPH1-PILOT",
                    "next_review_task": "T402_post_pilot_review_before_child_spans_or_broader_behavior",
                }
                for key, value in expected_output_pilot.items():
                    if output_pilot.get(key) != value:
                        raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_output_pilot.{key} must be {value!r}")
                if output_pilot.get("selected_children") != []:
                    raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_output_pilot.selected_children must be []")
                pilot_tests = set(_require_string_list(output_pilot.get("tests"), "eph1_output_pilot.tests"))
                for required in {"tests/test_t401_eph1_output_pilot.py", "tests/test_chunking_orchestrator.py"}:
                    if required not in pilot_tests:
                        raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_output_pilot.tests missing {required}")
                for key in (
                    "child_spans_authorized",
                    "broader_epistle_generalization_authorized",
                    "evaluator_change_authorized",
                    "graph_edge_generation_allowed",
                    "retrieval_truth_authorized",
                    "embedding_or_vector_work_allowed",
                    "boundary_import_allowed",
                    "preferred_reading_authorized",
                    "source_tradition_preference_authorized",
                    "canon_scope_change_authorized",
                    "theology_authority_change_authorized",
                    "sqlite_database_creation_authorized",
                    "metadata_row_population_authorized",
                    "source_or_manuscript_rows_authorized",
                ):
                    if output_pilot.get(key) is not False:
                        raise ReadinessMapError(f"{_rel(path)}:{lane_id}: eph1_output_pilot.{key} must be false")
        elif lane.get("new_algorithm_work_ready") is not False:
            raise ReadinessMapError(f"{_rel(path)}:{lane_id}: new_algorithm_work_ready must be false")

    missing_lanes = sorted(REQUIRED_LANES - lane_ids)
    if missing_lanes:
        raise ReadinessMapError(f"{_rel(path)}: lane_sequence missing {missing_lanes}")
    if sorted(implementation_orders) != list(range(1, len(implementation_orders) + 1)):
        raise ReadinessMapError(f"{_rel(path)}: implementation_order values must be contiguous")

    next_route = data["next_route"]
    if not isinstance(next_route, dict):
        raise ReadinessMapError(f"{_rel(path)}: next_route must be a mapping")
    task_id = next_route.get("task_id")
    if task_id not in ALLOWED_NEXT_ROUTES:
        raise ReadinessMapError(
            f"{_rel(path)}: next_route.task_id must be one of {sorted(ALLOWED_NEXT_ROUTES)}"
        )
    expected_route_type = ALLOWED_NEXT_ROUTES[task_id]["route_type"]
    if next_route.get("route_type") != expected_route_type:
        raise ReadinessMapError(
            f"{_rel(path)}: next_route.route_type must be {expected_route_type} for {task_id}"
        )
    if task_id in {"T374", "T401", "T415"}:
        if next_route.get("output_change_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: {task_id} next_route.output_change_authorized must be true")
        if next_route.get("implementation_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: {task_id} next_route.implementation_authorized must be true")
    else:
        if next_route.get("output_change_authorized") is not False:
            raise ReadinessMapError(f"{_rel(path)}: next_route.output_change_authorized must be false")
        if next_route.get("implementation_authorized") is not False:
            raise ReadinessMapError(f"{_rel(path)}: next_route.implementation_authorized must be false")
    if task_id == "T385":
        _validate_t385_next_route(next_route, path)
    if task_id == "T392":
        _validate_t392_next_route(next_route, path)
    if task_id == "T393":
        _validate_t393_next_route(next_route, path)
    if task_id == "T397":
        _validate_t397_next_route(next_route, path)
    if task_id == "T401":
        _validate_t401_next_route(next_route, path)
    if task_id == "T415":
        _validate_t415_next_route(next_route, path)
    if task_id == "T384":
        expected_t384 = {
            "title": "Bible-Wide Research Readiness Synthesis",
            "starts_only_if": "T376_A_epistle_argument_research_runway_selected",
            "prior_lane_selection": ".ai/control/t376_epistle_research_runway.yaml",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "completion_surface": ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml",
            "completion_status": "complete_bible_wide_research_readiness_synthesis",
            "decision_register_entry": "CD-061",
            "lesson_index_entry": "LSN-013",
            "selected_t376_option": "T376-A",
            "selected_lane": "epistle_argument",
            "selection_mode": "bible_wide_research_readiness_complete_non_authorizing",
            "exact_next_non_output_step": "T385",
            "lesson": "research_autonomy_is_not_authority_autonomy",
        }
        for key, value in expected_t384.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T384 next_route.{key} must be {value!r}")
        if next_route.get("owner_decision_required_before_promotion_or_implementation") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T384 requires later owner decision")
        if next_route.get("next_owner_packet_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T384 next_owner_packet_required must be true")
        if next_route.get("exact_target_selected") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T384 exact_target_selected must be false")
        prior_entries = set(_require_string_list(next_route.get("prior_decision_register_entries"), "T384 prior_decision_register_entries"))
        if {"CD-056", "CD-057", "CD-060", "CD-061"} - prior_entries:
            raise ReadinessMapError(f"{_rel(path)}: T384 prior_decision_register_entries missing required ids")
        option_ids = {
            item.get("option_id")
            for item in next_route.get("available_target_options", [])
            if isinstance(item, dict)
        }
        if {"T384-A", "T384-B", "T384-C", "T384-D", "T384-E", "T384-F"} - option_ids:
            raise ReadinessMapError(f"{_rel(path)}: T384 available target options incomplete")
        _require_string_list(next_route.get("required_t384_work_must_record"), "T384 required_t384_work_must_record")
        for required in (
            "human_decision_map",
            "blocked_authority_changes",
            "exact_next_non_output_step",
        ):
            if required not in next_route["required_t384_work_must_record"]:
                raise ReadinessMapError(f"{_rel(path)}: T384 required_t384_work_must_record missing {required}")
        must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T384 must_fail_if"))
        for required in (
            "T384_synthesis_is_treated_as_owner_selection",
            "research_recommendation_is_treated_as_owner_selection",
            "whole_bible_output_is_run",
        ):
            if required not in must_fail:
                raise ReadinessMapError(f"{_rel(path)}: T384 must_fail_if missing {required}")
    if task_id == "T352":
        if next_route.get("review_packet_lane") != "epistle_argument":
            raise ReadinessMapError(f"{_rel(path)}: T352 next_route.review_packet_lane must be epistle_argument")
        if next_route.get("packet_status") != "pending_human_review":
            raise ReadinessMapError(f"{_rel(path)}: T352 next_route.packet_status must be pending_human_review")
        if next_route.get("prior_triage_task") != "T351":
            raise ReadinessMapError(f"{_rel(path)}: T352 next_route.prior_triage_task must be T351")
    if task_id == "T354":
        if next_route.get("review_packet_lane") != "gospel_discourse_wj":
            raise ReadinessMapError(f"{_rel(path)}: T354 next_route.review_packet_lane must be gospel_discourse_wj")
        if next_route.get("prior_inventory_task") != "T353":
            raise ReadinessMapError(f"{_rel(path)}: T354 next_route.prior_inventory_task must be T353")
        if next_route.get("inventory_status") != "generated_non_authorizing":
            raise ReadinessMapError(f"{_rel(path)}: T354 next_route.inventory_status must be generated_non_authorizing")
    if task_id == "T355":
        if next_route.get("review_packet_lane") != "gospel_discourse_wj":
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.review_packet_lane must be gospel_discourse_wj")
        if next_route.get("prior_inventory_task") != "T354":
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.prior_inventory_task must be T354")
        if next_route.get("selected_target") != "john3_wj_speaker_boundary":
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.selected_target must be john3_wj_speaker_boundary")
        if next_route.get("selected_target_status") != "selected_for_next_owner_review":
            raise ReadinessMapError(
                f"{_rel(path)}: T355 next_route.selected_target_status must be selected_for_next_owner_review"
            )
        if next_route.get("policy") != ".ai/control/wj_speaker_discourse_policy.yaml":
            raise ReadinessMapError(
                f"{_rel(path)}: T355 next_route.policy must be .ai/control/wj_speaker_discourse_policy.yaml"
            )
        if next_route.get("reviewed_gold_promoted") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T355 next_route.reviewed_gold_promoted must be false")
    if task_id == "T356":
        if next_route.get("review_packet_lane") != "gospel_discourse_wj":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.review_packet_lane must be gospel_discourse_wj")
        if next_route.get("prior_policy_task") != "T355":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.prior_policy_task must be T355")
        if next_route.get("selected_target") != "john3_wj_speaker_boundary":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.selected_target must be john3_wj_speaker_boundary")
        if next_route.get("john3_owner_selection_status") != "pending":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.john3_owner_selection_status must be pending")
        if next_route.get("john3_selected_option") != "pending":
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.john3_selected_option must be pending")
        if next_route.get("docket") != ".ai/control/john3_wj_owner_review_docket.yaml":
            raise ReadinessMapError(
                f"{_rel(path)}: T356 next_route.docket must be .ai/control/john3_wj_owner_review_docket.yaml"
            )
        if next_route.get("reviewed_gold_promoted") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T356 next_route.reviewed_gold_promoted must be false")
    if task_id == "T368":
        expected_t368 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "packet_status": "pending_human_review",
            "prior_owner_decision_task": "T367",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
            "john3_owner_selection_status": "selected",
            "john3_selected_option": "JOHN3-T356-B",
            "john3_selected_parent": "John.3.1-John.3.36",
        }
        for key, value in expected_t368.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T368 next_route.{key} must be {value}")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T368 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T368 next_route.{key} must be false")
    if task_id == "T369":
        expected_t369 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "pending_human_review",
            "owner_selection_status": "pending_owner_decision",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
            "textual_critical_policy_owner_options": ".ai/control/textual_critical_policy_owner_options.yaml",
            "textual_critical_case_policy": ".ai/control/textual_critical_case_policy.yaml",
        }
        for key, value in expected_t369.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T369 next_route.{key} must be {value}")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T369 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T369 next_route.{key} must be false")
    if task_id == "T370":
        expected_t370 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_evidence_prep_allowed",
            "owner_selection_status": "selected",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t370.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T370 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T370 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T369_parent_only_projected_selection":
            raise ReadinessMapError(f"{_rel(path)}: T370 next_route.starts_only_if is stale")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T370 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T370 next_route.{key} must be false")
    if task_id == "T371":
        expected_t371 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_evidence_packet_ready_for_owner_review",
            "owner_selection_status": "selected",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "evidence_prep_task": "T370",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t371.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T371 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T370_builds_governed_evidence_and_T379_selects_case_policy":
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.starts_only_if is stale")
        if next_route.get("owner_decision_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.owner_decision_required must be true")
        if next_route.get("variant_sensitive_policy_gate_task") != "T379":
            raise ReadinessMapError(f"{_rel(path)}: T371 variant_sensitive_policy_gate_task must be T379")
        if next_route.get("variant_sensitive_policy_selected") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 variant_sensitive_policy_selected must be true")
        if next_route.get("selected_textual_critical_policy") != "TCP-T378-B":
            raise ReadinessMapError(f"{_rel(path)}: T371 selected_textual_critical_policy must be TCP-T378-B")
        if next_route.get("t371_promotion_blocked_until_textual_policy") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T371 textual-policy blocker must be resolved")
        if next_route.get("variant_dependency_owner_decision_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 variant dependency owner decision must be required")
        if next_route.get("review_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T371 next_route.review_only must be true")
        for key in (
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T371 next_route.{key} must be false")
    if task_id == "T372":
        expected_t372 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "promotion_record": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
            "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_reviewed_gold_promoted",
            "owner_selection_status": "selected",
            "selected_t371_option": "T371-A",
            "parent_gold_promotion_task": "T371",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "evidence_prep_task": "T370",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t372.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T372 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T372 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T371_A_parent_only_reviewed_gold_promoted":
            raise ReadinessMapError(f"{_rel(path)}: T372 starts_only_if is stale")
        if next_route.get("reviewed_gold_promoted") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T372 reviewed_gold_promoted must be true")
        if next_route.get("variant_dependency_result") != "variant_non_dependent":
            raise ReadinessMapError(f"{_rel(path)}: T372 variant_dependency_result is stale")
        if next_route.get("variant_dependency_owner_decision_required") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T372 variant dependency owner decision must be resolved")
        if next_route.get("harness_only") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T372 next_route.harness_only must be true")
        if next_route.get("owner_implementation_authorization_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T372 implementation owner gate must be required")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T372 next_route.{key} must be false")
    if task_id == "T373":
        expected_t373 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "1COR8-10-T369-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "projected_owner_pattern",
            "projection_policy": ".ai/control/owner_decision_projection_policy.yaml",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "promotion_record": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
            "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
            "harness_plan": ".ai/control/t372_route_isolation_harness_plan.yaml",
            "harness_plan_status": "complete_non_output_changing_plan",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_reviewed_gold_promoted",
            "owner_selection_status": "selected",
            "selected_t371_option": "T371-A",
            "parent_gold_promotion_task": "T371",
            "prior_harness_task": "T372",
            "prior_owner_decision_task": "T367",
            "packet_strengthening_task": "T368",
            "parent_selection_task": "T369",
            "evidence_prep_task": "T370",
            "prior_packet_task": "T352",
            "prior_issue_dossier_task": "T361",
            "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
            "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
        }
        for key, value in expected_t373.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T373 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T373 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T372_route_isolation_harness_plan_complete":
            raise ReadinessMapError(f"{_rel(path)}: T373 starts_only_if is stale")
        if next_route.get("owner_decision_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T373 owner_decision_required must be true")
        if next_route.get("reviewed_gold_promoted") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T373 reviewed_gold_promoted must be true")
        if next_route.get("harness_only") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T373 next_route.harness_only must be false")
        if next_route.get("owner_implementation_authorization_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T373 implementation owner gate must be required")
        if next_route.get("next_task_if_authorized") != "T374":
            raise ReadinessMapError(f"{_rel(path)}: T373 next_task_if_authorized must be T374")
        required_owner = set(_require_string_list(
            next_route.get("required_owner_decision_must_record"),
            "T373 required_owner_decision_must_record",
        ))
        for item in (
            "exact_output_or_implementation_authorization_or_hold",
            "whether_parent_span_may_be_used_as_output_chunk_boundary",
            "whether_child_spans_remain_disallowed_or_are_separately_selected",
            "non_target_identity_proof_requirement",
            "same_baseline_evaluation_requirement",
            "decision_register_update_requirement",
        ):
            if item not in required_owner:
                raise ReadinessMapError(f"{_rel(path)}: T373 required owner decision missing {item}")
        if next_route.get("default_if_owner_unavailable") != "stop_before_implementation_or_output_change":
            raise ReadinessMapError(f"{_rel(path)}: T373 default_if_owner_unavailable must stop")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T373 next_route.{key} must be false")
    if task_id == "T374":
        expected_t374 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "T373-A",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "explicit_owner_authorization",
            "conflict_scan_result": "no_conflict_detected",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "promotion_record": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
            "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
            "harness_plan": ".ai/control/t372_route_isolation_harness_plan.yaml",
            "authorization_record": ".ai/control/t373_owner_implementation_authorization.yaml",
            "baseline_overlap_decision_packet": ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml",
            "baseline_overlap_status": "complete_owner_selected_additive_parent_overlay",
            "implementation_paused_until_owner_selects_baseline_overlap_option": False,
            "selected_baseline_overlap_option": "T374-OVERLAP-B",
            "additive_parent_overlay_selected": True,
            "preserve_existing_baseline_chunks_byte_identical": True,
            "delete_or_replace_existing_chunks_authorized": False,
            "duplicate_parent_coverage_allowed_for_exact_pilot": True,
            "adjacent_spill_splits_authorized": False,
            "replacement_style_implementation_paused": True,
            "replacement_safe_without_new_owner_decision": False,
            "additive_overlay_requires_owner_decision": True,
            "additive_overlay_owner_decision_recorded": True,
            "option_presentation_policy": ".ai/control/owner_decision_option_presentation_policy.yaml",
            "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
            "packet_status": "parent_only_reviewed_gold_promoted",
            "owner_selection_status": "selected",
            "selected_t371_option": "T371-A",
            "selected_t373_option": "T373-A",
            "implementation_authorization_task": "T373",
            "prior_harness_task": "T372",
            "variant_dependency_result": "variant_non_dependent",
            "general_parent_first_pilot_pattern": "parent_first_pilot_then_child_necessity_review",
            "post_pilot_child_necessity_review_required": True,
            "child_span_work_requires_later_owner_promotion": True,
        }
        for key, value in expected_t374.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T374 next_route.{key} must be {value}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T374 next_route.selected_children must be []")
        if next_route.get("starts_only_if") != "T373_A_authorizes_exact_parent_only_output_pilot":
            raise ReadinessMapError(f"{_rel(path)}: T374 starts_only_if is stale")
        if next_route.get("owner_decision_required") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T374 owner_decision_required must be false")
        if next_route.get("owner_implementation_authorization_recorded") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 owner implementation authorization must be recorded")
        if next_route.get("parent_span_as_chunk_boundary_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 parent span must be authorized")
        if next_route.get("parent_span_authorization_scope") != "exact_t374_pilot_only":
            raise ReadinessMapError(f"{_rel(path)}: T374 parent authorization scope must be exact")
        if next_route.get("route_behavior_authorized") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 route behavior must be authorized")
        if next_route.get("route_behavior_authorization_scope") != "exact_t374_target_only":
            raise ReadinessMapError(f"{_rel(path)}: T374 route scope must be exact")
        required_t374 = set(_require_string_list(
            next_route.get("required_t374_work_must_record"),
            "T374 required_t374_work_must_record",
        ))
        for item in (
            "parent_only_scope_proof",
            "selected_children_must_be_empty",
            "non_target_identity_proof",
            "same_baseline_evaluation",
            "changed_output_manifest",
            "decision_register_update",
            "validators_and_tests",
            "no_context_audit_surface",
            "post_pilot_child_necessity_review_gate",
        ):
            if item not in required_t374:
                raise ReadinessMapError(f"{_rel(path)}: T374 required work missing {item}")
        must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T374 must_fail_if"))
        for item in (
            "child_spans_are_added_without_later_owner_promotion",
            "child_spans_are_added_without_post_pilot_review",
            "route_behavior_applies_outside_1cor8_10",
            "graph_or_retrieval_truth_is_generated",
            "non_target_output_diff_is_detected",
        ):
            if item not in must_fail:
                raise ReadinessMapError(f"{_rel(path)}: T374 must_fail_if missing {item}")
        for key in ("evaluator_change_authorized", "graph_edge_generation_allowed", "retrieval_truth_authorized"):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T374 next_route.{key} must be false")
    if task_id == "T375":
        expected_t375 = {
            "recommended_target": "epistle_argument",
            "selected_target": "1cor8_10_food_offered_to_idols",
            "selected_passage": "1Cor.8-1Cor.10",
            "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
            "selected_option": "T374-OVERLAP-B",
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "selection_mode": "post_pilot_review_required",
            "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
            "owner_decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
            "promotion_record": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
            "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
            "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
            "harness_plan": ".ai/control/t372_route_isolation_harness_plan.yaml",
            "authorization_record": ".ai/control/t373_owner_implementation_authorization.yaml",
            "baseline_overlap_decision_packet": ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml",
            "implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "no_context_audit_surface": ".ai/audits/reports/20260620-T374-additive-parent-overlay.md",
            "decision_register_entry": "CD-056",
            "baseline_overlap_status": "complete_owner_selected_additive_parent_overlay",
            "selected_baseline_overlap_option": "T374-OVERLAP-B",
            "selected_t371_option": "T371-A",
            "selected_t373_option": "T373-A",
            "selected_t374_option": "T374-OVERLAP-B",
            "implementation_task": "T374",
            "next_task_after_t375": "T376",
            "route_behavior_authorization_scope": "none_review_only",
        }
        for key, value in expected_t375.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T375 next_route.{key} must be {value!r}")
        if next_route.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T375 next_route.selected_children must be []")
        for key in (
            "additive_parent_overlay_implemented",
            "preserve_existing_baseline_chunks_byte_identical",
            "baseline_prefix_matches_pre_t374_bytes",
            "reviewed_gold_promoted",
            "post_pilot_child_necessity_review_required",
            "child_span_work_requires_later_owner_promotion",
        ):
            if next_route.get(key) is not True:
                raise ReadinessMapError(f"{_rel(path)}: T375 next_route.{key} must be true")
        for key, value in (
            ("baseline_chunk_count", 1136),
            ("candidate_chunk_count", 1137),
            ("added_overlay_count", 1),
        ):
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T375 next_route.{key} must be {value}")
        required_t375 = set(_require_string_list(
            next_route.get("required_t375_work_must_record"),
            "T375 required_t375_work_must_record",
        ))
        for item in (
            "same_baseline_evaluation_review",
            "no_context_audit_review",
            "child_necessity_review",
            "selected_children_must_remain_empty_unless_later_owner_promotion",
            "decision_register_update_or_no_impact_marker",
            "validators_and_tests",
            "handoff_next_route_recommendation",
        ):
            if item not in required_t375:
                raise ReadinessMapError(f"{_rel(path)}: T375 required work missing {item}")
        must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T375 must_fail_if"))
        for item in (
            "child_spans_are_added_without_later_owner_promotion",
            "child_spans_are_added_without_post_pilot_review",
            "t374_overlay_is_treated_as_truth_bearing_hierarchy",
            "post_pilot_review_claims_child_spans_are_authorized",
            "graph_or_retrieval_truth_is_generated",
        ):
            if item not in must_fail:
                raise ReadinessMapError(f"{_rel(path)}: T375 must_fail_if missing {item}")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "child_spans_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T375 next_route.{key} must be false")
    if task_id == "T376":
        expected_t376 = {
            "title": "Select Next Chunking Lane From Decision Forecast",
            "starts_only_if": "T375_post_pilot_review_complete",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "selection_mode": "owner_decision_required",
            "reason_owner_required": "T375 completed the review-only post-pilot gate. Selecting the next chunking lane or target could shift theological, genre, review-gold, or implementation priorities and must be chosen by the owner.",
        }
        for key, value in expected_t376.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T376 next_route.{key} must be {value!r}")
        if set(next_route.get("prior_decision_register_entries", [])) != {"CD-056", "CD-057"}:
            raise ReadinessMapError(f"{_rel(path)}: T376 prior decision register entries are stale")
        if next_route.get("owner_decision_required") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T376 must require owner decision")
        options = next_route.get("available_lane_options")
        if not isinstance(options, list) or len(options) < 4:
            raise ReadinessMapError(f"{_rel(path)}: T376 must present lane options")
        option_ids = {option.get("option_id") for option in options if isinstance(option, dict)}
        if {"T376-A", "T376-B", "T376-C", "T376-D"} - option_ids:
            raise ReadinessMapError(f"{_rel(path)}: T376 lane options are incomplete")
        result = next_route.get("t375_result")
        if not isinstance(result, dict):
            raise ReadinessMapError(f"{_rel(path)}: T376 t375_result must be present")
        expected_result = {
            "selected_parent": "1Cor.8.1-1Cor.10.33",
            "same_baseline_reviewed": True,
            "no_context_audit_reviewed": True,
            "child_necessity_reviewed": True,
            "child_span_result": "child_spans_not_necessary_now",
            "child_spans_authorized": False,
            "output_change_authorized": False,
            "implementation_authorized": False,
        }
        for key, value in expected_result.items():
            if result.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T376 t375_result.{key} must be {value!r}")
        if result.get("selected_children") != []:
            raise ReadinessMapError(f"{_rel(path)}: T376 t375_result.selected_children must be []")
        must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T376 must_fail_if"))
        for item in (
            "T376_selects_lane_without_owner_decision",
            "child_spans_are_added_without_later_owner_promotion",
            "reviewed_gold_is_promoted_without_owner_gate",
            "graph_or_retrieval_truth_is_generated",
            "route_behavior_changes_without_exact_authorization",
            "whole_bible_output_is_run",
        ):
            if item not in must_fail:
                raise ReadinessMapError(f"{_rel(path)}: T376 must_fail_if missing {item}")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "child_spans_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T376 next_route.{key} must be false")
    if task_id == "T384":
        expected_t384 = {
            "title": "Bible-Wide Research Readiness Synthesis",
            "starts_only_if": "T376_A_epistle_argument_research_runway_selected",
            "prior_lane_selection": ".ai/control/t376_epistle_research_runway.yaml",
            "prior_post_pilot_review": ".ai/control/t375_post_pilot_review.yaml",
            "prior_implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
            "completion_surface": ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml",
            "completion_status": "complete_bible_wide_research_readiness_synthesis",
            "decision_register_entry": "CD-061",
            "lesson_index_entry": "LSN-013",
            "selected_t376_option": "T376-A",
            "selected_lane": "epistle_argument",
            "selection_mode": "bible_wide_research_readiness_complete_non_authorizing",
            "owner_decision_required_before_promotion_or_implementation": True,
            "exact_target_selected": False,
            "exact_next_non_output_step": "T385",
            "next_owner_packet_required": True,
            "lesson": "research_autonomy_is_not_authority_autonomy",
        }
        for key, value in expected_t384.items():
            if next_route.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: T384 next_route.{key} must be {value!r}")
        if set(next_route.get("prior_decision_register_entries", [])) != {"CD-056", "CD-057", "CD-060", "CD-061", "CD-062"}:
            raise ReadinessMapError(f"{_rel(path)}: T384 prior decision register entries are stale")
        options = next_route.get("available_target_options")
        if not isinstance(options, list) or len(options) < 6:
            raise ReadinessMapError(f"{_rel(path)}: T384 must present target options")
        option_ids = {option.get("option_id") for option in options if isinstance(option, dict)}
        if {"T384-A", "T384-B", "T384-C", "T384-D", "T384-E", "T384-F"} - option_ids:
            raise ReadinessMapError(f"{_rel(path)}: T384 target options are incomplete")
        required_work = set(_require_string_list(next_route.get("required_t384_work_must_record"), "T384 required_t384_work_must_record"))
        for item in (
            "serious_faithful_target_options",
            "repercussions_for_each_option",
            "contextual_reading_policy_fields",
            "source_metadata_evidence_only_handling",
            "original_language_phrase_context_review_where_used",
            "orthodox_hermeneutic_firewall_compliance",
            "no_exact_target_selected",
            "human_decision_map",
            "blocked_authority_changes",
            "exact_next_non_output_step",
            "audit_surface",
            "handoff_next_owner_gate",
        ):
            if item not in required_work:
                raise ReadinessMapError(f"{_rel(path)}: T384 required work missing {item}")
        must_fail = set(_require_string_list(next_route.get("must_fail_if"), "T384 must_fail_if"))
        for item in (
            "T384_selects_exact_target_without_owner_decision",
            "T384_synthesis_is_treated_as_owner_selection",
            "research_recommendation_is_treated_as_owner_selection",
            "reviewed_gold_is_promoted_without_owner_gate",
            "graph_or_retrieval_truth_is_generated",
            "whole_bible_output_is_run",
            "denominational_systematic_theology_becomes_chunk_authority",
        ):
            if item not in must_fail:
                raise ReadinessMapError(f"{_rel(path)}: T384 must_fail_if missing {item}")
        for key in (
            "output_change_authorized",
            "implementation_authorized",
            "reviewed_gold_promoted",
            "route_behavior_authorized",
            "child_spans_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
            "embedding_or_vector_work_allowed",
        ):
            if next_route.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: T384 next_route.{key} must be false")

    t398_synthesis = data.get("parallel_t398_phase_one_research_synthesis")
    if not isinstance(t398_synthesis, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t398_phase_one_research_synthesis must be a mapping")
    expected_t398 = {
        "task_id": "T398",
        "route_type": "whole_corpus_phase_one_research_synthesis",
        "path": ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml",
        "roadmap_doc": "docs/roadmap/T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md",
        "status": "complete_phase_one_whole_corpus_research_synthesis",
        "relation_to_next_route": "Parallel phase-one research synthesis; does not supersede the T401 output pilot/post-pilot review gate or authorize output.",
        "corpus_scope": "canonical_66",
        "canonical_book_count": 66,
        "canonical_passage_count": 31103,
        "every_canonical_passage_accounted_for_at_triage_depth": True,
        "every_verse_deeply_researched": False,
        "decision_register_entry": "CD-072",
        "lesson_index_entry": "LSN-026",
    }
    for key, value in expected_t398.items():
        if t398_synthesis.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t398_phase_one_research_synthesis.{key} must be {value!r}")
    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "exact_target_selected",
        "reviewed_gold_promoted",
        "child_spans_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "whole_bible_output_authorized",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "source_or_manuscript_rows_authorized",
        "theology_authority_change_authorized",
    ):
        if t398_synthesis.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t398_phase_one_research_synthesis.{key} must be false")

    t399_queue = data.get("parallel_t399_focused_research_queue")
    if not isinstance(t399_queue, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t399_focused_research_queue must be a mapping")
    expected_t399 = {
        "task_id": "T399",
        "route_type": "goal2_focused_research_queue",
        "path": ".ai/control/t399_focused_bible_wide_research_queue.yaml",
        "roadmap_doc": "docs/roadmap/T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md",
        "status": "complete_goal2_focused_research_queue",
        "relation_to_next_route": "Parallel focused research queue; does not supersede the T401 output pilot/post-pilot review gate or authorize output.",
        "corpus_scope": "canonical_66",
        "candidate_count": 22,
        "owner_decision_prompt_count": 8,
        "recommendation_is_owner_selection": False,
        "decision_register_entry": "CD-073",
        "lesson_index_entry": "LSN-027",
        "next_owner_action": "choose_one_T399_HDM_option_before_new_review_packet_strengthening",
        "next_chunking_route_remains": "T401_post_pilot_review_gate_after_exact_output_pilot",
    }
    for key, value in expected_t399.items():
        if t399_queue.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t399_focused_research_queue.{key} must be {value!r}")
    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "exact_target_selected",
        "reviewed_gold_promoted",
        "child_spans_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "whole_bible_output_authorized",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "source_or_manuscript_rows_authorized",
        "theology_authority_change_authorized",
    ):
        if t399_queue.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t399_focused_research_queue.{key} must be false")

    t402_runway = data.get("parallel_t402_low_complexity_runway")
    if not isinstance(t402_runway, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t402_low_complexity_runway must be a mapping")
    expected_t402 = {
        "task_id": "T402",
        "route_type": "whole_bible_low_complexity_candidate_runway",
        "post_pilot_review": ".ai/control/t402_eph1_post_pilot_review.yaml",
        "path": ".ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml",
        "roadmap_doc": "docs/roadmap/T402_LOW_COMPLEXITY_CHUNKING_RUNWAY.md",
        "status": "complete_review_research_only_candidate_runway",
        "relation_to_next_route": "Parallel post-pilot and whole-Bible review runway; does not supersede the T401 output-pilot evidence, select a next target, promote reviewed gold, or authorize output.",
        "corpus_scope": "canonical_66",
        "canonical_book_count": 66,
        "candidate_count": 66,
        "ready_for_review_packet": 38,
        "needs_context_research": 16,
        "needs_original_language_review": 2,
        "variant_sensitive_hold": 2,
        "theological_risk_hold": 6,
        "owner_decision_required": 1,
        "do_not_chunk_now": 1,
        "decision_register_entry": "CD-077",
        "lesson_index_entry": "LSN-031",
        "low_complexity_means_review_eligibility_only": True,
        "next_owner_action": "choose_one_T402_ready_candidate_before_review_packet_strengthening",
        "next_chunking_route_remains": "owner_selected_single_candidate_review_packet_only",
    }
    for key, value in expected_t402.items():
        if t402_runway.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t402_low_complexity_runway.{key} must be {value!r}")
    for key in (
        "exact_target_selected",
        "review_packet_strengthening_authorized_without_owner_selection",
        "reviewed_gold_promoted",
        "output_change_authorized",
        "implementation_authorized",
        "child_spans_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "whole_bible_output_pass_authorized",
        "preferred_reading_or_source_tradition_authorized",
        "canon_scope_change_authorized",
        "source_or_manuscript_rows_authorized",
        "theology_authority_change_authorized",
    ):
        if t402_runway.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t402_low_complexity_runway.{key} must be false")

    parallel_research = data.get("parallel_research_queue")
    if isinstance(parallel_research, dict):
        expected_parallel = {
            "task_id": "T358",
            "route_type": "whole_bible_research_registry",
            "path": ".ai/control/bible_wide_chunking_research_registry.yaml",
            "status": "complete_non_authorizing",
            "corpus_scope": "canonical_66",
            "book_count": 66,
        }
        for key, value in expected_parallel.items():
            if parallel_research.get(key) != value:
                raise ReadinessMapError(f"{_rel(path)}: parallel_research_queue.{key} must be {value}")
        for key in ("output_change_authorized", "implementation_authorized", "reviewed_gold_promoted"):
            if parallel_research.get(key) is not False:
                raise ReadinessMapError(f"{_rel(path)}: parallel_research_queue.{key} must be false")

    options = data.get("parallel_textual_critical_policy_options")
    if not isinstance(options, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_policy_options must be a mapping")
    if options.get("task_id") != "T378":
        raise ReadinessMapError(f"{_rel(path)}: textual-critical options task_id must be T378")
    if options.get("textual_critical_policy_selected") is not True:
        raise ReadinessMapError(f"{_rel(path)}: textual-critical options must record selected policy")
    if options.get("selected_policy") != "TCP-T378-B":
        raise ReadinessMapError(f"{_rel(path)}: textual-critical selected_policy must be TCP-T378-B")
    if options.get("selection_record") != ".ai/control/textual_critical_case_policy.yaml":
        raise ReadinessMapError(f"{_rel(path)}: textual-critical selection_record is stale")

    case_policy = data.get("parallel_textual_critical_case_policy")
    if not isinstance(case_policy, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_case_policy must be a mapping")
    expected_case = {
        "task_id": "T379",
        "path": ".ai/control/textual_critical_case_policy.yaml",
        "selected_policy": "TCP-T378-B",
        "projectable_pattern": "ODP-005",
    }
    for key, value in expected_case.items():
        if case_policy.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_case_policy.{key} must be {value}")
    if case_policy.get("variant_dependency_owner_decision_required") is not True:
        raise ReadinessMapError(f"{_rel(path)}: variant dependency owner decision must be required")
    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "reviewed_gold_promoted",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if case_policy.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_textual_critical_case_policy.{key} must be false")

    t371_packet = data.get("parallel_t371_owner_decision_packet")
    if not isinstance(t371_packet, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet must be a mapping")
    expected_t371_packet = {
        "task_id": "T380",
        "path": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
        "target_owner_task": "T371",
        "recommended_if_owner_agrees_with_variant_non_dependency": "T371-A",
        "conservative_hold_if_any_doubt": "T371-B",
    }
    for key, value in expected_t371_packet.items():
        if t371_packet.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet.{key} must be {value}")
    if set(t371_packet.get("exact_variant_refs", [])) != {"1Cor.9.20", "1Cor.10.9"}:
        raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet refs are stale")
    if t371_packet.get("owner_decision_required") is not False:
        raise ReadinessMapError(f"{_rel(path)}: T371 packet owner_decision_required must be false after T371-A")
    if t371_packet.get("owner_response_record") != ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml":
        raise ReadinessMapError(f"{_rel(path)}: T371 packet owner_response_record is stale")
    if t371_packet.get("selected_option") != "T371-A":
        raise ReadinessMapError(f"{_rel(path)}: T371 packet selected_option must be T371-A")
    for key in (
        "variant_dependency_finding_authorized",
        "variant_non_dependency_finding_authorized",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "reviewed_gold_promoted",
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if t371_packet.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_owner_decision_packet.{key} must be false")

    promotion = data.get("parallel_t371_parent_only_promotion_record")
    if not isinstance(promotion, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t371_parent_only_promotion_record must be a mapping")
    expected_promotion = {
        "task_id": "T371",
        "path": ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "status": "complete_parent_only_reviewed_gold_promoted",
        "selected_option": "T371-A",
        "boundary_dependency_or_non_dependency": "variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency": "variant_non_dependent",
    }
    for key, value in expected_promotion.items():
        if promotion.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_parent_only_promotion_record.{key} must be {value}")
    if set(promotion.get("exact_variant_refs", [])) != {"1Cor.9.20", "1Cor.10.9"}:
        raise ReadinessMapError(f"{_rel(path)}: T371 promotion refs are stale")
    if promotion.get("reviewed_gold_promoted") is not True:
        raise ReadinessMapError(f"{_rel(path)}: T371 promotion must record reviewed_gold_promoted true")
    for key in (
        "parent_span_as_chunk_boundary_authorized",
        "child_spans_authorized",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if promotion.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t371_parent_only_promotion_record.{key} must be false")

    t372_plan = data.get("parallel_t372_route_isolation_harness_plan")
    if not isinstance(t372_plan, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t372_route_isolation_harness_plan must be a mapping")
    expected_t372_plan = {
        "task_id": "T372",
        "path": ".ai/control/t372_route_isolation_harness_plan.yaml",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "status": "complete_non_output_changing_plan",
        "next_owner_gate": "T373",
    }
    for key, value in expected_t372_plan.items():
        if t372_plan.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t372_route_isolation_harness_plan.{key} must be {value}")
    if t372_plan.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise ReadinessMapError(f"{_rel(path)}: T372 plan selected_parent is stale")
    if t372_plan.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T372 plan selected_children must be []")
    if t372_plan.get("owner_implementation_authorization_required") is not True:
        raise ReadinessMapError(f"{_rel(path)}: T372 plan must require T373 owner authorization")
    for key in (
        "parent_span_as_chunk_boundary_authorized",
        "child_spans_authorized",
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if t372_plan.get(key) is not False:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t372_route_isolation_harness_plan.{key} must be false")

    t373_auth = data.get("parallel_t373_owner_implementation_authorization")
    if not isinstance(t373_auth, dict):
        raise ReadinessMapError(f"{_rel(path)}: parallel_t373_owner_implementation_authorization must be a mapping")
    expected_t373_auth = {
        "task_id": "T373",
        "path": ".ai/control/t373_owner_implementation_authorization.yaml",
        "option_presentation_policy": ".ai/control/owner_decision_option_presentation_policy.yaml",
        "status": "complete_owner_authorized_exact_parent_only_pilot",
        "selected_option": "T373-A",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "general_parent_first_pilot_pattern": "parent_first_pilot_then_child_necessity_review",
        "post_pilot_child_necessity_review_required": True,
        "child_span_work_requires_later_owner_promotion": True,
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "parent_span_as_chunk_boundary_authorized": True,
        "child_spans_authorized": False,
        "output_change_authorized": True,
        "implementation_authorized": True,
        "route_behavior_authorized": True,
        "evaluator_change_authorized": False,
        "graph_edge_generation_allowed": False,
        "retrieval_truth_authorized": False,
    }
    for key, value in expected_t373_auth.items():
        if t373_auth.get(key) != value:
            raise ReadinessMapError(f"{_rel(path)}: parallel_t373_owner_implementation_authorization.{key} must be {value!r}")
    if t373_auth.get("selected_children") != []:
        raise ReadinessMapError(f"{_rel(path)}: T373 parallel selected_children must be []")

    if data["next_route"].get("task_id") == "T374":
        if data["next_route"].get("baseline_overlap_decision_packet") != ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml":
            raise ReadinessMapError(f"{_rel(path)}: T374 baseline_overlap_decision_packet is stale")
        if data["next_route"].get("implementation_paused_until_owner_selects_baseline_overlap_option") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T374 owner-selection pause must be resolved")
        if data["next_route"].get("selected_baseline_overlap_option") != "T374-OVERLAP-B":
            raise ReadinessMapError(f"{_rel(path)}: T374 selected_baseline_overlap_option must be T374-OVERLAP-B")
        if data["next_route"].get("preserve_existing_baseline_chunks_byte_identical") is not True:
            raise ReadinessMapError(f"{_rel(path)}: T374 must preserve existing baseline chunks byte-identical")
        if data["next_route"].get("delete_or_replace_existing_chunks_authorized") is not False:
            raise ReadinessMapError(f"{_rel(path)}: T374 must not authorize deletion or replacement")

    non_authorizations = set(
        _require_string_list(data["explicit_non_authorizations"], "explicit_non_authorizations")
    )
    missing_non_authorizations = sorted(REQUIRED_NON_AUTHORIZATIONS - non_authorizations)
    if missing_non_authorizations:
        raise ReadinessMapError(
            f"{_rel(path)}: explicit_non_authorizations missing {missing_non_authorizations}"
        )

    return data


def main() -> int:
    try:
        validate_readiness_map()
    except ReadinessMapError as exc:
        print(f"Bible chunking readiness map validation failed: {exc}", file=sys.stderr)
        return 1
    print("Bible chunking readiness map validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
