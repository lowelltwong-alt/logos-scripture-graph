#!/usr/bin/env python3
"""Additive V3.2 closure policy for the frozen T550 Hosea V3.1 core.

V3.1 remains the byte-exact base policy.  V3.2 first executes that complete
policy, then requires a closed, canonical sidecar which closes observation
causality, rooted topology, full-system enumeration derivation, same-lease
chronology, and typed canonical continuity.  This module is pure: it performs
no filesystem, process, Windows, clock, lease, or transaction action.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any, Mapping


_V31_PATH = Path(__file__).with_name("rematerialization_live_gate_policy_v3_1.py")
_V31_SPEC = importlib.util.spec_from_file_location("t550_policy_v31_for_v32", _V31_PATH)
if _V31_SPEC is None or _V31_SPEC.loader is None:  # pragma: no cover
    raise ImportError("V3.1 policy loader unavailable")
V31 = importlib.util.module_from_spec(_V31_SPEC)
sys.modules.setdefault(_V31_SPEC.name, V31)
_V31_SPEC.loader.exec_module(V31)

SCHEMA_VERSION = "t550.rematerialization_live_gate_policy.v3_2"
EVIDENCE_SCHEMA = "t550.rematerialization_live_gate_evidence.v3_2"
RESULT_SCHEMA = "t550.v9_machine_precondition_result.v3_2"
SUCCESS_LABEL = V31.SUCCESS_LABEL
STATIC_ALLOWLIST_SHA256 = V31.STATIC_ALLOWLIST_SHA256
MAX_LEASE_SECONDS = V31.MAX_LEASE_SECONDS
MAX_INTEGER = (1 << 63) - 1
MAX_CLOCK_SKEW_SECONDS = 1
ENUMERATION_API = "NtQuerySystemInformation/SystemProcessInformation"
ENUMERATION_TERMINAL_STATUS = "ERROR_NO_MORE_FILES"

_SHA = re.compile(r"^[0-9a-f]{64}$")
_OPAQUE = re.compile(r"^[A-Za-z0-9_-]{32,128}$")
_NUMERIC_KEYS = {
    "ordinal",
    "attributes",
    "volume_serial",
    "size_bytes",
    "preimage_size_bytes",
    "staged_size_bytes",
    "expected_preimage_size_bytes",
    "expected_staged_size_bytes",
    "ntfs_link_count",
    "pid",
    "parent_pid",
    "raw_count",
    "system_process_count",
    "bounded_candidate_count",
    "opened_bounded_count",
    "classified_bounded_count",
    "access_denied_count",
    "pid_reuse_count",
    "omitted_count",
    "exited_count",
    "current_pid",
    "controller_pid",
    "decision_count",
    "start_monotonic_ns",
    "end_monotonic_ns",
    "observation_monotonic_ns",
    "validated_at_monotonic_ns",
    "validation_monotonic_ns",
    "lease_start_monotonic_ns",
}


class LiveGatePolicyV32Error(ValueError):
    """A closed V3.2 invariant failed."""


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
        raise LiveGatePolicyV32Error("value is not canonical JSON") from exc


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_value(value: Any) -> str:
    return digest_bytes(canonical_json_bytes(value))


def _closed(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveGatePolicyV32Error(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        raise LiveGatePolicyV32Error(
            f"{label} schema drift missing={sorted(keys - actual)} "
            f"extra={sorted(actual - keys)}"
        )
    return value


def _array(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise LiveGatePolicyV32Error(f"{label} must be an ordered array")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise LiveGatePolicyV32Error(f"{label} must be non-empty text")
    return value


def _sha(value: Any, label: str) -> str:
    text = _text(value, label)
    if _SHA.fullmatch(text) is None:
        raise LiveGatePolicyV32Error(f"{label} must be lowercase SHA-256")
    return text


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value < minimum
        or value > MAX_INTEGER
    ):
        raise LiveGatePolicyV32Error(
            f"{label} must be a strict integer in [{minimum}, {MAX_INTEGER}]"
        )
    return value


def _strict_numeric_tree(value: Any, label: str = "input") -> None:
    """Reject all floats and bool/negative/overflow substitutions in numeric fields."""
    if isinstance(value, float):
        raise LiveGatePolicyV32Error(f"{label} contains a float")
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in _NUMERIC_KEYS or key.endswith(("_count", "_bytes", "_monotonic_ns")):
                _integer(child, f"{label}.{key}")
            else:
                _strict_numeric_tree(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _strict_numeric_tree(child, f"{label}[{index}]")


def _utc(value: Any, label: str) -> datetime:
    text = _text(value, label)
    try:
        result = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LiveGatePolicyV32Error(f"{label} must be ISO-8601") from exc
    if result.tzinfo is None or result.utcoffset() != timezone.utc.utcoffset(result):
        raise LiveGatePolicyV32Error(f"{label} must identify UTC")
    return result.astimezone(timezone.utc)


def _identity(value: Any, label: str, *, directory: bool) -> dict[str, Any]:
    row = _closed(
        value,
        {"volume_serial", "file_id", "attributes", "is_directory", "reparse_point"},
        label,
    )
    volume = _integer(row["volume_serial"], f"{label}.volume_serial")
    file_id = _text(row["file_id"], f"{label}.file_id")
    _integer(row["attributes"], f"{label}.attributes")
    if row["is_directory"] is not directory or row["reparse_point"] is not False:
        raise LiveGatePolicyV32Error(f"{label} type or reparse drift")
    return dict(row)


def _identity_key(value: Mapping[str, Any]) -> tuple[int, str]:
    return value["volume_serial"], value["file_id"]


def _parse_canonical(raw: Any, expected_sha256: str, label: str) -> dict[str, Any]:
    if not isinstance(raw, bytes):
        raise LiveGatePolicyV32Error(f"{label} must be bytes")
    _sha(expected_sha256, f"expected {label} SHA-256")
    if digest_bytes(raw) != expected_sha256:
        raise LiveGatePolicyV32Error(f"{label} detached hash drift")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiveGatePolicyV32Error(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise LiveGatePolicyV32Error(f"{label} must be exact canonical object bytes")
    return value


def _v31_raw(raw: bytes, expected_sha256: str, label: str) -> dict[str, Any]:
    return _parse_canonical(raw, expected_sha256, label)


def _subject_rows(raw: Mapping[str, Any], v32: Mapping[str, Any]) -> dict[tuple[str, str], Any]:
    evidence = raw["evidence"]
    subjects: dict[tuple[str, str], Any] = {
        ("environment", "environment"): evidence["environment"],
        ("effect", "effects"): evidence["effects"],
        ("system_snapshot", "enumeration"): v32["enumeration"],
        ("topology", "rooted_topology"): v32["rooted_topology"],
    }
    for row in evidence["canonical_parents"]:
        subjects[("parent", row["parent_id"])] = row
    for row in evidence["targets"]:
        subjects[("target", row["target_id"])] = row
    for row in evidence["sentinels"]:
        subjects[("sentinel", row["sentinel_id"])] = row
    for row in evidence["bounded_process_snapshot"]["rows"]:
        subjects[("process", str(row["pid"]))] = row
    return subjects


def _validate_observations(
    value: Any, raw: Mapping[str, Any], v32: Mapping[str, Any]
) -> list[dict[str, Any]]:
    rows = _array(value, "observation attestations")
    subjects = _subject_rows(raw, v32)
    checker = raw["checker"]
    start_wall = _utc(checker["start_wall_utc"], "checker start wall")
    end_wall = _utc(checker["end_wall_utc"], "checker end wall")
    start_mono = _integer(checker["start_monotonic_ns"], "checker start monotonic")
    end_mono = _integer(checker["end_monotonic_ns"], "checker end monotonic")
    observed: set[tuple[str, str]] = set()
    result: list[dict[str, Any]] = []
    for index, item in enumerate(rows, 1):
        row = _closed(
            item,
            {
                "observation_class",
                "subject_id",
                "subject_sha256",
                "observation_wall_utc",
                "observation_monotonic_ns",
            },
            f"observation[{index}]",
        )
        key = (
            _text(row["observation_class"], "observation class"),
            _text(row["subject_id"], "observation subject"),
        )
        if key not in subjects or key in observed:
            raise LiveGatePolicyV32Error("observation subject is unknown or duplicated")
        if _sha(row["subject_sha256"], "observation subject digest") != digest_value(
            subjects[key]
        ):
            raise LiveGatePolicyV32Error("observation digest drift")
        wall = _utc(row["observation_wall_utc"], "observation wall")
        mono = _integer(row["observation_monotonic_ns"], "observation monotonic")
        if not start_wall <= wall <= end_wall or not start_mono <= mono <= end_mono:
            raise LiveGatePolicyV32Error("observation outside checker interval")
        subject = subjects[key]
        if key[0] in {"target", "sentinel", "process"} and (
            row["observation_wall_utc"] != subject["observation_wall_utc"]
            or mono != subject["observation_monotonic_ns"]
        ):
            raise LiveGatePolicyV32Error("observation timestamp binding drift")
        observed.add(key)
        result.append(dict(row))
    if observed != set(subjects):
        raise LiveGatePolicyV32Error("observation coverage is incomplete")
    return result


def _validate_topology(value: Any, raw: Mapping[str, Any]) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "volume_serial",
            "root_chain_from_volume",
            "parent_chains",
            "all_identity_keys_sha256",
        },
        "rooted topology",
    )
    env = raw["evidence"]["environment"]
    volume = _integer(row["volume_serial"], "topology volume serial")
    if volume != env["volume_serial"]:
        raise LiveGatePolicyV32Error("topology volume drift")
    root = env["volume_root_identity"]
    workspace = env["workspace_identity"]
    model = env["model_identity"]
    root_chain = [
        _identity(x, "root-chain identity", directory=True)
        for x in _array(row["root_chain_from_volume"], "root chain")
    ]
    if root_chain != [root, workspace, model]:
        raise LiveGatePolicyV32Error("volume/workspace/model rooted ancestry drift")
    directory_keys = [_identity_key(_identity(x, "root identity", directory=True)) for x in (root, workspace, model)]
    expected_parents = {item["parent_id"]: item for item in raw["evidence"]["canonical_parents"]}
    chains = _array(row["parent_chains"], "parent chains")
    if len(chains) != len(expected_parents):
        raise LiveGatePolicyV32Error("parent-chain coverage drift")
    seen: set[str] = set()
    normalized_chains: list[dict[str, Any]] = []
    for index, item in enumerate(chains, 1):
        chain = _closed(
            item,
            {"parent_id", "path_token", "identities_from_model"},
            f"parent chain[{index}]",
        )
        parent_id = _text(chain["parent_id"], "chain parent id")
        if parent_id not in expected_parents or parent_id in seen:
            raise LiveGatePolicyV32Error("parent-chain identity drift")
        expected = expected_parents[parent_id]
        if chain["path_token"] != expected["path_token"]:
            raise LiveGatePolicyV32Error("parent-chain path drift")
        identities = [
            _identity(x, "parent-chain identity", directory=True)
            for x in _array(chain["identities_from_model"], "chain identities")
        ]
        components = [] if expected["path_token"] == "." else expected["path_token"].split("/")
        if len(identities) != len(components):
            raise LiveGatePolicyV32Error("parent-chain component depth drift")
        if identities:
            if identities[-1] != expected["identity"]:
                raise LiveGatePolicyV32Error("parent-chain terminal identity drift")
            directory_keys.extend(_identity_key(x) for x in identities)
        elif expected["identity"] != model:
            raise LiveGatePolicyV32Error("dot parent must be exact model identity")
        seen.add(parent_id)
        normalized_chains.append(dict(chain))
    file_identities = [
        item["identity"]
        for item in [*raw["evidence"]["targets"], *raw["evidence"]["sentinels"]]
    ]
    file_keys = [
        _identity_key(_identity(x, "governed file identity", directory=False))
        for x in file_identities
    ]
    all_keys = directory_keys + file_keys
    if any(key[0] != volume for key in all_keys):
        raise LiveGatePolicyV32Error("cross-volume rooted topology")
    if len(all_keys) != len(set(all_keys)):
        raise LiveGatePolicyV32Error("root parent or file identity alias")
    if row["all_identity_keys_sha256"] != digest_value(
        [{"volume_serial": volume_key, "file_id": file_id} for volume_key, file_id in all_keys]
    ):
        raise LiveGatePolicyV32Error("topology identity digest drift")
    return {"raw": dict(row), "all_keys": all_keys}


def _validate_enumeration(value: Any, raw: Mapping[str, Any]) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "api_identity",
            "terminal_status",
            "raw_count",
            "rows",
            "rows_sha256",
            "derived_candidate_sha256",
            "opened_evidence_sha256",
        },
        "system enumeration",
    )
    if (
        row["api_identity"] != ENUMERATION_API
        or row["terminal_status"] != ENUMERATION_TERMINAL_STATUS
    ):
        raise LiveGatePolicyV32Error("system enumeration API or terminal status drift")
    rows: list[dict[str, Any]] = []
    pids: set[int] = set()
    for index, item in enumerate(_array(row["rows"], "system rows"), 1):
        item = _closed(
            item,
            {"ordinal", "pid", "parent_pid", "creation_token", "normalized_name"},
            f"system row[{index}]",
        )
        ordinal = _integer(item["ordinal"], "system ordinal", 1)
        pid = _integer(item["pid"], "system pid", 1)
        parent_pid = _integer(item["parent_pid"], "system parent pid")
        name = _text(item["normalized_name"], "system normalized name")
        if ordinal != index or name != name.casefold() or pid in pids:
            raise LiveGatePolicyV32Error("system row order name or PID drift")
        pids.add(pid)
        rows.append(dict(item))
    if _integer(row["raw_count"], "system raw count") != len(rows):
        raise LiveGatePolicyV32Error("system raw count drift")
    if row["rows_sha256"] != digest_value(rows):
        raise LiveGatePolicyV32Error("system enumeration digest drift")
    bounded_pids = {
        item["pid"] for item in rows if item["normalized_name"] in V31.BOUNDED_PROCESS_NAMES
    }
    parent_pids = {item["parent_pid"] for item in rows if item["pid"] in bounded_pids}
    derived = [
        item for item in rows if item["pid"] in bounded_pids or item["pid"] in parent_pids
    ]
    if row["derived_candidate_sha256"] != digest_value(derived):
        raise LiveGatePolicyV32Error("derived bounded candidate digest drift")
    opened = raw["evidence"]["bounded_process_snapshot"]["rows"]
    opened_projection = [
        {
            "ordinal": index,
            "pid": item["pid"],
            "parent_pid": item["parent_pid"],
            "creation_token": item["creation_token"],
            "normalized_name": item["normalized_name"],
        }
        for index, item in enumerate(opened, 1)
    ]
    if derived != opened_projection:
        raise LiveGatePolicyV32Error("every derived candidate must have exact opened evidence")
    if row["opened_evidence_sha256"] != digest_value(opened):
        raise LiveGatePolicyV32Error("opened process evidence digest drift")
    return {"raw": dict(row), "rows": rows, "derived": derived}


def _continuity_projection(raw: Mapping[str, Any], v32: Mapping[str, Any]) -> dict[str, Any]:
    evidence = raw["evidence"]
    enumeration = v32["enumeration"]
    return {
        "base_v3_1_continuity": V31._continuity_from_raw_record(raw),
        "lease_id": v32["lease_id"],
        "boot_identity": v32["boot_identity"],
        "lease_start_wall_utc": v32["lease_start_wall_utc"],
        "lease_start_monotonic_ns": v32["lease_start_monotonic_ns"],
        "rooted_topology": v32["rooted_topology"],
        "system_enumeration": {
            key: enumeration[key]
            for key in (
                "api_identity",
                "terminal_status",
                "raw_count",
                "rows",
                "rows_sha256",
                "derived_candidate_sha256",
            )
        },
        "environment": evidence["environment"],
        "parents": evidence["canonical_parents"],
    }


def _validate_sidecar(
    value: Any,
    raw: Mapping[str, Any],
    *,
    expected_phase: str,
    validation_wall: datetime,
    validation_mono: int,
) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "schema_version",
            "phase",
            "lease_id",
            "boot_identity",
            "lease_start_wall_utc",
            "lease_start_monotonic_ns",
            "rooted_topology",
            "enumeration",
            "observation_attestations",
            "continuity_sha256",
            "candidate_only",
            "non_authorizing",
        },
        "V3.2 evidence",
    )
    if row["schema_version"] != EVIDENCE_SCHEMA or row["phase"] != expected_phase:
        raise LiveGatePolicyV32Error("V3.2 evidence identity or phase drift")
    lease_id = _text(row["lease_id"], "opaque lease ID")
    if _OPAQUE.fullmatch(lease_id) is None:
        raise LiveGatePolicyV32Error("lease ID is not opaque")
    boot_identity = _sha(row["boot_identity"], "V3.2 boot identity")
    if boot_identity != raw["evidence"]["boot"]["boot_identity"]:
        raise LiveGatePolicyV32Error("boot identity drift")
    lease_start_wall = _utc(row["lease_start_wall_utc"], "lease start wall")
    lease_start_mono = _integer(
        row["lease_start_monotonic_ns"], "lease start monotonic"
    )
    capture = raw["evidence"]["capture"]
    capture_start_wall = _utc(capture["start_wall_utc"], "capture start wall")
    capture_start_mono = _integer(capture["start_monotonic_ns"], "capture start mono")
    if lease_start_wall > capture_start_wall or lease_start_mono > capture_start_mono:
        raise LiveGatePolicyV32Error("lease starts after capture")
    wall_elapsed = (validation_wall - lease_start_wall).total_seconds()
    mono_elapsed = (validation_mono - lease_start_mono) / 1_000_000_000
    if (
        wall_elapsed < 0
        or mono_elapsed < 0
        or wall_elapsed > MAX_LEASE_SECONDS
        or mono_elapsed > MAX_LEASE_SECONDS
        or abs(wall_elapsed - mono_elapsed) > MAX_CLOCK_SKEW_SECONDS
    ):
        raise LiveGatePolicyV32Error("whole-lease duration or clock skew drift")
    _validate_topology(row["rooted_topology"], raw)
    _validate_enumeration(row["enumeration"], raw)
    _validate_observations(row["observation_attestations"], raw, row)
    continuity = digest_value(_continuity_projection(raw, row))
    if _sha(row["continuity_sha256"], "canonical continuity hash") != continuity:
        raise LiveGatePolicyV32Error("canonical continuity hash drift")
    if row["candidate_only"] is not True or row["non_authorizing"] is not True:
        raise LiveGatePolicyV32Error("V3.2 authority drift")
    return {
        "raw": dict(row),
        "lease_id": lease_id,
        "boot_identity": boot_identity,
        "lease_start_wall": lease_start_wall,
        "lease_start_mono": lease_start_mono,
        "continuity_sha256": continuity,
    }


def _decorate_result(
    base: Mapping[str, Any], sidecar: Mapping[str, Any], sidecar_sha256: str
) -> dict[str, Any]:
    result = dict(base)
    result.update(
        {
            "schema_version": RESULT_SCHEMA,
            "base_v3_1_result_sha256": digest_value(dict(base)),
            "v3_2_evidence_sha256": sidecar_sha256,
            "lease_id": sidecar["lease_id"],
            "boot_identity": sidecar["boot_identity"],
            "continuity_sha256": sidecar["continuity_sha256"],
            "opaque_lease_verified_by_pure_policy": False,
        }
    )
    return result


def validate_live_gate_policy_v3_2(
    *,
    v3_2_evidence_bytes: bytes,
    expected_v3_2_evidence_sha256: str,
    prepare_v3_2_evidence_bytes: bytes | None = None,
    independently_expected_prepare_v3_2_evidence_sha256: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Validate the frozen V3.1 contract plus every additive V3.2 closure."""
    expected_phase = kwargs.get("expected_phase")
    if expected_phase not in {"prepare", "publish"}:
        raise LiveGatePolicyV32Error("phase must be prepare or publish")
    raw_bytes = kwargs.get("raw_measurement_bytes")
    raw_sha = kwargs.get("expected_raw_measurement_sha256")
    raw = _v31_raw(raw_bytes, raw_sha, "raw measurement")
    _strict_numeric_tree(raw, "raw measurement")
    for byte_key, sha_key, label in (
        ("component_lock_bytes", "expected_component_lock_sha256", "component lock"),
        (
            "execution_freeze_bytes",
            "expected_execution_freeze_sha256",
            "execution freeze",
        ),
    ):
        _strict_numeric_tree(
            _parse_canonical(kwargs.get(byte_key), kwargs.get(sha_key), label), label
        )
    allowlist_bytes = kwargs.get("static_allowlist_bytes")
    if not isinstance(allowlist_bytes, bytes):
        raise LiveGatePolicyV32Error("static allowlist must be bytes")
    try:
        allowlist_object = json.loads(allowlist_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiveGatePolicyV32Error("static allowlist is not UTF-8 JSON") from exc
    _strict_numeric_tree(allowlist_object, "static allowlist")
    _strict_numeric_tree(kwargs.get("capability_scope_projection"), "capability")
    validation_wall = _utc(kwargs.get("validation_wall_time_utc"), "validation wall")
    validation_mono = _integer(
        kwargs.get("validation_monotonic_ns"), "validation monotonic"
    )
    sidecar_raw = _parse_canonical(
        v3_2_evidence_bytes, expected_v3_2_evidence_sha256, "V3.2 evidence"
    )
    _strict_numeric_tree(sidecar_raw, "V3.2 evidence")
    sidecar = _validate_sidecar(
        sidecar_raw,
        raw,
        expected_phase=expected_phase,
        validation_wall=validation_wall,
        validation_mono=validation_mono,
    )

    base_kwargs = dict(kwargs)
    if expected_phase == "prepare":
        if (
            prepare_v3_2_evidence_bytes is not None
            or independently_expected_prepare_v3_2_evidence_sha256 is not None
        ):
            raise LiveGatePolicyV32Error("prepare cannot accept prior V3.2 evidence")
        try:
            base = V31.validate_live_gate_policy_v3_1(**base_kwargs)
        except V31.LiveGatePolicyV31Error as exc:
            raise LiveGatePolicyV32Error(str(exc)) from exc
        return _decorate_result(base, sidecar, expected_v3_2_evidence_sha256)

    if (
        prepare_v3_2_evidence_bytes is None
        or independently_expected_prepare_v3_2_evidence_sha256 is None
    ):
        raise LiveGatePolicyV32Error("publish requires retained prepare V3.2 evidence")
    prepare_raw_bytes = kwargs.get("prepare_raw_measurement_bytes")
    prepare_raw_sha = kwargs.get("independently_expected_prepare_raw_sha256")
    prepare_raw = _v31_raw(prepare_raw_bytes, prepare_raw_sha, "prepare raw measurement")
    _strict_numeric_tree(prepare_raw, "prepare raw measurement")
    prepare_sidecar_raw = _parse_canonical(
        prepare_v3_2_evidence_bytes,
        independently_expected_prepare_v3_2_evidence_sha256,
        "prepare V3.2 evidence",
    )
    _strict_numeric_tree(prepare_sidecar_raw, "prepare V3.2 evidence")

    supplied_prepare_result_bytes = kwargs.get("prepare_result_bytes")
    supplied_prepare_result_sha = kwargs.get(
        "independently_expected_prepare_result_sha256"
    )
    supplied_result = _parse_canonical(
        supplied_prepare_result_bytes, supplied_prepare_result_sha, "prepare result"
    )
    result_validation_wall = _utc(
        supplied_result.get("validated_at_wall_utc"), "prepare result validation wall"
    )
    result_validation_mono = _integer(
        supplied_result.get("validated_at_monotonic_ns"),
        "prepare result validation monotonic",
    )
    prepare_sidecar = _validate_sidecar(
        prepare_sidecar_raw,
        prepare_raw,
        expected_phase="prepare",
        validation_wall=result_validation_wall,
        validation_mono=result_validation_mono,
    )
    base_prepare_kwargs = dict(base_kwargs)
    for key in (
        "prepare_raw_measurement_bytes",
        "independently_expected_prepare_raw_sha256",
        "prepare_result_bytes",
        "independently_expected_prepare_result_sha256",
    ):
        base_prepare_kwargs.pop(key, None)
    base_prepare_kwargs.update(
        {
            "expected_phase": "prepare",
            "raw_measurement_bytes": prepare_raw_bytes,
            "expected_raw_measurement_sha256": prepare_raw_sha,
            "validation_wall_time_utc": supplied_result["validated_at_wall_utc"],
            "validation_monotonic_ns": supplied_result["validated_at_monotonic_ns"],
        }
    )
    try:
        recomputed_base = V31.validate_live_gate_policy_v3_1(**base_prepare_kwargs)
    except V31.LiveGatePolicyV31Error as exc:
        raise LiveGatePolicyV32Error(str(exc)) from exc
    recomputed_v32 = _decorate_result(
        recomputed_base,
        prepare_sidecar,
        independently_expected_prepare_v3_2_evidence_sha256,
    )
    if supplied_result != recomputed_v32:
        raise LiveGatePolicyV32Error("prepare V3.2 result does not recompute exactly")

    base_prepare_bytes = V31.canonical_json_bytes(recomputed_base)
    base_prepare_sha = V31.digest_bytes(base_prepare_bytes)
    base_kwargs["prepare_result_bytes"] = base_prepare_bytes
    base_kwargs["independently_expected_prepare_result_sha256"] = base_prepare_sha
    # The frozen V3.1 publish raw causally names its V3.1 prepare result.
    causal = raw["evidence"]["causal_parent"]
    if causal.get("prepare_result_sha256") != base_prepare_sha:
        raise LiveGatePolicyV32Error("publish base causal result hash drift")
    try:
        base = V31.validate_live_gate_policy_v3_1(**base_kwargs)
    except V31.LiveGatePolicyV31Error as exc:
        raise LiveGatePolicyV32Error(str(exc)) from exc

    if (
        sidecar["lease_id"] != prepare_sidecar["lease_id"]
        or sidecar["boot_identity"] != prepare_sidecar["boot_identity"]
        or sidecar["lease_start_wall"] != prepare_sidecar["lease_start_wall"]
        or sidecar["lease_start_mono"] != prepare_sidecar["lease_start_mono"]
    ):
        raise LiveGatePolicyV32Error("same opaque lease or boot continuity drift")
    if sidecar["continuity_sha256"] != prepare_sidecar["continuity_sha256"]:
        raise LiveGatePolicyV32Error("prepare/publish canonical continuity hash drift")
    prepare_validation_wall = result_validation_wall
    prepare_validation_mono = result_validation_mono
    publish_capture = raw["evidence"]["capture"]
    publish_start_wall = _utc(publish_capture["start_wall_utc"], "publish start wall")
    publish_start_mono = _integer(
        publish_capture["start_monotonic_ns"], "publish start monotonic"
    )
    gap_wall = (publish_start_wall - prepare_validation_wall).total_seconds()
    gap_mono = (publish_start_mono - prepare_validation_mono) / 1_000_000_000
    if (
        gap_wall < 0
        or gap_mono < 0
        or abs(gap_wall - gap_mono) > MAX_CLOCK_SKEW_SECONDS
    ):
        raise LiveGatePolicyV32Error("interphase dual-clock duration or skew drift")
    return _decorate_result(base, sidecar, expected_v3_2_evidence_sha256)


# A narrow helper used only to derive continuity from already parsed exact V3.1 raw.
def _install_v31_projection_helper() -> None:
    if hasattr(V31, "_continuity_from_raw_record"):
        return

    def helper(raw: Mapping[str, Any]) -> dict[str, Any]:
        evidence = raw["evidence"]
        target_fields = (
            "ordinal", "target_id", "role", "operation", "path_token", "parent_id",
            "parent_identity", "leaf_name", "identity", "size_bytes", "ntfs_link_count",
            "expected_preimage_size_bytes", "expected_staged_size_bytes",
            "expected_preimage_sha256", "expected_staged_sha256", "observed_sha256",
            "root_relative_opened", "replacement_requested", "mutation_observed",
        )
        sentinel_fields = (
            "ordinal", "sentinel_id", "role", "path_token", "parent_id",
            "parent_identity", "leaf_name", "identity", "size_bytes", "ntfs_link_count",
            "expected_sha256", "observed_sha256", "root_relative_opened",
            "replacement_requested", "mutation_observed",
        )
        process_fields = (
            "pid", "parent_pid", "creation_token", "normalized_name",
            "process_handle_access", "liveness_status", "executable",
        )
        snapshot = evidence["bounded_process_snapshot"]
        snapshot_fields = tuple(
            key for key in snapshot if key not in {"rows"}
        )
        rows = snapshot["rows"]
        by_pid = {item["pid"]: item for item in rows}
        return {
            "boot": evidence["boot"],
            "environment": evidence["environment"],
            "parents": evidence["canonical_parents"],
            "targets": [
                {key: item[key] for key in target_fields} for item in evidence["targets"]
            ],
            "sentinels": [
                {key: item[key] for key in sentinel_fields}
                for item in evidence["sentinels"]
            ],
            "process_snapshot": {key: snapshot[key] for key in snapshot_fields},
            "process_rows": [
                {key: item[key] for key in process_fields} for item in rows
            ],
            "current": {
                key: by_pid[snapshot["current_pid"]][key] for key in process_fields
            },
            "controller": {
                key: by_pid[snapshot["controller_pid"]][key] for key in process_fields
            },
        }

    V31._continuity_from_raw_record = helper


_install_v31_projection_helper()
validate_live_gate = validate_live_gate_policy_v3_2
