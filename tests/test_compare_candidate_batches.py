from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipelines.graph.compare_candidate_batches import compare_batches, materialize_outputs


def write_batch(path: Path, triples: list[tuple[str, str, str]]) -> None:
    rows = [
        {
            "id": f"id:{i}",
            "type": "RelationshipObject",
            "subject_id": s,
            "predicate": p,
            "object_id": o,
            "assertion_mode": "candidate",
            "evidence_refs": ["evidence"],
            "confidence": 0.5,
            "status": "candidate",
        }
        for i, (s, p, o) in enumerate(triples)
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def test_compare_batches_finds_agreement_and_disagreement(tmp_path: Path) -> None:
    batch_a = tmp_path / "a.jsonl"
    batch_b = tmp_path / "b.jsonl"
    shared = ("scripture:Rev.4.8", "quotesFrom", "scripture:Isa.6.3")
    only_a = ("scripture:Matt.1.23", "quotesFrom", "scripture:Isa.7.14")
    only_b = ("scripture:Rom.4.3", "quotesFrom", "scripture:Gen.15.6")
    write_batch(batch_a, [shared, only_a])
    write_batch(batch_b, [shared, only_b])

    result = compare_batches([batch_a, batch_b])

    assert set(result["agreements"]) == {shared}
    assert set(result["disagreements"]) == {only_a, only_b}

    agreement_path, disagreement_path, report_path = materialize_outputs(result, tmp_path / "comparison", tmp_path / "comparison.md")
    assert agreement_path.exists()
    assert disagreement_path.exists()
    assert report_path.exists()
    assert "Agreement triples (>=2 agents): 1" in report_path.read_text(encoding="utf-8")


def test_compare_batches_requires_two_batches(tmp_path: Path) -> None:
    batch = tmp_path / "a.jsonl"
    write_batch(batch, [])
    with pytest.raises(ValueError):
        compare_batches([batch])
