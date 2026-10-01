#!/usr/bin/env python3
"""Queue E13-102 (REPAIR-2 step 2 applied) and ledger E-39 plus an E-34 addendum."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
pos = json.loads((EZ / "ezek_ow15_position.v2.json").read_text(encoding="utf-8"))

q = {
    "id": "E13-102", "opened_at": NOW, "severity": "HIGH", "tier": "MEASURED", "blocks_close": False,
    "headline": ("REPAIR-2 STEP 2 IS APPLIED (39/39, then a 1/1 follow-up), the step-1 obligation is CLOSED, and the "
                 "pinned suite shows no hard member gained a flag. On the way: the in-flight pin guard had been reading "
                 "the rows file PINNED since 2026-09-15 because four watchdog-failed executions had no receipts, and "
                 "my step-2 gate missed a citation-sweep duty because it ran two suite members, not the suite."),
    "raised_by": "orchestrator (claude-opus-5)", "status": "DONE - step 3 next",
    "adjudication": {"attempt": "ezek_repair2_step2_adjudication_a1#e1", "model": "claude-fable-5-1",
                     "tokens_reported": 563321, "rows": 16, "base_A": 1, "base_B": 13, "merged": 2,
                     "refs_entries_added": 14, "orders_discharged": 95, "stops": 1, "carried_to_later_steps": 8,
                     "routed_to_e16": ["P03-015 rejected-alternative verdict under the ch-18 class ruling",
                                       "P03-019 close sentence - does the class ruling's mark-never-decides reach it",
                                       "P09-011 (the la-khen-turn class, already routed)",
                                       "P04-008 onset far face - MT 21:12's verse-final utterance named beside the pe"],
                     "the_stop": "P03-014: the boss audit's 'better ground for high' - the measurement is sound, the ground is unavailable under the class ruling",
                     "p02_008_mark_flag": "a member false positive: no Ezek.10.* key in the marks record; the 11:1 PE now named beside the absence",
                     "verified_by_the_orchestrator": "digests match the report; gate v2 re-run ALL_CLEAN on 16 rows; 95/1 reproduced"},
    "apply": {"sweep": "repair2_step2_grounds", "parity": "39/39", "set": 25, "append_ref": 14,
              "preimage": "1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425",
              "postimage": "5a8faee0511567e5926c91748d72a10b90f4910fa43e79081beccc2cbaea084b",
              "postcheck": "every proposed field equals the post-image; no row outside the proposal changed"},
    "followup": {"sweep": "repair2_step2_followup", "parity": "1/1",
                 "what": ("P04-008's appended entry mentioned the pe without the literal single-witness disclosure the "
                          "citation sweep requires; the annotation gained the words and kept its meaning"),
                 "postimage": "9abd545f4854c45610fb66a4b047d668596ed5fb492b348e76216dc220d13614"},
    "suite_after": {"file": "Ezek/repair2/step2_reconciliation/suite_delta_after_followup.json",
                    "verdict": "NO HARD MEMBER GAINED A FLAG", "register": "116 -> 105", "web_quotes": "40 -> 39",
                    "refs_mirror": "GREEN", "citation_sweep": "RED at the baseline's two wrong-verse problems (step 3)",
                    "universals": "+38 -17 (triage)"},
    "the_guard_that_could_never_clear": {
        "what": ("the in-flight pin guard treats an execution the transcript map names but no receipt records as IN "
                 "FLIGHT. Four primary executions (LF c21, LF c22, OL c20, OL c21 #e1) failed on the runtime watchdog at "
                 "2026-09-15 23:02:50Z; #e2 landed each attempt, but #e1 never received a receipt, so the guard has read "
                 "the rows file PINNED ever since."),
        "consequence": ("every rows mutation since then - the author wave, the remediation batch, REPAIR-2 step 1 - was "
                        "applied WITHOUT running the guard; had it been run it would have refused on dead executions. No "
                        "harm came of it, because those executions were dead, but a control that can only refuse is a "
                        "control that gets skipped."),
        "fix": "four receipts, outcome FAILED_BY_RUNTIME_WATCHDOG, superseded_by #e2, tokens UNAVAILABLE; the guard now reads CLEAR with nothing in flight",
    },
    "the_gate_that_ran_two_members": ("check_candidate_v2 ran the register and mirroring members; the adjudicator iterated "
                                      "to ALL_CLEAN and the full suite then found a citation-sweep disclosure duty the gate "
                                      "could not see. Every later author or adjudicator gate runs the WHOLE pinned suite on "
                                      "the candidate rows (repair2/suite_delta.py) as well as the per-row checks."),
    "census": {"file": "Ezek/ezek_ow15_position.v2.json", "LOWER_BOUND": pos["census"]["LOWER_BOUND"],
               "ceiling": pos["ceiling"]["value"], "headroom_UPPER_BOUND": pos["headroom"]["UPPER_BOUND"]},
}
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(q, ensure_ascii=False) + "\n")

LJ, LM = M8 / "error_pattern_ledger.v1.jsonl", M8 / "ERROR_PATTERN_LEDGER.v1.md"
e39 = {"id": "E-39", "kind": "error_pattern", "date": "2026-09-16", "severity": "high",
       "headline": "a failed execution with no receipt looks in flight forever, so the in-flight guard can only refuse - and a control that can only refuse gets skipped",
       "instance": q["the_guard_that_could_never_clear"]["what"] + " " + q["the_guard_that_could_never_clear"]["consequence"],
       "cure": ["write the receipt for EVERY execution at the moment it ends - including a watchdog failure - never only for the execution that lands",
                "a relaunch under the E-14 ladder records the prior execution's outcome in the same step that records the new launch",
                "when a guard refuses, read what it names before doing anything else; a refusal that names a dead execution is a capture defect, not a reason to skip the guard"],
       "tier": "MEASURED - the map, the receipts, the failure notifications and the guard's own output were read",
       "provenance": {"book": "Ezek", "queue": "E13-102", "found_at": NOW}}
e34 = {"id": "E-34", "kind": "error_pattern_addendum", "date": "2026-09-16",
       "instance": q["the_gate_that_ran_two_members"],
       "the_lesson_added": "a gate built as a SUBSET of the suite repeats E-34 one level down: the agent is faithful to the gate and the suite still fails. Hand agents the whole suite."}
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    for r in (e39, e34):
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join([
        "", "## E-39 - a failed execution with no receipt makes the in-flight guard refuse forever", "",
        e39["instance"], "",
        "**Cure.** A receipt for every execution the moment it ends, watchdog failures included; a relaunch records the "
        "prior execution's outcome in the same step; and a guard's refusal is read before anything else - a refusal that "
        "names a dead execution is a capture defect, never a reason to skip the guard.", "",
        "## E-34 addendum - a gate that runs a subset of the suite", "",
        e34["instance"] + " " + e34["the_lesson_added"], ""]))
print(json.dumps({"queue": "E13-102", "ledger": ["E-39", "E-34 addendum"],
                  "queue_rows": sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()),
                  "ledger_rows": sum(1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip())}, indent=1))
