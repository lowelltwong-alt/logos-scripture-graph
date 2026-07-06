from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SENTINEL_TEXT = "SENTINEL_SECRET_BIBLE_TEXT_SHOULD_NOT_APPEAR"


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def _word_tokens() -> list[dict]:
    return [
        {
            "id": "word:eng-web:Matt.1.1:1",
            "book": "Matt",
            "osis_ref": "Matt.1.1",
            "translation_id": "eng-web",
            "source_file": "41-MAT.usfm",
            "source_line": 10,
            "word_index": 1,
            "surface_text": SENTINEL_TEXT,
            "nesting_context": ["p", "wj"],
            "strong": "G2424",
        },
        {
            "id": "word:eng-web:Matt.1.1:2",
            "book": "Matt",
            "osis_ref": "Matt.1.1",
            "translation_id": "eng-web",
            "source_file": "41-MAT.usfm",
            "source_line": 10,
            "word_index": 2,
            "surface_text": "said",
            "nesting_context": ["p", "wj"],
            "strong_ids": ["G3004"],
        },
        {
            "id": "word:eng-web:Matt.1.1:3",
            "book": "Matt",
            "osis_ref": "Matt.1.1",
            "translation_id": "eng-web",
            "source_file": "41-MAT.usfm",
            "source_line": 10,
            "word_index": 3,
            "surface_text": "narrator",
            "nesting_context": ["p"],
        },
        {
            "id": "word:eng-web:Gen.1.1:1",
            "book": "Gen",
            "osis_ref": "Gen.1.1",
            "translation_id": "eng-web",
            "source_file": "01-GEN.usfm",
            "source_line": 20,
            "word_index": 1,
            "surface_text": "beginning",
            "nesting_context": ["p"],
            "strong": "H7225",
        },
        {
            "id": "word:eng-web:John.3.16:1",
            "book": "John",
            "osis_ref": "John.3.16",
            "translation_id": "eng-web",
            "source_file": "43-JHN.usfm",
            "source_line": 30,
            "word_index": 1,
            "surface_text": "For",
            "nesting_context": ["p", "wj"],
            "strongs": ["G1063", "XOTHER"],
        },
    ]


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def test_fast_word_token_signals_matches_python_on_fixture(tmp_path: Path) -> None:
    fixture = tmp_path / "word_tokens.jsonl"
    _write_jsonl(fixture, _word_tokens())

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_word_token_signals.py",
            "--require-rust",
            "--compare-python",
            str(fixture),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Rust/Python word-token signal parity passed" in result.stdout


def test_fast_word_token_signals_summary_is_no_text(tmp_path: Path) -> None:
    fixture = tmp_path / "word_tokens.jsonl"
    summary = tmp_path / "summary.json"
    _write_jsonl(fixture, _word_tokens())

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_word_token_signals.py",
            "--require-rust",
            "--summary-json",
            str(summary),
            str(fixture),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = summary.read_text(encoding="utf-8")
    data = json.loads(text)
    assert data["non_authorizing"] is True
    assert data["no_text"] is True
    assert data["records"] == 5
    assert data["wj_word_tokens"] == 3
    assert data["wj_token_runs"] == 2
    assert data["strong_g_occurrences"] == 3
    assert data["strong_h_occurrences"] == 1
    assert data["strong_other_occurrences"] == 1
    assert SENTINEL_TEXT not in text
    assert "narrator" not in text


def test_fast_word_token_signals_does_not_fallback_after_rust_failure(tmp_path: Path) -> None:
    fixture = tmp_path / "wrong_translation.jsonl"
    records = _word_tokens()
    records[0]["translation_id"] = "other"
    _write_jsonl(fixture, records)

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_word_token_signals.py",
            "--python-fallback",
            str(fixture),
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode != 0
    assert "translation_id other != expected eng-web" in combined
    assert "using Python fallback" not in combined


def test_fast_word_token_signals_python_fallback_only_when_rust_unavailable(tmp_path: Path) -> None:
    fixture = tmp_path / "word_tokens.jsonl"
    _write_jsonl(fixture, _word_tokens())

    result = _run(
        [
            sys.executable,
            "scripts/validate_fast_word_token_signals.py",
            "--python-fallback",
            "--cargo-bin",
            "definitely-not-cargo-for-t459",
            str(fixture),
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "using Python fallback" in result.stderr


def test_validate_all_adds_word_token_signal_gate_when_tokens_exist(tmp_path: Path, monkeypatch) -> None:
    from scripts import validate_all

    word_tokens = tmp_path / "word_tokens.jsonl"
    _write_jsonl(word_tokens, _word_tokens())
    monkeypatch.setattr(validate_all, "WORD_TOKENS", word_tokens)
    monkeypatch.setattr(validate_all, "CANON_SCOPE_FILES", [])
    monkeypatch.setattr(validate_all, "SMALL_CANON", [])
    monkeypatch.setattr(validate_all, "QA_REQUIRED", [])

    gates = validate_all.build_gates()
    matching = [cmd for name, cmd in gates if name == "validate_fast_word_token_signals.py (canonical)"]

    assert matching
    assert "validate_fast_word_token_signals.py" in " ".join(matching[0])
    assert "--python-fallback" in matching[0]


def test_validate_all_uses_stack_tip_task_id(monkeypatch) -> None:
    from scripts import validate_all

    def fake_base_ref(task_id: str) -> str:
        if task_id == "T459":
            return "codex/t457-fast-canonical-qa"
        return "origin/main"

    monkeypatch.setattr(validate_all, "task_base_ref", fake_base_ref)

    assert validate_all.stack_tip_task_ids(["T457", "T459"]) == ["T459"]
    assert validate_all.stack_tip_task_ids(["T457", "T459", "T999"]) == ["T459", "T999"]


def test_validate_all_uses_explicit_integration_task(monkeypatch) -> None:
    from scripts import validate_all

    def fake_integrates(task_id: str) -> list[str]:
        if task_id == "T460":
            return ["T456", "T457", "T458", "T459"]
        return []

    monkeypatch.setattr(validate_all, "task_integrates_task_ids", fake_integrates)

    assert validate_all.integration_task_scope_ids(["T456", "T457", "T458", "T459", "T460"]) == ["T460"]
    assert validate_all.integration_task_scope_ids(["T456", "T457", "T460", "T999"]) == [
        "T456",
        "T457",
        "T460",
        "T999",
    ]
