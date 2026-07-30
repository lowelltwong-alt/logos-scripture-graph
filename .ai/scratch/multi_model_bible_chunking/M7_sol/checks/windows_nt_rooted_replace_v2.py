#!/usr/bin/env python3
"""Environment-bound Windows rooted replacement with handle verification.

This module is deliberately narrow.  On Windows/NTFS it uses a held,
non-reparse directory handle, root-relative ``NtCreateFile`` calls, and
``NtSetInformationFile(FileRenameInformationEx)`` with
``REPLACE_IF_EXISTS | POSIX_SEMANTICS``.  The source is created and retained by
handle with no write/delete sharing.  The destination is always a validated
simple basename under the held root.

The primitive prevents destination-path diversion and source-byte
substitution.  It does *not* serialize an uncooperative writer that already
has the old target open.  Such a writer can lose an update immediately before
the rename.  Callers must acknowledge that residual race and provide their
own external publication gate.  There is no power-loss or set-level atomicity
claim.
"""
from __future__ import annotations

import ctypes
import hashlib
import os
import secrets
import sys
from contextlib import AbstractContextManager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence


if sys.platform != "win32":  # pragma: no cover - this module is Windows-only.
    raise RuntimeError("windows_nt_rooted_replace_v2 requires Windows")


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll")

HANDLE = ctypes.c_void_p
ULONG = ctypes.c_ulong
USHORT = ctypes.c_ushort
NTSTATUS = ctypes.c_long
ACCESS_MASK = ctypes.c_ulong

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
DELETE = 0x00010000
SYNCHRONIZE = 0x00100000
FILE_READ_ATTRIBUTES = 0x00000080
FILE_LIST_DIRECTORY = 0x00000001

FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004

CREATE_NEW = 1
OPEN_EXISTING = 3
FILE_CREATE = 2
FILE_OPEN = 1

FILE_ATTRIBUTE_READONLY = 0x00000001
FILE_ATTRIBUTE_DIRECTORY = 0x00000010
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400

FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000

FILE_NON_DIRECTORY_FILE = 0x00000040
FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020
FILE_OPEN_REPARSE_POINT = 0x00200000

OBJ_CASE_INSENSITIVE = 0x00000040

FILE_RENAME_INFORMATION_EX = 65
FILE_RENAME_REPLACE_IF_EXISTS = 0x00000001
FILE_RENAME_POSIX_SEMANTICS = 0x00000002

FILE_DISPOSITION_INFORMATION_EX = 64
FILE_DISPOSITION_DELETE = 0x00000001
FILE_DISPOSITION_POSIX_SEMANTICS = 0x00000002

FSCTL_GET_REPARSE_POINT = 0x000900A8
MAXIMUM_REPARSE_DATA_BUFFER_SIZE = 16 * 1024

FILE_BEGIN = 0

RESIDUAL_RACE_SCOPE = (
    "An uncooperative writer that already holds the old target open with "
    "compatible sharing can write after the preimage check and lose that "
    "update when the rooted rename replaces the directory entry."
)


class RootedReplaceError(RuntimeError):
    """Base error for fail-closed rooted replacement."""


class IdentityMismatch(RootedReplaceError):
    """An expected root or entry identity did not match."""


class HashMismatch(RootedReplaceError):
    """Expected or final bytes did not match."""


class ReparsePointRejected(RootedReplaceError):
    """A root or regular-file-only sentinel was a reparse point."""


class PostReplaceVerificationError(RootedReplaceError):
    """The rename occurred but final handle/path readback failed."""


class CleanupError(RootedReplaceError):
    """A not-yet-renamed private temporary could not be removed exactly."""


class ExternalGateRequired(RootedReplaceError):
    """The caller did not acknowledge the old-target lost-update residual."""


class _UNICODE_STRING(ctypes.Structure):
    _fields_ = [
        ("Length", USHORT),
        ("MaximumLength", USHORT),
        ("Buffer", ctypes.c_wchar_p),
    ]


class _OBJECT_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Length", ULONG),
        ("RootDirectory", HANDLE),
        ("ObjectName", ctypes.POINTER(_UNICODE_STRING)),
        ("Attributes", ULONG),
        ("SecurityDescriptor", ctypes.c_void_p),
        ("SecurityQualityOfService", ctypes.c_void_p),
    ]


class _IO_STATUS_BLOCK(ctypes.Structure):
    _fields_ = [
        ("Status", ctypes.c_void_p),
        ("Information", ctypes.c_size_t),
    ]


class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
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


class _FILE_RENAME_INFORMATION_EX_BUFFER(ctypes.Structure):
    _fields_ = [
        ("Flags", ULONG),
        ("RootDirectory", HANDLE),
        ("FileNameLength", ULONG),
        ("FileName", ctypes.c_wchar * 1),
    ]


class _FILE_DISPOSITION_INFORMATION_EX(ctypes.Structure):
    _fields_ = [("Flags", ULONG)]


kernel32.CreateFileW.argtypes = [
    ctypes.c_wchar_p,
    ctypes.c_ulong,
    ctypes.c_ulong,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.c_ulong,
    HANDLE,
]
kernel32.CreateFileW.restype = HANDLE
kernel32.CloseHandle.argtypes = [HANDLE]
kernel32.CloseHandle.restype = ctypes.c_int
kernel32.GetFileInformationByHandle.argtypes = [
    HANDLE,
    ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION),
]
kernel32.GetFileInformationByHandle.restype = ctypes.c_int
kernel32.GetFileSizeEx.argtypes = [HANDLE, ctypes.POINTER(ctypes.c_longlong)]
kernel32.GetFileSizeEx.restype = ctypes.c_int
kernel32.SetFilePointerEx.argtypes = [
    HANDLE,
    ctypes.c_longlong,
    ctypes.POINTER(ctypes.c_longlong),
    ctypes.c_ulong,
]
kernel32.SetFilePointerEx.restype = ctypes.c_int
kernel32.ReadFile.argtypes = [
    HANDLE,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong),
    ctypes.c_void_p,
]
kernel32.ReadFile.restype = ctypes.c_int
kernel32.WriteFile.argtypes = [
    HANDLE,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong),
    ctypes.c_void_p,
]
kernel32.WriteFile.restype = ctypes.c_int
kernel32.SetEndOfFile.argtypes = [HANDLE]
kernel32.SetEndOfFile.restype = ctypes.c_int
kernel32.FlushFileBuffers.argtypes = [HANDLE]
kernel32.FlushFileBuffers.restype = ctypes.c_int
kernel32.DeviceIoControl.argtypes = [
    HANDLE,
    ctypes.c_ulong,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong),
    ctypes.c_void_p,
]
kernel32.DeviceIoControl.restype = ctypes.c_int

ntdll.NtCreateFile.argtypes = [
    ctypes.POINTER(HANDLE),
    ACCESS_MASK,
    ctypes.POINTER(_OBJECT_ATTRIBUTES),
    ctypes.POINTER(_IO_STATUS_BLOCK),
    ctypes.c_void_p,
    ULONG,
    ULONG,
    ULONG,
    ULONG,
    ctypes.c_void_p,
    ULONG,
]
ntdll.NtCreateFile.restype = NTSTATUS
ntdll.NtSetInformationFile.argtypes = [
    HANDLE,
    ctypes.POINTER(_IO_STATUS_BLOCK),
    ctypes.c_void_p,
    ULONG,
    ULONG,
]
ntdll.NtSetInformationFile.restype = NTSTATUS
ntdll.RtlNtStatusToDosError.argtypes = [NTSTATUS]
ntdll.RtlNtStatusToDosError.restype = ULONG


@dataclass(frozen=True)
class FileIdentity:
    volume_serial: int
    file_id: int
    attributes: int
    is_directory: bool
    is_reparse_point: bool


@dataclass(frozen=True)
class EntrySnapshot:
    identity: FileIdentity
    sha256: str
    digest_kind: str


@dataclass(frozen=True)
class RootedReplaceResult:
    root_identity: FileIdentity
    preimage_identity: FileIdentity
    published_identity: FileIdentity
    intended_sha256: str
    old_target_changed_after_preimage_check: bool
    residual_race_scope: str = RESIDUAL_RACE_SCOPE
    power_loss_atomicity_claimed: bool = False
    set_atomicity_claimed: bool = False
    uncooperative_writer_excluded: bool = False


def _winerror(label: str) -> OSError:
    return ctypes.WinError(ctypes.get_last_error(), label)


def _raise_ntstatus(status: int, label: str) -> None:
    if status < 0:
        code = int(ntdll.RtlNtStatusToDosError(status))
        raise OSError(code, f"{label}: NTSTATUS 0x{status & 0xffffffff:08x}")


def _close(handle: int | None) -> None:
    if handle not in (None, 0, INVALID_HANDLE_VALUE):
        if not kernel32.CloseHandle(HANDLE(handle)):
            raise _winerror("CloseHandle")


def _identity(handle: int) -> FileIdentity:
    info = _BY_HANDLE_FILE_INFORMATION()
    if not kernel32.GetFileInformationByHandle(
        HANDLE(handle), ctypes.byref(info)
    ):
        raise _winerror("GetFileInformationByHandle")
    attrs = int(info.dwFileAttributes)
    return FileIdentity(
        volume_serial=int(info.dwVolumeSerialNumber),
        file_id=(int(info.nFileIndexHigh) << 32) | int(info.nFileIndexLow),
        attributes=attrs,
        is_directory=bool(attrs & FILE_ATTRIBUTE_DIRECTORY),
        is_reparse_point=bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT),
    )


def _open_root(root: Path) -> int:
    absolute = os.path.abspath(os.fspath(root))
    handle = kernel32.CreateFileW(
        absolute,
        FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES | SYNCHRONIZE,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    value = ctypes.cast(handle, ctypes.c_void_p).value
    if value == INVALID_HANDLE_VALUE:
        raise _winerror(f"open destination root {absolute}")
    try:
        identity = _identity(value)
        if not identity.is_directory:
            raise RootedReplaceError("destination root is not a directory")
        if identity.is_reparse_point:
            raise ReparsePointRejected(
                "destination root is a reparse point"
            )
        return value
    except BaseException:
        _close(value)
        raise


def _validate_basename(name: str, label: str) -> str:
    if not isinstance(name, str) or not name:
        raise RootedReplaceError(f"{label} must be a nonempty string")
    if name in {".", ".."} or name[-1] in {" ", "."}:
        raise RootedReplaceError(f"{label} is not an unambiguous basename")
    forbidden = set('<>:"/\\|?*')
    if any(ord(char) < 32 or char in forbidden for char in name):
        raise RootedReplaceError(f"{label} is not an unambiguous basename")
    stem = name.split(".", 1)[0].rstrip(" .").upper()
    if stem in {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }:
        raise RootedReplaceError(f"{label} is a reserved DOS basename")
    if len(name.encode("utf-16-le")) > 510:
        raise RootedReplaceError(f"{label} exceeds one NT path component")
    return name


def _relative_object_attributes(
    root_handle: int,
    basename: str,
) -> tuple[_OBJECT_ATTRIBUTES, _UNICODE_STRING, ctypes.Array]:
    buffer = ctypes.create_unicode_buffer(basename)
    encoded_length = len(basename.encode("utf-16-le"))
    unicode_name = _UNICODE_STRING(
        Length=encoded_length,
        MaximumLength=encoded_length + 2,
        Buffer=ctypes.cast(buffer, ctypes.c_wchar_p),
    )
    attributes = _OBJECT_ATTRIBUTES(
        Length=ctypes.sizeof(_OBJECT_ATTRIBUTES),
        RootDirectory=HANDLE(root_handle),
        ObjectName=ctypes.pointer(unicode_name),
        Attributes=OBJ_CASE_INSENSITIVE,
        SecurityDescriptor=None,
        SecurityQualityOfService=None,
    )
    return attributes, unicode_name, buffer


def _nt_open_relative(
    root_handle: int,
    basename: str,
    *,
    desired_access: int,
    share_access: int,
    disposition: int,
    file_attributes: int = FILE_ATTRIBUTE_NORMAL,
) -> int:
    _validate_basename(basename, "relative file name")
    attributes, unicode_name, buffer = _relative_object_attributes(
        root_handle, basename
    )
    _ = unicode_name, buffer
    io = _IO_STATUS_BLOCK()
    result = HANDLE()
    status = int(
        ntdll.NtCreateFile(
            ctypes.byref(result),
            ACCESS_MASK(desired_access),
            ctypes.byref(attributes),
            ctypes.byref(io),
            None,
            ULONG(file_attributes),
            ULONG(share_access),
            ULONG(disposition),
            ULONG(
                FILE_NON_DIRECTORY_FILE
                | FILE_SYNCHRONOUS_IO_NONALERT
                | FILE_OPEN_REPARSE_POINT
            ),
            None,
            ULONG(0),
        )
    )
    _raise_ntstatus(status, f"NtCreateFile({basename})")
    value = ctypes.cast(result, ctypes.c_void_p).value
    if value in (None, INVALID_HANDLE_VALUE):
        raise RootedReplaceError("NtCreateFile returned an invalid handle")
    return value


def _seek(handle: int, offset: int = 0) -> None:
    if not kernel32.SetFilePointerEx(
        HANDLE(handle), ctypes.c_longlong(offset), None, FILE_BEGIN
    ):
        raise _winerror("SetFilePointerEx")


def _read_regular_handle(handle: int) -> bytes:
    size = ctypes.c_longlong()
    if not kernel32.GetFileSizeEx(HANDLE(handle), ctypes.byref(size)):
        raise _winerror("GetFileSizeEx")
    if size.value < 0:
        raise RootedReplaceError("negative file size")
    _seek(handle)
    remaining = size.value
    chunks: list[bytes] = []
    while remaining:
        requested = min(remaining, 1024 * 1024)
        buffer = ctypes.create_string_buffer(requested)
        count = ctypes.c_ulong()
        if not kernel32.ReadFile(
            HANDLE(handle),
            buffer,
            requested,
            ctypes.byref(count),
            None,
        ):
            raise _winerror("ReadFile")
        if count.value == 0:
            raise RootedReplaceError("short handle read")
        chunks.append(buffer.raw[: count.value])
        remaining -= count.value
    return b"".join(chunks)


def _read_reparse_handle(handle: int) -> bytes:
    buffer = ctypes.create_string_buffer(MAXIMUM_REPARSE_DATA_BUFFER_SIZE)
    count = ctypes.c_ulong()
    if not kernel32.DeviceIoControl(
        HANDLE(handle),
        FSCTL_GET_REPARSE_POINT,
        None,
        0,
        buffer,
        len(buffer),
        ctypes.byref(count),
        None,
    ):
        raise _winerror("FSCTL_GET_REPARSE_POINT")
    return buffer.raw[: count.value]


def _snapshot_handle(handle: int) -> EntrySnapshot:
    identity = _identity(handle)
    if identity.is_directory:
        raise RootedReplaceError("file entry unexpectedly names a directory")
    if identity.is_reparse_point:
        data = _read_reparse_handle(handle)
        kind = "reparse_buffer"
    else:
        data = _read_regular_handle(handle)
        kind = "file_bytes"
    return EntrySnapshot(
        identity=identity,
        sha256=hashlib.sha256(data).hexdigest(),
        digest_kind=kind,
    )


def _write_handle_exact(handle: int, data: bytes) -> None:
    _seek(handle)
    view = memoryview(data)
    offset = 0
    while offset < len(view):
        part = view[offset : offset + 1024 * 1024]
        buffer = ctypes.create_string_buffer(part.tobytes())
        count = ctypes.c_ulong()
        if not kernel32.WriteFile(
            HANDLE(handle),
            buffer,
            len(part),
            ctypes.byref(count),
            None,
        ):
            raise _winerror("WriteFile")
        if count.value != len(part):
            raise RootedReplaceError("short handle write")
        offset += count.value
    if not kernel32.SetEndOfFile(HANDLE(handle)):
        raise _winerror("SetEndOfFile")
    if not kernel32.FlushFileBuffers(HANDLE(handle)):
        raise _winerror("FlushFileBuffers")


def _nt_rename_relative(
    source_handle: int,
    root_handle: int,
    target_basename: str,
) -> None:
    encoded = target_basename.encode("utf-16-le")
    offset = _FILE_RENAME_INFORMATION_EX_BUFFER.FileName.offset
    storage = ctypes.create_string_buffer(offset + len(encoded))
    info = _FILE_RENAME_INFORMATION_EX_BUFFER.from_buffer(storage)
    info.Flags = (
        FILE_RENAME_REPLACE_IF_EXISTS | FILE_RENAME_POSIX_SEMANTICS
    )
    info.RootDirectory = HANDLE(root_handle)
    info.FileNameLength = len(encoded)
    ctypes.memmove(ctypes.addressof(storage) + offset, encoded, len(encoded))
    io = _IO_STATUS_BLOCK()
    status = int(
        ntdll.NtSetInformationFile(
            HANDLE(source_handle),
            ctypes.byref(io),
            storage,
            ULONG(len(storage)),
            ULONG(FILE_RENAME_INFORMATION_EX),
        )
    )
    _raise_ntstatus(status, "NtSetInformationFile(FileRenameInformationEx)")


def _mark_delete_on_close(handle: int) -> None:
    info = _FILE_DISPOSITION_INFORMATION_EX(
        Flags=(
            FILE_DISPOSITION_DELETE | FILE_DISPOSITION_POSIX_SEMANTICS
        )
    )
    io = _IO_STATUS_BLOCK()
    status = int(
        ntdll.NtSetInformationFile(
            HANDLE(handle),
            ctypes.byref(io),
            ctypes.byref(info),
            ULONG(ctypes.sizeof(info)),
            ULONG(FILE_DISPOSITION_INFORMATION_EX),
        )
    )
    _raise_ntstatus(
        status, "NtSetInformationFile(FileDispositionInformationEx)"
    )


def inspect_root_identity(root: Path) -> FileIdentity:
    """Return the identity of a non-reparse directory root."""
    handle = _open_root(root)
    try:
        return _identity(handle)
    finally:
        _close(handle)


def inspect_rooted_entry(root: Path, basename: str) -> EntrySnapshot:
    """Inspect a root-relative entry without traversing its final reparse tag."""
    name = _validate_basename(basename, "target basename")
    root_handle = _open_root(root)
    entry_handle: int | None = None
    try:
        entry_handle = _nt_open_relative(
            root_handle,
            name,
            desired_access=GENERIC_READ | FILE_READ_ATTRIBUTES | SYNCHRONIZE,
            share_access=(
                FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE
            ),
            disposition=FILE_OPEN,
        )
        return _snapshot_handle(entry_handle)
    finally:
        _close(entry_handle)
        _close(root_handle)


class _TestHookAccess:
    """Narrow fault-injection access used only by the exact test matrix."""

    def __init__(self, source_handle: int, old_target_handle: int):
        self._source_handle = source_handle
        self._old_target_handle = old_target_handle

    def overwrite_published_source(self, data: bytes) -> None:
        _write_handle_exact(self._source_handle, data)

    def old_target_snapshot(self) -> EntrySnapshot:
        return _snapshot_handle(self._old_target_handle)


TestHook = Callable[[str, _TestHookAccess], None]


def rooted_replace_bytes(
    *,
    root: Path,
    target_basename: str,
    intended_bytes: bytes,
    expected_intended_sha256: str,
    expected_root_identity: FileIdentity,
    expected_preimage: EntrySnapshot,
    acknowledge_residual_race: bool,
    _temp_basename: str | None = None,
    _test_hook: TestHook | None = None,
) -> RootedReplaceResult:
    """Replace one existing rooted entry and verify handle/path convergence.

    ``acknowledge_residual_race`` is mandatory because this primitive does not
    exclude a compatible writer that already holds the old target open.
    ``_temp_basename`` and ``_test_hook`` are private deterministic test seams.
    """
    if not acknowledge_residual_race:
        raise ExternalGateRequired(RESIDUAL_RACE_SCOPE)
    target = _validate_basename(target_basename, "target basename")
    intended = bytes(intended_bytes)
    intended_sha = hashlib.sha256(intended).hexdigest()
    if intended_sha != expected_intended_sha256:
        raise HashMismatch("intended bytes do not match their expected hash")
    if not isinstance(expected_root_identity, FileIdentity):
        raise IdentityMismatch("expected root identity is required")
    if not isinstance(expected_preimage, EntrySnapshot):
        raise IdentityMismatch("expected preimage identity/hash is required")

    temporary = _validate_basename(
        _temp_basename
        or (
            f".{target}.{os.getpid()}.{secrets.token_hex(16)}"
            ".rooted-replace.tmp"
        ),
        "temporary basename",
    )
    if temporary.casefold() == target.casefold():
        raise RootedReplaceError(
            "temporary basename aliases the target basename"
        )

    root_handle: int | None = None
    source_handle: int | None = None
    old_target_handle: int | None = None
    final_path_handle: int | None = None
    renamed = False
    original_error: BaseException | None = None
    try:
        root_handle = _open_root(root)
        root_identity = _identity(root_handle)
        if root_identity != expected_root_identity:
            raise IdentityMismatch("destination root identity mismatch")

        source_handle = _nt_open_relative(
            root_handle,
            temporary,
            desired_access=(
                GENERIC_READ
                | GENERIC_WRITE
                | DELETE
                | FILE_READ_ATTRIBUTES
                | SYNCHRONIZE
            ),
            share_access=FILE_SHARE_READ,
            disposition=FILE_CREATE,
        )
        source_identity_before = _identity(source_handle)
        if source_identity_before.is_reparse_point:
            raise ReparsePointRejected(
                "new private source unexpectedly became a reparse point"
            )
        _write_handle_exact(source_handle, intended)
        source_before = _snapshot_handle(source_handle)
        if (
            source_before.sha256 != intended_sha
            or source_before.digest_kind != "file_bytes"
        ):
            raise HashMismatch("private source handle readback mismatch")

        old_target_handle = _nt_open_relative(
            root_handle,
            target,
            desired_access=(
                GENERIC_READ | FILE_READ_ATTRIBUTES | SYNCHRONIZE
            ),
            share_access=(
                FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE
            ),
            disposition=FILE_OPEN,
        )
        immediate_preimage = _snapshot_handle(old_target_handle)
        if immediate_preimage != expected_preimage:
            raise IdentityMismatch(
                "immediate root-relative target preimage mismatch"
            )

        access = _TestHookAccess(source_handle, old_target_handle)
        if _test_hook is not None:
            _test_hook("immediately_before_rename", access)
        _nt_rename_relative(source_handle, root_handle, target)
        renamed = True
        if _test_hook is not None:
            _test_hook("after_rename_before_readback", access)

        source_after = _snapshot_handle(source_handle)
        if (
            source_after.identity != source_before.identity
            or source_after.sha256 != intended_sha
            or source_after.digest_kind != "file_bytes"
        ):
            raise PostReplaceVerificationError(
                "published source-handle readback mismatch"
            )

        final_path_handle = _nt_open_relative(
            root_handle,
            target,
            desired_access=(
                GENERIC_READ | FILE_READ_ATTRIBUTES | SYNCHRONIZE
            ),
            share_access=(
                FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE
            ),
            disposition=FILE_OPEN,
        )
        final_path = _snapshot_handle(final_path_handle)
        if (
            final_path.identity != source_after.identity
            or final_path.sha256 != intended_sha
            or final_path.digest_kind != "file_bytes"
        ):
            raise PostReplaceVerificationError(
                "root-relative path and source handle did not converge"
            )
        old_target_after = _snapshot_handle(old_target_handle)
        old_changed = old_target_after != immediate_preimage
        if _identity(root_handle) != root_identity:
            raise PostReplaceVerificationError(
                "held destination root identity changed"
            )
        return RootedReplaceResult(
            root_identity=root_identity,
            preimage_identity=immediate_preimage.identity,
            published_identity=source_after.identity,
            intended_sha256=intended_sha,
            old_target_changed_after_preimage_check=old_changed,
        )
    except BaseException as exc:
        original_error = exc
        raise
    finally:
        cleanup_error: BaseException | None = None
        if source_handle is not None and not renamed:
            try:
                _mark_delete_on_close(source_handle)
            except BaseException as exc:
                cleanup_error = exc
        for handle in (
            final_path_handle,
            old_target_handle,
            source_handle,
            root_handle,
        ):
            try:
                _close(handle)
            except BaseException as exc:
                if cleanup_error is None:
                    cleanup_error = exc
        if cleanup_error is not None and original_error is None:
            raise CleanupError(
                "private temporary cleanup could not be verified"
            ) from cleanup_error
        if cleanup_error is not None and original_error is not None:
            raise CleanupError(
                "operation failed and private temporary cleanup also failed"
            ) from cleanup_error


class SentinelHandleGuard(AbstractContextManager["SentinelHandleGuard"]):
    """Hold exactly three regular sentinels while denying write/delete opens."""

    def __init__(
        self,
        paths: Sequence[Path],
        expected_sha256: Mapping[Path, str] | None = None,
    ):
        if len(paths) != 3:
            raise RootedReplaceError(
                "sentinel guard requires exactly three files"
            )
        normalized = [Path(os.path.abspath(os.fspath(path))) for path in paths]
        if len({os.path.normcase(os.fspath(path)) for path in normalized}) != 3:
            raise RootedReplaceError("sentinel paths must be distinct")
        self._paths = normalized
        self._expected = {
            Path(os.path.abspath(os.fspath(path))): digest
            for path, digest in (expected_sha256 or {}).items()
        }
        self._handles: list[tuple[Path, int, EntrySnapshot]] = []

    def __enter__(self) -> "SentinelHandleGuard":
        try:
            for path in self._paths:
                handle = kernel32.CreateFileW(
                    os.fspath(path),
                    GENERIC_READ | FILE_READ_ATTRIBUTES | SYNCHRONIZE,
                    FILE_SHARE_READ,
                    None,
                    OPEN_EXISTING,
                    FILE_FLAG_OPEN_REPARSE_POINT,
                    None,
                )
                value = ctypes.cast(handle, ctypes.c_void_p).value
                if value == INVALID_HANDLE_VALUE:
                    raise _winerror(f"open sentinel {path}")
                snapshot = _snapshot_handle(value)
                if snapshot.identity.is_reparse_point:
                    _close(value)
                    raise ReparsePointRejected(
                        f"sentinel is a reparse point: {path}"
                    )
                expected = self._expected.get(path)
                if expected is not None and snapshot.sha256 != expected:
                    _close(value)
                    raise HashMismatch(f"sentinel hash mismatch: {path}")
                self._handles.append((path, value, snapshot))
            self.verify()
            return self
        except BaseException:
            self._close_all()
            raise

    def verify(self) -> None:
        """Hash-verify all three held file identities through their handles."""
        if len(self._handles) != 3:
            raise RootedReplaceError("sentinel guard is not fully entered")
        for path, handle, initial in self._handles:
            current = _snapshot_handle(handle)
            if current != initial:
                raise HashMismatch(f"held sentinel changed: {path}")

    def _close_all(self) -> None:
        first: BaseException | None = None
        for _, handle, _ in reversed(self._handles):
            try:
                _close(handle)
            except BaseException as exc:
                if first is None:
                    first = exc
        self._handles.clear()
        if first is not None:
            raise first

    def __exit__(self, exc_type, exc, traceback) -> bool:
        verification_error: BaseException | None = None
        try:
            self.verify()
        except BaseException as caught:
            verification_error = caught
        self._close_all()
        if verification_error is not None:
            raise verification_error
        return False


def sentinel_handle_guard(
    paths: Sequence[Path],
    expected_sha256: Mapping[Path, str] | None = None,
) -> SentinelHandleGuard:
    """Construct the exact three-file sentinel guard."""
    return SentinelHandleGuard(paths, expected_sha256)

