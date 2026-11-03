# CONTROLLING-AGENT RULINGS (round 2, execution #e1): 1 Corinthians, S2's required changes, the class rulings and the next fix-up wave's scope (M8_fable, OW-36 queue)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl2` already exists. Write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl2\1cor_controlling_agent_rulings_r2_e1.v1.json`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl2\work\`, created with os.makedirs(exist_ok=True) and never
tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; the writers', the fix-up authors', S1's and S2's OUT
directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`; transcripts. Nothing from
another book passes as 1 Corinthians' (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the CONTROLLING AGENT for 1 Corinthians, round 2. Attempt `cor_controlling_rulings_r2_a1`, execution `cor_controlling_rulings_r2_a1#e1` (first execution). You authored
none of the rows, the strategy, the tools, the round-1 rulings or the reviews. S2, a fresh distinct checker, read
the FIXUP-1 applied rows and recorded readiness fit_with_changes: 13 changes
required and 15 new findings (4 major, 9 minor, 2 note). The orchestrator's queue proposes a ruling for each finding and for the
gate. The orchestrator proposes; you rule. You may adopt, change or reject any proposal, and you may add an id only for a
defect you find in the bytes. The round-1 rulings in `1cor_controlling_agent_rulings_E1.v1.json` stand unless you amend one by id, in words.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\1Cor\review\1cor_controlling_agent_queue_e2.v1.json` | `9025fffbbc06c44d6dc68788b13dfdd330b0f71965c774f34b652283c13c572a` |
| `SP\1Cor\review\1cor_fixup_wave_review_S2.json` | `240655556559bdf67b66ee6a2d4ea62e21104a7d6f0eb7d42107878d4766a3f3` |
| `SP\1Cor\review\BRIEF_S2.md` | `afbac2e3c98c23fcca8778858ab24c51563b852ba8a7ccdb692ed841cb0a24f0` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json` | `93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90` |
| `SP\1Cor\review\tool_fixes\s2_receipt_extract.v1.json` | `9ad1feba9373ea88fa4b572397413b7dc210050fca3483c9cdf5dc13e8d0f06f` |
| `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl` | `646f9eeaad82edaf0f4d1f6651ba1f7b06fbbefe0f3d8da1d0e07a4e7d8f8eec` |
| `SP\1Cor\fixup\draft_rows_fixup1_applied.manifest.json` | `05ee28d40fd88980cabce536ce2fda63e251f58c0eb8840a210113b3d6cb059c` |
| `SP\1Cor\review\cwo_1cor_post_fixup1_report.v1.json` | `ee3170b0f37688090ed87128fa1e77a71f3dd60d58adc8c4de9d081df53fcc2b` |
| `SP\1Cor\review\cwo_sweep_1cor.py` | `c6be0cb5d21a298be0c7c2ae2f0583b8db83ca9eebc58aed60d1a597e2d7e040` |
| `SP\1Cor\book_strategy_1Cor.md` | `70e344fed9f0f64654baa97dff80e03b706a1288b47de182628dc453212e39ca` |
| `SP\1Cor\strategy_plan_1Cor.json` | `a55044ceabc4dabd43a7e442ad7dfafb2268700a56904f3734d8c1bf5ab93ca4` |
| `SP\1Cor\tools\TOOLKIT.md` | `49de0883f5cbed7fd9e25fdc8a156a083f8794bdd6490de1b0eee82aa2c7361e` |
| `SP\1Cor\1Cor_rp.txt` | `94f7cf39fbd87f7952aba3ca957b7a4790edfb5d120dceffc8deac0ad0ccc2eb` |
| `SP\1Cor\1Cor_sbl.txt` | `354b6dcf5b5f43a24dd85918e9759eeeb3153dc5284ab707a4167b64919456ff` |
| `SP\1Cor\1Cor_web_clean.txt` | `7c8224ccf9eb0a06df20c5b2289d33ea32267dda136e88e73ea5761807cf0778` |
| `SP\1Cor\1cor_device_inventory.json` | `62c608d775710f56040d3889db9c2cc2a98f40589d15e9b11b8ba2af9b3795ad` |
| `SP\1Cor\pmarks_1Cor.json` | `5cd9055a8ecbfbc8dcf0f5dbc43e7bedbb0e69dc4fb7e8d9000e164e074c7fd7` |
| `SP\1Cor\tools\ngram7.py` | `2dc3a80d5785d2048fc7b17dac093a47c26f10599922bd083bb7158de10d0230` |
| `SP\1Cor\tools\run_validator_suite.py` | `ebe7197b35635d9f8cbf88914219003e32816ba37173f00205668eb5aab2dbb4` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `4dc47a3e406c7d5a2ca7bf6acd27960f9390424fe236d84b4083e586bb200b9b` |

How you may use each input:

- `SP\1Cor\review\1cor_controlling_agent_queue_e2.v1.json`: READ in full. The items you rule on.
- `SP\1Cor\review\1cor_fixup_wave_review_S2.json`: READ changes_required, new_findings, ruled_findings, carried_items, unresolved_uncertainty_bearing and unresolved_uncertainty in full; the rest where you check a fact.
- `SP\1Cor\review\BRIEF_S2.md`: READ where you check what the review was asked.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json`: READ in full. The standing rulings, corpus-wide orders and gate; they stand unless you amend them by id in words.
- `SP\1Cor\review\tool_fixes\s2_receipt_extract.v1.json`: READ where you check a licence (the FIXUP-1 allowed-change maps are inlined in its launch rows).
- `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl`: READ where you check a fact (the rows under review).
- `SP\1Cor\fixup\draft_rows_fixup1_applied.manifest.json`: READ where you check a fact.
- `SP\1Cor\review\cwo_1cor_post_fixup1_report.v1.json`: READ where you check a CWO classification.
- `SP\1Cor\review\cwo_sweep_1cor.py`: READ; you may RUN it on a private copy with --out under your OUT\work only (it writes --out and nothing else).
- `SP\1Cor\book_strategy_1Cor.md`: READ sections 6, 7, 8 and 11 in full; the rest where you check a fact. BINDING.
- `SP\1Cor\strategy_plan_1Cor.json`: READ where you check a fact.
- `SP\1Cor\tools\TOOLKIT.md`: READ where you check a tool contract. Where it and a tool's code differ, the code is the contract.
- `SP\1Cor\1Cor_rp.txt`: READ where you check bytes (Robinson-Pierpont Byzantine text, the primary witness).
- `SP\1Cor\1Cor_sbl.txt`: READ where you check bytes (SBLGNT, the secondary witness, signs kept).
- `SP\1Cor\1Cor_web_clean.txt`: READ where you check bytes (WEB).
- `SP\1Cor\1cor_device_inventory.json`: READ where you check a device class or key.
- `SP\1Cor\pmarks_1Cor.json`: READ where you check a mark.
- `SP\1Cor\tools\ngram7.py`: READ; you may RUN it on a private copy in your OUT\work (it writes nothing).
- `SP\1Cor\tools\run_validator_suite.py`: READ ONLY - NEVER RUN.
- `SP\campaign\grader_models.v1.json`: READ. The OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## What to rule on

**Every** item in the queue: S2-01, S2-02, S2-03, S2-04, S2-05, S2-06, S2-07, S2-08, S2-09, S2-10, S2-11, S2-12, S2-13, S2-14, S2-15, GATE-E2. One ruling per id; no id may be missing.

- Nothing here may weaken a HARD gate without saying so in words. A tool change that narrows what a HARD member
  counts must state why it cannot hide a real defect, and name the fixture that proves it.
- A class ruling that orders a sweep names its predicate and its fields exactly, in corpus_wide_orders (new ids continue
  after the round-1 ids), so the orchestrator runs it as its own sweep with its own coverage report (E-18). A widened
  predicate states what it adds over the round-1 predicate and how its false positives are classified.
- A fix-up order names the part, the rows and the exact spans or fields; the fix-up author changes nothing else. Where an
  order needs a field or a ref element outside the round-1 licence, the ruling licenses it in words.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
  interpretation (for example the 14:34-35 placement or the slogan attributions) in a boundary. Where a finding touches
  one, say so and route it to Fable's end review.
- Readiness wording you prescribe for the next check takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit
  or 'not fit'.
- **GATE-E2:** set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and
  `primaries_may_launch`. The key `s2_conditions` keeps its round-1 name so the tools that read it still work; in this
  round it holds the conditions the next fresh distinct check, S3, tests on the next applied rows.

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl2\1cor_controlling_agent_rulings_r2_e1.v1.json`

```
{"attempt_id":"cor_controlling_rulings_r2_a1","execution_id":"cor_controlling_rulings_r2_a1#e1",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|tool_fix|author_fixup:W<n>|s3|primaries|fable_end_review","order":"...","exact_spans":["..."]}]}],
 "corpus_wide_orders":[{"id":"CWO-1COR-NN","predicate":"<exact>","fields":"<exact>","remedy":"...","coverage_report":"..."}],
 "gate":{"tool_fixes_before_fixup":["..."],"fixup_may_launch":false,"fixup_parts":["W<n>"],"s2_conditions":["..."],"primaries_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Rule from the queue, S2's deliverable, the round-1 rulings and the strategy; open rows, bytes and tools only where you
check a fact. Keep to roughly 40 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl2

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_controlling_rulings_r2_a1","execution_id":"cor_controlling_rulings_r2_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
