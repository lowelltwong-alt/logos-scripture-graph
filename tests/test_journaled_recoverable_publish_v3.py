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
    / "journaled_recoverable_publish_v3.py"
)
SPEC = importlib.util.spec_from_file_location("journaled_publish_v3", MODULE_PATH)
assert SPEC and SPEC.loader
TX = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TX
SPEC.loader.exec_module(TX)


def make_case(tmp_path: Path, count: int = 3):
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
    receipt = TX.canonical_json_bytes(
        {
            "schema_version": "test-receipt.v1",
            "completion_state": "not_completed",
        }
    )
    return {
        "targets": targets,
        "allowed": allowed,
        "journal": tmp_path / "attempt" / "journal.json",
        "lock": tmp_path / "attempt" / "lock",
        "receipt_path": tmp_path / "attempt" / "receipt.json",
        "receipt": receipt,
    }


def run_case(case, injector=None, invariant=None):
    return TX.publish(
        application_id="test-one-shot",
        targets=case["targets"],
        journal_path=case["journal"],
        lock_path=case["lock"],
        receipt_path=case["receipt_path"],
        receipt_bytes=case["receipt"],
        allowed_canonical_paths=case["allowed"],
        invariant_check=invariant or (lambda _phase: None),
        failure_injector=injector,
    )


def assert_preimages(case):
    for target in case["targets"]:
        assert TX.sha256_file(target.canonical) == target.preimage_sha256


def assert_staged(case):
    for target in case["targets"]:
        assert TX.sha256_file(target.canonical) == target.staged_sha256


def test_success_and_completed_replay_are_idempotent(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    assert run_case(case)["status"] == "published"
    assert_staged(case)
    receipt_hash = TX.sha256_file(case["receipt_path"])
    journal_hash = TX.sha256_file(case["journal"])

    replay = run_case(case)
    assert replay["status"] == "idempotent_noop"
    assert replay["canonical_write_count"] == 0
    assert TX.sha256_file(case["receipt_path"]) == receipt_hash
    assert TX.sha256_file(case["journal"]) == journal_hash


@pytest.mark.parametrize("failure_after", [1, 2, 3])
def test_failure_after_each_replace_rolls_back(
    tmp_path: Path,
    failure_after: int,
) -> None:
    case = make_case(tmp_path)

    def inject(point, index):
        if point == "after_replace" and index == failure_after:
            raise RuntimeError(f"crash after {index}")

    with pytest.raises(TX.TransactionRolledBack):
        run_case(case, inject)
    assert_preimages(case)
    journal = json.loads(case["journal"].read_text(encoding="utf-8"))
    assert journal["phase"] == "rolled_back_verified"
    assert not case["lock"].exists()


@pytest.mark.parametrize("failure_after", range(1, 14))
def test_thirteen_target_failure_matrix_rolls_back(
    tmp_path: Path,
    failure_after: int,
) -> None:
    case = make_case(tmp_path, count=13)

    def inject(point, index):
        if point == "after_replace" and index == failure_after:
            raise RuntimeError(f"crash after {index}")

    with pytest.raises(TX.TransactionRolledBack):
        run_case(case, inject)
    assert_preimages(case)


def test_failure_after_last_replace_before_readback_rolls_back(
    tmp_path: Path,
) -> None:
    case = make_case(tmp_path, count=13)

    def inject(point, _index):
        if point == "after_last_replace_before_readback":
            raise RuntimeError("crash before full readback")

    with pytest.raises(TX.TransactionRolledBack):
        run_case(case, inject)
    assert_preimages(case)


def test_failure_before_first_replace_has_zero_changes(tmp_path: Path) -> None:
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "before_replace":
            raise RuntimeError("before replacement one")

    with pytest.raises(RuntimeError, match="before replacement one"):
        run_case(case, inject)
    assert_preimages(case)
    assert not case["lock"].exists()


def test_immediate_pre_replace_invariant_failure_rolls_back(
    tmp_path: Path,
) -> None:
    case = make_case(tmp_path, count=6)

    def invariant(phase: str) -> None:
        if phase == "before_replace_5":
            raise RuntimeError("path or sentinel changed before replace 5")

    with pytest.raises(
        TX.TransactionRolledBack,
        match="path or sentinel changed before replace 5",
    ):
        run_case(case, invariant=invariant)
    assert_preimages(case)


def test_immediate_pre_rollback_invariant_failure_requires_recovery(
    tmp_path: Path,
) -> None:
    case = make_case(tmp_path, count=4)

    def inject(point: str, index: int | None) -> None:
        if point == "after_replace" and index == 4:
            raise RuntimeError("force rollback")

    def invariant(phase: str) -> None:
        if phase == "before_rollback_replace_2":
            raise RuntimeError("path changed before rollback replace 2")

    with pytest.raises(TX.RecoveryRequired):
        run_case(case, injector=inject, invariant=invariant)
    journal = json.loads(case["journal"].read_text(encoding="utf-8"))
    assert journal["phase"] == "recovery_required"
    assert case["lock"].is_file()

def test_rollback_failure_retains_lock_and_recovery_required(
    tmp_path: Path,
) -> None:
    case = make_case(tmp_path)

    def inject(point, index):
        if point == "after_replace" and index == 2:
            raise RuntimeError("publish crash")
        if point == "before_rollback_replace" and index == 1:
            raise RuntimeError("rollback crash")

    with pytest.raises(TX.RecoveryRequired):
        run_case(case, inject)
    journal = json.loads(case["journal"].read_text(encoding="utf-8"))
    assert journal["phase"] == "recovery_required"
    assert case["lock"].exists()


@pytest.mark.parametrize(
    "point",
    [
        "immediately_before_receipt_write",
        "after_receipt_write",
        "after_receipt_readback_before_receipt_written_verified",
        "after_receipt_written_verified_before_completed",
    ],
)
def test_receipt_crash_replays_without_canonical_writes(
    tmp_path: Path,
    point: str,
) -> None:
    case = make_case(tmp_path)
    fired = False

    def inject(actual, _index):
        nonlocal fired
        if actual == point and not fired:
            fired = True
            raise KeyboardInterrupt(point)

    with pytest.raises(KeyboardInterrupt):
        run_case(case, inject)
    assert_staged(case)

    replay = run_case(case)
    assert replay["status"] == "receipt_recovered"
    assert replay["canonical_write_count"] == 0
    assert_staged(case)
    journal = json.loads(case["journal"].read_text(encoding="utf-8"))
    assert journal["phase"] == "completed"


def test_receipt_exception_preserves_pending_for_replay(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    fired = False

    def inject(point, _index):
        nonlocal fired
        if point == "immediately_before_receipt_write" and not fired:
            fired = True
            raise OSError("receipt filesystem unavailable")

    with pytest.raises(OSError, match="receipt filesystem unavailable"):
        run_case(case, inject)
    assert_staged(case)
    assert case["lock"].exists()
    journal = json.loads(case["journal"].read_text(encoding="utf-8"))
    assert journal["phase"] == "published_verified_receipt_pending"

    replay = run_case(case)
    assert replay["status"] == "receipt_recovered"
    assert replay["canonical_write_count"] == 0
    assert_staged(case)


def test_wrong_allowlist_fails_before_write(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    case["allowed"].remove(case["targets"][0].canonical)
    with pytest.raises(TX.TransactionError, match="exact allowlist"):
        run_case(case)
    assert_preimages(case)


def test_stale_archive_fails_before_write(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    case["targets"][1].archive.write_text("tampered\n", encoding="utf-8")
    with pytest.raises(TX.TransactionError, match="archive hash mismatch"):
        run_case(case)
    assert_preimages(case)


def test_second_publisher_is_rejected_by_existing_lock(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    case["lock"].parent.mkdir(parents=True, exist_ok=True)
    case["lock"].write_text("another-publisher\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="lock already exists"):
        run_case(case)
    assert_preimages(case)
    assert not case["journal"].exists()

def test_journal_appearing_between_read_and_lock_is_not_overwritten(
    tmp_path: Path,
) -> None:
    case = make_case(tmp_path)
    inner_completed = False

    def inject(point, _index):
        nonlocal inner_completed
        if (
            point == "after_initial_journal_read_before_lock"
            and not inner_completed
        ):
            inner_completed = True
            assert run_case(case)["status"] == "published"

    with pytest.raises(TX.RecoveryRequired, match="journal appeared"):
        run_case(case, inject)
    journal = json.loads(case["journal"].read_text(encoding="utf-8"))
    assert journal["phase"] == "completed"
    assert_staged(case)
    assert case["receipt_path"].is_file()
    assert not case["lock"].exists()
    assert run_case(case)["status"] == "idempotent_noop"