from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "roadmap" / "T344_REVELATION_OWNER_SELECTION_DOCKET.md"
TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    text = read(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def test_t344_docket_records_owner_selected_research_only_option() -> None:
    doc = read(DOC)

    assert "owner_selection_status: selected" in doc
    assert "selected_option: REV-T344-E" in doc
    assert "Rev.12.1-Rev.14.20" in doc
    for option in ["REV-T344-A", "REV-T344-B", "REV-T344-C", "REV-T344-D", "REV-T344-E"]:
        assert option in doc
    assert "Only one option may be selected." in doc
    assert "These spans are not approved unless the owner selects `REV-T344-C`." in doc
    assert "Revelation work may continue as research, review-packet" in doc


def test_t344_selected_e_is_research_only_and_non_authorizing() -> None:
    doc = read(DOC)
    task = load_yaml(TASK)
    auth = task["authorization"]

    assert task["status"] == "complete"
    assert auth["owner_selection_required"] is True
    assert auth["owner_selection_status"] == "selected"
    assert auth["selected_option"] == "REV-T344-E"
    assert auth["revelation_research_prep_only_allowed"] is True
    assert auth["non_output_changing_harnesses_allowed"] is True
    assert auth["non_output_changing_review_packets_allowed"] is True
    assert auth["non_output_changing_lane_prep_allowed"] is True
    assert auth["next_review_lane_after_revelation_research_prep"] == "epistle_argument_boundaries"
    assert auth["revelation_implementation_allowed"] is False
    assert auth["output_change_authorized"] is False
    assert auth["reviewed_gold_promoted"] is False
    assert auth["graph_edge_generation_allowed"] is False
    assert auth["embedding_or_vector_work_allowed"] is False
    assert "This docket does not authorize:" in doc
    assert "reviewed-gold promotion" in doc
    assert "generated chunk regeneration" in doc


def test_t344_preserves_revelation_hermeneutic_neutrality() -> None:
    doc = read(DOC)

    for phrase in [
        "preserve orthodox interpretive possibilities",
        "linear or non-linear chronology",
        "premillennial",
        "amillennial",
        "postmillennial",
        "preterist",
        "historicist",
        "futurist",
        "idealist",
        "symbolic identities",
        "Daniel or other cross-references",
    ]:
        assert phrase in doc


def test_t344_updates_readiness_and_decision_register() -> None:
    readiness = load_yaml(READINESS)
    register = read(REGISTER)
    by_lane = {lane["lane_id"]: lane for lane in readiness["lane_sequence"]}
    target = by_lane["revelation_apocalyptic"]["selected_review_target"]

    assert target["owner_selection_status"] == "selected"
    assert target["selected_option"] == "REV-T344-E"
    assert target["owner_selection_docket"] == "docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md"
    assert readiness["next_route"]["task_id"] == "T356"
    assert readiness["next_route"]["route_type"] == "john3_wj_owner_review_docket"
    assert readiness["next_route"]["owner_selection_status"] == "selected"
    assert readiness["next_route"]["selected_option"] == "REV-T344-E"
    assert readiness["next_route"]["prior_triage_task"] == "T351"
    assert readiness["next_route"]["prior_inventory_task"] == "T354"
    assert readiness["next_route"]["prior_policy_task"] == "T355"
    assert readiness["next_route"]["review_packet_lane"] == "gospel_discourse_wj"
    assert readiness["next_route"]["docket"] == ".ai/control/john3_wj_owner_review_docket.yaml"
    assert readiness["next_route"]["selected_target"] == "john3_wj_speaker_boundary"
    assert readiness["next_route"]["selected_target_status"] == "owner_selection_pending"
    assert readiness["next_route"]["john3_owner_selection_status"] == "pending"
    assert readiness["next_route"]["john3_selected_option"] == "pending"
    assert readiness["next_route"]["implementation_authorized"] is False
    assert readiness["next_route"]["output_change_authorized"] is False
    assert "CD-016" in register
    assert "Revelation owner selected research-only before reviewed gold or implementation" in register


def test_t344_records_t344r_next_and_keeps_t345_blocked() -> None:
    state = load_yaml(ROADMAP_STATE)
    phase_4 = state["phases"]["phase_4"]
    tasks = {task["id"]: task for task in phase_4["tasks"]}
    future = {task["id"]: task for task in phase_4["future_sequence"]}

    assert tasks["T344"]["status"] == "complete"
    assert tasks["T344"]["required_handoff"] == ".ai/handoffs/T344/handoff.md"
    assert tasks["T344"]["owner_selection_status"] == "selected"
    assert tasks["T344"]["selected_option"] == "REV-T344-E"
    assert tasks["T344"]["output_change_authorized"] is False
    assert "T344" not in future
    assert tasks["T351"]["status"] == "complete"
    assert tasks["T351"]["lane"] == "bible_wide_research_triage"
    assert tasks["T351"]["next_review_lane_after_completion"] == "select_from_review_packet_ready_lanes"
    assert tasks["T352"]["status"] == "complete"
    assert tasks["T352"]["lane"] == "epistle_argument"
    assert tasks["T352"]["packet_status"] == "pending_human_review"
    assert tasks["T353"]["status"] == "complete"
    assert tasks["T353"]["lane"] == "divine_name_title_capitalization"
    assert tasks["T353"]["inventory_status"] == "generated_non_authorizing"
    assert tasks["T354"]["status"] == "complete"
    assert tasks["T354"]["lane"] == "gospel_discourse_wj"
    assert tasks["T354"]["inventory_status"] == "generated_non_authorizing"
    assert tasks["T355"]["status"] == "complete"
    assert tasks["T355"]["lane"] == "gospel_discourse_wj"
    assert tasks["T355"]["policy_status"] == "selected_for_next_owner_review"
    assert tasks["T355"]["selected_target"] == "john3_wj_speaker_boundary"
    assert tasks["T356"]["status"] == "complete"
    assert tasks["T356"]["lane"] == "gospel_discourse_wj"
    assert tasks["T356"]["owner_selection_status"] == "pending"
    assert tasks["T356"]["selected_option"] == "pending"
    assert tasks["T356"]["docket"] == ".ai/control/john3_wj_owner_review_docket.yaml"
    assert tasks["T356"]["selected_target"] == "john3_wj_speaker_boundary"
    assert tasks["T358"]["status"] == "complete"
    assert tasks["T358"]["lane"] == "bible_wide_research"
    assert tasks["T358"]["research_registry"] == ".ai/control/bible_wide_chunking_research_registry.yaml"
    assert tasks["T358"]["book_count"] == 66
    assert tasks["T358"]["implementation_authorized"] is False
    assert tasks["T359"]["status"] == "complete"
    assert tasks["T359"]["lane"] == "source_metadata_research"
    assert tasks["T359"]["research_atlas"] == ".ai/control/source_metadata_research_atlas.yaml"
    assert tasks["T359"]["source_metadata_authority_allowed"] is False
    assert tasks["T360"]["status"] == "complete"
    assert tasks["T360"]["lane"] == "apocalyptic_prophetic_intertext"
    assert tasks["T360"]["dossier_queue"] == ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml"
    assert tasks["T360"]["intertext_truth_authorized"] is False
    assert tasks["T361"]["status"] == "complete"
    assert tasks["T361"]["lane"] == "epistle_argument"
    assert tasks["T361"]["dossier_queue"] == ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml"
    assert tasks["T361"]["doctrinal_system_selection_allowed"] is False
    assert tasks["T362"]["status"] == "complete"
    assert tasks["T362"]["lane"] == "gospel_discourse_wj"
    assert tasks["T362"]["dossier_queue"] == ".ai/control/gospel_wj_discourse_dossier_queue.yaml"
    assert tasks["T362"]["speaker_attribution_authorized"] is False
    assert tasks["T363"]["status"] == "complete"
    assert tasks["T363"]["lane"] == "narrative_pericope"
    assert tasks["T363"]["dossier_queue"] == ".ai/control/narrative_legal_covenant_dossier_queue.yaml"
    assert tasks["T363"]["covenant_theology_authorized"] is False
    assert tasks["T364"]["status"] == "complete"
    assert tasks["T364"]["lane"] == "wisdom_dialogue"
    assert tasks["T364"]["dossier_queue"] == ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml"
    assert tasks["T364"]["wisdom_theology_authorized"] is False
    assert future["T357"]["status"] == "planned"
    assert future["T357"]["requires_owner_selection"] is True
    assert future["T345"]["status"] == "planned"
    assert future["T345"]["requires_owner_selection_gate"] == "scripts/validate_owner_selection_implementation_gate.py"
