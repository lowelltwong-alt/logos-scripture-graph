from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_manuscript_source_catalog_sqlite_shell as validator


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data" / "candidate" / "source_catalog" / "manuscript_reliability" / "sqlite" / "seed_rows.jsonl"
SCHEMA = ROOT / "data" / "candidate" / "source_catalog" / "manuscript_reliability" / "sqlite" / "schema.sql"
CONTROL = ROOT / ".ai" / "control" / "manuscript_source_catalog_sqlite_shell.yaml"


def test_t395_manuscript_source_catalog_sqlite_shell_validates() -> None:
    result = validator.validate_manuscript_source_catalog_sqlite_shell()

    assert result["shell_id"] == "t395_manuscript_source_catalog_sqlite_shell"
    assert result["table_count"] == 12
    assert result["seeded_row_count"] == 37
    assert result["empty_shell_table_count"] == 8
    assert result["seeded_table_counts"] == validator.SEEDED_TABLE_COUNTS


def test_t395_seed_rows_are_limited_to_source_catalog_layers() -> None:
    rows = validator._read_seed(SEED)
    tables = {record["table"] for record in rows}

    assert tables == set(validator.SEEDED_TABLE_COUNTS)
    assert not tables & validator.EMPTY_SHELL_TABLES
    assert not any(table.startswith(("canonical_", "boundary_", "doctrine_")) for table in tables)


def test_t395_rows_have_required_metadata_and_no_text_storage() -> None:
    for record in validator._read_seed(SEED):
        row = record["row"]
        assert validator.COMMON_REQUIRED_ROW_FIELDS <= set(row)
        assert row["source_url"].startswith("https://")
        assert row["method"].strip()
        assert row["confidence"] in {"high", "medium", "low"}
        assert row["provenance_note"].strip()
        assert row["review_status"].strip()
        assert row["rights_access_status"].strip()
        assert "not" in row["non_authorizing_scope_label"]
        assert row["stores_scripture_text"] == 0
        assert row["stores_transcription_text"] == 0
        assert row["stores_boundary_text"] == 0


def test_t395_schema_has_no_forbidden_namespaces_or_text_columns() -> None:
    schema = SCHEMA.read_text(encoding="utf-8").lower()

    for prefix in ("canonical_", "boundary_", "doctrine_"):
        assert f"create table {prefix}" not in schema
        assert f"create view {prefix}" not in schema
    for forbidden in [
        "scripture_text text",
        "transcription_text text",
        "bible_text text",
        "source_text text",
        "reading_text text",
        "preferred_reading text",
    ]:
        assert forbidden not in schema


def test_t395_control_packet_preserves_non_authorizations() -> None:
    text = CONTROL.read_text(encoding="utf-8")

    for phrase in [
        "authorizes_committed_sqlite_database_file: false",
        "authorizes_witness_row_population: false",
        "authorizes_source_text_import: false",
        "authorizes_transcription_storage: false",
        "authorizes_bible_text_storage: false",
        "authorizes_preferred_reading: false",
        "authorizes_graph_edges: false",
        "authorizes_retrieval_truth: false",
        "authorizes_apologetic_conclusion_as_truth: false",
        "No canonical_* table or view",
    ]:
        assert phrase in text


def test_t395_validator_rejects_canonical_sqlite_object(monkeypatch: pytest.MonkeyPatch) -> None:
    original_read_text = validator._read_text

    def fake_read_text(path: Path) -> str:
        text = original_read_text(path)
        if path == validator.SCHEMA:
            return text + "\nCREATE TABLE canonical_source_catalog (id TEXT);\n"
        return text

    monkeypatch.setattr(validator, "_read_text", fake_read_text)

    with pytest.raises(validator.ManuscriptSourceCatalogSqliteShellError, match="forbidden SQLite object prefix"):
        validator.validate_manuscript_source_catalog_sqlite_shell(check_wiring=False)


def test_t395_validator_rejects_witness_seed_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_seed(SEED)
    rows.append({"table": "scripture_catalog_witness_record", "row": {}})
    monkeypatch.setattr(validator, "_read_seed", lambda path=SEED: rows)

    with pytest.raises(validator.ManuscriptSourceCatalogSqliteShellError, match="forbidden seed table"):
        validator.validate_manuscript_source_catalog_sqlite_shell(check_wiring=False)


def test_t395_validator_rejects_missing_provenance(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_seed(SEED)
    rows[0]["row"].pop("provenance_note")
    monkeypatch.setattr(validator, "_read_seed", lambda path=SEED: rows)

    with pytest.raises(validator.ManuscriptSourceCatalogSqliteShellError, match="provenance_note"):
        validator.validate_manuscript_source_catalog_sqlite_shell(check_wiring=False)


def test_t395_validator_rejects_source_url_outside_t391(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_seed(SEED)
    rows[0]["row"]["source_url"] = "https://example.com/not-a-t391-source"
    monkeypatch.setattr(validator, "_read_seed", lambda path=SEED: rows)

    with pytest.raises(validator.ManuscriptSourceCatalogSqliteShellError, match="not from T391 curated sources"):
        validator.validate_manuscript_source_catalog_sqlite_shell(check_wiring=False)
