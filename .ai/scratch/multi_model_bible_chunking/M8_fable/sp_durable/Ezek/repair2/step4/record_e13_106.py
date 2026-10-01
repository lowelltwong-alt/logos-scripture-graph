#!/usr/bin/env python3
"""Queue E13-106: REPAIR-2 step 4c landed; the forward-merge rival class routed to #e16; steps 5-7 prepared by probe.

Refuses if E13-106 already exists (a rerun must not append twice) and asserts the queue grew by exactly one line.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
before = Q.read_bytes()
if any(json.loads(l).get("id") == "E13-106" for l in before.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E13-106 already recorded")
adj = json.loads((EZ / "author" / "repair2_step4c" / "adjudication" / "adjudication.json").read_text(encoding="utf-8"))
delta = json.loads((EZ / "repair2" / "step4" / "suite_delta_after_4c.json").read_text(encoding="utf-8"))
rows_sha = sha(EZ / "repair" / "rows_v7_cwo24.jsonl")
if rows_sha != "2d7160f7d838d1c111791b6dc2e35b457d7899e4641a43371b1de99bd8eae422":
    raise SystemExit("REFUSED: rows are not at the step-4c post-image")
e = {
    "id": "E13-106", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
    "status": "DONE for step 4c; OPEN for #e16 (the forward-merge rival class keeps the role_tokens member in PRE phase)",
    "headline": ("REPAIR-2 STEP 4c LANDED: two blind Opus lanes and a Fable adjudication, 54 refs edits on 54 rows, rows "
                 "32f33f05 -> 2d7160f7, hard GREEN, triage 815 -> 810, no hard member gained a flag. SEVENTEEN rival "
                 "warrants stay unqualified BY DECISION: the adjudicator held that clause 6 v2 as written does not decide "
                 "a forward-merge rival's face and routed the class to #e16 with both readings. The role_tokens member "
                 "therefore stays in PRE phase; flipping it to POST now would turn a routed class question into a red suite."),
    "lanes": {"A": "101 discharged, 2 no-defect, 0 stops; qualified the forward merges on an INFERRED dissolved-seam convention",
              "B": "84 discharged, 19 stops; held the clause gives a forward merge no truthful face and named three class options"},
    "adjudication": {"file": "Ezek/author/repair2_step4c/adjudication/adjudication.json",
                     "sha256": sha(EZ / "author" / "repair2_step4c" / "adjudication" / "adjudication.json"),
                     "tally": adj.get("tally"), "forward_merge_class": adj.get("forward_merge_class"),
                     "class_decision": adj.get("class_decision"), "routed": adj.get("routed")},
    "orchestrator_checks": [
        "deliverable digests match the adjudicator's report",
        "gate v4 re-run by the orchestrator on the adjudicated proposal: ALL_CLEAN, hard GREEN, 17 unqualified, 0 defects",
        "the 17 unqualified warrants sit on exactly the 16 rows of the 18 STOP items (set equality)",
        "the gate's candidate rows file is byte-identical to the harness's planned post-image (2d7160f7...)",
        "apply: 54/54 parity, protected fields unchanged, no row outside the proposal changed",
        "full suite on the live rows: hard GREEN; suite delta against the step-3 baseline: %s" % delta.get("verdict"),
    ],
    "role_tokens_phase": "stays 'pre' (Ezek/tools/role_tokens_phase.json unchanged); flip to 'post' only when #e16 has ruled the forward-merge class and every warrant is qualified",
    "prepared_while_the_adjudication_ran": {
        "step_5": ("Ezek/repair2/step5/: build_step5_worklist.py (six sources, each from its record: register flags, the "
                   "orchestrator's own register/residue/grammar sweep fields by backup diff, spot findings, routed entries, "
                   "near/far observations, web_quotes flags), check_candidate_v5.py (claim accounting, English-form floor with "
                   "E13-86 fixtures - three of five caught, two disclosed as reading-only - completion measure; selftest 12/12; "
                   "end-to-end probe on an empty proposal clean), build_step5_brief.py (two halves, two blind lanes each; rule "
                   "substance extracted verbatim; brief-versus-suite PASS on both halves in probe)"),
        "step_6": ("Ezek/repair2/step6/: build_step6_worklist.py (distinct checks: transport 33/33 and recognition 64/64, 21/21, "
                   "2/2 by census list against an independent predicate scan of the witness; the ruling's counts reproduced - "
                   "4+4 released, 7 weighings plus 37:2 carried to disclosure, 5 onsets), build_step6_brief.py (PASS in probe)"),
        "step_7": ("Ezek/repair2/step7/build_step7_slices.py: every row REPAIR-2 touched, measured from sweep receipts and "
                   "backups, three lanes by stride, orders as data; probe on 2026-09-16 rows found 105 touched rows before 4c"),
    },
    "findings_while_preparing": [
        ("THE EIGHT HELD ITEMS WERE NEVER LISTED BY ID in any record - #e13, the author brief, E13-68 and #e15 all say 'peer_03's "
         "four sweep findings and peer_10's four transport rows'. The step-6 builder identifies them from the peers' own words "
         "(peer_10: P10-004 at 40:24, P10-006 at 40:48, P10-011 at 42:15, P10-012 at 43:1; peer_03: memberships 13:14, 13:21, "
         "13:23, 14:8, 15:7 mapped by span to four rows) and refuses if either count is not four. Same class as E-38: a count "
         "carried without its members."),
        ("AUTHOR_WAVE_BRIEF.v1.md section 13.2 SANCTIONS 'the section-mark record', 'the verse census', 'the device census' and "
         "'the division plan' as replacements for file names; #e15 Q9(a) BARS exactly those. The step-5 brief states the "
         "supersession explicitly, because a lane reading both pinned inputs would otherwise follow the older one."),
        ("The CONF-CAL audit sweep #e15 ordered exists only as a v1 in the session archive (repair2/session_910cbe15/ezek_r2/), "
         "which states it cannot be a usable audit until face qualifiers exist; a v2 deriving faces from the census, the marks and "
         "the verse-final test, as #e15 Q2's order describes, is owed before step 7 and #e16."),
        ("A first step-6 probe keyed a stale '20' transport figure on any '20' near 'transport' and returned 10 hits, 8 of them "
         "verse numbers (40:20, 46.19-20); the pattern now requires a COUNT phrase. The two real stale claims are P02-002 and "
         "P11-010."),
    ],
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
after = Q.read_bytes()
assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
print("E13-106 appended; queue rows:", sum(1 for l in after.decode("utf-8").splitlines() if l.strip()))
