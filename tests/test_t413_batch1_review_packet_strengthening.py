from __future__ import annotations

import pytest

from scripts.validate_t413_batch1_review_packet_strengthening import PACKETS, validate_t413_batch1


def test_t413_batch1_strengthening_validates() -> None:
    validate_t413_batch1()


@pytest.mark.parametrize("candidate_id,span,path", PACKETS)
def test_t413_batch1_packets_pending(candidate_id: str, span: str, path) -> None:
    text = path.read_text(encoding="utf-8")
    assert candidate_id in text
    assert span in text
    assert "Status: `pending_human_review`" in text
    assert "Reviewed gold promoted: false" in text
