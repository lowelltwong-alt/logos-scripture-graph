"""Focused tests for the candidate Psalm skill guardrail."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
ALGORITHM = ROOT / "pipelines" / "chunking" / "skills" / "candidate" / \
    "psalm-whole-then-stanza-v1" / "algorithm.py"
METADATA = ALGORITHM.with_name("SKILL_METADATA.json")


@pytest.fixture()
def psalm_skill() -> ModuleType:
    spec = importlib.util.spec_from_file_location("psalm_candidate_algorithm", ALGORITHM)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _chunk(start: str, end: str) -> dict:
    return {
        "type": "RetrievalChunk",
        "id": f"chunk:{start}-{end}",
        "osis_start": start,
        "osis_end": end,
        "genre": "psalms",
        "boundary_basis": ["whole_psalm"],
        "text": "Psalm text.",
    }


def _unit(book: str = "Ps", osis_ref: str | None = None) -> dict:
    return {"book": book, "osis_ref": osis_ref or f"{book}.1.1"}


def _units_for_reviewed_cases(module: ModuleType, *case_ids: str) -> list[dict]:
    refs: list[str] = []
    for case_id in case_ids:
        for start, end in module.REVIEWED_PSALM_CHAPTER_SPANS[case_id]:
            refs.extend([start, end])
    return [_unit(osis_ref=ref) for ref in dict.fromkeys(refs)]


def _call_skill(module: ModuleType, chunks: list[dict], units: list[dict] | None = None):
    def fake_chunk_book(*args, **kwargs):
        return chunks, 100 + len(chunks)

    module.chunker.chunk_book = fake_chunk_book
    return module.chunk_psalm_book(
        units or [_unit()],
        "psalms",
        {},
        "test-policy",
        {},
        {},
        100,
    )


def test_delegated_reviewed_psalm_gold_passes_unchanged(psalm_skill: ModuleType) -> None:
    chunks = [
        _chunk("Ps.23.1", "Ps.23.6"),
        _chunk("Ps.78.1", "Ps.78.69"),
        _chunk("Ps.78.70", "Ps.78.71"),
        _chunk("Ps.78.72", "Ps.78.72"),
        _chunk("Ps.105.1", "Ps.105.45"),
        _chunk("Ps.106.1", "Ps.106.48"),
    ]

    units = _units_for_reviewed_cases(
        psalm_skill,
        "ps23_whole_psalm",
        "ps78_parent_child_structural_split",
        "ps105_whole_psalm",
        "ps106_whole_psalm_with_b_marker_note",
    )

    returned_chunks, next_index = _call_skill(psalm_skill, chunks, units=units)

    assert returned_chunks == chunks
    assert next_index == 100 + len(chunks)


def test_partial_unreviewed_psalm_input_is_not_forced_into_gold_case(psalm_skill: ModuleType) -> None:
    chunks = [_chunk("Ps.2.1", "Ps.2.12")]

    returned_chunks, next_index = _call_skill(psalm_skill, chunks)

    assert returned_chunks == chunks
    assert next_index == 101


def test_reviewed_ps78_split_fails_closed_if_merged(psalm_skill: ModuleType) -> None:
    chunks = [_chunk("Ps.78.1", "Ps.78.72")]
    units = _units_for_reviewed_cases(psalm_skill, "ps78_parent_child_structural_split")

    with pytest.raises(ValueError, match="ps78_parent_child_structural_split"):
        _call_skill(psalm_skill, chunks, units=units)


def test_reviewed_ps106_whole_psalm_fails_closed_if_split(psalm_skill: ModuleType) -> None:
    chunks = [
        _chunk("Ps.106.1", "Ps.106.5"),
        _chunk("Ps.106.6", "Ps.106.48"),
    ]
    units = _units_for_reviewed_cases(psalm_skill, "ps106_whole_psalm_with_b_marker_note")

    with pytest.raises(ValueError, match="ps106_whole_psalm_with_b_marker_note"):
        _call_skill(psalm_skill, chunks, units=units)


def test_reviewed_ps119_sections_fail_closed_if_shifted(psalm_skill: ModuleType) -> None:
    chunks = [
        _chunk("Ps.119.1", "Ps.119.8"),
        _chunk("Ps.119.9", "Ps.119.176"),
    ]
    units = _units_for_reviewed_cases(psalm_skill, "ps119_acrostic_sections")

    with pytest.raises(ValueError, match="ps119_acrostic_sections"):
        _call_skill(psalm_skill, chunks, units=units)


def test_literal_psalm_skill_rejects_non_psalm_units(psalm_skill: ModuleType) -> None:
    with pytest.raises(ValueError, match="only handles book == 'Ps'"):
        _call_skill(psalm_skill, [], units=[_unit("Song")])


def test_skill_delegates_to_monolith_with_same_arguments(psalm_skill: ModuleType) -> None:
    units = [_unit(osis_ref="Ps.2.1")]
    budgets = {"soft_max_tokens": 1100}
    footnotes_by_osis = {"Ps.2.1": [{"id": "fn"}]}
    crossrefs_by_osis = {"Ps.2.1": [{"id": "xref"}]}
    chunks = [_chunk("Ps.2.1", "Ps.2.12")]
    captured = {}

    def fake_chunk_book(*args):
        captured["args"] = args
        return chunks, 42

    psalm_skill.chunker.chunk_book = fake_chunk_book

    returned_chunks, next_index = psalm_skill.chunk_psalm_book(
        units,
        "psalms",
        budgets,
        "policy-v-test",
        footnotes_by_osis,
        crossrefs_by_osis,
        41,
    )

    assert returned_chunks == chunks
    assert next_index == 42
    assert captured["args"] == (
        units,
        "psalms",
        budgets,
        "policy-v-test",
        footnotes_by_osis,
        crossrefs_by_osis,
        41,
    )


def test_reviewed_guardrail_scope_stays_literal_psalms_only(psalm_skill: ModuleType) -> None:
    refs = {
        ref
        for spans in psalm_skill.REVIEWED_PSALM_CHAPTER_SPANS.values()
        for span in spans
        for ref in span
    }

    assert refs
    assert all(ref.startswith("Ps.") for ref in refs)
    assert all(not ref.startswith(("PrMan.", "Ps151.")) for ref in refs)


def test_skill_metadata_cites_reviewed_psalm_evidence_only() -> None:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    refs = metadata["parameters"]["reviewed_gold_refs"]

    assert refs == [
        "eval/chunking_gold/per_form/psalms_gold_manifest.json",
        "eval/chunking_gold/review_packets/ps78_boundary_review.md",
        "eval/chunking_gold/review_packets/ps105_boundary_review.md",
        "eval/chunking_gold/review_packets/ps106_boundary_review.md",
    ]
    assert metadata["handles_books"] == ["Ps"]
    assert metadata["excluded_books"] == ["Song", "Lam"]
    assert metadata["eval"]["quality_improvement_claimed"] is False
