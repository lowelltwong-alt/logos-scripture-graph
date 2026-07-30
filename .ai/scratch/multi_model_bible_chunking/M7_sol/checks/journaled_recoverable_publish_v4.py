#!/usr/bin/env python3
"""Fail-closed, journaled publication with explicit rollback-only recovery.

This module does not claim power-loss atomicity, set-level atomicity, path
handle pinning, or a lock over unrelated global files.  Individual file
replacements are atomic on the local filesystem.  A retained exact lock,
durable journal, immutable preimage archive, and separate recovery marker make
interrupted local publication diagnosable and rollback-recoverable.

V4 never resumes an incomplete publication.  A later invocation may only
verify an already completed transaction or invoke :func:`recover_to_preimages`.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable


class TransactionError(RuntimeError):
    """Base class for fail-closed transaction failures."""


class RecoveryRequired(TransactionError):
    """Forward publication is forbidden until explicit recovery succeeds."""


@dataclass(frozen=True)
class Target:
    """One canonical target and its immutable archive/staged counterparts."""

    target_id: str
    logical_path: str
    canonical: Path
    archive: Path
    staged: Path
    preimage_sha256: str
    staged_sha256: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("x+b") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        if sha256_file(path) != sha256_bytes(data):
            raise TransactionError(f"readback mismatch for {path}")
    finally:
        temporary.unlink(missing_ok=True)


def _write_journal(path: Path, value: dict[str, Any]) -> None:
    _atomic_bytes(path, canonical_json_bytes(value))


def _verify_file(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise TransactionError(f"{label} is missing: {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise TransactionError(
            f"{label} hash mismatch for {path}: {actual} != {expected}"
        )


def _inject(
    injector: Callable[[str, int | None], None] | None,
    point: str,
    index: int | None = None,
) -> None:
    if injector is not None:
        injector(point, index)


def _journal_core(
    application_id: str,
    targets: list[Target],
) -> dict[str, Any]:
    return {
        "schema_version": "journaled_recoverable_publish.v4",
        "application_id": application_id,
        "transaction_kind": (
            "journaled_recoverable_not_power_loss_or_set_atomic"
        ),
        "target_count": len(targets),
        "targets": [
            {
                "target_id": target.target_id,
                "logical_path": target.logical_path,
                "preimage_sha256": target.preimage_sha256,
                "staged_sha256": target.staged_sha256,
            }
            for target in targets
        ],
    }


def journal_core_sha256(
    application_id: str,
    targets: list[Target],
) -> str:
    return sha256_bytes(
        canonical_json_bytes(_journal_core(application_id, targets))
    )


def _manifest_bytes(
    application_id: str,
    core_sha256: str,
    targets: list[Target],
) -> bytes:
    """Build the actual-published manifest from canonical readback hashes."""
    return canonical_json_bytes(
        {
            "schema_version": "actual_published_manifest.v1",
            "application_id": application_id,
            "journal_core_sha256": core_sha256,
            "target_count": len(targets),
            "targets": [
                {
                    "target_id": target.target_id,
                    "logical_path": target.logical_path,
                    "published_sha256": sha256_file(target.canonical),
                }
                for target in targets
            ],
        }
    )


def _receipt_bytes(
    application_id: str,
    core_sha256: str,
    manifest_sha256: str,
) -> bytes:
    """Return a prose-free completion receipt binding the manifest hash."""
    return canonical_json_bytes(
        {
            "schema_version": "published_receipt.v1",
            "application_id": application_id,
            "journal_core_sha256": core_sha256,
            "actual_published_manifest_sha256": manifest_sha256,
            "completion_state": "completed",
        }
    )


def _load_journal(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RecoveryRequired(
            f"transaction journal cannot be read exactly: {exc}"
        ) from exc
    if not isinstance(value, dict):
        raise RecoveryRequired("transaction journal is not a JSON object")
    return value


def _recovery_marker_value(
    *,
    application_id: str,
    core_sha256: str,
    reason_code: str,
    journal_path: Path,
    lock_path: Path,
) -> dict[str, Any]:
    journal_sha = (
        sha256_file(journal_path) if journal_path.is_file() else None
    )
    lock_sha = sha256_file(lock_path) if lock_path.is_file() else None
    return {
        "schema_version": "journaled_recovery_marker.v1",
        "application_id": application_id,
        "journal_core_sha256": core_sha256,
        "reason_code": reason_code,
        "observed_journal_sha256": journal_sha,
        "observed_lock_sha256": lock_sha,
        "forward_publication_allowed": False,
    }


def _write_recovery_marker(
    *,
    marker_path: Path,
    application_id: str,
    core_sha256: str,
    reason_code: str,
    journal_path: Path,
    lock_path: Path,
) -> None:
    value = _recovery_marker_value(
        application_id=application_id,
        core_sha256=core_sha256,
        reason_code=reason_code,
        journal_path=journal_path,
        lock_path=lock_path,
    )
    data = canonical_json_bytes(value)
    if marker_path.exists():
        if not marker_path.is_file() or marker_path.read_bytes() != data:
            raise RecoveryRequired(
                "a different durable recovery marker already exists"
            )
        return
    _atomic_bytes(marker_path, data)


def _read_lock(lock_path: Path) -> str | None:
    if not lock_path.exists():
        return None
    if not lock_path.is_file():
        raise RecoveryRequired("transaction lock is not a regular file")
    try:
        return lock_path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise RecoveryRequired(
            f"transaction lock cannot be read exactly: {exc}"
        ) from exc


def _ensure_exact_lock(lock_path: Path, application_id: str) -> bool:
    """Ensure the exact transaction lock exists; return whether we created it."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    observed = _read_lock(lock_path)
    if observed is not None:
        if observed != application_id:
            raise RecoveryRequired("transaction lock belongs to another owner")
        return False
    try:
        with lock_path.open("x", encoding="utf-8") as handle:
            handle.write(application_id + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        observed = _read_lock(lock_path)
        if observed != application_id:
            raise RecoveryRequired(
                "transaction lock was acquired by another owner"
            )
        return False
    return True


def _mark_recovery_required(
    journal_path: Path,
    journal: dict[str, Any],
    reason_code: str,
) -> None:
    journal["phase"] = "recovery_required"
    reasons = journal.setdefault("recovery_reason_codes", [])
    if reason_code not in reasons:
        reasons.append(reason_code)
    _write_journal(journal_path, journal)


def _durable_fail(
    *,
    marker_path: Path,
    application_id: str,
    core_sha256: str,
    reason_code: str,
    journal_path: Path,
    lock_path: Path,
    journal: dict[str, Any] | None,
) -> None:
    """Persist failure without modifying an untrusted journal."""
    if journal is not None and (
        journal.get("journal_core_sha256") == core_sha256
    ):
        _mark_recovery_required(journal_path, journal, reason_code)
        return
    _write_recovery_marker(
        marker_path=marker_path,
        application_id=application_id,
        core_sha256=core_sha256,
        reason_code=reason_code,
        journal_path=journal_path,
        lock_path=lock_path,
    )


def _validate_target_identities(targets: Iterable[Target]) -> None:
    seen_ids: set[str] = set()
    seen_logical_paths: set[str] = set()
    seen_paths: set[Path] = set()
    for target in targets:
        if target.target_id in seen_ids:
            raise TransactionError(f"duplicate target ID {target.target_id}")
        logical = PurePosixPath(target.logical_path)
        if (
            not target.logical_path
            or logical.is_absolute()
            or ".." in logical.parts
            or "\\" in target.logical_path
        ):
            raise TransactionError(
                f"invalid portable logical path {target.logical_path!r}"
            )
        if target.logical_path in seen_logical_paths:
            raise TransactionError(
                f"duplicate logical target {target.logical_path}"
            )
        resolved = target.canonical.resolve()
        if resolved in seen_paths:
            raise TransactionError(f"duplicate canonical target {resolved}")
        seen_ids.add(target.target_id)
        seen_logical_paths.add(target.logical_path)
        seen_paths.add(resolved)


def verify_targets(targets: Iterable[Target]) -> None:
    """Verify identities, canonical preimages, archives, and stages."""
    target_list = list(targets)
    _validate_target_identities(target_list)
    for target in target_list:
        _verify_file(
            target.canonical,
            target.preimage_sha256,
            "canonical preimage",
        )
        _verify_file(target.archive, target.preimage_sha256, "archive")
        _verify_file(target.staged, target.staged_sha256, "stage")


def _verify_all(
    targets: list[Target],
    *,
    use_staged: bool,
) -> None:
    for target in targets:
        expected = (
            target.staged_sha256 if use_staged else target.preimage_sha256
        )
        _verify_file(target.canonical, expected, "canonical readback")


def _assert_exact_allowlist(
    targets: list[Target],
    allowed_canonical_paths: set[Path],
) -> None:
    allowed = {path.resolve() for path in allowed_canonical_paths}
    actual = {target.canonical.resolve() for target in targets}
    if actual != allowed:
        raise TransactionError(
            "canonical targets do not equal exact allowlist"
        )


def _completed_replay(
    *,
    application_id: str,
    core_sha256: str,
    targets: list[Target],
    journal: dict[str, Any],
    journal_path: Path,
    lock_path: Path,
    manifest_path: Path,
    receipt_path: Path,
    recovery_marker_path: Path,
    invariant_check: Callable[[str], None],
) -> dict[str, Any]:
    try:
        _verify_all(targets, use_staged=True)
        manifest_bytes = _manifest_bytes(
            application_id,
            core_sha256,
            targets,
        )
        manifest_sha = sha256_bytes(manifest_bytes)
        if journal.get("actual_published_manifest_sha256") != manifest_sha:
            raise TransactionError(
                "completed journal manifest identity mismatch"
            )
        _verify_file(
            manifest_path,
            manifest_sha,
            "actual-published manifest",
        )
        receipt_bytes = _receipt_bytes(
            application_id,
            core_sha256,
            manifest_sha,
        )
        receipt_sha = sha256_bytes(receipt_bytes)
        if journal.get("receipt_sha256") != receipt_sha:
            raise TransactionError("completed journal receipt mismatch")
        _verify_file(receipt_path, receipt_sha, "published receipt")
        invariant_check("completed_replay")
    except BaseException as exc:
        reason = f"completed_replay_mismatch:{type(exc).__name__}"
        _durable_fail(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha256,
            reason_code=reason,
            journal_path=journal_path,
            lock_path=lock_path,
            journal=journal,
        )
        raise RecoveryRequired(reason) from exc
    lock_path.unlink(missing_ok=True)
    return {
        "status": "idempotent_noop",
        "canonical_write_count": 0,
        "journal_core_sha256": core_sha256,
        "actual_published_manifest_sha256": manifest_sha,
        "receipt_sha256": receipt_sha,
    }


def publish(
    *,
    application_id: str,
    targets: list[Target],
    journal_path: Path,
    lock_path: Path,
    manifest_path: Path,
    receipt_path: Path,
    recovery_marker_path: Path,
    allowed_canonical_paths: set[Path],
    invariant_check: Callable[[str], None],
    failure_injector: Callable[[str, int | None], None] | None = None,
) -> dict[str, Any]:
    """Publish once; never resume an incomplete forward transaction."""
    if not targets:
        raise TransactionError("transaction has no targets")
    _validate_target_identities(targets)
    _assert_exact_allowlist(targets, allowed_canonical_paths)
    core = _journal_core(application_id, targets)
    core_sha = journal_core_sha256(application_id, targets)

    try:
        existing = _load_journal(journal_path)
    except RecoveryRequired as exc:
        try:
            _ensure_exact_lock(lock_path, application_id)
        finally:
            _write_recovery_marker(
                marker_path=recovery_marker_path,
                application_id=application_id,
                core_sha256=core_sha,
                reason_code="corrupt_or_unreadable_journal",
                journal_path=journal_path,
                lock_path=lock_path,
            )
        raise

    if existing is not None:
        if existing.get("journal_core_sha256") != core_sha:
            try:
                _ensure_exact_lock(lock_path, application_id)
            finally:
                _write_recovery_marker(
                    marker_path=recovery_marker_path,
                    application_id=application_id,
                    core_sha256=core_sha,
                    reason_code="foreign_journal_core",
                    journal_path=journal_path,
                    lock_path=lock_path,
                )
            raise RecoveryRequired(
                "existing journal binds a different transaction core"
            )
        _ensure_exact_lock(lock_path, application_id)
        if existing.get("phase") == "completed":
            return _completed_replay(
                application_id=application_id,
                core_sha256=core_sha,
                targets=targets,
                journal=existing,
                journal_path=journal_path,
                lock_path=lock_path,
                manifest_path=manifest_path,
                receipt_path=receipt_path,
                recovery_marker_path=recovery_marker_path,
                invariant_check=invariant_check,
            )
        _mark_recovery_required(
            journal_path,
            existing,
            f"incomplete_replay:{existing.get('phase')!r}",
        )
        raise RecoveryRequired(
            "incomplete transaction requires rollback-only recovery"
        )

    _inject(
        failure_injector,
        "after_initial_journal_read_before_lock",
    )
    _ensure_exact_lock(lock_path, application_id)
    try:
        post_lock_existing = _load_journal(journal_path)
    except RecoveryRequired as exc:
        _write_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="journal_corrupt_after_lock",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise exc
    if post_lock_existing is not None:
        if post_lock_existing.get("journal_core_sha256") != core_sha:
            _write_recovery_marker(
                marker_path=recovery_marker_path,
                application_id=application_id,
                core_sha256=core_sha,
                reason_code="foreign_journal_appeared_after_lock",
                journal_path=journal_path,
                lock_path=lock_path,
            )
            raise RecoveryRequired(
                "foreign transaction journal appeared after lock"
            )
        if post_lock_existing.get("phase") == "completed":
            return _completed_replay(
                application_id=application_id,
                core_sha256=core_sha,
                targets=targets,
                journal=post_lock_existing,
                journal_path=journal_path,
                lock_path=lock_path,
                manifest_path=manifest_path,
                receipt_path=receipt_path,
                recovery_marker_path=recovery_marker_path,
                invariant_check=invariant_check,
            )
        _mark_recovery_required(
            journal_path,
            post_lock_existing,
            "unfinished_journal_appeared_after_lock",
        )
        raise RecoveryRequired(
            "unfinished transaction journal appeared after lock"
        )

    journal = {
        **core,
        "journal_core_sha256": core_sha,
        "phase": "preimages_verified",
        "last_completed_replacement": 0,
    }
    _write_journal(journal_path, journal)
    changed = False
    try:
        invariant_check("preflight")
        verify_targets(targets)
        journal["phase"] = "archive_and_stage_verified"
        _write_journal(journal_path, journal)
        invariant_check("before_publish")
        _inject(failure_injector, "before_replace", 0)
        journal["phase"] = "publishing"
        _write_journal(journal_path, journal)
        for index, target in enumerate(targets, 1):
            staged_bytes = target.staged.read_bytes()
            if sha256_bytes(staged_bytes) != target.staged_sha256:
                raise TransactionError(
                    f"staged bytes drift: {target.target_id}"
                )
            invariant_check(f"before_replace_{index}")
            _atomic_bytes(target.canonical, staged_bytes)
            changed = True
            _verify_file(
                target.canonical,
                target.staged_sha256,
                "published target",
            )
            journal["last_completed_replacement"] = index
            _write_journal(journal_path, journal)
            invariant_check(f"after_replace_{index}")
            _inject(failure_injector, "after_replace", index)

        _inject(
            failure_injector,
            "after_last_replace_before_readback",
            len(targets),
        )
        _verify_all(targets, use_staged=True)
        invariant_check("published_readback")
        _inject(
            failure_injector,
            "after_full_readback_before_manifest_pending",
        )

        manifest_bytes = _manifest_bytes(
            application_id,
            core_sha,
            targets,
        )
        manifest_sha = sha256_bytes(manifest_bytes)
        journal["phase"] = "published_verified_manifest_pending"
        journal["expected_actual_published_manifest_sha256"] = manifest_sha
        _write_journal(journal_path, journal)
        _inject(failure_injector, "immediately_before_manifest_write")
        if manifest_path.exists():
            raise TransactionError(
                "actual-published manifest already exists"
            )
        _atomic_bytes(manifest_path, manifest_bytes)
        _inject(failure_injector, "after_manifest_write")
        _verify_file(
            manifest_path,
            manifest_sha,
            "actual-published manifest",
        )
        _inject(
            failure_injector,
            "after_manifest_readback_before_manifest_written_verified",
        )

        receipt_bytes = _receipt_bytes(
            application_id,
            core_sha,
            manifest_sha,
        )
        receipt_sha = sha256_bytes(receipt_bytes)
        journal["phase"] = "manifest_written_verified_receipt_pending"
        journal["actual_published_manifest_sha256"] = manifest_sha
        journal["expected_receipt_sha256"] = receipt_sha
        _write_journal(journal_path, journal)
        _inject(failure_injector, "immediately_before_receipt_write")
        if receipt_path.exists():
            raise TransactionError("published receipt already exists")
        _atomic_bytes(receipt_path, receipt_bytes)
        _inject(failure_injector, "after_receipt_write")
        _verify_file(receipt_path, receipt_sha, "published receipt")
        _inject(
            failure_injector,
            "after_receipt_readback_before_receipt_written_verified",
        )

        journal["phase"] = "receipt_written_verified"
        journal["receipt_sha256"] = receipt_sha
        _write_journal(journal_path, journal)
        invariant_check("before_completed")
        _verify_all(targets, use_staged=True)
        _verify_file(
            manifest_path,
            manifest_sha,
            "actual-published manifest",
        )
        _verify_file(receipt_path, receipt_sha, "published receipt")
        _inject(
            failure_injector,
            "after_receipt_written_verified_before_completed",
        )
        journal["phase"] = "completed"
        _write_journal(journal_path, journal)
        lock_path.unlink()
        return {
            "status": "published",
            "canonical_write_count": len(targets),
            "journal_core_sha256": core_sha,
            "actual_published_manifest_sha256": manifest_sha,
            "receipt_sha256": receipt_sha,
        }
    except Exception as exc:
        reason = f"publish_failure:{type(exc).__name__}"
        _mark_recovery_required(journal_path, journal, reason)
        raise RecoveryRequired(reason) from exc
    finally:
        # ``changed`` intentionally exists for debugger/receipt evidence.  V4
        # retains the exact lock for every incomplete state, even zero-write
        # failures; explicit recovery is the sole cleanup path.
        _ = changed


def _auxiliary_cleanup_status(
    path: Path,
    expected_sha256: str | None,
    label: str,
) -> str | None:
    if not path.exists():
        return None
    if not path.is_file():
        return f"{label}_not_regular_file"
    if expected_sha256 is None:
        return f"{label}_exists_without_transaction_identity"
    if sha256_file(path) != expected_sha256:
        return f"{label}_hash_mismatch"
    path.unlink()
    return None


def _rollback_all(
    *,
    targets: list[Target],
    journal_path: Path,
    journal: dict[str, Any],
    invariant_check: Callable[[str], None],
    failure_injector: Callable[[str, int | None], None] | None,
) -> None:
    journal["phase"] = "rolling_back"
    _write_journal(journal_path, journal)
    failures: list[str] = []
    for reverse_index, target in enumerate(reversed(targets), 1):
        try:
            _inject(
                failure_injector,
                "before_rollback_replace",
                reverse_index,
            )
            archive_bytes = target.archive.read_bytes()
            if sha256_bytes(archive_bytes) != target.preimage_sha256:
                raise TransactionError(
                    f"rollback archive bytes drift: {target.target_id}"
                )
            invariant_check(f"before_rollback_replace_{reverse_index}")
            _atomic_bytes(target.canonical, archive_bytes)
            _verify_file(
                target.canonical,
                target.preimage_sha256,
                "rollback readback",
            )
            _inject(
                failure_injector,
                "after_rollback_replace",
                reverse_index,
            )
        except Exception as exc:
            failures.append(
                f"{target.target_id}:{type(exc).__name__}"
            )
    try:
        _verify_all(targets, use_staged=False)
    except Exception as exc:
        failures.append(f"full_rollback:{type(exc).__name__}")
    if failures:
        journal["phase"] = "recovery_required"
        journal["rollback_failures"] = failures
        _write_journal(journal_path, journal)
        raise RecoveryRequired("rollback could not be verified")
    journal["rollback_failures"] = []
    journal["phase"] = "rolled_back_targets_verified"
    _write_journal(journal_path, journal)


def recover_to_preimages(
    *,
    application_id: str,
    targets: list[Target],
    journal_path: Path,
    lock_path: Path,
    manifest_path: Path,
    receipt_path: Path,
    recovery_marker_path: Path,
    allowed_canonical_paths: set[Path],
    invariant_check: Callable[[str], None],
    failure_injector: Callable[[str, int | None], None] | None = None,
) -> dict[str, Any]:
    """Rollback all targets and remove only hash-matching V4 auxiliaries."""
    _validate_target_identities(targets)
    _assert_exact_allowlist(targets, allowed_canonical_paths)
    core_sha = journal_core_sha256(application_id, targets)
    try:
        journal = _load_journal(journal_path)
    except RecoveryRequired:
        _write_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_corrupt_journal",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise
    if journal is None:
        _write_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_missing_journal",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise RecoveryRequired("no transaction journal exists to recover")
    if journal.get("journal_core_sha256") != core_sha:
        _write_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_foreign_journal_core",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise RecoveryRequired("recovery journal binds a different core")
    if _read_lock(lock_path) != application_id:
        _write_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_missing_or_foreign_lock",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise RecoveryRequired(
            "recovery requires the matching retained exact lock"
        )
    if journal.get("phase") == "completed":
        _mark_recovery_required(
            journal_path,
            journal,
            "recovery_refuses_completed_transaction",
        )
        raise RecoveryRequired(
            "completed transaction cannot enter rollback recovery"
        )

    for target in targets:
        _verify_file(target.archive, target.preimage_sha256, "archive")
        current_sha = sha256_file(target.canonical)
        if current_sha not in {
            target.preimage_sha256,
            target.staged_sha256,
        }:
            _mark_recovery_required(
                journal_path,
                journal,
                f"foreign_canonical_bytes:{target.target_id}",
            )
            raise RecoveryRequired(
                f"canonical mismatch for {target.target_id}"
            )
    try:
        invariant_check("before_recovery")
    except BaseException as exc:
        _mark_recovery_required(
            journal_path,
            journal,
            f"before_recovery_invariant:{type(exc).__name__}",
        )
        raise

    _mark_recovery_required(
        journal_path,
        journal,
        "explicit_rollback_only_recovery",
    )
    _rollback_all(
        targets=targets,
        journal_path=journal_path,
        journal=journal,
        invariant_check=invariant_check,
        failure_injector=failure_injector,
    )

    cleanup_failures: list[str] = []
    receipt_failure = _auxiliary_cleanup_status(
        receipt_path,
        journal.get("expected_receipt_sha256"),
        "receipt",
    )
    if receipt_failure:
        cleanup_failures.append(receipt_failure)
    manifest_failure = _auxiliary_cleanup_status(
        manifest_path,
        journal.get("expected_actual_published_manifest_sha256"),
        "manifest",
    )
    if manifest_failure:
        cleanup_failures.append(manifest_failure)
    if cleanup_failures:
        journal["phase"] = "recovery_required"
        journal["auxiliary_cleanup_failures"] = cleanup_failures
        _write_journal(journal_path, journal)
        raise RecoveryRequired(
            "rollback succeeded but auxiliary cleanup was not exact"
        )

    try:
        invariant_check("after_recovery")
    except BaseException as exc:
        journal["phase"] = "recovery_required"
        journal["after_recovery_failure"] = type(exc).__name__
        _write_journal(journal_path, journal)
        raise
    journal["phase"] = "rolled_back_verified"
    journal["auxiliary_cleanup_failures"] = []
    _write_journal(journal_path, journal)
    lock_path.unlink()
    return {
        "status": "rolled_back_verified",
        "canonical_write_count": 0,
        "recovery_write_count": len(targets),
        "journal_core_sha256": core_sha,
    }
