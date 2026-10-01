# REPAIR-2 STEP 7 - SPOT RE-READ, STRIDE 3 (two blind lanes on this stride)

You are ONE OF TWO BLIND LANES reading the same 42 rows; you never see the other lane. Every row here was changed
by REPAIR-2 (confidence moves, grounds, measured-false repairs, the vocabulary installation, the register prose pass,
the transport batch). You READ; you write nothing to any row. Your findings go to the controlling agent and #e16.

## For every row, answer all eight - each with a verdict (OK | DEFECT | QUESTION), the evidence and its tier

1. **orders_executed** - each order in the row's per-sweep orders: DISCHARGED exactly, PARTIAL, NOT DONE, or an
   UNORDERED change (a field changed that no order names). Read the order's CONTENT against the edit, not its existence.
2. **conclusion_changed** - did any repair re-decide the boundary (a new ground, a new rival held differently, a grade
   moved without an order)? A grade that follows a newly disclosed fact is not a re-decision; say which it is.
3. **claims_true** - every factual claim in a changed field, re-measured against the witness, the marks and the census:
   verses, counts, Hebrew bytes, mark direction (a mark is recorded on the verse it FOLLOWS), K/Q and paseq; every
   mark, paseq or puncta mention carries the literal "single-witness" disclosure.
4. **new_absolutes** - any categorical claim ("never", "only", "every", "no ... anywhere"): sourced, or unsourced -
   C2-amended: unsourced means absent from BOTH pinned inputs.
5. **quotations** - five or more consecutive WEB words carry double curly quotes, a web: reference and the WEB's exact
   bytes; a counted device's fixed rendering is exempt (A6-b).
6. **role_tokens** - DEF-A4-ARGUED: every argued citation mirrored by a refs entry with a ROLE token; each WARRANT's
   face qualifier and each rival's seam pair true to verse, span and the prose; MT-borne devices on oshb:, English on
   web:; in the zone (MT 21:1-5 = WEB 20:45-49) entries on BOTH faces.
7. **register_and_english** - the register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file,
   tool, record, census, plan or key names, review or wave talk, repair narration; and every changed field READ IN FULL
   as English (a doubled article, colliding phrases, a dropped clause boundary, a sentence that no longer parses);
   and ROTATION across your rows - a repair batch that wrote the same sentence into many rows breaks the rule that no
   7-gram appears in more than a handful of rows and that a repeated statement has at least 4 distinct formulations;
   report any template you see in cross_row_patterns.
8. **confidence** - the grade against the CONF-CAL view in your slice. Where the view asks a question ("census absence
   on the near face 2:7"), ANSWER it from reading: name the licensed signal a reader finds on that face (a refrain, a
   discourse turn, a scene change, "he said to me") with its verse and tier, or confirm there is none. Never propose a
   new grade; state what the evidence on each face is. No grade is raised unasked.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `097799dcebed1c4e2fdf5a5cdb40c2547309570902c4059d32fc44ced64dbf3f` | the live rows |
| `SP\Ezek\repair2\step7\step7_spot_lane_3.v1.json` | `564f93a34420e236afe2ca623184c91c4f57877e33af466f7bc77b517034a6d7` | YOUR ROWS: before/after of every field REPAIR-2 changed, per-sweep orders as data, and the CONF-CAL view |
| `SP\Ezek\repair2\step7\confcal_audit.v2.json` | `b8324f30ed72f40d25d04e991faaabc15c4e0e0afff48e699ec96e2907e0399b` | the CONF-CAL audit member's full output (the view in your slices is taken from it) |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling that ordered REPAIR-2 and this re-read |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` | A-class rulings (A6, A7, A9, A10, A16) and C2 |
| `SP\Ezek\ezek_controlling_agent_ruling_e14.v1.json` | `b4943fd46f0fe9b2d2ac764e9b9393ae2bbd99ca0c394f5207f596c7643fd521` | DEF-A4-ARGUED and the #e14 Q2 refinement |
| `SP\Ezek\repair2\step5\step5_rule_substance.v1.json` | `b309bcc9c9a03798b665da67cb8b7765254a4c566529c6cbb5ac929539551b9b` | the substance of every barred rule id, verbatim |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `097799dcebed1c4e2fdf5a5cdb40c2547309570902c4059d32fc44ced64dbf3f` |
| `SP\Ezek\repair2\step7\step7_spot_lane_3.v1.json` | `564f93a34420e236afe2ca623184c91c4f57877e33af466f7bc77b517034a6d7` |
| `SP\Ezek\repair2\step7\confcal_audit.v2.json` | `b8324f30ed72f40d25d04e991faaabc15c4e0e0afff48e699ec96e2907e0399b` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` |
| `SP\Ezek\ezek_controlling_agent_ruling_e14.v1.json` | `b4943fd46f0fe9b2d2ac764e9b9393ae2bbd99ca0c394f5207f596c7643fd521` |
| `SP\Ezek\repair2\step5\step5_rule_substance.v1.json` | `b309bcc9c9a03798b665da67cb8b7765254a4c566529c6cbb5ac929539551b9b` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |

## Output - write early and rewrite at every stage (E-29); digest after the final write

`findings.json`: `per_row` {row: {the eight items}}, `findings_total_by_severity` (HIGH | MEDIUM | LOW over DEFECTs),
`cross_row_patterns`, `confcal_answers` {row: [{face, reading, verse, tier}]}, `what_i_could_not_verify`,
`e19_selfreport`, `limit`. Hebrew you quote is SLICED from the witness, never typed.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. A digest
that differs from the table: record both and stop.
