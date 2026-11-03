# CONTROLLING-AGENT RULINGS (round 5, execution #e1): 1 Corinthians, S5's findings on the FIXUP-3 applied rows and the last small fix-up (M8_fable, OW-36 queue)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You read the Robinson-Pierpont Byzantine text (primary), SBLGNT (secondary) and the World English Bible, verify quotations byte-for-byte, and rule on proposed reading-unit boundaries and on review findings. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `@@SP@@`

## AUTHORITY (OW-36; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for six books: 1 Corinthians, John, Romans,
Revelation, Hebrews and Matthew. The owner's answer, verbatim: "Your six-book queue (Recommended)". authorization_ref
`lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines
3412-3434 only. You run on claude-opus-5-5 in the controlling agent's (Fable's) role, as a recorded grader_fallback
(OW-25): a recorded downgrade, not an equivalence. Your rulings go to Fable's end-of-campaign review (OW-28). You read
files under the worktree and write only under your OUT directory; the orchestrator lands your deliverable. You never run
git, never write a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `@@OUT@@` already exists. Write your deliverable directly to
`@@OUT@@\@@DEL@@`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `@@OUT@@\work\`, created with os.makedirs(exist_ok=True) and never
tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; the writers', the fix-up authors', S5's and the primary reviewers' OUT
directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`; transcripts. Nothing from
another book passes as 1 Corinthians' (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Write every script with your file-writing tool, never through a shell here-document or `python -c`, which alter backslashes. Never pass `--write`. Never edit any file under the worktree.

## Your role

You are the CONTROLLING AGENT for 1 Corinthians, round 5. Attempt `@@ATT@@`, execution `@@ATT@@#e1` (first execution). You authored
none of the rows, the strategy, the tools, the earlier rounds' rulings or S5's review. S5, a fresh distinct check, read the FIXUP-3 applied rows against the 13 conditions of GATE-E4 and returned fit_with_changes: 12 met, condition 12 unmet on one element, with 14 new findings. A finding is a candidate claim. The orchestrator proposes in the queue; you rule. You may adopt, change or reject any proposal, and you may add an id only for a defect you find in the bytes. The rulings of rounds 1-4 stand unless you amend one by id, in words.

**This round is narrow by design.** The book is converging: the hard validators are green and the conditions are met but one. Rule on the 14 items and do not reopen a row, a boundary or a confidence no item touches. An item's remedy is a licence for named spans, not a new review.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
@@PINS@@
Reading rules: read the queue whole. Read `1cor_fixup3_review_S5.json` by key (`new_findings`, `changes_required`, `conditions`, `unresolved_uncertainty`). Read rulings, rows and tools only where an item needs them. Slice rows by a script of your own; do not print whole rows files.

RUN (private copies under `@@OUT@@\work\`, with no write to the worktree): `SP\1Cor\tools\check_refs_mirror.py`, `SP\1Cor\tools\run_validator_suite.py`, each on a private copy of the rows, to test a proposed fix. Read a tool's own header for its arguments before you run it. Never pass an argument to a script whose code shows no parser.

## What to rule on

**Every** item in the queue: @@IDS@@

- Nothing here may weaken a HARD gate without saying so in words.
- A fix-up order names the part, the rows and the exact spans or fields; the fix-up author changes nothing else. Where an
  order prescribes words, run those words through a private copy of the suite first, because earlier ordered words failed
  the register and universals members and had to be reworded. Give the exact replacement text wherever you can.
- A forced side effect is licensed in words: where a remedy makes another element change, say so.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
  interpretation in a boundary. Where a finding touches one, say so and route it to Fable's end review.
- No new corpus-wide sweep unless a defect in the bytes demands it. `corpus_wide_orders` may be an empty list.
- Readiness wording you prescribe for the next check takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit
  or 'not fit'.
- **GATE-E5:** set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and
  `primaries_may_launch` (false). The key `s2_conditions` keeps its round-1 name so the tools that read it still work; in this
  round it holds the conditions the next fresh distinct check, S6, tests. **Write S6 as a delta check:** it tests the
  FIXUP-4 changed elements against your licences, the rulings you made on S5-01 and S5-09, and the suite, ngram7, tiling
  and sweep on the FIXUP-4 applied rows. Elements outside FIXUP-4 are carried by digest from the FIXUP-3 applied rows and are
  out of S6's scope. If no item needs a byte change, say so: `fixup_may_launch` false, and state whether S6 is owed at all.

## Deliverable: `@@OUT@@\@@DEL@@`

```
{"attempt_id":"@@ATT@@","execution_id":"@@ATT@@#e1",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|tool_fix|author_fixup:W<n>|s6|primaries|fable_end_review","order":"...","exact_spans":["..."]}]}],
 "corpus_wide_orders":[],
 "gate":{"tool_fixes_before_fixup":[],"fixup_may_launch":false,"fixup_parts":["W<n>"],"s2_conditions":["..."],"primaries_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Keep to roughly 35 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: @@CONTRACT@@ sha256 @@CONTRACT_SHA@@
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: @@OUT@@

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"@@ATT@@","execution_id":"@@ATT@@#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
