# CONTROLLING-AGENT RULING #e17 - THE SECOND REVIEW'S SEAM AND GRADE QUESTIONS (Fable)

Attempt `ezek_controlling_agent_ruling_e17_a1`, execution `ezek_controlling_agent_ruling_e17_a1#e1`. You are Ezekiel's
controlling agent (OW-6b). Two blind Fable reviewers read the flagged regions after #e16 and escalated SEAM MOVES, which only
you may order, plus grade disagreements with #e16 and claim repairs. 56 rows are raised; both reviewers raised 26 of
them. You write ONE ruling file; you mutate no row.

## Decide, once each

1. **Every seam question** (the chapter-18 tiling; P08-011's fold-back into 36:1-15; the two-verse rows P04-007 and
   P06-013 against the over-split guard; 16:44-50 | 16:51-58; 17:11-21; the ch-20 sequence 20:27-44; 43:1-12; 44:1-3 |
   44:4-31; and any other a reviewer raised): MOVE or HOLD, with the faces measured on the witness. A MOVE is a RE-TILING
   ORDER: the rows it retires (by id), the new rows' spans (WEB face, as the corpus writes spans), each new row's grade
   with its ground, and which live row's prose each new row starts from. Keep the book's tiling exact: every verse in
   exactly one row.
2. **Every grade disagreement** between a reviewer and #e16: KEEP #e16's move or SUPERSEDE it, with the faces.
3. **Claim repairs** the reviewers measured (false face claims, apparatus gaps such as undisclosed K/Q and paseq in
   chs 44-48): order each exactly for the final remediation batch, or NO_ACTION with reason.
4. **Your own earlier text** the reviewers corrected (e.g. #e16's 44:15 'mid-verse', R-7's 'every near face', R-6's
   fixture width): record each correction.

## Orders - the executable form

`retiling_orders`: [{"retire": [row ids], "new_rows": [{"span", "grade", "ground", "prose_from"}], "faces"}].
`grade_decisions`: [{"row", "e16_move", "decision": "KEEP|SUPERSEDE", "to", "faces"}].
`orders_for_final_remediation`: [{"row", "field", "order", "kind": "mechanical|author", "tier"}] - a mechanical order names
exact before/after strings. `corrections_to_earlier_rulings`, `escalations_to_owner` (only what you cannot decide).

## Rules that bind every order

The register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file or record names, repair narration.
OW-18 tiers on claims. "single-witness" on any mark, paseq or puncta mention; a mark is recorded on the verse it FOLLOWS;
never hand-type Hebrew - SLICE it from the witness; five or more WEB words take double curly quotes and a web: reference
(A6-b exempts a counted device's fixed rendering); C2-amended - unsourced means absent from BOTH pinned inputs;
DEF-A4-ARGUED - every argued citation mirrored by a refs entry with a ROLE token, a verified face qualifier and seam pair
(':merge' for a merge rival, #e16 C1); the zone - MT 21:1-5 = WEB 20:45-49 - on BOTH faces; rotation - no 7-gram in more
than a handful of rows, at least 4 distinct formulations.

## Budget

The owner has set a hard token line for Ezekiel and it is close. Rule from the packet and the two reviews; measure only
what a decision rests on; do not re-review rows no reviewer raised.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `78a092c3a2ebf27d44dea346029e3d1940578caaca609827083756ce505dfd35` | the live rows (#e16's grade moves and mechanical orders are NOT yet applied) |
| `SP\Ezek\repair2\e17\e17_packet.v1.json` | `b3258054bf5d3248c0d3f7fdac2e566cee4981a8104a3670f8329fc6a3a5cd77` | THE PACKET: both reviewers' escalations and grade findings side by side by row, with #e16's move on each row |
| `SP\Ezek\author\second_review\lane_a\review.json` | `560e28c6549a7e4568c8b64261759f9882c5b4b77babcec0f72ced4232e0fa14` | second review, blind lane A, in full |
| `SP\Ezek\author\second_review\lane_b\review.json` | `c5f4825fb5409dafe1d97e35de320d5fcc83d14cc7c8a1ba304d941b19eab0d6` | second review, blind lane B, in full |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` | #e16 - your previous ruling |
| `SP\Ezek\repair2\e16\section7_check.v1.json` | `4d368ccf6a41a7c273fcde0e4b3f8ccd1f74d5d352c7de017e8fa403e0933726` | the orchestrator's section-7 check of #e16's conditional moves (R-5) |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` | the device census v3 (said_to_me_in_vision, colophons, vision returns) |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` | the division plan v1 (section 7 holds these regions) |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |
| `SP\Ezek\verse_inventory.json` | `7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54` | per-chapter verse counts, WEB face |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `78a092c3a2ebf27d44dea346029e3d1940578caaca609827083756ce505dfd35` |
| `SP\Ezek\repair2\e17\e17_packet.v1.json` | `b3258054bf5d3248c0d3f7fdac2e566cee4981a8104a3670f8329fc6a3a5cd77` |
| `SP\Ezek\author\second_review\lane_a\review.json` | `560e28c6549a7e4568c8b64261759f9882c5b4b77babcec0f72ced4232e0fa14` |
| `SP\Ezek\author\second_review\lane_b\review.json` | `c5f4825fb5409dafe1d97e35de320d5fcc83d14cc7c8a1ba304d941b19eab0d6` |
| `SP\Ezek\author\e16\ruling_e16.json` | `20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb` |
| `SP\Ezek\repair2\e16\section7_check.v1.json` | `4d368ccf6a41a7c273fcde0e4b3f8ccd1f74d5d352c7de017e8fa403e0933726` |
| `SP\Ezek\ezek_device_inventory.v3.json` | `02d2775dc6e5a93577ca5fecec8fa4bd19d650573020a81c906ee56394a06da2` |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |
| `SP\Ezek\verse_inventory.json` | `7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54` |

## Output - write early, rewrite at every stage (E-29), digest after the final write

`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_e17_out\ruling_e17.json` with the sections named above plus `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. A digest that
differs from the table: record both and stop.
