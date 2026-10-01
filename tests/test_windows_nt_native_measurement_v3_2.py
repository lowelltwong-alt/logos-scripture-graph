from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import MappingProxyType
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
    / "windows_nt_native_measurement_v3_2.py"
)
SPEC = importlib.util.spec_from_file_location(
    "windows_nt_native_measurement_v3_2_test", MODULE
)
assert SPEC and SPEC.loader
NATIVE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NATIVE
SPEC.loader.exec_module(NATIVE)


RETAINED_FIXTURES: list[str] = []
EXACT_SENTINELS = [
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
]


def _make_fixture(*, reparse_first: bool = False):
    base = Path(r"C:\tmp")
    if not base.exists():
        raise NATIVE.CoverageUnavailable("C:\\tmp unavailable")
    root = base / f"t550-v3-2-native-{uuid.uuid4().hex}"
    root.mkdir(exist_ok=False)
    RETAINED_FIXTURES.append(os.fspath(root))
    model = root / "workspace" / "model"
    for path in (
        model / "book_chunks",
        model / "reviews",
        model / "receipts",
    ):
        path.mkdir(parents=True, exist_ok=True)
    targets = [
        "book_chunks/target-01.jsonl",
        *[f"reviews/target-{index:02d}.json" for index in range(2, 13)],
        "receipts/target-13.json",
    ]
    for index, token in enumerate((*targets, *EXACT_SENTINELS), 1):
        path = model / token
        if reparse_first and index == 1:
            source = root / "reparse-source.txt"
            source.write_bytes(b"safe-disposable-source\n")
            try:
                os.symlink(source, path)
            except OSError as exc:
                return root, model, targets, list(EXACT_SENTINELS), exc
        else:
            path.write_bytes(f"fixed-v32-{index}\n".encode())
    return root, model, targets, list(EXACT_SENTINELS), None


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
            path.relative_to(root).as_posix(): path.read_bytes() for path in files
        },
        "members": {
            path.relative_to(root).as_posix(): tuple(
                sorted(child.name for child in path.iterdir())
            )
            for path in directories
        },
    }


def test_exact_three_model_root_sentinels_and_sealed_public_lease():
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    before = _snapshot(root)
    lease = None
    try:
        record, lease = _collect(root, targets, sentinels)
        assert record["schema_version"] == NATIVE.SCHEMA_VERSION
        assert [row["token"] for row in record["sentinels"]] == EXACT_SENTINELS
        assert {row["parent_token"] for row in record["sentinels"]} == {"."}
        model_identity = record["retained_directories"]["model"]
        assert all(
            row["parent_identity"] == model_identity
            for row in record["sentinels"]
        )
        assert record["lease"]["issued_resource_count"] == 16
        assert record["lease"]["resource_map_immutable_before_return"] is True
        assert record["lease"][
            "caller_retention_or_registration_surface_present"
        ] is False
        assert record["provenance"]["production_eligible"] is False
        for forbidden in ("retain", "handle", "register_resource", "issue"):
            assert not hasattr(lease, forbidden)
        body = dict(record)
        digest = body.pop("raw_measurement_sha256")
        assert digest == NATIVE.digest_value(body)
        with pytest.raises(TypeError):
            json.dumps(lease)
    finally:
        if lease is not None:
            lease.close()
    assert _snapshot(root) == before
    assert root.exists()


def test_issued_selectors_probe_only_the_bound_resources():
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    lease = None
    try:
        _, lease = _collect(root, targets, sentinels)
        for kind, ordinal in (("target", 1), ("sentinel", 1)):
            selector = lease.contention_token(kind=kind, ordinal=ordinal)
            assert lease.probe_contention(
                selector, intent="write"
            )["result"] == "PASS_SHARING_DENIED"
            assert lease.probe_contention(
                selector, intent="delete"
            )["result"] == "PASS_SHARING_DENIED"
        with pytest.raises(NATIVE.NativeV32Error, match="does not exist"):
            lease.contention_token(kind="target", ordinal=14)
    finally:
        if lease is not None:
            lease.close()
    assert root.exists()


def test_unknown_selector_makes_zero_native_probe_calls():
    class FakeApi:
        def __init__(self):
            self.probe_calls = 0

        def _probe_contention(self, parent_handle, leaf, *, intent):
            self.probe_calls += 1
            raise AssertionError("native probe must not run")

        def close(self, handle):
            pass

    api = FakeApi()
    state = NATIVE._LeaseState(
        api=api,
        handles={},
        resources=MappingProxyType({}),
        ordinal_tokens=MappingProxyType({}),
        nonce=b"x" * 32,
    )
    lease = NATIVE.NativeHandleLeaseV32(state)
    with pytest.raises(NATIVE.NativeV32Error, match="unknown issued"):
        lease.probe_contention("not-issued", intent="write")
    assert api.probe_calls == 0
    lease.close()


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        (["single-target.json"], "one-component target"),
        (["../escape.json"], "ambiguous token"),
        (["./escape.json"], "ambiguous token"),
        (["dir/../escape.json"], "ambiguous token"),
    ],
)
def test_one_component_targets_and_escapes_reject_before_file_open(
    replacement, message
):
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    changed = list(targets)
    changed[0] = replacement[0]
    with pytest.raises(NATIVE.NativeV32Error, match=message):
        _collect(root, changed, sentinels)
    assert root.exists()


@pytest.mark.parametrize(
    "sentinel",
    [
        "nested/not-root.jsonl",
        "../escape.jsonl",
        "./dot.jsonl",
        "dir/../escape.jsonl",
    ],
)
def test_nonexact_root_sentinel_shapes_reject(sentinel):
    root, _, targets, sentinels, error = _make_fixture()
    assert error is None
    changed = list(sentinels)
    changed[0] = sentinel
    with pytest.raises(NATIVE.NativeV32Error):
        _collect(root, targets, changed)
    assert root.exists()


def test_hardlink_rejected_and_fixture_retained():
    root, model, targets, sentinels, error = _make_fixture()
    assert error is None
    os.link(model / targets[0], model / "unapproved-hardlink.jsonl")
    with pytest.raises(NATIVE.NativeV32Error, match="link count one"):
        _collect(root, targets, sentinels)
    assert root.exists()


def test_reparse_rejected_or_explicitly_unavailable():
    root, _, targets, sentinels, error = _make_fixture(reparse_first=True)
    if error is not None:
        assert root.exists()
        pytest.skip(f"symlink creation unavailable: {type(error).__name__}: {error}")
    with pytest.raises(NATIVE.ReparseRejected, match="reparse point"):
        _collect(root, targets, sentinels)
    assert root.exists()


def test_production_cleanup_and_mutable_registration_surfaces_absent():
    for name in (
        "collect_production",
        "cleanup",
        "assert_safe_cleanup_target",
        "competing_open_denied",
    ):
        assert not hasattr(NATIVE, name)
    for name in ("retain", "handle", "register_resource"):
        assert not hasattr(NATIVE.NativeHandleLeaseV32, name)
    assert "shutil" not in NATIVE.__dict__
    assert "collect_test_only_temp_root" in NATIVE.__all__
