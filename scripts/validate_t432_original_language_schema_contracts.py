#!/usr/bin/env python3
"""Validate T432 original-language schema contracts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "original_language_schema_contracts.yaml"
SUBSTRATE = ROOT / ".ai" / "control" / "original_language_evidence_substrate.yaml"
TASK = ROOT / ".ai" / "tasks" / "T432.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T432" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T432" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T432_ORIGINAL_LANGUAGE_SCHEMA_CONTRACTS.md"
VALIDATE_SCHEMAS = ROOT / "scripts" / "validate_schemas.py"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

SCHEMA_FILES = {
    "SourceLanguageToken": ROOT / "schemas" / "source_language_token.schema.json",
    "EditorialLayer": ROOT / "schemas" / "editorial_layer.schema.json",
    "Lexeme": ROOT / "schemas" / "lexeme.schema.json",
    "AlignmentRecord": ROOT / "schemas" / "alignment_record.schema.json",
    "TextualVariant": ROOT / "schemas" / "textual_variant.schema.json",
    "Witness": ROOT / "schemas" / "witness.schema.json",
}

REQUIRED_COMMON = {
    "id",
    "type",
    "schema_version",
    "trust_zone",
    "status",
    "provenance",
    "authority",
    "non_authorizations",
}

FORBIDDEN_TRUST_ZONES = {"canonical", "asserted"}

FORBIDDEN_OUTPUT_DIRS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)

FORBIDDEN_AUTH_TRUE = {
    "authorizes_source_language_truth",
    "authorizes_lexical_truth",
    "authorizes_source_text_mutation",
    "authorizes_strongs_overlay_in_raw",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_canon_scope_change",
    "authorizes_translation_judgment",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_route_behavior",
    "authorizes_evaluator_behavior",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embeddings_or_indexes",
    "authorizes_theology_authority",
}


class T432SchemaContractError(ValueError):
    """Raised when T432 schema contracts are invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T432SchemaContractError(f"{_rel(path)}: unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T432SchemaContractError(f"{_rel(path)}: expected YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T432SchemaContractError(f"{_rel(path)}: unreadable JSON schema: {exc}") from exc
    if not isinstance(data, dict):
        raise T432SchemaContractError(f"{_rel(path)}: expected JSON object")
    return data


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if mapping.get(key) is not False:
            raise T432SchemaContractError(f"{label}.{key} must be false")


def _schema_required(schema: dict[str, Any], schema_name: str) -> set[str]:
    required = schema.get("required")
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise T432SchemaContractError(f"{schema_name}: required must be a string list")
    return set(required)


def _schema_property(schema: dict[str, Any], key: str, schema_name: str) -> dict[str, Any]:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise T432SchemaContractError(f"{schema_name}: properties must be a mapping")
    prop = properties.get(key)
    if not isinstance(prop, dict):
        raise T432SchemaContractError(f"{schema_name}: properties.{key} must be a mapping")
    return prop


def validate_schema_contract(schema_name: str, schema: dict[str, Any]) -> None:
    required = _schema_required(schema, schema_name)
    missing = sorted(REQUIRED_COMMON - required)
    if missing:
        raise T432SchemaContractError(f"{schema_name}: missing common required fields {missing}")

    trust_zone = _schema_property(schema, "trust_zone", schema_name)
    trust_enum = set(trust_zone.get("enum", []))
    forbidden = sorted(FORBIDDEN_TRUST_ZONES & trust_enum)
    if forbidden:
        raise T432SchemaContractError(f"{schema_name}: trust_zone must not allow {forbidden}")
    if not {"candidate", "context"} <= trust_enum:
        raise T432SchemaContractError(f"{schema_name}: trust_zone must allow candidate and context")

    non_auth = _schema_property(schema, "non_authorizations", schema_name)
    if non_auth.get("type") != "array" or int(non_auth.get("minItems", 0)) < 4:
        raise T432SchemaContractError(f"{schema_name}: non_authorizations must be a required non-empty array")

    authority = _schema_property(schema, "authority", schema_name)
    authority_props = authority.get("properties")
    authority_required = authority.get("required")
    if not isinstance(authority_props, dict) or not isinstance(authority_required, list):
        raise T432SchemaContractError(f"{schema_name}: authority must define required false flags")
    for key in authority_required:
        prop = authority_props.get(key)
        if not isinstance(prop, dict) or prop.get("const") is not False:
            raise T432SchemaContractError(f"{schema_name}: authority.{key} must be const false")

    if schema_name == "SourceLanguageToken":
        for key in ("source_id", "canonical_source_view_manifest", "source_file_sha256", "evidence_mode", "inferred_vs_observed"):
            if key not in required:
                raise T432SchemaContractError(f"{schema_name}: {key} is required")
        strong_id = schema["properties"].get("strong_id")
        if not isinstance(strong_id, dict) or "null" not in strong_id.get("type", []):
            raise T432SchemaContractError(f"{schema_name}: strong_id must be nullable evidence")

    if schema_name == "EditorialLayer":
        editorial = schema["properties"].get("is_editorial_not_autograph_certainty")
        if not isinstance(editorial, dict) or editorial.get("const") is not True:
            raise T432SchemaContractError(f"{schema_name}: must require editorial-not-autograph certainty flag")

    if schema_name == "TextualVariant":
        for key in ("preferred_reading_asserted", "source_tradition_preference_asserted", "textual_critical_decision_asserted"):
            prop = schema["properties"].get(key)
            if not isinstance(prop, dict) or prop.get("const") is not False:
                raise T432SchemaContractError(f"{schema_name}: {key} must be const false")
        readings = schema["properties"].get("readings")
        if not isinstance(readings, dict) or int(readings.get("minItems", 0)) < 2:
            raise T432SchemaContractError(f"{schema_name}: readings must require at least two readings")

    if schema_name == "Witness":
        for key in ("bulk_download_authorized", "transcription_storage_allowed", "image_storage_allowed"):
            if key not in required:
                raise T432SchemaContractError(f"{schema_name}: {key} is required")
        preferred = schema["properties"].get("source_tradition_preference_asserted")
        if not isinstance(preferred, dict) or preferred.get("const") is not False:
            raise T432SchemaContractError(f"{schema_name}: source_tradition_preference_asserted must be const false")


def _validate_no_forbidden_outputs(root: Path) -> None:
    for directory in FORBIDDEN_OUTPUT_DIRS:
        path = root / directory.relative_to(ROOT)
        if path.exists() and any(path.rglob("*")):
            raise T432SchemaContractError(f"{_rel(path)} must not contain T432 data outputs")


def validate_t432_original_language_schema_contracts(root: Path = ROOT) -> dict[str, Any]:
    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "original_language_schema_contracts":
        raise T432SchemaContractError("original_language_schema_contracts object_type is wrong")
    if control.get("schema_version") != "original_language_schema_contracts.v1":
        raise T432SchemaContractError("original_language_schema_contracts schema_version is wrong")
    authority = control.get("authority")
    if not isinstance(authority, dict):
        raise T432SchemaContractError("authority must be a mapping")
    _require_false(authority, FORBIDDEN_AUTH_TRUE, "authority")
    if control.get("rust_policy", {}).get("rust_added_in_t432") is not False:
        raise T432SchemaContractError("T432 rust_policy.rust_added_in_t432 must be false")

    substrate = _read_yaml(root / SUBSTRATE.relative_to(ROOT))
    schema_contracts = substrate.get("schema_contracts")
    if not isinstance(schema_contracts, dict):
        raise T432SchemaContractError("T430 substrate must reference T432 schema_contracts")
    if schema_contracts.get("control") != ".ai/control/original_language_schema_contracts.yaml":
        raise T432SchemaContractError("T430 substrate schema_contracts.control is wrong")

    task = _read_yaml(root / TASK.relative_to(ROOT))
    task_auth = task.get("authorization")
    if not isinstance(task_auth, dict):
        raise T432SchemaContractError("T432 task authorization must be a mapping")
    for key, value in task_auth.items():
        if key.startswith(("creates_", "changes_", "runs_", "authorizes_", "selects_", "stores_", "populates_")) and key not in {"creates_schema_contracts"}:
            if value is not False:
                raise T432SchemaContractError(f"T432 task authorization {key} must be false")

    for schema_name, schema_path in SCHEMA_FILES.items():
        validate_schema_contract(schema_name, _read_json(root / schema_path.relative_to(ROOT)))

    validate_schemas_text = (root / VALIDATE_SCHEMAS.relative_to(ROOT)).read_text(encoding="utf-8")
    validate_all_text = (root / VALIDATE_ALL.relative_to(ROOT)).read_text(encoding="utf-8")
    for rec_type in SCHEMA_FILES:
        if f'"{rec_type}"' not in validate_schemas_text:
            raise T432SchemaContractError(f"validate_schemas.py missing {rec_type}")
    if "validate_t432_original_language_schema_contracts.py" not in validate_all_text:
        raise T432SchemaContractError("validate_all.py must run the T432 validator")
    if "GITHUB_BASE_REF" not in validate_all_text:
        raise T432SchemaContractError("validate_all.py must honor GitHub base refs for stacked task branches")

    for required_file in (HANDOFF, DAD_PREFLIGHT, ROADMAP):
        path = root / required_file.relative_to(ROOT)
        if not path.exists():
            raise T432SchemaContractError(f"{_rel(path)} is missing")
    dad_text = (root / DAD_PREFLIGHT.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("t432 should stay python/control-plane", "t435", "rust"):
        if phrase not in dad_text:
            raise T432SchemaContractError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")
    roadmap_text = (root / ROADMAP.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("strong's", "preferred reading", "oldest-known", "rust", "t433"):
        if phrase not in roadmap_text:
            raise T432SchemaContractError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")

    _validate_no_forbidden_outputs(root)
    return control


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t432_original_language_schema_contracts(args.root.resolve())
    except T432SchemaContractError as exc:
        print(f"T432 original-language schema contract validation failed: {exc}", file=sys.stderr)
        return 1
    print("T432 original-language schema contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
