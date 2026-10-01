# CONTROLLING-AGENT RULINGS (execution #e3): Daniel, S1's findings, the tool fixes and FIXUP-1's scope (M8_fable, OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for a study corpus. You read the Masoretic text (OSHB/WLC) and the World English Bible, verify quotations byte-for-byte, and rule on proposed reading-unit boundaries and on review findings. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for Ezekiel and Daniel. Verbatim answers: on authority,
"Yes: Ezekiel, then Daniel"; on recording, "M8 log only". authorization_ref
`lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 807-874
only. You run on claude-opus-5-5 in the controlling agent's (Fable's) role, as a recorded grader_fallback (OW-25): a
recorded downgrade, not an equivalence. Your rulings go to Fable's end-of-campaign review (OW-28). You read files under
the worktree and write only under your OUT directory; the orchestrator lands your deliverable. You never run git, never
write a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl` already exists. Write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl\dan_controlling_agent_rulings_e3.v1.json`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl\work\`, created with os.makedirs(exist_ok=True) and never
tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; the writers' and S1's OUT directories, receipts, final messages
and evidence notes; every `*_attempt_receipts.jsonl`; transcripts. Nothing from another book passes as Daniel's (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the CONTROLLING AGENT for Daniel. Attempt `dan_controlling_rulings_a1`, execution `dan_controlling_rulings_a1#e3` (execution 3. This is a relaunch: #e2 hard-stopped itself before ruling, because the ledger had been appended after its brief pinned the ledger's digest (a pinned-input mismatch; the OW-11 range was unchanged); it produced nothing you may use). You authored none of
the rows, the strategy, the tools or the S1 review. S1, a distinct checker, landed on the combined writer draft:
verdict fit_with_changes, 11 findings (1 major, 5 minor, 5 notes). The orchestrator's queue proposes a ruling for each
finding, for S1's open questions and for the gate. The orchestrator proposes; you rule. You may adopt, change or reject
any proposal, and you may add an id only for a defect you find in the bytes.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Dan\review\dan_controlling_agent_queue_e1.v1.json` | `0b3ef9035f78dc1e48ee9028fe0e24056e08a99f3085b2e065a2dc89ecf9f8a2` |
| `SP\Dan\review\dan_writer_wave_spot_review_S1.json` | `e7e725a9301ccab2a9139d9f2f6c8e504200488f4bb78148fef761762212ea7f` |
| `SP\Dan\review\BRIEF_S1_e2.md` | `f2616baf14edd804a22a79d7724df6a8fabc7a5e8e34a60cb34cbd72cd0f2a22` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\strategy_plan_Dan.json` | `a35acfb997ce8c659fc840ae638fc2cd88d7eb3eb13f0bbe481c7d588d418ef4` |
| `SP\Dan\tools\TOOLKIT.md` | `c05b81466651c6b1f61f43f0c8ff48ada675618b86d0a1db1ccf121d9eeb0fd5` |
| `SP\Dan\writer\draft_rows_combined.jsonl` | `693e468fd4b166ea4ff57bf5729ff7f952c218727e6ceed61ba77df1b9ef8830` |
| `SP\Dan\writer\draft_rows_combined.report.json` | `898b5c6276814063d3e61676b4aaccf11b2d3bfb4480026f0eae99626c26e028` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\tools\ngram7.py` | `5faf1c2aa3b6f1e6d360e6bb135892efa6b7c350274f995fc87855cd98356c81` |
| `SP\Dan\tools\run_validator_suite.py` | `f5d1fc5a526cff5348716d5a34037745a0714dedc0c8b2d0b8c35a5a5973698e` |
| `SP\Dan\tools\check_universals.py` | `65575ff272592ae00e90aae181808ea3e55966a7506bab8b50b23d612139007e` |
| `SP\Dan\tools\check_marks.py` | `df1818f72467102408985321848c63b79e4e4ba018a8b67d768a65107a3ab3b7` |
| `SP\Dan\tools\cap_sweep.py` | `91be20cb82dd861a093fbf2957a95ba3b7fcaec5df66bceac0c7c64c5f8fdfa1` |
| `SP\Dan\tools\citation_sweep.py` | `d5bd9b33a9c050a96932fe410c6f935cab94c12282f80593340fd7aa1c5ec652` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `1face1767986712d95fa7da0ca0f90d0850d69025f0dbc887a5b322ec8001941` |

How you may use each input:

- `SP\Dan\review\dan_controlling_agent_queue_e1.v1.json`: READ in full. The items you rule on.
- `SP\Dan\review\dan_writer_wave_spot_review_S1.json`: READ new_findings, ngram7, flags, confidence and unresolved_uncertainty in full; the rest where you check a fact.
- `SP\Dan\review\BRIEF_S1_e2.md`: READ where you check what S1 was asked.
- `SP\Dan\book_strategy_Dan.md`: READ sections 6, 7, 8 and 11 in full; the rest where you check a fact. BINDING.
- `SP\Dan\strategy_plan_Dan.json`: READ where you check a fact.
- `SP\Dan\tools\TOOLKIT.md`: READ where you check a tool contract. Where it and a tool's code differ, the code is the contract.
- `SP\Dan\writer\draft_rows_combined.jsonl`: READ where you check a fact (the 75 rows S1 reviewed).
- `SP\Dan\writer\draft_rows_combined.report.json`: READ where you check a fact.
- `SP\Dan\Dan_oshb.txt`: READ where you check bytes (OSHB/WLC, MT numbering).
- `SP\Dan\Dan_web_clean.txt`: READ where you check bytes (WEB).
- `SP\Dan\dan_device_inventory.json`: READ where you check a device class or key.
- `SP\Dan\pmarks_Dan.json`: READ where you check a mark or the kq layer.
- `SP\Dan\tools\ngram7.py`: READ; you may RUN it on a private copy in your scratch (it writes nothing).
- `SP\Dan\tools\run_validator_suite.py`: READ ONLY - NEVER RUN.
- `SP\Dan\tools\check_universals.py`: READ ONLY - NEVER RUN.
- `SP\Dan\tools\check_marks.py`: READ ONLY - NEVER RUN.
- `SP\Dan\tools\cap_sweep.py`: READ ONLY - NEVER RUN.
- `SP\Dan\tools\citation_sweep.py`: READ ONLY - NEVER RUN.
- `SP\campaign\grader_models.v1.json`: READ. The OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only (OW-11, the owner's exception, OW-11-h).

## What to rule on

**Every** item in the queue: S1-ROUTING, S1-01, S1-02, S1-03, S1-04, S1-05, S1-06, S1-07, S1-08, S1-09, S1-10, S1-11, U-FRONTIER, U-QUOTE-LABEL, U-ZONEDUAL, GATE-E1. One ruling per id; no id may be missing.

- Nothing here may weaken a HARD gate without saying so in words. A tool change that narrows what a HARD member
  counts (S1-07) must state why it cannot hide a real defect, and name the fixture that proves it.
- A class ruling that orders a sweep names its predicate and its fields exactly, in corpus_wide_orders, so the
  orchestrator runs it as its own sweep with its own coverage report (E-18).
- A fix-up order names the part, the rows and the exact spans or fields; the fix-up author changes nothing else.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or encodes one eschatological
  timeline in a boundary. Where a finding touches one, say so and route it to Fable's end review.
- Readiness wording you prescribe for S2 takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit or 'not
  fit'.
- **GATE-E1:** set `tool_fixes_before_fixup`, `fixup1_may_launch`, `fixup1_parts`, `s2_conditions` and
  `primaries_may_launch`.

## Deliverable: `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_ctl\dan_controlling_agent_rulings_e3.v1.json`

```
{"attempt_id":"dan_controlling_rulings_a1","execution_id":"dan_controlling_rulings_a1#e3",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|tool_fix|author_fixup:W<n>|s2|primaries|fable_end_review","order":"...","exact_spans":["..."]}]}],
 "corpus_wide_orders":[{"id":"CWO-DAN-NN","predicate":"<exact>","fields":"<exact>","remedy":"...","coverage_report":"..."}],
 "gate":{"tool_fixes_before_fixup":["..."],"fixup1_may_launch":false,"fixup1_parts":["W<n>"],"s2_conditions":["..."],"primaries_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## Budget

Rule from the queue, S1's deliverable and the strategy; open rows, bytes and tools only where you check a fact. Keep to
roughly 40 tool calls. Report exactly what you ran and what it returned.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"dan_controlling_rulings_a1","execution_id":"dan_controlling_rulings_a1#e3",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
