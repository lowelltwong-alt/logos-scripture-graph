from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
MODULE = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
    / "windows_nt_native_measurement_v3_1.py"
)
SPEC = importlib.util.spec_from_file_location(
    "windows_nt_native_measurement_v3_1_test", MODULE
)
assert SPEC and SPEC.loader
NATIVE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NATIVE
SPEC.loader.exec_module(NATIVE)


RETAINED_FIXTURES: list[str] = []
REPARSE_COVERAGE = "not_run"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _make_fixture(*, reparse_first: bool = False):
    base = Path(r"C:\tmp")
    if not base.exists():
        raise NATIVE.CoverageUnavailable("C:\\tmp unavailable")
    root = base / f"t550-v3-1-native-{uuid.uuid4().hex}"
    root.mkdir(exist_ok=False)
    RETAINED_FIXTURES.append(os.fspath(root))
    model = root / "workspace" / "model"
    for path in (
        model / "book_chunks",
        model / "reviews",
        model / "receipts",
        model / "sentinels",
    ):
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
        path = model / token
        if reparse_first and index == 1:
            source = root / "reparse-source.txt"
            source.write_bytes(b"safe-disposable-source\n")
            try:
                os.symlink(source, path)
            except OSError as exc:
                return root, model, targets, sentinels, exc
        else:
            path.write_bytes(f"fixed-v31-{index}\n".encode())
    return root, model, targets, sentinels, None


def _collect(root: Path, targets, sentinels):
    return NATIVE.collect_test_only_temp_root(
        test_root=root,
        workspace_token="workspace",
        model_token="model",
        target_tokens=targets,
        sentinel_tokens=sentinels,
    )


def _snapshot(root: Path):
    files = sorted(path for path in root.rglob("*") if path.is_file())
    directories = sorted(path for path in root.rglob("*") if path.is_dir())
    return {
        "bytes": {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in files
        },
        "members": {
            path.relative_to(root).as_posix(): tuple(
                sorted(child.name for child in path.iterdir())
            )
            for path in directories
        },
    }


def _expect(error_type, action, match: str):
    try:
        action()
    except error_type as exc:
        assert match in str(exc)
        return
    raise AssertionError(f"expected {error_type.__name__}: {match}")


def test_real_read_only_measurement_and_retained_continuity():
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    before = _snapshot(root)
    lease = None
    try:
        record, lease = _collect(root, targets, sentinels)
        assert record["schema_version"] == NATIVE.SCHEMA_VERSION
        assert record["provenance"] == {
            "backend_id": NATIVE.BACKEND_ID,
            "adapter_class": "environment_bound_exception",
            "test_only": True,
            "production_eligible": False,
            "canonical_or_global_scope": False,
            "effect_authorized": False,
            "provider_injection_available": False,
            "production_collector_present": False,
            "owner_capability_present": False,
        }
        assert len(record["targets"]) == 13
        assert len(record["sentinels"]) == 3
        assert {
            "volume-root",
            "test-root",
            "workspace",
            "model",
        }.issubset(record["retained_directories"])
        assert record["capture"]["final_handle_validation_before_record_seal"]
        assert record["access_effects"][
            "arbitrary_caller_path_write_delete_api_present"
        ] is False
        assert record["content_effects"]["directory_member_delta"].startswith(
            "coverage_unavailable"
        )
        assert record["metadata_and_cloud_effects"][
            "zero_filesystem_effect_claimed"
        ] is False
        assert record["cleanup"]["helper_cleanup_authority_present"] is False
        assert record["process_evidence"]["inventory_exhaustive"] is False
        assert record["process_evidence"]["writer_exclusion_claimed"] is False
        body = dict(record)
        digest = body.pop("raw_measurement_sha256")
        assert digest == NATIVE.digest_value(body)
        try:
            json.dumps(lease)
        except TypeError:
            pass
        else:
            raise AssertionError("lease unexpectedly serializable")
    finally:
        if lease is not None:
            lease.close()
    assert _snapshot(root) == before
    assert root.exists()


def test_contention_probe_is_opaque_token_and_handle_relative_only():
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    lease = None
    token = None
    try:
        _, lease = _collect(root, targets, sentinels)
        token = lease.contention_token(kind="target", ordinal=1)
        assert lease.probe_contention(token, intent="write")["result"] == (
            "PASS_SHARING_DENIED"
        )
        assert lease.probe_contention(token, intent="delete")["result"] == (
            "PASS_SHARING_DENIED"
        )
        sentinel_token = lease.contention_token(kind="sentinel", ordinal=1)
        assert lease.probe_contention(
            sentinel_token, intent="write"
        )["result"] == "PASS_SHARING_DENIED"
        _expect(
            NATIVE.NativeV31Error,
            lambda: lease.probe_contention(
                os.fspath(root / "workspace/model/book_chunks/target-01.jsonl"),
                intent="write",
            ),
            "unknown opaque",
        )
    finally:
        if lease is not None:
            lease.close()
    assert token is not None
    _expect(
        NATIVE.NativeV31Error,
        lambda: lease.probe_contention(token, intent="write"),
        "closed",
    )
    assert root.exists()


def test_outside_root_and_escape_tokens_fail_before_native_file_open():
    _expect(
        NATIVE.UnsafeTestRoot,
        lambda: NATIVE.verify_safe_test_root(ROOT),
        "root must be one direct",
    )
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    escaped = list(targets)
    escaped[0] = "../outside-root.json"
    _expect(
        NATIVE.NativeV31Error,
        lambda: _collect(root, escaped, sentinels),
        "ambiguous token",
    )
    assert root.exists()


def test_hardlink_is_a_hard_block_and_fixture_is_retained():
    root, model, targets, sentinels, error = _make_fixture()
    assert error is None
    os.link(model / targets[0], model / "unapproved-hardlink.jsonl")
    _expect(
        NATIVE.NativeV31Error,
        lambda: _collect(root, targets, sentinels),
        "link count one",
    )
    assert root.exists()


def test_reparse_is_rejected_or_coverage_is_explicitly_unavailable():
    global REPARSE_COVERAGE
    root, _, targets, sentinels, error = _make_fixture(reparse_first=True)
    if error is not None:
        REPARSE_COVERAGE = f"coverage_unavailable:{type(error).__name__}:{error}"
        assert "PASS" not in REPARSE_COVERAGE
        assert root.exists()
        return
    _expect(
        NATIVE.ReparseRejected,
        lambda: _collect(root, targets, sentinels),
        "reparse point",
    )
    REPARSE_COVERAGE = "PASS_REPARSE_REJECTED"
    assert root.exists()


def test_native_architecture_and_effect_classes_are_honest():
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    lease = None
    try:
        record, lease = _collect(root, targets, sentinels)
        architecture = record["platform"]["architecture"]
        assert architecture["source"] == (
            "GetNativeSystemInfo_and_IsWow64Process2"
        )
        assert architecture["native_processor_architecture_code"] >= 0
        assert architecture["python_pointer_bits"] in (32, 64)
        assert record["content_effects"][
            "target_bytes_initial_final_equal"
        ] is True
        assert record["content_effects"][
            "sentinel_bytes_initial_final_equal"
        ] is True
        assert record["metadata_and_cloud_effects"]["access_time_effect"] == (
            "unmeasured_may_change"
        )
        assert record["metadata_and_cloud_effects"]["cloud_hydration_effect"] == (
            "unmeasured_may_change"
        )
    finally:
        if lease is not None:
            lease.close()
    assert root.exists()


def test_production_and_path_cleanup_surfaces_do_not_exist():
    assert not hasattr(NATIVE, "collect_production")
    assert not hasattr(NATIVE, "competing_open_denied")
    assert not hasattr(NATIVE._Api, "probe_contention")
    assert not hasattr(NATIVE, "assert_safe_cleanup_target")
    assert not hasattr(NATIVE, "cleanup")
    assert "shutil" not in NATIVE.__dict__
    assert "collect_test_only_temp_root" in NATIVE.__all__
