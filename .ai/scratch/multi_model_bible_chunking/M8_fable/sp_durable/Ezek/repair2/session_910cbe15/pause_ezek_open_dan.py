#!/usr/bin/env python3
"""OW-20: pause Ezekiel at REPAIR-2 step 2, preserve every in-flight artifact durably, and record the owner's
decision to open Daniel's Phase 0 - in every carrier the session-close law names - so a CLEARED session resumes
from disk alone. The in-flight pin guard returned CLEAR on every target before this ran.

Order of writes: (1) durable tool copy with manifest, (2) Ezekiel pause handoff, (3) queue entry, (4) ledger MD
and JSONL, (5) close-gate addendum, (6) CYCLE_STATE entry carrying the new CURSOR - last, because the state index
builder reads the cursor and everything the cursor points to must already exist.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc).isoformat()
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
SCR = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
CURSOR = "ezek_paused_repair2_step2_lanes_held_daniel_phase0_opened_ow20"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
ROWS_SHA = "1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425"
if sha(ROWS) != ROWS_SHA:
    raise SystemExit("REFUSED: the rows moved; the handoff would describe a state that is not on disk")

OWNER_WORDS = [
    "what next daniel? companc or clear reprompt?",
    "give me a goal prompt to get you everything you need to start daniel  and give em the instructions to "
    "commpact or clear reporomt with the prompt to actually start daniel becasue its ready for daniel",
]

# ---------------------------------------------------------------- (1) durable tool copy
DST = EZ / "repair2" / "session_910cbe15"
manifest = {}
for sub in ("ezek_aw", "ezek_r2", "ezek_step2"):
    src = SCR / sub
    for f in sorted(src.rglob("*")):
        if not f.is_file() or "suite_runs" in f.parts or "__pycache__" in f.parts:
            continue
        rel = f.relative_to(SCR)
        out = DST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, out)
        if sha(out) != sha(f):
            raise SystemExit("REFUSED: durable copy mismatch at %s" % rel)
        manifest[str(rel).replace("\\", "/")] = sha(f)
shutil.copyfile(SCR / "pause_ezek_open_dan.py", DST / "pause_ezek_open_dan.py")
manifest["pause_ezek_open_dan.py"] = sha(DST / "pause_ezek_open_dan.py")
(DST / "MANIFEST.json").write_text(json.dumps({
    "what": "every script, plan, brief, slice and lane file REPAIR-2 used in session 910cbe15, copied from the "
            "session scratchpad (which a cleared session cannot find) with per-file sha256; suite_runs excluded "
            "because they are regenerated from the rows",
    "copied_at": NOW, "files": len(manifest), "sha256": manifest}, indent=1), encoding="utf-8", newline="\n")

# ---------------------------------------------------------------- (2) Ezekiel pause handoff
L = []
a = L.append
a("# EZEKIEL - PAUSED AT REPAIR-2 STEP 2 (owner decision OW-20, 2026-09-16)")
a("")
a("**Ezekiel is PAUSED, not CLOSED.** The owner opened Daniel's Phase 0 with Ezekiel mid-REPAIR-2. Every close-gate")
a("item remains owed. OW-11's authority covers Ezekiel and Daniel only and EXPIRES AT DANIEL'S CLOSE, so Ezekiel")
a("must be resumed and closed before Daniel's close gate. This file is the resume point; the queue")
a("(ezek_controlling_agent_queue_e13.v1.jsonl, E13-01..E13-99) is the itemized record behind it.")
a("")
a("## Exact state on disk")
a("")
a("- rows: `repair/rows_v7_cwo24.jsonl` sha256 `%s` (pre-wave `25cdba56...` -> after wave and remediation" % ROWS_SHA)
a("  `64d9eff0...` -> after REPAIR-2 step 1 `1238eb24...`). Per-sweep preimage backups sit beside it as `.pre_<digest12>`.")
a("- controlling ruling in force: `ezek_controlling_agent_ruling_e15.v1.json` sha256 `%s`." % sha(EZ / "ezek_controlling_agent_ruling_e15.v1.json"))
a("  Its `repair2_batch_composition_and_sequence` is the work order for everything below.")
a("- budget: OW-15 position `ezek_ow15_position.v1.json` - census LOWER BOUND 39,426,659 of the 55,000,000 ceiling")
a("  (read from `sp_durable/campaign/budget_ceilings.v1.json`), plus the two step-2 lanes (293,322 + 345,317) not yet in")
a("  that snapshot. Re-run the census tool before any launch.")
a("- tools and plans used this session: `repair2/session_910cbe15/` with `MANIFEST.json` (per-file sha256).")
a("")
a("## REPAIR-2 progress")
a("")
a("| step | state | record |")
a("|---|---|---|")
a("| 0 baselines | DONE | E13-93 |")
a("| 1 nine grade moves | DONE, 9/9 parity; the ruling's count base was wrong (27 stated, 22 measured) - E-35 | E13-94 |")
a("| 2 grounds (16 rows) | IN PROGRESS: two blind lanes DELIVERED and RECEIPTED, NOT reconciled, NOT applied | E13-98, E13-99 |")
a("| 3 measured-false anywhere | NOT STARTED | #e15 Q10 |")
a("| 4 vocabulary | mechanical face arm BUILT and distinct-checked (111 derivable, 88 corroborated, 0 contradicted), NOT applied | E13-96 |")
a("| 5 register prose pass | NOT STARTED | #e15 Q9 |")
a("| 6 transport items + A16 weighings | NOT STARTED | #e15 |")
a("| 7 full suite + spot re-read at full coverage with ORDERS in slices | NOT STARTED | #e15 Q1 |")
a("")
a("**Open obligation that blocks close:** the nine step-1 rows carry a grade their prose does not yet state until step 2 lands.")
a("")
a("## Step 2 - the reconciliation docket, exactly as it stands")
a("")
a("Deliverables (durable): `author/repair2_step2/lane_a/` and `lane_b/` (proposal.json + discharge.json), receipts in")
a("`author/repair2_step2/ezek_repair2_step2_attempt_receipts.jsonl`. Lane A: 109 discharged / 41 stops / 7 disagreements.")
a("Lane B: 223 discharged / 0 stops / 28 disagreements.")
a("")
a("1. **The step-2 gate's mirror arm was INERT.** `check_candidate.py` read a `mirrored` key that `check_refs_mirror.analyze_row`")
a("   never sets; the member's `items` list IS the unmirrored argued citations. Fix: any `items` entry makes the row unclean;")
a("   add a positive fixture (lane B's P08-002 at 33:21 must fail). Lane B found it. ALL_CLEAN from both lanes certifies")
a("   the register arms only.")
a("2. **The lanes answered the broken gate in opposite ways.** Lane A wrote ordered verses by POSITION to avoid an A4 failure")
a("   it expected; lane B named 13 uncovered argued citations on purpose (33:21, 39:28, 33:1, WEB 21:7, 21:18, 18:9, 18:21,")
a("   18:24, 18:27, 19:1, 37:13, 39:20, 10:22). The A4 duty is real. Cure at reconciliation: name the verses by number and")
a("   install matching refs entries in the SAME batch, each already carrying its ROLE token and face qualifier (this does not")
a("   collide with step 4, whose mechanical arm touches only wave-installed WARRANT-onset/close tokens).")
a("3. **Refs now contradict corrected prose** (lane B): P03-014 (18:3 'mid-verse'), P03-017 (the samekh decides the close),")
a("   P09-001 ('mark-only' at 37:10 and 37:12), P09-010 ('-plus-mark' at 39:20; the false 39:23 device entry #e15 Q4 ordered OUT).")
a("4. **Calls for the orchestrator/#e16:** P03-015's 18:9 verse-final ground under the ch-18 class ruling; P09-001's holding")
a("   sentence; P09-009 edit beyond its list; P04-008 residual 'without a competing onset'; P03-019 'mark helps decide the close'")
a("   (does the ch-18 CLASS ruling reach it? lane A read no); lane A's claim that a dotted '39.20' is invisible to the mirror")
a("   member (lane B's prose shows 39:20 read as AT_SEAM - verify the context difference).")
a("5. **Suite, item by item (`suite_candidates.py`, run with PYTHONUTF8=1):** lane A - register 116->105, web_quotes 40->39,")
a("   citation_sweep / mark_symmetry / language_zones / cap_sweep unchanged; ngram7 worst reuse now lane A's own 'is the shape")
a("   this row's medium' in 9 rows against a gate of 10 - vary it. Lane B's suite run NOT yet done. Baseline hard_status RED")
a("   (citation_sweep's two wrong-verse runs, P08-011 and P10-008, surfaced by the Q6 fix - step 3 items).")
a("6. **`reconcile.py`** (claims-level, selftest-gated): one selftest fixture fails because of MY fixture design (the Qere case")
a("   adds device words to one lane only, so DIVERGENT is correct) - fix the fixture to use the Qere row on both lanes.")
a("   Labelled Qere forms are exempt from verse-text collation (boss audit, A1); inherited runs are corpus findings, not lane conflicts.")
a("7. Apply only through `ezek_aw/guarded_apply.py` from preimage `1238eb24...`, simulate first, digest after the final write.")
a("")
a("## For #e16 (assembled, not launched)")
a("")
a("- E13-94 / E-35: #e13's `high_rows_after: 27` contradicts its own list (23); #e15 inherited it. Truth: 22 before step 1, 18 after.")
a("- E13-97: the la-khen-turn messenger class (17:19, 20:30, 39:25) - limb (b) MEASURED to fail at all three; all three are their")
a("  row's FIRST verse, so an unlicensed turn puts three SHIPPED SEAMS in question -> OW-6b(b) second Fable review.")
a("  Table: `ezek_lakhen_onset_class.v1.json` (positive controls agree with four ruling measurements).")
a("- The CONF-CAL audit list becomes readable only after step 4 installs face qualifiers (#e15 Q2/Q5).")
a("- Open queue items still addressed to the controlling agent: E13-67, E13-68, E13-70, E13-84, E13-85, E13-89, E13-90, E13-91.")
a("")
a("## After REPAIR-2")
a("")
a("#e16 ruling round; the OW-6b(b) second Fable review of the §7 regions (ch-18 tiling, 16:44-50 vs 16:44-58, 37:1-14 rival,")
a("and the three la-khen seams if #e16 rules the turn unlicensed); the OW-17 scholar-record Fable audit; OW-15 restated;")
a("close gate items 1-25; completion receipt; OW-12 status update. Owner questions still open: the decorrelated third lens")
a("(OW-6 escalation), the persistent carrier-map control (BOSS-ESC-1), the Greek NT witness (gates 27 of 42 remaining books).")
a("")
a("## Controls this session did NOT run, disclosed")
a("")
a("- `_brief_pin_check.py` was not run before the two step-2 lane launches, and the OW-11 authority paragraph was not in those")
a("  launch messages (OW-11-h, OW-11-l (p)).")
a("- `_inflight_pin_guard.py` was not run before several earlier record appends this session; it WAS run, CLEAR on all")
a("  seven targets, before the writes that paused Ezekiel.")
a("- The resume carriers (this CYCLE_STATE's cursor, CURRENT_STATE.v1.json, RESUME_PROMPT_CURRENT.md) were left stale from")
a("  the c12 primaries cursor through every later phase; `_safe_to_clear_check.py` refused on it. Recorded as E-37.")
HANDOFF = EZ / "EZEK_PAUSE_HANDOFF_REPAIR2.v1.md"
HANDOFF.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")

# ---------------------------------------------------------------- (3) queue entry
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
q = {
    "id": "E13-99", "opened_at": NOW, "severity": "HIGH",
    "headline": ("LANE B IS IN AND FOUND MY STEP-2 GATE'S MIRROR ARM INERT; E13-98's account of the gate is CORRECTED; "
                 "and by OWNER DECISION OW-20 Ezekiel is PAUSED at REPAIR-2 step 2 and Daniel's Phase 0 opens."),
    "raised_by": "orchestrator (claude-opus-5)", "status": "PAUSED - resume from EZEK_PAUSE_HANDOFF_REPAIR2.v1.md",
    "blocks_close": True, "tier": "MEASURED",
    "correction_to_E13_98": (
        "E13-98 said the gate's mirror arm 'fails a row whose prose argues a verse with no refs entry'. It did not: "
        "check_candidate.py filtered on a 'mirrored' key that check_refs_mirror.analyze_row never sets, so "
        "x.get('mirrored', True) was always true and the arm could never fire. What is true: the A4 argued-citation "
        "duty exists in the pinned rule and member (the member's `items` list is exactly the unmirrored argued "
        "citations - 13 on lane B's rows, matching lane B's own count verse for verse); lane A complied with the duty "
        "as it read it; my gate could not enforce it. The brief/duty contradiction E13-98 describes is real; the gate "
        "behaviour it describes was not."),
    "the_inert_arm_is_E36_in_my_own_gate": (
        "I built check_candidate.py before recording E-36 and did not audit it when I recorded the class. A positive "
        "fixture - one row that must fail - would have caught it on its first run. The global policy's 'audit sibling "
        "paths' clause names this duty; I recorded the class and skipped the audit."),
    "lane_b": {"receipt": "Ezek/author/repair2_step2/ezek_repair2_step2_attempt_receipts.jsonl",
               "tokens_reported": 345317, "discharged": 223, "stops": 0, "disagreements": 28,
               "gate_rerun_by_orchestrator": "ALL_CLEAN, 0 register flags - certifies the register arms only"},
    "owner_decision": {"id": "OW-20", "words_verbatim": OWNER_WORDS,
                       "concern_stated_before_the_decision": (
                           "the orchestrator told the owner Ezekiel is not closed (REPAIR-2 step 2 of 7, #e16, the "
                           "OW-6b(b) review and the close gate all owed) and that OW-11's one-boundary rule opens "
                           "Daniel only after Ezekiel closes; the owner then asked for the prompt to start Daniel "
                           "'because its ready for daniel'")},
    "handoff": {"file": "Ezek/EZEK_PAUSE_HANDOFF_REPAIR2.v1.md", "sha256": sha(HANDOFF)},
    "tools_durable": {"dir": "Ezek/repair2/session_910cbe15", "files": len(manifest),
                      "manifest_sha256": sha(DST / "MANIFEST.json")},
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(q, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------- (4) ledger MD and JSONL
LJ, LM = M8 / "error_pattern_ledger.v1.jsonl", M8 / "ERROR_PATTERN_LEDGER.v1.md"
ow20 = {
    "id": "OW-20", "kind": "owner_directive", "date": "2026-09-16",
    "words_verbatim": OWNER_WORDS,
    "what_it_decides": ("open Daniel's Phase 0 now, with Ezekiel PAUSED at REPAIR-2 step 2 rather than closed. It "
                        "waives OW-11's one-boundary ORDERING for this transition only."),
    "what_it_does_not_change": [
        "Ezekiel is NOT closed; every Ezekiel close-gate item stays owed",
        "OW-11's authority covers Ezekiel and Daniel only and expires at Daniel's close, so Ezekiel must be resumed "
        "and closed before Daniel's close gate",
        "the OW-9 hard stop at Daniel's close",
        "Daniel's own 25M ceiling (OW-15 carrier), OW-13 roles, OW-17 scholar-record gates, OW-18 tiers, OW-19 two blind lanes",
    ],
    "orchestrator_reading_labelled": ("INFERRED: 'its ready for daniel' means ready to OPEN Phase 0 - Daniel has no "
                                      "staged files on disk yet, so Phase 0 is the staging step. When Ezekiel's "
                                      "REPAIR-2 resumes (interleaved or after Daniel's strategy) is NOT stated by "
                                      "the owner and is asked at Daniel's Phase 0 close."),
    "resume_point": "sp_durable/Ezek/EZEK_PAUSE_HANDOFF_REPAIR2.v1.md",
    "carriers": ["ledger MD", "ledger JSONL", "CAMPAIGN_CLOSE_GATE.v1.md addendum", "Ezek freeze/CYCLE_STATE.md",
                 "CURRENT_STATE.v1.json (regenerated)", "RESUME_PROMPT_CURRENT.md (re-versioned)"],
}
e36_add = {
    "id": "E-36", "kind": "error_pattern_addendum", "date": "2026-09-16",
    "instance": ("the step-2 gate check_candidate.py - built BEFORE E-36 was recorded - had an inert mirror arm "
                 "keyed on a field the member never sets; both lanes' ALL_CLEAN certified two arms, not three. "
                 "Found by author lane B, not by the orchestrator."),
    "the_lesson_added": ("recording a class obliges an audit of every SIBLING check already built for the same "
                         "shape, the same day. The positive fixture - a row that must fail - is the audit."),
}
e37 = {
    "id": "E-37", "kind": "error_pattern", "date": "2026-09-16",
    "headline": ("the itemized record stayed current while the three resume carriers a cleared session reads FIRST "
                 "stayed stale for many phases"),
    "severity": "high",
    "severity_basis": ("no resume happened on the stale state, so observed impact is zero. Counterfactual: a cleared "
                       "session would have bound to phase ezek_primaries_ready and re-entered a book already through "
                       "peers, boss, four rulings, an applied author wave and REPAIR-2 step 1."),
    "instance": ("the Ezek CYCLE_STATE cursor last moved at ezek_primaries_c12_inflight_22_of_44_landed_ow17_recorded; "
                 "CURRENT_STATE.v1.json still said ezek_primaries_ready, disagreeing even with that; "
                 "RESUME_PROMPT_CURRENT.md bound to the index. The queue meanwhile grew to 99 entries. "
                 "_safe_to_clear_check.py refused - including five of its own must-pass selftest fixtures, which "
                 "evaluate against live disk - and its rule 'do not print any prompt' held."),
    "why_it_happened": ("the carriers are written at a CLEAR, and this work ran through one very long session "
                        "with compactions instead of clears, so no clear ever forced the write"),
    "cure": ["append a CURSOR line at every phase transition, not at a clear",
             "run _safe_to_clear_check.py at every landing as a drift detector, not only before printing a prompt",
             "treat a compaction like a clear for the durability law: the carriers must pass before compacting"],
    "tier": "MEASURED - the cursor, the index phase and the checker's refusals were all read from disk",
}
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    for r in (ow20, e36_add, e37):
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
md = [
    "", "## OW-20 - OWNER DIRECTIVE (2026-09-16): open Daniel's Phase 0 with Ezekiel PAUSED at REPAIR-2 step 2", "",
    "**Owner words (verbatim):** \"%s\" / \"%s\"" % tuple(OWNER_WORDS), "",
    "**Decides:** Daniel's Phase 0 opens now; Ezekiel is paused, not closed. OW-11's one-boundary ORDERING is waived for",
    "this transition only. **Does not change:** every Ezekiel close-gate item stays owed; OW-11's authority expires at",
    "Daniel's close, so Ezekiel closes before Daniel's close gate; the OW-9 hard stop at Daniel's close; Daniel's 25M",
    "ceiling; OW-13/17/18/19. **Concern stated first:** the orchestrator told the owner Ezekiel was not closed and what",
    "remained; the owner then asked for the Daniel prompt. **Resume point:** sp_durable/Ezek/EZEK_PAUSE_HANDOFF_REPAIR2.v1.md.", "",
    "## E-36 addendum - the sibling audit that was not done", "",
    "The step-2 gate `check_candidate.py`, built before E-36 was recorded, had an inert mirror arm keyed on a field the",
    "member never sets. Author lane B found it. Recording a class obliges an audit of every sibling check already built",
    "for the same shape, the same day; a positive fixture - a row that must fail - is that audit.", "",
    "## E-37 - resume carriers stale while the itemized record stayed current", "",
    "The CYCLE_STATE cursor stopped at the c12 primaries phase, CURRENT_STATE.v1.json at `ezek_primaries_ready`, and the",
    "resume prompt bound to the index - through peers, boss, four rulings, an applied author wave and REPAIR-2 step 1 -",
    "while the queue grew to 99 entries. `_safe_to_clear_check.py` refused, five of its own must-pass fixtures with it,",
    "and its rule \"do not print any prompt\" held. Cause: the carriers are written at a clear, and this work ran through",
    "compactions instead. **Cure:** a CURSOR line at every phase transition; the safe-to-clear check at every landing as a",
    "drift detector; a compaction is held to the same durability law as a clear.", "",
]
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(md))

# ---------------------------------------------------------------- (5) close-gate addendum
G = M8 / "CAMPAIGN_CLOSE_GATE.v1.md"
with G.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join([
        "", "## Addendum 2026-09-16 - OW-20 (Ezekiel paused, Daniel Phase 0 opened)", "",
        "- Ezekiel's close gate is NOT evaluated and NOT waived: Ezekiel is paused at REPAIR-2 step 2 and every item stays owed.",
        "- Ordering: Ezekiel must pass its close gate BEFORE Daniel's close gate is evaluated, because OW-11's authority for",
        "  both books expires at Daniel's close.",
        "- Resume point: sp_durable/Ezek/EZEK_PAUSE_HANDOFF_REPAIR2.v1.md.", ""]))

# ---------------------------------------------------------------- (6) CYCLE_STATE, with the cursor last
CS = EZ / "freeze" / "CYCLE_STATE.md"
cs = [
    "", "## 2026-09-16 - EZEKIEL PAUSED AT REPAIR-2 STEP 2; OWNER DIRECTIVE OW-20 OPENS DANIEL'S PHASE 0", "",
    "- SINCE THE LAST CURSOR (c12, primaries 22 of 44), TRANSCRIBED FROM THE QUEUE: primaries completed 44 of 44 and the",
    "  peer round completed with no boundary change proposed anywhere (E13-56); the boss audit landed; controlling rulings",
    "  #e12, #e13, #e14 and #e15 landed; the author-wave worklist was built and the wave applied (427 edits on 137 rows,",
    "  exact parity on seven sweeps) and regressed three checks, then was remediated back to hard GREEN (E13-78, E13-83);",
    "  the device inventory v2 landed (E13-66); the OW-17 scholar record was generated and checked 8/8 (E13-69); the spot",
    "  wave ran and #e15 re-framed its findings (E13-87..E13-92); REPAIR-2 step 0 (E13-93) and step 1 (E13-94) are done;",
    "  step 2's two blind author lanes are delivered and receipted, not reconciled, not applied (E13-98, E13-99).",
    "- ROWS: repair/rows_v7_cwo24.jsonl sha256 %s." % ROWS_SHA,
    "- OW-20 (owner, verbatim): \"%s\" / \"%s\". Ezekiel is PAUSED, not closed; every close-gate item stays owed; Ezekiel" % tuple(OWNER_WORDS),
    "  closes before Daniel's close gate because OW-11's authority expires there. Concern stated to the owner first.",
    "- RESUME POINT: sp_durable/Ezek/EZEK_PAUSE_HANDOFF_REPAIR2.v1.md (sha256 %s); tools at repair2/session_910cbe15." % sha(HANDOFF)[:16],
    "- DISCLOSED: the resume carriers were stale since c12 (E-37); the step-2 gate's mirror arm was inert (E-36 addendum,",
    "  E13-99); _brief_pin_check was not run before the two step-2 launches. The in-flight pin guard was CLEAR on every",
    "  target before these writes.",
    "- CURSOR: phase = %s." % CURSOR, "",
]
with CS.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(cs))

print(json.dumps({"tools_copied": len(manifest), "handoff_sha256": sha(HANDOFF),
                  "queue_rows": sum(1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()),
                  "ledger_jsonl_rows": sum(1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip()),
                  "cursor": CURSOR}, indent=1))
