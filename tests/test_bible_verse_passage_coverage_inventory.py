from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import validate_bible_verse_passage_coverage_inventory as validator


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_inventory.jsonl"


def test_t386_bible_verse_passage_coverage_inventory_validates_current_repo() -> None:
    result = validator.validate_bible_verse_passage_coverage_inventory(
        check_repo_wiring=False,
    )

    assert result["record_count"] == 31103
    assert set(result["status_counts"]) == validator.REQUIRED_STATUS
    assert result["flag_counts"]["source_metadata_sensitive"] > 30000
    assert result["flag_counts"]["review_packet_needed"] > 0
    assert result["flag_counts"]["speaker_wj_red_letter_discourse_boundary_risk"] > 0
    assert result["flag_counts"]["known_non_orthodox_pressure_passage"] > 0
    assert result["owner_decision_counts"]["T386-HDM-007"] > 0


def test_t386_current_repo_wiring_is_present() -> None:
    result = validator.validate_bible_verse_passage_coverage_inventory()

    assert result["record_count"] == 31103


def test_t386_rejects_missing_canonical_record(tmp_path: Path) -> None:
    candidate = tmp_path / "missing-record.jsonl"
    with INVENTORY.open(encoding="utf-8") as source, candidate.open("w", encoding="utf-8", newline="\n") as target:
        for line_number, line in enumerate(source, start=1):
            if line_number == 1:
                continue
            target.write(line)

    with pytest.raises(validator.CoverageInventoryError, match="missing coverage"):
        validator.validate_bible_verse_passage_coverage_inventory(
            candidate,
            check_generated_summaries=False,
            check_repo_wiring=False,
        )


def test_t386_rejects_duplicate_canonical_record(tmp_path: Path) -> None:
    candidate = tmp_path / "duplicate-record.jsonl"
    with INVENTORY.open(encoding="utf-8") as source, candidate.open("w", encoding="utf-8", newline="\n") as target:
        first = source.readline()
        target.write(first)
        target.write(first)
        for line in source:
            target.write(line)

    with pytest.raises(validator.CoverageInventoryError, match="duplicate coverage record"):
        validator.validate_bible_verse_passage_coverage_inventory(
            candidate,
            check_generated_summaries=False,
            check_repo_wiring=False,
        )


def test_t386_rejects_blocked_record_marked_routine(tmp_path: Path) -> None:
    candidate = tmp_path / "blocked-as-routine.jsonl"
    changed = False
    with INVENTORY.open(encoding="utf-8") as source, candidate.open("w", encoding="utf-8", newline="\n") as target:
        for line in source:
            row = json.loads(line)
            if not changed and "blocked_authority_action" in row["flags"]:
                row["coverage_status"] = "routine_under_existing_policy"
                changed = True
            target.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    assert changed
    with pytest.raises(validator.CoverageInventoryError, match="blocked_authority_action"):
        validator.validate_bible_verse_passage_coverage_inventory(
            candidate,
            check_generated_summaries=False,
            check_repo_wiring=False,
        )
