# FINAL REMEDIATION - EZEKIEL. Author brief, SLICE 5 of 6, blind lane B

Attempt `ezek_final_s5_lane_b_a1`, execution `ezek_final_s5_lane_b_a1#e1`. You are ONE OF TWO BLIND
LANES on this slice; a Fable adjudicator reconciles you with the other lane, whose work you never see. Every other slice has
its own lanes. This is the last authoring pass before the book's final check. Your slice: 22 rows, 80 owed
items: C4TOKEN 2, CONFCAL 3, E16 18, E17 7, GROUND 7, R6 9, REG 10, RETILE 1, RIVALTOKEN 2, S7DEF 17, S7OUT 3, WEBQ 1. Some low-severity items on this slice are assigned to the other lane only; they are not in your file.

## The item classes (each item carries its order and its data; read the order, then the data)

- **RETILE** - a row the controlling agent re-tiled. Span, grade, unit type and collection are FINAL. Its prose is a seed
  (the ruling's ground verbatim, and the retired rows' rejected-alternative and device texts joined), so it still argues
  seams the row no longer has. REWRITE the row whole as one record of this span, from the ruling's ground, faces and
  required tokens (in the item's data) and the witness. The hard flags on the seed travel with the item: the ruling's
  tokens place some marks on the verse AFTER the mark (a mark is recorded on the verse it FOLLOWS) and give one later pair
  verse ':far' (it is ':near'). Write them true. Keep every mark, paseq and K/Q disclosure for the verses of this span.
  The gate REPORTS the anchors you remove from a seed to the adjudicator instead of requiring accounting.
- **S7DEF / S7OUT / R6** - a defect a reader found, an out-of-scope observation, a routed repair. RE-MEASURE on the witness
  first; repair what reproduces with the smallest change that makes the row true; NO_DEFECT with evidence otherwise.
- **E16 / E17** - an order of the controlling agent: execute it exactly; STOP with evidence if it cannot be made true. An
  order carried from a retired row applies only where it still applies to this span.
- **GROUND** - the grade was moved by the controlling agent: make the prose state the ground of the grade it carries in
  the faces' own terms, and remove any sentence that argues the old grade.
- **CONFCAL** - the audit derives a range from the faces that does not hold the grade. State the ground that holds it (a
  plan naming, a guard, a disclosed reading) or record GRADE_QUESTION with the faces. NEVER change a grade.
- **RIVALTOKEN / C4TOKEN** - a rival weighed in prose with no WARRANT-rival entry, or a 'he said to me' verse inside a
  vision interior to the span with none: add the entry (qualifier by side; the pair as the annotation's first token;
  ':merge' when the rival contests this row's own seam) with the ground that holds the row, or reword where the pair is
  not in fact weighed.
- **REG / WEBQ / MARKSYM** - member flags: state the substance instead of a label; put five or more WEB words in double
  curly quotes with an in-field web: reference; make a mark claim true to the apparatus.

**No grade, span, identity or signals change.** A grade you believe wrong is a GRADE_QUESTION, never an edit.

## Rules for what you may write

- **Change no claim beyond an item's order.** The gate extracts every face reference, verse number, Hebrew run, evidence
  tier word, count and curly-quoted English from a row's prose; anything your edit removes must be ACCOUNTED FOR in
  discharge.json under `claim_accounting[row]` as `{"anchor": <exact string the gate prints>, "why": ...}` (RETILE rows:
  reported, not required).
- **Refs:** add or re-gloss the entries an item needs; each new entry takes a ROLE token and, on a WARRANT, a verified
  face qualifier (a seam pair first on a rival). Every argued citation is mirrored by a refs entry with a ROLE token.
  MT-borne devices sit on the oshb: face; English quotations on the web: face.
- **Quotations:** five or more consecutive WEB words are a quotation whatever the delimiter: double curly quotes and an
  in-field web: reference; a run that is only the WEB's fixed rendering of a counted device is exempt.
- **Marks:** recorded on the verse they FOLLOW; every mark, paseq or puncta mention carries "single-witness". **Hebrew:**
  never hand-typed - SLICED from the witness or the live row. **Categorical claims:** unsourced means absent from BOTH
  pinned inputs. **The zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32; an entry touching it is written on
  BOTH faces. **Rotation:** no 7-gram in more than a handful of rows; vary repeated statements.
- **The register rule:** a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names, digests,
  record, census, plan, inventory or worklist names, scale labels ('tier-1'), review or wave talk, repair narration. State
  substance; name the witness and its layers; "(sweep: N verses)" is the one sanctioned count shorthand. **Read back as
  English** every field you change after your final edit, and record `read_back: true` per item only then.

## Budget and token economy (owner directive; binding)

The owner has set a hard token line for this book and it is close, and a measured audit showed where the cost really
goes: every file you pull into context is re-read on every one of your later tool calls. So:

- **Work from your extract and your slice file.** Do NOT open the live rows file, the worklist, or the three witness
  sources unless a verse you need is missing from your extract - the gate reads the rows and the worklist for you.
- **Build your proposal in ONE pass**: assemble it with a single script that writes proposal.json and discharge.json,
  rather than many small edits.
- **Run the gate when your proposal is complete** - twice at most: once to see the verdict, once after fixing what it
  reports. If a third run is truly needed, say why in `limit`.
- Measure only what an item rests on; do not re-review fields no item names; never print a whole file into your context.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554` | the live rows |
| `SP\Ezek\repair2\final\final_slices_s5_laneB.v1.json` | `279c1b0dfcf58b2bd07e2b8f30424ef3844eedc608a487ad122c44ca5621d859` | YOUR ROWS: span, grade, prose, refs and the owed items |
| `SP\Ezek\repair2\final\final_worklist.v2.json` | `ab0848ae473d6d21364b14a0f3f9e302b0d9c32a86d2cc05c1049de3cf1ced20` | the worklist (the gate's scope) |
| `SP\Ezek\repair2\final\final_substance.v1.json` | `52c6ef1c1a33fec054102d1bf12fd0c196b059da509ddde7235010602a23beda` | the substance you apply, verbatim from the records that define it |
| `SP\Ezek\author\e17\ruling_e17.json` | `499fb7807d0eccff8f6ec4501f45120de6dfc93af6200b94011fdc3cdb519790` | the controlling agent's latest ruling (re-tilings, grade decisions, orders) |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` | the ruling before it (class rulings, orders) |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling that set the role vocabulary and the register rule |
| `SP\Ezek\repair2\final\check_candidate_v6.py` | `6d288ecb557518a4e4952e0aa68da612a1bd5b44e71766a5b41956d3c0f268e9` | YOUR GATE (v6) |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `c98a74d01aa5c7ed79f30b1e15fd23dd4896c2f8fab8641f247c8a8df768333c` | imported by the gate |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `5d311aaede7309f71c82133c99ed42fe013dc53d8b1f95d632a8b4d5227f0502` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `40c9facf4140d95650a55081de21e69f34e62e166a301b54c9c029ce246278b2` | the register member |
| `SP\Ezek\tools\check_role_tokens.py` | `30d3da8340c2ce9624b718bfd570150f10fd25bd4f8a7755f3e8a626b42c877e` | the hard member that verifies every face qualifier and seam pair |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` | that member's pinned phase |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\check_web_quotes.py` | `8f0f25405c4cd5214f7a755331f362e8f1b55214f04a8a1a03c40cfe7110318b` | the quotation member |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\repair2\final\final_extract_s5.v1.json` | `fc04ea70e64cb183f4cab50f744d700b9dee616e3253a23132be14784641d588` | YOUR WITNESS EXTRACT: every verse of your rows' spans with three verses of margin - the Hebrew line sliced from the witness, the WEB text, and the marks, paseq and K/Q on each verse. Work from this; the three files below are the sources it was sliced from and you open one only if a verse you need is absent here |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse (source of the extract; opening it costs your whole context) |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB; source of the extract) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness; source of the extract) |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` | the device census v3 (said-to-me, colophons, vision returns; additive over v2) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census v2 |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` | the division plan (sections 6-7 name cut sites and regions) |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554` |
| `SP\Ezek\repair2\final\final_slices_s5_laneB.v1.json` | `279c1b0dfcf58b2bd07e2b8f30424ef3844eedc608a487ad122c44ca5621d859` |
| `SP\Ezek\repair2\final\final_worklist.v2.json` | `ab0848ae473d6d21364b14a0f3f9e302b0d9c32a86d2cc05c1049de3cf1ced20` |
| `SP\Ezek\repair2\final\final_substance.v1.json` | `52c6ef1c1a33fec054102d1bf12fd0c196b059da509ddde7235010602a23beda` |
| `SP\Ezek\author\e17\ruling_e17.json` | `499fb7807d0eccff8f6ec4501f45120de6dfc93af6200b94011fdc3cdb519790` |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
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
| `SP\Ezek\repair2\final\final_extract_s5.v1.json` | `fc04ea70e64cb183f4cab50f744d700b9dee616e3253a23132be14784641d588` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |

## Your gate

`python -B <SP>\Ezek\repair2\final\check_candidate_v6.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s5_lane_b\proposal.json --work C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s5_lane_b\gate_work --discharge C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s5_lane_b\discharge.json --worklist <SP>\Ezek\repair2\final\final_worklist.v2.json`

Run until ALL_CLEAN is true. It checks the per-row delta, claim accounting, new English-form problems, the entry form of
every added refs entry, and the WHOLE pinned suite with no hard member allowed to gain a flag.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s5_lane_b\proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs as FULL lists.
2. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final\s5_lane_b\discharge.json` - `items`: per item id (F-nnn) `status` DISCHARGED | NO_DEFECT | STOP | GRADE_QUESTION,
   `what_i_wrote` or `evidence`, `read_back`; top-level `claim_accounting`, `grade_questions`, `gate`,
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry; never list,
glob or search directories - open the exact paths above. Escalate rather than write: any seam move, any grade you believe
wrong, a pinned input that contradicts itself, a digest that differs from the table.
