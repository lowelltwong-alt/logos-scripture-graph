from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path


from pipelines.graph.discover_connections import (
    Candidate,
    VerseText,
    candidate_to_record,
    discover_citation_formula,
    discover_lexical_cooccurrence,
    discover_shared_rare_phrase,
    load_editorial_crossref_pairs,
    merge_candidates,
    normalize_tokens,
    run_discovery,
)


def verse(osis: str, text: str, testament: str) -> VerseText:
    return VerseText(
        osis_ref=osis,
        passage_id=f"scripture:{osis}",
        text=text,
        tokens=tuple(normalize_tokens(text)),
        testament=testament,
    )


def validate_record(record: dict) -> None:
    required = {"id", "type", "subject_id", "predicate", "object_id", "assertion_mode", "evidence_refs", "confidence", "status"}
    assert required <= set(record)
    assert record["type"] == "RelationshipObject"
    assert record["assertion_mode"] == "candidate"
    assert record["status"] == "candidate"
    assert record["trust_zone"] == "candidate"
    assert record["evidence_refs"]


def test_lexical_cooccurrence_emits_candidate_edges(tmp_path: Path) -> None:
    verses = {
        "Isa.1.1": verse("Isa.1.1", "Alpha beta old", "OT"),
        "Matt.1.1": verse("Matt.1.1", "Alpha beta new", "NT"),
        "Luke.1.1": verse("Luke.1.1", "Only alpha", "NT"),
    }
    tokens = tmp_path / "word_tokens.jsonl"
    rows = [
        {"osis_ref": "Isa.1.1", "strong": "H1"},
        {"osis_ref": "Matt.1.1", "strong": "H1"},
        {"osis_ref": "Luke.1.1", "strong": "H1"},
        {"osis_ref": "Isa.1.1", "strong": "H2"},
        {"osis_ref": "Matt.1.1", "strong": "H2"},
    ]
    tokens.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")

    candidates = discover_lexical_cooccurrence(tokens, verses, rare_df_max=3, min_shared_strongs=2)

    assert candidates
    record = candidate_to_record(candidates[0], "test-agent", "2026-06-05")
    validate_record(record)
    assert record["predicate"] == "thematicallyRelatedTo"
    assert "strong:H1:df=3" in record["evidence_refs"]
    assert "strong:H2:df=2" in record["evidence_refs"]


def test_shared_rare_phrase_emits_nt_to_ot_candidate() -> None:
    verses = {
        "Isa.6.3": verse("Isa.6.3", "Holy holy holy is Yahweh of Armies", "OT"),
        "Rev.4.8": verse("Rev.4.8", "Holy holy holy is the Lord God Almighty", "NT"),
        "Gen.1.1": verse("Gen.1.1", "In the beginning God created", "OT"),
    }

    candidates = discover_shared_rare_phrase(verses, n_min=4, n_max=4, max_phrase_occurrences=2)

    assert [(c.subject_osis, c.object_osis) for c in candidates] == [("Rev.4.8", "Isa.6.3")]
    record = candidate_to_record(candidates[0], "test-agent", "2026-06-05")
    validate_record(record)
    assert record["predicate"] == "alludesTo"
    assert any(str(e).startswith("phrase:holy holy holy is") for e in record["evidence_refs"])


def test_citation_formula_requires_formula_and_phrase_match() -> None:
    verses = {
        "Isa.40.3": verse("Isa.40.3", "The voice of one crying in the wilderness", "OT"),
        "Matt.3.3": verse("Matt.3.3", "For this is he who was spoken by the prophet, the voice of one crying in the wilderness", "NT"),
        "Luke.1.1": verse("Luke.1.1", "the voice of one crying in the wilderness", "NT"),
    }

    candidates = discover_citation_formula(verses, n_min=5, n_max=7, max_phrase_occurrences=3)

    assert [(c.subject_osis, c.object_osis, c.predicate) for c in candidates] == [("Matt.3.3", "Isa.40.3", "quotesFrom")]
    record = candidate_to_record(candidates[0], "test-agent", "2026-06-05")
    validate_record(record)
    assert "formula:spoken by the prophet" in record["evidence_refs"]


def test_merge_dedups_editorial_crossrefs() -> None:
    verses = {
        "Isa.6.3": verse("Isa.6.3", "holy holy holy", "OT"),
        "Rev.4.8": verse("Rev.4.8", "holy holy holy", "NT"),
    }
    cand = Candidate("Rev.4.8", "quotesFrom", "Isa.6.3", "test", ["evidence"], 0.8, "test")

    emitted, deduped, invalid = merge_candidates([cand], {("Rev.4.8", "Isa.6.3")}, verses, 10)

    assert emitted == []
    assert deduped == 1
    assert invalid == 0


def test_run_discovery_writes_candidate_only_batch(tmp_path: Path) -> None:
    witnesses = tmp_path / "translation_witnesses.jsonl"
    word_tokens = tmp_path / "word_tokens.jsonl"
    crossrefs = tmp_path / "editorial_cross_references.jsonl"
    out = tmp_path / "batch.jsonl"
    manifest = tmp_path / "batch.manifest.yaml"
    report = tmp_path / "report.md"
    witness_rows = [
        {"osis_ref": "Isa.6.3", "passage_id": "scripture:Isa.6.3", "text": "Holy holy holy is Yahweh of Armies"},
        {"osis_ref": "Rev.4.8", "passage_id": "scripture:Rev.4.8", "text": "Holy holy holy is the Lord God Almighty"},
    ]
    witnesses.write_text("".join(json.dumps(r) + "\n" for r in witness_rows), encoding="utf-8")
    word_tokens.write_text("", encoding="utf-8")
    crossrefs.write_text("", encoding="utf-8")

    records, counts = run_discovery(Namespace(
        word_tokens=str(word_tokens), witnesses=str(witnesses), crossrefs=str(crossrefs),
        agent="test-agent", out=str(out), manifest=str(manifest), report=str(report), created_at="2026-06-05",
        max_total_candidates=20, lexical_rare_df_max=6, lexical_min_shared_strongs=2, lexical_max_candidates=20,
        phrase_n_min=4, phrase_n_max=4, phrase_max_occurrences=2, phrase_max_candidates=20,
        citation_n_min=4, citation_n_max=5, citation_max_occurrences=2, citation_max_candidates=20,
    ))

    assert out.exists()
    assert manifest.exists()
    assert report.exists()
    assert counts["deduped_editorial_crossrefs"] == 0
    assert records
    for record in records:
        validate_record(record)
