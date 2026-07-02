"""Tests for T417 draft review packet validator."""
from __future__ import annotations

from pathlib import Path

from scripts.validate_t417_batch2_review_packet_drafts import (
    _check_non_authorizing_text,
    _discover_drafts,
    validate_drafts,
)


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


def test_contradictory_true_markers_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad_draft.md"
    text = "Implementation allowed: false\nImplementation allowed: true\n"
    errors: list[str] = []
    _check_non_authorizing_text(path, text, errors)
    assert any("contradictory authority marker" in err for err in errors)
