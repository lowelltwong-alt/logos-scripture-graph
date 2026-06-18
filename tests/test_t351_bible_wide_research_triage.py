from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_bible_chunking_research_triage as validator


ROOT = Path(__file__).resolve().parents[1]
TRIAGE_MAP = ROOT / ".ai" / "control" / "bible_chunking_research_triage_map.yaml"
ATLAS = ROOT / "docs" / "roadmap" / "T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md"
TASK = ROOT / ".ai" / "tasks" / "T351.task.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
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


def test_t351_triage_map_validates_and_is_non_authorizing() -> None:
    data = validator.validate_triage_map(TRIAGE_MAP)

    assert data["object_type"] == "bible_chunking_research_triage_map"
    assert data["trust_zone"] == "canonical"
    assert set(data["allowed_triage_statuses"]) == validator.ALLOWED_STATUSES
    assert data["authority"]["records_research_triage"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_new_algorithm_work"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_revelation_implementation"] is False
    assert data["authority"]["authorizes_graph_or_vector_work"] is False


def test_t351_classifies_required_lanes_before_chunking() -> None:
    data = validator.validate_triage_map(TRIAGE_MAP)
    lanes = {lane["lane_id"]: lane for lane in data["lanes"]}

    assert set(lanes) >= validator.REQUIRED_LANES
    assert lanes["revelation_apocalyptic"]["triage_status"] == "research_first"
    assert lanes["epistle_argument"]["triage_status"] == "review_packet_ready"
    assert lanes["narrative_pericope"]["triage_status"] == "review_packet_ready"
    assert lanes["legal_covenant"]["triage_status"] == "review_packet_ready"
    assert lanes["psalms_poetry"]["triage_status"] == "governed_hold"
    assert lanes["divine_name_title_capitalization"]["triage_status"] == "research_first"
    assert lanes["bible_wide_orchestration"]["triage_status"] == "implementation_blocked"
    assert all(lane["output_change_authorized"] is False for lane in lanes.values())
    assert all(lane["implementation_authorized"] is False for lane in lanes.values())
    assert all(lane["reviewed_gold_promoted"] is False for lane in lanes.values())


def test_t351_divine_capitalization_rule_is_non_authorizing() -> None:
    data = validator.validate_triage_map(TRIAGE_MAP)
    lanes = {lane["lane_id"]: lane for lane in data["lanes"]}
    rule = data["evidence_rules"]["divine_name_capitalization"]
    lane = lanes["divine_name_title_capitalization"]

    for phrase in [
        "God/god",
        "LORD/Lord/lord",
        "Spirit/spirit",
        "Father/father",
        "Word/word",
        "Holy Spirit/holy spirit",
        "graph edges",
        "chunk boundaries",
        "Trinitarian relation",
    ]:
        assert phrase in rule
    assert lane["triage_status"] == "research_first"
    assert lane["output_change_authorized"] is False
    assert lane["implementation_authorized"] is False
    assert lane["reviewed_gold_promoted"] is False
    assert "John.1.1-John.1.18 Word/word" in lane["review_packet_candidates"]
    assert "Capitalization can encode divine identity" in lane["downstream_theological_risks"][0]


def test_t351_atlas_records_whole_bible_first_decision() -> None:
    atlas = read(ATLAS)

    for phrase in [
        "Research the entire Bible first",
        "review_packet_ready",
        "research_first",
        "governed_hold",
        "implementation_blocked",
        "Epistle argument boundaries are still a strong candidate",
        "Divine Name/Title Capitalization Watchlist",
        "God/god",
        "Spirit/spirit",
        "Word/word",
        "That is not implementation authority",
        "T351 does not authorize",
    ]:
        assert phrase in atlas


def test_t351_task_and_roadmap_are_active_and_numeric() -> None:
    task = load_yaml(TASK)
    state = load_yaml(ROADMAP_STATE)
    phase_4 = state["phases"]["phase_4"]
    tasks = {item["id"]: item for item in phase_4["tasks"]}
    future = {item["id"]: item for item in phase_4["future_sequence"]}

    assert task["id"] == "T351"
    assert task["status"] == "complete"
    assert task["authorization"]["bible_wide_research_triage_allowed"] is True
    assert task["authorization"]["output_change_authorized"] is False
    assert tasks["T344"]["status"] == "complete"
    assert tasks["T351"]["status"] == "complete"
    assert tasks["T351"]["supersedes_invalid_task_id"] == "T344R"
    assert tasks["T352"]["status"] == "complete"
    assert tasks["T352"]["lane"] == "epistle_argument"
    assert tasks["T353"]["status"] == "complete"
    assert tasks["T353"]["lane"] == "divine_name_title_capitalization"
    assert tasks["T354"]["status"] == "complete"
    assert tasks["T354"]["lane"] == "gospel_discourse_wj"
    assert tasks["T355"]["status"] == "complete"
    assert tasks["T355"]["lane"] == "gospel_discourse_wj"
    assert tasks["T355"]["selected_target"] == "john3_wj_speaker_boundary"
    assert tasks["T356"]["status"] == "complete"
    assert tasks["T356"]["lane"] == "gospel_discourse_wj"
    assert tasks["T356"]["owner_selection_status"] == "selected"
    assert tasks["T356"]["selected_option"] == "JOHN3-T356-B"
    assert tasks["T356"]["selected_target"] == "john3_wj_speaker_boundary"
    assert tasks["T358"]["status"] == "complete"
    assert tasks["T358"]["lane"] == "bible_wide_research"
    assert tasks["T358"]["book_count"] == 66
    assert tasks["T358"]["output_change_authorized"] is False
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
    assert tasks["T365"]["status"] == "complete"
    assert tasks["T365"]["lane"] == "prophetic_oracle"
    assert tasks["T365"]["dossier_queue"] == ".ai/control/prophetic_oracle_vision_dossier_queue.yaml"
    assert tasks["T365"]["fulfillment_theology_authorized"] is False
    assert tasks["T365"]["temple_theology_authorized"] is False
    assert tasks["T366"]["status"] == "complete"
    assert tasks["T366"]["lane"] == "textual_variant_source_tradition"
    assert tasks["T366"]["dossier_queue"] == ".ai/control/textual_variant_source_tradition_dossier_queue.yaml"
    assert tasks["T366"]["textual_critical_decision_authorized"] is False
    assert tasks["T366"]["boundary_import_allowed"] is False
    assert "T344R" not in future
    assert future["T357"]["status"] == "planned"
    assert future["T345"]["status"] == "planned"


def test_t351_decision_register_records_triage_decision() -> None:
    register = read(REGISTER)

    assert "CD-017" in register
    assert "Bible-wide research triage before more chunking algorithm work" in register
    assert "review_packet_ready" in register
    assert "lane_implementation_without_review_packet" in register
    assert "CD-018" in register
    assert "Divine-name capitalization is evidence, not graph or chunk authority" in register
    assert "capitalization_driven_graph_edge" in register
    assert "translation_convention_as_theological_truth" in register


def test_triage_validator_rejects_output_authority(tmp_path: Path) -> None:
    text = TRIAGE_MAP.read_text(encoding="utf-8")
    text = text.replace("authorizes_chunk_output_change: false", "authorizes_chunk_output_change: true")
    candidate = tmp_path / "triage.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(validator.TriageMapError, match="authorizes_chunk_output_change"):
        validator.validate_triage_map(candidate)
