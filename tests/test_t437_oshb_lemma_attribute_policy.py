from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts import validate_t437_oshb_lemma_attribute_policy as validator


ROOT = Path(__file__).resolve().parents[1]


def test_t437_policy_validates_current_repo() -> None:
    result = validator.validate_t437_oshb_lemma_attribute_policy()

    assert result["oshb_included_rows"] == 39


def test_t437_rejects_allowlist_local_lemma_claim() -> None:
    source = validator._oshb_allowlist_source(ROOT)
    bad = copy.deepcopy(source)
    bad["contains_source_provided_lemmas"] = True

    with pytest.raises(validator.T437PolicyError, match="contains_source_provided_lemmas"):
        validator._require_policy(bad, "allowlist.openscriptures_oshb")


def test_t437_rejects_missing_strong_lookup_hint_policy() -> None:
    source = validator._oshb_allowlist_source(ROOT)
    bad = copy.deepcopy(source)
    bad["contains_source_provided_strong_lookup_hints"] = False

    with pytest.raises(validator.T437PolicyError, match="strong_lookup_hints"):
        validator._require_policy(bad, "allowlist.openscriptures_oshb")


def test_t437_rejects_t436_policy_regression() -> None:
    parity = validator._read_json(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/parity_summary.json"
    )
    bad = copy.deepcopy(parity)
    bad["metadata_policy_coverage"]["policy_covers_observed_lemma_attribute"] = False

    with pytest.raises(validator.T437PolicyError, match="policy_covers_observed_lemma_attribute"):
        validator.validate_t436_policy_coverage(bad)
