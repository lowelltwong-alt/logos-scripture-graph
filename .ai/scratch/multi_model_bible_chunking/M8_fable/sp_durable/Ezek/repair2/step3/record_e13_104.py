#!/usr/bin/env python3
"""Queue E13-104: REPAIR-2 step 3 applied - the corpus is hard GREEN - and every routed item carried forward by name."""
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
e = {
    "id": "E13-104", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": False, "raised_by": "orchestrator (claude-opus-5)", "status": "DONE - step 4 next",
    "headline": ("REPAIR-2 STEP 3 APPLIED (47/47 on 32 rows) AND THE CORPUS IS HARD GREEN for the first time since the "
                 "Q6 citation-sweep fix exposed the two wrong-verse runs: citation_sweep GREEN, triage 834 -> 815, no "
                 "hard member gained a flag."),
    "adjudication": {"attempt": "ezek_repair2_step3_adjudication_a1#e1", "model": "claude-fable-5-1",
                     "tokens_reported": 443997, "rows": 32, "fields": 47, "discharged": 55, "no_defect": 18,
                     "stop": 0, "facts_reproduced": "113 exact-key checks; 106 PASS; 7 test-literal artifacts cleared",
                     "verified_by_orchestrator": "digests matched; gate v3.1 re-run ALL_CLEAN; candidate hard GREEN",
                     "twelve_gate_defect_stops": "all decided on the merits under v3.1"},
    "apply": {"sweep": "repair2_step3_measured_false", "parity": "47/47",
              "by_field": {"boundary_rationale": 14, "device_notes": 9, "strongest_rejected_alternative": 9,
                           "boundary_evidence_refs": 13, "observed_substrate_signals": 2},
              "preimage": "9abd545f4854c45610fb66a4b047d668596ed5fb492b348e76216dc220d13614",
              "postimage": "199d81c08fbfeb311f51419f4032ab604b32465d5805a681a3908e00736ae8d3",
              "postcheck": "field-by-field; no row outside the proposal changed",
              "applier": "Ezek/repair2/apply_proposal.py (step-agnostic, generated set edits with expected-before values)"},
    "suite_after": {"file": "Ezek/repair2/step3/suite_delta_after_apply.json", "hard_status": "GREEN (was RED)",
                    "triage_flags": "834 -> 815", "verdict": "NO HARD MEMBER GAINED A FLAG"},
    "ROUTED_BY_THE_ADJUDICATOR_carried_forward_by_name": {
        "e16": ["P02-018 CONF-CAL question (S3-010; the grade stays medium per the ruling)",
                "P02-002 'sweep: 20 verses' transport figure - the same stale class as Q10-12 on a row the worklist missed",
                "P02-001 'visions of God' sweep claim at 1:1 (unprefixed, not transport)",
                "P01-006 mark-direction sentence on 3:16/3:17",
                "P03-019 signal closure.formula_final against the corrected prose"],
        "step_4": ["P02-018 refs[2] and refs[3] wording", "legacy token-less mirror entries on P08-012 and P08-004",
                   "P05-008 'byte-observed' against counted-class wording (step 4 or 5)"],
        "step_5": ["15 pre-existing register flags, including one on the HIGH row P02-020",
                   "6 pre-existing web_quotes case mismatches (step 5 or #e16)"],
        "second_fable_review": ["P05-002 22:22 - lane B's finding examined and rejected on the bytes; confirmation only"],
        "ruling_defect_for_e16": ("#e15 Q10's three truncated-quotation items (ruling line 270) carry lane 01's ROTATED "
                                  "row pairing - 41:22, 41:26 and 40:38 are not the verses of the rows named - and the "
                                  "step-3 worklist inherited it; lane A's ESC-3 found it and the adjudicator decided each "
                                  "row on what it actually quotes"),
        "disclosed_readings": "three edits rest on the adjudicator's disclosed readings (P06-001 refs[2], P10-014 refs[1], "
                              "P01-002 the 2:1 quotation); each can be struck alone",
    },
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
print("E13-104 appended; queue rows:", sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()))
