#!/usr/bin/env python3
"""NT-native handle-relative replacement for one existing Windows file.

This is an environment-bound experiment for the T550 Hosea publication
transaction.  It calls ``NtSetInformationFile`` with
``FileRenameInformationEx`` and these documented flags:

* ``FILE_RENAME_REPLACE_IF_EXISTS``; and
* ``FILE_RENAME_POSIX_SEMANTICS``.

The POSIX flag is material: Microsoft documents that it permits replacement
while handles to the old target remain open.  Consequently this module keeps a
read-only/no-delete target handle held through the namespace transition,
instead of introducing a check/close/rename substitution window.

The primitive proves one atomic filesystem namespace transition only.  It does
not claim power-loss durability or multi-file/set atomicity.  It fails closed
unless all directory, target, temporary, and post-rename identity/hash checks
hold on the current Windows filesystem.
"""
from __future__ import annotations

import ctypes
import hashlib
import os
import secrets
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Callable, Iterator


class WindowsNtReplaceError(RuntimeError):
    """A required NT handle-relative replacement invariant failed."""


class UnsupportedPlatformError(WindowsNtReplaceError):
    """The Windows-only primitive was called on another platform."""


class ReparsePointError(WindowsNtReplaceError):
    """A protected path is a reparse point."""


class IdentityMismatchError(WindowsNtReplaceError):
    """A protected pathname no longer identifies its held object."""


class HashMismatchError(WindowsNtReplaceError):
    """Bytes read from a held handle do not match the required digest."""


class NtSetInformationFileError(OSError):
    """``NtSetInformationFile`` failed, preserving both status namespaces."""

    def __init__(self, ntstatus: int, winerror: int) -> None:
        self.ntstatus = ntstatus & 0xFFFFFFFF
        self.winerror = winerror
        super().__init__(
            winerror,
            "NtSetInformationFile(FileRenameInformationEx) failed: "
            f"NTSTATUS=0x{self.ntstatus:08X}; "
            f"Win32={winerror} ({ctypes.FormatError(winerror).strip()})",
        )


@dataclass(frozen=True)
class FileIdentity:
    volume_serial_number: int
    file_index: int


@dataclass(frozen=True)
class ReplacementReceipt:
    destination: Path
    sha256: str
    byte_count: int
    directory_identity: FileIdentity
    file_identity: FileIdentity
    nt_information_class: int = 65
    nt_rename_flags: int = 0x00000003
    protection_claim: str = (
        "one_nt_namespace_transition_with_held_handles;"
        "not_power_loss_or_set_atomicity"
    )


_IS_WINDOWS = os.name == "nt" and sys.platform.startswith("win")

if _IS_WINDOWS:
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _ntdll = ctypes.WinDLL("ntdll", use_last_error=False)

    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    _GENERIC_READ = 0x80000000
    _GENERIC_WRITE = 0x40000000
    _DELETE = 0x00010000
    _FILE_TRAVERSE = 0x00000020
    _FILE_READ_ATTRIBUTES = 0x00000080
    _SYNCHRONIZE = 0x00100000
    _FILE_SHARE_READ = 0x00000001
    _FILE_SHARE_WRITE = 0x00000002
    _OPEN_EXISTING = 3
    _CREATE_NEW = 1
    _FILE_ATTRIBUTE_NORMAL = 0x00000080
    _FILE_ATTRIBUTE_TEMPORARY = 0x00000100
    _FILE_ATTRIBUTE_DIRECTORY = 0x00000010
    _FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
    _FILE_FLAG_WRITE_THROUGH = 0x80000000
    _FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    _FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
    _FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
    _FILE_RENAME_INFORMATION_EX = 65
    _FILE_RENAME_REPLACE_IF_EXISTS = 0x00000001
    _FILE_RENAME_POSIX_SEMANTICS = 0x00000002

    class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("dwFileAttributes", wintypes.DWORD),
            ("ftCreationTime", wintypes.FILETIME),
            ("ftLastAccessTime", wintypes.FILETIME),
            ("ftLastWriteTime", wintypes.FILETIME),
            ("dwVolumeSerialNumber", wintypes.DWORD),
            ("nFileSizeHigh", wintypes.DWORD),
            ("nFileSizeLow", wintypes.DWORD),
            ("nNumberOfLinks", wintypes.DWORD),
            ("nFileIndexHigh", wintypes.DWORD),
            ("nFileIndexLow", wintypes.DWORD),
        ]

    class _IO_STATUS_BLOCK(ctypes.Structure):
        _fields_ = [
            ("StatusOrPointer", ctypes.c_void_p),
            ("Information", ctypes.c_size_t),
        ]

    class _FILE_RENAME_INFORMATION_EX_HEADER(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.ULONG),
            ("RootDirectory", wintypes.HANDLE),
            ("FileNameLength", wintypes.ULONG),
            ("FileName", wintypes.WCHAR * 1),
        ]

    _kernel32.CreateFileW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    _kernel32.CreateFileW.restype = wintypes.HANDLE
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.GetFileInformationByHandle.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION),
    ]
    _kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
    _kernel32.GetFinalPathNameByHandleW.argtypes = [
        wintypes.HANDLE,
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
    ]
    _kernel32.GetFinalPathNameByHandleW.restype = wintypes.DWORD
    _kernel32.GetFileSizeEx.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_longlong),
    ]
    _kernel32.GetFileSizeEx.restype = wintypes.BOOL
    _kernel32.SetFilePointerEx.argtypes = [
        wintypes.HANDLE,
        ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_longlong),
        wintypes.DWORD,
    ]
    _kernel32.SetFilePointerEx.restype = wintypes.BOOL
    _kernel32.ReadFile.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.c_void_p,
    ]
    _kernel32.ReadFile.restype = wintypes.BOOL
    _kernel32.WriteFile.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.c_void_p,
    ]
    _kernel32.WriteFile.restype = wintypes.BOOL
    _kernel32.FlushFileBuffers.argtypes = [wintypes.HANDLE]
    _kernel32.FlushFileBuffers.restype = wintypes.BOOL

    _ntdll.NtSetInformationFile.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_IO_STATUS_BLOCK),
        ctypes.c_void_p,
        wintypes.ULONG,
        ctypes.c_int,
    ]
    _ntdll.NtSetInformationFile.restype = ctypes.c_long
    _ntdll.RtlNtStatusToDosError.argtypes = [ctypes.c_long]
    _ntdll.RtlNtStatusToDosError.restype = wintypes.ULONG


def _require_windows() -> None:
    if not _IS_WINDOWS:
        raise UnsupportedPlatformError(
            "NT handle-bound replacement is unavailable off Windows"
        )


def _win_error(operation: str, path: Path | None = None) -> OSError:
    code = ctypes.get_last_error()
    suffix = f" for {path}" if path is not None else ""
    return OSError(code, f"{operation} failed{suffix}: {ctypes.FormatError(code)}")


def _close(handle: int | None) -> None:
    if handle is None or handle == _INVALID_HANDLE_VALUE:
        return
    if not _kernel32.CloseHandle(handle):
        raise _win_error("CloseHandle")


def _create_file(
    path: Path,
    *,
    access: int,
    share: int,
    disposition: int,
    flags: int,
) -> int:
    handle = _kernel32.CreateFileW(
        str(path), access, share, None, disposition, flags, None
    )
    if handle == _INVALID_HANDLE_VALUE:
        raise _win_error("CreateFileW", path)
    return handle


def _checked_drive_path(path: Path) -> Path:
    raw = str(path)
    if "\x00" in raw:
        raise WindowsNtReplaceError("NUL is forbidden in a path")
    if any(part == ".." for part in PureWindowsPath(raw).parts):
        raise WindowsNtReplaceError("parent traversal is forbidden")
    absolute = Path(os.path.abspath(raw))
    pure = PureWindowsPath(str(absolute))
    if not pure.drive or not pure.root or str(absolute).startswith("\\\\"):
        raise WindowsNtReplaceError("only absolute local-drive paths are supported")
    return absolute


def _strip_extended_prefix(value: str) -> str:
    if value.startswith("\\\\?\\UNC\\"):
        return "\\\\" + value[8:]
    if value.startswith("\\\\?\\"):
        return value[4:]
    return value


def _normalized(path: Path | str) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(str(path))))


def _final_path(handle: int) -> Path:
    capacity = 512
    while True:
        buffer = ctypes.create_unicode_buffer(capacity)
        length = _kernel32.GetFinalPathNameByHandleW(handle, buffer, capacity, 0)
        if not length:
            raise _win_error("GetFinalPathNameByHandleW")
        if length < capacity:
            return Path(_strip_extended_prefix(buffer.value))
        capacity = int(length) + 1


def _validate_final_path(handle: int, expected: Path) -> None:
    actual = _final_path(handle)
    if _normalized(actual) != _normalized(expected):
        raise IdentityMismatchError(
            f"held handle path mismatch: {actual} != {expected}"
        )


def _handle_information(handle: int) -> tuple[FileIdentity, int, int]:
    info = _BY_HANDLE_FILE_INFORMATION()
    if not _kernel32.GetFileInformationByHandle(handle, ctypes.byref(info)):
        raise _win_error("GetFileInformationByHandle")
    identity = FileIdentity(
        int(info.dwVolumeSerialNumber),
        (int(info.nFileIndexHigh) << 32) | int(info.nFileIndexLow),
    )
    size = (int(info.nFileSizeHigh) << 32) | int(info.nFileSizeLow)
    return identity, int(info.dwFileAttributes), size


def _ensure_kind(handle: int, path: Path, *, directory: bool) -> FileIdentity:
    identity, attributes, _ = _handle_information(handle)
    if attributes & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise ReparsePointError(f"reparse point is forbidden: {path}")
    if bool(attributes & _FILE_ATTRIBUTE_DIRECTORY) != directory:
        expected = "directory" if directory else "regular file"
        raise WindowsNtReplaceError(f"expected {expected}: {path}")
    return identity


def _handle_bytes(handle: int) -> bytes:
    size = ctypes.c_longlong()
    if not _kernel32.GetFileSizeEx(handle, ctypes.byref(size)):
        raise _win_error("GetFileSizeEx")
    if not _kernel32.SetFilePointerEx(handle, 0, None, 0):
        raise _win_error("SetFilePointerEx")
    remaining = int(size.value)
    chunks: list[bytes] = []
    while remaining:
        requested = min(remaining, 1024 * 1024)
        buffer = ctypes.create_string_buffer(requested)
        read = wintypes.DWORD()
        if not _kernel32.ReadFile(
            handle, buffer, requested, ctypes.byref(read), None
        ):
            raise _win_error("ReadFile")
        if not read.value:
            raise WindowsNtReplaceError("unexpected EOF from held file")
        chunks.append(buffer.raw[: int(read.value)])
        remaining -= int(read.value)
    return b"".join(chunks)


def _write_handle_bytes(handle: int, data: bytes) -> None:
    offset = 0
    while offset < len(data):
        block = data[offset : offset + 1024 * 1024]
        buffer = ctypes.create_string_buffer(block, len(block))
        written = wintypes.DWORD()
        if not _kernel32.WriteFile(
            handle, buffer, len(block), ctypes.byref(written), None
        ):
            raise _win_error("WriteFile")
        if not written.value:
            raise WindowsNtReplaceError("zero-byte WriteFile")
        offset += int(written.value)
    if not _kernel32.FlushFileBuffers(handle):
        raise _win_error("FlushFileBuffers")


def _sha256_handle(handle: int) -> str:
    return hashlib.sha256(_handle_bytes(handle)).hexdigest()


def _directory_components(directory: Path) -> list[Path]:
    absolute = _checked_drive_path(directory)
    pure = PureWindowsPath(str(absolute))
    current = Path(pure.anchor)
    result = [current]
    for part in pure.parts[1:]:
        current = current / part
        result.append(current)
    return result


@dataclass
class _HeldDirectoryChain:
    directory: Path
    handles: list[int]
    identities: list[FileIdentity]

    @property
    def directory_handle(self) -> int:
        return self.handles[-1]

    @property
    def directory_identity(self) -> FileIdentity:
        return self.identities[-1]

    def verify(self) -> None:
        components = _directory_components(self.directory)
        if len(components) != len(self.handles):
            raise IdentityMismatchError("directory component count changed")
        for path, handle, expected in zip(
            components, self.handles, self.identities, strict=True
        ):
            if _ensure_kind(handle, path, directory=True) != expected:
                raise IdentityMismatchError(f"held directory changed: {path}")
            probe = _create_file(
                path,
                access=_FILE_TRAVERSE | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
                share=_FILE_SHARE_READ | _FILE_SHARE_WRITE,
                disposition=_OPEN_EXISTING,
                flags=_FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
            )
            try:
                if _ensure_kind(probe, path, directory=True) != expected:
                    raise IdentityMismatchError(f"directory path rebound: {path}")
            finally:
                _close(probe)


@contextmanager
def _hold_directory_chain(directory: Path) -> Iterator[_HeldDirectoryChain]:
    handles: list[int] = []
    identities: list[FileIdentity] = []
    try:
        for component in _directory_components(directory):
            handle = _create_file(
                component,
                access=_FILE_TRAVERSE | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
                share=_FILE_SHARE_READ | _FILE_SHARE_WRITE,
                disposition=_OPEN_EXISTING,
                flags=_FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
            )
            handles.append(handle)
            identities.append(_ensure_kind(handle, component, directory=True))
        held = _HeldDirectoryChain(
            _checked_drive_path(directory), handles, identities
        )
        held.verify()
        yield held
        held.verify()
    finally:
        first_error: BaseException | None = None
        for handle in reversed(handles):
            try:
                _close(handle)
            except BaseException as exc:
                first_error = first_error or exc
        if first_error is not None:
            raise first_error


def _open_regular_guard(path: Path) -> int:
    handle = _create_file(
        path,
        access=_GENERIC_READ,
        share=_FILE_SHARE_READ,
        disposition=_OPEN_EXISTING,
        flags=_FILE_FLAG_OPEN_REPARSE_POINT | _FILE_FLAG_SEQUENTIAL_SCAN,
    )
    try:
        _ensure_kind(handle, path, directory=False)
        _validate_final_path(handle, path)
        return handle
    except BaseException:
        _close(handle)
        raise


def _nt_rename_relative_ex(
    source_handle: int,
    destination_directory_handle: int,
    destination_name: str,
) -> None:
    if (
        not destination_name
        or destination_name in {".", ".."}
        or "\\" in destination_name
        or "/" in destination_name
        or "\x00" in destination_name
    ):
        raise WindowsNtReplaceError(
            "destination must be one immediate child basename"
        )
    encoded = destination_name.encode("utf-16-le")
    # Microsoft specifies a caller buffer of at least sizeof(structure) plus
    # FileNameLength.  FileName begins at its real ABI offset, not at the
    # structure's alignment-rounded sizeof boundary.
    total = ctypes.sizeof(_FILE_RENAME_INFORMATION_EX_HEADER) + len(encoded)
    buffer = ctypes.create_string_buffer(total)
    header = _FILE_RENAME_INFORMATION_EX_HEADER.from_buffer(buffer)
    header.Flags = (
        _FILE_RENAME_REPLACE_IF_EXISTS | _FILE_RENAME_POSIX_SEMANTICS
    )
    header.RootDirectory = destination_directory_handle
    header.FileNameLength = len(encoded)
    ctypes.memmove(
        ctypes.addressof(buffer)
        + _FILE_RENAME_INFORMATION_EX_HEADER.FileName.offset,
        encoded,
        len(encoded),
    )
    io_status = _IO_STATUS_BLOCK()
    status = int(
        _ntdll.NtSetInformationFile(
            source_handle,
            ctypes.byref(io_status),
            ctypes.byref(buffer),
            total,
            _FILE_RENAME_INFORMATION_EX,
        )
    )
    if status < 0:
        winerror = int(_ntdll.RtlNtStatusToDosError(status))
        raise NtSetInformationFileError(status, winerror)


def atomic_replace_verified(
    destination: Path | str,
    data: bytes,
    *,
    expected_sha256: str | None = None,
    _test_hook: Callable[[str, Path | None], None] | None = None,
) -> ReplacementReceipt:
    """Replace one existing file through a held-directory-relative NT rename."""

    _require_windows()
    if not isinstance(data, bytes):
        raise TypeError("data must be exact bytes")
    destination_path = _checked_drive_path(Path(destination))
    if destination_path.name in {"", ".", ".."}:
        raise WindowsNtReplaceError("invalid destination basename")
    data_hash = hashlib.sha256(data).hexdigest()
    required_hash = expected_sha256 or data_hash
    if required_hash != data_hash:
        raise HashMismatchError("expected SHA-256 does not match input bytes")
    hook = _test_hook or (lambda _point, _path: None)
    temporary_path: Path | None = None
    temporary_handle: int | None = None
    temporary_created = False
    renamed = False
    target_handle: int | None = None

    with _hold_directory_chain(destination_path.parent) as held:
        hook("directory_chain_held", destination_path.parent)
        held.verify()
        target_handle = _open_regular_guard(destination_path)
        try:
            target_identity = _ensure_kind(
                target_handle, destination_path, directory=False
            )
            hook("target_guarded", destination_path)
            if (
                _ensure_kind(target_handle, destination_path, directory=False)
                != target_identity
            ):
                raise IdentityMismatchError("held target identity changed")
            source_directory = destination_path.parent.parent
            if source_directory == destination_path.parent:
                raise WindowsNtReplaceError(
                    "a distinct same-volume source directory is required"
                )
            temporary_path = source_directory / (
                f".{destination_path.parent.name}.{destination_path.name}."
                f"{os.getpid()}.{secrets.token_hex(16)}.nttmp"
            )
            hook("temporary_name_chosen", temporary_path)
            temporary_handle = _create_file(
                temporary_path,
                access=_GENERIC_READ | _GENERIC_WRITE | _DELETE,
                share=_FILE_SHARE_READ,
                disposition=_CREATE_NEW,
                flags=(
                    _FILE_ATTRIBUTE_NORMAL
                    | _FILE_ATTRIBUTE_TEMPORARY
                    | _FILE_FLAG_WRITE_THROUGH
                    | _FILE_FLAG_OPEN_REPARSE_POINT
                ),
            )
            temporary_created = True
            temporary_identity = _ensure_kind(
                temporary_handle, temporary_path, directory=False
            )
            _validate_final_path(temporary_handle, temporary_path)
            _write_handle_bytes(temporary_handle, data)
            if _sha256_handle(temporary_handle) != required_hash:
                raise HashMismatchError("temporary handle hash mismatch")
            hook("temporary_verified", temporary_path)
            if _sha256_handle(temporary_handle) != required_hash:
                raise HashMismatchError("temporary handle changed")
            held.verify()
            if (
                _ensure_kind(target_handle, destination_path, directory=False)
                != target_identity
            ):
                raise IdentityMismatchError("held target identity changed")
            _validate_final_path(target_handle, destination_path)
            hook("before_nt_rename", destination_path)
            held.verify()
            if (
                _ensure_kind(target_handle, destination_path, directory=False)
                != target_identity
            ):
                raise IdentityMismatchError("held target identity changed")
            if _sha256_handle(temporary_handle) != required_hash:
                raise HashMismatchError("temporary changed before rename")

            # The old target guard intentionally stays open.  InformationEx
            # with POSIX semantics is the documented mechanism that allows
            # replacing its directory entry while preserving the old handle.
            _nt_rename_relative_ex(
                temporary_handle,
                held.directory_handle,
                destination_path.name,
            )
            renamed = True
            hook("after_nt_rename", destination_path)
            _validate_final_path(temporary_handle, destination_path)
            renamed_identity = _ensure_kind(
                temporary_handle, destination_path, directory=False
            )
            if renamed_identity != temporary_identity:
                raise IdentityMismatchError("renamed temporary identity changed")
            if _sha256_handle(temporary_handle) != required_hash:
                raise HashMismatchError("renamed handle hash mismatch")
            # The held old-target handle must still identify the old object.
            if (
                _ensure_kind(target_handle, destination_path, directory=False)
                != target_identity
            ):
                raise IdentityMismatchError("old target held identity changed")
            held.verify()
            path_handle = _open_regular_guard(destination_path)
            try:
                if (
                    _ensure_kind(path_handle, destination_path, directory=False)
                    != temporary_identity
                ):
                    raise IdentityMismatchError(
                        "destination path does not identify renamed temporary"
                    )
                if _sha256_handle(path_handle) != required_hash:
                    raise HashMismatchError("destination path hash mismatch")
            finally:
                _close(path_handle)
            return ReplacementReceipt(
                destination=destination_path,
                sha256=required_hash,
                byte_count=len(data),
                directory_identity=held.directory_identity,
                file_identity=temporary_identity,
            )
        finally:
            if target_handle is not None:
                _close(target_handle)
            if temporary_handle is not None:
                _close(temporary_handle)
            if temporary_created and temporary_path is not None and not renamed:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError as exc:
                    raise WindowsNtReplaceError(
                        f"could not clean temporary {temporary_path}: {exc}"
                    ) from exc
