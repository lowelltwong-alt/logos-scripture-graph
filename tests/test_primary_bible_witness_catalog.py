from __future__ import annotations

import json
from pathlib import Path

from scripts import validate_primary_bible_witness_catalog as validator


def test_primary_bible_witness_catalog_passes(monkeypatch) -> None:
    monkeypatch.delenv("LOGOS_EXTERNAL_ASSET_ROOT", raising=False)
    result = validator.validate_primary_bible_witness_catalog(check_wiring=True)
    assert result["ok"], result["errors"]


def test_duplicate_source_id_fails(tmp_path: Path, monkeypatch) -> None:
    root = Path(__file__).resolve().parent.parent
    catalog = root / "data" / "candidate" / "source_catalog" / "primary_bible_witnesses"
    rows_path = catalog / "source_catalog_rows.jsonl"
    original = rows_path.read_text(encoding="utf-8")
    try:
        duped = original + original.splitlines()[0] + "\n"
        rows_path.write_text(duped, encoding="utf-8")
        result = validator.validate_primary_bible_witness_catalog(check_wiring=False)
        assert not result["ok"]
        assert any("duplicate source_id" in err for err in result["errors"])
    finally:
        rows_path.write_text(original, encoding="utf-8")


def test_reuse_sources_reference_manifests(monkeypatch) -> None:
    monkeypatch.delenv("LOGOS_EXTERNAL_ASSET_ROOT", raising=False)
    result = validator.validate_primary_bible_witness_catalog(check_wiring=False)
    assert result["ok"], result["errors"]


def test_catalog_rejects_scripture_text_or_graph_payload(monkeypatch) -> None:
    monkeypatch.delenv("LOGOS_EXTERNAL_ASSET_ROOT", raising=False)
    root = Path(__file__).resolve().parent.parent
    rows_path = root / "data" / "candidate" / "source_catalog" / "primary_bible_witnesses" / "source_catalog_rows.jsonl"
    original = rows_path.read_text(encoding="utf-8")
    try:
        row = json.loads(original.splitlines()[0])
        row["passage_text"] = "In the beginning"
        row["embedding"] = [0.1, 0.2]
        rows_path.write_text(json.dumps(row) + "\n" + "\n".join(original.splitlines()[1:]) + "\n", encoding="utf-8")
        result = validator.validate_primary_bible_witness_catalog(check_wiring=False)
        assert not result["ok"]
        assert any("prohibited field" in err for err in result["errors"])
    finally:
        rows_path.write_text(original, encoding="utf-8")


def test_catalog_rejects_greek_or_hebrew_text(monkeypatch) -> None:
    monkeypatch.delenv("LOGOS_EXTERNAL_ASSET_ROOT", raising=False)
    root = Path(__file__).resolve().parent.parent
    rows_path = root / "data" / "candidate" / "source_catalog" / "primary_bible_witnesses" / "source_catalog_rows.jsonl"
    original = rows_path.read_text(encoding="utf-8")
    try:
        row = json.loads(original.splitlines()[0])
        row["title"] = "λογος"
        rows_path.write_text(json.dumps(row) + "\n" + "\n".join(original.splitlines()[1:]) + "\n", encoding="utf-8")
        result = validator.validate_primary_bible_witness_catalog(check_wiring=False)
        assert not result["ok"]
        assert any("original-language text" in err for err in result["errors"])
    finally:
        rows_path.write_text(original, encoding="utf-8")


def test_catalog_rejects_pipeline_admission_reference(tmp_path: Path, monkeypatch) -> None:
    pipeline = tmp_path / "import_witnesses.py"
    pipeline.write_text("ROOT = 'data/candidate/source_catalog/primary_bible_witnesses'\n", encoding="utf-8")
    monkeypatch.setattr(validator, "PIPELINE_DIRS", (tmp_path,))
    errors = validator._validate_no_pipeline_admission_path()
    assert any("pipeline code must not reference" in error for error in errors)
