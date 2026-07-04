from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts import validate_dad_outbox as validator


ROOT = Path(__file__).resolve().parents[1]
OUTBOX = ROOT / ".digital-asset" / "mail" / "outbox.jsonl"


def read_rows() -> list[dict]:
    return [json.loads(line) for line in OUTBOX.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def t424_row(rows: list[dict]) -> dict:
    for row in rows:
        if row.get("message_id") == validator.T424_MESSAGE_ID:
            return row
    raise AssertionError("missing T424 row")


def test_dad_outbox_validates_current_repo() -> None:
    rows = validator.validate_dad_outbox(OUTBOX)
    row = t424_row(rows)

    assert row["message_type"] == "lesson_and_asset_candidate"
    assert row["requires_local_adoption"] is True
    assert "asset-candidate:rust-first-coding-runtime-preflight" in row["asset_candidates"]


def test_dad_outbox_requires_t424_asset_candidates(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    row = t424_row(rows)
    row["asset_candidates"] = ["asset-candidate:rust-fast-validator-leaf-cli"]
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    with pytest.raises(validator.DadOutboxError, match="asset_candidates"):
        validator.validate_dad_outbox(candidate)


def test_dad_outbox_rejects_authority_leakage(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    row = t424_row(rows)
    row["non_authorizations"] = ["dad_override_local_authority"]
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    with pytest.raises(validator.DadOutboxError, match="non_authorizations"):
        validator.validate_dad_outbox(candidate)
