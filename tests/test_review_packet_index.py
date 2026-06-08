from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "eval" / "chunking_gold" / "review_packets"
INDEX = PACKET_DIR / "review_packet_index.json"
MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "psalms_gold_manifest.json"
OBSERVED = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "observed_stress_behavior.json"

REQUIRED_ENTRY_FIELDS = {
    "entry_id",
    "case_id",
    "passage",
    "source_path",
    "entry_type",
    "status",
    "decision",
    "human_review_required",
    "output_change_authorized",
    "implementation_allowed",
    "gold_manifest_case_id",
    "observed_status",
    "recommended_next_action",
    "risk_tags",
    "applicable_rules",
    "notes",
}

CONTROLLED_ENTRY_TYPES = {
    "reviewed_gold",
    "review_packet",
    "observed_audit_case",
    "policy_required",
    "manual_investigation_required",
}

CONTROLLED_STATUSES = {
    "reviewed_gold",
    "pending_human_review",
    "needs_review_packet",
    "variant_policy_required",
    "speaker_review_required",
    "source_tradition_review_required",
    "manual_investigation_required",
    "not_authorized",
}

SUPPORTED_REVIEWED_ENTRY_IDS = {
    "packet_ps78_boundary_review",
    "packet_ps105_boundary_review",
    "packet_ps106_boundary_review",
    "manifest_ps23_whole_psalm",
    "manifest_ps119_acrostic_sections",
    "manifest_short_psalm_holdouts",
    "manifest_ps3_superscription_attached",
    "manifest_non_target_poetry_controls",
    "manifest_ps78_parent_child_structural_split",
    "manifest_ps105_whole_psalm",
    "manifest_ps106_whole_psalm_with_b_marker_note",
    "observed_ps105_historical_psalm",
    "observed_ps106_historical_confession",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def index() -> dict:
    return load_json(INDEX)


def entries() -> list[dict]:
    return index()["entries"]


def entries_by_id() -> dict[str, dict]:
    return {entry["entry_id"]: entry for entry in entries()}


def test_review_packet_index_root_is_diagnostic_only() -> None:
    data = index()
    assert data["schema_version"] == "review-packet-index.v0"
    assert data["index_id"] == "T319-review-packet-index-promotion-queue"
    assert data["status"] == "diagnostic_control_surface"
    assert data["implementation_allowed"] is False
    assert data["output_change_authorized"] is False
    assert data["baseline"]["leaderboard_run"] is False
    assert "not chunking improvement" in data["baseline"]["score_interpretation"]
    assert set(data["controlled_entry_types"]) == CONTROLLED_ENTRY_TYPES
    assert set(data["controlled_statuses"]) == CONTROLLED_STATUSES


def test_entries_have_required_fields_and_controlled_values() -> None:
    seen_ids: set[str] = set()
    for entry in entries():
        assert REQUIRED_ENTRY_FIELDS <= set(entry), entry.get("entry_id")
        assert entry["entry_id"] not in seen_ids
        seen_ids.add(entry["entry_id"])
        assert entry["entry_type"] in CONTROLLED_ENTRY_TYPES, entry["entry_id"]
        assert entry["status"] in CONTROLLED_STATUSES, entry["entry_id"]
        assert entry["output_change_authorized"] is False, entry["entry_id"]
        assert entry["implementation_allowed"] is False, entry["entry_id"]
        assert "no_output_authorization" in entry["applicable_rules"], entry["entry_id"]
        assert "no_new_reviewed_gold_t319" in entry["applicable_rules"], entry["entry_id"]


def test_every_review_packet_file_is_indexed() -> None:
    packet_files = {
        f"eval/chunking_gold/review_packets/{path.name}"
        for path in PACKET_DIR.glob("*.md")
        if path.name != "REVIEW_PACKET_INDEX.md"
    }
    indexed_sources = {entry["source_path"] for entry in entries()}
    assert packet_files <= indexed_sources


def test_every_psalm_manifest_reviewed_case_is_indexed() -> None:
    manifest_cases = {
        case["case_id"]
        for case in load_json(MANIFEST)["reviewed_gold"]
    }
    indexed_manifest_cases = {
        entry["case_id"]
        for entry in entries()
        if entry["source_path"] == "eval/chunking_gold/per_form/psalms_gold_manifest.json"
    }
    assert manifest_cases == indexed_manifest_cases


def test_every_observed_audit_case_is_indexed_or_explicitly_excluded() -> None:
    observed_cases = {
        entry["case_id"]
        for entry in load_json(OBSERVED)["entries"]
    }
    indexed_observed_cases = {
        entry["case_id"]
        for entry in entries()
        if entry["source_path"] == "eval/chunking_gold/stress_atlas/observed_stress_behavior.json"
    }
    exclusions = set(index()["documented_exclusions"])
    assert observed_cases <= indexed_observed_cases | exclusions
    assert not exclusions


def test_reviewed_gold_entries_are_only_pre_t319_supported_cases() -> None:
    reviewed_ids = {
        entry["entry_id"]
        for entry in entries()
        if entry["status"] == "reviewed_gold"
    }
    assert reviewed_ids == SUPPORTED_REVIEWED_ENTRY_IDS
    for entry_id in reviewed_ids:
        entry = entries_by_id()[entry_id]
        assert entry["human_review_required"] is False
        assert entry["output_change_authorized"] is False
        assert entry["implementation_allowed"] is False


def test_pending_policy_and_manual_entries_fail_closed() -> None:
    for entry in entries():
        if entry["status"] == "reviewed_gold":
            continue
        assert entry["human_review_required"] is True, entry["entry_id"]
        assert entry["output_change_authorized"] is False, entry["entry_id"]
        assert entry["implementation_allowed"] is False, entry["entry_id"]
        assert entry["decision"] != "approved", entry["entry_id"]


def test_applicable_rules_cover_variant_speaker_source_and_pending_risks() -> None:
    for entry in entries():
        rules = set(entry["applicable_rules"])
        risk_tags = set(entry["risk_tags"])
        if entry["status"] == "pending_human_review":
            assert (
                "pending_packets_non_authorizing" in rules
                or "observed_audit_non_authorizing" in rules
            ), entry["entry_id"]
        if entry["status"] == "variant_policy_required" or "major_textual_variant" in risk_tags:
            assert "variant_policy_before_gold" in rules, entry["entry_id"]
        if entry["status"] == "speaker_review_required" or "speaker_boundary" in risk_tags:
            assert "speaker_review_required" in rules, entry["entry_id"]
        if entry["status"] == "source_tradition_review_required":
            assert "source_tradition_review_required" in rules, entry["entry_id"]
        if entry["status"] == "manual_investigation_required":
            assert "manual_investigation_required" in rules, entry["entry_id"]
        if "words_of_jesus" in risk_tags or entry["case_id"].find("_wj_") != -1:
            assert "wj_evidence_not_authority" in rules, entry["entry_id"]


def test_textual_variant_entries_are_not_reviewed_gold() -> None:
    for entry in entries():
        if "major_textual_variant" in entry["risk_tags"]:
            assert entry["status"] != "reviewed_gold", entry["entry_id"]


def test_promotion_queue_is_non_authorizing() -> None:
    queue = index()["promotion_queue"]
    assert queue
    for item in queue:
        assert item["output_change_authorized"] is False
        assert item["implementation_allowed"] is False
        assert item["status"] != "reviewed_gold"


def test_pending_entries_contain_no_positive_authorization_language() -> None:
    forbidden_positive_phrases = {
        '"output_change_authorized": true',
        '"implementation_allowed": true',
        "authorizes output-changing work",
        "approved for implementation",
        "may change chunk output",
        "this is a chunking improvement",
    }
    for entry in entries():
        if entry["status"] == "reviewed_gold":
            continue
        serialized = json.dumps(entry, sort_keys=True).lower()
        for phrase in forbidden_positive_phrases:
            assert phrase not in serialized, f"{entry['entry_id']} contains {phrase}"
