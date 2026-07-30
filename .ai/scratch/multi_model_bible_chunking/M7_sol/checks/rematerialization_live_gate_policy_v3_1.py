#!/usr/bin/env python3
"""Pure V3.1 machine-precondition policy for T550 Hosea.

All bytes, hashes, wall times, monotonic values, identities, and observations
are supplied by the caller.  This module performs no filesystem, process,
Windows, clock, authorization, lease, or transaction action.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import PurePosixPath
import re
from typing import Any, Mapping


SCHEMA_VERSION = "t550.rematerialization_live_gate_policy.v3_1"
COMPONENT_SCHEMA = "t550.v9_component_lock.v3_1"
FREEZE_SCHEMA = "t550.v9_execution_freeze.v3_1"
RAW_SCHEMA = "t550.windows_live_environment_raw_record.v3_1"
RESULT_SCHEMA = "t550.v9_machine_precondition_result.v3_1"
CAPABILITY_SCHEMA = "t550.owner_capability_scope_projection.v3_1"
SUCCESS_LABEL = "MACHINE_PRECONDITIONS_PASS_HUMAN_GATE_UNVERIFIED"

CONTRACT_SHA256 = "28b503b96b6790d65c72685caa4d6c63ea68a6cfb4473dddb5612d0c60d71b22"
POLICY_DOCKET_SHA256 = "142b322c9d647da9290743d2676244008f7694e2375f45073318285ca7943a46"
WINDOWS_DOCKET_SHA256 = "a2f7944cb33161457d7f092631046c1608ed7c6be8422c04800ec9c56dc781bd"
V2_REJECTION_SHA256 = "24546d7abddf881e5fdb7fff872dc3cb386ad81c2b8bdee04147badfa66f9c2f"
DESIGN_BOSS_RULING_SHA256 = "67af1a7766947172c0197b58a161d3a6af669010d1ff9c68dac59b9b8e4fa6ee"
CORRECTED_DESIGN_RESOLUTION_SHA256 = "e5a727f849ff242079151722dd93fd214a34bf0e40de6be6c01b6c811c301e85"
CORRECTED_DESIGN_BOSS_CHECK_SHA256 = "9963403f8e639c1765ca28151df2e06c34d07b26a51b83e9ca19b5507425f7f8"
STATIC_ALLOWLIST_SHA256 = "a3e18ac151a4d0fb51afc282874e873f2c3344b5aab858bc5da1d1e2acec4a80"
STATIC_ALLOWLIST_VALIDATOR_SHA256 = "9aad85eee7adf116198cfa3cd2f77e2223e7e8c48b2cfc652496d6144749a98b"
STATIC_ALLOWLIST_TESTS_SHA256 = "3e63dbfc7a381b3f9c4b348f58c2c7a67276101fa65cdb1a09b8780107e0f43c"
PREDECESSOR_ALLOWLIST_SHA256 = "ceb51bb9bf51679164390cf07a46c5f3a1d307428355d987a6f4ae5b24bfa4ed"
SOURCE_MANIFEST_SHA256 = "f272661602efa1cab09fe224b6283fb2e0c1e072e9a8b54d0edcd6fa024885c4"
ALLOWLIST_TARGET_PROJECTION_SHA256 = "39afdd97f7eb7844a0b91a833317f15970383153430a64459dddb5c15cc7af4f"
ALLOWLIST_SENTINEL_PROJECTION_SHA256 = "2cbe6e8a0e912705ae8760ff5fe22f172d86ce0e62ee29061cb6a3b53e77c686"
ALLOWLIST_SOURCE_RENDER_SHA256 = "c8d287a4ff6a42154b36ec537aa7bceff75491e06442838c9437c9e272ecb2de"
ALLOWLIST_NORMALIZATION_SHA256 = "9349b6bae86ea5827aab2b166871e736ae6c4fa4717353255be21df5c14b8e13"
ALLOWLIST_COUNTS_SHA256 = "6226dacad3a97e5ea048abab63176e511ecf9ccc2d6fcfe5cf7e9c9516348919"

MAX_LEASE_SECONDS = 120
GOVERNED_COUNT = 13
REPLACEMENT_COUNT = 8
GUARD_ONLY_COUNT = 5
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
CURRENT_PROCESS_NAMES = ("python.exe", "pythonw.exe")
CONTROLLER_PROCESS_NAMES = ("codex.exe",)
DENIED_EFFECTS = (
    "comparison",
    "commit",
    "global_sidecars",
    "merge",
    "promotion",
    "push",
)
MACHINE_BLOCKERS = (
    "EXTERNAL_OWNER_CAPABILITY_UNAVAILABLE_TO_PURE_POLICY",
    "OPAQUE_IN_PROCESS_LEASE_UNAVAILABLE_TO_PURE_POLICY",
    "REVIEWED_RELEASE_ORIGIN_UNVERIFIED_BY_PURE_POLICY",
    "STRICT_HIDDEN_WRITER_DISSENT_REQUIRES_HUMAN_DECISION",
)

EXPECTED_PARENT_ROWS = (
    ("model-root", "."),
    ("hos-book-chunks-parent", "book_chunks/Hos"),
    ("hos-receipts-parent", "receipts"),
    ("hos-reviews-parent", "reviews/Hos"),
)
PARENT_ID_BY_TOKEN = {token: identifier for identifier, token in EXPECTED_PARENT_ROWS}

_GRAPH_SPEC = {
    "contract": ("normative_contract", ()),
    "corrected_design_boss_check": (
        "design_review",
        ("corrected_design_resolution",),
    ),
    "corrected_design_resolution": (
        "design_errata",
        ("contract", "design_boss_ruling", "v3_policy_docket", "v3_windows_docket"),
    ),
    "design_boss_ruling": (
        "design_hold",
        ("contract", "v3_policy_docket", "v3_windows_docket"),
    ),
    "live_instance_checker": (
        "deterministic_checker",
        ("policy_v3_1", "production_collector"),
    ),
    "policy_v3_1": (
        "portable_policy_core",
        (
            "contract",
            "corrected_design_boss_check",
            "v2_rejection",
            "v3_1_allowlist_validator",
            "v3_1_allowlist_validator_tests",
            "v3_1_static_allowlist",
        ),
    ),
    "policy_v3_1_tests": ("deterministic_test", ("policy_v3_1",)),
    "production_collector": (
        "runtime_adapter",
        ("policy_v3_1", "v3_1_static_allowlist"),
    ),
    "production_wrapper": (
        "runtime_wrapper",
        ("live_instance_checker", "transaction_kernel"),
    ),
    "rooted_replace_primitive": (
        "runtime_primitive",
        ("v3_1_static_allowlist",),
    ),
    "sealed_launcher": ("runtime_launcher", ("production_wrapper",)),
    "transaction_kernel": (
        "transaction_kernel",
        ("policy_v3_1", "production_collector", "rooted_replace_primitive"),
    ),
    "v2_rejection": ("rejected_predecessor", ()),
    "v3_1_allowlist_validator": (
        "deterministic_validator",
        ("v3_1_static_allowlist", "v3_predecessor_allowlist", "v6_source_manifest"),
    ),
    "v3_1_allowlist_validator_tests": (
        "deterministic_test",
        ("v3_1_allowlist_validator", "v3_1_static_allowlist"),
    ),
    "v3_1_static_allowlist": (
        "static_allowlist",
        ("v3_predecessor_allowlist", "v6_source_manifest"),
    ),
    "v3_policy_docket": ("design_docket", ()),
    "v3_predecessor_allowlist": ("static_allowlist_predecessor", ()),
    "v3_windows_docket": ("design_docket", ()),
    "v6_source_manifest": ("source_manifest", ()),
}
_KNOWN_GRAPH_HASHES = {
    "contract": CONTRACT_SHA256,
    "corrected_design_boss_check": CORRECTED_DESIGN_BOSS_CHECK_SHA256,
    "corrected_design_resolution": CORRECTED_DESIGN_RESOLUTION_SHA256,
    "design_boss_ruling": DESIGN_BOSS_RULING_SHA256,
    "v2_rejection": V2_REJECTION_SHA256,
    "v3_1_allowlist_validator": STATIC_ALLOWLIST_VALIDATOR_SHA256,
    "v3_1_allowlist_validator_tests": STATIC_ALLOWLIST_TESTS_SHA256,
    "v3_1_static_allowlist": STATIC_ALLOWLIST_SHA256,
    "v3_policy_docket": POLICY_DOCKET_SHA256,
    "v3_predecessor_allowlist": PREDECESSOR_ALLOWLIST_SHA256,
    "v3_windows_docket": WINDOWS_DOCKET_SHA256,
    "v6_source_manifest": SOURCE_MANIFEST_SHA256,
}

_SHA = re.compile(r"^[0-9a-f]{64}$")


class LiveGatePolicyV31Error(ValueError):
    """A closed V3.1 structural invariant failed."""


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
        raise LiveGatePolicyV31Error("value is not canonical JSON") from exc


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_value(value: Any) -> str:
    return digest_bytes(canonical_json_bytes(value))


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LiveGatePolicyV31Error(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_exact_json_bytes(
    raw: Any,
    expected_sha256: str,
    label: str,
    *,
    require_canonical: bool,
) -> dict[str, Any]:
    if not isinstance(raw, bytes):
        raise LiveGatePolicyV31Error(f"{label} must be bytes")
    _sha(expected_sha256, f"expected {label} SHA-256")
    if digest_bytes(raw) != expected_sha256:
        raise LiveGatePolicyV31Error(f"{label} detached hash drift")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiveGatePolicyV31Error(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise LiveGatePolicyV31Error(f"{label} must contain an object")
    if require_canonical and canonical_json_bytes(value) != raw:
        raise LiveGatePolicyV31Error(f"{label} is not exact canonical bytes")
    return value


def _closed(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveGatePolicyV31Error(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        raise LiveGatePolicyV31Error(
            f"{label} schema drift missing={sorted(keys - actual)} "
            f"extra={sorted(actual - keys)}"
        )
    return value


def _array(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise LiveGatePolicyV31Error(f"{label} must be an ordered array")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise LiveGatePolicyV31Error(f"{label} must be non-empty text")
    return value


def _sha(value: Any, label: str) -> str:
    text = _text(value, label)
    if _SHA.fullmatch(text) is None:
        raise LiveGatePolicyV31Error(f"{label} must be lowercase SHA-256")
    return text


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise LiveGatePolicyV31Error(f"{label} must be integer >= {minimum}")
    return value


def _boolean(value: Any, expected: bool, label: str) -> None:
    if value is not expected:
        raise LiveGatePolicyV31Error(f"{label} must be {expected}")


def _utc(value: Any, label: str) -> datetime:
    text = _text(value, label)
    try:
        result = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LiveGatePolicyV31Error(f"{label} must be ISO-8601") from exc
    if result.tzinfo is None or result.utcoffset() != timezone.utc.utcoffset(result):
        raise LiveGatePolicyV31Error(f"{label} must identify UTC")
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


def _identity_key(value: Mapping[str, Any]) -> tuple[int, str]:
    return value["volume_serial"], value["file_id"]


def _executable(value: Any, label: str) -> dict[str, Any]:
    row = _closed(value, {"identity", "size_bytes", "sha256"}, label)
    return {
        "identity": _identity(row["identity"], f"{label}.identity", directory=False),
        "size_bytes": _integer(row["size_bytes"], f"{label}.size_bytes", 1),
        "sha256": _sha(row["sha256"], f"{label}.sha256"),
    }


def _path_relation(value: Any, label: str) -> tuple[str, str, str]:
    token = _text(value, label)
    if (
        "\\" in token
        or token.startswith("/")
        or token.endswith("/")
        or ":" in token
    ):
        raise LiveGatePolicyV31Error(f"{label} is not normalized model-relative")
    path = PurePosixPath(token)
    if any(part in ("", ".", "..") or part.endswith((" ", ".")) for part in path.parts):
        raise LiveGatePolicyV31Error(f"{label} has ambiguous components")
    rendered = path.as_posix()
    if rendered != token or len(path.parts) < 1:
        raise LiveGatePolicyV31Error(f"{label} is not canonical")
    parent = "." if len(path.parts) == 1 else path.parent.as_posix()
    return token, parent, path.name


def _parent_token(value: Any, label: str) -> str:
    token = _text(value, label)
    if token == ".":
        return token
    rendered, _, _ = _path_relation(f"{token}/__leaf__", label)
    return rendered.rsplit("/", 1)[0]


def _validate_allowlist(value: Any) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "schema_version",
            "task_id",
            "book",
            "application_family",
            "predecessor_allowlist",
            "source_render",
            "normalization",
            "governed_counts",
            "targets",
            "sentinels",
            "file_identity_rows_deferred_to_post_static_execution_freeze",
            "live_measurement_executed",
            "candidate_only",
            "non_authorizing",
        },
        "static allowlist",
    )
    if (
        row["schema_version"] != "m7_hosea_v9_static_allowlist.v3_1"
        or row["task_id"] != "T550"
        or row["book"] != "Hos"
        or row["application_family"]
        != "T550-HOS-SEMANTIC-PROSE-REMATERIALIZATION-V9"
    ):
        raise LiveGatePolicyV31Error("allowlist identity drift")
    predecessor = _closed(
        row["predecessor_allowlist"], {"schema_version", "path", "sha256"}, "predecessor"
    )
    if (
        predecessor["schema_version"] != "m7_hosea_v9_static_allowlist.v3"
        or predecessor["sha256"] != PREDECESSOR_ALLOWLIST_SHA256
    ):
        raise LiveGatePolicyV31Error("allowlist predecessor drift")
    source = _closed(
        row["source_render"],
        {
            "generation",
            "prepare_manifest_sha256",
            "independent_content_pass_sha256",
            "decision_count",
            "coverage",
            "accepted",
            "held",
        },
        "allowlist source_render",
    )
    normalization = _closed(
        row["normalization"],
        {
            "path_separator",
            "relative_to",
            "absolute_paths_forbidden",
            "dot_and_dotdot_components_forbidden",
            "alternate_data_stream_suffix_forbidden",
            "trailing_dot_or_space_forbidden",
            "unicode_normalization",
            "windows_casefold_uniqueness_required",
            "windows_reserved_device_names_forbidden",
        },
        "allowlist normalization",
    )
    counts = _closed(
        row["governed_counts"],
        {
            "governed_member_count",
            "replacement_count",
            "guard_only_count",
            "sentinel_count",
        },
        "allowlist counts",
    )
    if digest_value(dict(source)) != ALLOWLIST_SOURCE_RENDER_SHA256:
        raise LiveGatePolicyV31Error("allowlist source render projection drift")
    if digest_value(dict(normalization)) != ALLOWLIST_NORMALIZATION_SHA256:
        raise LiveGatePolicyV31Error("allowlist normalization projection drift")
    if digest_value(dict(counts)) != ALLOWLIST_COUNTS_SHA256:
        raise LiveGatePolicyV31Error("allowlist count projection drift")

    targets = _array(row["targets"], "allowlist targets")
    sentinels = _array(row["sentinels"], "allowlist sentinels")
    target_keys = {
        "ordinal",
        "target_id",
        "role",
        "operation",
        "path_token",
        "parent_token",
        "leaf_name",
        "preimage_sha256",
        "preimage_size_bytes",
        "staged_sha256",
        "staged_size_bytes",
    }
    sentinel_keys = {
        "ordinal",
        "sentinel_id",
        "role",
        "path_token",
        "parent_token",
        "leaf_name",
        "expected_sha256",
    }
    operations = {"replace": 0, "guard_only": 0}
    paths: list[str] = []
    for index, raw in enumerate(targets, 1):
        target = _closed(raw, target_keys, f"allowlist target[{index}]")
        if target["ordinal"] != index:
            raise LiveGatePolicyV31Error("allowlist target order drift")
        token, parent, leaf = _path_relation(target["path_token"], "target path")
        if target["parent_token"] != parent or target["leaf_name"] != leaf:
            raise LiveGatePolicyV31Error("allowlist target parent/leaf drift")
        if parent not in PARENT_ID_BY_TOKEN:
            raise LiveGatePolicyV31Error("allowlist target parent is not exact")
        operation = target["operation"]
        if operation not in operations:
            raise LiveGatePolicyV31Error("unknown governed operation")
        operations[operation] += 1
        preimage = (
            _sha(target["preimage_sha256"], "target preimage"),
            _integer(target["preimage_size_bytes"], "target preimage size"),
        )
        staged = (
            _sha(target["staged_sha256"], "target staged"),
            _integer(target["staged_size_bytes"], "target staged size"),
        )
        if operation == "guard_only" and preimage != staged:
            raise LiveGatePolicyV31Error("guard_only allowlist state drift")
        if operation == "replace" and preimage == staged:
            raise LiveGatePolicyV31Error("replace allowlist state drift")
        paths.append(token.casefold())
    for index, raw in enumerate(sentinels, 1):
        sentinel = _closed(raw, sentinel_keys, f"allowlist sentinel[{index}]")
        if sentinel["ordinal"] != index:
            raise LiveGatePolicyV31Error("allowlist sentinel order drift")
        token, parent, leaf = _path_relation(sentinel["path_token"], "sentinel path")
        if (
            parent != "."
            or sentinel["parent_token"] != "."
            or sentinel["leaf_name"] != leaf
        ):
            raise LiveGatePolicyV31Error("model-root one-level sentinel drift")
        _sha(sentinel["expected_sha256"], "sentinel expected hash")
        paths.append(token.casefold())
    if (
        len(targets) != GOVERNED_COUNT
        or operations != {"replace": REPLACEMENT_COUNT, "guard_only": GUARD_ONLY_COUNT}
        or len(sentinels) != SENTINEL_COUNT
        or len(paths) != len(set(paths))
    ):
        raise LiveGatePolicyV31Error("allowlist governed-set drift")
    if digest_value(targets) != ALLOWLIST_TARGET_PROJECTION_SHA256:
        raise LiveGatePolicyV31Error("exact allowlist target projection drift")
    if digest_value(sentinels) != ALLOWLIST_SENTINEL_PROJECTION_SHA256:
        raise LiveGatePolicyV31Error("exact allowlist sentinel projection drift")
    for key, expected in {
        "file_identity_rows_deferred_to_post_static_execution_freeze": True,
        "live_measurement_executed": False,
        "candidate_only": True,
        "non_authorizing": True,
    }.items():
        _boolean(row[key], expected, f"allowlist.{key}")
    return {"raw": dict(row), "targets": targets, "sentinels": sentinels}


def _validate_artifact_graph(value: Any) -> dict[str, Any]:
    graph = _closed(
        value,
        {
            "schema_version",
            "external_trust_anchor_kind",
            "component_lock_contains_own_digest",
            "exact_dependency_closure",
            "nodes",
        },
        "artifact graph",
    )
    if (
        graph["schema_version"] != "t550.v9_artifact_graph.v3_1"
        or graph["external_trust_anchor_kind"]
        != "product_runtime_detached_digest_api"
    ):
        raise LiveGatePolicyV31Error("artifact graph identity drift")
    _boolean(
        graph["component_lock_contains_own_digest"],
        False,
        "graph component own digest",
    )
    _boolean(graph["exact_dependency_closure"], True, "graph exact closure")
    nodes = _array(graph["nodes"], "artifact graph nodes")
    if len(nodes) != len(_GRAPH_SPEC):
        raise LiveGatePolicyV31Error("artifact graph extra or missing node")
    parsed: dict[str, dict[str, Any]] = {}
    observed_order: list[str] = []
    for index, raw in enumerate(nodes):
        node = _closed(
            raw,
            {"artifact_id", "artifact_type", "sha256", "depends_on"},
            f"artifact node[{index}]",
        )
        identifier = _text(node["artifact_id"], "artifact ID")
        if identifier in parsed:
            raise LiveGatePolicyV31Error("duplicate artifact node")
        expected = _GRAPH_SPEC.get(identifier)
        dependencies = tuple(_array(node["depends_on"], "artifact dependencies"))
        if expected is None or node["artifact_type"] != expected[0]:
            raise LiveGatePolicyV31Error("artifact node type or ID drift")
        if dependencies != expected[1] or list(dependencies) != sorted(set(dependencies)):
            raise LiveGatePolicyV31Error("artifact dependency edge drift")
        artifact_sha = _sha(node["sha256"], "artifact SHA-256")
        if identifier in _KNOWN_GRAPH_HASHES and artifact_sha != _KNOWN_GRAPH_HASHES[identifier]:
            raise LiveGatePolicyV31Error("known artifact hash drift")
        parsed[identifier] = {
            "artifact_id": identifier,
            "artifact_type": node["artifact_type"],
            "sha256": artifact_sha,
            "depends_on": list(dependencies),
        }
        observed_order.append(identifier)
    if observed_order != sorted(_GRAPH_SPEC):
        raise LiveGatePolicyV31Error("artifact node order drift")
    for identifier, node in parsed.items():
        if any(dependency not in parsed for dependency in node["depends_on"]):
            raise LiveGatePolicyV31Error(f"artifact dependency omission at {identifier}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            raise LiveGatePolicyV31Error("artifact dependency cycle")
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in parsed[identifier]["depends_on"]:
            visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in parsed:
        visit(identifier)
    return {"raw": dict(graph), "nodes": parsed}


def _validate_component(value: Any) -> dict[str, Any]:
    row = _closed(
        value,
        {
            "schema_version",
            "generation_id",
            "artifact_graph",
            "process_policy",
            "checker_policy",
            "candidate_only",
            "non_authorizing",
        },
        "component lock",
    )
    if (
        row["schema_version"] != COMPONENT_SCHEMA
        or row["generation_id"] != "T550-HOS-V9-V3-1-DRAFT"
    ):
        raise LiveGatePolicyV31Error("component identity drift")
    graph = _validate_artifact_graph(row["artifact_graph"])
    process_policy = _closed(
        row["process_policy"],
        {
            "bounded_process_names",
            "current_process_names",
            "controller_process_names",
            "required_snapshot_status",
            "required_access_status",
            "required_liveness_status",
            "hidden_writer_exclusion_proven",
            "strict_hidden_writer_dissent_preserved",
        },
        "component process policy",
    )
    if (
        tuple(process_policy["bounded_process_names"]) != BOUNDED_PROCESS_NAMES
        or tuple(process_policy["current_process_names"]) != CURRENT_PROCESS_NAMES
        or tuple(process_policy["controller_process_names"])
        != CONTROLLER_PROCESS_NAMES
        or process_policy["required_snapshot_status"] != "COMPLETE"
        or process_policy["required_access_status"] != "ALL_ROWS_OPENED"
        or process_policy["required_liveness_status"] != "WAIT_TIMEOUT_RUNNING"
    ):
        raise LiveGatePolicyV31Error("component process policy drift")
    _boolean(
        process_policy["hidden_writer_exclusion_proven"],
        False,
        "hidden writer exclusion",
    )
    _boolean(
        process_policy["strict_hidden_writer_dissent_preserved"],
        True,
        "hidden writer dissent",
    )
    checker_policy = _closed(
        row["checker_policy"],
        {
            "checker_artifact_id",
            "phases",
            "causal_order",
            "human_or_async_wait_inside_lease",
        },
        "component checker policy",
    )
    if (
        checker_policy["checker_artifact_id"] != "live_instance_checker"
        or checker_policy["phases"] != ["prepare", "publish"]
        or checker_policy["causal_order"]
        != [
            "capture_started",
            "checker_started",
            "checker_completed",
            "capture_completed",
            "policy_validation",
        ]
    ):
        raise LiveGatePolicyV31Error("checker policy drift")
    _boolean(
        checker_policy["human_or_async_wait_inside_lease"],
        False,
        "checker async wait",
    )
    _boolean(row["candidate_only"], True, "component candidate_only")
    _boolean(row["non_authorizing"], True, "component non_authorizing")
    return {
        "raw": dict(row),
        "graph": graph,
        "process_policy": dict(process_policy),
    }


def _parent_rows(value: Any, model_identity: Mapping[str, Any], label: str) -> list[dict[str, Any]]:
    rows = _array(value, label)
    if len(rows) != len(EXPECTED_PARENT_ROWS):
        raise LiveGatePolicyV31Error("canonical parent count drift")
    result: list[dict[str, Any]] = []
    identities: list[tuple[int, str]] = []
    for index, (raw, expected) in enumerate(zip(rows, EXPECTED_PARENT_ROWS, strict=True), 1):
        row = _closed(raw, {"ordinal", "parent_id", "path_token", "identity"}, f"{label}[{index}]")
        if row["ordinal"] != index or row["parent_id"] != expected[0] or _parent_token(row["path_token"], f"{label}.path_token") != expected[1]:
            raise LiveGatePolicyV31Error("canonical parent mapping drift")
        identity = _identity(row["identity"], f"{label}.identity", directory=True)
        if expected[1] == ".":
            if identity != model_identity:
                raise LiveGatePolicyV31Error("model-root dot parent identity drift")
        else:
            identities.append(_identity_key(identity))
        result.append({"ordinal": index, "parent_id": expected[0], "path_token": expected[1], "identity": identity})
    if len(identities) != len(set(identities)) or _identity_key(model_identity) in identities:
        raise LiveGatePolicyV31Error("canonical parent identity alias")
    return result


def _freeze_files(value: Any, allowlist_rows: list[Mapping[str, Any]], parents: Mapping[str, Mapping[str, Any]], *, sentinel: bool) -> list[dict[str, Any]]:
    rows = _array(value, "freeze sentinels" if sentinel else "freeze targets")
    expected_count = SENTINEL_COUNT if sentinel else GOVERNED_COUNT
    if len(rows) != expected_count:
        raise LiveGatePolicyV31Error("freeze governed file count drift")
    keys = ({"ordinal", "sentinel_id", "role", "path_token", "parent_id", "leaf_name", "identity", "size_bytes", "ntfs_link_count", "expected_sha256"} if sentinel else {"ordinal", "target_id", "role", "operation", "path_token", "parent_id", "leaf_name", "identity", "size_bytes", "preimage_size_bytes", "staged_size_bytes", "ntfs_link_count", "preimage_sha256", "staged_sha256"})
    result: list[dict[str, Any]] = []
    identity_keys: list[tuple[int, str]] = []
    for index, (raw, allowed) in enumerate(zip(rows, allowlist_rows, strict=True), 1):
        row = _closed(raw, keys, f"freeze file[{index}]")
        token, parent_token, leaf = _path_relation(row["path_token"], "freeze file path")
        expected_parent_id = PARENT_ID_BY_TOKEN[parent_token]
        logical_keys = (("ordinal", "sentinel_id", "role", "path_token", "leaf_name", "expected_sha256") if sentinel else ("ordinal", "target_id", "role", "operation", "path_token", "leaf_name", "preimage_sha256", "staged_sha256", "preimage_size_bytes", "staged_size_bytes"))
        if any(row[key] != allowed[key] for key in logical_keys):
            raise LiveGatePolicyV31Error("freeze file allowlist projection drift")
        if row["parent_id"] != expected_parent_id or expected_parent_id not in parents:
            raise LiveGatePolicyV31Error("freeze file parent relation drift")
        identity = _identity(row["identity"], "freeze file identity", directory=False)
        if _integer(row["ntfs_link_count"], "freeze link count", 1) != 1:
            raise LiveGatePolicyV31Error("freeze hardlink count must equal one")
        size = _integer(row["size_bytes"], "freeze file size")
        if not sentinel and (
            size != allowed["preimage_size_bytes"]
            or row["preimage_size_bytes"] != allowed["preimage_size_bytes"]
            or row["staged_size_bytes"] != allowed["staged_size_bytes"]
        ):
            raise LiveGatePolicyV31Error("freeze target size drift")
        identity_keys.append(_identity_key(identity))
        item = {**{key: row[key] for key in logical_keys}, "parent_id": expected_parent_id, "parent_token": parent_token, "identity": identity, "size_bytes": size, "ntfs_link_count": 1}
        if not sentinel:
            item["guard_replacement_forbidden"] = row["operation"] == "guard_only"
        result.append(item)
    if len(identity_keys) != len(set(identity_keys)):
        raise LiveGatePolicyV31Error("governed file identity alias")
    return result


def _frozen_process_identity(value: Any, label: str, *, current: bool) -> dict[str, Any]:
    row = _closed(value, {"role", "normalized_name", "executable"}, label)
    expected_role = "current" if current else "controller"
    if row["role"] != expected_role:
        raise LiveGatePolicyV31Error(f"{label} role drift")
    name = _text(row["normalized_name"], f"{label}.normalized_name").casefold()
    permitted = CURRENT_PROCESS_NAMES if current else CONTROLLER_PROCESS_NAMES
    if name not in permitted or name != row["normalized_name"]:
        raise LiveGatePolicyV31Error(f"{label} name drift")
    return {"role": expected_role, "normalized_name": name, "executable": _executable(row["executable"], f"{label}.executable")}


def _validate_freeze(value: Any, component_sha256: str, component_graph_sha256: str, allowlist: Mapping[str, Any]) -> dict[str, Any]:
    row = _closed(value, {"schema_version", "generation_id", "component_lock_sha256", "component_graph_sha256", "reviewed_release_sha256", "static_allowlist_sha256", "target_projection_sha256", "sentinel_projection_sha256", "frozen_at_utc", "pre_freeze_boot_identity", "identity_lifetime_policy", "environment", "canonical_parents", "targets", "sentinels", "process_identities", "candidate_only", "non_authorizing"}, "execution freeze")
    if row["schema_version"] != FREEZE_SCHEMA or row["generation_id"] != "T550-HOS-V9-V3-1-DRAFT" or row["component_lock_sha256"] != component_sha256 or row["component_graph_sha256"] != component_graph_sha256 or row["static_allowlist_sha256"] != STATIC_ALLOWLIST_SHA256 or row["target_projection_sha256"] != ALLOWLIST_TARGET_PROJECTION_SHA256 or row["sentinel_projection_sha256"] != ALLOWLIST_SENTINEL_PROJECTION_SHA256:
        raise LiveGatePolicyV31Error("execution freeze identity drift")
    _sha(row["reviewed_release_sha256"], "reviewed release SHA-256")
    frozen_at = _utc(row["frozen_at_utc"], "freeze frozen_at")
    _sha(row["pre_freeze_boot_identity"], "pre-freeze boot identity")
    lifetime = _closed(row["identity_lifetime_policy"], {"stable_file_and_executable_identities_only", "ephemeral_pid_start_handle_ancestry_frozen", "ephemeral_continuity_only_inside_live_lease"}, "identity lifetime policy")
    _boolean(lifetime["stable_file_and_executable_identities_only"], True, "stable identity policy")
    _boolean(lifetime["ephemeral_pid_start_handle_ancestry_frozen"], False, "ephemeral freeze policy")
    _boolean(lifetime["ephemeral_continuity_only_inside_live_lease"], True, "ephemeral continuity policy")
    environment = _closed(row["environment"], {"os_name", "os_build", "native_architecture", "process_architecture", "filesystem", "volume_guid", "volume_serial", "volume_root_identity", "workspace_identity", "model_identity"}, "freeze environment")
    if environment["os_name"] != "Windows" or environment["filesystem"] != "NTFS":
        raise LiveGatePolicyV31Error("freeze platform drift")
    for key in ("os_build", "native_architecture", "process_architecture", "volume_guid"):
        _text(environment[key], f"environment.{key}")
    _integer(environment["volume_serial"], "environment.volume_serial")
    frozen_environment = {**dict(environment), "volume_root_identity": _identity(environment["volume_root_identity"], "volume root", directory=True), "workspace_identity": _identity(environment["workspace_identity"], "workspace", directory=True), "model_identity": _identity(environment["model_identity"], "model", directory=True)}
    root_keys = [_identity_key(frozen_environment[key]) for key in ("volume_root_identity", "workspace_identity", "model_identity")]
    if len(root_keys) != len(set(root_keys)):
        raise LiveGatePolicyV31Error("root identity alias")
    parents = _parent_rows(row["canonical_parents"], frozen_environment["model_identity"], "freeze parents")
    parent_map = {item["parent_id"]: item for item in parents}
    targets = _freeze_files(row["targets"], allowlist["targets"], parent_map, sentinel=False)
    sentinels = _freeze_files(row["sentinels"], allowlist["sentinels"], parent_map, sentinel=True)
    all_file_keys = [_identity_key(item["identity"]) for item in [*targets, *sentinels]]
    if len(all_file_keys) != len(set(all_file_keys)):
        raise LiveGatePolicyV31Error("target/sentinel identity alias")
    process_identities = _closed(row["process_identities"], {"current", "controller"}, "frozen process identities")
    current = _frozen_process_identity(process_identities["current"], "frozen current", current=True)
    controller = _frozen_process_identity(process_identities["controller"], "frozen controller", current=False)
    if _identity_key(current["executable"]["identity"]) == _identity_key(controller["executable"]["identity"]):
        raise LiveGatePolicyV31Error("current/controller executable identity alias")
    _boolean(row["candidate_only"], True, "freeze candidate_only")
    _boolean(row["non_authorizing"], True, "freeze non_authorizing")
    return {"raw": dict(row), "frozen_at": frozen_at, "environment": frozen_environment, "parents": parents, "parent_map": parent_map, "targets": targets, "sentinels": sentinels, "process_current": current, "process_controller": controller}

def _validate_capability(value: Any, expected_reference_sha256: str, freeze: Mapping[str, Any], validation_time: datetime) -> dict[str, Any]:
    row = _closed(value, {"schema_version", "reference_sha256", "subject", "task_id", "book", "execution_freeze_sha256", "reviewed_release_sha256", "static_allowlist_sha256", "phases", "denied_effects", "issued_at_utc", "expires_at_utc", "identity_assurance", "origin_verified", "single_use_verified", "local_json_alone_sufficient"}, "capability projection")
    if row["schema_version"] != CAPABILITY_SCHEMA or row["reference_sha256"] != expected_reference_sha256 or row["subject"] != "Lowell Wong" or row["task_id"] != "T550" or row["book"] != "Hos" or row["execution_freeze_sha256"] != freeze["execution_freeze_sha256"] or row["reviewed_release_sha256"] != freeze["raw"]["reviewed_release_sha256"] or row["static_allowlist_sha256"] != STATIC_ALLOWLIST_SHA256 or row["phases"] != ["prepare", "publish", "recover"] or tuple(row["denied_effects"]) != DENIED_EFFECTS:
        raise LiveGatePolicyV31Error("capability scope drift")
    issued = _utc(row["issued_at_utc"], "capability issued")
    expires = _utc(row["expires_at_utc"], "capability expires")
    if not issued <= validation_time <= expires:
        raise LiveGatePolicyV31Error("capability descriptive time scope drift")
    if row["identity_assurance"] != "descriptive_unverified":
        raise LiveGatePolicyV31Error("local capability identity overclaim")
    _boolean(row["origin_verified"], False, "capability origin")
    _boolean(row["single_use_verified"], False, "capability single use")
    _boolean(row["local_json_alone_sufficient"], False, "capability local JSON")
    return dict(row)


def _capture(value: Any) -> dict[str, Any]:
    row = _closed(value, {"start_wall_utc", "end_wall_utc", "start_monotonic_ns", "end_monotonic_ns"}, "capture")
    start_wall = _utc(row["start_wall_utc"], "capture start wall")
    end_wall = _utc(row["end_wall_utc"], "capture end wall")
    start_mono = _integer(row["start_monotonic_ns"], "capture start monotonic")
    end_mono = _integer(row["end_monotonic_ns"], "capture end monotonic")
    wall_duration = (end_wall - start_wall).total_seconds()
    mono_duration = (end_mono - start_mono) / 1_000_000_000
    if wall_duration < 0 or mono_duration < 0 or wall_duration > MAX_LEASE_SECONDS or mono_duration > MAX_LEASE_SECONDS or abs(wall_duration - mono_duration) > 1:
        raise LiveGatePolicyV31Error("capture chronology drift")
    return {"raw": dict(row), "start_wall": start_wall, "end_wall": end_wall, "start_mono": start_mono, "end_mono": end_mono}


def _observation(wall: Any, mono: Any, capture: Mapping[str, Any], label: str) -> tuple[str, int]:
    observed_wall = _utc(wall, f"{label} wall")
    observed_mono = _integer(mono, f"{label} monotonic")
    if not capture["start_wall"] <= observed_wall <= capture["end_wall"] or not capture["start_mono"] <= observed_mono <= capture["end_mono"]:
        raise LiveGatePolicyV31Error(f"{label} outside capture")
    return _text(wall, f"{label} wall text"), observed_mono


def _raw_files(value: Any, frozen: list[Mapping[str, Any]], parents: Mapping[str, Mapping[str, Any]], capture: Mapping[str, Any], *, sentinel: bool) -> list[dict[str, Any]]:
    rows = _array(value, "raw sentinels" if sentinel else "raw targets")
    if len(rows) != len(frozen):
        raise LiveGatePolicyV31Error("raw governed file count drift")
    keys = ({"ordinal", "sentinel_id", "role", "path_token", "parent_id", "parent_identity", "leaf_name", "identity", "size_bytes", "ntfs_link_count", "expected_sha256", "observed_sha256", "root_relative_opened", "replacement_requested", "mutation_observed", "observation_wall_utc", "observation_monotonic_ns"} if sentinel else {"ordinal", "target_id", "role", "operation", "path_token", "parent_id", "parent_identity", "leaf_name", "identity", "size_bytes", "expected_preimage_size_bytes", "expected_staged_size_bytes", "ntfs_link_count", "expected_preimage_sha256", "expected_staged_sha256", "observed_sha256", "root_relative_opened", "replacement_requested", "mutation_observed", "observation_wall_utc", "observation_monotonic_ns"})
    result: list[dict[str, Any]] = []
    for index, (raw, expected) in enumerate(zip(rows, frozen, strict=True), 1):
        row = _closed(raw, keys, f"raw file[{index}]")
        logical_keys = (("ordinal", "sentinel_id", "role", "path_token", "parent_id", "leaf_name") if sentinel else ("ordinal", "target_id", "role", "operation", "path_token", "parent_id", "leaf_name"))
        if any(row[key] != expected[key] for key in logical_keys):
            raise LiveGatePolicyV31Error("raw file logical projection drift")
        parent = parents[expected["parent_id"]]
        if row["parent_identity"] != parent["identity"]:
            raise LiveGatePolicyV31Error("raw file parent identity drift")
        identity = _identity(row["identity"], "raw file identity", directory=False)
        if identity != expected["identity"] or row["size_bytes"] != expected["size_bytes"] or row["ntfs_link_count"] != 1:
            raise LiveGatePolicyV31Error("raw file identity size or hardlink drift")
        if sentinel:
            if row["expected_sha256"] != expected["expected_sha256"] or row["observed_sha256"] != expected["expected_sha256"]:
                raise LiveGatePolicyV31Error("sentinel byte drift")
        else:
            if row["expected_preimage_sha256"] != expected["preimage_sha256"] or row["expected_staged_sha256"] != expected["staged_sha256"] or row["expected_preimage_size_bytes"] != expected["preimage_size_bytes"] or row["expected_staged_size_bytes"] != expected["staged_size_bytes"] or row["observed_sha256"] != expected["preimage_sha256"]:
                raise LiveGatePolicyV31Error("target byte drift")
            if expected["operation"] == "guard_only" and not expected["guard_replacement_forbidden"]:
                raise LiveGatePolicyV31Error("guard replacement authority drift")
        _boolean(row["root_relative_opened"], True, "root-relative open")
        _boolean(row["replacement_requested"], False, "replacement requested")
        _boolean(row["mutation_observed"], False, "mutation observed")
        wall, mono = _observation(row["observation_wall_utc"], row["observation_monotonic_ns"], capture, "file observation")
        result.append({**dict(row), "identity": identity, "observation_wall_utc": wall, "observation_monotonic_ns": mono})
    return result


def _process_row(value: Any, capture: Mapping[str, Any], label: str) -> dict[str, Any]:
    row = _closed(value, {"pid", "parent_pid", "creation_token", "normalized_name", "process_handle_access", "liveness_status", "executable", "observation_wall_utc", "observation_monotonic_ns"}, label)
    pid = _integer(row["pid"], f"{label}.pid", 1)
    parent_pid = _integer(row["parent_pid"], f"{label}.parent_pid")
    name = _text(row["normalized_name"], f"{label}.name").casefold()
    if name != row["normalized_name"] or name not in BOUNDED_PROCESS_NAMES:
        raise LiveGatePolicyV31Error("unclassified bounded process name")
    if row["process_handle_access"] != "OPENED_QUERY_AND_SYNCHRONIZE":
        raise LiveGatePolicyV31Error("process access uncertainty")
    if row["liveness_status"] != "WAIT_TIMEOUT_RUNNING":
        raise LiveGatePolicyV31Error("process exit or liveness uncertainty")
    wall, mono = _observation(row["observation_wall_utc"], row["observation_monotonic_ns"], capture, "process observation")
    return {"pid": pid, "parent_pid": parent_pid, "creation_token": _text(row["creation_token"], "process creation token"), "normalized_name": name, "process_handle_access": row["process_handle_access"], "liveness_status": row["liveness_status"], "executable": _executable(row["executable"], f"{label}.executable"), "observation_wall_utc": wall, "observation_monotonic_ns": mono}


def _process_snapshot(value: Any, freeze: Mapping[str, Any], capture: Mapping[str, Any]) -> dict[str, Any]:
    row = _closed(value, {"snapshot_status", "access_status", "pid_reuse_status", "omission_status", "partial_reason", "system_process_count", "bounded_candidate_count", "opened_bounded_count", "classified_bounded_count", "access_denied_count", "pid_reuse_count", "omitted_count", "exited_count", "current_pid", "controller_pid", "bounded_identity_sha256", "rows"}, "bounded process snapshot")
    if row["snapshot_status"] != "COMPLETE" or row["access_status"] != "ALL_ROWS_OPENED" or row["pid_reuse_status"] != "NONE" or row["omission_status"] != "NONE" or row["partial_reason"] is not None:
        raise LiveGatePolicyV31Error("partial or uncertain bounded process snapshot")
    for key in ("access_denied_count", "pid_reuse_count", "omitted_count", "exited_count"):
        if row[key] != 0:
            raise LiveGatePolicyV31Error("bounded process snapshot failure count")
    rows = [_process_row(raw, capture, f"process[{index}]") for index, raw in enumerate(_array(row["rows"], "process rows"))]
    count = len(rows)
    system_count = _integer(row["system_process_count"], "system process count", count)
    if row["bounded_candidate_count"] != count or row["opened_bounded_count"] != count or row["classified_bounded_count"] != count or system_count < count:
        raise LiveGatePolicyV31Error("bounded process omission or access mismatch")
    pids = [item["pid"] for item in rows]
    identities = [(item["pid"], item["creation_token"]) for item in rows]
    if len(pids) != len(set(pids)) or len(identities) != len(set(identities)):
        raise LiveGatePolicyV31Error("PID reuse or duplicate process row")
    identity_fields = ("pid", "parent_pid", "creation_token", "normalized_name", "process_handle_access", "liveness_status", "executable")
    identity_projection = [
        {key: item[key] for key in identity_fields} for item in rows
    ]
    if row["bounded_identity_sha256"] != digest_value(identity_projection):
        raise LiveGatePolicyV31Error("bounded process evidence digest drift")
    by_pid = {item["pid"]: item for item in rows}
    current = by_pid.get(row["current_pid"])
    controller = by_pid.get(row["controller_pid"])
    if current is None or controller is None or current["parent_pid"] != controller["pid"]:
        raise LiveGatePolicyV31Error("current/controller causal relation drift")
    if current["normalized_name"] != freeze["process_current"]["normalized_name"] or current["executable"] != freeze["process_current"]["executable"]:
        raise LiveGatePolicyV31Error("frozen current executable drift")
    if controller["normalized_name"] != freeze["process_controller"]["normalized_name"] or controller["executable"] != freeze["process_controller"]["executable"]:
        raise LiveGatePolicyV31Error("frozen controller executable drift")
    blockers = [item for item in rows if item["pid"] not in {current["pid"], controller["pid"]}]
    if blockers:
        raise LiveGatePolicyV31Error("unrelated bounded writer process present")
    return {"raw": dict(row), "rows": rows, "current": current, "controller": controller}

def _validate_raw(value: Any, *, phase: str, raw_sha256: str, component_sha256: str, freeze_sha256: str, component: Mapping[str, Any], freeze: Mapping[str, Any], expected_prepare_raw_sha256: str | None, expected_prepare_result_sha256: str | None, validation_wall: datetime, validation_mono: int) -> dict[str, Any]:
    row = _closed(value, {"schema_version", "generation_id", "phase", "evidence", "checker", "candidate_only", "non_authorizing"}, "raw record")
    if row["schema_version"] != RAW_SCHEMA or row["generation_id"] != "T550-HOS-V9-V3-1-DRAFT" or row["phase"] != phase:
        raise LiveGatePolicyV31Error("raw identity or phase drift")
    evidence = _closed(row["evidence"], {"component_lock_sha256", "execution_freeze_sha256", "static_allowlist_sha256", "evidence_class", "provenance", "causal_parent", "capture", "boot", "environment", "canonical_parents", "targets", "sentinels", "bounded_process_snapshot", "effects"}, "raw evidence")
    if evidence["component_lock_sha256"] != component_sha256 or evidence["execution_freeze_sha256"] != freeze_sha256 or evidence["static_allowlist_sha256"] != STATIC_ALLOWLIST_SHA256 or evidence["evidence_class"] != "read_only_collector_zero_delta":
        raise LiveGatePolicyV31Error("raw dependency or evidence-class drift")
    provenance = _closed(evidence["provenance"], {"collector_artifact_id", "collector_sha256", "test_only", "injection_enabled", "production_eligible", "complete_bounded_snapshot_required"}, "raw provenance")
    collector = component["graph"]["nodes"]["production_collector"]
    if provenance["collector_artifact_id"] != "production_collector" or provenance["collector_sha256"] != collector["sha256"]:
        raise LiveGatePolicyV31Error("production collector provenance drift")
    _boolean(provenance["test_only"], False, "collector test_only")
    _boolean(provenance["injection_enabled"], False, "collector injection")
    _boolean(provenance["production_eligible"], True, "collector production eligibility")
    _boolean(provenance["complete_bounded_snapshot_required"], True, "snapshot requirement")
    causal = _closed(evidence["causal_parent"], {"kind", "prepare_raw_sha256", "prepare_result_sha256"}, "raw causal parent")
    if phase == "prepare":
        if causal != {"kind": "none", "prepare_raw_sha256": None, "prepare_result_sha256": None}:
            raise LiveGatePolicyV31Error("prepare causal parent must be empty")
    elif causal != {"kind": "validated_prepare", "prepare_raw_sha256": expected_prepare_raw_sha256, "prepare_result_sha256": expected_prepare_result_sha256}:
        raise LiveGatePolicyV31Error("publish causal parent drift")
    capture = _capture(evidence["capture"])
    boot = _closed(evidence["boot"], {"boot_identity", "boot_time_utc"}, "raw boot")
    boot_identity = _sha(boot["boot_identity"], "boot identity")
    boot_time = _utc(boot["boot_time_utc"], "boot time")
    if boot_identity == freeze["raw"]["pre_freeze_boot_identity"] or not freeze["frozen_at"] < boot_time <= capture["start_wall"]:
        raise LiveGatePolicyV31Error("restart and boot chronology drift")
    environment = _closed(evidence["environment"], set(freeze["raw"]["environment"]), "raw environment")
    normalized_environment = {**dict(environment), "volume_root_identity": _identity(environment["volume_root_identity"], "raw volume root", directory=True), "workspace_identity": _identity(environment["workspace_identity"], "raw workspace", directory=True), "model_identity": _identity(environment["model_identity"], "raw model", directory=True)}
    if normalized_environment != freeze["environment"]:
        raise LiveGatePolicyV31Error("raw stable environment drift")
    parents = _parent_rows(evidence["canonical_parents"], normalized_environment["model_identity"], "raw parents")
    if parents != freeze["parents"]:
        raise LiveGatePolicyV31Error("raw canonical parent continuity drift")
    parent_map = {item["parent_id"]: item for item in parents}
    targets = _raw_files(evidence["targets"], freeze["targets"], parent_map, capture, sentinel=False)
    sentinels = _raw_files(evidence["sentinels"], freeze["sentinels"], parent_map, capture, sentinel=True)
    processes = _process_snapshot(evidence["bounded_process_snapshot"], freeze, capture)
    effects = _closed(evidence["effects"], {"canonical_governed_path_mutated", "global_sidecar_path_mutated", "guard_only_replacement_attempted", "transaction_action_attempted", "directory_membership_changed"}, "raw effects")
    for key in effects:
        _boolean(effects[key], False, f"effects.{key}")
    checker = _closed(row["checker"], {"checker_artifact_id", "checker_sha256", "checker_run_token", "checked_phase", "checked_evidence_sha256", "status", "start_wall_utc", "end_wall_utc", "start_monotonic_ns", "end_monotonic_ns"}, "raw checker")
    expected_checker = component["graph"]["nodes"]["live_instance_checker"]
    if checker["checker_artifact_id"] != "live_instance_checker" or checker["checker_sha256"] != expected_checker["sha256"] or checker["checked_phase"] != phase or checker["checked_evidence_sha256"] != digest_value(dict(evidence)) or checker["status"] != "PASS_BOUNDED_READ_ONLY":
        raise LiveGatePolicyV31Error("checker binding or result drift")
    _text(checker["checker_run_token"], "checker run token")
    checker_start_wall = _utc(checker["start_wall_utc"], "checker start wall")
    checker_end_wall = _utc(checker["end_wall_utc"], "checker end wall")
    checker_start_mono = _integer(checker["start_monotonic_ns"], "checker start mono")
    checker_end_mono = _integer(checker["end_monotonic_ns"], "checker end mono")
    if not capture["start_wall"] <= checker_start_wall <= checker_end_wall <= capture["end_wall"] <= validation_wall or not capture["start_mono"] <= checker_start_mono <= checker_end_mono <= capture["end_mono"] <= validation_mono:
        raise LiveGatePolicyV31Error("checker causal chronology drift")
    if (validation_wall - capture["start_wall"]).total_seconds() > MAX_LEASE_SECONDS or (validation_mono - capture["start_mono"]) / 1_000_000_000 > MAX_LEASE_SECONDS:
        raise LiveGatePolicyV31Error("policy validation exceeded lease")
    _boolean(row["candidate_only"], True, "raw candidate_only")
    _boolean(row["non_authorizing"], True, "raw non_authorizing")
    return {"raw": dict(row), "raw_sha256": raw_sha256, "phase": phase, "evidence": dict(evidence), "capture": capture, "boot": {"boot_identity": boot_identity, "boot_time_utc": boot["boot_time_utc"]}, "environment": normalized_environment, "parents": parents, "targets": targets, "sentinels": sentinels, "processes": processes, "checker": dict(checker), "validation_wall": validation_wall, "validation_mono": validation_mono}


def _continuity(value: Mapping[str, Any]) -> dict[str, Any]:
    target_fields = (
        "ordinal", "target_id", "role", "operation", "path_token",
        "parent_id", "parent_identity", "leaf_name", "identity", "size_bytes",
        "ntfs_link_count", "expected_preimage_size_bytes",
        "expected_staged_size_bytes", "expected_preimage_sha256",
        "expected_staged_sha256",
        "observed_sha256", "root_relative_opened", "replacement_requested",
        "mutation_observed",
    )
    sentinel_fields = (
        "ordinal", "sentinel_id", "role", "path_token", "parent_id",
        "parent_identity", "leaf_name", "identity", "size_bytes",
        "ntfs_link_count", "expected_sha256", "observed_sha256",
        "root_relative_opened", "replacement_requested", "mutation_observed",
    )
    process_fields = (
        "pid", "parent_pid", "creation_token", "normalized_name",
        "process_handle_access", "liveness_status", "executable",
    )
    snapshot_fields = (
        "snapshot_status", "access_status", "pid_reuse_status", "omission_status",
        "partial_reason", "system_process_count", "bounded_candidate_count",
        "opened_bounded_count", "classified_bounded_count", "access_denied_count",
        "pid_reuse_count", "omitted_count", "exited_count", "current_pid",
        "controller_pid", "bounded_identity_sha256",
    )
    return {
        "boot": value["boot"],
        "environment": value["environment"],
        "parents": value["parents"],
        "targets": [{key: row[key] for key in target_fields} for row in value["targets"]],
        "sentinels": [{key: row[key] for key in sentinel_fields} for row in value["sentinels"]],
        "process_snapshot": {
            key: value["processes"]["raw"][key] for key in snapshot_fields
        },
        "process_rows": [
            {key: row[key] for key in process_fields}
            for row in value["processes"]["rows"]
        ],
        "current": {
            key: value["processes"]["current"][key] for key in process_fields
        },
        "controller": {
            key: value["processes"]["controller"][key] for key in process_fields
        },
    }


_RESULT_KEYS = {"schema_version", "success_label", "phase", "component_lock_sha256", "component_graph_sha256", "static_allowlist_sha256", "execution_freeze_sha256", "reviewed_release_sha256", "raw_measurement_sha256", "continuity_sha256", "capability_reference_sha256", "checker_sha256", "checker_run_token", "validated_at_wall_utc", "validated_at_monotonic_ns", "expected_prepare_raw_sha256", "expected_prepare_result_sha256", "governed_member_count", "replacement_count", "guard_only_count", "sentinel_count", "machine_preconditions_pass", "human_identity_verified", "owner_capability_present_and_verified", "owner_capability_origin_verified_by_pure_policy", "opaque_lease_verified_by_pure_policy", "reviewed_release_origin_verified_by_pure_policy", "replace_replacement_authorized", "guard_only_replacement_authorized", "effect_authorized", "publication_authorized", "transaction_completion_authorized", "canonical_execution_blocked", "hidden_writer_exclusion_proven", "strict_hidden_writer_dissent_preserved", "machine_blockers", "candidate_only", "non_authorizing"}


def _make_result(*, phase: str, component_sha256: str, component_graph_sha256: str, freeze_sha256: str, freeze: Mapping[str, Any], raw: Mapping[str, Any], capability_reference_sha256: str, validation_wall_text: str, validation_mono: int, expected_prepare_raw_sha256: str | None, expected_prepare_result_sha256: str | None) -> dict[str, Any]:
    return {"schema_version": RESULT_SCHEMA, "success_label": SUCCESS_LABEL, "phase": phase, "component_lock_sha256": component_sha256, "component_graph_sha256": component_graph_sha256, "static_allowlist_sha256": STATIC_ALLOWLIST_SHA256, "execution_freeze_sha256": freeze_sha256, "reviewed_release_sha256": freeze["raw"]["reviewed_release_sha256"], "raw_measurement_sha256": raw["raw_sha256"], "continuity_sha256": digest_value(_continuity(raw)), "capability_reference_sha256": capability_reference_sha256, "checker_sha256": raw["checker"]["checker_sha256"], "checker_run_token": raw["checker"]["checker_run_token"], "validated_at_wall_utc": validation_wall_text, "validated_at_monotonic_ns": validation_mono, "expected_prepare_raw_sha256": expected_prepare_raw_sha256, "expected_prepare_result_sha256": expected_prepare_result_sha256, "governed_member_count": GOVERNED_COUNT, "replacement_count": REPLACEMENT_COUNT, "guard_only_count": GUARD_ONLY_COUNT, "sentinel_count": SENTINEL_COUNT, "machine_preconditions_pass": True, "human_identity_verified": False, "owner_capability_present_and_verified": False, "owner_capability_origin_verified_by_pure_policy": False, "opaque_lease_verified_by_pure_policy": False, "reviewed_release_origin_verified_by_pure_policy": False, "replace_replacement_authorized": False, "guard_only_replacement_authorized": False, "effect_authorized": False, "publication_authorized": False, "transaction_completion_authorized": False, "canonical_execution_blocked": True, "hidden_writer_exclusion_proven": False, "strict_hidden_writer_dissent_preserved": True, "machine_blockers": list(MACHINE_BLOCKERS), "candidate_only": True, "non_authorizing": True}


def _parse_prepare_result(raw: bytes, expected_sha256: str) -> dict[str, Any]:
    row = parse_exact_json_bytes(raw, expected_sha256, "prepare result", require_canonical=True)
    _closed(row, _RESULT_KEYS, "prepare result")
    return row


def validate_live_gate_policy_v3_1(
    *,
    static_allowlist_bytes: bytes,
    expected_static_allowlist_sha256: str,
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
        raise LiveGatePolicyV31Error("phase must be prepare or publish")
    if expected_static_allowlist_sha256 != STATIC_ALLOWLIST_SHA256:
        raise LiveGatePolicyV31Error("static allowlist trust anchor drift")
    validation_wall = _utc(validation_wall_time_utc, "validation wall")
    validation_mono = _integer(validation_monotonic_ns, "validation monotonic")
    allowlist_raw = parse_exact_json_bytes(
        static_allowlist_bytes,
        expected_static_allowlist_sha256,
        "static allowlist",
        require_canonical=False,
    )
    allowlist = _validate_allowlist(allowlist_raw)
    component_raw = parse_exact_json_bytes(
        component_lock_bytes,
        expected_component_lock_sha256,
        "component lock",
        require_canonical=True,
    )
    component = _validate_component(component_raw)
    component_graph_sha256 = digest_value(component["graph"]["raw"])
    freeze_raw = parse_exact_json_bytes(
        execution_freeze_bytes,
        expected_execution_freeze_sha256,
        "execution freeze",
        require_canonical=True,
    )
    freeze = _validate_freeze(
        freeze_raw,
        expected_component_lock_sha256,
        component_graph_sha256,
        allowlist,
    )
    if freeze["raw"]["reviewed_release_sha256"] != expected_reviewed_release_sha256:
        raise LiveGatePolicyV31Error("reviewed release detached hash drift")
    _sha(expected_reviewed_release_sha256, "expected reviewed release SHA-256")
    _sha(expected_capability_reference_sha256, "expected capability reference")
    freeze["execution_freeze_sha256"] = expected_execution_freeze_sha256
    _validate_capability(
        capability_scope_projection,
        expected_capability_reference_sha256,
        freeze,
        validation_wall,
    )
    raw_record = parse_exact_json_bytes(
        raw_measurement_bytes,
        expected_raw_measurement_sha256,
        "raw measurement",
        require_canonical=True,
    )
    measured = _validate_raw(
        raw_record,
        phase=expected_phase,
        raw_sha256=expected_raw_measurement_sha256,
        component_sha256=expected_component_lock_sha256,
        freeze_sha256=expected_execution_freeze_sha256,
        component=component,
        freeze=freeze,
        expected_prepare_raw_sha256=independently_expected_prepare_raw_sha256,
        expected_prepare_result_sha256=independently_expected_prepare_result_sha256,
        validation_wall=validation_wall,
        validation_mono=validation_mono,
    )
    prior_values = (
        prepare_raw_measurement_bytes,
        independently_expected_prepare_raw_sha256,
        prepare_result_bytes,
        independently_expected_prepare_result_sha256,
    )
    if expected_phase == "prepare":
        if any(value is not None for value in prior_values):
            raise LiveGatePolicyV31Error("prepare cannot accept prior phase evidence")
        return _make_result(
            phase="prepare",
            component_sha256=expected_component_lock_sha256,
            component_graph_sha256=component_graph_sha256,
            freeze_sha256=expected_execution_freeze_sha256,
            freeze=freeze,
            raw=measured,
            capability_reference_sha256=expected_capability_reference_sha256,
            validation_wall_text=validation_wall_time_utc,
            validation_mono=validation_mono,
            expected_prepare_raw_sha256=None,
            expected_prepare_result_sha256=None,
        )
    if any(value is None for value in prior_values):
        raise LiveGatePolicyV31Error(
            "publish requires independently retained prepare raw and result bytes/hashes"
        )
    assert prepare_raw_measurement_bytes is not None
    assert independently_expected_prepare_raw_sha256 is not None
    assert prepare_result_bytes is not None
    assert independently_expected_prepare_result_sha256 is not None
    prepare_result = _parse_prepare_result(
        prepare_result_bytes,
        independently_expected_prepare_result_sha256,
    )
    if (
        prepare_result["schema_version"] != RESULT_SCHEMA
        or prepare_result["success_label"] != SUCCESS_LABEL
        or prepare_result["phase"] != "prepare"
        or prepare_result["component_lock_sha256"] != expected_component_lock_sha256
        or prepare_result["component_graph_sha256"] != component_graph_sha256
        or prepare_result["static_allowlist_sha256"] != STATIC_ALLOWLIST_SHA256
        or prepare_result["execution_freeze_sha256"] != expected_execution_freeze_sha256
        or prepare_result["capability_reference_sha256"] != expected_capability_reference_sha256
    ):
        raise LiveGatePolicyV31Error("prepare result dependency or phase drift")
    prepare_validation_wall = _utc(
        prepare_result["validated_at_wall_utc"], "prepare validation wall"
    )
    prepare_validation_mono = _integer(
        prepare_result["validated_at_monotonic_ns"], "prepare validation monotonic"
    )
    prepare_raw_record = parse_exact_json_bytes(
        prepare_raw_measurement_bytes,
        independently_expected_prepare_raw_sha256,
        "prepare raw measurement",
        require_canonical=True,
    )
    prepare_measured = _validate_raw(
        prepare_raw_record,
        phase="prepare",
        raw_sha256=independently_expected_prepare_raw_sha256,
        component_sha256=expected_component_lock_sha256,
        freeze_sha256=expected_execution_freeze_sha256,
        component=component,
        freeze=freeze,
        expected_prepare_raw_sha256=None,
        expected_prepare_result_sha256=None,
        validation_wall=prepare_validation_wall,
        validation_mono=prepare_validation_mono,
    )
    recomputed_prepare = _make_result(
        phase="prepare",
        component_sha256=expected_component_lock_sha256,
        component_graph_sha256=component_graph_sha256,
        freeze_sha256=expected_execution_freeze_sha256,
        freeze=freeze,
        raw=prepare_measured,
        capability_reference_sha256=expected_capability_reference_sha256,
        validation_wall_text=prepare_result["validated_at_wall_utc"],
        validation_mono=prepare_validation_mono,
        expected_prepare_raw_sha256=None,
        expected_prepare_result_sha256=None,
    )
    if prepare_result != recomputed_prepare:
        raise LiveGatePolicyV31Error("prepare result does not recompute exactly")
    if _continuity(measured) != _continuity(prepare_measured):
        raise LiveGatePolicyV31Error("prepare/publish full continuity drift")
    if (
        not prepare_measured["capture"]["end_wall"]
        <= prepare_validation_wall
        <= measured["capture"]["start_wall"]
        <= validation_wall
        or not prepare_measured["capture"]["end_mono"]
        <= prepare_validation_mono
        <= measured["capture"]["start_mono"]
        <= validation_mono
    ):
        raise LiveGatePolicyV31Error("prepare/publish causal chronology drift")
    return _make_result(
        phase="publish",
        component_sha256=expected_component_lock_sha256,
        component_graph_sha256=component_graph_sha256,
        freeze_sha256=expected_execution_freeze_sha256,
        freeze=freeze,
        raw=measured,
        capability_reference_sha256=expected_capability_reference_sha256,
        validation_wall_text=validation_wall_time_utc,
        validation_mono=validation_mono,
        expected_prepare_raw_sha256=independently_expected_prepare_raw_sha256,
        expected_prepare_result_sha256=independently_expected_prepare_result_sha256,
    )


validate_live_gate = validate_live_gate_policy_v3_1
