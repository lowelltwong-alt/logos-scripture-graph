from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "eval" / "chunking_gold" / "review_packets"

PENDING_PACKETS = {
    "isa52_13_53_12_boundary_review.md": "isa52_13_53_12_servant_song",
    "mark16_9_20_textual_variant_review.md": "mark16_9_20_longer_ending",
    "john7_53_8_11_textual_variant_review.md": "john7_53_8_11_pericope_adulterae",
    "john3_wj_speaker_boundary_review.md": "john3_wj_speaker_boundary",
    "matt5_7_wj_discourse_review.md": "matt5_7_sermon_on_mount_wj_discourse",
    "ps136_boundary_review.md": "ps136_refrain_litany",
    "rev12_14_symbolic_scenes_review.md": "rev12_18_vision_cycle",
    "eph1_3_14_argument_review.md": "eph1_3_14_greek_sentence",
    "rom9_11_argument_review.md": "rom9_11_argument",
    "heb7_10_priesthood_argument_review.md": "heb7_10_priesthood_argument",
    "1cor8_10_food_offered_to_idols_review.md": "1cor8_10_food_offered_to_idols",
}

REVIEWED_WHOLE_PSALM_PACKETS = {
    "ps105_boundary_review.md": "ps105_historical_psalm",
    "ps106_boundary_review.md": "ps106_historical_confession",
}

REVIEWED_STRUCTURAL_PACKETS = {
    "ps89_boundary_review.md": "ps89_royal_lament",
}


def test_pending_review_packets_exist_and_stay_pending() -> None:
    for filename, case_id in PENDING_PACKETS.items():
        text = (PACKET_DIR / filename).read_text(encoding="utf-8")
        assert "Status: `pending_human_review`" in text, filename
        assert f"Stress atlas case ID: `{case_id}`" in text, filename
        assert "Decision: pending" in text, filename
        assert "This packet does not authorize output-changing work." in text, filename


def test_pending_review_packets_do_not_claim_reviewed_gold() -> None:
    forbidden = {
        "Status: `reviewed_gold`",
        "approved_structural_split_under_parent_whole_psalm",
        "authorizes_output_change",
        "implementation_allowed: true",
        "output_change_authorized: true",
        "reviewed_gold_promoted: true",
    }
    for filename in PENDING_PACKETS:
        text = (PACKET_DIR / filename).read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text, f"{filename} contains forbidden phrase {phrase}"


def test_t317_psalm_packets_record_reviewed_whole_psalm_gold() -> None:
    for filename, case_id in REVIEWED_WHOLE_PSALM_PACKETS.items():
        text = (PACKET_DIR / filename).read_text(encoding="utf-8")
        assert "Status: `reviewed_gold`" in text, filename
        assert f"Stress atlas case ID: `{case_id}`" in text, filename
        assert "Decision: approved_preserve_current_whole_psalm" in text, filename
        assert "This reviewed decision does not authorize output-changing work." in text, filename
        assert "Decision: pending" not in text, filename


def test_t337b_ps89_packet_records_owner_authorized_structural_gold() -> None:
    for filename, case_id in REVIEWED_STRUCTURAL_PACKETS.items():
        text = (PACKET_DIR / filename).read_text(encoding="utf-8")
        assert "Status: `approved_structural_split_under_parent_whole_psalm`" in text, filename
        assert f"Stress atlas case ID: `{case_id}`" in text, filename
        assert "Decision: approved_with_scope_note" in text, filename
        assert "implementation_allowed: true" in text, filename
        assert "output_change_authorized: true" in text, filename
        assert "reviewed_gold_promoted: true" in text, filename
        assert "T338 has not started" in text, filename


def test_t317_words_of_jesus_packets_preserve_marker_governance() -> None:
    for filename in {
        "john3_wj_speaker_boundary_review.md",
        "matt5_7_wj_discourse_review.md",
    }:
        text = (PACKET_DIR / filename).read_text(encoding="utf-8")
        assert "\\wj is evidence, not authority" in text, filename
        assert "speaker attribution requires human review" in text.lower(), filename
        assert "This packet does not authorize output-changing work." in text, filename
