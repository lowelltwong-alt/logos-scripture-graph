from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from pipelines.util.canonical_scope import canonical_66_books
from scripts.qa_canonical_corpus import GLOSSARY_REL, PASSAGES_REL, SIDECAR_RELS, WITNESSES_REL, WORD_TOKENS_REL


ROOT = Path(__file__).resolve().parents[1]


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def _write_canonical_fixture(root: Path) -> None:
    passages = []
    witnesses = []
    word_tokens = []
    for book in canonical_66_books():
        osis_ref = "Acts.8.37" if book == "Acts" else f"{book}.1.1"
        passage_id = f"scripture:{osis_ref}"
        passages.append({"id": passage_id, "book": book, "osis_ref": osis_ref})
        witnesses.append(
            {
                "id": f"translation-witness:eng-web:{osis_ref}",
                "book": book,
                "osis_ref": osis_ref,
                "passage_id": passage_id,
                "text": "" if osis_ref == "Acts.8.37" else f"{book} fixture text.",
            }
        )
        if osis_ref != "Acts.8.37":
            word_tokens.append(
                {
                    "id": f"word-token:{osis_ref}:1",
                    "book": book,
                    "osis_ref": osis_ref,
                    "passage_id": passage_id,
                }
            )

    _write_jsonl(root / PASSAGES_REL, passages)
    _write_jsonl(root / WITNESSES_REL, witnesses)
    for rel in SIDECAR_RELS:
        _write_jsonl(root / rel, [])
    _write_jsonl(
        root / "translations" / "eng-web" / "footnotes.jsonl",
        [
            {
                "id": "footnote:eng-web:Acts.8.37:0001",
                "book": "Acts",
                "osis_ref": "Acts.8.37",
                "passage_id": "scripture:Acts.8.37",
                "text": "Textual variant fixture footnote.",
            }
        ],
    )
    _write_jsonl(root / GLOSSARY_REL, [])
    _write_jsonl(root / WORD_TOKENS_REL, word_tokens)


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def test_fast_canonical_qa_agrees_with_python_on_valid_fixture(tmp_path: Path) -> None:
    _write_canonical_fixture(tmp_path)

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_canonical_qa.py",
            "--require-rust",
            "--compare-python",
            "--canonical-root",
            str(tmp_path),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Fast canonical corpus QA passed" in result.stdout
    assert "Rust/Python canonical QA verdict parity passed" in result.stdout


def test_fast_canonical_qa_rejects_missing_witness_alignment(tmp_path: Path) -> None:
    _write_canonical_fixture(tmp_path)
    witnesses = [
        json.loads(line)
        for line in (tmp_path / WITNESSES_REL).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    _write_jsonl(tmp_path / WITNESSES_REL, witnesses[:-1])

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_canonical_qa.py",
            "--require-rust",
            "--compare-python",
            "--canonical-root",
            str(tmp_path),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "translation_witnesses count" in combined
    assert "Rust/Python canonical QA verdict parity passed" in combined


def test_fast_canonical_qa_rejects_authority_like_glossary_entry(tmp_path: Path) -> None:
    _write_canonical_fixture(tmp_path)
    _write_jsonl(tmp_path / GLOSSARY_REL, [{"id": "glossary:abba", "term": "Abba"}])

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_canonical_qa.py",
            "--require-rust",
            "--compare-python",
            "--canonical-root",
            str(tmp_path),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "not explicitly marked non-Scripture" in combined
    assert "Rust/Python canonical QA verdict parity passed" in combined


def test_validate_all_uses_fast_canonical_qa_wrapper() -> None:
    from scripts import validate_all

    gates = validate_all.build_gates()
    names = [name for name, _ in gates]

    assert "validate_fast_canonical_qa.py (canonical)" in names or "qa_canonical_corpus.py" not in names
