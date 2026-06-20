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
    assert by_lane["epistle_argument"]["new_algorithm_work_ready"] is True
    assert all(
        lane["new_algorithm_work_ready"] is False
        for lane_id, lane in by_lane.items()
        if lane_id != "epistle_argument"
    )


def test_lessons_are_stored_in_first_class_surfaces() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    surfaces = set(data["lessons_storage"]["surfaces"])
    assert validator.REQUIRED_LESSON_SURFACES <= surfaces
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
    assert ".ai/control/orthodox_hermeneutic_firewall_docket.yaml" in surfaces
    assert ".ai/control/textual_critical_policy_docket.yaml" in surfaces
    assert ".ai/control/textual_critical_policy_owner_options.yaml" in surfaces
    assert ".ai/control/textual_critical_case_policy.yaml" in surfaces
    assert ".ai/control/t371_variant_dependency_owner_decision_packet.yaml" in surfaces
    assert ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml" in surfaces
    assert ".ai/control/t372_route_isolation_harness_plan.yaml" in surfaces
    assert ".ai/control/t373_owner_implementation_authorization.yaml" in surfaces
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

    assert data["next_route"]["task_id"] == "T374"
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

    assert data["next_route"]["task_id"] == "T374"
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

    assert data["next_route"]["task_id"] == "T374"
    assert data["next_route"]["variant_sensitive_policy_gate_task"] == "T379"
    assert data["next_route"]["variant_sensitive_policy_selected"] is True
    assert data["next_route"]["selected_textual_critical_policy"] == "TCP-T378-B"
    assert data["next_route"]["t371_promotion_blocked_until_textual_policy"] is False
    assert data["next_route"]["variant_dependency_owner_decision_required"] is False
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

    assert data["next_route"]["task_id"] == "T374"
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

    assert data["next_route"]["task_id"] == "T374"
    assert data["next_route"]["owner_decision_packet"] == ".ai/control/t371_variant_dependency_owner_decision_packet.yaml"
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


def test_next_route_advances_to_t374_after_t373_authorization() -> None:
    data = validator.validate_readiness_map(READINESS_MAP)

    assert data["next_route"]["task_id"] == "T374"
    assert data["next_route"]["route_type"] == "epistle_argument_route_isolated_output_pilot"
    assert data["next_route"]["starts_only_if"] == "T373_A_authorizes_exact_parent_only_output_pilot"
    assert data["next_route"]["recommended_target"] == "epistle_argument"
    assert data["next_route"]["selected_target"] == "1cor8_10_food_offered_to_idols"
    assert data["next_route"]["selected_passage"] == "1Cor.8-1Cor.10"
    assert data["next_route"]["exact_parent_candidate"] == "1Cor.8.1-1Cor.10.33"
    assert data["next_route"]["selected_option"] == "T373-A"
    assert data["next_route"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["next_route"]["selected_children"] == []
    assert data["next_route"]["selection_mode"] == "explicit_owner_authorization"
    assert data["next_route"]["projection_policy"] == ".ai/control/owner_decision_projection_policy.yaml"
    assert data["next_route"]["conflict_scan_result"] == "no_conflict_detected"
    assert data["next_route"]["review_packet"] == "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md"
    assert data["next_route"]["owner_review_docket"] == ".ai/control/1cor8_10_epistle_owner_review_docket.yaml"
    assert data["next_route"]["evidence_packet"] == "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml"
    assert data["next_route"]["owner_decision_packet"] == ".ai/control/t371_variant_dependency_owner_decision_packet.yaml"
    assert data["next_route"]["promotion_record"] == ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
    assert data["next_route"]["reviewed_gold_manifest"] == "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
    assert data["next_route"]["reviewed_gold_case_id"] == "1cor8_10_parent_only_reviewed_gold"
    assert data["next_route"]["harness_plan"] == ".ai/control/t372_route_isolation_harness_plan.yaml"
    assert data["next_route"]["authorization_record"] == ".ai/control/t373_owner_implementation_authorization.yaml"
    assert data["next_route"]["option_presentation_policy"] == ".ai/control/owner_decision_option_presentation_policy.yaml"
    assert data["next_route"]["harness_plan_status"] == "complete_non_output_changing_plan"
    assert data["next_route"]["packet_status"] == "parent_only_reviewed_gold_promoted"
    assert data["next_route"]["owner_selection_status"] == "selected"
    assert data["next_route"]["owner_decision_required"] is False
    assert data["next_route"]["selected_t371_option"] == "T371-A"
    assert data["next_route"]["selected_t373_option"] == "T373-A"
    assert data["next_route"]["prior_owner_decision_task"] == "T367"
    assert data["next_route"]["general_parent_first_pilot_pattern"] == "parent_first_pilot_then_child_necessity_review"
    assert data["next_route"]["post_pilot_child_necessity_review_required"] is True
    assert data["next_route"]["child_span_work_requires_later_owner_promotion"] is True
    assert data["next_route"]["packet_strengthening_task"] == "T368"
    assert data["next_route"]["parent_selection_task"] == "T369"
    assert data["next_route"]["evidence_prep_task"] == "T370"
    assert data["next_route"]["parent_gold_promotion_task"] == "T371"
    assert data["next_route"]["implementation_authorization_task"] == "T373"
    assert data["next_route"]["prior_harness_task"] == "T372"
    assert data["next_route"]["prior_packet_task"] == "T352"
    assert data["next_route"]["prior_issue_dossier_task"] == "T361"
    assert data["next_route"]["orthodox_firewall"] == ".ai/control/orthodox_hermeneutic_firewall_docket.yaml"
    assert data["next_route"]["textual_critical_policy_docket"] == ".ai/control/textual_critical_policy_docket.yaml"
    assert data["next_route"]["harness_only"] is False
    assert data["next_route"]["owner_implementation_authorization_recorded"] is True
    assert data["next_route"]["output_change_authorized"] is True
    assert data["next_route"]["output_change_authorization_scope"] == "exact_t374_pilot_only"
    assert data["next_route"]["implementation_authorized"] is True
    assert data["next_route"]["implementation_authorization_scope"] == "exact_t374_pilot_only"
    assert data["next_route"]["reviewed_gold_promoted"] is True
    assert data["next_route"]["parent_span_as_chunk_boundary_authorized"] is True
    assert data["next_route"]["parent_span_authorization_scope"] == "exact_t374_pilot_only"
    assert data["next_route"]["route_behavior_authorized"] is True
    assert data["next_route"]["route_behavior_authorization_scope"] == "exact_t374_target_only"
    assert data["next_route"]["evaluator_change_authorized"] is False
    assert data["next_route"]["graph_edge_generation_allowed"] is False
    assert "no_context_audit_surface" in data["next_route"]["required_t374_work_must_record"]
    assert "post_pilot_child_necessity_review_gate" in data["next_route"]["required_t374_work_must_record"]
    assert "child_spans_are_added_without_later_owner_promotion" in data["next_route"]["must_fail_if"]
    assert "child_spans_are_added_without_post_pilot_review" in data["next_route"]["must_fail_if"]

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
