from __future__ import annotations

from pathlib import Path

from pipelines.chunking.evaluate_chunks import score
from pipelines.chunking.leaderboard import eligible


def chunk(start: str, end: str, *, genre: str = "psalms", text: str = "A complete sentence.") -> dict:
    return {
        "osis_start": start,
        "osis_end": end,
        "genre": genre,
        "text": text,
        "validation": {"sentence_ended": text.endswith((".", "!", "?"))},
        "boundary_basis": ["test"],
        "has_lexeme_alignment": True,
    }


def hard_gate_baseline() -> list[dict]:
    return [
        chunk("Gen.1.1", "Gen.1.1", genre="narrative"),
        chunk("Ps.23.1", "Ps.23.6"),
    ]


def reviewed_ps78_split() -> list[dict]:
    return [
        chunk("Ps.78.1", "Ps.78.69"),
        chunk("Ps.78.70", "Ps.78.71"),
        chunk("Ps.78.72", "Ps.78.72"),
    ]


def test_psalm_song_lamentations_same_chapter_do_not_collide() -> None:
    metrics = score([
        chunk("Ps.3.1", "Ps.3.8"),
        chunk("Song.3.1", "Song.3.11"),
        chunk("Lam.3.1", "Lam.3.66"),
    ])

    assert metrics["psalms_fragmented"] == 0
    assert metrics["literal_psalms_fragmented"] == 0
    assert metrics["poetry_books_fragmented"] == 0


def test_same_book_chapter_multiple_chunks_still_counts_fragmented() -> None:
    metrics = score([
        chunk("Ps.78.1", "Ps.78.69"),
        chunk("Ps.78.70", "Ps.78.72"),
    ])

    assert metrics["literal_psalms_fragmented_raw"] == 1
    assert metrics["reviewed_structural_splits"] == []
    assert metrics["psalms_fragmented"] == 1
    assert metrics["literal_psalms_fragmented"] == 1
    assert metrics["poetry_books_fragmented"] == 1


def test_reviewed_psalm_78_structural_split_is_excluded_from_bad_fragmentation() -> None:
    metrics = score(reviewed_ps78_split())

    assert metrics["literal_psalms_fragmented_raw"] == 1
    assert metrics["literal_psalms_fragmented"] == 0
    assert metrics["psalms_fragmented"] == 0
    assert len(metrics["reviewed_structural_splits"]) == 1
    assert metrics["reviewed_structural_splits"][0]["case_id"] == "ps78_parent_child_structural_split"
    assert metrics["reviewed_structural_splits"][0]["osis_span"] == "Ps.78.1-Ps.78.72"


def test_reviewed_split_boundary_mismatch_does_not_exclude() -> None:
    metrics = score([
        chunk("Ps.78.1", "Ps.78.68"),
        chunk("Ps.78.69", "Ps.78.71"),
        chunk("Ps.78.72", "Ps.78.72"),
    ])

    assert metrics["literal_psalms_fragmented_raw"] == 1
    assert metrics["reviewed_structural_splits"] == []
    assert metrics["literal_psalms_fragmented"] == 1


def test_missing_or_malformed_manifest_falls_back_to_raw_counting(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not-json", encoding="utf-8")

    missing_metrics = score(reviewed_ps78_split(), psalms_gold_manifest=missing)
    malformed_metrics = score(reviewed_ps78_split(), psalms_gold_manifest=malformed)

    for metrics in (missing_metrics, malformed_metrics):
        assert metrics["literal_psalms_fragmented_raw"] == 1
        assert metrics["reviewed_structural_splits"] == []
        assert metrics["literal_psalms_fragmented"] == 1


def test_unreviewed_multi_chunk_literal_psalm_still_counts_fragmented() -> None:
    metrics = score([
        chunk("Ps.79.1", "Ps.79.6"),
        chunk("Ps.79.7", "Ps.79.13"),
    ])

    assert metrics["literal_psalms_fragmented_raw"] == 1
    assert metrics["reviewed_structural_splits"] == []
    assert metrics["literal_psalms_fragmented"] == 1


def test_psalm_119_intentional_sections_are_reported_not_penalized() -> None:
    metrics = score([
        chunk("Ps.119.1", "Ps.119.8"),
        chunk("Ps.119.9", "Ps.119.16"),
    ])

    assert metrics["psalm119_section_chunks"] == 2
    assert metrics["literal_psalms_fragmented_raw"] == 0
    assert metrics["reviewed_structural_splits"] == []
    assert metrics["psalms_fragmented"] == 0
    assert metrics["literal_psalms_fragmented"] == 0
    assert metrics["poetry_books_fragmented"] == 0


def test_psalm_23_one_chunk_hard_gate_still_works() -> None:
    good = score(hard_gate_baseline())
    assert good["gold_psalm23_one_chunk"] is True
    assert eligible(good) is True

    split_psalm_23 = score([
        chunk("Gen.1.1", "Gen.1.1", genre="narrative"),
        chunk("Ps.23.1", "Ps.23.3"),
        chunk("Ps.23.4", "Ps.23.6"),
    ])
    assert split_psalm_23["gold_psalm23_one_chunk"] is False
    assert eligible(split_psalm_23) is False


def test_existing_hard_gates_remain_intact() -> None:
    clean = score(hard_gate_baseline())
    assert clean["usfm_leaks"] == 0
    assert clean["book_crossings"] == 0
    assert clean["sentence_integrity_pct"] == 100.0
    assert clean["gold_psalm23_one_chunk"] is True
    assert clean["gold_gen1_no_midsentence"] is True
    assert eligible(clean) is True

    leak = score(hard_gate_baseline() + [chunk("John.1.1", "John.1.1", genre="gospels", text="Raw \\p leak.")])
    assert leak["usfm_leaks"] == 1
    assert eligible(leak) is False

    crossing = score(hard_gate_baseline() + [chunk("Gen.1.1", "Exod.1.1", genre="narrative")])
    assert crossing["book_crossings"] == 1
    assert eligible(crossing) is False

    mid_sentence = score([
        chunk("Gen.1.1", "Gen.1.1", genre="narrative", text="In the beginning"),
        chunk("Ps.23.1", "Ps.23.6"),
    ])
    assert mid_sentence["sentence_integrity_pct"] == 0.0
    assert mid_sentence["gold_gen1_no_midsentence"] is False
    assert eligible(mid_sentence) is False
