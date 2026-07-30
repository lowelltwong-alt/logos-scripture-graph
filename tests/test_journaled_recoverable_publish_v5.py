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
    / "journaled_recoverable_publish_v5.py"
)
SPEC = importlib.util.spec_from_file_location(
    "journaled_publish_v5",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
TX = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TX
SPEC.loader.exec_module(TX)


APP_ID = "test-v5-one-shot"


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


def assert_owned_lock(case):
    lock = json.loads(case["lock"].read_text(encoding="utf-8"))
    assert lock["schema_version"] == "journaled_publish_lock.v1"
    assert lock["application_id"] == APP_ID
    assert len(lock["owner_token"]) == 64
    if case["journal"].is_file():
        state = journal(case)
        assert lock["journal_core_sha256"] == state["journal_core_sha256"]
        assert lock["owner_token"] == state["lock_owner_token"]


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
    assert result["journal_core_sha256"] == TX.journal_core_sha256(
        APP_ID,
        case["targets"],
        case["manifest"],
        case["receipt"],
    )
    assert_staged(case)
    manifest = json.loads(case["manifest"].read_text(encoding="utf-8"))
    receipt = json.loads(case["receipt"].read_text(encoding="utf-8"))
    assert manifest["target_count"] == 13
    assert [row["published_sha256"] for row in manifest["targets"]] == [
        target.staged_sha256 for target in case["targets"]
    ]
    assert receipt == {
        "schema_version": "published_receipt.v2",
        "application_id": APP_ID,
        "transaction_intent_sha256": manifest[
            "transaction_intent_sha256"
        ],
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
    assert_owned_lock(case)
    assert_staged(case)

    with pytest.raises(TX.RecoveryRequired, match="marker"):
        publish(case)
    assert journal(case)["phase"] == phase
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
    assert_owned_lock(case)
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
    assert_owned_lock(case)
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
    assert_owned_lock(case)
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
    assert_owned_lock(case)
    assert not case["manifest"].exists()
    assert not case["receipt"].exists()

def test_corrupt_journal_gets_separate_marker_without_lock(
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
    assert not case["lock"].exists()
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
    with pytest.raises(TX.RecoveryRequired, match="immutable core"):
        publish(case)
    assert case["journal"].read_bytes() == before
    assert json.loads(case["marker"].read_text("utf-8"))[
        "reason_code"
    ] == "foreign_or_tampered_journal_core"
    assert not case["lock"].exists()
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
    assert_owned_lock(case)
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
    assert_owned_lock(case)
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


def test_completed_receipt_mismatch_marks_recovery_without_lock(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    case["receipt"].write_text("foreign\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="completed_replay"):
        publish(case)
    assert journal(case)["phase"] == "recovery_required"
    assert case["marker"].is_file()
    assert not case["lock"].exists()
    assert_staged(case)

def test_completed_manifest_mismatch_marks_recovery_without_lock(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    assert publish(case)["status"] == "published"
    case["manifest"].write_text("foreign\n", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired, match="completed_replay"):
        publish(case)
    assert journal(case)["phase"] == "recovery_required"
    assert case["marker"].is_file()
    assert not case["lock"].exists()
    assert_staged(case)
    assert case["receipt"].exists()


def test_second_publisher_same_app_cannot_enter_lock_no_journal_window(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    observed_lock: bytes | None = None

    def interleave(point, _index):
        nonlocal observed_lock
        if point == "after_lock_before_initial_journal":
            observed_lock = case["lock"].read_bytes()
            with pytest.raises(TX.RecoveryRequired, match="existing lock"):
                publish(case)
            assert case["lock"].read_bytes() == observed_lock
            assert not case["journal"].exists()

    with pytest.raises(TX.RecoveryRequired, match="marker"):
        publish(case, injector=interleave)
    assert observed_lock is not None
    assert case["lock"].read_bytes() == observed_lock
    assert not case["journal"].exists()
    assert case["marker"].is_file()
    assert_preimages(case)
    with pytest.raises(TX.RecoveryRequired, match="marker"):
        publish(case)
    assert case["lock"].read_bytes() == observed_lock


@pytest.mark.parametrize("failure", [OSError, KeyboardInterrupt])
def test_initial_journal_write_failure_retains_lock_and_durable_gate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: type[BaseException],
):
    case = make_case(tmp_path)
    original = TX._write_journal
    calls = 0

    def fail_initial(path, value):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise failure("initial journal unavailable")
        return original(path, value)

    monkeypatch.setattr(TX, "_write_journal", fail_initial)
    with pytest.raises(failure):
        publish(case)
    assert calls == 1
    lock_before = case["lock"].read_bytes()
    assert not case["journal"].exists()
    marker = json.loads(case["marker"].read_text(encoding="utf-8"))
    assert marker["reason_code"] == (
        f"initialization_failure:{failure.__name__}"
    )
    assert marker["forward_publication_allowed"] is False
    assert_preimages(case)
    with pytest.raises(TX.RecoveryRequired, match="marker"):
        publish(case)
    assert case["lock"].read_bytes() == lock_before
    assert not case["journal"].exists()


def test_corrupt_journal_marker_blocks_after_journal_is_removed(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    case["journal"].parent.mkdir(parents=True, exist_ok=True)
    case["journal"].write_text("{truncated", encoding="utf-8")
    with pytest.raises(TX.RecoveryRequired):
        publish(case)
    marker_before = case["marker"].read_bytes()
    case["journal"].unlink()
    with pytest.raises(TX.RecoveryRequired, match="marker"):
        publish(case)
    assert case["marker"].read_bytes() == marker_before
    assert not case["journal"].exists()
    assert not case["lock"].exists()
    assert_preimages(case)


def test_marker_blocks_completed_replay_and_tamper_cannot_bypass(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    result = publish(case)
    TX._write_recovery_marker(
        marker_path=case["marker"],
        application_id=APP_ID,
        core_sha256=result["journal_core_sha256"],
        reason_code="test_completed_gate",
        journal_path=case["journal"],
        lock_path=case["lock"],
    )
    journal_before = case["journal"].read_bytes()
    with pytest.raises(TX.RecoveryRequired, match="marker"):
        publish(case)
    assert case["journal"].read_bytes() == journal_before
    case["marker"].write_bytes(b"{tampered")
    with pytest.raises(TX.RecoveryRequired, match="marker"):
        publish(case)
    assert case["journal"].read_bytes() == journal_before
    assert_staged(case)


def test_foreign_lock_token_is_never_deleted_at_completion(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    foreign = b"foreign-owner-lock\n"

    def replace_lock(point, _index):
        if point == "after_receipt_written_verified_before_completed":
            case["lock"].write_bytes(foreign)

    with pytest.raises(TX.RecoveryRequired, match="publish_failure"):
        publish(case, injector=replace_lock)
    assert case["lock"].read_bytes() == foreign
    assert case["marker"].is_file()
    assert journal(case)["phase"] == "recovery_required"
    assert_staged(case)

def test_second_publisher_cannot_reenter_validated_active_journal(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    observed = False

    def interleave(point, _index):
        nonlocal observed
        if point == "after_initial_journal_write" and not observed:
            observed = True
            journal_before = case["journal"].read_bytes()
            lock_before = case["lock"].read_bytes()
            with pytest.raises(TX.RecoveryRequired, match="rollback-only"):
                publish(case)
            assert case["journal"].read_bytes() == journal_before
            assert case["lock"].read_bytes() == lock_before
            assert not case["marker"].exists()

    assert publish(case, injector=interleave)["status"] == "published"
    assert observed
    assert_staged(case)
    assert journal(case)["phase"] == "completed"
    assert not case["lock"].exists()
    assert not case["marker"].exists()

def test_marker_appearing_mid_publish_stops_before_next_forward_write(
    tmp_path: Path,
):
    case = make_case(tmp_path)

    def place_marker(point, index):
        if point == "after_replace" and index == 3:
            state = journal(case)
            TX._write_recovery_marker(
                marker_path=case["marker"],
                application_id=APP_ID,
                core_sha256=state["journal_core_sha256"],
                reason_code="test_mid_publish_gate",
                journal_path=case["journal"],
                lock_path=case["lock"],
            )

    with pytest.raises(TX.RecoveryRequired, match="publish_failure"):
        publish(case, injector=place_marker)
    assert [
        TX.sha256_file(target.canonical) == target.staged_sha256
        for target in case["targets"]
    ] == [True, True, True] + [False] * 10
    assert case["marker"].is_file()
    assert_owned_lock(case)
    assert journal(case)["phase"] == "recovery_required"