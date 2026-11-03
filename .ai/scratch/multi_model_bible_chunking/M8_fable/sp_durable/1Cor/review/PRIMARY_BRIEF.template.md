# PRIMARY REVIEWER BRIEF: {{LANE_TITLE}} lens, 1 Corinthians, cluster {{CLUSTER}} (M8_fable, hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You read the Robinson-Pierpont Byzantine text (Unlicense), the SBLGNT (CC BY 4.0) and the World English Bible (public domain), verify quotations byte for byte, and review proposed reading-unit boundaries. The task is textual and literary review.

You are the {{LANE_TITLE}} primary reviewer for cluster {{CLUSTER}}. The work is candidate-only, NON-AUTHORIZING research. This brief is binding. Attempt `{{ATTEMPT}}`, execution `{{EXECUTION}}`. You run on claude-opus-5-5 (OW-25).

{{EFFICIENCY}}
## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `{{OUT}}` already exists, and so does its `work\` subdirectory. Write your deliverable directly to `{{OUT}}\{{DELIVERABLE}}`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A shell wildcard is a glob.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. A tool call that carries a `glob` parameter, or whose `path` names a DIRECTORY, is a glob in form even when it matches one file. State in your final message that you ran no listing and no glob. **Never open any session or agent transcript, `.output` file or compaction summary path, including your own, even if your context names one; if your context is compacted, rebuild from your OUT working files only.**

## GOVERNANCE

- SP is `{{SP}}`. It is read-only for you. Write nothing under SP, not even a debug file.
- Every file you write goes under `{{OUT}}`: the deliverable at the exact path above, and your own scripts, private copies, tool reports and saved units under `{{OUT}}\work\`. Nothing anywhere else.
- Never run git, never write a receipt, never touch any registry. You do not run the workspace validator (it runs git).
- **Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` in the environment and run `python -B`. Write scripts with your file-writing tool, never as a heredoc or `python -c` with escapes. Write every file with LF line endings (write bytes, or open with newline="\n"); a CR byte in your deliverable is refused at landing.
- **The tools you may RUN** are exactly these, each on PRIVATE COPIES of rows under `{{OUT}}\work\` and with every output path under `{{OUT}}\work\`: `SP\1Cor\tools\check_tiling.py`, `SP\1Cor\tools\run_validator_suite.py` (it writes `<copy>.validator_report.json` beside its input, so it must only ever see a copy in your `work\`), and `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py` (it writes nothing). You may import `SP\1Cor\tools\cor_lib.py` from your own scripts. Every other pinned tool is READ ONLY: `normalize_greek_in_json.py --write` and other tools under `SP\1Cor\tools\` write files when run.

## BLINDNESS: this is the point of the whole round

You see the rows file at its digest, the cluster plan, the witness files, the mark layer, the device inventory, the offset map, the verse inventories, the strategy, its machine plan, TOOLKIT.md and the tools. **You never see** any other primary lane's output, any earlier review of these rows, the fix-up briefs or their orders, any controlling execution's rulings, or any transcript. The two questions the rulings send to the primaries are copied into this brief whole. Other lanes are reviewing the same rows under other lenses, and the value of the round is that none saw another.

**FORBIDDEN:** every other model lane (`M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol`, `comparison\`); every other book's directory under SP (nothing from another book passes as this book's, E-65); the Greek apparatus and the Swete reference directories under `greek_substrate\`; `SP\1Cor\review\` and `SP\1Cor\fixup\` beyond the files named in the PINNED INPUTS table; every `*_attempt_receipts.jsonl`; `SP\1Cor\freeze\`; the writers', reviewers', fix-up authors' and other primaries' OUT directories and final messages; the campaign logs and transcripts.

## PINNED INPUTS

These are the sha256 digests of the bytes on disk as this brief was built. Record the digest of each input as you read it; a mismatch is a hard stop: report it and stop.

{{PINS}}

## The corpus and your cluster

The rows file is `SP\1Cor\fixup\draft_rows_fixup2_applied.jsonl` at `{{ROWS_SHA}}`: {{ROWS_N}} rows tiling the 437 WEB verses of 1 Corinthians. Your cluster is **{{CLUSTER}}** (writer part {{PART}}, {{SPAN}}): {{CLUSTER_N}} rows, `{{ROW_IDS}}`. The cluster plan `SP\1Cor\review_clusters.json` holds {{N_CLUSTERS}} clusters by the rule "{{CLUSTER_RULE}}". **Review every row in your cluster. There is no sampling.** Read the neighbouring row on each side of your cluster's first and last row as context for the seam ({{NEIGHBOURS}}), but give items only for your own rows.

{{RT_SCOPE}}## Questions you are given, and must answer

Give one `triage_answers` entry for each of {{TRIAGE_IDS}}; where none of its rows is in your cluster, say `in_my_cluster: false` and nothing more. These are asked, not ruled: no reading or tradition is selected by a question.

{{TRIAGE}}

**A suite flag over your rows is a question, never a verdict, and a row with no flag has not been found clean.** You may run the suite on a private copy to see its flags.

## Checklists (from the binding strategy; the strategy wins where this summary and it differ, and the difference is a finding against this brief)

1. **NUMBERING.** WEB, RP and SBLGNT numbering are identical in 1 Corinthians. Spans are C:V-C:V on the WEB face with an ASCII hyphen; a dual span, an `oshb:` token or an `mt:` token is a finding. Inline tokens are `web:`, `rp:` or `sbl:` with a real verse.
2. **WITNESSES.** Greek is quoted from RP, sliced by script. SBL is quoted only to disclose a differing reading on which the row's argument rests. A quote that crosses an SBL variant sign reaches only the skeleton tier, and a row resting on such wording names both readings. Both attribution lines travel with any Greek quotation.
3. **MARKS (three types, never conflated).** An RP pilcrow is single-witness evidence: it informs and never decides. A WEB paragraph or a chapter division never drives a boundary (strategy section 4 states the full rule, and convention C1 the mark direction). An SBL sign marks a variant site and nothing else. Test every claimed mark in BOTH directions against `pmarks_1Cor.json`: a claimed mark that is not there, and a mark at or inside the row that is there and misdescribed. Absence of a mark is never counter-evidence. Measured at the pinned digest for orientation only, the file's `tally` reads {{TALLY}}; read every tally from the file.
4. **TIER WORDS (strategy section 8 item 11; OW-18).** Every count and claim carries its true tier and names the layer or script that holds it. A stronger word than the evidence is a defect; a weaker one is not. Implication is assertion.
5. **QUOTATIONS.** English is quoted only from the WEB, sliced by script, verbatim, under the quotation contract in TOOLKIT.md. Row prose must not reproduce an unquoted witness run (strategy section 8 item 15).
6. **REGISTER (strategy section 8 items 9, 10 and 13).** Descriptive, third person, plain prose; no devotional or polemical voice; a divided reading is reported neutrally, attributed, never preferred and never moving a seam; cross-tradition material is metadata in prose only.
7. **BOTH SIDES (OW-3).** Every seam is assessed from both sides: an onset-only diagnosis is incomplete until the adjacent unit's close is weighed.

**A finding names the FACT and the VERSE to install, never a sentence to paste.** If every reviewer proposes wording, the wording converges and the seven-word gate fails.

## Your lens: {{LANE_TITLE}}

{{LENS}}

## EVERY GREEK STRING YOU WRITE IS COPIED, NEVER ASSEMBLED

A lane downstream of you cannot detect an assembled quotation from your packet alone, so this is a hard rule. A right conclusion on a fabricated quotation is still a defect.

1. **COPY** the exact substring out of `1Cor_rp.txt` (or `1Cor_sbl.txt` for a disclosed SBL reading, signs kept). Never retype it, strip or add an accent, or construct a variant notation the file does not itself contain.
2. **VERIFY before you write it**: the string must be findable as an exact substring of the line you took it from. Do this programmatically; combining marks are invisible by eye.
3. **NAME a variant site rather than rendering it.** A description by verse and position is precise and safe.
4. **Before you return**, run every Greek-script run in your finished deliverable back against the witness it cites, confirm each is present, and report that check in `verification_evidence` with the count checked. The landing tool repeats the test.

## Save as you go (the efficiency contract)

After each row is judged, append its finished item as one JSON line to `{{OUT}}\work\items.jsonl` and overwrite `{{OUT}}\work\cursor.json` with `{"next_row": "<id or DONE>", "items_saved": N}`. If your context is compacted or you are interrupted, resume from those two files only. A partial file is not acceptance; only the deliverable below is.

## Deliverable

Write JSON only, LF line endings, to `{{OUT}}\{{DELIVERABLE}}`:

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution named at the top of this brief>",
 "book":"1Cor","role":"primary_{{LANE}}","cluster":"{{CLUSTER}}",
 "model_ordered":"claude-opus-5-5 (grader_fallback, OW-25)",
 "rows_file":{"path":"1Cor/fixup/draft_rows_fixup2_applied.jsonl","sha256":"<the digest you hashed>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "rows_reviewed":["<every row id in your cluster; no sampling>"],
 "items":[{"row_id":"W1-001",
    "verdict":"support | challenge",
    "severity":"high | medium | low   (present EXACTLY when verdict is challenge, and absent on a support)",
    "claim":"the fact, stated by content, with its verse",
    "tier":"MEASURED | EXTRACTED | TRANSCRIBED | REPORTED | INFERRED | ASSUMED   (the true tier of YOUR claim)",
    "decision":"keep | cut at <exact verse> | confidence stands | confidence moves to <level> | reword <field>",
    "both_sides":"what the evidence on EACH side of the seam says (required for every cut you propose)",
    "suggested_fix":{"fact":"the fact to install","verse":"the verse it rests on"},
    "evidence":["<exact ref or byte quote>"]}],
 "triage_answers":[{"id":"TRIAGE-1COR-01","in_my_cluster":true,"rows":["..."],"decision":"...","evidence":["..."]}],
 "summary":{"supports":0,"challenges":0,"by_severity":{"high":0,"medium":0,"low":0}},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"<state that you ran no listing and no glob>",
 "limit":"one lens on one cluster; candidate-only, non-authorizing research review"}
```

**THE FIELD NAMES ABOVE ARE THE CONTRACT AND THE LANDING TOOL ENFORCES THEM EXACTLY.** `role` is the string `primary_{{LANE}}`; items are keyed `row_id`; the fact field is `claim`; `summary` uses `supports`, `challenges` and `by_severity`. `severity` takes `high`, `medium` or `low` and is present exactly when `verdict` is `challenge`. `attempt_id`, `execution_id` and `cluster` must equal this brief's exactly. One item per row in your cluster, no more and no fewer, each with a non-empty `claim`, a `tier` from the list and a non-empty `evidence`. A row with several findings carries its gravest as the item and the rest inside `evidence`, each named. `summary` must equal the counts recomputed over `items`. `triage_answers` carries exactly one entry for each of {{TRIAGE_IDS}}. `rows_file.sha256` must be `{{ROWS_SHA}}`.

## Budget

Keep to roughly {{BUDGET}} tool calls. Report exactly what you ran and what it returned.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only: `attempt_id`, `execution_id`, `cluster`, `sources` (exact paths with the digest you took), `deliverable`, `deliverable_sha256`, `rows_reviewed`, `summary`, `changes_made_or_no_change`, `verification_evidence`, `unresolved_uncertainty`, `e19_selfreport`, `limit` ("accountable work summary; not chain of thought and not independent proof").

**Do not soften a challenge to make the round look clean, and do not manufacture one to look thorough.** A row that is right is supported with its reason.
