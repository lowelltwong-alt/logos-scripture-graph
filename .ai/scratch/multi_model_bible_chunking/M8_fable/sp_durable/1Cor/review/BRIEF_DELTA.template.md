# {{LANE}}: FRESH DISTINCT DELTA CHECK of the 1 Corinthians {{ROUND}} applied rows (M8_fable, hard-book track)

You are the DISTINCT CHECKER {{LANE}} for 1 Corinthians. The work is candidate-only, NON-AUTHORIZING research. This brief
is binding. Attempt `{{ATTEMPT}}`, execution `{{EXECUTION}}`. You run on claude-opus-5-5 (OW-25).

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
- Every file you write goes under `{{OUT}}`: the deliverable at the exact path above, and your scripts, private copies
  and tool reports under `{{OUT}}\work\`. Never run git, never write a receipt, never touch any registry.
- **FORBIDDEN:** every path not named in this brief, including other models' directories, other books, the Greek
  apparatus and Swete directories, every receipt file, every earlier review and its prose, and all author output. You
  judge from the bytes, the rulings and your own runs. A record of what someone did is a claim to test.
- **Running Python:** set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`, and run `python -B`.
- **The tools you may RUN**, each only on PRIVATE COPIES of rows under `{{OUT}}\work\` and with every output path under
  `{{OUT}}\work\`, are: `SP\1Cor\tools\check_tiling.py` (`COPY --range 1Cor.1.1-1Cor.16.24`), `SP\1Cor\tools\ngram7.py`
  (`COPY --gate 10 --full-ids`), `SP\1Cor\tools\run_validator_suite.py` (`COPY`; it writes
  `<copy>.validator_report.json` beside its input) and `SP\1Cor\review\cwo_sweep_1cor.py` (`COPY --out FILE.json`). Run
  each from a working directory under your `work\`. Every other pinned file is READ ONLY.

## What happened, and the one deviation you must test

The rows reached the controlling round {{CONTROLLING}}, which issued byte-exact orders. The gate named the fix-up authors
as recipients. No author ran. The orchestrator applied the orders mechanically from the rulings file with
`SP\campaign\_apply_exact_orders.py`. Treat that as a stated deviation and a claim. Its stated reason is that every
author order carries exact spans, so an author would have had nothing to write. Your job includes testing that reason.
You authored none of the rows, tools or rulings. This is a delta check, not a lens, and it does not count toward the
strategy's section-11 lens record.

## THE GATE YOU TEST (verbatim from `gate.s2_conditions` of the rulings; the key keeps its round-1 name)

{{GATE}}

`primaries_may_launch` is false and stays false. A gate flip is the orchestrator's act after your deliverable lands.

## PINNED INPUTS

Each digest is of the bytes on disk as this brief was built. A mismatch is a hard stop.

{{PINS}}

**Read first:** the rulings file whole. It is the only standard here. Do not read the rows file whole; extract the
changed elements with your own script.

## Questions: answer each from the bytes and from your own runs

1. **CONDITIONS 1 TO 7.** For each, status `met` or `not_met`, with evidence and the runs behind it. Condition 7 binds
   your own readiness wording. Write your own comparison script. Do not import or reuse the apply tool.
2. **THE DEVIATION.** Read the FULL text of every author order, not only its spans. Is anything ordered beyond what its
   spans carry: a further edit, a condition, a duty to choose words, a duty to re-check something? List each order with
   `covered_by_spans` true or false. A false is a `fit_with_changes` change, at severity `blocker`.
3. **THE CHANGED TEXT.** Read every changed element whole, in its row, beside the FIXUP-3 element. Does each new sentence
   read as grammatical English and say what the ruling meant? Does it fit the row's verse range? Does any Greek token,
   citation or count it carries agree with the row's own substrate? Say so element by element, each with `accept` or
   `defect`.
4. **THE MANIFEST.** Do its source digest, its rulings digest, its element list and its `suite_on_copy` figures agree
   with what you measured? Any difference is a finding.
5. **OTHER ORDERS.** The rulings also send orders to `s6`, `orchestrator` and `fable_end_review`. Carry out the two `s6`
   orders. For the rest, say only whether the rows must change now to honour one. Do not judge the routed items.
6. **READINESS.** `fit`, or `fit_with_changes` with every change listed by row and route. There is no third value. A
   condition not met is `fit_with_changes` at severity `blocker`. Do not reopen rulings. Report a matter outside this
   delta as a `note`, routed `fable_end_review`, and it does not affect readiness.

## Deliverable: `{{OUT}}\{{DELIVERABLE}}`

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "readiness":"fit|fit_with_changes",
 "changes_required":[{"id":"{{LANE}}-01","rows":["..."],"what":"...","route":"fixup:W<n>|orchestrator_cwo|tool_fix|controlling_agent|fable_end_review"}],
 "rows_file_reviewed":{"path":"SP\\1Cor\\fixup\\{{APPLIED_NAME}}","sha256":"<digest you read>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "conditions":[{"n":1,"text":"<verbatim>","status":"met|not_met","evidence":"...","runs":["<tool + args -> result>"]}],
 "spans":{"rows_changed":0,"elements_changed":0,"outside_licence":[],"equal_to_licensed_set":true,"exact_spans":[{"ruling":"...","row":"...","field":"...","span_fixed":true}],"verdict":"accept|defect"},
 "orders":[{"ruling":"...","to":"...","covered_by_spans":true,"note":"..."}],
 "changed_text":[{"row":"...","field":"...","verdict":"accept|defect","findings":["..."]}],
 "manifest":{"agrees":true,"differences":[]},
 "suite":{"hard_status":"...","members":{},"dead_members":[],"ngram7":"...","tiling":"...","refs_mirror_worklist":[]},
 "cwo":{"pre":{},"post":{},"changed_classes":[]},
 "new_findings":[{"id":"{{LANE}}-01","severity":"blocker|major|minor|note","row_or_artifact":"...","claim":"...","evidence":"...","suggested_fix":"...","route":"fixup:W<n>|orchestrator_cwo|tool_fix|controlling_agent|fable_end_review"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Roughly 30 tool calls. Use a few scripts of your own in `work\`, written with the Write tool, whose output is a summary
and not a dump. Report exactly what you ran and what it returned. A claimed run that did not happen is the worst thing
you can put in a record.

## YOUR FINAL MESSAGE (evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "deviations":["<anything outside this brief>"],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named; opened no transcript",
 "readiness":"...","new_finding_count":0,"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
