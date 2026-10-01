#!/usr/bin/env python3
"""Read-only, environment-bound Windows publication measurements.

This module measures facts needed by the T550 V9 external environment gate.
It never prepares, publishes, replaces, deletes, creates a probe, or changes
OneDrive or restart state.  The default backend is Windows-only.  A backend
may be injected so the policy layer can be tested without depending on a live
machine.

The result is deliberately modest evidence:

* process inventory is a bounded, point-in-time name/PID snapshot and is
  always labelled ``inventory_exhaustive=false``;
* open checks prove only that the requested read-only sharing modes could be
  held together at the sampled instant;
* no claim is made about future writers, pre-opened handles, power-loss
  durability, or atomicity of a multi-file set.
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import platform
import sys
from contextlib import AbstractContextManager, ExitStack
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence


SCHEMA_VERSION = "windows_live_environment_measurement.v1"
EXACT_TARGET_COUNT = 13
EXACT_SENTINEL_COUNT = 3

TARGET_OPEN_MODE = "exclusive_read"
SENTINEL_OPEN_MODE = "deny_write_and_delete"

DEFAULT_BOUNDED_PROCESS_NAMES = frozenset(
    {
        "python.exe",
        "pythonw.exe",
        "py.exe",
        "onedrive.exe",
        "onedrivestandaloneupdater.exe",
        "dropbox.exe",
        "googledrivefs.exe",
        "box.exe",
        "boxdrive.exe",
        "iclouddrive.exe",
        "syncthing.exe",
        "robocopy.exe",
        "rsync.exe",
    }
)
PYTHON_PROCESS_NAMES = frozenset({"python.exe", "pythonw.exe", "py.exe"})
SYNC_PROCESS_NAMES = frozenset(
    {
        "onedrive.exe",
        "onedrivestandaloneupdater.exe",
        "dropbox.exe",
        "googledrivefs.exe",
        "box.exe",
        "boxdrive.exe",
        "iclouddrive.exe",
        "syncthing.exe",
    }
)


class LiveEnvironmentMeasurementError(RuntimeError):
    """Base class for fail-closed measurement errors."""


class UnsupportedPlatform(LiveEnvironmentMeasurementError):
    """The real backend was requested on a non-Windows platform."""


class CountMismatch(LiveEnvironmentMeasurementError):
    """The caller did not provide the exact governed file set."""


class ContainmentViolation(LiveEnvironmentMeasurementError):
    """A requested path was not contained by its declared root."""


class ReparsePointRejected(LiveEnvironmentMeasurementError):
    """A root, parent, target, or sentinel used a reparse component."""


class IdentityMismatch(LiveEnvironmentMeasurementError):
    """A path identity changed or aliased another governed path."""


class HashMismatch(LiveEnvironmentMeasurementError):
    """A measured file hash did not match its expected or held value."""


class DirectoryMembershipChanged(LiveEnvironmentMeasurementError):
    """A canonical parent gained or lost an entry during measurement."""


class FilesystemRejected(LiveEnvironmentMeasurementError):
    """The live volume is not the required NTFS environment."""


@dataclass(frozen=True)
class ObjectIdentity:
    """Stable-by-handle identity fields used during one measurement."""

    volume_serial: int
    file_id: int
    attributes: int
    is_directory: bool
    is_reparse_point: bool

    def key(self) -> tuple[int, int]:
        return self.volume_serial, self.file_id


@dataclass(frozen=True)
class FileSnapshot:
    """Identity and exact byte digest from one held file handle."""

    identity: ObjectIdentity
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class PathExpectation:
    """One exact logical file and the bytes expected before publication."""

    logical_path: str
    path: Path
    expected_sha256: str


@dataclass(frozen=True)
class ProcessObservation:
    pid: int
    name: str


class HeldRegularFile(Protocol):
    """Read-only handle retained by a backend during the open check."""

    def snapshot(self) -> FileSnapshot:
        """Return identity and bytes through the retained handle."""


class MeasurementBackend(Protocol):
    """Injectable operating-system measurement boundary."""

    current_pid: int

    def now_utc(self) -> datetime:
        ...

    def boot_facts(self) -> Mapping[str, Any]:
        ...

    def os_facts(self) -> Mapping[str, Any]:
        ...

    def volume_facts(self, path: Path) -> Mapping[str, Any]:
        ...

    def assert_no_reparse_chain(self, path: Path) -> None:
        ...

    def directory_identity(self, path: Path) -> ObjectIdentity:
        ...

    def directory_members(self, path: Path) -> Sequence[str]:
        ...

    def snapshot_regular_file(self, path: Path) -> FileSnapshot:
        ...

    def hold_regular_file(
        self, path: Path, mode: str
    ) -> AbstractContextManager[HeldRegularFile]:
        ...

    def list_processes(self) -> Sequence[ProcessObservation]:
        ...


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _identity_dict(value: ObjectIdentity) -> dict[str, Any]:
    return asdict(value)


def _snapshot_dict(value: FileSnapshot) -> dict[str, Any]:
    return {
        "identity": _identity_dict(value.identity),
        "sha256": value.sha256,
        "size_bytes": value.size_bytes,
    }


def _validate_sha256(value: str, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise HashMismatch(f"{label} is not a lowercase SHA-256 digest")
    return value


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _path_key(path: Path) -> str:
    return os.path.normcase(os.fspath(_absolute(path)))


def _require_contained(path: Path, root: Path, label: str) -> None:
    absolute_path = _absolute(path)
    absolute_root = _absolute(root)
    try:
        common = Path(os.path.commonpath([absolute_path, absolute_root]))
    except ValueError as exc:
        raise ContainmentViolation(f"{label} is on a different volume") from exc
    if _path_key(common) != _path_key(absolute_root):
        raise ContainmentViolation(f"{label} escapes its declared root")


def _member_digest(names: Sequence[str]) -> dict[str, Any]:
    ordered = sorted(str(name) for name in names)
    if len(ordered) != len(set(ordered)):
        raise IdentityMismatch("directory member enumeration contains duplicates")
    return {
        "member_count": len(ordered),
        "member_names_sha256": _sha256_bytes(_canonical_json_bytes(ordered)),
    }


def _require_same_snapshot(
    before: FileSnapshot,
    after: FileSnapshot,
    label: str,
) -> None:
    if before.identity != after.identity:
        raise IdentityMismatch(f"{label} identity changed during measurement")
    if (
        before.sha256 != after.sha256
        or before.size_bytes != after.size_bytes
    ):
        raise HashMismatch(f"{label} bytes changed during measurement")


def _classify_process(name: str) -> tuple[str, ...]:
    lowered = name.casefold()
    values: list[str] = []
    if lowered in PYTHON_PROCESS_NAMES:
        values.append("python")
    if lowered.startswith("onedrive") and lowered.endswith(".exe"):
        values.extend(("onedrive", "sync"))
    elif lowered in SYNC_PROCESS_NAMES:
        values.append("sync")
    if lowered in {"robocopy.exe", "rsync.exe"}:
        values.append("copy_or_writer")
    return tuple(values)


def _process_measurement(
    processes: Sequence[ProcessObservation],
    *,
    current_pid: int,
    bounded_process_names: Sequence[str],
) -> dict[str, Any]:
    bounded = {name.casefold() for name in bounded_process_names}
    if not bounded:
        raise LiveEnvironmentMeasurementError(
            "bounded process-name set may not be empty"
        )
    seen_pids: set[int] = set()
    matches: list[dict[str, Any]] = []
    observed_count = 0
    for process in processes:
        observed_count += 1
        if (
            not isinstance(process.pid, int)
            or process.pid < 0
            or not isinstance(process.name, str)
            or not process.name
        ):
            raise LiveEnvironmentMeasurementError(
                "process snapshot contains an invalid name or PID"
            )
        if process.pid in seen_pids:
            raise LiveEnvironmentMeasurementError(
                "process snapshot contains a duplicate PID"
            )
        seen_pids.add(process.pid)
        lowered = process.name.casefold()
        if lowered in bounded or (
            lowered.startswith("onedrive") and lowered.endswith(".exe")
        ):
            classifications = _classify_process(process.name)
            matches.append(
                {
                    "pid": process.pid,
                    "name": process.name,
                    "is_current_process": process.pid == current_pid,
                    "classifications": list(classifications),
                }
            )
    matches.sort(key=lambda item: (item["name"].casefold(), item["pid"]))
    onedrive = [
        row for row in matches if "onedrive" in row["classifications"]
    ]
    python = [row for row in matches if "python" in row["classifications"]]
    other_python = [row for row in python if not row["is_current_process"]]
    sync = [row for row in matches if "sync" in row["classifications"]]
    return {
        "collection_scope": "bounded_process_name_and_pid_snapshot",
        "inventory_exhaustive": False,
        "inventory_caveat": (
            "The name/PID snapshot is point-in-time and does not enumerate "
            "all open handles, resident code, kernel writers, future "
            "processes, or hidden/protected activity."
        ),
        "current_pid": current_pid,
        "observed_process_count": observed_count,
        "bounded_name_count": len(bounded),
        "bounded_names": sorted(bounded),
        "matched_process_count": len(matches),
        "matched_processes": matches,
        "python_process_count": len(python),
        "other_python_process_count": len(other_python),
        "sync_process_count": len(sync),
        "onedrive_process_count": len(onedrive),
        "onedrive_absent_in_bounded_snapshot": not onedrive,
    }


def _prepare_expectations(
    values: Sequence[PathExpectation],
    *,
    expected_count: int,
    root: Path,
    label: str,
) -> list[PathExpectation]:
    if len(values) != expected_count:
        raise CountMismatch(
            f"{label} count {len(values)} does not equal {expected_count}"
        )
    logical_seen: set[str] = set()
    path_seen: set[str] = set()
    result: list[PathExpectation] = []
    for value in values:
        if not isinstance(value, PathExpectation):
            raise CountMismatch(f"{label} entry is not a PathExpectation")
        if (
            not value.logical_path
            or value.logical_path.startswith(("/", "\\"))
            or ".." in Path(value.logical_path).parts
        ):
            raise ContainmentViolation(
                f"{label} logical path is not a safe relative path"
            )
        expected = _validate_sha256(
            value.expected_sha256, f"{label} {value.logical_path}"
        )
        path = _absolute(value.path)
        _require_contained(path, root, f"{label} {value.logical_path}")
        logical_key = value.logical_path.replace("\\", "/").casefold()
        path_key = _path_key(path)
        if logical_key in logical_seen or path_key in path_seen:
            raise CountMismatch(f"{label} entries must be distinct")
        logical_seen.add(logical_key)
        path_seen.add(path_key)
        result.append(
            PathExpectation(
                logical_path=value.logical_path.replace("\\", "/"),
                path=path,
                expected_sha256=expected,
            )
        )
    return result


def collect_live_environment_measurement(
    *,
    workspace_root: Path,
    model_root: Path,
    targets: Sequence[PathExpectation],
    sentinels: Sequence[PathExpectation],
    backend: MeasurementBackend | None = None,
    bounded_process_names: Sequence[str] = tuple(
        sorted(DEFAULT_BOUNDED_PROCESS_NAMES)
    ),
) -> dict[str, Any]:
    """Collect one fail-closed, read-only V9 live-environment measurement.

    Exactly 13 target and three sentinel expectations are required.  All
    governed files must be regular, non-reparse files below ``model_root``.
    Workspace, model, and each distinct canonical target parent are sampled
    by identity before and during the held-handle check.  The function creates
    no directory members and modifies no file bytes.
    """

    selected: MeasurementBackend
    if backend is None:
        selected = WindowsMeasurementBackend()
    else:
        selected = backend

    workspace = _absolute(workspace_root)
    model = _absolute(model_root)
    _require_contained(model, workspace, "model root")
    prepared_targets = _prepare_expectations(
        targets,
        expected_count=EXACT_TARGET_COUNT,
        root=model,
        label="target",
    )
    prepared_sentinels = _prepare_expectations(
        sentinels,
        expected_count=EXACT_SENTINEL_COUNT,
        root=model,
        label="sentinel",
    )
    all_file_keys = {
        _path_key(value.path)
        for value in (*prepared_targets, *prepared_sentinels)
    }
    if len(all_file_keys) != EXACT_TARGET_COUNT + EXACT_SENTINEL_COUNT:
        raise CountMismatch("target and sentinel file sets overlap")

    parent_by_key = {
        _path_key(value.path.parent): _absolute(value.path.parent)
        for value in prepared_targets
    }
    parents = [
        parent_by_key[key]
        for key in sorted(parent_by_key)
    ]
    if not parents:
        raise CountMismatch("at least one canonical target parent is required")

    for path in (workspace, model, *parents):
        selected.assert_no_reparse_chain(path)
    for value in (*prepared_targets, *prepared_sentinels):
        selected.assert_no_reparse_chain(value.path)

    workspace_identity = selected.directory_identity(workspace)
    model_identity = selected.directory_identity(model)
    if not workspace_identity.is_directory or not model_identity.is_directory:
        raise IdentityMismatch("workspace and model roots must be directories")
    if (
        workspace_identity.is_reparse_point
        or model_identity.is_reparse_point
    ):
        raise ReparsePointRejected("workspace or model root is a reparse point")

    parent_identities: dict[Path, ObjectIdentity] = {}
    parent_members_before: dict[Path, dict[str, Any]] = {}
    for parent in parents:
        identity = selected.directory_identity(parent)
        if not identity.is_directory:
            raise IdentityMismatch("canonical parent is not a directory")
        if identity.is_reparse_point:
            raise ReparsePointRejected(
                f"canonical parent is a reparse point: {parent}"
            )
        parent_identities[parent] = identity
        parent_members_before[parent] = _member_digest(
            selected.directory_members(parent)
        )
    parent_keys = [identity.key() for identity in parent_identities.values()]
    if len(parent_keys) != len(set(parent_keys)):
        raise IdentityMismatch(
            "distinct canonical parent paths alias one directory identity"
        )

    volume = dict(selected.volume_facts(workspace))
    filesystem_name = str(volume.get("filesystem_name", ""))
    if filesystem_name.casefold() != "ntfs":
        raise FilesystemRejected(
            f"live workspace filesystem is not NTFS: {filesystem_name!r}"
        )
    volume_serial = volume.get("volume_serial")
    if not isinstance(volume_serial, int):
        raise FilesystemRejected("volume serial is missing or invalid")
    for label, identity in (
        ("workspace", workspace_identity),
        ("model", model_identity),
        *(
            (f"canonical parent {parent}", identity)
            for parent, identity in parent_identities.items()
        ),
    ):
        if identity.volume_serial != volume_serial:
            raise IdentityMismatch(f"{label} is not on the measured volume")

    target_before: dict[str, FileSnapshot] = {}
    sentinel_before: dict[str, FileSnapshot] = {}
    for value, destination in (
        *((value, target_before) for value in prepared_targets),
        *((value, sentinel_before) for value in prepared_sentinels),
    ):
        snapshot = selected.snapshot_regular_file(value.path)
        if snapshot.identity.is_directory:
            raise IdentityMismatch(
                f"regular file expected: {value.logical_path}"
            )
        if snapshot.identity.is_reparse_point:
            raise ReparsePointRejected(
                f"file is a reparse point: {value.logical_path}"
            )
        if snapshot.identity.volume_serial != volume_serial:
            raise IdentityMismatch(
                f"file is not on measured volume: {value.logical_path}"
            )
        if snapshot.sha256 != value.expected_sha256:
            raise HashMismatch(
                f"preimage hash mismatch: {value.logical_path}"
            )
        destination[value.logical_path] = snapshot
    file_identity_keys = [
        snapshot.identity.key()
        for snapshot in (*target_before.values(), *sentinel_before.values())
    ]
    if len(file_identity_keys) != len(set(file_identity_keys)):
        raise IdentityMismatch(
            "target or sentinel paths alias a governed file identity"
        )

    processes = _process_measurement(
        selected.list_processes(),
        current_pid=selected.current_pid,
        bounded_process_names=bounded_process_names,
    )
    captured_at = selected.now_utc()
    if captured_at.tzinfo is None:
        raise LiveEnvironmentMeasurementError(
            "measurement clock returned a timezone-naive value"
        )

    held_target_snapshots: dict[str, FileSnapshot] = {}
    held_sentinel_snapshots: dict[str, FileSnapshot] = {}
    held_target_handles: dict[str, HeldRegularFile] = {}
    held_sentinel_handles: dict[str, HeldRegularFile] = {}
    with ExitStack() as stack:
        for value in prepared_targets:
            held = stack.enter_context(
                selected.hold_regular_file(value.path, TARGET_OPEN_MODE)
            )
            snapshot = held.snapshot()
            _require_same_snapshot(
                target_before[value.logical_path],
                snapshot,
                f"target {value.logical_path}",
            )
            held_target_snapshots[value.logical_path] = snapshot
            held_target_handles[value.logical_path] = held
        for value in prepared_sentinels:
            held = stack.enter_context(
                selected.hold_regular_file(value.path, SENTINEL_OPEN_MODE)
            )
            snapshot = held.snapshot()
            _require_same_snapshot(
                sentinel_before[value.logical_path],
                snapshot,
                f"sentinel {value.logical_path}",
            )
            held_sentinel_snapshots[value.logical_path] = snapshot
            held_sentinel_handles[value.logical_path] = held

        if selected.directory_identity(workspace) != workspace_identity:
            raise IdentityMismatch(
                "workspace identity changed during held-open measurement"
            )
        if selected.directory_identity(model) != model_identity:
            raise IdentityMismatch(
                "model identity changed during held-open measurement"
            )
        for parent in parents:
            if selected.directory_identity(parent) != parent_identities[parent]:
                raise IdentityMismatch(
                    f"canonical parent identity changed: {parent}"
                )
            current_members = _member_digest(
                selected.directory_members(parent)
            )
            if current_members != parent_members_before[parent]:
                raise DirectoryMembershipChanged(
                    f"canonical parent membership changed: {parent}"
                )
        for logical_path, initial, held in (
            *(
                (
                    logical_path,
                    held_target_snapshots[logical_path],
                    handle,
                )
                for logical_path, handle in held_target_handles.items()
            ),
            *(
                (
                    logical_path,
                    held_sentinel_snapshots[logical_path],
                    handle,
                )
                for logical_path, handle in held_sentinel_handles.items()
            ),
        ):
            _require_same_snapshot(
                initial,
                held.snapshot(),
                f"held file {logical_path}",
            )

    for value in prepared_targets:
        after = selected.snapshot_regular_file(value.path)
        _require_same_snapshot(
            target_before[value.logical_path],
            after,
            f"target {value.logical_path}",
        )
    for value in prepared_sentinels:
        after = selected.snapshot_regular_file(value.path)
        _require_same_snapshot(
            sentinel_before[value.logical_path],
            after,
            f"sentinel {value.logical_path}",
        )
    if selected.directory_identity(workspace) != workspace_identity:
        raise IdentityMismatch("workspace identity changed after open check")
    if selected.directory_identity(model) != model_identity:
        raise IdentityMismatch("model identity changed after open check")
    parent_rows: list[dict[str, Any]] = []
    for parent in parents:
        if selected.directory_identity(parent) != parent_identities[parent]:
            raise IdentityMismatch(
                f"canonical parent identity changed after open check: {parent}"
            )
        after_members = _member_digest(selected.directory_members(parent))
        if after_members != parent_members_before[parent]:
            raise DirectoryMembershipChanged(
                f"canonical parent membership changed after open check: {parent}"
            )
        parent_rows.append(
            {
                "path": os.fspath(parent),
                "identity": _identity_dict(parent_identities[parent]),
                "directory_members_before": parent_members_before[parent],
                "directory_members_after": after_members,
                "directory_members_unchanged": True,
            }
        )

    target_rows = [
        {
            "ordinal": index,
            "logical_path": value.logical_path,
            "path": os.fspath(value.path),
            "expected_sha256": value.expected_sha256,
            "measured": _snapshot_dict(target_before[value.logical_path]),
            "exclusive_open_capability": True,
            "unchanged_before_during_after": True,
        }
        for index, value in enumerate(prepared_targets, 1)
    ]
    sentinel_rows = [
        {
            "ordinal": index,
            "logical_path": value.logical_path,
            "path": os.fspath(value.path),
            "expected_sha256": value.expected_sha256,
            "measured": _snapshot_dict(sentinel_before[value.logical_path]),
            "deny_write_delete_open_capability": True,
            "unchanged_before_during_after": True,
        }
        for index, value in enumerate(prepared_sentinels, 1)
    ]
    boot = dict(selected.boot_facts())
    os_measurement = dict(selected.os_facts())
    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "captured_at_utc": captured_at.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "measurement_status": "PASS_POINT_IN_TIME_READ_ONLY",
        "boot": boot,
        "windows": os_measurement,
        "volume": volume,
        "workspace": {
            "path": os.fspath(workspace),
            "identity": _identity_dict(workspace_identity),
        },
        "model": {
            "path": os.fspath(model),
            "identity": _identity_dict(model_identity),
        },
        "canonical_parent_count": len(parent_rows),
        "canonical_parents": parent_rows,
        "target_count": len(target_rows),
        "targets": target_rows,
        "sentinel_count": len(sentinel_rows),
        "sentinels": sentinel_rows,
        "process_snapshot": processes,
        "open_measurement": {
            "target_mode": TARGET_OPEN_MODE,
            "sentinel_mode": SENTINEL_OPEN_MODE,
            "all_targets_held_simultaneously": True,
            "all_sentinels_held_with_targets": True,
            "point_in_time_exclusive_open_checks_passed": True,
            "exclusive_open_target_count": EXACT_TARGET_COUNT,
            "sentinel_open_count": EXACT_SENTINEL_COUNT,
        },
        "claims": {
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
        },
    }
    body["measurement_body_sha256"] = _sha256_bytes(
        _canonical_json_bytes(body)
    )
    return body


class _WindowsApi:
    """Lazy ctypes declarations for the real Windows-only backend."""

    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    GENERIC_READ = 0x80000000
    FILE_READ_ATTRIBUTES = 0x00000080
    SYNCHRONIZE = 0x00100000

    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004

    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_DIRECTORY = 0x00000010
    FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000

    TH32CS_SNAPPROCESS = 0x00000002
    MAX_PATH = 260

    class BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("dwFileAttributes", ctypes.c_ulong),
            ("ftCreationTimeLow", ctypes.c_ulong),
            ("ftCreationTimeHigh", ctypes.c_ulong),
            ("ftLastAccessTimeLow", ctypes.c_ulong),
            ("ftLastAccessTimeHigh", ctypes.c_ulong),
            ("ftLastWriteTimeLow", ctypes.c_ulong),
            ("ftLastWriteTimeHigh", ctypes.c_ulong),
            ("dwVolumeSerialNumber", ctypes.c_ulong),
            ("nFileSizeHigh", ctypes.c_ulong),
            ("nFileSizeLow", ctypes.c_ulong),
            ("nNumberOfLinks", ctypes.c_ulong),
            ("nFileIndexHigh", ctypes.c_ulong),
            ("nFileIndexLow", ctypes.c_ulong),
        ]

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.c_ulong),
            ("cntUsage", ctypes.c_ulong),
            ("th32ProcessID", ctypes.c_ulong),
            ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
            ("th32ModuleID", ctypes.c_ulong),
            ("cntThreads", ctypes.c_ulong),
            ("th32ParentProcessID", ctypes.c_ulong),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", ctypes.c_ulong),
            ("szExeFile", ctypes.c_wchar * 260),
        ]

    class RTL_OSVERSIONINFOW(ctypes.Structure):
        _fields_ = [
            ("dwOSVersionInfoSize", ctypes.c_ulong),
            ("dwMajorVersion", ctypes.c_ulong),
            ("dwMinorVersion", ctypes.c_ulong),
            ("dwBuildNumber", ctypes.c_ulong),
            ("dwPlatformId", ctypes.c_ulong),
            ("szCSDVersion", ctypes.c_wchar * 128),
        ]

    class SYSTEM_TIMEOFDAY_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BootTime", ctypes.c_longlong),
            ("CurrentTime", ctypes.c_longlong),
            ("TimeZoneBias", ctypes.c_longlong),
            ("CurrentTimeZoneId", ctypes.c_ulong),
            ("Reserved", ctypes.c_ulong),
            ("BootTimeBias", ctypes.c_ulonglong),
            ("SleepTimeBias", ctypes.c_ulonglong),
        ]

    def __init__(self) -> None:
        if sys.platform != "win32":
            raise UnsupportedPlatform(
                "the live measurement backend requires Windows"
            )
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.ntdll = ctypes.WinDLL("ntdll")

        self.kernel32.CreateFileW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.c_void_p,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.c_void_p,
        ]
        self.kernel32.CreateFileW.restype = ctypes.c_void_p
        self.kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        self.kernel32.CloseHandle.restype = ctypes.c_int
        self.kernel32.GetFileInformationByHandle.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(self.BY_HANDLE_FILE_INFORMATION),
        ]
        self.kernel32.GetFileInformationByHandle.restype = ctypes.c_int
        self.kernel32.GetFileSizeEx.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_longlong),
        ]
        self.kernel32.GetFileSizeEx.restype = ctypes.c_int
        self.kernel32.SetFilePointerEx.argtypes = [
            ctypes.c_void_p,
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.c_ulong,
        ]
        self.kernel32.SetFilePointerEx.restype = ctypes.c_int
        self.kernel32.ReadFile.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.c_void_p,
        ]
        self.kernel32.ReadFile.restype = ctypes.c_int
        self.kernel32.GetFileAttributesW.argtypes = [ctypes.c_wchar_p]
        self.kernel32.GetFileAttributesW.restype = ctypes.c_ulong
        self.kernel32.GetVolumePathNameW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_ulong,
        ]
        self.kernel32.GetVolumePathNameW.restype = ctypes.c_int
        self.kernel32.GetVolumeNameForVolumeMountPointW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_ulong,
        ]
        self.kernel32.GetVolumeNameForVolumeMountPointW.restype = ctypes.c_int
        self.kernel32.GetVolumeInformationW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.c_wchar_p,
            ctypes.c_ulong,
        ]
        self.kernel32.GetVolumeInformationW.restype = ctypes.c_int
        self.kernel32.CreateToolhelp32Snapshot.argtypes = [
            ctypes.c_ulong,
            ctypes.c_ulong,
        ]
        self.kernel32.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
        self.kernel32.Process32FirstW.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(self.PROCESSENTRY32W),
        ]
        self.kernel32.Process32FirstW.restype = ctypes.c_int
        self.kernel32.Process32NextW.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(self.PROCESSENTRY32W),
        ]
        self.kernel32.Process32NextW.restype = ctypes.c_int
        self.ntdll.RtlGetVersion.argtypes = [
            ctypes.POINTER(self.RTL_OSVERSIONINFOW)
        ]
        self.ntdll.RtlGetVersion.restype = ctypes.c_long
        self.ntdll.NtQuerySystemInformation.argtypes = [
            ctypes.c_ulong,
            ctypes.c_void_p,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong),
        ]
        self.ntdll.NtQuerySystemInformation.restype = ctypes.c_long

    def winerror(self, label: str) -> OSError:
        return ctypes.WinError(ctypes.get_last_error(), label)

    def close(self, handle: int | None) -> None:
        if handle not in (None, 0, self.INVALID_HANDLE_VALUE):
            if not self.kernel32.CloseHandle(ctypes.c_void_p(handle)):
                raise self.winerror("CloseHandle")

    def open_path(self, path: Path, *, directory: bool, share: int) -> int:
        flags = self.FILE_FLAG_OPEN_REPARSE_POINT
        if directory:
            flags |= self.FILE_FLAG_BACKUP_SEMANTICS
        raw = self.kernel32.CreateFileW(
            os.fspath(path),
            self.GENERIC_READ | self.FILE_READ_ATTRIBUTES | self.SYNCHRONIZE,
            share,
            None,
            self.OPEN_EXISTING,
            flags,
            None,
        )
        value = ctypes.cast(raw, ctypes.c_void_p).value
        if value == self.INVALID_HANDLE_VALUE:
            raise self.winerror(f"CreateFileW({path})")
        return int(value)

    def identity(self, handle: int) -> ObjectIdentity:
        info = self.BY_HANDLE_FILE_INFORMATION()
        if not self.kernel32.GetFileInformationByHandle(
            ctypes.c_void_p(handle), ctypes.byref(info)
        ):
            raise self.winerror("GetFileInformationByHandle")
        attributes = int(info.dwFileAttributes)
        return ObjectIdentity(
            volume_serial=int(info.dwVolumeSerialNumber),
            file_id=(int(info.nFileIndexHigh) << 32)
            | int(info.nFileIndexLow),
            attributes=attributes,
            is_directory=bool(attributes & self.FILE_ATTRIBUTE_DIRECTORY),
            is_reparse_point=bool(
                attributes & self.FILE_ATTRIBUTE_REPARSE_POINT
            ),
        )

    def snapshot(self, handle: int) -> FileSnapshot:
        identity = self.identity(handle)
        if identity.is_directory:
            raise IdentityMismatch("regular file handle names a directory")
        if identity.is_reparse_point:
            raise ReparsePointRejected("regular file is a reparse point")
        size = ctypes.c_longlong()
        if not self.kernel32.GetFileSizeEx(
            ctypes.c_void_p(handle), ctypes.byref(size)
        ):
            raise self.winerror("GetFileSizeEx")
        if size.value < 0:
            raise IdentityMismatch("regular file reports a negative size")
        if not self.kernel32.SetFilePointerEx(
            ctypes.c_void_p(handle), 0, None, 0
        ):
            raise self.winerror("SetFilePointerEx")
        digest = hashlib.sha256()
        remaining = int(size.value)
        while remaining:
            requested = min(remaining, 1024 * 1024)
            buffer = ctypes.create_string_buffer(requested)
            count = ctypes.c_ulong()
            if not self.kernel32.ReadFile(
                ctypes.c_void_p(handle),
                buffer,
                requested,
                ctypes.byref(count),
                None,
            ):
                raise self.winerror("ReadFile")
            if count.value == 0:
                raise HashMismatch("short read from regular file handle")
            digest.update(buffer.raw[: count.value])
            remaining -= int(count.value)
        return FileSnapshot(
            identity=identity,
            sha256=digest.hexdigest(),
            size_bytes=int(size.value),
        )


class _WindowsHeldRegularFile(
    AbstractContextManager["_WindowsHeldRegularFile"]
):
    def __init__(self, api: _WindowsApi, path: Path, mode: str):
        self._api = api
        self._path = path
        self._mode = mode
        self._handle: int | None = None

    def __enter__(self) -> "_WindowsHeldRegularFile":
        if self._mode == TARGET_OPEN_MODE:
            share = 0
        elif self._mode == SENTINEL_OPEN_MODE:
            share = self._api.FILE_SHARE_READ
        else:
            raise LiveEnvironmentMeasurementError(
                f"unknown held-file mode: {self._mode}"
            )
        self._handle = self._api.open_path(
            self._path, directory=False, share=share
        )
        try:
            self.snapshot()
            return self
        except BaseException:
            self._api.close(self._handle)
            self._handle = None
            raise

    def snapshot(self) -> FileSnapshot:
        if self._handle is None:
            raise LiveEnvironmentMeasurementError(
                "held file is not currently open"
            )
        return self._api.snapshot(self._handle)

    def __exit__(self, exc_type, exc, traceback) -> bool:
        handle, self._handle = self._handle, None
        self._api.close(handle)
        return False


class WindowsMeasurementBackend:
    """Actual Windows/NTFS read-only collector."""

    def __init__(self) -> None:
        self._api = _WindowsApi()
        self.current_pid = os.getpid()

    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def boot_facts(self) -> Mapping[str, Any]:
        value = self._api.SYSTEM_TIMEOFDAY_INFORMATION()
        returned = ctypes.c_ulong()
        status = int(
            self._api.ntdll.NtQuerySystemInformation(
                3,
                ctypes.byref(value),
                ctypes.sizeof(value),
                ctypes.byref(returned),
            )
        )
        if status < 0:
            raise LiveEnvironmentMeasurementError(
                f"NtQuerySystemInformation(SystemTimeOfDayInformation) "
                f"failed: NTSTATUS 0x{status & 0xffffffff:08x}"
            )
        windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
        boot_time = windows_epoch + timedelta(
            microseconds=value.BootTime // 10
        )
        boot_identity = _sha256_bytes(
            f"windows-boot-filetime:{value.BootTime}".encode("ascii")
        )
        return {
            "collection_method": (
                "NtQuerySystemInformation(SystemTimeOfDayInformation)"
            ),
            "boot_time_windows_filetime_100ns": int(value.BootTime),
            "boot_time_utc": boot_time.isoformat().replace("+00:00", "Z"),
            "boot_identity_sha256": boot_identity,
        }

    def os_facts(self) -> Mapping[str, Any]:
        info = self._api.RTL_OSVERSIONINFOW()
        info.dwOSVersionInfoSize = ctypes.sizeof(info)
        status = int(self._api.ntdll.RtlGetVersion(ctypes.byref(info)))
        if status < 0:
            raise LiveEnvironmentMeasurementError(
                f"RtlGetVersion failed: NTSTATUS "
                f"0x{status & 0xffffffff:08x}"
            )
        return {
            "collection_method": "RtlGetVersion_and_platform.machine",
            "major_version": int(info.dwMajorVersion),
            "minor_version": int(info.dwMinorVersion),
            "build_number": int(info.dwBuildNumber),
            "service_pack": str(info.szCSDVersion),
            "native_architecture": platform.machine(),
            "python_architecture": platform.architecture()[0],
        }

    def volume_facts(self, path: Path) -> Mapping[str, Any]:
        volume_path = ctypes.create_unicode_buffer(32768)
        if not self._api.kernel32.GetVolumePathNameW(
            os.fspath(path), volume_path, len(volume_path)
        ):
            raise self._api.winerror("GetVolumePathNameW")
        volume_guid = ctypes.create_unicode_buffer(32768)
        if not self._api.kernel32.GetVolumeNameForVolumeMountPointW(
            volume_path.value, volume_guid, len(volume_guid)
        ):
            raise self._api.winerror("GetVolumeNameForVolumeMountPointW")
        label = ctypes.create_unicode_buffer(32768)
        filesystem = ctypes.create_unicode_buffer(32768)
        serial = ctypes.c_ulong()
        component_length = ctypes.c_ulong()
        flags = ctypes.c_ulong()
        if not self._api.kernel32.GetVolumeInformationW(
            volume_path.value,
            label,
            len(label),
            ctypes.byref(serial),
            ctypes.byref(component_length),
            ctypes.byref(flags),
            filesystem,
            len(filesystem),
        ):
            raise self._api.winerror("GetVolumeInformationW")
        return {
            "collection_method": (
                "GetVolumePathNameW_GetVolumeNameForVolumeMountPointW_"
                "GetVolumeInformationW"
            ),
            "volume_mount_path": volume_path.value,
            "volume_guid": volume_guid.value,
            "volume_serial": int(serial.value),
            "volume_serial_hex": f"{serial.value:08X}",
            "filesystem_name": filesystem.value,
            "filesystem_flags": int(flags.value),
            "filesystem_flags_hex": f"0x{flags.value:08X}",
            "maximum_component_length": int(component_length.value),
        }

    def assert_no_reparse_chain(self, path: Path) -> None:
        absolute = _absolute(path)
        parts = absolute.parts
        if not parts:
            raise ReparsePointRejected("empty absolute path")
        current = Path(parts[0])
        invalid = 0xFFFFFFFF
        for part in parts[1:]:
            current /= part
            attributes = int(
                self._api.kernel32.GetFileAttributesW(os.fspath(current))
            )
            if attributes == invalid:
                raise self._api.winerror(
                    f"GetFileAttributesW({current})"
                )
            if attributes & self._api.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ReparsePointRejected(
                    f"reparse component rejected: {current}"
                )

    def directory_identity(self, path: Path) -> ObjectIdentity:
        handle = self._api.open_path(
            path,
            directory=True,
            share=(
                self._api.FILE_SHARE_READ
                | self._api.FILE_SHARE_WRITE
                | self._api.FILE_SHARE_DELETE
            ),
        )
        try:
            identity = self._api.identity(handle)
            if not identity.is_directory:
                raise IdentityMismatch(f"not a directory: {path}")
            if identity.is_reparse_point:
                raise ReparsePointRejected(
                    f"directory is a reparse point: {path}"
                )
            return identity
        finally:
            self._api.close(handle)

    def directory_members(self, path: Path) -> Sequence[str]:
        with os.scandir(path) as iterator:
            return tuple(entry.name for entry in iterator)

    def snapshot_regular_file(self, path: Path) -> FileSnapshot:
        handle = self._api.open_path(
            path,
            directory=False,
            share=(
                self._api.FILE_SHARE_READ
                | self._api.FILE_SHARE_WRITE
                | self._api.FILE_SHARE_DELETE
            ),
        )
        try:
            return self._api.snapshot(handle)
        finally:
            self._api.close(handle)

    def hold_regular_file(
        self, path: Path, mode: str
    ) -> AbstractContextManager[HeldRegularFile]:
        return _WindowsHeldRegularFile(self._api, path, mode)

    def list_processes(self) -> Sequence[ProcessObservation]:
        raw = self._api.kernel32.CreateToolhelp32Snapshot(
            self._api.TH32CS_SNAPPROCESS, 0
        )
        handle = ctypes.cast(raw, ctypes.c_void_p).value
        if handle == self._api.INVALID_HANDLE_VALUE:
            raise self._api.winerror("CreateToolhelp32Snapshot")
        result: list[ProcessObservation] = []
        try:
            entry = self._api.PROCESSENTRY32W()
            entry.dwSize = ctypes.sizeof(entry)
            if not self._api.kernel32.Process32FirstW(
                ctypes.c_void_p(handle), ctypes.byref(entry)
            ):
                raise self._api.winerror("Process32FirstW")
            while True:
                result.append(
                    ProcessObservation(
                        pid=int(entry.th32ProcessID),
                        name=str(entry.szExeFile),
                    )
                )
                entry.dwSize = ctypes.sizeof(entry)
                if not self._api.kernel32.Process32NextW(
                    ctypes.c_void_p(handle), ctypes.byref(entry)
                ):
                    error = ctypes.get_last_error()
                    if error == 18:  # ERROR_NO_MORE_FILES
                        break
                    raise self._api.winerror("Process32NextW")
        finally:
            self._api.close(handle)
        return tuple(result)

