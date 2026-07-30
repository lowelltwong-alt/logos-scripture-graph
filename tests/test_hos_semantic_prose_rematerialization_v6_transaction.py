from __future__ import annotations

import contextlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

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
    / "rematerialize_semantic_prose_v6.py"
)
KERNEL_PATH = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
    / "journaled_recoverable_publish_v3.py"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


REMAT = load_module("hos_rematerialize_v6_transaction", WRAPPER_PATH)
KERNEL = load_module("hos_journaled_publish_v3_transaction", KERNEL_PATH)
REAL_KERNEL_PUBLISH = KERNEL.publish


@dataclass
class IsolatedCase:
    model: Path
    review: Path
    attempt: Path
    archive: Path
    stage: Path
    prepare_manifest: Path
    prepare_receipt: Path
    prepare_journal: Path
    preimage_manifest: Path
    archive_manifest: Path
    staged_manifest: Path
    expanded_diff_manifest: Path
    journal: Path
    lock: Path
    application_receipt: Path
    logical_paths: tuple[str, ...]
    entries: list[dict[str, Any]]
    targets: list[Any]
    receipt_bytes: bytes

    @property
    def allowed(self) -> set[Path]:
        return {self.model / rel for rel in self.logical_paths}


class KernelHarness:
    """Delegate the wrapper call to the real kernel with a test injector."""

    def __init__(
        self,
        injector: Callable[[str, int | None], None] | None = None,
    ) -> None:
        self.injector = injector

    def publish(self, **kwargs):
        return REAL_KERNEL_PUBLISH(
            **kwargs,
            failure_injector=self.injector,
        )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(REMAT.canonical_json_bytes(value))


@pytest.fixture
def isolated_case(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> IsolatedCase:
    model = tmp_path / "model"
    review = model / "reviews" / "Hos"
    attempt = review / "rematerialization_attempts" / REMAT.APPLICATION_ID
    archive = attempt / "archive"
    stage = attempt / "stage"
    logical_paths = tuple(
        f"reviews/Hos/transaction-fixture-{index:02d}.json"
        for index in range(1, 14)
    )
    entries: list[dict[str, Any]] = []
    targets: list[Any] = []
    for ordinal, rel in enumerate(logical_paths, 1):
        canonical = model / rel
        archived = archive / rel
        staged = stage / rel
        old = REMAT.canonical_json_bytes(
            {"member": ordinal, "state": "preimage"}
        )
        new = REMAT.canonical_json_bytes(
            {"member": ordinal, "state": "staged"}
        )
        canonical.parent.mkdir(parents=True, exist_ok=True)
        archived.parent.mkdir(parents=True, exist_ok=True)
        staged.parent.mkdir(parents=True, exist_ok=True)
        canonical.write_bytes(old)
        archived.write_bytes(old)
        staged.write_bytes(new)
        entry = {
            "ordinal": ordinal,
            "target_id": f"Hos-rematerialize-v6-{ordinal:02d}",
            "path": rel,
            "preimage_sha256": REMAT.digest_bytes(old),
            "archive_sha256": REMAT.digest_bytes(old),
            "staged_sha256": REMAT.digest_bytes(new),
            "preimage_size_bytes": len(old),
            "archive_size_bytes": len(old),
            "staged_size_bytes": len(new),
        }
        entries.append(entry)
        targets.append(
            KERNEL.Target(
                target_id=entry["target_id"],
                logical_path=rel,
                canonical=canonical,
                archive=archived,
                staged=staged,
                preimage_sha256=entry["preimage_sha256"],
                staged_sha256=entry["staged_sha256"],
            )
        )

    paths = {
        "PREPARE_MANIFEST": attempt / "prepare_manifest_v6.json",
        "PREPARE_RECEIPT": attempt / "prepare_receipt_v6.json",
        "PREPARE_JOURNAL": attempt / "prepare_journal_v6.json",
        "PREIMAGE_MANIFEST": attempt / "preimage_manifest_v6.json",
        "ARCHIVE_MANIFEST": attempt / "archive_manifest_v6.json",
        "STAGED_MANIFEST": attempt / "staged_manifest_v6.json",
        "EXPANDED_DIFF_MANIFEST": (
            attempt / "expanded_typed_diff_manifest_v6.json"
        ),
        "JOURNAL": attempt / "publish_journal_v6.json",
        "LOCK": review / ".hosea_mutation.lock",
        "APPLICATION_RECEIPT": (
            review / "semantic_prose_rematerialization_application_receipt_v6.json"
        ),
    }
    for name, path in paths.items():
        monkeypatch.setattr(REMAT, name, path)
    monkeypatch.setattr(REMAT, "MODEL", model)
    monkeypatch.setattr(REMAT, "REVIEW", review)
    monkeypatch.setattr(REMAT, "ATTEMPT", attempt)
    monkeypatch.setattr(REMAT, "ARCHIVE", archive)
    monkeypatch.setattr(REMAT, "STAGE", stage)
    monkeypatch.setattr(REMAT, "TARGETS", logical_paths)
    monkeypatch.setattr(
        REMAT,
        "LegacyExecutionGuard",
        lambda: contextlib.nullcontext(),
    )

    write_json(paths["PREIMAGE_MANIFEST"], {"kind": "preimages"})
    write_json(paths["ARCHIVE_MANIFEST"], {"kind": "archives"})
    write_json(paths["STAGED_MANIFEST"], {"kind": "staged"})
    write_json(paths["EXPANDED_DIFF_MANIFEST"], {"kind": "expanded-diff"})
    write_json(
        paths["PREPARE_JOURNAL"],
        {
            "schema_version": "test-prepare-journal.v1",
            "application_id": REMAT.APPLICATION_ID,
            "phase": "prepare_receipt_verified",
        },
    )
    manifest = {
        "schema_version": "m7_hosea_render_prepare_manifest.v6",
        "task_id": "T550",
        "book": "Hos",
        "application_id": REMAT.APPLICATION_ID,
        "writer_sha256": REMAT.digest(WRAPPER_PATH),
        "kernel_sha256": REMAT.digest(KERNEL_PATH),
        "target_count": 13,
        "target_tuple_sha256": REMAT.target_tuple_digest(entries),
        "targets": entries,
        "preimage_manifest_sha256": REMAT.digest(
            paths["PREIMAGE_MANIFEST"]
        ),
        "archive_manifest_sha256": REMAT.digest(paths["ARCHIVE_MANIFEST"]),
        "staged_manifest_sha256": REMAT.digest(paths["STAGED_MANIFEST"]),
        "expanded_diff_manifest_sha256": REMAT.digest(
            paths["EXPANDED_DIFF_MANIFEST"]
        ),
    }
    write_json(paths["PREPARE_MANIFEST"], manifest)
    receipt = {
        "schema_version": "m7_hosea_render_prepare_receipt.v6",
        "task_id": "T550",
        "book": "Hos",
        "application_id": REMAT.APPLICATION_ID,
        "prepare_manifest_sha256": REMAT.digest(paths["PREPARE_MANIFEST"]),
        "target_tuple_sha256": manifest["target_tuple_sha256"],
        "writer_sha256": REMAT.digest(WRAPPER_PATH),
        "kernel_sha256": REMAT.digest(KERNEL_PATH),
        "candidate_only": True,
        "non_authorizing": True,
    }
    write_json(paths["PREPARE_RECEIPT"], receipt)
    receipt_bytes = REMAT.canonical_json_bytes(
        {
            "schema_version": "isolated-application-receipt.v1",
            "application_id": REMAT.APPLICATION_ID,
            "completion_state": "not_completed",
        }
    )
    return IsolatedCase(
        model=model,
        review=review,
        attempt=attempt,
        archive=archive,
        stage=stage,
        prepare_manifest=paths["PREPARE_MANIFEST"],
        prepare_receipt=paths["PREPARE_RECEIPT"],
        prepare_journal=paths["PREPARE_JOURNAL"],
        preimage_manifest=paths["PREIMAGE_MANIFEST"],
        archive_manifest=paths["ARCHIVE_MANIFEST"],
        staged_manifest=paths["STAGED_MANIFEST"],
        expanded_diff_manifest=paths["EXPANDED_DIFF_MANIFEST"],
        journal=paths["JOURNAL"],
        lock=paths["LOCK"],
        application_receipt=paths["APPLICATION_RECEIPT"],
        logical_paths=logical_paths,
        entries=entries,
        targets=targets,
        receipt_bytes=receipt_bytes,
    )


def assert_preimages(case: IsolatedCase) -> None:
    assert {
        KERNEL.sha256_file(target.canonical) for target in case.targets
    } == {entry["preimage_sha256"] for entry in case.entries}


def assert_staged(case: IsolatedCase) -> None:
    assert {
        KERNEL.sha256_file(target.canonical) for target in case.targets
    } == {entry["staged_sha256"] for entry in case.entries}


def direct_kernel_publish(
    case: IsolatedCase,
    *,
    injector: Callable[[str, int | None], None] | None = None,
    invariant: Callable[[str], None] | None = None,
):
    return REAL_KERNEL_PUBLISH(
        application_id=REMAT.APPLICATION_ID,
        targets=case.targets,
        journal_path=case.journal,
        lock_path=case.lock,
        receipt_path=case.application_receipt,
        receipt_bytes=case.receipt_bytes,
        allowed_canonical_paths=case.allowed,
        invariant_check=invariant or (lambda _phase: None),
        failure_injector=injector,
    )


def install_publish_context(
    monkeypatch: pytest.MonkeyPatch,
    case: IsolatedCase,
    *,
    injector: Callable[[str, int | None], None] | None = None,
    invariant: Callable[[str], None] | None = None,
) -> None:
    context = {
        "manifest": {
            "targets": case.entries,
            "writer_sha256": REMAT.digest(WRAPPER_PATH),
            "kernel_sha256": REMAT.digest(KERNEL_PATH),
        },
        "kernel": KernelHarness(injector),
        "targets": case.targets,
        "journal_core_sha256": KERNEL.journal_core_sha256(
            REMAT.APPLICATION_ID,
            case.targets,
        ),
        "application_receipt": json.loads(case.receipt_bytes),
        "application_receipt_bytes": case.receipt_bytes,
        "evidence_paths": [],
        "evidence_hashes": {},
        "boss": {},
        "invocation": {},
        "environment_exception": {},
    }
    monkeypatch.setattr(REMAT, "transaction_context", lambda **_kwargs: context)
    monkeypatch.setattr(
        REMAT,
        "build_transaction_invariants",
        lambda **_kwargs: invariant or (lambda _phase: None),
    )
    monkeypatch.setattr(REMAT, "verify_pins", lambda **_kwargs: None)


def wrapper_publish(case: IsolatedCase):
    return REMAT.publish(
        prepare_receipt_sha256=REMAT.digest(case.prepare_receipt),
        checker_path=case.review / "not-used-checker.json",
        boss_ruling_path=case.review / "not-used-boss.json",
        boss_invocation_path=case.review / "not-used-invocation.json",
        environment_exception_path=case.review / "not-used-exception.json",
    )


@pytest.mark.parametrize("abrupt_state", ["publishing", "rolling_back"])
def test_wrapper_recover_restores_all_13_without_review_authorization(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
    abrupt_state: str,
) -> None:
    case = isolated_case

    def stop_publish(point: str, index: int | None) -> None:
        if point == "after_replace" and index == 13:
            raise KeyboardInterrupt("abrupt publish stop")

    with pytest.raises(KeyboardInterrupt):
        direct_kernel_publish(case, injector=stop_publish)
    assert case.lock.is_file()
    if abrupt_state == "rolling_back":

        def stop_rollback(point: str, index: int | None) -> None:
            if point == "after_rollback_replace" and index == 5:
                raise KeyboardInterrupt("abrupt rollback stop")

        with pytest.raises(KeyboardInterrupt):
            KERNEL.recover_to_preimages(
                application_id=REMAT.APPLICATION_ID,
                targets=case.targets,
                journal_path=case.journal,
                lock_path=case.lock,
                receipt_path=case.application_receipt,
                allowed_canonical_paths=case.allowed,
                invariant_check=lambda _phase: None,
                failure_injector=stop_rollback,
            )
    assert json.loads(case.journal.read_text("utf-8"))["phase"] == abrupt_state

    unrelated_review = case.review / "unrelated-checker-boss-auth.json"
    unrelated_global = case.model / "unrelated-global-sidecar.jsonl"
    unrelated_source = case.model / "unrelated-source.xml"
    for path in (unrelated_review, unrelated_global, unrelated_source):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("drifted after the interruption\n", encoding="utf-8")
    monkeypatch.setattr(
        REMAT,
        "EXPECTED_PINS",
        {unrelated_review: "not-the-current-hash"},
    )
    monkeypatch.setattr(
        REMAT,
        "GLOBAL_SIDECAR_PINS",
        {unrelated_global: "not-the-current-hash"},
    )
    monkeypatch.setattr(
        REMAT,
        "SOURCE_PINS",
        {unrelated_source: "not-the-current-hash"},
    )

    result = REMAT.recover(
        prepare_receipt_sha256=REMAT.digest(case.prepare_receipt)
    )
    assert result["status"] == "rolled_back_verified"
    assert result["recover_only"] is True
    assert result["publication_attempted"] is False
    assert result["review_authorization_artifacts_required"] is False
    assert result["recovery_write_count"] == 13
    assert_preimages(case)
    assert not case.lock.exists()
    assert not case.application_receipt.exists()


def test_wrapper_publish_success_and_receipt_are_idempotent(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = isolated_case
    install_publish_context(monkeypatch, case)
    first = wrapper_publish(case)
    assert first["status"] == "published"
    assert first["canonical_write_count"] == 13
    assert first["application_receipt_sha256"] == REMAT.digest_bytes(
        case.receipt_bytes
    )
    assert_staged(case)
    receipt_hash = REMAT.digest(case.application_receipt)
    journal_hash = REMAT.digest(case.journal)

    replay = wrapper_publish(case)
    assert replay["status"] == "idempotent_noop"
    assert replay["canonical_write_count"] == 0
    assert REMAT.digest(case.application_receipt) == receipt_hash
    assert REMAT.digest(case.journal) == journal_hash


@pytest.mark.parametrize("failure_after", range(1, 14))
def test_wrapper_publish_failure_after_each_replace_rolls_back(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
    failure_after: int,
) -> None:
    case = isolated_case

    def inject(point: str, index: int | None) -> None:
        if point == "after_replace" and index == failure_after:
            raise RuntimeError(f"wrapper stop after replacement {index}")

    install_publish_context(monkeypatch, case, injector=inject)
    with pytest.raises(
        KERNEL.TransactionRolledBack,
        match=f"wrapper stop after replacement {failure_after}",
    ):
        wrapper_publish(case)
    assert_preimages(case)
    assert json.loads(case.journal.read_text("utf-8"))["phase"] == (
        "rolled_back_verified"
    )
    assert not case.lock.exists()


@pytest.mark.parametrize("rollback_stop", range(1, 14))
def test_wrapper_rollback_interruption_each_member_is_recoverable(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
    rollback_stop: int,
) -> None:
    case = isolated_case

    def inject(point: str, index: int | None) -> None:
        if point == "after_replace" and index == 13:
            raise RuntimeError("force wrapper rollback")
        if point == "before_rollback_replace" and index == rollback_stop:
            raise RuntimeError(f"wrapper rollback stop {index}")

    install_publish_context(monkeypatch, case, injector=inject)
    with pytest.raises(KERNEL.RecoveryRequired):
        wrapper_publish(case)
    assert json.loads(case.journal.read_text("utf-8"))["phase"] == (
        "recovery_required"
    )
    assert case.lock.is_file()

    result = REMAT.recover(
        prepare_receipt_sha256=REMAT.digest(case.prepare_receipt)
    )
    assert result["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case.lock.exists()

def test_wrapper_publish_after_final_before_readback_rolls_back(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = isolated_case

    def inject(point: str, _index: int | None) -> None:
        if point == "after_last_replace_before_readback":
            raise RuntimeError("stop after final before readback")

    install_publish_context(monkeypatch, case, injector=inject)
    with pytest.raises(
        KERNEL.TransactionRolledBack,
        match="stop after final before readback",
    ):
        wrapper_publish(case)
    assert_preimages(case)
    assert json.loads(case.journal.read_text("utf-8"))[
        "phase"
    ] == "rolled_back_verified"
    assert not case.lock.exists()


def test_wrapper_publish_receipt_pending_replays_without_target_writes(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = isolated_case
    fired = False

    def inject(point: str, _index: int | None) -> None:
        nonlocal fired
        if point == "immediately_before_receipt_write" and not fired:
            fired = True
            raise OSError("receipt temporarily unavailable")

    install_publish_context(monkeypatch, case, injector=inject)
    with pytest.raises(OSError, match="temporarily unavailable"):
        wrapper_publish(case)
    assert_staged(case)
    assert case.lock.is_file()
    assert json.loads(case.journal.read_text("utf-8"))[
        "phase"
    ] == "published_verified_receipt_pending"

    result = wrapper_publish(case)
    assert result["status"] == "receipt_recovered"
    assert result["canonical_write_count"] == 0
    assert_staged(case)
    assert not case.lock.exists()


def test_wrapper_publish_rejects_second_publisher_journal_interleaving(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = isolated_case
    inner_completed = False

    def inject(point: str, _index: int | None) -> None:
        nonlocal inner_completed
        if (
            point == "after_initial_journal_read_before_lock"
            and not inner_completed
        ):
            inner_completed = True
            assert direct_kernel_publish(case)["status"] == "published"

    install_publish_context(monkeypatch, case, injector=inject)
    with pytest.raises(KERNEL.RecoveryRequired, match="journal appeared"):
        wrapper_publish(case)
    assert json.loads(case.journal.read_text("utf-8"))["phase"] == "completed"
    assert_staged(case)
    assert not case.lock.exists()

    result = wrapper_publish(case)
    assert result["status"] == "idempotent_noop"
    assert result["canonical_write_count"] == 0


def test_wrapper_publish_enforces_exact_allowlist(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = isolated_case
    escaped = case.review / "outside-exact-allowlist.json"
    escaped.write_bytes(case.targets[0].canonical.read_bytes())
    target = case.targets[0]
    case.targets[0] = KERNEL.Target(
        target_id=target.target_id,
        logical_path=target.logical_path,
        canonical=escaped,
        archive=target.archive,
        staged=target.staged,
        preimage_sha256=target.preimage_sha256,
        staged_sha256=target.staged_sha256,
    )
    install_publish_context(monkeypatch, case)
    with pytest.raises(KERNEL.TransactionError, match="exact allowlist"):
        wrapper_publish(case)
    assert_preimages(case)
    assert not case.journal.exists()
    assert not case.lock.exists()


def test_wrapper_publish_respects_shared_lock_contention(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = isolated_case
    case.lock.parent.mkdir(parents=True, exist_ok=True)
    case.lock.write_text("another-writer\n", encoding="utf-8")
    install_publish_context(monkeypatch, case)
    with pytest.raises(KERNEL.RecoveryRequired, match="lock already exists"):
        wrapper_publish(case)
    assert_preimages(case)
    assert not case.journal.exists()
    assert case.lock.read_text("utf-8").strip() == "another-writer"


def test_wrapper_publish_global_before_completed_failure_is_replayable(
    isolated_case: IsolatedCase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = isolated_case
    fail_global = True

    def invariant(phase: str) -> None:
        if phase == "before_completed" and fail_global:
            raise RuntimeError("global sentinel changed before completed")

    install_publish_context(monkeypatch, case, invariant=invariant)
    with pytest.raises(RuntimeError, match="global sentinel changed"):
        wrapper_publish(case)
    assert_staged(case)
    assert case.lock.is_file()
    assert case.application_receipt.is_file()
    assert json.loads(case.journal.read_text("utf-8"))[
        "phase"
    ] == "receipt_written_verified"

    fail_global = False
    result = wrapper_publish(case)
    assert result["status"] == "receipt_recovered"
    assert result["canonical_write_count"] == 0
    assert_staged(case)
    assert not case.lock.exists()


def test_already_loaded_legacy_writer_refuses_v6_shared_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    legacy = load_module(
        "hos_active_legacy_writer_shared_lock_test",
        REMAT.ACTIVE_LEGACY_WRITER,
    )
    shared_lock = tmp_path / ".hosea_mutation.lock"
    monkeypatch.setattr(legacy, "MUTATION_LOCK", shared_lock)
    legacy_called = False

    def mark_legacy_called() -> None:
        nonlocal legacy_called
        legacy_called = True

    monkeypatch.setattr(legacy, "_materialize_unlocked", mark_legacy_called)
    shared_lock.write_text("V6-PUBLISHER-OWNS-LOCK\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="mutation lock already exists"):
        legacy.materialize()

    assert legacy_called is False
    assert shared_lock.read_text(encoding="utf-8") == (
        "V6-PUBLISHER-OWNS-LOCK\n"
    )


def test_active_legacy_writer_releases_only_its_own_shared_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    legacy = load_module(
        "hos_active_legacy_writer_lock_release_test",
        REMAT.ACTIVE_LEGACY_WRITER,
    )
    shared_lock = tmp_path / ".hosea_mutation.lock"
    monkeypatch.setattr(legacy, "MUTATION_LOCK", shared_lock)
    monkeypatch.setattr(legacy, "_materialize_unlocked", lambda: None)

    legacy.materialize()

    assert not shared_lock.exists()

def test_frozen_adapter_active_writer_and_shared_lock_roles_are_distinct() -> None:
    assert REMAT.LEGACY_ADAPTER.name == (
        "corrective_re_review_v2_frozen_render_adapter.py"
    )
    assert REMAT.ACTIVE_LEGACY_WRITER.name == "corrective_re_review_v2.py"
    assert REMAT.LEGACY_ADAPTER != REMAT.ACTIVE_LEGACY_WRITER
    assert REMAT.LOCK == REMAT.SHARED_MUTATION_LOCK
    assert REMAT.LOCK.parent == REMAT.REVIEW
    assert REMAT.EXPECTED_PINS[REMAT.LEGACY_ADAPTER] == REMAT.digest(
        REMAT.LEGACY_ADAPTER
    )
    assert REMAT.EXPECTED_PINS[REMAT.ACTIVE_LEGACY_WRITER] == REMAT.digest(
        REMAT.ACTIVE_LEGACY_WRITER
    )
