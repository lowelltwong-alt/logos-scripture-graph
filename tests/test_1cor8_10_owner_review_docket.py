from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_1cor8_10_owner_review_docket as validator


def test_1cor8_10_owner_review_docket_validates_current_repo() -> None:
    data = validator.validate_1cor8_10_owner_review_docket()

    assert data["target"]["target_id"] == "1cor8_10_food_offered_to_idols"
    assert data["target"]["exact_parent_candidate"] == "1Cor.8.1-1Cor.10.33"
    assert data["owner_selection"]["owner_selection_status"] == "selected"
    assert data["owner_selection"]["selection_mode"] == "projected_owner_pattern"
    assert data["owner_selection"]["selected_option"] == "1COR8-10-T369-B"
    assert data["owner_selection"]["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["owner_selection"]["selected_children"] == []
    assert data["authority"]["authorizes_parent_only_review_target"] is True
    assert data["authority"]["authorizes_reviewed_gold"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["authority"]["authorizes_output_change"] is False


def test_1cor8_10_owner_review_docket_has_all_owner_options() -> None:
    data = validator.validate_1cor8_10_owner_review_docket()
    options = {item["option_id"]: item for item in data["options"]}

    assert set(options) == validator.REQUIRED_OPTIONS
    assert options["1COR8-10-T369-B"]["selected_parent_candidate"] == "1Cor.8.1-1Cor.10.33"
    assert options["1COR8-10-T369-C"]["selected_parent_candidate"] == "1Cor.8.1-1Cor.10.33"
    child_spans = {
        child["span"]
        for child in options["1COR8-10-T369-C"]["child_span_candidates"]
    }
    assert "1Cor.10.14-1Cor.10.22" in child_spans
    assert all(option["implementation_allowed_now"] is False for option in options.values())


def test_1cor8_10_owner_review_docket_rejects_authorizing_reviewed_gold(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_1cor8_10_owner_review_docket())
    data["authority"]["authorizes_reviewed_gold"] = True
    candidate = tmp_path / "1cor.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.OneCorDocketError, match="authorizes_reviewed_gold"):
        validator.validate_1cor8_10_owner_review_docket(candidate)


def test_1cor8_10_owner_review_docket_rejects_premature_selection(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_1cor8_10_owner_review_docket())
    data["owner_selection"]["selected_option"] = "1COR8-10-T369-C"
    data["owner_selection"]["selected_children"] = ["1Cor.8.1-1Cor.8.13"]
    candidate = tmp_path / "1cor.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.OneCorDocketError, match="selected_option"):
        validator.validate_1cor8_10_owner_review_docket(candidate)
