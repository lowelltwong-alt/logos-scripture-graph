from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/checks/rematerialization_live_gate_policy_v3.py"
SPEC = importlib.util.spec_from_file_location("t550_policy_v3", MODULE)
assert SPEC and SPEC.loader
P = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = P
SPEC.loader.exec_module(P)

BASE = datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc)
MONO = 9_000_000_000_000


def iso(seconds: int) -> str:
    return (BASE + timedelta(seconds=seconds)).isoformat().replace("+00:00", "Z")


def sha(number: int) -> str:
    return f"{number:064x}"


def ident(number: int, directory: bool) -> dict:
    return {
        "volume_serial": 77,
        "file_id": f"file-{number}",
        "attributes": 16 if directory else 32,
        "is_directory": directory,
        "reparse_point": False,
    }


def component() -> dict:
    dependencies = [
        {"artifact_id": name, "sha256": sha(100 + index)}
        for index, name in enumerate(sorted(P.REQUIRED_DEPENDENCY_IDS))
    ]
    for row in dependencies:
        exact = {
            "design_boss_ruling": P.DESIGN_BOSS_RULING_SHA256,
            "corrected_design_resolution": P.CORRECTED_DESIGN_RESOLUTION_SHA256,
            "corrected_design_boss_check": P.CORRECTED_DESIGN_BOSS_CHECK_SHA256,
        }.get(row["artifact_id"])
        if exact:
            row["sha256"] = exact
    return {
        "schema_version": P.COMPONENT_SCHEMA,
        "generation_id": "v9-v3-static-generation",
        "contract_sha256": P.CONTRACT_SHA256,
        "policy_docket_sha256": P.POLICY_DOCKET_SHA256,
        "windows_docket_sha256": P.WINDOWS_DOCKET_SHA256,
        "v2_rejection_sha256": P.V2_REJECTION_SHA256,
        "design_boss_ruling_sha256": P.DESIGN_BOSS_RULING_SHA256,
        "corrected_design_resolution_sha256": P.CORRECTED_DESIGN_RESOLUTION_SHA256,
        "corrected_design_boss_check_sha256": P.CORRECTED_DESIGN_BOSS_CHECK_SHA256,
        "hash_topology": {
            "external_trust_anchor_kind": "product_runtime_detached_digest_api",
            "component_lock_contains_own_digest": False,
            "component_lock_contains_post_component_review_hashes": False,
            "execution_freeze_contains_own_digest": False,
            "runtime_capability_supplies_execution_freeze_digest": True,
        },
        "review_timing_policy": {
            "static_reviews_before_restart": True,
            "live_instance_checker_inside_lease": True,
            "human_or_async_wait_inside_lease": False,
        },
        "dependencies": dependencies,
        "bounded_process_names": list(P.BOUNDED_PROCESS_NAMES),
        "bounded_process_policy_sha256": P.digest_value(
            list(P.BOUNDED_PROCESS_NAMES)
        ),
        "candidate_only": True,
        "non_authorizing": True,
    }


def freeze(component_sha: str, capability_sha: str) -> dict:
    parents = [
        {
            "ordinal": ordinal,
            "id": f"parent-{ordinal}",
            "path_token": f"area-{ordinal}/parent",
            "identity": ident(10 + ordinal, True),
        }
        for ordinal in range(1, 5)
    ]
    targets = []
    for ordinal in range(1, 14):
        parent = parents[(ordinal - 1) % 3]
        targets.append(
            {
                "ordinal": ordinal,
                "id": f"target-{ordinal:02d}",
                "role": f"book-local-{ordinal:02d}",
                "path_token": f"{parent['path_token']}/target-{ordinal:02d}.json",
                "parent_id": parent["id"],
                "leaf_name": f"target-{ordinal:02d}.json",
                "identity": ident(100 + ordinal, False),
                "size_bytes": 1000 + ordinal,
                "ntfs_link_count": 1,
                "preimage_sha256": sha(200 + ordinal),
                "staged_sha256": sha(300 + ordinal),
            }
        )
    sentinels = []
    for ordinal in range(1, 4):
        parent = parents[3]
        sentinels.append(
            {
                "ordinal": ordinal,
                "id": f"sentinel-{ordinal}",
                "role": f"global-sidecar-{ordinal}",
                "path_token": f"{parent['path_token']}/sentinel-{ordinal}.jsonl",
                "parent_id": parent["id"],
                "leaf_name": f"sentinel-{ordinal}.jsonl",
                "identity": ident(200 + ordinal, False),
                "size_bytes": 2000 + ordinal,
                "ntfs_link_count": 1,
                "expected_sha256": sha(400 + ordinal),
            }
        )
    volume = {
        "volume_guid": "volume-guid-77",
        "volume_serial": 77,
        "filesystem": "NTFS",
        "filesystem_flags": ["case-preserved", "unicode"],
        "volume_root_identity": ident(1, True),
        "workspace_identity": ident(2, True),
        "model_identity": ident(3, True),
    }
    return {
        "schema_version": P.FREEZE_SCHEMA,
        "task_id": "T550",
        "book": "Hos",
        "application_id": "T550-HOS-V9-V3",
        "freeze_id": "v3-freeze-1",
        "frozen_at_utc": iso(-100),
        "pre_freeze_boot_identity": "old-boot",
        "component_lock_sha256": component_sha,
        "reviewed_release_sha256": sha(888),
        "identity_lifetime_policy": {
            "stable_pre_restart_only": True,
            "ephemeral_pid_start_handle_ancestry_frozen": False,
            "ephemeral_prepare_publish_continuity_only": True,
        },
        "targets": targets,
        "target_tuple_sha256": P.digest_value(targets),
        "sentinels": sentinels,
        "sentinel_tuple_sha256": P.digest_value(sentinels),
        "canonical_parents": parents,
        "os_allowlist": {
            "name": "Windows",
            "build": "26100",
            "native_architecture": "AMD64",
            "runtime_architecture": "64bit",
        },
        "volume_allowlist": volume,
        "bounded_process_policy_sha256": P.digest_value(
            list(P.BOUNDED_PROCESS_NAMES)
        ),
        "capability_reference_sha256": capability_sha,
        "permitted_phases": ["prepare", "publish", "rollback_only_recovery"],
        "candidate_only": True,
        "non_authorizing": True,
    }


def capability(freeze_doc: dict, freeze_sha: str, reference_sha: str) -> dict:
    return {
        "reference_sha256": reference_sha,
        "asserted_principal": "Lowell Wong",
        "task_id": "T550",
        "book": "Hos",
        "application_id": freeze_doc["application_id"],
        "execution_freeze_sha256": freeze_sha,
        "reviewed_release_sha256": freeze_doc["reviewed_release_sha256"],
        "target_tuple_sha256": freeze_doc["target_tuple_sha256"],
        "sentinel_tuple_sha256": freeze_doc["sentinel_tuple_sha256"],
        "permitted_phases": ["prepare", "publish", "rollback_only_recovery"],
        "issued_at_utc": iso(-20),
        "expires_at_utc": iso(100),
        "identity_assurance": "external_unverified_by_pure_policy",
        "local_json_alone_sufficient": False,
        "denied_effects": P.DENIED_EFFECTS,
    }


def raw(phase: str, freeze_doc: dict, component_doc: dict, component_sha: str, offset: int = 0) -> dict:
    start, end = offset, offset + 3
    parents = deepcopy(freeze_doc["canonical_parents"])
    parent_map = {row["id"]: row for row in parents}
    targets = []
    for item in freeze_doc["targets"]:
        targets.append(
            {
                "ordinal": item["ordinal"],
                "id": item["id"],
                "role": item["role"],
                "path_token": item["path_token"],
                "parent_id": item["parent_id"],
                "parent_identity": deepcopy(parent_map[item["parent_id"]]["identity"]),
                "leaf_name": item["leaf_name"],
                "identity": deepcopy(item["identity"]),
                "size_bytes": item["size_bytes"],
                "ntfs_link_count": item["ntfs_link_count"],
                "expected_preimage_sha256": item["preimage_sha256"],
                "expected_staged_sha256": item["staged_sha256"],
                "observed_sha256": item["preimage_sha256"],
                "root_relative_opened": True,
                "observation_wall_utc": iso(offset + 1),
                "observation_monotonic_ns": MONO + (offset + 1) * 1_000_000_000,
            }
        )
    sentinels = []
    for item in freeze_doc["sentinels"]:
        sentinels.append(
            {
                "ordinal": item["ordinal"],
                "id": item["id"],
                "role": item["role"],
                "path_token": item["path_token"],
                "parent_id": item["parent_id"],
                "parent_identity": deepcopy(parent_map[item["parent_id"]]["identity"]),
                "leaf_name": item["leaf_name"],
                "identity": deepcopy(item["identity"]),
                "size_bytes": item["size_bytes"],
                "ntfs_link_count": item["ntfs_link_count"],
                "expected_sha256": item["expected_sha256"],
                "observed_sha256": item["expected_sha256"],
                "root_relative_opened": True,
                "observation_wall_utc": iso(offset + 1),
                "observation_monotonic_ns": MONO + (offset + 1) * 1_000_000_000,
            }
        )
    deps = deepcopy(component_doc["dependencies"])
    collector_sha = next(
        row["sha256"] for row in deps if row["artifact_id"] == "production_collector"
    )
    live_checker_sha = next(
        row["sha256"] for row in deps if row["artifact_id"] == "live_instance_checker"
    )
    return {
        "schema_version": P.RAW_SCHEMA,
        "provenance": {
            "mode": "actual_windows_ntfs_sealed_v3",
            "production_collector_sha256": collector_sha,
            "component_lock_sha256": component_sha,
            "loaded_dependencies": deps,
            "provider_injection_available": False,
            "test_backend_available": False,
        },
        "evidence_class": "read_only_collector_zero_delta",
        "live_instance_checker": {
            "checker_id": "live_instance_checker",
            "checker_sha256": live_checker_sha,
            "status": "PASS_BOUNDED_READ_ONLY",
            "start_wall_utc": iso(offset + 1),
            "end_wall_utc": iso(offset + 2),
            "start_monotonic_ns": MONO + (offset + 1) * 1_000_000_000,
            "end_monotonic_ns": MONO + (offset + 2) * 1_000_000_000,
        },
        "task_id": "T550",
        "book": "Hos",
        "application_id": freeze_doc["application_id"],
        "phase": phase,
        "capture": {
            "capture_id": f"{phase}-{offset}",
            "start_wall_utc": iso(start),
            "end_wall_utc": iso(end),
            "start_monotonic_ns": MONO + start * 1_000_000_000,
            "end_monotonic_ns": MONO + end * 1_000_000_000,
            "max_duration_seconds": 60,
        },
        "boot": {"boot_identity": "new-boot", "boot_time_utc": iso(-90)},
        "operating_system": deepcopy(freeze_doc["os_allowlist"]),
        "volume": {
            key: deepcopy(freeze_doc["volume_allowlist"][key])
            for key in (
                "volume_guid",
                "volume_serial",
                "filesystem",
                "filesystem_flags",
                "volume_root_identity",
            )
        },
        "workspace_identity": deepcopy(
            freeze_doc["volume_allowlist"]["workspace_identity"]
        ),
        "model_identity": deepcopy(
            freeze_doc["volume_allowlist"]["model_identity"]
        ),
        "canonical_parents": parents,
        "targets": targets,
        "sentinels": sentinels,
        "observer_process_identity": {
            "pid": 100,
            "start_token": "current-start",
            "executable_identity": "current-executable",
        },
        "processes": [
            {
                "pid": 42,
                "parent_pid": 1,
                "normalized_name": "codex.exe",
                "start_token": "parent-start",
                "executable_identity": "parent-executable",
                "access_status": "opened_query_handle",
                "liveness_wait_result": "WAIT_TIMEOUT_RUNNING",
                "executable_handle_identity_available": True,
                "classification_status": "classified_by_code_fixed_policy",
                "observation_wall_utc": iso(offset + 2),
                "observation_monotonic_ns": MONO + (offset + 2) * 1_000_000_000,
            },
            {
                "pid": 100,
                "parent_pid": 42,
                "normalized_name": "python.exe",
                "start_token": "current-start",
                "executable_identity": "current-executable",
                "access_status": "opened_query_handle",
                "liveness_wait_result": "WAIT_TIMEOUT_RUNNING",
                "executable_handle_identity_available": True,
                "classification_status": "classified_by_code_fixed_policy",
                "observation_wall_utc": iso(offset + 2),
                "observation_monotonic_ns": MONO + (offset + 2) * 1_000_000_000,
            },
        ],
        "bounded_process_policy_sha256": P.digest_value(
            list(P.BOUNDED_PROCESS_NAMES)
        ),
        "effects": {
            "read_only_measurement": True,
            "probe_files_created": False,
            "directory_members_changed": False,
            "file_bytes_changed": False,
            "delete_or_replace_attempted": False,
            "publication_attempted": False,
        },
        "limitations": {
            "inventory_exhaustive": False,
            "future_or_preopened_writers_excluded": False,
            "lost_update_before_rename_possible": True,
            "overwrite_after_readback_possible": True,
            "power_loss_durability_claimed": False,
            "set_atomicity_claimed": False,
        },
        "candidate_only": True,
        "non_authorizing": True,
    }


def fixture(phase: str = "prepare", offset: int = 0):
    component_doc = component()
    component_bytes = P.canonical_json_bytes(component_doc)
    component_sha = P.digest_bytes(component_bytes)
    reference_sha = sha(999)
    freeze_doc = freeze(component_sha, reference_sha)
    freeze_bytes = P.canonical_json_bytes(freeze_doc)
    freeze_sha = P.digest_bytes(freeze_bytes)
    capability_doc = capability(freeze_doc, freeze_sha, reference_sha)
    raw_doc = raw(phase, freeze_doc, component_doc, component_sha, offset)
    raw_bytes = P.canonical_json_bytes(raw_doc)
    return {
        "component_doc": component_doc,
        "component_bytes": component_bytes,
        "component_sha": component_sha,
        "freeze_doc": freeze_doc,
        "freeze_bytes": freeze_bytes,
        "freeze_sha": freeze_sha,
        "capability": capability_doc,
        "reference_sha": reference_sha,
        "raw_doc": raw_doc,
        "raw_bytes": raw_bytes,
        "raw_sha": P.digest_bytes(raw_bytes),
    }


def validate_prepare(value=None):
    x = value or fixture()
    return P.validate_live_gate_policy_v3(
        component_lock_bytes=x["component_bytes"],
        expected_component_lock_sha256=x["component_sha"],
        execution_freeze_bytes=x["freeze_bytes"],
        expected_execution_freeze_sha256=x["freeze_sha"],
        expected_reviewed_release_sha256=x["freeze_doc"]["reviewed_release_sha256"],
        raw_measurement_bytes=x["raw_bytes"],
        expected_raw_measurement_sha256=x["raw_sha"],
        capability_scope_projection=x["capability"],
        expected_capability_reference_sha256=x["reference_sha"],
        expected_phase="prepare",
        validation_wall_time_utc=iso(5),
        validation_monotonic_ns=MONO + 5_000_000_000,
    )


def rebuild_raw(x):
    x["raw_bytes"] = P.canonical_json_bytes(x["raw_doc"])
    x["raw_sha"] = P.digest_bytes(x["raw_bytes"])
    return x


def test_prepare_pass_is_machine_only() -> None:
    result = validate_prepare()
    assert result["success_label"] == P.SUCCESS_LABEL
    assert result["human_identity_verified"] is False
    assert result["effect_authorized"] is False
    assert result["owner_capability_verification_outside_policy"] is True
    assert result["in_process_lease_outside_policy"] is True
    assert result["external_owner_capability_present_and_verified"] is False
    assert result["reviewed_release_origin_verified_by_pure_policy"] is False
    assert result["canonical_execution_blocked"] is True
    assert result["transaction_completion_authorized"] is False
    assert result["machine_blockers"] == P.MACHINE_BLOCKERS
    assert "before_single_completed_transition" in result["required_terminal_ordering"]


def test_exact_shell_then_codex_controller_chain_is_permitted() -> None:
    x = fixture()
    current = next(
        row for row in x["raw_doc"]["processes"] if row["pid"] == 100
    )
    current["parent_pid"] = 43
    x["raw_doc"]["processes"].append(
        {
            "pid": 43,
            "parent_pid": 42,
            "normalized_name": "pwsh.exe",
            "start_token": "shell-start",
            "executable_identity": "shell-executable",
            "access_status": "opened_query_handle",
            "liveness_wait_result": "WAIT_TIMEOUT_RUNNING",
            "executable_handle_identity_available": True,
            "classification_status": "classified_by_code_fixed_policy",
            "observation_wall_utc": iso(2),
            "observation_monotonic_ns": MONO + 2_000_000_000,
        }
    )
    rebuild_raw(x)
    assert validate_prepare(x)["success_label"] == P.SUCCESS_LABEL


def test_unrelated_codex_process_remains_a_writer_blocker() -> None:
    x = fixture()
    x["raw_doc"]["processes"].append(
        {
            "pid": 777,
            "parent_pid": 1,
            "normalized_name": "codex.exe",
            "start_token": "unrelated-codex-start",
            "executable_identity": "unrelated-codex-executable",
            "access_status": "opened_query_handle",
            "liveness_wait_result": "WAIT_TIMEOUT_RUNNING",
            "executable_handle_identity_available": True,
            "classification_status": "classified_by_code_fixed_policy",
            "observation_wall_utc": iso(2),
            "observation_monotonic_ns": MONO + 2_000_000_000,
        }
    )
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match="writer blocker"):
        validate_prepare(x)


def test_duplicate_key_rejected_before_policy() -> None:
    raw_bytes = b'{"a":1,"a":2}\n'
    with pytest.raises(P.LiveGatePolicyV3Error, match="duplicate JSON key"):
        P.parse_canonical_bytes(raw_bytes, P.digest_bytes(raw_bytes), "probe")


def test_detached_raw_hash_one_bit_drift_rejected() -> None:
    x = fixture()
    wrong = ("0" if x["raw_sha"][0] != "0" else "1") + x["raw_sha"][1:]
    with pytest.raises(P.LiveGatePolicyV3Error, match="detached hash"):
        P.validate_live_gate_policy_v3(
            component_lock_bytes=x["component_bytes"],
            expected_component_lock_sha256=x["component_sha"],
            execution_freeze_bytes=x["freeze_bytes"],
            expected_execution_freeze_sha256=x["freeze_sha"],
            expected_reviewed_release_sha256=x["freeze_doc"]["reviewed_release_sha256"],
            raw_measurement_bytes=x["raw_bytes"],
            expected_raw_measurement_sha256=wrong,
            capability_scope_projection=x["capability"],
            expected_capability_reference_sha256=x["reference_sha"],
            expected_phase="prepare",
            validation_wall_time_utc=iso(5),
            validation_monotonic_ns=MONO + 5_000_000_000,
        )


@pytest.mark.parametrize(
    ("mutation", "match"),
    [
        (lambda r: r["targets"][0].__setitem__("parent_id", "parent-2"), "parent_id"),
        (lambda r: r["targets"][0].__setitem__("leaf_name", "other.json"), "leaf_name"),
        (lambda r: r["targets"][0].__setitem__("identity", ident(999, False)), "file identity"),
    ],
)
def test_v2_parent_swap_and_same_parent_file_substitution_rejected(mutation, match) -> None:
    x = fixture()
    mutation(x["raw_doc"])
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match=match):
        validate_prepare(x)


def test_v2_hidden_writer_is_derived_and_rejected() -> None:
    x = fixture()
    x["raw_doc"]["processes"].append(
        {
            "pid": 777,
            "parent_pid": 1,
            "normalized_name": "onedrive.exe",
            "start_token": "od-start",
            "executable_identity": "od-exe",
            "access_status": "opened_query_handle",
            "liveness_wait_result": "WAIT_TIMEOUT_RUNNING",
            "executable_handle_identity_available": True,
            "classification_status": "classified_by_code_fixed_policy",
            "observation_wall_utc": iso(2),
            "observation_monotonic_ns": MONO + 2_000_000_000,
        }
    )
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match="OneDrive"):
        validate_prepare(x)


def test_v2_boot_after_capture_rejected() -> None:
    x = fixture()
    x["raw_doc"]["boot"]["boot_time_utc"] = iso(10)
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match="chronology"):
        validate_prepare(x)


def test_v2_parent_identity_alias_rejected_by_freeze() -> None:
    x = fixture()
    x["freeze_doc"]["canonical_parents"][1]["identity"] = deepcopy(
        x["freeze_doc"]["canonical_parents"][0]["identity"]
    )
    x["freeze_bytes"] = P.canonical_json_bytes(x["freeze_doc"])
    x["freeze_sha"] = P.digest_bytes(x["freeze_bytes"])
    x["capability"]["execution_freeze_sha256"] = x["freeze_sha"]
    with pytest.raises(P.LiveGatePolicyV3Error, match="parent identity alias"):
        validate_prepare(x)


def publish(prepare, current, prepare_result, **overrides):
    result_bytes = P.canonical_json_bytes(prepare_result)
    args = dict(
        component_lock_bytes=current["component_bytes"],
        expected_component_lock_sha256=current["component_sha"],
        execution_freeze_bytes=current["freeze_bytes"],
        expected_execution_freeze_sha256=current["freeze_sha"],
        expected_reviewed_release_sha256=current["freeze_doc"]["reviewed_release_sha256"],
        raw_measurement_bytes=current["raw_bytes"],
        expected_raw_measurement_sha256=current["raw_sha"],
        capability_scope_projection=current["capability"],
        expected_capability_reference_sha256=current["reference_sha"],
        expected_phase="publish",
        validation_wall_time_utc=iso(15),
        validation_monotonic_ns=MONO + 15_000_000_000,
        prepare_raw_measurement_bytes=prepare["raw_bytes"],
        independently_expected_prepare_raw_sha256=prepare["raw_sha"],
        prepare_result_bytes=result_bytes,
        independently_expected_prepare_result_sha256=P.digest_bytes(result_bytes),
    )
    args.update(overrides)
    return P.validate_live_gate_policy_v3(**args)


def test_publish_requires_independently_supplied_prepare_hashes() -> None:
    prep = fixture()
    prep_result = validate_prepare(prep)
    current = fixture("publish", 10)
    result = publish(prep, current, prep_result)
    assert result["success_label"] == P.SUCCESS_LABEL
    assert result["expected_prepare_raw_sha256"] == prep["raw_sha"]
    with pytest.raises(P.LiveGatePolicyV3Error, match="detached hash"):
        publish(
            prep,
            current,
            prep_result,
            independently_expected_prepare_raw_sha256=sha(12345),
        )


def test_publish_recomputes_exact_prepare_result() -> None:
    prep = fixture()
    prep_result = validate_prepare(prep)
    prep_result["effect_authorized"] = True
    current = fixture("publish", 10)
    with pytest.raises(P.LiveGatePolicyV3Error, match="recompute"):
        publish(prep, current, prep_result)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda r: r["observer_process_identity"].__setitem__("start_token", "changed"),
        lambda r: r["processes"][0].__setitem__("executable_identity", "changed"),
        lambda r: r["sentinels"][0].__setitem__("size_bytes", 99999),
        lambda r: r["volume"].__setitem__("volume_guid", "other-volume"),
    ],
)
def test_prepare_publish_full_continuity_rejects_one_bit_material_drift(mutation) -> None:
    prep = fixture()
    prep_result = validate_prepare(prep)
    current = fixture("publish", 10)
    mutation(current["raw_doc"])
    rebuild_raw(current)
    with pytest.raises(P.LiveGatePolicyV3Error):
        publish(prep, current, prep_result)


def test_local_capability_json_cannot_claim_human_identity() -> None:
    x = fixture()
    x["capability"]["identity_assurance"] = "human_identity_verified"
    with pytest.raises(P.LiveGatePolicyV3Error, match="overclaim"):
        validate_prepare(x)


def test_process_access_uncertainty_is_a_hard_block() -> None:
    x = fixture()
    x["raw_doc"]["processes"][0]["access_status"] = "access_denied"
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match="access uncertainty"):
        validate_prepare(x)


def test_hardlink_count_must_be_exactly_one() -> None:
    x = fixture()
    x["raw_doc"]["targets"][0]["ntfs_link_count"] = 2
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match="hardlink"):
        validate_prepare(x)


def test_synthetic_receipt_cannot_satisfy_read_only_policy() -> None:
    x = fixture()
    x["raw_doc"]["evidence_class"] = "synthetic_transaction_intended_delta"
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match="conflated"):
        validate_prepare(x)


def test_live_instance_checker_must_pass_inside_lease() -> None:
    x = fixture()
    x["raw_doc"]["live_instance_checker"]["status"] = "coverage_unavailable"
    rebuild_raw(x)
    with pytest.raises(P.LiveGatePolicyV3Error, match="did not pass"):
        validate_prepare(x)


def test_pre_restart_freeze_cannot_contain_ephemeral_identity_expectations() -> None:
    x = fixture()
    x["freeze_doc"]["identity_lifetime_policy"][
        "ephemeral_pid_start_handle_ancestry_frozen"
    ] = True
    x["freeze_bytes"] = P.canonical_json_bytes(x["freeze_doc"])
    x["freeze_sha"] = P.digest_bytes(x["freeze_bytes"])
    x["capability"]["execution_freeze_sha256"] = x["freeze_sha"]
    with pytest.raises(P.LiveGatePolicyV3Error, match="ephemeral freeze"):
        validate_prepare(x)

def test_contract_and_design_hashes_are_exact() -> None:
    assert P.CONTRACT_SHA256 == "28b503b96b6790d65c72685caa4d6c63ea68a6cfb4473dddb5612d0c60d71b22"
    assert P.POLICY_DOCKET_SHA256 == "142b322c9d647da9290743d2676244008f7694e2375f45073318285ca7943a46"
    assert P.WINDOWS_DOCKET_SHA256 == "a2f7944cb33161457d7f092631046c1608ed7c6be8422c04800ec9c56dc781bd"
    assert P.V2_REJECTION_SHA256 == "24546d7abddf881e5fdb7fff872dc3cb386ad81c2b8bdee04147badfa66f9c2f"
    assert P.DESIGN_BOSS_RULING_SHA256 == "67af1a7766947172c0197b58a161d3a6af669010d1ff9c68dac59b9b8e4fa6ee"
    assert P.CORRECTED_DESIGN_RESOLUTION_SHA256 == "e5a727f849ff242079151722dd93fd214a34bf0e40de6be6c01b6c811c301e85"
    assert P.CORRECTED_DESIGN_BOSS_CHECK_SHA256 == "9963403f8e639c1765ca28151df2e06c34d07b26a51b83e9ca19b5507425f7f8"
