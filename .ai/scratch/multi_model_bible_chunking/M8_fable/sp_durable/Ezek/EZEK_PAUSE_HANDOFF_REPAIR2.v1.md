# EZEKIEL - PAUSED AT REPAIR-2 STEP 2 (owner decision OW-20, 2026-09-16)

**Ezekiel is PAUSED, not CLOSED.** The owner opened Daniel's Phase 0 with Ezekiel mid-REPAIR-2. Every close-gate
item remains owed. OW-11's authority covers Ezekiel and Daniel only and EXPIRES AT DANIEL'S CLOSE, so Ezekiel
must be resumed and closed before Daniel's close gate. This file is the resume point; the queue
(ezek_controlling_agent_queue_e13.v1.jsonl, E13-01..E13-99) is the itemized record behind it.

## Exact state on disk

- rows: `repair/rows_v7_cwo24.jsonl` sha256 `1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425` (pre-wave `25cdba56...` -> after wave and remediation
  `64d9eff0...` -> after REPAIR-2 step 1 `1238eb24...`). Per-sweep preimage backups sit beside it as `.pre_<digest12>`.
- controlling ruling in force: `ezek_controlling_agent_ruling_e15.v1.json` sha256 `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3`.
  Its `repair2_batch_composition_and_sequence` is the work order for everything below.
- budget: OW-15 position `ezek_ow15_position.v1.json` - census LOWER BOUND 39,426,659 of the 55,000,000 ceiling
  (read from `sp_durable/campaign/budget_ceilings.v1.json`), plus the two step-2 lanes (293,322 + 345,317) not yet in
  that snapshot. Re-run the census tool before any launch.
- tools and plans used this session: `repair2/session_910cbe15/` with `MANIFEST.json` (per-file sha256).

## REPAIR-2 progress

| step | state | record |
|---|---|---|
| 0 baselines | DONE | E13-93 |
| 1 nine grade moves | DONE, 9/9 parity; the ruling's count base was wrong (27 stated, 22 measured) - E-35 | E13-94 |
| 2 grounds (16 rows) | IN PROGRESS: two blind lanes DELIVERED and RECEIPTED, NOT reconciled, NOT applied | E13-98, E13-99 |
| 3 measured-false anywhere | NOT STARTED | #e15 Q10 |
| 4 vocabulary | mechanical face arm BUILT and distinct-checked (111 derivable, 88 corroborated, 0 contradicted), NOT applied | E13-96 |
| 5 register prose pass | NOT STARTED | #e15 Q9 |
| 6 transport items + A16 weighings | NOT STARTED | #e15 |
| 7 full suite + spot re-read at full coverage with ORDERS in slices | NOT STARTED | #e15 Q1 |

**Open obligation that blocks close:** the nine step-1 rows carry a grade their prose does not yet state until step 2 lands.

## Step 2 - the reconciliation docket, exactly as it stands

Deliverables (durable): `author/repair2_step2/lane_a/` and `lane_b/` (proposal.json + discharge.json), receipts in
`author/repair2_step2/ezek_repair2_step2_attempt_receipts.jsonl`. Lane A: 109 discharged / 41 stops / 7 disagreements.
Lane B: 223 discharged / 0 stops / 28 disagreements.

1. **The step-2 gate's mirror arm was INERT.** `check_candidate.py` read a `mirrored` key that `check_refs_mirror.analyze_row`
   never sets; the member's `items` list IS the unmirrored argued citations. Fix: any `items` entry makes the row unclean;
   add a positive fixture (lane B's P08-002 at 33:21 must fail). Lane B found it. ALL_CLEAN from both lanes certifies
   the register arms only.
2. **The lanes answered the broken gate in opposite ways.** Lane A wrote ordered verses by POSITION to avoid an A4 failure
   it expected; lane B named 13 uncovered argued citations on purpose (33:21, 39:28, 33:1, WEB 21:7, 21:18, 18:9, 18:21,
   18:24, 18:27, 19:1, 37:13, 39:20, 10:22). The A4 duty is real. Cure at reconciliation: name the verses by number and
   install matching refs entries in the SAME batch, each already carrying its ROLE token and face qualifier (this does not
   collide with step 4, whose mechanical arm touches only wave-installed WARRANT-onset/close tokens).
3. **Refs now contradict corrected prose** (lane B): P03-014 (18:3 'mid-verse'), P03-017 (the samekh decides the close),
   P09-001 ('mark-only' at 37:10 and 37:12), P09-010 ('-plus-mark' at 39:20; the false 39:23 device entry #e15 Q4 ordered OUT).
4. **Calls for the orchestrator/#e16:** P03-015's 18:9 verse-final ground under the ch-18 class ruling; P09-001's holding
   sentence; P09-009 edit beyond its list; P04-008 residual 'without a competing onset'; P03-019 'mark helps decide the close'
   (does the ch-18 CLASS ruling reach it? lane A read no); lane A's claim that a dotted '39.20' is invisible to the mirror
   member (lane B's prose shows 39:20 read as AT_SEAM - verify the context difference).
5. **Suite, item by item (`suite_candidates.py`, run with PYTHONUTF8=1):** lane A - register 116->105, web_quotes 40->39,
   citation_sweep / mark_symmetry / language_zones / cap_sweep unchanged; ngram7 worst reuse now lane A's own 'is the shape
   this row's medium' in 9 rows against a gate of 10 - vary it. Lane B's suite run NOT yet done. Baseline hard_status RED
   (citation_sweep's two wrong-verse runs, P08-011 and P10-008, surfaced by the Q6 fix - step 3 items).
6. **`reconcile.py`** (claims-level, selftest-gated): one selftest fixture fails because of MY fixture design (the Qere case
   adds device words to one lane only, so DIVERGENT is correct) - fix the fixture to use the Qere row on both lanes.
   Labelled Qere forms are exempt from verse-text collation (boss audit, A1); inherited runs are corpus findings, not lane conflicts.
7. Apply only through `ezek_aw/guarded_apply.py` from preimage `1238eb24...`, simulate first, digest after the final write.

## For #e16 (assembled, not launched)

- E13-94 / E-35: #e13's `high_rows_after: 27` contradicts its own list (23); #e15 inherited it. Truth: 22 before step 1, 18 after.
- E13-97: the la-khen-turn messenger class (17:19, 20:30, 39:25) - limb (b) MEASURED to fail at all three; all three are their
  row's FIRST verse, so an unlicensed turn puts three SHIPPED SEAMS in question -> OW-6b(b) second Fable review.
  Table: `ezek_lakhen_onset_class.v1.json` (positive controls agree with four ruling measurements).
- The CONF-CAL audit list becomes readable only after step 4 installs face qualifiers (#e15 Q2/Q5).
- Open queue items still addressed to the controlling agent: E13-67, E13-68, E13-70, E13-84, E13-85, E13-89, E13-90, E13-91.

## After REPAIR-2

#e16 ruling round; the OW-6b(b) second Fable review of the §7 regions (ch-18 tiling, 16:44-50 vs 16:44-58, 37:1-14 rival,
and the three la-khen seams if #e16 rules the turn unlicensed); the OW-17 scholar-record Fable audit; OW-15 restated;
close gate items 1-25; completion receipt; OW-12 status update. Owner questions still open: the decorrelated third lens
(OW-6 escalation), the persistent carrier-map control (BOSS-ESC-1), the Greek NT witness (gates 27 of 42 remaining books).

## Controls this session did NOT run, disclosed

- `_brief_pin_check.py` was not run before the two step-2 lane launches, and the OW-11 authority paragraph was not in those
  launch messages (OW-11-h, OW-11-l (p)).
- `_inflight_pin_guard.py` was not run before several earlier record appends this session; it WAS run, CLEAR on all
  seven targets, before the writes that paused Ezekiel.
- The resume carriers (this CYCLE_STATE's cursor, CURRENT_STATE.v1.json, RESUME_PROMPT_CURRENT.md) were left stale from
  the c12 primaries cursor through every later phase; `_safe_to_clear_check.py` refused on it. Recorded as E-37.

## Addendum (same session, after the pause) - step-2 reconciliation ANALYSIS: nothing decided, nothing applied

Supersedes items 5 and 6 of the step-2 docket above. Artifacts: `repair2/step2_reconciliation/MANIFEST.json`. Rows unchanged at `1238eb24...`.

**Pinned suite, item by item against the live baseline (PYTHONUTF8=1):**

- Lane A: register 116 -> 105 (11 removed, 0 added); web_quotes 40 -> 39 (P08-012's single-curly quote cleared); refs_mirror stays GREEN (+6 far-side citations, no duty); universals 665 -> 680 (triage); ngram7 worst reuse is lane A's own 'is the shape this row's medium' in 9 rows against a gate of 10 - vary it. No hard member moved.
- Lane B: register 116 -> 105 (11 removed, 0 added); **refs_mirror GREEN -> FLAGS with +13 worklist citations** - exactly the 13 uncovered argued citations lane B disclosed, so the PINNED member does enforce the A4 duty (the correction to E13-98 is confirmed from both sides); mark_symmetry 4 -> 5 (+1 at P02-008: 'chapter 10 carries no parashah mark' flagged false_mark_absence_claim because the span's 11:1 carries a PE - the claim is about chapter 10 and #e15 Q4 states it true, so this looks like a member false positive, INFERRED, needing a reader); universals 665 -> 686; web_quotes unchanged (lane B did not clear the P08-012 quote flag).

**Claims-level reconciliation (`reconcile.py`, selftest 11/11):** 16 rows, 207 comparisons - CONVERGENT 1, DIVERGENT 15. Every stated grade matches its row in both lanes; no verse is placed verse-final by one lane and mid-verse by the other; all quoted Hebrew is EXACT, an unpointed skeleton, or a labelled Qere.

**Divergence shape (choices, not factual disagreement):** verses named only by B 13, only by A 0; device-word divergences 5; live sentences removed only by A 10, only by B 8. Shared gate constraint on P03-016, P03-017, P04-008, P08-002, P08-012, P09-010 - agreement there is the brief's wall, not corroboration.

**Three reader defects in my own reconciler, fixed before the result was trusted, each with a regression fixture:** a mis-designed Qere fixture; position words bound to every verse in a sentence (a false P03-015 conflict over identical claims worded 'mid-verse recurrences' and 'non-final recurrences'); and position claims collapsed into a dict keyed by verse, so an assertion and a rejected hypothetical for the same verse survived arbitrarily per lane (a false P03-017 conflict at 18:23).

**Decisions still owed at reconciliation - NOT taken here:**

1. Per row, lane A's position-phrasing or lane B's numbered verses; if B's, install the matching refs entries in the SAME batch, each already carrying its ROLE token and face qualifier, or refs_mirror goes FLAGS.
2. Vary lane A's templated phrase before it reaches the ngram7 gate.
3. Read the P02-008 mark_symmetry flag against the bytes.
4. Both lanes KEPT a live sentence at P03-015 rejecting the fused 18:5-20 row because 18:9's utterance is verse-final; under #e15's ch-18 class ruling a verse-final utterance followed by no fresh onset is paragraph-final, so that ground may be stale - reconciliation or #e16.
5. The calls already listed in item 4 of the docket above.
