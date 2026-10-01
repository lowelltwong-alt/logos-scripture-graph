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
    "journaled_publish_v4",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
TX = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TX
SPEC.loader.exec_module(TX)


APP_ID = "test-v4-one-shot"


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


def publish(case, *, injector=None, invariant=None):
    return TX.publish(
        application_id=APP_ID,
        targets=case["targets"],
        journal_path=case["journal"],
        lock_path=case["lock"],
        manifest_path=case["manifest"],
        receipt_path=case["receipt"],
        recovery_marker_path=case["marker"],
        allowed_canonical_paths=case["allowed"],
        invariant_check=invariant or (lambda _phase: None),
        failure_injector=injector,
    )


def recover(case, *, injector=None, invariant=None):
    return TX.recover_to_preimages(
        application_id=APP_ID,
        targets=case["targets"],
        journal_path=case["journal"],
        lock_path=case["lock"],
        manifest_path=case["manifest"],
        receipt_path=case["receipt"],
        recovery_marker_path=case["marker"],
        allowed_canonical_paths=case["allowed"],
        invariant_check=invariant or (lambda _phase: None),
        failure_injector=injector,
    )


def journal(case):
    return json.loads(case["journal"].read_text(encoding="utf-8"))


def assert_preimages(case):
    assert all(
        TX.sha256_file(target.canonical) == target.preimage_sha256
        for target in case["targets"]
    )


def assert_staged(case):
    assert all(
        TX.sha256_file(target.canonical) == target.staged_sha256
        for target in case["targets"]
    )


def test_success_writes_manifest_then_prose_free_receipt(tmp_path: Path):
    case = make_case(tmp_path)
    result = publish(case)
    assert result["status"] == "published"
    assert_staged(case)
    manifest = json.loads(case["manifest"].read_text(encoding="utf-8"))
    receipt = json.loads(case["receipt"].read_text(encoding="utf-8"))
    assert manifest["target_count"] == 13
    assert [row["published_sha256"] for row in manifest["targets"]] == [
        target.staged_sha256 for target in case["targets"]
    ]
    assert receipt == {
        "schema_version": "published_receipt.v1",
        "application_id": APP_ID,
        "journal_core_sha256": result["journal_core_sha256"],
        "actual_published_manifest_sha256": TX.sha256_file(
            case["manifest"]
        ),
        "completion_state": "completed",
    }
    assert "reason" not in receipt
    assert journal(case)["phase"] == "completed"
    assert not case["lock"].exists()


def test_completed_replay_is_idempotent(tmp_path: Path):
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    before = {
        path: TX.sha256_file(path)
        for path in (
            case["journal"],
            case["manifest"],
            case["receipt"],
        )
    }
    result = publish(case)
    assert result["status"] == "idempotent_noop"
    assert result["canonical_write_count"] == 0
    assert before == {path: TX.sha256_file(path) for path in before}
    assert not case["lock"].exists()


@pytest.mark.parametrize(
    ("point", "phase", "manifest_exists", "receipt_exists"),
    [
        (
            "after_full_readback_before_manifest_pending",
            "publishing",
            False,
            False,
        ),
        (
            "immediately_before_manifest_write",
            "published_verified_manifest_pending",
            False,
            False,
        ),
        (
            "after_manifest_write",
            "published_verified_manifest_pending",
            True,
            False,
        ),
        (
            "after_manifest_readback_before_manifest_written_verified",
            "published_verified_manifest_pending",
            True,
            False,
        ),
        (
            "immediately_before_receipt_write",
            "manifest_written_verified_receipt_pending",
            True,
            False,
        ),
        (
            "after_receipt_write",
            "manifest_written_verified_receipt_pending",
            True,
            True,
        ),
        (
            "after_receipt_readback_before_receipt_written_verified",
            "manifest_written_verified_receipt_pending",
            True,
            True,
        ),
        (
            "after_receipt_written_verified_before_completed",
            "receipt_written_verified",
            True,
            True,
        ),
    ],
)
def test_every_postpublish_phase_requires_rollback_only_recovery(
    tmp_path: Path,
    point: str,
    phase: str,
    manifest_exists: bool,
    receipt_exists: bool,
):
    case = make_case(tmp_path)

    def inject(actual, _index):
        if actual == point:
            raise KeyboardInterrupt(point)

    with pytest.raises(KeyboardInterrupt):
        publish(case, injector=inject)
    assert journal(case)["phase"] == phase
    assert case["manifest"].exists() is manifest_exists
    assert case["receipt"].exists() is receipt_exists
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert_staged(case)

    with pytest.raises(TX.RecoveryRequired, match="rollback-only"):
        publish(case)
    assert journal(case)["phase"] == "recovery_required"
    assert recover(case)["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()
    assert not case["lock"].exists()


def test_manifest_readback_mismatch_is_durable_and_not_forwarded(
    tmp_path: Path,
):
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "after_manifest_write":
            case["manifest"].write_text("foreign\n", encoding="utf-8")

    with pytest.raises(TX.RecoveryRequired):
        publish(case, injector=inject)
    assert journal(case)["phase"] == "recovery_required"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert not case["receipt"].exists()
    with pytest.raises(TX.RecoveryRequired, match="auxiliary cleanup"):
        recover(case)
    assert_preimages(case)
    assert case["manifest"].read_text(encoding="utf-8") == "foreign\n"
    assert case["lock"].exists()


def test_receipt_readback_mismatch_is_durable_and_not_forwarded(
    tmp_path: Path,
):
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "after_receipt_write":
            case["receipt"].write_text("foreign\n", encoding="utf-8")

    with pytest.raises(TX.RecoveryRequired):
        publish(case, injector=inject)
    assert journal(case)["phase"] == "recovery_required"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    with pytest.raises(TX.RecoveryRequired, match="auxiliary cleanup"):
        recover(case)
    assert_preimages(case)
    assert not case["manifest"].exists()
    assert case["receipt"].read_text(encoding="utf-8") == "foreign\n"
    assert case["lock"].exists()


@pytest.mark.parametrize(
    "point",
    [
        "immediately_before_manifest_write",
        "immediately_before_receipt_write",
    ],
)
def test_auxiliary_write_error_marks_recovery_and_rolls_back(
    tmp_path: Path,
    point: str,
):
    case = make_case(tmp_path)

    def inject(actual, _index):
        if actual == point:
            raise OSError(f"{point} unavailable")

    with pytest.raises(TX.RecoveryRequired, match="publish_failure"):
        publish(case, injector=inject)
    assert journal(case)["phase"] == "recovery_required"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert recover(case)["status"] == "rolled_back_verified"
    assert_preimages(case)
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()


def test_full_readback_canonical_mismatch_writes_no_auxiliaries(
    tmp_path: Path,
):
    case = make_case(tmp_path)

    def inject(point, _index):
        if point == "after_last_replace_before_readback":
            case["targets"][7].canonical.write_text(
                "foreign\n",
                encoding="utf-8",
            )

    with pytest.raises(TX.RecoveryRequired, match="publish_failure"):
        publish(case, injector=inject)
    assert journal(case)["phase"] == "recovery_required"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()

def test_corrupt_journal_gets_separate_marker_and_exact_lock(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    case["journal"].parent.mkdir(parents=True, exist_ok=True)
    case["journal"].write_text("{truncated", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="cannot be read"):
        publish(case)
    assert case["journal"].read_text(encoding="utf-8") == "{truncated"
    marker = json.loads(case["marker"].read_text(encoding="utf-8"))
    assert marker["reason_code"] == "corrupt_or_unreadable_journal"
    assert marker["forward_publication_allowed"] is False
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert_preimages(case)


def test_foreign_core_gets_separate_marker_without_journal_overwrite(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    case["journal"].parent.mkdir(parents=True, exist_ok=True)
    foreign = {"journal_core_sha256": "0" * 64, "phase": "publishing"}
    case["journal"].write_text(
        json.dumps(foreign) + "\n",
        encoding="utf-8",
    )
    before = case["journal"].read_bytes()
    with pytest.raises(TX.RecoveryRequired, match="different"):
        publish(case)
    assert case["journal"].read_bytes() == before
    assert json.loads(case["marker"].read_text("utf-8"))[
        "reason_code"
    ] == "foreign_journal_core"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert_preimages(case)


def test_preflight_canonical_mismatch_is_durable_with_zero_writes(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    case["targets"][4].canonical.write_text("foreign\n", encoding="utf-8")
    before = [target.canonical.read_bytes() for target in case["targets"]]
    with pytest.raises(TX.RecoveryRequired):
        publish(case)
    assert journal(case)["phase"] == "recovery_required"
    assert [target.canonical.read_bytes() for target in case["targets"]] == before
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()


def test_invariant_mismatch_after_replacement_stops_forward_writes(
    tmp_path: Path,
):
    case = make_case(tmp_path)

    def invariant(phase):
        if phase == "after_replace_4":
            raise RuntimeError("sentinel mismatch")

    with pytest.raises(TX.RecoveryRequired):
        publish(case, invariant=invariant)
    assert journal(case)["phase"] == "recovery_required"
    assert [
        TX.sha256_file(target.canonical) == target.staged_sha256
        for target in case["targets"]
    ] == [True, True, True, True] + [False] * 9
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()


def test_two_publishers_interleaving_does_not_overwrite_journal(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    inner_completed = False

    def inject(point, _index):
        nonlocal inner_completed
        if (
            point == "after_initial_journal_read_before_lock"
            and not inner_completed
        ):
            inner_completed = True
            assert publish(case)["status"] == "published"

    result = publish(case, injector=inject)
    assert result["status"] == "idempotent_noop"
    assert journal(case)["phase"] == "completed"
    assert_staged(case)
    assert not case["lock"].exists()


def test_completed_receipt_mismatch_marks_recovery_and_retains_lock(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    case["receipt"].write_text("foreign\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="completed_replay"):
        publish(case)
    assert journal(case)["phase"] == "recovery_required"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert_staged(case)

def test_completed_manifest_mismatch_marks_recovery_and_retains_lock(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    case["manifest"].write_text("foreign\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="completed_replay"):
        publish(case)
    assert journal(case)["phase"] == "recovery_required"
    assert case["lock"].read_text(encoding="utf-8").strip() == APP_ID
    assert_staged(case)
    assert case["receipt"].exists()
