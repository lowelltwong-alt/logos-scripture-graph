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


def test_dad_outbox_requires_existing_lesson_slot(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    row = t424_row(rows)
    row["lesson_learned_slot"] = ".digital-asset/lessons/missing_t424_slot.yaml"
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    with pytest.raises(validator.DadOutboxError, match="missing DAD lesson slot"):
        validator.validate_dad_outbox(candidate)


def test_dad_outbox_requires_existing_context_map_entry(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    rows.append(
        {
            "message_id": "msg-bad-missing-context",
            "direction": "outbound",
            "from_repo": "logos-scripture-graph",
            "to_hub": "dad://hub/Digital-Assett-Directory",
            "message_type": "lesson_candidate",
            "trust_zone": "candidate",
            "requires_local_adoption": True,
            "local_adoption_required": True,
            "task_id": "T425",
            "subject": "Bad missing context",
            "summary": "Points at a context-map entry that does not exist.",
            "context_map_entry": "ctx-missing-t425",
            "non_authorizations": ["dad_override_local_authority"],
        }
    )
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    with pytest.raises(validator.DadOutboxError, match="missing context_map_entry"):
        validator.validate_dad_outbox(candidate)


def test_dad_outbox_rejects_lesson_slot_message_mismatch(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    rows.append(
        {
            "message_id": "msg-bad-slot-mismatch",
            "direction": "outbound",
            "from_repo": "logos-scripture-graph",
            "to_hub": "dad://hub/Digital-Assett-Directory",
            "message_type": "lesson_candidate",
            "trust_zone": "candidate",
            "requires_local_adoption": True,
            "local_adoption_required": True,
            "task_id": "T425",
            "subject": "Bad slot mismatch",
            "summary": "Points at an existing slot owned by another message.",
            "lesson_learned_slot": ".digital-asset/lessons/t425_dad_lesson_slot_integrity.yaml",
            "non_authorizations": ["dad_override_local_authority"],
        }
    )
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    with pytest.raises(validator.DadOutboxError, match="source_outbox_message_id"):
        validator.validate_dad_outbox(candidate)


def test_dad_outbox_rejects_authority_leakage(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    row = t424_row(rows)
    row["non_authorizations"] = ["dad_override_local_authority"]
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    with pytest.raises(validator.DadOutboxError, match="non_authorizations"):
        validator.validate_dad_outbox(candidate)


def test_dad_outbox_accepts_additional_lesson_candidate_rows(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    rows.append(
        {
            "message_id": "msg-test-additional-lesson-candidate",
            "direction": "outbound",
            "from_repo": "logos-scripture-graph",
            "to_hub": "dad://hub/Digital-Assett-Directory",
            "message_type": "lesson_candidate",
            "trust_zone": "candidate",
            "requires_local_adoption": True,
            "local_adoption_required": True,
            "task_id": "T441",
            "subject": "T441 follow-up lesson",
            "summary": "Future owner-option roots must remain denied until selected.",
            "artifacts": [
                "scripts/validate_t441_rust_alignment_coverage_index.py",
                "tests/test_t441_rust_alignment_coverage_index.py",
            ],
            "non_authorizations": [
                "dad_override_local_authority",
                "production_root_opening",
                "theology_authority",
            ],
        }
    )
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    validated = validator.validate_dad_outbox(candidate)

    assert any(row["message_id"] == "msg-test-additional-lesson-candidate" for row in validated)


def test_dad_outbox_rejects_lesson_candidate_without_local_authority_denial(tmp_path: Path) -> None:
    rows = copy.deepcopy(read_rows())
    rows.append(
        {
            "message_id": "msg-bad-lesson",
            "direction": "outbound",
            "from_repo": "logos-scripture-graph",
            "to_hub": "dad://hub/Digital-Assett-Directory",
            "message_type": "lesson_candidate",
            "trust_zone": "candidate",
            "requires_local_adoption": True,
            "task_id": "T999",
            "subject": "Bad lesson",
            "summary": "Missing DAD authority boundary.",
            "non_authorizations": ["theology_authority"],
        }
    )
    candidate = tmp_path / "outbox.jsonl"
    write_jsonl(candidate, rows)

    with pytest.raises(validator.DadOutboxError, match="dad_override_local_authority"):
        validator.validate_dad_outbox(candidate)
