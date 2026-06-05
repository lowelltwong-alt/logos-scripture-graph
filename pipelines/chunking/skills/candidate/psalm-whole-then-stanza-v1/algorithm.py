"""Candidate Psalm skill seam for T310 Increment 3a.

This module intentionally delegates to the current monolith Psalm behavior. It
exists so the orchestrator can route literal Psalms through a skill boundary
without changing chunk bytes.
"""
from __future__ import annotations

from typing import Any

from pipelines.chunking import chunker

SKILL_ID = "psalm-whole-then-stanza-v1"
TARGET_BOOK = "Ps"


def chunk_psalm_book(
    units: list[dict[str, Any]],
    genre: str,
    budgets: dict[str, int],
    policy_version: str,
    footnotes_by_osis: dict[str, list],
    crossrefs_by_osis: dict[str, list],
    start_index: int,
) -> tuple[list[dict[str, Any]], int]:
    """Chunk literal Psalms by delegating to the existing monolith implementation."""
    bad_books = sorted({unit.get("book") for unit in units if unit.get("book") != TARGET_BOOK})
    if bad_books:
        raise ValueError(f"{SKILL_ID} only handles book == {TARGET_BOOK!r}; got {bad_books}")
    return chunker.chunk_book(
        units,
        genre,
        budgets,
        policy_version,
        footnotes_by_osis,
        crossrefs_by_osis,
        start_index,
    )
