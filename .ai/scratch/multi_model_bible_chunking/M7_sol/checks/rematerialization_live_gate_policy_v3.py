#!/usr/bin/env python3
"""Pure V3 machine-precondition policy for T550 Hosea.

The caller supplies canonical JSON bytes and detached hashes.  This module does
not read a host, a clock, a process, or a file; authenticate a human; create a
live lease; or authorize an effect.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import PurePosixPath
import re
from typing import Any, Mapping


SCHEMA_VERSION = "t550.rematerialization_live_gate_policy.v3"
COMPONENT_SCHEMA = "t550.v9_component_lock.v3"
FREEZE_SCHEMA = "t550.v9_execution_freeze.v3"
RAW_SCHEMA = "t550.windows_live_environment_raw_record.v3"
RESULT_SCHEMA = "t550.v9_machine_precondition_result.v3"
SUCCESS_LABEL = "MACHINE_PRECONDITIONS_PASS_HUMAN_GATE_UNVERIFIED"
CONTRACT_SHA256 = "28b503b96b6790d65c72685caa4d6c63ea68a6cfb4473dddb5612d0c60d71b22"
POLICY_DOCKET_SHA256 = "142b322c9d647da9290743d2676244008f7694e2375f45073318285ca7943a46"
WINDOWS_DOCKET_SHA256 = "a2f7944cb33161457d7f092631046c1608ed7c6be8422c04800ec9c56dc781bd"
V2_REJECTION_SHA256 = "24546d7abddf881e5fdb7fff872dc3cb386ad81c2b8bdee04147badfa66f9c2f"
DESIGN_BOSS_RULING_SHA256 = "67af1a7766947172c0197b58a161d3a6af669010d1ff9c68dac59b9b8e4fa6ee"
CORRECTED_DESIGN_RESOLUTION_SHA256 = "e5a727f849ff242079151722dd93fd214a34bf0e40de6be6c01b6c811c301e85"
CORRECTED_DESIGN_BOSS_CHECK_SHA256 = "9963403f8e639c1765ca28151df2e06c34d07b26a51b83e9ca19b5507425f7f8"
MAX_LEASE_SECONDS = 120
TARGET_COUNT = 13
SENTINEL_COUNT = 3

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
PERMITTED_CONTROLLER_NAMES = ("codex.exe", "powershell.exe", "pwsh.exe")
REQUIRED_DEPENDENCY_IDS = {
    "contract",
    "corrected_design_boss_check",
    "corrected_design_resolution",
    "design_boss_ruling",
    "live_instance_checker",
    "policy",
    "production_collector",
    "production_wrapper",
    "rooted_replace_primitive",
    "transaction_kernel",
    "v2_rejection",
    "v3_policy_docket",
    "v3_windows_docket",
}
DENIED_EFFECTS = [
    "comparison",
    "commit",
    "global_sidecars",
    "merge",
    "promotion",
    "push",
]
OUTSIDE_POLICY_REQUIREMENTS = [
    "corrected_design_and_fresh_design_consistency_review",
    "external_owner_capability_verification",
    "independent_checker_and_boss_provenance",
    "opaque_in_process_handle_lease",
    "trusted_independent_prepare_digest_retention",
    "windows_handle_measurement_and_revalidation",
]
MACHINE_BLOCKERS = [
    "EXTERNAL_OWNER_CAPABILITY_UNAVAILABLE_TO_PURE_POLICY",
    "OPAQUE_IN_PROCESS_LEASE_UNAVAILABLE_TO_PURE_POLICY",
    "REVIEWED_RELEASE_ORIGIN_UNVERIFIED_BY_PURE_POLICY",
]

_SHA = re.compile(r"^[0-9a-f]{64}$")


class LiveGatePolicyV3Error(ValueError):
    pass


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
        raise LiveGatePolicyV3Error("value is not canonical JSON") from exc


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_value(value: Any) -> str:
    return digest_bytes(canonical_json_bytes(value))


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LiveGatePolicyV3Error(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_canonical_bytes(
    raw: Any, expected_sha256: str, label: str
) -> dict[str, Any]:
    if not isinstance(raw, bytes):
        raise LiveGatePolicyV3Error(f"{label} must be bytes")
    _sha(expected_sha256, f"expected {label} SHA-256")
    if digest_bytes(raw) != expected_sha256:
        raise LiveGatePolicyV3Error(f"{label} detached hash drift")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiveGatePolicyV3Error(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise LiveGatePolicyV3Error(f"{label} must contain an object")
    if canonical_json_bytes(value) != raw:
        raise LiveGatePolicyV3Error(f"{label} is not exact canonical bytes")
    return value


def _closed(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveGatePolicyV3Error(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        raise LiveGatePolicyV3Error(
            f"{label} schema drift missing={sorted(keys-actual)} "
            f"extra={sorted(actual-keys)}"
        )
    return value


def _list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise LiveGatePolicyV3Error(f"{label} must be an ordered array")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise LiveGatePolicyV3Error(f"{label} must be non-empty text")
    return value


def _sha(value: Any, label: str) -> str:
    text = _text(value, label)
    if _SHA.fullmatch(text) is None:
        raise LiveGatePolicyV3Error(f"{label} must be lowercase SHA-256")
    return text


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise LiveGatePolicyV3Error(f"{label} must be integer >= {minimum}")
    return value


def _boolean(value: Any, expected: bool, label: str) -> None:
    if value is not expected:
        raise LiveGatePolicyV3Error(f"{label} must be {expected}")


def _utc(value: Any, label: str) -> datetime:
    text = _text(value, label)
    try:
        result = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LiveGatePolicyV3Error(f"{label} must be ISO-8601") from exc
    if result.tzinfo is None or result.utcoffset() != timezone.utc.utcoffset(result):
        raise LiveGatePolicyV3Error(f"{label} must identify UTC")
    return result.astimezone(timezone.utc)


def _identity(value: Any, label: str, *, directory: bool) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "volume_serial",
            "file_id",
            "attributes",
            "is_directory",
            "reparse_point",
        },
        label,
    )
    _integer(row["volume_serial"], f"{label}.volume_serial")
    _text(row["file_id"], f"{label}.file_id")
    _integer(row["attributes"], f"{label}.attributes")
    _boolean(row["is_directory"], directory, f"{label}.is_directory")
    _boolean(row["reparse_point"], False, f"{label}.reparse_point")
    return dict(row)


def _identity_key(identity: Mapping[str, Any]) -> tuple[int, str]:
    return identity["volume_serial"], identity["file_id"]


def _token(value: Any, label: str) -> tuple[str, str, str]:
    token = _text(value, label)
    if (
        "\\" in token
        or token.startswith("/")
        or token.endswith("/")
        or ":" in token
    ):
        raise LiveGatePolicyV3Error(f"{label} is not normalized model-relative")
    path = PurePosixPath(token)
    if any(part in ("", ".", "..") or part.endswith((" ", ".")) for part in path.parts):
        raise LiveGatePolicyV3Error(f"{label} has ambiguous components")
    rendered = path.as_posix()
    if rendered != token or len(path.parts) < 2:
        raise LiveGatePolicyV3Error(f"{label} is not canonical")
    return token, path.parent.as_posix(), path.name


def _artifact_rows(value: Any, label: str) -> list[dict[str, str]]:
    rows = _list(value, label)
    result = []
    for index, raw in enumerate(rows):
        row = _closed(raw, {"artifact_id", "sha256"}, f"{label}[{index}]")
        result.append(
            {
                "artifact_id": _text(row["artifact_id"], "artifact_id"),
                "sha256": _sha(row["sha256"], "artifact sha256"),
            }
        )
    ids = [row["artifact_id"] for row in result]
    if ids != sorted(set(ids)):
        raise LiveGatePolicyV3Error(f"{label} IDs must be sorted and unique")
    return result


def _validate_component(value: Any) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "schema_version",
            "generation_id",
            "contract_sha256",
            "policy_docket_sha256",
            "windows_docket_sha256",
            "v2_rejection_sha256",
            "design_boss_ruling_sha256",
            "corrected_design_resolution_sha256",
            "corrected_design_boss_check_sha256",
            "hash_topology",
            "review_timing_policy",
            "dependencies",
            "bounded_process_names",
            "bounded_process_policy_sha256",
            "candidate_only",
            "non_authorizing",
        },
        "component_lock",
    )
    if row["schema_version"] != COMPONENT_SCHEMA:
        raise LiveGatePolicyV3Error("component schema drift")
    expected_constants = {
        "contract_sha256": CONTRACT_SHA256,
        "policy_docket_sha256": POLICY_DOCKET_SHA256,
        "windows_docket_sha256": WINDOWS_DOCKET_SHA256,
        "v2_rejection_sha256": V2_REJECTION_SHA256,
        "design_boss_ruling_sha256": DESIGN_BOSS_RULING_SHA256,
        "corrected_design_resolution_sha256": CORRECTED_DESIGN_RESOLUTION_SHA256,
        "corrected_design_boss_check_sha256": CORRECTED_DESIGN_BOSS_CHECK_SHA256,
    }
    for key, expected in expected_constants.items():
        if row[key] != expected:
            raise LiveGatePolicyV3Error(f"component {key} drift")
    _text(row["generation_id"], "component generation_id")
    topology = _closed(
        row["hash_topology"],
        {
            "external_trust_anchor_kind",
            "component_lock_contains_own_digest",
            "component_lock_contains_post_component_review_hashes",
            "execution_freeze_contains_own_digest",
            "runtime_capability_supplies_execution_freeze_digest",
        },
        "component hash_topology",
    )
    if topology["external_trust_anchor_kind"] != "product_runtime_detached_digest_api":
        raise LiveGatePolicyV3Error("external trust anchor drift")
    for key, expected in {
        "component_lock_contains_own_digest": False,
        "component_lock_contains_post_component_review_hashes": False,
        "execution_freeze_contains_own_digest": False,
        "runtime_capability_supplies_execution_freeze_digest": True,
    }.items():
        _boolean(topology[key], expected, f"hash_topology.{key}")
    timing = _closed(
        row["review_timing_policy"],
        {
            "static_reviews_before_restart",
            "live_instance_checker_inside_lease",
            "human_or_async_wait_inside_lease",
        },
        "component review_timing_policy",
    )
    _boolean(timing["static_reviews_before_restart"], True, "static review timing")
    _boolean(timing["live_instance_checker_inside_lease"], True, "live checker timing")
    _boolean(timing["human_or_async_wait_inside_lease"], False, "async wait timing")
    dependencies = _artifact_rows(row["dependencies"], "component dependencies")
    if not REQUIRED_DEPENDENCY_IDS.issubset(
        {item["artifact_id"] for item in dependencies}
    ):
        raise LiveGatePolicyV3Error("component dependency set is incomplete")
    dependency_map = {item["artifact_id"]: item["sha256"] for item in dependencies}
    if dependency_map["design_boss_ruling"] != DESIGN_BOSS_RULING_SHA256:
        raise LiveGatePolicyV3Error("design boss ruling dependency drift")
    if dependency_map["corrected_design_resolution"] != CORRECTED_DESIGN_RESOLUTION_SHA256:
        raise LiveGatePolicyV3Error("corrected design resolution dependency drift")
    if dependency_map["corrected_design_boss_check"] != CORRECTED_DESIGN_BOSS_CHECK_SHA256:
        raise LiveGatePolicyV3Error("corrected design boss check dependency drift")
    if tuple(row["bounded_process_names"]) != BOUNDED_PROCESS_NAMES:
        raise LiveGatePolicyV3Error("bounded process policy is caller-omittable")
    if row["bounded_process_policy_sha256"] != digest_value(
        list(BOUNDED_PROCESS_NAMES)
    ):
        raise LiveGatePolicyV3Error("bounded process policy digest drift")
    _boolean(row["candidate_only"], True, "component candidate_only")
    _boolean(row["non_authorizing"], True, "component non_authorizing")
    return {"raw": dict(row), "dependencies": dependencies}


def _freeze_identity_rows(
    value: Any, label: str, *, directory: bool
) -> list[dict[str, Any]]:
    rows = _list(value, label)
    result = []
    for index, raw in enumerate(rows, 1):
        row = _closed(
            raw,
            {"ordinal", "id", "path_token", "identity"},
            f"{label}[{index - 1}]",
        )
        if row["ordinal"] != index:
            raise LiveGatePolicyV3Error(f"{label} order drift")
        token, _, _ = _token(row["path_token"], f"{label}.path_token")
        result.append(
            {
                "ordinal": index,
                "id": _text(row["id"], f"{label}.id"),
                "path_token": token,
                "identity": _identity(
                    row["identity"], f"{label}.identity", directory=directory
                ),
            }
        )
    if len({row["id"] for row in result}) != len(result):
        raise LiveGatePolicyV3Error(f"{label} IDs are not unique")
    return result


def _freeze_files(
    value: Any, label: str, *, target: bool
) -> list[dict[str, Any]]:
    expected_count = TARGET_COUNT if target else SENTINEL_COUNT
    rows = _list(value, label)
    if len(rows) != expected_count:
        raise LiveGatePolicyV3Error(f"{label} must contain {expected_count} rows")
    keys = {
        "ordinal",
        "id",
        "role",
        "path_token",
        "parent_id",
        "leaf_name",
        "identity",
        "size_bytes",
        "ntfs_link_count",
        "preimage_sha256",
        "staged_sha256",
    } if target else {
        "ordinal",
        "id",
        "role",
        "path_token",
        "parent_id",
        "leaf_name",
        "identity",
        "size_bytes",
        "ntfs_link_count",
        "expected_sha256",
    }
    result = []
    for ordinal, raw in enumerate(rows, 1):
        row = _closed(raw, keys, f"{label}[{ordinal - 1}]")
        if row["ordinal"] != ordinal:
            raise LiveGatePolicyV3Error(f"{label} order drift")
        token, parent_token, leaf = _token(row["path_token"], f"{label}.path_token")
        if row["leaf_name"] != leaf:
            raise LiveGatePolicyV3Error(f"{label} leaf/token drift")
        item = {
            "ordinal": ordinal,
            "id": _text(row["id"], f"{label}.id"),
            "role": _text(row["role"], f"{label}.role"),
            "path_token": token,
            "parent_token": parent_token,
            "parent_id": _text(row["parent_id"], f"{label}.parent_id"),
            "leaf_name": leaf,
            "identity": _identity(
                row["identity"], f"{label}.identity", directory=False
            ),
            "size_bytes": _integer(row["size_bytes"], f"{label}.size_bytes"),
            "ntfs_link_count": _integer(
                row["ntfs_link_count"], f"{label}.ntfs_link_count", 1
            ),
        }
        if item["ntfs_link_count"] != 1:
            raise LiveGatePolicyV3Error("hardlink count must be exactly one")
        if target:
            item["preimage_sha256"] = _sha(
                row["preimage_sha256"], f"{label}.preimage"
            )
            item["staged_sha256"] = _sha(
                row["staged_sha256"], f"{label}.staged"
            )
            if item["preimage_sha256"] == item["staged_sha256"]:
                raise LiveGatePolicyV3Error("target staged bytes equal preimage")
        else:
            item["expected_sha256"] = _sha(
                row["expected_sha256"], f"{label}.expected"
            )
        result.append(item)
    if len({row["id"] for row in result}) != expected_count:
        raise LiveGatePolicyV3Error(f"{label} IDs are not unique")
    if len({row["path_token"] for row in result}) != expected_count:
        raise LiveGatePolicyV3Error(f"{label} tokens are not unique")
    return result


def _validate_freeze(
    value: Any,
    component_sha256: str,
    reviewed_release_sha256: str,
    capability_reference_sha256: str,
) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "schema_version",
            "task_id",
            "book",
            "application_id",
            "freeze_id",
            "frozen_at_utc",
            "pre_freeze_boot_identity",
            "component_lock_sha256",
            "reviewed_release_sha256",
            "identity_lifetime_policy",
            "targets",
            "target_tuple_sha256",
            "sentinels",
            "sentinel_tuple_sha256",
            "canonical_parents",
            "os_allowlist",
            "volume_allowlist",
            "bounded_process_policy_sha256",
            "capability_reference_sha256",
            "permitted_phases",
            "candidate_only",
            "non_authorizing",
        },
        "execution_freeze",
    )
    if row["schema_version"] != FREEZE_SCHEMA:
        raise LiveGatePolicyV3Error("freeze schema drift")
    if row["task_id"] != "T550" or row["book"] != "Hos":
        raise LiveGatePolicyV3Error("freeze task/book drift")
    _text(row["application_id"], "freeze application_id")
    _text(row["freeze_id"], "freeze freeze_id")
    frozen_at = _utc(row["frozen_at_utc"], "freeze frozen_at_utc")
    _text(row["pre_freeze_boot_identity"], "freeze pre_freeze_boot_identity")
    if row["component_lock_sha256"] != component_sha256:
        raise LiveGatePolicyV3Error("freeze/component detached hash drift")
    if row["reviewed_release_sha256"] != reviewed_release_sha256:
        raise LiveGatePolicyV3Error("freeze/reviewed release detached hash drift")
    lifetime = _closed(
        row["identity_lifetime_policy"],
        {
            "stable_pre_restart_only",
            "ephemeral_pid_start_handle_ancestry_frozen",
            "ephemeral_prepare_publish_continuity_only",
        },
        "freeze identity_lifetime_policy",
    )
    _boolean(lifetime["stable_pre_restart_only"], True, "stable identity policy")
    _boolean(
        lifetime["ephemeral_pid_start_handle_ancestry_frozen"],
        False,
        "ephemeral freeze policy",
    )
    _boolean(
        lifetime["ephemeral_prepare_publish_continuity_only"],
        True,
        "ephemeral continuity policy",
    )
    targets = _freeze_files(row["targets"], "freeze.targets", target=True)
    sentinels = _freeze_files(row["sentinels"], "freeze.sentinels", target=False)
    if row["target_tuple_sha256"] != digest_value(row["targets"]):
        raise LiveGatePolicyV3Error("target tuple digest drift")
    if row["sentinel_tuple_sha256"] != digest_value(row["sentinels"]):
        raise LiveGatePolicyV3Error("sentinel tuple digest drift")
    parents = _freeze_identity_rows(
        row["canonical_parents"], "freeze.canonical_parents", directory=True
    )
    parent_by_id = {item["id"]: item for item in parents}
    parent_keys = [_identity_key(item["identity"]) for item in parents]
    if len(parent_keys) != len(set(parent_keys)):
        raise LiveGatePolicyV3Error("canonical parent identity alias")
    for item in (*targets, *sentinels):
        parent = parent_by_id.get(item["parent_id"])
        if parent is None or parent["path_token"] != item["parent_token"]:
            raise LiveGatePolicyV3Error("frozen parent/token relation drift")
    all_file_keys = [_identity_key(item["identity"]) for item in (*targets, *sentinels)]
    if len(all_file_keys) != TARGET_COUNT + SENTINEL_COUNT or len(
        set(all_file_keys)
    ) != TARGET_COUNT + SENTINEL_COUNT:
        raise LiveGatePolicyV3Error("frozen target/sentinel identity alias")
    os_allow = _closed(
        row["os_allowlist"],
        {"name", "build", "native_architecture", "runtime_architecture"},
        "freeze.os_allowlist",
    )
    if os_allow["name"] != "Windows":
        raise LiveGatePolicyV3Error("freeze must require Windows")
    for key in ("build", "native_architecture", "runtime_architecture"):
        _text(os_allow[key], f"freeze os {key}")
    volume_allow = _closed(
        row["volume_allowlist"],
        {
            "volume_guid",
            "volume_serial",
            "filesystem",
            "filesystem_flags",
            "volume_root_identity",
            "workspace_identity",
            "model_identity",
        },
        "freeze.volume_allowlist",
    )
    _text(volume_allow["volume_guid"], "freeze volume_guid")
    _integer(volume_allow["volume_serial"], "freeze volume_serial")
    if volume_allow["filesystem"] != "NTFS":
        raise LiveGatePolicyV3Error("freeze must require NTFS")
    flags = _list(volume_allow["filesystem_flags"], "freeze filesystem_flags")
    if not flags or flags != sorted(set(flags)):
        raise LiveGatePolicyV3Error("freeze filesystem_flags drift")
    for key in ("volume_root_identity", "workspace_identity", "model_identity"):
        identity = _identity(
            volume_allow[key], f"freeze.{key}", directory=True
        )
        if identity["volume_serial"] != volume_allow["volume_serial"]:
            raise LiveGatePolicyV3Error(f"freeze {key} volume drift")
    root_keys = [
        _identity_key(volume_allow[key])
        for key in ("volume_root_identity", "workspace_identity", "model_identity")
    ]
    if len(set(root_keys)) != 3:
        raise LiveGatePolicyV3Error("freeze root identity alias")
    if row["bounded_process_policy_sha256"] != digest_value(
        list(BOUNDED_PROCESS_NAMES)
    ):
        raise LiveGatePolicyV3Error("freeze process policy drift")
    if row["capability_reference_sha256"] != capability_reference_sha256:
        raise LiveGatePolicyV3Error("freeze capability reference drift")
    if row["permitted_phases"] != ["prepare", "publish", "rollback_only_recovery"]:
        raise LiveGatePolicyV3Error("freeze permitted phases drift")
    _boolean(row["candidate_only"], True, "freeze candidate_only")
    _boolean(row["non_authorizing"], True, "freeze non_authorizing")
    return {
        "raw": dict(row),
        "frozen_at": frozen_at,
        "targets": targets,
        "sentinels": sentinels,
        "parents": parents,
        "parent_by_id": parent_by_id,
        "os": dict(os_allow),
        "volume": dict(volume_allow),
    }


def _validate_capability(
    value: Any,
    expected_reference_sha256: str,
    freeze: Mapping[str, Any],
    validation_wall: datetime,
) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "reference_sha256",
            "asserted_principal",
            "task_id",
            "book",
            "application_id",
            "execution_freeze_sha256",
            "reviewed_release_sha256",
            "target_tuple_sha256",
            "sentinel_tuple_sha256",
            "permitted_phases",
            "issued_at_utc",
            "expires_at_utc",
            "identity_assurance",
            "local_json_alone_sufficient",
            "denied_effects",
        },
        "capability_scope_projection",
    )
    if row["reference_sha256"] != expected_reference_sha256:
        raise LiveGatePolicyV3Error("capability reference drift")
    if row["asserted_principal"] != "Lowell Wong":
        raise LiveGatePolicyV3Error("capability asserted principal drift")
    if (
        row["task_id"] != "T550"
        or row["book"] != "Hos"
        or row["application_id"] != freeze["raw"]["application_id"]
        or row["execution_freeze_sha256"] != digest_value(freeze["raw"])
        or row["reviewed_release_sha256"] != freeze["raw"]["reviewed_release_sha256"]
        or row["target_tuple_sha256"] != freeze["raw"]["target_tuple_sha256"]
        or row["sentinel_tuple_sha256"] != freeze["raw"]["sentinel_tuple_sha256"]
    ):
        raise LiveGatePolicyV3Error("capability scope drift")
    if row["permitted_phases"] != ["prepare", "publish", "rollback_only_recovery"]:
        raise LiveGatePolicyV3Error("capability phases drift")
    issued = _utc(row["issued_at_utc"], "capability issued_at_utc")
    expires = _utc(row["expires_at_utc"], "capability expires_at_utc")
    if not (issued <= validation_wall < expires):
        raise LiveGatePolicyV3Error("capability descriptive scope is stale")
    if row["identity_assurance"] != "external_unverified_by_pure_policy":
        raise LiveGatePolicyV3Error("capability identity overclaim")
    _boolean(
        row["local_json_alone_sufficient"],
        False,
        "capability local_json_alone_sufficient",
    )
    if row["denied_effects"] != DENIED_EFFECTS:
        raise LiveGatePolicyV3Error("capability denied effects drift")
    return dict(row)


def _observation(
    wall: Any,
    mono: Any,
    capture: Mapping[str, Any],
    label: str,
) -> None:
    observed_wall = _utc(wall, f"{label}.wall")
    observed_mono = _integer(mono, f"{label}.mono")
    if not (
        capture["start_wall"] <= observed_wall <= capture["end_wall"]
        and capture["start_mono"] <= observed_mono <= capture["end_mono"]
    ):
        raise LiveGatePolicyV3Error(f"{label} outside capture")


def _raw_file_rows(
    value: Any,
    frozen: list[dict[str, Any]],
    parents: Mapping[str, Any],
    capture: Mapping[str, Any],
    *,
    target: bool,
) -> list[dict[str, Any]]:
    label = "raw.targets" if target else "raw.sentinels"
    rows = _list(value, label)
    if len(rows) != len(frozen):
        raise LiveGatePolicyV3Error(f"{label} count drift")
    keys = {
        "ordinal",
        "id",
        "role",
        "path_token",
        "parent_id",
        "parent_identity",
        "leaf_name",
        "identity",
        "size_bytes",
        "ntfs_link_count",
        "expected_preimage_sha256",
        "expected_staged_sha256",
        "observed_sha256",
        "root_relative_opened",
        "observation_wall_utc",
        "observation_monotonic_ns",
    } if target else {
        "ordinal",
        "id",
        "role",
        "path_token",
        "parent_id",
        "parent_identity",
        "leaf_name",
        "identity",
        "size_bytes",
        "ntfs_link_count",
        "expected_sha256",
        "observed_sha256",
        "root_relative_opened",
        "observation_wall_utc",
        "observation_monotonic_ns",
    }
    result = []
    for index, (raw, expected) in enumerate(zip(rows, frozen, strict=True)):
        row = _closed(raw, keys, f"{label}[{index}]")
        for key in ("ordinal", "id", "role", "path_token", "parent_id", "leaf_name"):
            if row[key] != expected[key]:
                raise LiveGatePolicyV3Error(f"{label} {key} allowlist drift")
        parent = parents[expected["parent_id"]]
        if row["parent_identity"] != parent["identity"]:
            raise LiveGatePolicyV3Error(f"{label} parent identity drift")
        identity = _identity(row["identity"], f"{label}.identity", directory=False)
        if identity != expected["identity"]:
            raise LiveGatePolicyV3Error(f"{label} file identity drift")
        if row["size_bytes"] != expected["size_bytes"]:
            raise LiveGatePolicyV3Error(f"{label} size drift")
        if row["ntfs_link_count"] != 1 or row["ntfs_link_count"] != expected["ntfs_link_count"]:
            raise LiveGatePolicyV3Error(f"{label} hardlink count drift")
        if target:
            if (
                row["expected_preimage_sha256"] != expected["preimage_sha256"]
                or row["expected_staged_sha256"] != expected["staged_sha256"]
                or row["observed_sha256"] != expected["preimage_sha256"]
            ):
                raise LiveGatePolicyV3Error("target byte allowlist drift")
        elif (
            row["expected_sha256"] != expected["expected_sha256"]
            or row["observed_sha256"] != expected["expected_sha256"]
        ):
            raise LiveGatePolicyV3Error("sentinel byte allowlist drift")
        _boolean(row["root_relative_opened"], True, f"{label} root_relative_opened")
        _observation(
            row["observation_wall_utc"],
            row["observation_monotonic_ns"],
            capture,
            label,
        )
        result.append(dict(row))
    return result


def _process_rows(
    value: Any,
    observer: Mapping[str, Any],
    capture: Mapping[str, Any],
) -> dict[str, Any]:
    rows = _list(value, "raw.processes")
    normalized = []
    seen_pid: set[int] = set()
    seen_identity: set[tuple[int, str]] = set()
    for index, raw in enumerate(rows):
        row = _closed(
            raw,
            {
                "pid",
                "parent_pid",
                "normalized_name",
                "start_token",
                "executable_identity",
                "access_status",
                "liveness_wait_result",
                "executable_handle_identity_available",
                "classification_status",
                "observation_wall_utc",
                "observation_monotonic_ns",
            },
            f"raw.processes[{index}]",
        )
        pid = _integer(row["pid"], "process pid", 1)
        parent_pid = _integer(row["parent_pid"], "process parent_pid")
        name = _text(row["normalized_name"], "process normalized_name").casefold()
        if name != row["normalized_name"] or not name.endswith(".exe"):
            raise LiveGatePolicyV3Error("process name is not normalized")
        start = _text(row["start_token"], "process start_token")
        executable = _text(row["executable_identity"], "process executable_identity")
        if row["access_status"] != "opened_query_handle":
            raise LiveGatePolicyV3Error("process access uncertainty")
        if row["liveness_wait_result"] != "WAIT_TIMEOUT_RUNNING":
            raise LiveGatePolicyV3Error("process exited or liveness uncertain")
        _boolean(
            row["executable_handle_identity_available"],
            True,
            "process executable handle identity available",
        )
        if row["classification_status"] != "classified_by_code_fixed_policy":
            raise LiveGatePolicyV3Error("process classification uncertainty")
        if pid in seen_pid or (pid, start) in seen_identity:
            raise LiveGatePolicyV3Error("duplicate or contradictory process identity")
        seen_pid.add(pid)
        seen_identity.add((pid, start))
        _observation(
            row["observation_wall_utc"],
            row["observation_monotonic_ns"],
            capture,
            "process observation",
        )
        normalized.append(dict(row))
    current = [
        item
        for item in normalized
        if item["pid"] == observer["pid"]
        and item["start_token"] == observer["start_token"]
        and item["executable_identity"] == observer["executable_identity"]
    ]
    if len(current) != 1:
        raise LiveGatePolicyV3Error("current process identity is not exact")
    current_row = current[0]
    by_pid = {item["pid"]: item for item in normalized}
    parent = by_pid.get(current_row["parent_pid"])
    if parent is None:
        raise LiveGatePolicyV3Error("current parent process is not exact")
    if parent["normalized_name"] not in PERMITTED_CONTROLLER_NAMES:
        raise LiveGatePolicyV3Error("parent process is not a permitted controller")
    controllers = [parent]
    if parent["normalized_name"] in ("powershell.exe", "pwsh.exe"):
        codex_parent = by_pid.get(parent["parent_pid"])
        if codex_parent is None or codex_parent["normalized_name"] != "codex.exe":
            raise LiveGatePolicyV3Error(
                "shell controller is not directly hosted by exact Codex parent"
            )
        controllers.append(codex_parent)
    elif parent["normalized_name"] != "codex.exe":
        raise LiveGatePolicyV3Error("controller ancestry shape is not permitted")
    permitted_pids = {
        current_row["pid"],
        *(item["pid"] for item in controllers),
    }
    onedrive = [
        item for item in normalized if item["normalized_name"] == "onedrive.exe"
    ]
    blockers = [
        item
        for item in normalized
        if item["normalized_name"] in BOUNDED_PROCESS_NAMES
        and item["pid"] not in permitted_pids
    ]
    if onedrive:
        raise LiveGatePolicyV3Error("derived OneDrive blocker set is nonempty")
    if blockers:
        raise LiveGatePolicyV3Error("derived writer blocker set is nonempty")
    return {
        "rows": normalized,
        "current": current_row,
        "parent": parent,
        "permitted_controllers": controllers,
        "derived_onedrive": onedrive,
        "derived_blockers": blockers,
    }


def _validate_raw(
    value: Any,
    component: Mapping[str, Any],
    component_sha256: str,
    freeze: Mapping[str, Any],
    phase: str,
    validation_wall: datetime,
    validation_mono: int,
) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "schema_version",
            "provenance",
            "evidence_class",
            "live_instance_checker",
            "task_id",
            "book",
            "application_id",
            "phase",
            "capture",
            "boot",
            "operating_system",
            "volume",
            "workspace_identity",
            "model_identity",
            "canonical_parents",
            "targets",
            "sentinels",
            "observer_process_identity",
            "processes",
            "bounded_process_policy_sha256",
            "effects",
            "limitations",
            "candidate_only",
            "non_authorizing",
        },
        "raw_record",
    )
    if row["schema_version"] != RAW_SCHEMA:
        raise LiveGatePolicyV3Error("raw schema drift")
    if row["evidence_class"] != "read_only_collector_zero_delta":
        raise LiveGatePolicyV3Error("synthetic and read-only evidence classes are conflated")
    if (
        row["task_id"] != "T550"
        or row["book"] != "Hos"
        or row["application_id"] != freeze["raw"]["application_id"]
        or row["phase"] != phase
    ):
        raise LiveGatePolicyV3Error("raw scope or phase drift")
    provenance = _closed(
        row["provenance"],
        {
            "mode",
            "production_collector_sha256",
            "component_lock_sha256",
            "loaded_dependencies",
            "provider_injection_available",
            "test_backend_available",
        },
        "raw.provenance",
    )
    if provenance["mode"] != "actual_windows_ntfs_sealed_v3":
        raise LiveGatePolicyV3Error("raw production provenance drift")
    if provenance["component_lock_sha256"] != component_sha256:
        raise LiveGatePolicyV3Error("raw component lock drift")
    loaded = _artifact_rows(
        provenance["loaded_dependencies"], "raw loaded_dependencies"
    )
    if loaded != component["dependencies"]:
        raise LiveGatePolicyV3Error("raw dependency set drift")
    collector = {
        item["artifact_id"]: item["sha256"] for item in loaded
    }.get("production_collector")
    if provenance["production_collector_sha256"] != collector:
        raise LiveGatePolicyV3Error("raw collector hash drift")
    _boolean(
        provenance["provider_injection_available"],
        False,
        "provider injection available",
    )
    _boolean(provenance["test_backend_available"], False, "test backend available")
    capture_row = _closed(
        row["capture"],
        {
            "capture_id",
            "start_wall_utc",
            "end_wall_utc",
            "start_monotonic_ns",
            "end_monotonic_ns",
            "max_duration_seconds",
        },
        "raw.capture",
    )
    _text(capture_row["capture_id"], "capture_id")
    start_wall = _utc(capture_row["start_wall_utc"], "capture start wall")
    end_wall = _utc(capture_row["end_wall_utc"], "capture end wall")
    start_mono = _integer(capture_row["start_monotonic_ns"], "capture start mono")
    end_mono = _integer(capture_row["end_monotonic_ns"], "capture end mono")
    maximum = _integer(capture_row["max_duration_seconds"], "capture maximum", 1)
    wall_duration = (end_wall - start_wall).total_seconds()
    mono_duration = (end_mono - start_mono) / 1_000_000_000
    wall_age = (validation_wall - end_wall).total_seconds()
    mono_age = (validation_mono - end_mono) / 1_000_000_000
    if (
        maximum > MAX_LEASE_SECONDS
        or not 0 <= wall_duration <= maximum
        or not 0 <= mono_duration <= maximum
        or abs(wall_duration - mono_duration) > 1
        or not 0 <= wall_age <= maximum
        or not 0 <= mono_age <= maximum
        or abs(wall_age - mono_age) > 1
    ):
        raise LiveGatePolicyV3Error("dual-clock lease drift")
    capture = {
        "start_wall": start_wall,
        "end_wall": end_wall,
        "start_mono": start_mono,
        "end_mono": end_mono,
    }
    live_checker = _closed(
        row["live_instance_checker"],
        {
            "checker_id",
            "checker_sha256",
            "status",
            "start_wall_utc",
            "end_wall_utc",
            "start_monotonic_ns",
            "end_monotonic_ns",
        },
        "raw.live_instance_checker",
    )
    if live_checker["checker_id"] != "live_instance_checker":
        raise LiveGatePolicyV3Error("live checker ID drift")
    dependency_map = {
        item["artifact_id"]: item["sha256"] for item in component["dependencies"]
    }
    if live_checker["checker_sha256"] != dependency_map["live_instance_checker"]:
        raise LiveGatePolicyV3Error("live checker dependency drift")
    if live_checker["status"] != "PASS_BOUNDED_READ_ONLY":
        raise LiveGatePolicyV3Error("live checker did not pass inside lease")
    _observation(
        live_checker["start_wall_utc"],
        live_checker["start_monotonic_ns"],
        capture,
        "live checker start",
    )
    _observation(
        live_checker["end_wall_utc"],
        live_checker["end_monotonic_ns"],
        capture,
        "live checker end",
    )
    boot = _closed(
        row["boot"], {"boot_identity", "boot_time_utc"}, "raw.boot"
    )
    boot_time = _utc(boot["boot_time_utc"], "boot time")
    if (
        boot["boot_identity"] == freeze["raw"]["pre_freeze_boot_identity"]
        or not freeze["frozen_at"] < boot_time <= start_wall
    ):
        raise LiveGatePolicyV3Error("restart-after-freeze chronology drift")
    os_row = _closed(
        row["operating_system"],
        {"name", "build", "native_architecture", "runtime_architecture"},
        "raw.operating_system",
    )
    if dict(os_row) != freeze["os"]:
        raise LiveGatePolicyV3Error("OS build/architecture drift")
    volume = _closed(
        row["volume"],
        {
            "volume_guid",
            "volume_serial",
            "filesystem",
            "filesystem_flags",
            "volume_root_identity",
        },
        "raw.volume",
    )
    expected_volume = freeze["volume"]
    for key in ("volume_guid", "volume_serial", "filesystem", "filesystem_flags"):
        if volume[key] != expected_volume[key]:
            raise LiveGatePolicyV3Error(f"volume {key} drift")
    if _identity(
        volume["volume_root_identity"], "raw volume root", directory=True
    ) != expected_volume["volume_root_identity"]:
        raise LiveGatePolicyV3Error("volume root identity drift")
    workspace = _identity(
        row["workspace_identity"], "raw workspace", directory=True
    )
    model = _identity(row["model_identity"], "raw model", directory=True)
    if (
        workspace != expected_volume["workspace_identity"]
        or model != expected_volume["model_identity"]
    ):
        raise LiveGatePolicyV3Error("workspace/model identity drift")
    raw_parents = _freeze_identity_rows(
        row["canonical_parents"], "raw.canonical_parents", directory=True
    )
    if raw_parents != freeze["parents"]:
        raise LiveGatePolicyV3Error("canonical parent mapping drift")
    parent_map = {item["id"]: item for item in raw_parents}
    target_rows = _raw_file_rows(
        row["targets"], freeze["targets"], parent_map, capture, target=True
    )
    sentinel_rows = _raw_file_rows(
        row["sentinels"], freeze["sentinels"], parent_map, capture, target=False
    )
    observer = _closed(
        row["observer_process_identity"],
        {"pid", "start_token", "executable_identity"},
        "raw.observer_process_identity",
    )
    _integer(observer["pid"], "observer pid", 1)
    _text(observer["start_token"], "observer start_token")
    _text(observer["executable_identity"], "observer executable_identity")
    processes = _process_rows(row["processes"], observer, capture)
    if row["bounded_process_policy_sha256"] != digest_value(
        list(BOUNDED_PROCESS_NAMES)
    ):
        raise LiveGatePolicyV3Error("raw bounded process policy drift")
    effects = _closed(
        row["effects"],
        {
            "read_only_measurement",
            "probe_files_created",
            "directory_members_changed",
            "file_bytes_changed",
            "delete_or_replace_attempted",
            "publication_attempted",
        },
        "raw.effects",
    )
    for key, expected in {
        "read_only_measurement": True,
        "probe_files_created": False,
        "directory_members_changed": False,
        "file_bytes_changed": False,
        "delete_or_replace_attempted": False,
        "publication_attempted": False,
    }.items():
        _boolean(effects[key], expected, f"effects.{key}")
    limits = _closed(
        row["limitations"],
        {
            "inventory_exhaustive",
            "future_or_preopened_writers_excluded",
            "lost_update_before_rename_possible",
            "overwrite_after_readback_possible",
            "power_loss_durability_claimed",
            "set_atomicity_claimed",
        },
        "raw.limitations",
    )
    for key, expected in {
        "inventory_exhaustive": False,
        "future_or_preopened_writers_excluded": False,
        "lost_update_before_rename_possible": True,
        "overwrite_after_readback_possible": True,
        "power_loss_durability_claimed": False,
        "set_atomicity_claimed": False,
    }.items():
        _boolean(limits[key], expected, f"limitations.{key}")
    _boolean(row["candidate_only"], True, "raw candidate_only")
    _boolean(row["non_authorizing"], True, "raw non_authorizing")
    return {
        "raw": dict(row),
        "boot": dict(boot),
        "os": dict(os_row),
        "volume": dict(volume),
        "workspace": workspace,
        "model": model,
        "parents": raw_parents,
        "targets": target_rows,
        "sentinels": sentinel_rows,
        "processes": processes,
    }


def _continuity(value: Mapping[str, Any]) -> dict[str, Any]:
    target_fields = (
        "ordinal",
        "id",
        "role",
        "path_token",
        "parent_id",
        "parent_identity",
        "leaf_name",
        "identity",
        "size_bytes",
        "ntfs_link_count",
        "expected_preimage_sha256",
        "expected_staged_sha256",
        "observed_sha256",
    )
    sentinel_fields = (
        "ordinal",
        "id",
        "role",
        "path_token",
        "parent_id",
        "parent_identity",
        "leaf_name",
        "identity",
        "size_bytes",
        "ntfs_link_count",
        "expected_sha256",
        "observed_sha256",
    )
    process_fields = (
        "pid",
        "parent_pid",
        "normalized_name",
        "start_token",
        "executable_identity",
        "access_status",
        "liveness_wait_result",
        "executable_handle_identity_available",
        "classification_status",
    )
    return {
        "boot": value["boot"],
        "os": value["os"],
        "volume": value["volume"],
        "workspace": value["workspace"],
        "model": value["model"],
        "parents": value["parents"],
        "targets": [
            {key: row[key] for key in target_fields} for row in value["targets"]
        ],
        "sentinels": [
            {key: row[key] for key in sentinel_fields}
            for row in value["sentinels"]
        ],
        "current_process": {
            key: value["processes"]["current"][key] for key in process_fields
        },
        "parent_process": {
            key: value["processes"]["parent"][key] for key in process_fields
        },
        "bounded_process_rows": [
            {key: row[key] for key in process_fields}
            for row in value["processes"]["rows"]
        ],
        "process_policy_sha256": value["raw"]["bounded_process_policy_sha256"],
    }


_RESULT_KEYS = {
    "schema_version",
    "success_label",
    "phase",
    "gate_id",
    "application_id",
    "component_lock_sha256",
    "reviewed_release_sha256",
    "execution_freeze_sha256",
    "design_boss_ruling_sha256",
    "evidence_class",
    "raw_measurement_sha256",
    "continuity_sha256",
    "capability_reference_sha256",
    "validated_at_wall_utc",
    "validated_at_monotonic_ns",
    "expected_prepare_raw_sha256",
    "expected_prepare_result_sha256",
    "human_identity_verified",
    "effect_authorized",
    "external_owner_capability_present_and_verified",
    "reviewed_release_origin_verified_by_pure_policy",
    "canonical_execution_blocked",
    "transaction_completion_authorized",
    "required_terminal_ordering",
    "post_completed_drift_policy",
    "static_review_reused_as_live_instance_review",
    "machine_blockers",
    "local_json_alone_sufficient",
    "owner_capability_verification_outside_policy",
    "in_process_lease_outside_policy",
    "outside_policy_requirements",
    "candidate_only",
    "non_authorizing",
}


def _result(
    measured: Mapping[str, Any],
    freeze: Mapping[str, Any],
    *,
    phase: str,
    component_sha256: str,
    freeze_sha256: str,
    raw_sha256: str,
    capability_reference_sha256: str,
    validation_wall: datetime,
    validation_mono: int,
    expected_prepare_raw_sha256: str | None,
    expected_prepare_result_sha256: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA,
        "success_label": SUCCESS_LABEL,
        "phase": phase,
        "gate_id": measured["raw"]["capture"]["capture_id"],
        "application_id": freeze["raw"]["application_id"],
        "component_lock_sha256": component_sha256,
        "reviewed_release_sha256": freeze["raw"]["reviewed_release_sha256"],
        "execution_freeze_sha256": freeze_sha256,
        "design_boss_ruling_sha256": DESIGN_BOSS_RULING_SHA256,
        "evidence_class": "read_only_collector_zero_delta",
        "raw_measurement_sha256": raw_sha256,
        "continuity_sha256": digest_value(_continuity(measured)),
        "capability_reference_sha256": capability_reference_sha256,
        "validated_at_wall_utc": validation_wall.isoformat().replace("+00:00", "Z"),
        "validated_at_monotonic_ns": validation_mono,
        "expected_prepare_raw_sha256": expected_prepare_raw_sha256,
        "expected_prepare_result_sha256": expected_prepare_result_sha256,
        "human_identity_verified": False,
        "effect_authorized": False,
        "external_owner_capability_present_and_verified": False,
        "reviewed_release_origin_verified_by_pure_policy": False,
        "canonical_execution_blocked": True,
        "transaction_completion_authorized": False,
        "required_terminal_ordering": (
            "all_authority_bearing_final_checks_before_single_completed_transition"
        ),
        "post_completed_drift_policy": (
            "diagnostic_only_unknown_state_no_automatic_overwrite_or_rollback"
        ),
        "static_review_reused_as_live_instance_review": False,
        "machine_blockers": MACHINE_BLOCKERS,
        "local_json_alone_sufficient": False,
        "owner_capability_verification_outside_policy": True,
        "in_process_lease_outside_policy": True,
        "outside_policy_requirements": OUTSIDE_POLICY_REQUIREMENTS,
        "candidate_only": True,
        "non_authorizing": True,
    }


def validate_live_gate_policy_v3(
    *,
    component_lock_bytes: bytes,
    expected_component_lock_sha256: str,
    execution_freeze_bytes: bytes,
    expected_execution_freeze_sha256: str,
    expected_reviewed_release_sha256: str,
    raw_measurement_bytes: bytes,
    expected_raw_measurement_sha256: str,
    capability_scope_projection: Any,
    expected_capability_reference_sha256: str,
    expected_phase: str,
    validation_wall_time_utc: str,
    validation_monotonic_ns: int,
    prepare_raw_measurement_bytes: bytes | None = None,
    independently_expected_prepare_raw_sha256: str | None = None,
    prepare_result_bytes: bytes | None = None,
    independently_expected_prepare_result_sha256: str | None = None,
) -> dict[str, Any]:
    if expected_phase not in ("prepare", "publish"):
        raise LiveGatePolicyV3Error("phase must be prepare or publish")
    validation_wall = _utc(validation_wall_time_utc, "validation wall time")
    validation_mono = _integer(
        validation_monotonic_ns, "validation monotonic ns"
    )
    component_raw = parse_canonical_bytes(
        component_lock_bytes,
        expected_component_lock_sha256,
        "component lock",
    )
    component = _validate_component(component_raw)
    freeze_raw = parse_canonical_bytes(
        execution_freeze_bytes,
        expected_execution_freeze_sha256,
        "execution freeze",
    )
    _sha(
        expected_capability_reference_sha256,
        "expected capability reference sha256",
    )
    _sha(expected_reviewed_release_sha256, "expected reviewed release sha256")
    freeze = _validate_freeze(
        freeze_raw,
        expected_component_lock_sha256,
        expected_reviewed_release_sha256,
        expected_capability_reference_sha256,
    )
    _validate_capability(
        capability_scope_projection,
        expected_capability_reference_sha256,
        freeze,
        validation_wall,
    )
    raw = parse_canonical_bytes(
        raw_measurement_bytes,
        expected_raw_measurement_sha256,
        "raw measurement",
    )
    measured = _validate_raw(
        raw,
        component,
        expected_component_lock_sha256,
        freeze,
        expected_phase,
        validation_wall,
        validation_mono,
    )
    if expected_phase == "prepare":
        if any(
            value is not None
            for value in (
                prepare_raw_measurement_bytes,
                independently_expected_prepare_raw_sha256,
                prepare_result_bytes,
                independently_expected_prepare_result_sha256,
            )
        ):
            raise LiveGatePolicyV3Error("prepare cannot accept prior evidence")
        return _result(
            measured,
            freeze,
            phase="prepare",
            component_sha256=expected_component_lock_sha256,
            freeze_sha256=expected_execution_freeze_sha256,
            raw_sha256=expected_raw_measurement_sha256,
            capability_reference_sha256=expected_capability_reference_sha256,
            validation_wall=validation_wall,
            validation_mono=validation_mono,
            expected_prepare_raw_sha256=None,
            expected_prepare_result_sha256=None,
        )
    if (
        prepare_raw_measurement_bytes is None
        or independently_expected_prepare_raw_sha256 is None
        or prepare_result_bytes is None
        or independently_expected_prepare_result_sha256 is None
    ):
        raise LiveGatePolicyV3Error(
            "publish requires independently expected prepare raw/result hashes"
        )
    prepare_result_raw = parse_canonical_bytes(
        prepare_result_bytes,
        independently_expected_prepare_result_sha256,
        "prepare result",
    )
    _closed(prepare_result_raw, _RESULT_KEYS, "prepare result")
    if (
        prepare_result_raw["schema_version"] != RESULT_SCHEMA
        or prepare_result_raw["success_label"] != SUCCESS_LABEL
        or prepare_result_raw["phase"] != "prepare"
    ):
        raise LiveGatePolicyV3Error("prepare result label or phase drift")
    original_wall = _utc(
        prepare_result_raw["validated_at_wall_utc"],
        "prepare result validation wall",
    )
    original_mono = _integer(
        prepare_result_raw["validated_at_monotonic_ns"],
        "prepare result validation mono",
    )
    prepare_raw = parse_canonical_bytes(
        prepare_raw_measurement_bytes,
        independently_expected_prepare_raw_sha256,
        "prepare raw measurement",
    )
    prepare_measured = _validate_raw(
        prepare_raw,
        component,
        expected_component_lock_sha256,
        freeze,
        "prepare",
        original_wall,
        original_mono,
    )
    recomputed_prepare = _result(
        prepare_measured,
        freeze,
        phase="prepare",
        component_sha256=expected_component_lock_sha256,
        freeze_sha256=expected_execution_freeze_sha256,
        raw_sha256=independently_expected_prepare_raw_sha256,
        capability_reference_sha256=expected_capability_reference_sha256,
        validation_wall=original_wall,
        validation_mono=original_mono,
        expected_prepare_raw_sha256=None,
        expected_prepare_result_sha256=None,
    )
    if prepare_result_raw != recomputed_prepare:
        raise LiveGatePolicyV3Error("prepare result does not recompute exactly")
    if _continuity(measured) != _continuity(prepare_measured):
        raise LiveGatePolicyV3Error("prepare/publish full continuity drift")
    return _result(
        measured,
        freeze,
        phase="publish",
        component_sha256=expected_component_lock_sha256,
        freeze_sha256=expected_execution_freeze_sha256,
        raw_sha256=expected_raw_measurement_sha256,
        capability_reference_sha256=expected_capability_reference_sha256,
        validation_wall=validation_wall,
        validation_mono=validation_mono,
        expected_prepare_raw_sha256=independently_expected_prepare_raw_sha256,
        expected_prepare_result_sha256=independently_expected_prepare_result_sha256,
    )


validate_live_gate = validate_live_gate_policy_v3
