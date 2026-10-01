# REPAIR-2 STEP 2 - ADJUDICATION OF TWO BLIND AUTHOR LANES (Fable)

Attempt `ezek_repair2_step2_adjudication_a1`, execution `ezek_repair2_step2_adjudication_a1#e1`. You are the controlling adjudicator for this step (OW-13: Fable
adjudicates). Two blind Opus author lanes wrote ground prose for the same 16 rows from the same orders. You see
both - that is your role - and you produce ONE reconciled proposal the orchestrator will apply.

## Why this step exists

Nine of these rows had their confidence grade moved mechanically at REPAIR-2 step 1, and their prose does not yet
state the ground for the grade they now carry. #e15's rule: "no row again carries a grade its own text does not
state". Seven more carry stale or measurably false ground sentences #e15 ordered corrected. Your proposal closes
that obligation.

## What the comparison already established (read the pinned files; do not take this summary on trust)

- The lanes AGREE on every mechanically checkable claim: stated grades, verse-final versus mid-verse placements,
  and quoted Hebrew. The claims-level reconciliation found 0 conflicts in 207 comparisons, 15 rows divergent in
  choices and 1 convergent.
- They DIVERGE in form. Lane A describes 13 ordered verses by position ("the verse before"); lane B names them by
  number. Naming by number is more checkable, AND the pinned mirroring member enforces DEF-A4-ARGUED: every argued
  citation needs a refs entry carrying a ROLE token. Lane B's prose alone takes refs_mirror from GREEN to FLAGS on
  exactly those 13 citations. The gate you hold measures the same thing.
- Divergent sentence removals: 10 live sentences removed only by A, 8 only by B. Each removal must be justified by
  an order or by a measured falsity; otherwise the sentence stays.
- Suite notes: A reuses one phrase ("is the shape this row's medium ...") in 9 rows against a 7-gram gate of 10 rows;
  B adds one mark_symmetry flag at P02-008 (see decision 3); A cleared a single-curly-quote flag at P08-012 that B
  did not.

## The decisions you own, and must record one by one in adjudication.json

1. PER ROW: take A, take B, or merge. Where an order names a verse, NAME IT BY NUMBER and mirror it with a new refs
   entry in the same proposal (form below). Where you keep A's positional wording, say why.
2. VARY the templated sentence so no 7-gram stands in more than a handful of rows; at least 4 distinct
   formulations across the rows that state the same kind of ground.
3. P02-008: lane B's sentence that chapter 10 carries no section mark is flagged by the mark member because the
   span's MT 11:1 carries a PE. Read `pmarks_Ezek.json` by exact path. A mark is recorded on the verse it FOLLOWS.
   Decide whether the sentence is true as written and phrase it so it cannot be read as a claim about the whole
   span; if the flag is a member false positive, say so with the bytes.
4. P03-015 (and any row with the same sentence): both lanes KEPT a live sentence refusing the fused 18:5-20 row
   because 18:9's utterance is verse-final. #e15's ch-18 class finding says a verse-final utterance followed by no
   fresh onset is PARAGRAPH-final. Rule whether that ground still stands, is restated, or is removed - or route it to
   #e16 with your reasons. A false only-ground is a STOP, never a substitution.
5. The calls both lanes raised: lane B - P03-015's 18:9 ground; P09-001's holding sentence; P09-009's edit beyond its
   repair list; P04-008's residual "without a competing onset". Lane A - P03-019 (does the ch-18 CLASS ruling reach
   a close sentence that lets the mark help decide?); its claim that a dotted "39.20" is invisible to the mirror
   member (lane B's prose shows 39:20 read as an argued citation - check the context difference).
6. Every order in every slice ends DISCHARGED (quote the sentence) or a STOP (with the evidence). An order silently
   dropped is the defect this whole repair exists to cure.

## Hard constraints

- NO grade, span, identity or protected field changes. Grades were applied at step 1 and are not yours to move.
- REFS ARE APPEND-ONLY. Never remove, reword or reorder a live entry - not even P09-010's false 39:23 device entry,
  which step 3 removes; record it as a carried obligation instead.
- NEW REFS ENTRIES take the vocabulary PINNED TODAY: `<face>:Ezek.C.V[-Ezek.C.V] [TOKEN] annotation`, exactly one
  ROLE token from check_refs_mirror.ROLE_VOCABULARY, NO face qualifier (":near"/":far" are installed by step 4's
  sweep, which will pick your entries up), an annotation of one to six words. An MT-borne device (mark, K/Q, paseq,
  note, device) sits on the oshb: face; a quotation on the web: face. Inside the renumbering zone (MT 21:1-5 = WEB
  20:45-49; MT 21:6-37 = WEB 21:1-32) every entry is written on BOTH faces as `web:... = oshb:...`, mapped by the
  offset map and never by arithmetic.
- REGISTER RULE: row prose is a scholar-facing record. No rule identifiers, no ruling numbers, no file or tool
  names, no digests, no "the audit", no "the division plan", no review or wave talk, no repair narration. State the
  fact about the text.
- HEBREW: never hand-type Hebrew. Every run is SLICED from `Ezek_oshb.txt` (or from the live row) by exact bytes. A
  labelled Qere form collates against its K/Q note, not the running text. Mark, paseq and puncta entries carry the
  literal disclosure "single-witness".
- ENGLISH: a run of five or more WEB words is a quotation and takes double curly quotes plus an in-field web:
  reference; the A6-b exemption covers formula renderings only when the row names the device.
- CATEGORICAL CLAIMS: C2-amended - a claim that something is unsourced must be absent from BOTH pinned inputs; the
  census governs counts and membership.
- TIERS (OW-18): record each factual claim's true tier in adjudication.json - MEASURED (you verified it in the bytes
  this execution) > EXTRACTED > TRANSCRIBED > REPORTED > INFERRED > ASSUMED > UNAVAILABLE. UNAVAILABLE is a value.
  Corroboration never upgrades a tier.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425` | the live rows (step 1 applied); every row you write starts from these bytes |
| `SP\Ezek\repair2\session_910cbe15\ezek_step2\step2_slices.v1.json` | `e9ab2552ba6e254b43ad7bb25197e6d691fa6899fc88a53483620f3c3c4c4ec3` | per row: live prose, live refs, grade, and THE ORDERS verbatim |
| `SP\Ezek\author\repair2_step2\lane_a\proposal.json` | `d096f01afb337c562adba209de14191508436ecd3fab8c7cfae7b5569e9140c6` | blind author lane A - proposed prose |
| `SP\Ezek\author\repair2_step2\lane_a\discharge.json` | `ff8abdfa2904452a16b98ed71420d735795657585095700cb9dee54da61bec00` | lane A - order-by-order discharge, stops, disagreements |
| `SP\Ezek\author\repair2_step2\lane_b\proposal.json` | `c69c4730fee3a106fa2dba3ee39d3b36192b3378bce0762204aeef146aa7bc49` | blind author lane B - proposed prose |
| `SP\Ezek\author\repair2_step2\lane_b\discharge.json` | `02ef6e3e48a816a319d76200d7e4974ebe7e8476b92a3c320bad6583e25d2096` | lane B - order-by-order discharge, stops, disagreements |
| `SP\Ezek\repair2\step2_reconciliation\reconciliation.v1.json` | `65cc807a01a9294aa52183f25f0609e2588d91f1422f9e55ea56512b3be2cd7c` | claims-level comparison of A and B (0 conflicts in 207 comparisons) |
| `SP\Ezek\repair2\step2_reconciliation\suite_delta_lanes_a_b.json` | `d632e75e0659c8a3eb0f0f46e0d10d11424d556304f30110042732ef29fd7b9f` | the pinned validator suite on each lane's candidate, item by item against the live baseline |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | YOUR GATE - run it on your proposal until ALL_CLEAN |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` | imported by the gate (read-only) |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate (read-only); its ROLE_VOCABULARY is the vocabulary in force |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate (read-only); web_to_mt is the zone mapping |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the controlling ruling whose orders the slices carry |
| `SP\Ezek\EZEK_PAUSE_HANDOFF_REPAIR2.v1.md` | `60629112bf9e21eb547c2a934cc375c799137c1c66cca8069e5e765672283346` | the step-2 docket and its addendum (decisions owed) |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) - slice Hebrew from here, never type it |
| `SP\Ezek\Ezek_web_clean.txt` | `a7e59bcbcd19607485cfb6c6c1f8f831eb63fd2a81d164ce8e25fcb1a7a2088a` | the English version (WEB) - quote from here verbatim |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | section marks, K/Q notes, paseq (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census (counts and class membership) |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT numbering map and its zone |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425` |
| `SP\Ezek\repair2\session_910cbe15\ezek_step2\step2_slices.v1.json` | `e9ab2552ba6e254b43ad7bb25197e6d691fa6899fc88a53483620f3c3c4c4ec3` |
| `SP\Ezek\author\repair2_step2\lane_a\proposal.json` | `d096f01afb337c562adba209de14191508436ecd3fab8c7cfae7b5569e9140c6` |
| `SP\Ezek\author\repair2_step2\lane_a\discharge.json` | `ff8abdfa2904452a16b98ed71420d735795657585095700cb9dee54da61bec00` |
| `SP\Ezek\author\repair2_step2\lane_b\proposal.json` | `c69c4730fee3a106fa2dba3ee39d3b36192b3378bce0762204aeef146aa7bc49` |
| `SP\Ezek\author\repair2_step2\lane_b\discharge.json` | `02ef6e3e48a816a319d76200d7e4974ebe7e8476b92a3c320bad6583e25d2096` |
| `SP\Ezek\repair2\step2_reconciliation\reconciliation.v1.json` | `65cc807a01a9294aa52183f25f0609e2588d91f1422f9e55ea56512b3be2cd7c` |
| `SP\Ezek\repair2\step2_reconciliation\suite_delta_lanes_a_b.json` | `d632e75e0659c8a3eb0f0f46e0d10d11424d556304f30110042732ef29fd7b9f` |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\EZEK_PAUSE_HANDOFF_REPAIR2.v1.md` | `60629112bf9e21eb547c2a934cc375c799137c1c66cca8069e5e765672283346` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\Ezek_web_clean.txt` | `a7e59bcbcd19607485cfb6c6c1f8f831eb63fd2a81d164ce8e25fcb1a7a2088a` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |

## The gate

Run, by exact path: `python -B C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\repair2\step2_reconciliation\check_candidate_v2.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step2_adjudication\proposal.json`

Iterate until it prints `"ALL_CLEAN": true`. Its selftest runs first and refuses a verdict if an arm cannot fire.
It is a floor: it cannot tell you a sentence is TRUE, only that it is well-formed, mirrored and in register.

## Outputs - write early, rewrite at every stage (E-29), digest after your final write

1. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step2_adjudication\proposal.json` - `{"<row>": {"<prose field>": "<full text>", "boundary_evidence_refs": [<FULL list: every live entry unchanged, then your new entries>]}}`. Include a field only if you change it.
2. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step2_adjudication\adjudication.json` - per row: `base` (A|B|merge), `why`, `sentences_removed` (each with the order or measured falsity that removes it), `refs_entries_added` (each with the citation it mirrors), `decisions` (items 1-5 above that touch the row, each with ground and tier), `orders` (every slice order -> DISCHARGED with the sentence, or STOP with evidence), `carried_obligations` (for steps 3-7 or #e16); plus top-level `gate` (the final ALL_CLEAN output summary), `routed_to_e16`, `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Never modify any file under the worktree. Never run git, write a receipt, or touch a registry. Never run the
validator suite - the gate above is the one check you run. Escalate rather than write: any seam move, any grade you
believe wrong, a pinned input that contradicts itself, a digest that differs from the table.
