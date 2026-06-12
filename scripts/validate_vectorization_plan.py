#!/usr/bin/env python3
"""Validate T348 vectorization/edge-durability planning contracts (fail closed).

Enforces, while the plan is planning_only:
  - all authorization flags in scripture_vectorization_plan.yaml stay false
    (and owner-gate flags stay true);
  - the embedding-model registry contains no approved models;
  - the retrieval-profile registry contains no production profiles, at most
    one default-for-scripture profile, and no default profile that includes
    boundary material;
  - registry entries that do exist carry schema-required fields and any
    referenced embedding model is registered;
  - the four retrieval/graph schemas parse and declare required fields;
  - no vector index manifest exists while index builds are unauthorized;
  - the plan, registries, and schemas declare planning-only metadata with no
    governance authority.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - exercised only in under-provisioned envs
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parent.parent

PLAN = ROOT / ".ai" / "control" / "scripture_vectorization_plan.yaml"
MODELS = ROOT / "config" / "retrieval" / "embedding_models.yaml"
PROFILES = ROOT / "config" / "retrieval" / "retrieval_profiles.yaml"
INDEX_MANIFEST_DIR = ROOT / "config" / "retrieval" / "index_manifests"
PREDICATE_REGISTRY = ROOT / "config" / "governance" / "predicate_registry.yaml"
SCHEMAS = {
    "embedding_model": ROOT / "schemas" / "embedding_model.schema.json",
    "vector_index_manifest": ROOT / "schemas" / "vector_index_manifest.schema.json",
    "retrieval_profile": ROOT / "schemas" / "retrieval_profile.schema.json",
    "graph_edge_record": ROOT / "schemas" / "graph_edge_record.schema.json",
}
INDEX_MANIFEST_SUFFIXES = {".json", ".yaml", ".yml"}
CONTRACT_METADATA_KEY = "contract_metadata"
SCHEMA_CONTRACT_METADATA_KEY = "x_contract_metadata"
REQUIRED_NON_AUTHORIZED_ACTIONS = {
    "embedding_runs",
    "vector_index_builds",
    "graph_edge_generation",
    "boundary_imports",
    "backend_selection",
    "retrieval_profile_promotion",
}
REQUIRED_SUBSTRATE_GAPS = {
    "TextSpan",
    "ContextPacket",
    "SourceLanguageWitness",
    "AlignmentRecord",
}

MUST_BE_FALSE = [
    "embedding_runs_allowed",
    "index_builds_allowed",
    "model_inferred_edge_generation_allowed",
    "vector_space_mixing_allowed",
    "shared_index_with_non_bible_corpora_allowed",
    "boundary_material_in_default_scripture_retrieval",
    "chunk_policy_tuning_from_retrieval_eval_allowed",
]
MUST_BE_TRUE = [
    "default_scripture_retrieval_change_requires_owner",
    "reviewed_semantic_edges_require_owner",
]

class VectorizationPlanError(ValueError):
    """Raised when the vectorization planning contracts are violated."""


def load_yaml(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except (OSError, yaml.YAMLError) as exc:
        raise VectorizationPlanError(f"{path}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise VectorizationPlanError(f"{path}: expected a YAML mapping")
    return data


def validate_contract_metadata(container: dict, label: str, *, key: str = CONTRACT_METADATA_KEY) -> None:
    metadata = container.get(key)
    if not isinstance(metadata, dict):
        raise VectorizationPlanError(f"{label}: {key} must be a mapping")
    if metadata.get("task_id") != "T348":
        raise VectorizationPlanError(
            f"{label}: {key}.task_id must be T348, found {metadata.get('task_id')!r}"
        )
    if metadata.get("contract_scope") != "planning_only":
        raise VectorizationPlanError(
            f"{label}: {key}.contract_scope must be planning_only, "
            f"found {metadata.get('contract_scope')!r}"
        )
    if metadata.get("governance_authority") is not False:
        raise VectorizationPlanError(
            f"{label}: {key}.governance_authority must be false, "
            f"found {metadata.get('governance_authority')!r}"
        )
    note = metadata.get("authority_note")
    if not isinstance(note, str) or "not governance authority" not in note.lower():
        raise VectorizationPlanError(
            f"{label}: {key}.authority_note must state this is not governance authority"
        )
    actions = metadata.get("non_authorized_actions")
    if not isinstance(actions, list):
        raise VectorizationPlanError(f"{label}: {key}.non_authorized_actions must be a list")
    if not all(isinstance(action, str) for action in actions):
        raise VectorizationPlanError(f"{label}: {key}.non_authorized_actions must list strings")
    missing = sorted(REQUIRED_NON_AUTHORIZED_ACTIONS - set(actions))
    if missing:
        raise VectorizationPlanError(
            f"{label}: {key}.non_authorized_actions missing {missing}"
        )


def require_jsonschema() -> None:
    if Draft202012Validator is None:
        raise VectorizationPlanError(
            "jsonschema is required for fail-closed T348 validation; install the "
            "project validate extra with: pip install -e \".[validate]\""
        )


def load_schema(path: Path) -> dict:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VectorizationPlanError(f"{path}: schema unreadable: {exc}") from exc
    for key in ("$schema", "title", "type", "required", "properties"):
        if key not in schema:
            raise VectorizationPlanError(f"{path}: schema missing {key}")
    validate_contract_metadata(schema, str(path), key=SCHEMA_CONTRACT_METADATA_KEY)
    require_jsonschema()
    Draft202012Validator.check_schema(schema)
    return schema


def schema_validator(schema_name: str) -> Draft202012Validator:
    require_jsonschema()
    return Draft202012Validator(load_schema(SCHEMAS[schema_name]))


def format_schema_error(error) -> str:
    path = ".".join(str(part) for part in error.absolute_path)
    if path:
        return f"{path}: {error.message}"
    return error.message


def validate_against_schema(record: object, validator: Draft202012Validator, label: str) -> None:
    errors = sorted(validator.iter_errors(record), key=lambda err: list(err.absolute_path))
    if errors:
        joined = "; ".join(format_schema_error(err) for err in errors[:5])
        raise VectorizationPlanError(f"{label}: schema violation: {joined}")


def load_predicate_names() -> set[str]:
    registry = load_yaml(PREDICATE_REGISTRY)
    predicates = registry.get("predicates")
    if not isinstance(predicates, dict) or not predicates:
        raise VectorizationPlanError(f"{PREDICATE_REGISTRY}: predicates must be a non-empty mapping")
    return set(predicates)


def validate_plan(plan_path: Path) -> dict:
    plan = load_yaml(plan_path)
    validate_contract_metadata(plan, str(plan_path))
    if plan.get("status") != "planning_only":
        raise VectorizationPlanError(
            f"{plan_path}: status must be planning_only, found {plan.get('status')!r}"
        )
    for key in MUST_BE_FALSE:
        if plan.get(key) is not False:
            raise VectorizationPlanError(
                f"{plan_path}: {key} must be false (fail closed), found {plan.get(key)!r}"
            )
    for key in MUST_BE_TRUE:
        if plan.get(key) is not True:
            raise VectorizationPlanError(
                f"{plan_path}: {key} must be true, found {plan.get(key)!r}"
            )
    gate = plan.get("master_context_gate")
    if not isinstance(gate, dict):
        raise VectorizationPlanError(f"{plan_path}: master_context_gate must be a mapping")
    if gate.get("owner_authorization_required") is not True:
        raise VectorizationPlanError(
            f"{plan_path}: master_context_gate.owner_authorization_required must be true"
        )
    blocked = gate.get("blocked_until_implemented")
    if not isinstance(blocked, list):
        raise VectorizationPlanError(
            f"{plan_path}: master_context_gate.blocked_until_implemented must list substrate gaps"
        )
    missing = sorted(REQUIRED_SUBSTRATE_GAPS - set(blocked))
    if missing:
        raise VectorizationPlanError(
            f"{plan_path}: master_context_gate.blocked_until_implemented missing {missing}"
        )
    return plan


def validate_models(models_path: Path) -> dict[str, dict]:
    registry = load_yaml(models_path)
    validate_contract_metadata(registry, str(models_path))
    models = registry.get("models")
    if not isinstance(models, list):
        raise VectorizationPlanError(f"{models_path}: models must be a list")
    validator = schema_validator("embedding_model")
    by_id: dict[str, dict] = {}
    for idx, entry in enumerate(models):
        if not isinstance(entry, dict):
            raise VectorizationPlanError(f"{models_path}: model entry {idx} must be a mapping")
        validate_against_schema(entry, validator, f"{models_path}: model entry {idx}")
        model_id = entry["embedding_model_id"]
        if model_id in by_id:
            raise VectorizationPlanError(f"{models_path}: duplicate embedding_model_id {model_id}")
        if entry["status"] == "approved" and not entry.get("owner_decision_ref"):
            raise VectorizationPlanError(
                f"{models_path}: {model_id} is approved without owner_decision_ref"
            )
        if entry["status"] == "approved":
            raise VectorizationPlanError(
                f"{models_path}: {model_id} has status approved while the "
                "plan is planning_only; model approval requires the owner-gated embedding task"
            )
        by_id[model_id] = entry
    return by_id


def validate_one_index_manifest(entry: object, models_by_id: dict[str, dict], label: str) -> dict:
    if not isinstance(entry, dict):
        raise VectorizationPlanError(f"{label}: index manifest must be a mapping")
    validate_against_schema(entry, schema_validator("vector_index_manifest"), label)
    model_id = entry["embedding_model_id"]
    model = models_by_id.get(model_id)
    if model is None:
        raise VectorizationPlanError(f"{label}: references unregistered embedding model {model_id}")
    comparisons = {
        "embedding_model_version": "model_version",
        "dimension": "dimension",
        "distance_metric": "distance_metric",
        "normalization": "normalization",
    }
    for manifest_key, model_key in comparisons.items():
        if entry[manifest_key] != model[model_key]:
            raise VectorizationPlanError(
                f"{label}: {manifest_key} {entry[manifest_key]!r} does not match "
                f"registered model {model_id} {model_key} {model[model_key]!r}"
            )
    return entry


def validate_index_manifests(
    manifest_dir: Path,
    models_by_id: dict[str, dict],
    *,
    allow_manifests: bool,
) -> dict[str, dict]:
    manifests_by_id: dict[str, dict] = {}
    if not manifest_dir.exists():
        return manifests_by_id

    files = [p for p in manifest_dir.rglob("*") if p.is_file()]
    if files and not allow_manifests:
        raise VectorizationPlanError(
            f"{manifest_dir}: {len(files)} file(s) present under reserved index manifest "
            "directory while index_builds_allowed is false"
        )

    manifests = [
        p for p in files
        if p.suffix.lower() in INDEX_MANIFEST_SUFFIXES
    ]
    for path in sorted(manifests, key=lambda p: p.as_posix()):
        entry = load_yaml(path)
        manifest = validate_one_index_manifest(entry, models_by_id, str(path))
        index_id = manifest["index_id"]
        if index_id in manifests_by_id:
            raise VectorizationPlanError(f"{manifest_dir}: duplicate index_id {index_id}")
        manifests_by_id[index_id] = manifest

    return manifests_by_id


def validate_profiles(
    profiles_path: Path,
    models_by_id: dict[str, dict],
    manifests_by_id: dict[str, dict],
    *,
    index_builds_allowed: bool,
) -> None:
    registry = load_yaml(profiles_path)
    validate_contract_metadata(registry, str(profiles_path))
    profiles = registry.get("profiles")
    if not isinstance(profiles, list):
        raise VectorizationPlanError(f"{profiles_path}: profiles must be a list")
    validator = schema_validator("retrieval_profile")
    defaults = 0
    seen_profile_ids: set[str] = set()
    for idx, entry in enumerate(profiles):
        if not isinstance(entry, dict):
            raise VectorizationPlanError(f"{profiles_path}: profile entry {idx} must be a mapping")
        validate_against_schema(entry, validator, f"{profiles_path}: profile entry {idx}")
        profile_id = entry["profile_id"]
        if profile_id in seen_profile_ids:
            raise VectorizationPlanError(f"{profiles_path}: duplicate profile_id {profile_id}")
        seen_profile_ids.add(profile_id)
        if entry["status"] in {"production", "active"}:
            raise VectorizationPlanError(
                f"{profiles_path}: {profile_id} has status {entry['status']} while index "
                "builds are unauthorized"
            )
        index_ids = entry["index_ids"]
        if index_ids and not index_builds_allowed:
            raise VectorizationPlanError(
                f"{profiles_path}: {profile_id} references index_ids while index builds are "
                "unauthorized"
            )
        if entry["default_for_scripture"]:
            defaults += 1
            if entry.get("owner_gated") is not True:
                raise VectorizationPlanError(
                    f"{profiles_path}: {profile_id} is default_for_scripture but owner_gated "
                    "is not true"
                )
            if not entry.get("owner_decision_ref"):
                raise VectorizationPlanError(
                    f"{profiles_path}: {profile_id} is default_for_scripture without "
                    "owner_decision_ref"
                )
            if entry.get("includes_boundary_material") is not False:
                raise VectorizationPlanError(
                    f"{profiles_path}: {profile_id} is default_for_scripture but "
                    "includes boundary material; the default Scripture profile must exclude it"
                )
        model_id = entry["query_embedding_model_id"]
        if model_id not in models_by_id:
            raise VectorizationPlanError(
                f"{profiles_path}: {profile_id} references unregistered embedding "
                f"model {model_id}"
            )
        for index_id in index_ids:
            manifest = manifests_by_id.get(index_id)
            if manifest is None:
                raise VectorizationPlanError(
                    f"{profiles_path}: {profile_id} references unregistered vector index "
                    f"{index_id}"
                )
            if manifest["embedding_model_id"] != model_id:
                raise VectorizationPlanError(
                    f"{profiles_path}: {profile_id} query model {model_id} does not match "
                    f"{index_id} model {manifest['embedding_model_id']}"
                )
    if defaults > 1:
        raise VectorizationPlanError(
            f"{profiles_path}: at most one profile may set default_for_scripture: true"
        )


def validate_schemas() -> None:
    loaded = {name: load_schema(path) for name, path in SCHEMAS.items()}
    edge_type_enum = set(
        loaded["graph_edge_record"]["properties"]["edge_type"].get("enum") or []
    )
    predicate_names = load_predicate_names()
    if edge_type_enum != predicate_names:
        raise VectorizationPlanError(
            f"{SCHEMAS['graph_edge_record']}: edge_type enum must match "
            f"{PREDICATE_REGISTRY} predicates; schema-only={sorted(edge_type_enum - predicate_names)}, "
            f"registry-only={sorted(predicate_names - edge_type_enum)}"
        )


def validate_graph_edge_record(record: object) -> None:
    """Validate one graph edge record against schema + predicate registry."""
    validate_schemas()
    validate_against_schema(
        record,
        schema_validator("graph_edge_record"),
        "graph edge record",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=PLAN)
    parser.add_argument("--models", type=Path, default=MODELS)
    parser.add_argument("--profiles", type=Path, default=PROFILES)
    parser.add_argument("--index-manifest-dir", type=Path, default=INDEX_MANIFEST_DIR)
    args = parser.parse_args(argv)

    try:
        plan = validate_plan(args.plan)
        models_by_id = validate_models(args.models)
        manifests_by_id = validate_index_manifests(
            args.index_manifest_dir,
            models_by_id,
            allow_manifests=plan.get("index_builds_allowed") is True,
        )
        validate_profiles(
            args.profiles,
            models_by_id,
            manifests_by_id,
            index_builds_allowed=plan.get("index_builds_allowed") is True,
        )
        validate_schemas()
    except VectorizationPlanError as exc:
        print(f"Vectorization plan validation failed: {exc}", file=sys.stderr)
        return 1

    print("Vectorization plan validation passed (planning-only, fail closed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
