"""Focused direct semantic tests for the pure T550 V3.1 policy."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE = (
    ROOT
    / ".ai/scratch/multi_model_bible_chunking/M7_sol/checks/"
    "rematerialization_live_gate_policy_v3_1.py"
)
ALLOWLIST_PATH = (
    ROOT
    / ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Hos/"
    "v9_static_allowlist_v3_1.json"
)
SPEC = importlib.util.spec_from_file_location("t550_policy_v31", MODULE)
assert SPEC and SPEC.loader
P = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = P
SPEC.loader.exec_module(P)

BASE = datetime(2026, 7, 28, 18, 0, tzinfo=timezone.utc)
MONO = 11_000_000_000_000


def iso(seconds: int) -> str:
    return (BASE + timedelta(seconds=seconds)).isoformat().replace("+00:00", "Z")


def sha(number: int) -> str:
    return f"{number:064x}"


def identity(number: int, *, directory: bool) -> dict:
    return {
        "volume_serial": 77,
        "file_id": f"file-{number}",
        "attributes": 16 if directory else 32,
        "is_directory": directory,
        "reparse_point": False,
    }


def executable(number: int) -> dict:
    return {
        "identity": identity(number, directory=False),
        "size_bytes": 10_000 + number,
        "sha256": sha(1_000 + number),
    }


def allowlist_bytes() -> bytes:
    return ALLOWLIST_PATH.read_bytes()


def allowlist_doc() -> dict:
    return json.loads(allowlist_bytes())


def graph() -> dict:
    nodes = []
    for index, artifact_id in enumerate(sorted(P._GRAPH_SPEC), 1):
        artifact_type, dependencies = P._GRAPH_SPEC[artifact_id]
        nodes.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "sha256": P._KNOWN_GRAPH_HASHES.get(artifact_id, sha(2_000 + index)),
                "depends_on": list(dependencies),
            }
        )
    return {
        "schema_version": "t550.v9_artifact_graph.v3_1",
        "external_trust_anchor_kind": "product_runtime_detached_digest_api",
        "component_lock_contains_own_digest": False,
        "exact_dependency_closure": True,
        "nodes": nodes,
    }


def component() -> dict:
    return {
        "schema_version": P.COMPONENT_SCHEMA,
        "generation_id": "T550-HOS-V9-V3-1-DRAFT",
        "artifact_graph": graph(),
        "process_policy": {
            "bounded_process_names": list(P.BOUNDED_PROCESS_NAMES),
            "current_process_names": list(P.CURRENT_PROCESS_NAMES),
            "controller_process_names": list(P.CONTROLLER_PROCESS_NAMES),
            "required_snapshot_status": "COMPLETE",
            "required_access_status": "ALL_ROWS_OPENED",
            "required_liveness_status": "WAIT_TIMEOUT_RUNNING",
            "hidden_writer_exclusion_proven": False,
            "strict_hidden_writer_dissent_preserved": True,
        },
        "checker_policy": {
            "checker_artifact_id": "live_instance_checker",
            "phases": ["prepare", "publish"],
            "causal_order": [
                "capture_started",
                "checker_started",
                "checker_completed",
                "capture_completed",
                "policy_validation",
            ],
            "human_or_async_wait_inside_lease": False,
        },
        "candidate_only": True,
        "non_authorizing": True,
    }


def canonical(value: object) -> bytes:
    return P.canonical_json_bytes(value)


def parent_rows(model_identity: dict) -> list[dict]:
    rows = []
    for ordinal, (parent_id, token) in enumerate(P.EXPECTED_PARENT_ROWS, 1):
        rows.append(
            {
                "ordinal": ordinal,
                "parent_id": parent_id,
                "path_token": token,
                "identity": (
                    deepcopy(model_identity)
                    if token == "."
                    else identity(20 + ordinal, directory=True)
                ),
            }
        )
    return rows


def freeze(component_sha: str, graph_sha: str) -> dict:
    allowed = allowlist_doc()
    model_identity = identity(3, directory=True)
    parents = parent_rows(model_identity)
    targets = []
    for row in allowed["targets"]:
        targets.append(
            {
                "ordinal": row["ordinal"],
                "target_id": row["target_id"],
                "role": row["role"],
                "operation": row["operation"],
                "path_token": row["path_token"],
                "parent_id": P.PARENT_ID_BY_TOKEN[row["parent_token"]],
                "leaf_name": row["leaf_name"],
                "identity": identity(100 + row["ordinal"], directory=False),
                "size_bytes": row["preimage_size_bytes"],
                "preimage_size_bytes": row["preimage_size_bytes"],
                "staged_size_bytes": row["staged_size_bytes"],
                "ntfs_link_count": 1,
                "preimage_sha256": row["preimage_sha256"],
                "staged_sha256": row["staged_sha256"],
            }
        )
    sentinels = []
    for row in allowed["sentinels"]:
        sentinels.append(
            {
                "ordinal": row["ordinal"],
                "sentinel_id": row["sentinel_id"],
                "role": row["role"],
                "path_token": row["path_token"],
                "parent_id": P.PARENT_ID_BY_TOKEN[row["parent_token"]],
                "leaf_name": row["leaf_name"],
                "identity": identity(200 + row["ordinal"], directory=False),
                "size_bytes": 50_000 + row["ordinal"],
                "ntfs_link_count": 1,
                "expected_sha256": row["expected_sha256"],
            }
        )
    return {
        "schema_version": P.FREEZE_SCHEMA,
        "generation_id": "T550-HOS-V9-V3-1-DRAFT",
        "component_lock_sha256": component_sha,
        "component_graph_sha256": graph_sha,
        "reviewed_release_sha256": sha(500),
        "static_allowlist_sha256": P.STATIC_ALLOWLIST_SHA256,
        "target_projection_sha256": P.ALLOWLIST_TARGET_PROJECTION_SHA256,
        "sentinel_projection_sha256": P.ALLOWLIST_SENTINEL_PROJECTION_SHA256,
        "frozen_at_utc": iso(-1_000),
        "pre_freeze_boot_identity": sha(501),
        "identity_lifetime_policy": {
            "stable_file_and_executable_identities_only": True,
            "ephemeral_pid_start_handle_ancestry_frozen": False,
            "ephemeral_continuity_only_inside_live_lease": True,
        },
        "environment": {
            "os_name": "Windows",
            "os_build": "26100",
            "native_architecture": "AMD64",
            "process_architecture": "AMD64",
            "filesystem": "NTFS",
            "volume_guid": "volume-guid-77",
            "volume_serial": 77,
            "volume_root_identity": identity(1, directory=True),
            "workspace_identity": identity(2, directory=True),
            "model_identity": model_identity,
        },
        "canonical_parents": parents,
        "targets": targets,
        "sentinels": sentinels,
        "process_identities": {
            "current": {
                "role": "current",
                "normalized_name": "python.exe",
                "executable": executable(301),
            },
            "controller": {
                "role": "controller",
                "normalized_name": "codex.exe",
                "executable": executable(302),
            },
        },
        "candidate_only": True,
        "non_authorizing": True,
    }


def capability(freeze_doc: dict, freeze_sha: str) -> dict:
    return {
        "schema_version": P.CAPABILITY_SCHEMA,
        "reference_sha256": sha(600),
        "subject": "Lowell Wong",
        "task_id": "T550",
        "book": "Hos",
        "execution_freeze_sha256": freeze_sha,
        "reviewed_release_sha256": freeze_doc["reviewed_release_sha256"],
        "static_allowlist_sha256": P.STATIC_ALLOWLIST_SHA256,
        "phases": ["prepare", "publish", "recover"],
        "denied_effects": list(P.DENIED_EFFECTS),
        "issued_at_utc": iso(-100),
        "expires_at_utc": iso(100),
        "identity_assurance": "descriptive_unverified",
        "origin_verified": False,
        "single_use_verified": False,
        "local_json_alone_sufficient": False,
    }


def raw(
    phase: str,
    component_doc: dict,
    component_sha: str,
    freeze_doc: dict,
    freeze_sha: str,
    *,
    offset: int,
    prepare_raw_sha: str | None = None,
    prepare_result_sha: str | None = None,
) -> dict:
    start = offset
    end = offset + 10
    observation = offset + 5
    parent_map = {
        row["parent_id"]: row for row in freeze_doc["canonical_parents"]
    }
    targets = []
    for row in freeze_doc["targets"]:
        targets.append(
            {
                "ordinal": row["ordinal"],
                "target_id": row["target_id"],
                "role": row["role"],
                "operation": row["operation"],
                "path_token": row["path_token"],
                "parent_id": row["parent_id"],
                "parent_identity": deepcopy(
                    parent_map[row["parent_id"]]["identity"]
                ),
                "leaf_name": row["leaf_name"],
                "identity": deepcopy(row["identity"]),
                "size_bytes": row["size_bytes"],
                "expected_preimage_size_bytes": row["preimage_size_bytes"],
                "expected_staged_size_bytes": row["staged_size_bytes"],
                "ntfs_link_count": 1,
                "expected_preimage_sha256": row["preimage_sha256"],
                "expected_staged_sha256": row["staged_sha256"],
                "observed_sha256": row["preimage_sha256"],
                "root_relative_opened": True,
                "replacement_requested": False,
                "mutation_observed": False,
                "observation_wall_utc": iso(observation),
                "observation_monotonic_ns": MONO + observation * 1_000_000_000,
            }
        )
    sentinels = []
    for row in freeze_doc["sentinels"]:
        sentinels.append(
            {
                "ordinal": row["ordinal"],
                "sentinel_id": row["sentinel_id"],
                "role": row["role"],
                "path_token": row["path_token"],
                "parent_id": row["parent_id"],
                "parent_identity": deepcopy(
                    parent_map[row["parent_id"]]["identity"]
                ),
                "leaf_name": row["leaf_name"],
                "identity": deepcopy(row["identity"]),
                "size_bytes": row["size_bytes"],
                "ntfs_link_count": 1,
                "expected_sha256": row["expected_sha256"],
                "observed_sha256": row["expected_sha256"],
                "root_relative_opened": True,
                "replacement_requested": False,
                "mutation_observed": False,
                "observation_wall_utc": iso(observation),
                "observation_monotonic_ns": MONO + observation * 1_000_000_000,
            }
        )
    process_rows = [
        {
            "pid": 42,
            "parent_pid": 1,
            "creation_token": "codex-start",
            "normalized_name": "codex.exe",
            "process_handle_access": "OPENED_QUERY_AND_SYNCHRONIZE",
            "liveness_status": "WAIT_TIMEOUT_RUNNING",
            "executable": deepcopy(
                freeze_doc["process_identities"]["controller"]["executable"]
            ),
            "observation_wall_utc": iso(observation),
            "observation_monotonic_ns": MONO + observation * 1_000_000_000,
        },
        {
            "pid": 100,
            "parent_pid": 42,
            "creation_token": "python-start",
            "normalized_name": "python.exe",
            "process_handle_access": "OPENED_QUERY_AND_SYNCHRONIZE",
            "liveness_status": "WAIT_TIMEOUT_RUNNING",
            "executable": deepcopy(
                freeze_doc["process_identities"]["current"]["executable"]
            ),
            "observation_wall_utc": iso(observation),
            "observation_monotonic_ns": MONO + observation * 1_000_000_000,
        },
    ]
    identity_fields = (
        "pid",
        "parent_pid",
        "creation_token",
        "normalized_name",
        "process_handle_access",
        "liveness_status",
        "executable",
    )
    process_projection = [
        {key: row[key] for key in identity_fields} for row in process_rows
    ]
    graph_nodes = {
        row["artifact_id"]: row
        for row in component_doc["artifact_graph"]["nodes"]
    }
    evidence = {
        "component_lock_sha256": component_sha,
        "execution_freeze_sha256": freeze_sha,
        "static_allowlist_sha256": P.STATIC_ALLOWLIST_SHA256,
        "evidence_class": "read_only_collector_zero_delta",
        "provenance": {
            "collector_artifact_id": "production_collector",
            "collector_sha256": graph_nodes["production_collector"]["sha256"],
            "test_only": False,
            "injection_enabled": False,
            "production_eligible": True,
            "complete_bounded_snapshot_required": True,
        },
        "causal_parent": (
            {
                "kind": "none",
                "prepare_raw_sha256": None,
                "prepare_result_sha256": None,
            }
            if phase == "prepare"
            else {
                "kind": "validated_prepare",
                "prepare_raw_sha256": prepare_raw_sha,
                "prepare_result_sha256": prepare_result_sha,
            }
        ),
        "capture": {
            "start_wall_utc": iso(start),
            "end_wall_utc": iso(end),
            "start_monotonic_ns": MONO + start * 1_000_000_000,
            "end_monotonic_ns": MONO + end * 1_000_000_000,
        },
        "boot": {"boot_identity": sha(502), "boot_time_utc": iso(-500)},
        "environment": deepcopy(freeze_doc["environment"]),
        "canonical_parents": deepcopy(freeze_doc["canonical_parents"]),
        "targets": targets,
        "sentinels": sentinels,
        "bounded_process_snapshot": {
            "snapshot_status": "COMPLETE",
            "access_status": "ALL_ROWS_OPENED",
            "pid_reuse_status": "NONE",
            "omission_status": "NONE",
            "partial_reason": None,
            "system_process_count": 500,
            "bounded_candidate_count": 2,
            "opened_bounded_count": 2,
            "classified_bounded_count": 2,
            "access_denied_count": 0,
            "pid_reuse_count": 0,
            "omitted_count": 0,
            "exited_count": 0,
            "current_pid": 100,
            "controller_pid": 42,
            "bounded_identity_sha256": P.digest_value(process_projection),
            "rows": process_rows,
        },
        "effects": {
            "canonical_governed_path_mutated": False,
            "global_sidecar_path_mutated": False,
            "guard_only_replacement_attempted": False,
            "transaction_action_attempted": False,
            "directory_membership_changed": False,
        },
    }
    return {
        "schema_version": P.RAW_SCHEMA,
        "generation_id": "T550-HOS-V9-V3-1-DRAFT",
        "phase": phase,
        "evidence": evidence,
        "checker": {
            "checker_artifact_id": "live_instance_checker",
            "checker_sha256": graph_nodes["live_instance_checker"]["sha256"],
            "checker_run_token": f"checker-{phase}-{offset}",
            "checked_phase": phase,
            "checked_evidence_sha256": P.digest_value(evidence),
            "status": "PASS_BOUNDED_READ_ONLY",
            "start_wall_utc": iso(offset + 6),
            "end_wall_utc": iso(offset + 7),
            "start_monotonic_ns": MONO + (offset + 6) * 1_000_000_000,
            "end_monotonic_ns": MONO + (offset + 7) * 1_000_000_000,
        },
        "candidate_only": True,
        "non_authorizing": True,
    }


def fixture() -> dict:
    component_doc = component()
    component_bytes = canonical(component_doc)
    component_sha = P.digest_bytes(component_bytes)
    graph_sha = P.digest_value(component_doc["artifact_graph"])
    freeze_doc = freeze(component_sha, graph_sha)
    freeze_bytes = canonical(freeze_doc)
    freeze_sha = P.digest_bytes(freeze_bytes)
    capability_doc = capability(freeze_doc, freeze_sha)
    prepare_doc = raw(
        "prepare",
        component_doc,
        component_sha,
        freeze_doc,
        freeze_sha,
        offset=0,
    )
    prepare_bytes = canonical(prepare_doc)
    return {
        "allowlist_bytes": allowlist_bytes(),
        "component_doc": component_doc,
        "component_bytes": component_bytes,
        "component_sha": component_sha,
        "freeze_doc": freeze_doc,
        "freeze_bytes": freeze_bytes,
        "freeze_sha": freeze_sha,
        "capability": capability_doc,
        "prepare_doc": prepare_doc,
        "prepare_bytes": prepare_bytes,
        "prepare_sha": P.digest_bytes(prepare_bytes),
    }


def rebuild_component(x: dict) -> None:
    x["component_bytes"] = canonical(x["component_doc"])
    x["component_sha"] = P.digest_bytes(x["component_bytes"])


def rebuild_freeze(x: dict) -> None:
    x["freeze_bytes"] = canonical(x["freeze_doc"])
    x["freeze_sha"] = P.digest_bytes(x["freeze_bytes"])
    x["capability"]["execution_freeze_sha256"] = x["freeze_sha"]


def rebuild_prepare(x: dict) -> None:
    x["prepare_doc"]["checker"]["checked_evidence_sha256"] = P.digest_value(
        x["prepare_doc"]["evidence"]
    )
    x["prepare_bytes"] = canonical(x["prepare_doc"])
    x["prepare_sha"] = P.digest_bytes(x["prepare_bytes"])


def validate_prepare(x: dict | None = None) -> dict:
    x = x or fixture()
    return P.validate_live_gate_policy_v3_1(
        static_allowlist_bytes=x["allowlist_bytes"],
        expected_static_allowlist_sha256=P.STATIC_ALLOWLIST_SHA256,
        component_lock_bytes=x["component_bytes"],
        expected_component_lock_sha256=x["component_sha"],
        execution_freeze_bytes=x["freeze_bytes"],
        expected_execution_freeze_sha256=x["freeze_sha"],
        expected_reviewed_release_sha256=x["freeze_doc"][
            "reviewed_release_sha256"
        ],
        raw_measurement_bytes=x["prepare_bytes"],
        expected_raw_measurement_sha256=x["prepare_sha"],
        capability_scope_projection=x["capability"],
        expected_capability_reference_sha256=sha(600),
        expected_phase="prepare",
        validation_wall_time_utc=iso(11),
        validation_monotonic_ns=MONO + 11 * 1_000_000_000,
    )


def publish_fixture(x: dict | None = None) -> dict:
    x = x or fixture()
    prepare_result = validate_prepare(x)
    prepare_result_bytes = canonical(prepare_result)
    prepare_result_sha = P.digest_bytes(prepare_result_bytes)
    publish_doc = raw(
        "publish",
        x["component_doc"],
        x["component_sha"],
        x["freeze_doc"],
        x["freeze_sha"],
        offset=20,
        prepare_raw_sha=x["prepare_sha"],
        prepare_result_sha=prepare_result_sha,
    )
    publish_bytes = canonical(publish_doc)
    return {
        **x,
        "prepare_result": prepare_result,
        "prepare_result_bytes": prepare_result_bytes,
        "prepare_result_sha": prepare_result_sha,
        "publish_doc": publish_doc,
        "publish_bytes": publish_bytes,
        "publish_sha": P.digest_bytes(publish_bytes),
    }


def validate_publish(x: dict | None = None) -> dict:
    x = x or publish_fixture()
    return P.validate_live_gate_policy_v3_1(
        static_allowlist_bytes=x["allowlist_bytes"],
        expected_static_allowlist_sha256=P.STATIC_ALLOWLIST_SHA256,
        component_lock_bytes=x["component_bytes"],
        expected_component_lock_sha256=x["component_sha"],
        execution_freeze_bytes=x["freeze_bytes"],
        expected_execution_freeze_sha256=x["freeze_sha"],
        expected_reviewed_release_sha256=x["freeze_doc"][
            "reviewed_release_sha256"
        ],
        raw_measurement_bytes=x["publish_bytes"],
        expected_raw_measurement_sha256=x["publish_sha"],
        capability_scope_projection=x["capability"],
        expected_capability_reference_sha256=sha(600),
        expected_phase="publish",
        validation_wall_time_utc=iso(31),
        validation_monotonic_ns=MONO + 31 * 1_000_000_000,
        prepare_raw_measurement_bytes=x["prepare_bytes"],
        independently_expected_prepare_raw_sha256=x["prepare_sha"],
        prepare_result_bytes=x["prepare_result_bytes"],
        independently_expected_prepare_result_sha256=x["prepare_result_sha"],
    )


def rejects(call, text: str) -> None:
    try:
        call()
    except P.LiveGatePolicyV31Error as exc:
        assert text.casefold() in str(exc).casefold(), str(exc)
    else:
        raise AssertionError(f"expected LiveGatePolicyV31Error containing {text!r}")


def test_prepare_is_machine_only_and_binds_real_allowlist() -> None:
    result = validate_prepare()
    assert result["success_label"] == P.SUCCESS_LABEL
    assert result["static_allowlist_sha256"] == P.STATIC_ALLOWLIST_SHA256
    assert result["governed_member_count"] == 13
    assert result["replacement_count"] == 8
    assert result["guard_only_count"] == 5
    assert result["human_identity_verified"] is False
    assert result["effect_authorized"] is False
    assert result["canonical_execution_blocked"] is True


def test_root_and_one_level_parent_projection_passes() -> None:
    x = fixture()
    assert x["freeze_doc"]["canonical_parents"][0]["path_token"] == "."
    assert (
        x["freeze_doc"]["canonical_parents"][0]["identity"]
        == x["freeze_doc"]["environment"]["model_identity"]
    )
    assert {row["path_token"] for row in x["freeze_doc"]["sentinels"]} == {
        "low_confidence_register.jsonl",
        "frontier_escalation_queue.jsonl",
        "atlas_candidate_feed.jsonl",
    }
    assert any(
        row["path_token"].startswith("receipts/")
        for row in x["freeze_doc"]["targets"]
    )
    validate_prepare(x)


def test_exact_allowlist_substitution_rejected() -> None:
    x = fixture()
    altered = json.loads(x["allowlist_bytes"])
    altered["targets"][0]["role"] = "attacker-role"
    x["allowlist_bytes"] = json.dumps(altered).encode("utf-8")
    rejects(lambda: validate_prepare(x), "hash")


def test_model_root_parent_identity_swap_rejected() -> None:
    x = fixture()
    x["freeze_doc"]["canonical_parents"][0]["identity"] = identity(
        999, directory=True
    )
    rebuild_freeze(x)
    x["prepare_doc"]["evidence"]["execution_freeze_sha256"] = x["freeze_sha"]
    x["prepare_doc"]["evidence"]["canonical_parents"] = deepcopy(
        x["freeze_doc"]["canonical_parents"]
    )
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "model-root")


def test_graph_extra_dependency_rejected() -> None:
    x = fixture()
    x["component_doc"]["artifact_graph"]["nodes"].append(
        {
            "artifact_id": "zz-extra",
            "artifact_type": "post_component_review",
            "sha256": sha(9_001),
            "depends_on": [],
        }
    )
    rebuild_component(x)
    rejects(lambda: validate_prepare(x), "extra or missing")


def test_graph_back_edge_rejected() -> None:
    x = fixture()
    node = next(
        row
        for row in x["component_doc"]["artifact_graph"]["nodes"]
        if row["artifact_id"] == "contract"
    )
    node["depends_on"] = ["sealed_launcher"]
    rebuild_component(x)
    rejects(lambda: validate_prepare(x), "dependency edge")


def test_current_executable_hash_drift_rejected() -> None:
    x = fixture()
    current = x["prepare_doc"]["evidence"]["bounded_process_snapshot"]["rows"][1]
    current["executable"]["sha256"] = sha(9_002)
    fields = (
        "pid",
        "parent_pid",
        "creation_token",
        "normalized_name",
        "process_handle_access",
        "liveness_status",
        "executable",
    )
    rows = x["prepare_doc"]["evidence"]["bounded_process_snapshot"]["rows"]
    x["prepare_doc"]["evidence"]["bounded_process_snapshot"][
        "bounded_identity_sha256"
    ] = P.digest_value([{key: row[key] for key in fields} for row in rows])
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "frozen current executable")


def test_unclassified_current_name_rejected() -> None:
    x = fixture()
    x["prepare_doc"]["evidence"]["bounded_process_snapshot"]["rows"][1][
        "normalized_name"
    ] = "evil.exe"
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "unclassified")


def test_incomplete_process_snapshot_rejected() -> None:
    x = fixture()
    snapshot = x["prepare_doc"]["evidence"]["bounded_process_snapshot"]
    snapshot["snapshot_status"] = "PARTIAL"
    snapshot["partial_reason"] = "access_denied"
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "partial or uncertain")


def test_omitted_bounded_process_rejected() -> None:
    x = fixture()
    snapshot = x["prepare_doc"]["evidence"]["bounded_process_snapshot"]
    snapshot["omission_status"] = "OMITTED"
    snapshot["omitted_count"] = 1
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "partial or uncertain")


def test_pid_reuse_rejected() -> None:
    x = fixture()
    snapshot = x["prepare_doc"]["evidence"]["bounded_process_snapshot"]
    snapshot["pid_reuse_status"] = "DETECTED"
    snapshot["pid_reuse_count"] = 1
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "partial or uncertain")


def test_unrelated_onedrive_writer_rejected() -> None:
    x = fixture()
    snapshot = x["prepare_doc"]["evidence"]["bounded_process_snapshot"]
    extra = deepcopy(snapshot["rows"][0])
    extra.update(
        {
            "pid": 777,
            "parent_pid": 1,
            "creation_token": "onedrive-start",
            "normalized_name": "onedrive.exe",
            "executable": executable(777),
        }
    )
    snapshot["rows"].append(extra)
    for key in (
        "bounded_candidate_count",
        "opened_bounded_count",
        "classified_bounded_count",
    ):
        snapshot[key] = 3
    fields = (
        "pid",
        "parent_pid",
        "creation_token",
        "normalized_name",
        "process_handle_access",
        "liveness_status",
        "executable",
    )
    snapshot["bounded_identity_sha256"] = P.digest_value(
        [{key: row[key] for key in fields} for row in snapshot["rows"]]
    )
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "unrelated bounded writer")


def test_guard_only_replacement_request_rejected() -> None:
    x = fixture()
    guard = next(
        row
        for row in x["prepare_doc"]["evidence"]["targets"]
        if row["operation"] == "guard_only"
    )
    guard["replacement_requested"] = True
    rebuild_prepare(x)
    rejects(lambda: validate_prepare(x), "replacement requested")


def test_reversed_checker_interval_rejected() -> None:
    x = fixture()
    checker = x["prepare_doc"]["checker"]
    checker["start_wall_utc"], checker["end_wall_utc"] = (
        checker["end_wall_utc"],
        checker["start_wall_utc"],
    )
    checker["start_monotonic_ns"], checker["end_monotonic_ns"] = (
        checker["end_monotonic_ns"],
        checker["start_monotonic_ns"],
    )
    x["prepare_bytes"] = canonical(x["prepare_doc"])
    x["prepare_sha"] = P.digest_bytes(x["prepare_bytes"])
    rejects(lambda: validate_prepare(x), "checker causal chronology")


def test_publish_green_and_prepare_recomputes() -> None:
    result = validate_publish()
    assert result["phase"] == "publish"
    assert result["publication_authorized"] is False
    assert result["canonical_execution_blocked"] is True


def test_publish_before_prepare_rejected() -> None:
    x = publish_fixture()
    publish = raw(
        "publish",
        x["component_doc"],
        x["component_sha"],
        x["freeze_doc"],
        x["freeze_sha"],
        offset=0,
        prepare_raw_sha=x["prepare_sha"],
        prepare_result_sha=x["prepare_result_sha"],
    )
    x["publish_doc"] = publish
    x["publish_bytes"] = canonical(publish)
    x["publish_sha"] = P.digest_bytes(x["publish_bytes"])
    rejects(lambda: validate_publish(x), "prepare/publish causal chronology")


def test_prepare_result_substitution_rejected() -> None:
    x = publish_fixture()
    x["prepare_result"]["effect_authorized"] = True
    x["prepare_result_bytes"] = canonical(x["prepare_result"])
    x["prepare_result_sha"] = P.digest_bytes(x["prepare_result_bytes"])
    x["publish_doc"]["evidence"]["causal_parent"][
        "prepare_result_sha256"
    ] = x["prepare_result_sha"]
    x["publish_doc"]["checker"]["checked_evidence_sha256"] = P.digest_value(
        x["publish_doc"]["evidence"]
    )
    x["publish_bytes"] = canonical(x["publish_doc"])
    x["publish_sha"] = P.digest_bytes(x["publish_bytes"])
    rejects(lambda: validate_publish(x), "prepare result does not recompute")
