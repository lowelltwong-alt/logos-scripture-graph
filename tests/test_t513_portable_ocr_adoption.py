from pathlib import Path

import pytest
import yaml

from pipelines.ingest.portable_ocr_adapter import OcrAdmissionError, build_execution_plan


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / ".ai" / "control" / "t513_portable_ocr_adoption.yaml"


@pytest.fixture()
def policy():
    return yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))


def request(external: Path, use_class: str = "synthetic_fixture"):
    return {
        "source_id": "synthetic-script-smoke",
        "use_class": use_class,
        "input_path": str(external / "inputs" / "sample.png"),
        "output_root": str(external / "outputs"),
        "engine_ids": ["engine-a@1", "engine-b@2"],
    }


def test_synthetic_plan_is_metadata_only_and_never_promotes(tmp_path, policy):
    plan = build_execution_plan(request(tmp_path), policy, repo_root=ROOT, external_root=tmp_path)
    assert plan.payload_access_authorized is False
    assert plan.execution_authorized is False
    assert plan.stage == "preliminary_metadata_only"
    assert plan.scripture_promotion_authorized is False


def test_induocr_is_disabled_and_requires_rights(tmp_path, policy):
    candidate = request(tmp_path, "external_benchmark")
    candidate["benchmark_id"] = "induocr"
    candidate["benchmark_revision"] = policy["benchmarks"]["induocr"]["pinned_huggingface_revision"]
    candidate["benchmark_manifest_sha256"] = "a" * 64
    candidate["rights_record"] = {"decision_id": "future", "status": "approved", "record_sha256": "b" * 64}
    with pytest.raises(OcrAdmissionError, match="not authorized"):
        build_execution_plan(candidate, policy, repo_root=ROOT, external_root=tmp_path)


def test_portable_induocr_profile_contains_no_downloader_or_training_authority():
    import json

    profile = json.loads(
        (ROOT / "tools" / "portable_ocr" / "benchmarks" / "induocr.profile.json").read_text(encoding="utf-8")
    )
    assert profile["enabled"] is False
    assert profile["automatic_download"] is False
    assert profile["training_use"] is False
    assert profile["expected_files_and_sha256"] == []


def test_public_research_source_is_not_currently_authorized(tmp_path, policy):
    candidate = request(tmp_path, "authorized_public_research_source")
    candidate["rights_record"] = {"decision_id": "future", "status": "approved", "record_sha256": "b" * 64}
    candidate["content_sha256"] = "a" * 64
    with pytest.raises(OcrAdmissionError, match="not authorized"):
        build_execution_plan(candidate, policy, repo_root=ROOT, external_root=tmp_path)


def test_rejects_single_or_duplicate_engine(tmp_path, policy):
    candidate = request(tmp_path)
    candidate["engine_ids"] = ["same@1", "same@1"]
    with pytest.raises(OcrAdmissionError, match="two genuinely distinct"):
        build_execution_plan(candidate, policy, repo_root=ROOT, external_root=tmp_path)


def test_rejects_repo_and_onedrive_payload_paths(tmp_path, policy):
    candidate = request(tmp_path)
    candidate["input_path"] = str(ROOT / "sample.png")
    with pytest.raises(OcrAdmissionError, match="LOGOS_EXTERNAL_ASSET_ROOT"):
        build_execution_plan(candidate, policy, repo_root=ROOT, external_root=tmp_path)
    onedrive = tmp_path / "OneDrive" / "payloads"
    candidate = request(tmp_path)
    candidate["input_path"] = str(onedrive / "sample.png")
    with pytest.raises(OcrAdmissionError, match="OneDrive"):
        build_execution_plan(candidate, policy, repo_root=ROOT, external_root=tmp_path)


def test_external_root_and_required_fields_fail_closed(tmp_path, policy):
    with pytest.raises(OcrAdmissionError, match="LOGOS_EXTERNAL_ASSET_ROOT"):
        build_execution_plan(request(tmp_path), policy, repo_root=ROOT, external_root=None)
    candidate = request(tmp_path)
    del candidate["source_id"]
    with pytest.raises(OcrAdmissionError, match="missing required"):
        build_execution_plan(candidate, policy, repo_root=ROOT, external_root=tmp_path)


def test_future_boolean_flips_do_not_grant_payload_or_execution_access(tmp_path, policy):
    import copy

    future = copy.deepcopy(policy)
    future["benchmarks"]["induocr"]["enabled"] = True
    future["authority"]["induocr_download_authorized"] = True
    future["authority"]["induocr_execution_authorized"] = True
    candidate = request(tmp_path, "external_benchmark")
    candidate.update({
        "benchmark_id": "induocr",
        "benchmark_revision": future["benchmarks"]["induocr"]["pinned_huggingface_revision"],
        "benchmark_manifest_sha256": "a" * 64,
        "rights_record": {"decision_id": "approved-future", "status": "approved", "record_sha256": "b" * 64},
    })
    plan = build_execution_plan(candidate, future, repo_root=ROOT, external_root=tmp_path)
    assert plan.payload_access_authorized is False
    assert plan.execution_authorized is False


def test_future_metadata_rejects_fake_hashes_and_unstructured_rights(tmp_path, policy):
    import copy

    future = copy.deepcopy(policy)
    future["authority"]["manuscript_ocr_execution_authorized"] = True
    candidate = request(tmp_path, "authorized_public_research_source")
    candidate["content_sha256"] = "z" * 64
    candidate["rights_record"] = {"decision_id": "future", "status": "approved", "record_sha256": "b" * 64}
    with pytest.raises(OcrAdmissionError, match="hexadecimal"):
        build_execution_plan(candidate, future, repo_root=ROOT, external_root=tmp_path)
    candidate["content_sha256"] = "a" * 64
    candidate["rights_record"] = "approved"
    with pytest.raises(OcrAdmissionError, match="structured rights_record"):
        build_execution_plan(candidate, future, repo_root=ROOT, external_root=tmp_path)
