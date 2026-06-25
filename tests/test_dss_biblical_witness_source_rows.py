from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_dss_biblical_witness_source_rows as validator


ROOT = Path(__file__).resolve().parents[1]
ROWS = (
    ROOT
    / "data"
    / "candidate"
    / "source_catalog"
    / "manuscript_reliability"
    / "sqlite"
    / "dss_biblical_witness_rows.jsonl"
)


def test_t396_dss_biblical_witness_source_rows_validate() -> None:
    result = validator.validate_dss_biblical_witness_source_rows()

    assert result["task_id"] == "T396"
    assert result["witness_id"] == "dss_great_isaiah_scroll_1qisa"
    assert result["population_row_count"] == 9
    assert result["seeded_row_count"] == 37
    assert result["population_table_counts"] == validator.POPULATED_TABLE_COUNTS


def test_t396_rows_are_great_isaiah_metadata_only() -> None:
    records = validator._read_population_rows(ROWS)

    assert len(records) == 9
    assert {record["table"] for record in records} == set(validator.POPULATED_TABLE_COUNTS)
    for record in records:
        row = record["row"]
        assert validator.COMMON_REQUIRED_ROW_FIELDS <= set(row)
        assert row["source_url"] in validator.ALLOWED_SOURCE_URLS
        assert row["confidence"] in {"high", "medium", "low"}
        assert row["method"].strip()
        assert row["provenance_note"].strip()
        assert row["review_status"].strip()
        assert row["rights_access_status"].strip()
        assert "not" in row["non_authorizing_scope_label"]
        assert row["stores_scripture_text"] == 0
        assert row["stores_transcription_text"] == 0
        assert row["stores_boundary_text"] == 0
        assert not (validator.FORBIDDEN_ROW_KEYS & set(row))
        if record["table"] != "scripture_holding_institution":
            witness = row.get("witness_id_candidate", row.get("witness_or_catalog_ref", row.get("witness_group")))
            assert witness == validator.WITNESS_ID


def test_t396_validator_rejects_missing_provenance(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_population_rows(ROWS)
    rows[0]["row"].pop("provenance_note")
    monkeypatch.setattr(validator, "_read_population_rows", lambda path=ROWS: rows)

    with pytest.raises(validator.DssBiblicalWitnessSourceRowsError, match="provenance_note"):
        validator.validate_dss_biblical_witness_source_rows(check_wiring=False)


def test_t396_validator_rejects_text_bearing_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_population_rows(ROWS)
    rows[0]["row"]["source_text"] = "forbidden"
    monkeypatch.setattr(validator, "_read_population_rows", lambda path=ROWS: rows)

    with pytest.raises(validator.DssBiblicalWitnessSourceRowsError, match="forbidden text-bearing keys"):
        validator.validate_dss_biblical_witness_source_rows(check_wiring=False)


def test_t396_validator_rejects_authorizing_label(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_population_rows(ROWS)
    rows[0]["row"]["non_authorizing_scope_label"] = "scripture_authority"
    monkeypatch.setattr(validator, "_read_population_rows", lambda path=ROWS: rows)

    with pytest.raises(validator.DssBiblicalWitnessSourceRowsError, match="must deny authority"):
        validator.validate_dss_biblical_witness_source_rows(check_wiring=False)


def test_t396_validator_rejects_unscoped_witness(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_population_rows(ROWS)
    rows[1]["row"]["witness_id_candidate"] = "dss_unreviewed_extra_witness"
    monkeypatch.setattr(validator, "_read_population_rows", lambda path=ROWS: rows)

    with pytest.raises(validator.DssBiblicalWitnessSourceRowsError, match="unexpected witness"):
        validator.validate_dss_biblical_witness_source_rows(check_wiring=False)


def test_t396_validator_rejects_unapproved_source_url(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = validator._read_population_rows(ROWS)
    rows[0]["row"]["source_url"] = "https://example.com/not-an-official-anchor"
    monkeypatch.setattr(validator, "_read_population_rows", lambda path=ROWS: rows)

    with pytest.raises(validator.DssBiblicalWitnessSourceRowsError, match="source_url not allowed"):
        validator.validate_dss_biblical_witness_source_rows(check_wiring=False)
