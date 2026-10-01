from __future__ import annotations

import importlib.util
import json
import sys
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
    / "journaled_recoverable_publish_v4.py"
)
SPEC = importlib.util.spec_from_file_location(
    "journaled_publish_v4_recovery",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
TX = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TX
SPEC.loader.exec_module(TX)


APP_ID = "test-v4-recovery"


def make_case(tmp_path: Path, count: int = 13):
    targets = []
    allowed = set()
    for index in range(1, count + 1):
        canonical = tmp_path / "current" / f"{index}.txt"
        archive = tmp_path / "attempt" / "archive" / f"{index}.txt"
        staged = tmp_path / "attempt" / "stage" / f"{index}.txt"
        canonical.parent.mkdir(parents=True, exist_ok=True)
        archive.parent.mkdir(parents=True, exist_ok=True)
        staged.parent.mkdir(parents=True, exist_ok=True)
        old = f"old-{index}\n".encode()
        new = f"new-{index}\n".encode()
        canonical.write_bytes(old)
        archive.write_bytes(old)
        staged.write_bytes(new)
        targets.append(
            TX.Target(
                target_id=f"target-{index}",
                logical_path=f"current/{index}.txt",
                canonical=canonical,
                archive=archive,
                staged=staged,
                preimage_sha256=TX.sha256_bytes(old),
                staged_sha256=TX.sha256_bytes(new),
            )
        )
        allowed.add(canonical)
    attempt = tmp_path / "attempt"
    return {
        "targets": targets,
        "allowed": allowed,
        "journal": attempt / "journal.json",
        "lock": attempt / "lock",
        "manifest": attempt / "actual_published_manifest.json",
        "receipt": attempt / "receipt.json",
        "marker": attempt / "recovery_required.json",
    }


def publish(case, injector=None):
    return TX.publish(
        application_id=APP_ID,
        targets=case["targets"],
        journal_path=case["journal"],
        lock_path=case["lock"],
        manifest_path=case["manifest"],
        receipt_path=case["receipt"],
        recovery_marker_path=case["marker"],
        allowed_canonical_paths=case["allowed"],
        invariant_check=lambda _phase: None,
        failure_injector=injector,
    )


def recover(case, injector=None):
    return TX.recover_to_preimages(
        application_id=APP_ID,
        targets=case["targets"],
        journal_path=case["journal"],
        lock_path=case["lock"],
        manifest_path=case["manifest"],
        receipt_path=case["receipt"],
        recovery_marker_path=case["marker"],
        allowed_canonical_paths=case["allowed"],
        invariant_check=lambda _phase: None,
        failure_injector=injector,
    )


def phase(case):
    return json.loads(case["journal"].read_text("utf-8"))["phase"]


def assert_preimages(case):
    assert all(
        TX.sha256_file(target.canonical) == target.preimage_sha256
        for target in case["targets"]
    )


@pytest.mark.parametrize("stop_after", range(1, 14))
def test_baseexception_restart_requires_recovery_and_restores_all(
    tmp_path: Path,
    stop_after: int,
):
    case = make_case(tmp_path)

    def inject(point, index):
        if point == "after_replace" and index == stop_after:
            raise KeyboardInterrupt(f"stop after {index}")

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    with pytest.raises(TX.RecoveryRequired, match="rollback-only"):
        publish(case)
    assert phase(case) == "recovery_required"
    assert recover(case)["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case["lock"].exists()
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()


@pytest.mark.parametrize("stop_after", range(1, 14))
def test_baseexception_during_rollback_restarts_rollback_only(
    tmp_path: Path,
    stop_after: int,
):
    case = make_case(tmp_path)

    def stop_publish(point, index):
        if point == "after_replace" and index == 13:
            raise KeyboardInterrupt("stop published target set")

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=stop_publish)
    with pytest.raises(TX.RecoveryRequired):
        publish(case)

    def stop_rollback(point, index):
        if point == "after_rollback_replace" and index == stop_after:
            raise KeyboardInterrupt(f"stop rollback {index}")

    with pytest.raises(KeyboardInterrupt):
        recover(case, injector=stop_rollback)
    assert phase(case) == "rolling_back"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert recover(case)["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case["lock"].exists()


def test_recovery_removes_only_exact_matching_auxiliaries(tmp_path: Path):
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "after_receipt_write":
            raise KeyboardInterrupt(point)

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    manifest_hash = TX.sha256_file(case["manifest"])
    receipt_hash = TX.sha256_file(case["receipt"])
    assert recover(case)["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()
    assert len(manifest_hash) == 64
    assert len(receipt_hash) == 64


def test_recovery_never_deletes_foreign_receipt(tmp_path: Path):
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "after_receipt_write":
            raise KeyboardInterrupt(point)

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    case["receipt"].write_text("foreign-receipt\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="auxiliary cleanup"):
        recover(case)
    assert_preimages(case)
    assert case["receipt"].read_text(encoding="utf-8") == (
        "foreign-receipt\n"
    )
    assert not case["manifest"].exists()
    assert phase(case) == "recovery_required"
    assert case["lock"].exists()


def test_recovery_never_deletes_foreign_manifest(tmp_path: Path):
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "after_manifest_write":
            raise KeyboardInterrupt(point)

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    case["manifest"].write_text("foreign-manifest\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="auxiliary cleanup"):
        recover(case)
    assert_preimages(case)
    assert case["manifest"].read_text(encoding="utf-8") == (
        "foreign-manifest\n"
    )
    assert phase(case) == "recovery_required"
    assert case["lock"].exists()


def test_recovery_refuses_foreign_canonical_without_overwrite(
    tmp_path: Path,
):
    case = make_case(tmp_path)

    def inject(point, index):
        if point == "after_replace" and index == 6:
            raise KeyboardInterrupt(point)

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    foreign_target = case["targets"][2]
    foreign_target.canonical.write_text("foreign\n", encoding="utf-8")
    before = [target.canonical.read_bytes() for target in case["targets"]]
    with pytest.raises(TX.RecoveryRequired, match="canonical mismatch"):
        recover(case)
    assert [target.canonical.read_bytes() for target in case["targets"]] == before
    assert phase(case) == "recovery_required"
    assert case["lock"].exists()


def test_recovery_refuses_completed_transaction(tmp_path: Path):
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    case["lock"].write_text(APP_ID + "\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="completed"):
        recover(case)
    assert phase(case) == "recovery_required"
    assert case["lock"].exists()


def test_recovery_corrupt_journal_uses_marker_without_overwrite(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    case["journal"].parent.mkdir(parents=True, exist_ok=True)
    case["journal"].write_text("{broken", encoding="utf-8")
    case["lock"].write_text(APP_ID + "\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="cannot be read"):
        recover(case)
    assert case["journal"].read_text(encoding="utf-8") == "{broken"
    marker = json.loads(case["marker"].read_text(encoding="utf-8"))
    assert marker["reason_code"] == "recovery_corrupt_journal"
    assert case["lock"].exists()


def test_recovery_foreign_journal_uses_marker_without_overwrite(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    case["journal"].parent.mkdir(parents=True, exist_ok=True)
    case["lock"].write_text(APP_ID + "\n", encoding="utf-8")
    case["journal"].write_text(
        '{"journal_core_sha256":"foreign","phase":"publishing"}\n',
        encoding="utf-8",
    )
    before = case["journal"].read_bytes()
    with pytest.raises(TX.RecoveryRequired, match="different core"):
        recover(case)
    assert case["journal"].read_bytes() == before
    assert json.loads(case["marker"].read_text(encoding="utf-8"))[
        "reason_code"
    ] == "recovery_foreign_journal_core"
    assert case["lock"].exists()


def test_rollback_exception_marks_recovery_and_retains_lock(
    tmp_path: Path,
):
    case = make_case(tmp_path)

    def stop_publish(point, index):
        if point == "after_replace" and index == 13:
            raise KeyboardInterrupt(point)

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=stop_publish)
    with pytest.raises(TX.RecoveryRequired):
        publish(case)

    def fail_one(point, index):
        if point == "before_rollback_replace" and index == 4:
            raise RuntimeError("one rollback failure")

    with pytest.raises(TX.RecoveryRequired, match="rollback"):
        recover(case, injector=fail_one)
    assert phase(case) == "recovery_required"
    assert case["lock"].exists()
    assert recover(case)["status"] == "rolled_back_verified"
    assert_preimages(case)
