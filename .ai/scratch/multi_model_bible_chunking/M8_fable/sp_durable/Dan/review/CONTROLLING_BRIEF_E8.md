# CONTROLLING-AGENT RULINGS E8 (execution #e1): Daniel, the findings of the P13 review of the FIXUP-6 changes (M8_fable, OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for a study corpus. You read the Masoretic text (OSHB/WLC) and the World English Bible, verify quotations byte-for-byte, and rule on proposed reading-unit boundaries and on review findings. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for Ezekiel and Daniel. Verbatim answers: on authority,
"Yes: Ezekiel, then Daniel"; on recording, "M8 log only". authorization_ref
`lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 807-874
only. You run on claude-opus-5-5 in the controlling agent's (Fable's) role, as a recorded grader_fallback (OW-25): a
recorded downgrade, not an equivalence. Your rulings go to Fable's end-of-campaign review (OW-28). You read files under
the worktree and write only under your OUT directory; the orchestrator lands your deliverable. You never run git, never
write a receipt and never touch the registry.

## Continuation (binding)

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl8
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.

A complete unit here is one ruled queue id. After each, write the rulings so far and the id you take next to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl8\work\progress.json` (LF). If you are continued after an interruption, open that exact path and go on from its
cursor; say so in your final message.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl8` already exists. Write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl8\dan_controlling_agent_rulings_E8_e1.v1.json`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl8\work\`, created with os.makedirs(exist_ok=True) and never
tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; the writers', the reviewers' and the fix-up authors' OUT directories,
final messages and evidence notes (including every `final_message_*` file under `SP\Dan\fixup\`); every
`*_attempt_receipts.jsonl`; transcripts. Nothing from another book passes as Daniel's (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. You may run small read-only scripts of your own on the pinned inputs, in your
`work\` directory. Never run any tool marked NEVER RUN. Never pass `--write`. Never edit any file under the worktree.

## Your role

You are the CONTROLLING AGENT for Daniel. Attempt `dan_controlling_rulings_a8`, execution `dan_controlling_rulings_a8#e1` (first execution). You authored none of the rows,
the strategy, the tools, the reviews, the fix-ups or the rulings E1 to E7. Ruling E7 let the FIXUP-6 rows be installed
and ordered the P13 review: two blind non-author lanes with different briefs on the 148 change records of parts W1 to
W7. Both lanes landed. GATE-E7 orders that any P13 finding of medium or high returns to you; one finding is graded
medium, and the orchestrator returns the low findings, the extra findings and the lanes' reported limits with it so
that one fix-up can carry everything you order. The queue holds 9 ids. The orchestrator proposes; you rule.
You may adopt, change or reject any proposal, re-grade a finding with a reason, and add an id only for a defect you
find in the bytes. A lane's finding is REPORTED: check each against the pinned rows and witnesses before you rule on
it. Every lane ran on one model family, so their agreement is not independent confirmation.

**The landed packets are inputs; the lanes' final messages and work files are not.**

**TEST BEFORE YOU ORDER (binding):** for any exact span you order, copy the pinned installed rows file to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl8\work\`,
apply your 'before -> after' to the copy with a small script that writes LF bytes, run the suite on the copy, and
compare `summary.triage_flags` with 83 (the state of the pinned installed rows). Put the command and its result
in the ruling's evidence. A content order (what a field must say and must no longer say, worded by the fix-up author)
needs no such test from you; the orchestrator measures the applied result against the gate conditions.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Dan\review\dan_controlling_agent_queue_e8.v1.json` | `b3f034bbe0bb039e26cd604beb4684d6032e6af9e9227ecc01dfda7a64f4846b` |
| `SP\Dan\review\p13\p13_TB.json` | `702863ac77e034bf01799d54d019911a11cf73bf68004f747e6084162584daed` |
| `SP\Dan\review\p13\p13_OS.json` | `0bf96b2b70912ef6f5ff83b625431699e4d57a4cd1f8853baeef5c80e5cea6ca` |
| `SP\Dan\review\p13\fixup6_changes_for_review.json` | `64bcc21163c0b2ce51f538fe5cf6168f8419729010675485b4f38b7f5a4bebc8` |
| `SP\Dan\fixup\draft_rows_fixup6_applied.jsonl` | `4b0489010c772555bd483d464cce3beade1aa9454469c9503c9d256080b07ad5` |
| `SP\Dan\fixup\draft_rows_fixup5_applied.jsonl` | `2bee5919f06c22aa61b8bedf2e66ba4b22218f4ec70e6f9b65b3049aaa0f8aca` |
| `SP\Dan\review\dan_controlling_agent_rulings_E7.v1.json` | `0648ec2988fac5d25cb48026bf0ff4268674910c2c62dd684435b2bf8fbca9ef` |
| `SP\Dan\review\dan_controlling_agent_rulings_E6.v1.json` | `d1626dea516a88039fbc6124934994f973b99c7d1e615b4ce435e31feb646759` |
| `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json` | `680b621d178e1f1c173204d504131c7c80f0de6a78bfe93dd52a10a060c318c0` |
| `SP\Dan\tools\run_validator_suite.py` | `5592e8f637dba58542d946dbc8414e350d8c88eea54c6f433eb05303659b348f` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\dan_language_zones.json` | `903cf551acd9fc7a4e2a3721bb1431435eeb52141cb0429799f19ad566f70a6b` |
| `SP\Dan\web_mt_offset_map.json` | `833d2ce37d015eccaaaac856d52c1931b9fd26bccb343064013fefc1da603da5` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md` | `4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `a78e50d7b8b9aec94955eb74f401b41322790666ef497b5780b16d11e5142216` |

How you may use each input:

- `SP\Dan\review\dan_controlling_agent_queue_e8.v1.json`: READ in full. The items you rule on.
- `SP\Dan\review\p13\p13_TB.json`: READ every challenge item, every extra finding, question_W1_010 and unresolved_uncertainty; the support items where you check a fact. The landed packet of lane 'claims against the bytes'.
- `SP\Dan\review\p13\p13_OS.json`: READ every challenge item, every extra finding, question_W1_010 and unresolved_uncertainty; the support items where you check a fact. The landed packet of lane 'orders and scope'.
- `SP\Dan\review\p13\fixup6_changes_for_review.json`: READ the records an item names (id, row, field, before, after, ruling id, scan). The 148 FIXUP-6 change records as the lanes saw them.
- `SP\Dan\fixup\draft_rows_fixup6_applied.jsonl`: READ in full each row an item names; the rest where you check a fact (the installed FIXUP-6 rows). Copy it to your work directory to run the suite or to test an 'after'.
- `SP\Dan\fixup\draft_rows_fixup5_applied.jsonl`: READ where you compare a field with its state before FIXUP-6. You may copy it to your work directory and run the suite on the copy.
- `SP\Dan\review\dan_controlling_agent_rulings_E7.v1.json`: READ the gate, and each ruling an item touches. BINDING unless you amend one by id with a reason.
- `SP\Dan\review\dan_controlling_agent_rulings_E6.v1.json`: READ each ruling whose order an item touches. BINDING unless you amend one by id with a reason.
- `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json`: READ where you check a prior ruling (the TIER-ONLY RULE and its grammar). BINDING unless you amend one by id with a reason.
- `SP\Dan\tools\run_validator_suite.py`: RUN, only on a private copy of a rows file in your work directory: `python -B <this path> <your copy>`; its report is written beside your copy as `<your copy>.validator_report.json`. The suite opens its own member tools and data files; that is not a listing by you. Never run it on a file under SP.
- `SP\Dan\book_strategy_Dan.md`: READ where you check a fact. BINDING.
- `SP\Dan\Dan_oshb.txt`: READ the verses an item cites, and elsewhere where you check bytes (OSHB/WLC, MT numbering).
- `SP\Dan\Dan_web_clean.txt`: READ the verses an item cites, and elsewhere where you check bytes (WEB). A verse may run on to continuation lines after its verse line.
- `SP\Dan\pmarks_Dan.json`: READ where you check a mark (the Masoretic mark layer; one witness).
- `SP\Dan\dan_device_inventory.json`: READ the lists every item on a device hit names. Pinned; not rebuilt for this book.
- `SP\Dan\dan_language_zones.json`: READ for item P13-LANE-LIMITS (a) and wherever a row tiers a statement to the language-zone layer.
- `SP\Dan\web_mt_offset_map.json`: READ where a row lies in a numbering zone (chapter 4 and 5:31 to 6:28).
- `SP\campaign\grader_models.v1.json`: READ. The OW-25 fallback model and its statement.
- `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md`: READ. The neutral continuation contract named in the efficiency block below.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only (OW-11, the owner's exception, OW-11-h).

## What to rule on

**Every** item in the queue: TIER-WEAK-OPENER, W2-008-THREE-TERMS, W2-014-TWELVE-MONTHS, W6-003-ONCE-LISTED, W4-006-SPEAKING-VERB, W1-010-LOOSE-CLASS, OLD-FORM-UNCHANGED, P13-LANE-LIMITS, GATE-E8. One ruling per id, in that order; no id may be missing.

- Nothing here may weaken a HARD gate without saying so in words. If you read a gate condition of E7 more narrowly or
  more widely than its words, amend it by id and give the reason.
- A fix-up order names the part (W8 for the new part), the row and the field, and is either an exact span
  ('before -> after', the 'before' occurring exactly once in the field as it stands in the pinned installed rows) or a
  content order; the fix-up author changes nothing else. A correction of a claim may only make the row say what the
  pinned bytes say; it adds no new reading. Where an order needs a list entry removed or added, say so in words and
  name the entries.
- A tier word must be true: MEASURED names a script, EXTRACTED names a pinned file, and a claim that rests on
  neither is INFERRED. Any annotation you order must match the E3 grammar in full.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or encodes one eschatological
  timeline in a boundary. Where an item touches one, say so and route it to Fable's end review.
- Any fix-up order requires the author to write output files with LF line endings and each change record to carry
  the field's entry index and a 'before' text unique in that field.
- **GATE-E8:** set `p13_met` (true only if no medium or high finding stays open and you order no correction),
  `fixup7_may_launch` and `fixup7_parts`, `rereview_of_fixup7` (in words the orchestrator can check with a script:
  which records, how many lanes, what closes it), `peers_conditions` (the conditions of E7 as they now stand, in full,
  amended ones marked) and `peers_may_launch` (true only if `p13_met` is true and no fix-up is ordered).

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl8\dan_controlling_agent_rulings_E8_e1.v1.json`

```
{"attempt_id":"dan_controlling_rulings_a8","execution_id":"dan_controlling_rulings_a8#e1",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|author_fixup:W8|review_fixup7|peers|fable_end_review","order":"...","row":"...","field":"...","exact_spans":["<before> -> <after>"]}]}],
 "corpus_wide_orders":[{"id":"CWO-DAN-NN","predicate":"<exact>","fields":"<exact>","remedy":"...","coverage_report":"..."}],
 "gate":{"p13_met":false,"fixup7_may_launch":false,"fixup7_parts":["W8"],"rereview_of_fixup7":"...","peers_conditions":["..."],"peers_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Rule from the queue, the packets and the bytes; open rows, layers and prior rulings where you check a fact. Keep to
roughly 40 tool calls; batch your byte checks into a few scripts in your work directory. Write the deliverable with LF
line endings (write bytes, or open with newline="\n"). Report exactly what you ran and what it returned.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"dan_controlling_rulings_a8","execution_id":"dan_controlling_rulings_a8#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
