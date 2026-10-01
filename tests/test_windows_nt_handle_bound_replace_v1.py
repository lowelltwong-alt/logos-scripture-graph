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
    / "windows_nt_handle_bound_replace_v1.py"
)


def _load_module():
    name = "t550_windows_nt_handle_bound_replace_v1"
    spec = importlib.util.spec_from_file_location(name, MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


n = _load_module()
pytestmark = pytest.mark.skipif(
    os.name != "nt", reason="NT handle semantics require the exact Windows runtime"
)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _temporary_members(target: Path) -> list[Path]:
    return list(
        target.parent.parent.glob(
            f".{target.parent.name}.{target.name}.*.nttmp"
        )
    )


def _assert_exact_runtime_nonviable(caught: pytest.ExceptionInfo) -> None:
    error = caught.value
    assert isinstance(error, n.NtSetInformationFileError)
    assert error.ntstatus == 0xC0000043  # STATUS_SHARING_VIOLATION
    assert error.winerror == 32  # ERROR_SHARING_VIOLATION


def test_nt_relative_replace_existing_is_nonviable_on_exact_runtime(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    staged = b'{"decision":"Hos-001"}\n'

    with pytest.raises(n.NtSetInformationFileError) as caught:
        n.atomic_replace_verified(
            target, staged, expected_sha256=_digest(staged)
        )

    _assert_exact_runtime_nonviable(caught)
    assert target.read_bytes() == b"old\n"
    assert _temporary_members(target) == []


def test_wrong_requested_bytes_digest_fails_before_any_touch(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")

    with pytest.raises(n.HashMismatchError):
        n.atomic_replace_verified(
            target, b"new\n", expected_sha256=_digest(b"different\n")
        )

    assert target.read_bytes() == b"old\n"
    assert _temporary_members(target) == []


def test_held_parent_identity_blocks_parent_substitution(
    tmp_path: Path,
) -> None:
    protected = tmp_path / "protected"
    protected.mkdir()
    target = protected / "target.jsonl"
    target.write_bytes(b"old\n")
    moved = tmp_path / "moved"
    denied: list[bool] = []

    def hook(point: str, path: Path | None) -> None:
        if point == "directory_chain_held":
            try:
                protected.rename(moved)
            except OSError:
                denied.append(True)
            else:  # pragma: no cover - a Windows sharing regression
                denied.append(False)

    with pytest.raises(n.NtSetInformationFileError) as caught:
        n.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    _assert_exact_runtime_nonviable(caught)
    assert denied == [True]
    assert protected.is_dir()
    assert target.read_bytes() == b"old\n"
    assert _temporary_members(target) == []


def test_precreated_temp_substitution_fails_without_deleting_attacker(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    attacker = b"attacker-owned\n"
    substituted: list[Path] = []

    def hook(point: str, path: Path | None) -> None:
        if point == "temporary_name_chosen":
            assert path is not None
            path.write_bytes(attacker)
            substituted.append(path)

    with pytest.raises(OSError):
        n.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    assert target.read_bytes() == b"old\n"
    assert len(substituted) == 1
    assert substituted[0].read_bytes() == attacker
    substituted[0].unlink()


def test_open_temp_blocks_write_delete_and_name_substitution(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    denied: list[bool] = []

    def must_be_denied(action) -> None:
        try:
            action()
        except OSError:
            denied.append(True)
        else:  # pragma: no cover - a Windows sharing regression
            denied.append(False)

    def hook(point: str, path: Path | None) -> None:
        if point == "temporary_verified":
            assert path is not None
            replacement = target.parent.parent / "attacker-temp.nttmp"
            replacement.write_bytes(b"attacker\n")
            must_be_denied(lambda: path.write_bytes(b"mutated\n"))
            must_be_denied(lambda: path.unlink())
            must_be_denied(lambda: os.replace(replacement, path))
            replacement.unlink(missing_ok=True)

    with pytest.raises(n.NtSetInformationFileError) as caught:
        n.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    _assert_exact_runtime_nonviable(caught)
    assert denied == [True, True, True]
    assert target.read_bytes() == b"old\n"
    assert _temporary_members(target) == []


def test_existing_target_guard_blocks_concurrent_mutation_through_rename(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    denied: list[bool] = []

    def must_be_denied(action) -> None:
        try:
            action()
        except OSError:
            denied.append(True)
        else:  # pragma: no cover - a Windows sharing regression
            denied.append(False)

    def hook(point: str, path: Path | None) -> None:
        if point in {"target_guarded", "before_nt_rename"}:
            assert path == target
            replacement = tmp_path / f"replacement-{point}.jsonl"
            replacement.write_bytes(b"attacker\n")
            must_be_denied(lambda: target.write_bytes(b"mutated\n"))
            must_be_denied(lambda: target.unlink())
            must_be_denied(lambda: os.replace(replacement, target))
            replacement.unlink(missing_ok=True)

    with pytest.raises(n.NtSetInformationFileError) as caught:
        n.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    _assert_exact_runtime_nonviable(caught)
    assert denied == [True, True, True, True, True, True]
    assert target.read_bytes() == b"old\n"
    assert _temporary_members(target) == []


def test_exception_after_temp_verification_cleans_temp_and_preserves_target(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")

    def hook(point: str, path: Path | None) -> None:
        if point == "temporary_verified":
            raise RuntimeError("injected stop")

    with pytest.raises(RuntimeError, match="injected stop"):
        n.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    assert target.read_bytes() == b"old\n"
    assert _temporary_members(target) == []


def test_target_reparse_is_rejected_when_symlinks_are_available(
    tmp_path: Path,
) -> None:
    real = tmp_path / "real.jsonl"
    real.write_bytes(b"old\n")
    link = tmp_path / "link.jsonl"
    try:
        link.symlink_to(real)
    except OSError as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")

    with pytest.raises(n.ReparsePointError):
        n.atomic_replace_verified(link, b"new\n")

    assert real.read_bytes() == b"old\n"
    assert _temporary_members(link) == []


def test_parent_reparse_is_rejected_when_symlinks_are_available(
    tmp_path: Path,
) -> None:
    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    target = real_parent / "target.jsonl"
    target.write_bytes(b"old\n")
    linked_parent = tmp_path / "linked-parent"
    try:
        linked_parent.symlink_to(real_parent, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"directory symlink creation unavailable: {exc}")

    with pytest.raises(n.ReparsePointError):
        n.atomic_replace_verified(linked_parent / target.name, b"new\n")

    assert target.read_bytes() == b"old\n"
    assert _temporary_members(linked_parent / target.name) == []
