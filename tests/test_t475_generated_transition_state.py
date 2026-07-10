from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts.run_t475_shadow_delta import jsonl_stats
from scripts.validate_t475_generated_transition_state import (
    T475TransitionError,
    classify_counts,
    validate_allowed_state,
    validate_semantic_manifest,
)


def _write_jsonl(path: Path, records: list[dict]) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in records),
        encoding="utf-8",
    )
    return jsonl_stats(path, path.as_posix())


def test_classify_generated_transition_counts() -> None:
    assert classify_counts(677688, 1130) == "baseline"
    assert classify_counts(677686, 1127) == "candidate"
    assert classify_counts(677686, 1130) == "unknown"


def test_allowed_state_accepts_baseline_without_deferral(tmp_path: Path) -> None:
    word_tokens = tmp_path / "data/canonical/translations/eng-web/word_tokens.jsonl"
    footnotes = tmp_path / "data/canonical/translations/eng-web/footnotes.jsonl"
    word_tokens.parent.mkdir(parents=True)
    word_tokens.write_bytes(b"{}\n" * 677688)
    footnotes.write_bytes(b"{}\n" * 1130)
    assert validate_allowed_state(tmp_path) == {
        "state": "baseline",
        "surfaces": 0,
        "rows": 0,
        "deferred": [],
    }


def test_allowed_state_rejects_partial_transition(tmp_path: Path) -> None:
    word_tokens = tmp_path / "data/canonical/translations/eng-web/word_tokens.jsonl"
    footnotes = tmp_path / "data/canonical/translations/eng-web/footnotes.jsonl"
    word_tokens.parent.mkdir(parents=True)
    word_tokens.write_bytes(b"{}\n" * 677686)
    footnotes.write_bytes(b"{}\n" * 1130)
    with pytest.raises(T475TransitionError, match="neither the baseline nor the exact candidate"):
        validate_allowed_state(tmp_path)


def test_semantic_manifest_accepts_exact_candidate(tmp_path: Path) -> None:
    manifest_rows = []
    for index in range(10):
        rel = f"canonical/translations/eng-web/surface_{index}.jsonl"
        target = tmp_path / "data/canonical/translations/eng-web" / f"surface_{index}.jsonl"
        count, digest = _write_jsonl(target, [{"id": f"row-{index}", "value": index}])
        manifest_rows.append(
            {
                "path": rel,
                "row_count": count,
                "stable_key_digest": digest,
            }
        )
    manifest = tmp_path / "candidate_manifest.json"
    manifest.write_text(json.dumps({"files": manifest_rows}), encoding="utf-8")
    result = validate_semantic_manifest(tmp_path, manifest)
    assert result == {"surfaces": 10, "rows": 10}


def test_semantic_manifest_rejects_content_drift(tmp_path: Path) -> None:
    manifest_rows = []
    for index in range(10):
        rel = f"canonical/translations/eng-web/surface_{index}.jsonl"
        target = tmp_path / "data/canonical/translations/eng-web" / f"surface_{index}.jsonl"
        count, digest = _write_jsonl(target, [{"id": f"row-{index}", "value": index}])
        manifest_rows.append({"path": rel, "row_count": count, "stable_key_digest": digest})
    manifest = tmp_path / "candidate_manifest.json"
    manifest.write_text(json.dumps({"files": manifest_rows}), encoding="utf-8")
    _write_jsonl(
        tmp_path / "data/canonical/translations/eng-web/surface_4.jsonl",
        [{"id": "row-4", "value": "drift"}],
    )
    with pytest.raises(T475TransitionError, match="digest differs"):
        validate_semantic_manifest(tmp_path, manifest)


def test_validate_all_defers_only_declared_legacy_gates(monkeypatch) -> None:
    from scripts import validate_all

    monkeypatch.setattr(validate_all, "t475_candidate_transition_active", lambda: True)
    names = [name for name, _cmd in validate_all.build_gates()]
    assert "validate_t475_generated_transition_state.py" in names
    assert not (validate_all.T475_DEFERRED_GENERATED_GATES & set(names))
    assert "validate_t475_usfm_shadow_delta_gate.py --require-artifacts" in names
