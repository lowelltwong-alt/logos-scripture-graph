"""Tests for T417 batch2 draft review packet validator."""
from __future__ import annotations

from pathlib import Path

from scripts.validate_t417_batch2_review_packet_drafts import DRAFTS, validate_drafts

ROOT = Path(__file__).resolve().parent.parent


def test_batch2_drafts_validate_clean() -> None:
    assert validate_drafts() == []


def test_all_six_draft_files_exist() -> None:
    assert len(DRAFTS) == 6
    for path in DRAFTS.values():
        assert path.is_file()
