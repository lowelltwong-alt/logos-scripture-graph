from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts import build_cursor_observation_pack as packer
from scripts import validate_rust_observation_substrate as validator


ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    _write(path, "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n")


def _canonical_books() -> list[str]:
    data = yaml.safe_load((ROOT / "config" / "canon" / "canonical_66_books.yaml").read_text(encoding="utf-8"))
    return data["canonical_66_books"]


def _minimal_substrate(root: Path) -> Path:
    out = root / "observation_substrate" / "current"
    books = _canonical_books()
    _write(
        out / "scan_manifest.json",
        json.dumps(
            {
                "type": "RustObservationScanManifest",
                "schema_version": "rust_observation_substrate.v1",
                "scanner": "tools/usfm_observation_scanner",
                "scanner_version": "0.1.0",
                "non_authorizing": True,
                "no_text": True,
                "source_path": "data/raw/bible/eng-web/usfm/eng-web_usfm.zip",
                "source_sha256_short": "abcdef1234567890",
                "canonical_book_count": 66,
                "source_file_count": 83,
                "output_files": validator.REQUIRED_OUTPUTS,
                "authority": {"authorizes_chunk_output_change": False},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    _write_jsonl(
        out / "book_observations.jsonl",
        [
            {
                "type": "RustObservationBook",
                "schema_version": "rust_observation_substrate.v1",
                "non_authorizing": True,
                "no_text": True,
                "book_id": book,
                "usfm_code": book.upper()[:3],
                "source_entry": f"{book}.usfm",
                "source_class": "canonical_66",
                "sha256_short": "abcdef12",
                "bytes_read": 1,
                "char_count": 1,
                "line_count": 1,
                "chapter_count": 1,
                "verse_count": 1,
                "marker_counts": {"v": 1},
                "strong_h_count": 1 if book == "Jonah" else 0,
                "strong_g_count": 1 if book == "2John" else 0,
                "feature_flags": ["has_strong_h"] if book == "Jonah" else [],
            }
            for book in books
        ],
    )
    _write_jsonl(
        out / "verse_observations.jsonl",
        [
            {
                "type": "RustObservationVerse",
                "schema_version": "rust_observation_substrate.v1",
                "non_authorizing": True,
                "no_text": True,
                "book_id": "2John",
                "osis_ref": "2John.1.1",
                "chapter": 1,
                "verse": 1,
                "source_line_start": 1,
                "source_line_end": 1,
                "marker_counts": {"v": 1, "w": 1},
                "strong_ids": ["G4245"],
                "feature_flags": ["has_strong_g"],
            }
        ],
    )
    _write_jsonl(
        out / "span_observation_features.jsonl",
        [
            {
                "type": "RustObservationSpanFeature",
                "schema_version": "rust_observation_substrate.v1",
                "non_authorizing": True,
                "no_text": True,
                "span_id": "2John-chapter-1",
                "book_id": "2John",
                "osis_start": "2John.1.1",
                "osis_end": "2John.1.1",
                "span_kind": "chapter_observed_feature_rollup",
                "verse_count": 1,
                "marker_counts": {"v": 1},
                "risk_flags": [],
            }
        ],
    )
    _write_jsonl(out / "risk_signal_index.jsonl", [])
    _write_jsonl(
        out / "strong_occurrence_index.jsonl",
        [
            {
                "type": "RustObservationStrongOccurrence",
                "schema_version": "rust_observation_substrate.v1",
                "non_authorizing": True,
                "no_text": True,
                "strong_id": "G4245",
                "book_id": "2John",
                "osis_ref": "2John.1.1",
                "language_layer": "greek",
                "occurrence_count": 1,
            }
        ],
    )
    _write(out / "marker_anomalies.jsonl", "")
    return out


def test_t412_contract_validates_current_repo() -> None:
    result = validator.validate_rust_observation_substrate()

    assert result["mode"] == "contract"
    assert result["task_id"] == "T412"


def test_generated_substrate_accepts_no_text_canonical_66_fixture(tmp_path: Path) -> None:
    substrate = _minimal_substrate(tmp_path)

    result = validator.validate_generated_substrate(substrate)

    assert result["canonical_books"] == 66
    assert result["verses"] == 1


def test_generated_substrate_rejects_missing_canonical_book(tmp_path: Path) -> None:
    substrate = _minimal_substrate(tmp_path)
    rows = [json.loads(line) for line in (substrate / "book_observations.jsonl").read_text(encoding="utf-8").splitlines()]
    _write_jsonl(substrate / "book_observations.jsonl", rows[:-1])

    with pytest.raises(validator.RustObservationSubstrateError, match="canonical_66 book order"):
        validator.validate_generated_substrate(substrate)


def test_generated_substrate_rejects_text_bearing_row(tmp_path: Path) -> None:
    substrate = _minimal_substrate(tmp_path)
    rows = [json.loads(line) for line in (substrate / "verse_observations.jsonl").read_text(encoding="utf-8").splitlines()]
    rows[0]["text"] = "In the beginning"
    _write_jsonl(substrate / "verse_observations.jsonl", rows)

    with pytest.raises(validator.RustObservationSubstrateError, match="forbidden text-bearing key"):
        validator.validate_generated_substrate(substrate)


def test_generated_substrate_rejects_authority_true(tmp_path: Path) -> None:
    substrate = _minimal_substrate(tmp_path)
    manifest = json.loads((substrate / "scan_manifest.json").read_text(encoding="utf-8"))
    manifest["authority"]["authorizes_chunk_output_change"] = True
    _write(substrate / "scan_manifest.json", json.dumps(manifest) + "\n")

    with pytest.raises(validator.RustObservationSubstrateError, match="forbidden authority"):
        validator.validate_generated_substrate(substrate)


def test_cursor_pack_check_and_write_are_task_scoped(tmp_path: Path) -> None:
    substrate = _minimal_substrate(tmp_path)

    checked = packer.build_cursor_observation_pack(input_dir=substrate, task_id="T411", check=True)
    written = packer.build_cursor_observation_pack(
        input_dir=substrate,
        task_id="T411",
        output_dir=tmp_path / "agent_work" / "T411" / "ledger_inputs",
    )

    assert checked["mode"] == "check"
    assert written["manifest"]["selected_books"] == ["2John", "Jonah", "Phlm"]
    assert written["manifest"]["risk_signal_counts"] == {}
    assert (tmp_path / "agent_work" / "T411" / "ledger_inputs" / "cursor_pack_manifest.json").is_file()


def test_strongs_remain_observable_without_becoming_risk_signals(tmp_path: Path) -> None:
    substrate = _minimal_substrate(tmp_path)

    result = validator.validate_generated_substrate(substrate)
    verse_rows = [
        json.loads(line)
        for line in (substrate / "verse_observations.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    risk_rows = [
        json.loads(line)
        for line in (substrate / "risk_signal_index.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert result["verses"] == 1
    assert verse_rows[0]["strong_ids"] == ["G4245"]
    assert "has_strong_g" in verse_rows[0]["feature_flags"]
    assert risk_rows == []


def test_contract_validator_requires_rust_hash_dependencies(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cargo = (ROOT / "tools" / "usfm_observation_scanner" / "Cargo.toml").read_text(encoding="utf-8")
    broken = cargo.replace('hex = "0.4"\n', "").replace('sha2 = "0.10"\n', "")
    temp_cargo = tmp_path / "Cargo.toml"
    temp_cargo.write_text(broken, encoding="utf-8")
    monkeypatch.setattr(validator, "RUST_CARGO", temp_cargo)

    with pytest.raises(validator.RustObservationSubstrateError, match="hex ="):
        validator.validate_contract()


def test_validate_all_uses_contract_validator_not_full_rust_scan() -> None:
    text = (ROOT / "scripts" / "validate_all.py").read_text(encoding="utf-8")

    assert "validate_rust_observation_substrate.py" in text
    assert "cargo run --manifest-path tools/usfm_observation_scanner/Cargo.toml" not in text
