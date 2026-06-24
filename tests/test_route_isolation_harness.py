from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.chunking.route_isolation_harness import RouteIsolationError, compare_chunk_jsonl


TARGET = "Eph.1.3-Eph.1.14"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def chunk(chunk_id: str, start: str, end: str, text: str = "same") -> dict:
    return {"id": chunk_id, "osis_start": start, "osis_end": end, "text": text}


def test_exact_parent_overlay_preserves_non_target_bytes(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.jsonl"
    candidate = tmp_path / "candidate.jsonl"
    rows = [
        chunk("a", "Eph.1.1", "Eph.1.2"),
        chunk("b", "Eph.1.15", "Eph.1.23"),
    ]
    write_jsonl(baseline, rows)
    write_jsonl(candidate, [rows[0], chunk("target-parent", "Eph.1.3", "Eph.1.14"), rows[1]])

    report = compare_chunk_jsonl(baseline, candidate, target_span=TARGET)

    assert report.non_target_byte_identical is True
    assert report.added_keys == ["target-parent"]
    assert report.changed_spans == [TARGET]


def test_non_target_change_fails(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.jsonl"
    candidate = tmp_path / "candidate.jsonl"
    write_jsonl(baseline, [chunk("a", "Eph.1.1", "Eph.1.2")])
    write_jsonl(candidate, [chunk("a", "Eph.1.1", "Eph.1.2", text="changed")])

    with pytest.raises(RouteIsolationError, match="unauthorized span"):
        compare_chunk_jsonl(baseline, candidate, target_span=TARGET)


def test_adjacent_spillover_fails(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.jsonl"
    candidate = tmp_path / "candidate.jsonl"
    write_jsonl(baseline, [chunk("a", "Eph.1.1", "Eph.1.2")])
    write_jsonl(candidate, [chunk("a", "Eph.1.1", "Eph.1.2"), chunk("spill", "Eph.1.3", "Eph.1.15")])

    with pytest.raises(RouteIsolationError, match="unauthorized span"):
        compare_chunk_jsonl(baseline, candidate, target_span=TARGET)


def test_child_subspan_fails_when_child_spans_not_authorized(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.jsonl"
    candidate = tmp_path / "candidate.jsonl"
    write_jsonl(baseline, [chunk("a", "Eph.1.1", "Eph.1.2")])
    write_jsonl(candidate, [chunk("a", "Eph.1.1", "Eph.1.2"), chunk("child", "Eph.1.3", "Eph.1.6")])

    with pytest.raises(RouteIsolationError, match="unauthorized span"):
        compare_chunk_jsonl(baseline, candidate, target_span=TARGET)


def test_child_payload_fails_even_on_parent_span_without_authorization(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.jsonl"
    candidate = tmp_path / "candidate.jsonl"
    write_jsonl(baseline, [chunk("a", "Eph.1.1", "Eph.1.2")])
    parent = chunk("target-parent", "Eph.1.3", "Eph.1.14")
    parent["selected_children"] = [{"osis_start": "Eph.1.3", "osis_end": "Eph.1.6"}]
    write_jsonl(candidate, [chunk("a", "Eph.1.1", "Eph.1.2"), parent])

    with pytest.raises(RouteIsolationError, match="child-span payload"):
        compare_chunk_jsonl(baseline, candidate, target_span=TARGET)
