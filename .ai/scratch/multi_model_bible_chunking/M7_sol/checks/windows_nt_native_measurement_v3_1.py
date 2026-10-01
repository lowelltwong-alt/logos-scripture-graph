#!/usr/bin/env python3
"""Safer Windows/NTFS native measurement adapter for T550 V3.1 tests.

This module is an environment-bound, test-only runtime adapter.  It accepts
only one disposable ``C:\\tmp\\t550-v3-1-native-<nonce>`` tree, exposes no
production collector, accepts no caller path for write/delete access, and
grants no cleanup authority.  If handle-relative cleanup is unavailable, the
fixture must be retained for human inspection instead of recursively removed
by path.
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
import secrets
import sys
import time
from typing import Any, Sequence


SCHEMA_VERSION = "windows_nt_native_measurement_v3_1.test_only.v1"
ADAPTER_CLASS = "environment_bound_exception"
BACKEND_ID = "windows_nt_native_v3_1_disposable_ntfs_test_only"
TEST_ROOT_PATTERN = re.compile(r"^t550-v3-1-native-[0-9a-f]{32}$")
TARGET_COUNT = 13
SENTINEL_COUNT = 3
MAX_CAPTURE_SECONDS = 120

__all__ = [
    "BACKEND_ID",
    "CoverageUnavailable",
    "NativeHandleLeaseV31",
    "NativeV31Error",
    "ReparseRejected",
    "SCHEMA_VERSION",
    "UnsafeTestRoot",
    "collect_test_only_temp_root",
    "digest_value",
    "verify_safe_test_root",
]


class NativeV31Error(RuntimeError):
    """A test-only native invariant failed closed."""


class UnsupportedPlatform(NativeV31Error):
    """The adapter was invoked outside supported Windows/NTFS."""


class UnsafeTestRoot(NativeV31Error):
    """The requested root was not the exact disposable nonce shape."""


class ReparseRejected(NativeV31Error):
    """A retained root, directory, or file was a reparse point."""


class CoverageUnavailable(NativeV31Error):
    """A test condition cannot be established safely on this host."""


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
        raise NativeV31Error("naive clock")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_parts(token: str) -> tuple[str, ...]:
    if not isinstance(token, str) or not token:
        raise NativeV31Error("empty relative token")
    path = PureWindowsPath(token.replace("\\", "/"))
    if path.is_absolute() or path.drive:
        raise NativeV31Error(f"absolute token forbidden: {token!r}")
    if any(
        part in ("", ".", "..")
        or ":" in part
        or part.endswith((" ", "."))
        for part in path.parts
    ):
        raise NativeV31Error(f"ambiguous token forbidden: {token!r}")
    return tuple(path.parts)


def verify_safe_test_root(path: Path) -> Path:
    """Resolve the sole root the adapter may inspect; never authorizes cleanup."""
    if os.name != "nt" or sys.platform != "win32":
        raise UnsupportedPlatform("Windows native adapter requires win32")
    resolved = Path(path).resolve(strict=True)
    tmp_root = Path(r"C:\tmp").resolve(strict=True)
    if (
        resolved.parent != tmp_root
        or TEST_ROOT_PATTERN.fullmatch(resolved.name) is None
    ):
        raise UnsafeTestRoot(
            "root must be one direct C:\\tmp\\t550-v3-1-native-<32 hex> child"
        )
    repository = Path(__file__).resolve().parents[5]
    try:
        resolved.relative_to(repository)
    except ValueError:
        pass
    else:
        raise UnsafeTestRoot("test root is inside repository")
    try:
        repository.relative_to(resolved)
    except ValueError:
        pass
    else:
        raise UnsafeTestRoot("test root contains repository")
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


class _SYSTEM_INFO_ARCH(ctypes.Structure):
    _fields_ = [
        ("wProcessorArchitecture", wintypes.WORD),
        ("wReserved", wintypes.WORD),
    ]


class _SYSTEM_INFO_UNION(ctypes.Union):
    _fields_ = [("dwOemId", wintypes.DWORD), ("arch", _SYSTEM_INFO_ARCH)]


class _SYSTEM_INFO(ctypes.Structure):
    _anonymous_ = ("union",)
    _fields_ = [
        ("union", _SYSTEM_INFO_UNION),
        ("dwPageSize", wintypes.DWORD),
        ("lpMinimumApplicationAddress", wintypes.LPVOID),
        ("lpMaximumApplicationAddress", wintypes.LPVOID),
        ("dwActiveProcessorMask", ctypes.c_size_t),
        ("dwNumberOfProcessors", wintypes.DWORD),
        ("dwProcessorType", wintypes.DWORD),
        ("dwAllocationGranularity", wintypes.DWORD),
        ("wProcessorLevel", wintypes.WORD),
        ("wProcessorRevision", wintypes.WORD),
    ]


class _PROCESSENTRY32W(ctypes.Structure):
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
    ordinal: int
    kind: str
    token: str
    parent_token: str
    leaf: str
    parent_identity: HandleIdentity
    identity: HandleIdentity
    size_bytes: int
    sha256: str
    observed_wall_utc: str
    observed_monotonic_ns: int
    open_policy: str


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
    FILE_DIRECTORY_FILE = 0x00000001
    FILE_NON_DIRECTORY_FILE = 0x00000040
    FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020
    FILE_OPEN_REPARSE_POINT = 0x00200000
    OBJ_CASE_INSENSITIVE = 0x00000040
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    TH32CS_SNAPPROCESS = 0x00000002
    WAIT_TIMEOUT = 0x00000102
    WAIT_FAILED = 0xFFFFFFFF
    STATUS_SHARING_VIOLATION = 0xC0000043

    def __init__(self) -> None:
        if os.name != "nt" or sys.platform != "win32":
            raise UnsupportedPlatform("native adapter requires Windows")
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
        self.kernel32.GetNativeSystemInfo.argtypes = [
            ctypes.POINTER(_SYSTEM_INFO)
        ]
        self.kernel32.GetNativeSystemInfo.restype = None
        self.kernel32.GetCurrentProcess.argtypes = []
        self.kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        self.ntdll.NtOpenFile.argtypes = [
            ctypes.POINTER(wintypes.HANDLE),
            wintypes.DWORD,
            ctypes.POINTER(_OBJECT_ATTRIBUTES),
            ctypes.POINTER(_IO_STATUS_BLOCK),
            wintypes.DWORD,
            wintypes.DWORD,
        ]
        self.ntdll.NtOpenFile.restype = ctypes.c_long
        self.ntdll.RtlGetVersion.restype = ctypes.c_long
        self.ntdll.NtQuerySystemInformation.restype = ctypes.c_long

    def error(self, label: str) -> OSError:
        return ctypes.WinError(ctypes.get_last_error(), label)

    def close(self, handle: int | None) -> None:
        if handle not in (None, 0, self.INVALID_HANDLE_VALUE):
            if not self.kernel32.CloseHandle(wintypes.HANDLE(handle)):
                raise self.error("CloseHandle")

    def open_full_readonly(self, path: Path, *, directory: bool) -> int:
        flags = self.FILE_FLAG_OPEN_REPARSE_POINT
        if directory:
            flags |= self.FILE_FLAG_BACKUP_SEMANTICS
        raw = self.kernel32.CreateFileW(
            os.fspath(path),
            self.GENERIC_READ | self.FILE_READ_ATTRIBUTES | self.SYNCHRONIZE,
            self.FILE_SHARE_READ | self.FILE_SHARE_WRITE | self.FILE_SHARE_DELETE,
            None,
            self.OPEN_EXISTING,
            flags,
            None,
        )
        value = ctypes.cast(raw, ctypes.c_void_p).value
        if value == self.INVALID_HANDLE_VALUE:
            raise self.error(f"CreateFileW({path})")
        return int(value)

    def _nt_open_relative(
        self,
        parent_handle: int,
        leaf: str,
        *,
        directory: bool,
        share: int,
        desired_access: int,
    ) -> tuple[int, int | None]:
        parts = _safe_parts(leaf)
        if len(parts) != 1:
            raise NativeV31Error("native relative open requires one exact leaf")
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
                desired_access,
                ctypes.byref(attrs),
                ctypes.byref(iosb),
                share,
                options,
            )
        )
        if status < 0:
            return status & 0xFFFFFFFF, None
        return 0, int(ctypes.cast(result, ctypes.c_void_p).value)

    def open_relative_readonly(
        self,
        parent_handle: int,
        leaf: str,
        *,
        directory: bool,
        share: int,
    ) -> int:
        status, handle = self._nt_open_relative(
            parent_handle,
            leaf,
            directory=directory,
            share=share,
            desired_access=(
                self.FILE_READ_DATA | self.FILE_READ_ATTRIBUTES | self.SYNCHRONIZE
            ),
        )
        if status or handle is None:
            raise NativeV31Error(
                f"NtOpenFile({leaf}) NTSTATUS=0x{status:08x}"
            )
        return handle

    def _probe_contention(
        self, parent_handle: int, leaf: str, *, intent: str
    ) -> dict[str, Any]:
        desired = {
            "write": self.GENERIC_WRITE | self.SYNCHRONIZE,
            "delete": self.DELETE | self.SYNCHRONIZE,
        }.get(intent)
        if desired is None:
            raise NativeV31Error("contention intent must be write or delete")
        status, handle = self._nt_open_relative(
            parent_handle,
            leaf,
            directory=False,
            share=self.FILE_SHARE_READ | self.FILE_SHARE_WRITE | self.FILE_SHARE_DELETE,
            desired_access=desired,
        )
        if status == self.STATUS_SHARING_VIOLATION:
            return {
                "intent": intent,
                "result": "PASS_SHARING_DENIED",
                "ntstatus": f"0x{status:08x}",
                "access_effect": "open_request_only_no_write_or_delete_performed",
            }
        if status:
            raise CoverageUnavailable(
                f"contention probe {intent} returned NTSTATUS=0x{status:08x}"
            )
        assert handle is not None
        self.close(handle)
        return {
            "intent": intent,
            "result": "FAIL_COMPETING_OPEN_SUCCEEDED",
            "ntstatus": "0x00000000",
            "access_effect": "open_request_only_no_write_or_delete_performed",
        }

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
        return HandleIdentity(
            volume_serial=int(file_id.volume_serial_number),
            file_id=bytes(file_id.file_id.identifier).hex(),
            attributes=attributes,
            reparse_tag=int(tag.reparse_tag),
            is_directory=bool(attributes & self.FILE_ATTRIBUTE_DIRECTORY),
            reparse_point=bool(attributes & self.FILE_ATTRIBUTE_REPARSE_POINT),
            link_count=int(standard.number_of_links),
            delete_pending=bool(standard.delete_pending),
        )

    def hash_file(self, handle: int) -> tuple[int, str]:
        size = ctypes.c_longlong()
        if not self.kernel32.GetFileSizeEx(wintypes.HANDLE(handle), ctypes.byref(size)):
            raise self.error("GetFileSizeEx")
        if not self.kernel32.SetFilePointerEx(wintypes.HANDLE(handle), 0, None, 0):
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
            if not count.value:
                raise NativeV31Error("short handle read")
            digest.update(buffer.raw[: count.value])
            remaining -= int(count.value)
        return int(size.value), digest.hexdigest()

    def require_running(self, handle: int, expected_start: str | None = None) -> str:
        wait = int(self.kernel32.WaitForSingleObject(wintypes.HANDLE(handle), 0))
        if wait == self.WAIT_FAILED:
            raise self.error("WaitForSingleObject")
        if wait != self.WAIT_TIMEOUT:
            raise CoverageUnavailable(f"diagnostic process is not running: 0x{wait:08x}")
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
            raise self.error("GetProcessTimes")
        token = f"windows-filetime:{creation.integer()}"
        if expected_start is not None and token != expected_start:
            raise CoverageUnavailable("diagnostic process PID/start identity changed")
        return token


class NativeHandleLeaseV31:
    """Opaque test-only lease; contention probes require an issued token."""

    __slots__ = (
        "_api",
        "_handles",
        "_resources",
        "_ordinal_tokens",
        "_closed",
        "_nonce",
    )

    def __init__(self, api: _Api) -> None:
        self._api = api
        self._handles: dict[str, int] = {}
        self._resources: dict[str, tuple[str, str]] = {}
        self._ordinal_tokens: dict[tuple[str, int], str] = {}
        self._closed = False
        self._nonce = secrets.token_bytes(32)

    def retain(self, label: str, handle: int) -> int:
        if self._closed or label in self._handles:
            self._api.close(handle)
            raise NativeV31Error("invalid retained handle")
        self._handles[label] = handle
        return handle

    def handle(self, label: str) -> int:
        if self._closed:
            raise NativeV31Error("lease is closed")
        return self._handles[label]

    def register_resource(
        self,
        *,
        kind: str,
        ordinal: int,
        parent_label: str,
        leaf: str,
    ) -> None:
        token = secrets.token_hex(32)
        self._resources[token] = (parent_label, leaf)
        self._ordinal_tokens[(kind, ordinal)] = token

    def contention_token(self, *, kind: str, ordinal: int) -> str:
        if self._closed:
            raise NativeV31Error("lease is closed")
        if kind not in ("target", "sentinel") or isinstance(ordinal, bool):
            raise NativeV31Error("invalid retained resource selector")
        try:
            return self._ordinal_tokens[(kind, ordinal)]
        except KeyError as exc:
            raise NativeV31Error("retained resource selector was not issued") from exc

    def probe_contention(self, opaque_token: str, *, intent: str) -> dict[str, Any]:
        if self._closed:
            raise NativeV31Error("lease is closed")
        if not isinstance(opaque_token, str) or opaque_token not in self._resources:
            raise NativeV31Error("unknown opaque lease resource token")
        parent_label, leaf = self._resources[opaque_token]
        return self._api._probe_contention(
            self.handle(parent_label), leaf, intent=intent
        )

    def nonce_sha256(self) -> str:
        return hashlib.sha256(self._nonce).hexdigest()

    def close(self) -> None:
        if self._closed:
            return
        failures = []
        for label in reversed(tuple(self._handles)):
            try:
                self._api.close(self._handles[label])
            except BaseException as exc:
                failures.append((label, exc))
        self._handles.clear()
        self._resources.clear()
        self._ordinal_tokens.clear()
        self._closed = True
        if failures:
            raise NativeV31Error("one or more retained handles failed to close")

    def __enter__(self) -> "NativeHandleLeaseV31":
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        self.close()
        return False

    def __reduce__(self):
        raise TypeError("NativeHandleLeaseV31 is intentionally non-serializable")


def _require_identity(
    identity: HandleIdentity, *, directory: bool, label: str, single_link: bool = False
) -> None:
    if identity.reparse_point:
        raise ReparseRejected(f"{label} is a reparse point")
    if identity.is_directory is not directory:
        raise NativeV31Error(f"{label} object-kind drift")
    if identity.delete_pending:
        raise NativeV31Error(f"{label} is delete-pending")
    if single_link and identity.link_count != 1:
        raise NativeV31Error(
            f"{label} requires NTFS link count one; observed {identity.link_count}"
        )


def _volume_facts(api: _Api, root: Path) -> dict[str, Any]:
    mount = ctypes.create_unicode_buffer(32768)
    if not api.kernel32.GetVolumePathNameW(os.fspath(root), mount, len(mount)):
        raise api.error("GetVolumePathNameW")
    guid = ctypes.create_unicode_buffer(32768)
    if not api.kernel32.GetVolumeNameForVolumeMountPointW(
        mount.value, guid, len(guid)
    ):
        raise api.error("GetVolumeNameForVolumeMountPointW")
    filesystem = ctypes.create_unicode_buffer(32768)
    serial = wintypes.DWORD()
    max_component = wintypes.DWORD()
    flags = wintypes.DWORD()
    if not api.kernel32.GetVolumeInformationW(
        mount.value,
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
        raise UnsupportedPlatform(f"disposable root is not NTFS: {filesystem.value}")
    return {
        "mount_path": mount.value,
        "volume_guid": guid.value,
        "volume_serial": int(serial.value),
        "filesystem": filesystem.value,
        "filesystem_flags_raw": int(flags.value),
        "maximum_component_length": int(max_component.value),
    }


def _native_platform_facts(api: _Api) -> dict[str, Any]:
    version = _RTL_OSVERSIONINFOW()
    version.dwOSVersionInfoSize = ctypes.sizeof(version)
    status = int(api.ntdll.RtlGetVersion(ctypes.byref(version)))
    if status < 0:
        raise NativeV31Error(
            f"RtlGetVersion NTSTATUS=0x{status & 0xFFFFFFFF:08x}"
        )
    info = _SYSTEM_INFO()
    api.kernel32.GetNativeSystemInfo(ctypes.byref(info))
    arch_code = int(info.union.arch.wProcessorArchitecture)
    arch_names = {
        0: "PROCESSOR_ARCHITECTURE_INTEL",
        5: "PROCESSOR_ARCHITECTURE_ARM",
        9: "PROCESSOR_ARCHITECTURE_AMD64",
        12: "PROCESSOR_ARCHITECTURE_ARM64",
    }
    process_machine = wintypes.WORD()
    native_machine = wintypes.WORD()
    is_wow64_process2 = getattr(api.kernel32, "IsWow64Process2", None)
    wow64_status: dict[str, Any]
    if is_wow64_process2 is None:
        wow64_status = {
            "status": "coverage_unavailable",
            "reason": "IsWow64Process2 unavailable",
        }
    else:
        is_wow64_process2.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.WORD),
            ctypes.POINTER(wintypes.WORD),
        ]
        is_wow64_process2.restype = wintypes.BOOL
        if not is_wow64_process2(
            api.kernel32.GetCurrentProcess(),
            ctypes.byref(process_machine),
            ctypes.byref(native_machine),
        ):
            raise api.error("IsWow64Process2")
        wow64_status = {
            "status": "measured",
            "process_machine": int(process_machine.value),
            "native_machine": int(native_machine.value),
        }
    return {
        "os": {
            "name": "Windows",
            "major": int(version.dwMajorVersion),
            "minor": int(version.dwMinorVersion),
            "build": int(version.dwBuildNumber),
        },
        "architecture": {
            "source": "GetNativeSystemInfo_and_IsWow64Process2",
            "native_processor_architecture_code": arch_code,
            "native_processor_architecture": arch_names.get(
                arch_code, f"UNKNOWN_{arch_code}"
            ),
            "native_processor_count": int(info.dwNumberOfProcessors),
            "python_pointer_bits": ctypes.sizeof(ctypes.c_void_p) * 8,
            "wow64": wow64_status,
        },
    }


def _boot_facts(api: _Api) -> dict[str, Any]:
    value = _SYSTEM_TIMEOFDAY_INFORMATION()
    returned = wintypes.ULONG()
    status = int(
        api.ntdll.NtQuerySystemInformation(
            3,
            ctypes.byref(value),
            ctypes.sizeof(value),
            ctypes.byref(returned),
        )
    )
    if status < 0:
        raise NativeV31Error(
            f"NtQuerySystemInformation NTSTATUS=0x{status & 0xFFFFFFFF:08x}"
        )
    boot = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(
        microseconds=int(value.BootTime) // 10
    )
    return {
        "boot_filetime_100ns": int(value.BootTime),
        "boot_time_utc": _iso(boot),
        "boot_identity": hashlib.sha256(
            f"windows-boot-filetime:{int(value.BootTime)}".encode("ascii")
        ).hexdigest(),
    }


def _process_snapshot(api: _Api) -> dict[int, tuple[int, str]]:
    api.kernel32.CreateToolhelp32Snapshot.argtypes = [
        wintypes.DWORD,
        wintypes.DWORD,
    ]
    api.kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    raw = api.kernel32.CreateToolhelp32Snapshot(api.TH32CS_SNAPPROCESS, 0)
    handle = ctypes.cast(raw, ctypes.c_void_p).value
    if handle == api.INVALID_HANDLE_VALUE:
        raise api.error("CreateToolhelp32Snapshot")
    api.kernel32.Process32FirstW.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_PROCESSENTRY32W),
    ]
    api.kernel32.Process32FirstW.restype = wintypes.BOOL
    api.kernel32.Process32NextW.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_PROCESSENTRY32W),
    ]
    api.kernel32.Process32NextW.restype = wintypes.BOOL
    rows: dict[int, tuple[int, str]] = {}
    try:
        entry = _PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(entry)
        if not api.kernel32.Process32FirstW(
            wintypes.HANDLE(handle), ctypes.byref(entry)
        ):
            raise api.error("Process32FirstW")
        while True:
            pid = int(entry.th32ProcessID)
            if pid in rows:
                raise CoverageUnavailable("duplicate PID in diagnostic snapshot")
            rows[pid] = (
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
    return rows


def _diagnostic_process_evidence(
    api: _Api, lease: NativeHandleLeaseV31
) -> dict[str, Any]:
    snapshot = _process_snapshot(api)
    rows = []
    gaps = []
    pid = os.getpid()
    seen = set()
    for depth in range(3):
        if pid <= 0 or pid in seen:
            break
        seen.add(pid)
        snapshot_row = snapshot.get(pid)
        if snapshot_row is None:
            gaps.append({"pid": pid, "reason": "missing_from_snapshot"})
            break
        parent_pid, name = snapshot_row
        process = api.kernel32.OpenProcess(
            api.PROCESS_QUERY_LIMITED_INFORMATION | api.SYNCHRONIZE,
            False,
            pid,
        )
        handle = ctypes.cast(process, ctypes.c_void_p).value
        if not handle:
            gaps.append(
                {
                    "pid": pid,
                    "name": name,
                    "reason": f"OpenProcess_winerror_{ctypes.get_last_error()}",
                }
            )
            if depth == 0:
                raise CoverageUnavailable("current process diagnostic inaccessible")
            break
        lease.retain(f"diagnostic-process:{depth}:{pid}", int(handle))
        start = api.require_running(int(handle))
        capacity = wintypes.DWORD(32768)
        image = ctypes.create_unicode_buffer(capacity.value)
        if not api.kernel32.QueryFullProcessImageNameW(
            wintypes.HANDLE(handle), 0, image, ctypes.byref(capacity)
        ):
            gaps.append(
                {
                    "pid": pid,
                    "name": name,
                    "reason": f"QueryFullProcessImageNameW_winerror_{ctypes.get_last_error()}",
                }
            )
            if depth == 0:
                raise CoverageUnavailable("current executable diagnostic unavailable")
            break
        executable = api.open_full_readonly(Path(image.value), directory=False)
        lease.retain(f"diagnostic-executable:{depth}:{pid}", executable)
        executable_identity = api.identity(executable)
        _require_identity(
            executable_identity,
            directory=False,
            label=f"diagnostic executable {pid}",
        )
        size, sha256 = api.hash_file(executable)
        api.require_running(int(handle), expected_start=start)
        rows.append(
            {
                "depth": depth,
                "pid": pid,
                "parent_pid": parent_pid,
                "normalized_snapshot_name": name,
                "start_token": start,
                "liveness": "WAIT_TIMEOUT_RUNNING_AND_START_UNCHANGED",
                "executable_identity": asdict(executable_identity),
                "executable_size_bytes": size,
                "executable_sha256": sha256,
            }
        )
        pid = parent_pid
    return {
        "evidence_class": "diagnostic_current_ancestry_only",
        "production_eligible": False,
        "inventory_exhaustive": False,
        "writer_exclusion_claimed": False,
        "snapshot_row_count": len(snapshot),
        "observed_rows": rows,
        "coverage_gaps": gaps,
    }


def _validate_final(
    api: _Api,
    lease: NativeHandleLeaseV31,
    directory_identities: dict[str, HandleIdentity],
    file_rows: Sequence[FileObservation],
) -> None:
    for label, expected in directory_identities.items():
        observed = api.identity(lease.handle(label))
        _require_identity(observed, directory=True, label=label)
        if observed != expected:
            raise NativeV31Error(f"{label} identity changed before record seal")
    for row in file_rows:
        label = f"{row.kind}:{row.ordinal}"
        handle = lease.handle(label)
        identity = api.identity(handle)
        _require_identity(
            identity, directory=False, label=label, single_link=True
        )
        if identity != row.identity:
            raise NativeV31Error(f"{label} identity changed before record seal")
        size, sha256 = api.hash_file(handle)
        if (size, sha256) != (row.size_bytes, row.sha256):
            raise NativeV31Error(f"{label} bytes changed before record seal")


def collect_test_only_temp_root(
    *,
    test_root: Path,
    workspace_token: str,
    model_token: str,
    target_tokens: Sequence[str],
    sentinel_tokens: Sequence[str],
) -> tuple[dict[str, Any], NativeHandleLeaseV31]:
    """Measure only one disposable NTFS fixture and return retained handles."""
    root = verify_safe_test_root(test_root)
    if len(target_tokens) != TARGET_COUNT or len(sentinel_tokens) != SENTINEL_COUNT:
        raise NativeV31Error("fixture requires exactly 13 targets and 3 sentinels")
    if len(set(target_tokens) | set(sentinel_tokens)) != 16:
        raise NativeV31Error("fixture tokens must be distinct")
    workspace_parts = _safe_parts(workspace_token)
    model_parts = _safe_parts(model_token)
    if len(workspace_parts) != 1 or len(model_parts) != 1:
        raise NativeV31Error("workspace/model tokens must each be one component")
    all_tokens = [*target_tokens, *sentinel_tokens]
    token_parts = {token: _safe_parts(token) for token in all_tokens}
    if any(len(parts) < 2 for parts in token_parts.values()):
        raise NativeV31Error("file token requires parent plus leaf in V3.1 fixture")

    api = _Api()
    lease = NativeHandleLeaseV31(api)
    started_wall = datetime.now(timezone.utc)
    started_mono = time.monotonic_ns()
    try:
        volume = _volume_facts(api, root)
        platform = _native_platform_facts(api)
        boot = _boot_facts(api)
        volume_handle = api.open_full_readonly(
            Path(volume["volume_guid"]), directory=True
        )
        lease.retain("volume-root", volume_handle)
        volume_identity = api.identity(volume_handle)
        _require_identity(volume_identity, directory=True, label="volume-root")

        root_handle = api.open_full_readonly(root, directory=True)
        lease.retain("test-root", root_handle)
        root_identity = api.identity(root_handle)
        _require_identity(root_identity, directory=True, label="test-root")

        workspace_handle = api.open_relative_readonly(
            root_handle,
            workspace_parts[0],
            directory=True,
            share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
        )
        lease.retain("workspace", workspace_handle)
        workspace_identity = api.identity(workspace_handle)
        _require_identity(workspace_identity, directory=True, label="workspace")

        model_handle = api.open_relative_readonly(
            workspace_handle,
            model_parts[0],
            directory=True,
            share=api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE,
        )
        lease.retain("model", model_handle)
        model_identity = api.identity(model_handle)
        _require_identity(model_identity, directory=True, label="model")

        parent_tokens = sorted(
            {
                "/".join(parts[:-1])
                for parts in token_parts.values()
            }
        )
        parent_handles: dict[str, int] = {}
        parent_identities: dict[str, HandleIdentity] = {}
        for parent_token in parent_tokens:
            current_handle = model_handle
            accumulated = []
            for part in _safe_parts(parent_token):
                accumulated.append(part)
                key = "/".join(accumulated)
                if key in parent_handles:
                    current_handle = parent_handles[key]
                    continue
                handle = api.open_relative_readonly(
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
                _require_identity(
                    identity, directory=True, label=f"parent:{key}"
                )
                parent_handles[key] = handle
                parent_identities[key] = identity
                current_handle = handle
        parent_keys = {
            (row.volume_serial, row.file_id) for row in parent_identities.values()
        }
        if len(parent_keys) != len(parent_identities):
            raise NativeV31Error("parent identity alias")

        file_rows: list[FileObservation] = []
        file_keys = set()
        sentinel_set = set(sentinel_tokens)
        for token in all_tokens:
            parts = token_parts[token]
            parent_token = "/".join(parts[:-1])
            leaf = parts[-1]
            kind = "sentinel" if token in sentinel_set else "target"
            ordinal = (
                sentinel_tokens.index(token) + 1
                if kind == "sentinel"
                else target_tokens.index(token) + 1
            )
            share = api.FILE_SHARE_READ if kind == "sentinel" else 0
            handle = api.open_relative_readonly(
                parent_handles[parent_token],
                leaf,
                directory=False,
                share=share,
            )
            lease.retain(f"{kind}:{ordinal}", handle)
            identity = api.identity(handle)
            _require_identity(
                identity,
                directory=False,
                label=f"{kind}:{ordinal}",
                single_link=True,
            )
            key = (identity.volume_serial, identity.file_id)
            if key in file_keys:
                raise NativeV31Error("file identity alias")
            file_keys.add(key)
            size, sha256 = api.hash_file(handle)
            row = FileObservation(
                ordinal=ordinal,
                kind=kind,
                token=token.replace("\\", "/"),
                parent_token=parent_token,
                leaf=leaf,
                parent_identity=parent_identities[parent_token],
                identity=identity,
                size_bytes=size,
                sha256=sha256,
                observed_wall_utc=_iso(datetime.now(timezone.utc)),
                observed_monotonic_ns=time.monotonic_ns(),
                open_policy=(
                    "read_handle_share_read_only"
                    if kind == "sentinel"
                    else "read_handle_exclusive_share_zero"
                ),
            )
            file_rows.append(row)
            lease.register_resource(
                kind=kind,
                ordinal=ordinal,
                parent_label=f"parent:{parent_token}",
                leaf=leaf,
            )

        process = _diagnostic_process_evidence(api, lease)
        directory_identities = {
            "volume-root": volume_identity,
            "test-root": root_identity,
            "workspace": workspace_identity,
            "model": model_identity,
            **{
                f"parent:{key}": value
                for key, value in parent_identities.items()
            },
        }
        _validate_final(api, lease, directory_identities, file_rows)
        ended_wall = datetime.now(timezone.utc)
        ended_mono = time.monotonic_ns()
        duration = (ended_mono - started_mono) / 1_000_000_000
        if duration < 0 or duration > MAX_CAPTURE_SECONDS:
            raise NativeV31Error("capture exceeded bounded duration")

        targets = [asdict(row) for row in file_rows if row.kind == "target"]
        sentinels = [
            asdict(row) for row in file_rows if row.kind == "sentinel"
        ]
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "provenance": {
                "backend_id": BACKEND_ID,
                "adapter_class": ADAPTER_CLASS,
                "test_only": True,
                "production_eligible": False,
                "canonical_or_global_scope": False,
                "effect_authorized": False,
                "provider_injection_available": False,
                "production_collector_present": False,
                "owner_capability_present": False,
            },
            "safe_test_root": os.fspath(root),
            "capture": {
                "start_wall_utc": _iso(started_wall),
                "end_wall_utc": _iso(ended_wall),
                "start_monotonic_ns": started_mono,
                "end_monotonic_ns": ended_mono,
                "duration_seconds": duration,
                "final_handle_validation_before_record_seal": True,
            },
            "boot": boot,
            "platform": platform,
            "volume": {
                **volume,
                "volume_root_identity": asdict(volume_identity),
            },
            "retained_directories": {
                label: asdict(identity)
                for label, identity in directory_identities.items()
            },
            "targets": targets,
            "sentinels": sentinels,
            "process_evidence": process,
            "lease": {
                "opaque_nonserializable": True,
                "lease_nonce_sha256": lease.nonce_sha256(),
                "contention_probe_selector": (
                    "issued_opaque_resource_token_only_no_path_argument"
                ),
            },
            "access_effects": {
                "collector_read_handle_opens": True,
                "collector_write_access_requests": 0,
                "collector_delete_access_requests": 0,
                "contention_probe_is_separate_test_only_access_request": True,
                "contention_probe_performs_write_or_delete": False,
                "arbitrary_caller_path_write_delete_api_present": False,
            },
            "content_effects": {
                "target_bytes_initial_final_equal": True,
                "sentinel_bytes_initial_final_equal": True,
                "directory_member_delta": (
                    "coverage_unavailable_no_handle_relative_directory_enumerator"
                ),
                "probe_file_created_by_collector": False,
                "delete_or_replace_attempted_by_collector": False,
            },
            "metadata_and_cloud_effects": {
                "access_time_effect": "unmeasured_may_change",
                "cloud_hydration_effect": "unmeasured_may_change",
                "zero_filesystem_effect_claimed": False,
            },
            "cleanup": {
                "helper_cleanup_authority_present": False,
                "path_recursive_cleanup_authorized": False,
                "required_disposition": (
                    "retain_fixture_for_human_inspection_until_separate_"
                    "handle_relative_cleanup_exists"
                ),
            },
            "limitations": {
                "process_inventory_complete": False,
                "process_writer_exclusion_proven": False,
                "future_preopened_hidden_kernel_sync_writers_excluded": False,
                "directory_member_zero_delta_proven_by_helper": False,
                "metadata_zero_effect_proven": False,
                "cloud_hydration_zero_effect_proven": False,
                "production_evidence": False,
                "canonical_readiness": False,
            },
        }
        record["raw_measurement_sha256"] = digest_value(record)
        return record, lease
    except BaseException:
        lease.close()
        raise
