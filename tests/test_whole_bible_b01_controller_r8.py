from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_whole_bible_b01_controller_r8 import ROLES, prepare


def test_prepare_freezes_manifest_before_role_assignment(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text('{"source":"metadata-only"}', encoding="utf-8")
    run = prepare(root=tmp_path / "run", book="Num", run_id="r8-controller", attempt_id="a1", source_paths=[source])
    manifest = json.loads((run.packet_dir / "input-manifest.json").read_text(encoding="utf-8"))
    assert manifest["candidate_only"] is True and manifest["non_authorizing"] is True
    assert manifest["source_ids"] and manifest["source_digests"]
    assignment = run.assign(ROLES[0])
    assert (run.events_dir / f"{assignment['assignment_event_id']}.json").exists()
    assert json.loads((run.packet_dir / "input-manifest.json").read_text(encoding="utf-8")) == manifest


def test_result_is_controller_bound_and_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text('{"book":"Num","metadata":true}', encoding="utf-8")
    run = prepare(root=tmp_path / "run", book="Num", run_id="r8-result", attempt_id="a1", source_paths=[source])
    assignment = run.assign(ROLES[1], provider_family="test-provider")
    report = {"observations": [{"observation_id": "o-001", "scope": "Num", "claim": "Literary observation only.", "evidence_refs": ["s1"], "confidence": "medium"}], "uncertainties": ["boundary remains candidate"], "source_refs": ["s1"]}
    path = run.record_result(assignment, agent_instance_id="agent-r8-test", report=report, provider_family="test-provider")
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["input_manifest_sha256"] == run.manifest_sha256
    assert len(doc["controller_event_ids"]) == 3
    assert doc["identity"]["provider_family"] == "test-provider"
    assert run.record_result(assignment, agent_instance_id="agent-r8-test", report=report, provider_family="test-provider") == path


def test_result_rejects_extra_payload_and_unknown_role(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text("{}", encoding="utf-8")
    run = prepare(root=tmp_path / "run", book="Num", run_id="r8-negative", attempt_id="a1", source_paths=[source])
    with pytest.raises(ValueError, match="unsupported B01 role"):
        run.assign("theology_decider")
    assignment = run.assign(ROLES[2])
    with pytest.raises(ValueError, match="only observations"):
        run.record_result(assignment, agent_instance_id="agent-r8-test", report={"observations": [], "uncertainties": [], "source_refs": [], "raw_text": "no"})
