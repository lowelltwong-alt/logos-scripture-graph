from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_john3_owner_review_docket as validator


def test_john3_owner_review_docket_validates_current_repo() -> None:
    data = validator.validate_john3_owner_review_docket()

    assert data["target"]["target_id"] == "john3_wj_speaker_boundary"
    assert data["target"]["passage"] == "John.3.1-John.3.36"
    assert data["owner_selection"]["owner_selection_status"] == "selected"
    assert data["owner_selection"]["selected_option"] == "JOHN3-T356-B"
    assert data["owner_selection"]["selected_parent"] == "John.3.1-John.3.36"
    assert data["owner_selection"]["selected_children"] == []
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["authority"]["authorizes_parent_only_review_target"] is True
    assert data["authority"]["authorizes_parent_span_as_reviewed_gold"] is False


def test_john3_owner_review_docket_has_all_owner_options() -> None:
    data = validator.validate_john3_owner_review_docket()
    options = {item["option_id"]: item for item in data["options"]}

    assert set(options) == validator.REQUIRED_OPTIONS
    assert options["JOHN3-T356-B"]["selected_parent_candidate"] == "John.3.1-John.3.36"
    assert options["JOHN3-T356-C"]["selected_parent_candidate"] == "John.3.1-John.3.36"
    assert any(
        child["span"] == "John.3.9-John.3.21"
        for child in options["JOHN3-T356-C"]["child_span_candidates"]
    )
    assert all(option["implementation_allowed_now"] is False for option in options.values())


def test_john3_owner_review_docket_rejects_authorizing_parent_span(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_john3_owner_review_docket())
    data["authority"]["authorizes_parent_span"] = True
    candidate = tmp_path / "john3.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.John3DocketError, match="authorizes_parent_span"):
        validator.validate_john3_owner_review_docket(candidate)


def test_john3_owner_review_docket_rejects_stale_pending_selection(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_john3_owner_review_docket())
    data["owner_selection"]["owner_selection_status"] = "pending"
    data["owner_selection"]["selected_option"] = "pending"
    candidate = tmp_path / "john3.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.John3DocketError, match="owner_selection_status"):
        validator.validate_john3_owner_review_docket(candidate)
