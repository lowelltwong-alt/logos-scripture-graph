from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
    / "rematerialization_live_gate_policy_v1.py"
)
SPEC = importlib.util.spec_from_file_location("live_gate_policy_v1", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
policy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy)

BASE_WALL = datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc)
BASE_MONO = 8_000_000_000


def _hash(number: int) -> str:
    return f"{number:064x}"


def _authorization() -> dict:
    return {
        "reference_id": "lowell-task-attestation-v9",
        "provenance": {
            "source_kind": "external_human_attestation",
            "source_reference": "codex-task:T550:user-message:example",
            "captured_by": "environment-adapter-v9",
            "capture_method": "exact-reference-and-text-digest",
        },
        "asserted_principal": "Lowell Wong",
        "authorization_text_sha256": _hash(900),
        "application_id": "T550-HOS-V9-ONE-SHOT",
        "phase_scope": ["prepare", "publish"],
        "identity_assurance": (
            "external_evidence_not_cryptographic_identity_proof"
        ),
        "revoked": False,
    }


def _identity() -> dict:
    return {
        "boot": {"boot_id": "boot-after-v9-freeze"},
        "operating_system": {
            "name": "example-os",
            "version": "1.2.3",
            "architecture": "x86_64",
        },
        "volume": {"volume_id": "volume-7", "filesystem": "example-fs"},
        "workspace": {
            "workspace_id": "workspace-root-identity",
            "root_identity": "root-handle-identity",
        },
        "model": {"model_id": "M7_sol", "runtime_id": "runtime-build-9"},
        "parent": {
            "process_id": 4242,
            "process_start_token": "parent-start-77",
            "executable_identity": "parent-image-identity",
        },
    }


def _targets() -> list[dict]:
    return [
        {
            "ordinal": ordinal,
            "target_id": f"hos-target-{ordinal:02d}",
            "path_token": f"book-local/path-{ordinal:02d}.jsonl",
            "root_identity": "frozen-book-local-root",
            "preimage_sha256": _hash(ordinal),
            "staged_sha256": _hash(100 + ordinal),
            "observed_sha256": _hash(ordinal),
            "state": "preimage",
            "regular_file": True,
            "reparse_point": False,
        }
        for ordinal in range(1, 14)
    ]


def _sentinel_state() -> list[dict]:
    return [
        {
            "ordinal": ordinal,
            "sentinel_id": f"global-sidecar-{ordinal}",
            "expected_sha256": _hash(200 + ordinal),
        }
        for ordinal in range(1, 4)
    ]


def _frozen() -> dict:
    return {
        "implementation_sha256": _hash(301),
        "test_sha256": _hash(302),
        "evidence_sha256": [
            {"evidence_id": "architecture-ruling", "sha256": _hash(303)},
            {"evidence_id": "kernel-check", "sha256": _hash(304)},
            {"evidence_id": "rooted-primitive-check", "sha256": _hash(305)},
        ],
    }


def _expectations() -> dict:
    return {
        "schema_version": policy.EXPECTATIONS_SCHEMA_VERSION,
        "frozen_artifacts": _frozen(),
        "human_authorization": _authorization(),
        "current_identity": _identity(),
        "target_snapshots": _targets(),
        "sentinel_state": _sentinel_state(),
    }


def _iso(offset_seconds: int) -> str:
    return (BASE_WALL + timedelta(seconds=offset_seconds)).isoformat()


def _record(phase: str = "prepare", offset_seconds: int = 0) -> dict:
    observed_at = offset_seconds + 2
    targets = _targets()
    sentinels = _sentinel_state()
    return {
        "schema_version": policy.SCHEMA_VERSION,
        "gate_id": f"gate-{phase}-{offset_seconds}",
        "task_id": "T550",
        "application_id": "T550-HOS-V9-ONE-SHOT",
        "phase": phase,
        "frozen_artifacts": _frozen(),
        "human_authorization": _authorization(),
        "current_identity": _identity(),
        "target_snapshots": targets,
        "bounded_process_snapshot": {
            "captured_wall_time_utc": _iso(observed_at),
            "captured_monotonic_ns": BASE_MONO
            + observed_at * 1_000_000_000,
            "snapshot_claims_exhaustive_inventory": False,
            "onedrive_fully_exited": True,
            "onedrive_process_matches": [],
            "in_scope_writer_process_matches": [],
            "observer_limitations_acknowledged": True,
        },
        "point_in_time_open_checks": [
            {
                "ordinal": row["ordinal"],
                "target_id": row["target_id"],
                "observed_sha256": row["observed_sha256"],
                "exclusive_open_succeeded": True,
                "regular_file": True,
                "reparse_point": False,
                "check_scope": "point_in_time_only",
                "captured_wall_time_utc": _iso(observed_at),
                "captured_monotonic_ns": BASE_MONO
                + observed_at * 1_000_000_000,
            }
            for row in targets
        ],
        "sentinel_checks": [
            {
                **row,
                "observed_sha256": row["expected_sha256"],
                "passed": True,
                "check_scope": "point_in_time_only",
                "captured_wall_time_utc": _iso(observed_at),
                "captured_monotonic_ns": BASE_MONO
                + observed_at * 1_000_000_000,
            }
            for row in sentinels
        ],
        "lease": {
            "phase": phase,
            "issued_wall_time_utc": _iso(offset_seconds),
            "expires_wall_time_utc": _iso(offset_seconds + 60),
            "issued_monotonic_ns": BASE_MONO
            + offset_seconds * 1_000_000_000,
            "expires_monotonic_ns": BASE_MONO
            + (offset_seconds + 60) * 1_000_000_000,
            "max_duration_seconds": 60,
        },
        "residual_race_acknowledgments": {
            "bounded_inventory_not_exhaustive": True,
            "uncooperative_or_preopened_writer_can_race": True,
            "lost_update_before_rename_possible": True,
            "overwrite_after_readback_possible": True,
            "process_crash_recovery_only": True,
            "power_loss_durability_claimed": False,
            "thirteen_file_set_atomicity_claimed": False,
            "global_sidecar_install_authorized": False,
            "candidate_only": True,
            "non_authorizing": True,
        },
        "gate_effect": "candidate_precondition_evidence_only",
        "publication_authority_claimed": False,
        "candidate_only": True,
        "non_authorizing": True,
    }


def _validate_prepare(record: dict | None = None) -> dict:
    return policy.validate_live_gate_policy(
        record or _record(),
        _expectations(),
        expected_phase="prepare",
        now_wall_time_utc=_iso(5),
        now_monotonic_ns=BASE_MONO + 5_000_000_000,
    )


def test_prepare_pass_is_explicitly_non_authorizing() -> None:
    result = _validate_prepare()
    assert result["verdict"] == "PASS"
    assert result["candidate_only"] is True
    assert result["publication_authority_claimed"] is False
    assert result["human_identity_cryptographically_verified"] is False
    assert result["bounded_process_snapshot_exhaustive"] is False
    assert result["residual_races_eliminated"] is False


def test_publish_pass_requires_prepare_identity_equality() -> None:
    prepare = _record("prepare", 0)
    publish = _record("publish", 10)
    result = policy.validate_live_gate_policy(
        publish,
        _expectations(),
        expected_phase="publish",
        now_wall_time_utc=_iso(15),
        now_monotonic_ns=BASE_MONO + 15_000_000_000,
        prepare_record=prepare,
    )
    assert result["verdict"] == "PASS"
    assert result["phase"] == "publish"


@pytest.mark.parametrize(
    "location",
    ["implementation_sha256", "test_sha256", "evidence_sha256"],
)
def test_one_bit_frozen_hash_mutation_fails(location: str) -> None:
    record = _record()
    if location == "evidence_sha256":
        old = record["frozen_artifacts"][location][0]["sha256"]
        record["frozen_artifacts"][location][0]["sha256"] = (
            ("1" if old[0] == "0" else "0") + old[1:]
        )
    else:
        old = record["frozen_artifacts"][location]
        record["frozen_artifacts"][location] = (
            ("1" if old[0] == "0" else "0") + old[1:]
        )
    with pytest.raises(policy.LiveGatePolicyError, match="drifted"):
        _validate_prepare(record)


def test_stale_wall_or_monotonic_lease_fails() -> None:
    record = _record()
    with pytest.raises(policy.LiveGatePolicyError, match="stale"):
        policy.validate_live_gate_policy(
            record,
            _expectations(),
            expected_phase="prepare",
            now_wall_time_utc=_iso(61),
            now_monotonic_ns=BASE_MONO + 61_000_000_000,
        )


def test_missing_required_field_fails_closed() -> None:
    record = _record()
    del record["current_identity"]["parent"]
    with pytest.raises(policy.LiveGatePolicyError, match="schema drift"):
        _validate_prepare(record)


@pytest.mark.parametrize(
    "field",
    ["target_snapshots", "point_in_time_open_checks"],
)
def test_wrong_target_or_open_count_fails(field: str) -> None:
    record = _record()
    record[field].pop()
    with pytest.raises(policy.LiveGatePolicyError, match="exactly 13"):
        _validate_prepare(record)


@pytest.mark.parametrize(
    "field",
    ["target_snapshots", "point_in_time_open_checks", "sentinel_checks"],
)
def test_wrong_order_fails(field: str) -> None:
    record = _record()
    record[field][0], record[field][1] = record[field][1], record[field][0]
    with pytest.raises(policy.LiveGatePolicyError, match="order"):
        _validate_prepare(record)


def test_wrong_sentinel_count_fails() -> None:
    record = _record()
    record["sentinel_checks"].pop()
    with pytest.raises(policy.LiveGatePolicyError, match="exactly 3"):
        _validate_prepare(record)


def test_false_exhaustive_inventory_claim_fails() -> None:
    record = _record()
    record["bounded_process_snapshot"][
        "snapshot_claims_exhaustive_inventory"
    ] = True
    with pytest.raises(policy.LiveGatePolicyError, match="must be False"):
        _validate_prepare(record)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("onedrive_fully_exited", False),
        ("onedrive_process_matches", [{"pid": 7}]),
        ("in_scope_writer_process_matches", [{"pid": 8}]),
    ],
)
def test_bounded_process_snapshot_must_be_clear(
    field: str, value: object
) -> None:
    record = _record()
    record["bounded_process_snapshot"][field] = value
    with pytest.raises(policy.LiveGatePolicyError):
        _validate_prepare(record)


def test_phase_drift_between_record_and_lease_fails() -> None:
    record = _record("prepare")
    record["lease"]["phase"] = "publish"
    with pytest.raises(policy.LiveGatePolicyError, match="lease.phase drift"):
        _validate_prepare(record)


def test_phase_drift_against_expected_phase_fails() -> None:
    record = _record("publish")
    with pytest.raises(policy.LiveGatePolicyError, match="record.phase drift"):
        policy.validate_live_gate_policy(
            record,
            _expectations(),
            expected_phase="prepare",
            now_wall_time_utc=_iso(5),
            now_monotonic_ns=BASE_MONO + 5_000_000_000,
        )


def test_publish_without_prepare_fails() -> None:
    publish = _record("publish", 10)
    with pytest.raises(policy.LiveGatePolicyError, match="requires prepare_record"):
        policy.validate_live_gate_policy(
            publish,
            _expectations(),
            expected_phase="publish",
            now_wall_time_utc=_iso(15),
            now_monotonic_ns=BASE_MONO + 15_000_000_000,
        )


@pytest.mark.parametrize(
    "identity_path",
    [
        ("boot", "boot_id"),
        ("operating_system", "architecture"),
        ("volume", "volume_id"),
        ("workspace", "workspace_id"),
        ("model", "model_id"),
        ("parent", "process_start_token"),
    ],
)
def test_prepare_to_publish_identity_drift_fails(
    identity_path: tuple[str, str]
) -> None:
    prepare = _record("prepare", 0)
    publish = _record("publish", 10)
    section, field = identity_path
    publish["current_identity"][section][field] += "-drift"
    expectations = _expectations()
    expectations["current_identity"] = deepcopy(publish["current_identity"])
    with pytest.raises(
        policy.LiveGatePolicyError, match="prepare-to-publish current_identity"
    ):
        policy.validate_live_gate_policy(
            publish,
            expectations,
            expected_phase="publish",
            now_wall_time_utc=_iso(15),
            now_monotonic_ns=BASE_MONO + 15_000_000_000,
            prepare_record=prepare,
        )


def test_prepare_to_publish_target_state_drift_fails() -> None:
    prepare = _record("prepare", 0)
    publish = _record("publish", 10)
    publish["target_snapshots"][0]["root_identity"] = "changed-root"
    expectations = _expectations()
    expectations["target_snapshots"] = deepcopy(publish["target_snapshots"])
    with pytest.raises(
        policy.LiveGatePolicyError, match="prepare-to-publish target_snapshots"
    ):
        policy.validate_live_gate_policy(
            publish,
            expectations,
            expected_phase="publish",
            now_wall_time_utc=_iso(15),
            now_monotonic_ns=BASE_MONO + 15_000_000_000,
            prepare_record=prepare,
        )


def test_authorization_never_claims_cryptographic_identity() -> None:
    record = _record()
    record["human_authorization"]["identity_assurance"] = (
        "cryptographically_verified_human"
    )
    with pytest.raises(
        policy.LiveGatePolicyError, match="must not claim cryptographic"
    ):
        _validate_prepare(record)


def test_residual_race_acknowledgment_cannot_be_narrowed() -> None:
    record = _record()
    record["residual_race_acknowledgments"][
        "uncooperative_or_preopened_writer_can_race"
    ] = False
    with pytest.raises(policy.LiveGatePolicyError, match="must be True"):
        _validate_prepare(record)

