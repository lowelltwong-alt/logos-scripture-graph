from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "chunking_stress_cases.json"
OBSERVED = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "observed_stress_behavior.json"
OBSERVED_MD = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "OBSERVED_STRESS_BEHAVIOR.md"

ALLOWED_OBSERVED_STATUSES = {
    "acceptable_current_behavior",
    "needs_review_packet",
    "review_packet_pending",
    "reviewed_gold_preserves_current_behavior",
    "variant_policy_required",
    "speaker_review_required",
    "source_tradition_review_required",
    "unknown_needs_human_review",
}

ALLOWED_NEXT_STEPS = {
    "none_current_behavior_acceptable",
    "create_review_packet",
    "await_human_review",
    "consider_future_gold_after_review",
    "define_variant_policy_before_gold",
    "define_speaker_policy_before_gold",
    "define_source_tradition_policy_before_gold",
    "manual_investigation_required",
}

REQUIRED_ENTRY_FIELDS = {
    "case_id",
    "passage",
    "observed_status",
    "current_chunks_touching_case",
    "case_fully_contained_in_one_chunk",
    "case_split_across_chunks",
    "case_mixed_with_extra_context",
    "chunk_crosses_book_boundary",
    "textual_variant_zone",
    "speaker_marker_evidence_present",
    "marker_evidence",
    "review_packet_exists",
    "review_status",
    "recommended_next_step",
    "implementation_allowed",
    "notes",
}

REVIEWED_CURRENT_BEHAVIOR_CASES = {
    "ps105_historical_psalm",
    "ps106_historical_confession",
}

PENDING_REVIEW_CASES = {
    "isa52_13_53_12_servant_song",
    "mark16_9_20_longer_ending",
    "john7_53_8_11_pericope_adulterae",
    "john3_wj_speaker_boundary",
    "matt5_7_sermon_on_mount_wj_discourse",
    "john7_53_8_11_wj_variant_speech",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def atlas_case_ids() -> set[str]:
    return {case["case_id"] for case in load_json(ATLAS)["cases"]}


def observed_entries() -> list[dict]:
    return load_json(OBSERVED)["entries"]


def observed_by_id() -> dict[str, dict]:
    return {entry["case_id"]: entry for entry in observed_entries()}


def test_observed_behavior_root_is_diagnostic_only() -> None:
    data = load_json(OBSERVED)
    assert data["schema_version"] == "observed-stress-behavior.v0"
    assert data["audit_id"] == "T318-observed-stress-atlas-behavior"
    assert data["status"] == "diagnostic_observation_only"
    assert data["implementation_allowed"] is False
    assert data["current_chunker_output"]["committed"] is False
    assert data["current_chunker_output"]["chunk_output_changed"] is False
    assert data["baseline"]["leaderboard_run"] is False
    assert "not chunking improvement" in data["baseline"]["score_interpretation"]


def test_every_stress_case_has_observed_entry() -> None:
    atlas_ids = atlas_case_ids()
    observed_ids = set(observed_by_id())
    assert observed_ids == atlas_ids
    assert len(observed_ids) == load_json(OBSERVED)["summary"]["stress_cases_audited"]


def test_observed_entries_have_required_fields_and_non_authorizing_flags() -> None:
    for entry in observed_entries():
        assert REQUIRED_ENTRY_FIELDS <= set(entry), entry.get("case_id")
        assert entry["implementation_allowed"] is False, entry["case_id"]
        assert isinstance(entry["current_chunks_touching_case"], list), entry["case_id"]
        assert isinstance(entry["case_fully_contained_in_one_chunk"], bool), entry["case_id"]
        assert isinstance(entry["case_split_across_chunks"], bool), entry["case_id"]
        assert isinstance(entry["case_mixed_with_extra_context"], bool), entry["case_id"]
        assert isinstance(entry["chunk_crosses_book_boundary"], bool), entry["case_id"]
        assert isinstance(entry["textual_variant_zone"], bool), entry["case_id"]
        assert isinstance(entry["speaker_marker_evidence_present"], bool), entry["case_id"]
        assert isinstance(entry["marker_evidence"], dict), entry["case_id"]
        assert isinstance(entry["review_packet_exists"], bool), entry["case_id"]
        assert isinstance(entry["notes"], str) and entry["notes"], entry["case_id"]


def test_observed_statuses_and_next_steps_are_controlled() -> None:
    data = load_json(OBSERVED)
    assert set(data["allowed_observed_statuses"]) == ALLOWED_OBSERVED_STATUSES
    assert set(data["allowed_recommended_next_steps"]) == ALLOWED_NEXT_STEPS
    for entry in observed_entries():
        assert entry["observed_status"] in ALLOWED_OBSERVED_STATUSES, entry["case_id"]
        assert entry["recommended_next_step"] in ALLOWED_NEXT_STEPS, entry["case_id"]


def test_reviewed_gold_preservation_claims_are_supported_only_for_ps105_ps106() -> None:
    for entry in observed_entries():
        claims_reviewed_current = (
            entry["observed_status"] == "reviewed_gold_preserves_current_behavior"
            or entry["review_status"] == "reviewed_gold"
        )
        if claims_reviewed_current:
            assert entry["case_id"] in REVIEWED_CURRENT_BEHAVIOR_CASES
            assert entry["review_packet_exists"] is True
            assert entry["recommended_next_step"] == "none_current_behavior_acceptable"


def test_pending_review_entries_stay_pending_and_non_authorizing() -> None:
    entries = observed_by_id()
    for case_id in PENDING_REVIEW_CASES:
        entry = entries[case_id]
        assert entry["review_packet_exists"] is True
        assert entry["review_status"] == "pending_human_review"
        assert entry["observed_status"] == "review_packet_pending"
        assert entry["recommended_next_step"] == "await_human_review"
        assert entry["implementation_allowed"] is False


def test_marker_evidence_is_diagnostic_not_authority() -> None:
    entries = observed_by_id()
    for case_id in {
        "gospels_wj_marker_spans",
        "john3_wj_speaker_boundary",
        "matt5_7_sermon_on_mount_wj_discourse",
        "john13_17_wj_farewell_discourse_marker_focus",
        "synoptic_apocalyptic_wj_discourses",
        "john7_53_8_11_wj_variant_speech",
    }:
        marker_evidence = entries[case_id]["marker_evidence"]
        assert entries[case_id]["speaker_marker_evidence_present"] is True
        assert marker_evidence["wj_word_token_refs_count"] > 0
        assert entries[case_id]["implementation_allowed"] is False

    selah = entries["psalms_selah_qs_markers"]
    assert selah["marker_evidence"]["qs_refs_count"] > 0
    assert selah["implementation_allowed"] is False


def test_observed_behavior_contains_no_positive_authorization_language() -> None:
    serialized = json.dumps(load_json(OBSERVED), sort_keys=True).lower()
    markdown = OBSERVED_MD.read_text(encoding="utf-8").lower()
    forbidden_positive_phrases = {
        '"implementation_allowed": true',
        "implementation_allowed: true",
        "authorizes output-changing work",
        "approved for implementation",
        "may change chunk output",
        "this is a chunking improvement",
    }
    for phrase in forbidden_positive_phrases:
        assert phrase not in serialized
        assert phrase not in markdown
    assert "does not authorize output-changing work" in markdown
    assert "not chunking improvement" in markdown
