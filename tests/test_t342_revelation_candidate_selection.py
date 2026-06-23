from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "roadmap" / "T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md"
TASK = ROOT / ".ai" / "tasks" / "T342.task.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    text = read(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def test_t342_selects_rev12_14_only() -> None:
    doc = read(DOC)

    assert "T342 selects exactly one Revelation review-packet target" in doc
    assert "Rev.12-Rev.14" in doc
    assert "Rev.12.1-Rev.14.20" in doc
    assert "rev12_14_symbolic_scenes" in doc
    assert "T343 should create a pending, non-authorizing review packet" in doc


def test_t342_is_non_authorizing() -> None:
    doc = read(DOC)
    task = load_yaml(TASK)
    auth = task["authorization"]

    assert "does not create a review packet" in doc
    assert "does not authorize" in doc
    assert auth["revelation_implementation_allowed"] is False
    assert auth["output_change_authorized"] is False
    assert auth["reviewed_gold_promoted"] is False
    assert auth["review_packet_created"] is False
    assert auth["boundary_import_allowed"] is False
    assert auth["boundary_apocryphal_material_import_allowed"] is False
    assert auth["global_rule_allowed"] is False
    assert auth["t327g_allowed"] is False


def test_t342_through_t376_remain_complete_while_live_route_points_to_t384() -> None:
    state = load_yaml(ROADMAP_STATE)
    readiness = load_yaml(READINESS)
    tasks = {task["id"]: task for task in state["phases"]["phase_4"]["tasks"]}
    future = {task["id"]: task for task in state["phases"]["phase_4"]["future_sequence"]}

    assert tasks["T342"]["status"] == "complete"
    assert tasks["T342"]["required_handoff"] == ".ai/handoffs/T342/handoff.md"
    assert "T342" not in future
    assert tasks["T343"]["status"] == "complete"
    assert tasks["T343"]["required_handoff"] == ".ai/handoffs/T343/handoff.md"
    assert "T343" not in future
    assert tasks["T344"]["status"] == "complete"
    assert tasks["T344"]["required_handoff"] == ".ai/handoffs/T344/handoff.md"
    assert "T344" not in future
    assert tasks["T351"]["status"] == "complete"
    assert tasks["T351"]["required_handoff"] == ".ai/handoffs/T351/handoff.md"
    assert tasks["T352"]["status"] == "complete"
    assert tasks["T352"]["required_handoff"] == ".ai/handoffs/T352/handoff.md"
    assert tasks["T353"]["status"] == "complete"
    assert tasks["T353"]["required_handoff"] == ".ai/handoffs/T353/handoff.md"
    assert tasks["T354"]["status"] == "complete"
    assert tasks["T354"]["required_handoff"] == ".ai/handoffs/T354/handoff.md"
    assert tasks["T355"]["status"] == "complete"
    assert tasks["T355"]["required_handoff"] == ".ai/handoffs/T355/handoff.md"
    assert tasks["T356"]["status"] == "complete"
    assert tasks["T356"]["required_handoff"] == ".ai/handoffs/T356/handoff.md"
    assert tasks["T356"]["selected_target"] == "john3_wj_speaker_boundary"
    assert tasks["T356"]["owner_selection_status"] == "selected"
    assert tasks["T356"]["selected_option"] == "JOHN3-T356-B"
    assert tasks["T358"]["status"] == "complete"
    assert tasks["T358"]["required_handoff"] == ".ai/handoffs/T358/handoff.md"
    assert tasks["T358"]["corpus_scope"] == "canonical_66"
    assert tasks["T359"]["status"] == "complete"
    assert tasks["T359"]["required_handoff"] == ".ai/handoffs/T359/handoff.md"
    assert tasks["T359"]["research_atlas"] == ".ai/control/source_metadata_research_atlas.yaml"
    assert tasks["T360"]["status"] == "complete"
    assert tasks["T360"]["required_handoff"] == ".ai/handoffs/T360/handoff.md"
    assert tasks["T360"]["dossier_queue"] == ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml"
    assert tasks["T361"]["status"] == "complete"
    assert tasks["T361"]["required_handoff"] == ".ai/handoffs/T361/handoff.md"
    assert tasks["T361"]["dossier_queue"] == ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml"
    assert tasks["T362"]["status"] == "complete"
    assert tasks["T362"]["required_handoff"] == ".ai/handoffs/T362/handoff.md"
    assert tasks["T362"]["dossier_queue"] == ".ai/control/gospel_wj_discourse_dossier_queue.yaml"
    assert tasks["T363"]["status"] == "complete"
    assert tasks["T363"]["required_handoff"] == ".ai/handoffs/T363/handoff.md"
    assert tasks["T363"]["dossier_queue"] == ".ai/control/narrative_legal_covenant_dossier_queue.yaml"
    assert tasks["T364"]["status"] == "complete"
    assert tasks["T364"]["required_handoff"] == ".ai/handoffs/T364/handoff.md"
    assert tasks["T364"]["dossier_queue"] == ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml"
    assert tasks["T365"]["status"] == "complete"
    assert tasks["T365"]["required_handoff"] == ".ai/handoffs/T365/handoff.md"
    assert tasks["T365"]["dossier_queue"] == ".ai/control/prophetic_oracle_vision_dossier_queue.yaml"
    assert tasks["T366"]["status"] == "complete"
    assert tasks["T366"]["required_handoff"] == ".ai/handoffs/T366/handoff.md"
    assert tasks["T366"]["dossier_queue"] == ".ai/control/textual_variant_source_tradition_dossier_queue.yaml"
    assert tasks["T367"]["status"] == "complete"
    assert tasks["T367"]["required_handoff"] == ".ai/handoffs/T367/handoff.md"
    assert tasks["T367"]["john3_selected_option"] == "JOHN3-T356-B"
    assert tasks["T368"]["status"] == "complete"
    assert tasks["T368"]["required_handoff"] == ".ai/handoffs/T368/handoff.md"
    assert tasks["T368"]["owner_review_docket"] == ".ai/control/1cor8_10_epistle_owner_review_docket.yaml"
    assert future["T369"]["status"] == "complete"
    assert future["T369"]["selected_option"] == "1COR8-10-T369-B"
    assert future["T369"]["selected_children"] == []
    assert future["T370"]["status"] == "complete"
    assert future["T370"]["evidence_packet"] == "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml"
    assert future["T370"]["reviewed_gold_promoted"] is False
    assert future["T371"]["status"] == "complete"
    assert future["T371"]["selected_option"] == "T371-A"
    assert future["T371"]["reviewed_gold_promoted"] is True
    assert future["T372"]["status"] == "complete"
    assert future["T372"]["harness_plan"] == ".ai/control/t372_route_isolation_harness_plan.yaml"
    assert future["T373"]["status"] == "complete"
    assert future["T374"]["status"] == "complete_output_changed_additive_parent_overlay"
    assert future["T375"]["status"] == "complete_review_only_child_spans_not_necessary_now"
    assert future["T376"]["status"] == "complete_selected_research_first_epistle_argument_runway"
    assert readiness["next_route"]["task_id"] == "T392"
    assert readiness["next_route"]["route_type"] == "epistle_argument_review_packet_strengthening"
    assert readiness["next_route"]["starts_only_if"] == "explicit_owner_selection_of_T385_A"
    assert readiness["next_route"]["review_packet"] == "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md"
    assert readiness["next_route"]["completion_status"] == "complete_review_packet_strengthening_only"
    assert readiness["next_route"]["selected_t376_option"] == "T376-A"
    assert readiness["next_route"]["selected_lane"] == "epistle_argument"
    assert readiness["next_route"]["selection_mode"] == "owner_selected_review_packet_strengthening_only"
    assert readiness["next_route"]["selected_option"] == "T385-A"
    assert readiness["next_route"]["review_packet_strengthened"] is True
    assert readiness["next_route"]["exact_next_owner_action"] == "Goal5_owner_reviewed_gold_promotion_decision_packet"
    assert readiness["next_route"]["owner_decision_required_before_promotion_or_implementation"] is True
    assert readiness["next_route"]["exact_target_selected_for_promotion_or_implementation"] is False
    assert readiness["next_route"]["output_change_authorized"] is False
    assert readiness["next_route"]["implementation_authorized"] is False
    assert readiness["next_route"]["reviewed_gold_promoted"] is False
    assert readiness["next_route"]["child_spans_authorized"] is False


def test_t342_risk_gate_categories_present() -> None:
    doc = read(DOC)

    for heading in [
        "Confirmed Risks",
        "Plausible Risks",
        "Unlikely But High-Impact Risks",
        "Watch-Later Conditions",
        "Tests Or Guards Needed",
        "Owner Decisions Needed",
    ]:
        assert heading in doc
