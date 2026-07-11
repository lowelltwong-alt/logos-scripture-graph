from __future__ import annotations

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
