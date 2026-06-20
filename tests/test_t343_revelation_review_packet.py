from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "roadmap" / "T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md"
PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "rev12_14_symbolic_scenes_review.md"
INDEX = ROOT / "eval" / "chunking_gold" / "review_packets" / "review_packet_index.json"
TASK = ROOT / ".ai" / "tasks" / "T343.task.yaml"
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


def test_t343_packet_is_pending_and_non_authorizing() -> None:
    packet = read(PACKET)
    task = load_yaml(TASK)
    auth = task["authorization"]

    assert "Status: `pending_human_review`" in packet
    assert "Rev.12.1-Rev.14.20" in packet
    assert "rev12_14_symbolic_scenes" in packet
    assert "This packet does not authorize output-changing work." in packet
    assert auth["review_packet_created"] is True
    assert auth["review_packet_status"] == "pending_human_review"
    assert auth["revelation_implementation_allowed"] is False
    assert auth["output_change_authorized"] is False
    assert auth["reviewed_gold_promoted"] is False
    assert auth["source_metadata_authority_allowed"] is False
    assert auth["internal_cross_reference_authority_allowed"] is False
    assert auth["strongs_number_authority_allowed"] is False
    assert auth["greek_lexical_rarity_authority_allowed"] is False


def test_t343_preserves_orthodox_interpretive_possibilities() -> None:
    combined = read(PACKET) + "\n" + read(DOC)

    for phrase in [
        "premillennial",
        "amillennial",
        "postmillennial",
        "preterist",
        "historicist",
        "futurist",
        "idealist",
        "Daniel cross-references",
        "preserve orthodox interpretive possibilities",
        "descriptive and text-local",
    ]:
        assert phrase in combined


def test_t343_source_metadata_is_evidence_not_authority() -> None:
    combined = read(PACKET) + "\n" + read(DOC)

    for phrase in [
        "internal cross-references",
        "Strong's-style",
        "Greek lexical rarity",
        "Source metadata",
        "not authority",
        "not become automatic Scripture authority",
        "lexical authority",
        "intertext authority",
        "graph-edge authority",
        "chunk-boundary authority",
    ]:
        assert phrase in combined


def test_t343_index_lists_packet_as_pending() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    entries = {entry["entry_id"]: entry for entry in data["entries"]}
    queue = {item["entry_id"]: item for item in data["promotion_queue"]}
    entry = entries["packet_rev12_14_symbolic_scenes_review"]

    assert entry["case_id"] == "rev12_14_symbolic_scenes"
    assert entry["status"] == "pending_human_review"
    assert entry["decision"] == "requires_more_research_before_gold"
    assert entry["recommended_next_action"] == "continue_revelation_research_prep"
    assert entry["output_change_authorized"] is False
    assert entry["implementation_allowed"] is False
    assert queue["packet_rev12_14_symbolic_scenes_review"]["priority"] == 18
    assert queue["packet_rev12_14_symbolic_scenes_review"]["recommended_next_action"] == "continue_revelation_research_prep"
    assert queue["packet_rev12_14_symbolic_scenes_review"]["implementation_allowed"] is False


def test_t343_readiness_now_points_to_t375_1cor_review_not_revelation_implementation() -> None:
    readiness = load_yaml(READINESS)
    by_lane = {lane["lane_id"]: lane for lane in readiness["lane_sequence"]}
    target = by_lane["revelation_apocalyptic"]["selected_review_target"]

    assert readiness["next_route"]["task_id"] == "T375"
    assert readiness["next_route"]["route_type"] == "epistle_argument_post_pilot_review"
    assert readiness["next_route"]["starts_only_if"] == "T374_additive_parent_overlay_implemented"
    assert readiness["next_route"]["selected_target"] == "1cor8_10_food_offered_to_idols"
    assert readiness["next_route"]["selected_option"] == "T374-OVERLAP-B"
    assert readiness["next_route"]["selected_children"] == []
    assert readiness["next_route"]["conflict_scan_result"] == "no_conflict_detected"
    assert readiness["next_route"]["owner_review_docket"] == ".ai/control/1cor8_10_epistle_owner_review_docket.yaml"
    assert readiness["next_route"]["evidence_packet"] == "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml"
    assert readiness["next_route"]["promotion_record"] == ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
    assert readiness["next_route"]["reviewed_gold_manifest"] == "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
    assert readiness["next_route"]["harness_plan"] == ".ai/control/t372_route_isolation_harness_plan.yaml"
    assert readiness["next_route"]["authorization_record"] == ".ai/control/t373_owner_implementation_authorization.yaml"
    assert readiness["next_route"]["implementation_manifest"] == ".ai/control/t374_additive_parent_overlay_manifest.yaml"
    assert readiness["next_route"]["owner_decision_required"] is False
    assert readiness["next_route"]["implementation_authorized"] is False
    assert readiness["next_route"]["output_change_authorized"] is False
    assert readiness["next_route"]["orthodox_firewall"] == ".ai/control/orthodox_hermeneutic_firewall_docket.yaml"
    assert readiness["next_route"]["textual_critical_policy_docket"] == ".ai/control/textual_critical_policy_docket.yaml"
    assert readiness["next_route"]["owner_selection_status"] == "selected"
    assert target["packet_status"] == "pending_human_review"
    assert target["owner_selection_status"] == "selected"
    assert target["selected_option"] == "REV-T344-E"
    assert target["implementation_allowed"] is False
    assert target["output_change_authorized"] is False
    assert target["reviewed_gold_promoted"] is False


def test_t343_decision_register_records_metadata_lesson() -> None:
    register = read(REGISTER)

    assert "CD-015" in register
    assert "Source metadata is evidence, not authority for chunking" in register
    assert "automatic_strongs_lexical_authority" in register
    assert "automatic_cross_reference_edge" in register
    assert "CD-025" in register
    assert "Source-metadata research atlas is evidence-only review memory" in register
    assert "CD-026" in register
    assert "Apocalyptic and prophetic intertext dossiers preserve hermeneutic options" in register
    assert "CD-032" in register
    assert "Textual-variant/source-tradition dossiers preserve canon-boundary neutrality" in register
