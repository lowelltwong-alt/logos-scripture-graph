# S5: FRESH DISTINCT-CHECKER REVIEW of the 1 Corinthians FIXUP-3 applied rows (M8_fable, hard-book track)

You are the DISTINCT CHECKER S5 for 1 Corinthians. The work is candidate-only, NON-AUTHORIZING research. This brief is
binding. Attempt `{{ATTEMPT}}`, execution `{{EXECUTION}}`. You run on claude-opus-5-5 (OW-25).

{{EFFICIENCY}}
## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `{{OUT}}` already exists, and so does its `work\` subdirectory.
Write your deliverable directly to `{{OUT}}\{{DELIVERABLE}}`. **Never run any existence check, listing, glob or
recursive search against it or any other directory.** A shell wildcard is a glob.

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
  `greek_substrate\`; the writers' and the fix-up authors' OUT directories, their final messages (`final_*.json`) and
  every receipt file other than the extract pinned below; the S1, S2 and S3 review deliverables and their prose; the
  primary lanes' reports and the controlling queues; the FIXUP-1 and FIXUP-2 briefs and landed files. You judge the
  rows from the bytes, the strategy, the rulings and your own runs. A record of what someone did is a claim to test.
- **Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` in the
  environment and run `python -B`. The suite and the fixtures start child processes; without the variable a child
  could write bytecode under SP, which is a write under SP.
- **The tools you may RUN** are exactly these, each on PRIVATE COPIES of rows under `{{OUT}}\work\` and with every
  output path under `{{OUT}}\work\`: `SP\1Cor\tools\check_tiling.py`, `SP\1Cor\tools\ngram7.py`,
  `SP\1Cor\tools\run_validator_suite.py` (it writes `<copy>.validator_report.json` beside its input, so it must only
  ever see a copy in your `work\`), `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py` (it writes nothing),
  `SP\1Cor\review\cwo_sweep_1cor.py` (`ROWS.jsonl --out FILE.json`; `--out` under your `work\` only),
  `SP\1Cor\review\tools\test_cwo05.py` and `SP\1Cor\review\tools\test_cwo0607.py` (read each docstring for its
  arguments; `--work` must be a directory under your `work\`), and `SP\1Cor\review\tool_fixes\mutants_tf5.py` (`--work`
  and `--out` under your `work\`). You may import `SP\1Cor\tools\cor_lib.py` from your own scripts. Every other pinned
  tool is READ ONLY: `normalize_greek_in_json.py --write` and other tools under `SP\1Cor\tools\` write files when run.

## Your role

Six writer parts tiled the 437 WEB verses. Two fix-up rounds and three reviews brought the rows to the primary round:
{{ROWS_N}} rows, ten clusters, 23 landed primary lanes. The fourth controlling execution (E4) ruled on the primaries'
challenges: {{N_RULINGS}} rulings, two new corpus-wide orders, {{N_UNRES}} unresolved-uncertainty items. Two tool fixes
(TF-4, CWO-1COR-05; TF-5, CWO-1COR-06 and -07) were installed by receipt; FIXUP-3 on all six parts landed, and the
orchestrator applied it into `SP\1Cor\fixup\draft_rows_fixup3_applied.jsonl`. GATE-E4 names S5 as the next check; no S4
ran. You authored none of the rows, the strategy, the tools, any fix-up, any ruling or any earlier review. This is a
spot review, not a lens: it does not count toward the strategy's section-11 lens record. Your readiness verdict decides
whether the book's review stage may end and the close lanes may begin.

## THE GATE YOU TEST (verbatim from `gate.s2_conditions` of the E4 rulings; the key keeps its round-1 name)

{{GATE}}

The first condition binds you directly: the readiness value is `fit` (the rows are fit as they stand) or
`fit_with_changes` (with every required change named by row). For the others the orchestrator's records say MET; you
test each one from the bytes and your own runs. A record is a claim, not a finding. `primaries_may_launch` is false and
stays false; a gate flip is the orchestrator's receipt act after your deliverable lands, not yours.

## LINE ENDINGS (ledger E-73; read this before you compare any digest)

The repository normalizes text to LF. Some digests recorded in this campaign were taken on CRLF bytes of files that
are now LF on disk; their content is otherwise the same. `SP\campaign\eol_digest_corrections.v1.jsonl` has one row per
affected pair. The extract's `orchestrator_measured` block classifies every (path, digest) pair it carries ({{EXTRACT_COUNTS}}).

When a recorded digest does not equal the sha256 of the bytes you read:
- compute the CRLF form yourself (normalize to LF, then replace each LF with CR LF) and hash it; if that equals the
  recorded digest, it is the E-73 class and NOT drift;
- if the path is a tool and a later receipt row in the extract records the digest now on disk, it is superseded and
  NOT drift;
- otherwise it IS drift: report it as a finding with both digests.
The digests in the PINNED INPUTS table below are all of the bytes now on disk; a mismatch there is a hard stop.

## PINNED INPUTS

Verify nothing you read has changed: these are the sha256 digests of the files as this brief was built.

{{PINS}}

**Read first:** `SP\1Cor\tools\TOOLKIT.md` and `SP\1Cor\book_strategy_1Cor.md` whole, then the E4 rulings file whole.
The strategy is BINDING; you judge the rows against it. Where the toolkit and a tool's code differ, the code is the
contract.

## Questions: answer every one, from the bytes and from your own runs

1. **TOOL-FIX RECEIPTS AND GATE FLIP (conditions 7, 8).** The extract carries the TF-4 and TF-5 installs, the coverage
   report and the gate flip that let FIXUP-3 launch. Does each install name the ruling that ordered it; does each sweep
   digest chain (`before_sha256`, `after_sha256`, the pre copy) hold, and does the last one equal the tool on disk; does
   each evidence digest match in LF or CRLF form; does the evidence support the `outcome` and `tests`? Re-run on private
   copies of the FIXUP-2 applied rows: `test_cwo05.py` (11 plants), `test_cwo0607.py` with `--pre` set to the TF-5 pre
   copy (10 plants), and `mutants_tf5.py`; compare each with its recorded result. Then PLANT in a private rows copy, by
   your own hand: one sentence that CWO-1COR-05's predicate must catch and a like sentence it must clear; one Greek run
   with a CWO-1COR-06 defect and a clean one; one disclosed variant verse absent from `variant_disclosed` for CWO-1COR-07
   and a listed one. Were TF-4, TF-5 and the gate flip recorded before every FIXUP-3 `launched_at` in the extract?
2. **FIXUP-3 SPANS (condition 12).** Diff a private copy of `SP\1Cor\fixup\draft_rows_fixup2_applied.jsonl` against the
   FIXUP-3 applied rows, field by field (list fields element by element), by `decision_id`. List every changed (row,
   field). Each must be licensed by an E4 order to that part, by S3-01 for W4, or by CWO-1COR-06 or -07, and must do what
   the order says and no more (read the part's pinned FIXUP-3 brief for the exact instruction). Every other field of
   every row must be byte-identical. Then, for every order that names exact spans, show from the row bytes, row by row,
   that each span is fixed (gone, or replaced as ordered), including S3-01's seven W4 spans; show that each RP and SBL
   slice in a changed field is unchanged or spliced from the witness. Compare your list with
   `fixup3_licence_table.v1.json`, the six `fixup3_W<n>_changes.json` files, the completion rows' `lander_checks` and the
   manifest. The licence table is a triage aid written by the orchestrator: its `outside_spans` hunks and its
   `row_named` class are where a change could outrun an order, so read those by hand. Confirm that each part's landed
   rows file equals the applied rows on that part's rows.
3. **SUITE, WRITER VALIDATOR, TILING, NGRAM7 (conditions 2-4).** On a private copy of the applied rows:
   `run_validator_suite.py` (report `hard_status`, each member's status, the triage flags and dead members);
   `check_tiling.py <copy> --range 1Cor.1.1-1Cor.16.24`; `ngram7.py` at gate 10 (read its argument handling first). Run
   `_validate_writer_part_1cor.py` on each part's rows and report any RED and its cause: the E4 record REPORTS a RED on
   index form only, which you test. Compare with the manifest's `suite_on_scratch_copy` and the post-FIXUP-3 report.
   Report every 7-gram shared by 7 or more rows as an early warning, classified as tool-induced boilerplate, a register
   defect or a needed disclosure.
4. **CORPUS-WIDE ORDERS (conditions 5-10).** Read CWO-1COR-01 and -02 in the E1 rulings, -04 in E2, -05 in E3, -06 and
   -07 in E4. Run the pinned sweep on a private copy, and also write your own scan from each order's stated predicate;
   compare both with `cwo_1cor_post_fixup3_report.v1.json` and explain any difference. Read by hand every CWO-1COR-01 B
   hit, every CWO-1COR-04 hit, every CWO-1COR-05 hit and every CWO-1COR-06 hit, and give your own class for each. The
   report carries the orchestrator's hand classes; test each. W6-013's false-positive class must be re-read against its
   new bytes (S3-05), and W1-011 re-classed against its new bytes. Recompute the rule-14 count of CWO-1COR-02 on all rows.
   For condition 9, list every sentence with the whole word REPORTED in the three named fields of any row and say what
   record it names. For condition 10, run the stated regex.
5. **CONFIDENCE AND COUNT (condition 11).** Show `confidence` for W6-007, W6-013 and W6-014 and for every other row
   against the FIXUP-2 applied rows, with the count of `high`.
6. **RULED FINDINGS.** For every ruling id in the E4 rulings ({{RULING_IDS}}), one status: `cured` (the rows or the
   installed tools now show the cure), `not_cured`, or `not_applicable` (rejected, recorded only, or routed elsewhere),
   with the evidence. Where an author reworded an ordered word to clear a suite flag, judge whether the order is met in
   substance. For each E4 unresolved-uncertainty item, say in one line whether the applied rows bear on it.
7. **CARRIED ITEMS.** `SP\1Cor\fixup\landed3\author_unresolved_for_S5.md` holds the orchestrator's digest of the six
   authors' open items. They are claims to test, not findings. For each, say what the bytes show, whether it needs a
   change, and the route (`no_change`, `fixup:W<n>`, `orchestrator_cwo`, `tool_fix`, `controlling_agent`,
   `fable_end_review`). Items E4 has already routed to Fable's end review need no second route, only a line saying the
   bytes still pose the question.
8. **CHANGED ROWS.** For every row FIXUP-3 changed: every maximal Greek run (the run pattern in `cor_lib.py`) in the
   changed fields is a byte substring of the RP line, or for a disclosed SBLGNT reading of the SBLGNT line, at the verse
   the row cites; every inline token (`web:`, `rp:`, `sbl:`) names a real verse; the section-8 register holds in the new
   words (no homiletics, no adjudicated divided reading, no positional or cross-part reference, no edition mark,
   chapter, verse, paragraph or punctuation deciding a seam); counts and universal claims carry a provenance tier; a
   removal left no broken sentence, dangling separator or orphaned reference, and every seam kept its ground. A count a
   row states and a script it names are checked against the witness bytes: count it yourself.
9. **UNTOUCHED ROWS, a sample for regressions.** At least 12 rows FIXUP-3 did not change, or the whole set if fewer, at
   least one per part where one exists, chosen by a rule you state before you look. For each: `unit_type` and its
   evidence, the strategy's granularity and split guards, `strongest_rejected_alternative` is a real rival argued from
   the bytes, section-8 register, provenance tiers. You are a fresh reader; report what you find even if no earlier
   review raised it.
10. **DIGESTS AND LANES (condition 13).** For every (path, sha256) pair in the extract's rows and in the manifest:
    classify match, CRLF form (E-73), superseded tool, or drift. Compare with the extract's `orchestrator_measured`
    block and say where you differ. From the extract's launch and completion rows, say how many 1 Corinthians launches
    lack completion rows, and whether more than three FIXUP-3 authors could have been in flight at once.
11. **READINESS.** `fit`, or `fit_with_changes` with every change listed by row, each with its route. There is no third
    value. If a gate condition is not met, that is `fit_with_changes` with the change that would meet it, at severity
    `blocker`.

## Deliverable: `{{OUT}}\{{DELIVERABLE}}`

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "readiness":"fit|fit_with_changes",
 "changes_required":[{"id":"S5-01","rows":["..."],"what":"...","route":"fixup:W<n>|orchestrator_cwo|tool_fix|controlling_agent|fable_end_review"}],
 "rows_file_reviewed":{"path":"SP\\1Cor\\fixup\\draft_rows_fixup3_applied.jsonl","sha256":"<digest you read>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "conditions":[{"n":1,"text":"<verbatim>","status":"met|not_met","evidence":"...","runs":["<tool + args -> result>"]}],
 "tool_fix_receipts":[{"id":"TF-4","ruling":"...","receipt_line":0,"tools":"match|superseded|drift","evidence_digests":"match|crlf_form|drift","fixture_rerun":"...","plant":{"planted":"...","with_plant":"...","without_plant":"..."},"installed_before_fixup":"...","verdict":"accept|defect","findings":["..."]}],
 "fixup3_spans":{"rows_changed":0,"fields_changed":0,"outside_licence":[],"beyond_order":[],"untouched_fields_identical":true,"landed_equals_applied":true,"agrees_with_change_records":true,"exact_spans":[{"ruling":"...","row":"...","field":"...","span_fixed":true,"evidence":"..."}],"verdict":"accept|defect","findings":["..."]},
 "suite":{"hard_status":"...","members":{},"triage_flags":0,"dead_members":[],"writer_validator":{},"tiling":"...","ngram7":"...","agrees_with_records":true,"ngram_early_warnings":[]},
 "cwo":{"CWO-1COR-01":{"A":0,"B":0,"b_hits_read_by_hand":0,"my_classes":[{"row":"...","field":"...","class":"...","evidence":"..."}]},"CWO-1COR-02":{"fail":0,"of":0},"CWO-1COR-04":{"hits":0,"support_use_open":0,"count_excess_open":0,"units_read_by_hand":0,"my_classes":[]},"CWO-1COR-05":{"hits":0,"open_true":0,"my_classes":[]},"CWO-1COR-06":{"hits":0,"open_true":0,"my_classes":[]},"CWO-1COR-07":{"unlisted":0},"reported_sentences":[{"row":"...","field":"...","record_named":"..."}],"self_citation_regex_hits":0,"differences":[],"verdict":"accept|defect"},
 "confidence":{"high_count":0,"W6-007":"...","W6-013":"...","W6-014":"...","other_rows_changed":[]},
 "ruled_findings":[{"id":"...","status":"cured|not_cured|not_applicable","evidence":"..."}],
 "unresolved_uncertainty_bearing":[{"item":"...","bears":"yes|no","note":"..."}],
 "carried_items":[{"item":"...","rows":["..."],"bytes_show":"...","change_needed":true,"route":"..."}],
 "changed_rows":[{"row":"...","fields":["..."],"bytes":"accept|defect","tokens":"accept|defect","register":"accept|defect","findings":["..."]}],
 "untouched_sample":{"selection_rule":"...","rows":[{"row":"...","verdict":"accept|defect","findings":["..."]}]},
 "digests":{"pairs":0,"match":0,"crlf_form":0,"superseded":0,"drift":[],"differs_from_orchestrator":[],"launches_without_completion":0},
 "new_findings":[{"id":"S5-01","severity":"blocker|major|minor|note","row_or_artifact":"...","claim":"...","evidence":"...","suggested_fix":"...","route":"fixup:W<n>|orchestrator_cwo|tool_fix|controlling_agent|fable_end_review"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Do the deterministic parts (questions 2, 3, 4, 5, 8, 10 and the sample selection) with a few scripts of your own in
`work\`, written with the Write tool, so their output is a summary and not a dump. Keep to roughly 120 tool calls.
Report exactly what you ran and what it returned; a claimed tool run that did not happen is the worst thing you can
put in a record.

## YOUR FINAL MESSAGE (evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "deviations":["<any tool-internal data file you opened, any failed write, anything outside this brief>"],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named; opened no transcript",
 "readiness":"...","new_finding_count":0,"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
