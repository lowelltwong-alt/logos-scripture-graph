# CONTROLLING-AGENT RULINGS (round 1, execution #e1): 1 Corinthians, S1's findings, the tool fixes and the fix-up wave's scope (M8_fable, OW-36 queue)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl1` already exists. Write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl1\1cor_controlling_agent_rulings_r1_e1.v1.json`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl1\work\`, created with os.makedirs(exist_ok=True) and never
tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; the writers' and S1's OUT directories, receipts, final messages
and evidence notes; every `*_attempt_receipts.jsonl`; transcripts. Nothing from another book passes as 1 Corinthians'
(E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the CONTROLLING AGENT for 1 Corinthians. Attempt `cor_controlling_rulings_r1_a1`, execution `cor_controlling_rulings_r1_a1#e1` (first execution). You authored none of
the rows, the strategy, the tools or the S1 review. S1, a distinct checker, landed on the combined writer draft:
verdict fit_with_changes, 13 findings (4 major, 4 minor, 5 note). The orchestrator's queue proposes a ruling for each finding,
for S1's open questions and for the gate. The orchestrator proposes; you rule. You may adopt, change or reject any
proposal, and you may add an id only for a defect you find in the bytes.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\1Cor\review\1cor_controlling_agent_queue_e1.v1.json` | `673274b0123eacf7fe618c8159497270dedea0119b650d23ae431f67583be446` |
| `SP\1Cor\review\1cor_writer_wave_spot_review_S1.json` | `6586e74003e7bd13821710736df5c3075eef535460cc1758e58157fff06b6e3d` |
| `SP\1Cor\review\BRIEF_S1.md` | `279bd3b25c6865ad36ef1536a0bfac6c432f96cae0672af187e6cc2542fec78d` |
| `SP\1Cor\book_strategy_1Cor.md` | `70e344fed9f0f64654baa97dff80e03b706a1288b47de182628dc453212e39ca` |
| `SP\1Cor\strategy_plan_1Cor.json` | `a55044ceabc4dabd43a7e442ad7dfafb2268700a56904f3734d8c1bf5ab93ca4` |
| `SP\1Cor\tools\TOOLKIT.md` | `a8313a3a8140c70847981597ac4d36d1811896b73cd88f4f5049af4d4a847b62` |
| `SP\1Cor\writer\draft_rows_combined.jsonl` | `3d328c8afa9f2616b963413a15041d916e0d54ad474835da4f92af90b2588af6` |
| `SP\1Cor\writer\draft_rows_combined.report.json` | `9e4d40a46db8d8db1e4f8b9bd6733cc947159cca1e5bc88cb11040d627f361b4` |
| `SP\1Cor\1Cor_rp.txt` | `94f7cf39fbd87f7952aba3ca957b7a4790edfb5d120dceffc8deac0ad0ccc2eb` |
| `SP\1Cor\1Cor_sbl.txt` | `354b6dcf5b5f43a24dd85918e9759eeeb3153dc5284ab707a4167b64919456ff` |
| `SP\1Cor\1Cor_web_clean.txt` | `7c8224ccf9eb0a06df20c5b2289d33ea32267dda136e88e73ea5761807cf0778` |
| `SP\1Cor\1cor_device_inventory.json` | `62c608d775710f56040d3889db9c2cc2a98f40589d15e9b11b8ba2af9b3795ad` |
| `SP\1Cor\pmarks_1Cor.json` | `5cd9055a8ecbfbc8dcf0f5dbc43e7bedbb0e69dc4fb7e8d9000e164e074c7fd7` |
| `SP\1Cor\tools\ngram7.py` | `8646f540acc36975c66a3b0949e509a4a3d41039aecaedd6bb874d9834fd0e3c` |
| `SP\1Cor\tools\run_validator_suite.py` | `ebe7197b35635d9f8cbf88914219003e32816ba37173f00205668eb5aab2dbb4` |
| `SP\1Cor\tools\check_universals.py` | `e047b8dfbd99f56d86556ef073cd8c0c63886db3bd66cfa9c31433b4042f009f` |
| `SP\1Cor\tools\check_marks.py` | `eb092ed3f802604a63b47c6ebe0fb3db7375e25bd3efc8ff29fe6abe791d6c45` |
| `SP\1Cor\tools\cap_sweep.py` | `1280c21dbd9bf6eaf7feed7d0923b6dcb71e3cf28c0c3b9a0e366c655389a867` |
| `SP\1Cor\tools\citation_sweep.py` | `84514c10f26d2ebf3e85cc109fad63fc00f92d173ba0a8d6504e7677ec0e9914` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `4dc47a3e406c7d5a2ca7bf6acd27960f9390424fe236d84b4083e586bb200b9b` |

How you may use each input:

- `SP\1Cor\review\1cor_controlling_agent_queue_e1.v1.json`: READ in full. The items you rule on.
- `SP\1Cor\review\1cor_writer_wave_spot_review_S1.json`: READ new_findings, ngram7, flags, confidence and unresolved_uncertainty in full; the rest where you check a fact.
- `SP\1Cor\review\BRIEF_S1.md`: READ where you check what S1 was asked.
- `SP\1Cor\book_strategy_1Cor.md`: READ sections 6, 7, 8 and 11 in full; the rest where you check a fact. BINDING.
- `SP\1Cor\strategy_plan_1Cor.json`: READ where you check a fact.
- `SP\1Cor\tools\TOOLKIT.md`: READ where you check a tool contract. Where it and a tool's code differ, the code is the contract.
- `SP\1Cor\writer\draft_rows_combined.jsonl`: READ where you check a fact (the rows S1 reviewed).
- `SP\1Cor\writer\draft_rows_combined.report.json`: READ where you check a fact.
- `SP\1Cor\1Cor_rp.txt`: READ where you check bytes (Robinson-Pierpont Byzantine text, the primary witness).
- `SP\1Cor\1Cor_sbl.txt`: READ where you check bytes (SBLGNT, the secondary witness, signs kept).
- `SP\1Cor\1Cor_web_clean.txt`: READ where you check bytes (WEB).
- `SP\1Cor\1cor_device_inventory.json`: READ where you check a device class or key.
- `SP\1Cor\pmarks_1Cor.json`: READ where you check a mark.
- `SP\1Cor\tools\ngram7.py`: READ; you may RUN it on a private copy in your OUT\work (it writes nothing).
- `SP\1Cor\tools\run_validator_suite.py`: READ ONLY - NEVER RUN.
- `SP\1Cor\tools\check_universals.py`: READ ONLY - NEVER RUN.
- `SP\1Cor\tools\check_marks.py`: READ ONLY - NEVER RUN.
- `SP\1Cor\tools\cap_sweep.py`: READ ONLY - NEVER RUN.
- `SP\1Cor\tools\citation_sweep.py`: READ ONLY - NEVER RUN.
- `SP\campaign\grader_models.v1.json`: READ. The OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## What to rule on

**Every** item in the queue: S1-ROUTING, S1-01, S1-01b, S1-02, S1-02b, S1-03, S1-04, S1-05, S1-06, S1-07, S1-08, S1-09, S1-10, S1-11, U-SINGLE-LANE, GATE-E1. One ruling per id; no id may be missing.

- Nothing here may weaken a HARD gate without saying so in words. A tool change that narrows what a HARD member
  counts must state why it cannot hide a real defect, and name the fixture that proves it.
- A class ruling that orders a sweep names its predicate and its fields exactly, in corpus_wide_orders, so the
  orchestrator runs it as its own sweep with its own coverage report (E-18).
- A fix-up order names the part, the rows and the exact spans or fields; the fix-up author changes nothing else.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
  interpretation (for example the 14:34-35 placement or the slogan attributions) in a boundary. Where a finding touches
  one, say so and route it to Fable's end review.
- Readiness wording you prescribe for S2 takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit or 'not
  fit'.
- **GATE-E1:** set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and
  `primaries_may_launch`.

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl1\1cor_controlling_agent_rulings_r1_e1.v1.json`

```
{"attempt_id":"cor_controlling_rulings_r1_a1","execution_id":"cor_controlling_rulings_r1_a1#e1",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|tool_fix|author_fixup:W<n>|s2|primaries|fable_end_review","order":"...","exact_spans":["..."]}]}],
 "corpus_wide_orders":[{"id":"CWO-1COR-NN","predicate":"<exact>","fields":"<exact>","remedy":"...","coverage_report":"..."}],
 "gate":{"tool_fixes_before_fixup":["..."],"fixup_may_launch":false,"fixup_parts":["W<n>"],"s2_conditions":["..."],"primaries_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Rule from the queue, S1's deliverable and the strategy; open rows, bytes and tools only where you check a fact. Keep to
roughly 40 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_ctl1

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_controlling_rulings_r1_a1","execution_id":"cor_controlling_rulings_r1_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
