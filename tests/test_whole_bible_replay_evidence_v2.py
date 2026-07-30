from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from scripts import validate_whole_bible_candidate_workflow_v2 as static_v2
from scripts import write_whole_bible_stage_receipt_v2 as writer_v2
from scripts import whole_bible_replay_evidence_v2 as core


@pytest.fixture
def scratch() -> Path:
    default_parent = Path(r"C:\tmp\logos-scripture-v2-tests") if os.name == "nt" else Path(tempfile.gettempdir()) / "logos-scripture-v2-tests"
    parent = Path(os.environ.get("LOGOS_V2_TEST_TMP", str(default_parent)))
    parent.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix="rev7-", dir=parent))
    try:
        yield path
    finally:
        shutil.rmtree(path)


def _write(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _assert_code(code: str, call) -> None:
    with pytest.raises(core.ReplayEvidenceError) as exc:
        call()
    assert exc.value.code == code


def _execution(prompt: str) -> dict:
    roles = core.EXPECTED_ROLES
    functions = {
        "original_language_translation_scout": ["translation_forecast"],
        "literary_form_scout": ["literary_form_forecast"],
        "canonical_relations_and_premortem_scout": ["canonical_relation_forecast", "premortem"],
        "second_temple_rabbinic_context_scout": ["ancient_context_gap_check"],
    }
    return {
        "schema_version": "whole_bible_b01_prompt_execution.v1", "book": "Num", "run_id": "run-1",
        "stage_attempt_id": "attempt-1", "execution_id": f"exec-{prompt}", "assignment_id": f"assign-{prompt}",
        "agent_instance_id": f"agent-{prompt}", "prompt_template_id": prompt, "role_id": roles[prompt],
        "assigned_functions": functions[prompt], "dual_role_assignment": prompt == "canonical_relations_and_premortem_scout",
        "input_artifact_ids": ["canonical_passages"], "output_artifact_ids": [f"report-{prompt}"],
        "prompt_pack_sha256": core.digest_file(core.PROMPTS), "workflow_sha256": core.digest_file(core.WORKFLOW),
        "runtime_adapter_sha256": core.digest_file(core.ADAPTER), "started_at": "2026-07-22T12:00:00Z",
        "finished_at": "2026-07-22T12:01:00Z", "time_source": "runtime_attested",
        "status": "gap_returned" if prompt == "second_temple_rabbinic_context_scout" else "succeeded",
        "raw_result_path_or_gap": "gap:not_checked_by_execution_shape_test", "raw_result_sha256_or_gap": "gap:not_checked_by_execution_shape_test",
        "scout_artifact_blindness": True, "sibling_model_maps_read": False, "shared_model_substrate": True,
        "counts_as_cross_model_independent_vote": False, "contains_scripture_text": False,
        "contains_source_rows": False, "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }


def test_revision7_static_contract_is_candidate_only() -> None:
    result = static_v2.validate()
    assert result["book_jobs"] == 66
    assert result["supported_stage_ceiling"] == "B00"
    assert result["B02_authorized"] is False
    assert result["replay_qualified"] is False


def test_revision7_b01_materialization_is_fail_closed() -> None:
    assert core.AUTHORIZED_STAGES == ("B00",)
    assert core.B01_MATERIALIZATION_ENABLED is False


def test_revision7_runbook_captures_mesh_boss_and_appeals() -> None:
    text = core.RUNBOOK.read_text(encoding="utf-8")
    for required in ("original_language_translation_scout", "literary_form_scout", "canonical_relations_and_premortem_scout", "second_temple_rabbinic_context_scout", "evidence_dispute_boss", "appeal", "B02_authorized"):
        assert required in text


def test_prepare_does_not_allow_an_already_selected_stage(scratch: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    draft = _write(scratch / "draft.json", {"draft": True})
    campaign = _write(scratch / "campaign.json", {"campaign": True})
    registry = _write(scratch / "registry.json", {"registry": True})
    observed: dict = {}

    def selected_guard(**kwargs):
        observed.update(kwargs)
        if kwargs.get("allow_selected_validation", False):
            raise AssertionError("preparation bypassed the selected-stage guard")
        raise core.ReplayEvidenceError("QF-12-IMMUTABLE-ATTEMPT", "successful B00 is already selected; use a fresh run")

    monkeypatch.setattr(writer_v2, "_build_candidate", selected_guard)
    _assert_code("QF-12-IMMUTABLE-ATTEMPT", lambda: writer_v2.prepare_stage_receipt(draft_path=draft, campaign_path=campaign, registry_path=registry, model_root=scratch, root=scratch, allow_test_roots=True))
    assert observed.get("allow_selected_validation", False) is False
    assert not (scratch / "attempt" / "prepared_commit.json").exists()
def test_v2_receipt_log_is_idempotent_and_rejects_conflict(scratch: Path) -> None:
    path = scratch / "receipts.v2.jsonl"
    row = {"schema_version": "whole_bible_stage_receipt_log.v2", "campaign_id": "c", "book": "Num", "run_id": "r", "stage_id": "B00", "attempt_id": "a", "receipt_path": "state/receipt.json", "receipt_sha256": "sha256:" + "1" * 64, "outcome": "succeeded", "non_authorizing": True}
    core.ensure_v2_receipt_log(path, row, root=scratch)
    core.ensure_v2_receipt_log(path, row, root=scratch)
    assert core.load_v2_receipt_log(path, root=scratch) == [row]
    conflict = dict(row, receipt_sha256="sha256:" + "2" * 64)
    _assert_code("QF-LOG-PARITY", lambda: core.ensure_v2_receipt_log(path, conflict, root=scratch))
def test_revision6_numbers_b00_still_validates_unchanged() -> None:
    completed = subprocess.run(
        [sys.executable, "-B", "-m", "scripts.validate_whole_bible_stage_receipts", "--book", "Num", "--run-id", "num-native-r6-20260722a", "--require-through", "B00"],
        cwd=core.ROOT, capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert result["selected_stages"] == ["B00"]
    assert result["replay_qualified"] is False


def test_exact_gapless_form_partition_is_rejected() -> None:
    passages, _ = core._book_rows("Num", core.ROOT)
    ordinals = {row["osis_ref"]: index for index, row in enumerate(passages)}
    value = [{"scope": "Num.1.1-Num.10.10"}, {"scope": "Num.10.11-Num.36.13"}]
    _assert_code("QF-15-B01-BOUNDARY-LEAKAGE", lambda: core.reject_partition_like_ranges(value, ordinals=ordinals))


def test_sparse_overlapping_form_observations_are_allowed() -> None:
    passages, _ = core._book_rows("Num", core.ROOT)
    ordinals = {row["osis_ref"]: index for index, row in enumerate(passages)}
    value = [{"scope": "Num.10.35-Num.10.36"}, {"scope": "Num.10.11-Num.12.16"}, {"scope": "Num.22.2-Num.24.25"}]
    core.reject_partition_like_ranges(value, ordinals=ordinals)


def test_book_row_cache_invalidates_on_exact_content_change(scratch: Path) -> None:
    passage_path = scratch / "data/canonical/scripture/passages/passages.jsonl"
    witness_path = scratch / "data/canonical/translations/eng-web/translation_witnesses.jsonl"
    passage_path.parent.mkdir(parents=True)
    witness_path.parent.mkdir(parents=True)
    passage_path.write_text(json.dumps({"book": "Num", "chapter": 1, "osis_ref": "Num.1.1"}) + "\n", encoding="utf-8")
    witness_path.write_text(json.dumps({"osis_ref": "Num.1.1", "text": "First test verse."}) + "\n", encoding="utf-8")
    first, _ = core._book_rows("Num", scratch)
    assert len(first) == 1
    passage_path.write_text(passage_path.read_text(encoding="utf-8") + json.dumps({"book": "Num", "chapter": 1, "osis_ref": "Num.1.2"}) + "\n", encoding="utf-8")
    witness_path.write_text(witness_path.read_text(encoding="utf-8") + json.dumps({"osis_ref": "Num.1.2", "text": "Second test verse."}) + "\n", encoding="utf-8")
    second, _ = core._book_rows("Num", scratch)
    assert len(second) == 2

@pytest.mark.parametrize("payload", [
    {"chain_of_thought": "hidden"},
    {"source": "<osis><verse>raw</verse></osis>"},
    {"text": "metadata masquerading as text"},
])
def test_b01_payload_scanner_rejects_hidden_or_source_payload(scratch: Path, payload: dict) -> None:
    path = _write(scratch / "payload.json", payload)
    _assert_code("QF-20-B01-PAYLOAD", lambda: core.validate_b01_payload([path], book="Num", root=core.ROOT))


def test_b01_payload_scanner_rejects_exact_canonical_verse(scratch: Path) -> None:
    _, witnesses = core._book_rows("Num", core.ROOT)
    path = _write(scratch / "verse.json", {"observation": witnesses[0]["text"]})
    _assert_code("QF-20-B01-PAYLOAD", lambda: core.validate_b01_payload([path], book="Num", root=core.ROOT))


def test_b01_payload_scanner_allows_references_hashes_and_paraphrase(scratch: Path) -> None:
    path = _write(scratch / "safe.json", {"scope": "Num.10.35-Num.10.36", "sha256": "sha256:" + "0" * 64, "summary": "Paired ark sayings require contextual review."})
    core.validate_b01_payload([path], book="Num", root=core.ROOT)


def test_numbers_source_views_are_archive_exact() -> None:
    core.validate_source_view_ancestry(
        manifest_path=core.ROOT / "data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml",
        archive_path=core.ROOT / "data/raw/original_language/hebrew/openscriptures_oshb/raw/openscriptures_oshb-3d15126fb1ef.zip",
        view_manifest_path=core.ROOT / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/canonical_source_view_manifest.yaml",
        ledger_path=core.ROOT / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/included_files.jsonl",
        view_path=core.ROOT / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Num.xml", book="Num",
    )
    core.validate_source_view_ancestry(
        manifest_path=core.ROOT / "data/raw/original_language/hebrew/tanach_us_uxlc/source_manifest.yaml",
        archive_path=core.ROOT / "data/raw/original_language/hebrew/tanach_us_uxlc/raw/Tanach.xml.zip",
        view_manifest_path=core.ROOT / "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/canonical_source_view_manifest.yaml",
        ledger_path=core.ROOT / "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/included_files.jsonl",
        view_path=core.ROOT / "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/files/Num.xml", book="Num",
    )


def test_numbers_oshb_feature_set_is_exact() -> None:
    qere, reversed_nun = core._oshb_num_features(core.ROOT / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Num.xml")
    assert qere == ["Num.1.16", "Num.12.3", "Num.14.36", "Num.16.11", "Num.21.32", "Num.23.13", "Num.26.9", "Num.32.7", "Num.34.4"]
    assert reversed_nun == ["Num.10.34", "Num.10.36"]


def test_execution_requires_strict_runtime_time() -> None:
    row = _execution("original_language_translation_scout")
    row["finished_at"] = row["started_at"]
    _assert_code("QF-19-B01-TIMING", lambda: core.validate_b01_execution(row, book="Num", run_id="run-1", attempt_id="attempt-1", input_ids={"canonical_passages"}, output_ids={row["output_artifact_ids"][0]}))


def test_canonical_premortem_execution_requires_dual_function_disclosure() -> None:
    row = _execution("canonical_relations_and_premortem_scout")
    row["dual_role_assignment"] = False
    _assert_code("QF-16-B01-ROLE-EXECUTION-GAP", lambda: core.validate_b01_execution(row, book="Num", run_id="run-1", attempt_id="attempt-1", input_ids={"canonical_passages"}, output_ids={row["output_artifact_ids"][0]}))


def test_ancient_context_role_must_execute_a_gap_when_unqualified() -> None:
    row = _execution("second_temple_rabbinic_context_scout")
    row["status"] = "succeeded"
    _assert_code("QF-16-B01-ROLE-EXECUTION-GAP", lambda: core.validate_b01_execution(row, book="Num", run_id="run-1", attempt_id="attempt-1", input_ids={"canonical_passages"}, output_ids={row["output_artifact_ids"][0]}))


def test_attempt_bundle_paths_are_exact(scratch: Path) -> None:
    base = core.attempt_root(scratch, "Num", "run-1", "B01", "attempt-1")
    core.validate_attempt_bundle_paths(
        draft_path=base / "draft.json", input_manifest_path=base / "manifests/input.json",
        output_manifest_path=base / "manifests/output.json", model_root=scratch,
        book="Num", run_id="run-1", stage_id="B01", attempt_id="attempt-1",
    )
    _assert_code("QF-12-IMMUTABLE-ATTEMPT", lambda: core.validate_attempt_bundle_paths(
        draft_path=base / "wrong.json", input_manifest_path=base / "manifests/input.json",
        output_manifest_path=base / "manifests/output.json", model_root=scratch,
        book="Num", run_id="run-1", stage_id="B01", attempt_id="attempt-1",
    ))


def test_v2_fails_closed_on_B02() -> None:
    receipt = {"stage_id": "B02"}
    _assert_code("QF-21-UNMIGRATED-STAGE", lambda: core.validate_stage_semantics(receipt))


def test_prepared_B00_has_no_stage_side_effect() -> None:
    run = core.run_dir(core.MODEL_ROOT, "Num", "num-native-r7-20260722a")
    prepared = run / "attempts/B00/b00-preflight-1/prepared_commit.json"
    assert prepared.is_file()
    assert not (run / "run_index.json").exists()
    assert not (run / "stages/B00/b00-preflight-1.json").exists()
    row = core.load_json(prepared)
    assert row["candidate_receipt"]["stage_id"] == "B00"
    assert row["candidate_receipt"]["campaign_revision"] == 7
