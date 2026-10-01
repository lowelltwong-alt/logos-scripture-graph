#!/usr/bin/env python3
"""Append ledger E-40, the E-35 and E-38 addenda, and learning-log L-0060..L-0063 (append-only, idempotent, prefix-checked).

The caller runs SP/campaign/_inflight_pin_guard.py on the three targets first.
"""
import json
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
LJ, LM, LL = M8 / "error_pattern_ledger.v1.jsonl", M8 / "ERROR_PATTERN_LEDGER.v1.md", M8 / "orchestration_learning_log.v1.jsonl"
D = "2026-09-16"

ledger = [
    {"id": "E-40", "kind": "error_pattern", "date": D, "severity": "high",
     "headline": "a ruling that bars what an earlier brief sanctions leaves the brief pinned and contrary",
     "instance": ("AUTHOR_WAVE_BRIEF.v1.md section 13.2 told authors to write 'the section-mark record', 'the verse census', "
                  "'the device census' and 'the division plan' in place of file names. #e15 Q9(a) later BARRED exactly those "
                  "referents ('never names a record, census, plan, inventory, worklist, digest or key'). The brief was never "
                  "re-versioned and stays a pinned input of later steps as the source of rule substance, so a step-5 lane "
                  "reading both would find two instructions and the older one is the more specific. Found by the "
                  "orchestrator while building the step-5 brief, before any launch."),
     "cure": ("(1) A ruling's landing lists every pinned brief whose instruction it contradicts, by section. (2) Any later "
              "brief that pins the older one states the supersession verbatim - the step-5 brief does. (3) The brief-versus-"
              "suite check gains a superseded-phrase arm the next time a brief is re-versioned.")},
    {"id": "E-35", "kind": "error_pattern_addendum", "date": D,
     "instance": ("'the eight held items - peer_03's four sweep findings and peer_10's four transport rows' is carried by #e13, "
                  "the author brief, E13-68 and #e15, and no record lists the eight by id. The step-6 builder reconstructs "
                  "them from the peers' own words (peer_10 names P10-004, P10-006, P10-011, P10-012 with verses; peer_03 names "
                  "memberships 13:14, 13:21, 13:23, 14:8, 15:7, mapped to four rows by span) and refuses unless both counts "
                  "come to four."),
     "the_lesson_added": "a count carried as the identity of a set is E-35 in a new form: a hold, release or routing names its members by id at the moment it is written."},
    {"id": "E-38", "kind": "error_pattern_addendum", "date": D,
     "instance": ("the first draft of the CONF-CAL audit member v2 read 'no census signal on a face' as 'no licensed signal': "
                  "83 seams had no near-face signal and 55 grades read as above their evidence. Sampling eight rows before "
                  "use showed the census cannot see refrains outside its counted classes, discourse turns, scene changes or "
                  "'he said to me', and that a strict verse-final test cannot apply #e14 Q2's refinement. The member now "
                  "derives a RANGE of limbs per seam and names the basis of every disagreement ('census absence on the near "
                  "face 2:7')."),
     "the_lesson_added": "a census cannot see what it does not count: an audit derived from one reports an absence as a question with its basis, never as a finding."},
]
md = """
## E-40 - a ruling that bars what an earlier brief sanctions leaves the brief pinned and contrary

**Instance.** AUTHOR_WAVE_BRIEF.v1.md section 13.2 told authors to write "the section-mark record", "the verse census", "the device census" and "the division plan" in place of file names. #e15 Q9(a) later barred exactly those referents. The brief was never re-versioned and stays a pinned input of later steps as the source of rule substance, so a lane reading both finds two instructions and the older one is the more specific. Found by the orchestrator while building the step-5 brief, before any launch.

**Cure.** (1) A ruling's landing lists every pinned brief whose instruction it contradicts, by section. (2) Any later brief that pins the older one states the supersession verbatim - the step-5 brief does. (3) The brief-versus-suite check gains a superseded-phrase arm the next time a brief is re-versioned.

## E-35 addendum - a count carried as the identity of a set

"The eight held items" is carried by #e13, the author brief, E13-68 and #e15, and no record lists the eight by id. The step-6 builder reconstructs them from the peers' own words and refuses unless both counts come to four. A hold, release or routing names its members by id at the moment it is written.

## E-38 addendum - a census cannot see what it does not count

The first draft of the CONF-CAL audit member v2 read "no census signal on a face" as "no licensed signal": 83 seams had no near-face signal and 55 grades read as above their evidence. Sampling eight rows before use showed the census cannot see refrains outside its counted classes, discourse turns, scene changes or "he said to me", and that a strict verse-final test cannot apply #e14 Q2's refinement. The member now derives a range of limbs per seam and names the basis of every disagreement. An audit derived from a census reports an absence as a question with its basis, never as a finding.
"""
learning = [
    {"id": "L-0060", "stage": "adjudication", "element": "brief_design",
     "observation": ("Two blind lanes split 17 items on a class question (forward-merge rivals): one applied a convention it "
                     "labelled INFERRED, one stopped. The adjudication brief stated the divergence without a preference and "
                     "let the adjudicator decide only if the clause as written decides; it routed the class to #e16 with both "
                     "readings rather than adopting either convention."),
     "recommendation": "When lanes split on what a rule means rather than on what the text says, give the adjudicator an explicit routing path and forbid inventing the rule.",
     "verdict": "ADOPTED", "metric": "17 routed items, 0 invented conventions written", "evidence_refs": ["E13-106"]},
    {"id": "L-0061", "stage": "apply", "element": "control",
     "observation": "Before applying the step-4c proposal the digest of the gate's candidate rows file was compared with the harness's planned post-image; they were identical (2d7160f7).",
     "recommendation": "Make gate-candidate / harness-plan digest parity a standard pre-apply check: it proves the rows that were checked are the rows that get written.",
     "verdict": "ADOPTED", "metric": "1 of 1 parity match", "evidence_refs": ["E13-106"]},
    {"id": "L-0062", "stage": "orchestration", "element": "idle_time",
     "observation": ("While an adjudication ran, the next three steps' builders, gate and briefs were written and run in probe "
                     "mode with the brief-versus-suite check. The probes caught a web_quotes row-mapping miss, a peer membership "
                     "parse miss, a stale-count pattern with 8 of 10 false hits, five and then one missing duty phrases, and a "
                     "census-absence design error - all before any launch."),
     "recommendation": "Build and probe the next step's tooling during every agent wait; a probe build writes only to scratch and cannot be launched from.",
     "verdict": "ADOPTED", "metric": "7 defects caught pre-launch, 0 reached a lane", "evidence_refs": ["E13-106", "E-40", "E-38 addendum"]},
    {"id": "L-0063", "stage": "checkpoint", "element": "carrier_wording",
     "observation": "The safe-to-clear checker's repairs_done arm refused 'REPAIR-2 step 4c is LANDED' (a repair word and a completion word within 50 characters); the checkpoint tool restored the prior prompt as designed.",
     "recommendation": "Carrier wording for REPAIR-2 progress: 'the REPAIR-2 sequence stands at step N, with step X recorded in its receipts'.",
     "verdict": "ADOPTED", "metric": "2 refusals this session, 0 stale prompts left", "evidence_refs": ["E-37"]},
]
jl = LJ.read_bytes()
existing = [json.loads(l) for l in jl.decode("utf-8").splitlines() if l.strip()]
if any(e.get("id") == "E-40" for e in existing):
    raise SystemExit("REFUSED: E-40 already recorded")
ll = LL.read_bytes()
if any(json.loads(l).get("id") == "L-0060" for l in ll.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: L-0060 already recorded")
mb = LM.read_bytes()
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    for e in ledger:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(md)
with LL.open("a", encoding="utf-8", newline="\n") as fh:
    for e in learning:
        fh.write(json.dumps(dict({"schema": "m8_orchestration_learning.v1", "date": D, "book": "Ezek"}, **e, supersedes=None),
                            ensure_ascii=False) + "\n")
assert LJ.read_bytes().startswith(jl) and LM.read_bytes().startswith(mb) and LL.read_bytes().startswith(ll)
print("ledger rows:", sum(1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip()),
      "| learning rows:", sum(1 for l in LL.read_text(encoding="utf-8").splitlines() if l.strip()))
