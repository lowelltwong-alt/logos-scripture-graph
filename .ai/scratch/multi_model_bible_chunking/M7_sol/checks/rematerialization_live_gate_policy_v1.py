#!/usr/bin/env python3
"""Provider-neutral, side-effect-free policy for a short-lived live gate.

This module validates evidence supplied by an environment adapter.  It does
not inspect the host, authenticate a human, open a target, authorize a
publication, or mutate anything.  A successful result means only that the
supplied evidence matches the caller's independently frozen expectations and
the narrow candidate-only policy below.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "rematerialization_live_gate_policy.v1"
EXPECTATIONS_SCHEMA_VERSION = "rematerialization_live_gate_expectations.v1"
TARGET_COUNT = 13
SENTINEL_COUNT = 3
MAX_LEASE_SECONDS = 120
MAX_PREPARE_TO_PUBLISH_SECONDS = 300
PHASES = ("prepare", "publish")

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_NON_CRYPTOGRAPHIC_IDENTITY_ASSURANCE = (
    "external_evidence_not_cryptographic_identity_proof"
)
_GATE_EFFECT = "candidate_precondition_evidence_only"

_TOP_KEYS = {
    "schema_version",
    "gate_id",
    "task_id",
    "application_id",
    "phase",
    "frozen_artifacts",
    "human_authorization",
    "current_identity",
    "target_snapshots",
    "bounded_process_snapshot",
    "point_in_time_open_checks",
    "sentinel_checks",
    "lease",
    "residual_race_acknowledgments",
    "gate_effect",
    "publication_authority_claimed",
    "candidate_only",
    "non_authorizing",
}
_EXPECTATION_KEYS = {
    "schema_version",
    "frozen_artifacts",
    "human_authorization",
    "current_identity",
    "target_snapshots",
    "sentinel_state",
}
_FROZEN_KEYS = {
    "implementation_sha256",
    "test_sha256",
    "evidence_sha256",
}
_EVIDENCE_HASH_KEYS = {"evidence_id", "sha256"}
_AUTHORIZATION_KEYS = {
    "reference_id",
    "provenance",
    "asserted_principal",
    "authorization_text_sha256",
    "application_id",
    "phase_scope",
    "identity_assurance",
    "revoked",
}
_PROVENANCE_KEYS = {
    "source_kind",
    "source_reference",
    "captured_by",
    "capture_method",
}
_IDENTITY_KEYS = {
    "boot",
    "operating_system",
    "volume",
    "workspace",
    "model",
    "parent",
}
_BOOT_KEYS = {"boot_id"}
_OS_KEYS = {"name", "version", "architecture"}
_VOLUME_KEYS = {"volume_id", "filesystem"}
_WORKSPACE_KEYS = {"workspace_id", "root_identity"}
_MODEL_KEYS = {"model_id", "runtime_id"}
_PARENT_KEYS = {
    "process_id",
    "process_start_token",
    "executable_identity",
}
_TARGET_KEYS = {
    "ordinal",
    "target_id",
    "path_token",
    "root_identity",
    "preimage_sha256",
    "staged_sha256",
    "observed_sha256",
    "state",
    "regular_file",
    "reparse_point",
}
_BOUNDED_SNAPSHOT_KEYS = {
    "captured_wall_time_utc",
    "captured_monotonic_ns",
    "snapshot_claims_exhaustive_inventory",
    "onedrive_fully_exited",
    "onedrive_process_matches",
    "in_scope_writer_process_matches",
    "observer_limitations_acknowledged",
}
_OPEN_CHECK_KEYS = {
    "ordinal",
    "target_id",
    "observed_sha256",
    "exclusive_open_succeeded",
    "regular_file",
    "reparse_point",
    "check_scope",
    "captured_wall_time_utc",
    "captured_monotonic_ns",
}
_SENTINEL_EXPECTATION_KEYS = {"ordinal", "sentinel_id", "expected_sha256"}
_SENTINEL_CHECK_KEYS = {
    "ordinal",
    "sentinel_id",
    "expected_sha256",
    "observed_sha256",
    "passed",
    "check_scope",
    "captured_wall_time_utc",
    "captured_monotonic_ns",
}
_LEASE_KEYS = {
    "phase",
    "issued_wall_time_utc",
    "expires_wall_time_utc",
    "issued_monotonic_ns",
    "expires_monotonic_ns",
    "max_duration_seconds",
}
_RACE_KEYS = {
    "bounded_inventory_not_exhaustive",
    "uncooperative_or_preopened_writer_can_race",
    "lost_update_before_rename_possible",
    "overwrite_after_readback_possible",
    "process_crash_recovery_only",
    "power_loss_durability_claimed",
    "thirteen_file_set_atomicity_claimed",
    "global_sidecar_install_authorized",
    "candidate_only",
    "non_authorizing",
}


class LiveGatePolicyError(ValueError):
    """Raised when the supplied live-gate evidence fails closed."""


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveGatePolicyError(f"{label} must be an object")
    return value


def _closed(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    obj = _mapping(value, label)
    actual = set(obj)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        raise LiveGatePolicyError(
            f"{label} schema drift; missing={missing}, extra={extra}"
        )
    return obj


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if not isinstance(value, (list, tuple)):
        raise LiveGatePolicyError(f"{label} must be an ordered array")
    return value


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LiveGatePolicyError(f"{label} must be a non-empty string")
    return value


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise LiveGatePolicyError(
            f"{label} must be a lowercase 64-character SHA-256"
        )
    return value


def _exact_bool(value: Any, expected: bool, label: str) -> None:
    if value is not expected:
        raise LiveGatePolicyError(f"{label} must be {expected}")


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise LiveGatePolicyError(f"{label} must be a positive integer")
    return value


def _nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise LiveGatePolicyError(f"{label} must be a non-negative integer")
    return value


def _utc(value: Any, label: str) -> datetime:
    text = _nonempty(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LiveGatePolicyError(f"{label} is not ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise LiveGatePolicyError(f"{label} must identify UTC")
    return parsed.astimezone(timezone.utc)


def _canonical(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise LiveGatePolicyError("record is not canonical-JSON compatible") from exc
    return rendered.encode("utf-8")


def _equal(actual: Any, expected: Any, label: str) -> None:
    if _canonical(actual) != _canonical(expected):
        raise LiveGatePolicyError(f"{label} drifted from frozen expectation")


def _validate_frozen_artifacts(value: Any, label: str) -> Mapping[str, Any]:
    frozen = _closed(value, _FROZEN_KEYS, label)
    _sha(frozen["implementation_sha256"], f"{label}.implementation_sha256")
    _sha(frozen["test_sha256"], f"{label}.test_sha256")
    rows = _sequence(frozen["evidence_sha256"], f"{label}.evidence_sha256")
    if not rows:
        raise LiveGatePolicyError(f"{label}.evidence_sha256 must not be empty")
    ids: list[str] = []
    for index, raw in enumerate(rows, start=1):
        row_label = f"{label}.evidence_sha256[{index}]"
        row = _closed(raw, _EVIDENCE_HASH_KEYS, row_label)
        ids.append(_nonempty(row["evidence_id"], f"{row_label}.evidence_id"))
        _sha(row["sha256"], f"{row_label}.sha256")
    if len(ids) != len(set(ids)):
        raise LiveGatePolicyError(f"{label}.evidence_id values must be unique")
    if ids != sorted(ids):
        raise LiveGatePolicyError(
            f"{label}.evidence_sha256 must use stable evidence_id order"
        )
    return frozen


def _validate_authorization(
    value: Any, label: str, application_id: str
) -> Mapping[str, Any]:
    auth = _closed(value, _AUTHORIZATION_KEYS, label)
    _nonempty(auth["reference_id"], f"{label}.reference_id")
    provenance = _closed(auth["provenance"], _PROVENANCE_KEYS, f"{label}.provenance")
    if provenance["source_kind"] != "external_human_attestation":
        raise LiveGatePolicyError(
            f"{label}.provenance.source_kind must be external_human_attestation"
        )
    for key in ("source_reference", "captured_by", "capture_method"):
        _nonempty(provenance[key], f"{label}.provenance.{key}")
    _nonempty(auth["asserted_principal"], f"{label}.asserted_principal")
    _sha(auth["authorization_text_sha256"], f"{label}.authorization_text_sha256")
    if auth["application_id"] != application_id:
        raise LiveGatePolicyError(f"{label}.application_id drift")
    if auth["phase_scope"] != ["prepare", "publish"]:
        raise LiveGatePolicyError(f"{label}.phase_scope drift")
    if auth["identity_assurance"] != _NON_CRYPTOGRAPHIC_IDENTITY_ASSURANCE:
        raise LiveGatePolicyError(
            f"{label} must not claim cryptographic human identity"
        )
    _exact_bool(auth["revoked"], False, f"{label}.revoked")
    return auth


def _validate_identity(value: Any, label: str) -> Mapping[str, Any]:
    identity = _closed(value, _IDENTITY_KEYS, label)
    boot = _closed(identity["boot"], _BOOT_KEYS, f"{label}.boot")
    operating_system = _closed(
        identity["operating_system"], _OS_KEYS, f"{label}.operating_system"
    )
    volume = _closed(identity["volume"], _VOLUME_KEYS, f"{label}.volume")
    workspace = _closed(
        identity["workspace"], _WORKSPACE_KEYS, f"{label}.workspace"
    )
    model = _closed(identity["model"], _MODEL_KEYS, f"{label}.model")
    parent = _closed(identity["parent"], _PARENT_KEYS, f"{label}.parent")
    _nonempty(boot["boot_id"], f"{label}.boot.boot_id")
    for key in _OS_KEYS:
        _nonempty(
            operating_system[key], f"{label}.operating_system.{key}"
        )
    for key in _VOLUME_KEYS:
        _nonempty(volume[key], f"{label}.volume.{key}")
    for key in _WORKSPACE_KEYS:
        _nonempty(workspace[key], f"{label}.workspace.{key}")
    for key in _MODEL_KEYS:
        _nonempty(model[key], f"{label}.model.{key}")
    _positive_int(parent["process_id"], f"{label}.parent.process_id")
    _nonempty(
        parent["process_start_token"], f"{label}.parent.process_start_token"
    )
    _nonempty(
        parent["executable_identity"], f"{label}.parent.executable_identity"
    )
    return identity


def _validate_targets(value: Any, label: str) -> Sequence[Any]:
    rows = _sequence(value, label)
    if len(rows) != TARGET_COUNT:
        raise LiveGatePolicyError(
            f"{label} must contain exactly {TARGET_COUNT} targets"
        )
    ids: list[str] = []
    path_tokens: list[str] = []
    for ordinal, raw in enumerate(rows, start=1):
        row_label = f"{label}[{ordinal}]"
        row = _closed(raw, _TARGET_KEYS, row_label)
        if row["ordinal"] != ordinal:
            raise LiveGatePolicyError(f"{row_label}.ordinal/order drift")
        ids.append(_nonempty(row["target_id"], f"{row_label}.target_id"))
        path_tokens.append(
            _nonempty(row["path_token"], f"{row_label}.path_token")
        )
        _nonempty(row["root_identity"], f"{row_label}.root_identity")
        preimage = _sha(row["preimage_sha256"], f"{row_label}.preimage_sha256")
        staged = _sha(row["staged_sha256"], f"{row_label}.staged_sha256")
        observed = _sha(row["observed_sha256"], f"{row_label}.observed_sha256")
        if preimage == staged:
            raise LiveGatePolicyError(f"{row_label} has no material byte change")
        if row["state"] != "preimage" or observed != preimage:
            raise LiveGatePolicyError(f"{row_label} is not at its frozen preimage")
        _exact_bool(row["regular_file"], True, f"{row_label}.regular_file")
        _exact_bool(row["reparse_point"], False, f"{row_label}.reparse_point")
    if len(ids) != len(set(ids)):
        raise LiveGatePolicyError(f"{label}.target_id values must be unique")
    if len(path_tokens) != len(set(path_tokens)):
        raise LiveGatePolicyError(f"{label}.path_token values must be unique")
    return rows


def _validate_sentinel_expectations(value: Any, label: str) -> Sequence[Any]:
    rows = _sequence(value, label)
    if len(rows) != SENTINEL_COUNT:
        raise LiveGatePolicyError(
            f"{label} must contain exactly {SENTINEL_COUNT} sentinels"
        )
    ids: list[str] = []
    for ordinal, raw in enumerate(rows, start=1):
        row_label = f"{label}[{ordinal}]"
        row = _closed(raw, _SENTINEL_EXPECTATION_KEYS, row_label)
        if row["ordinal"] != ordinal:
            raise LiveGatePolicyError(f"{row_label}.ordinal/order drift")
        ids.append(_nonempty(row["sentinel_id"], f"{row_label}.sentinel_id"))
        _sha(row["expected_sha256"], f"{row_label}.expected_sha256")
    if len(ids) != len(set(ids)):
        raise LiveGatePolicyError(f"{label}.sentinel_id values must be unique")
    return rows


def _validate_expectations(
    value: Any, application_id: str
) -> Mapping[str, Any]:
    expected = _closed(value, _EXPECTATION_KEYS, "expectations")
    if expected["schema_version"] != EXPECTATIONS_SCHEMA_VERSION:
        raise LiveGatePolicyError("expectations.schema_version drift")
    _validate_frozen_artifacts(
        expected["frozen_artifacts"], "expectations.frozen_artifacts"
    )
    _validate_authorization(
        expected["human_authorization"],
        "expectations.human_authorization",
        application_id,
    )
    _validate_identity(
        expected["current_identity"], "expectations.current_identity"
    )
    _validate_targets(
        expected["target_snapshots"], "expectations.target_snapshots"
    )
    _validate_sentinel_expectations(
        expected["sentinel_state"], "expectations.sentinel_state"
    )
    return expected


def _validate_lease(
    value: Any,
    phase: str,
    now_wall_time_utc: datetime,
    now_monotonic_ns: int,
) -> tuple[datetime, datetime, int, int]:
    lease = _closed(value, _LEASE_KEYS, "record.lease")
    if lease["phase"] != phase:
        raise LiveGatePolicyError("record.lease.phase drift")
    issued_wall = _utc(
        lease["issued_wall_time_utc"], "record.lease.issued_wall_time_utc"
    )
    expires_wall = _utc(
        lease["expires_wall_time_utc"], "record.lease.expires_wall_time_utc"
    )
    issued_mono = _nonnegative_int(
        lease["issued_monotonic_ns"], "record.lease.issued_monotonic_ns"
    )
    expires_mono = _positive_int(
        lease["expires_monotonic_ns"], "record.lease.expires_monotonic_ns"
    )
    max_duration = _positive_int(
        lease["max_duration_seconds"], "record.lease.max_duration_seconds"
    )
    if max_duration > MAX_LEASE_SECONDS:
        raise LiveGatePolicyError("record.lease exceeds short-lease policy")
    wall_seconds = (expires_wall - issued_wall).total_seconds()
    mono_seconds = (expires_mono - issued_mono) / 1_000_000_000
    if (
        wall_seconds <= 0
        or mono_seconds <= 0
        or wall_seconds > max_duration
        or mono_seconds > max_duration
        or abs(wall_seconds - mono_seconds) > 1.0
    ):
        raise LiveGatePolicyError("record.lease clocks disagree or exceed scope")
    if not (issued_wall <= now_wall_time_utc < expires_wall):
        raise LiveGatePolicyError("record.lease wall clock is stale or premature")
    if not (issued_mono <= now_monotonic_ns < expires_mono):
        raise LiveGatePolicyError(
            "record.lease monotonic clock is stale or premature"
        )
    return issued_wall, expires_wall, issued_mono, expires_mono


def _require_capture_in_lease(
    wall_value: Any,
    mono_value: Any,
    label: str,
    lease_bounds: tuple[datetime, datetime, int, int],
    now_wall: datetime,
    now_mono: int,
) -> None:
    issued_wall, expires_wall, issued_mono, expires_mono = lease_bounds
    captured_wall = _utc(wall_value, f"{label}.captured_wall_time_utc")
    captured_mono = _nonnegative_int(
        mono_value, f"{label}.captured_monotonic_ns"
    )
    if not (issued_wall <= captured_wall <= now_wall < expires_wall):
        raise LiveGatePolicyError(f"{label} wall-clock capture is outside lease")
    if not (issued_mono <= captured_mono <= now_mono < expires_mono):
        raise LiveGatePolicyError(f"{label} monotonic capture is outside lease")


def _validate_bounded_snapshot(
    value: Any,
    lease_bounds: tuple[datetime, datetime, int, int],
    now_wall: datetime,
    now_mono: int,
) -> None:
    label = "record.bounded_process_snapshot"
    snapshot = _closed(value, _BOUNDED_SNAPSHOT_KEYS, label)
    _require_capture_in_lease(
        snapshot["captured_wall_time_utc"],
        snapshot["captured_monotonic_ns"],
        label,
        lease_bounds,
        now_wall,
        now_mono,
    )
    _exact_bool(
        snapshot["snapshot_claims_exhaustive_inventory"],
        False,
        f"{label}.snapshot_claims_exhaustive_inventory",
    )
    _exact_bool(
        snapshot["onedrive_fully_exited"],
        True,
        f"{label}.onedrive_fully_exited",
    )
    if snapshot["onedrive_process_matches"] != []:
        raise LiveGatePolicyError(f"{label}.onedrive_process_matches must be empty")
    if snapshot["in_scope_writer_process_matches"] != []:
        raise LiveGatePolicyError(
            f"{label}.in_scope_writer_process_matches must be empty"
        )
    _exact_bool(
        snapshot["observer_limitations_acknowledged"],
        True,
        f"{label}.observer_limitations_acknowledged",
    )


def _validate_open_checks(
    value: Any,
    targets: Sequence[Any],
    lease_bounds: tuple[datetime, datetime, int, int],
    now_wall: datetime,
    now_mono: int,
) -> None:
    label = "record.point_in_time_open_checks"
    rows = _sequence(value, label)
    if len(rows) != TARGET_COUNT:
        raise LiveGatePolicyError(
            f"{label} must contain exactly {TARGET_COUNT} checks"
        )
    for ordinal, (raw, target) in enumerate(zip(rows, targets), start=1):
        row_label = f"{label}[{ordinal}]"
        row = _closed(raw, _OPEN_CHECK_KEYS, row_label)
        if row["ordinal"] != ordinal or row["target_id"] != target["target_id"]:
            raise LiveGatePolicyError(f"{row_label} target/order drift")
        if row["observed_sha256"] != target["observed_sha256"]:
            raise LiveGatePolicyError(f"{row_label}.observed_sha256 drift")
        _exact_bool(
            row["exclusive_open_succeeded"],
            True,
            f"{row_label}.exclusive_open_succeeded",
        )
        _exact_bool(row["regular_file"], True, f"{row_label}.regular_file")
        _exact_bool(row["reparse_point"], False, f"{row_label}.reparse_point")
        if row["check_scope"] != "point_in_time_only":
            raise LiveGatePolicyError(f"{row_label}.check_scope drift")
        _require_capture_in_lease(
            row["captured_wall_time_utc"],
            row["captured_monotonic_ns"],
            row_label,
            lease_bounds,
            now_wall,
            now_mono,
        )


def _validate_sentinel_checks(
    value: Any,
    expected: Sequence[Any],
    lease_bounds: tuple[datetime, datetime, int, int],
    now_wall: datetime,
    now_mono: int,
) -> None:
    label = "record.sentinel_checks"
    rows = _sequence(value, label)
    if len(rows) != SENTINEL_COUNT:
        raise LiveGatePolicyError(
            f"{label} must contain exactly {SENTINEL_COUNT} checks"
        )
    for ordinal, (raw, frozen) in enumerate(zip(rows, expected), start=1):
        row_label = f"{label}[{ordinal}]"
        row = _closed(raw, _SENTINEL_CHECK_KEYS, row_label)
        if (
            row["ordinal"] != ordinal
            or row["sentinel_id"] != frozen["sentinel_id"]
            or row["expected_sha256"] != frozen["expected_sha256"]
            or row["observed_sha256"] != frozen["expected_sha256"]
        ):
            raise LiveGatePolicyError(f"{row_label} state/order drift")
        _exact_bool(row["passed"], True, f"{row_label}.passed")
        if row["check_scope"] != "point_in_time_only":
            raise LiveGatePolicyError(f"{row_label}.check_scope drift")
        _require_capture_in_lease(
            row["captured_wall_time_utc"],
            row["captured_monotonic_ns"],
            row_label,
            lease_bounds,
            now_wall,
            now_mono,
        )


def _validate_race_acknowledgments(value: Any) -> None:
    label = "record.residual_race_acknowledgments"
    ack = _closed(value, _RACE_KEYS, label)
    for key in (
        "bounded_inventory_not_exhaustive",
        "uncooperative_or_preopened_writer_can_race",
        "lost_update_before_rename_possible",
        "overwrite_after_readback_possible",
        "process_crash_recovery_only",
        "candidate_only",
        "non_authorizing",
    ):
        _exact_bool(ack[key], True, f"{label}.{key}")
    for key in (
        "power_loss_durability_claimed",
        "thirteen_file_set_atomicity_claimed",
        "global_sidecar_install_authorized",
    ):
        _exact_bool(ack[key], False, f"{label}.{key}")


def _validate_prepare_continuity(
    prepare_record: Any,
    publish_record: Mapping[str, Any],
    publish_issued_wall: datetime,
    publish_issued_mono: int,
) -> None:
    prepare = _closed(prepare_record, _TOP_KEYS, "prepare_record")
    if prepare["schema_version"] != SCHEMA_VERSION:
        raise LiveGatePolicyError("prepare_record.schema_version drift")
    if prepare["phase"] != "prepare":
        raise LiveGatePolicyError("publish requires a prepare-phase record")
    for key in ("task_id", "application_id"):
        if prepare[key] != publish_record[key]:
            raise LiveGatePolicyError(f"prepare-to-publish {key} drift")
    _equal(
        publish_record["current_identity"],
        prepare["current_identity"],
        "prepare-to-publish current_identity",
    )
    _equal(
        publish_record["frozen_artifacts"],
        prepare["frozen_artifacts"],
        "prepare-to-publish frozen_artifacts",
    )
    _equal(
        publish_record["human_authorization"],
        prepare["human_authorization"],
        "prepare-to-publish human_authorization",
    )
    _equal(
        publish_record["target_snapshots"],
        prepare["target_snapshots"],
        "prepare-to-publish target_snapshots",
    )
    prepare_lease = _closed(
        prepare["lease"], _LEASE_KEYS, "prepare_record.lease"
    )
    if prepare_lease["phase"] != "prepare":
        raise LiveGatePolicyError("prepare_record.lease.phase drift")
    prepare_issued_wall = _utc(
        prepare_lease["issued_wall_time_utc"],
        "prepare_record.lease.issued_wall_time_utc",
    )
    prepare_issued_mono = _nonnegative_int(
        prepare_lease["issued_monotonic_ns"],
        "prepare_record.lease.issued_monotonic_ns",
    )
    wall_gap = (publish_issued_wall - prepare_issued_wall).total_seconds()
    mono_gap = (publish_issued_mono - prepare_issued_mono) / 1_000_000_000
    if (
        wall_gap < 0
        or mono_gap < 0
        or wall_gap > MAX_PREPARE_TO_PUBLISH_SECONDS
        or mono_gap > MAX_PREPARE_TO_PUBLISH_SECONDS
        or abs(wall_gap - mono_gap) > 1.0
    ):
        raise LiveGatePolicyError(
            "prepare-to-publish continuity is stale or clocks disagree"
        )


def validate_live_gate_policy(
    record: Any,
    expectations: Any,
    *,
    expected_phase: str,
    now_wall_time_utc: str | datetime,
    now_monotonic_ns: int,
    prepare_record: Any | None = None,
) -> dict[str, Any]:
    """Validate a prepare or publish live-gate record without side effects.

    ``expectations`` must come from a separately frozen adapter surface.  This
    function deliberately accepts observations as data instead of collecting
    them, so no host or provider API becomes policy authority.
    """
    if expected_phase not in PHASES:
        raise LiveGatePolicyError("expected_phase must be prepare or publish")
    now_wall = (
        now_wall_time_utc.astimezone(timezone.utc)
        if isinstance(now_wall_time_utc, datetime)
        and now_wall_time_utc.tzinfo is not None
        else _utc(now_wall_time_utc, "now_wall_time_utc")
    )
    if not isinstance(now_wall, datetime) or now_wall.tzinfo is None:
        raise LiveGatePolicyError("now_wall_time_utc must be timezone-aware")
    now_mono = _nonnegative_int(now_monotonic_ns, "now_monotonic_ns")

    live = _closed(record, _TOP_KEYS, "record")
    if live["schema_version"] != SCHEMA_VERSION:
        raise LiveGatePolicyError("record.schema_version drift")
    for key in ("gate_id", "task_id", "application_id"):
        _nonempty(live[key], f"record.{key}")
    if live["phase"] != expected_phase:
        raise LiveGatePolicyError("record.phase drift")

    expected = _validate_expectations(expectations, live["application_id"])
    frozen = _validate_frozen_artifacts(
        live["frozen_artifacts"], "record.frozen_artifacts"
    )
    authorization = _validate_authorization(
        live["human_authorization"],
        "record.human_authorization",
        live["application_id"],
    )
    identity = _validate_identity(
        live["current_identity"], "record.current_identity"
    )
    targets = _validate_targets(
        live["target_snapshots"], "record.target_snapshots"
    )
    _equal(frozen, expected["frozen_artifacts"], "frozen_artifacts")
    _equal(
        authorization,
        expected["human_authorization"],
        "human_authorization",
    )
    _equal(identity, expected["current_identity"], "current_identity")
    _equal(targets, expected["target_snapshots"], "target_snapshots")

    lease_bounds = _validate_lease(
        live["lease"], live["phase"], now_wall, now_mono
    )
    _validate_bounded_snapshot(
        live["bounded_process_snapshot"], lease_bounds, now_wall, now_mono
    )
    _validate_open_checks(
        live["point_in_time_open_checks"],
        targets,
        lease_bounds,
        now_wall,
        now_mono,
    )
    sentinels = _validate_sentinel_expectations(
        expected["sentinel_state"], "expectations.sentinel_state"
    )
    _validate_sentinel_checks(
        live["sentinel_checks"],
        sentinels,
        lease_bounds,
        now_wall,
        now_mono,
    )
    _validate_race_acknowledgments(live["residual_race_acknowledgments"])

    if live["gate_effect"] != _GATE_EFFECT:
        raise LiveGatePolicyError("record.gate_effect drift")
    _exact_bool(
        live["publication_authority_claimed"],
        False,
        "record.publication_authority_claimed",
    )
    _exact_bool(live["candidate_only"], True, "record.candidate_only")
    _exact_bool(live["non_authorizing"], True, "record.non_authorizing")

    issued_wall, _, issued_mono, _ = lease_bounds
    if expected_phase == "prepare":
        if prepare_record is not None:
            raise LiveGatePolicyError(
                "prepare phase must not receive prepare_record"
            )
    else:
        if prepare_record is None:
            raise LiveGatePolicyError(
                "publish phase requires prepare_record continuity evidence"
            )
        _validate_prepare_continuity(
            prepare_record, live, issued_wall, issued_mono
        )

    return {
        "schema_version": "rematerialization_live_gate_validation_result.v1",
        "verdict": "PASS",
        "phase": expected_phase,
        "gate_id": live["gate_id"],
        "record_sha256": hashlib.sha256(_canonical(live)).hexdigest(),
        "candidate_only": True,
        "non_authorizing": True,
        "publication_authority_claimed": False,
        "human_identity_cryptographically_verified": False,
        "bounded_process_snapshot_exhaustive": False,
        "residual_races_eliminated": False,
    }


validate_live_gate = validate_live_gate_policy

