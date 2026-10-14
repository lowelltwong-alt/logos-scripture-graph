# P13 REVIEW, lane OS (orders and scope): Daniel, the FIXUP-6 changes (M8_fable, OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for a study corpus. You read the Masoretic text (OSHB/WLC) and the World English Bible, verify quotations byte-for-byte, and review changes made to the prose of candidate reading units (chunk rows).

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for Ezekiel and Daniel. Verbatim answers: on authority,
"Yes: Ezekiel, then Daniel"; on recording, "M8 log only". authorization_ref
`lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 807-874
only. You run on claude-opus-5-5 as a recorded grader_fallback (OW-25): a recorded downgrade, not an equivalence. You
read files under the worktree and write only under your OUT directory; the orchestrator lands your deliverable. You
never run git, never write a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_p13\out_OS_e1` already exists, with its `work\` subdirectory. Write your
deliverable directly to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_p13\out_OS_e1\dan_p13_OS.json`. **Never run any existence check, listing, glob or recursive search**, on SP, on
OUT or anywhere else; a shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_p13\out_OS_e1\work\`.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. State in your final
message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; every path under `SP\Dan\fixup\landed6\`; every
`final_message_*` file; every other file under `SP\Dan\review\p13\` than the one pinned below; the OUT directory of
any other lane; every `*_attempt_receipts.jsonl`; transcripts. Nothing from another book passes as Daniel's (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run
`python -B`. You may run small read-only scripts of your own on the pinned inputs, in your `work\` directory. Never pass
`--write`. Never edit any file under the worktree.

## Your role

Attempt `dan_p13_OS_a1`, execution `dan_p13_OS_a1#e1`. You are one of two review lanes that work blind to each other, under different
briefs. You authored none of the rows, the fix-ups or the rulings. FIXUP-6 changed 61 of Daniel's 75 rows through
148 change records in seven parts (W1 to W7), under the orders of controlling ruling E6; ruling E7 then accepted
the measured result and ordered this review. The pinned extract lists every record: its id (`W3#12` is record 12 of
part W3), row, field, entry index for a list field, the `before` and `after` text, the id of the ruling it was made
under, and the `scan` the author recorded. The authors' own reasons are withheld on purpose: judge the change, not the
account of it. Every lane ran on one model family, so agreement between lanes is not independent confirmation; only
what you test on the bytes counts.

You are the lane **orders and scope**. For every record, find the order it carries out (its `ruling_id` in the E6
rulings; for part W7 the class orders CLASS-LOW-ONLY, CLASS-TIER-WORD and CLASS-INVENTORY-ARTIFACTS and gate condition
P10, as E7 GATE-E7 describes them) and judge:

- whether the change does what the order says, in the field the order names, and nothing beyond it: no new reading,
  no new claim the order did not call for, no sentence dropped that the order did not touch;
- whether the field, as it now stands in the applied row, is coherent with the other fields of the same row (span,
  unit_type, boundary_rationale, strongest_rejected_alternative, the list fields) and with the row before and the row after;
- whether a rejected alternative is stated fairly: rows W2-011, W2-012, W2-013, W4-008 and W4-009 in particular; no
  change may adjudicate a divided reading, select a textual reading or tradition, or build one eschatological timeline
  into a boundary;
- whether every tier annotation the record added matches the grammar of the TIER-ONLY RULE in the E3 rulings (an
  annotation that stands unchanged inside the record's `before` text is carried and is not tested: E7);
- whether any changed field still holds a file stem of a pinned input or the name of a model.

You check a fact on the witnesses wherever a judgement needs it, but the systematic test of every claim against the
bytes is the other lane's.

**One question put to you by E7:** in row W1-010, `observed_substrate_signals[2]` names the answering formula at
oshb:Dan.2.27, which the device inventory lists in the loose class only; the entry is unchanged from the base. Should
it be marked as loose-class? Answer in `question_W1_010` with the bytes you read.

**Severity** of a challenge: **high** = the changed text states a basis for a boundary that the pinned bytes refute, or
the change moves or breaks a boundary argument; **medium** = a changed sentence makes a factual claim the bytes refute,
carries a tier word that is not true, or leaves an order not carried out; **low** = imprecise or awkward wording, or a
style point, with no false claim. A finding about text that FIXUP-6 did not change goes in `extra_findings`, not in
`items`.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Dan\review\p13\fixup6_changes_for_review.json` | `64bcc21163c0b2ce51f538fe5cf6168f8419729010675485b4f38b7f5a4bebc8` |
| `SP\Dan\fixup\draft_rows_fixup6_applied.jsonl` | `4b0489010c772555bd483d464cce3beade1aa9454469c9503c9d256080b07ad5` |
| `SP\Dan\fixup\draft_rows_fixup5_applied.jsonl` | `2bee5919f06c22aa61b8bedf2e66ba4b22218f4ec70e6f9b65b3049aaa0f8aca` |
| `SP\Dan\review\dan_controlling_agent_rulings_E6.v1.json` | `d1626dea516a88039fbc6124934994f973b99c7d1e615b4ce435e31feb646759` |
| `SP\Dan\review\dan_controlling_agent_rulings_E7.v1.json` | `0648ec2988fac5d25cb48026bf0ff4268674910c2c62dd684435b2bf8fbca9ef` |
| `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json` | `680b621d178e1f1c173204d504131c7c80f0de6a78bfe93dd52a10a060c318c0` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\web_mt_offset_map.json` | `833d2ce37d015eccaaaac856d52c1931b9fd26bccb343064013fefc1da603da5` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `a78e50d7b8b9aec94955eb74f401b41322790666ef497b5780b16d11e5142216` |

How you may use each input:

- `SP\Dan\review\p13\fixup6_changes_for_review.json`: READ in full. The 148 records you review; one item each.
- `SP\Dan\fixup\draft_rows_fixup6_applied.jsonl`: READ in full every row a record names (61 rows), and its neighbours where you judge a seam. The 75 rows as they stand after FIXUP-6. You may copy it to your work directory.
- `SP\Dan\fixup\draft_rows_fixup5_applied.jsonl`: READ where you compare a field with its state before FIXUP-6.
- `SP\Dan\review\dan_controlling_agent_rulings_E6.v1.json`: READ each ruling a record's ruling_id names, its orders in full, and the gate. BINDING.
- `SP\Dan\review\dan_controlling_agent_rulings_E7.v1.json`: READ the gate and the rulings an item touches (the gate conditions as they now stand; what E7 accepted). BINDING.
- `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json`: READ the TIER-ONLY RULE and its grammar. BINDING.
- `SP\Dan\book_strategy_Dan.md`: READ where you check a fact. BINDING.
- `SP\Dan\Dan_oshb.txt`: READ the verses a record cites (OSHB/WLC, MT numbering).
- `SP\Dan\Dan_web_clean.txt`: READ the verses a record cites (WEB). A verse may run on to continuation lines after its verse line.
- `SP\Dan\pmarks_Dan.json`: READ where you check a mark (the Masoretic mark layer; one witness).
- `SP\Dan\dan_device_inventory.json`: READ where you check a device hit. Pinned; not rebuilt for this book.
- `SP\Dan\web_mt_offset_map.json`: READ where a row lies in a numbering zone (chapter 4 and 5:31 to 6:28).
- `SP\campaign\grader_models.v1.json`: READ. The OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only (OW-11, the owner's exception, OW-11-h).

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_p13\out_OS_e1\dan_p13_OS.json`

JSON, LF line endings (write bytes, or open with newline="\n"), exactly one item per record, in the extract's order:

```
{"attempt_id":"dan_p13_OS_a1","execution_id":"dan_p13_OS_a1#e1","book":"Dan","role":"p13_OS",
 "rows_file":{"path":"SP\\Dan\\fixup\\draft_rows_fixup6_applied.jsonl","sha256":"<digest of the bytes you read>"},
 "records_reviewed":["W1#1","..."],
 "items":[{"record":"W1#1","row":"W1-006","field":"...","verdict":"support|challenge","severity":"high|medium|low (challenge only)",
           "claim":"<what you tested and found, in one or two sentences>","tier":"MEASURED|EXTRACTED|INFERRED",
           "evidence":["<exact path + verse or bytes, or the command and its output>"],"decision":"<what should happen: keep, or the correction owed>"}],
 "extra_findings":[{"row":"...","field":"...","severity":"high|medium|low","claim":"...","tier":"...","evidence":["..."],"decision":"..."}],
 "question_W1_010":{"answer":"...","evidence":["..."]},
 "summary":{"supports":0,"challenges":0,"by_severity":{"high":0,"medium":0,"low":0}},
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

`summary` counts `items` only. The tier of an item is the tier of your own finding: MEASURED if a script of yours
produced it (give the command and output), EXTRACTED if you read it in a pinned file (give path and place), otherwise
INFERRED. Do not use the name of any model in the deliverable.

## Budget

Roughly 60 tool calls. Batch your byte checks into a few scripts in your work directory; do not open the witnesses
verse by verse by hand where a script can slice them. Report exactly what you ran and what it returned.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"dan_p13_OS_a1","execution_id":"dan_p13_OS_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "challenges":[{"record":"...","severity":"...","claim":"..."}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
