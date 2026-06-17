from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_epistle_argument_review_packets import PACKETS, validate_epistle_packets


ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "eval" / "chunking_gold" / "review_packets"
INDEX = PACKET_DIR / "review_packet_index.json"
OBSERVED = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "observed_stress_behavior.json"
TASK = ROOT / ".ai" / "tasks" / "T352.task.yaml"
ROADMAP = ROOT / "docs" / "roadmap" / "T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_t352_validator_passes_current_repo() -> None:
    validate_epistle_packets()


def test_t352_packets_are_pending_and_non_authorizing() -> None:
    for case_id, spec in PACKETS.items():
        text = (PACKET_DIR / spec["packet"]).read_text(encoding="utf-8")
        assert "Status: `pending_human_review`" in text
        assert f"Stress atlas case ID: `{case_id}`" in text
        assert "Implementation allowed: false" in text
        assert "Output change authorized: false" in text
        assert "Reviewed gold promoted: false" in text
        assert "This packet does not authorize output-changing work." in text
        assert "No option above is approved. No reviewed gold is promoted." in text


def test_t352_index_entries_are_pending_review_packets() -> None:
    index = load_json(INDEX)
    entries = {entry["entry_id"]: entry for entry in index["entries"]}

    assert index["summary"]["total_entries"] == 68
    assert index["summary"]["pending_human_review"] == 23
    assert index["summary"]["needs_review_packet"] == 19
    assert index["summary"]["review_packet_files_indexed"] == 15
    for spec in PACKETS.values():
        entry = entries[spec["entry_id"]]
        assert entry["entry_type"] == "review_packet"
        assert entry["status"] == "pending_human_review"
        assert entry["decision"] == "pending"
        assert entry["human_review_required"] is True
        assert entry["implementation_allowed"] is False
        assert entry["output_change_authorized"] is False
        assert "pending_packets_non_authorizing" in entry["applicable_rules"]


def test_t352_observed_entries_now_point_to_packets() -> None:
    observed = load_json(OBSERVED)
    entries = {entry["case_id"]: entry for entry in observed["entries"]}

    assert observed["summary"]["needs_review_packet"] == 19
    assert observed["summary"]["review_packet_pending"] == 12
    for case_id, spec in PACKETS.items():
        entry = entries[case_id]
        assert entry["observed_status"] == "review_packet_pending"
        assert entry["review_packet_exists"] is True
        assert entry["review_packet"] == spec["packet"]
        assert entry["review_status"] == "pending_human_review"
        assert entry["recommended_next_step"] == "await_human_review"
        assert entry["implementation_allowed"] is False


def test_t352_task_and_roadmap_record_non_authorization() -> None:
    task = TASK.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")

    assert "id: T352" in task
    assert "epistle_review_packets_allowed: true" in task
    assert "output_change_authorized: false" in task
    assert "implementation_authorized: false" in task
    assert "reviewed_gold_promoted: false" in task
    assert "T352 does not authorize" in roadmap
    assert "No option above is approved" not in roadmap

