import copy

import pytest

from scripts.validate_whole_bible_b01_typed_contract import B01ContractError, ROLES, validate_packet


def _doc():
    def ident(n, role):
        return {"execution_id": f"exec-{n}", "assignment_id": f"assign-{n}", "agent_instance_id": f"agent-{n}", "role_id": role}
    reports = {
        role: {"identity": ident(i, role), "payload": {"observations": [f"observation-{role}"], "evidence_refs": ["e1"]}}
        for i, role in enumerate(sorted(ROLES))
    }
    return ({"schema_version": "whole_bible_b01_typed_contract.v1", "kind": "evidence_packet", "book": "Num", "run_id": "r1", "stage_attempt_id": "a1", "candidate_only": True, "non_authorizing": True, "identity": ident("packet", "controller"), "payload": {}}, reports,
            {"identity": ident("syn", "synth"), "payload": {"role_report_artifact_ids": list(ROLES)}},
            {"identity": ident("rt", "redteam"), "payload": {"findings": ["finding"]}},
            {"identity": ident("boss", "boss"), "payload": {"input_manifest_sha256": "sha256:manifest", "verdict": "NO_GO", "dissent": ["held"], "appeal_route": "human"}})


def test_valid_typed_packet():
    packet, reports, synthesis, redteam, boss = _doc()
    validate_packet(packet, manifest={"input": "sha256:manifest"}, role_reports=reports, synthesis=synthesis, redteam=redteam, boss=boss)


@pytest.mark.parametrize("mutator,code", [
    (lambda p, r, s, t, b: r.pop(next(iter(r))), "QF-16-B01-INPUT-CLOSURE"),
    (lambda p, r, s, t, b: r[next(iter(r))]["payload"].pop("observations"), "QF-16-B01-ROLE-REPORT"),
    (lambda p, r, s, t, b: b["identity"].update(r[next(iter(r))]["identity"]), "QF-B01-BOSS"),
    (lambda p, r, s, t, b: b["payload"].update({"dissent": []}), "QF-B01-APPEAL-CLOSURE"),
])
def test_typed_packet_rejects_redteam_mutations(mutator, code):
    packet, reports, synthesis, redteam, boss = _doc()
    mutator(packet, reports, synthesis, redteam, boss)
    with pytest.raises(B01ContractError, match=code):
        validate_packet(packet, manifest={"input": "sha256:manifest"}, role_reports=reports, synthesis=synthesis, redteam=redteam, boss=boss)


def test_payload_normalization_blocks_zero_width_chunk_map():
    packet, reports, synthesis, redteam, boss = _doc()
    packet["payload"] = {"c\u200bhunkMap": []}
    with pytest.raises(B01ContractError, match="QF-20-B01-PAYLOAD"):
        validate_packet(packet, manifest={"input": "sha256:manifest"}, role_reports=reports, synthesis=synthesis, redteam=redteam, boss=boss)
