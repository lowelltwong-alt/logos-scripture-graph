#!/usr/bin/env python3
"""Windows/NTFS native measurement primitives for T550 V9 component V3.

This is *not* the Hosea production launcher and cannot issue production
evidence.  Its only public collector is explicitly test-only and accepts only
an isolated ``C:\\tmp\\t550-v3-native-<nonce>`` tree.  It uses real Windows
handles, retains them in a non-serializable lease, and never prepares,
publishes, recovers, restarts, or changes OneDrive.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import sys
import time
from typing import Any, Iterable, Sequence


WINDOWS_DESIGN_DOCKET_SHA256 = (
    "a2f7944cb33161457d7f092631046c1608ed7c6be8422c04800ec9c56dc781bd"
)
POLICY_DESIGN_DOCKET_SHA256 = (
    "142b322c9d647da9290743d2676244008f7694e2375f45073318285ca7943a46"
)
CONTRACT_V3_SHA256 = (
    "28b503b96b6790d65c72685caa4d6c63ea68a6cfb4473dddb5612d0c60d71b22"
)
BOSS_DESIGN_RULING_SHA256 = (
    "67af1a7766947172c0197b58a161d3a6af669010d1ff9c68dac59b9b8e4fa6ee"
)
SCHEMA_VERSION = "windows_nt_native_measurement_v3.test_only.v2"
TEST_BACKEND_ID = "windows_nt_native_v3_temp_root_test_only"
TEST_ROOT_PATTERN = re.compile(r"^t550-v3-native-[0-9a-f]{32}$")
MAX_CAPTURE_SECONDS = 120


class NativeMeasurementV3Error(RuntimeError):
    """Native measurement or safety contract failed closed."""


class UnsupportedPlatform(NativeMeasurementV3Error):
    """The native helper was invoked outside Windows/NTFS."""


class UnsafeTestRoot(NativeMeasurementV3Error):
    """The requested test root is not an isolated C:\\tmp nonce."""


class ReparseRejected(NativeMeasurementV3Error):
    """A retained root, parent, or leaf is a reparse point."""


class CoverageUnavailable(NativeMeasurementV3Error):
    """The host cannot safely exercise an optional effects case."""


def canonical_json_bytes(value: Any) -> bytes:
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


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _iso(value: datetime) -> str:
    if value.tzinfo is None:
        raise NativeMeasurementV3Error("naive wall clock")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_relative(token: str) -> tuple[str, ...]:
    if not isinstance(token, str) or not token:
        raise NativeMeasurementV3Error("empty relative token")
    rendered = token.replace("\\", "/")
    path = PureWindowsPath(rendered)
    if path.is_absolute() or path.drive or any(part in ("", ".", "..") for part in path.parts):
        raise NativeMeasurementV3Error(f"unsafe relative token: {token!r}")
    if any(":" in part or part.endswith((" ", ".")) for part in path.parts):
        raise NativeMeasurementV3Error(f"ambiguous relative token: {token!r}")
    return tuple(path.parts)


def verify_safe_test_root(path: Path) -> Path:
    """Resolve and verify the only tree this test-only helper may inspect."""
    if os.name != "nt" or sys.platform != "win32":
        raise UnsupportedPlatform("Windows native helper requires win32")
    resolved = Path(path).resolve(strict=True)
    tmp_root = Path(r"C:\tmp").resolve(strict=True)
    if resolved.parent != tmp_root or TEST_ROOT_PATTERN.fullmatch(resolved.name) is None:
        raise UnsafeTestRoot(
            "test root must be one direct C:\\tmp\\t550-v3-native-<32 hex> child"
        )
    implementation_root = Path(__file__).resolve().parents[5]
    try:
        resolved.relative_to(implementation_root)
    except ValueError:
        pass
    else:
        raise UnsafeTestRoot("test root may not be inside the repository")
    try:
        implementation_root.relative_to(resolved)
    except ValueError:
        pass
    else:
        raise UnsafeTestRoot("test root may not contain the repository")
    return resolved


class _FILE_ID_128(ctypes.Structure):
    _fields_ = [("identifier", ctypes.c_ubyte * 16)]


class _FILE_ID_INFO(ctypes.Structure):
    _fields_ = [
        ("volume_serial_number", ctypes.c_ulonglong),
        ("file_id", _FILE_ID_128),
    ]


class _FILE_ATTRIBUTE_TAG_INFO(ctypes.Structure):
    _fields_ = [
        ("file_attributes", wintypes.DWORD),
        ("reparse_tag", wintypes.DWORD),
    ]


class _FILE_STANDARD_INFO(ctypes.Structure):
    _fields_ = [
        ("allocation_size", ctypes.c_longlong),
        ("end_of_file", ctypes.c_longlong),
        ("number_of_links", wintypes.DWORD),
        ("delete_pending", wintypes.BOOLEAN),
        ("directory", wintypes.BOOLEAN),
    ]


class _FILETIME(ctypes.Structure):
    _fields_ = [("low", wintypes.DWORD), ("high", wintypes.DWORD)]

    def integer(self) -> int:
        return (int(self.high) << 32) | int(self.low)


class _UNICODE_STRING(ctypes.Structure):
    _fields_ = [
        ("Length", ctypes.c_ushort),
        ("MaximumLength", ctypes.c_ushort),
        ("Buffer", ctypes.c_wchar_p),
    ]


class _OBJECT_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Length", wintypes.ULONG),
        ("RootDirectory", wintypes.HANDLE),
        ("ObjectName", ctypes.POINTER(_UNICODE_STRING)),
        ("Attributes", wintypes.ULONG),
        ("SecurityDescriptor", wintypes.LPVOID),
        ("SecurityQualityOfService", wintypes.LPVOID),
    ]


class _IO_STATUS_BLOCK(ctypes.Structure):
    _fields_ = [("Status", ctypes.c_void_p), ("Information", ctypes.c_size_t)]


class _RTL_OSVERSIONINFOW(ctypes.Structure):
    _fields_ = [
        ("dwOSVersionInfoSize", wintypes.DWORD),
        ("dwMajorVersion", wintypes.DWORD),
        ("dwMinorVersion", wintypes.DWORD),
        ("dwBuildNumber", wintypes.DWORD),
        ("dwPlatformId", wintypes.DWORD),
        ("szCSDVersion", ctypes.c_wchar * 128),
    ]


class _SYSTEM_TIMEOFDAY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BootTime", ctypes.c_longlong),
        ("CurrentTime", ctypes.c_longlong),
        ("TimeZoneBias", ctypes.c_longlong),
        ("CurrentTimeZoneId", wintypes.ULONG),
        ("Reserved", wintypes.ULONG),
        ("BootTimeBias", ctypes.c_ulonglong),
        ("SleepTimeBias", ctypes.c_ulonglong),
    ]


@dataclass(frozen=True)
class HandleIdentity:
    volume_serial: int
    file_id: str
    attributes: int
    reparse_tag: int
    is_directory: bool
    reparse_point: bool
    link_count: int
    delete_pending: bool


@dataclass(frozen=True)
class FileObservation:
    token: str
    parent_token: str
    leaf: str
    parent_identity: HandleIdentity
    identity: HandleIdentity
    size_bytes: int
    sha256: str
    observed_wall_utc: str
    observed_monotonic_ns: int
    open_mode: str


@dataclass(frozen=True)
class ProcessObservation:
    pid: int
    parent_pid: int
    normalized_measured_name: str
    start_token: str
    executable_file_identity: HandleIdentity
    observed_wall_utc: str
    observed_monotonic_ns: int
    identity_phase: str
    liveness_check: str


class _Api:
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    DELETE = 0x00010000
    FILE_READ_DATA = 0x00000001
    FILE_READ_ATTRIBUTES = 0x00000080
    SYNCHRONIZE = 0x00100000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    OPEN_EXISTING = 3
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
    FILE_ATTRIBUTE_DIRECTORY = 0x10
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    FILE_ID_INFO_CLASS = 18
    FILE_ATTRIBUTE_TAG_INFO_CLASS = 9
    FILE_STANDARD_INFO_CLASS = 1
    FILE_NAME_INFO_CLASS = 2
    FILE_DIRECTORY_FILE = 0x00000001
    FILE_NON_DIRECTORY_FILE = 0x00000040
    FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020
    FILE_OPEN_REPARSE_POINT = 0x00200000
    OBJ_CASE_INSENSITIVE = 0x00000040
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    TH32CS_SNAPPROCESS = 0x00000002
    WAIT_OBJECT_0 = 0x00000000
    WAIT_TIMEOUT = 0x00000102
    WAIT_FAILED = 0xFFFFFFFF

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(wintypes.ULONG)),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", ctypes.c_wchar * 260),
        ]

    def __init__(self) -> None:
        if os.name != "nt" or sys.platform != "win32":
            raise UnsupportedPlatform("native helper requires Windows")
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.ntdll = ctypes.WinDLL("ntdll")
        self.kernel32.CreateFileW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        self.kernel32.CreateFileW.restype = wintypes.HANDLE
        self.kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        self.kernel32.CloseHandle.restype = wintypes.BOOL
        self.kernel32.GetFileInformationByHandleEx.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            wintypes.LPVOID,
            wintypes.DWORD,
        ]
        self.kernel32.GetFileInformationByHandleEx.restype = wintypes.BOOL
        self.kernel32.GetFileSizeEx.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_longlong),
        ]
        self.kernel32.GetFileSizeEx.restype = wintypes.BOOL
        self.kernel32.SetFilePointerEx.argtypes = [
            wintypes.HANDLE,
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_longlong),
            wintypes.DWORD,
        ]
        self.kernel32.SetFilePointerEx.restype = wintypes.BOOL
        self.kernel32.ReadFile.argtypes = [
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ]
        self.kernel32.ReadFile.restype = wintypes.BOOL
        self.kernel32.OpenProcess.argtypes = [
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD,
        ]
        self.kernel32.OpenProcess.restype = wintypes.HANDLE
        self.kernel32.GetProcessTimes.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(_FILETIME),
            ctypes.POINTER(_FILETIME),
            ctypes.POINTER(_FILETIME),
            ctypes.POINTER(_FILETIME),
        ]
        self.kernel32.GetProcessTimes.restype = wintypes.BOOL
        self.kernel32.QueryFullProcessImageNameW.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.LPWSTR,
            ctypes.POINTER(wintypes.DWORD),
        ]
        self.kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
        self.kernel32.WaitForSingleObject.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
        ]
        self.kernel32.WaitForSingleObject.restype = wintypes.DWORD
        self.kernel32.GetVolumePathNameW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            wintypes.DWORD,
        ]
        self.kernel32.GetVolumePathNameW.restype = wintypes.BOOL
        self.kernel32.GetVolumeNameForVolumeMountPointW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            wintypes.DWORD,
        ]
        self.kernel32.GetVolumeNameForVolumeMountPointW.restype = wintypes.BOOL
        self.ntdll.NtOpenFile.restype = ctypes.c_long
        self.ntdll.RtlGetVersion.restype = ctypes.c_long
        self.ntdll.NtQuerySystemInformation.restype = ctypes.c_long

    def error(self, label: str) -> OSError:
        return ctypes.WinError(ctypes.get_last_error(), label)

    def close(self, handle: int | None) -> None:
        if handle not in (None, 0, self.INVALID_HANDLE_VALUE):
            if not self.kernel32.CloseHandle(wintypes.HANDLE(handle)):
                raise self.error("CloseHandle")

    def open_full(
        self,
        path: Path,
        *,
        directory: bool,
        share: int,
        access: int | None = None,
    ) -> int:
        desired = access if access is not None else (
            self.GENERIC_READ | self.FILE_READ_ATTRIBUTES | self.SYNCHRONIZE
        )
        flags = self.FILE_FLAG_OPEN_REPARSE_POINT
        if directory:
            flags |= self.FILE_FLAG_BACKUP_SEMANTICS
        raw = self.kernel32.CreateFileW(
            os.fspath(path),
            desired,
            share,
            None,
            self.OPEN_EXISTING,
            flags,
            None,
        )
        value = ctypes.cast(raw, ctypes.c_void_p).value
        if value == self.INVALID_HANDLE_VALUE:
            raise self.error(f"CreateFileW({path})")
        return int(value)

    def open_relative(
        self,
        parent_handle: int,
        leaf: str,
        *,
        directory: bool,
        share: int,
    ) -> int:
        parts = _safe_relative(leaf)
        if len(parts) != 1:
            raise NativeMeasurementV3Error("relative native open requires one exact leaf")
        buffer = ctypes.create_unicode_buffer(parts[0])
        name = _UNICODE_STRING(
            Length=len(parts[0].encode("utf-16-le")),
            MaximumLength=(len(parts[0]) + 1) * 2,
            Buffer=ctypes.cast(buffer, ctypes.c_wchar_p),
        )
        attrs = _OBJECT_ATTRIBUTES(
            Length=ctypes.sizeof(_OBJECT_ATTRIBUTES),
            RootDirectory=wintypes.HANDLE(parent_handle),
            ObjectName=ctypes.pointer(name),
            Attributes=self.OBJ_CASE_INSENSITIVE,
            SecurityDescriptor=None,
            SecurityQualityOfService=None,
        )
        iosb = _IO_STATUS_BLOCK()
        result = wintypes.HANDLE()
        options = self.FILE_SYNCHRONOUS_IO_NONALERT | self.FILE_OPEN_REPARSE_POINT
        options |= self.FILE_DIRECTORY_FILE if directory else self.FILE_NON_DIRECTORY_FILE
        status = int(
            self.ntdll.NtOpenFile(
                ctypes.byref(result),
                self.FILE_READ_DATA | self.FILE_READ_ATTRIBUTES | self.SYNCHRONIZE,
                ctypes.byref(attrs),
                ctypes.byref(iosb),
                share,
                options,
            )
        )
        if status < 0:
            raise NativeMeasurementV3Error(
                f"NtOpenFile({leaf}) NTSTATUS=0x{status & 0xffffffff:08x}"
            )
        return int(ctypes.cast(result, ctypes.c_void_p).value)

    def identity(self, handle: int) -> HandleIdentity:
        file_id = _FILE_ID_INFO()
        if not self.kernel32.GetFileInformationByHandleEx(
            wintypes.HANDLE(handle),
            self.FILE_ID_INFO_CLASS,
            ctypes.byref(file_id),
            ctypes.sizeof(file_id),
        ):
            raise self.error("GetFileInformationByHandleEx(FileIdInfo)")
        tag = _FILE_ATTRIBUTE_TAG_INFO()
        if not self.kernel32.GetFileInformationByHandleEx(
            wintypes.HANDLE(handle),
            self.FILE_ATTRIBUTE_TAG_INFO_CLASS,
            ctypes.byref(tag),
            ctypes.sizeof(tag),
        ):
            raise self.error("GetFileInformationByHandleEx(FileAttributeTagInfo)")
        standard = _FILE_STANDARD_INFO()
        if not self.kernel32.GetFileInformationByHandleEx(
            wintypes.HANDLE(handle),
            self.FILE_STANDARD_INFO_CLASS,
            ctypes.byref(standard),
            ctypes.sizeof(standard),
        ):
            raise self.error("GetFileInformationByHandleEx(FileStandardInfo)")
        attributes = int(tag.file_attributes)
        identifier = bytes(file_id.file_id.identifier).hex()
        return HandleIdentity(
            volume_serial=int(file_id.volume_serial_number),
            file_id=identifier,
            attributes=attributes,
            reparse_tag=int(tag.reparse_tag),
            is_directory=bool(attributes & self.FILE_ATTRIBUTE_DIRECTORY),
            reparse_point=bool(attributes & self.FILE_ATTRIBUTE_REPARSE_POINT),
            link_count=int(standard.number_of_links),
            delete_pending=bool(standard.delete_pending),
        )

    def file_name(self, handle: int) -> str:
        size = 65536
        buffer = ctypes.create_string_buffer(size)
        if not self.kernel32.GetFileInformationByHandleEx(
            wintypes.HANDLE(handle),
            self.FILE_NAME_INFO_CLASS,
            buffer,
            size,
        ):
            raise self.error("GetFileInformationByHandleEx(FileNameInfo)")
        length = ctypes.cast(buffer, ctypes.POINTER(wintypes.DWORD)).contents.value
        raw = buffer.raw[4 : 4 + length]
        return raw.decode("utf-16-le")

    def hash_file(self, handle: int) -> tuple[int, str]:
        size = ctypes.c_longlong()
        if not self.kernel32.GetFileSizeEx(wintypes.HANDLE(handle), ctypes.byref(size)):
            raise self.error("GetFileSizeEx")
        if not self.kernel32.SetFilePointerEx(
            wintypes.HANDLE(handle), 0, None, 0
        ):
            raise self.error("SetFilePointerEx")
        remaining = int(size.value)
        digest = hashlib.sha256()
        while remaining:
            requested = min(remaining, 1024 * 1024)
            buffer = ctypes.create_string_buffer(requested)
            count = wintypes.DWORD()
            if not self.kernel32.ReadFile(
                wintypes.HANDLE(handle),
                buffer,
                requested,
                ctypes.byref(count),
                None,
            ):
                raise self.error("ReadFile")
            if count.value == 0:
                raise NativeMeasurementV3Error("short handle read")
            digest.update(buffer.raw[: count.value])
            remaining -= int(count.value)
        return int(size.value), digest.hexdigest()

    def require_process_running(
        self,
        handle: int,
        *,
        label: str,
        expected_start_token: str | None = None,
    ) -> str:
        wait = int(
            self.kernel32.WaitForSingleObject(wintypes.HANDLE(handle), 0)
        )
        if wait == self.WAIT_FAILED:
            raise self.error(f"WaitForSingleObject({label})")
        if wait != self.WAIT_TIMEOUT:
            raise NativeMeasurementV3Error(
                f"{label} is not running: wait=0x{wait:08x}"
            )
        creation, exit_time, kernel_time, user_time = (
            _FILETIME(),
            _FILETIME(),
            _FILETIME(),
            _FILETIME(),
        )
        if not self.kernel32.GetProcessTimes(
            wintypes.HANDLE(handle),
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel_time),
            ctypes.byref(user_time),
        ):
            raise self.error(f"GetProcessTimes({label})")
        token = f"windows-filetime:{creation.integer()}"
        if expected_start_token is not None and token != expected_start_token:
            raise NativeMeasurementV3Error(
                f"{label} PID/start identity changed"
            )
        return token


class NativeHandleLeaseV3:
    """Opaque, process-local, test-only retained-handle lease."""

    __slots__ = ("_api", "_handles", "_closed", "_nonce", "provenance")

    def __init__(self, api: _Api) -> None:
        self._api = api
        self._handles: dict[str, int] = {}
        self._closed = False
        self._nonce = os.urandom(32)
        self.provenance = TEST_BACKEND_ID

    def retain(self, label: str, handle: int) -> int:
        if self._closed or label in self._handles:
            self._api.close(handle)
            raise NativeMeasurementV3Error("invalid lease retention")
        self._handles[label] = handle
        return handle

    def handle(self, label: str) -> int:
        if self._closed:
            raise NativeMeasurementV3Error("lease is closed")
        return self._handles[label]

    def labels(self) -> tuple[str, ...]:
        return tuple(sorted(self._handles))

    def nonce_sha256(self) -> str:
        return hashlib.sha256(self._nonce).hexdigest()

    def close(self) -> None:
        if self._closed:
            return
        failures: list[BaseException] = []
        for label in reversed(tuple(self._handles)):
            try:
                self._api.close(self._handles[label])
            except BaseException as exc:
                failures.append(exc)
        self._handles.clear()
        self._closed = True
        if failures:
            raise NativeMeasurementV3Error("one or more retained handles failed to close")

    def __enter__(self) -> "NativeHandleLeaseV3":
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        self.close()
        return False

    def __reduce__(self):
        raise TypeError("NativeHandleLeaseV3 is intentionally non-serializable")


def _require_non_reparse(identity: HandleIdentity, *, directory: bool, label: str) -> None:
    if identity.reparse_point:
        raise ReparseRejected(f"{label} is a reparse point")
    if identity.is_directory is not directory:
        raise NativeMeasurementV3Error(f"{label} object-kind drift")


def _require_single_link(identity: HandleIdentity, *, label: str) -> None:
    if identity.is_directory:
        raise NativeMeasurementV3Error(f"{label} expected a file")
    if identity.delete_pending:
        raise NativeMeasurementV3Error(f"{label} is delete-pending")
    if identity.link_count != 1:
        raise NativeMeasurementV3Error(
            f"{label} requires NTFS link count one; "
            f"observed {identity.link_count}"
        )


def _directory_members(path: Path) -> tuple[str, ...]:
    return tuple(sorted(entry.name for entry in os.scandir(path)))


def _volume_facts(api: _Api, path: Path) -> dict[str, Any]:
    volume_path = ctypes.create_unicode_buffer(32768)
    if not api.kernel32.GetVolumePathNameW(
        os.fspath(path), volume_path, len(volume_path)
    ):
        raise api.error("GetVolumePathNameW")
    volume_guid = ctypes.create_unicode_buffer(32768)
    if not api.kernel32.GetVolumeNameForVolumeMountPointW(
        volume_path.value, volume_guid, len(volume_guid)
    ):
        raise api.error("GetVolumeNameForVolumeMountPointW")
    filesystem = ctypes.create_unicode_buffer(32768)
    serial = wintypes.DWORD()
    max_component = wintypes.DWORD()
    flags = wintypes.DWORD()
    if not api.kernel32.GetVolumeInformationW(
        volume_path.value,
        None,
        0,
        ctypes.byref(serial),
        ctypes.byref(max_component),
        ctypes.byref(flags),
        filesystem,
        len(filesystem),
    ):
        raise api.error("GetVolumeInformationW")
    if filesystem.value.upper() != "NTFS":
        raise UnsupportedPlatform(f"safe test root is not NTFS: {filesystem.value}")
    return {
        "mount_path": volume_path.value,
        "volume_guid": volume_guid.value,
        "volume_serial": int(serial.value),
        "filesystem": filesystem.value,
        "filesystem_flags": int(flags.value),
        "maximum_component_length": int(max_component.value),
    }


def _boot_os_facts(api: _Api) -> tuple[dict[str, Any], dict[str, Any]]:
    version = _RTL_OSVERSIONINFOW()
    version.dwOSVersionInfoSize = ctypes.sizeof(version)
    status = int(api.ntdll.RtlGetVersion(ctypes.byref(version)))
    if status < 0:
        raise NativeMeasurementV3Error(
            f"RtlGetVersion NTSTATUS=0x{status & 0xffffffff:08x}"
        )
    tod = _SYSTEM_TIMEOFDAY_INFORMATION()
    returned = wintypes.ULONG()
    status = int(
        api.ntdll.NtQuerySystemInformation(
            3,
            ctypes.byref(tod),
            ctypes.sizeof(tod),
            ctypes.byref(returned),
        )
    )
    if status < 0:
        raise NativeMeasurementV3Error(
            f"NtQuerySystemInformation NTSTATUS=0x{status & 0xffffffff:08x}"
        )
    boot_time = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(
        microseconds=int(tod.BootTime) // 10
    )
    boot = {
        "boot_filetime_100ns": int(tod.BootTime),
        "boot_identity": hashlib.sha256(
            f"windows-boot-filetime:{int(tod.BootTime)}".encode("ascii")
        ).hexdigest(),
        "boot_time_utc": _iso(boot_time),
    }
    operating_system = {
        "name": "Windows",
        "major": int(version.dwMajorVersion),
        "minor": int(version.dwMinorVersion),
        "build": int(version.dwBuildNumber),
        "native_architecture": os.environ.get("PROCESSOR_ARCHITECTURE", "unknown"),
        "python_bits": ctypes.sizeof(ctypes.c_void_p) * 8,
    }
    return boot, operating_system


def _process_table(api: _Api) -> dict[int, tuple[int, str]]:
    api.kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    api.kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    raw = api.kernel32.CreateToolhelp32Snapshot(api.TH32CS_SNAPPROCESS, 0)
    handle = ctypes.cast(raw, ctypes.c_void_p).value
    if handle == api.INVALID_HANDLE_VALUE:
        raise api.error("CreateToolhelp32Snapshot")
    result: dict[int, tuple[int, str]] = {}
    try:
        entry = api.PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(entry)
        api.kernel32.Process32FirstW.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(api.PROCESSENTRY32W),
        ]
        api.kernel32.Process32FirstW.restype = wintypes.BOOL
        api.kernel32.Process32NextW.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(api.PROCESSENTRY32W),
        ]
        api.kernel32.Process32NextW.restype = wintypes.BOOL
        if not api.kernel32.Process32FirstW(
            wintypes.HANDLE(handle), ctypes.byref(entry)
        ):
            raise api.error("Process32FirstW")
        while True:
            pid = int(entry.th32ProcessID)
            if pid in result:
                raise NativeMeasurementV3Error("duplicate PID in process snapshot")
            result[pid] = (
                int(entry.th32ParentProcessID),
                str(entry.szExeFile).casefold(),
            )
            entry.dwSize = ctypes.sizeof(entry)
            if not api.kernel32.Process32NextW(
                wintypes.HANDLE(handle), ctypes.byref(entry)
            ):
                if ctypes.get_last_error() == 18:
                    break
                raise api.error("Process32NextW")
    finally:
        api.close(int(handle))
    return result


def _observe_process(
    api: _Api,
    lease: NativeHandleLeaseV3,
    table: dict[int, tuple[int, str]],
    pid: int,
    depth: int,
) -> ProcessObservation:
    if pid not in table:
        raise NativeMeasurementV3Error(f"PID {pid} missing from process snapshot")
    parent_pid, measured_name = table[pid]
    process = api.kernel32.OpenProcess(
        api.PROCESS_QUERY_LIMITED_INFORMATION | api.SYNCHRONIZE,
        False,
        pid,
    )
    value = ctypes.cast(process, ctypes.c_void_p).value
    if not value:
        raise api.error(f"OpenProcess({pid})")
    lease.retain(f"process:{depth}:{pid}", int(value))
    start_token = api.require_process_running(
        int(value), label=f"process {pid}"
    )
    capacity = wintypes.DWORD(32768)
    image_buffer = ctypes.create_unicode_buffer(capacity.value)
    if not api.kernel32.QueryFullProcessImageNameW(
        wintypes.HANDLE(value), 0, image_buffer, ctypes.byref(capacity)
    ):
        raise api.error(f"QueryFullProcessImageNameW({pid})")
    image_handle = api.open_full(
        Path(image_buffer.value),
        directory=False,
        share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
    )
    lease.retain(f"process-image:{depth}:{pid}", image_handle)
    image_identity = api.identity(image_handle)
    _require_non_reparse(
        image_identity, directory=False, label=f"process executable {pid}"
    )
    api.require_process_running(
        int(value),
        label=f"process {pid}",
        expected_start_token=start_token,
    )
    return ProcessObservation(
        pid=pid,
        parent_pid=parent_pid,
        normalized_measured_name=measured_name,
        start_token=start_token,
        executable_file_identity=image_identity,
        observed_wall_utc=_iso(datetime.now(timezone.utc)),
        observed_monotonic_ns=time.monotonic_ns(),
        identity_phase="ephemeral_live_post_invocation_not_frozen",
        liveness_check=(
            "WaitForSingleObject(handle,0)==WAIT_TIMEOUT_and_"
            "start_token_unchanged"
        ),
    )


def _observe_ancestry(
    api: _Api,
    lease: NativeHandleLeaseV3,
    *,
    maximum_depth: int = 3,
) -> list[ProcessObservation]:
    table = _process_table(api)
    rows: list[ProcessObservation] = []
    pid = os.getpid()
    seen: set[int] = set()
    for depth in range(maximum_depth):
        if pid <= 0:
            break
        if pid in seen:
            raise NativeMeasurementV3Error(
                "cycle in bounded process ancestry"
            )
        if pid not in table:
            raise NativeMeasurementV3Error(
                f"bounded ancestry PID {pid} missing from snapshot"
            )
        seen.add(pid)
        row = _observe_process(api, lease, table, pid, depth)
        rows.append(row)
        pid = row.parent_pid
    if not rows or rows[0].pid != os.getpid():
        raise NativeMeasurementV3Error("current process identity was not observed")
    return rows


def _final_live_validation(
    api: _Api,
    lease: NativeHandleLeaseV3,
    target_rows: Sequence[FileObservation],
    sentinel_rows: Sequence[FileObservation],
    process_rows: Sequence[ProcessObservation],
) -> None:
    for is_sentinel, rows in (
        (False, target_rows),
        (True, sentinel_rows),
    ):
        for row in rows:
            label = (
                f"sentinel:{row.token}"
                if is_sentinel
                else f"target:{row.token}"
            )
            handle = lease.handle(label)
            identity = api.identity(handle)
            _require_non_reparse(identity, directory=False, label=label)
            _require_single_link(identity, label=label)
            if identity != row.identity:
                raise NativeMeasurementV3Error(
                    f"{label} identity changed before record seal"
                )
            size, sha256 = api.hash_file(handle)
            if (size, sha256) != (row.size_bytes, row.sha256):
                raise NativeMeasurementV3Error(
                    f"{label} bytes changed before record seal"
                )
    for depth, row in enumerate(process_rows):
        api.require_process_running(
            lease.handle(f"process:{depth}:{row.pid}"),
            label=f"process {row.pid}",
            expected_start_token=row.start_token,
        )


def collect_test_only_temp_root(
    *,
    test_root: Path,
    workspace_token: str,
    model_token: str,
    target_tokens: Sequence[str],
    sentinel_tokens: Sequence[str],
) -> tuple[dict[str, Any], NativeHandleLeaseV3]:
    """Collect actual Windows evidence from one disposable temp tree only.

    The returned record is permanently marked test-only and production
    ineligible.  The caller must close the returned lease before safe cleanup.
    """
    root = verify_safe_test_root(test_root)
    if len(target_tokens) != 13 or len(sentinel_tokens) != 3:
        raise NativeMeasurementV3Error("test fixture requires exactly 13 + 3 files")
    if len(set(target_tokens) | set(sentinel_tokens)) != 16:
        raise NativeMeasurementV3Error("test fixture tokens must be distinct")
    workspace_parts = _safe_relative(workspace_token)
    model_parts = _safe_relative(model_token)
    if len(workspace_parts) != 1 or len(model_parts) != 1:
        raise NativeMeasurementV3Error("test workspace/model must be one component")
    all_tokens = [*target_tokens, *sentinel_tokens]
    for token in all_tokens:
        parts = _safe_relative(token)
        if len(parts) < 2:
            raise NativeMeasurementV3Error("file token requires parent plus leaf")
    workspace = root / workspace_parts[0]
    model = workspace / model_parts[0]
    for candidate in (workspace, model, *(model / t for t in all_tokens)):
        resolved = candidate.resolve(strict=True)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise UnsafeTestRoot("fixture path escaped safe root") from exc

    api = _Api()
    lease = NativeHandleLeaseV3(api)
    start_wall = datetime.now(timezone.utc)
    start_mono = time.monotonic_ns()
    try:
        volume = _volume_facts(api, root)
        boot, operating_system = _boot_os_facts(api)
        volume_root_handle = api.open_full(
            Path(volume["volume_guid"]),
            directory=True,
            share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
        )
        lease.retain("volume-root", volume_root_handle)
        volume_root_identity = api.identity(volume_root_handle)
        _require_non_reparse(
            volume_root_identity, directory=True, label="volume root"
        )
        workspace_handle = api.open_full(
            workspace,
            directory=True,
            share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
        )
        lease.retain("workspace", workspace_handle)
        workspace_identity = api.identity(workspace_handle)
        _require_non_reparse(workspace_identity, directory=True, label="workspace")
        model_handle = api.open_relative(
            workspace_handle,
            model_parts[0],
            directory=True,
            share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
        )
        lease.retain("model", model_handle)
        model_identity = api.identity(model_handle)
        _require_non_reparse(model_identity, directory=True, label="model")

        parent_tokens = sorted(
            {str(PureWindowsPath(token).parent).replace("\\", "/") for token in all_tokens}
        )
        parent_handles: dict[str, int] = {}
        parent_identities: dict[str, HandleIdentity] = {}
        parent_members_before: dict[str, tuple[str, ...]] = {}
        for parent_token in parent_tokens:
            parts = _safe_relative(parent_token)
            current_handle = model_handle
            current_path = model
            accumulated: list[str] = []
            for part in parts:
                accumulated.append(part)
                key = "/".join(accumulated)
                if key in parent_handles:
                    current_handle = parent_handles[key]
                    current_path /= part
                    continue
                handle = api.open_relative(
                    current_handle,
                    part,
                    directory=True,
                    share=(
                        api.FILE_SHARE_READ
                        | api.FILE_SHARE_WRITE
                        | api.FILE_SHARE_DELETE
                    ),
                )
                lease.retain(f"parent:{key}", handle)
                identity = api.identity(handle)
                _require_non_reparse(identity, directory=True, label=f"parent {key}")
                parent_handles[key] = handle
                parent_identities[key] = identity
                current_handle = handle
                current_path /= part
            parent_members_before[parent_token] = _directory_members(model / parent_token)

        if len(
            {
                (identity.volume_serial, identity.file_id)
                for identity in parent_identities.values()
            }
        ) != len(parent_identities):
            raise NativeMeasurementV3Error("canonical parent identity alias")

        target_rows: list[FileObservation] = []
        sentinel_rows: list[FileObservation] = []
        all_file_identities: set[tuple[int, str]] = set()
        sentinel_set = set(sentinel_tokens)
        for token in all_tokens:
            parts = _safe_relative(token)
            parent_token = "/".join(parts[:-1])
            leaf = parts[-1]
            parent_handle = parent_handles[parent_token]
            is_sentinel = token in sentinel_set
            share = api.FILE_SHARE_READ if is_sentinel else 0
            handle = api.open_relative(
                parent_handle, leaf, directory=False, share=share
            )
            label = (
                f"sentinel:{token}" if is_sentinel else f"target:{token}"
            )
            lease.retain(label, handle)
            identity = api.identity(handle)
            _require_non_reparse(identity, directory=False, label=label)
            _require_single_link(identity, label=label)
            key = (identity.volume_serial, identity.file_id)
            if key in all_file_identities:
                raise NativeMeasurementV3Error("target/sentinel file identity alias")
            all_file_identities.add(key)
            observed_name = PureWindowsPath(api.file_name(handle)).name
            if observed_name.casefold() != leaf.casefold():
                raise NativeMeasurementV3Error("handle leaf-name relation drift")
            size, sha256 = api.hash_file(handle)
            row = FileObservation(
                token=token.replace("\\", "/"),
                parent_token=parent_token,
                leaf=leaf,
                parent_identity=parent_identities[parent_token],
                identity=identity,
                size_bytes=size,
                sha256=sha256,
                observed_wall_utc=_iso(datetime.now(timezone.utc)),
                observed_monotonic_ns=time.monotonic_ns(),
                open_mode=(
                    "test_only_sentinel_deny_write_delete"
                    if is_sentinel
                    else "test_only_target_exclusive_measurement"
                ),
            )
            (sentinel_rows if is_sentinel else target_rows).append(row)

        process_rows = _observe_ancestry(api, lease)
        parent_members_after = {
            token: _directory_members(model / token) for token in parent_tokens
        }
        if parent_members_after != parent_members_before:
            raise NativeMeasurementV3Error("directory membership changed during capture")
        _final_live_validation(
            api,
            lease,
            target_rows,
            sentinel_rows,
            process_rows,
        )
        end_wall = datetime.now(timezone.utc)
        end_mono = time.monotonic_ns()
        duration = (end_mono - start_mono) / 1_000_000_000
        if duration < 0 or duration > MAX_CAPTURE_SECONDS:
            raise NativeMeasurementV3Error("capture exceeded bounded lease")
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "provenance": {
                "backend_id": TEST_BACKEND_ID,
                "test_only": True,
                "production_eligible": False,
                "effect_authorized": False,
                "injection_enabled": False,
                "windows_design_docket_sha256": WINDOWS_DESIGN_DOCKET_SHA256,
                "policy_design_docket_sha256": POLICY_DESIGN_DOCKET_SHA256,
                "contract_v3_sha256": CONTRACT_V3_SHA256,
                "boss_design_ruling_sha256": BOSS_DESIGN_RULING_SHA256,
                "receipt_class": "read_only_collector",
                "synthetic_transaction_receipt": False,
                "owner_capability_supplied": False,
            },
            "artifact_dependency_topology": {
                "class": "fixed_input_hashes_only_no_self_or_review_back_edge",
                "external_runtime_trust_anchor_supplied": False,
                "execution_freeze_created": False,
            },
            "identity_phases": {
                "stable_test_fixture": (
                    "file_root_volume_and_executable_file_identities"
                ),
                "ephemeral_live": (
                    "pid_start_handle_lease_nonce_and_live_ancestry_not_frozen"
                ),
                "restart_occurred": False,
            },
            "review_timing": {
                "static_or_human_review_inside_lease": False,
                "fresh_live_check": (
                    "deterministic_final_handle_revalidation_before_record_seal"
                ),
            },
            "lifecycle": {
                "transaction_completed_state_entered": False,
                "final_live_validation_before_record_seal": True,
                "post_completed_validation_claimed": False,
            },
            "safe_test_root": os.fspath(root),
            "capture": {
                "start_wall_utc": _iso(start_wall),
                "end_wall_utc": _iso(end_wall),
                "start_monotonic_ns": start_mono,
                "end_monotonic_ns": end_mono,
                "duration_seconds": duration,
            },
            "boot": boot,
            "operating_system": operating_system,
            "volume": {
                **volume,
                "volume_root_identity": asdict(volume_root_identity),
            },
            "workspace": {
                "token": workspace_token,
                "identity": asdict(workspace_identity),
            },
            "model": {"token": model_token, "identity": asdict(model_identity)},
            "canonical_parents": [
                {
                    "token": token,
                    "identity": asdict(parent_identities[token]),
                    "members_before": list(parent_members_before[token]),
                    "members_after": list(parent_members_after[token]),
                }
                for token in parent_tokens
            ],
            "targets": [asdict(row) for row in target_rows],
            "sentinels": [asdict(row) for row in sentinel_rows],
            "process_ancestry": [asdict(row) for row in process_rows],
            "retained_handle_labels": list(lease.labels()),
            "lease_nonce_sha256": lease.nonce_sha256(),
            "effects": {
                "canonical_or_global_path_opened": False,
                "probe_file_created_by_collector": False,
                "delete_or_replace_attempted_by_collector": False,
                "restart_or_onedrive_action_attempted": False,
                "prepare_publish_or_recover_attempted": False,
                "governed_bytes_changed": False,
                "directory_members_changed": False,
                "receipt_class": "read_only_zero_byte_and_member_delta",
                "synthetic_replacement_exercised": False,
                "metadata_effect_status": "coverage_unavailable",
            },
            "limitations": {
                "production_evidence": False,
                "process_inventory_exhaustive": False,
                "future_or_preopened_writers_excluded": False,
                "power_loss_durability_proven": False,
                "set_atomicity_proven": False,
                "metadata_or_cloud_hydration_zero_effect_proven": False,
                "external_owner_capability_present": False,
                "canonical_readiness_claimed": False,
                "terminal_completed_state_claimed": False,
            },
        }
        record["raw_measurement_sha256"] = digest_value(record)
        return record, lease
    except BaseException:
        lease.close()
        raise


def competing_open_denied(path: Path, *, delete_access: bool = False) -> bool:
    """Return whether a real competing write/delete open is sharing-denied."""
    api = _Api()
    access = api.DELETE if delete_access else api.GENERIC_WRITE
    try:
        handle = api.open_full(
            Path(path),
            directory=False,
            share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
            access=access,
        )
    except OSError as exc:
        if getattr(exc, "winerror", None) == 32:
            return True
        raise
    else:
        api.close(handle)
        return False


def exercise_reparse_rejection(test_root: Path) -> dict[str, Any]:
    """Exercise one safe temp-root symlink; report unavailable without PASS."""
    root = verify_safe_test_root(test_root)
    source = root / "reparse-source.txt"
    link = root / "reparse-link.txt"
    source.write_bytes(b"reparse-fixture\n")
    try:
        os.symlink(source, link)
    except OSError as exc:
        return {
            "case": "reparse_rejection",
            "status": "coverage_unavailable",
            "reason": f"{type(exc).__name__}: {exc}",
        }
    api = _Api()
    handle: int | None = None
    try:
        handle = api.open_full(
            link,
            directory=False,
            share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
        )
        identity = api.identity(handle)
        if not identity.reparse_point:
            raise NativeMeasurementV3Error("symlink did not expose reparse identity")
        return {
            "case": "reparse_rejection",
            "status": "PASS_REJECTED_REPARSE",
            "reparse_tag": identity.reparse_tag,
        }
    finally:
        if handle is not None:
            api.close(handle)


def assert_safe_cleanup_target(test_root: Path) -> Path:
    """Re-verify the exact nonce directory immediately before test cleanup."""
    return verify_safe_test_root(test_root)
