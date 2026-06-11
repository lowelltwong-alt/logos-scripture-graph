from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_vectorization_plan.py"
PLAN = ROOT / ".ai" / "control" / "scripture_vectorization_plan.yaml"
MODELS = ROOT / "config" / "retrieval" / "embedding_models.yaml"
PROFILES = ROOT / "config" / "retrieval" / "retrieval_profiles.yaml"
CONTRACT = ROOT / "docs" / "architecture" / "SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md"


def _load_module():
    spec = importlib.util.spec_from_file_location("validate_vectorization_plan", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_validator(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_plan_flags_are_fail_closed() -> None:
    plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    assert plan["status"] == "planning_only"
    assert plan["embedding_runs_allowed"] is False
    assert plan["index_builds_allowed"] is False
    assert plan["model_inferred_edge_generation_allowed"] is False
    assert plan["vector_space_mixing_allowed"] is False
    assert plan["shared_index_with_non_bible_corpora_allowed"] is False
    assert plan["boundary_material_in_default_scripture_retrieval"] is False
    assert plan["chunk_policy_tuning_from_retrieval_eval_allowed"] is False
    assert plan["default_scripture_retrieval_change_requires_owner"] is True
    assert plan["reviewed_semantic_edges_require_owner"] is True
    assert plan["master_context_gate"]["owner_authorization_required"] is True


def test_validator_passes_on_committed_state() -> None:
    result = _run_validator()
    assert result.returncode == 0, result.stderr
    assert "planning-only, fail closed" in result.stdout


def test_validator_fails_closed_on_authorizing_plan(tmp_path: Path) -> None:
    plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    plan["embedding_runs_allowed"] = True
    tampered = tmp_path / "plan.yaml"
    tampered.write_text(yaml.safe_dump(plan), encoding="utf-8")

    result = _run_validator("--plan", str(tampered))
    assert result.returncode == 1
    assert "embedding_runs_allowed" in result.stderr


def test_validator_fails_closed_on_approved_model_while_planning(tmp_path: Path) -> None:
    models = {
        "registry_id": "test",
        "models": [
            {
                "embedding_model_id": "emb:test-model-1",
                "provider": "test",
                "model_name": "test-model",
                "model_version": "1",
                "dimension": 8,
                "normalization": "l2",
                "distance_metric": "cosine",
                "status": "approved",
                "owner_decision_ref": "fake",
                "created_at": "2026-06-11",
            }
        ],
    }
    models_path = tmp_path / "models.yaml"
    models_path.write_text(yaml.safe_dump(models), encoding="utf-8")

    result = _run_validator("--models", str(models_path))
    assert result.returncode == 1
    assert "approved" in result.stderr


def test_validator_fails_closed_on_boundary_material_in_default_profile(tmp_path: Path) -> None:
    models = {
        "registry_id": "test",
        "models": [
            {
                "embedding_model_id": "emb:test-model-1",
                "provider": "test",
                "model_name": "test-model",
                "model_version": "1",
                "dimension": 8,
                "normalization": "l2",
                "distance_metric": "cosine",
                "status": "registered",
                "created_at": "2026-06-11",
            }
        ],
    }
    profiles = {
        "registry_id": "test",
        "profiles": [
            {
                "profile_id": "rprof:default-test",
                "purpose": "test",
                "index_ids": [],
                "query_embedding_model_id": "emb:test-model-1",
                "default_for_scripture": True,
                "includes_boundary_material": True,
                "owner_gated": True,
                "status": "candidate",
            }
        ],
    }
    models_path = tmp_path / "models.yaml"
    profiles_path = tmp_path / "profiles.yaml"
    models_path.write_text(yaml.safe_dump(models), encoding="utf-8")
    profiles_path.write_text(yaml.safe_dump(profiles), encoding="utf-8")

    result = _run_validator("--models", str(models_path), "--profiles", str(profiles_path))
    assert result.returncode == 1
    assert "boundary material" in result.stderr


def test_validator_fails_closed_on_unregistered_query_model(tmp_path: Path) -> None:
    profiles = {
        "registry_id": "test",
        "profiles": [
            {
                "profile_id": "rprof:orphan",
                "purpose": "test",
                "index_ids": [],
                "query_embedding_model_id": "emb:never-registered",
                "default_for_scripture": False,
                "owner_gated": True,
                "status": "candidate",
            }
        ],
    }
    profiles_path = tmp_path / "profiles.yaml"
    profiles_path.write_text(yaml.safe_dump(profiles), encoding="utf-8")

    result = _run_validator("--profiles", str(profiles_path))
    assert result.returncode == 1
    assert "unregistered embedding" in result.stderr


def test_schemas_parse_and_enforce_edge_classes() -> None:
    module = _load_module()
    module.validate_schemas()

    edge_schema = json.loads(
        (ROOT / "schemas" / "graph_edge_record.schema.json").read_text(encoding="utf-8")
    )
    classes = edge_schema["properties"]["edge_class"]["enum"]
    assert classes == ["structural_derived", "reviewed_semantic", "model_inferred_candidate"]

    index_schema = json.loads(
        (ROOT / "schemas" / "vector_index_manifest.schema.json").read_text(encoding="utf-8")
    )
    for pin in ("embedding_model_id", "chunk_set_sha256", "chunk_policy_version", "corpus_baseline"):
        assert pin in index_schema["required"]


def test_registries_are_empty_planning_skeletons() -> None:
    models = yaml.safe_load(MODELS.read_text(encoding="utf-8"))
    profiles = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))
    assert models["models"] == []
    assert profiles["profiles"] == []


def test_contract_doc_preserves_non_authorization_and_gates() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "authorizes no embedding run" in text
    assert "Do not skip" in text and "embeddings or graph edges" in text
    assert "One embedding model per index" in text
    assert "structural_derived" in text and "reviewed_semantic" in text
    assert "model_inferred_candidate" in text
    assert "What This Contract Does Not Authorize" in text
    assert "RISK-GATE-001" in text
    assert "T327G or Revelation implementation" in text
