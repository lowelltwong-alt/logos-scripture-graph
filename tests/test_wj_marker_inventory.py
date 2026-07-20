from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import build_wj_marker_inventory as builder
from scripts import validate_wj_marker_inventory as validator

pytestmark = pytest.mark.generated_data(
    "data/canonical/translations/eng-web/word_tokens.jsonl"
)


@pytest.fixture(scope="module")
def built_inventory() -> dict:
    return builder.build_inventory()


def test_wj_marker_inventory_passes_current_repo() -> None:
    data = validator.validate_wj_marker_inventory()
    assert data["authority"]["authorizes_jesus_speaker_attribution"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False


def test_wj_marker_inventory_builder_is_deterministic(built_inventory: dict) -> None:
    assert built_inventory == builder.build_inventory()


def test_wj_marker_inventory_counts_current_wj_evidence(built_inventory: dict) -> None:
    data = built_inventory
    assert data["summary"]["wj_word_tokens"] == 38094
    assert data["summary"]["wj_token_runs"] == 675
    assert data["summary"]["books_with_wj"] == ["Matt", "Mark", "Luke", "John", "Acts", "1Cor", "2Cor", "1Tim", "Rev"]

    books = {item["book"]: item for item in data["book_summaries"]}
    assert books["Matt"]["wj_word_tokens"] == 12296
    assert books["John"]["wj_word_tokens"] == 7738
    assert books["Rev"]["wj_word_tokens"] == 1725
    assert books["1Cor"]["wj_word_tokens"] == 33


def test_wj_marker_inventory_records_known_review_cases(built_inventory: dict) -> None:
    data = built_inventory
    cases = {item["case_id"]: item for item in data["known_review_cases"]}

    assert cases["john3_wj_speaker_boundary"]["review_status"] == "pending_human_review"
    assert cases["matt5_7_sermon_on_mount_wj_discourse"]["review_status"] == "pending_human_review"
    assert cases["john13_17_wj_farewell_discourse_marker_focus"]["recommended_next_step"] == "define_speaker_policy_before_gold"
    for case in cases.values():
        assert case["implementation_allowed"] is False
        assert case["wj_word_token_refs_count"] > 0


def test_wj_marker_inventory_rejects_authorizing_policy(tmp_path: Path, built_inventory: dict) -> None:
    data = copy.deepcopy(built_inventory)
    data["authority"]["authorizes_speaker_boundary"] = True
    candidate = tmp_path / "wj.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.WJMarkerInventoryError, match="authorizes_speaker_boundary"):
        validator.validate_wj_marker_inventory(candidate)


def test_wj_marker_inventory_rejects_stale_counts(tmp_path: Path, built_inventory: dict) -> None:
    data = copy.deepcopy(built_inventory)
    data["summary"]["wj_word_tokens"] += 1
    candidate = tmp_path / "wj.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.WJMarkerInventoryError, match="wj_word_tokens"):
        validator.validate_wj_marker_inventory(candidate)
