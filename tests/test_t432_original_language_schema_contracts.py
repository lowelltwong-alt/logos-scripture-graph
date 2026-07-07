from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts import validate_t432_original_language_schema_contracts as validator


ROOT = Path(__file__).resolve().parents[1]
SOURCE_TOKEN_SCHEMA = ROOT / "schemas" / "source_language_token.schema.json"
VARIANT_SCHEMA = ROOT / "schemas" / "textual_variant.schema.json"
WITNESS_SCHEMA = ROOT / "schemas" / "witness.schema.json"


def _schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_t432_original_language_schema_contracts_validate_current_repo() -> None:
    data = validator.validate_t432_original_language_schema_contracts()

    assert data["authority"]["authorizes_preferred_reading"] is False
    assert data["rust_policy"]["rust_added_in_t432"] is False


def test_t432_schema_contract_rejects_canonical_trust_zone() -> None:
    data = _schema(SOURCE_TOKEN_SCHEMA)
    data["properties"]["trust_zone"]["enum"].append("canonical")

    with pytest.raises(validator.T432SchemaContractError, match="trust_zone"):
        validator.validate_schema_contract("SourceLanguageToken", data)


def test_t432_schema_contract_rejects_missing_non_authorizations() -> None:
    data = _schema(SOURCE_TOKEN_SCHEMA)
    data["required"].remove("non_authorizations")

    with pytest.raises(validator.T432SchemaContractError, match="non_authorizations"):
        validator.validate_schema_contract("SourceLanguageToken", data)


def test_t432_variant_rejects_preferred_reading_authority() -> None:
    data = _schema(VARIANT_SCHEMA)
    data["properties"]["preferred_reading_asserted"] = {"const": True}

    with pytest.raises(validator.T432SchemaContractError, match="preferred_reading_asserted"):
        validator.validate_schema_contract("TextualVariant", data)


def test_t432_witness_rejects_source_tradition_preference() -> None:
    data = _schema(WITNESS_SCHEMA)
    data["properties"]["source_tradition_preference_asserted"] = {"const": True}

    with pytest.raises(validator.T432SchemaContractError, match="source_tradition_preference_asserted"):
        validator.validate_schema_contract("Witness", data)


def test_t432_forbidden_output_detection(tmp_path: Path) -> None:
    root = tmp_path
    forbidden = root / "data/candidate/original_language_evidence/source_tokens"
    forbidden.mkdir(parents=True)
    (forbidden / "tokens.jsonl").write_text("{}", encoding="utf-8")

    with pytest.raises(validator.T432SchemaContractError, match="source_tokens"):
        validator._validate_no_forbidden_outputs(root)
