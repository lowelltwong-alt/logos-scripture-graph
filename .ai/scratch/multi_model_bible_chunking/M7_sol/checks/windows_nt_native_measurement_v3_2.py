#!/usr/bin/env python3
"""T550 V3.2 Windows/NTFS measurement helper for disposable tests only.

This environment-bound adapter has no production eligibility or cleanup
authority.  It accepts only a disposable ``C:\\tmp`` fixture, retains all
handles internally, and returns a sealed lease whose contention API can name
only one of the sixteen resources issued by the collector.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import re
import secrets
import sys
import time
from types import MappingProxyType
from typing import Any, Mapping, Sequence


_V31_PATH = Path(__file__).with_name("windows_nt_native_measurement_v3_1.py")
_EXPECTED_V31_DEPENDENCY_SHA256 = (
    "d7288164bc444385c57b6e5372fde741201ee76fa0965c7ac128c781c5eff9c5"
)
if hashlib.sha256(_V31_PATH.read_bytes()).hexdigest() != _EXPECTED_V31_DEPENDENCY_SHA256:
    raise ImportError("frozen V3.1 native dependency hash drift")
_V31_SPEC = importlib.util.spec_from_file_location(
    "_t550_windows_nt_native_measurement_v31_dependency", _V31_PATH
)
if _V31_SPEC is None or _V31_SPEC.loader is None:
    raise ImportError(f"cannot load frozen V3.1 native dependency: {_V31_PATH}")
_v31 = importlib.util.module_from_spec(_V31_SPEC)
sys.modules[_V31_SPEC.name] = _v31
_V31_SPEC.loader.exec_module(_v31)


SCHEMA_VERSION = "windows_nt_native_measurement_v3_2.test_only.v1"
ADAPTER_CLASS = "environment_bound_exception"
BACKEND_ID = "windows_nt_native_v3_2_disposable_ntfs_test_only"
TEST_ROOT_PATTERN = re.compile(r"^t550-v3-2-native-[0-9a-f]{32}$")
TARGET_COUNT = 13
SENTINEL_COUNT = 3
RESOURCE_COUNT = TARGET_COUNT + SENTINEL_COUNT
MAX_CAPTURE_SECONDS = 120

NativeV32Error = _v31.NativeV31Error
UnsupportedPlatform = _v31.UnsupportedPlatform
UnsafeTestRoot = _v31.UnsafeTestRoot
ReparseRejected = _v31.ReparseRejected
CoverageUnavailable = _v31.CoverageUnavailable
HandleIdentity = _v31.HandleIdentity
FileObservation = _v31.FileObservation
_Api = _v31._Api

__all__ = [
    "BACKEND_ID",
    "CoverageUnavailable",
    "NativeHandleLeaseV32",
    "NativeV32Error",
    "ReparseRejected",
    "SCHEMA_VERSION",
    "UnsafeTestRoot",
    "collect_test_only_temp_root",
    "digest_value",
    "verify_safe_test_root",
]


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
        raise NativeV32Error("naive clock")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_parts(token: str) -> tuple[str, ...]:
    if not isinstance(token, str) or not token:
        raise NativeV32Error("empty relative token")
    normalized = token.replace("\\", "/")
    raw_parts = normalized.split("/")
    if any(part in ("", ".", "..") for part in raw_parts):
        raise NativeV32Error(f"ambiguous token forbidden: {token!r}")
    path = PureWindowsPath(normalized)
    if path.is_absolute() or path.drive:
        raise NativeV32Error(f"absolute token forbidden: {token!r}")
    if any(
        part in ("", ".", "..") or ":" in part or part.endswith((" ", "."))
        for part in path.parts
    ):
        raise NativeV32Error(f"ambiguous token forbidden: {token!r}")
    return tuple(path.parts)


def verify_safe_test_root(path: Path) -> Path:
    """Resolve the sole observable root; this never authorizes cleanup."""
    if os.name != "nt" or sys.platform != "win32":
        raise UnsupportedPlatform("Windows native adapter requires win32")
    resolved = Path(path).resolve(strict=True)
    tmp_root = Path(r"C:\tmp").resolve(strict=True)
    if (
        resolved.parent != tmp_root
        or TEST_ROOT_PATTERN.fullmatch(resolved.name) is None
    ):
        raise UnsafeTestRoot(
            "root must be one direct C:\\tmp\\t550-v3-2-native-<32 hex> child"
        )
    repository = Path(__file__).resolve().parents[5]
    for outer, inner in ((repository, resolved), (resolved, repository)):
        try:
            inner.relative_to(outer)
        except ValueError:
            continue
        raise UnsafeTestRoot("test root and repository must be disjoint")
    return resolved


@dataclass(frozen=True)
class _IssuedResource:
    parent_label: str
    leaf_label: str
    leaf: str
    parent_identity: HandleIdentity
    leaf_identity: HandleIdentity
    size_bytes: int
    sha256: str


class _LeaseState:
    __slots__ = (
        "api",
        "handles",
        "resources",
        "ordinal_tokens",
        "closed",
        "nonce",
    )

    def __init__(
        self,
        *,
        api: _Api,
        handles: dict[str, int],
        resources: Mapping[str, _IssuedResource],
        ordinal_tokens: Mapping[tuple[str, int], str],
        nonce: bytes,
    ) -> None:
        self.api = api
        self.handles = handles
        self.resources = resources
        self.ordinal_tokens = ordinal_tokens
        self.closed = False
        self.nonce = nonce

    def close(self) -> None:
        if self.closed:
            return
        failures = []
        for label in reversed(tuple(self.handles)):
            try:
                self.api.close(self.handles[label])
            except BaseException as exc:
                failures.append((label, exc))
        self.handles.clear()
        self.closed = True
        if failures:
            raise NativeV32Error("one or more retained handles failed to close")


class NativeHandleLeaseV32:
    """Sealed test lease exposing selectors, contention probes, and close only."""

    __slots__ = ("__state",)

    def __init__(self, state: _LeaseState) -> None:
        self.__state = state

    def contention_token(self, *, kind: str, ordinal: int) -> str:
        state = self.__state
        if state.closed:
            raise NativeV32Error("lease is closed")
        if kind not in ("target", "sentinel") or isinstance(ordinal, bool):
            raise NativeV32Error("invalid issued resource selector")
        try:
            return state.ordinal_tokens[(kind, ordinal)]
        except KeyError as exc:
            raise NativeV32Error("issued resource selector does not exist") from exc

    def probe_contention(self, issued_selector: str, *, intent: str) -> dict[str, Any]:
        state = self.__state
        if state.closed:
            raise NativeV32Error("lease is closed")
        if not isinstance(issued_selector, str):
            raise NativeV32Error("unknown issued lease resource selector")
        try:
            resource = state.resources[issued_selector]
        except KeyError as exc:
            raise NativeV32Error("unknown issued lease resource selector") from exc

        parent_handle = state.handles[resource.parent_label]
        leaf_handle = state.handles[resource.leaf_label]
        parent_identity = state.api.identity(parent_handle)
        _require_identity(
            parent_identity, directory=True, label=resource.parent_label
        )
        if parent_identity != resource.parent_identity:
            raise NativeV32Error("issued resource parent identity changed")
        leaf_identity = state.api.identity(leaf_handle)
        _require_identity(
            leaf_identity,
            directory=False,
            label=resource.leaf_label,
            single_link=True,
        )
        if leaf_identity != resource.leaf_identity:
            raise NativeV32Error("issued resource leaf identity changed")
        size_bytes, sha256 = state.api.hash_file(leaf_handle)
        if (size_bytes, sha256) != (resource.size_bytes, resource.sha256):
            raise NativeV32Error("issued resource leaf bytes changed")
        return state.api._probe_contention(
            parent_handle, resource.leaf, intent=intent
        )

    def nonce_sha256(self) -> str:
        return hashlib.sha256(self.__state.nonce).hexdigest()

    def close(self) -> None:
        self.__state.close()

    def __enter__(self) -> "NativeHandleLeaseV32":
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        self.close()
        return False

    def __reduce__(self):
        raise TypeError("NativeHandleLeaseV32 is intentionally non-serializable")


class _LeaseBuilder:
    """Collector-private mutable builder; never returned to callers."""

    __slots__ = (
        "_api",
        "_handles",
        "_resources",
        "_ordinal_tokens",
        "_nonce",
        "_sealed",
    )

    def __init__(self, api: _Api) -> None:
        self._api = api
        self._handles: dict[str, int] = {}
        self._resources: dict[str, _IssuedResource] = {}
        self._ordinal_tokens: dict[tuple[str, int], str] = {}
        self._nonce = secrets.token_bytes(32)
        self._sealed = False

    def retain(self, label: str, handle: int) -> int:
        if self._sealed or label in self._handles:
            self._api.close(handle)
            raise NativeV32Error("invalid collector-private retained handle")
        self._handles[label] = handle
        return handle

    def handle(self, label: str) -> int:
        if self._sealed:
            raise NativeV32Error("collector resource builder is sealed")
        return self._handles[label]

    def issue(
        self,
        *,
        kind: str,
        ordinal: int,
        parent_label: str,
        leaf_label: str,
        leaf: str,
        parent_identity: HandleIdentity,
        leaf_identity: HandleIdentity,
        size_bytes: int,
        sha256: str,
    ) -> None:
        if self._sealed:
            raise NativeV32Error("collector resource builder is sealed")
        key = (kind, ordinal)
        if key in self._ordinal_tokens:
            raise NativeV32Error("duplicate collector resource selector")
        token = secrets.token_hex(32)
        self._resources[token] = _IssuedResource(
            parent_label=parent_label,
            leaf_label=leaf_label,
            leaf=leaf,
            parent_identity=parent_identity,
            leaf_identity=leaf_identity,
            size_bytes=size_bytes,
            sha256=sha256,
        )
        self._ordinal_tokens[key] = token

    def seal(self) -> NativeHandleLeaseV32:
        if self._sealed or len(self._resources) != RESOURCE_COUNT:
            raise NativeV32Error("exact immutable 16-resource map required")
        self._sealed = True
        state = _LeaseState(
            api=self._api,
            handles=self._handles,
            resources=MappingProxyType(dict(self._resources)),
            ordinal_tokens=MappingProxyType(dict(self._ordinal_tokens)),
            nonce=self._nonce,
        )
        return NativeHandleLeaseV32(state)

    def close(self) -> None:
        if self._sealed:
            return
        failures = []
        for label in reversed(tuple(self._handles)):
            try:
                self._api.close(self._handles[label])
            except BaseException as exc:
                failures.append((label, exc))
        self._handles.clear()
        if failures:
            raise NativeV32Error("one or more retained handles failed to close")


def _require_identity(
    identity: HandleIdentity,
    *,
    directory: bool,
    label: str,
    single_link: bool = False,
) -> None:
    if identity.reparse_point:
        raise ReparseRejected(f"{label} is a reparse point")
    if identity.is_directory is not directory:
        raise NativeV32Error(f"{label} object-kind drift")
    if identity.delete_pending:
        raise NativeV32Error(f"{label} is delete-pending")
    if single_link and identity.link_count != 1:
        raise NativeV32Error(
            f"{label} requires NTFS link count one; observed {identity.link_count}"
        )


def _identity_key(identity: HandleIdentity) -> tuple[int, str]:
    return (identity.volume_serial, identity.file_id)


def _validate_final(
    api: _Api,
    builder: _LeaseBuilder,
    directory_identities: Mapping[str, HandleIdentity],
    file_rows: Sequence[FileObservation],
) -> None:
    for label, expected in directory_identities.items():
        observed = api.identity(builder.handle(label))
        _require_identity(observed, directory=True, label=label)
        if observed != expected:
            raise NativeV32Error(f"{label} identity changed before resource seal")
    for row in file_rows:
        label = f"{row.kind}:{row.ordinal}"
        observed = api.identity(builder.handle(label))
        _require_identity(
            observed, directory=False, label=label, single_link=True
        )
        if observed != row.identity:
            raise NativeV32Error(f"{label} identity changed before resource seal")
        size_bytes, sha256 = api.hash_file(builder.handle(label))
        if (size_bytes, sha256) != (row.size_bytes, row.sha256):
            raise NativeV32Error(f"{label} bytes changed before resource seal")


def collect_test_only_temp_root(
    *,
    test_root: Path,
    workspace_token: str,
    model_token: str,
    target_tokens: Sequence[str],
    sentinel_tokens: Sequence[str],
) -> tuple[dict[str, Any], NativeHandleLeaseV32]:
    """Measure one disposable NTFS fixture and return a sealed lease."""
    root = verify_safe_test_root(test_root)
    if len(target_tokens) != TARGET_COUNT or len(sentinel_tokens) != SENTINEL_COUNT:
        raise NativeV32Error("fixture requires exactly 13 targets and 3 sentinels")
    if len(set(target_tokens) | set(sentinel_tokens)) != RESOURCE_COUNT:
        raise NativeV32Error("fixture tokens must be distinct")
    workspace_parts = _safe_parts(workspace_token)
    model_parts = _safe_parts(model_token)
    if len(workspace_parts) != 1 or len(model_parts) != 1:
        raise NativeV32Error("workspace/model tokens must each be one component")

    target_parts = {token: _safe_parts(token) for token in target_tokens}
    sentinel_parts = {token: _safe_parts(token) for token in sentinel_tokens}
    if any(len(parts) < 2 for parts in target_parts.values()):
        raise NativeV32Error("one-component target token forbidden")
    if any(len(parts) != 1 for parts in sentinel_parts.values()):
        raise NativeV32Error("each exact root sentinel must be one component")

    api = _Api()
    builder = _LeaseBuilder(api)
    lease: NativeHandleLeaseV32 | None = None
    started_wall = datetime.now(timezone.utc)
    started_mono = time.monotonic_ns()
    try:
        volume = _v31._volume_facts(api, root)
        platform = _v31._native_platform_facts(api)
        boot = _v31._boot_facts(api)

        volume_handle = builder.retain(
            "volume-root",
            api.open_full_readonly(Path(volume["volume_guid"]), directory=True),
        )
        volume_identity = api.identity(volume_handle)
        _require_identity(volume_identity, directory=True, label="volume-root")

        root_handle = builder.retain(
            "test-root", api.open_full_readonly(root, directory=True)
        )
        root_identity = api.identity(root_handle)
        _require_identity(root_identity, directory=True, label="test-root")

        all_share = (
            api.FILE_SHARE_READ | api.FILE_SHARE_WRITE | api.FILE_SHARE_DELETE
        )
        workspace_handle = builder.retain(
            "workspace",
            api.open_relative_readonly(
                root_handle,
                workspace_parts[0],
                directory=True,
                share=all_share,
            ),
        )
        workspace_identity = api.identity(workspace_handle)
        _require_identity(workspace_identity, directory=True, label="workspace")

        model_handle = builder.retain(
            "model",
            api.open_relative_readonly(
                workspace_handle,
                model_parts[0],
                directory=True,
                share=all_share,
            ),
        )
        model_identity = api.identity(model_handle)
        _require_identity(model_identity, directory=True, label="model")

        parent_tokens = sorted(
            {"/".join(parts[:-1]) for parts in target_parts.values()}
        )
        parent_handles: dict[str, int] = {".": model_handle}
        parent_identities: dict[str, HandleIdentity] = {".": model_identity}
        for parent_token in parent_tokens:
            current_handle = model_handle
            accumulated: list[str] = []
            for part in _safe_parts(parent_token):
                accumulated.append(part)
                key = "/".join(accumulated)
                if key in parent_handles:
                    current_handle = parent_handles[key]
                    continue
                handle = builder.retain(
                    f"parent:{key}",
                    api.open_relative_readonly(
                        current_handle, part, directory=True, share=all_share
                    ),
                )
                identity = api.identity(handle)
                _require_identity(identity, directory=True, label=f"parent:{key}")
                parent_handles[key] = handle
                parent_identities[key] = identity
                current_handle = handle

        directory_identities = {
            "volume-root": volume_identity,
            "test-root": root_identity,
            "workspace": workspace_identity,
            "model": model_identity,
            **{
                f"parent:{key}": value
                for key, value in parent_identities.items()
                if key != "."
            },
        }
        directory_keys = [_identity_key(value) for value in directory_identities.values()]
        if len(directory_keys) != len(set(directory_keys)):
            raise NativeV32Error("root or parent directory identity alias")
        model_volume = model_identity.volume_serial
        if any(
            identity.volume_serial != model_volume
            for identity in directory_identities.values()
        ):
            raise NativeV32Error("root or parent crossed model volume")

        file_rows: list[FileObservation] = []
        file_keys: set[tuple[int, str]] = set()
        all_tokens = [*target_tokens, *sentinel_tokens]
        for token in all_tokens:
            kind = "sentinel" if token in sentinel_parts else "target"
            parts = sentinel_parts[token] if kind == "sentinel" else target_parts[token]
            ordinal = (
                sentinel_tokens.index(token) + 1
                if kind == "sentinel"
                else target_tokens.index(token) + 1
            )
            parent_token = "." if len(parts) == 1 else "/".join(parts[:-1])
            leaf = parts[-1]
            parent_label = "model" if parent_token == "." else f"parent:{parent_token}"
            parent_identity = parent_identities[parent_token]
            share = api.FILE_SHARE_READ if kind == "sentinel" else 0
            leaf_label = f"{kind}:{ordinal}"
            handle = builder.retain(
                leaf_label,
                api.open_relative_readonly(
                    parent_handles[parent_token],
                    leaf,
                    directory=False,
                    share=share,
                ),
            )
            identity = api.identity(handle)
            _require_identity(
                identity, directory=False, label=leaf_label, single_link=True
            )
            key = _identity_key(identity)
            if (
                key in file_keys
                or key in set(directory_keys)
                or identity.volume_serial != model_volume
            ):
                raise NativeV32Error("file identity alias or volume drift")
            file_keys.add(key)
            size_bytes, sha256 = api.hash_file(handle)
            file_rows.append(
                FileObservation(
                    ordinal=ordinal,
                    kind=kind,
                    token=token.replace("\\", "/"),
                    parent_token=parent_token,
                    leaf=leaf,
                    parent_identity=parent_identity,
                    identity=identity,
                    size_bytes=size_bytes,
                    sha256=sha256,
                    observed_wall_utc=_iso(datetime.now(timezone.utc)),
                    observed_monotonic_ns=time.monotonic_ns(),
                    open_policy=(
                        "read_handle_share_read_only"
                        if kind == "sentinel"
                        else "read_handle_exclusive_share_zero"
                    ),
                )
            )

        process = _v31._diagnostic_process_evidence(api, builder)
        _validate_final(api, builder, directory_identities, file_rows)

        for row in file_rows:
            parent_label = (
                "model" if row.parent_token == "." else f"parent:{row.parent_token}"
            )
            builder.issue(
                kind=row.kind,
                ordinal=row.ordinal,
                parent_label=parent_label,
                leaf_label=f"{row.kind}:{row.ordinal}",
                leaf=row.leaf,
                parent_identity=row.parent_identity,
                leaf_identity=row.identity,
                size_bytes=row.size_bytes,
                sha256=row.sha256,
            )
        lease = builder.seal()

        ended_wall = datetime.now(timezone.utc)
        ended_mono = time.monotonic_ns()
        duration = (ended_mono - started_mono) / 1_000_000_000
        if duration < 0 or duration > MAX_CAPTURE_SECONDS:
            raise NativeV32Error("capture exceeded bounded duration")

        targets = [asdict(row) for row in file_rows if row.kind == "target"]
        sentinels = [asdict(row) for row in file_rows if row.kind == "sentinel"]
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
                "final_handle_validation_before_resource_seal": True,
            },
            "boot": boot,
            "platform": platform,
            "volume": {**volume, "volume_root_identity": asdict(volume_identity)},
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
                "issued_resource_count": RESOURCE_COUNT,
                "resource_map_immutable_before_return": True,
                "caller_retention_or_registration_surface_present": False,
                "contention_probe_selector": (
                    "collector_issued_selector_only_no_path_argument"
                ),
                "parent_and_leaf_revalidated_before_contention_open": True,
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
        if lease is not None:
            lease.close()
        else:
            builder.close()
        raise
