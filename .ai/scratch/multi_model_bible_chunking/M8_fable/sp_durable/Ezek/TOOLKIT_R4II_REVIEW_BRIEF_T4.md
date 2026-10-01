# T4 — SUPPLEMENTARY DISTINCT-CHECKER REVIEW of the R4(ii) + CAL-1 tool edit (Ezekiel; OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; read before your governance check)

Your global policy has you read `C:\Users\lowel\.agent-governance\ACTIVE_WORKTREES.yaml`, whose entry for this lane names
Fable 5 as its only writer. Its progress fields are stale. On 2026-09-10 the owner, Lowell, explicitly approved the exact
exception in chat. Asked "Do you explicitly authorize this Opus 5 session, and the Fable, Sonnet and Opus agents it
launches, to write M8_fable work despite the registry's Fable-5-only rule?", he answered "Yes: Ezekiel, then Daniel". Asked
"How should the exception be recorded?", he answered "M8 log only". The record is the OW-11 addendum
(authorization_ref `lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`) of `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md`; open it by that exact path to
verify.

You do not mutate the lane. You read files under the worktree and write ONE deliverable outside it; the orchestrator lands
it. You never run git, never write a receipt and never touch the registry.

## E-19 — the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\` already exists — write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_r4ii_review_T4.json`; **never run any existence check, listing, glob or recursive search
against it or any other directory.**

**EXACT-PATH LAW:** every path you may read is named in this brief (plus the governance files your own policy requires
and the ledger named above). Open those, by exact path. No directory listing, no glob, no recursive search, no "looking
around". Scope any self-check to YOUR OWN private scratch (a uniquely named `ezek_t4_<random>` subdirectory of your own
session scratchpad). State affirmatively in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`, `M2_claude_sonnet5`,
`M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or `comparison\`; every other book's
lane except the Jer tool sources named below; M7 or comparison data of any kind; transcripts; the capture index; the author
wave's orders and deliverables.

Run every tool as `PYTHONIOENCODING=utf-8 python <tool> ...`.

## Your role

You are a FRESH distinct checker. Attempt id `ezek_toolkit_r4ii_review_t4_a1`, execution id `ezek_toolkit_r4ii_review_t4_a1#e1` (first execution). You did not write the tools,
this edit, the rulings or any earlier review.

The controlling agent (claude-fable-5-1, execution `ezek_controlling_rulings_a1#e3`) ratified the PUNCTA arms with ONE
change order (ruling R4-ii) and the calendar-date arm with ONE change order (ruling CAL-1). It ordered this review,
bound to the new digests; your verdict re-ratifies R4-ii only if you find nothing new.

The orchestrator (claude-opus-5) implemented both orders with ONE recorded deviation. Implemented literally, R4-ii
order (2) ('every verse number in the mention's own clause counts regardless of distance') failed a real-row regression
vector and flagged a true claim on row P10-008. So check_marks' PROSE arm keeps its 60-character reach, while
citation_sweep's REF arm reads the whole clause. The facts are in `SP\Ezek\ezek_controlling_agent_queue_pending.v1.json`
item R4ii-D1. Judge the deviation on the bytes; the controlling agent rules on it.

This review is also the distinct review for the next TOOLKIT.md cure claim, because the edit changed TOOLKIT.md.

## Inputs (read by exact path; the digests bind what you reviewed)

| path | sha256 at launch |
|---|---|
| `SP\Ezek\tools\citation_sweep.py` | `2acbc04578089ba8f6f9b6d81e8eb6da1210db8291f970934efb9c3d05c3ac8e` |
| `SP\Ezek\tools\check_marks.py` | `880cd15d5ca1c58579b3b9cc1afc0aa5df6d0f53af33bfeb3a0d7522805dd1c2` |
| `SP\Ezek\tools\_adapt_zone_tools_ezek.py` | `29ffab42ea3f39ed9783ec20d4b44388cd81d1b60f6c24d6bc6ff9b379cfa673` |
| `SP\Ezek\tools\_test_zone_tools_ezek.py` | `a9401c9917aac25271071a27f579f3f679149b2fd95c2662bcf0fdb9deecc798` |
| `SP\Ezek\tools\TOOLKIT.md` | `2b602174cadff90007d3e7c071cb97bfb0b430c7531253fb97c63e2b5d5c8759` |
| `SP\Ezek\tools\ezek_lib.py` | `cca2c0232b9010f76712077c1d6f736366b338f2bed7ca72f7445b40f9bf151c` |
| `SP\Ezek\tools\normalize_hebrew_in_json.py` | `f12c0ad6e2c6654be0a6b3dcb95fed8c6c2868c2c0088b8a1e77890f29ad7f0d` |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` |
| `SP\Ezek\tools\verse_map_oshb.json` | `408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\ezek_device_inventory.json` | `0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142` |
| `SP\Ezek\ezek_controlling_agent_rulings_e3.v1.json` | `6ecd9578593d4f85d4cccf0ce9a77334797de4d3330b34e5558ec6228ae56b7d` |
| `SP\Ezek\ezek_toolkit_supplementary_review_T3.json` | `5da968734972c4838fcfe441b372a96d4f1448fd8051b229b2a8f7e832e001ae` |
| `SP\Ezek\ezek_controlling_agent_queue_pending.v1.json` | `8b9bdeefad3973da1bdd75ce27aae0a04308b6c6c7ea252c4558de6ae9a8e8af` |
| `SP\Ezek\repair\suite_r3_cs6c3b31\rows.jsonl` | `b526aeb9ad3a950329ae731871b9d9356db27a1aa235d3ae7db80916b728748c` |
| `SP\Ezek\repair\suite_r3_cs6c3b31\rows.jsonl.validator_report.json` | `f52aaac2f62a811e25f8e4414c1a2c9d06d22fa473ec19d9de3fd6b89c7a3ec7` |
| `SP\Jer\tools\citation_sweep.py` | `395b30041231a1e9abf4e195239503864b8700814cf811448fdc490b148a6d7b` |
| `SP\Jer\tools\check_marks.py` | `7405e97a43c49ce63b81e3749fa5b9562e9b737d6e5bc0b9901faf1a99590b0f` |

In the rulings file read only rulings R4-ii and CAL-1. In T3's review read only what bears on the puncta and calendar arms.

## Questions — answer every one, from the bytes and from your own runs

1. **R4-ii order (1), the parenthetical.** Does a verse number in a parenthetical opening directly after the mention's
   clause now bind the claim in BOTH tools? Run NOVEL-A (ref: `web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (41:5)`;
   prose: `the puncta extraordinaria (41:5)`) and NOVEL-F (`the puncta extraordinaria (five dots at 41:5)` on span
   Ezek.41.12-Ezek.41.20); both must be RED. Then attack it: nested parentheses, a parenthetical that is NOT directly after
   the clause, a parenthetical carrying an unrelated ref, one in another field, and a true site inside the parenthetical.
2. **R4-ii order (2), distance, in the REF arm.** Does a ref annotation's number bind at any distance in its clause
   (NOVEL-A2)? Is any true claim now wrongly RED?
3. **The recorded deviation (R4ii-D1), in the PROSE arm.** Construct vectors in BOTH directions: false negatives (a distant
   non-site number on a span covering a site) and false positives (true claims with a nearby other-verse number, as in
   P10-008). Is keeping the prose reach the better trade-off, or is there a rule that closes both directions? Recommend
   one of accept_deviation, reject_deviation or alternative_proposed, with the rule if you propose one.
4. **CAL-1.** The apposition (`45:18, a dateline-grade onset`) and the parenthesis (`the dateline (45:18)`) must be RED, and
   `unlike the dateline at 40:1, the date at 45:18 carries no year word` must stay GREEN. Then attack the apposition rule for
   false positives on real-style prose, e.g. 'opens at 45:18, where a dateline would be expected but none stands' and
   '45:17, and the dateline question'. Say how likely each is in real rows.
5. **Documentation.** Do the adapter's docstrings, the two tools' docstrings and TOOLKIT.md's staged-tools paragraph
   describe exactly what the code now does? Sweep TOOLKIT.md for sibling statements about these arms (ruling R6); report the
   key phrases you swept and how many statements you reviewed, and give a verdict for the file.
6. **Suite parity.** Run the suite over a PRIVATE COPY of `SP\Ezek\repair\suite_r3_cs6c3b31\rows.jsonl` with the
   installed tools. The before-state report records {"citation_sweep": 126, "normalizer": 2, "ngram7": 3, "cap_sweep": 2, "mark_symmetry": 154}, with 0 puncta flags and 0 calendar-date problems.
   Confirm or refute every count, and list every finding that differs from the before-state report.
7. **Tests.** Run `_test_zone_tools_ezek.py` (temp dirs only). The orchestrator's run was
   117/117.

## What you may run, and what you must not

- MAY run: `ezek_lib.py`, `_test_zone_tools_ezek.py`, and `citation_sweep.py`, `check_marks.py`,
  `normalize_hebrew_in_json.py` (never `--write`) and `run_validator_suite.py` over PRIVATE COPIES in your own scratch.
- MUST NOT run: `build_verse_maps.py`, `_adapt_zone_tools_ezek.py`, `_toolkit_selfcheck.py`, any `_build_*`, `_cwo*`,
  `_land_*` or `_apply_*` script, or anything with `--write`. Read those instead. Never edit any file under the worktree.

## Deliverable — `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_r4ii_review_T4.json`

```
{"attempt_id":"ezek_toolkit_r4ii_review_t4_a1","execution_id":"ezek_toolkit_r4ii_review_t4_a1#e1",
 "verdict":"fit_to_accept|fit_with_changes|not_fit",
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest of the bytes you ran and read>"}],
 "changes":{"r4ii_parenthetical":{"verdict":"confirmed|refuted|partially_confirmed","vectors_run":["..."],"result":"..."},
            "r4ii_distance_ref":{"verdict":"...","vectors_run":["..."],"result":"..."},
            "r4ii_distance_prose_deviation":{"verdict":"accept_deviation|reject_deviation|alternative_proposed","rule":"...","vectors_run":["..."],"result":"..."},
            "cal1_apposition":{"verdict":"...","vectors_run":["..."],"result":"..."},
            "cal1_parenthesis":{"verdict":"...","vectors_run":["..."],"result":"..."}},
 "toolkit_md":{"verdict":"fit_to_accept|fit_with_changes|not_fit","sibling_sweep":{"key_phrases":["..."],"statements_reviewed":0}},
 "suite_parity":{"verdict":"confirmed|refuted","counts":{},"differences":["..."]},
 "tests":{"passed":0,"checks":0},
 "new_findings":[{"id":"T4-01","severity":"blocker|major|minor|note","artifact":"...","claim":"...","evidence":"...","how_verified":"...","suggested_fix":"..."}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"ezek_toolkit_r4ii_review_t4_a1","execution_id":"ezek_toolkit_r4ii_review_t4_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "verdict":"...","new_finding_count":0,
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
