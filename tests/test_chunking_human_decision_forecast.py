from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_chunking_human_decision_forecast as validator


ROOT = Path(__file__).resolve().parents[1]
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T369_HUMAN_DECISION_FORECAST_AND_CHUNKING_READY_ROADMAP.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_chunking_human_decision_forecast_validates_current_repo() -> None:
    data = validator.validate_chunking_human_decision_forecast()

    assert data["object_type"] == "chunking_human_decision_forecast"
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["goal_blocked_explanation"]["thread_goal_status"] == "blocked"


def test_forecast_names_predictable_human_decision_gates() -> None:
    data = validator.validate_chunking_human_decision_forecast()
    by_id = {item["decision_id"]: item for item in data["front_loaded_decisions"]}

    assert set(by_id) >= validator.REQUIRED_DECISIONS
    assert by_id["HDF-001"]["earliest_task"] == "T369"
    assert by_id["HDF-001"]["status"] == "projected_owner_pattern_selected"
    assert by_id["HDF-001"]["selected_option"] == "1COR8-10-T369-B"
    assert by_id["HDF-001"]["selected_children"] == []
    assert by_id["HDF-001"]["conflict_scan_result"] == "no_conflict_detected"
    assert by_id["HDF-002"]["status"] == "selected_case_by_case_policy"
    assert by_id["HDF-002"]["selected_policy"] == "TCP-T378-B"
    assert by_id["HDF-002"]["policy_record"] == ".ai/control/textual_critical_case_policy.yaml"
    assert by_id["HDF-002"]["projection_policy_pattern"] == "ODP-005"
    assert by_id["HDF-003"]["status"] == "t371_a_parent_only_reviewed_gold_promoted"
    assert by_id["HDF-003"]["current_decision_packet"] == ".ai/control/t371_variant_dependency_owner_decision_packet.yaml"
    assert by_id["HDF-003"]["promotion_record"] == ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
    assert by_id["HDF-003"]["reviewed_gold_manifest"] == "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
    assert by_id["HDF-003"]["selected_option"] == "T371-A"
    assert by_id["HDF-003"]["reviewed_gold_promoted"] is True
    assert by_id["HDF-003"]["next_safe_task"] == "T372"
    assert by_id["HDF-003"]["next_owner_gate"] == "T373"
    assert by_id["HDF-013"]["status"] == "complete_non_output_changing_plan"
    assert by_id["HDF-013"]["harness_plan"] == ".ai/control/t372_route_isolation_harness_plan.yaml"
    assert by_id["HDF-013"]["next_owner_gate"] == "T373"
    assert by_id["HDF-014"]["status"] == "complete_owner_authorized_exact_parent_only_pilot"
    assert by_id["HDF-014"]["authorization_record"] == ".ai/control/t373_owner_implementation_authorization.yaml"
    assert by_id["HDF-014"]["selected_option"] == "T373-A"
    assert by_id["HDF-014"]["selected_children"] == []
    assert by_id["HDF-014"]["next_task"] == "T374"
    assert "chunk_output_change" in by_id["HDF-004"]["must_stop_for"]
    assert by_id["HDF-005"]["status"] == "selected_t373_a"
    assert by_id["HDF-006"]["status"] == "decided_for_t374_parent_only_first"
    assert "post-pilot review" in by_id["HDF-006"]["parent_first_pilot_pattern"]
    assert "child_span_without_post_pilot_review" in by_id["HDF-006"]["non_authorizations"]
    assert by_id["HDF-007"]["recommended_default_if_owner_unavailable"] == "systematic_theology_can_be_advisory_not_chunk_authority"
    assert by_id["HDF-012"]["recommended_default_if_owner_unavailable"] == "require_no_context_audit_before_merge"
    assert by_id["HDF-012"]["status"] == "decided_for_t374_required"


def test_forecast_defines_chunking_ready_without_authorizing_output() -> None:
    data = validator.validate_chunking_human_decision_forecast()
    ready = data["chunking_ready_definition"]

    assert "owner_selected_exact_target" in ready["ready_for_first_output_changing_chunk_pr_requires"]
    assert "reviewed_gold_or_equivalent_governed_evidence_promoted_by_owner" in ready["ready_for_first_output_changing_chunk_pr_requires"]
    assert "explicit_owner_implementation_authorization" in ready["ready_for_first_output_changing_chunk_pr_requires"]
    assert "owner_decision_option_presentation_policy_if_owner_gate" in ready["ready_for_first_output_changing_chunk_pr_requires"]
    assert "packet_is_pending_human_review" in ready["not_ready_if"]
    assert "do_not_treat_this_forecast_as_authorization" in data["what_not_to_do"]
    assert "do_not_present_owner_gates_without_options_repercussions_risks_and_non_authorizations" in data["what_not_to_do"]


def test_forecast_roadmap_doc_explains_what_not_to_do() -> None:
    text = ROADMAP_DOC.read_text(encoding="utf-8")

    assert "Why The Goal Looked Blocked" in text
    assert "Front-Loaded Human Decisions" in text
    assert "HDF-001 - 1 Corinthians 8-10 Owner Option" in text
    assert "Do not treat this roadmap or forecast as authorization" in text
    assert "Do not implement chunks from pending packets" in text
    assert "projected owner pattern" in text
    assert "conflicting prior owner decisions" in text


def test_roadmap_state_contains_explicit_t369_to_t376_runway() -> None:
    state = yaml.safe_load(ROADMAP_STATE.read_text(encoding="utf-8"))
    future = {
        item["id"]: item
        for item in state["phases"]["phase_4"]["future_sequence"]
    }

    for task_id in ("T369", "T370", "T379", "T380", "T371", "T372", "T373", "T374", "T375", "T376"):
        assert task_id in future
    assert future["T369"]["human_decision_forecast"] == ".ai/control/chunking_human_decision_forecast.yaml"
    assert future["T369"]["status"] == "complete"
    assert future["T369"]["selected_option"] == "1COR8-10-T369-B"
    assert future["T370"]["status"] == "complete"
    assert future["T370"]["starts_only_if"] == "T369_parent_only_projected_selection"
    assert future["T370"]["evidence_packet"] == "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml"
    assert future["T370"]["reviewed_gold_promoted"] is False
    assert future["T379"]["status"] == "complete"
    assert future["T379"]["selected_policy"] == "TCP-T378-B"
    assert future["T379"]["policy_record"] == ".ai/control/textual_critical_case_policy.yaml"
    assert future["T380"]["status"] == "complete"
    assert future["T380"]["owner_decision_packet"] == ".ai/control/t371_variant_dependency_owner_decision_packet.yaml"
    assert future["T380"]["target_owner_task"] == "T371"
    assert future["T371"]["status"] == "complete"
    assert future["T371"]["owner_decision_required"] is False
    assert future["T371"]["starts_only_if"] == "T370_builds_governed_evidence_and_T379_selects_case_policy"
    assert future["T371"]["evidence_packet"] == "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml"
    assert future["T371"]["selected_option"] == "T371-A"
    assert future["T371"]["promotion_record"] == ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
    assert future["T371"]["reviewed_gold_manifest"] == "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
    assert future["T371"]["reviewed_gold_promoted"] is True
    assert future["T372"]["status"] == "complete"
    assert future["T372"]["starts_only_if"] == "T371_A_parent_only_reviewed_gold_promoted"
    assert future["T372"]["harness_plan"] == ".ai/control/t372_route_isolation_harness_plan.yaml"
    assert future["T372"]["harness_only"] is True
    assert future["T372"]["owner_implementation_authorization_required"] is True
    assert future["T373"]["starts_only_if"] == "T372_route_isolation_harness_plan_complete"
    assert future["T373"]["status"] == "complete"
    assert future["T373"]["owner_decision_required"] is False
    assert future["T373"]["selected_option"] == "T373-A"
    assert future["T373"]["authorization_record"] == ".ai/control/t373_owner_implementation_authorization.yaml"
    assert "CD-052" in future["T373"]["decision_register_entries"]
    assert future["T373"]["general_parent_first_pilot_pattern"] == "parent_first_pilot_then_child_necessity_review"
    assert future["T373"]["post_pilot_child_necessity_review_required"] is True
    assert future["T373"]["implementation_authorized"] is True
    assert future["T373"]["child_spans_authorized"] is False
    assert future["T374"]["starts_only_if"] == "T373_A_authorizes_exact_parent_only_output_pilot"
    assert future["T374"]["output_change_authorized"] is True
    assert future["T374"]["implementation_authorized"] is True
    assert future["T374"]["child_spans_authorized"] is False
    assert future["T374"]["requires_post_pilot_child_necessity_review_gate"] is True
    assert future["T375"]["post_pilot_child_necessity_review_required"] is True
    assert future["T375"]["child_span_work_requires_later_owner_promotion"] is True


def test_forecast_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_chunking_human_decision_forecast())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "forecast.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.ForecastError, match="authorizes_chunk_output_change"):
        validator.validate_chunking_human_decision_forecast(candidate)


def test_forecast_rejects_missing_1cor_owner_gate(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_chunking_human_decision_forecast())
    data["front_loaded_decisions"] = [
        item for item in data["front_loaded_decisions"] if item["decision_id"] != "HDF-001"
    ]
    candidate = tmp_path / "forecast.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.ForecastError, match="missing front-loaded decisions"):
        validator.validate_chunking_human_decision_forecast(candidate)
