#!/usr/bin/env python3
"""Queue E13-105: REPAIR-2 step 4a (mechanical vocabulary) applied and step 4b (role-token member) installed."""
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
v = json.loads((EZ / "repair2" / "step4" / "mechanical_proposal_verdict.v1.json").read_text(encoding="utf-8"))
e = {
    "id": "E13-105", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "MEDIUM", "tier": "MEASURED",
    "blocks_close": False, "raised_by": "orchestrator (claude-opus-5)", "status": "DONE - step 4c (author batch) next",
    "headline": ("REPAIR-2 STEP 4a APPLIED (124 derived face qualifiers and 31 X2 re-faces on 98 rows, corpus still hard "
                 "GREEN) AND 4b INSTALLED THE CLAUSE-6-v2 ROLE-TOKEN MEMBER AS A HARD SUITE MEMBER - after a probe proved "
                 "the pinned suite unchanged by qualified tokens."),
    "step_4a": {
        "plans": {"face_qualification": "124 derivable on rows 199d81c0; decorrelated word-reader 95 corroborated, 0 contradicted; 3 zone entries and 2 interior-without-device entries routed to authors",
                  "x2_reface": "31 MT-borne device entries web: -> oshb: outside the zone, each with identity by web_to_mt and the device recorded on the MT verse; 2 routed (P09-008 39:12 and 39:14 name a device no census class records)"},
        "probe_before_write": "all qualifiers applied in memory: suite summary identical, no hard member moved, the only movement the same flags re-keyed; role-token member verified every qualifier",
        "verdict_before_write": v,
        "apply": {"sweep": "repair2_step4a_mechanical_vocabulary", "parity": "98/98",
                  "preimage": "199d81c08fbfeb311f51419f4032ab604b32465d5805a681a3908e00736ae8d3",
                  "postimage": "32f33f05e8adb185027b278813537b8b466f58a7a82eabad186e5ad72dcf398e"},
        "suite_after": "hard GREEN, triage 815, no hard member gained a flag"},
    "step_4b": {
        "member": "Ezek/tools/check_role_tokens.py - verifies :near/:far/:interior against verse and span for WARRANT-onset/close, the seam pair and side for WARRANT-rival, the clause 6 v2 vocabulary including WARRANT-absence and DISCLOSURE-absence with the deprecated alias; selftest 6 of 6 with six planted defects each flagged",
        "registered": "run_validator_suite.py registers role_tokens as a HARD member (status FLAGS or ERROR makes hard RED)",
        "phase": "pinned in tools/role_tokens_phase.json = pre (a present qualifier is verified; an unqualified warrant is counted, not flagged); an absent phase file means STRICT. Flip to post, with a receipt, when step 4 closes.",
        "brief_check": ("check_brief_vs_suite.py now DISCOVERS members from the runner's own '\"name\": run(' lines - its "
                        "old pattern matched none of them and silently fell back to the last report on disk, which could "
                        "never know a newly installed member - and maps role_tokens to its duty"),
        "suite_on_live_rows_with_member": "hard GREEN, triage 815, role_tokens GREEN (pre phase)",
        "backups": ["Ezek/repair2/step4/run_validator_suite.py.pre_4c0caa08a299",
                    "Ezek/repair2/step4/check_brief_vs_suite.py.pre_0d1a7befd01a"]},
    "an_expectation_of_mine_that_was_wrong": ("I expected the step-3 author brief to FAIL the brief check once the member "
                                               "was discoverable; it PASSES, because it says 'NO face qualifier (step 4 "
                                               "installs those)' - which is exactly the right duty for step 3. The phrase "
                                               "test matched a prohibition, and here the prohibition is the duty."),
    "remaining_for_step_4c": "80 unqualified warrants (mostly WARRANT-rival needing seam pairs), the zone and interior routings, the ANCHOR absences at 40:38 and 41:9 (x2), and every step-4 item carried by the step-2 and step-3 adjudications and #e15's per-row repairs",
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
print("E13-105 appended; queue rows:", sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()))
