from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def _valid_records() -> list[dict]:
    return [
        {
            "id": "scripture:Gen.1.1",
            "type": "ScripturePassage",
            "book": "Gen",
            "osis_ref": "Gen.1.1",
            "source_sha256": "abc123",
            "license": "public-domain",
            "canon_profiles": ["protestant_66"],
        },
        {
            "id": "witness:eng-web:Gen.1.1",
            "type": "TranslationWitness",
            "book": "Gen",
            "osis_ref": "Gen.1.1",
            "passage_id": "scripture:Gen.1.1",
            "translation_id": "eng-web",
            "text": "In the beginning God created the heavens and the earth.",
            "source_sha256": "abc123",
            "license": "public-domain",
        },
    ]


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def test_fast_jsonl_agrees_with_python_on_valid_fixture(tmp_path: Path) -> None:
    fixture = tmp_path / "valid.jsonl"
    _write_jsonl(fixture, _valid_records())

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_jsonl.py",
            "--require-rust",
            "--compare-python",
            "--require-canon",
            str(fixture),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Rust/Python JSONL validator verdict parity passed" in result.stdout


def test_fast_jsonl_rejects_missing_id(tmp_path: Path) -> None:
    fixture = tmp_path / "missing_id.jsonl"
    records = _valid_records()
    records[0].pop("id")
    _write_jsonl(fixture, records)

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_jsonl.py",
            "--require-rust",
            "--require-canon",
            str(fixture),
        ]
    )

    assert result.returncode != 0
    assert "missing id" in result.stdout


def test_fast_canonical_scope_rejects_noncanonical_book(tmp_path: Path) -> None:
    fixture = tmp_path / "tobit.jsonl"
    _write_jsonl(
        fixture,
        [
            {
                "id": "scripture:Tob.1.1",
                "type": "ScripturePassage",
                "book": "Tob",
                "osis_ref": "Tob.1.1",
                "source_sha256": "abc123",
                "license": "public-domain",
                "canon_profiles": ["deuterocanonical"],
            }
        ],
    )

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_canonical_scope.py",
            "--require-rust",
            "--compare-python",
            str(fixture),
        ]
    )

    assert result.returncode != 0
    assert "non-66" in result.stdout + result.stderr


def test_fast_jsonl_python_fallback_only_when_rust_unavailable(tmp_path: Path) -> None:
    fixture = tmp_path / "valid.jsonl"
    _write_jsonl(fixture, _valid_records())

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_jsonl.py",
            "--python-fallback",
            "--cargo-bin",
            "definitely-not-cargo-for-t424",
            "--require-canon",
            str(fixture),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "using Python fallback" in result.stderr


def test_validate_all_uses_fast_wrappers_for_heavy_canonical_scans() -> None:
    text = (ROOT / "scripts" / "validate_all.py").read_text(encoding="utf-8")

    assert "validate_fast_jsonl.py" in text
    assert "validate_fast_canonical_scope.py" in text
    assert "qa_canonical_corpus.py" in text
