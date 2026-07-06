from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts import validate_t435_original_language_observation_scanner as validator


ROOT = Path(__file__).resolve().parents[1]


def test_t435_contract_validates_current_repo() -> None:
    validator.validate_contract()


def test_t435_rejects_authority_true() -> None:
    row = {
        "authority": {"authorizes_source_language_truth": True},
        "text_storage_policy": {"no_text": True, "stores_source_text": False},
    }

    with pytest.raises(validator.T435ValidationError, match="authorizes_source_language_truth"):
        validator._require_authority_false(row, "row")


def test_t435_rejects_text_bearing_keys() -> None:
    row = {
        "surface_text": "Παῦλος",
        "authority": {"authorizes_source_language_truth": False},
        "text_storage_policy": {"no_text": True, "stores_source_text": False},
    }

    with pytest.raises(validator.T435ValidationError, match="surface_text"):
        validator._require_no_forbidden_keys(row, "row")


def test_t435_rejects_strongs_population_for_sblgnt_token() -> None:
    included = validator._included_by_view_path()
    source_view_path, included_row = next(iter(included.items()))
    row = {
        "id": "t435:source-token-shape:sblgnt:Phlm.1.1:000001",
        "type": "SblgntSourceTokenShapeObservation",
        "schema_version": "original_language_observation_scanner.v1",
        "task_id": "T435",
        "source_id": "sblgnt",
        "source_view_path": source_view_path,
        "source_file_sha256": included_row["sha256"],
        "source_archive_path": included_row["source_archive_path"],
        "language": "greek",
        "book_id": included_row["book_id"],
        "osis_ref": f"{included_row['book_id']}.1.1",
        "verse_token_index": 1,
        "content_sha256_short": "abc123",
        "content_char_count": 6,
        "strong_id": "G3972",
        "lemma": None,
        "morphology": None,
        "contains_source_provided_lemmas": False,
        "contains_source_provided_morphology": False,
        "contains_source_provided_strongs": False,
        "evidence_mode": "observed_source_view_shape",
        "inferred_vs_observed": "observed",
        "trust_zone": "candidate",
        "status": "observation_shadow",
        "text_storage_policy": {"no_text": True, "stores_source_text": False},
        "authority": {"authorizes_source_language_truth": False},
    }

    with pytest.raises(validator.T435ValidationError, match="strong_id"):
        validator._validate_tokens([row], included)


def test_t435_rejects_incomplete_generated_ledgers(tmp_path: Path) -> None:
    output = tmp_path / "out"
    output.mkdir()
    manifest = {
        "object_type": "t435_sblgnt_observation_scan_manifest",
        "schema_version": "original_language_observation_scanner.v1",
        "source_id": "sblgnt",
        "language": "greek",
        "no_authority": True,
        "no_text": True,
        "output_files": sorted(validator.EXPECTED_OUTPUT_FILES),
        "row_counts": {
            "source_view_file_observations": 99,
            "verse_token_observations": 0,
            "source_token_shape_index": 0,
            "editorial_layer_shape_index": 0,
        },
        "text_storage_policy": {"no_text": True, "stores_source_text": False},
        "authority": {"authorizes_source_language_truth": False},
    }
    (output / "scan_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    for name in (
        "source_view_file_observations.jsonl",
        "verse_token_observations.jsonl",
        "source_token_shape_index.jsonl",
        "editorial_layer_shape_index.jsonl",
    ):
        (output / name).write_text("", encoding="utf-8")
    (output / "t433_shadow_parity.json").write_text(
        json.dumps(
            {
                "status": "pass",
                "rust_source_token_shapes": 41,
                "t433_source_language_tokens": 41,
                "rust_editorial_shapes": 7,
                "t433_editorial_layers": 7,
                "authority": {"authorizes_source_language_truth": False},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(validator.T435ValidationError, match="editorial rows missing"):
        validator.validate_generated(output)


def test_t435_validate_all_uses_contract_mode_only() -> None:
    text = (ROOT / "scripts" / "validate_all.py").read_text(encoding="utf-8")

    assert "validate_t435_original_language_observation_scanner.py" in text
    assert "cargo run --manifest-path tools/original_language_observation_scanner" not in text
