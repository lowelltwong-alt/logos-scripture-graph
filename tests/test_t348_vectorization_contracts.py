from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_vectorization_plan.py"
PLAN = ROOT / ".ai" / "control" / "scripture_vectorization_plan.yaml"
MODELS = ROOT / "config" / "retrieval" / "embedding_models.yaml"
PROFILES = ROOT / "config" / "retrieval" / "retrieval_profiles.yaml"
CONTRACT = ROOT / "docs" / "architecture" / "SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md"
REQUIRED_NON_AUTHORIZED_ACTIONS = {
    "embedding_runs",
    "vector_index_builds",
    "graph_edge_generation",
    "boundary_imports",
    "backend_selection",
    "retrieval_profile_promotion",
}


def _contract_metadata() -> dict:
    return {
        "task_id": "T348",
        "contract_scope": "planning_only",
        "governance_authority": False,
        "authority_note": (
            "Planning metadata only; not governance authority and not authorization to run "
            "embeddings, build indexes, generate graph edges, import boundary corpora, choose "
            "a backend, or promote retrieval profiles."
        ),
        "non_authorized_actions": sorted(REQUIRED_NON_AUTHORIZED_ACTIONS),
    }


def _assert_planning_only_metadata(metadata: dict) -> None:
    assert metadata["task_id"] == "T348"
    assert metadata["contract_scope"] == "planning_only"
    assert metadata["governance_authority"] is False
    assert "not governance authority" in metadata["authority_note"]
    assert REQUIRED_NON_AUTHORIZED_ACTIONS.issubset(set(metadata["non_authorized_actions"]))


def _model(**overrides: object) -> dict:
    entry = {
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
    entry.update(overrides)
    return entry


def _models_registry(*entries: dict) -> dict:
    return {
        "registry_id": "test",
        "contract_metadata": _contract_metadata(),
        "models": list(entries or [_model()]),
    }


def _profile(**overrides: object) -> dict:
    entry = {
        "profile_id": "rprof:test",
        "purpose": "test",
        "index_ids": [],
        "query_embedding_model_id": "emb:test-model-1",
        "default_for_scripture": False,
        "owner_gated": True,
        "status": "candidate",
    }
    entry.update(overrides)
    return entry


def _profiles_registry(*entries: dict) -> dict:
    return {
        "registry_id": "test",
        "contract_metadata": _contract_metadata(),
        "profiles": list(entries),
    }


def _manifest(**overrides: object) -> dict:
    entry = {
        "index_id": "vidx:test-index",
        "embedding_model_id": "emb:test-model-1",
        "embedding_model_version": "1",
        "source_corpus": "eng-web_canonical_66",
        "chunk_set_sha256": "a" * 64,
        "chunk_policy_version": "chunk-policy-test",
        "corpus_baseline": "post_t327_canonical_66_corpus",
        "dimension": 8,
        "normalization": "l2",
        "distance_metric": "cosine",
        "backend": "test-backend",
        "status": "candidate",
        "built_at": "2026-06-11T00:00:00Z",
    }
    entry.update(overrides)
    return entry


def _write_yaml(path: Path, value: object) -> Path:
    path.write_text(yaml.safe_dump(value), encoding="utf-8")
    return path


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
    _assert_planning_only_metadata(plan["contract_metadata"])
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
    assert {
        "TextSpan",
        "ContextPacket",
        "SourceLanguageWitness",
        "AlignmentRecord",
    }.issubset(set(plan["master_context_gate"]["blocked_until_implemented"]))


def test_t348_artifacts_carry_non_governance_authority_metadata() -> None:
    module = _load_module()
    plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    models = yaml.safe_load(MODELS.read_text(encoding="utf-8"))
    profiles = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))

    _assert_planning_only_metadata(plan["contract_metadata"])
    _assert_planning_only_metadata(models["contract_metadata"])
    _assert_planning_only_metadata(profiles["contract_metadata"])

    for schema_path in module.SCHEMAS.values():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        _assert_planning_only_metadata(schema["x_contract_metadata"])


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


def test_validator_fails_closed_on_missing_contract_metadata(tmp_path: Path) -> None:
    plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    plan.pop("contract_metadata")
    tampered = tmp_path / "plan.yaml"
    tampered.write_text(yaml.safe_dump(plan), encoding="utf-8")

    result = _run_validator("--plan", str(tampered))

    assert result.returncode == 1
    assert "contract_metadata" in result.stderr


def test_validator_fails_closed_on_governance_authority_metadata(tmp_path: Path) -> None:
    models = _models_registry()
    models["contract_metadata"]["governance_authority"] = True
    models_path = _write_yaml(tmp_path / "models.yaml", models)

    result = _run_validator("--models", str(models_path))

    assert result.returncode == 1
    assert "governance_authority" in result.stderr


def test_schema_governance_authority_metadata_fails() -> None:
    module = _load_module()
    schema = json.loads(module.SCHEMAS["embedding_model"].read_text(encoding="utf-8"))
    schema["x_contract_metadata"]["governance_authority"] = True

    with pytest.raises(module.VectorizationPlanError, match="governance_authority"):
        module.validate_contract_metadata(
            schema,
            "schema",
            key=module.SCHEMA_CONTRACT_METADATA_KEY,
        )


def test_validator_fails_closed_on_approved_model_while_planning(tmp_path: Path) -> None:
    models_path = _write_yaml(
        tmp_path / "models.yaml",
        _models_registry(_model(status="approved", owner_decision_ref="fake")),
    )

    result = _run_validator("--models", str(models_path))
    assert result.returncode == 1
    assert "approved" in result.stderr


def test_validator_fails_closed_on_boundary_material_in_default_profile(tmp_path: Path) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(
            _profile(
                profile_id="rprof:default-test",
                default_for_scripture=True,
                includes_boundary_material=True,
                owner_gated=True,
                owner_decision_ref="owner-decision:test",
            )
        ),
    )

    result = _run_validator("--models", str(models_path), "--profiles", str(profiles_path))
    assert result.returncode == 1
    assert "includes_boundary_material" in result.stderr


def test_validator_fails_closed_on_unregistered_query_model(tmp_path: Path) -> None:
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(
            _profile(
                profile_id="rprof:orphan",
                query_embedding_model_id="emb:never-registered",
            )
        ),
    )

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
    assert classes == ["structural_deterministic", "reviewed_semantic", "model_inferred_candidate"]
    assert "enum" in edge_schema["properties"]["edge_type"]

    index_schema = json.loads(
        (ROOT / "schemas" / "vector_index_manifest.schema.json").read_text(encoding="utf-8")
    )
    for pin in (
        "embedding_model_id",
        "embedding_model_version",
        "dimension",
        "normalization",
        "distance_metric",
        "chunk_set_sha256",
        "chunk_policy_version",
        "corpus_baseline",
    ):
        assert pin in index_schema["required"]


@pytest.mark.parametrize("missing", ["embedding_model_version", "normalization"])
def test_index_manifest_missing_vector_space_pin_fails(missing: str) -> None:
    module = _load_module()
    manifest = _manifest()
    manifest.pop(missing)

    with pytest.raises(module.VectorizationPlanError, match=missing):
        module.validate_one_index_manifest(manifest, {"emb:test-model-1": _model()}, "manifest")


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("dimension", 9),
        ("distance_metric", "dot"),
        ("normalization", "none"),
        ("embedding_model_version", "2"),
    ],
)
def test_index_manifest_model_mismatch_fails(field: str, bad_value: object) -> None:
    module = _load_module()

    with pytest.raises(module.VectorizationPlanError, match=field):
        module.validate_one_index_manifest(
            _manifest(**{field: bad_value}),
            {"emb:test-model-1": _model()},
            "manifest",
        )


def test_index_manifest_present_fails_while_planning_only(tmp_path: Path) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    manifest_dir = tmp_path / "index_manifests"
    manifest_dir.mkdir()
    _write_yaml(manifest_dir / "idx.yaml", _manifest())

    result = _run_validator(
        "--models",
        str(models_path),
        "--index-manifest-dir",
        str(manifest_dir),
    )

    assert result.returncode == 1
    assert "index manifest" in result.stderr
    assert "index_builds_allowed is false" in result.stderr


def test_reserved_index_manifest_dir_rejects_any_file_suffix_while_planning(tmp_path: Path) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    manifest_dir = tmp_path / "index_manifests"
    nested_dir = manifest_dir / "nested"
    nested_dir.mkdir(parents=True)
    (nested_dir / "evading-manifest.parquet").write_text("not a manifest", encoding="utf-8")

    result = _run_validator(
        "--models",
        str(models_path),
        "--index-manifest-dir",
        str(manifest_dir),
    )

    assert result.returncode == 1
    assert "reserved index manifest directory" in result.stderr
    assert "index_builds_allowed is false" in result.stderr


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("dimension", "wrong_type"),
        ("normalization", "unsafe_norm"),
        ("distance_metric", "made_up_metric"),
        ("status", "live"),
    ],
)
def test_embedding_model_schema_violations_fail(tmp_path: Path, field: str, bad_value: object) -> None:
    models_path = _write_yaml(
        tmp_path / "models.yaml",
        _models_registry(_model(**{field: bad_value})),
    )

    result = _run_validator("--models", str(models_path))

    assert result.returncode == 1
    assert field in result.stderr


def test_duplicate_embedding_model_id_fails(tmp_path: Path) -> None:
    models_path = _write_yaml(
        tmp_path / "models.yaml",
        _models_registry(_model(), _model(provider="second")),
    )

    result = _run_validator("--models", str(models_path))

    assert result.returncode == 1
    assert "duplicate embedding_model_id" in result.stderr


def test_duplicate_profile_id_fails(tmp_path: Path) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(_profile(), _profile(purpose="second")),
    )

    result = _run_validator("--models", str(models_path), "--profiles", str(profiles_path))

    assert result.returncode == 1
    assert "duplicate profile_id" in result.stderr


def test_malformed_registry_yaml_fails(tmp_path: Path) -> None:
    models_path = tmp_path / "models.yaml"
    models_path.write_text("models: [", encoding="utf-8")

    result = _run_validator("--models", str(models_path))

    assert result.returncode == 1
    assert "YAML unreadable" in result.stderr


def test_default_scripture_profile_with_index_ids_fails_while_planning(tmp_path: Path) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(
            _profile(
                profile_id="rprof:default-test",
                index_ids=["vidx:ghost-index"],
                default_for_scripture=True,
                includes_boundary_material=False,
                owner_gated=True,
                owner_decision_ref="owner-decision:test",
            )
        ),
    )

    result = _run_validator("--models", str(models_path), "--profiles", str(profiles_path))

    assert result.returncode == 1
    assert "index_ids" in result.stderr
    assert "unauthorized" in result.stderr


def test_default_scripture_profile_owner_gated_false_fails(tmp_path: Path) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(
            _profile(
                profile_id="rprof:default-test",
                default_for_scripture=True,
                includes_boundary_material=False,
                owner_gated=False,
                owner_decision_ref="owner-decision:test",
            )
        ),
    )

    result = _run_validator("--models", str(models_path), "--profiles", str(profiles_path))

    assert result.returncode == 1
    assert "owner_gated" in result.stderr


def test_default_scripture_profile_missing_owner_decision_fails(tmp_path: Path) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(
            _profile(
                profile_id="rprof:default-test",
                default_for_scripture=True,
                includes_boundary_material=False,
                owner_gated=True,
            )
        ),
    )

    result = _run_validator("--models", str(models_path), "--profiles", str(profiles_path))

    assert result.returncode == 1
    assert "owner_decision_ref" in result.stderr


def test_profile_referencing_nonexistent_index_fails_when_manifests_allowed(tmp_path: Path) -> None:
    module = _load_module()
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(_profile(index_ids=["vidx:missing"])),
    )

    with pytest.raises(module.VectorizationPlanError, match="unregistered vector index"):
        module.validate_profiles(
            profiles_path,
            {"emb:test-model-1": _model()},
            {},
            index_builds_allowed=True,
        )


@pytest.mark.parametrize("status", ["production", "active"])
def test_profile_production_or_active_status_fails_during_planning(
    tmp_path: Path,
    status: str,
) -> None:
    models_path = _write_yaml(tmp_path / "models.yaml", _models_registry())
    profiles_path = _write_yaml(
        tmp_path / "profiles.yaml",
        _profiles_registry(_profile(status=status)),
    )

    result = _run_validator("--models", str(models_path), "--profiles", str(profiles_path))

    assert result.returncode == 1
    assert status in result.stderr


def _edge(**overrides: object) -> dict:
    entry = {
        "edge_id": "edge:test",
        "edge_class": "model_inferred_candidate",
        "edge_type": "quotesFrom",
        "subject_ref": "Ps.1.1",
        "object_ref": "Ps.2.1",
        "status": "candidate_unreviewed",
        "generator_model": "test-generator",
        "prompt_version": "prompt-v1",
        "provenance_ref": "prov:test",
    }
    entry.update(overrides)
    return entry


def test_valid_model_inferred_candidate_edge_shape_passes() -> None:
    module = _load_module()
    module.validate_graph_edge_record(_edge())


def test_model_inferred_candidate_without_prompt_version_fails() -> None:
    module = _load_module()
    edge = _edge()
    edge.pop("prompt_version")

    with pytest.raises(module.VectorizationPlanError, match="prompt_version"):
        module.validate_graph_edge_record(edge)


def test_model_inferred_candidate_without_rebuild_provenance_fails() -> None:
    module = _load_module()
    edge = _edge()
    edge.pop("provenance_ref")

    with pytest.raises(module.VectorizationPlanError, match="not valid under any"):
        module.validate_graph_edge_record(edge)


def test_model_inferred_candidate_with_reviewed_status_fails() -> None:
    module = _load_module()

    with pytest.raises(module.VectorizationPlanError, match="candidate_unreviewed"):
        module.validate_graph_edge_record(_edge(status="reviewed_approved"))


def test_reviewed_semantic_without_evidence_fails() -> None:
    module = _load_module()

    with pytest.raises(module.VectorizationPlanError, match="evidence_refs"):
        module.validate_graph_edge_record(
            _edge(
                edge_class="reviewed_semantic",
                status="reviewed_approved",
                reviewer_ref="reviewer:test",
                reviewed_at="2026-06-11",
            )
        )


def test_reviewed_semantic_without_reviewer_fails() -> None:
    module = _load_module()

    with pytest.raises(module.VectorizationPlanError, match="reviewer_ref"):
        module.validate_graph_edge_record(
            _edge(
                edge_class="reviewed_semantic",
                status="reviewed_approved",
                evidence_refs=["evidence:test"],
                reviewed_at="2026-06-11",
            )
        )


def test_reviewed_semantic_candidate_status_fails() -> None:
    module = _load_module()

    with pytest.raises(module.VectorizationPlanError, match="reviewed_approved"):
        module.validate_graph_edge_record(
            _edge(
                edge_class="reviewed_semantic",
                status="candidate_unreviewed",
                evidence_refs=["evidence:test"],
                reviewer_ref="reviewer:test",
                reviewed_at="2026-06-11",
            )
        )


def test_unknown_edge_type_fails() -> None:
    module = _load_module()

    with pytest.raises(module.VectorizationPlanError, match="not one of"):
        module.validate_graph_edge_record(_edge(edge_type="made_up_edge"))


@pytest.mark.parametrize(
    "missing_gap",
    ["TextSpan", "ContextPacket", "SourceLanguageWitness", "AlignmentRecord"],
)
def test_missing_master_context_substrate_gap_fails(tmp_path: Path, missing_gap: str) -> None:
    plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    plan["master_context_gate"]["blocked_until_implemented"].remove(missing_gap)
    plan_path = _write_yaml(tmp_path / "plan.yaml", plan)

    result = _run_validator("--plan", str(plan_path))

    assert result.returncode == 1
    assert missing_gap in result.stderr


def test_removed_master_context_substrate_gate_fails(tmp_path: Path) -> None:
    plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    plan.pop("master_context_gate")
    plan_path = _write_yaml(tmp_path / "plan.yaml", plan)

    result = _run_validator("--plan", str(plan_path))

    assert result.returncode == 1
    assert "master_context_gate" in result.stderr


def test_registries_are_empty_planning_skeletons() -> None:
    models = yaml.safe_load(MODELS.read_text(encoding="utf-8"))
    profiles = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))
    assert models["models"] == []
    assert profiles["profiles"] == []


def test_contract_doc_preserves_non_authorization_and_gates() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Governance authority: none" in text
    assert "not governance authority" in text
    assert "authorizes no embedding run" in text
    assert "Do not skip" in text and "embeddings or graph edges" in text
    assert "One embedding model per index" in text
    assert "structural_deterministic" in text and "reviewed_semantic" in text
    assert "model_inferred_candidate" in text
    assert "What This Contract Does Not Authorize" in text
    assert "RISK-GATE-001" in text
    assert "T327G or Revelation implementation" in text
