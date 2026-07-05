from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import validate_t436_jonah_hebrew_metadata_pilot as validator


ROOT = Path(__file__).resolve().parents[1]


def test_t436_jonah_hebrew_metadata_pilot_validates_current_repo() -> None:
    manifest = validator.validate_t436_jonah_hebrew_metadata_pilot()

    assert manifest["no_text_ledgers"] is True
    assert manifest["metadata_flag_drift"]["requires_policy_before_rust_expansion"] is True


def test_t436_builder_check_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_t436_jonah_hebrew_metadata_pilot.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_t436_rejects_per_verse_parity_drift() -> None:
    rows = validator._read_jsonl(
        ROOT
        / "data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/verse_token_observations.jsonl"
    )
    bad = copy.deepcopy(rows)
    for row in bad:
        if row["source_id"] == "openscriptures_oshb" and row["osis_ref"] == "Jonah.1.1":
            row["token_count"] += 1
            break

    with pytest.raises(validator.T436PilotError, match="token-count drift|source_token_ids"):
        validator.validate_verse_rows(bad)


def test_t436_rejects_oshb_lemma_copied_to_local_field() -> None:
    rows = validator._read_jsonl(
        ROOT / "data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/token_shape_index.jsonl"
    )
    bad = copy.deepcopy(rows)
    for row in bad:
        if row["source_id"] == "openscriptures_oshb":
            row["strong_id"] = "H3068"
            break

    with pytest.raises(validator.T436PilotError, match="forbidden text/value key strong_id"):
        validator.validate_token_rows(bad)


def test_t436_rejects_text_leakage() -> None:
    rows = validator._read_jsonl(
        ROOT / "data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/token_shape_index.jsonl"
    )
    bad = copy.deepcopy(rows)
    bad[0]["surface_text"] = "יונה"

    with pytest.raises(validator.T436PilotError, match="forbidden text/value key surface_text"):
        validator.validate_token_rows(bad)


def test_t436_rejects_rust_expansion_allowed() -> None:
    summary = validator._read_json(
        ROOT / "data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/parity_summary.json"
    )
    bad = copy.deepcopy(summary)
    bad["rust_expansion_allowed"] = True

    with pytest.raises(validator.T436PilotError, match="must not allow Rust expansion"):
        validator.validate_parity_summary(bad)
