"""Tests for whole-Bible multi-model chunking fork validator."""
from __future__ import annotations

from scripts.validate_multi_model_whole_bible_chunking_fork import validate


def test_fork_scaffold_validates() -> None:
    assert validate() == []
