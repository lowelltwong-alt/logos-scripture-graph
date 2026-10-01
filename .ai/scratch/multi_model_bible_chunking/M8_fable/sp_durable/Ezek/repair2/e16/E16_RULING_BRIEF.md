# CONTROLLING-AGENT RULING #e16 - EZEKIEL (Fable)

Attempt `ezek_controlling_agent_ruling_e16_a1`, execution `ezek_controlling_agent_ruling_e16_a1#e1`. Under OW-6b you are
the CONTROLLING agent for Ezekiel: boundary decisions, grade decisions, class rulings and escalations are your calls.
You write ONE ruling file; you mutate no row. The orchestrator executes your orders - mechanically where an order is
deterministic, through two blind author lanes and a Fable adjudication otherwise - in the final remediation batch.

## What #e16 decides (each in its own section of ruling_e16.json)

1. **C3 - the lakhen-turn messenger onsets** (17:19, 20:30, 39:25; #e15 Q2 held the class "decided once"). All three are
   their row's FIRST verse, so the ruling reaches three shipped seams, not only grades. Decide whether such a turn, with
   no addressee change and no verse-final close-role formula before it, is a licensed onset; state what follows for each
   of the three rows (seam stands and its ground / grade, or the escalation a seam move requires - you may not move a
   seam silently; a seam move is an escalation with its evidence).
2. **C1 - the forward-merge rival face** (17 entries plus S4-085's qualifier; the step-4c adjudicator routed both
   readings and every entry). Decide the grammar - one of the named options or a better one you state - so that every
   WARRANT carries a verified face; order the exact entry for each affected row; say whether the role_tokens member needs
   a new arm (a tool order) and the condition under which its phase flips from pre to post.
3. **C2 - the merge-rival pairing convention** the readers found applied four ways; rule one convention and order each
   row that departs from it.
4. **C4 - the CONF-CAL member's coverage**: whether "he said to me" inside a vision and an interior transport verse are
   licensed onsets for the scale; whether an interior rival weighed in prose with no rival token must be tokenised; any
   tool order for the member.
5. **THE CONF-CAL DOCKET**: for each of the 46 rows, and each within-reader-range row whose readers' answers settle it,
   KEEP the grade with its stated ground, or MOVE it with the ground and the faces named. The readers' answers are
   readings, not rulings; a grade the evidence does not support moves; no grade moves without a ground. The scale's
   rule stands: no grade is raised unasked - you are asked here.
6. **THE 92 STEP-7 QUESTIONS AND THE ROUTED ENTRIES**: answer each that needs a ruling; mark the rest as author work
   for the remediation batch with the exact order, or NO_ACTION with the reason.

## Orders - the form the orchestrator can execute

`orders_for_final_remediation`: a list of `{"row", "field", "order", "kind": "mechanical" | "author", "tier",
"source_item"}`. A mechanical order names an exact before/after string or an exact token change; an author order
names the claim to correct and the evidence. `grade_moves`: `{"row", "from", "to", "ground", "faces"}`. `tool_orders`:
member changes with the fixture that must fail before and pass after. `escalations`: anything that needs a seam move
or the owner.

## Rules that bind every order you issue (the authors will be gated on them)

The register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file or record names, repair
narration; state substance, name the witness and its layers. OW-18 tiers on every claim. "single-witness" on any mark,
paseq or puncta mention; a mark is recorded on the verse it FOLLOWS; never hand-type Hebrew - SLICE it from the witness;
five or more WEB words take double curly quotes and a web: reference (A6-b exempts a counted device's fixed rendering);
C2-amended - unsourced means absent from BOTH pinned inputs; DEF-A4-ARGUED - every argued citation mirrored by a refs
entry with a ROLE token whose face qualifier and seam pair are verified; the zone - MT 21:1-5 = WEB 20:45-49 - on BOTH
faces; rotation - no 7-gram in more than a handful of rows, at least 4 distinct formulations.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `78a092c3a2ebf27d44dea346029e3d1940578caaca609827083756ce505dfd35` | the live rows |
| `SP\Ezek\repair2\e16\e16_packet.v1.json` | `8010f48853beddb49435edec09a9cee6c2329175369bac8e78a16c6a9c4dd1d6` | THE PACKET: the four class questions, the CONF-CAL docket with both step-7 readers' answers, the 92 step-7 questions, the 57 routed entries |
| `SP\Ezek\repair2\step7\confcal_audit.v2.json` | `5afd973591ecf47afa19e864c6f6618bef060e863b71ca7a85b6a3bb10bdeb0f` | the CONF-CAL audit member v2's full output (faces, ranges, bases) |
| `SP\Ezek\repair2\step7\step7_reconciled.v1.json` | `7da382eeee38f627c594666809956f5f764520bb2119ee82ed9d3e0586e1fc9c` | the step-7 reconciliation in full (both readers' evidence per row and item) |
| `SP\Ezek\repair2\e16\e16_docket.v1.json` | `e5121566b09ceb1e2ef4cfbdda02aea35acd9fad76fc8fb8c0fc662e79376e24` | the #e16 docket collector's full output |
| `SP\Ezek\author\repair2_step4c\adjudication\adjudication.json` | `d00c1ad9ba5b65620eaf84ac91796f8c2ed1404cd5defadc22855b04d9941f4a` | the step-4c adjudication (the forward-merge class and its entries) |
| `SP\Ezek\ezek_controlling_agent_queue_e13.v1.jsonl` | `a04648379614ea89061d82098bc067e4401b8b7ac77d2797a1265964384f9ff0` | the e13 queue (E13-97 lakhen table; E13-106..109 on REPAIR-2 steps 4c-7) |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | #e15 - Q2's unified rival definitions and CONF-CAL high limb, Q5 clause 6 v2 |
| `SP\Ezek\ezek_controlling_agent_ruling_e14.v1.json` | `b4943fd46f0fe9b2d2ac764e9b9393ae2bbd99ca0c394f5207f596c7643fd521` | #e14 - Q2's mid-verse refinement |
| `SP\Ezek\ezek_controlling_agent_ruling_e13.v1.json` | `3bfa29925c9b3a6f95c0c4875ea5073168de34c2b98790c117d86c5c0779a194` | #e13 - CONF-CAL and CUT-RULE as ruled |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` | #e12 - the A/C/D class rulings |
| `SP\Ezek\AUTHOR_WAVE_BRIEF.v1.md` | `31f58d77c318ef8e9d2b6c746f3de56ea39884d63650290f1e2765c453eaf5ad` | CONF-CAL, CUT-RULE and precedence as briefed (its 13.2 phrase list is superseded by #e15 Q9(a)) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `78a092c3a2ebf27d44dea346029e3d1940578caaca609827083756ce505dfd35` |
| `SP\Ezek\repair2\e16\e16_packet.v1.json` | `8010f48853beddb49435edec09a9cee6c2329175369bac8e78a16c6a9c4dd1d6` |
| `SP\Ezek\repair2\step7\confcal_audit.v2.json` | `5afd973591ecf47afa19e864c6f6618bef060e863b71ca7a85b6a3bb10bdeb0f` |
| `SP\Ezek\repair2\step7\step7_reconciled.v1.json` | `7da382eeee38f627c594666809956f5f764520bb2119ee82ed9d3e0586e1fc9c` |
| `SP\Ezek\repair2\e16\e16_docket.v1.json` | `e5121566b09ceb1e2ef4cfbdda02aea35acd9fad76fc8fb8c0fc662e79376e24` |
| `SP\Ezek\author\repair2_step4c\adjudication\adjudication.json` | `d00c1ad9ba5b65620eaf84ac91796f8c2ed1404cd5defadc22855b04d9941f4a` |
| `SP\Ezek\ezek_controlling_agent_queue_e13.v1.jsonl` | `a04648379614ea89061d82098bc067e4401b8b7ac77d2797a1265964384f9ff0` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\ezek_controlling_agent_ruling_e14.v1.json` | `b4943fd46f0fe9b2d2ac764e9b9393ae2bbd99ca0c394f5207f596c7643fd521` |
| `SP\Ezek\ezek_controlling_agent_ruling_e13.v1.json` | `3bfa29925c9b3a6f95c0c4875ea5073168de34c2b98790c117d86c5c0779a194` |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` |
| `SP\Ezek\AUTHOR_WAVE_BRIEF.v1.md` | `31f58d77c318ef8e9d2b6c746f3de56ea39884d63650290f1e2765c453eaf5ad` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |

## Output - write early, rewrite at every stage (E-29), digest after the final write

`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_e16_out\ruling_e16.json` with sections `c1_forward_merge`, `c2_merge_pairing`, `c3_lakhen_turn`, `c4_confcal_member`,
`confcal_docket`, `questions_and_routed`, `orders_for_final_remediation`, `grade_moves`, `tool_orders`, `escalations`,
`role_tokens_phase_flip`, `what_i_could_not_verify`, `e19_selfreport`, `limit`. Every byte fact MEASURED over the pinned
inputs and labelled; every reading labelled as a reading.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. A digest that
differs from the table: record both and stop.
