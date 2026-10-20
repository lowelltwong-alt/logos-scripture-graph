# S1: DISTINCT-CHECKER SPOT REVIEW of the 1 Corinthians writer wave (M8_fable, hard-book track)

You are the DISTINCT CHECKER for the 1 Corinthians writer wave. The work is candidate-only, NON-AUTHORIZING research.
This brief is binding. Attempt `{{ATTEMPT}}`, execution `{{EXECUTION}}`. You run on claude-opus-5-5 (OW-25).

{{EFFICIENCY}}
## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `{{OUT}}` already exists. Write your deliverable directly to
`{{OUT}}\{{DELIVERABLE}}`. **Never run any existence check, listing, glob or recursive search against it or any other
directory.** A shell wildcard is a glob.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No directory
listing, no glob, no recursive search, no looking around. State in your final message that you ran no listing and no
glob. **Never open any session or agent transcript, `.output` file or compaction summary path, including your own,
even if your context names one; if your context is compacted, rebuild from your OUT working files only.**

## GOVERNANCE

- SP is `{{SP}}`. It is read-only for you. Write nothing under SP, not even a debug file.
- Every file you write goes under `{{OUT}}`: the deliverable at the exact path above, and your own scripts, private
  copies and tool reports under `{{OUT}}\work\`. Nothing anywhere else.
- Never run git, never write a receipt, never touch any registry.
- **FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
  `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
  `comparison\`; every other book's directory under SP; the Greek apparatus and the Swete reference directories under
  `greek_substrate\`; the writers' OUT directories, their receipts and their final messages. You judge the rows from
  the bytes, the strategy and your own runs, never from what a writer said about them.
- **Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` in the
  environment and run `python -B`. The suite starts its members as child processes; without the variable a child could
  write bytecode into `SP\1Cor\tools\`, which is a write under SP.
- **The tools you may RUN** are exactly these, each only on a PRIVATE COPY under `{{OUT}}\work\`:
  `SP\1Cor\tools\check_tiling.py`, `SP\1Cor\tools\ngram7.py`, `SP\1Cor\tools\run_validator_suite.py` (it writes
  `<copy>.validator_report.json` beside its input, so it must only ever see a copy in your `work\`), and
  `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py` (it writes nothing). You may import `SP\1Cor\tools\cor_lib.py`
  from your own scripts. Every other pinned tool is READ ONLY: `normalize_greek_in_json.py --write` and other tools
  under `SP\1Cor\tools\` write files when run.

## Your role

Six writer parts (W1-W6, each on claude-opus-5-5, blind to one another) tiled the 437 WEB verses of 1 Corinthians.
The orchestrator combined their deliverables unchanged except `chunk_index_in_book` into
`SP\1Cor\writer\draft_rows_combined.jsonl` ({{ROWS_N}} rows) and installed it by receipt. You authored none of the rows,
the strategy, the tools or any earlier review. Your findings decide what the controlling execution rules on, what the
deterministic sweeps fix and which part a fix-up routes to. This is a spot review, not a lens: it does not count toward
the strategy's §11 lens record (two blind lanes plus the reception-tradition lens run later, over the cured rows).

## PINNED INPUTS

Verify nothing you read has changed: these are the sha256 digests of the files as this brief was built.

{{PINS}}

**Read first:** `SP\1Cor\tools\TOOLKIT.md` and `SP\1Cor\book_strategy_1Cor.md` whole. The strategy is BINDING; you
judge the rows against it. Where the toolkit and a tool's code differ, the code is the contract.

## Questions: answer every one, from the bytes and from your own runs

1. **FORM AND TILING, full coverage.** On a private copy: `check_tiling.py <copy> --range 1Cor.1.1-1Cor.16.24`; the
   23-field schema; `decision_id` unique; `chunk_index_in_book` 1..{{ROWS_N}} in span order; no row straddles any of the
   {{N_PARENTS}} parents (`strategy_plan_1Cor.json` `parents`). Slice the copy by `writer_part` and run
   `_validate_writer_part_1cor.py <slice> --part W<n> --attempt cor_writer_W<n>_a1` on each of the six slices.
2. **SEAMS, full coverage.** Every internal parent seam, every seam where one part's rows meet the next part's, all
   {{N_SCR}} `scrutiny_targets` and all {{N_DEV}} `device_review_items` of `strategy_plan_1Cor.json`: is the edge argued
   from BOTH sides from the bytes; is the evidence of the tier the row claims (an edition mark alone, such as an RP
   pilcrow, a WEB paragraph start or edition punctuation, is single-witness texture and never decides; see the
   strategy's device rulings); does the row follow the strategy's working answer, or disclose and justify a departure;
   is the grade honest for the evidence given? Where a row's seam coincides with an edition mark, say whether the row's
   argument stands without the mark.
3. **STRATIFIED ROW SAMPLE.** At least 30 rows: every `high` and every `low` row; every row touching 11:2-11:34,
   12:1-14:40 or the 14:33-14:36 block; every row of one verse or of more than twelve verses; then at least three more
   per part chosen by a rule you state in advance (for example every fourth row by `chunk_index_in_book`). For each:
   `unit_type` is a strategy unit type and its evidence is named; the strategy's granularity and the over- and
   under-split guards hold; `strongest_rejected_alternative` is a real rival argued from the bytes; the §8 register
   holds (no homiletics, no adjudicated divided reading, every contested reading attributed to its holders with none
   preferred, no positional or cross-part reference, no chapter, verse, paragraph or punctuation driving a seam); every
   count and universal claim carries its provenance tier; no cross-tradition material is a ref or evidence.
4. **BYTES, full coverage, by script.** Every maximal Greek run (the run pattern in `cor_lib.py`) in every field of
   every row: is it a byte substring of the RP line, or for a disclosed SBLGNT reading of the SBLGNT line, at the
   verse the row cites for it? Report every run that is not, every run presented as RP that is SBLGNT-only, and every
   run bound to the wrong verse. Every inline token (`web:`, `rp:`, `sbl:`) names a real verse; no `oshb:` or `mt:`
   token appears; `language` follows the convention in the writer validator.
5. **BOOK-WIDE CHECKS.** Run `ngram7.py` and the suite on a private copy of the whole file. The orchestrator MEASURED,
   on its own scratch copy: {{BOOKWIDE}}. Reproduce or refute it. A per-part check cannot see a phrase repeated across
   parts: report every 7-gram shared by 7 or more rows as an early warning, and classify each repeated phrase as
   tool-induced boilerplate, a register defect or a needed disclosure, with the minimal cure (which rows to reword, a
   tool change, or both).
6. **FLAGS.** Read the suite report's FLAGS members. If there are any, sample at least 15 flagged items across at least
   four parts (or all of them if fewer): tool false positive, row defect, or neither, with evidence from the tool
   source and the row bytes.
7. **CONFIDENCE HONESTY.** The draft's spread is MEASURED in the combine report: {{CONF}}. From your sample, is that
   honest holding with bespoke rationales (the strategy asks for it), systematic under-grading, or boilerplate that
   repeats across rows? Name the rows either way. Never recommend rounding a grade up without byte evidence.

## Deliverable: `{{OUT}}\{{DELIVERABLE}}`

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "verdict":"fit_to_accept|fit_with_changes|not_fit",
 "rows_file_reviewed":{"path":"SP\\1Cor\\writer\\draft_rows_combined.jsonl","sha256":"<digest you read>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "form":{"verdict":"accept|defect","runs":["<tool + args -> result>"],"findings":["..."]},
 "seams":[{"seam":"1Cor.C.V/1Cor.C.V","kind":"parent|part_join|scrutiny_target|device_review_item","rows":["..."],"verdict":"accept|defect|for_fable","findings":["..."]}],
 "row_sample":{"selection_rule":"...","rows":[{"row":"...","verdict":"accept|defect","findings":["..."]}]},
 "bytes":{"runs_checked":0,"not_byte_exact":[],"misattributed_witness":[],"wrong_verse":[],"token_defects":[],"language_defects":[],"verdict":"accept|defect"},
 "book_wide":{"reproduced":true,"ngram7":[{"phrase":"...","rows":["..."],"classification":"...","cure":"..."}],"early_warnings":[]},
 "flags":{"sampled":0,"items":[{"flag":"...","row":"...","disposition":"tool_false_positive|row_defect|neither","evidence":"..."}]},
 "confidence":{"verdict":"honest|under_graded|boilerplate|mixed","findings":["..."]},
 "new_findings":[{"id":"S1-01","severity":"blocker|major|minor|note","row_or_artifact":"...","claim":"...","evidence":"...","suggested_fix":"...","route":"fixup:W<n>|orchestrator_cwo|tool_fix|controlling_agent|fable_end_review"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Do the deterministic parts (questions 1, 4, 5 and the sample selection) with one or two scripts of your own in
`work\`, so their output is a summary, not a dump. Keep to roughly 80 tool calls. Report exactly what you ran and what
it returned; a claimed tool run that did not happen is the worst thing you can put in a record.

## YOUR FINAL MESSAGE (evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named; opened no transcript",
 "verdict":"...","new_finding_count":0,"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
