from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "eval" / "chunking_gold" / "review_packets"

EXPECTED_PACKETS = {
    "ps105_boundary_review.md": "ps105_historical_psalm",
    "ps106_boundary_review.md": "ps106_historical_confession",
    "isa52_13_53_12_boundary_review.md": "isa52_13_53_12_servant_song",
    "mark16_9_20_textual_variant_review.md": "mark16_9_20_longer_ending",
    "john7_53_8_11_textual_variant_review.md": "john7_53_8_11_pericope_adulterae",
}


def test_t316b_review_packets_exist_and_stay_pending() -> None:
    for filename, case_id in EXPECTED_PACKETS.items():
        text = (PACKET_DIR / filename).read_text(encoding="utf-8")
        assert "Status: `pending_human_review`" in text, filename
        assert f"Stress atlas case ID: `{case_id}`" in text, filename
        assert "Decision: pending" in text, filename
        assert "This packet does not authorize output-changing work." in text, filename


def test_t316b_review_packets_do_not_claim_reviewed_gold() -> None:
    forbidden = {
        "reviewed_gold",
        "approved_structural_split_under_parent_whole_psalm",
        "authorizes_output_change",
        "implementation_allowed: true",
    }
    for filename in EXPECTED_PACKETS:
        text = (PACKET_DIR / filename).read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in forbidden:
            assert phrase not in lowered, f"{filename} contains forbidden phrase {phrase}"

