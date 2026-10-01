from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import uuid

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
    / "windows_nt_native_measurement_v3.py"
)
SPEC = importlib.util.spec_from_file_location(
    "windows_nt_native_measurement_v3_test", MODULE
)
assert SPEC and SPEC.loader
NATIVE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NATIVE
SPEC.loader.exec_module(NATIVE)


pytestmark = pytest.mark.skipif(
    os.name != "nt" or sys.platform != "win32",
    reason="actual Windows/NTFS test-only helper",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_safe_fixture():
    base = Path(r"C:\tmp")
    if not base.exists():
        pytest.skip("C:\\tmp is unavailable; real Windows coverage unavailable")
    root = base / f"t550-v3-native-{uuid.uuid4().hex}"
    root.mkdir(exist_ok=False)
    workspace = root / "workspace"
    model = workspace / "model"
    target_parents = [
        model / "book_chunks",
        model / "reviews",
        model / "receipts",
    ]
    sentinel_parent = model / "sentinels"
    for path in (*target_parents, sentinel_parent):
        path.mkdir(parents=True, exist_ok=True)
    targets = [
        "book_chunks/target-01.jsonl",
        *[f"reviews/target-{index:02d}.json" for index in range(2, 13)],
        "receipts/target-13.json",
    ]
    sentinels = [
        f"sentinels/global-{index}.jsonl" for index in range(1, 4)
    ]
    for index, token in enumerate((*targets, *sentinels), 1):
        (model / token).write_bytes(f"fixed-{index}\n".encode())
    return root, model, targets, sentinels


def snapshot(root: Path):
    files = sorted(path for path in root.rglob("*") if path.is_file())
    directories = sorted(path for path in root.rglob("*") if path.is_dir())
    return {
        "bytes": {path.relative_to(root).as_posix(): path.read_bytes() for path in files},
        "members": {
            path.relative_to(root).as_posix(): tuple(
                sorted(child.name for child in path.iterdir())
            )
            for path in directories
        },
    }


def cleanup(root: Path):
    exact = NATIVE.assert_safe_cleanup_target(root)
    assert exact == root.resolve(strict=True)
    shutil.rmtree(exact)


def collect_fixture(root: Path, targets, sentinels):
    return NATIVE.collect_test_only_temp_root(
        test_root=root,
        workspace_token="workspace",
        model_token="model",
        target_tokens=targets,
        sentinel_tokens=sentinels,
    )


def test_real_ntfs_measurement_is_test_only_and_zero_byte_member_delta():
    root, _, targets, sentinels = make_safe_fixture()
    before = snapshot(root)
    lease = None
    try:
        record, lease = collect_fixture(root, targets, sentinels)
        assert record["provenance"] == {
            "backend_id": NATIVE.TEST_BACKEND_ID,
            "test_only": True,
            "production_eligible": False,
            "effect_authorized": False,
            "injection_enabled": False,
            "windows_design_docket_sha256": NATIVE.WINDOWS_DESIGN_DOCKET_SHA256,
            "policy_design_docket_sha256": NATIVE.POLICY_DESIGN_DOCKET_SHA256,
            "contract_v3_sha256": NATIVE.CONTRACT_V3_SHA256,
            "boss_design_ruling_sha256": NATIVE.BOSS_DESIGN_RULING_SHA256,
            "receipt_class": "read_only_collector",
            "synthetic_transaction_receipt": False,
            "owner_capability_supplied": False,
        }
        assert record["volume"]["filesystem"] == "NTFS"
        assert len(record["targets"]) == 13
        assert len(record["sentinels"]) == 3
        assert record["process_ancestry"][0]["pid"] == os.getpid()
        body = dict(record)
        digest = body.pop("raw_measurement_sha256")
        assert digest == NATIVE.digest_value(body)
        assert record["lifecycle"] == {
            "transaction_completed_state_entered": False,
            "final_live_validation_before_record_seal": True,
            "post_completed_validation_claimed": False,
        }
        assert (
            record["review_timing"]["static_or_human_review_inside_lease"]
            is False
        )
        assert record["provenance"]["receipt_class"] == "read_only_collector"
        assert record["effects"]["synthetic_replacement_exercised"] is False
        assert all(
            row["identity"]["link_count"] == 1
            for row in (*record["targets"], *record["sentinels"])
        )
        assert all(
            row["liveness_check"].startswith("WaitForSingleObject")
            for row in record["process_ancestry"]
        )
        with pytest.raises(TypeError):
            json.dumps(lease)
    finally:
        try:
            if lease is not None:
                lease.close()
                lease = None
            assert snapshot(root) == before
        finally:
            cleanup(root)


def test_real_sentinel_handles_deny_competing_write_and_delete():
    root, model, targets, sentinels = make_safe_fixture()
    lease = None
    try:
        _, lease = collect_fixture(root, targets, sentinels)
        sentinel = model / sentinels[0]
        assert NATIVE.competing_open_denied(sentinel) is True
        assert NATIVE.competing_open_denied(sentinel, delete_access=True) is True
    finally:
        if lease is not None:
            lease.close()
        cleanup(root)


def test_real_exact_leaf_and_parent_identities_are_distinct():
    root, _, targets, sentinels = make_safe_fixture()
    lease = None
    try:
        record, lease = collect_fixture(root, targets, sentinels)
        parent_ids = {
            (
                row["identity"]["volume_serial"],
                row["identity"]["file_id"],
            )
            for row in record["canonical_parents"]
        }
        assert len(parent_ids) == len(record["canonical_parents"])
        file_ids = {
            (
                row["identity"]["volume_serial"],
                row["identity"]["file_id"],
            )
            for row in (*record["targets"], *record["sentinels"])
        }
        assert len(file_ids) == 16
        for row in (*record["targets"], *record["sentinels"]):
            assert row["token"].endswith(row["leaf"])
            assert row["identity"]["reparse_point"] is False
            assert row["identity"]["link_count"] == 1
            assert row["parent_identity"]["is_directory"] is True
    finally:
        if lease is not None:
            lease.close()
        cleanup(root)


def test_real_reparse_rejection_or_explicit_coverage_unavailable():
    root, _, _, _ = make_safe_fixture()
    try:
        result = NATIVE.exercise_reparse_rejection(root)
        assert result["status"] in {
            "PASS_REJECTED_REPARSE",
            "coverage_unavailable",
        }
        if result["status"] == "coverage_unavailable":
            assert "reason" in result
            assert "PASS" not in result["status"]
    finally:
        cleanup(root)


def test_unsafe_root_is_rejected_before_collection(tmp_path):
    with pytest.raises(NATIVE.UnsafeTestRoot):
        NATIVE.collect_test_only_temp_root(
            test_root=tmp_path,
            workspace_token="workspace",
            model_token="model",
            target_tokens=[f"a/t-{index}" for index in range(13)],
            sentinel_tokens=[f"b/s-{index}" for index in range(3)],
        )


def test_pinned_design_and_contract_hashes_are_exact():
    assert NATIVE.WINDOWS_DESIGN_DOCKET_SHA256 == (
        "a2f7944cb33161457d7f092631046c1608ed7c6be8422c04800ec9c56dc781bd"
    )
    assert NATIVE.POLICY_DESIGN_DOCKET_SHA256 == (
        "142b322c9d647da9290743d2676244008f7694e2375f45073318285ca7943a46"
    )
    assert NATIVE.CONTRACT_V3_SHA256 == (
        "28b503b96b6790d65c72685caa4d6c63ea68a6cfb4473dddb5612d0c60d71b22"
    )
    assert NATIVE.BOSS_DESIGN_RULING_SHA256 == (
        "67af1a7766947172c0197b58a161d3a6af669010d1ff9c68dac59b9b8e4fa6ee"
    )
    assert not hasattr(NATIVE, "collect_production")


def test_real_extra_hardlink_is_a_hard_block():
    root, model, targets, sentinels = make_safe_fixture()
    lease = None
    try:
        os.link(model / targets[0], model / "unapproved-hardlink.jsonl")
        with pytest.raises(
            NATIVE.NativeMeasurementV3Error,
            match="link count one",
        ):
            _, lease = collect_fixture(root, targets, sentinels)
    finally:
        if lease is not None:
            lease.close()
        cleanup(root)
