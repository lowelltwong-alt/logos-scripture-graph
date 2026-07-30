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
SPEC = importlib.util.spec_from_file_location("journaled_publish_v3_recovery", MODULE_PATH)
assert SPEC and SPEC.loader
TX = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TX
SPEC.loader.exec_module(TX)


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
    return {
        "targets": targets,
        "allowed": allowed,
        "journal": tmp_path / "attempt" / "journal.json",
        "lock": tmp_path / "attempt" / "lock",
        "receipt_path": tmp_path / "attempt" / "receipt.json",
        "receipt": TX.canonical_json_bytes({"receipt": "one"}),
    }


def publish(case, *, receipt=None, invariant=None, injector=None):
    return TX.publish(
        application_id="recovery-one-shot",
        targets=case["targets"],
        journal_path=case["journal"],
        lock_path=case["lock"],
        receipt_path=case["receipt_path"],
        receipt_bytes=case["receipt"] if receipt is None else receipt,
        allowed_canonical_paths=case["allowed"],
        invariant_check=invariant or (lambda _phase: None),
        failure_injector=injector,
    )


def recover(case, injector=None):
    return TX.recover_to_preimages(
        application_id="recovery-one-shot",
        targets=case["targets"],
        journal_path=case["journal"],
        lock_path=case["lock"],
        receipt_path=case["receipt_path"],
        allowed_canonical_paths=case["allowed"],
        invariant_check=lambda _phase: None,
        failure_injector=injector,
    )


def assert_preimages(case):
    assert all(
        TX.sha256_file(target.canonical) == target.preimage_sha256
        for target in case["targets"]
    )


@pytest.mark.parametrize("stop_after", range(1, 14))
def test_baseexception_restart_recovers_all_preimages(
    tmp_path: Path,
    stop_after: int,
) -> None:
    case = make_case(tmp_path)

    def inject(point, index):
        if point == "after_replace" and index == stop_after:
            raise KeyboardInterrupt(f"stop after {index}")

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    assert case["lock"].exists()
    with pytest.raises(TX.RecoveryRequired):
        publish(case)
    assert json.loads(case["journal"].read_text("utf-8"))["phase"] == "recovery_required"
    result = recover(case)
    assert result["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case["lock"].exists()


@pytest.mark.parametrize("stop_after", range(1, 14))
def test_baseexception_during_rollback_is_recoverable(
    tmp_path: Path,
    stop_after: int,
) -> None:
    case = make_case(tmp_path)

    def stop_publish(point, index):
        if point == "after_replace" and index == 13:
            raise KeyboardInterrupt("stop completed replacement set")

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=stop_publish)
    with pytest.raises(TX.RecoveryRequired):
        publish(case)

    def stop_rollback(point, index):
        if point == "after_rollback_replace" and index == stop_after:
            raise KeyboardInterrupt(f"stop rollback after {index}")

    with pytest.raises(KeyboardInterrupt):
        recover(case, injector=stop_rollback)
    assert case["lock"].exists()
    assert json.loads(case["journal"].read_text("utf-8"))["phase"] == "rolling_back"
    result = recover(case)
    assert result["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case["lock"].exists()

def receipt_written_case(tmp_path: Path):
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "after_receipt_written_verified_before_completed":
            raise KeyboardInterrupt("stop after receipt-written")

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    journal = json.loads(case["journal"].read_text("utf-8"))
    assert journal["phase"] == "receipt_written_verified"
    return case


def test_receipt_written_missing_receipt_fails_closed(tmp_path: Path) -> None:
    case = receipt_written_case(tmp_path)
    case["receipt_path"].unlink()
    with pytest.raises(TX.RecoveryRequired):
        publish(case)


def test_receipt_written_tampered_receipt_fails_closed(tmp_path: Path) -> None:
    case = receipt_written_case(tmp_path)
    case["receipt_path"].write_text("tampered\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired):
        publish(case)


def test_wrong_expected_receipt_identity_fails_closed(tmp_path: Path) -> None:
    case = receipt_written_case(tmp_path)
    wrong = TX.canonical_json_bytes({"receipt": "different"})
    with pytest.raises(TX.RecoveryRequired, match="receipt identity"):
        publish(case, receipt=wrong)


def test_completed_matching_lock_residue_is_cleaned(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    case["lock"].write_text("recovery-one-shot\n", encoding="utf-8")
    assert publish(case)["status"] == "idempotent_noop"
    assert not case["lock"].exists()


def test_completed_mismatching_lock_residue_fails_closed(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    case["lock"].write_text("wrong-application\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="lock residue"):
        publish(case)


def test_corrupt_journal_fails_closed(tmp_path: Path) -> None:
    case = make_case(tmp_path)
    case["journal"].parent.mkdir(parents=True, exist_ok=True)
    case["journal"].write_text("{truncated", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="cannot be read"):
        publish(case)


@pytest.mark.parametrize(
    "mutation",
    ["route", "web", "oshb", "uxlc", "wrapper", "legacy_adapter"],
)
def test_after_archive_before_publish_input_mutation_has_zero_writes(
    tmp_path: Path,
    mutation: str,
) -> None:
    case = make_case(tmp_path)

    def invariant(phase):
        if phase == "before_publish":
            raise RuntimeError(f"{mutation} changed")

    with pytest.raises(RuntimeError, match="changed"):
        publish(case, invariant=invariant)
    assert_preimages(case)


@pytest.mark.parametrize(
    "mutation",
    ["route", "web", "oshb", "uxlc", "wrapper", "legacy_adapter"],
)
def test_during_publish_input_mutation_rolls_back(
    tmp_path: Path,
    mutation: str,
) -> None:
    case = make_case(tmp_path)

    def invariant(phase):
        if phase == "after_replace_5":
            raise RuntimeError(f"{mutation} changed")

    with pytest.raises(TX.TransactionRolledBack):
        publish(case, invariant=invariant)
    assert_preimages(case)
