#!/usr/bin/env python3
"""Journaled, recoverable multi-file publication for local candidate artifacts.

This module deliberately does not claim set-level atomicity.  Each replacement
is atomic on the local filesystem, while a durable journal plus verified
preimage archive makes the ordered set recoverable.
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


class TransactionRolledBack(TransactionError):
    """Publication failed and every preimage was restored and verified."""


class RecoveryRequired(TransactionError):
    """Publication failed and exact rollback could not be verified."""


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


def verify_targets(targets: Iterable[Target]) -> None:
    """Verify portable identities, canonical preimages, archives, and stages."""
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
        _verify_file(
            target.canonical,
            target.preimage_sha256,
            "canonical preimage",
        )
        _verify_file(target.archive, target.preimage_sha256, "archive")
        _verify_file(target.staged, target.staged_sha256, "stage")


def _journal_core(
    application_id: str,
    targets: list[Target],
) -> dict[str, Any]:
    return {
        "schema_version": "journaled_recoverable_publish.v2",
        "application_id": application_id,
        "transaction_kind": "journaled_recoverable_not_set_atomic",
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
    """Return the immutable transaction-core digest (receipt independent)."""
    return sha256_bytes(
        canonical_json_bytes(_journal_core(application_id, targets))
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


def _mark_recovery_required(
    journal_path: Path,
    journal: dict[str, Any],
    reason: str,
) -> None:
    """Persist a same-identity replay inconsistency before failing closed."""
    journal["phase"] = "recovery_required"
    journal["recovery_reason"] = reason
    _write_journal(journal_path, journal)


def _inject(
    injector: Callable[[str, int | None], None] | None,
    point: str,
    index: int | None = None,
) -> None:
    if injector is not None:
        injector(point, index)


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


def _rollback(
    targets: list[Target],
    journal_path: Path,
    journal: dict[str, Any],
    injector: Callable[[str, int | None], None] | None,
) -> None:
    rollback_failures: list[str] = []
    journal["phase"] = "rolling_back"
    _write_journal(journal_path, journal)
    for reverse_index, target in enumerate(reversed(targets), 1):
        try:
            _inject(injector, "before_rollback_replace", reverse_index)
            _atomic_bytes(target.canonical, target.archive.read_bytes())
            _verify_file(
                target.canonical,
                target.preimage_sha256,
                "rollback readback",
            )
            _inject(injector, "after_rollback_replace", reverse_index)
        except Exception as exc:  # keep restoring remaining targets
            rollback_failures.append(
                f"{target.target_id}: {type(exc).__name__}: {exc}"
            )
    try:
        _verify_all(targets, use_staged=False)
    except Exception as exc:
        rollback_failures.append(
            f"full rollback verification: {type(exc).__name__}: {exc}"
        )
    if rollback_failures:
        journal["phase"] = "recovery_required"
        journal["rollback_failures"] = rollback_failures
        _write_journal(journal_path, journal)
        raise RecoveryRequired("; ".join(rollback_failures))
    journal["phase"] = "rolled_back_verified"
    journal["rollback_failures"] = []
    _write_journal(journal_path, journal)


def recover_to_preimages(
    *,
    application_id: str,
    targets: list[Target],
    journal_path: Path,
    lock_path: Path,
    receipt_path: Path,
    allowed_canonical_paths: set[Path],
    invariant_check: Callable[[str], None],
    failure_injector: Callable[[str, int | None], None] | None = None,
) -> dict[str, Any]:
    """Recover an interrupted publish or rollback to all exact preimages."""
    allowed = {path.resolve() for path in allowed_canonical_paths}
    actual = {target.canonical.resolve() for target in targets}
    if actual != allowed:
        raise RecoveryRequired("recovery target set is not the exact allowlist")
    journal = _load_journal(journal_path)
    if journal is None:
        raise RecoveryRequired("no transaction journal exists to recover")
    core_sha = journal_core_sha256(application_id, targets)
    if journal.get("journal_core_sha256") != core_sha:
        raise RecoveryRequired("recovery journal binds a different core")
    if (
        not lock_path.is_file()
        or lock_path.read_text(encoding="utf-8").strip()
        != application_id
    ):
        raise RecoveryRequired("recovery requires the matching retained lock")
    phase = journal.get("phase")
    if phase not in {
        "publishing",
        "rolling_back",
        "recovery_required",
    }:
        raise RecoveryRequired(f"phase {phase!r} is not rollback-recoverable")
    if receipt_path.exists():
        raise RecoveryRequired(
            "rollback recovery refuses a pre-existing application receipt"
        )
    for target in targets:
        _verify_file(target.archive, target.preimage_sha256, "archive")
        _verify_file(target.staged, target.staged_sha256, "stage")
    invariant_check("before_recovery")
    journal["phase"] = "recovery_required"
    _write_journal(journal_path, journal)
    _rollback(targets, journal_path, journal, failure_injector)
    try:
        invariant_check("after_recovery")
    except BaseException as exc:
        journal["phase"] = "recovery_required"
        journal["after_recovery_failure"] = (
            f"{type(exc).__name__}: {exc}"
        )
        _write_journal(journal_path, journal)
        raise
    lock_path.unlink(missing_ok=True)
    return {
        "status": "rolled_back_verified",
        "canonical_write_count": 0,
        "recovery_write_count": len(targets),
        "journal_core_sha256": core_sha,
    }


def publish(
    *,
    application_id: str,
    targets: list[Target],
    journal_path: Path,
    lock_path: Path,
    receipt_path: Path,
    receipt_bytes: bytes,
    allowed_canonical_paths: set[Path],
    invariant_check: Callable[[str], None],
    failure_injector: Callable[[str, int | None], None] | None = None,
) -> dict[str, Any]:
    """Publish a verified staged set with rollback and receipt recovery.

    ``invariant_check`` is called at each named phase so callers can rehash
    source inputs, code, and out-of-scope sentinels.
    """
    if not targets:
        raise TransactionError("transaction has no targets")
    receipt_sha = sha256_bytes(receipt_bytes)
    allowed = {path.resolve() for path in allowed_canonical_paths}
    actual = {target.canonical.resolve() for target in targets}
    if actual != allowed:
        raise TransactionError("canonical targets do not equal exact allowlist")
    core = _journal_core(application_id, targets)
    core_sha = journal_core_sha256(application_id, targets)
    existing = _load_journal(journal_path)

    if existing is not None:
        if existing.get("journal_core_sha256") != core_sha:
            raise RecoveryRequired("existing journal binds a different core")
        if existing.get("expected_receipt_sha256") != receipt_sha:
            reason = "existing journal binds a different receipt identity"
            _mark_recovery_required(journal_path, existing, reason)
            raise RecoveryRequired(reason)
        phase = existing.get("phase")
        if phase == "completed":
            try:
                _verify_all(targets, use_staged=True)
                _verify_file(
                    receipt_path,
                    receipt_sha,
                    "application receipt",
                )
                invariant_check("completed_replay")
                if lock_path.exists():
                    if (
                        not lock_path.is_file()
                        or lock_path.read_text(encoding="utf-8").strip()
                        != application_id
                    ):
                        raise RecoveryRequired(
                            "completed journal has a mismatching lock residue"
                        )
                    lock_path.unlink()
            except Exception as exc:
                reason = f"completed replay inconsistency: {exc}"
                _mark_recovery_required(journal_path, existing, reason)
                raise RecoveryRequired(reason) from exc
            return {
                "status": "idempotent_noop",
                "canonical_write_count": 0,
                "journal_core_sha256": core_sha,
            }
        if phase in {
            "published_verified_receipt_pending",
            "receipt_written_verified",
        }:
            if (
                not lock_path.is_file()
                or lock_path.read_text(encoding="utf-8").strip()
                != application_id
            ):
                reason = (
                    "receipt-pending journal has no matching retained lock"
                )
                _mark_recovery_required(journal_path, existing, reason)
                raise RecoveryRequired(reason)
            _verify_all(targets, use_staged=True)
            invariant_check("receipt_pending_replay")
            if phase == "published_verified_receipt_pending":
                if receipt_path.exists():
                    _verify_file(
                        receipt_path,
                        receipt_sha,
                        "application receipt",
                    )
                else:
                    _inject(
                        failure_injector,
                        "immediately_before_receipt_write",
                    )
                    _atomic_bytes(receipt_path, receipt_bytes)
                    _inject(failure_injector, "after_receipt_write")
                _verify_file(
                    receipt_path,
                    receipt_sha,
                    "application receipt",
                )
                _inject(
                    failure_injector,
                    "after_receipt_readback_before_receipt_written_verified",
                )
                existing["phase"] = "receipt_written_verified"
                existing["receipt_sha256"] = receipt_sha
                _write_journal(journal_path, existing)
            else:
                if existing.get("receipt_sha256") != receipt_sha:
                    reason = (
                        "receipt-written journal binds a different receipt"
                    )
                    _mark_recovery_required(
                        journal_path,
                        existing,
                        reason,
                    )
                    raise RecoveryRequired(reason)
            try:
                _verify_file(
                    receipt_path,
                    receipt_sha,
                    "application receipt",
                )
            except TransactionError as exc:
                reason = str(exc)
                _mark_recovery_required(journal_path, existing, reason)
                raise RecoveryRequired(reason) from exc
            invariant_check("before_completed")
            _inject(
                failure_injector,
                "after_receipt_written_verified_before_completed",
            )
            existing["phase"] = "completed"
            _write_journal(journal_path, existing)
            lock_path.unlink(missing_ok=True)
            return {
                "status": "receipt_recovered",
                "canonical_write_count": 0,
                "journal_core_sha256": core_sha,
            }
        if phase in {"publishing", "rolling_back", "recovery_required"}:
            existing["phase"] = "recovery_required"
            _write_journal(journal_path, existing)
        raise RecoveryRequired(
            f"unfinished or ambiguous transaction phase {phase!r}"
        )

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with lock_path.open("x", encoding="utf-8") as handle:
            handle.write(application_id + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise RecoveryRequired("transaction lock already exists") from exc

    journal = {
        **core,
        "journal_core_sha256": core_sha,
        "expected_receipt_sha256": receipt_sha,
        "phase": "preimages_verified",
        "last_completed_replacement": 0,
    }
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
            _atomic_bytes(target.canonical, target.staged.read_bytes())
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
        journal["phase"] = "published_verified_receipt_pending"
        _write_journal(journal_path, journal)
        _inject(failure_injector, "immediately_before_receipt_write")
        _atomic_bytes(receipt_path, receipt_bytes)
        _inject(failure_injector, "after_receipt_write")
        _verify_file(receipt_path, receipt_sha, "application receipt")
        _inject(
            failure_injector,
            "after_receipt_readback_before_receipt_written_verified",
        )
        journal["phase"] = "receipt_written_verified"
        journal["receipt_sha256"] = receipt_sha
        _write_journal(journal_path, journal)
        invariant_check("before_completed")
        _verify_file(receipt_path, receipt_sha, "application receipt")
        _inject(
            failure_injector,
            "after_receipt_written_verified_before_completed",
        )
        journal["phase"] = "completed"
        _write_journal(journal_path, journal)
        lock_path.unlink(missing_ok=True)
        return {
            "status": "published",
            "canonical_write_count": len(targets),
            "journal_core_sha256": core_sha,
            "receipt_sha256": receipt_sha,
        }
    except Exception as exc:
        if journal.get("phase") in {
            "published_verified_receipt_pending",
            "receipt_written_verified",
        }:
            journal["receipt_phase_failure"] = (
                f"{type(exc).__name__}: {exc}"
            )
            _write_journal(journal_path, journal)
            # Retain the lock and recover only receipt/journal state on replay.
            raise
        if not changed:
            journal["phase"] = "failed_before_publish"
            journal["failure"] = f"{type(exc).__name__}: {exc}"
            _write_journal(journal_path, journal)
            lock_path.unlink(missing_ok=True)
            raise
        journal["failure"] = f"{type(exc).__name__}: {exc}"
        try:
            _rollback(
                targets,
                journal_path,
                journal,
                failure_injector,
            )
        except RecoveryRequired:
            # Retain lock and journal for deterministic recovery.
            raise
        lock_path.unlink(missing_ok=True)
        raise TransactionRolledBack(str(exc)) from exc
