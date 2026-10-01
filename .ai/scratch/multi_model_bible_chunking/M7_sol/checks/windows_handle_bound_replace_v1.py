#!/usr/bin/env python3
"""Windows handle-bound file replacement and read-only sentinel guards.

These primitives are deliberately environment-bound.  They use Win32 handles
and sharing rules to protect names and bytes against other cooperating Windows
processes while the handles are held.  They do *not* provide power-loss
durability or multi-file/set atomicity.

``atomic_replace_verified``:

* holds every destination-directory component open without ``FILE_SHARE_DELETE``;
* rejects reparse points in the directory chain, old destination, and temporary;
* creates the temporary with ``CREATE_NEW`` and verifies bytes by its handle;
* renames by ``SetFileInformationByHandle(FileRenameInfo)`` using the held
  destination-directory handle as ``RootDirectory``; and
* proves that the renamed temporary handle and a fresh destination-path handle
  identify the same file and contain the requested bytes.

``SentinelHandleGuard`` opens every sentinel for read with only
``FILE_SHARE_READ``.  Windows therefore rejects new write/delete/rename handles
for the guard lifetime.  Hashes are read from the held handles on entry and
exit, and path identity is rechecked before release.
"""
from __future__ import annotations

import ctypes
import hashlib
import os
import secrets
import sys
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Callable, Iterator, Mapping


class WindowsHandleProtectionError(RuntimeError):
    """A Windows handle/path protection invariant could not be established."""


class UnsupportedPlatformError(WindowsHandleProtectionError):
    """The requested Windows-only primitive was called on another platform."""


class ReparsePointError(WindowsHandleProtectionError):
    """A protected path contains a symlink or other reparse point."""


class IdentityMismatchError(WindowsHandleProtectionError):
    """A path no longer names the file or directory held by the guard."""


class HashMismatchError(WindowsHandleProtectionError):
    """Handle-read bytes do not match the required SHA-256."""


@dataclass(frozen=True)
class FileIdentity:
    """Stable identity exposed by ``BY_HANDLE_FILE_INFORMATION``."""

    volume_serial_number: int
    file_index: int


@dataclass(frozen=True)
class ReplacementReceipt:
    """Verified result of one handle-bound atomic name replacement."""

    destination: Path
    sha256: str
    byte_count: int
    directory_identity: FileIdentity
    file_identity: FileIdentity
    protection_claim: str = (
        "windows_process_handle_path_protection_not_power_loss_or_set_atomicity"
    )


_IS_WINDOWS = os.name == "nt" and sys.platform.startswith("win")

if _IS_WINDOWS:
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    _GENERIC_READ = 0x80000000
    _GENERIC_WRITE = 0x40000000
    _DELETE = 0x00010000
    _FILE_LIST_DIRECTORY = 0x0001
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
    _FILE_RENAME_INFO_CLASS = 3
    _ERROR_FILE_NOT_FOUND = 2
    _ERROR_PATH_NOT_FOUND = 3

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
    _kernel32.SetFileInformationByHandle.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    _kernel32.SetFileInformationByHandle.restype = wintypes.BOOL


def _require_windows() -> None:
    if not _IS_WINDOWS:
        raise UnsupportedPlatformError(
            "Windows handle-bound protection is unavailable on this platform"
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
        str(path),
        access,
        share,
        None,
        disposition,
        flags,
        None,
    )
    if handle == _INVALID_HANDLE_VALUE:
        raise _win_error("CreateFileW", path)
    return handle


def _handle_information(handle: int) -> tuple[FileIdentity, int, int]:
    info = _BY_HANDLE_FILE_INFORMATION()
    if not _kernel32.GetFileInformationByHandle(handle, ctypes.byref(info)):
        raise _win_error("GetFileInformationByHandle")
    identity = FileIdentity(
        volume_serial_number=int(info.dwVolumeSerialNumber),
        file_index=(int(info.nFileIndexHigh) << 32) | int(info.nFileIndexLow),
    )
    size = (int(info.nFileSizeHigh) << 32) | int(info.nFileSizeLow)
    return identity, int(info.dwFileAttributes), size


def _ensure_kind(
    handle: int,
    *,
    path: Path,
    directory: bool,
) -> FileIdentity:
    identity, attributes, _ = _handle_information(handle)
    if attributes & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise ReparsePointError(f"reparse point is forbidden: {path}")
    is_directory = bool(attributes & _FILE_ATTRIBUTE_DIRECTORY)
    if is_directory != directory:
        kind = "directory" if directory else "regular file"
        raise WindowsHandleProtectionError(f"expected {kind}: {path}")
    return identity


def _strip_extended_prefix(value: str) -> str:
    if value.startswith("\\\\?\\UNC\\"):
        return "\\\\" + value[8:]
    if value.startswith("\\\\?\\"):
        return value[4:]
    return value


def _normalized_path(path: Path | str) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(str(path))))


def _final_path(handle: int) -> Path:
    capacity = 512
    while True:
        buffer = ctypes.create_unicode_buffer(capacity)
        length = _kernel32.GetFinalPathNameByHandleW(
            handle, buffer, capacity, 0
        )
        if not length:
            raise _win_error("GetFinalPathNameByHandleW")
        if length < capacity:
            return Path(_strip_extended_prefix(buffer.value))
        capacity = length + 1


def _validate_final_name(handle: int, expected: Path) -> None:
    actual = _final_path(handle)
    if _normalized_path(actual) != _normalized_path(expected):
        raise IdentityMismatchError(
            f"handle final path mismatch: {actual} != {expected}"
        )


def _handle_bytes(handle: int) -> bytes:
    size = ctypes.c_longlong()
    if not _kernel32.GetFileSizeEx(handle, ctypes.byref(size)):
        raise _win_error("GetFileSizeEx")
    if size.value < 0:
        raise WindowsHandleProtectionError("negative file size")
    if not _kernel32.SetFilePointerEx(handle, 0, None, 0):
        raise _win_error("SetFilePointerEx")
    remaining = int(size.value)
    chunks: list[bytes] = []
    while remaining:
        request = min(remaining, 1024 * 1024)
        buffer = ctypes.create_string_buffer(request)
        read = wintypes.DWORD()
        if not _kernel32.ReadFile(
            handle, buffer, request, ctypes.byref(read), None
        ):
            raise _win_error("ReadFile")
        if read.value == 0:
            raise WindowsHandleProtectionError(
                "unexpected EOF while hashing held file"
            )
        chunks.append(buffer.raw[: read.value])
        remaining -= int(read.value)
    return b"".join(chunks)


def _write_handle_bytes(handle: int, data: bytes) -> None:
    offset = 0
    view = memoryview(data)
    while offset < len(data):
        block = bytes(view[offset : offset + 1024 * 1024])
        buffer = ctypes.create_string_buffer(block, len(block))
        written = wintypes.DWORD()
        if not _kernel32.WriteFile(
            handle, buffer, len(block), ctypes.byref(written), None
        ):
            raise _win_error("WriteFile")
        if written.value == 0:
            raise WindowsHandleProtectionError("zero-byte WriteFile")
        offset += int(written.value)
    if not _kernel32.FlushFileBuffers(handle):
        raise _win_error("FlushFileBuffers")


def _sha256_handle(handle: int) -> str:
    return hashlib.sha256(_handle_bytes(handle)).hexdigest()


def _checked_absolute_drive_path(path: Path) -> Path:
    raw = str(path)
    if "\x00" in raw:
        raise WindowsHandleProtectionError("NUL is forbidden in a path")
    absolute = Path(os.path.abspath(raw))
    pure = PureWindowsPath(str(absolute))
    if not pure.drive or not pure.root or str(absolute).startswith("\\\\"):
        raise WindowsHandleProtectionError(
            "only absolute local drive paths are supported"
        )
    if any(part == ".." for part in PureWindowsPath(raw).parts):
        raise WindowsHandleProtectionError("parent traversal is forbidden")
    return absolute


def _directory_components(directory: Path) -> list[Path]:
    absolute = _checked_absolute_drive_path(directory)
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
            actual = _ensure_kind(handle, path=path, directory=True)
            if actual != expected:
                raise IdentityMismatchError(
                    f"held directory identity changed: {path}"
                )
            probe = _create_file(
                path,
                access=_GENERIC_READ,
                share=_FILE_SHARE_READ | _FILE_SHARE_WRITE,
                disposition=_OPEN_EXISTING,
                flags=(
                    _FILE_FLAG_BACKUP_SEMANTICS
                    | _FILE_FLAG_OPEN_REPARSE_POINT
                ),
            )
            try:
                probed = _ensure_kind(probe, path=path, directory=True)
                if probed != expected:
                    raise IdentityMismatchError(
                        f"directory path was rebound: {path}"
                    )
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
                access=_GENERIC_READ,
                share=_FILE_SHARE_READ | _FILE_SHARE_WRITE,
                disposition=_OPEN_EXISTING,
                flags=(
                    _FILE_FLAG_BACKUP_SEMANTICS
                    | _FILE_FLAG_OPEN_REPARSE_POINT
                ),
            )
            handles.append(handle)
            identities.append(
                _ensure_kind(handle, path=component, directory=True)
            )
        held = _HeldDirectoryChain(
            directory=_checked_absolute_drive_path(directory),
            handles=handles,
            identities=identities,
        )
        held.verify()
        yield held
        held.verify()
    finally:
        close_error: Exception | None = None
        for handle in reversed(handles):
            try:
                _close(handle)
            except Exception as exc:  # preserve closing every held component
                close_error = close_error or exc
        if close_error is not None:
            raise close_error


def _open_regular_read_guard(path: Path) -> int:
    handle = _create_file(
        path,
        access=_GENERIC_READ,
        share=_FILE_SHARE_READ,
        disposition=_OPEN_EXISTING,
        flags=_FILE_FLAG_OPEN_REPARSE_POINT | _FILE_FLAG_SEQUENTIAL_SCAN,
    )
    try:
        _ensure_kind(handle, path=path, directory=False)
        _validate_final_name(handle, path)
        return handle
    except BaseException:
        _close(handle)
        raise


def _rename_relative(
    source_handle: int,
    directory_handle: int,
    destination_name: str,
) -> None:
    if not destination_name or "\\" in destination_name or "/" in destination_name:
        raise WindowsHandleProtectionError(
            "destination must be one immediate child name"
        )
    encoded_length = len(destination_name.encode("utf-16-le"))
    character_count = len(destination_name)

    class _FILE_RENAME_INFO(ctypes.Structure):
        _fields_ = [
            ("ReplaceIfExists", wintypes.BOOLEAN),
            ("RootDirectory", wintypes.HANDLE),
            ("FileNameLength", wintypes.DWORD),
            ("FileName", wintypes.WCHAR * character_count),
        ]

    info = _FILE_RENAME_INFO()
    info.ReplaceIfExists = True
    info.RootDirectory = directory_handle
    info.FileNameLength = encoded_length
    info.FileName = destination_name
    if not _kernel32.SetFileInformationByHandle(
        source_handle,
        _FILE_RENAME_INFO_CLASS,
        ctypes.byref(info),
        ctypes.sizeof(info),
    ):
        raise _win_error("SetFileInformationByHandle(FileRenameInfo)")


def atomic_replace_verified(
    destination: Path | str,
    data: bytes,
    *,
    expected_sha256: str | None = None,
    _test_hook: Callable[[str, Path | None], None] | None = None,
) -> ReplacementReceipt:
    """Atomically replace one existing regular file and prove the result.

    The atomic guarantee is only the one filesystem namespace transition made
    by ``FileRenameInfo``.  This function does not make surrounding files
    atomic and cannot promise persistence across power loss.

    ``_test_hook`` exists solely for deterministic adversarial tests.  Runtime
    callers should not supply it.
    """

    _require_windows()
    if not isinstance(data, bytes):
        raise TypeError("data must be exact bytes")
    destination_path = _checked_absolute_drive_path(Path(destination))
    if destination_path.name in {"", ".", ".."}:
        raise WindowsHandleProtectionError("invalid destination name")
    required_hash = expected_sha256 or hashlib.sha256(data).hexdigest()
    if required_hash != hashlib.sha256(data).hexdigest():
        raise HashMismatchError("expected SHA-256 does not match input bytes")
    hook = _test_hook or (lambda _point, _path: None)
    temporary_path: Path | None = None
    temporary_handle: int | None = None
    temporary_created = False
    old_target_handle: int | None = None
    renamed = False

    with _hold_directory_chain(destination_path.parent) as held:
        hook("directory_chain_held", destination_path.parent)
        old_target_handle = _open_regular_read_guard(destination_path)
        try:
            old_identity = _ensure_kind(
                old_target_handle, path=destination_path, directory=False
            )
            hook("old_target_guarded", destination_path)
            source_directory = destination_path.parent.parent
            if source_directory == destination_path.parent:
                raise WindowsHandleProtectionError(
                    "a distinct same-volume source directory is required for "
                    "handle-relative FileRenameInfo"
                )
            temporary_path = source_directory / (
                f".{destination_path.parent.name}.{destination_path.name}."
                f"{os.getpid()}.{secrets.token_hex(16)}.tmp"
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
                temporary_handle, path=temporary_path, directory=False
            )
            _validate_final_name(temporary_handle, temporary_path)
            _write_handle_bytes(temporary_handle, data)
            if _sha256_handle(temporary_handle) != required_hash:
                raise HashMismatchError("temporary handle hash mismatch")
            hook("temporary_verified", temporary_path)
            held.verify()
            current_target = _open_regular_read_guard(destination_path)
            try:
                current_identity = _ensure_kind(
                    current_target, path=destination_path, directory=False
                )
                if current_identity != old_identity:
                    raise IdentityMismatchError(
                        "destination changed while replacement was prepared"
                    )
            finally:
                _close(current_target)
            # The old read guard must be released for replace-if-exists.  The
            # parent handles remain held, and the relative handle rename plus
            # final identity/readback checks fail closed if the target changes.
            _close(old_target_handle)
            old_target_handle = None
            hook("before_relative_rename", destination_path)
            held.verify()
            _rename_relative(
                temporary_handle,
                held.directory_handle,
                destination_path.name,
            )
            renamed = True
            hook("after_relative_rename", destination_path)
            _validate_final_name(temporary_handle, destination_path)
            renamed_identity = _ensure_kind(
                temporary_handle, path=destination_path, directory=False
            )
            if renamed_identity != temporary_identity:
                raise IdentityMismatchError(
                    "renamed handle identity differs from temporary identity"
                )
            if _sha256_handle(temporary_handle) != required_hash:
                raise HashMismatchError("renamed handle hash mismatch")
            held.verify()
            path_handle = _open_regular_read_guard(destination_path)
            try:
                path_identity = _ensure_kind(
                    path_handle, path=destination_path, directory=False
                )
                if path_identity != temporary_identity:
                    raise IdentityMismatchError(
                        "destination path does not name renamed temporary"
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
            if old_target_handle is not None:
                _close(old_target_handle)
            if temporary_handle is not None:
                _close(temporary_handle)
            if temporary_created and temporary_path is not None and not renamed:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError as exc:
                    raise WindowsHandleProtectionError(
                        f"could not clean temporary {temporary_path}: {exc}"
                    ) from exc


@dataclass
class _HeldSentinel:
    path: Path
    expected_sha256: str
    handle: int
    identity: FileIdentity
    chain: _HeldDirectoryChain


class SentinelHandleGuard:
    """Hold read-only sentinels so new writes/deletes/renames are denied."""

    def __init__(self, expected: Mapping[Path | str, str]) -> None:
        _require_windows()
        if not expected:
            raise ValueError("at least one sentinel is required")
        self._expected = {
            _checked_absolute_drive_path(Path(path)): digest
            for path, digest in expected.items()
        }
        if len(self._expected) != len(expected):
            raise WindowsHandleProtectionError("duplicate sentinel path")
        self._stack: ExitStack | None = None
        self._held: list[_HeldSentinel] = []

    def __enter__(self) -> "SentinelHandleGuard":
        _require_windows()
        if self._stack is not None:
            raise WindowsHandleProtectionError(
                "sentinel guard cannot be entered twice"
            )
        stack = ExitStack()
        held: list[_HeldSentinel] = []
        try:
            for path, expected_hash in sorted(
                self._expected.items(), key=lambda item: str(item[0]).lower()
            ):
                if (
                    len(expected_hash) != 64
                    or any(ch not in "0123456789abcdef" for ch in expected_hash)
                ):
                    raise ValueError(f"invalid lowercase SHA-256 for {path}")
                chain = stack.enter_context(
                    _hold_directory_chain(path.parent)
                )
                handle = _open_regular_read_guard(path)
                stack.callback(_close, handle)
                identity = _ensure_kind(handle, path=path, directory=False)
                actual_hash = _sha256_handle(handle)
                if actual_hash != expected_hash:
                    raise HashMismatchError(
                        f"sentinel hash mismatch for {path}: "
                        f"{actual_hash} != {expected_hash}"
                    )
                held.append(
                    _HeldSentinel(
                        path=path,
                        expected_sha256=expected_hash,
                        handle=handle,
                        identity=identity,
                        chain=chain,
                    )
                )
        except BaseException:
            stack.close()
            raise
        self._stack = stack
        self._held = held
        return self

    def verify_unchanged(self) -> None:
        """Recheck bytes and path identities while all guards remain held."""

        if self._stack is None:
            raise WindowsHandleProtectionError("sentinel guard is not active")
        for sentinel in self._held:
            sentinel.chain.verify()
            identity = _ensure_kind(
                sentinel.handle, path=sentinel.path, directory=False
            )
            if identity != sentinel.identity:
                raise IdentityMismatchError(
                    f"sentinel handle identity changed: {sentinel.path}"
                )
            if _sha256_handle(sentinel.handle) != sentinel.expected_sha256:
                raise HashMismatchError(
                    f"sentinel held bytes changed: {sentinel.path}"
                )
            probe = _open_regular_read_guard(sentinel.path)
            try:
                path_identity = _ensure_kind(
                    probe, path=sentinel.path, directory=False
                )
                if path_identity != sentinel.identity:
                    raise IdentityMismatchError(
                        f"sentinel path was rebound: {sentinel.path}"
                    )
                if _sha256_handle(probe) != sentinel.expected_sha256:
                    raise HashMismatchError(
                        f"sentinel path bytes changed: {sentinel.path}"
                    )
            finally:
                _close(probe)

    def __exit__(self, exc_type, exc, traceback) -> bool:
        if self._stack is None:
            return False
        verification_error: BaseException | None = None
        try:
            self.verify_unchanged()
        except BaseException as caught:
            verification_error = caught
        stack = self._stack
        self._stack = None
        self._held = []
        stack.close()
        if verification_error is not None:
            raise verification_error
        return False


@contextmanager
def sentinel_file_guard(
    expected: Mapping[Path | str, str],
) -> Iterator[SentinelHandleGuard]:
    """Convenience context manager for ``SentinelHandleGuard``."""

    with SentinelHandleGuard(expected) as guard:
        yield guard

