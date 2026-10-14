# RE-REVIEW OF FIXUP-10, lane OS (orders and scope): Daniel, the 1 FIXUP-10 change records (M8_fable, OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for a study corpus. You read the Masoretic text (OSHB/WLC) and the World English Bible, verify quotations byte-for-byte, and review changes made to the prose of candidate reading units (chunk rows).

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for Ezekiel and Daniel. Verbatim answers: on authority,
"Yes: Ezekiel, then Daniel"; on recording, "M8 log only". authorization_ref
`lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 807-874
only. You run on claude-opus-5-5 as a recorded grader_fallback (OW-25): a recorded downgrade, not an equivalence. You
read files under the worktree and write only under your OUT directory; the orchestrator lands your deliverable. You
never run git, never write a receipt and never touch the registry.

## Continuation (binding)

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_rr10\out_OS_e1
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.

A complete unit here is one item. The progress file is written after each item: directly after the item, and before
you answer the checks or write the deliverable, write the item and the cursor to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_rr10\out_OS_e1\work\progress.json` (LF). If you are continued after an interruption, open that exact path and go on from
its cursor; say so in your final message.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_rr10\out_OS_e1` already exists, with its `work\` subdirectory. Write your
deliverable directly to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_rr10\out_OS_e1\dan_rr10_OS.json`. **Never run any existence check, listing, glob or recursive search**, on SP, on
OUT or anywhere else; a shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_rr10\out_OS_e1\work\`.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. State in your final
message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; every path under `SP\Dan\fixup\landed6\`,
`SP\Dan\fixup\landed7\`, `SP\Dan\fixup\landed8\`, `SP\Dan\fixup\landed9\` and `SP\Dan\fixup\landed10\`; every path under `SP\Dan\review\p13\`, `SP\Dan\review\p13r7\`
`SP\Dan\review\peer\`, `SP\Dan\review\rr8\`, `SP\Dan\review\rr9\`, `SP\Dan\review\p_evidence_fx9\` and `SP\Dan\review\p_evidence_fx10\`; every `final_message_*` file; every other file under `SP\Dan\review\rr10\` than the two
pinned below; the OUT directory of any other lane; every
`*_attempt_receipts.jsonl`; transcripts. Nothing from another book passes as Daniel's (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run
`python -B`. You may run small read-only scripts of your own on the pinned inputs, in your `work\` directory. Never pass
`--write`. Never edit any file under the worktree.

## Your role

Attempt `dan_rr10_OS_a1`, execution `dan_rr10_OS_a1#e1`. You are one of two review lanes that work blind to each other, under different
briefs. You authored none of the rows, the fix-ups (parts W9, W10 and W11 among them) or the rulings. FIXUP-10 changed
Daniel's 75 rows through 1 change record in one part (W11), under controlling ruling E12, which ordered one
exact replacement, in `W4-004` `boundary_evidence_refs` entry 1. E12 also ordered this review. The pinned extract
holds the record: its id (`W11#1`), `kind`, row, field, entry index, the `before` and `after` text and the id of the
ruling it was made under. `span`, `confidence` and `unit_type` were not to change. Every lane ran on one model
family, so agreement between lanes is not independent confirmation; only what you test on the bytes counts. The
ruling prints a script output of its own for the device words; that output is a claim under test, not your
evidence: you run a pattern-match script of your own on oshb Dan.7.14.

You are the lane **orders and scope**. For each record, find the order it carries out (the order addressed to
`author_fixup:W11` for that row and field in the ruling its `ruling_id` names) and judge:

- that `before` and `after` are exactly the text before and after ` -> ` in the one string of the order's
  `exact_spans`, in the field and entry index the order names, and that the applied entry holds the after text;
- that the diff between the base rows and the applied rows, made by a script of your own, holds nothing beyond the
  one ordered place, and that `span`, `confidence` and `unit_type` are unchanged in every row;
- that the field, as it now stands, is coherent with the other fields of the same row and with the rows before and after;
- that `W4-004` `boundary_rationale` is byte-equal to its state in the base rows, and what it says of the same words;
- that the changed list entry took no tier word, and that the count of each tier word in every row equals its count
  in the base rows (by a script of your own);
- that no changed field holds a file stem of a pinned input, the name of a model, a row id, a ruling id or process talk.

You check a fact on the witnesses wherever a judgement needs it, but the systematic test of every claim against the
bytes is the other lane's.

**Three checks both lanes owe (ordered by E12). Answer each in `checks`, with the bytes you read:**

1. `after_text_equal`: whether `W4-004` `boundary_evidence_refs` entry 1 of the applied rows holds the E12 after text
   exactly once and the E12 before text nowhere. `equal` true or false.
2. `w4_004_device_words_match_pattern`: by a script of your own, whether oshb Dan.7.14 has the word count the entry
   gives, and the inventory pattern of `everlasting_dominion_aram`, searched over the words of that verse with the
   marks stripped, matches exactly the words the entry gives (positions counted from 1). `matches` true or false;
   give the script path in `script` and what it printed in `script_output`.
3. `w4_004_entry_agrees_with_row`: whether the entry does not contradict `W4-004` `boundary_rationale` or the mark
   layer at Dan.7.14. `agrees` true or false.

A "no" is an honest answer; give it wherever the bytes give it.

For every item give `bytes_read` (the exact bytes you read to reach the verdict) and `asks_row_change`: true if your
decision is that the text of a row should change again, false if it should be kept as it stands.

**Severity** of a challenge: **high** = the changed text states a basis for a boundary that the pinned bytes refute, or
the change moves or breaks a boundary argument; **medium** = a changed sentence makes a factual claim the bytes refute,
carries a tier word that is not true, or leaves an order not carried out; **low** = imprecise or awkward wording, or a
style point, with no false claim. A finding about text that FIXUP-10 did not change goes in `extra_findings`, not in
`items`, and is graded by the same scale.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Dan\review\rr10\fixup10_changes_for_review.json` | `5c61bfc97cee18d80b46901a3f72e44d7b6a8c6f4b907b371f4094197d9f0ba1` |
| `SP\Dan\fixup\draft_rows_fixup10_applied.jsonl` | `ccf8040c65e92019d405ba79f9c837fa2c4594d82fc0245143b99e93770a88c6` |
| `SP\Dan\fixup\draft_rows_fixup9_applied.jsonl` | `e7892fc94c02dfd9f12dd089c9dbb8df6a01ee51fb9c380957e31d57fad78ab2` |
| `SP\Dan\review\dan_controlling_agent_rulings_E12.v1.json` | `8bc16d34306a990deeb39637e6314b5465da6865dbd647fb4b456a905a2285e1` |
| `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json` | `680b621d178e1f1c173204d504131c7c80f0de6a78bfe93dd52a10a060c318c0` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\review\rr10\rr10_form_check.py` | `8c1b2920c1d546d568bee6b69509c3551678de8f2a94cb8c3c0efecf6d625b8b` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md` | `4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `a78e50d7b8b9aec94955eb74f401b41322790666ef497b5780b16d11e5142216` |

How you may use each input:

- `SP\Dan\review\rr10\fixup10_changes_for_review.json`: READ in full. The 1 records you review; one item each.
- `SP\Dan\fixup\draft_rows_fixup10_applied.jsonl`: READ in full the row the record names, and its neighbours where you judge a seam. The 75 rows as they stand after FIXUP-10. You may copy it to your work directory.
- `SP\Dan\fixup\draft_rows_fixup9_applied.jsonl`: READ where you compare a field with its state before FIXUP-10 (the installed rows as FIXUP-9 left them).
- `SP\Dan\review\dan_controlling_agent_rulings_E12.v1.json`: READ the ruling a record's ruling_id names, its orders to author_fixup:W11 and their exact_spans in full, and the gate. BINDING.
- `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json`: READ the TIER-ONLY RULE and its grammar. BINDING.
- `SP\Dan\book_strategy_Dan.md`: READ where you check a fact. BINDING.
- `SP\Dan\Dan_oshb.txt`: READ the verses a record cites (OSHB/WLC, MT numbering).
- `SP\Dan\Dan_web_clean.txt`: READ the verses a record cites (WEB). A verse may run on to continuation lines after its verse line.
- `SP\Dan\pmarks_Dan.json`: READ where you check a mark (the Masoretic mark layer; one witness).
- `SP\Dan\dan_device_inventory.json`: READ wherever a record names a device listing, a class or a reading of the inventory. Pinned; not rebuilt for this book.
- `SP\Dan\review\rr10\rr10_form_check.py`: RUN on your own deliverable, as the Deliverable section says. It reads your deliverable and the pinned extract only, and tests form.
- `SP\campaign\grader_models.v1.json`: READ. The OW-25 fallback model and its statement.
- `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md`: READ. The neutral continuation contract named in the efficiency block.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only (OW-11, the owner's exception, OW-11-h).

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_rr10\out_OS_e1\dan_rr10_OS.json`

JSON, LF line endings (write bytes, or open with newline="\n"), exactly one item per record, in the extract's order:

```
{"attempt_id":"dan_rr10_OS_a1","execution_id":"dan_rr10_OS_a1#e1","book":"Dan","role":"rr10_OS",
 "rows_file":{"path":"SP\\Dan\\fixup\\draft_rows_fixup10_applied.jsonl","sha256":"<digest of the bytes you read>"},
 "records_reviewed":["W11#1"],
 "items":[{"record":"W11#1","row":"...","field":"...","verdict":"support|challenge","severity":"high|medium|low (challenge only)",
           "claim":"<what you tested and found, in one or two sentences>","tier":"MEASURED|EXTRACTED|INFERRED",
           "bytes_read":"<path, place and the exact bytes you read for this item>",
           "evidence":["<exact path + verse or bytes, or the command and its output>"],
           "asks_row_change":false,"decision":"<what should happen: keep, or the correction owed>"}],
 "extra_findings":[{"row":"...","field":"...","severity":"high|medium|low","claim":"...","tier":"...","evidence":["..."],"decision":"..."}],
 "checks":{"after_text_equal":[{"record":"W11#1","equal":true,"bytes_read":"..."}],
           "w4_004_device_words_match_pattern":{"matches":true,"script":"<path of your script>","script_output":"<what it printed>","bytes_read":"..."},
           "w4_004_entry_agrees_with_row":{"agrees":true,"bytes_read":"..."}},
 "summary":{"supports":0,"challenges":0,"by_severity":{"high":0,"medium":0,"low":0}},
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

`summary` counts `items` only. The tier of an item is the tier of your own finding: MEASURED if a script of yours
produced it (give the command and output), EXTRACTED if you read it in a pinned file (give path and place), otherwise
INFERRED. Do not use the name of any model in the deliverable.

**THE FORM IS CHECKED BY SCRIPT. These are the lines packets most often miss:**

- `records_reviewed` is a list of the record ids, in the extract's order; `items` holds exactly one object per record,
  in that order, each with `record`, `verdict`, `claim`, `tier`, `bytes_read` (one non-empty STRING), `evidence` (a
  non-empty LIST of strings), `asks_row_change` (a boolean) and `decision`; `severity` only on a challenge;
- `extra_findings` is a LIST (empty if you have none); each entry has `severity`, `claim`, `tier`, `evidence` (a
  non-empty list of strings) and `decision`;
- `checks` holds the three keys shown, in the shapes shown, every `bytes_read`, `script` and `script_output` a
  non-empty string;
- `summary` equals the counts of your own `items`; `unresolved_uncertainty` is a list.

**Before your final message, RUN the pinned form check on your deliverable** and repeat until it prints an empty
`form_problems` list:

`python -B C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Dan\review\rr10\rr10_form_check.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_rr10\out_OS_e1\dan_rr10_OS.json OS dan_rr10_OS_a1#e1`

It tests the FORM only. Change the form of your packet to satisfy it; never change a verdict, a grade or a check
answer to satisfy it. Quote its last output in your final message.

## Budget

Roughly 15 tool calls. Batch your byte checks into a few scripts in your work directory; do not open the witnesses
verse by verse by hand where a script can slice them. Report exactly what you ran and what it returned.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"dan_rr10_OS_a1","execution_id":"dan_rr10_OS_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "challenges":[{"record":"...","severity":"...","claim":"..."}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
