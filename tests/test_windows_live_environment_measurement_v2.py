from __future__ import annotations

from contextlib import AbstractContextManager
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "checks"
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ADAPTER = load(
    "windows_live_environment_measurement_v2_test",
    CHECKS / "windows_live_environment_measurement_v2.py",
)
V1 = load(
    "windows_live_environment_measurement_v1_for_v2_test",
    CHECKS / "windows_live_environment_measurement_v1.py",
)
POLICY = load(
    "rematerialization_live_gate_policy_v2_for_adapter_test",
    CHECKS / "rematerialization_live_gate_policy_v2.py",
)

BASE = datetime(2026, 7, 28, 14, 0, tzinfo=timezone.utc)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class FakeClock:
    def __init__(self) -> None:
        self.tick = 0

    def now_utc(self):
        value = BASE + timedelta(milliseconds=self.tick)
        self.tick += 1
        return value

    def monotonic_ns(self):
        value = 8_000_000_000_000 + self.tick * 1_000_000
        self.tick += 1
        return value


class Held(AbstractContextManager):
    def __init__(self, backend, path):
        self.backend = backend
        self.path = Path(path)

    def __enter__(self):
        self.backend.open_paths.append(self.path)
        return self

    def snapshot(self):
        return self.backend.snapshot_regular_file(self.path)

    def __exit__(self, exc_type, exc, traceback):
        return False


class FakeBackend:
    def __init__(self, workspace, model, files, processes) -> None:
        self.current_pid = 99
        self.workspace = Path(workspace)
        self.model = Path(model)
        self.files = files
        self.processes = processes
        self.open_paths = []
        self.directory_ids = {}
        for index, path in enumerate(
            {self.workspace, self.model, *(item.parent for item in files)}, 1
        ):
            self.directory_ids[Path(path)] = V1.ObjectIdentity(
                77, 1000 + index, 16, True, False
            )

    def now_utc(self):
        return BASE

    def boot_facts(self):
        return {
            "collection_method": "fake",
            "boot_time_windows_filetime_100ns": 1,
            "boot_time_utc": (BASE - timedelta(minutes=5))
            .isoformat()
            .replace("+00:00", "Z"),
            "boot_identity_sha256": sha(b"new-boot"),
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
            "volume_mount_path": "C:\\",
            "volume_guid": r"\\?\Volume{fake}\\",
            "volume_serial": 77,
            "volume_serial_hex": "0000004D",
            "filesystem_name": "NTFS",
            "filesystem_flags": 3,
            "filesystem_flags_hex": "0x00000003",
            "maximum_component_length": 255,
        }

    def assert_no_reparse_chain(self, path):
        return None

    def directory_identity(self, path):
        return self.directory_ids[Path(path)]

    def directory_members(self, path):
        path = Path(path)
        return tuple(sorted(item.name for item in self.files if item.parent == path))

    def snapshot_regular_file(self, path):
        path = Path(path)
        data = self.files[path]
        index = sorted(self.files).index(path) + 1
        return V1.FileSnapshot(
            V1.ObjectIdentity(77, index, 32, False, False),
            sha(data),
            len(data),
        )

    def hold_regular_file(self, path, mode):
        return Held(self, path)

    def list_processes(self):
        return self.processes


def expectations(tmp_path: Path):
    workspace = tmp_path / "workspace"
    model = workspace / ".ai" / "model"
    review = model / "reviews" / "Hos"
    chunks = model / "book_chunks" / "Hos"
    receipts = model / "receipts"
    global_dir = model / "global"
    for path in (review, chunks, receipts, global_dir):
        path.mkdir(parents=True, exist_ok=True)
    target_paths = [
        chunks / "chunks.jsonl",
        *[review / f"target-{n:02d}.json" for n in range(2, 13)],
        receipts / "completion.json",
    ]
    sentinel_paths = [global_dir / f"sidecar-{n}.jsonl" for n in range(1, 4)]
    files = {}
    targets = []
    for ordinal, path in enumerate(target_paths, 1):
        data = f"old-{ordinal}\n".encode()
        files[path] = data
        parent_id = {
            chunks: "parent-chunks",
            review: "parent-reviews",
            receipts: "parent-receipts",
        }[path.parent]
        targets.append(
            ADAPTER.TargetExpectation(
                ordinal=ordinal,
                target_id=f"hos-{ordinal:02d}",
                role=f"book-local-{ordinal:02d}",
                path_token=path.relative_to(model).as_posix(),
                path=path,
                parent_id=parent_id,
                preimage_sha256=sha(data),
                staged_sha256=sha(f"new-{ordinal}\n".encode()),
            )
        )
    sentinels = []
    for ordinal, path in enumerate(sentinel_paths, 1):
        data = f"global-{ordinal}\n".encode()
        files[path] = data
        sentinels.append(
            ADAPTER.SentinelExpectation(
                ordinal=ordinal,
                sentinel_id=f"global-{ordinal}",
                role=f"global-sidecar-{ordinal}",
                path_token=path.relative_to(model).as_posix(),
                path=path,
                parent_id="parent-global",
                expected_sha256=sha(data),
            )
        )
    return workspace, model, files, targets, sentinels


def collect(tmp_path: Path, *, processes=None):
    workspace, model, files, targets, sentinels = expectations(tmp_path)
    backend = FakeBackend(
        workspace,
        model,
        files,
        processes
        or [
            V1.ProcessObservation(99, "python.exe"),
            V1.ProcessObservation(100, "explorer.exe"),
        ],
    )
    before = {path: data for path, data in files.items()}
    members_before = sorted(path.as_posix() for path in tmp_path.rglob("*"))
    result = ADAPTER.collect_live_environment_measurement_v2(
        application_id="T550-HOS-V9-TEST",
        phase="prepare",
        gate_id="gate-prepare",
        workspace_root=workspace,
        workspace_path_token="workspace",
        model_root=model,
        model_path_token=".ai/model",
        targets=targets,
        sentinels=sentinels,
        backend=backend,
        clock=FakeClock(),
        parent_process_provider=lambda: {
            "pid": 42,
            "start_token": "parent-start",
            "executable_identity": sha(b"parent"),
        },
    )
    assert files == before
    assert sorted(path.as_posix() for path in tmp_path.rglob("*")) == members_before
    return result, targets, sentinels


def policy_expectations(result, targets, sentinels):
    frozen_at = (BASE - timedelta(minutes=10)).isoformat().replace(
        "+00:00", "Z"
    )
    return {
        "schema_version": POLICY.EXPECTATIONS_SCHEMA_VERSION,
        "contract_sha256": POLICY.CONTRACT_SHA256,
        "predecessor_rejection_sha256": POLICY.PREDECESSOR_REJECTION_SHA256,
        "task_id": "T550",
        "book": "Hos",
        "application_id": "T550-HOS-V9-TEST",
        "freeze": {
            "freeze_id": "freeze-v9",
            "frozen_at_utc": frozen_at,
            "pre_freeze_boot_identity": sha(b"old-boot"),
            "implementation_and_test_hashes": [
                {"artifact_id": "adapter", "sha256": sha(b"adapter")},
                {"artifact_id": "policy", "sha256": sha(b"policy")},
            ],
            "evidence_hashes": [
                {"artifact_id": "boss", "sha256": sha(b"boss")},
                {"artifact_id": "checker", "sha256": sha(b"checker")},
            ],
            "targets": [
                {
                    "ordinal": row.ordinal,
                    "target_id": row.target_id,
                    "role": row.role,
                    "path_token": row.path_token,
                    "preimage_sha256": row.preimage_sha256,
                    "staged_sha256": row.staged_sha256,
                }
                for row in targets
            ],
            "sentinels": [
                {
                    "ordinal": row.ordinal,
                    "sentinel_id": row.sentinel_id,
                    "role": row.role,
                    "path_token": row.path_token,
                    "expected_sha256": row.expected_sha256,
                }
                for row in sentinels
            ],
            "bounded_process_names": list(POLICY.BOUNDED_PROCESS_NAMES),
            "bounded_process_policy_sha256": POLICY.process_policy_sha256(),
        },
        "human_authorization": {
            "reference_id": "future-user-message",
            "source_kind": "external_human_attestation",
            "source_reference": "codex-task:T550:future",
            "asserted_principal": "Lowell Wong",
            "authorization_text_sha256": sha(b"authorization"),
            "identity_assurance": (
                "external_evidence_not_cryptographic_identity_proof"
            ),
            "local_json_alone_sufficient": False,
            "observed_by_checker": True,
            "observed_by_boss": True,
            "revoked": False,
        },
        "candidate_only": True,
        "non_authorizing": True,
    }


def test_adapter_is_byte_and_directory_member_read_only(tmp_path) -> None:
    result, _, _ = collect(tmp_path)
    assert result["effects"]["probe_files_created"] is False
    assert result["effects"]["delete_or_replace_attempted"] is False
    assert result["effects"]["attempt_created"] is False
    assert len(result["targets"]) == 13
    assert len(result["sentinels"]) == 3


def test_adapter_output_passes_policy_v2_directly(tmp_path) -> None:
    result, targets, sentinels = collect(tmp_path)
    expected = policy_expectations(result, targets, sentinels)
    end_wall = result["capture"]["end_wall_time_utc"]
    end_mono = result["capture"]["end_monotonic_ns"]
    passed = POLICY.validate_live_gate_policy_v2(
        result,
        expected,
        expected_phase="prepare",
        now_wall_time_utc=end_wall,
        now_monotonic_ns=end_mono,
    )
    assert passed["verdict"] == "PASS"
    assert passed["raw_measurement_sha256"] == POLICY.digest_value(result)


def test_adapter_uses_noncaller_omittable_process_policy(tmp_path) -> None:
    result, _, _ = collect(tmp_path)
    assert result["process_policy"]["names"] == list(
        POLICY.BOUNDED_PROCESS_NAMES
    )
    assert result["process_policy"]["sha256"] == POLICY.process_policy_sha256()


def test_other_bounded_process_blocks_policy(tmp_path) -> None:
    result, targets, sentinels = collect(
        tmp_path,
        processes=[
            V1.ProcessObservation(99, "python.exe"),
            V1.ProcessObservation(123, "pwsh.exe"),
        ],
    )
    expected = policy_expectations(result, targets, sentinels)
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="writer"):
        POLICY.validate_live_gate_policy_v2(
            result,
            expected,
            expected_phase="prepare",
            now_wall_time_utc=result["capture"]["end_wall_time_utc"],
            now_monotonic_ns=result["capture"]["end_monotonic_ns"],
        )


def test_onedrive_blocks_policy(tmp_path) -> None:
    result, targets, sentinels = collect(
        tmp_path,
        processes=[
            V1.ProcessObservation(99, "python.exe"),
            V1.ProcessObservation(123, "OneDrive.exe"),
        ],
    )
    expected = policy_expectations(result, targets, sentinels)
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="OneDrive"):
        POLICY.validate_live_gate_policy_v2(
            result,
            expected,
            expected_phase="prepare",
            now_wall_time_utc=result["capture"]["end_wall_time_utc"],
            now_monotonic_ns=result["capture"]["end_monotonic_ns"],
        )


def test_role_path_or_parent_substitution_fails_policy(tmp_path) -> None:
    result, targets, sentinels = collect(tmp_path)
    expected = policy_expectations(result, targets, sentinels)
    drifted = json.loads(json.dumps(result))
    drifted["targets"][0]["parent_id"] = "parent-unknown"
    with pytest.raises(POLICY.LiveGatePolicyV2Error, match="parent"):
        POLICY.validate_live_gate_policy_v2(
            drifted,
            expected,
            expected_phase="prepare",
            now_wall_time_utc=drifted["capture"]["end_wall_time_utc"],
            now_monotonic_ns=drifted["capture"]["end_monotonic_ns"],
        )


def test_contract_hash_is_exact() -> None:
    assert ADAPTER.CONTRACT_SHA256 == POLICY.CONTRACT_SHA256
