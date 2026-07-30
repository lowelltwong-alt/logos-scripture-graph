#!/usr/bin/env python3
"""Pure policy for the T550 V9 measured live-environment gate.

This module performs no filesystem, process, clock, Windows, or publication
operations.  It validates a complete adapter measurement against separately
frozen expectations.  PASS is candidate precondition evidence only: it does
not authenticate Lowell, eliminate concurrent-writer races, or authorize an
effect.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "rematerialization_live_gate_policy.v2"
EXPECTATIONS_SCHEMA_VERSION = "rematerialization_live_gate_expectations.v2"
MEASUREMENT_SCHEMA_VERSION = "windows_live_environment_measurement.v2"
RESULT_SCHEMA_VERSION = "rematerialization_live_gate_validation_result.v2"
CONTRACT_SHA256 = (
    "beea267ec9685fa59d4b5bcadd02ed1f238b626703dde56974971d779fdcd82d"
)
PREDECESSOR_REJECTION_SHA256 = (
    "8cc0ea76a7ac0181f54617c5c7e6d82af4aff970aeb0ef9babb8f1a0467380cd"
)
TARGET_COUNT = 13
SENTINEL_COUNT = 3
MAX_LEASE_SECONDS = 120

# The adapter may observe more processes, but a caller may not narrow this
# security-relevant classification set.
BOUNDED_PROCESS_NAMES = (
    "codex.exe",
    "git.exe",
    "googledrivefs.exe",
    "onedrive.exe",
    "powershell.exe",
    "pwsh.exe",
    "python.exe",
    "pythonw.exe",
    "robocopy.exe",
    "syncthing.exe",
    "xcopy.exe",
)

_SHA = re.compile(r"^[0-9a-f]{64}$")


class LiveGatePolicyV2Error(ValueError):
    """Raised when V2 live-gate evidence fails closed."""


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return (
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise LiveGatePolicyV2Error("value is not canonical-JSON compatible") from exc


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def process_policy_sha256(names: Sequence[str] = BOUNDED_PROCESS_NAMES) -> str:
    return digest_value(list(names))


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveGatePolicyV2Error(f"{label} must be an object")
    return value


def _closed(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    row = _mapping(value, label)
    actual = set(row)
    if actual != keys:
        raise LiveGatePolicyV2Error(
            f"{label} schema drift: missing={sorted(keys - actual)}, "
            f"extra={sorted(actual - keys)}"
        )
    return row


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if not isinstance(value, list):
        raise LiveGatePolicyV2Error(f"{label} must be an ordered array")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise LiveGatePolicyV2Error(f"{label} must be a non-empty string")
    return value


def _sha(value: Any, label: str) -> str:
    text = _text(value, label)
    if not _SHA.fullmatch(text):
        raise LiveGatePolicyV2Error(f"{label} must be lowercase SHA-256")
    return text


def _bool(value: Any, expected: bool, label: str) -> None:
    if value is not expected:
        raise LiveGatePolicyV2Error(f"{label} must be {expected}")


def _int(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise LiveGatePolicyV2Error(f"{label} must be an integer >= {minimum}")
    return value


def _utc(value: Any, label: str) -> datetime:
    text = _text(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LiveGatePolicyV2Error(f"{label} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise LiveGatePolicyV2Error(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _same(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise LiveGatePolicyV2Error(f"{label} drift")


_ARTIFACT_KEYS = {"artifact_id", "sha256"}
_TARGET_EXPECTATION_KEYS = {
    "ordinal",
    "target_id",
    "role",
    "path_token",
    "preimage_sha256",
    "staged_sha256",
}
_SENTINEL_EXPECTATION_KEYS = {
    "ordinal",
    "sentinel_id",
    "role",
    "path_token",
    "expected_sha256",
}
_AUTH_KEYS = {
    "reference_id",
    "source_kind",
    "source_reference",
    "asserted_principal",
    "authorization_text_sha256",
    "identity_assurance",
    "local_json_alone_sufficient",
    "observed_by_checker",
    "observed_by_boss",
    "revoked",
}
_FREEZE_KEYS = {
    "freeze_id",
    "frozen_at_utc",
    "pre_freeze_boot_identity",
    "implementation_and_test_hashes",
    "evidence_hashes",
    "targets",
    "sentinels",
    "bounded_process_names",
    "bounded_process_policy_sha256",
}
_EXPECTATION_KEYS = {
    "schema_version",
    "contract_sha256",
    "predecessor_rejection_sha256",
    "task_id",
    "book",
    "application_id",
    "freeze",
    "human_authorization",
    "candidate_only",
    "non_authorizing",
}


def _artifact_rows(value: Any, label: str) -> list[dict[str, str]]:
    rows = _sequence(value, label)
    if not rows:
        raise LiveGatePolicyV2Error(f"{label} must not be empty")
    result: list[dict[str, str]] = []
    for index, raw in enumerate(rows):
        row = _closed(raw, _ARTIFACT_KEYS, f"{label}[{index}]")
        result.append(
            {
                "artifact_id": _text(
                    row["artifact_id"], f"{label}[{index}].artifact_id"
                ),
                "sha256": _sha(row["sha256"], f"{label}[{index}].sha256"),
            }
        )
    ids = [row["artifact_id"] for row in result]
    if ids != sorted(set(ids)):
        raise LiveGatePolicyV2Error(f"{label} IDs must be unique and sorted")
    return result


def _target_expectations(value: Any) -> list[dict[str, Any]]:
    rows = _sequence(value, "expectations.freeze.targets")
    if len(rows) != TARGET_COUNT:
        raise LiveGatePolicyV2Error("expectations must freeze exactly 13 targets")
    result: list[dict[str, Any]] = []
    for ordinal, raw in enumerate(rows, 1):
        row = _closed(
            raw,
            _TARGET_EXPECTATION_KEYS,
            f"expectations.freeze.targets[{ordinal - 1}]",
        )
        if row["ordinal"] != ordinal:
            raise LiveGatePolicyV2Error("target expectation order drift")
        result.append(
            {
                "ordinal": ordinal,
                "target_id": _text(row["target_id"], "target_id"),
                "role": _text(row["role"], "target role"),
                "path_token": _text(row["path_token"], "target path_token"),
                "preimage_sha256": _sha(
                    row["preimage_sha256"], "target preimage_sha256"
                ),
                "staged_sha256": _sha(
                    row["staged_sha256"], "target staged_sha256"
                ),
            }
        )
    if len({row["target_id"] for row in result}) != TARGET_COUNT:
        raise LiveGatePolicyV2Error("target IDs must be unique")
    if len({row["path_token"] for row in result}) != TARGET_COUNT:
        raise LiveGatePolicyV2Error("target path tokens must be unique")
    return result


def _sentinel_expectations(value: Any) -> list[dict[str, Any]]:
    rows = _sequence(value, "expectations.freeze.sentinels")
    if len(rows) != SENTINEL_COUNT:
        raise LiveGatePolicyV2Error("expectations must freeze exactly 3 sentinels")
    result: list[dict[str, Any]] = []
    for ordinal, raw in enumerate(rows, 1):
        row = _closed(
            raw,
            _SENTINEL_EXPECTATION_KEYS,
            f"expectations.freeze.sentinels[{ordinal - 1}]",
        )
        if row["ordinal"] != ordinal:
            raise LiveGatePolicyV2Error("sentinel expectation order drift")
        result.append(
            {
                "ordinal": ordinal,
                "sentinel_id": _text(row["sentinel_id"], "sentinel_id"),
                "role": _text(row["role"], "sentinel role"),
                "path_token": _text(row["path_token"], "sentinel path_token"),
                "expected_sha256": _sha(
                    row["expected_sha256"], "sentinel expected_sha256"
                ),
            }
        )
    return result


def _validate_expectations(value: Any) -> dict[str, Any]:
    row = _closed(value, _EXPECTATION_KEYS, "expectations")
    if row["schema_version"] != EXPECTATIONS_SCHEMA_VERSION:
        raise LiveGatePolicyV2Error("expectations schema_version drift")
    if row["contract_sha256"] != CONTRACT_SHA256:
        raise LiveGatePolicyV2Error("V2 contract hash drift")
    if row["predecessor_rejection_sha256"] != PREDECESSOR_REJECTION_SHA256:
        raise LiveGatePolicyV2Error("predecessor rejection hash drift")
    if row["task_id"] != "T550" or row["book"] != "Hos":
        raise LiveGatePolicyV2Error("task or book drift")
    application_id = _text(row["application_id"], "expectations.application_id")
    _bool(row["candidate_only"], True, "expectations.candidate_only")
    _bool(row["non_authorizing"], True, "expectations.non_authorizing")

    freeze = _closed(row["freeze"], _FREEZE_KEYS, "expectations.freeze")
    frozen_at = _utc(freeze["frozen_at_utc"], "freeze.frozen_at_utc")
    _text(freeze["freeze_id"], "freeze.freeze_id")
    _text(
        freeze["pre_freeze_boot_identity"],
        "freeze.pre_freeze_boot_identity",
    )
    implementation = _artifact_rows(
        freeze["implementation_and_test_hashes"],
        "freeze.implementation_and_test_hashes",
    )
    evidence = _artifact_rows(freeze["evidence_hashes"], "freeze.evidence_hashes")
    targets = _target_expectations(freeze["targets"])
    sentinels = _sentinel_expectations(freeze["sentinels"])
    names = _sequence(freeze["bounded_process_names"], "bounded_process_names")
    if tuple(names) != BOUNDED_PROCESS_NAMES:
        raise LiveGatePolicyV2Error(
            "bounded process policy is caller-omittable or drifted"
        )
    if freeze["bounded_process_policy_sha256"] != process_policy_sha256():
        raise LiveGatePolicyV2Error("bounded process policy digest drift")

    auth = _closed(
        row["human_authorization"], _AUTH_KEYS, "expectations.human_authorization"
    )
    _text(auth["reference_id"], "authorization.reference_id")
    if auth["source_kind"] != "external_human_attestation":
        raise LiveGatePolicyV2Error("authorization must be external human evidence")
    _text(auth["source_reference"], "authorization.source_reference")
    if auth["asserted_principal"] != "Lowell Wong":
        raise LiveGatePolicyV2Error("authorization asserted principal drift")
    _sha(
        auth["authorization_text_sha256"],
        "authorization.authorization_text_sha256",
    )
    if (
        auth["identity_assurance"]
        != "external_evidence_not_cryptographic_identity_proof"
    ):
        raise LiveGatePolicyV2Error("authorization identity assurance overclaim")
    _bool(
        auth["local_json_alone_sufficient"],
        False,
        "authorization.local_json_alone_sufficient",
    )
    _bool(auth["observed_by_checker"], True, "authorization.observed_by_checker")
    _bool(auth["observed_by_boss"], True, "authorization.observed_by_boss")
    _bool(auth["revoked"], False, "authorization.revoked")
    return {
        "application_id": application_id,
        "frozen_at": frozen_at,
        "pre_freeze_boot_identity": freeze["pre_freeze_boot_identity"],
        "implementation": implementation,
        "evidence": evidence,
        "targets": targets,
        "sentinels": sentinels,
        "authorization": dict(auth),
        "raw": dict(row),
    }


_IDENTITY_KEYS = {
    "volume_serial",
    "file_id",
    "attributes",
    "is_directory",
    "reparse_point",
}
_ROOT_KEYS = {"path_token", "identity"}
_PARENT_KEYS = {"parent_id", "path_token", "identity"}
_OS_KEYS = {"name", "version", "build", "architecture"}
_VOLUME_KEYS = {
    "volume_guid",
    "volume_serial",
    "filesystem",
    "filesystem_flags",
}
_BOOT_KEYS = {"boot_identity", "boot_time_utc"}
_PARENT_PROCESS_KEYS = {
    "pid",
    "start_token",
    "executable_identity",
}
_CAPTURE_KEYS = {
    "start_wall_time_utc",
    "end_wall_time_utc",
    "start_monotonic_ns",
    "end_monotonic_ns",
    "max_duration_seconds",
}
_MEASURED_TARGET_KEYS = {
    "ordinal",
    "target_id",
    "role",
    "path_token",
    "parent_id",
    "identity",
    "size_bytes",
    "expected_preimage_sha256",
    "expected_staged_sha256",
    "observed_sha256",
    "regular_file",
    "reparse_point",
    "exclusive_open_succeeded",
    "open_wall_time_utc",
    "open_monotonic_ns",
}
_MEASURED_SENTINEL_KEYS = {
    "ordinal",
    "sentinel_id",
    "role",
    "path_token",
    "parent_id",
    "identity",
    "size_bytes",
    "expected_sha256",
    "observed_sha256",
    "regular_file",
    "reparse_point",
    "deny_write_delete_open_succeeded",
    "open_wall_time_utc",
    "open_monotonic_ns",
}
_PROCESS_POLICY_KEYS = {"names", "sha256"}
_PROCESS_MATCH_KEYS = {
    "pid",
    "name",
    "classification",
    "is_current_process",
}
_PROCESS_SNAPSHOT_KEYS = {
    "inventory_exhaustive",
    "current_process_id",
    "observed_process_count",
    "matched_processes",
    "onedrive_matches",
    "in_scope_writer_matches",
    "observer_limitations_acknowledged",
}
_EFFECT_KEYS = {
    "read_only_measurement",
    "probe_files_created",
    "directory_members_changed",
    "file_bytes_changed",
    "delete_or_replace_attempted",
    "attempt_created",
    "restart_or_onedrive_action_attempted",
    "publication_attempted",
}
_RACE_KEYS = {
    "bounded_inventory_not_exhaustive",
    "future_or_preopened_writers_excluded",
    "lost_update_before_rename_possible",
    "overwrite_after_readback_possible",
    "process_crash_recovery_only",
    "power_loss_durability_claimed",
    "thirteen_file_set_atomicity_claimed",
    "global_sidecar_install_authorized",
}
_MEASUREMENT_KEYS = {
    "schema_version",
    "gate_id",
    "task_id",
    "book",
    "application_id",
    "phase",
    "capture",
    "boot",
    "operating_system",
    "volume",
    "workspace",
    "model",
    "canonical_parents",
    "parent_process",
    "targets",
    "sentinels",
    "process_policy",
    "process_snapshot",
    "effects",
    "residual_races",
    "candidate_only",
    "non_authorizing",
}


def _identity(value: Any, label: str) -> dict[str, Any]:
    row = _closed(value, _IDENTITY_KEYS, label)
    _int(row["volume_serial"], f"{label}.volume_serial")
    _text(row["file_id"], f"{label}.file_id")
    _int(row["attributes"], f"{label}.attributes")
    if not isinstance(row["is_directory"], bool):
        raise LiveGatePolicyV2Error(f"{label}.is_directory must be a boolean")
    _bool(row["reparse_point"], False, f"{label}.reparse_point")
    return dict(row)


def _root(value: Any, label: str) -> dict[str, Any]:
    row = _closed(value, _ROOT_KEYS, label)
    result = {
        "path_token": _text(row["path_token"], f"{label}.path_token"),
        "identity": _identity(row["identity"], f"{label}.identity"),
    }
    _bool(result["identity"]["is_directory"], True, f"{label}.is_directory")
    return result


def _parents(value: Any, volume_serial: int) -> list[dict[str, Any]]:
    rows = _sequence(value, "measurement.canonical_parents")
    if not rows:
        raise LiveGatePolicyV2Error("canonical parent list must not be empty")
    result: list[dict[str, Any]] = []
    for index, raw in enumerate(rows):
        row = _closed(raw, _PARENT_KEYS, f"canonical_parents[{index}]")
        identity = _identity(row["identity"], f"canonical_parents[{index}].identity")
        if identity["volume_serial"] != volume_serial:
            raise LiveGatePolicyV2Error("canonical parent volume drift")
        _bool(
            identity["is_directory"],
            True,
            f"canonical_parents[{index}].is_directory",
        )
        result.append(
            {
                "parent_id": _text(row["parent_id"], "canonical parent_id"),
                "path_token": _text(row["path_token"], "canonical parent path_token"),
                "identity": identity,
            }
        )
    if [row["parent_id"] for row in result] != sorted(
        {row["parent_id"] for row in result}
    ):
        raise LiveGatePolicyV2Error("canonical parents must be unique and sorted")
    return result


def _capture(value: Any, now_wall: datetime, now_mono: int) -> dict[str, Any]:
    row = _closed(value, _CAPTURE_KEYS, "measurement.capture")
    start_wall = _utc(row["start_wall_time_utc"], "capture.start_wall_time_utc")
    end_wall = _utc(row["end_wall_time_utc"], "capture.end_wall_time_utc")
    start_mono = _int(
        row["start_monotonic_ns"], "capture.start_monotonic_ns"
    )
    end_mono = _int(row["end_monotonic_ns"], "capture.end_monotonic_ns")
    maximum = _int(
        row["max_duration_seconds"], "capture.max_duration_seconds", minimum=1
    )
    if maximum > MAX_LEASE_SECONDS:
        raise LiveGatePolicyV2Error("measurement lease exceeds 120 seconds")
    wall_duration = (end_wall - start_wall).total_seconds()
    mono_duration = (end_mono - start_mono) / 1_000_000_000
    if (
        wall_duration < 0
        or mono_duration < 0
        or wall_duration > maximum
        or mono_duration > maximum
        or abs(wall_duration - mono_duration) > 1.0
    ):
        raise LiveGatePolicyV2Error("measurement dual-clock duration drift")
    wall_age = (now_wall - end_wall).total_seconds()
    mono_age = (now_mono - end_mono) / 1_000_000_000
    if (
        wall_age < 0
        or mono_age < 0
        or wall_age > maximum
        or mono_age > maximum
        or abs(wall_age - mono_age) > 1.0
    ):
        raise LiveGatePolicyV2Error("measurement is stale or clocks disagree")
    return {
        "start_wall": start_wall,
        "end_wall": end_wall,
        "start_mono": start_mono,
        "end_mono": end_mono,
        "raw": dict(row),
    }


def _inside_capture(
    wall_value: Any,
    mono_value: Any,
    capture: Mapping[str, Any],
    label: str,
) -> None:
    wall = _utc(wall_value, f"{label}.wall")
    mono = _int(mono_value, f"{label}.mono")
    if not (
        capture["start_wall"] <= wall <= capture["end_wall"]
        and capture["start_mono"] <= mono <= capture["end_mono"]
    ):
        raise LiveGatePolicyV2Error(f"{label} is outside the capture lease")


def _validate_measurement(
    value: Any,
    expected: Mapping[str, Any],
    *,
    expected_phase: str,
    now_wall: datetime,
    now_mono: int,
) -> dict[str, Any]:
    row = _closed(value, _MEASUREMENT_KEYS, "measurement")
    if row["schema_version"] != MEASUREMENT_SCHEMA_VERSION:
        raise LiveGatePolicyV2Error("measurement schema_version drift")
    if row["task_id"] != "T550" or row["book"] != "Hos":
        raise LiveGatePolicyV2Error("measurement task/book drift")
    if row["application_id"] != expected["application_id"]:
        raise LiveGatePolicyV2Error("measurement application_id drift")
    if row["phase"] != expected_phase:
        raise LiveGatePolicyV2Error("measurement phase drift")
    _text(row["gate_id"], "measurement.gate_id")
    _bool(row["candidate_only"], True, "measurement.candidate_only")
    _bool(row["non_authorizing"], True, "measurement.non_authorizing")
    capture = _capture(row["capture"], now_wall, now_mono)

    boot = _closed(row["boot"], _BOOT_KEYS, "measurement.boot")
    boot_identity = _text(boot["boot_identity"], "boot.boot_identity")
    boot_time = _utc(boot["boot_time_utc"], "boot.boot_time_utc")
    if boot_identity == expected["pre_freeze_boot_identity"]:
        raise LiveGatePolicyV2Error("Windows restart after freeze is not proven")
    if boot_time <= expected["frozen_at"]:
        raise LiveGatePolicyV2Error("current boot is not after the frozen hashes")

    operating_system = _closed(
        row["operating_system"], _OS_KEYS, "measurement.operating_system"
    )
    for key in _OS_KEYS:
        _text(operating_system[key], f"operating_system.{key}")
    volume = _closed(row["volume"], _VOLUME_KEYS, "measurement.volume")
    _text(volume["volume_guid"], "volume.volume_guid")
    volume_serial = _int(volume["volume_serial"], "volume.volume_serial")
    if str(volume["filesystem"]).upper() != "NTFS":
        raise LiveGatePolicyV2Error("V9 environment must be NTFS")
    flags = _sequence(volume["filesystem_flags"], "volume.filesystem_flags")
    if not flags or any(not isinstance(item, str) or not item for item in flags):
        raise LiveGatePolicyV2Error("volume filesystem flags are incomplete")

    workspace = _root(row["workspace"], "measurement.workspace")
    model = _root(row["model"], "measurement.model")
    for label, root in (("workspace", workspace), ("model", model)):
        if root["identity"]["volume_serial"] != volume_serial:
            raise LiveGatePolicyV2Error(f"{label} volume identity drift")
    parents = _parents(row["canonical_parents"], volume_serial)
    parent_ids = {item["parent_id"] for item in parents}

    parent_process = _closed(
        row["parent_process"], _PARENT_PROCESS_KEYS, "measurement.parent_process"
    )
    _int(parent_process["pid"], "parent_process.pid", minimum=1)
    _text(parent_process["start_token"], "parent_process.start_token")
    _text(
        parent_process["executable_identity"],
        "parent_process.executable_identity",
    )

    measured_targets = _sequence(row["targets"], "measurement.targets")
    if len(measured_targets) != TARGET_COUNT:
        raise LiveGatePolicyV2Error("measurement must contain 13 targets")
    target_results: list[dict[str, Any]] = []
    identities: set[tuple[int, str]] = set()
    for index, (raw, frozen) in enumerate(
        zip(measured_targets, expected["targets"], strict=True)
    ):
        measured = _closed(raw, _MEASURED_TARGET_KEYS, f"targets[{index}]")
        for key in ("ordinal", "target_id", "role", "path_token"):
            if measured[key] != frozen[key]:
                raise LiveGatePolicyV2Error(f"target {index + 1} {key} drift")
        if measured["parent_id"] not in parent_ids:
            raise LiveGatePolicyV2Error("target parent identity is not frozen")
        identity = _identity(measured["identity"], f"targets[{index}].identity")
        if identity["volume_serial"] != volume_serial:
            raise LiveGatePolicyV2Error("target volume identity drift")
        _bool(identity["is_directory"], False, "target identity is_directory")
        identity_key = (identity["volume_serial"], identity["file_id"])
        if identity_key in identities:
            raise LiveGatePolicyV2Error("target/sentinel file identity alias")
        identities.add(identity_key)
        _int(measured["size_bytes"], f"targets[{index}].size_bytes")
        if (
            measured["expected_preimage_sha256"] != frozen["preimage_sha256"]
            or measured["expected_staged_sha256"] != frozen["staged_sha256"]
            or measured["observed_sha256"] != frozen["preimage_sha256"]
        ):
            raise LiveGatePolicyV2Error("target hash allowlist drift")
        _bool(measured["regular_file"], True, "target regular_file")
        _bool(measured["reparse_point"], False, "target reparse_point")
        _bool(
            measured["exclusive_open_succeeded"],
            True,
            "target exclusive_open_succeeded",
        )
        _inside_capture(
            measured["open_wall_time_utc"],
            measured["open_monotonic_ns"],
            capture,
            f"targets[{index}].open",
        )
        target_results.append(dict(measured))

    measured_sentinels = _sequence(row["sentinels"], "measurement.sentinels")
    if len(measured_sentinels) != SENTINEL_COUNT:
        raise LiveGatePolicyV2Error("measurement must contain 3 sentinels")
    sentinel_results: list[dict[str, Any]] = []
    for index, (raw, frozen) in enumerate(
        zip(measured_sentinels, expected["sentinels"], strict=True)
    ):
        measured = _closed(raw, _MEASURED_SENTINEL_KEYS, f"sentinels[{index}]")
        for key in ("ordinal", "sentinel_id", "role", "path_token"):
            if measured[key] != frozen[key]:
                raise LiveGatePolicyV2Error(f"sentinel {index + 1} {key} drift")
        if measured["parent_id"] not in parent_ids:
            raise LiveGatePolicyV2Error("sentinel parent identity is not frozen")
        identity = _identity(measured["identity"], f"sentinels[{index}].identity")
        if identity["volume_serial"] != volume_serial:
            raise LiveGatePolicyV2Error("sentinel volume identity drift")
        _bool(identity["is_directory"], False, "sentinel identity is_directory")
        identity_key = (identity["volume_serial"], identity["file_id"])
        if identity_key in identities:
            raise LiveGatePolicyV2Error("target/sentinel file identity alias")
        identities.add(identity_key)
        _int(measured["size_bytes"], f"sentinels[{index}].size_bytes")
        if (
            measured["expected_sha256"] != frozen["expected_sha256"]
            or measured["observed_sha256"] != frozen["expected_sha256"]
        ):
            raise LiveGatePolicyV2Error("sentinel hash allowlist drift")
        _bool(measured["regular_file"], True, "sentinel regular_file")
        _bool(measured["reparse_point"], False, "sentinel reparse_point")
        _bool(
            measured["deny_write_delete_open_succeeded"],
            True,
            "sentinel deny_write_delete_open_succeeded",
        )
        _inside_capture(
            measured["open_wall_time_utc"],
            measured["open_monotonic_ns"],
            capture,
            f"sentinels[{index}].open",
        )
        sentinel_results.append(dict(measured))

    process_policy = _closed(
        row["process_policy"], _PROCESS_POLICY_KEYS, "measurement.process_policy"
    )
    if tuple(process_policy["names"]) != BOUNDED_PROCESS_NAMES:
        raise LiveGatePolicyV2Error("measurement process policy can omit names")
    if process_policy["sha256"] != process_policy_sha256():
        raise LiveGatePolicyV2Error("measurement process policy digest drift")
    process_snapshot = _closed(
        row["process_snapshot"],
        _PROCESS_SNAPSHOT_KEYS,
        "measurement.process_snapshot",
    )
    _bool(
        process_snapshot["inventory_exhaustive"],
        False,
        "process_snapshot.inventory_exhaustive",
    )
    _int(process_snapshot["current_process_id"], "current_process_id", minimum=1)
    _int(process_snapshot["observed_process_count"], "observed_process_count")
    matches = _sequence(
        process_snapshot["matched_processes"], "matched_processes"
    )
    for index, raw_match in enumerate(matches):
        match = _closed(raw_match, _PROCESS_MATCH_KEYS, f"matched_processes[{index}]")
        _int(match["pid"], "matched process pid", minimum=1)
        name = _text(match["name"], "matched process name").casefold()
        if name not in BOUNDED_PROCESS_NAMES:
            raise LiveGatePolicyV2Error("matched process is outside frozen policy")
        _text(match["classification"], "matched process classification")
        if not isinstance(match["is_current_process"], bool):
            raise LiveGatePolicyV2Error("matched process current flag is invalid")
    if process_snapshot["onedrive_matches"] != []:
        raise LiveGatePolicyV2Error("OneDrive is not fully exited")
    if process_snapshot["in_scope_writer_matches"] != []:
        raise LiveGatePolicyV2Error("an in-scope writer process is present")
    _bool(
        process_snapshot["observer_limitations_acknowledged"],
        True,
        "observer limitations",
    )

    effects = _closed(row["effects"], _EFFECT_KEYS, "measurement.effects")
    for key, required in {
        "read_only_measurement": True,
        "probe_files_created": False,
        "directory_members_changed": False,
        "file_bytes_changed": False,
        "delete_or_replace_attempted": False,
        "attempt_created": False,
        "restart_or_onedrive_action_attempted": False,
        "publication_attempted": False,
    }.items():
        _bool(effects[key], required, f"effects.{key}")
    races = _closed(
        row["residual_races"], _RACE_KEYS, "measurement.residual_races"
    )
    for key, required in {
        "bounded_inventory_not_exhaustive": True,
        "future_or_preopened_writers_excluded": False,
        "lost_update_before_rename_possible": True,
        "overwrite_after_readback_possible": True,
        "process_crash_recovery_only": True,
        "power_loss_durability_claimed": False,
        "thirteen_file_set_atomicity_claimed": False,
        "global_sidecar_install_authorized": False,
    }.items():
        _bool(races[key], required, f"residual_races.{key}")
    return {
        "raw": dict(row),
        "capture": capture,
        "boot": dict(boot),
        "operating_system": dict(operating_system),
        "volume": dict(volume),
        "workspace": workspace,
        "model": model,
        "canonical_parents": parents,
        "parent_process": dict(parent_process),
        "targets": target_results,
        "sentinels": sentinel_results,
        "process_policy": dict(process_policy),
    }


def _continuity_projection(measured: Mapping[str, Any]) -> dict[str, Any]:
    target_fields = (
        "ordinal",
        "target_id",
        "role",
        "path_token",
        "parent_id",
        "identity",
        "size_bytes",
        "expected_preimage_sha256",
        "expected_staged_sha256",
        "observed_sha256",
    )
    sentinel_fields = (
        "ordinal",
        "sentinel_id",
        "role",
        "path_token",
        "parent_id",
        "identity",
        "size_bytes",
        "expected_sha256",
        "observed_sha256",
    )
    return {
        "boot": measured["boot"],
        "operating_system": measured["operating_system"],
        "volume": measured["volume"],
        "workspace": measured["workspace"],
        "model": measured["model"],
        "canonical_parents": measured["canonical_parents"],
        "parent_process": measured["parent_process"],
        "process_policy": measured["process_policy"],
        "targets": [
            {key: row[key] for key in target_fields} for row in measured["targets"]
        ],
        "sentinels": [
            {key: row[key] for key in sentinel_fields}
            for row in measured["sentinels"]
        ],
    }


def _result(
    measured: Mapping[str, Any],
    expected: Mapping[str, Any],
    *,
    phase: str,
    now_wall: datetime,
    now_mono: int,
) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA_VERSION,
        "verdict": "PASS",
        "phase": phase,
        "gate_id": measured["raw"]["gate_id"],
        "application_id": expected["application_id"],
        "expectations_sha256": digest_value(expected["raw"]),
        "raw_measurement_sha256": digest_value(measured["raw"]),
        "continuity_projection_sha256": digest_value(
            _continuity_projection(measured)
        ),
        "validated_at_wall_time_utc": now_wall.isoformat().replace("+00:00", "Z"),
        "validated_at_monotonic_ns": now_mono,
        "candidate_precondition_evidence_only": True,
        "human_identity_cryptographically_verified": False,
        "bounded_process_inventory_exhaustive": False,
        "residual_writer_races_eliminated": False,
        "publication_authority_claimed": False,
        "candidate_only": True,
        "non_authorizing": True,
    }


def validate_live_gate_policy_v2(
    measurement: Any,
    expectations: Any,
    *,
    expected_phase: str,
    now_wall_time_utc: str | datetime,
    now_monotonic_ns: int,
    prepare_measurement: Any | None = None,
    prepare_result: Any | None = None,
) -> dict[str, Any]:
    """Validate one prepare or publish measurement without side effects."""
    if expected_phase not in ("prepare", "publish"):
        raise LiveGatePolicyV2Error("expected_phase must be prepare or publish")
    now_wall = (
        now_wall_time_utc.astimezone(timezone.utc)
        if isinstance(now_wall_time_utc, datetime)
        and now_wall_time_utc.tzinfo is not None
        else _utc(now_wall_time_utc, "now_wall_time_utc")
    )
    now_mono = _int(now_monotonic_ns, "now_monotonic_ns")
    expected = _validate_expectations(expectations)
    measured = _validate_measurement(
        measurement,
        expected,
        expected_phase=expected_phase,
        now_wall=now_wall,
        now_mono=now_mono,
    )
    result = _result(
        measured,
        expected,
        phase=expected_phase,
        now_wall=now_wall,
        now_mono=now_mono,
    )
    if expected_phase == "prepare":
        if prepare_measurement is not None or prepare_result is not None:
            raise LiveGatePolicyV2Error("prepare phase cannot receive prior evidence")
        return result
    if prepare_measurement is None or prepare_result is None:
        raise LiveGatePolicyV2Error(
            "publish requires exact prepare measurement and PASS result"
        )
    prior = _mapping(prepare_result, "prepare_result")
    original_wall = _utc(
        prior.get("validated_at_wall_time_utc"),
        "prepare_result.validated_at_wall_time_utc",
    )
    original_mono = _int(
        prior.get("validated_at_monotonic_ns"),
        "prepare_result.validated_at_monotonic_ns",
    )
    recomputed_measured = _validate_measurement(
        prepare_measurement,
        expected,
        expected_phase="prepare",
        now_wall=original_wall,
        now_mono=original_mono,
    )
    recomputed_result = _result(
        recomputed_measured,
        expected,
        phase="prepare",
        now_wall=original_wall,
        now_mono=original_mono,
    )
    if dict(prior) != recomputed_result:
        raise LiveGatePolicyV2Error("prepare PASS result does not recompute exactly")
    _same(
        _continuity_projection(measured),
        _continuity_projection(recomputed_measured),
        "prepare-to-publish material identity and sentinel continuity",
    )
    result["prepare_result_sha256"] = digest_value(recomputed_result)
    result["prepare_measurement_sha256"] = digest_value(
        recomputed_measured["raw"]
    )
    return result


validate_live_gate = validate_live_gate_policy_v2
