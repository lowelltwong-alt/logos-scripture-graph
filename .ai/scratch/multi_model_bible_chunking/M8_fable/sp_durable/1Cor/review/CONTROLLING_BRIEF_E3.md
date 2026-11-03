# CONTROLLING-AGENT RULINGS (round 3, execution #e1): 1 Corinthians, S3's required changes, the class rulings and the next fix-up wave's scope (M8_fable, OW-36 queue)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl3` already exists. Write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl3\1cor_controlling_agent_rulings_r3_e1.v1.json`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl3\work\`, created with os.makedirs(exist_ok=True) and never
tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; the writers', the fix-up authors', S1's, S2's and S3's OUT
directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`; transcripts. Nothing from
another book passes as 1 Corinthians' (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the CONTROLLING AGENT for 1 Corinthians, round 3. Attempt `cor_controlling_rulings_r3_a1`, execution `cor_controlling_rulings_r3_a1#e1` (first execution). You authored
none of the rows, the strategy, the tools, the earlier rounds' rulings or the reviews. S3, a fresh distinct checker, read
the FIXUP-2 applied rows and recorded readiness fit_with_changes: 1 changes
required and 7 new findings (1 major, 2 minor, 4 note). The orchestrator's queue proposes a ruling for each finding and for the
gate. The orchestrator proposes; you rule. You may adopt, change or reject any proposal, and you may add an id only for a
defect you find in the bytes. The rulings of rounds 1-2 (`1cor_controlling_agent_rulings_E2.v1.json` and the earlier rulings pinned below) stand unless you amend one by id, in words.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\1Cor\review\1cor_controlling_agent_queue_e3.v1.json` | `fd622c02669105aa78daf2c45ed436120a8ab66774a28cc8a42c045c581b2e06` |
| `SP\1Cor\review\1cor_fixup2_review_S3.json` | `250665975db7b5288b121eb7ff4d3eb9a5d05ea06b3a3dfcb883f41ea9043d01` |
| `SP\1Cor\review\BRIEF_S3.md` | `d3ebf3ae392c5d996c4ccc8042fc5272f20670e2a035a5d414a9378b578a4caf` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E2.v1.json` | `1299a598b60bbf3c8fb193381ead098e394242a713d8bac4e584b39fdf0e0541` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json` | `93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90` |
| `SP\1Cor\review\tool_fixes\s3_receipt_extract.v1.json` | `8bb4715180d88d059193a0135fbe519238d363a327e0ece78371c3c7beb6519b` |
| `SP\1Cor\fixup\draft_rows_fixup2_applied.jsonl` | `75933a142375d8736ae71cdcc7f0e0b9052c36ea4ac4b87ccacf676ae50c6fbe` |
| `SP\1Cor\fixup\draft_rows_fixup2_applied.manifest.json` | `cc03908bda77079e47f3a8b511a595d9ac3ab415c94918b9b303385a3cbba422` |
| `SP\1Cor\review\cwo_1cor_post_fixup2_report.v1.json` | `87de15f46d123b3a4fb3e42f8ab69f4abeb3d22221b47000e6bbe479dd3d3611` |
| `SP\1Cor\review\cwo_sweep_1cor.py` | `bb71fd0bc1347ac6ff17f5d0222249d78b19de8e6ce43b7a31eea276fbd58cd9` |
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

- `SP\1Cor\review\1cor_controlling_agent_queue_e3.v1.json`: READ in full. The items you rule on.
- `SP\1Cor\review\1cor_fixup2_review_S3.json`: READ changes_required, new_findings, ruled_findings, carried_items, unresolved_uncertainty_bearing and unresolved_uncertainty in full; the rest where you check a fact.
- `SP\1Cor\review\BRIEF_S3.md`: READ where you check what the review was asked.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E2.v1.json`: READ in full. The standing rulings, corpus-wide orders and gate; they stand unless you amend them by id in words.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json`: READ in full. The round-1 rulings; they stand unless a later round or you amend one by id in words.
- `SP\1Cor\review\tool_fixes\s3_receipt_extract.v1.json`: READ where you check a licence (the FIXUP-2 allowed-change maps are inlined in its launch rows).
- `SP\1Cor\fixup\draft_rows_fixup2_applied.jsonl`: READ where you check a fact (the rows under review).
- `SP\1Cor\fixup\draft_rows_fixup2_applied.manifest.json`: READ where you check a fact.
- `SP\1Cor\review\cwo_1cor_post_fixup2_report.v1.json`: READ where you check a CWO classification.
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

**Every** item in the queue: S3-01, S3-02, S3-03, S3-04, S3-05, S3-06, S3-07, GATE-E3. One ruling per id; no id may be missing.

- Nothing here may weaken a HARD gate without saying so in words. A tool change that narrows what a HARD member
  counts must state why it cannot hide a real defect, and name the fixture that proves it.
- A class ruling that orders a sweep names its predicate and its fields exactly, in corpus_wide_orders (new ids continue
  after the earlier rounds' ids), so the orchestrator runs it as its own sweep with its own coverage report (E-18). A widened
  predicate states what it adds over the standing predicate and how its false positives are classified.
- A fix-up order names the part, the rows and the exact spans or fields; the fix-up author changes nothing else. Where an
  order needs a field or a ref element outside the standing licence, the ruling licenses it in words.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
  interpretation (for example the 14:34-35 placement or the slogan attributions) in a boundary. Where a finding touches
  one, say so and route it to Fable's end review.
- Readiness wording you prescribe for the next check takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit
  or 'not fit'.
- **GATE-E3:** set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and
  `primaries_may_launch`. The key `s2_conditions` keeps its round-1 name so the tools that read it still work; in this
  round it holds the conditions the next fresh distinct check, S4, tests on the next applied rows.

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl3\1cor_controlling_agent_rulings_r3_e1.v1.json`

```
{"attempt_id":"cor_controlling_rulings_r3_a1","execution_id":"cor_controlling_rulings_r3_a1#e1",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|tool_fix|author_fixup:W<n>|s4|primaries|fable_end_review","order":"...","exact_spans":["..."]}]}],
 "corpus_wide_orders":[{"id":"CWO-1COR-NN","predicate":"<exact>","fields":"<exact>","remedy":"...","coverage_report":"..."}],
 "gate":{"tool_fixes_before_fixup":["..."],"fixup_may_launch":false,"fixup_parts":["W<n>"],"s2_conditions":["..."],"primaries_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Rule from the queue, S3's deliverable, the earlier rounds' rulings and the strategy; open rows, bytes and tools only where you
check a fact. Keep to roughly 40 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl3

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_controlling_rulings_r3_a1","execution_id":"cor_controlling_rulings_r3_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
