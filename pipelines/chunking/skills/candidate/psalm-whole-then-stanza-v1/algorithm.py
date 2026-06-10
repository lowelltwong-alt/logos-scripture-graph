"""Candidate Psalm skill seam for literal Book of Psalms routing.

This module keeps literal Psalms isolated behind the candidate skill boundary.
It delegates to the current monolith Psalm behavior, then applies only the
owner-reviewed Psalm 89 Option C target authorized by T337B.
"""
from __future__ import annotations

from typing import Any

from pipelines.chunking import chunker

SKILL_ID = "psalm-whole-then-stanza-v1"
TARGET_BOOK = "Ps"
PS89_CASE_ID = "ps89_owner_decision_option_c"
PS89_PARENT_SPAN = ("Ps.89.1", "Ps.89.52")
PS89_APPROVED_CHILD_SPANS = [
    ("Ps.89.1", "Ps.89.4"),
    ("Ps.89.5", "Ps.89.18"),
    ("Ps.89.19", "Ps.89.37"),
    ("Ps.89.38", "Ps.89.45"),
    ("Ps.89.46", "Ps.89.48"),
    ("Ps.89.49", "Ps.89.52"),
]
PS89_REQUIRED_REFS = {f"Ps.89.{verse}" for verse in range(1, 53)}

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
    PS89_CASE_ID: PS89_APPROVED_CHILD_SPANS,
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

REVIEWED_PSALM_REQUIRED_REFS: dict[str, set[str]] = {
    PS89_CASE_ID: PS89_REQUIRED_REFS,
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
        required_refs = REVIEWED_PSALM_REQUIRED_REFS.get(case_id, expected_endpoints)
        if not required_refs <= input_osis_refs:
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


def _ref_range(units_by_ref: dict[str, dict[str, Any]], start: str, end: str) -> list[dict[str, Any]]:
    book, chapter, first_verse = start.split(".")
    end_book, end_chapter, last_verse = end.split(".")
    if (book, chapter) != (end_book, end_chapter):
        raise ValueError(f"{SKILL_ID} Psalm 89 split cannot cross chapters: {start}-{end}")
    span_units = [
        units_by_ref[f"{book}.{chapter}.{verse}"]
        for verse in range(int(first_verse), int(last_verse) + 1)
    ]
    return span_units


def _chunk_index(chunk: dict[str, Any]) -> int:
    raw_id = str(chunk.get("id", ""))
    suffix = raw_id.rsplit("--", 1)[-1]
    try:
        return int(suffix)
    except ValueError:
        return 0


def _make_ps89_child_chunk(
    *,
    units: list[dict[str, Any]],
    genre: str,
    policy_version: str,
    index: int,
    child_number: int,
    footnotes_by_osis: dict[str, list],
    crossrefs_by_osis: dict[str, list],
) -> dict[str, Any]:
    basis = {"reviewed_structural_split", "whole_psalm_split"}
    if units[-1]["osis_ref"] == "Ps.89.52":
        basis.add("book_iii_doxology_scope_note")
    child = chunker.make_chunk(
        units,
        genre,
        basis,
        policy_version,
        index,
        footnotes_by_osis,
        crossrefs_by_osis,
    )
    child["id"] = f"{child['id']}-ps89-child-{child_number:02d}"
    child["boundary_basis"] = [
        "reviewed_structural_split",
        "whole_psalm_split",
    ]
    if units[-1]["osis_ref"] == "Ps.89.52":
        child["boundary_basis"].append("book_iii_doxology_scope_note")
    return child


def _apply_ps89_owner_option_c(
    chunks: list[dict[str, Any]],
    units: list[dict[str, Any]],
    genre: str,
    policy_version: str,
    footnotes_by_osis: dict[str, list],
    crossrefs_by_osis: dict[str, list],
    input_osis_refs: set[str],
) -> list[dict[str, Any]]:
    """Apply the owner-approved Psalm 89 Option C split, and nothing else."""
    if not PS89_REQUIRED_REFS <= input_osis_refs:
        return chunks

    ps89_chunks = _chunks_touching_chapters(chunks, {"89"})
    observed_spans = [
        (str(chunk.get("osis_start", "")), str(chunk.get("osis_end", "")))
        for chunk in ps89_chunks
    ]
    if observed_spans == PS89_APPROVED_CHILD_SPANS:
        return chunks
    if observed_spans != [PS89_PARENT_SPAN]:
        raise ValueError(
            f"{SKILL_ID} cannot apply {PS89_CASE_ID}: expected delegated Psalm 89 "
            f"parent {PS89_PARENT_SPAN}, observed {observed_spans}"
        )

    units_by_ref = {str(unit.get("osis_ref", "")): unit for unit in units}
    missing = sorted(PS89_REQUIRED_REFS - set(units_by_ref))
    if missing:
        raise ValueError(f"{SKILL_ID} missing Psalm 89 units for reviewed split: {missing}")

    parent_chunk = ps89_chunks[0]
    parent_index = _chunk_index(parent_chunk)
    children = [
        _make_ps89_child_chunk(
            units=_ref_range(units_by_ref, start, end),
            genre=genre,
            policy_version=policy_version,
            index=parent_index,
            child_number=child_number,
            footnotes_by_osis=footnotes_by_osis,
            crossrefs_by_osis=crossrefs_by_osis,
        )
        for child_number, (start, end) in enumerate(PS89_APPROVED_CHILD_SPANS, start=1)
    ]

    replaced: list[dict[str, Any]] = []
    inserted = False
    for chunk in chunks:
        if (chunk.get("osis_start"), chunk.get("osis_end")) == PS89_PARENT_SPAN:
            replaced.extend(children)
            inserted = True
        else:
            replaced.append(chunk)
    if not inserted:
        raise ValueError(f"{SKILL_ID} could not find delegated Psalm 89 parent chunk")
    return replaced


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
    chunks = _apply_ps89_owner_option_c(
        chunks,
        units,
        genre,
        policy_version,
        footnotes_by_osis,
        crossrefs_by_osis,
        input_osis_refs,
    )
    _validate_reviewed_psalm_gold(chunks, input_osis_refs)
    return chunks, next_index
