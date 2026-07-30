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
    / "windows_handle_bound_replace_v1.py"
)


def _load_module():
    name = "t550_windows_handle_bound_replace_v1"
    spec = importlib.util.spec_from_file_location(name, MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


w = _load_module()
pytestmark = pytest.mark.skipif(
    os.name != "nt", reason="Windows handle semantics are environment-bound"
)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _temporary_members(directory: Path, target_name: str) -> list[Path]:
    local = list(directory.glob(f".{target_name}.*.tmp"))
    ancestor = list(
        directory.parent.glob(f".{directory.name}.{target_name}.*.tmp")
    )
    return local + ancestor


def test_required_relative_handle_replacement_fails_closed_on_exact_runtime(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    staged = b'{"decision":"Hos-001"}\n'

    with pytest.raises(OSError) as caught:
        w.atomic_replace_verified(
            target, staged, expected_sha256=_digest(staged)
        )

    assert caught.value.errno == 87  # ERROR_INVALID_PARAMETER
    assert target.read_bytes() == b"old\n"
    assert _temporary_members(tmp_path, target.name) == []


def test_wrong_requested_hash_fails_before_touching_target(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")

    with pytest.raises(w.HashMismatchError):
        w.atomic_replace_verified(target, b"new\n", expected_sha256="0" * 64)

    assert target.read_bytes() == b"old\n"
    assert _temporary_members(tmp_path, target.name) == []


def test_precreated_temporary_substitution_fails_closed_without_deleting_attacker(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    attacker_bytes = b"attacker-owned\n"
    substituted: list[Path] = []

    def hook(point: str, path: Path | None) -> None:
        if point == "temporary_name_chosen":
            assert path is not None
            path.write_bytes(attacker_bytes)
            substituted.append(path)

    with pytest.raises(OSError):
        w.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    assert target.read_bytes() == b"old\n"
    assert len(substituted) == 1
    assert substituted[0].read_bytes() == attacker_bytes


def test_open_temporary_cannot_be_substituted(tmp_path: Path) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    denied: list[bool] = []

    def hook(point: str, path: Path | None) -> None:
        if point == "temporary_verified":
            assert path is not None
            attacker = tmp_path / "attacker.tmp"
            attacker.write_bytes(b"attacker\n")
            try:
                os.replace(attacker, path)
            except OSError:
                denied.append(True)
            else:  # pragma: no cover - a Windows sharing regression
                denied.append(False)

    w.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    assert denied == [True]
    assert target.read_bytes() == b"new\n"


def test_guarded_old_target_rejects_write_rename_and_delete(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")
    other = tmp_path / "other.jsonl"
    other.write_bytes(b"other\n")
    results: list[bool] = []

    def must_be_denied(action) -> None:
        try:
            action()
        except OSError:
            results.append(True)
        else:  # pragma: no cover - a Windows sharing regression
            results.append(False)

    def hook(point: str, path: Path | None) -> None:
        if point == "old_target_guarded":
            must_be_denied(lambda: path.write_bytes(b"mutated\n"))
            must_be_denied(lambda: path.unlink())
            must_be_denied(lambda: os.replace(other, path))

    w.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    assert results == [True, True, True]
    assert target.read_bytes() == b"new\n"


def test_held_parent_rejects_swap_attempt(tmp_path: Path) -> None:
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

    w.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    assert denied == [True]
    assert target.read_bytes() == b"new\n"


def test_exception_after_temp_verification_cleans_temp_and_preserves_target(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.jsonl"
    target.write_bytes(b"old\n")

    def hook(point: str, path: Path | None) -> None:
        if point == "temporary_verified":
            raise RuntimeError("injected stop")

    with pytest.raises(RuntimeError, match="injected stop"):
        w.atomic_replace_verified(target, b"new\n", _test_hook=hook)

    assert target.read_bytes() == b"old\n"
    assert _temporary_members(tmp_path, target.name) == []


def test_sentinel_guard_denies_concurrent_write_rename_and_delete(
    tmp_path: Path,
) -> None:
    sentinel = tmp_path / "global-sidecar.jsonl"
    sentinel.write_bytes(b"frozen\n")
    replacement = tmp_path / "replacement.jsonl"
    replacement.write_bytes(b"replacement\n")

    with w.sentinel_file_guard({sentinel: _digest(b"frozen\n")}) as guard:
        guard.verify_unchanged()
        with pytest.raises(OSError):
            sentinel.write_bytes(b"mutated\n")
        with pytest.raises(OSError):
            sentinel.unlink()
        with pytest.raises(OSError):
            sentinel.rename(tmp_path / "renamed.jsonl")
        with pytest.raises(OSError):
            os.replace(replacement, sentinel)
        guard.verify_unchanged()

    assert sentinel.read_bytes() == b"frozen\n"
    sentinel.write_bytes(b"after-release\n")
    assert sentinel.read_bytes() == b"after-release\n"


def test_sentinel_wrong_hash_fails_and_releases_handles(
    tmp_path: Path,
) -> None:
    sentinel = tmp_path / "global-sidecar.jsonl"
    sentinel.write_bytes(b"frozen\n")

    with pytest.raises(w.HashMismatchError):
        with w.sentinel_file_guard({sentinel: "0" * 64}):
            pytest.fail("guard body must not run")

    sentinel.write_bytes(b"released\n")
    assert sentinel.read_bytes() == b"released\n"


def test_sentinel_guard_cleans_handles_when_body_raises(tmp_path: Path) -> None:
    sentinel = tmp_path / "global-sidecar.jsonl"
    sentinel.write_bytes(b"frozen\n")

    with pytest.raises(RuntimeError, match="body failed"):
        with w.sentinel_file_guard({sentinel: _digest(b"frozen\n")}):
            raise RuntimeError("body failed")

    sentinel.unlink()
    assert not sentinel.exists()


def test_destination_symlink_or_reparse_is_rejected_when_supported(
    tmp_path: Path,
) -> None:
    real = tmp_path / "real.jsonl"
    real.write_bytes(b"old\n")
    link = tmp_path / "link.jsonl"
    try:
        link.symlink_to(real)
    except OSError as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")

    with pytest.raises(w.ReparsePointError):
        w.atomic_replace_verified(link, b"new\n")

    assert real.read_bytes() == b"old\n"


def test_parent_symlink_or_reparse_is_rejected_when_supported(
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

    with pytest.raises(w.ReparsePointError):
        w.atomic_replace_verified(linked_parent / target.name, b"new\n")

    assert target.read_bytes() == b"old\n"


def test_empty_sentinel_set_is_rejected() -> None:
    with pytest.raises(ValueError):
        w.SentinelHandleGuard({})

