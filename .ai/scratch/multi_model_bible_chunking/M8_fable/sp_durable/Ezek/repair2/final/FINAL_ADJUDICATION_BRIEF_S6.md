# FINAL REMEDIATION - ADJUDICATION OF TWO BLIND AUTHOR LANES, SLICE 6 (Fable)

Attempt `ezek_final_s6_adjudication_a1`, execution `ezek_final_s6_adjudication_a1#e1`. You are the controlling
adjudicator for this slice (OW-13: Fable adjudicates). Two blind Opus lanes answered the owed items of this slice in the
book's last authoring pass; you produce ONE proposal. Every other slice has its own adjudicator.

## What you decide, recorded in adjudication.json

1. Per item (F-nnn): DISCHARGED (with the text you adopt), NO_DEFECT (with evidence), STOP (with evidence) or
   GRADE_QUESTION (with the faces). 12 items were given to lane A alone (a low-severity defect one earlier reader
   raised); on those, lane A's work is the only lane - read it against the witness yourself before adopting it.
2. Per changed field: which lane's text you adopt, or a reconciled text of your own where neither lane's text both states
   the substance and reads as English - and why. A reconciled text owes everything a lane's text owes.
3. READ EVERY ADOPTED FIELD IN FULL AS ENGLISH after your final edit (the second reading under OW-19); record
   `read_back: true` per field only then.
4. CLAIMS: any anchor the gate reports removed on a non-re-tiled row is accounted for in your own
   `claim_accounting[row]`, taken from the lane you followed or written by you; a claim neither lane can account for is
   restored, never dropped. On a re-tiled row the gate reports the anchors removed from the seed: confirm the row you adopt
   still states every face the ruling measured and every disclosure for the verses of its span.
5. GRADE QUESTIONS and anything beyond this pass (a seam move, a class question): listed under `routed` with the faces.
   Never change a grade, span, identity or signals.

## Where the lanes diverge - computed from their files, stated without a preference

- items whose statuses differ: 3; missing from a discharge: A 0, B 0
- fields only lane A changed: 9; only lane B: 5; both changed differently: 44; identically: 6
- stops: lane A 0, lane B 2; grade questions: lane A 0, lane B 0

The full lists are in the pinned divergence file. A field only one lane changed is a question in itself: was the other
lane right to leave it, or did it miss an owed item?

## Grade caps the orchestrator applies after the merge

The controlling agent's class ruling K3 (#e17) caps a row whose span or region the plan names as an open question at medium_low; the pinned caps plan lists, with the plan text measured, the rows above that cap. On this slice: P07-004, P07-009. The orchestrator moves each to medium_low through its own guarded confidence operation after the merge - you change no grade. The prose you adopt on these rows must not argue a medium grade; where an item asks for the grade's ground, state in one clause, in the faces' own terms, that the plan holds the region as an open question, which holds the grade at medium_low. If you measure that the plan does NOT name a listed span or region, say so with the text under routed, and the row is not capped.

## Rules - lane A's brief is pinned and binds you identically

The register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names, digests, record,
census, plan, inventory or worklist names, scale labels, review or wave talk, repair narration. "single-witness" on any
mark, paseq or puncta mention; a mark is recorded on the verse it FOLLOWS; never hand-type Hebrew - SLICE it from the
witness or the live row; five or more WEB words take double curly quotes and a web: reference (a counted device's fixed
rendering is exempt); unsourced means absent from BOTH pinned inputs; every argued citation stays mirrored by a refs entry
with a ROLE token whose face qualifier and seam pair agree with the prose (':merge' for a rival that contests the row's own
seam); the zone - MT 21:1-5 = WEB 20:45-49 - on BOTH faces; no 7-gram in more than a handful of rows.

## Budget

The owner's token line for this book is close. Adjudicate from the lanes' files and the divergence map; measure on the
witness only what a decision rests on.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554` | the live rows |
| `SP\Ezek\repair2\final\final_slices_s6_laneA.v1.json` | `fb289d19dc4401c93fe496cbdf6570780d60cccd3eb07cffd42a3056d5e2d948` | this slice's rows, prose and ALL owed items (lane A's file) |
| `SP\Ezek\repair2\final\final_slices_s6_laneB.v1.json` | `b1500633ab571a800fc6c508bfcf8cd81a7aa67c8a07c86b8f5aaf0caef9733f` | lane B's file (omits the scope-cut-3 items) |
| `SP\Ezek\repair2\final\final_worklist.v2.json` | `ab0848ae473d6d21364b14a0f3f9e302b0d9c32a86d2cc05c1049de3cf1ced20` | the worklist (the gate's scope) |
| `SP\Ezek\repair2\final\final_substance.v1.json` | `52c6ef1c1a33fec054102d1bf12fd0c196b059da509ddde7235010602a23beda` | the substance, verbatim from the records that define it |
| `SP\Ezek\repair2\final\FINAL_AUTHOR_BRIEF_S6_A.md` | `1539cfbaa2a29566ec9e3bbcdaaad76207df2bc79f608d9315955846ffc98b8c` | the brief lane A held; its rules bind you identically |
| `SP\Ezek\author\final\s6_lane_a\proposal.json` | `b7851b99b1e5f0d3d8314ac7c3139d5602ed852441d76571f4680d6bd3622760` | blind lane A - proposal |
| `SP\Ezek\author\final\s6_lane_a\discharge.json` | `5aadf3974c56774603788c486b4a7379d28e8d26cf3225d5a98236126dfb6d87` | blind lane A - per-item discharge and claim accounting |
| `SP\Ezek\author\final\s6_lane_b\proposal.json` | `cca1c6c0b01952e0fa30eda37ca11a540f19ceadf5d401197e4a876e1a7e3b08` | blind lane B - proposal |
| `SP\Ezek\author\final\s6_lane_b\discharge.json` | `802356fe30664096deac73b09af82b8a75fcb1177e35738e89b21e5241337238` | blind lane B - per-item discharge and claim accounting |
| `SP\Ezek\repair2\final\final_divergence_s6.v1.json` | `99d9aee4ae7c5f76273028b358e0ab5ce32d96c4d80082fd63714b854ad8dd8e` | where the lanes diverge, computed from their files (a map, not a reading) |
| `SP\Ezek\repair2\final\k3_caps_plan.v1.json` | `306f9fcc74685a29335755b1cf196e21c2a6dbe0bcc81847faa0e969776b63a9` | the grade caps the orchestrator applies after the merge (#e17 K3), with the section-7 text measured |
| `SP\Ezek\author\e17\ruling_e17.json` | `499fb7807d0eccff8f6ec4501f45120de6dfc93af6200b94011fdc3cdb519790` | the controlling agent's latest ruling |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` | the ruling before it |
| `SP\Ezek\repair2\final\check_candidate_v6.py` | `6d288ecb557518a4e4952e0aa68da612a1bd5b44e71766a5b41956d3c0f268e9` | YOUR GATE (v6) |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `c98a74d01aa5c7ed79f30b1e15fd23dd4896c2f8fab8641f247c8a8df768333c` | imported by the gate |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `5d311aaede7309f71c82133c99ed42fe013dc53d8b1f95d632a8b4d5227f0502` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `40c9facf4140d95650a55081de21e69f34e62e166a301b54c9c029ce246278b2` | the register member |
| `SP\Ezek\tools\check_role_tokens.py` | `30d3da8340c2ce9624b718bfd570150f10fd25bd4f8a7755f3e8a626b42c877e` | a hard member |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` | its pinned phase |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\check_web_quotes.py` | `8f0f25405c4cd5214f7a755331f362e8f1b55214f04a8a1a03c40cfe7110318b` | the quotation member |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` | the device census v3 |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` | the division plan |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554` |
| `SP\Ezek\repair2\final\final_slices_s6_laneA.v1.json` | `fb289d19dc4401c93fe496cbdf6570780d60cccd3eb07cffd42a3056d5e2d948` |
| `SP\Ezek\repair2\final\final_slices_s6_laneB.v1.json` | `b1500633ab571a800fc6c508bfcf8cd81a7aa67c8a07c86b8f5aaf0caef9733f` |
| `SP\Ezek\repair2\final\final_worklist.v2.json` | `ab0848ae473d6d21364b14a0f3f9e302b0d9c32a86d2cc05c1049de3cf1ced20` |
| `SP\Ezek\repair2\final\final_substance.v1.json` | `52c6ef1c1a33fec054102d1bf12fd0c196b059da509ddde7235010602a23beda` |
| `SP\Ezek\repair2\final\FINAL_AUTHOR_BRIEF_S6_A.md` | `1539cfbaa2a29566ec9e3bbcdaaad76207df2bc79f608d9315955846ffc98b8c` |
| `SP\Ezek\author\final\s6_lane_a\proposal.json` | `b7851b99b1e5f0d3d8314ac7c3139d5602ed852441d76571f4680d6bd3622760` |
| `SP\Ezek\author\final\s6_lane_a\discharge.json` | `5aadf3974c56774603788c486b4a7379d28e8d26cf3225d5a98236126dfb6d87` |
| `SP\Ezek\author\final\s6_lane_b\proposal.json` | `cca1c6c0b01952e0fa30eda37ca11a540f19ceadf5d401197e4a876e1a7e3b08` |
| `SP\Ezek\author\final\s6_lane_b\discharge.json` | `802356fe30664096deac73b09af82b8a75fcb1177e35738e89b21e5241337238` |
| `SP\Ezek\repair2\final\final_divergence_s6.v1.json` | `99d9aee4ae7c5f76273028b358e0ab5ce32d96c4d80082fd63714b854ad8dd8e` |
| `SP\Ezek\repair2\final\k3_caps_plan.v1.json` | `306f9fcc74685a29335755b1cf196e21c2a6dbe0bcc81847faa0e969776b63a9` |
| `SP\Ezek\author\e17\ruling_e17.json` | `499fb7807d0eccff8f6ec4501f45120de6dfc93af6200b94011fdc3cdb519790` |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` |
| `SP\Ezek\repair2\final\check_candidate_v6.py` | `6d288ecb557518a4e4952e0aa68da612a1bd5b44e71766a5b41956d3c0f268e9` |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `c98a74d01aa5c7ed79f30b1e15fd23dd4896c2f8fab8641f247c8a8df768333c` |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `5d311aaede7309f71c82133c99ed42fe013dc53d8b1f95d632a8b4d5227f0502` |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` |
| `SP\Ezek\tools\check_register.py` | `40c9facf4140d95650a55081de21e69f34e62e166a301b54c9c029ce246278b2` |
| `SP\Ezek\tools\check_role_tokens.py` | `30d3da8340c2ce9624b718bfd570150f10fd25bd4f8a7755f3e8a626b42c877e` |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` |
| `SP\Ezek\tools\check_web_quotes.py` | `8f0f25405c4cd5214f7a755331f362e8f1b55214f04a8a1a03c40cfe7110318b` |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |

## The gate

`python -B <SP>\Ezek\repair2\final\check_candidate_v6.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s6_adjudication\proposal.json --work C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s6_adjudication\gate_work --discharge C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s6_adjudication\adjudication.json --worklist <SP>\Ezek\repair2\final\final_worklist.v2.json`

Run it until ALL_CLEAN is true; report the completion measure beside it, and account for every register flag you leave.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s6_adjudication\proposal.json` - only changed fields, FULL new values (refs as full lists).
2. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s6_adjudication\adjudication.json` - `items` per item id; `fields` per changed field (lane followed or reconciled, why);
   top-level `claim_accounting`, `grade_questions`, `gate` with the completion measure, `routed`,
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry; never list,
glob or search directories. Escalate rather than write: any seam move, any grade you believe wrong, a pinned input that
contradicts itself, a digest that differs from the table.
