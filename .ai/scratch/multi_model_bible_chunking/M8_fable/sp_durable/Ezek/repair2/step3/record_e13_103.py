#!/usr/bin/env python3
"""Queue E13-103: both step-3 lanes landed; two gate-v3 defects both lanes hit; gate v3.1; adjudication launched."""
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
e = {
    "id": "E13-103", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": False, "raised_by": "orchestrator (claude-opus-5)", "status": "adjudication IN FLIGHT",
    "headline": ("BOTH STEP-3 LANES LANDED AND BOTH TAKE THE CORPUS FROM HARD RED TO HARD GREEN ON THEIR CANDIDATES - and "
                 "BOTH independently hit the same contradiction in my gate v3, which could never pass three rows. Gate "
                 "v3.1 corrects it and a second defect lane A found; the Fable adjudication runs under v3.1."),
    "lanes": {
        "A": {"tokens_reported": 547300, "rows_proposed": 21, "discharged": 42, "no_defect": 16, "stop": 15,
              "orchestrator_gate_rerun": "ALL_CLEAN; hard GREEN; cleared citation_sweep 2, register 15, web_quotes 2"},
        "B": {"tokens_reported": 523870, "rows_proposed": 24, "discharged": 42, "no_defect": 18, "stop": 13,
              "orchestrator_gate_rerun": "ALL_CLEAN; hard GREEN; cleared citation_sweep 2, register 26, web_quotes 2"},
        "receipts": "Ezek/author/repair2_step3/ezek_repair2_step3_attempt_receipts.jsonl"},
    "gate_v3_defects_found_by_the_lanes": [
        {"what": ("TWO RULES THAT COULD NOT BOTH BE MET: v3 refused edits to fields no owed item named, yet marked a row "
                  "unclean for register flags ANYWHERE in it; P02-003, P08-013 and P09-002 carry pre-existing flags in "
                  "untouched fields and could never be clean"),
         "found_by": "BOTH lanes independently - A stopped eight items (ESC-1); B left the rows out and escalated",
         "shape": "E-34 in the orchestrator's own gate, the same day the E-34 subset addendum was recorded"},
        {"what": ("ADVISORY HINTS MADE BINDING: v3 took each worklist item's field list - the orchestrator's guesses - as "
                  "hard scope, and four claims sit in a field the list did not name"),
         "found_by": "lane A (ESC-2: S3-009, S3-010, S3-014, S3-016)"},
    ],
    "gate_v3_1": {"file": "Ezek/repair2/step3/check_candidate_v3_1.py",
                  "changes": ["per-row flags judged as a DELTA against the live row - only introduced flags count",
                              "scope by ROW; observed_substrate_signals only where an item names it; hints advisory"],
                  "selftest": "6 of 6, including the exact contradiction both lanes hit as a case that must now pass",
                  "probe": "run end to end on lane B's real proposal: ALL_CLEAN, hard GREEN, v3.1's delta output shape"},
    "other_lane_escalations_routed_to_the_adjudicator": [
        "lane A ESC-3: S3-024 names 41:26 on P10-005 and S3-025 names 40:38 on P01-002 - verses outside the row",
        "lane A ESC-4: S3-010 would leave a medium sentence without a ground; S3-029 needs step-5 register work in a HIGH row"],
    "adjudication_launch": {"attempt": "ezek_repair2_step3_adjudication_a1#e1", "model": "claude-fable-5-1",
                            "brief": "Ezek/repair2/step3/STEP3_ADJUDICATION_BRIEF.md (f2ba8ddd...)",
                            "controls": "brief-versus-suite PASS (after a failed first check on a missing register-rule "
                                        "phrase), pin check MATCH, validator pass, budget test, mapped at launch"},
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
print("E13-103 appended; queue rows:", sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()))
