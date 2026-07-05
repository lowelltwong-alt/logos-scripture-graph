from __future__ import annotations

import copy

import pytest

from scripts import validate_t440_jonah_hebrew_parser_contract as validator


def test_t440_parser_contract_validates_current_repo() -> None:
    control = validator.validate_t440_jonah_hebrew_parser_contract()

    assert control["rust_policy"]["rust_added_in_t440"] is False
    assert control["rust_policy"]["t441_may_design_no_text_rust_checker_after_t440"] is True


def test_t440_rejects_raw_archive_source_view_path() -> None:
    control = validator.validate_t440_jonah_hebrew_parser_contract()
    bad = copy.deepcopy(control)
    bad["parser_contracts"][0]["source_view_path"] = "data/raw/original_language/hebrew/tanach_us_uxlc/raw/Tanach.xml.zip"

    with pytest.raises(validator.T440ParserContractError, match="canonical source views"):
        validator.validate_source_contracts(bad)


def test_t440_rejects_oshb_lemma_as_local_lemma_authority() -> None:
    control = validator.validate_t440_jonah_hebrew_parser_contract()
    bad = copy.deepcopy(control)
    oshb = next(row for row in bad["parser_contracts"] if row["source_id"] == "openscriptures_oshb")
    oshb["token_attribute_semantics"]["contains_source_provided_lemmas"] = True

    with pytest.raises(validator.T440ParserContractError, match="contains_source_provided_lemmas"):
        validator.validate_source_contracts(bad)


def test_t440_rejects_rust_scanner_inside_t440() -> None:
    control = validator.validate_t440_jonah_hebrew_parser_contract()
    bad = copy.deepcopy(control)
    bad["rust_policy"]["rust_scanner_allowed_inside_t440"] = True

    with pytest.raises(validator.T440ParserContractError, match="rust_scanner_allowed_inside_t440"):
        validator.validate_rust_policy(bad)


def test_t440_requires_negative_fixture_for_count_semantics() -> None:
    control = validator.validate_t440_jonah_hebrew_parser_contract()
    bad = copy.deepcopy(control)
    bad["negative_fixture_requirements"] = [
        row for row in bad["negative_fixture_requirements"] if row["id"] != "reject_count_match_as_semantic_parity"
    ]

    with pytest.raises(validator.T440ParserContractError, match="reject_count_match_as_semantic_parity"):
        validator.validate_negative_fixture_requirements(bad)


def test_t440_rejects_visible_hebrew_text_in_contract() -> None:
    control = validator.validate_t440_jonah_hebrew_parser_contract()
    bad = copy.deepcopy(control)
    bad["parser_contracts"][0]["authority_note"] = "visible Hebrew leak: \u05d9\u05d5\u05e0\u05d4"

    with pytest.raises(validator.T440ParserContractError, match="visible Greek/Hebrew text"):
        validator._reject_visible_biblical_text(bad, "control")
