from __future__ import annotations

import hashlib
import importlib.util
import os
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
    / "windows_nt_rooted_replace_v2.py"
)
SPEC = importlib.util.spec_from_file_location(
    "windows_nt_rooted_replace_v2",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
NT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NT
SPEC.loader.exec_module(NT)


pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="the rooted replacement contract is Windows-specific",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_case(tmp_path: Path):
    root = tmp_path / "root"
    root.mkdir()
    target = root / "target.json"
    old = b'{"state":"old"}\n'
    new = b'{"state":"new"}\n'
    target.write_bytes(old)
    return {
        "root": root,
        "target": target,
        "old": old,
        "new": new,
        "root_identity": NT.inspect_root_identity(root),
        "preimage": NT.inspect_rooted_entry(root, target.name),
    }


def replace(case, **overrides):
    arguments = {
        "root": case["root"],
        "target_basename": case["target"].name,
        "intended_bytes": case["new"],
        "expected_intended_sha256": sha(case["new"]),
        "expected_root_identity": case["root_identity"],
        "expected_preimage": case["preimage"],
        "acknowledge_residual_race": True,
    }
    arguments.update(overrides)
    return NT.rooted_replace_bytes(**arguments)


def make_symlink(link: Path, target: Path, *, directory: bool = False) -> None:
    os.symlink(target, link, target_is_directory=directory)
    assert link.is_symlink()


def test_exact_root_relative_success_and_claim_limits(tmp_path: Path):
    case = make_case(tmp_path)

    result = replace(case)

    assert case["target"].read_bytes() == case["new"]
    assert result.intended_sha256 == sha(case["new"])
    assert result.root_identity == case["root_identity"]
    assert result.preimage_identity == case["preimage"].identity
    assert result.published_identity != result.preimage_identity
    assert result.old_target_changed_after_preimage_check is False
    assert "uncooperative writer" in result.residual_race_scope
    assert result.power_loss_atomicity_claimed is False
    assert result.set_atomicity_claimed is False
    assert result.uncooperative_writer_excluded is False
    assert not list(case["root"].glob("*.rooted-replace.tmp"))


def test_external_gate_is_mandatory_before_any_mutation(tmp_path: Path):
    case = make_case(tmp_path)

    with pytest.raises(NT.ExternalGateRequired):
        replace(case, acknowledge_residual_race=False)

    assert case["target"].read_bytes() == case["old"]
    assert list(case["root"].iterdir()) == [case["target"]]


def test_wrong_intended_bytes_rejected_before_temp_creation(tmp_path: Path):
    case = make_case(tmp_path)

    with pytest.raises(NT.HashMismatch):
        replace(case, expected_intended_sha256=sha(b"not-the-new-bytes"))

    assert case["target"].read_bytes() == case["old"]
    assert list(case["root"].iterdir()) == [case["target"]]


def test_wrong_parent_identity_rejected_and_private_temp_cleaned(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    wrong_identity = NT.inspect_root_identity(other)
    temp_name = ".known.rooted-replace.tmp"

    with pytest.raises(NT.IdentityMismatch):
        replace(
            case,
            expected_root_identity=wrong_identity,
            _temp_basename=temp_name,
        )

    assert case["target"].read_bytes() == case["old"]
    assert not (case["root"] / temp_name).exists()


@pytest.mark.parametrize(
    "bad_name",
    [
        "../target.json",
        "sub/target.json",
        r"sub\target.json",
        "target.json:stream",
        "target.json.",
        "target.json ",
        "CON",
    ],
)
def test_traversal_and_ambiguous_target_basenames_rejected(
    tmp_path: Path,
    bad_name: str,
):
    case = make_case(tmp_path)

    with pytest.raises(NT.RootedReplaceError):
        replace(case, target_basename=bad_name)

    assert case["target"].read_bytes() == case["old"]


@pytest.mark.parametrize(
    "bad_temp",
    ["../escape.tmp", r"sub\escape.tmp", "target.json", "NUL"],
)
def test_unsafe_or_aliasing_temp_name_rejected(
    tmp_path: Path,
    bad_temp: str,
):
    case = make_case(tmp_path)

    with pytest.raises(NT.RootedReplaceError):
        replace(case, _temp_basename=bad_temp)

    assert case["target"].read_bytes() == case["old"]


def test_wrong_preimage_hash_or_identity_rejected(tmp_path: Path):
    case = make_case(tmp_path)
    wrong = NT.EntrySnapshot(
        identity=case["preimage"].identity,
        sha256="0" * 64,
        digest_kind=case["preimage"].digest_kind,
    )
    temp_name = ".wrong-preimage.rooted-replace.tmp"

    with pytest.raises(NT.IdentityMismatch):
        replace(case, expected_preimage=wrong, _temp_basename=temp_name)

    assert case["target"].read_bytes() == case["old"]
    assert not (case["root"] / temp_name).exists()


def test_reparse_destination_root_is_rejected(tmp_path: Path):
    actual_root = tmp_path / "actual"
    actual_root.mkdir()
    linked_root = tmp_path / "linked"
    make_symlink(linked_root, actual_root, directory=True)

    with pytest.raises(NT.ReparsePointRejected):
        NT.inspect_root_identity(linked_root)


def test_existing_reparse_temp_is_never_opened_or_traversed(tmp_path: Path):
    case = make_case(tmp_path)
    victim = tmp_path / "temp-victim"
    victim.write_bytes(b"victim\n")
    temp_name = ".occupied.rooted-replace.tmp"
    make_symlink(case["root"] / temp_name, victim)

    with pytest.raises(OSError):
        replace(case, _temp_basename=temp_name)

    assert victim.read_bytes() == b"victim\n"
    assert (case["root"] / temp_name).is_symlink()
    assert case["target"].read_bytes() == case["old"]


def test_target_reparse_entry_replaced_without_traversing_victim(
    tmp_path: Path,
):
    root = tmp_path / "root"
    root.mkdir()
    victim = tmp_path / "victim.json"
    victim_bytes = b'{"victim":true}\n'
    victim.write_bytes(victim_bytes)
    target = root / "target.json"
    make_symlink(target, victim)
    expected = NT.inspect_rooted_entry(root, target.name)
    assert expected.identity.is_reparse_point
    new = b'{"published":true}\n'

    result = NT.rooted_replace_bytes(
        root=root,
        target_basename=target.name,
        intended_bytes=new,
        expected_intended_sha256=sha(new),
        expected_root_identity=NT.inspect_root_identity(root),
        expected_preimage=expected,
        acknowledge_residual_race=True,
    )

    assert victim.read_bytes() == victim_bytes
    assert not target.is_symlink()
    assert target.read_bytes() == new
    assert result.preimage_identity.is_reparse_point
    assert not result.published_identity.is_reparse_point


def test_existing_old_target_writer_can_only_lose_update_not_divert_rename(
    tmp_path: Path,
):
    case = make_case(tmp_path)
    root_handle = NT._open_root(case["root"])
    writer_handle = None
    rogue = b'{"state":"bad"}\n'
    try:
        writer_handle = NT._nt_open_relative(
            root_handle,
            case["target"].name,
            desired_access=(
                NT.GENERIC_READ
                | NT.GENERIC_WRITE
                | NT.FILE_READ_ATTRIBUTES
                | NT.SYNCHRONIZE
            ),
            share_access=(
                NT.FILE_SHARE_READ
                | NT.FILE_SHARE_WRITE
                | NT.FILE_SHARE_DELETE
            ),
            disposition=NT.FILE_OPEN,
        )

        def race(phase, access):
            if phase == "immediately_before_rename":
                NT._write_handle_exact(writer_handle, rogue)

        result = replace(case, _test_hook=race)
        old_handle_after = NT._snapshot_handle(writer_handle)
    finally:
        NT._close(writer_handle)
        NT._close(root_handle)

    assert case["target"].read_bytes() == case["new"]
    assert old_handle_after.sha256 == sha(rogue)
    assert result.old_target_changed_after_preimage_check is True
    assert "lose that update" in result.residual_race_scope


def test_post_rename_source_mutation_is_detected(tmp_path: Path):
    case = make_case(tmp_path)
    corrupted = b'{"state":"bad"}\n'

    def mutate(phase, access):
        if phase == "after_rename_before_readback":
            access.overwrite_published_source(corrupted)

    with pytest.raises(NT.PostReplaceVerificationError):
        replace(case, _test_hook=mutate)

    assert case["target"].read_bytes() == corrupted
    assert not list(case["root"].glob("*.rooted-replace.tmp"))


def test_exception_before_rename_removes_exact_private_temp(tmp_path: Path):
    case = make_case(tmp_path)
    temp_name = ".exception.rooted-replace.tmp"

    def fail(phase, access):
        if phase == "immediately_before_rename":
            raise RuntimeError("injected")

    with pytest.raises(RuntimeError, match="injected"):
        replace(case, _temp_basename=temp_name, _test_hook=fail)

    assert case["target"].read_bytes() == case["old"]
    assert not (case["root"] / temp_name).exists()


def test_three_sentinel_handles_deny_write_delete_and_rename(
    tmp_path: Path,
):
    sentinels = [tmp_path / f"sentinel-{index}" for index in range(3)]
    payloads = [f"sentinel-{index}\n".encode() for index in range(3)]
    for path, payload in zip(sentinels, payloads):
        path.write_bytes(payload)
    expected = {
        path: sha(payload) for path, payload in zip(sentinels, payloads)
    }
    replacement = tmp_path / "replacement"
    replacement.write_bytes(b"replacement\n")

    with NT.sentinel_handle_guard(sentinels, expected) as guard:
        with pytest.raises(OSError):
            sentinels[0].write_bytes(b"mutated\n")
        with pytest.raises(OSError):
            os.replace(replacement, sentinels[1])
        with pytest.raises(OSError):
            sentinels[2].unlink()
        guard.verify()

    assert [path.read_bytes() for path in sentinels] == payloads
    assert replacement.read_bytes() == b"replacement\n"
    sentinels[0].write_bytes(b"after-close\n")
    assert sentinels[0].read_bytes() == b"after-close\n"


def test_sentinel_entry_failure_closes_already_opened_handles(tmp_path: Path):
    sentinels = [tmp_path / f"sentinel-{index}" for index in range(3)]
    for path in sentinels:
        path.write_bytes(b"same\n")
    expected = {path: sha(b"same\n") for path in sentinels}
    expected[sentinels[1]] = "f" * 64

    with pytest.raises(NT.HashMismatch):
        with NT.sentinel_handle_guard(sentinels, expected):
            raise AssertionError("not reached")

    for path in sentinels:
        path.write_bytes(b"writable-after-failure\n")


def test_sentinel_body_exception_still_verifies_and_closes(tmp_path: Path):
    sentinels = [tmp_path / f"sentinel-{index}" for index in range(3)]
    for path in sentinels:
        path.write_bytes(b"same\n")

    with pytest.raises(RuntimeError, match="body failure"):
        with NT.sentinel_handle_guard(sentinels):
            raise RuntimeError("body failure")

    for path in sentinels:
        path.unlink()

