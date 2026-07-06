from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import validate_t433_phlm_alignment_pilot as validator


ROOT = Path(__file__).resolve().parents[1]


def test_t433_phlm_alignment_pilot_validates_current_repo() -> None:
    manifest = validator.validate_t433_phlm_alignment_pilot()

    assert manifest["source_id"] == "sblgnt"
    assert manifest["authority"]["authorizes_translation_judgment"] is False


def test_t433_builder_check_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_t433_phlm_alignment_pilot.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_t433_rejects_strongs_on_sblgnt_source_token() -> None:
    rows = validator._read_jsonl(
        ROOT / "data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/source_language_tokens.jsonl"
    )
    bad = copy.deepcopy(rows)
    bad[0]["strong_id"] = "G3972"

    with pytest.raises(validator.T433PilotError, match="Strong"):
        validator.validate_source_tokens(bad)


def test_t433_rejects_high_confidence_alignment() -> None:
    tokens = validator._read_jsonl(
        ROOT / "data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/source_language_tokens.jsonl"
    )
    alignments = validator._read_jsonl(
        ROOT / "data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/alignment_records.jsonl"
    )
    bad = copy.deepcopy(alignments)
    bad[0]["confidence"] = "high"

    with pytest.raises(validator.T433PilotError, match="confidence"):
        validator.validate_alignments(bad, {str(row["source_token_id"]) for row in tokens})


def test_t433_rejects_editorial_authority() -> None:
    tokens = validator._read_jsonl(
        ROOT / "data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/source_language_tokens.jsonl"
    )
    layers = validator._read_jsonl(
        ROOT / "data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/editorial_layers.jsonl"
    )
    bad = copy.deepcopy(layers)
    bad[0]["authority"]["authorizes_chunk_boundary"] = True

    with pytest.raises(validator.T433PilotError, match="authorizes_chunk_boundary"):
        validator.validate_editorial_layers(bad, {str(row["source_token_id"]) for row in tokens})
