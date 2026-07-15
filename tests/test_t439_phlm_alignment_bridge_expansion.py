from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import validate_t439_phlm_alignment_bridge_expansion as validator


ROOT = Path(__file__).resolve().parents[1]


def test_t439_phlm_alignment_bridge_expansion_validates_current_repo() -> None:
    manifest = validator.validate_t439_phlm_alignment_bridge_expansion()

    assert manifest["counts"]["source_language_tokens"] == 334
    assert manifest["counts"]["alignment_records"] == 25
    assert manifest["no_text_policy"]["stores_source_text"] is False


@pytest.mark.generated_data("data/canonical/translations/eng-web/word_tokens.jsonl")
def test_t439_generated_parity_builder_check_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_t439_phlm_alignment_bridge_expansion.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_t439_rejects_source_token_text_leak() -> None:
    row = validator._read_jsonl(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion/source_language_tokens.jsonl"
    )[0]
    bad = copy.deepcopy(row)
    bad["surface_text"] = "Παῦλος"

    with pytest.raises(validator.T439PilotError, match="surface_text"):
        validator._reject_text_leak(bad, "bad-token")


def test_t439_rejects_source_strong_population() -> None:
    rows = validator._read_jsonl(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion/source_language_tokens.jsonl"
    )
    bad_rows = copy.deepcopy(rows)
    bad_rows[0]["strong_id"] = "G3972"

    with pytest.raises(validator.T439PilotError, match="Strong"):
        validator.validate_source_tokens(bad_rows)


def test_t439_rejects_alignment_confidence_upgrade() -> None:
    tokens = validator._read_jsonl(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion/source_language_tokens.jsonl"
    )
    by_ref = validator.validate_source_tokens(tokens)
    rows = validator._read_jsonl(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion/alignment_records.jsonl"
    )
    bad_rows = copy.deepcopy(rows)
    bad_rows[0]["confidence"] = "medium"

    with pytest.raises(validator.T439PilotError, match="low-confidence"):
        validator.validate_alignments(bad_rows, by_ref)


def test_t439_rejects_unredacted_editorial_value() -> None:
    rows = validator._read_jsonl(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion/editorial_layers.jsonl"
    )
    bad_rows = copy.deepcopy(rows)
    bad_rows[0]["observed_value"] = "·"

    token_rows = validator._read_jsonl(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion/source_language_tokens.jsonl"
    )
    by_ref = validator.validate_source_tokens(token_rows)
    source_token_ids = {token_id for token_ids in by_ref.values() for token_id in token_ids}

    with pytest.raises(validator.T439PilotError, match="redacted"):
        validator.validate_editorial_layers(bad_rows, source_token_ids)
