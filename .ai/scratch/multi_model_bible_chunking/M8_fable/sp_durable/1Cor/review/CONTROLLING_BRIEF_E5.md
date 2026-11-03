# CONTROLLING-AGENT RULINGS (round 5, execution #e1): 1 Corinthians, S5's findings on the FIXUP-3 applied rows and the last small fix-up (M8_fable, OW-36 queue)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You read the Robinson-Pierpont Byzantine text (primary), SBLGNT (secondary) and the World English Bible, verify quotations byte-for-byte, and rule on proposed reading-unit boundaries and on review findings. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-36; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for six books: 1 Corinthians, John, Romans,
Revelation, Hebrews and Matthew. The owner's answer, verbatim: "Your six-book queue (Recommended)". authorization_ref
`lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines
3412-3434 only. You run on claude-opus-5-5 in the controlling agent's (Fable's) role, as a recorded grader_fallback
(OW-25): a recorded downgrade, not an equivalence. Your rulings go to Fable's end-of-campaign review (OW-28). You read
files under the worktree and write only under your OUT directory; the orchestrator lands your deliverable. You never run
git, never write a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl5` already exists. Write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl5\1cor_controlling_agent_rulings_r5_e1.v1.json`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl5\work\`, created with os.makedirs(exist_ok=True) and never
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

You are the CONTROLLING AGENT for 1 Corinthians, round 5. Attempt `cor_controlling_rulings_r5_a1`, execution `cor_controlling_rulings_r5_a1#e1` (first execution). You authored
none of the rows, the strategy, the tools, the earlier rounds' rulings or S5's review. S5, a fresh distinct check, read the FIXUP-3 applied rows against the 13 conditions of GATE-E4 and returned fit_with_changes: 12 met, condition 12 unmet on one element, with 14 new findings. A finding is a candidate claim. The orchestrator proposes in the queue; you rule. You may adopt, change or reject any proposal, and you may add an id only for a defect you find in the bytes. The rulings of rounds 1-4 stand unless you amend one by id, in words.

**This round is narrow by design.** The book is converging: the hard validators are green and the conditions are met but one. Rule on the 14 items and do not reopen a row, a boundary or a confidence no item touches. An item's remedy is a licence for named spans, not a new review.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\1Cor\review\1cor_controlling_agent_queue_e5.v1.json` | `a33ed9108f6543d0fc43692c8869ace1812b584c19e8cae571ccd848a274d8d1` |
| `SP\1Cor\review\1cor_fixup3_review_S5.json` | `5162f92b1819320f80bee089568a39e2264ec842da7833c3a03be32f6b8a99fe` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E4.v1.json` | `33ac57245ee930b1484a1227fc019e11c6f082b5c984a20ecc9e7c765d463187` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E3.v1.json` | `a7f32674dee0b0e27f25803729f93142cefdaf2847f9d7122010397e992efe70` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E2.v1.json` | `1299a598b60bbf3c8fb193381ead098e394242a713d8bac4e584b39fdf0e0541` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json` | `93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90` |
| `SP\1Cor\fixup\draft_rows_fixup3_applied.jsonl` | `c21035080156a2ef0ee79e2384ec9aa8985e62e00d421277898a7f475490e03c` |
| `SP\1Cor\fixup\draft_rows_fixup3_applied.manifest.json` | `170264a506b4cd144b5d65e74f545086b33791ec1bb51c8cb8cee3e434414ca5` |
| `SP\1Cor\fixup\fixup3_licence_table.v1.json` | `c1dea0d79a4b0af355b30f19bd0363b748dfe2b8e552b7dfd9b594cd1e078fd9` |
| `SP\1Cor\fixup\landed3\author_unresolved_for_S5.md` | `e9b6fd2b8c33f87b89a77a6400151134a0534efb1ceb1b2c916a4dc1a0abcf00` |
| `SP\1Cor\review\cwo_1cor_post_fixup3_report.v1.json` | `46e43ad5bd1ca4836c8b61cfe6f4daf394de37677a6187ff8147fd6cce230208` |
| `SP\1Cor\book_strategy_1Cor.md` | `70e344fed9f0f64654baa97dff80e03b706a1288b47de182628dc453212e39ca` |
| `SP\1Cor\strategy_plan_1Cor.json` | `a55044ceabc4dabd43a7e442ad7dfafb2268700a56904f3734d8c1bf5ab93ca4` |
| `SP\1Cor\tools\TOOLKIT.md` | `49de0883f5cbed7fd9e25fdc8a156a083f8794bdd6490de1b0eee82aa2c7361e` |
| `SP\1Cor\1Cor_rp.txt` | `94f7cf39fbd87f7952aba3ca957b7a4790edfb5d120dceffc8deac0ad0ccc2eb` |
| `SP\1Cor\1Cor_sbl.txt` | `354b6dcf5b5f43a24dd85918e9759eeeb3153dc5284ab707a4167b64919456ff` |
| `SP\1Cor\1Cor_web_clean.txt` | `7c8224ccf9eb0a06df20c5b2289d33ea32267dda136e88e73ea5761807cf0778` |
| `SP\1Cor\tools\check_refs_mirror.py` | `6784d4efcf6820d4495c8ba8d66ce505daa473e4c13882b352476f12654ca285` |
| `SP\1Cor\tools\run_validator_suite.py` | `ebe7197b35635d9f8cbf88914219003e32816ba37173f00205668eb5aab2dbb4` |
| `SP\1Cor\fixup\landed3\W3_e1\measure_w3b.py` | `9e625b63b3b594f4f0be01dca0fae32fd6a4a9f96817ef49af61a76baa8c0460` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `6203b792d859de99869799119e00831db6c4534b9326451936d2b21ab5e5fa04` |

Reading rules: read the queue whole. Read `1cor_fixup3_review_S5.json` by key (`new_findings`, `changes_required`, `conditions`, `unresolved_uncertainty`). Read rulings, rows and tools only where an item needs them. Slice rows by a script of your own; do not print whole rows files.

RUN (private copies under `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl5\work\`, with no write to the worktree): `SP\1Cor\tools\check_refs_mirror.py`, `SP\1Cor\tools\run_validator_suite.py`, each on a private copy of the rows, to test a proposed fix. Read a tool's own header for its arguments before you run it. Never pass an argument to a script whose code shows no parser.

## What to rule on

**Every** item in the queue: R5-S5-01, R5-S5-02, R5-S5-03, R5-S5-04, R5-S5-05, R5-S5-06, R5-S5-07, R5-S5-08, R5-S5-09, R5-S5-10, R5-S5-11, R5-S5-12, R5-S5-13, R5-S5-14

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

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl5\1cor_controlling_agent_rulings_r5_e1.v1.json`

```
{"attempt_id":"cor_controlling_rulings_r5_a1","execution_id":"cor_controlling_rulings_r5_a1#e1",
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
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl5

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_controlling_rulings_r5_a1","execution_id":"cor_controlling_rulings_r5_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
