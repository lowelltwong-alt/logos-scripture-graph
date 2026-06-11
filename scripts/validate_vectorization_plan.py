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
  - no vector index manifest exists while index builds are unauthorized.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

PLAN = ROOT / ".ai" / "control" / "scripture_vectorization_plan.yaml"
MODELS = ROOT / "config" / "retrieval" / "embedding_models.yaml"
PROFILES = ROOT / "config" / "retrieval" / "retrieval_profiles.yaml"
INDEX_MANIFEST_DIR = ROOT / "config" / "retrieval" / "index_manifests"
SCHEMAS = [
    ROOT / "schemas" / "embedding_model.schema.json",
    ROOT / "schemas" / "vector_index_manifest.schema.json",
    ROOT / "schemas" / "retrieval_profile.schema.json",
    ROOT / "schemas" / "graph_edge_record.schema.json",
]

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

MODEL_REQUIRED = [
    "embedding_model_id", "provider", "model_name", "model_version",
    "dimension", "normalization", "distance_metric", "status", "created_at",
]
PROFILE_REQUIRED = [
    "profile_id", "purpose", "index_ids", "query_embedding_model_id",
    "default_for_scripture", "owner_gated", "status",
]


class VectorizationPlanError(ValueError):
    """Raised when the vectorization planning contracts are violated."""


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise VectorizationPlanError(f"{path}: expected a YAML mapping")
    return data


def validate_plan(plan_path: Path) -> dict:
    plan = load_yaml(plan_path)
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
    gate = plan.get("master_context_gate") or {}
    if gate.get("owner_authorization_required") is not True:
        raise VectorizationPlanError(
            f"{plan_path}: master_context_gate.owner_authorization_required must be true"
        )
    return plan


def validate_models(models_path: Path) -> dict[str, dict]:
    registry = load_yaml(models_path)
    models = registry.get("models")
    if not isinstance(models, list):
        raise VectorizationPlanError(f"{models_path}: models must be a list")
    by_id: dict[str, dict] = {}
    for entry in models:
        missing = [k for k in MODEL_REQUIRED if k not in entry]
        if missing:
            raise VectorizationPlanError(
                f"{models_path}: model entry missing required fields {missing}"
            )
        if entry["status"] == "approved" and not entry.get("owner_decision_ref"):
            raise VectorizationPlanError(
                f"{models_path}: {entry['embedding_model_id']} is approved without owner_decision_ref"
            )
        if entry["status"] == "approved":
            raise VectorizationPlanError(
                f"{models_path}: {entry['embedding_model_id']} has status approved while the "
                "plan is planning_only; model approval requires the owner-gated embedding task"
            )
        by_id[entry["embedding_model_id"]] = entry
    return by_id


def validate_profiles(profiles_path: Path, models_by_id: dict[str, dict]) -> None:
    registry = load_yaml(profiles_path)
    profiles = registry.get("profiles")
    if not isinstance(profiles, list):
        raise VectorizationPlanError(f"{profiles_path}: profiles must be a list")
    defaults = 0
    for entry in profiles:
        missing = [k for k in PROFILE_REQUIRED if k not in entry]
        if missing:
            raise VectorizationPlanError(
                f"{profiles_path}: profile entry missing required fields {missing}"
            )
        if entry["status"] == "production":
            raise VectorizationPlanError(
                f"{profiles_path}: {entry['profile_id']} has status production while index "
                "builds are unauthorized"
            )
        if entry["default_for_scripture"]:
            defaults += 1
            if entry.get("includes_boundary_material"):
                raise VectorizationPlanError(
                    f"{profiles_path}: {entry['profile_id']} is default_for_scripture but "
                    "includes boundary material; the default Scripture profile must exclude it"
                )
        model_id = entry["query_embedding_model_id"]
        if model_id not in models_by_id:
            raise VectorizationPlanError(
                f"{profiles_path}: {entry['profile_id']} references unregistered embedding "
                f"model {model_id}"
            )
    if defaults > 1:
        raise VectorizationPlanError(
            f"{profiles_path}: at most one profile may set default_for_scripture: true"
        )


def validate_schemas() -> None:
    for path in SCHEMAS:
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise VectorizationPlanError(f"{path}: schema unreadable: {exc}") from exc
        for key in ("$schema", "title", "type", "required", "properties"):
            if key not in schema:
                raise VectorizationPlanError(f"{path}: schema missing {key}")


def validate_no_index_manifests() -> None:
    if INDEX_MANIFEST_DIR.exists():
        manifests = [p for p in INDEX_MANIFEST_DIR.rglob("*") if p.is_file() and p.suffix in {".json", ".yaml", ".yml"}]
        if manifests:
            raise VectorizationPlanError(
                f"{INDEX_MANIFEST_DIR}: {len(manifests)} index manifest(s) present while "
                "index_builds_allowed is false"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=PLAN)
    parser.add_argument("--models", type=Path, default=MODELS)
    parser.add_argument("--profiles", type=Path, default=PROFILES)
    args = parser.parse_args(argv)

    try:
        validate_plan(args.plan)
        models_by_id = validate_models(args.models)
        validate_profiles(args.profiles, models_by_id)
        validate_schemas()
        validate_no_index_manifests()
    except VectorizationPlanError as exc:
        print(f"Vectorization plan validation failed: {exc}", file=sys.stderr)
        return 1

    print("Vectorization plan validation passed (planning-only, fail closed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
