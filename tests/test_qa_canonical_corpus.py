from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.qa_canonical_corpus import (
    CanonicalCorpusQAError,
    GLOSSARY_REL,
    PASSAGES_REL,
    SIDECAR_RELS,
    WITNESSES_REL,
    WORD_TOKENS_REL,
    run_qa,
)


MINI_BOOKS = ("Gen", "Exod")
BLOCKED = {"FRT", "GLO", "Tob"}


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def write_valid_fixture(root: Path) -> None:
    passages = [
        {"id": "scripture:Gen.1.1", "book": "Gen", "osis_ref": "Gen.1.1"},
        {"id": "scripture:Exod.1.1", "book": "Exod", "osis_ref": "Exod.1.1"},
    ]
    witnesses = [
        {
            "id": "translation-witness:eng-web:Gen.1.1",
            "osis_ref": "Gen.1.1",
            "passage_id": "scripture:Gen.1.1",
            "text": "Genesis fixture text.",
        },
        {
            "id": "translation-witness:eng-web:Exod.1.1",
            "osis_ref": "Exod.1.1",
            "passage_id": "scripture:Exod.1.1",
            "text": "Exodus fixture text.",
        },
    ]
    write_jsonl(root / PASSAGES_REL, passages)
    write_jsonl(root / WITNESSES_REL, witnesses)
    for rel in SIDECAR_RELS:
        write_jsonl(root / rel, [])
    write_jsonl(root / GLOSSARY_REL, [])
    write_jsonl(
        root / WORD_TOKENS_REL,
        [
            {"id": "word-token:Gen.1.1:1", "book": "Gen", "passage_id": "scripture:Gen.1.1"},
            {"id": "word-token:Exod.1.1:1", "book": "Exod", "passage_id": "scripture:Exod.1.1"},
        ],
    )


def run_mini(root: Path):
    return run_qa(root, expected_books=MINI_BOOKS, blocked_books=BLOCKED)


def write_empty_variant_fixture(root: Path, *, with_footnote: bool) -> None:
    write_jsonl(root / PASSAGES_REL, [{"id": "scripture:Acts.8.37", "book": "Acts", "osis_ref": "Acts.8.37"}])
    write_jsonl(
        root / WITNESSES_REL,
        [
            {
                "id": "translation-witness:eng-web:Acts.8.37",
                "osis_ref": "Acts.8.37",
                "passage_id": "scripture:Acts.8.37",
                "text": "",
            }
        ],
    )
    for rel in SIDECAR_RELS:
        write_jsonl(root / rel, [])
    if with_footnote:
        write_jsonl(
            root / SIDECAR_RELS[1],
            [
                {
                    "id": "footnote:eng-web:Acts.8.37:0001",
                    "book": "Acts",
                    "osis_ref": "Acts.8.37",
                    "passage_id": "scripture:Acts.8.37",
                    "text": "TR adds the verse.",
                }
            ],
        )
    write_jsonl(root / GLOSSARY_REL, [])
    write_jsonl(root / WORD_TOKENS_REL, [])


def test_valid_mini_fixture_passes(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    report = run_mini(tmp_path)
    assert report.passage_count == 2
    assert report.witness_count == 2
    assert report.canonical_books == MINI_BOOKS
    assert report.word_token_count == 2


def test_missing_book_identity_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_jsonl(
        tmp_path / PASSAGES_REL,
        [
            {"id": "scripture:Gen.1.1", "book": "Gen", "osis_ref": "Gen.1.1"},
            {"id": "scripture:unclassified", "chapter": 1},
        ],
    )
    with pytest.raises(CanonicalCorpusQAError, match="missing canonical book identity"):
        run_mini(tmp_path)


def test_duplicate_passage_id_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_jsonl(
        tmp_path / PASSAGES_REL,
        [
            {"id": "scripture:Gen.1.1", "book": "Gen", "osis_ref": "Gen.1.1"},
            {"id": "scripture:Gen.1.1", "book": "Gen", "osis_ref": "Gen.1.1"},
        ],
    )
    with pytest.raises(CanonicalCorpusQAError, match="duplicate passage id scripture:Gen.1.1"):
        run_mini(tmp_path)


def test_excluded_book_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_jsonl(
        tmp_path / PASSAGES_REL,
        [
            {"id": "scripture:Gen.1.1", "book": "Gen", "osis_ref": "Gen.1.1"},
            {"id": "scripture:Tob.1.1", "book": "Tob", "osis_ref": "Tob.1.1"},
        ],
    )
    with pytest.raises(CanonicalCorpusQAError, match="non-66 book Tob"):
        run_mini(tmp_path)


def test_missing_witness_alignment_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_jsonl(
        tmp_path / WITNESSES_REL,
        [
            {
                "id": "translation-witness:eng-web:Gen.1.1",
                "osis_ref": "Gen.1.1",
                "passage_id": "scripture:Gen.1.1",
                "text": "Genesis fixture text.",
            }
        ],
    )
    with pytest.raises(CanonicalCorpusQAError, match="translation_witnesses count 1 != passages count 2"):
        run_mini(tmp_path)


def test_empty_witness_text_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_jsonl(
        tmp_path / WITNESSES_REL,
        [
            {
                "id": "translation-witness:eng-web:Gen.1.1",
                "osis_ref": "Gen.1.1",
                "passage_id": "scripture:Gen.1.1",
                "text": "",
            },
            {
                "id": "translation-witness:eng-web:Exod.1.1",
                "osis_ref": "Exod.1.1",
                "passage_id": "scripture:Exod.1.1",
                "text": "Exodus fixture text.",
            },
        ],
    )
    with pytest.raises(CanonicalCorpusQAError, match="witness text is empty"):
        run_mini(tmp_path)


def test_known_empty_variant_witness_requires_footnote(tmp_path: Path) -> None:
    write_empty_variant_fixture(tmp_path, with_footnote=False)
    with pytest.raises(CanonicalCorpusQAError, match="no explanatory footnote"):
        run_qa(tmp_path, expected_books=("Acts",), blocked_books=BLOCKED)


def test_known_empty_variant_witness_with_footnote_passes(tmp_path: Path) -> None:
    write_empty_variant_fixture(tmp_path, with_footnote=True)
    report = run_qa(tmp_path, expected_books=("Acts",), blocked_books=BLOCKED)
    assert report.allowed_empty_witness_refs == ("Acts.8.37",)


def test_sidecar_excluded_book_fails(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_jsonl(
        tmp_path / SIDECAR_RELS[0],
        [{"id": "boundary:Tob.1.1", "book": "Tob", "passage_id": "scripture:Gen.1.1"}],
    )
    with pytest.raises(CanonicalCorpusQAError, match="non-66 book Tob"):
        run_mini(tmp_path)


def test_glossary_entry_requires_explicit_non_scripture_scope(tmp_path: Path) -> None:
    write_valid_fixture(tmp_path)
    write_jsonl(tmp_path / GLOSSARY_REL, [{"id": "glossary:abba", "term": "Abba"}])
    with pytest.raises(CanonicalCorpusQAError, match="not explicitly marked non-Scripture"):
        run_mini(tmp_path)
