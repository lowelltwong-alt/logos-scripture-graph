from __future__ import annotations

import importlib.util
import inspect
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
WRAPPER_PATH = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "reviews"
    / "Hos"
    / "rematerialize_semantic_prose_v7.py"
)
KERNEL_PATH = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
    / "journaled_recoverable_publish_v4.py"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


REMAT = load_module("hos_rematerialize_v7_transaction", WRAPPER_PATH)
KERNEL = load_module("hos_journaled_publish_v4_transaction", KERNEL_PATH)


@dataclass(frozen=True)
class OutputTarget:
    target_id: str
    logical_path: str
    staged_sha256: str


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(REMAT.canonical_json_bytes(value))


def publication_kwargs(tmp_path: Path) -> dict[str, object]:
    return {
        "prepare_receipt_sha256": "0" * 64,
        "checker_path": tmp_path / "checker.json",
        "boss_ruling_path": tmp_path / "boss.json",
        "boss_invocation_path": tmp_path / "invocation.json",
        "environment_exception_path": tmp_path / "exception.json",
        "legacy_process_exclusion_path": tmp_path / "legacy-gate.json",
    }


def test_v7_publication_fails_before_context_or_any_repository_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The unqualified handle primitive is a real blocker, not a fake PASS."""
    before_targets = {
        rel: REMAT.digest(REMAT.MODEL / rel) for rel in REMAT.TARGETS
    }
    before_globals = {
        path: REMAT.digest(path) for path in REMAT.GLOBAL_SIDECAR_PINS
    }
    context_called = False

    def forbidden_context(**_kwargs):
        nonlocal context_called
        context_called = True
        raise AssertionError("transaction context must not be reached")

    monkeypatch.setattr(REMAT, "transaction_context", forbidden_context)
    with pytest.raises(
        RuntimeError,
        match="handle_bound_replacement_primitive_unavailable",
    ):
        REMAT.publish(**publication_kwargs(tmp_path))

    assert context_called is False
    assert {
        rel: REMAT.digest(REMAT.MODEL / rel) for rel in REMAT.TARGETS
    } == before_targets
    assert {
        path: REMAT.digest(path) for path in REMAT.GLOBAL_SIDECAR_PINS
    } == before_globals


def test_v7_does_not_claim_a_wrapper_failure_matrix_pass() -> None:
    assert REMAT.HANDLE_BOUND_REPLACE_STATUS == (
        "BLOCKED_UNQUALIFIED_WINDOWS_PRIMITIVE"
    )
    assert REMAT.TRANSACTION_KERNEL_STATUS == (
        "BLOCKED_INDEPENDENT_CHECKER_FINDINGS"
    )
    assert "ERROR_INVALID_PARAMETER_87" in REMAT.PUBLICATION_BLOCKERS
    assert "journaled_recoverable_publish_v4_unqualified" in (
        REMAT.PUBLICATION_BLOCKERS
    )
    assert not REMAT.FAILURE_EVIDENCE.exists()


def test_required_matrix_inventory_is_closed_and_complete() -> None:
    required = REMAT.REQUIRED_CHECKER_CASES
    semantic = {
        "boundary_mutation",
        "confidence_mutation",
        "review_attempt_id_mutation",
        "fifth_sidecar_scalar_mutation",
        "hold_id_mutation",
        "human_question_mutation",
        "review_status_mutation",
        "decision_id_mutation",
        "non_authorizing_mutation",
    }
    assert semantic <= required
    for phase in ("prepublish", "during_publish"):
        assert {
            f"{phase}_{name}_mutation"
            for name in ("route", "web", "oshb", "uxlc", "wrapper", "legacy")
        } <= required
    assert {f"publish_stop_after_{i}" for i in range(1, 14)} <= required
    assert {f"rollback_stop_after_{i}" for i in range(1, 14)} <= required
    assert {
        "after_full_readback_before_manifest_pending",
        "immediately_before_manifest_write",
        "after_manifest_write",
        "after_manifest_readback_before_manifest_written_verified",
        "immediately_before_receipt_write",
        "after_receipt_write",
        "after_receipt_readback_before_receipt_written_verified",
        "after_receipt_written_verified_before_completed",
        "journal_corrupt",
        "foreign_journal_core_marker",
        "corrupt_recovery_marker",
        "foreign_recovery_marker",
        "global_sentinel_race",
        "global_handle_guard_race",
        "canonical_path_swap",
        "canonical_reparse_swap",
        "replacement_temp_swap",
        "second_publisher",
        "already_loaded_legacy_writer",
        "prepatch_resident_legacy_process_external_gate",
    } <= required


def test_kernel_v4_owns_manifest_receipt_and_recovery_marker_api() -> None:
    publish_parameters = inspect.signature(KERNEL.publish).parameters
    recover_parameters = inspect.signature(KERNEL.recover_to_preimages).parameters
    for parameters in (publish_parameters, recover_parameters):
        assert "manifest_path" in parameters
        assert "receipt_path" in parameters
        assert "recovery_marker_path" in parameters
        assert "receipt_bytes" not in parameters
    assert KERNEL.canonical_json_bytes(
        {"schema_version": "published_receipt.v1"}
    ).endswith(b"\n")


def test_published_outputs_are_separate_deterministic_closed_objects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path = tmp_path / "actual-manifest.json"
    receipt_path = tmp_path / "receipt.json"
    monkeypatch.setattr(REMAT, "ACTUAL_PUBLISHED_MANIFEST", manifest_path)
    monkeypatch.setattr(REMAT, "APPLICATION_RECEIPT", receipt_path)
    target = OutputTarget("Hos-rematerialize-v7-01", "one.json", "a" * 64)
    core = "b" * 64
    manifest = {
        "schema_version": "actual_published_manifest.v1",
        "application_id": REMAT.APPLICATION_ID,
        "journal_core_sha256": core,
        "target_count": 1,
        "targets": [
            {
                "target_id": target.target_id,
                "logical_path": target.logical_path,
                "published_sha256": target.staged_sha256,
            }
        ],
    }
    write_json(manifest_path, manifest)
    manifest_sha = REMAT.digest(manifest_path)
    receipt = {
        "schema_version": "published_receipt.v1",
        "application_id": REMAT.APPLICATION_ID,
        "journal_core_sha256": core,
        "actual_published_manifest_sha256": manifest_sha,
        "completion_state": "completed",
    }
    write_json(receipt_path, receipt)
    receipt_sha = REMAT.digest(receipt_path)

    result = REMAT.verify_published_outputs(
        kernel=KERNEL,
        targets=[target],
        journal_core_sha256=core,
        result={
            "actual_published_manifest_sha256": manifest_sha,
            "receipt_sha256": receipt_sha,
        },
    )
    assert result == {
        "actual_published_manifest_sha256": manifest_sha,
        "application_receipt_sha256": receipt_sha,
    }
    assert set(json.loads(receipt_path.read_text("utf-8"))) == {
        "schema_version",
        "application_id",
        "journal_core_sha256",
        "actual_published_manifest_sha256",
        "completion_state",
    }


@pytest.mark.parametrize("tamper", ["manifest", "receipt"])
def test_published_output_tamper_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tamper: str,
) -> None:
    manifest_path = tmp_path / "actual-manifest.json"
    receipt_path = tmp_path / "receipt.json"
    monkeypatch.setattr(REMAT, "ACTUAL_PUBLISHED_MANIFEST", manifest_path)
    monkeypatch.setattr(REMAT, "APPLICATION_RECEIPT", receipt_path)
    target = OutputTarget("id", "one.json", "a" * 64)
    core = "b" * 64
    write_json(
        manifest_path,
        {
            "schema_version": "actual_published_manifest.v1",
            "application_id": REMAT.APPLICATION_ID,
            "journal_core_sha256": core,
            "target_count": 1,
            "targets": [
                {
                    "target_id": "id",
                    "logical_path": "one.json",
                    "published_sha256": "a" * 64,
                }
            ],
        },
    )
    manifest_sha = REMAT.digest(manifest_path)
    write_json(
        receipt_path,
        {
            "schema_version": "published_receipt.v1",
            "application_id": REMAT.APPLICATION_ID,
            "journal_core_sha256": core,
            "actual_published_manifest_sha256": manifest_sha,
            "completion_state": "completed",
        },
    )
    receipt_sha = REMAT.digest(receipt_path)
    if tamper == "manifest":
        value = json.loads(manifest_path.read_text("utf-8"))
        value["targets"][0]["published_sha256"] = "c" * 64
        write_json(manifest_path, value)
        message = "actual-published manifest"
    else:
        value = json.loads(receipt_path.read_text("utf-8"))
        value["completion_state"] = "not_completed"
        write_json(receipt_path, value)
        message = "published receipt"
    with pytest.raises(RuntimeError, match=message):
        REMAT.verify_published_outputs(
            kernel=KERNEL,
            targets=[target],
            journal_core_sha256=core,
            result={
                "actual_published_manifest_sha256": manifest_sha,
                "receipt_sha256": receipt_sha,
            },
        )


def valid_legacy_gate(prepare_sha: str) -> dict[str, object]:
    return {
        "schema_version": REMAT.LEGACY_PROCESS_EXCLUSION_SCHEMA,
        "task_id": "T550",
        "book": "Hos",
        "application_id": REMAT.APPLICATION_ID,
        "gate_id": "independent-host-gate-001",
        "issued_by": "independent-runtime-operator",
        "gate_type": "fresh_host_or_exhaustive_process_inventory_attestation",
        "checked_active_legacy_writer_sha256": REMAT.digest(
            REMAT.ACTIVE_LEGACY_WRITER
        ),
        "checked_prepare_receipt_sha256": prepare_sha,
        "pre_patch_resident_legacy_process_possible": False,
        "external_gate_status": "PASS",
        "deterministic_process_memory_proof_claimed": False,
        "candidate_only": True,
        "non_authorizing": True,
    }


def test_prepatch_resident_legacy_process_is_an_explicit_external_gate(
    tmp_path: Path,
) -> None:
    prepare_sha = "d" * 64
    path = tmp_path / "legacy-gate.json"
    write_json(path, valid_legacy_gate(prepare_sha))
    assert REMAT.validate_legacy_process_exclusion(path, prepare_sha)[
        "external_gate_status"
    ] == "PASS"

    value = valid_legacy_gate(prepare_sha)
    value["pre_patch_resident_legacy_process_possible"] = True
    write_json(path, value)
    with pytest.raises(
        RuntimeError,
        match="pre_patch_resident_legacy_process_possible",
    ):
        REMAT.validate_legacy_process_exclusion(path, prepare_sha)


def test_publish_signature_requires_external_legacy_process_gate() -> None:
    assert "legacy_process_exclusion_path" in inspect.signature(
        REMAT.publish
    ).parameters