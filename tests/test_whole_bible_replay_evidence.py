from __future__ import annotations

import json
import subprocess
import shutil
import tempfile
import sys
from pathlib import Path

import pytest

from scripts import validate_whole_bible_candidate_workflow as workflow_validator
from scripts import validate_whole_bible_stage_receipts as chain_validator
from scripts import whole_bible_replay_evidence as core
from scripts import write_whole_bible_terminal_completion_receipt as terminal_writer


DIGEST = "sha256:" + "0" * 64


@pytest.fixture
def tmp_path() -> Path:
    parent = core.ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "checks" / "test_sandboxes"
    parent.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix="replay-", dir=parent))
    try:
        yield path
    finally:
        shutil.rmtree(path)


def _scope() -> dict:
    return {
        "authoring_independent_from_sibling_maps": True,
        "artifact_blindness": True,
        "role_separation": True,
        "shared_model_substrate": True,
        "runtime_model_identity_attested": False,
        "independent_model_or_provider_evidence": False,
        "counts_as_cross_model_independent_vote": False,
        "convergence_weight": "one_model_voice",
    }


def _values(stage_id: str) -> dict:
    return {
        "B00": {"sibling_map_exclusion_verified": True, "source_digests_pinned": True, "campaign_projection_algorithm": "exact_campaign_bytes_and_canonical_job_projection"},
        "B01": {"ancient_context_activation_status": "corpus_gap_recorded"},
        "B02": {"root_author_attempt_id": "author-1"},
        "B03": {"frozen_revision": "r1", "per_chunk_sha256": {"d1": DIGEST}},
        "B04": {"primary_role_ids": ["original-language", "literary"], "review_revision": "r1", "blindness_attested": True, "controller_assignment_ids": ["a1", "a2"]},
        "B05": {"frozen_revision": "r1"},
        "B06": {"provisional_written_at": "2026-07-22T10:00:00Z", "peer_premortem_first_read_at": "2026-07-22T10:01:00Z", "final_ruling_written_at": "2026-07-22T10:02:00Z", "changes_after_peer_or_premortem": []},
        "B07": {"appeal_count": 1, "unresolved_appeal_count": 1, "appeal_ids": ["a1"], "unresolved_appeal_ids": ["a1"]},
        "B08": {"revision_action": "no_change", "invalidated_review_ids": []},
        "B09": {"checked_decision_ids": ["d1"], "overall_status": "pass", "unresolved_hold_ids": [], "unresolved_appeal_ids": []},
        "B10": {"terminal_completion_receipt_path_intent": "candidate/terminal.json", "terminal_completion_receipt_written": False},
    }[stage_id]


def _receipt(stage_id: str) -> dict:
    refs = {name: f"artifact-{index}" for index, name in enumerate(sorted(core.REQUIRED_STAGE_ARTIFACTS[stage_id]))}
    return {
        "stage_id": stage_id,
        "book": "Num",
        "run_id": "run-1",
        "started_at": "2026-07-22T09:00:00Z",
        "finished_at": "2026-07-22T09:01:00Z",
        "outcome": "succeeded",
        "prior_stage_receipt_sha256": None if stage_id == "B00" else DIGEST,
        "prior_stage_receipt_path": None if stage_id == "B00" else "prior.json",
        "stage_evidence": {"artifact_refs": refs, "artifact_sha256": {name: DIGEST for name in refs}, "values": _values(stage_id)},
        "independence_scope": _scope(),
        "shared_model_substrate": True,
        "counts_as_cross_model_independent_vote": False,
    }


def _assert_code(code: str, call) -> None:
    with pytest.raises(core.ReplayEvidenceError) as exc:
        call()
    assert exc.value.code == code


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def test_qf01_rejects_plan_that_has_not_materialized(tmp_path: Path) -> None:
    campaign = {"campaign_id": "test", "revision": 6, "phases": [{"waves": [{"subwaves": [{"jobs": [{"id": "J-004-NUM", "stage_plan": []}]}]}]}]}
    campaign_path = tmp_path / "campaign.json"
    _write_json(campaign_path, campaign)
    _assert_code("QF-01-PLAN-NOT-RUN", lambda: chain_validator.validate_run(book="Num", run_id="run-1", require_complete=False, campaign_path=campaign_path, model_root=tmp_path / "model", root=tmp_path, allow_test_roots=True))


def test_qf03_rejects_boss_backfill_chronology() -> None:
    receipt = _receipt("B06")
    receipt["stage_evidence"]["values"]["peer_premortem_first_read_at"] = "2026-07-22T09:59:00Z"
    _assert_code("QF-03-BOSS-BACKFILL", lambda: core.validate_stage_semantics(receipt))


def test_qf04_rejects_fake_cross_model_independence() -> None:
    receipt = _receipt("B04")
    receipt["counts_as_cross_model_independent_vote"] = True
    receipt["independence_scope"]["counts_as_cross_model_independent_vote"] = True
    _assert_code("QF-04-FAKE-BLINDNESS", lambda: core.validate_stage_semantics(receipt))


@pytest.mark.parametrize(
    ("stage_id", "mutate", "code"),
    [
        ("B07", lambda row: row["stage_evidence"]["values"].update(appeal_count=0, unresolved_appeal_count=1), "QF-05-APPEAL-ERASURE"),
        ("B08", lambda row: row["stage_evidence"]["values"].update(revision_action="silent_rewrite"), "QF-06-LINEAGE-LOSS"),
        ("B10", lambda row: row["stage_evidence"]["values"].update(terminal_completion_receipt_written=True), "QF-11-HASH-CYCLE"),
    ],
)
def test_stage_semantics_reject_known_exploits(stage_id: str, mutate, code: str) -> None:
    receipt = _receipt(stage_id)
    mutate(receipt)
    _assert_code(code, lambda: core.validate_stage_semantics(receipt))


def test_qf12_failed_attempt_requires_fingerprint() -> None:
    receipt = _receipt("B02")
    receipt["outcome"] = "failed"
    _assert_code("QF-12-SAME-STATE-RETRY", lambda: core.validate_stage_semantics(receipt))


def test_immutable_attempt_path_rejects_changed_bytes(tmp_path: Path) -> None:
    target = tmp_path / "attempt.json"
    core.atomic_write(target, b"one\n", immutable=True)
    _assert_code("QF-12-IMMUTABLE-ATTEMPT", lambda: core.atomic_write(target, b"two\n", immutable=True))


@pytest.mark.parametrize(
    ("artifact_location", "direction", "code"),
    [
        (".ai/scratch/multi_model_bible_chunking/M6_other/output.json", "input", "QF-08-SIBLING-CONTAMINATION"),
        ("outside/output.json", "output", "QF-09-FORBIDDEN-EFFECT"),
    ],
)
def test_manifest_enforces_resolved_candidate_scope(tmp_path: Path, artifact_location: str, direction: str, code: str) -> None:
    model_root = tmp_path / ".ai/scratch/multi_model_bible_chunking/M7_sol"
    artifact = tmp_path / artifact_location
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("evidence\n", encoding="utf-8")
    manifest_path = model_root / "manifest.json"
    manifest = {
        "schema_version": "whole_bible_artifact_manifest.v1",
        "manifest_id": "m1",
        "book": "Num",
        "run_id": "run-1",
        "stage_id": "B00",
        "direction": direction,
        "artifacts": [{"artifact_id": "evidence", "path": artifact.relative_to(tmp_path).as_posix(), "sha256": core.digest_file(artifact), "media_type": "application/json", "scope": "candidate"}],
        "contains_scripture_text": False,
        "contains_source_rows": False,
        "contains_prompts_or_hidden_reasoning": False,
        "non_authorizing": True,
    }
    _write_json(manifest_path, manifest)
    _assert_code(code, lambda: core.validate_artifact_manifest(manifest_path, root=tmp_path, model_root=model_root, book="Num", run_id="run-1", stage_id="B00", direction=direction))


def test_relabelled_sibling_copy_path_is_not_a_trusted_input() -> None:
    model_prefix = ".ai/scratch/multi_model_bible_chunking/M7_sol/"
    _assert_code("QF-08-SIBLING-CONTAMINATION", lambda: core.validate_input_path_authority(".ai/context/copied_sibling_map.json", model_prefix=model_prefix))

def test_repo_path_rejects_traversal(tmp_path: Path) -> None:
    _assert_code("QF-08-SIBLING-CONTAMINATION", lambda: core.resolve_repo_path("../escape.json", tmp_path))


def test_qf02_rejects_stale_artifact_hash(tmp_path: Path) -> None:
    model_root = tmp_path / ".ai/scratch/multi_model_bible_chunking/M7_sol"
    artifact = model_root / "artifact.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("evidence\n", encoding="utf-8")
    manifest_path = model_root / "manifest.json"
    manifest = {
        "schema_version": "whole_bible_artifact_manifest.v1", "manifest_id": "m1", "book": "Num", "run_id": "run-1", "stage_id": "B00", "direction": "output",
        "artifacts": [{"artifact_id": "evidence", "path": artifact.relative_to(tmp_path).as_posix(), "sha256": DIGEST, "media_type": "application/json", "scope": "candidate"}],
        "contains_scripture_text": False, "contains_source_rows": False, "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    _write_json(manifest_path, manifest)
    _assert_code("QF-02-FORGED-CHAIN", lambda: core.validate_artifact_manifest(manifest_path, root=tmp_path, model_root=model_root, book="Num", run_id="run-1", stage_id="B00", direction="output"))


def test_gate_bundle_rejects_shell_composition(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence.log"
    evidence.write_text("passed\n", encoding="utf-8")
    digest = core.digest_file(evidence)
    gate_ids = [row["gate_id"] for row in core.load_yaml(core.WORKFLOW)["required_completion_gates"]]
    gates = []
    for index, gate_id in enumerate(gate_ids):
        argv = ["python", "validator.py"] if index else ["python", "validator.py;whoami"]
        gates.append({"gate_id": gate_id, "argv": argv, "exit_code": 0, "status": "passed", "evidence_path": evidence.relative_to(tmp_path).as_posix(), "evidence_sha256": digest, "stdout_sha256": digest})
    bundle = {"schema_version": "whole_bible_completion_gate_bundle.v1", "book": "Num", "run_id": "run-1", "gates": gates, "contains_scripture_text": False, "contains_source_rows": False, "non_authorizing": True}
    bundle_path = tmp_path / "bundle.json"
    _write_json(bundle_path, bundle)
    _assert_code("QF-GATE", lambda: terminal_writer.validate_gate_bundle(bundle_path, book="Num", run_id="run-1", root=tmp_path))


def test_terminal_schema_cannot_claim_qualification_by_label() -> None:
    receipt = {
        "schema_version": "whole_bible_terminal_completion_receipt.v1", "receipt_id": "r", "campaign_id": "c", "campaign_revision": 6, "book": "Num", "run_id": "run-1",
        "b10_stage_receipt_path": "b10.json", "b10_stage_receipt_sha256": DIGEST,
        "extended_evidence_manifest_path": "manifest.json", "extended_evidence_manifest_sha256": DIGEST,
        "completion_gate_bundle_path": "bundle.json", "completion_gate_bundle_sha256": DIGEST,
        "completion_gates": [{"gate_id": "g", "argv": ["python", "gate.py"], "exit_code": 0, "status": "passed", "evidence_path": "evidence.log", "evidence_sha256": DIGEST, "stdout_sha256": DIGEST}],
        "final_artifact_closure": {"artifact.json": DIGEST}, "outcome": "candidate_complete", "unresolved_hold_ids": [], "unresolved_appeal_ids": [],
        "written_at": "2026-07-22T10:00:00Z", "receipt_written_last": True, "replay_plumbing_validated": True,
        "replay_qualified": True, "launch_qualified": False, "whole_bible_form_language_qualified": False,
        "counts_as_cross_model_independent_vote": False, "candidate_only": True, "promotion_authorized": False, "non_authorizing": True,
    }
    _assert_code("QF-SCHEMA", lambda: core.validate_schema(receipt, core.TERMINAL_SCHEMA, "terminal"))


def test_qf14_static_status_cannot_self_qualify() -> None:
    execution = {
        "mode": "specification_only",
        "qualification_status": "replay_qualified",
        "launch_command": "not-authorized",
        "auto_advance_requires_qualification_receipt": True,
    }
    with pytest.raises(workflow_validator.WorkflowValidationError, match="QF-14-QUALIFIED-BY-LABEL"):
        workflow_validator.validate_qualification_boundary(execution)


def test_static_candidate_paths_cannot_escape_m7_root() -> None:
    workflow_validator.require_candidate_scoped_path(
        ".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/Num/runs/<run_id>/run_index.json",
        "valid",
    )
    with pytest.raises(workflow_validator.WorkflowValidationError, match="escapes candidate model root"):
        workflow_validator.require_candidate_scoped_path(
            ".ai/scratch/multi_model_bible_chunking/M6_other/output.json",
            "sibling",
        )


def test_alternate_runtime_roots_are_rejected(tmp_path: Path) -> None:
    campaign_path = tmp_path / "campaign.json"
    _write_json(campaign_path, {"campaign_id": "x", "revision": 6})
    _assert_code("QF-13-ADAPTER-SPLIT", lambda: chain_validator.validate_run(book="Num", run_id="run-1", require_complete=False, campaign_path=campaign_path, model_root=tmp_path / "model", root=tmp_path))


def test_gate_bundle_requires_exact_workflow_argv(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence.log"
    evidence.write_text("passed\n", encoding="utf-8")
    digest = core.digest_file(evidence)
    gates = [
        {"gate_id": gate_id, "argv": ["python", "dummy.py"], "exit_code": 0, "status": "passed", "evidence_path": "evidence.log", "evidence_sha256": digest, "stdout_sha256": digest}
        for gate_id in core.expected_completion_gate_argv(book="Num", run_id="run-1")
    ]
    bundle_path = tmp_path / "bundle.json"
    _write_json(bundle_path, {"schema_version": "whole_bible_completion_gate_bundle.v1", "book": "Num", "run_id": "run-1", "gates": gates, "contains_scripture_text": False, "contains_source_rows": False, "non_authorizing": True})
    _assert_code("QF-GATE", lambda: core.validate_completion_gate_bundle(bundle_path, book="Num", run_id="run-1", root=tmp_path))


def test_terminal_dispositions_are_derived_not_draft_controlled() -> None:
    b07 = _receipt("B07")
    b09 = _receipt("B09")
    b09["stage_evidence"]["values"].update(unresolved_hold_ids=["d1"], unresolved_appeal_ids=["a1"], overall_status="pass_with_holds")
    holds, appeals, outcome = core.derive_terminal_dispositions(b07, b09)
    assert holds == ["d1"]
    assert appeals == ["a1"]
    assert outcome == "candidate_complete_with_holds"
    b09["stage_evidence"]["values"]["unresolved_appeal_ids"] = []
    _assert_code("QF-05-APPEAL-ERASURE", lambda: core.derive_terminal_dispositions(b07, b09))


def test_declared_stage_validator_module_command_imports_and_fails_closed() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "scripts.validate_whole_bible_stage_receipts", "--book", "Num", "--run-id", "absent-run"],
        cwd=core.ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 1
    assert "QF-01-PLAN-NOT-RUN" in completed.stderr
    assert "ModuleNotFoundError" not in completed.stderr

def test_repository_specification_contract_passes_but_does_not_qualify_replay() -> None:
    workflow_validator.validate_workflow()
    workflow_validator.validate_prompts()
    workflow_validator.validate_adapter_and_family()
    workflow_validator.validate_live_campaign()