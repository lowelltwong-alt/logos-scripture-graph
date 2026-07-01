"""Tests for T417 draft review packet validator."""
from __future__ import annotations

from scripts.validate_t417_batch2_review_packet_drafts import _discover_drafts, validate_drafts


def test_drafts_validate_clean() -> None:
    assert validate_drafts() == []


def test_core_batch_draft_files_exist() -> None:
    drafts = _discover_drafts()
    for candidate_id in (
        "T402-LC-057",
        "T402-LC-065",
        "T402-LC-032",
        "T402-LC-048",
        "T402-LC-049",
        "T402-LC-050",
    ):
        assert candidate_id in drafts
