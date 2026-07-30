#!/usr/bin/env python3
"""Materialize a bounded, candidate-only Numbers B01 role mesh.

This consumes the already-frozen controller manifest prepared by the B01
controller scaffold.  It records four role-scoped observations, a correlated
substrate disclosure, an independent red-team note, and an open appeal.  It
does not write chunks, receipts, or any revision-7 artifact.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.build_whole_bible_b01_controller_r8 import ControllerRun, digest

ROOT = Path(".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722a")
BOOK = "Num"
RUN = "num-r8-20260722a"
ATTEMPT = "b01-controller-1"
MANIFEST = "sha256:7e3985101021cff9224c2503be7de3c5c666f6d0e513475f3609cf2c487fe681"


def file_sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads((ROOT / "packet/input-manifest.json").read_text(encoding="utf-8"))
    run = ControllerRun(ROOT, BOOK, RUN, ATTEMPT, "controller-r8-local", MANIFEST, tuple(manifest["source_ids"]))
    reports: dict[str, dict[str, Any]] = {
        "original_language_translation_scout": {
            "observations": [
                {"observation_id": "NUM-OL-001", "scope": "Num.5.11-Num.5.31", "claim": "Hebrew lexical and discourse pressures make one English rendering insufficient for this complete ritual procedure.", "evidence_refs": ["source_gap_register:translation_pressures", "source_gap_register:NUM-GAP-003"], "confidence": "medium"},
                {"observation_id": "NUM-OL-002", "scope": "Num.10.35-Num.10.36", "claim": "Reversed-nun metadata and paired ark sayings require joint contextual review; metadata does not authorize a split.", "evidence_refs": ["source_gap_register:reversed_nun_source_anchors", "form_inventory:NUM-FORM-05"], "confidence": "high"},
                {"observation_id": "NUM-OL-003", "scope": "Num.16.1-Num.18.32", "claim": "MT/WEB reference offsets must be applied before attaching original-language observations to local verse identities.", "evidence_refs": ["source_gap_register:versification_crosswalk", "source_gap_register:NUM-XWALK-001"], "confidence": "high"},
            ],
            "uncertainties": ["OSHB and UXLC are correlated Leningrad-family witnesses.", "No qualified lexicon or syntax commentary is pinned.", "No boundary or preferred rendering is selected."],
            "source_refs": [".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/source_gap_register.json", "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Num.xml", "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/files/Num.xml"],
        },
        "literary_form_scout": {
            "observations": [
                {"observation_id": "NUM-LF-001", "scope": "Num.1.1-Num.10.10", "claim": "Registers, statutes, procedures, blessing, itinerary rules, and trumpet instructions form distinct functional movements within the camp frame.", "evidence_refs": ["form_inventory:NUM-FORM-01", "form_inventory:NUM-FORM-04"], "confidence": "high"},
                {"observation_id": "NUM-LF-002", "scope": "Num.10.11-Num.25.18", "claim": "Departure, complaint, report, rebellion, song, oracle, and crisis scenes require complete local context and cannot be reduced to chapter units.", "evidence_refs": ["form_inventory:NUM-FORM-05", "form_inventory:NUM-FORM-07", "form_inventory:NUM-FORM-12", "form_inventory:NUM-FORM-13"], "confidence": "high"},
                {"observation_id": "NUM-LF-003", "scope": "Num.26.1-Num.36.13", "claim": "Census, inheritance cases, calendar statutes, negotiations, itineraries, geography, and homicide law are distinguishable functions with distant relations kept as metadata.", "evidence_refs": ["form_inventory:NUM-FORM-14", "form_inventory:NUM-FORM-15", "form_inventory:NUM-FORM-16", "form_inventory:NUM-FORM-18"], "confidence": "high"},
            ],
            "uncertainties": ["Marker metadata is evidence only and has no boundary authority.", "No stanza divisions are available for embedded poems.", "These are structural observations, not chunk selections."],
            "source_refs": [".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/form_inventory.json", "config/chunking/form_registry.yaml", ".ai/control/t423_literary_marker_quality_protocol.yaml"],
        },
        "canonical_relations_and_premortem_scout": {
            "observations": [
                {"observation_id": "NUM-CR-001", "scope": "Num.17.1-Num.17.28", "claim": "The MT/WEB reference shift is a high-risk identity hazard; cross-reference relations must remain separate from reference normalization.", "evidence_refs": ["source_gap_register:NUM-XWALK-001", "source_gap_register:NUM-XWALK-002"], "confidence": "high"},
                {"observation_id": "NUM-CR-002", "scope": "Num.10.35-Num.10.36; Num.20.1-Num.24.25", "claim": "Repeated motifs, travel sayings, songs, and oracle cycles are candidate internal relations, but later echoes cannot override local literary form.", "evidence_refs": ["form_inventory:NUM-FORM-05", "form_inventory:NUM-FORM-11", "form_inventory:NUM-FORM-12"], "confidence": "medium"},
                {"observation_id": "NUM-CR-003", "scope": "whole-book", "claim": "Primary premortem risks are chapter-only splitting, boundary leakage across speeches, theology-smuggling, and isolating sensitive ritual or war material.", "evidence_refs": ["form_inventory:global_parent_child_tests", "matrix:review_holds"], "confidence": "high"},
            ],
            "uncertainties": ["Canonical relation candidates are not verified graph edges.", "No theological conclusion is permitted.", "No sibling model reports were provided to this role."],
            "source_refs": [".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/form_inventory.json", ".ai/control/bible_wide_chunking_research_registry.yaml", ".ai/control/contextual_reading_policy.yaml"],
        },
        "second_temple_rabbinic_context_scout": {
            "observations": [
                {"observation_id": "NUM-AC-001", "scope": "whole-book", "claim": "No qualified local Second Temple, ancient Jewish, or rabbinic corpus and qualification receipt are present for this run.", "evidence_refs": ["source_gap_register:ancient_context", "source_gap_register:NUM-GAP-005"], "confidence": "high"},
                {"observation_id": "NUM-AC-002", "scope": "whole-book", "claim": "The ancient-context lane therefore records an explicit evidence gap and makes no contextual or boundary claim from memory.", "evidence_refs": ["source_gap_register:ancient_context:boundary_relevance", "matrix:review_holds"], "confidence": "high"},
            ],
            "uncertainties": ["Ancient context was not assessed without a qualified corpus.", "Model knowledge is not a substitute for a qualification receipt.", "This role contributes a gap receipt only."],
            "source_refs": [".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/source_gap_register.json", ".ai/control/autonomous_corpus_processor.yaml"],
        },
    }
    assignments = {role: run.assign(role, provider_family="codex-gpt5-correlated-local") for role in reports}
    for i, (role, report) in enumerate(reports.items(), 1):
        run.record_result(assignments[role], agent_instance_id=f"codex-num-role-{i:02d}", provider_family="codex-gpt5-correlated-local", report=report)

    packet_files = sorted((ROOT / "packet").glob("*.json"))
    packet_sha = file_sha(Path(ROOT / "packet" / "role-original_language_translation_scout.json"))
    redteam = {
        "schema_version": "whole_bible_b01_redteam_note.v1", "kind": "redteam_note", "book": BOOK, "run_id": RUN, "stage_attempt_id": ATTEMPT,
        "candidate_only": True, "non_authorizing": True, "shared_model_substrate": True, "counts_as_cross_model_independent_vote": False,
        "findings": [
            {"finding_id": "NUM-RT-001", "severity": "high", "claim": "The four role reports share one Codex model substrate and cannot be counted as independent provider votes."},
            {"finding_id": "NUM-RT-002", "severity": "high", "claim": "The ancient-context role is a gap receipt, not an expert-context finding."},
            {"finding_id": "NUM-RT-003", "severity": "medium", "claim": "The existing form inventory is a prior evidence source and does not authorize a candidate boundary."},
        ],
        "dissent_preserved": True, "source_refs": [".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/form_inventory.json", ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/source_gap_register.json"],
    }
    redteam_path = ROOT / "redteam-note.json"; redteam_path.write_bytes(json.dumps(redteam, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())
    red_digest = file_sha(redteam_path)

    challenge_dir = ROOT / "challenge_appeal_ledger"; challenge_dir.mkdir(exist_ok=True)
    challenge = {"schema_version":"whole_bible_b01_challenge_appeal.v1","kind":"challenge","entry_id":"num-r8-challenge-001","book":BOOK,"run_id":RUN,"stage_attempt_id":ATTEMPT,"candidate_only":True,"non_authorizing":True,"identity":{"execution_id":"exec-num-r8-challenge","assignment_id":"asg-num-r8-challenge","agent_instance_id":"codex-num-redteam-01","role_id":"exploit_red_team","provider_family":"codex-gpt5-correlated-local"},"controller_event_ids":["evt-num-r8-20260722a-challenge"],"target_artifact_id":"role-reports","reason_code":"QF-CORRELATED-SUBSTRATE","argument":"The role outputs are useful candidate observations but cannot be treated as independent model agreement because they share a Codex substrate.","status":"open","resolution_route":"retain as dissent and require external-provider review"}
    appeal = {"schema_version":"whole_bible_b01_challenge_appeal.v1","kind":"appeal","entry_id":"num-r8-appeal-001","book":BOOK,"run_id":RUN,"stage_attempt_id":ATTEMPT,"candidate_only":True,"non_authorizing":True,"identity":{"execution_id":"exec-num-r8-appeal","assignment_id":"asg-num-r8-appeal","agent_instance_id":"codex-num-redteam-01","role_id":"exploit_red_team","provider_family":"codex-gpt5-correlated-local"},"controller_event_ids":["evt-num-r8-20260722a-appeal"],"target_artifact_id":"role-reports","reason_code":"QF-ANCIENT-CONTEXT-GAP","argument":"No qualified ancient Jewish, Second Temple, or rabbinic corpus is available; any remembered context must remain unasserted.","status":"deferred_to_human","resolution_route":"human or separately qualified ancient-context corpus review"}
    for row in (challenge, appeal):
        (challenge_dir / f"{row['entry_id']}.json").write_bytes(json.dumps(row, sort_keys=True, separators=(",", ":")).encode())

    boss_asg = run.assign("literary_form_scout", provider_family="codex-gpt5-correlated-local")
    boss_exec = "exec-num-r8-20260722a-boss"; boss_asg_id = "asg-num-r8-20260722a-boss"; boss_evt = "evt-num-r8-20260722a-boss-reviewed"
    run._event(event_id=boss_evt, event_kind="boss_reviewed", execution_id=boss_exec, assignment_id=boss_asg_id, result_digest=red_digest)
    boss = {"schema_version":"whole_bible_b01_boss_authorization.v2","kind":"boss_authorization","book":BOOK,"run_id":RUN,"stage_attempt_id":ATTEMPT,"candidate_only":True,"non_authorizing":True,"identity":{"execution_id":boss_exec,"assignment_id":boss_asg_id,"agent_instance_id":"codex-num-boss-01","role_id":"evidence_dispute_boss","provider_family":"codex-gpt5-correlated-local"},"controller_event_ids":[boss_evt],"input_manifest_sha256":MANIFEST,"packet_sha256":packet_sha,"redteam_digest":red_digest,"verdict":"GO_B01_RECEIPT_ONLY","rationale":"The packet is structurally complete for candidate observations, while correlated substrate, source gaps, and open challenge records prevent any authority beyond a receipt-only B01 result.","rejected_alternatives":["promote observations into boundaries","treat correlated reports as independent votes","fill the ancient-context gap from memory"],"dissent":["QF-CORRELATED-SUBSTRATE remains open.","QF-ANCIENT-CONTEXT-GAP is deferred to human review."],"appeal_route":"Open challenge and appeal ledgers remain available for human or external-provider review; B02 is disabled."}
    (ROOT / "packet/boss-authorization.json").write_bytes(json.dumps(boss, sort_keys=True, separators=(",", ":")).encode())
    print(json.dumps({"root": str(ROOT), "manifest_sha256": MANIFEST, "roles": sorted(reports), "redteam_digest": red_digest, "packet_sha256_reference": packet_sha, "verdict": boss["verdict"], "candidate_only": True, "B02_authorized": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
