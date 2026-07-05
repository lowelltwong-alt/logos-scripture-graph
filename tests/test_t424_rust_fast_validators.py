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


def _chunk_record(
    *,
    book: str = "Phlm",
    span: str = "Phlm.1.1-Phlm.1.3",
    chunk_index: int = 1,
    decision_id: str = "M6-Phlm-001",
    model_id: str = "M6_fable5",
) -> dict:
    return {
        "model_id": model_id,
        "book": book,
        "span": span,
        "chunk_index_in_book": chunk_index,
        "literature_type_guess": "epistle_greeting",
        "boundary_evidence_refs": ["book_strategy:Phlm"],
        "strong_or_hebrew_tags_used": False,
        "wj_or_red_letter_considered": False,
        "confidence": "medium",
        "decision_id": decision_id,
        "non_authorizing": True,
    }


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


def test_fast_jsonl_matches_python_on_empty_canon_profiles(tmp_path: Path) -> None:
    fixture = tmp_path / "empty_canon_profiles.jsonl"
    records = _valid_records()
    records[0]["canon_profiles"] = []
    _write_jsonl(fixture, records)

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

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "missing canon_profiles" in combined
    assert "Rust/Python JSONL validator verdict parity passed" in combined


def test_fast_jsonl_matches_python_on_null_canon_profiles(tmp_path: Path) -> None:
    fixture = tmp_path / "null_canon_profiles.jsonl"
    records = _valid_records()
    records[0]["canon_profiles"] = None
    _write_jsonl(fixture, records)

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

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "missing canon_profiles" in combined
    assert "Rust/Python JSONL validator verdict parity passed" in combined


def test_fast_jsonl_matches_python_on_missing_witness_passage_id(tmp_path: Path) -> None:
    fixture = tmp_path / "missing_passage_id.jsonl"
    records = _valid_records()
    records[1].pop("passage_id")
    _write_jsonl(fixture, records)

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

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "points to missing ScripturePassage" in combined
    assert "Rust/Python JSONL validator verdict parity passed" in combined


def test_fast_jsonl_matches_python_on_unknown_witness_passage_id(tmp_path: Path) -> None:
    fixture = tmp_path / "unknown_passage_id.jsonl"
    records = _valid_records()
    records[1]["passage_id"] = "scripture:Gen.99.99"
    _write_jsonl(fixture, records)

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

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "points to missing ScripturePassage" in combined
    assert "Rust/Python JSONL validator verdict parity passed" in combined


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


def test_fast_canonical_scope_rejects_custom_canon_with_python_compare(tmp_path: Path) -> None:
    fixture = tmp_path / "valid.jsonl"
    custom_canon = tmp_path / "custom_canon.yaml"
    _write_jsonl(fixture, _valid_records())
    custom_canon.write_text("canonical_66_books: []\nexcluded_books: []\n", encoding="utf-8")

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_canonical_scope.py",
            "--require-rust",
            "--compare-python",
            "--canon",
            str(custom_canon),
            str(fixture),
        ]
    )

    assert result.returncode != 0
    assert "Custom --canon is not supported" in result.stderr


def test_fast_chunk_map_agrees_with_python_on_valid_fixture(tmp_path: Path) -> None:
    fixture = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_jsonl(
        fixture,
        [
            _chunk_record(span="Phlm.1.1-Phlm.1.3", chunk_index=1, decision_id="M6-Phlm-001"),
            _chunk_record(span="Phlm.1.4-Phlm.1.7", chunk_index=2, decision_id="M6-Phlm-002"),
        ],
    )

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_chunk_map.py",
            "--require-rust",
            "--compare-python",
            "--model-id",
            "M6_fable5",
            "--book",
            "Phlm",
            str(fixture),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Rust/Python chunk-map validator verdict parity passed" in result.stdout


def test_fast_chunk_map_rejects_non_authorizing_false(tmp_path: Path) -> None:
    fixture = tmp_path / "whole_bible_chunk_map.jsonl"
    record = _chunk_record()
    record["non_authorizing"] = False
    _write_jsonl(fixture, [record])

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_chunk_map.py",
            "--require-rust",
            "--compare-python",
            str(fixture),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "non_authorizing must be true" in combined
    assert "Rust/Python chunk-map validator verdict parity passed" in combined


def test_fast_chunk_map_rejects_duplicate_decision_id(tmp_path: Path) -> None:
    fixture = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_jsonl(
        fixture,
        [
            _chunk_record(span="Phlm.1.1-Phlm.1.3", chunk_index=1, decision_id="dup"),
            _chunk_record(span="Phlm.1.4-Phlm.1.7", chunk_index=2, decision_id="dup"),
        ],
    )

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_chunk_map.py",
            "--require-rust",
            "--compare-python",
            str(fixture),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "duplicate decision_id dup" in combined
    assert "Rust/Python chunk-map validator verdict parity passed" in combined


def test_fast_chunk_map_rejects_overlap_and_noncontiguous_indices(tmp_path: Path) -> None:
    fixture = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_jsonl(
        fixture,
        [
            _chunk_record(span="Phlm.1.1-Phlm.1.5", chunk_index=1, decision_id="M6-Phlm-001"),
            _chunk_record(span="Phlm.1.4-Phlm.1.7", chunk_index=3, decision_id="M6-Phlm-002"),
        ],
    )

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_chunk_map.py",
            "--require-rust",
            "--compare-python",
            str(fixture),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "chunk_index_in_book must be contiguous" in combined
    assert "overlaps or inverts order" in combined
    assert "Rust/Python chunk-map validator verdict parity passed" in combined


def test_fast_chunk_map_rejects_allowed_book_scope_mismatch(tmp_path: Path) -> None:
    fixture = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_jsonl(fixture, [_chunk_record(book="Jonah", span="Jonah.1.1-Jonah.1.3")])

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_chunk_map.py",
            "--require-rust",
            "--compare-python",
            "--book",
            "Phlm",
            str(fixture),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "not in allowed scope" in combined
    assert "Rust/Python chunk-map validator verdict parity passed" in combined


def test_fast_chunk_map_rejects_missing_full_bible_coverage(tmp_path: Path) -> None:
    fixture = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_jsonl(fixture, [_chunk_record()])

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_chunk_map.py",
            "--require-rust",
            "--compare-python",
            "--require-full-bible",
            str(fixture),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "missing books" in combined
    assert "Rust/Python chunk-map validator verdict parity passed" in combined


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


def test_fast_chunk_map_python_fallback_only_when_rust_unavailable(tmp_path: Path) -> None:
    fixture = tmp_path / "whole_bible_chunk_map.jsonl"
    _write_jsonl(fixture, [_chunk_record()])

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_chunk_map.py",
            "--python-fallback",
            "--cargo-bin",
            "definitely-not-cargo-for-t424",
            str(fixture),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "using Python fallback" in result.stderr


def test_validate_all_uses_fast_wrappers_for_heavy_canonical_scans() -> None:
    from scripts import validate_all

    gates = validate_all.build_gates()
    fast_gates = [(name, cmd) for name, cmd in gates if "validate_fast_" in name]
    qa_gates = [(name, cmd) for name, cmd in gates if name == "qa_canonical_corpus.py"]

    assert {name for name, _ in fast_gates} >= {
        "validate_fast_canonical_scope.py (canonical)",
        "validate_fast_jsonl.py (canonical)",
    }
    assert all("(canonical)" in name for name, _ in fast_gates)
    assert qa_gates
    assert all("validate_fast_" not in " ".join(cmd) for _, cmd in qa_gates)
