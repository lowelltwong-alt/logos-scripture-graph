from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from pipelines.graph.discover_connections import (
    Candidate,
    Witness,
    discover_citation_formulas,
    discover_lexical_cooccurrence,
    discover_shared_rare_phrases,
)

ROOT = Path(__file__).resolve().parents[1]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def relationship_validator() -> Draft202012Validator:
    schema = json.loads((ROOT / "schemas" / "relationship_object.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def assert_candidate_contract(candidate: Candidate) -> None:
    record = candidate.to_record("test-agent", "2026-06-05T00:00:00+00:00")
    errors = list(relationship_validator().iter_errors(record))
    assert errors == []
    assert record["assertion_mode"] == "candidate"
    assert record["status"] == "candidate"
    assert record["trust_zone"] == "candidate"
    assert record["evidence_refs"]


def test_lexical_cooccurrence_emits_schema_valid_candidate(tmp_path):
    word_tokens = tmp_path / "word_tokens.jsonl"
    write_jsonl(
        word_tokens,
        [
            {"type": "WordToken", "osis_ref": "John.1.1", "strong": "G0001"},
            {"type": "WordToken", "osis_ref": "John.1.1", "strong": "G0002"},
            {"type": "WordToken", "osis_ref": "Rom.1.1", "strong": "G0001"},
            {"type": "WordToken", "osis_ref": "Rom.1.1", "strong": "G0002"},
            {"type": "WordToken", "osis_ref": "Matt.1.1", "strong": "G0001"},
        ],
    )

    candidates, stats = discover_lexical_cooccurrence(
        word_tokens,
        editorial_pairs=set(),
        rare_df_max=3,
        min_shared_lemmas=2,
        limit=10,
    )

    assert stats["rare_strong_total"] == 2
    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.predicate == "thematicallyRelatedTo"
    assert {"strong:G0001", "strong:G0002"}.issubset(set(candidate.evidence_refs))
    assert_candidate_contract(candidate)


def test_shared_rare_phrase_emits_nt_to_ot_and_dedups_crossref():
    witnesses = {
        "Isa.9.2": Witness("Isa.9.2", "The people who walked in darkness have seen a great light."),
        "Matt.4.16": Witness("Matt.4.16", "The people who walked in darkness saw a great light."),
    }

    candidates, stats = discover_shared_rare_phrases(
        witnesses,
        editorial_pairs={frozenset(("Isa.9.2", "Matt.4.16"))},
        min_n=4,
        max_n=5,
        max_phrase_df=2,
        limit=10,
    )
    assert candidates == []
    assert stats["deduped_editorial_crossrefs"] >= 1

    candidates, _ = discover_shared_rare_phrases(
        witnesses,
        editorial_pairs=set(),
        min_n=4,
        max_n=5,
        max_phrase_df=2,
        limit=10,
    )
    assert candidates
    candidate = candidates[0]
    assert candidate.subject_osis == "Matt.4.16"
    assert candidate.object_osis == "Isa.9.2"
    assert candidate.predicate == "alludesTo"
    assert any(ref.startswith("phrase:") for ref in candidate.evidence_refs)
    assert_candidate_contract(candidate)


def test_citation_formula_requires_formula_and_matched_phrase():
    witnesses = {
        "Mic.5.2": Witness("Mic.5.2", "But you, Bethlehem, land of Judah, are not least among the rulers."),
        "Matt.2.5": Witness(
            "Matt.2.5",
            "For it is written, You Bethlehem land of Judah are not least among the rulers.",
        ),
    }

    candidates, stats = discover_citation_formulas(
        witnesses,
        editorial_pairs=set(),
        min_n=4,
        max_n=6,
        max_phrase_df=2,
        limit=10,
    )

    assert stats["nt_formula_occurrences"] == 1
    assert candidates
    candidate = candidates[0]
    assert candidate.predicate == "quotesFrom"
    assert candidate.subject_osis == "Matt.2.5"
    assert candidate.object_osis == "Mic.5.2"
    assert any(ref.startswith("formula:") for ref in candidate.evidence_refs)
    assert_candidate_contract(candidate)
