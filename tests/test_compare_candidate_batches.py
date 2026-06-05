from __future__ import annotations

import json
from pathlib import Path

from pipelines.graph.compare_candidate_batches import compare_batches


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def rel(subject: str, predicate: str, obj: str, agent: str, confidence: float = 0.7) -> dict:
    return {
        "id": f"cand:rel:{subject}--{predicate}--{obj}",
        "type": "RelationshipObject",
        "subject_id": f"scripture:{subject}",
        "predicate": predicate,
        "object_id": f"scripture:{obj}",
        "assertion_mode": "candidate",
        "evidence_refs": [f"phrase:{subject}-{obj}"],
        "confidence": confidence,
        "trust_zone": "candidate",
        "status": "candidate",
        "provenance": {"created_by": f"connection_discoverer:{agent}"},
    }


def test_compare_batches_splits_agreement_and_disagreement(tmp_path):
    batch_a = tmp_path / "a.jsonl"
    batch_b = tmp_path / "b.jsonl"
    write_jsonl(
        batch_a,
        [
            rel("Matt.2.5", "quotesFrom", "Mic.5.2", "agent-a", 0.8),
            rel("John.1.1", "thematicallyRelatedTo", "Gen.1.1", "agent-a", 0.5),
        ],
    )
    write_jsonl(
        batch_b,
        [
            rel("Matt.2.5", "quotesFrom", "Mic.5.2", "agent-b", 0.9),
            rel("Rev.4.8", "quotesFrom", "Isa.6.3", "agent-b", 0.85),
        ],
    )

    comparison = compare_batches([batch_a, batch_b])

    assert comparison["agreement_count"] == 1
    assert comparison["disagreement_count"] == 2
    agreement = comparison["agreements"][0]
    assert agreement["subject_id"] == "scripture:Matt.2.5"
    assert agreement["predicate"] == "quotesFrom"
    assert agreement["object_id"] == "scripture:Mic.5.2"
    assert agreement["agents"] == ["agent-a", "agent-b"]
    assert agreement["highest_confidence"] == 0.9
