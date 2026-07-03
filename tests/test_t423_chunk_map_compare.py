"""Tests for T423 chunk map utils, validation, and comparison."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.compare_multi_model_bible_chunk_maps import compare_models
from scripts.t423_chunk_map_utils import (
    agreement_tier,
    majority_required,
    normalize_span,
    parse_span,
)
from scripts.validate_whole_bible_chunk_map import validate_chunk_map


def _chunk(model_id: str, book: str, idx: int, span: str, **extra: object) -> dict:
    base = {
        "model_id": model_id,
        "book": book,
        "span": span,
        "chunk_index_in_book": idx,
        "literature_type_guess": "narrative",
        "boundary_evidence_refs": ["observation_substrate"],
        "strong_or_hebrew_tags_used": False,
        "wj_or_red_letter_considered": False,
        "confidence": "medium",
        "decision_id": f"{model_id}-{book}-{idx:03d}",
        "non_authorizing": True,
    }
    base.update(extra)
    return base


def _write_map(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def _write_manifest(folder: Path, model_id: str, *, books: list[str] | None = None) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "model_manifest.yaml").write_text(
        yaml.safe_dump({"model_id": model_id, "research_baseline_read": True}),
        encoding="utf-8",
    )
    completion = {b: {"status": "complete"} for b in (books or ["Phlm", "Jude"])}
    (folder / "marathon_progress.yaml").write_text(
        yaml.safe_dump(
            {
                "model_id": model_id,
                "marathon_status": "complete",
                "books_completed": 66,
                "books_total": 66,
                "book_completion": completion,
            }
        ),
        encoding="utf-8",
    )


def test_majority_formula() -> None:
    assert majority_required(3) == 3
    assert majority_required(5) == 4
    assert majority_required(10) == 7
    assert agreement_tier(4, 5) == "easy_majority"
    assert agreement_tier(5, 5) == "full_consensus"
    assert agreement_tier(2, 5) is None


def test_normalize_span() -> None:
    assert normalize_span("Gen.1.1-Gen.1.31") == "Gen.1.1-Gen.1.31"
    assert normalize_span("Gen.1.1") == "Gen.1.1"


def test_parse_span_rejects_cross_book() -> None:
    with pytest.raises(ValueError):
        parse_span("Gen.1.1-Exod.1.1")


def test_validate_chunk_map_ok(tmp_path: Path) -> None:
    path = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_map(
        path,
        [
            _chunk("M1", "Phlm", 1, "Phlm.1.1-Phlm.1.7"),
            _chunk("M1", "Phlm", 2, "Phlm.1.8-Phlm.1.25"),
        ],
    )
    assert validate_chunk_map(path, expected_model_id="M1") == []


def test_validate_chunk_map_overlap_error(tmp_path: Path) -> None:
    path = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_map(
        path,
        [
            _chunk("M1", "Phlm", 1, "Phlm.1.1-Phlm.1.10"),
            _chunk("M1", "Phlm", 2, "Phlm.1.8-Phlm.1.25"),
        ],
    )
    errors = validate_chunk_map(path)
    assert any("overlaps" in e for e in errors)


def test_compare_agreement_and_delta(tmp_path: Path) -> None:
    m1 = tmp_path / "M1_cursor"
    m2 = tmp_path / "M2_codex"
    _write_manifest(m1, "M1_cursor")
    _write_manifest(m2, "M2_codex")
    rows_m1 = [
        _chunk("M1_cursor", "Phlm", 1, "Phlm.1.1-Phlm.1.7"),
        _chunk("M1_cursor", "Phlm", 2, "Phlm.1.8-Phlm.1.25"),
        _chunk("M1_cursor", "Jude", 1, "Jude.1.1-Jude.1.2"),
    ]
    rows_m2 = [
        _chunk("M2_codex", "Phlm", 1, "Phlm.1.1-Phlm.1.3"),
        _chunk("M2_codex", "Phlm", 2, "Phlm.1.2-Phlm.1.25"),
        _chunk("M2_codex", "Jude", 1, "Jude.1.1-Jude.1.2"),
    ]
    _write_map(m1 / "whole_bible_chunk_map.jsonl", rows_m1)
    _write_map(m2 / "whole_bible_chunk_map.jsonl", rows_m2)

    result = compare_models([m1, m2], books=["Phlm", "Jude"], allow_easy_at_n3=True)
    assert result["overall_verse_coverage_agreement_rate"] > 0
    assert any(a["book"] == "Jude" for a in result["agreements"])
    assert any(d["book"] == "Phlm" for d in result["deltas"])


def test_compare_high_agreement_despite_chunk_count_mismatch(tmp_path: Path) -> None:
    """Same boundaries, different chunk counts — verse-coverage must not score 0%."""
    folders = []
    for i in range(1, 6):
        mid = f"M{i}_model"
        folder = tmp_path / mid
        _write_manifest(folder, mid, books=["Phlm"])
        if i == 2:
            rows = [_chunk(mid, "Phlm", 1, "Phlm.1.1-Phlm.1.25")]
        else:
            rows = [
                _chunk(mid, "Phlm", 1, "Phlm.1.1-Phlm.1.7"),
                _chunk(mid, "Phlm", 2, "Phlm.1.8-Phlm.1.25"),
            ]
        _write_map(folder / "whole_bible_chunk_map.jsonl", rows)
        folders.append(folder)

    result = compare_models(folders, books=["Phlm"], allow_easy_at_n3=False)
    assert result["overall_verse_coverage_agreement_rate"] >= 0.8
    assert not any(d.get("delta_kind") == "split_count_mismatch" for d in result["deltas"])


def test_compare_easy_majority_at_n5(tmp_path: Path) -> None:
    folders = []
    for i in range(1, 6):
        mid = f"M{i}_model"
        folder = tmp_path / mid
        _write_manifest(folder, mid, books=["Jude"])
        rows = [_chunk(mid, "Jude", 1, "Jude.1.1-Jude.1.2")]
        if i == 5:
            rows = [_chunk(mid, "Jude", 1, "Jude.1.1-Jude.1.1"), _chunk(mid, "Jude", 2, "Jude.1.2-Jude.1.2")]
        _write_map(folder / "whole_bible_chunk_map.jsonl", rows)
        folders.append(folder)

    result = compare_models(folders, books=["Jude"], allow_easy_at_n3=False)
    easy = [a for a in result["agreements"] if a.get("agreement_tier") == "easy_majority"]
    assert easy
    assert easy[0]["span"] == "Jude.1.1-Jude.1.2"


def test_compare_false_consensus_stress_book(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from scripts import compare_multi_model_bible_chunk_maps as cmp

    monkeypatch.setattr(cmp, "_load_stress_books", lambda: {"Rev"})

    m1 = tmp_path / "M1_cursor"
    m2 = tmp_path / "M2_codex"
    _write_manifest(m1, "M1_cursor", books=["Rev"])
    _write_manifest(m2, "M2_codex", books=["Rev"])
    rows = [_chunk("M1_cursor", "Rev", 1, "Rev.1.1-Rev.1.8"), _chunk("M1_cursor", "Rev", 2, "Rev.1.9-Rev.1.20")]
    rows2 = [_chunk("M2_codex", "Rev", 1, "Rev.1.1-Rev.1.8"), _chunk("M2_codex", "Rev", 2, "Rev.1.9-Rev.1.20")]
    _write_map(m1 / "whole_bible_chunk_map.jsonl", rows)
    _write_map(m2 / "whole_bible_chunk_map.jsonl", rows2)

    result = compare_models([m1, m2], books=["Rev"], allow_easy_at_n3=True)
    assert any(w["book"] == "Rev" for w in result["false_consensus_warnings"])
