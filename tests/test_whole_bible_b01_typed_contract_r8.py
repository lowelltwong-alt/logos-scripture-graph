import copy
import json
from pathlib import Path

import pytest

from scripts.validate_whole_bible_b01_typed_contract_r8 import B01R8Error, validate_packet_dir
from scripts.validate_whole_bible_b01_packet_binding_r8 import packet_digest, validate as validate_binding


ROLES = ["original_language_translation_scout", "literary_form_scout", "canonical_relations_and_premortem_scout", "second_temple_rabbinic_context_scout"]
MANIFEST = "sha256:" + "1" * 64


def _identity(n, role):
    return {"execution_id": f"exec-{n}-0001", "assignment_id": f"assign-{n}-0001", "agent_instance_id": f"agent-{n}-0001", "role_id": role, "provider_family": "test"}


def _doc(role, n):
    return {"schema_version": "whole_bible_b01_role_report.v2", "kind": "role_report", "book": "Num", "run_id": "r8", "stage_attempt_id": "a1", "candidate_only": True, "non_authorizing": True, "identity": _identity(n, role), "controller_event_ids": [f"event-{n}-start", f"event-{n}-done"], "input_manifest_sha256": MANIFEST, "observations": [{"observation_id": f"obs-{n}", "scope": "Num", "claim": "A bounded literary observation with evidence.", "evidence_refs": ["src-1"], "confidence": "medium"}], "uncertainties": [], "source_refs": ["src-1"]}


def _packet(tmp_path: Path):
    docs = {f"role-{i}.json": _doc(role, i) for i, role in enumerate(ROLES)}
    docs["manifest.json"] = {"schema_version": "whole_bible_b01_input_manifest.v1", "kind": "input_manifest", "book": "Num", "run_id": "r8", "stage_attempt_id": "a1", "candidate_only": True, "non_authorizing": True, "identity": _identity("manifest", "controller"), "controller_event_ids": ["event-manifest"], "input_manifest_sha256": MANIFEST, "source_ids": ["src-1"], "source_digests": {"src-1": "sha256:" + "2" * 64}}
    boss = {"schema_version": "whole_bible_b01_boss_authorization.v2", "kind": "boss_authorization", "book": "Num", "run_id": "r8", "stage_attempt_id": "a1", "candidate_only": True, "non_authorizing": True, "identity": _identity("boss", "boss"), "controller_event_ids": ["event-boss"], "input_manifest_sha256": MANIFEST, "packet_sha256": "", "redteam_digest": "sha256:" + "3" * 64, "verdict": "NO_GO", "rationale": "Independent review found unresolved concerns and records them.", "rejected_alternatives": ["proceed without evidence"], "dissent": ["role dissent recorded"], "appeal_route": "deferred_to_human_review_queue"}
    docs["boss.json"] = boss
    for name, value in docs.items(): (tmp_path / name).write_text(json.dumps(value), encoding="utf-8")
    boss["packet_sha256"] = packet_digest({name: value for name, value in docs.items() if name != "boss.json"})
    (tmp_path / "boss.json").write_text(json.dumps(boss), encoding="utf-8")


def test_r8_packet_requires_exact_manifest_and_boss_binding(tmp_path):
    _packet(tmp_path)
    result = validate_binding(tmp_path, book="Num", run_id="r8", attempt="a1")
    assert result["B02_authorized"] is False
    boss_path = tmp_path / "boss.json"
    boss = json.loads(boss_path.read_text())
    boss["packet_sha256"] = "sha256:" + "f" * 64
    boss_path.write_text(json.dumps(boss), encoding="utf-8")
    with pytest.raises(B01R8Error, match="QF-B01-BOSS"):
        validate_binding(tmp_path, book="Num", run_id="r8", attempt="a1")


def test_r8_rejects_unicode_boundary_smuggling(tmp_path):
    _packet(tmp_path)
    report = next(tmp_path.glob("role-*.json"))
    doc = json.loads(report.read_text())
    doc["observations"][0]["s\u200bpan"] = "smuggled"
    report.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(B01R8Error, match="QF-15-B01-BOUNDARY-LEAKAGE"):
        validate_packet_dir(tmp_path, book="Num", run_id="r8", attempt="a1")



