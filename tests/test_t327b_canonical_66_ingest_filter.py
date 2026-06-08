from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
import yaml

from pipelines.ingest.usfm_importer import main as importer_main
from pipelines.util.canonical_scope import (
    CanonicalScopeError,
    assert_records_are_canonical_66,
    canonical_66_books,
    excluded_books,
    filter_to_canonical_66,
    is_canonical_66_book,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "canon" / "canonical_66_books.yaml"
DOC = ROOT / "docs" / "roadmap" / "T327B_CANONICAL_66_INGEST_FILTER.md"
TASK = ROOT / ".ai" / "tasks" / "T327B.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T327B" / "handoff.md"

REQUIRED_EXCLUDED = {
    "FRT",
    "GLO",
    "Tob",
    "Jdt",
    "AddEsth",
    "Wis",
    "Sir",
    "Bar",
    "1Macc",
    "2Macc",
    "1Esd",
    "PrMan",
    "Ps151",
    "3Macc",
    "2Esd",
    "4Macc",
    "AddDan",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def test_allow_list_parses_and_contains_exactly_66_unique_books() -> None:
    data = yaml.safe_load(read(CONFIG))
    books = data["canonical_66_books"]
    assert len(books) == 66
    assert len(set(books)) == 66
    assert books == list(canonical_66_books())
    assert books[0] == "Gen"
    assert books[-1] == "Rev"


def test_excluded_books_are_absent_from_allow_list() -> None:
    books = set(canonical_66_books())
    excluded = set(excluded_books())
    assert REQUIRED_EXCLUDED <= excluded
    assert not books & REQUIRED_EXCLUDED
    assert not books & {"FRT", "GLO"}


def test_known_canonical_and_excluded_book_membership() -> None:
    assert is_canonical_66_book("GEN")
    assert is_canonical_66_book("Gen")
    assert is_canonical_66_book("John.3.16")
    assert is_canonical_66_book("Rev")
    for book in REQUIRED_EXCLUDED:
        assert not is_canonical_66_book(book)


def test_synthetic_mixed_input_filters_to_canonical_only() -> None:
    records = [
        {"id": "scripture:Gen.1.1", "book": "Gen"},
        {"id": "scripture:Tob.1.1", "book": "Tob"},
        {"id": "scripture:John.1.1", "osis_ref": "John.1.1"},
        {"id": "source:GLO:abba", "book": "GLO"},
        {"id": "source:FRT:intro", "usfm_book": "FRT"},
    ]
    filtered = filter_to_canonical_66(records)
    assert [record["id"] for record in filtered] == ["scripture:Gen.1.1", "scripture:John.1.1"]


def test_importer_filter_flag_excludes_non_66_from_canonical_outputs(tmp_path: Path) -> None:
    archive = tmp_path / "fixture.zip"
    john = "\n".join([r"\id JHN Test", r"\c 1", r"\v 1 Canonical fixture text."])
    tob = "\n".join([r"\id TOB Test", r"\c 1", r"\v 1 Noncanonical fixture text."])
    glossary = "\n".join([r"\id GLO", r"\ili \k Abba\k* Abba means father."])
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("73-JHNeng-web.usfm", john)
        zf.writestr("41-TOBeng-web.usfm", tob)
        zf.writestr("106-GLOeng-web.usfm", glossary)

    canonical = tmp_path / "canonical"
    processed = tmp_path / "processed"
    result = importer_main(
        [
            "--archive",
            str(archive),
            "--canonical-root",
            str(canonical),
            "--processed-root",
            str(processed),
            "--skip-sha-check",
            "--canonical-66-filter",
        ]
    )
    assert result == 0

    passages = read_jsonl(canonical / "scripture" / "passages" / "passages.jsonl")
    witnesses = read_jsonl(canonical / "translations" / "eng-web" / "translation_witnesses.jsonl")
    glossary_entries = read_jsonl(canonical / "translations" / "eng-web" / "glossary_entries.jsonl")
    events = read_jsonl(processed / "usfm_events.jsonl")

    assert {record["book"] for record in passages} == {"John"}
    assert {record["osis_ref"].split(".", 1)[0] for record in witnesses} == {"John"}
    assert glossary_entries == []
    assert {"John", "Tob", "GLO"} <= {record["osis_book"] for record in events}


def test_synthetic_validator_fails_closed_on_non_66_record() -> None:
    with pytest.raises(CanonicalScopeError, match="Ps151"):
        assert_records_are_canonical_66(
            [
                {"id": "scripture:Matt.1.1", "book": "Matt"},
                {"id": "scripture:Ps151.1.1", "book": "Ps151"},
            ],
            source="synthetic",
        )


def test_synthetic_validator_accepts_valid_canonical_book_identity() -> None:
    assert_records_are_canonical_66(
        [
            {"id": "scripture:Gen.1.1", "book": "Gen"},
            {"id": "witness:eng-web:John.3.16", "osis_ref": "John.3.16"},
            {"id": "scripture:Rev.22.21", "passage_id": "scripture:Rev.22.21"},
        ],
        source="synthetic",
    )


@pytest.mark.parametrize("book", ["GLO", "FRT"])
def test_synthetic_validator_fails_on_front_or_glossary_books(book: str) -> None:
    with pytest.raises(CanonicalScopeError, match=book):
        assert_records_are_canonical_66(
            [{"id": f"source:{book}:sample", "book": book}],
            source="synthetic",
        )


def test_synthetic_validator_fails_closed_on_missing_book_identity() -> None:
    with pytest.raises(CanonicalScopeError, match="missing canonical book identity"):
        assert_records_are_canonical_66(
            [{"id": "canonical-sidecar:unclassified", "text": "No book metadata here."}],
            source="synthetic",
        )


def test_glossary_like_record_without_book_identity_fails_in_canonical_output_mode() -> None:
    glossary_like_record = {
        "id": "glossary:abba",
        "term": "Abba",
        "definition": "father",
        "source_marker": "k",
    }
    with pytest.raises(CanonicalScopeError, match="synthetic-glossary:1"):
        assert_records_are_canonical_66([glossary_like_record], source="synthetic-glossary")


def test_validator_script_checks_config_without_existing_generated_outputs() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_canonical_66_scope.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "config validation passed" in result.stdout


def test_validator_script_fails_on_synthetic_non_66_jsonl(tmp_path: Path) -> None:
    sample = tmp_path / "mixed.jsonl"
    sample.write_text(
        "\n".join(
            [
                json.dumps({"id": "scripture:Rom.1.1", "book": "Rom"}),
                json.dumps({"id": "scripture:Bar.1.1", "book": "Bar"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_canonical_66_scope.py"), str(sample)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "Bar" in result.stderr


def test_validator_script_fails_on_synthetic_unclassified_jsonl(tmp_path: Path) -> None:
    sample = tmp_path / "unclassified.jsonl"
    sample.write_text(
        json.dumps({"id": "glossary:abba", "term": "Abba", "definition": "father"}) + "\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_canonical_66_scope.py"), str(sample)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "missing canonical book identity" in result.stderr


def test_t327b_docs_record_non_regeneration_boundary() -> None:
    combined = "\n".join(read(path) for path in [DOC, TASK, HANDOFF])
    assert "Existing generated outputs may still contain non-66 records until T327C" in combined
    assert "T327D" in combined
    assert "T327E" in combined
    assert "does not regenerate canonical outputs" in combined
    assert "does not mutate raw/canonical data" in combined
