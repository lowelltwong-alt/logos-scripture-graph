# T2 — FRESH DISTINCT-CHECKER REVIEW of the repair of T1's toolkit findings (Ezekiel; OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## E-19 — the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\` already exists — write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_repair_review_T2.json`; **never run any existence check, listing, glob or recursive search
against it or any other directory.**

**EXACT-PATH LAW:** every path you may read is named in this brief. Open those, by exact path. No directory listing, no
glob, no recursive search, no "looking around". Scope any self-check to YOUR OWN private scratch. State affirmatively in
your final message that you ran no listing and no glob.

**GOVERNANCE:** the worktree `C:\wt\logos-t423-m8-fable` is a gated lane. You write NOTHING anywhere under it; never run
git; never write a receipt. Your one write is the deliverable named above, outside the worktree. Private scratch goes in a
uniquely-named subdirectory (`ezek_t2_<random>`) of YOUR OWN session scratchpad.

**AUTHORITY (OWNER DIRECTIVE OW-11, 2026-09-10).** The registry names Fable 5 as this lane's only writer. Asked in chat, the
owner answered verbatim: "Do you explicitly authorize this Opus 5 session, and the Fable, Sonnet and Opus agents it launches,
to write M8_fable work despite the registry's Fable-5-only rule?"="Yes: Ezekiel, then Daniel", and "How should the exception
be recorded?"="M8 log only". The record is the 2026-09-10 addendum of `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md` (open it by that exact path if you want to
verify). Even so, you write nothing inside the worktree: the orchestrator lands your deliverable.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`, `M2_claude_sonnet5`,
`M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or `comparison\`; every other book's
lane except the Jer tool sources named below; M7 or comparison data of any kind; transcripts; the capture index.

Run every tool as `PYTHONIOENCODING=utf-8 python <tool> ...`.

## Your role

You are a FRESH distinct checker. Attempt id `ezek_toolkit_repair_review_t2_a1`, execution id `ezek_toolkit_repair_review_t2_a1#e1` (first execution; previous_execution_id null). You
did not write the toolkit, the repair, or the review it answers. A distinct checker (T1) reviewed the staged toolkit and found
two blockers, two minors, a note, and one unclear hard-gate difference. The orchestrator (claude-opus-5) repaired them. While
testing that repair, it found and fixed one more defect of its own: its new nearest-number binding reached across a row's
field boundary into the span string. Your job is to decide whether each cure is real. A cure is not cured because its author
says so (OW-10): you must run things, and record the digest of the bytes you ran them against.

## Inputs (read by exact path; the digests bind what you reviewed)

| path | sha256 at launch |
|---|---|
| `SP\Ezek\ezek_toolkit_review_T1.json` | `2a341d583b3d8d68d8f2f1a953bc40150d8ace090e66b70b1616ef13bbc96a0b` |
| `SP\Ezek\tools\citation_sweep.py` | `e020d4999fd7a547b65dcb988fdd80416b0db41944b7c244fb189eb4af5486d1` |
| `SP\Ezek\tools\check_marks.py` | `be49861070fd6416b45fa6acecd636f0a52e891afd3e4eb1f5a6853e34c2a741` |
| `SP\Ezek\tools\normalize_hebrew_in_json.py` | `07b58b19f0883ecd32a353fa9b9189e68b97cbfca7d55dc35e416eaa17c94e86` |
| `SP\Ezek\tools\_adapt_zone_tools_ezek.py` | `5cb0ff664be5846b11cf46996d92bee81727f0b327219f09eabc99995604e908` |
| `SP\Ezek\tools\_test_zone_tools_ezek.py` | `e0686ef2f9a39e8652026b5fa6c62532bf6d50ea01a23122dcf44d15abc7ab9d` |
| `SP\Ezek\tools\ezek_lib.py` | `083bdd854f5a2feb1edaa27263035754eb9355fa0859549a09983d762284177d` |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` |
| `SP\Ezek\tools\TOOLKIT.md` | `6d2579804f198f1711c529d75f7f70cbeb59c5bb3bc8681c2efa9be9ebf8baa9` |
| `SP\Ezek\tools\verse_map_oshb.json` | `408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\writer\draft_rows_combined.suite_view.jsonl` | `a4e24747d741805348e34478b1903cc29491d0a447fb6835d5e2fbe05c4b496a` |
| `SP\Ezek\writer\draft_rows_combined.suite_view.jsonl.validator_report.json` | `0febdd93bee891cced87a9a1b65bece1083680d18857920d6fe34c956c9b8234` |
| `SP\Ezek\writer\ezek_tier0_suite_summary.v1.json` | `c06f8b6ef0392c30132244281b571357392f1859076f5891ad08e3ecf4ffa075` |
| `SP\Jer\tools\citation_sweep.py` | `395b30041231a1e9abf4e195239503864b8700814cf811448fdc490b148a6d7b` |
| `SP\Jer\tools\check_marks.py` | `7405e97a43c49ce63b81e3749fa5b9562e9b737d6e5bc0b9901faf1a99590b0f` |
| `SP\Jer\tools\normalize_hebrew_in_json.py` | `2b324774e1ed8b7a0b463fd36b77e48edb22672f7bc2217c4556f2898feb982e` |

## Questions — answer every one, from the bytes and from your own runs

1. **Cure status of every T1 item** (T1-01..T1-05 and the three hard_gate_weakening entries in the landed T1 review):
   cured / not_cured / partially_cured / no_change_needed. For each, name the vector you ran and its result. Re-run T1's
   own attacks first, then variants of them.
2. **Did the repair open a new hole?** The puncta arms now bind a claim to the C:V or C.V number nearest it within 60
   characters of the same field, and fall back to span or range coverage only when no number is written. Attack that: a
   false claim whose nearest number is a site while the claim is about another verse; a true claim whose nearest number is
   a neighbouring non-site verse (a false flag); range forms like "40:5-40:16"; "MT 46.22" against "46:22"; multi-line
   fields; a negation two words away; "not without", "never lacking".
3. **The Qere disclosure window** is now 160 characters around the quote. Can an undisclosed Qere pass by standing near
   another quote's keyword? Does a real disclosure written well after a long quote still pass?
4. **Documentation:** do the docstrings of both tools and of the normalizer describe exactly what the code now does?
5. **Hard-gate parity:** compare the repaired arms with the Jer sources. Is any new behavioural difference undocumented or
   untested?
6. **Suite parity:** run the suite over a PRIVATE COPY of the view and confirm the hard counts match the landed report
   (citation_sweep 546, normalizer 24, ngram7 3, cap_sweep 4) with zero puncta flags and zero puncta problems.

## What you may run, and what you must not

- MAY run: `ezek_lib.py`, `_test_zone_tools_ezek.py` (temp dirs only), and `citation_sweep.py`, `check_marks.py`,
  `normalize_hebrew_in_json.py` (never `--write`) and `run_validator_suite.py` over PRIVATE COPIES in your own scratch
  (the suite writes its report beside its input).
- MUST NOT run: `build_verse_maps.py`, either `_adapt_*.py`, `_build_suite_view_ezek.py`, `_summarize_tier0_suite_ezek.py`,
  or anything with `--write`. Read those instead. Never edit any file anywhere under the worktree.

## Deliverable — `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_repair_review_T2.json`

```
{"attempt_id":"ezek_toolkit_repair_review_t2_a1","execution_id":"ezek_toolkit_repair_review_t2_a1#e1",
 "verdict":"fit_to_accept|fit_with_changes|not_fit",
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest of the bytes you ran and read>"}],
 "cure_status":[{"t1_item":"T1-01","status":"cured|not_cured|partially_cured|no_change_needed","vector_run":"...","result":"...","evidence":"..."}],
 "new_findings":[{"id":"T2-01","severity":"blocker|major|minor|note","artifact":"...","claim":"...","evidence":"...","how_verified":"...","suggested_fix":"..."}],
 "answers":{"q1":"...","q2":"...","q3":"...","q4":"...","q5":"...","q6":"..."},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"ezek_toolkit_repair_review_t2_a1","execution_id":"ezek_toolkit_repair_review_t2_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "verdict":"...","cured":0,"not_cured":0,"new_finding_count":0,
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
