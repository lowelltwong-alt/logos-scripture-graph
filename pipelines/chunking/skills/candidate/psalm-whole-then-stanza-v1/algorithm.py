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

REVIEWED_PSALM_CHAPTER_SPANS: dict[str, list[tuple[str, str]]] = {
    "ps1_short_whole_psalm": [("Ps.1.1", "Ps.1.6")],
    "ps3_superscription_attached": [("Ps.3.1", "Ps.3.8")],
    "ps8_short_whole_psalm": [("Ps.8.1", "Ps.8.9")],
    "ps23_whole_psalm": [("Ps.23.1", "Ps.23.6")],
    "ps78_parent_child_structural_split": [
        ("Ps.78.1", "Ps.78.69"),
        ("Ps.78.70", "Ps.78.71"),
        ("Ps.78.72", "Ps.78.72"),
    ],
    "ps100_short_whole_psalm": [("Ps.100.1", "Ps.100.5")],
    "ps105_whole_psalm": [("Ps.105.1", "Ps.105.45")],
    "ps106_whole_psalm_with_b_marker_note": [("Ps.106.1", "Ps.106.48")],
    "ps117_short_whole_psalm": [("Ps.117.1", "Ps.117.2")],
    "ps119_acrostic_sections": [
        ("Ps.119.1", "Ps.119.7"),
        ("Ps.119.8", "Ps.119.15"),
        ("Ps.119.16", "Ps.119.23"),
        ("Ps.119.24", "Ps.119.31"),
        ("Ps.119.32", "Ps.119.39"),
        ("Ps.119.40", "Ps.119.47"),
        ("Ps.119.48", "Ps.119.55"),
        ("Ps.119.56", "Ps.119.63"),
        ("Ps.119.64", "Ps.119.71"),
        ("Ps.119.72", "Ps.119.79"),
        ("Ps.119.80", "Ps.119.87"),
        ("Ps.119.88", "Ps.119.95"),
        ("Ps.119.96", "Ps.119.103"),
        ("Ps.119.104", "Ps.119.111"),
        ("Ps.119.112", "Ps.119.119"),
        ("Ps.119.120", "Ps.119.127"),
        ("Ps.119.128", "Ps.119.135"),
        ("Ps.119.136", "Ps.119.143"),
        ("Ps.119.144", "Ps.119.151"),
        ("Ps.119.152", "Ps.119.159"),
        ("Ps.119.160", "Ps.119.167"),
        ("Ps.119.168", "Ps.119.176"),
    ],
}


def _chapter(ref: str) -> str | None:
    parts = ref.split(".")
    if len(parts) < 3 or parts[0] != TARGET_BOOK:
        return None
    return parts[1]


def _chunks_touching_chapters(chunks: list[dict[str, Any]], chapters: set[str]) -> list[dict[str, Any]]:
    matching: list[dict[str, Any]] = []
    for chunk in chunks:
        start_chapter = _chapter(str(chunk.get("osis_start", "")))
        end_chapter = _chapter(str(chunk.get("osis_end", "")))
        if start_chapter in chapters or end_chapter in chapters:
            matching.append(chunk)
    return matching


def _validate_reviewed_psalm_gold(chunks: list[dict[str, Any]], input_osis_refs: set[str]) -> None:
    """Fail closed when delegated Psalm output violates reviewed Psalm gold."""
    for case_id, expected_spans in REVIEWED_PSALM_CHAPTER_SPANS.items():
        expected_endpoints = {ref for span in expected_spans for ref in span}
        if not expected_endpoints <= input_osis_refs:
            continue
        expected_chapters = {
            chapter
            for span in expected_spans
            for chapter in (_chapter(span[0]), _chapter(span[1]))
            if chapter is not None
        }
        observed_chunks = _chunks_touching_chapters(chunks, expected_chapters)
        if not observed_chunks:
            continue
        observed_spans = [
            (str(chunk.get("osis_start", "")), str(chunk.get("osis_end", "")))
            for chunk in observed_chunks
        ]
        if observed_spans != expected_spans:
            raise ValueError(
                f"{SKILL_ID} delegated output violated reviewed Psalm gold "
                f"{case_id}: expected {expected_spans}, observed {observed_spans}"
            )


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
    input_osis_refs = {str(unit.get("osis_ref", "")) for unit in units}
    chunks, next_index = chunker.chunk_book(
        units,
        genre,
        budgets,
        policy_version,
        footnotes_by_osis,
        crossrefs_by_osis,
        start_index,
    )
    _validate_reviewed_psalm_gold(chunks, input_osis_refs)
    return chunks, next_index
