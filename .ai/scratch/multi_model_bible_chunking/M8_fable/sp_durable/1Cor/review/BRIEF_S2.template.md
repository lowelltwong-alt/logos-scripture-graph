# S2: FRESH DISTINCT-CHECKER REVIEW of the 1 Corinthians FIXUP-1 applied rows (M8_fable, hard-book track)

You are the DISTINCT CHECKER S2 for 1 Corinthians. The work is candidate-only, NON-AUTHORIZING research. This brief is
binding. Attempt `{{ATTEMPT}}`, execution `{{EXECUTION}}`. You run on claude-opus-5-5 (OW-25).

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
  `greek_substrate\`; the writers' and the fix-up authors' OUT directories, their final messages (`final_*.json`) and
  every receipt file other than the extract pinned below; the S1 review deliverable and its prose. You judge the rows
  from the bytes, the strategy, the rulings and your own runs. A record of what someone did is a claim to test.
- **Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` in the
  environment and run `python -B`. The suite and the fixtures start child processes; without the variable a child
  could write bytecode under SP, which is a write under SP.
- **The tools you may RUN** are exactly these, each on PRIVATE COPIES of rows under `{{OUT}}\work\` and with every
  output path under `{{OUT}}\work\`:
  `SP\1Cor\tools\check_tiling.py`, `SP\1Cor\tools\ngram7.py`, `SP\1Cor\tools\run_validator_suite.py` (it writes
  `<copy>.validator_report.json` beside its input, so it must only ever see a copy in your `work\`),
  `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py` (it writes nothing), `SP\1Cor\review\cwo_sweep_1cor.py`
  (`ROWS.jsonl --out FILE.json`; `--out` under your `work\` only), and the two fixture scripts
  `SP\1Cor\review\tool_fixes\fixtures_tf1.py` and `fixtures_tf2.py` (read each docstring for its arguments; `--work`
  must be a directory under your `work\`; they run `_exec_as.py`, which writes nothing). You may import
  `SP\1Cor\tools\cor_lib.py` from your own scripts. Every other pinned tool is READ ONLY: `normalize_greek_in_json.py
  --write` and other tools under `SP\1Cor\tools\` write files when run.

## Your role

Six writer parts tiled the 437 WEB verses; S1 reviewed the combined draft; a controlling execution ruled on S1's
findings once (E1: {{N_RULINGS}} rulings, {{N_UNRES}} unresolved-uncertainty items, {{N_CWO}} corpus-wide orders); two
tool fixes (TF-1 for S1-07, TF-2 for S1-08) were installed by receipt; FIXUP-1 on W2, W3, W4, W5 and W6 landed, and the
orchestrator applied it into `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl` ({{ROWS_N}} rows). You authored none of the
rows, the strategy, the tools, any fix-up, any ruling or any earlier review. Your readiness verdict decides whether the
two blind row-review lanes and the reception-tradition lens may launch on these rows. This is a spot review, not a lens:
it does not count toward the strategy's §11 lens record.

## THE GATE YOU TEST (verbatim from `gate.s2_conditions` of the E1 rulings)

{{GATE}}

The last condition binds you directly: the readiness value is `fit` (the rows are fit as they stand) or
`fit_with_changes` (with every required change named by row). For the others the orchestrator's records say MET; you
test each one from the bytes and your own runs. A record is a claim, not a finding. The gate's `primaries_may_launch`
is false; flipping it is the orchestrator's receipt act after your deliverable lands, not yours.

## LINE ENDINGS (ledger E-73; read this before you compare any digest)

The repository normalizes text to LF. Some digests recorded in this campaign were taken on CRLF bytes of files that
are now LF on disk; their content is otherwise the same. `SP\campaign\eol_digest_corrections.v1.jsonl` has one row per
affected pair: `path`, `recorded_sha256`, `canonical_lf_sha256`, `recorded_in`, `recorded_in_row`. The extract's
`orchestrator_measured` block classifies every (path, digest) pair it carries; the orchestrator MEASURED {{EXTRACT_COUNTS}}.

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

**Read first:** `SP\1Cor\tools\TOOLKIT.md` and `SP\1Cor\book_strategy_1Cor.md` whole, then the E1 rulings file whole.
The strategy is BINDING; you judge the rows against it. Where the toolkit and a tool's code differ, the code is the
contract.

## Questions: answer every one, from the bytes and from your own runs

1. **TOOL-FIX RECEIPTS.** The receipts are rows 7 (TF-1, ruling S1-07) and 8 (TF-2, ruling S1-08) of the review
   receipts, copied in `SP\1Cor\review\tool_fixes\s2_receipt_extract.v1.json`; row 9 is the gate flip that let FIXUP-1
   launch. For each: does the receipt name the ruling that ordered it; does each tool's `after_sha256` equal the tool
   on disk and `before_sha256` its pinned pre copy; does each evidence digest match in LF or CRLF form; does the
   evidence support the receipt's `outcome` and `tests`? Re-run each fixture script yourself (`--work` under your
   `work\`; `--baseline` the pinned pre copy with its digest) and compare with the recorded result. Then PLANT: for
   TF-1, one index gap in a private slice must go RED in `--book-index` mode and GREEN without it; for TF-2, confirm
   from the code and a run that the narrowing strips only what the receipt says it strips, and that a planted repeated
   7-gram of ordinary prose at the gate count still goes RED. Were both installed before any FIXUP-1 launch (compare
   `recorded_at` of rows 7-9 with `launched_at` of the FIXUP-1 launch rows in the extract)?
2. **FIXUP-1 SPANS.** Diff a private copy of `SP\1Cor\writer\draft_rows_combined.jsonl` against the applied rows, field
   by field, by `decision_id`. List every changed (row, field). Each must appear in the `allowed` list of its part's
   licence map, inlined in the extract's FIXUP-1 launch rows (`allowed_change_map.inlined`), and the change must do
   what the cited rulings or corpus-wide orders ordered, and no more (read the part's pinned fix-up brief for the
   exact instruction). Every other field of every row must be byte-identical. Report anything outside. Confirm that
   each part's landed rows file equals the applied rows on that part's rows, and compare your list with the five
   `fixup1_W<n>_changes.json` files, the completion rows' `lander_checks` and the manifest.
3. **SUITE, TILING, NGRAM7 (gate conditions on the suite, ngram7 and tiling).** On a private copy of the applied rows:
   `run_validator_suite.py` (report `hard_status`, each member's status, the triage flags and dead members);
   `check_tiling.py <copy> --range 1Cor.1.1-1Cor.16.24`; `ngram7.py` at gate 10 as TF-2 installed it (read its argument
   handling first). Compare with the manifest's `suite_on_scratch_copy` and the post-fixup report's `CWO-1COR-03`
   block. Report every 7-gram shared by 7 or more rows as an early warning, classified as tool-induced boilerplate, a
   register defect or a needed disclosure.
4. **CORPUS-WIDE ORDERS (the two CWO report conditions).** Read the {{N_CWO}} orders in `corpus_wide_orders` of the E1
   rulings. Run the pinned sweep on a private copy, and also write your own scan from each order's stated predicate;
   compare both with `SP\1Cor\review\cwo_1cor_post_fixup1_report.v1.json` (and its baseline,
   `cwo_1cor_baseline_report.v1.json`) and explain any difference. Read every hit the post report lists by hand and give
   your own class. Two of its classes are marked INFERRED by the orchestrator (the hits in W3-006 and W6-005 that it
   classed compliant because their pilcrow sentence "informs" and does not decide); test those two against the
   order's predicate and the strategy's device rulings. Recompute the rule-14 count of the second order on all rows.
5. **RULED FINDINGS.** For every ruling id in the E1 rulings ({{RULING_IDS}}), one status: `cured` (the rows or the
   installed tools now show the cure), `not_cured`, or `not_applicable` (rejected, recorded only, or routed elsewhere),
   with the evidence. For each unresolved-uncertainty item, say in one line whether the applied rows bear on it.
6. **CARRIED ITEMS.** The fix-up authors reported the following. They are lane reports, not adjudicated: claims to
   test, not findings. For each, say what the bytes show, whether it needs a change, and the route
   (`no_change`, `fixup:W<n>`, `orchestrator_cwo`, `tool_fix`, `controlling_agent`, `fable_end_review`):
   a. W3-004.boundary_rationale: an edit licensed by S1-05 (the text "in 1Cor 8:1-11:1") was not made because, the
      author reports, `check_refs_mirror` would then read an argued citation the row's refs do not carry, and adding a
      ref was outside the licence.
   b. W3-001 keeps a chapter-fallback cap mention; the author reports that deleting it turns `cap_sweep` (E-02) RED,
      a conflict with S1-06.
   c. Deletions in W3 `device_notes` joined two untouched sentences into 2 junction 7-grams on 7 rows (below gate 10).
   d. W5 and W6 left WEB-paragraph and pilcrow mentions that their licences did not cover byte-identical; strategy §8
      rule 4 may bear on them. Find every such mention in W5 and W6 and judge each.
   e. W6 applied its own reading of S1-01b ("at most one bare pilcrow location item"); judge whether the rows meet
      the ruling's text.
   f. The W5-010 and W5-014 rewordings: check their register, tiers and evidence.
   g. W2-015 keeps `frontier_flag_considered` true (S1-05 permitted false, did not require it), and its new
      `device_notes` sentence may restate content already in the row.
   h. W4-001 and W4-003 `boundary_evidence_refs[0]`: two `rp:` refs still read that the RP pilcrow at 11:2 / 11:17
      "agrees and decides nothing"; the author reports that curing them needs an order licensing a ref-element edit.
   i. W4-003's rationale still names the WEB paragraph start at 11:23 although its `web:` ref for 11:23 was deleted.
7. **CHANGED ROWS.** For every row FIXUP-1 changed: every maximal Greek run (the run pattern in `cor_lib.py`) in the
   changed fields is a byte substring of the RP line, or for a disclosed SBLGNT reading of the SBLGNT line, at the
   verse the row cites; every inline token (`web:`, `rp:`, `sbl:`) names a real verse; the §8 register holds in the
   new words (no homiletics, no adjudicated divided reading, no positional or cross-part reference, no edition mark,
   chapter, verse, paragraph or punctuation deciding a seam); counts and universal claims carry a provenance tier.
8. **UNTOUCHED ROWS, a sample for regressions.** At least 12 rows no fix-up changed, at least one per part W1-W6,
   chosen by a rule you state before you look (for example every sixth row by `chunk_index_in_book`). For each:
   `unit_type` and its evidence, the strategy's granularity and split guards, `strongest_rejected_alternative` is a
   real rival argued from the bytes, §8 register, provenance tiers. You are a fresh reader; report what you find even
   if no earlier review raised it.
9. **DIGESTS.** For every (path, sha256) pair in the extract's rows and in the manifest: classify match, CRLF form
   (E-73), superseded tool, or drift. Compare with the extract's `orchestrator_measured` block and say where you
   differ.
10. **READINESS.** `fit`, or `fit_with_changes` with every change listed by row, each with its route. There is no third
   value. If a gate condition is not met, that is `fit_with_changes` with the change that would meet it, at severity
   `blocker`.

## Deliverable: `{{OUT}}\{{DELIVERABLE}}`

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "readiness":"fit|fit_with_changes",
 "changes_required":[{"id":"S2-01","rows":["..."],"what":"...","route":"fixup:W<n>|orchestrator_cwo|tool_fix|controlling_agent|fable_end_review"}],
 "rows_file_reviewed":{"path":"SP\\1Cor\\fixup\\draft_rows_fixup1_applied.jsonl","sha256":"<digest you read>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "conditions":[{"n":1,"text":"<verbatim>","status":"met|not_met","evidence":"...","runs":["<tool + args -> result>"]}],
 "tool_fix_receipts":[{"id":"TF-1","ruling":"S1-07","receipt_row":7,"tools":"match|superseded|drift","evidence_digests":"match|crlf_form|drift","fixture_rerun":"...","plant":{"planted":"...","with_plant":"...","without_plant":"..."},"installed_before_fixup":"...","verdict":"accept|defect","findings":["..."]}],
 "fixup1_spans":{"rows_changed":0,"fields_changed":0,"outside_licence":[],"beyond_order":[],"untouched_fields_identical":true,"landed_equals_applied":true,"agrees_with_change_records":true,"verdict":"accept|defect","findings":["..."]},
 "suite":{"hard_status":"...","members":{},"triage_flags":0,"dead_members":[],"tiling":"...","ngram7":"...","agrees_with_records":true,"ngram_early_warnings":[]},
 "cwo":{"CWO-1COR-01":{"A":0,"B":0,"support_use_open":0,"hits_read_by_hand":0,"my_classes":[{"row":"...","field":"...","class":"...","evidence":"..."}]},"CWO-1COR-02":{"fail":0,"of":0},"CWO-1COR-03":"...","differences":[],"verdict":"accept|defect"},
 "ruled_findings":[{"id":"...","status":"cured|not_cured|not_applicable","evidence":"..."}],
 "unresolved_uncertainty_bearing":[{"item":"...","bears":"yes|no","note":"..."}],
 "carried_items":[{"item":"a","rows":["..."],"bytes_show":"...","change_needed":true,"route":"..."}],
 "changed_rows":[{"row":"...","fields":["..."],"bytes":"accept|defect","tokens":"accept|defect","register":"accept|defect","findings":["..."]}],
 "untouched_sample":{"selection_rule":"...","rows":[{"row":"...","verdict":"accept|defect","findings":["..."]}]},
 "digests":{"pairs":0,"match":0,"crlf_form":0,"superseded":0,"drift":[],"differs_from_orchestrator":[]},
 "new_findings":[{"id":"S2-01","severity":"blocker|major|minor|note","row_or_artifact":"...","claim":"...","evidence":"...","suggested_fix":"...","route":"fixup:W<n>|orchestrator_cwo|tool_fix|controlling_agent|fable_end_review"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Do the deterministic parts (questions 2, 3, 4, 7, 9 and the sample selection) with a few scripts of your own in
`work\`, written with the Write tool, so their output is a summary and not a dump. Keep to roughly 100 tool calls.
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
