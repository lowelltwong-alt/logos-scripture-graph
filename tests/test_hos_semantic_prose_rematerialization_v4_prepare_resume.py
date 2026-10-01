from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "reviews"
    / "Hos"
    / "rematerialize_semantic_prose_v4.py"
)
SPEC = importlib.util.spec_from_file_location(
    "hos_rematerialize_v4_prepare_resume",
    SCRIPT,
)
assert SPEC and SPEC.loader
REMAT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REMAT
SPEC.loader.exec_module(REMAT)


VALIDATOR_IDS = [
    "official_chunk_map",
    "corrective_review_depth",
    "literary_quality_protocol",
    "review_coverage",
    "exact_ordered_coverage",
]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_fixture_file(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def snapshot_tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): REMAT.digest(path)
        for path in sorted(
            (member for member in root.rglob("*") if member.is_file()),
            key=lambda member: member.relative_to(root).as_posix(),
        )
    }


def configure_isolated_prepare(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> dict[str, Any]:
    fixture_root = tmp_path / "fixture-root"
    model = fixture_root / "model"
    review = model / "reviews" / "Hos"
    attempt = (
        review
        / "rematerialization_attempts"
        / REMAT.APPLICATION_ID
    )
    archive = attempt / "archive"
    stage = attempt / "stage"
    model.mkdir(parents=True)
    review.mkdir(parents=True)

    monkeypatch.setattr(REMAT, "ROOT", fixture_root)
    monkeypatch.setattr(REMAT, "MODEL", model)
    monkeypatch.setattr(REMAT, "REVIEW", review)
    monkeypatch.setattr(REMAT, "ATTEMPT", attempt)
    monkeypatch.setattr(REMAT, "ARCHIVE", archive)
    monkeypatch.setattr(REMAT, "STAGE", stage)
    monkeypatch.setattr(
        REMAT,
        "PREPARE_MANIFEST",
        attempt / "prepare_manifest_v4.json",
    )
    monkeypatch.setattr(
        REMAT,
        "PREPARE_RECEIPT",
        attempt / "prepare_receipt_v4.json",
    )
    monkeypatch.setattr(
        REMAT,
        "PREPARE_JOURNAL",
        attempt / "prepare_journal_v4.json",
    )
    monkeypatch.setattr(
        REMAT,
        "EXPANDED_DIFF_MANIFEST",
        attempt / "expanded_typed_diff_manifest_v4.json",
    )
    monkeypatch.setattr(
        REMAT,
        "PREIMAGE_MANIFEST",
        attempt / "preimage_manifest_v4.json",
    )
    monkeypatch.setattr(
        REMAT,
        "ARCHIVE_MANIFEST",
        attempt / "archive_manifest_v4.json",
    )
    monkeypatch.setattr(
        REMAT,
        "STAGED_MANIFEST",
        attempt / "staged_manifest_v4.json",
    )

    fixed_paths = {
        "ROUTE": fixture_root / "pins" / "route.json",
        "LEGACY_ADAPTER": fixture_root / "pins" / "legacy.py",
        "KERNEL_PATH": fixture_root / "pins" / "kernel.py",
        "PLAN": fixture_root / "pins" / "plan.json",
        "PLAN_CHECK": fixture_root / "pins" / "plan-check.json",
        "V3_BOSS_RULING": fixture_root / "pins" / "v3-boss.json",
    }
    for index, (name, path) in enumerate(fixed_paths.items(), 1):
        write_fixture_file(path, f"{name}:{index}\n".encode())
        monkeypatch.setattr(REMAT, name, path)

    source_pin = fixture_root / "pins" / "source.xml"
    write_fixture_file(source_pin, b"<source fixture='true'/>\n")
    global_pins = {
        model / "low_confidence_register.jsonl": b'{"fixture":"low"}\n',
        model / "frontier_escalation_queue.jsonl": (
            b'{"fixture":"frontier"}\n'
        ),
        model / "atlas_candidate_feed.jsonl": b'{"fixture":"atlas"}\n',
    }
    for path, payload in global_pins.items():
        write_fixture_file(path, payload)

    expected_pins = {
        path: REMAT.digest(path)
        for path in fixed_paths.values()
    }
    source_pins = {source_pin: REMAT.digest(source_pin)}
    global_sidecar_pins = {
        path: REMAT.digest(path)
        for path in global_pins
    }
    monkeypatch.setattr(REMAT, "EXPECTED_PINS", expected_pins)
    monkeypatch.setattr(REMAT, "SOURCE_PINS", source_pins)
    monkeypatch.setattr(
        REMAT,
        "GLOBAL_SIDECAR_PINS",
        global_sidecar_pins,
    )
    protected_projection = sha256_bytes(b"fixture protected projection\n")
    monkeypatch.setattr(
        REMAT,
        "PROTECTED_ROUTE_PROJECTION_SHA256",
        protected_projection,
    )
    monkeypatch.setattr(
        REMAT,
        "protected_route_projection_sha256",
        lambda: protected_projection,
    )
    monkeypatch.setattr(
        REMAT,
        "verify_v3_failed_attempt_preserved",
        lambda: None,
    )

    preimages: dict[str, bytes] = {}
    staged: dict[str, bytes] = {}
    for index, rel in enumerate(REMAT.TARGETS, 1):
        if rel.endswith(".jsonl"):
            preimage = (
                json.dumps(
                    {"fixture": "preimage", "ordinal": index},
                    separators=(",", ":"),
                )
                + "\n"
            ).encode()
            staged_payload = (
                json.dumps(
                    {"fixture": "staged", "ordinal": index},
                    separators=(",", ":"),
                )
                + "\n"
            ).encode()
        else:
            preimage = REMAT.canonical_json_bytes(
                {"fixture": "preimage", "ordinal": index}
            )
            staged_payload = REMAT.canonical_json_bytes(
                {"fixture": "staged", "ordinal": index}
            )
        write_fixture_file(model / rel, preimage)
        preimages[rel] = preimage
        staged[rel] = staged_payload

    monkeypatch.setattr(
        REMAT,
        "EXPECTED_PREIMAGES",
        {rel: sha256_bytes(payload) for rel, payload in preimages.items()},
    )
    monkeypatch.setattr(
        REMAT,
        "EXPECTED_STAGED",
        {rel: sha256_bytes(payload) for rel, payload in staged.items()},
    )
    monkeypatch.setattr(
        REMAT,
        "build_render",
        lambda: (
            dict(staged),
            {
                "fixture": "deterministic-prepare-resume",
                "target_count": 13,
            },
        ),
    )

    def fake_expanded_manifest(
        _old_sidecar: dict[str, Any],
        _new_sidecar: dict[str, Any],
        _rendered: dict[str, bytes],
    ) -> dict[str, Any]:
        return {
            "schema_version": (
                "m7_hosea_expanded_typed_diff_manifest.v4"
            ),
            "task_id": "T550",
            "book": "Hos",
            "route_change_count": 114,
            "route_changes": [
                {"ordinal": index}
                for index in range(1, 115)
            ],
            "sidecar_change_count": 4,
            "sidecar_changes": [
                {"ordinal": index}
                for index in range(1, 5)
            ],
            "physical_projection_target_count": 13,
            "physical_projection_diffs": [
                {"ordinal": index, "path": rel}
                for index, rel in enumerate(REMAT.TARGETS, 1)
            ],
            "protected_route_projection_sha256": protected_projection,
            "zero_other_changes_required": True,
        }

    monkeypatch.setattr(
        REMAT,
        "build_expanded_diff_manifest",
        fake_expanded_manifest,
    )
    monkeypatch.setattr(
        REMAT,
        "validate_complete_staged_contract",
        lambda _stage, _sidecar: [
            {"validator_id": validator_id, "status": "PASS"}
            for validator_id in VALIDATOR_IDS
        ],
    )
    return {
        "model": model,
        "attempt": attempt,
        "preimages": preimages,
    }


def assert_canonical_preimages_unchanged(
    model: Path,
    preimages: dict[str, bytes],
) -> None:
    assert {
        rel: (model / rel).read_bytes()
        for rel in REMAT.TARGETS
    } == preimages


def assert_exact_completed_prepare_ledger(attempt: Path) -> None:
    phase_root = attempt / "prepare_phases"
    expected_members = [
        f"{ordinal:02d}_{phase}.json"
        for ordinal, phase in REMAT.PREPARE_PHASES.items()
    ]
    assert sorted(path.name for path in phase_root.iterdir()) == (
        expected_members
    )
    journal = json.loads(
        REMAT.PREPARE_JOURNAL.read_text(encoding="utf-8")
    )
    assert journal == {
        "schema_version": "m7_hosea_prepare_journal.v4",
        "application_id": REMAT.APPLICATION_ID,
        "phase_count": 6,
        "phase_ledger_sha256": journal["phase_ledger_sha256"],
        "status": "completed",
        "candidate_only": True,
        "non_authorizing": True,
    }
    assert len(journal["phase_ledger_sha256"]) == 64


@pytest.mark.parametrize("crash_after_phase", range(1, 7))
def test_prepare_v4_exact_resumes_after_each_phase_interrupt(
    crash_after_phase: int,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = configure_isolated_prepare(tmp_path, monkeypatch)
    original_record = REMAT.record_prepare_phase
    interrupted = False

    def interrupt_once(
        ordinal: int,
        phase: str,
        payload: dict[str, Any],
    ) -> None:
        nonlocal interrupted
        original_record(ordinal, phase, payload)
        if ordinal == crash_after_phase and not interrupted:
            interrupted = True
            raise KeyboardInterrupt(
                f"fixture interruption after prepare phase {ordinal}"
            )

    monkeypatch.setattr(REMAT, "record_prepare_phase", interrupt_once)
    with pytest.raises(
        KeyboardInterrupt,
        match=f"after prepare phase {crash_after_phase}",
    ):
        REMAT.prepare_v4()

    interrupted_member = (
        fixture["attempt"]
        / "prepare_phases"
        / (
            f"{crash_after_phase:02d}_"
            f"{REMAT.PREPARE_PHASES[crash_after_phase]}.json"
        )
    )
    assert interrupted_member.is_file()
    assert not REMAT.PREPARE_JOURNAL.exists()
    assert_canonical_preimages_unchanged(
        fixture["model"],
        fixture["preimages"],
    )

    resumed = REMAT.prepare_v4()
    assert resumed["status"] in {
        "prepared",
        "prepared_idempotent_noop",
    }
    assert_exact_completed_prepare_ledger(fixture["attempt"])
    assert_canonical_preimages_unchanged(
        fixture["model"],
        fixture["preimages"],
    )

    before_third_call = snapshot_tree(fixture["attempt"])
    third = REMAT.prepare_v4()
    after_third_call = snapshot_tree(fixture["attempt"])
    assert third["status"] == "prepared_idempotent_noop"
    assert before_third_call == after_third_call
    assert_exact_completed_prepare_ledger(fixture["attempt"])
    assert_canonical_preimages_unchanged(
        fixture["model"],
        fixture["preimages"],
    )


def test_prepare_v4_fails_closed_on_unexpected_phase_member(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = configure_isolated_prepare(tmp_path, monkeypatch)
    REMAT.prepare_v4()
    phase_root = fixture["attempt"] / "prepare_phases"
    (phase_root / "07_unexpected.json").write_text(
        '{"unexpected":true}\n',
        encoding="utf-8",
    )

    with pytest.raises(
        RuntimeError,
        match="prepare phase ledger member set/order drift",
    ):
        REMAT.prepare_v4()
    assert_canonical_preimages_unchanged(
        fixture["model"],
        fixture["preimages"],
    )


def test_prepare_v4_fails_closed_on_drifted_phase_member(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = configure_isolated_prepare(tmp_path, monkeypatch)
    REMAT.prepare_v4()
    phase_one = (
        fixture["attempt"]
        / "prepare_phases"
        / "01_started.json"
    )
    value = json.loads(phase_one.read_text(encoding="utf-8"))
    value["candidate_only"] = False
    phase_one.write_bytes(REMAT.canonical_json_bytes(value))

    with pytest.raises(RuntimeError, match="prepare phase record drift"):
        REMAT.prepare_v4()
    assert_canonical_preimages_unchanged(
        fixture["model"],
        fixture["preimages"],
    )
