#!/usr/bin/env python3
"""Lossless Windows adapter for the T550 V9 live-gate policy V2.

The adapter delegates read-only handle measurement to the independently tested
V1 collector, fixes the bounded process-name policy in code, records dual
clocks around every held-file open, and emits the exact closed record consumed
by ``rematerialization_live_gate_policy_v2``.  It never creates probes,
attempts, or publication artifacts and never deletes or replaces a path.
"""
from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime, timezone
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Callable, Mapping, Protocol, Sequence


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
V1_PATH = MODEL / "checks" / "windows_live_environment_measurement_v1.py"
POLICY_PATH = MODEL / "checks" / "rematerialization_live_gate_policy_v2.py"
CONTRACT_PATH = MODEL / "reviews" / "Hos" / "v9_live_gate_contract_v2.json"
CONTRACT_SHA256 = (
    "beea267ec9685fa59d4b5bcadd02ed1f238b626703dde56974971d779fdcd82d"
)


class WindowsLiveEnvironmentV2Error(RuntimeError):
    """Raised when the V2 adapter cannot produce exact read-only evidence."""


@dataclass(frozen=True)
class TargetExpectation:
    ordinal: int
    target_id: str
    role: str
    path_token: str
    path: Path
    parent_id: str
    preimage_sha256: str
    staged_sha256: str


@dataclass(frozen=True)
class SentinelExpectation:
    ordinal: int
    sentinel_id: str
    role: str
    path_token: str
    path: Path
    parent_id: str
    expected_sha256: str


class Clock(Protocol):
    def now_utc(self) -> datetime:
        ...

    def monotonic_ns(self) -> int:
        ...


class SystemClock:
    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic_ns(self) -> int:
        return time.monotonic_ns()


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise WindowsLiveEnvironmentV2Error(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_bytes(value: Any) -> bytes:
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


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _iso(value: datetime) -> str:
    if value.tzinfo is None:
        raise WindowsLiveEnvironmentV2Error("clock returned naive datetime")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _keys(value: Any, expected: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise WindowsLiveEnvironmentV2Error(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        raise WindowsLiveEnvironmentV2Error(
            f"{label} schema drift: missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )
    return value


def _assert_sha(value: str, label: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise WindowsLiveEnvironmentV2Error(
            f"{label} is not lowercase SHA-256"
        )


def _path_key(path: Path) -> str:
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def _member_digest(names: Sequence[str]) -> str:
    ordered = sorted(str(name) for name in names)
    if len(ordered) != len(set(ordered)):
        raise WindowsLiveEnvironmentV2Error(
            "directory member enumeration contains duplicates"
        )
    return _digest(ordered)


def _object_identity(source: Any, *, directory: bool) -> dict[str, Any]:
    return _identity(
        {
            "volume_serial": source.volume_serial,
            "file_id": source.file_id,
            "attributes": source.attributes,
            "is_directory": source.is_directory,
            "is_reparse_point": source.is_reparse_point,
        },
        directory=directory,
    )


def _identity(source: Mapping[str, Any], *, directory: bool) -> dict[str, Any]:
    row = _keys(
        source,
        {
            "volume_serial",
            "file_id",
            "attributes",
            "is_directory",
            "is_reparse_point",
        },
        "V1 identity",
    )
    if row["is_directory"] is not directory:
        raise WindowsLiveEnvironmentV2Error("V1 identity kind drift")
    if row["is_reparse_point"] is not False:
        raise WindowsLiveEnvironmentV2Error("V1 reparse identity rejected")
    return {
        "volume_serial": int(row["volume_serial"]),
        "file_id": str(row["file_id"]),
        "attributes": int(row["attributes"]),
        "is_directory": directory,
        "reparse_point": False,
    }


class _TimedHeldFile(AbstractContextManager):
    def __init__(
        self,
        inner: AbstractContextManager,
        *,
        logical_path: str,
        clock: Clock,
        observations: dict[str, tuple[str, int]],
    ) -> None:
        self._inner = inner
        self._logical_path = logical_path
        self._clock = clock
        self._observations = observations

    def __enter__(self):
        value = self._inner.__enter__()
        self._observations[self._logical_path] = (
            _iso(self._clock.now_utc()),
            self._clock.monotonic_ns(),
        )
        return value

    def __exit__(self, exc_type, exc, traceback) -> bool:
        return bool(self._inner.__exit__(exc_type, exc, traceback))


class _TimedBackend:
    """Transparent V1 backend wrapper that timestamps successful held opens."""

    def __init__(self, inner: Any, clock: Clock) -> None:
        self._inner = inner
        self._clock = clock
        self.current_pid = inner.current_pid
        self.open_observations: dict[str, tuple[str, int]] = {}

    def now_utc(self):
        return self._clock.now_utc()

    def boot_facts(self):
        return self._inner.boot_facts()

    def os_facts(self):
        return self._inner.os_facts()

    def volume_facts(self, path):
        return self._inner.volume_facts(path)

    def assert_no_reparse_chain(self, path):
        return self._inner.assert_no_reparse_chain(path)

    def directory_identity(self, path):
        return self._inner.directory_identity(path)

    def directory_members(self, path):
        return self._inner.directory_members(path)

    def snapshot_regular_file(self, path):
        return self._inner.snapshot_regular_file(path)

    def list_processes(self):
        return self._inner.list_processes()

    def hold_regular_file(self, path, mode):
        logical = _path_key(Path(path))
        return _TimedHeldFile(
            self._inner.hold_regular_file(path, mode),
            logical_path=logical,
            clock=self._clock,
            observations=self.open_observations,
        )


def _default_parent_process_facts() -> dict[str, Any]:
    """Read the current parent process identity without mutating it."""
    if os.name != "nt":
        raise WindowsLiveEnvironmentV2Error(
            "actual parent-process measurement is Windows-only"
        )
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    query = 0x1000  # PROCESS_QUERY_LIMITED_INFORMATION
    parent_pid = os.getppid()
    kernel32.OpenProcess.argtypes = [
        ctypes.c_ulong,
        ctypes.c_int,
        ctypes.c_ulong,
    ]
    kernel32.OpenProcess.restype = ctypes.c_void_p
    handle = kernel32.OpenProcess(query, False, parent_pid)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        creation = ctypes.c_ulonglong()
        exit_time = ctypes.c_ulonglong()
        kernel = ctypes.c_ulonglong()
        user = ctypes.c_ulonglong()
        if not kernel32.GetProcessTimes(
            ctypes.c_void_p(handle),
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        size = ctypes.c_ulong(32768)
        buffer = ctypes.create_unicode_buffer(size.value)
        if not kernel32.QueryFullProcessImageNameW(
            ctypes.c_void_p(handle), 0, buffer, ctypes.byref(size)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        image = Path(buffer.value)
        stat = image.stat()
        executable_identity = _digest(
            {
                "normalized_path": os.path.normcase(os.fspath(image)),
                "st_dev": int(stat.st_dev),
                "st_ino": int(stat.st_ino),
                "size": int(stat.st_size),
                "mtime_ns": int(stat.st_mtime_ns),
            }
        )
        return {
            "pid": parent_pid,
            "start_token": f"windows-filetime:{creation.value}",
            "executable_identity": executable_identity,
        }
    finally:
        kernel32.CloseHandle(ctypes.c_void_p(handle))


_V1_TOP_KEYS = {
    "schema_version",
    "captured_at_utc",
    "measurement_status",
    "boot",
    "windows",
    "volume",
    "workspace",
    "model",
    "canonical_parent_count",
    "canonical_parents",
    "target_count",
    "targets",
    "sentinel_count",
    "sentinels",
    "process_snapshot",
    "open_measurement",
    "claims",
    "measurement_body_sha256",
}

_V1_OPEN_MEASUREMENT = {
    "target_mode": "exclusive_read",
    "sentinel_mode": "deny_write_and_delete",
    "all_targets_held_simultaneously": True,
    "all_sentinels_held_with_targets": True,
    "point_in_time_exclusive_open_checks_passed": True,
    "exclusive_open_target_count": 13,
    "sentinel_open_count": 3,
}

_V1_CLAIMS = {
    "read_only_measurement": True,
    "canonical_parent_probe_files_created": False,
    "directory_members_changed": False,
    "file_bytes_changed": False,
    "attempt_directories_created": False,
    "delete_or_replace_attempted": False,
    "restart_or_onedrive_mutation_attempted": False,
    "inventory_exhaustive": False,
    "open_checks_point_in_time_only": True,
    "future_or_preopened_writers_excluded": False,
    "power_loss_durability_claimed": False,
    "set_atomicity_claimed": False,
    "publication_authorized": False,
    "publication_attempted": False,
}

_V1_PROCESS_KEYS = {
    "collection_scope",
    "inventory_exhaustive",
    "inventory_caveat",
    "current_pid",
    "observed_process_count",
    "bounded_name_count",
    "bounded_names",
    "matched_process_count",
    "matched_processes",
    "python_process_count",
    "other_python_process_count",
    "sync_process_count",
    "onedrive_process_count",
    "onedrive_absent_in_bounded_snapshot",
}


def _validate_v1_digest(source: Mapping[str, Any]) -> None:
    expected = source["measurement_body_sha256"]
    _assert_sha(expected, "V1 measurement_body_sha256")
    body = dict(source)
    body.pop("measurement_body_sha256")
    if _digest(body) != expected:
        raise WindowsLiveEnvironmentV2Error("V1 measurement digest drift")


def _path_expectations(v1: Any, values: Sequence[Any]) -> list[Any]:
    return [
        v1.PathExpectation(
            logical_path=value.path_token,
            path=Path(value.path),
            expected_sha256=(
                value.preimage_sha256
                if isinstance(value, TargetExpectation)
                else value.expected_sha256
            ),
        )
        for value in values
    ]


def _parent_map(
    targets: Sequence[TargetExpectation],
    sentinels: Sequence[SentinelExpectation],
) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for value in (*targets, *sentinels):
        key = _path_key(Path(value.path).parent)
        pair = (value.parent_id, str(Path(value.path_token).parent).replace("\\", "/"))
        if key in result and result[key] != pair:
            raise WindowsLiveEnvironmentV2Error(
                "one canonical parent has conflicting ID or path token"
            )
        result[key] = pair
    return result


def collect_live_environment_measurement_v2(
    *,
    application_id: str,
    phase: str,
    gate_id: str,
    workspace_root: Path,
    workspace_path_token: str,
    model_root: Path,
    model_path_token: str,
    targets: Sequence[TargetExpectation],
    sentinels: Sequence[SentinelExpectation],
    backend: Any | None = None,
    clock: Clock | None = None,
    parent_process_provider: Callable[[], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Collect the exact V2 record; all effects are read-only observations."""
    if phase not in ("prepare", "publish"):
        raise WindowsLiveEnvironmentV2Error("phase must be prepare or publish")
    if len(targets) != 13 or len(sentinels) != 3:
        raise WindowsLiveEnvironmentV2Error("V9 requires exactly 13 + 3 files")
    if [row.ordinal for row in targets] != list(range(1, 14)):
        raise WindowsLiveEnvironmentV2Error("target ordinal/order drift")
    if [row.ordinal for row in sentinels] != list(range(1, 4)):
        raise WindowsLiveEnvironmentV2Error("sentinel ordinal/order drift")
    if len({row.target_id for row in targets}) != 13:
        raise WindowsLiveEnvironmentV2Error("target IDs must be unique")
    if len({row.path_token for row in targets}) != 13:
        raise WindowsLiveEnvironmentV2Error("target path tokens must be unique")
    for value in targets:
        _assert_sha(value.preimage_sha256, "target preimage")
        _assert_sha(value.staged_sha256, "target staged")
    for value in sentinels:
        _assert_sha(value.expected_sha256, "sentinel expected")

    if _sha256_file(CONTRACT_PATH) != CONTRACT_SHA256:
        raise WindowsLiveEnvironmentV2Error("V2 contract hash drift")
    policy = _load_module("t550_live_gate_policy_v2_adapter", POLICY_PATH)
    v1 = _load_module("t550_windows_measurement_v1_adapter", V1_PATH)
    selected_clock = clock or SystemClock()
    selected_backend = backend or v1.WindowsMeasurementBackend()
    timed_backend = _TimedBackend(selected_backend, selected_clock)
    parent_tokens = _parent_map(targets, sentinels)
    parent_paths: dict[str, Path] = {}
    for value in (*targets, *sentinels):
        key = _path_key(Path(value.path).parent)
        parent_paths[key] = Path(os.path.abspath(Path(value.path).parent))
    start_wall = selected_clock.now_utc()
    start_mono = selected_clock.monotonic_ns()
    parent_before: dict[str, tuple[Any, str]] = {}
    for key, parent in parent_paths.items():
        timed_backend.assert_no_reparse_chain(parent)
        identity = timed_backend.directory_identity(parent)
        normalized_identity = _object_identity(identity, directory=True)
        if normalized_identity["reparse_point"]:
            raise WindowsLiveEnvironmentV2Error(
                "canonical parent reparse identity rejected"
            )
        parent_before[key] = (
            identity,
            _member_digest(timed_backend.directory_members(parent)),
        )
    source = v1.collect_live_environment_measurement(
        workspace_root=workspace_root,
        model_root=model_root,
        targets=_path_expectations(v1, targets),
        sentinels=_path_expectations(v1, sentinels),
        bounded_process_names=policy.BOUNDED_PROCESS_NAMES,
        backend=timed_backend,
    )
    for key, parent in parent_paths.items():
        identity, members = parent_before[key]
        if timed_backend.directory_identity(parent) != identity:
            raise WindowsLiveEnvironmentV2Error(
                "canonical parent identity changed during measurement"
            )
        if _member_digest(timed_backend.directory_members(parent)) != members:
            raise WindowsLiveEnvironmentV2Error(
                "canonical parent membership changed during measurement"
            )
    end_wall = selected_clock.now_utc()
    end_mono = selected_clock.monotonic_ns()
    source = _keys(source, _V1_TOP_KEYS, "V1 measurement")
    _validate_v1_digest(source)
    if source["measurement_status"] != "PASS_POINT_IN_TIME_READ_ONLY":
        raise WindowsLiveEnvironmentV2Error("V1 measurement did not pass")
    if source["open_measurement"] != _V1_OPEN_MEASUREMENT:
        raise WindowsLiveEnvironmentV2Error("V1 held-open claims drift")
    if source["claims"] != _V1_CLAIMS:
        raise WindowsLiveEnvironmentV2Error("V1 effect claims drift")
    if (
        source["target_count"] != 13
        or source["sentinel_count"] != 3
    ):
        raise WindowsLiveEnvironmentV2Error("V1 exact count drift")

    volume_source = source["volume"]
    volume_serial = int(volume_source["volume_serial"])
    v1_parent_keys: set[str] = set()
    for raw in source["canonical_parents"]:
        key = _path_key(Path(raw["path"]))
        if key not in parent_tokens:
            raise WindowsLiveEnvironmentV2Error("unknown canonical parent")
        v1_parent_keys.add(key)
        if (
            raw["directory_members_unchanged"] is not True
            or raw["directory_members_before"] != raw["directory_members_after"]
        ):
            raise WindowsLiveEnvironmentV2Error(
                "canonical parent membership drift"
            )
        if _identity(raw["identity"], directory=True) != _object_identity(
            parent_before[key][0], directory=True
        ):
            raise WindowsLiveEnvironmentV2Error(
                "V1 canonical parent identity drift"
            )
    target_parent_keys = {
        _path_key(Path(value.path).parent) for value in targets
    }
    if v1_parent_keys != target_parent_keys:
        raise WindowsLiveEnvironmentV2Error(
            "V1 canonical target-parent set drift"
        )
    parents: list[dict[str, Any]] = []
    for key in sorted(parent_paths):
        parent_id, path_token = parent_tokens[key]
        parents.append(
            {
                "parent_id": parent_id,
                "path_token": path_token,
                "identity": _object_identity(
                    parent_before[key][0], directory=True
                ),
            }
        )
    parents.sort(key=lambda row: row["parent_id"])

    source_targets = source["targets"]
    target_rows: list[dict[str, Any]] = []
    for expected, raw in zip(targets, source_targets, strict=True):
        if raw["logical_path"] != expected.path_token:
            raise WindowsLiveEnvironmentV2Error("V1 target path-token drift")
        if raw["expected_sha256"] != expected.preimage_sha256:
            raise WindowsLiveEnvironmentV2Error("V1 target preimage drift")
        observed = raw["measured"]
        open_time = timed_backend.open_observations.get(_path_key(expected.path))
        if open_time is None:
            raise WindowsLiveEnvironmentV2Error("target open timestamp missing")
        target_rows.append(
            {
                "ordinal": expected.ordinal,
                "target_id": expected.target_id,
                "role": expected.role,
                "path_token": expected.path_token,
                "parent_id": expected.parent_id,
                "identity": _identity(observed["identity"], directory=False),
                "size_bytes": int(observed["size_bytes"]),
                "expected_preimage_sha256": expected.preimage_sha256,
                "expected_staged_sha256": expected.staged_sha256,
                "observed_sha256": observed["sha256"],
                "regular_file": True,
                "reparse_point": False,
                "exclusive_open_succeeded": bool(
                    raw["exclusive_open_capability"]
                ),
                "open_wall_time_utc": open_time[0],
                "open_monotonic_ns": open_time[1],
            }
        )

    sentinel_rows: list[dict[str, Any]] = []
    for expected, raw in zip(sentinels, source["sentinels"], strict=True):
        if raw["logical_path"] != expected.path_token:
            raise WindowsLiveEnvironmentV2Error("V1 sentinel path-token drift")
        if raw["expected_sha256"] != expected.expected_sha256:
            raise WindowsLiveEnvironmentV2Error("V1 sentinel hash drift")
        observed = raw["measured"]
        open_time = timed_backend.open_observations.get(_path_key(expected.path))
        if open_time is None:
            raise WindowsLiveEnvironmentV2Error("sentinel open timestamp missing")
        sentinel_rows.append(
            {
                "ordinal": expected.ordinal,
                "sentinel_id": expected.sentinel_id,
                "role": expected.role,
                "path_token": expected.path_token,
                "parent_id": expected.parent_id,
                "identity": _identity(observed["identity"], directory=False),
                "size_bytes": int(observed["size_bytes"]),
                "expected_sha256": expected.expected_sha256,
                "observed_sha256": observed["sha256"],
                "regular_file": True,
                "reparse_point": False,
                "deny_write_delete_open_succeeded": bool(
                    raw["deny_write_delete_open_capability"]
                ),
                "open_wall_time_utc": open_time[0],
                "open_monotonic_ns": open_time[1],
            }
        )

    process_source = _keys(
        source["process_snapshot"], _V1_PROCESS_KEYS, "V1 process_snapshot"
    )
    expected_process_names = sorted(policy.BOUNDED_PROCESS_NAMES)
    if (
        process_source["collection_scope"]
        != "bounded_process_name_and_pid_snapshot"
        or process_source["inventory_exhaustive"] is not False
        or process_source["bounded_names"] != expected_process_names
        or process_source["bounded_name_count"] != len(expected_process_names)
        or process_source["matched_process_count"]
        != len(process_source["matched_processes"])
    ):
        raise WindowsLiveEnvironmentV2Error("V1 process policy drift")
    matched = []
    in_scope = []
    onedrive = []
    for raw in process_source["matched_processes"]:
        classifications = sorted(raw["classifications"])
        item = {
            "pid": int(raw["pid"]),
            "name": str(raw["name"]).casefold(),
            "classification": "+".join(classifications) or "bounded_other",
            "is_current_process": bool(raw["is_current_process"]),
        }
        matched.append(item)
        if "onedrive" in classifications:
            onedrive.append(item)
        if not item["is_current_process"]:
            in_scope.append(item)

    parent_provider = parent_process_provider or _default_parent_process_facts
    parent_process = dict(parent_provider())
    _keys(
        parent_process,
        {"pid", "start_token", "executable_identity"},
        "parent_process",
    )
    body = {
        "schema_version": policy.MEASUREMENT_SCHEMA_VERSION,
        "gate_id": gate_id,
        "task_id": "T550",
        "book": "Hos",
        "application_id": application_id,
        "phase": phase,
        "capture": {
            "start_wall_time_utc": _iso(start_wall),
            "end_wall_time_utc": _iso(end_wall),
            "start_monotonic_ns": start_mono,
            "end_monotonic_ns": end_mono,
            "max_duration_seconds": policy.MAX_LEASE_SECONDS,
        },
        "boot": {
            "boot_identity": source["boot"]["boot_identity_sha256"],
            "boot_time_utc": source["boot"]["boot_time_utc"],
        },
        "operating_system": {
            "name": "Windows",
            "version": (
                f"{source['windows']['major_version']}."
                f"{source['windows']['minor_version']}"
            ),
            "build": str(source["windows"]["build_number"]),
            "architecture": (
                f"{source['windows']['native_architecture']}/"
                f"{source['windows']['python_architecture']}"
            ),
        },
        "volume": {
            "volume_guid": str(volume_source["volume_guid"]),
            "volume_serial": volume_serial,
            "filesystem": str(volume_source["filesystem_name"]),
            "filesystem_flags": [
                str(volume_source["filesystem_flags_hex"]),
                f"max_component:{volume_source['maximum_component_length']}",
            ],
        },
        "workspace": {
            "path_token": workspace_path_token,
            "identity": _identity(source["workspace"]["identity"], directory=True),
        },
        "model": {
            "path_token": model_path_token,
            "identity": _identity(source["model"]["identity"], directory=True),
        },
        "canonical_parents": parents,
        "parent_process": parent_process,
        "targets": target_rows,
        "sentinels": sentinel_rows,
        "process_policy": {
            "names": list(policy.BOUNDED_PROCESS_NAMES),
            "sha256": policy.process_policy_sha256(),
        },
        "process_snapshot": {
            "inventory_exhaustive": False,
            "current_process_id": int(process_source["current_pid"]),
            "observed_process_count": int(
                process_source["observed_process_count"]
            ),
            "matched_processes": matched,
            "onedrive_matches": onedrive,
            "in_scope_writer_matches": in_scope,
            "observer_limitations_acknowledged": True,
        },
        "effects": {
            "read_only_measurement": True,
            "probe_files_created": False,
            "directory_members_changed": False,
            "file_bytes_changed": False,
            "delete_or_replace_attempted": False,
            "attempt_created": False,
            "restart_or_onedrive_action_attempted": False,
            "publication_attempted": False,
        },
        "residual_races": {
            "bounded_inventory_not_exhaustive": True,
            "future_or_preopened_writers_excluded": False,
            "lost_update_before_rename_possible": True,
            "overwrite_after_readback_possible": True,
            "process_crash_recovery_only": True,
            "power_loss_durability_claimed": False,
            "thirteen_file_set_atomicity_claimed": False,
            "global_sidecar_install_authorized": False,
        },
        "candidate_only": True,
        "non_authorizing": True,
    }
    # A direct policy call is the adapter-to-policy compatibility gate.  The
    # caller supplies frozen expectations and current validation clocks later;
    # here we guarantee only that the raw schema can be canonicalized.
    _canonical_bytes(body)
    return body


collect_live_environment_measurement = collect_live_environment_measurement_v2
