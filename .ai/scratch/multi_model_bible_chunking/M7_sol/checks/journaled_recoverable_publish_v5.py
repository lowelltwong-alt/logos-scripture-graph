#!/usr/bin/env python3
"""Fail-closed, journaled publication with explicit rollback-only recovery.

This module does not claim power-loss atomicity, set-level atomicity, path
handle pinning, or a lock over unrelated global files.  Individual file
replacements are atomic on the local filesystem.  A retained exact lock,
durable journal, immutable preimage archive, and separate recovery marker make
interrupted local publication diagnosable and rollback-recoverable.

V5 never resumes an incomplete publication.  Locks are acquisition-specific,
and a lock created by another invocation is never admitted as reentrant merely
because it names the same application.  A durable recovery marker is an
enforced forward gate.  Manifest and receipt paths and their deterministic
hashes are bound into the immutable journal core, so rollback cleanup does not
trust mutable later journal fields or mutable caller-supplied hashes.

A later invocation may only verify an already completed transaction or invoke
:func:`recover_to_preimages`.  The module makes no path-handle, unrelated
global-file, power-loss, or set-level atomicity claim.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
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


def _portable_absolute_path(path: Path) -> str:
    """Return the exact environment-bound auxiliary identity."""
    return path.resolve().as_posix()


def _transaction_intent(
    application_id: str,
    targets: list[Target],
) -> dict[str, Any]:
    return {
        "schema_version": "journaled_publish_intent.v1",
        "application_id": application_id,
        "transaction_kind": (
            "journaled_recoverable_not_power_loss_or_set_atomic"
        ),
        "target_count": len(targets),
        "targets": [
            {
                "target_id": target.target_id,
                "logical_path": target.logical_path,
                "canonical_path": _portable_absolute_path(target.canonical),
                "archive_path": _portable_absolute_path(target.archive),
                "staged_path": _portable_absolute_path(target.staged),
                "preimage_sha256": target.preimage_sha256,
                "staged_sha256": target.staged_sha256,
            }
            for target in targets
        ],
    }


def _manifest_bytes(
    application_id: str,
    intent_sha256: str,
    targets: list[Target],
) -> bytes:
    """Build deterministic expected manifest bytes from the frozen stages."""
    return canonical_json_bytes(
        {
            "schema_version": "actual_published_manifest.v2",
            "application_id": application_id,
            "transaction_intent_sha256": intent_sha256,
            "target_count": len(targets),
            "targets": [
                {
                    "target_id": target.target_id,
                    "logical_path": target.logical_path,
                    "published_sha256": target.staged_sha256,
                }
                for target in targets
            ],
        }
    )


def _receipt_bytes(
    application_id: str,
    intent_sha256: str,
    manifest_sha256: str,
) -> bytes:
    """Return a prose-free completion receipt binding intent and manifest."""
    return canonical_json_bytes(
        {
            "schema_version": "published_receipt.v2",
            "application_id": application_id,
            "transaction_intent_sha256": intent_sha256,
            "actual_published_manifest_sha256": manifest_sha256,
            "completion_state": "completed",
        }
    )


def _journal_core(
    application_id: str,
    targets: list[Target],
    manifest_path: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    intent = _transaction_intent(application_id, targets)
    intent_sha = sha256_bytes(canonical_json_bytes(intent))
    manifest_sha = sha256_bytes(
        _manifest_bytes(application_id, intent_sha, targets)
    )
    receipt_sha = sha256_bytes(
        _receipt_bytes(application_id, intent_sha, manifest_sha)
    )
    return {
        "schema_version": "journaled_recoverable_publish.v5",
        "transaction_intent": intent,
        "transaction_intent_sha256": intent_sha,
        "auxiliaries": [
            {
                "auxiliary_id": "actual_published_manifest",
                "path": _portable_absolute_path(manifest_path),
                "expected_sha256": manifest_sha,
            },
            {
                "auxiliary_id": "published_receipt",
                "path": _portable_absolute_path(receipt_path),
                "expected_sha256": receipt_sha,
            },
        ],
    }


def journal_core_sha256(
    application_id: str,
    targets: list[Target],
    manifest_path: Path,
    receipt_path: Path,
) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            _journal_core(
                application_id,
                targets,
                manifest_path,
                receipt_path,
            )
        )
    )


def _core_auxiliary(
    core: dict[str, Any],
    auxiliary_id: str,
) -> tuple[Path, str]:
    rows = core.get("auxiliaries")
    if not isinstance(rows, list):
        raise RecoveryRequired("journal core auxiliaries are malformed")
    matches = [
        row
        for row in rows
        if isinstance(row, dict)
        and row.get("auxiliary_id") == auxiliary_id
    ]
    if len(matches) != 1:
        raise RecoveryRequired(
            f"journal core has no unique {auxiliary_id} identity"
        )
    row = matches[0]
    path_value = row.get("path")
    expected = row.get("expected_sha256")
    if (
        not isinstance(path_value, str)
        or not path_value
        or not isinstance(expected, str)
        or len(expected) != 64
    ):
        raise RecoveryRequired(
            f"journal core {auxiliary_id} identity is malformed"
        )
    return Path(path_value), expected


def _validated_journal_core(
    journal: dict[str, Any],
    expected_core_sha256: str | None = None,
) -> tuple[dict[str, Any], str]:
    core = journal.get("immutable_core")
    recorded = journal.get("journal_core_sha256")
    if not isinstance(core, dict) or not isinstance(recorded, str):
        raise RecoveryRequired("journal immutable core is missing")
    actual = sha256_bytes(canonical_json_bytes(core))
    if actual != recorded:
        raise RecoveryRequired("journal immutable core hash mismatch")
    if expected_core_sha256 is not None and actual != expected_core_sha256:
        raise RecoveryRequired("journal binds a different transaction core")
    return core, actual

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
        "schema_version": "journaled_recovery_marker.v2",
        "application_id": application_id,
        "journal_core_sha256": core_sha256,
        "reason_code": reason_code,
        "observed_journal_sha256": journal_sha,
        "observed_lock_sha256": lock_sha,
        "forward_publication_allowed": False,
    }


def _load_recovery_marker(
    marker_path: Path,
) -> tuple[dict[str, Any], bytes] | None:
    if not marker_path.exists():
        return None
    if not marker_path.is_file():
        raise RecoveryRequired(
            "durable recovery marker is not a regular file"
        )
    try:
        data = marker_path.read_bytes()
        value = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RecoveryRequired(
            f"durable recovery marker cannot be read exactly: {exc}"
        ) from exc
    if (
        not isinstance(value, dict)
        or value.get("schema_version")
        != "journaled_recovery_marker.v2"
        or value.get("forward_publication_allowed") is not False
    ):
        raise RecoveryRequired("durable recovery marker is malformed")
    return value, data


def _validated_recovery_marker(
    marker_path: Path,
    *,
    application_id: str,
    core_sha256: str,
) -> tuple[dict[str, Any], bytes] | None:
    loaded = _load_recovery_marker(marker_path)
    if loaded is None:
        return None
    value, data = loaded
    if (
        value.get("application_id") != application_id
        or value.get("journal_core_sha256") != core_sha256
    ):
        raise RecoveryRequired(
            "durable recovery marker belongs to a foreign transaction"
        )
    return value, data


def _enforce_marker_blocks_forward(
    marker_path: Path,
    *,
    application_id: str,
    core_sha256: str,
) -> None:
    try:
        loaded = _validated_recovery_marker(
            marker_path,
            application_id=application_id,
            core_sha256=core_sha256,
        )
    except RecoveryRequired as exc:
        raise RecoveryRequired(
            "durable recovery marker forbids forward publication"
        ) from exc
    if loaded is not None:
        raise RecoveryRequired(
            "durable recovery marker forbids forward publication"
        )


def _write_recovery_marker(
    *,
    marker_path: Path,
    application_id: str,
    core_sha256: str,
    reason_code: str,
    journal_path: Path,
    lock_path: Path,
) -> bytes:
    existing = _validated_recovery_marker(
        marker_path,
        application_id=application_id,
        core_sha256=core_sha256,
    )
    if existing is not None:
        return existing[1]
    value = _recovery_marker_value(
        application_id=application_id,
        core_sha256=core_sha256,
        reason_code=reason_code,
        journal_path=journal_path,
        lock_path=lock_path,
    )
    data = canonical_json_bytes(value)
    _atomic_bytes(marker_path, data)
    return data


def _best_effort_recovery_marker(
    *,
    marker_path: Path,
    application_id: str,
    core_sha256: str,
    reason_code: str,
    journal_path: Path,
    lock_path: Path,
) -> None:
    try:
        _write_recovery_marker(
            marker_path=marker_path,
            application_id=application_id,
            core_sha256=core_sha256,
            reason_code=reason_code,
            journal_path=journal_path,
            lock_path=lock_path,
        )
    except BaseException:
        # The acquisition-specific lock is deliberately retained.  Therefore
        # marker I/O failure still cannot admit a new publisher.
        pass


def _lock_bytes(
    application_id: str,
    core_sha256: str,
    owner_token: str,
) -> bytes:
    return canonical_json_bytes(
        {
            "schema_version": "journaled_publish_lock.v1",
            "application_id": application_id,
            "journal_core_sha256": core_sha256,
            "owner_token": owner_token,
        }
    )


def _acquire_lock(
    lock_path: Path,
    application_id: str,
    core_sha256: str,
) -> tuple[str, bytes]:
    """Exclusively create an invocation-specific lock; never reenter."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    owner_token = secrets.token_hex(32)
    data = _lock_bytes(application_id, core_sha256, owner_token)
    try:
        with lock_path.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise RecoveryRequired(
            "an existing transaction lock blocks this invocation"
        ) from exc
    return owner_token, data


def _read_lock_bytes(lock_path: Path) -> bytes | None:
    if not lock_path.exists():
        return None
    if not lock_path.is_file():
        raise RecoveryRequired("transaction lock is not a regular file")
    try:
        return lock_path.read_bytes()
    except OSError as exc:
        raise RecoveryRequired(
            f"transaction lock cannot be read exactly: {exc}"
        ) from exc


def _validate_owned_lock(
    *,
    lock_path: Path,
    application_id: str,
    core_sha256: str,
    owner_token: str,
) -> bytes:
    expected = _lock_bytes(application_id, core_sha256, owner_token)
    observed = _read_lock_bytes(lock_path)
    if observed != expected:
        raise RecoveryRequired(
            "transaction lock ownership does not match the journal"
        )
    return expected


def _journal_owner_token(journal: dict[str, Any]) -> str:
    owner_token = journal.get("lock_owner_token")
    if not isinstance(owner_token, str) or len(owner_token) != 64:
        raise RecoveryRequired("journal lock owner token is malformed")
    return owner_token


def _validate_journal_owned_lock(
    *,
    lock_path: Path,
    journal: dict[str, Any],
    application_id: str,
    core_sha256: str,
) -> tuple[str, bytes]:
    owner_token = _journal_owner_token(journal)
    expected = _validate_owned_lock(
        lock_path=lock_path,
        application_id=application_id,
        core_sha256=core_sha256,
        owner_token=owner_token,
    )
    if journal.get("lock_sha256") != sha256_bytes(expected):
        raise RecoveryRequired("journal lock hash does not match its owner")
    return owner_token, expected


def _remove_exact_file(path: Path, expected_bytes: bytes, label: str) -> None:
    observed = _read_lock_bytes(path) if label == "lock" else (
        path.read_bytes() if path.is_file() else None
    )
    if observed != expected_bytes:
        raise RecoveryRequired(f"{label} changed before exact cleanup")
    path.unlink()

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
        try:
            _validated_journal_core(journal, core_sha256)
            _mark_recovery_required(journal_path, journal, reason_code)
        except BaseException:
            pass
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
    core: dict[str, Any],
    core_sha256: str,
    targets: list[Target],
    journal: dict[str, Any],
    journal_path: Path,
    lock_path: Path,
    recovery_marker_path: Path,
    invariant_check: Callable[[str], None],
) -> dict[str, Any]:
    """Verify a completed transaction without acquiring or deleting a lock."""
    _enforce_marker_blocks_forward(
        recovery_marker_path,
        application_id=application_id,
        core_sha256=core_sha256,
    )
    if lock_path.exists():
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha256,
            reason_code="completed_replay_observed_existing_lock",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise RecoveryRequired(
            "completed replay is blocked by an existing lock"
        )
    intent_sha = core["transaction_intent_sha256"]
    manifest_path, manifest_sha = _core_auxiliary(
        core,
        "actual_published_manifest",
    )
    receipt_path, receipt_sha = _core_auxiliary(
        core,
        "published_receipt",
    )
    try:
        _validated_journal_core(journal, core_sha256)
        _verify_all(targets, use_staged=True)
        expected_manifest = _manifest_bytes(
            application_id,
            intent_sha,
            targets,
        )
        if sha256_bytes(expected_manifest) != manifest_sha:
            raise TransactionError("core-bound manifest hash mismatch")
        _verify_file(
            manifest_path,
            manifest_sha,
            "actual-published manifest",
        )
        expected_receipt = _receipt_bytes(
            application_id,
            intent_sha,
            manifest_sha,
        )
        if sha256_bytes(expected_receipt) != receipt_sha:
            raise TransactionError("core-bound receipt hash mismatch")
        _verify_file(receipt_path, receipt_sha, "published receipt")
        _enforce_marker_blocks_forward(
            recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha256,
        )
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
    core = _journal_core(
        application_id,
        targets,
        manifest_path,
        receipt_path,
    )
    core_sha = sha256_bytes(canonical_json_bytes(core))
    intent_sha = core["transaction_intent_sha256"]

    # A marker is a durable forward gate even if its JSON is corrupt or foreign.
    _enforce_marker_blocks_forward(
        recovery_marker_path,
        application_id=application_id,
        core_sha256=core_sha,
    )
    try:
        existing = _load_journal(journal_path)
    except RecoveryRequired:
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="corrupt_or_unreadable_journal",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise

    if existing is not None:
        try:
            existing_core, _ = _validated_journal_core(
                existing,
                core_sha,
            )
        except RecoveryRequired:
            _best_effort_recovery_marker(
                marker_path=recovery_marker_path,
                application_id=application_id,
                core_sha256=core_sha,
                reason_code="foreign_or_tampered_journal_core",
                journal_path=journal_path,
                lock_path=lock_path,
            )
            raise
        _enforce_marker_blocks_forward(
            recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
        )
        if existing.get("phase") == "completed":
            return _completed_replay(
                application_id=application_id,
                core=existing_core,
                core_sha256=core_sha,
                targets=targets,
                journal=existing,
                journal_path=journal_path,
                lock_path=lock_path,
                recovery_marker_path=recovery_marker_path,
                invariant_check=invariant_check,
            )
        try:
            _validate_journal_owned_lock(
                lock_path=lock_path,
                journal=existing,
                application_id=application_id,
                core_sha256=core_sha,
            )
        except RecoveryRequired:
            _best_effort_recovery_marker(
                marker_path=recovery_marker_path,
                application_id=application_id,
                core_sha256=core_sha,
                reason_code="incomplete_journal_without_owned_lock",
                journal_path=journal_path,
                lock_path=lock_path,
            )
            raise
        # This invocation does not own the acquisition-specific token.  A
        # validated owner journal may still belong to a live publisher, so the
        # contender neither mutates its journal nor manufactures a marker.
        raise RecoveryRequired(
            "active or incomplete transaction requires rollback-only recovery"
        )

    _inject(
        failure_injector,
        "after_initial_journal_read_before_lock",
    )
    _enforce_marker_blocks_forward(
        recovery_marker_path,
        application_id=application_id,
        core_sha256=core_sha,
    )
    raced_existing = _load_journal(journal_path)
    if raced_existing is not None:
        try:
            raced_core, _ = _validated_journal_core(
                raced_existing,
                core_sha,
            )
        except RecoveryRequired:
            _best_effort_recovery_marker(
                marker_path=recovery_marker_path,
                application_id=application_id,
                core_sha256=core_sha,
                reason_code="foreign_journal_appeared_before_lock",
                journal_path=journal_path,
                lock_path=lock_path,
            )
            raise
        if raced_existing.get("phase") == "completed":
            return _completed_replay(
                application_id=application_id,
                core=raced_core,
                core_sha256=core_sha,
                targets=targets,
                journal=raced_existing,
                journal_path=journal_path,
                lock_path=lock_path,
                recovery_marker_path=recovery_marker_path,
                invariant_check=invariant_check,
            )
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="incomplete_journal_appeared_before_lock",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise RecoveryRequired(
            "a noncompleted journal appeared before lock acquisition"
        )
    if lock_path.exists():
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="existing_lock_without_validated_owning_journal",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise RecoveryRequired(
            "an existing lock without a validated owning journal blocks publish"
        )
    owner_token, owned_lock_bytes = _acquire_lock(
        lock_path,
        application_id,
        core_sha,
    )
    journal: dict[str, Any] | None = None
    try:
        _inject(failure_injector, "after_lock_before_initial_journal")
        _enforce_marker_blocks_forward(
            recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
        )
        post_lock_existing = _load_journal(journal_path)
        if post_lock_existing is not None:
            raise RecoveryRequired(
                "a journal appeared after this invocation acquired its lock"
            )
        journal = {
            "immutable_core": core,
            "journal_core_sha256": core_sha,
            "lock_owner_token": owner_token,
            "lock_sha256": sha256_bytes(owned_lock_bytes),
            "phase": "preimages_verified",
            "last_completed_replacement": 0,
        }
        _inject(failure_injector, "before_initial_journal_write")
        _write_journal(journal_path, journal)
        _inject(failure_injector, "after_initial_journal_write")
    except BaseException as exc:
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code=(
                f"initialization_failure:{type(exc).__name__}"
            ),
            journal_path=journal_path,
            lock_path=lock_path,
        )
        # Never delete the acquisition-specific lock.  Even if marker I/O also
        # failed, a later invocation cannot treat this lock as reentrant.
        raise

    changed = False
    try:
        _validated_journal_core(journal, core_sha)
        _validate_owned_lock(
            lock_path=lock_path,
            application_id=application_id,
            core_sha256=core_sha,
            owner_token=owner_token,
        )
        _enforce_marker_blocks_forward(
            recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
        )
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
            _enforce_marker_blocks_forward(
                recovery_marker_path,
                application_id=application_id,
                core_sha256=core_sha,
            )
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
            intent_sha,
            targets,
        )
        manifest_core_path, manifest_sha = _core_auxiliary(
            core,
            "actual_published_manifest",
        )
        if manifest_core_path.resolve() != manifest_path.resolve():
            raise TransactionError("manifest path diverges from journal core")
        if sha256_bytes(manifest_bytes) != manifest_sha:
            raise TransactionError("manifest hash diverges from journal core")
        journal["phase"] = "published_verified_manifest_pending"
        _write_journal(journal_path, journal)
        _inject(failure_injector, "immediately_before_manifest_write")
        _enforce_marker_blocks_forward(
            recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
        )
        if manifest_core_path.exists():
            raise TransactionError(
                "actual-published manifest already exists"
            )
        _atomic_bytes(manifest_core_path, manifest_bytes)
        _inject(failure_injector, "after_manifest_write")
        _verify_file(
            manifest_core_path,
            manifest_sha,
            "actual-published manifest",
        )
        _inject(
            failure_injector,
            "after_manifest_readback_before_manifest_written_verified",
        )

        receipt_bytes = _receipt_bytes(
            application_id,
            intent_sha,
            manifest_sha,
        )
        receipt_core_path, receipt_sha = _core_auxiliary(
            core,
            "published_receipt",
        )
        if receipt_core_path.resolve() != receipt_path.resolve():
            raise TransactionError("receipt path diverges from journal core")
        if sha256_bytes(receipt_bytes) != receipt_sha:
            raise TransactionError("receipt hash diverges from journal core")
        journal["phase"] = "manifest_written_verified_receipt_pending"
        _write_journal(journal_path, journal)
        _inject(failure_injector, "immediately_before_receipt_write")
        _enforce_marker_blocks_forward(
            recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
        )
        if receipt_core_path.exists():
            raise TransactionError("published receipt already exists")
        _atomic_bytes(receipt_core_path, receipt_bytes)
        _inject(failure_injector, "after_receipt_write")
        _verify_file(receipt_core_path, receipt_sha, "published receipt")
        _inject(
            failure_injector,
            "after_receipt_readback_before_receipt_written_verified",
        )

        journal["phase"] = "receipt_written_verified"
        _write_journal(journal_path, journal)
        invariant_check("before_completed")
        _verify_all(targets, use_staged=True)
        _verify_file(
            manifest_core_path,
            manifest_sha,
            "actual-published manifest",
        )
        _verify_file(receipt_core_path, receipt_sha, "published receipt")
        _inject(
            failure_injector,
            "after_receipt_written_verified_before_completed",
        )
        _validate_owned_lock(
            lock_path=lock_path,
            application_id=application_id,
            core_sha256=core_sha,
            owner_token=owner_token,
        )
        _enforce_marker_blocks_forward(
            recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
        )
        journal["phase"] = "completed"
        _write_journal(journal_path, journal)
        _remove_exact_file(lock_path, owned_lock_bytes, "lock")
        return {
            "status": "published",
            "canonical_write_count": len(targets),
            "journal_core_sha256": core_sha,
            "actual_published_manifest_sha256": manifest_sha,
            "receipt_sha256": receipt_sha,
        }
    except Exception as exc:
        reason = f"publish_failure:{type(exc).__name__}"
        _durable_fail(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code=reason,
            journal_path=journal_path,
            lock_path=lock_path,
            journal=journal,
        )
        raise RecoveryRequired(reason) from exc
    except BaseException as exc:
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code=f"publish_interrupted:{type(exc).__name__}",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise
    finally:
        # V5 retains the exact lock for every incomplete state, including a
        # zero-write failure.  Explicit rollback recovery is the only cleanup.
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
    """Rollback all targets and remove only core-bound V5 auxiliaries."""
    _validate_target_identities(targets)
    _assert_exact_allowlist(targets, allowed_canonical_paths)
    expected_core = _journal_core(
        application_id,
        targets,
        manifest_path,
        receipt_path,
    )
    core_sha = sha256_bytes(canonical_json_bytes(expected_core))

    # A valid marker authorizes rollback-only handling, never forward work.  A
    # corrupt or foreign marker blocks recovery before any target or auxiliary
    # mutation because its ownership cannot be established.
    marker = _validated_recovery_marker(
        recovery_marker_path,
        application_id=application_id,
        core_sha256=core_sha,
    )
    try:
        journal = _load_journal(journal_path)
    except RecoveryRequired:
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_corrupt_journal",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise
    if journal is None:
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_missing_journal",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise RecoveryRequired("no transaction journal exists to recover")
    try:
        core, _ = _validated_journal_core(journal, core_sha)
    except RecoveryRequired:
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_foreign_or_tampered_journal_core",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise
    try:
        owner_token, owned_lock_bytes = _validate_journal_owned_lock(
            lock_path=lock_path,
            journal=journal,
            application_id=application_id,
            core_sha256=core_sha,
        )
    except RecoveryRequired:
        _best_effort_recovery_marker(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_missing_or_foreign_lock",
            journal_path=journal_path,
            lock_path=lock_path,
        )
        raise
    _ = owner_token
    if journal.get("phase") == "completed":
        _durable_fail(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="recovery_refuses_completed_transaction",
            journal_path=journal_path,
            lock_path=lock_path,
            journal=journal,
        )
        raise RecoveryRequired(
            "completed transaction cannot enter rollback recovery"
        )

    manifest_core_path, manifest_sha = _core_auxiliary(
        core,
        "actual_published_manifest",
    )
    receipt_core_path, receipt_sha = _core_auxiliary(
        core,
        "published_receipt",
    )
    if (
        manifest_core_path.resolve() != manifest_path.resolve()
        or receipt_core_path.resolve() != receipt_path.resolve()
    ):
        _durable_fail(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code="caller_auxiliary_path_mismatch",
            journal_path=journal_path,
            lock_path=lock_path,
            journal=journal,
        )
        raise RecoveryRequired(
            "caller auxiliary paths diverge from journal core"
        )

    for target in targets:
        _verify_file(target.archive, target.preimage_sha256, "archive")
        current_sha = sha256_file(target.canonical)
        if current_sha not in {
            target.preimage_sha256,
            target.staged_sha256,
        }:
            _durable_fail(
                marker_path=recovery_marker_path,
                application_id=application_id,
                core_sha256=core_sha,
                reason_code=f"foreign_canonical_bytes:{target.target_id}",
                journal_path=journal_path,
                lock_path=lock_path,
                journal=journal,
            )
            raise RecoveryRequired(
                f"canonical mismatch for {target.target_id}"
            )
    try:
        invariant_check("before_recovery")
    except BaseException as exc:
        _durable_fail(
            marker_path=recovery_marker_path,
            application_id=application_id,
            core_sha256=core_sha,
            reason_code=f"before_recovery_invariant:{type(exc).__name__}",
            journal_path=journal_path,
            lock_path=lock_path,
            journal=journal,
        )
        raise

    _durable_fail(
        marker_path=recovery_marker_path,
        application_id=application_id,
        core_sha256=core_sha,
        reason_code="explicit_rollback_only_recovery",
        journal_path=journal_path,
        lock_path=lock_path,
        journal=journal,
    )
    marker = _validated_recovery_marker(
        recovery_marker_path,
        application_id=application_id,
        core_sha256=core_sha,
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
        receipt_core_path,
        receipt_sha,
        "receipt",
    )
    if receipt_failure:
        cleanup_failures.append(receipt_failure)
    manifest_failure = _auxiliary_cleanup_status(
        manifest_core_path,
        manifest_sha,
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
    _remove_exact_file(lock_path, owned_lock_bytes, "lock")
    if marker is not None:
        _remove_exact_file(
            recovery_marker_path,
            marker[1],
            "recovery marker",
        )
    return {
        "status": "rolled_back_verified",
        "canonical_write_count": 0,
        "recovery_write_count": len(targets),
        "journal_core_sha256": core_sha,
    }
