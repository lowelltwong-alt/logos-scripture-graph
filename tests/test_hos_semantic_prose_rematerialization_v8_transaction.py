from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "reviews" / "Hos" / "rematerialize_semantic_prose_v8.py"
SPEC = importlib.util.spec_from_file_location("hos_rematerialize_v8_transaction", SCRIPT)
assert SPEC and SPEC.loader
REMAT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REMAT
SPEC.loader.exec_module(REMAT)


def artifact_kwargs(tmp_path: Path) -> dict[str, object]:
    return {
        "prepare_receipt_sha256": "0" * 64,
        "checker_path": tmp_path / "checker.json",
        "boss_ruling_path": tmp_path / "boss.json",
        "boss_invocation_path": tmp_path / "boss-invocation.json",
        "environment_exception_path": tmp_path / "environment.json",
        "legacy_process_exclusion_path": tmp_path / "legacy.json",
    }


@pytest.mark.parametrize("action", ["publish", "recover"])
def test_publish_and_recover_share_fail_closed_qualification_gate(
    action: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    context_called = False

    def forbidden_context(**_kwargs):
        nonlocal context_called
        context_called = True
        raise AssertionError("context reached before qualification")

    monkeypatch.setattr(REMAT, "transaction_context", forbidden_context)
    monkeypatch.setattr(
        REMAT,
        "require_qualified_publication_primitives",
        lambda: (_ for _ in ()).throw(RuntimeError("qualification blocked")),
    )
    with pytest.raises(RuntimeError, match="qualification blocked"):
        getattr(REMAT, action)(**artifact_kwargs(tmp_path))
    assert context_called is False


def test_publish_and_recover_require_identical_review_artifacts() -> None:
    publish = inspect.signature(REMAT.publish)
    recover = inspect.signature(REMAT.recover)
    assert tuple(publish.parameters) == tuple(recover.parameters)
    assert tuple(publish.parameters) == (
        "prepare_receipt_sha256",
        "checker_path",
        "boss_ruling_path",
        "boss_invocation_path",
        "environment_exception_path",
        "legacy_process_exclusion_path",
    )


def test_sentinel_guard_lifetime_and_rooted_adapter_are_in_both_paths() -> None:
    for action in (REMAT.publish, REMAT.recover):
        source = inspect.getsource(action)
        assert "sentinel_handle_guard" in source
        assert source.index("sentinel_handle_guard") < source.index("transaction_context")
        assert "install_rooted_canonical_adapter" in source
        assert "restore_kernel_atomic_adapter" in source
        assert source.count("sentinel_guard.verify()") >= 3


def test_v5_manifest_receipt_and_journal_api_are_exact() -> None:
    verify_source = inspect.getsource(REMAT.verify_published_outputs)
    context_source = inspect.getsource(REMAT.transaction_context)
    assert '"actual_published_manifest.v2"' in verify_source
    assert '"published_receipt.v2"' in verify_source
    assert "transaction_intent_sha256" in verify_source
    assert "journal_core_sha256" in context_source
    assert "ACTUAL_PUBLISHED_MANIFEST, APPLICATION_RECEIPT" in context_source


def test_environment_schema_is_closed_and_explicitly_non_exhaustive() -> None:
    source = inspect.getsource(REMAT.validate_authorization_artifacts)
    for token in (
        "EXACT_LOWELL_ACKNOWLEDGMENT_TEXT",
        "windows_restart_after_frozen_v8_hashes",
        "zero_other_python_processes_confirmed",
        "zero_sync_processes_confirmed",
        "zero_other_writer_processes_confirmed",
        "snapshot_claims_exhaustive_inventory",
        "onedrive_fully_exited",
        "point_in_time_exclusive_open_checks_passed",
        "exclusive_open_target_count",
        "global_sentinel_handle_count",
        "authorizes_rollback_only_recovery",
        "forbids_global_sidecar_install",
    ):
        assert token in source