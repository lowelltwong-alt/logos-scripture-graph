from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_bible_chunking_readiness_map as validator


ROOT = Path(__file__).resolve().parents[1]
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"


def test_readiness_map_validates_and_is_non_authorizing() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    assert data["object_type"] == "bible_chunking_readiness_map"
    assert data["trust_zone"] == "canonical"
    assert data["authority"]["records_readiness"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_new_algorithm_work"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_skill_lifecycle_promotion"] is False
    assert data["authority"]["authorizes_boundary_import"] is False


def test_faithful_route_is_one_lane_at_a_time() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    assert data["faithful_execution_model"]["route"] == "one_lane_at_a_time_under_bible_wide_map"
    assert data["current_baseline"]["corpus_scope"] == "canonical_66"
    assert data["current_baseline"]["improvement_claim_allowed"] is False


def test_required_lanes_are_present_and_block_new_algorithm_work() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    by_lane = {lane["lane_id"]: lane for lane in data["lane_sequence"]}

    assert set(by_lane) >= validator.REQUIRED_LANES
    assert by_lane["revelation_apocalyptic"]["review_order"] == 1
    assert by_lane["bible_wide_orchestration"]["implementation_order"] == 9
    assert by_lane["epistle_argument"]["new_algorithm_work_ready"] is False
    assert by_lane["epistle_argument"]["current_state"] == "t376_a_epistle_research_runway_selected_next_t384_options_matrix"
    assert all(
        lane["new_algorithm_work_ready"] is False
        for lane in by_lane.values()
    )


def test_lessons_are_stored_in_first_class_surfaces() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    surfaces = set(data["lessons_storage"]["surfaces"])
    assert validator.REQUIRED_LESSON_SURFACES <= surfaces
    assert ".ai/control/chunking_lesson_index.yaml" in surfaces
    assert ".ai/control/chunking_theological_decision_register.yaml" in surfaces
    assert ".ai/control/john3_wj_owner_review_docket.yaml" in surfaces
    assert ".ai/control/bible_wide_chunking_research_registry.yaml" in surfaces
    assert ".ai/control/source_metadata_research_atlas.yaml" in surfaces
    assert ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml" in surfaces
    assert ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml" in surfaces
    assert ".ai/control/gospel_wj_discourse_dossier_queue.yaml" in surfaces
    assert ".ai/control/narrative_legal_covenant_dossier_queue.yaml" in surfaces
    assert ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml" in surfaces
    assert ".ai/control/prophetic_oracle_vision_dossier_queue.yaml" in surfaces
    assert ".ai/control/textual_variant_source_tradition_dossier_queue.yaml" in surfaces
    assert ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml" in surfaces
    assert ".ai/control/contextual_reading_policy.yaml" in surfaces
    assert ".ai/control/orthodox_hermeneutic_firewall_docket.yaml" in surfaces
    assert ".ai/control/textual_critical_policy_docket.yaml" in surfaces
    assert ".ai/control/textual_critical_policy_owner_options.yaml" in surfaces
    assert ".ai/control/textual_critical_case_policy.yaml" in surfaces
    assert ".ai/control/t371_variant_dependency_owner_decision_packet.yaml" in surfaces
    assert ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml" in surfaces
    assert ".ai/control/t372_route_isolation_harness_plan.yaml" in surfaces
    assert ".ai/control/t373_owner_implementation_authorization.yaml" in surfaces
    assert ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml" in surfaces
    assert ".ai/control/t374_additive_parent_overlay_manifest.yaml" in surfaces
    assert ".ai/control/t375_post_pilot_review.yaml" in surfaces
    assert ".ai/control/t376_epistle_research_runway.yaml" in surfaces
    assert ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml" in surfaces
    assert ".ai/control/t385_owner_decision_packet.yaml" in surfaces
    assert ".ai/control/owner_decision_option_presentation_policy.yaml" in surfaces
    assert "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json" in surfaces
    assert ".ai/control/1cor8_10_epistle_owner_review_docket.yaml" in surfaces
    assert ".ai/control/chunking_human_decision_forecast.yaml" in surfaces
    assert ".ai/control/governance_memory_durability_policy.yaml" in surfaces
    assert ".ai/control/owner_decision_projection_policy.yaml" in surfaces


def test_prophetic_oracle_lane_records_t365_without_algorithm_authority() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    by_lane = {lane["lane_id"]: lane for lane in data["lane_sequence"]}
    prophetic = by_lane["prophetic_oracle"]

    assert prophetic["current_state"] == "t365_research_dossier_queue_seeded_needs_review_packets"
    assert prophetic["new_algorithm_work_ready"] is False
    assert prophetic["dossier_queue"]["task_id"] == "T365"
    assert prophetic["dossier_queue"]["path"] == ".ai/control/prophetic_oracle_vision_dossier_queue.yaml"
    assert prophetic["dossier_queue"]["output_change_authorized"] is False
    assert prophetic["dossier_queue"]["implementation_authorized"] is False
    assert prophetic["dossier_queue"]["reviewed_gold_promoted"] is False


def test_textual_variant_source_tradition_lane_records_t366_without_algorithm_authority() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    by_lane = {lane["lane_id"]: lane for lane in data["lane_sequence"]}
    textual = by_lane["textual_variant_source_tradition"]

    assert textual["current_state"] == "t366_research_dossier_queue_seeded_needs_policy_or_review_packets"
    assert textual["new_algorithm_work_ready"] is False
    assert textual["dossier_queue"]["task_id"] == "T366"
    assert textual["dossier_queue"]["path"] == ".ai/control/textual_variant_source_tradition_dossier_queue.yaml"
    assert textual["dossier_queue"]["output_change_authorized"] is False
    assert textual["dossier_queue"]["implementation_authorized"] is False
    assert textual["dossier_queue"]["reviewed_gold_promoted"] is False
    assert "Mark.16.9-Mark.16.20" in textual["candidate_cases"]
    assert "1John.5.6-1John.5.8" in textual["candidate_cases"]


def test_parallel_research_queue_records_t358_without_replacing_next_route() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    queue = data["parallel_research_queue"]

    assert data["next_route"]["task_id"] == "T385"
    assert queue["task_id"] == "T358"
    assert queue["route_type"] == "whole_bible_research_registry"
    assert queue["path"] == ".ai/control/bible_wide_chunking_research_registry.yaml"
    assert queue["corpus_scope"] == "canonical_66"
    assert queue["book_count"] == 66
    assert queue["output_change_authorized"] is False
    assert queue["implementation_authorized"] is False
    assert queue["reviewed_gold_promoted"] is False


def test_parallel_original_language_pressure_queue_does_not_replace_next_route() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    queue = data["parallel_original_language_pressure_queue"]

    assert data["next_route"]["task_id"] == "T385"
    assert queue["task_id"] == "T377"
    assert queue["route_type"] == "cross_lane_original_language_pressure_memory"
    assert queue["path"] == ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml"
    assert queue["output_change_authorized"] is False
    assert queue["implementation_authorized"] is False
    assert queue["reviewed_gold_promoted"] is False
    assert queue["source_language_authority_allowed"] is False
    assert queue["translation_preference_authorized"] is False
    assert queue["nonorthodox_source_authority_allowed"] is False
    assert queue["extra_canonical_source_authority_allowed"] is False
    assert queue["graph_edge_generation_allowed"] is False
    assert queue["retrieval_truth_authorized"] is False


def test_parallel_textual_critical_policy_options_block_t371_promotion() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    queue = data["parallel_textual_critical_policy_options"]

    assert data["next_route"]["task_id"] == "T385"
    assert queue["task_id"] == "T378"
    assert queue["path"] == ".ai/control/textual_critical_policy_owner_options.yaml"
    assert queue["recommended_option"] == "TCP-T378-B"
    assert queue["textual_critical_policy_selected"] is True
    assert queue["selected_policy"] == "TCP-T378-B"
    assert queue["selection_record"] == ".ai/control/textual_critical_case_policy.yaml"
    assert queue["preferred_reading_authorized"] is False
    assert queue["source_tradition_preference_authorized"] is False
    assert queue["reviewed_gold_promoted"] is False
    assert queue["graph_edge_generation_allowed"] is False
    assert queue["retrieval_truth_authorized"] is False


def test_parallel_textual_critical_case_policy_records_t379_without_promotion() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    policy = data["parallel_textual_critical_case_policy"]

    assert data["next_route"]["task_id"] == "T385"
    assert policy["task_id"] == "T379"
    assert policy["path"] == ".ai/control/textual_critical_case_policy.yaml"
    assert policy["selected_policy"] == "TCP-T378-B"
    assert policy["projectable_pattern"] == "ODP-005"
    assert policy["variant_dependency_owner_decision_required"] is True
    assert policy["preferred_reading_authorized"] is False
    assert policy["source_tradition_preference_authorized"] is False
    assert policy["reviewed_gold_promoted"] is False
    assert policy["graph_edge_generation_allowed"] is False
    assert policy["retrieval_truth_authorized"] is False


def test_parallel_t371_owner_decision_packet_does_not_promote_gold() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    packet = data["parallel_t371_owner_decision_packet"]

    assert data["next_route"]["task_id"] == "T385"
    assert data["next_route"]["owner_packet"] == ".ai/control/t385_owner_decision_packet.yaml"
    assert packet["task_id"] == "T380"
    assert packet["path"] == ".ai/control/t371_variant_dependency_owner_decision_packet.yaml"
    assert packet["target_owner_task"] == "T371"
    assert set(packet["exact_variant_refs"]) == {"1Cor.9.20", "1Cor.10.9"}
    assert packet["recommended_if_owner_agrees_with_variant_non_dependency"] == "T371-A"
    assert packet["conservative_hold_if_any_doubt"] == "T371-B"
    assert packet["owner_decision_required"] is False
    assert packet["owner_response_record"] == ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
    assert packet["selected_option"] == "T371-A"
    assert packet["variant_dependency_finding_authorized"] is False
    assert packet["variant_non_dependency_finding_authorized"] is False
    assert packet["preferred_reading_authorized"] is False
    assert packet["source_tradition_preference_authorized"] is False
    assert packet["reviewed_gold_promoted"] is False
    assert packet["output_change_authorized"] is False
    assert packet["implementation_authorized"] is False


def test_next_route_records_completed_t385_owner_packet_and_pending_owner_gate() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    assert data["next_route"]["task_id"] == "T385"
    assert data["next_route"]["route_type"] == "owner_decision_packet_only"
    assert data["next_route"]["starts_only_if"] == "T384_bible_wide_research_readiness_synthesis_complete_and_T386_coverage_complete"
    assert data["next_route"]["completion_status"] == "complete_owner_decision_packet_only"
    assert data["next_route"]["owner_packet"] == ".ai/control/t385_owner_decision_packet.yaml"
    assert data["next_route"]["roadmap_doc"] == "docs/roadmap/T385_OWNER_DECISION_PACKET.md"
    assert data["next_route"]["validator"] == "scripts/validate_t385_owner_decision_packet.py"
    assert data["next_route"]["required_handoff"] == ".ai/handoffs/T385/handoff.md"
    assert data["next_route"]["decision_register_entry"] == "CD-066"
    assert data["next_route"]["lesson_index_entry"] == "LSN-020"
    assert set(data["next_route"]["prior_decision_register_entries"]) == {
        "CD-061",
        "CD-062",
        "CD-063",
        "CD-064",
        "CD-065",
        "CD-066",
    }
    assert data["next_route"]["selected_t376_option"] == "T376-A"
    assert data["next_route"]["selected_lane"] == "epistle_argument"
    assert data["next_route"]["selection_mode"] == "owner_packet_complete_non_authorizing"
    assert data["next_route"]["owner_decision_required_before_goal_4"] is True
    assert data["next_route"]["owner_decision_required_before_promotion_or_implementation"] is True
    assert data["next_route"]["owner_selection_status"] == "pending"
    assert data["next_route"]["recommended_option"] == "T385-A"
    assert data["next_route"]["recommended_passage"] == "Eph.1.3-Eph.1.14"
    assert data["next_route"]["recommendation_is_owner_selection"] is False
    assert data["next_route"]["exact_target_selected"] is False
    assert data["next_route"]["goal_4_can_run_after"] == "explicit_owner_selection_of_one_T385_option"
    assert set(data["next_route"]["serious_faithful_options"]) == {
        "T385-A",
        "T385-B",
        "T385-C",
        "T385-D",
        "T385-E",
        "T385-F",
        "T385-G",
        "T385-H",
        "T385-I",
    }
    assert data["next_route"]["output_change_authorized"] is False
    assert data["next_route"]["implementation_authorized"] is False
    assert data["next_route"]["reviewed_gold_promoted"] is False
    assert data["next_route"]["review_packet_strengthening_authorized"] is False
    assert data["next_route"]["route_behavior_authorized"] is False
    assert data["next_route"]["child_spans_authorized"] is False
    assert data["next_route"]["evaluator_change_authorized"] is False
    assert data["next_route"]["graph_edge_generation_allowed"] is False
    assert data["next_route"]["embedding_or_vector_work_allowed"] is False
    assert data["next_route"]["preferred_reading_authorized"] is False
    assert data["next_route"]["source_tradition_preference_authorized"] is False
    assert data["next_route"]["theology_authority_change_authorized"] is False
    assert "T385_recommendation_is_treated_as_owner_selection" in data["next_route"]["must_fail_if"]
    assert "Goal4_runs_without_explicit_owner_selection" in data["next_route"]["must_fail_if"]
    assert "T385_strengthens_review_packet_without_owner_selection" in data["next_route"]["must_fail_if"]
    assert "recommendation_is_not_owner_selection" in data["next_route"]["required_t385_packet_records"]
    assert "handoff_next_owner_gate" in data["next_route"]["required_t385_packet_records"]

    by_lane = {lane["lane_id"]: lane for lane in data["lane_sequence"]}
    epistle = by_lane["epistle_argument"]
    assert epistle["parent_only_evidence_packet"]["task_id"] == "T370"
    assert epistle["parent_only_evidence_packet"]["status"] == "ready_for_owner_promotion_review"
    assert epistle["parent_only_evidence_packet"]["reviewed_gold_promoted"] is False
    promotion = epistle["parent_only_reviewed_gold_promotion"]
    assert promotion["task_id"] == "T371"
    assert promotion["selected_option"] == "T371-A"
    assert promotion["reviewed_gold_promoted"] is True
    assert promotion["selected_children"] == []
    assert promotion["parent_span_as_chunk_boundary_authorized"] is False
    implementation = epistle["additive_parent_overlay_implementation"]
    assert implementation["task_id"] == "T374"
    assert implementation["path"] == ".ai/control/t374_additive_parent_overlay_manifest.yaml"
    assert implementation["status"] == "complete_output_changed_additive_parent_overlay"
    assert implementation["selected_children"] == []
    assert implementation["baseline_prefix_matches_pre_t374_bytes"] is True
    assert implementation["non_target_output_diff_detected"] is False
    assert implementation["child_spans_authorized"] is False
    review = epistle["post_pilot_review"]
    assert review["task_id"] == "T375"
    assert review["path"] == ".ai/control/t375_post_pilot_review.yaml"
    assert review["status"] == "complete_review_only_child_spans_not_necessary_now"
    assert review["selected_children"] == []
    assert review["same_baseline_reviewed"] is True
    assert review["no_context_audit_reviewed"] is True
    assert review["child_necessity_reviewed"] is True
    assert review["child_spans_necessary_now"] is False
    assert review["next_route"] == "T376"
    runway = epistle["research_runway_selection"]
    assert runway["task_id"] == "T376"
    assert runway["path"] == ".ai/control/t376_epistle_research_runway.yaml"
    assert runway["selected_option"] == "T376-A"
    assert runway["exact_target_selected"] is False
    assert runway["next_route"] == "T384"
    assert runway["output_change_authorized"] is False
    assert runway["implementation_authorized"] is False
    assert runway["reviewed_gold_promoted"] is False
    assert runway["graph_edge_generation_allowed"] is False

    plan = data["parallel_t372_route_isolation_harness_plan"]
    assert plan["task_id"] == "T372"
    assert plan["path"] == ".ai/control/t372_route_isolation_harness_plan.yaml"
    assert plan["status"] == "complete_non_output_changing_plan"
    assert plan["next_owner_gate"] == "T373"
    assert plan["output_change_authorized"] is False
    assert plan["implementation_authorized"] is False

    auth = data["parallel_t373_owner_implementation_authorization"]
    assert auth["task_id"] == "T373"
    assert auth["path"] == ".ai/control/t373_owner_implementation_authorization.yaml"
    assert auth["selected_option"] == "T373-A"
    assert auth["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert auth["selected_children"] == []
    assert auth["general_parent_first_pilot_pattern"] == "parent_first_pilot_then_child_necessity_review"
    assert auth["post_pilot_child_necessity_review_required"] is True
    assert auth["child_span_work_requires_later_owner_promotion"] is True
    assert auth["parent_span_as_chunk_boundary_authorized"] is True
    assert auth["child_spans_authorized"] is False
    assert auth["output_change_authorized"] is True
    assert auth["implementation_authorized"] is True


def test_parallel_t371_promotion_record_is_narrow_and_non_output_changing() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)
    promotion = data["parallel_t371_parent_only_promotion_record"]

    assert promotion["task_id"] == "T371"
    assert promotion["path"] == ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
    assert promotion["reviewed_gold_manifest"] == "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
    assert promotion["reviewed_gold_case_id"] == "1cor8_10_parent_only_reviewed_gold"
    assert promotion["selected_option"] == "T371-A"
    assert set(promotion["exact_variant_refs"]) == {"1Cor.9.20", "1Cor.10.9"}
    assert promotion["boundary_dependency_or_non_dependency"] == "variant_non_dependent"
    assert promotion["reviewed_gold_dependency_or_non_dependency"] == "variant_non_dependent"
    assert promotion["reviewed_gold_promoted"] is True
    assert promotion["child_spans_authorized"] is False
    assert promotion["output_change_authorized"] is False
    assert promotion["implementation_authorized"] is False


def test_validator_rejects_missing_required_lane(tmp_path: Path) -> None:
    text = READINESS_MAP.read_text(encoding="utf-8")
    text = text.replace("lane_id: gospel_discourse_wj", "lane_id: gospel_discourse_missing")
    candidate = tmp_path / "readiness.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(validator.ReadinessMapError, match="lane_sequence missing"):
        validator.validate_readiness_map(candidate)
