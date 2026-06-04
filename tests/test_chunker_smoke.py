"""Smoke tests for the v0 chunker (regression guard for CHK-4).

CHK-4 was a hard crash (`KeyError: 'translation_witness'`) when the chunker met
the T201 passage/witness split. These tests assert the join works and no raw
USFM markup leaks into chunk text.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKER = ROOT / "pipelines" / "chunking" / "chunker.py"
RAW_USFM_RE = re.compile(r"\\(?:\+?[A-Za-z0-9]+)\*?")

PASSAGES = [
    {"id": "scripture:John.1.1", "type": "ScripturePassage", "osis_ref": "John.1.1", "book": "John"},
    {"id": "scripture:John.1.2", "type": "ScripturePassage", "osis_ref": "John.1.2", "book": "John"},
    {"id": "scripture:John.1.3", "type": "ScripturePassage", "osis_ref": "John.1.3", "book": "John"},
]
WITNESSES = [
    {"id": "w1", "type": "TranslationWitness", "passage_id": "scripture:John.1.1",
     "osis_ref": "John.1.1", "text": "In the beginning was the Word."},
    {"id": "w2", "type": "TranslationWitness", "passage_id": "scripture:John.1.2",
     "osis_ref": "John.1.2", "text": "The same was in the beginning with God."},
    {"id": "w3", "type": "TranslationWitness", "passage_id": "scripture:John.1.3",
     "osis_ref": "John.1.3", "text": "All things were made through him."},
]


def _write_jsonl(path: Path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def test_chunker_joins_passages_and_witnesses(tmp_path):
    passages = tmp_path / "passages.jsonl"
    witnesses = tmp_path / "witnesses.jsonl"
    out = tmp_path / "chunks.jsonl"
    _write_jsonl(passages, PASSAGES)
    _write_jsonl(witnesses, WITNESSES)

    result = subprocess.run(
        [sys.executable, str(CHUNKER),
         "--passages", str(passages), "--witnesses", str(witnesses), "--out", str(out)],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "KeyError" not in result.stderr

    chunks = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(chunks) >= 1
    for chunk in chunks:
        assert chunk["type"] == "RetrievalChunk"
        assert chunk["text"], "chunk text must not be empty"
        assert not RAW_USFM_RE.search(chunk["text"]), "chunk text leaked raw USFM"
        assert chunk["boundary_basis"]
        assert chunk["osis_start"] and chunk["osis_end"]


def test_chunker_text_comes_from_witness(tmp_path):
    passages = tmp_path / "passages.jsonl"
    witnesses = tmp_path / "witnesses.jsonl"
    out = tmp_path / "chunks.jsonl"
    _write_jsonl(passages, PASSAGES)
    _write_jsonl(witnesses, WITNESSES)

    subprocess.run(
        [sys.executable, str(CHUNKER),
         "--passages", str(passages), "--witnesses", str(witnesses), "--out", str(out)],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    combined = " ".join(
        json.loads(line)["text"]
        for line in out.read_text(encoding="utf-8").splitlines() if line.strip()
    )
    assert "In the beginning was the Word." in combined
