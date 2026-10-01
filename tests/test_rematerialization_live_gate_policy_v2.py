from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
    / "rematerialization_live_gate_policy_v2.py"
)
SPEC = importlib.util.spec_from_file_location("live_gate_policy_v2", MODULE)
assert SPEC and SPEC.loader
POLICY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = POLICY
SPEC.loader.exec_module(POLICY)

BASE = datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc)
MONO = 5_000_000_000_000


def iso(seconds: int) -> str:
    return (BASE + timedelta(seconds=seconds)).isoformat().replace("+00:00", "Z")


def sha(number: int) -> str:
    return f"{number:064x}"


def identity(number: int, *, directory: bool = False) -> dict:
    return {
        "volume_serial": 77,
        "file_id": f"file-{number}",
        "attributes": 16 if directory else 32,
        "is_directory": directory,
        "reparse_point": False,
    }


def target_expectations() -> list[dict]:
    return [
        {
            "ordinal": n,
            "target_id": f"hos-{n:02d}",
            "role": f"book-local-{n:02d}",
            "path_token": f"reviews/Hos/target-{n:02d}.json",
            "preimage_sha256": sha(n),
            "staged_sha256": sha(100 + n),
        }
        for n in range(1, 14)
    ]


def sentinel_expectations() -> list[dict]:
    return [
        {
            "ordinal": n,
            "sentinel_id": f"global-{n}",
            "role": f"global-sidecar-{n}",
            "path_token": f"global/sidecar-{n}.jsonl",
            "expected_sha256": sha(200 + n),
        }
        for n in range(1, 4)
    ]


def expectations() -> dict:
    return {
        "schema_version": POLICY.EXPECTATIONS_SCHEMA_VERSION,
        "contract_sha256": POLICY.CONTRACT_SHA256,
        "predecessor_rejection_sha256": POLICY.PREDECESSOR_REJECTION_SHA256,
        "task_id": "T550",
        "book": "Hos",
        "application_id": "T550-HOS-V9-TEST",
        "freeze": {
            "freeze_id": "freeze-v9-test",
            "frozen_at_utc": iso(-100),
            "pre_freeze_boot_identity": "old-boot",
            "implementation_and_test_hashes": [
                {"artifact_id": "adapter", "sha256": sha(301)},
                {"artifact_id": "policy", "sha256": sha(302)},
            ],
            "evidence_hashes": [
                {"artifact_id": "boss", "sha256": sha(303)},
                {"artifact_id": "checker", "sha256": sha(304)},
            ],
            "targets": target_expectations(),
            "sentinels": sentinel_expectations(),
            "bounded_process_names": list(POLICY.BOUNDED_PROCESS_NAMES),
            "bounded_process_policy_sha256": POLICY.process_policy_sha256(),
        },
        "human_authorization": {
            "reference_id": "external-user-message-v9",
            "source_kind": "external_human_attestation",
            "source_reference": "codex-task:T550:user-message:future",
            "asserted_principal": "Lowell Wong",
            "authorization_text_sha256": sha(400),
            "identity_assurance": (
                "external_evidence_not_cryptographic_identity_proof"
            ),
            "local_json_alone_sufficient": False,
            "observed_by_checker": True,
            "observed_by_boss": True,
            "revoked": False,
        },
        "candidate_only": True,
        "non_authorizing": True,
    }


def measurement(phase: str, offset: int = 0) -> dict:
    targets = target_expectations()
    sentinels = sentinel_expectations()
    open_wall = iso(offset + 2)
    open_mono = MONO + (offset + 2) * 1_000_000_000
    parents = [
        {
            "parent_id": "parent-a",
            "path_token": "book_chunks/Hos",
            "identity": identity(900, directory=True),
        },
        {
            "parent_id": "parent-b",
            "path_token": "reviews/Hos",
            "identity": identity(901, directory=True),
        },
        {
            "parent_id": "parent-c",
            "path_token": "receipts",
            "identity": identity(902, directory=True),
        },
        {
            "parent_id": "parent-global",
            "path_token": "global",
            "identity": identity(903, directory=True),
        },
    ]
    return {
        "schema_version": POLICY.MEASUREMENT_SCHEMA_VERSION,
        "gate_id": f"gate-{phase}-{offset}",
        "task_id": "T550",
        "book": "Hos",
        "application_id": "T550-HOS-V9-TEST",
        "phase": phase,
        "capture": {
            "start_wall_time_utc": iso(offset),
            "end_wall_time_utc": iso(offset + 4),
            "start_monotonic_ns": MONO + offset * 1_000_000_000,
            "end_monotonic_ns": MONO + (offset + 4) * 1_000_000_000,
            "max_duration_seconds": 60,
        },
        "boot": {
            "boot_identity": "new-boot",
            "boot_time_utc": iso(-90),
        },
        "operating_system": {
            "name": "Windows",
            "version": "10.0",
            "build": "26100",
            "architecture": "AMD64",
        },
        "volume": {
            "volume_guid": r"\\?\Volume{test}\\",
            "volume_serial": 77,
            "filesystem": "NTFS",
            "filesystem_flags": ["case-preserved", "unicode"],
        },
        "workspace": {
            "path_token": "workspace",
            "identity": identity(800, directory=True),
        },
        "model": {
            "path_token": ".ai/scratch/multi_model_bible_chunking/M7_sol",
            "identity": identity(801, directory=True),
        },
        "canonical_parents": parents,
        "parent_process": {
            "pid": 42,
            "start_token": "parent-start-token",
            "executable_identity": "codex-parent-image",
        },
        "targets": [
            {
                "ordinal": row["ordinal"],
                "target_id": row["target_id"],
                "role": row["role"],
                "path_token": row["path_token"],
                "parent_id": (
                    "parent-a"
                    if row["ordinal"] == 2
                    else "parent-c"
                    if row["ordinal"] == 13
                    else "parent-b"
                ),
                "identity": identity(row["ordinal"]),
                "size_bytes": 1000 + row["ordinal"],
                "expected_preimage_sha256": row["preimage_sha256"],
                "expected_staged_sha256": row["staged_sha256"],
                "observed_sha256": sha(row["ordinal"]),
                "regular_file": True,
                "reparse_point": False,
                "exclusive_open_succeeded": True,
                "open_wall_time_utc": open_wall,
                "open_monotonic_ns": open_mono,
            }
            for row in targets
        ],
        "sentinels": [
            {
                **row,
                "parent_id": "parent-global",
                "identity": identity(100 + row["ordinal"]),
                "size_bytes": 2000 + row["ordinal"],
                "observed_sha256": row["expected_sha256"],
                "regular_file": True,
                "reparse_point": False,
                "deny_write_delete_open_succeeded": True,
                "open_wall_time_utc": open_wall,
                "open_monotonic_ns": open_mono,
            }
            for row in sentinels
        ],
        "process_policy": {
            "names": list(POLICY.BOUNDED_PROCESS_NAMES),
            "sha256": POLICY.process_policy_sha256(),
        },
        "process_snapshot": {
            "inventory_exhaustive": False,
            "current_process_id": 99,
            "observed_process_count": 3,
            "matched_processes": [
                {
                    "pid": 99,
                    "name": "python.exe",
                    "classification": "current_gate_process",
                    "is_current_process": True,
                }
            ],
            "onedrive_matches": [],
            "in_scope_writer_matches": [],
            "observer_limitations_acknowledged": True,
        },
        "effects": {
            "read_only_measurement": True,
            "probe_files_created": False,
            "directory_members_changed": False,
            "file_bytes_changed": False,
            "delete_or_replace_attempted": False,
            "attempt_created": False,
            "restart_or_onedrive_action_attempted": False,
            "publication_attempted": False,
        },
        "residual_races": {
            "bounded_inventory_not_exhaustive": True,
            "future_or_preopened_writers_excluded": False,
            "lost_update_before_rename_possible": True,
            "overwrite_after_readback_possible": True,
            "process_crash_recovery_only": True,
            "power_loss_durability_claimed": False,
            "thirteen_file_set_atomicity_claimed": False,
            "global_sidecar_install_authorized": False,
        },
        "candidate_only": True,
        "non_authorizing": True,
    }


def validate_prepare(record: dict | None = None, expected: dict | None = None):
    return POLICY.validate_live_gate_policy_v2(
        record or measurement("prepare"),
        expected or expectations(),
        expected_phase="prepare",
        now_wall_time_utc=iso(5),
        now_monotonic_ns=MONO + 5_000_000_000,
    )


def test_valid_prepare_passes_and_hash_binds_full_raw_record() -> None:
    record = measurement("prepare")
    result = validate_prepare(record)
    assert result["verdict"] == "PASS"
    assert result["raw_measurement_sha256"] == POLICY.digest_value(record)
    assert result["human_identity_cryptographically_verified"] is False
    assert result["publication_authority_claimed"] is False


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("boot", "boot_identity"), "old-boot", "restart"),
        (("boot", "boot_time_utc"), iso(-101), "not after"),
        (("operating_system", "build"), "", "non-empty"),
        (("volume", "filesystem"), "ReFS", "NTFS"),
        (("workspace", "identity", "reparse_point"), True, "reparse"),
        (("canonical_parents", 0, "identity", "file_id"), "", "non-empty"),
        (("targets", 0, "role"), "wrong", "role drift"),
        (("targets", 0, "identity", "file_id"), "file-2", "alias"),
        (("targets", 0, "observed_sha256"), sha(999), "hash allowlist"),
        (("targets", 0, "exclusive_open_succeeded"), False, "must be True"),
        (("sentinels", 0, "observed_sha256"), sha(999), "hash allowlist"),
        (("process_policy", "names"), ["python.exe"], "omit names"),
        (("process_snapshot", "onedrive_matches"), [1], "OneDrive"),
        (("process_snapshot", "in_scope_writer_matches"), [1], "writer"),
        (("effects", "probe_files_created"), True, "must be False"),
        (
            ("residual_races", "power_loss_durability_claimed"),
            True,
            "must be False",
        ),
    ],
)
def test_protected_measurement_mutations_fail_closed(path, value, message) -> None:
    record = measurement("prepare")
    cursor = record
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match=message):
        validate_prepare(record)


def test_local_json_alone_never_satisfies_external_human_gate() -> None:
    expected = expectations()
    expected["human_authorization"]["local_json_alone_sufficient"] = True
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="local_json"):
        validate_prepare(expected=expected)


def test_unknown_raw_measurement_field_fails_closed() -> None:
    record = measurement("prepare")
    record["unconsumed_security_field"] = "would be lossy"
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="schema drift"):
        validate_prepare(record)


def test_dual_clock_staleness_fails_closed() -> None:
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="stale"):
        POLICY.validate_live_gate_policy_v2(
            measurement("prepare"),
            expectations(),
            expected_phase="prepare",
            now_wall_time_utc=iso(100),
            now_monotonic_ns=MONO + 100_000_000_000,
        )


def test_publish_revalidates_exact_prepare_pass_and_continuity() -> None:
    prepare = measurement("prepare")
    prepare_result = validate_prepare(prepare)
    publish = measurement("publish", 10)
    result = POLICY.validate_live_gate_policy_v2(
        publish,
        expectations(),
        expected_phase="publish",
        now_wall_time_utc=iso(15),
        now_monotonic_ns=MONO + 15_000_000_000,
        prepare_measurement=prepare,
        prepare_result=prepare_result,
    )
    assert result["verdict"] == "PASS"
    assert result["prepare_result_sha256"] == POLICY.digest_value(prepare_result)


def test_publish_rejects_forged_prepare_pass() -> None:
    prepare = measurement("prepare")
    prepare_result = validate_prepare(prepare)
    prepare_result["verdict"] = "PASS_BUT_FORGED"
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="recompute exactly"):
        POLICY.validate_live_gate_policy_v2(
            measurement("publish", 10),
            expectations(),
            expected_phase="publish",
            now_wall_time_utc=iso(15),
            now_monotonic_ns=MONO + 15_000_000_000,
            prepare_measurement=prepare,
            prepare_result=prepare_result,
        )


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        ("volume", "volume_guid", r"\\?\Volume{drift}\\"),
        ("parent_process", "start_token", "new-parent"),
    ],
)
def test_publish_rejects_one_bit_material_identity_drift(
    section, field, value
) -> None:
    prepare = measurement("prepare")
    prepare_result = validate_prepare(prepare)
    publish = measurement("publish", 10)
    publish[section][field] = value
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="continuity"):
        POLICY.validate_live_gate_policy_v2(
            publish,
            expectations(),
            expected_phase="publish",
            now_wall_time_utc=iso(15),
            now_monotonic_ns=MONO + 15_000_000_000,
            prepare_measurement=prepare,
            prepare_result=prepare_result,
        )


def test_contract_and_predecessor_hashes_are_exact() -> None:
    assert POLICY.CONTRACT_SHA256 == (
        "beea267ec9685fa59d4b5bcadd02ed1f238b626703dde56974971d779fdcd82d"
    )
    assert POLICY.PREDECESSOR_REJECTION_SHA256 == (
        "8cc0ea76a7ac0181f54617c5c7e6d82af4aff970aeb0ef9babb8f1a0467380cd"
    )
