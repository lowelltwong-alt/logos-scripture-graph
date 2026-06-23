from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_t392_eph1_review_packet_strengthening import (
    PACKET,
    T392PacketError,
    validate_t392,
)


def test_t392_eph1_packet_strengthening_validates() -> None:
    validate_t392(PACKET)


def test_t392_packet_remains_pending_and_non_authorizing() -> None:
    text = PACKET.read_text(encoding="utf-8")

    assert "Status: `pending_human_review`" in text
    assert "Decision: pending" in text
    assert "Implementation allowed: false" in text
    assert "Output change authorized: false" in text
    assert "Reviewed gold promoted: false" in text
    assert "T392 strengthened packet: true" in text
    assert "No option above is approved. No reviewed gold is promoted." in text
    assert "Child spans remain unauthorized" in text
    assert "graph/retrieval/vector truth" in text


def test_t392_packet_records_context_source_language_variant_and_premortem() -> None:
    text = PACKET.read_text(encoding="utf-8")

    for phrase in (
        "Contextual Reading Fields",
        "boundary-claim:79-EPHeng-web.usfm:25:p",
        "Source Metadata And Original-Language Notes",
        "Phrase-before-word rule",
        "Variant And Source-Tradition Flags",
        "TCP-T378-B",
        "Theological Risk Flags",
        "Premortem Red-Team Pass",
        "God` in `Eph.1.14` with",
        "`G1519`",
    ):
        assert phrase in text


def test_t392_validator_rejects_output_authority(tmp_path: Path) -> None:
    candidate = tmp_path / "eph1_3_14_argument_review.md"
    text = PACKET.read_text(encoding="utf-8").replace(
        "Output change authorized: false",
        "Output change authorized: true",
        1,
    )
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(T392PacketError, match="Output change authorized: false"):
        validate_t392(candidate)
