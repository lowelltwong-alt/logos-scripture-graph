from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from contextlib import AbstractContextManager
from datetime import datetime, timezone
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
    / "windows_live_environment_measurement_v1.py"
)
SPEC = importlib.util.spec_from_file_location(
    "windows_live_environment_measurement_v1",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
MEASURE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MEASURE
SPEC.loader.exec_module(MEASURE)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class FakeHeldFile(AbstractContextManager["FakeHeldFile"]):
    def __init__(self, backend: "FakeBackend", path: Path, mode: str):
        self.backend = backend
        self.path = path
        self.mode = mode
        self.handle = None

    def __enter__(self) -> "FakeHeldFile":
        self.handle = self.path.open("rb")
        self.backend.held_paths.append((self.path, self.mode))
        return self

    def snapshot(self):
        assert self.handle is not None
        stat = os.fstat(self.handle.fileno())
        self.handle.seek(0)
        data = self.handle.read()
        identity = self.backend.identity_from_stat(stat, is_directory=False)
        if self.path == self.backend.drift_held_identity_for:
            identity = MEASURE.ObjectIdentity(
                volume_serial=identity.volume_serial,
                file_id=identity.file_id + 1000000,
                attributes=identity.attributes,
                is_directory=False,
                is_reparse_point=False,
            )
        return MEASURE.FileSnapshot(identity, sha(data), len(data))

    def __exit__(self, exc_type, exc, traceback) -> bool:
        assert self.handle is not None
        self.handle.close()
        self.handle = None
        return False


class FakeBackend:
    def __init__(self, *, processes=()):
        self.current_pid = 4242
        self.processes = tuple(processes)
        self.held_paths: list[tuple[Path, str]] = []
        self.reparse_paths: set[Path] = set()
        self.drift_held_identity_for: Path | None = None
        self.volume_serial = 0xA1B2C3D4

    def now_utc(self):
        return datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc)

    def boot_facts(self):
        return {
            "collection_method": "fake",
            "boot_time_windows_filetime_100ns": 133000000000000000,
            "boot_time_utc": "2026-07-28T11:00:00Z",
            "boot_identity_sha256": "b" * 64,
        }

    def os_facts(self):
        return {
            "collection_method": "fake",
            "major_version": 10,
            "minor_version": 0,
            "build_number": 26100,
            "service_pack": "",
            "native_architecture": "AMD64",
            "python_architecture": "64bit",
        }

    def volume_facts(self, path):
        return {
            "collection_method": "fake",
            "volume_mount_path": "X:\\",
            "volume_guid": r"\\?\Volume{fake}\\",
            "volume_serial": self.volume_serial,
            "volume_serial_hex": f"{self.volume_serial:08X}",
            "filesystem_name": "NTFS",
            "filesystem_flags": 0x1234,
            "filesystem_flags_hex": "0x00001234",
            "maximum_component_length": 255,
        }

    def identity_from_stat(self, stat, *, is_directory):
        return MEASURE.ObjectIdentity(
            volume_serial=self.volume_serial,
            file_id=int(stat.st_ino),
            attributes=0x10 if is_directory else 0x80,
            is_directory=is_directory,
            is_reparse_point=False,
        )

    def assert_no_reparse_chain(self, path):
        absolute = Path(os.path.abspath(path))
        for candidate in (absolute, *absolute.parents):
            if candidate in self.reparse_paths or candidate.is_symlink():
                raise MEASURE.ReparsePointRejected(
                    f"fake reparse component: {candidate}"
                )

    def directory_identity(self, path):
        return self.identity_from_stat(path.stat(), is_directory=True)

    def directory_members(self, path):
        return tuple(entry.name for entry in os.scandir(path))

    def snapshot_regular_file(self, path):
        stat = path.stat()
        data = path.read_bytes()
        return MEASURE.FileSnapshot(
            self.identity_from_stat(stat, is_directory=False),
            sha(data),
            len(data),
        )

    def hold_regular_file(self, path, mode):
        return FakeHeldFile(self, path, mode)

    def list_processes(self):
        return self.processes


def make_case(tmp_path: Path, *, processes=()):
    workspace = tmp_path / "workspace"
    model = workspace / "M7_sol"
    review = model / "reviews" / "Hos"
    chunks = model / "book_chunks" / "Hos"
    receipts = model / "receipts"
    for path in (review, chunks, receipts):
        path.mkdir(parents=True, exist_ok=True)

    target_paths = [
        *(review / f"review-{index:02d}.json" for index in range(1, 12)),
        chunks / "chunks.jsonl",
        receipts / "Hos_completion_v2.json",
    ]
    sentinel_paths = [
        model / "low_confidence_register.jsonl",
        model / "frontier_escalation_queue.jsonl",
        model / "atlas_candidate_feed.jsonl",
    ]
    for index, path in enumerate((*target_paths, *sentinel_paths), 1):
        path.write_bytes(f"fixed-bytes-{index}\n".encode())

    targets = [
        MEASURE.PathExpectation(
            logical_path=path.relative_to(model).as_posix(),
            path=path,
            expected_sha256=sha(path.read_bytes()),
        )
        for path in target_paths
    ]
    sentinels = [
        MEASURE.PathExpectation(
            logical_path=path.relative_to(model).as_posix(),
            path=path,
            expected_sha256=sha(path.read_bytes()),
        )
        for path in sentinel_paths
    ]
    return {
        "workspace": workspace,
        "model": model,
        "parents": [review, chunks, receipts],
        "target_paths": target_paths,
        "sentinel_paths": sentinel_paths,
        "targets": targets,
        "sentinels": sentinels,
        "backend": FakeBackend(processes=processes),
    }


def state(case):
    files = (*case["target_paths"], *case["sentinel_paths"])
    return {
        "bytes": {path: path.read_bytes() for path in files},
        "members": {
            parent: tuple(sorted(entry.name for entry in os.scandir(parent)))
            for parent in (
                case["model"],
                *case["parents"],
            )
        },
    }


def collect(case):
    return MEASURE.collect_live_environment_measurement(
        workspace_root=case["workspace"],
        model_root=case["model"],
        targets=case["targets"],
        sentinels=case["sentinels"],
        backend=case["backend"],
    )


def test_exact_read_only_measurement_has_zero_member_and_byte_delta(tmp_path):
    case = make_case(
        tmp_path,
        processes=(
            MEASURE.ProcessObservation(4242, "python.exe"),
            MEASURE.ProcessObservation(90, "explorer.exe"),
        ),
    )
    before = state(case)

    result = collect(case)

    assert state(case) == before
    assert result["measurement_status"] == "PASS_POINT_IN_TIME_READ_ONLY"
    assert result["target_count"] == 13
    assert result["sentinel_count"] == 3
    assert result["canonical_parent_count"] == 3
    assert result["open_measurement"] == {
        "target_mode": "exclusive_read",
        "sentinel_mode": "deny_write_and_delete",
        "all_targets_held_simultaneously": True,
        "all_sentinels_held_with_targets": True,
        "point_in_time_exclusive_open_checks_passed": True,
        "exclusive_open_target_count": 13,
        "sentinel_open_count": 3,
    }
    assert result["process_snapshot"]["inventory_exhaustive"] is False
    assert (
        result["process_snapshot"]["onedrive_absent_in_bounded_snapshot"]
        is True
    )
    assert result["claims"]["canonical_parent_probe_files_created"] is False
    assert result["claims"]["file_bytes_changed"] is False
    assert result["claims"]["delete_or_replace_attempted"] is False
    assert result["claims"]["publication_attempted"] is False
    assert len(result["measurement_body_sha256"]) == 64
    assert [mode for _, mode in case["backend"].held_paths].count(
        MEASURE.TARGET_OPEN_MODE
    ) == 13
    assert [mode for _, mode in case["backend"].held_paths].count(
        MEASURE.SENTINEL_OPEN_MODE
    ) == 3


def test_onedrive_and_other_python_are_detected_without_exhaustive_claim(
    tmp_path,
):
    case = make_case(
        tmp_path,
        processes=(
            MEASURE.ProcessObservation(4242, "python.exe"),
            MEASURE.ProcessObservation(5001, "pythonw.exe"),
            MEASURE.ProcessObservation(6002, "OneDrive.exe"),
            MEASURE.ProcessObservation(7003, "unrelated.exe"),
        ),
    )

    result = collect(case)["process_snapshot"]

    assert result["inventory_exhaustive"] is False
    assert result["onedrive_absent_in_bounded_snapshot"] is False
    assert result["onedrive_process_count"] == 1
    assert result["sync_process_count"] == 1
    assert result["python_process_count"] == 2
    assert result["other_python_process_count"] == 1
    assert {(row["pid"], row["name"]) for row in result["matched_processes"]} == {
        (4242, "python.exe"),
        (5001, "pythonw.exe"),
        (6002, "OneDrive.exe"),
    }


@pytest.mark.parametrize("kind", ["target", "sentinel"])
def test_reparse_file_is_rejected_without_mutation(tmp_path, kind):
    case = make_case(tmp_path)
    path = (
        case["target_paths"][0]
        if kind == "target"
        else case["sentinel_paths"][0]
    )
    case["backend"].reparse_paths.add(path)
    before = state(case)

    with pytest.raises(MEASURE.ReparsePointRejected):
        collect(case)

    assert state(case) == before
    assert case["backend"].held_paths == []


def test_held_identity_drift_fails_closed_and_changes_nothing(tmp_path):
    case = make_case(tmp_path)
    case["backend"].drift_held_identity_for = case["target_paths"][4]
    before = state(case)

    with pytest.raises(MEASURE.IdentityMismatch, match="identity changed"):
        collect(case)

    assert state(case) == before


def test_wrong_expected_hash_fails_before_any_held_open(tmp_path):
    case = make_case(tmp_path)
    value = case["targets"][7]
    case["targets"][7] = MEASURE.PathExpectation(
        logical_path=value.logical_path,
        path=value.path,
        expected_sha256="0" * 64,
    )
    before = state(case)

    with pytest.raises(MEASURE.HashMismatch, match="preimage hash mismatch"):
        collect(case)

    assert state(case) == before
    assert case["backend"].held_paths == []


def test_exact_counts_are_mandatory_before_measurement(tmp_path):
    case = make_case(tmp_path)

    with pytest.raises(MEASURE.CountMismatch, match="target count"):
        MEASURE.collect_live_environment_measurement(
            workspace_root=case["workspace"],
            model_root=case["model"],
            targets=case["targets"][:-1],
            sentinels=case["sentinels"],
            backend=case["backend"],
        )

    assert case["backend"].held_paths == []


def test_real_backend_is_explicitly_windows_only(monkeypatch):
    monkeypatch.setattr(MEASURE.sys, "platform", "not-windows")

    with pytest.raises(MEASURE.UnsupportedPlatform):
        MEASURE.WindowsMeasurementBackend()

