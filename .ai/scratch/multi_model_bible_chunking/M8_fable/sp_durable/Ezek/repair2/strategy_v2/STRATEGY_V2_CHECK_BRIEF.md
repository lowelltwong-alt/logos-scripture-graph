# EZEKIEL STRATEGY v2 - DISTINCT CHECK (Fable)

Attempt `ezek_strategy_v2_check_a1`, execution `ezek_strategy_v2_check_a1#e1`. An Opus author wrote the book strategy's
next version from 44 collected orders; the close clearance requires it distinct-checked before it is accepted. You audit
the landed candidate. You do not rewrite it.

## What you verify, recorded in strategy_v2_check.json

1. **Every disposition** (44): an APPLIED order is present and correct at the v2 location named; a CITES_ONLY entry
   really orders no change to the strategy (a ruling that only cites the plan as a ground); nothing ordered was dropped.
   Per entry: CONFIRMED or DEFECT with the evidence.
2. **The six unordered edits the author flagged** (29:9 mid-verse recognition; 30:6 in the 30:1-19 messenger paragraphs;
   the 45:18 calendar-date rule against the 45:18-25 row; the dual-written chapter 20-21 seams; shortened glosses; removed
   process labels): ACCEPT or REVERT each, measured on the witness where it states a fact about the text.
3. **The tiling**: every unit list v2 gives agrees with the live rows' spans (138 rows, every WEB verse once).
4. **The cut sites and devices**: named cut sites are presented as licensing, named on no device, or resting on a
   byte-false premise exactly as the cut-site licensing ruling (#e17 K1) classes them; the therefore-turn and the
   said-to-me / transport-in-vision rulings (#e16 C3, C4) agree with the device list.
5. **Register and conventions**: the register rule holds in v2's body (a scholar-facing record: no rule ids, file or tool
   names, digests or repair narration outside the "What changed" section); where v2 states the row conventions it states
   them as ruled: DEF-A4-ARGUED with a ROLE token, face qualifier and seam pair (':merge' for a merge rival);
   "single-witness" on marks, a mark recorded on the verse it FOLLOWS; never hand-type Hebrew (SLICED from the witness);
   five or more WEB words in double curly quotes with a web: reference (A6-b); C2-amended (absent from BOTH pinned
   inputs); the zone MT 21:1-5 = WEB 20:45-49 on BOTH faces; no 7-gram in more than a handful of rows, at least 4
   distinct formulations.

## Verdict

`fit_to_accept` only if no DEFECT stands; otherwise `not_fit`, and every DEFECT carries an EXACT correction: the v2 text
to find (unique) and the text to replace it with, so the orchestrator can apply it by guarded edit and re-verify.

## Budget

The owner's token line for this book is close. Verify each disposition at the location it names; measure on the witness
only what an unordered edit or a cut-site statement rests on.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\author\strategy_v2\book_strategy_Ezek.v2.md` | `0bb641458e6c631cb3a8b7aeba7b688a159955ff45f3c3edbc9071df13385143` | THE CANDIDATE you audit (strategy v2, landed, not yet accepted) |
| `SP\Ezek\author\strategy_v2\strategy_v2_dispositions.json` | `ee41013328c987343f11a5616b626e97a72208f703bb5d14a76fd18ef6883c59` | the author's disposition for every collected order, and the unordered edits it flags |
| `SP\Ezek\repair2\strategy_v2\strategy_v2_orders.v2.json` | `8868c31c37b96273bf4c81a94ccce0ed1eddd8b0ad5ed766f94ab258944867cb` | every collected order, verbatim with its location (44 entries) |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` | strategy v1 |
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554` | the live rows (138): the tiling v2 must describe |
| `SP\Ezek\author\e17\ruling_e17.json` | `499fb7807d0eccff8f6ec4501f45120de6dfc93af6200b94011fdc3cdb519790` | #e17 |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` | #e16 |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | #e15 |
| `SP\Ezek\ezek_controlling_agent_ruling_e14.v1.json` | `b4943fd46f0fe9b2d2ac764e9b9393ae2bbd99ca0c394f5207f596c7643fd521` | #e14 |
| `SP\Ezek\ezek_controlling_agent_ruling_e13.v1.json` | `3bfa29925c9b3a6f95c0c4875ea5073168de34c2b98790c117d86c5c0779a194` | #e13 |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` | #e12 |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` | the device census v3 |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census v2 |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |

Pin rows for the pre-launch check:

| `SP\Ezek\author\strategy_v2\book_strategy_Ezek.v2.md` | `0bb641458e6c631cb3a8b7aeba7b688a159955ff45f3c3edbc9071df13385143` |
| `SP\Ezek\author\strategy_v2\strategy_v2_dispositions.json` | `ee41013328c987343f11a5616b626e97a72208f703bb5d14a76fd18ef6883c59` |
| `SP\Ezek\repair2\strategy_v2\strategy_v2_orders.v2.json` | `8868c31c37b96273bf4c81a94ccce0ed1eddd8b0ad5ed766f94ab258944867cb` |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` |
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554` |
| `SP\Ezek\author\e17\ruling_e17.json` | `499fb7807d0eccff8f6ec4501f45120de6dfc93af6200b94011fdc3cdb519790` |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\ezek_controlling_agent_ruling_e14.v1.json` | `b4943fd46f0fe9b2d2ac764e9b9393ae2bbd99ca0c394f5207f596c7643fd521` |
| `SP\Ezek\ezek_controlling_agent_ruling_e13.v1.json` | `3bfa29925c9b3a6f95c0c4875ea5073168de34c2b98790c117d86c5c0779a194` |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |

## Output - write early, rewrite at every stage (E-29), digest after the final write

`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_strategy_v2_check\strategy_v2_check.json`: `verdict`, `dispositions` (44), `unordered_edits` (6), `tiling`, `cut_sites_and_devices`,
`register_and_conventions`, `defects` (each with its exact correction), `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus, the candidate or any pinned file; no git, receipts or registry;
never list, glob or search directories. A digest that differs from the table: record both and stop.
