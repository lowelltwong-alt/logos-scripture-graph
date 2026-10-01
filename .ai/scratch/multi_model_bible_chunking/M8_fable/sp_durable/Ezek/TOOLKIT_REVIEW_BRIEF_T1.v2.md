# T1 (v2, execution #e2) — DISTINCT-CHECKER REVIEW of the staged Ezekiel Tier-0 toolkit (m8-mesh-r3; OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## E-19 — the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\` already exists — write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_review_T1.json`; **never run any existence check, listing, glob or recursive search against it or any other
directory.**

**EXACT-PATH LAW:** every path you may read is named in this brief. Open those, by exact path. No directory listing,
no glob, no recursive search, no "looking around". Scope any self-check to YOUR OWN private scratch. State
affirmatively in your final message that you ran no listing and no glob.

**GOVERNANCE:** the worktree `C:\wt\logos-t423-m8-fable` is a gated lane — read-only for you; never run git, never
write a receipt. You write NOTHING anywhere under the worktree; your one write is the deliverable named above, outside it. Private scratch goes in a uniquely-named
subdirectory (`ezek_t1_<random>`) of YOUR OWN session scratchpad — never under SP, never at a scratchpad root.

**AUTHORITY (OWNER DIRECTIVE OW-11, 2026-09-10).** The registry names Fable 5 as this lane's only writer. Asked in chat, the owner answered verbatim: "Do you explicitly authorize this Opus 5 session, and the Fable, Sonnet and Opus agents it launches, to write M8_fable work despite the registry's Fable-5-only rule?"="Yes: Ezekiel, then Daniel", and "How should the exception be recorded?"="M8 log only". The record is the 2026-09-10 addendum of `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md`, which you may open by that exact path. **Even so, you write NOTHING inside `C:\wt\logos-t423-m8-fable`.** You write your one deliverable to the directory named above, outside the worktree, and the orchestrator lands it. You never have to act on an exception you cannot verify.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's lane under SP except the Jer/Lam tool sources this brief names; M7 or comparison
data of any kind; transcripts; `SP\campaign\capture_index.v1.jsonl`.

Run every tool as `PYTHONIOENCODING=utf-8 python <tool> ...` (without it the Windows codec crashes the tool).

## Your role

You are the DISTINCT CHECKER for work the orchestrator (claude-opus-5) authored. You did not build any of it. Your
attempt id is `ezek_toolkit_review_t1_a1`, your execution id `ezek_toolkit_review_t1_a1#e2`. This is the job's second execution; previous_execution_id `ezek_toolkit_review_t1_a1#e1`, which declined to write before the owner's exception existed and reviewed nothing. Your verdict feeds the
Fable controlling agent's ruling on queue addendum item R4; it rules on nothing by itself. Candidate-only,
NON-AUTHORIZING research.

## What was built, and why it needs an outside eye

The Ezekiel writer wave ran before the Tier-0 toolchain was staged. The orchestrator then staged it by adapting the
Jeremiah tools and changing their behaviour for Ezekiel's bytes. In doing so it found and fixed six of its own tool
defects, including arms that produced 12 false flags. An author that has already caught itself six times is exactly
the author whose seventh defect needs someone else to find.

## Artifacts in scope (bound: review THESE bytes and record the digest you actually read)

| path | sha256 at launch |
|---|---|
| `SP\Ezek\tools\ezek_lib.py` | `083bdd854f5a2feb1edaa27263035754eb9355fa0859549a09983d762284177d` |
| `SP\Ezek\tools\build_verse_maps.py` | `aea379415f97e1f3315645a03e0e37f6fe19f47922a42c9f640aa96e7ade22ca` |
| `SP\Ezek\tools\check_language_zones.py` | `6807b3b7b19000cb08a508ffb2b142959a8f275ceba12da0fd2bcd357efbc828` |
| `SP\Ezek\tools\cap_sweep.py` | `07ff84e3c6ec8b05f46afe6e823c07771f7e031dee753376df027af6fe95223b` |
| `SP\Ezek\tools\citation_sweep.py` | `879909d07d3bdcb278e9abe4341082eb6d6623e8894c7389b58ae18af8647ed0` |
| `SP\Ezek\tools\check_marks.py` | `07150380464f21cb48a77a72716439e45af6d3cdd4db631b7b347d71be151ca2` |
| `SP\Ezek\tools\normalize_hebrew_in_json.py` | `ffea52d4e75a3fbb15646f1460690c5bbd90821f961a6262b170efb29e7585a1` |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` |
| `SP\Ezek\tools\_adapt_book_specific_ezek.py` | `b8a2ad59bfe817c8a6101e979015b649d2006c4acc822cba86ad27d948ccc72e` |
| `SP\Ezek\tools\_adapt_zone_tools_ezek.py` | `ef4d4e6cf03dd8a5213fdd1a5e7d1473e82eb21649dfd8df1a785cc072ff4aa2` |
| `SP\Ezek\tools\_test_zone_tools_ezek.py` | `a305be02ec91a37e263943cb1be18423dc95c7b1f0b81f6165fa6efe9eabe848` |
| `SP\Ezek\tools\_audit_book_token_transform.py` | `fd751416eb0ad237e571ec91048336ab4d5fad2e052ff085ead82c5233604908` |
| `SP\Ezek\tools\TOOLKIT.md` | `6d2579804f198f1711c529d75f7f70cbeb59c5bb3bc8681c2efa9be9ebf8baa9` |
| `SP\Ezek\_build_suite_view_ezek.py` | `2bc3b9ffb441b773aa97da42e4dbd9d666c6e0bb8f95538f0bf82414c2ae0630` |
| `SP\Ezek\_summarize_tier0_suite_ezek.py` | `72ee0dd08426925a0be9ae8f7f667cc3cde6003f530e6d42d1cf945bab2aec42` |
| `SP\Ezek\_validate_writer_part.py` | `6d0503956e2ff908c181764cb97fe947228d744f4827ad35fb00f73498ec7602` |
| `SP\Ezek\writer\draft_rows_combined.jsonl` | `7b1a16ba5f07aa3443df2be423d6b1618319163720c8c3673409ff06198c6c0e` |
| `SP\Ezek\writer\draft_rows_combined.suite_view.jsonl` | `a4e24747d741805348e34478b1903cc29491d0a447fb6835d5e2fbe05c4b496a` |
| `SP\Ezek\writer\draft_rows_combined.suite_view.manifest.json` | `0233ed2b4f97f6636882f9e77db6a1d7f262d76c8f355cf2f655f17efac24c37` |
| `SP\Ezek\writer\draft_rows_combined.suite_view.jsonl.validator_report.json` | `0febdd93bee891cced87a9a1b65bece1083680d18857920d6fe34c956c9b8234` |
| `SP\Ezek\writer\ezek_tier0_suite_summary.v1.json` | `4a5fff93642ae99b85a51e60b06a0abad2e071ec6eea83f80af6930f8a83b838` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\Ezek_web_clean.txt` | `a7e59bcbcd19607485cfb6c6c1f8f831eb63fd2a81d164ce8e25fcb1a7a2088a` |
| `SP\Ezek\Ezek_web.usfm` | `e8e3bf3c4207c5da9897fee58c13bac2204c4a1467b367eb7479d52be205636c` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |
| `SP\Jer\tools\citation_sweep.py` | `395b30041231a1e9abf4e195239503864b8700814cf811448fdc490b148a6d7b` |
| `SP\Jer\tools\check_marks.py` | `7405e97a43c49ce63b81e3749fa5b9562e9b737d6e5bc0b9901faf1a99590b0f` |
| `SP\Jer\tools\cap_sweep.py` | `4785a1986a3daca6361fc6a9fd36be3aebdc845b7c1ed9decc47c2267a8046d1` |
| `SP\Jer\tools\build_verse_maps.py` | `3f2e40259bc11fbc8a1f7d629295f6f8c75856f35b7e1cddf596e86daba3b731` |
| `SP\Jer\tools\normalize_hebrew_in_json.py` | `2b324774e1ed8b7a0b463fd36b77e48edb22672f7bc2217c4556f2898feb982e` |
| `SP\Jer\tools\jer_lib.py` | `079c442437cabfe63167e10cafaee1869636273f9e44e378edbb9035798e51d7` |
| `SP\Lam\tools\check_language_zones.py` | `741184223aab5abdb32647df3f732cad0dc37a0a8f1035e767a09499f317ae7f` |

## Questions — answer every one, from the bytes

1. **Hard-gate weakening.** Compare each adapted tool with its Jer or Lam source. List EVERY behavioural difference.
   For each: is it documented in the tool's docstring, is it tested, and could it let a real defect pass that the
   source tool would have caught? This is the question that matters most.
2. **Qere tier** (normalizer; citation_sweep's Hebrew-binding arm). Can anything that is NOT a Qere pass — for
   example a run straddling a ketiv/qere junction, a ketiv, or an NFD-only match? Does a disclosed Qere always pass,
   and an undisclosed one always fail? Check against `pmarks_Ezek.json` `kq` and `ezek_lib.kq_split`.
3. **Puncta arms** (both tools). Given that U+05C4 stands only at MT 41:20 (five) and 46:22 (seven), can a false
   claim pass — a claim at the wrong verse, or a false "no puncta" inside a span covering a site? Does the
   adjacent-negation rule misread real prose?
4. **Editorial-note K/Q tier.** Can a ketiv/qere claim pass without byte support in the `notes_other` layer?
5. **Zone logic.** `web_pairs_in_offset_zone` / `mt_pairs_in_offset_zone` against `web_mt_offset_map.json`; the
   crosswalk messages; `build_verse_maps.py`'s seam asserts.
6. **Suite view** (`_build_suite_view_ezek.py`). Is it lossless? Could it hide a finding the rows carry, or create one
   they do not? Is its Hebrew copy bound to the right ref?
7. **Summary** (`_summarize_tier0_suite_ezek.py` and its output). Are the deterministic counts right against the
   report? Does `orchestrator_observations` overclaim?
8. **Tests** (`_test_zone_tools_ezek.py`). What adversarial case is missing? Write and run extra vectors in YOUR
   private scratch only.
9. **TOOLKIT.md** — the staged-tools section and the 2026-09-10 flagged-regions correction: is every factual claim
   true?

## What you may run, and what you must not

- MAY run: `ezek_lib.py` (selftest), `_toolkit_selfcheck.py`, `_test_zone_tools_ezek.py` (writes only to a temp
  dir), `_audit_book_token_transform.py` (read-only), and `citation_sweep.py`, `check_marks.py`, `cap_sweep.py`,
  `check_language_zones.py`, `normalize_hebrew_in_json.py` WITHOUT `--write`, over PRIVATE COPIES of rows you put in
  your own scratch. `run_validator_suite.py` writes its report beside its input, so run it ONLY on a private copy.
- MUST NOT run: `build_verse_maps.py`, either `_adapt_*.py`, `_build_suite_view_ezek.py`,
  `_summarize_tier0_suite_ezek.py`, or anything with `--write` — each of them writes under SP. Read them instead.
- Never edit any file under SP. A defect you find is reported, not fixed.

## Deliverable — `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_review_T1.json`

```
{"attempt_id":"ezek_toolkit_review_t1_a1","execution_id":"ezek_toolkit_review_t1_a1#e2",
 "verdict":"fit_to_accept|fit_with_changes|not_fit",
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<the digest of the bytes you read>"}],
 "hard_gate_weakening":[{"tool":"...","difference":"...","documented":true,"tested":true,"can_pass_a_real_defect":"yes|no|unclear","evidence":"..."}],
 "findings":[{"id":"T1-01","severity":"blocker|major|minor|note","artifact":"...","claim":"...","evidence":"<bytes, tool output>","how_verified":"...","suggested_fix":"..."}],
 "private_vectors_run":[{"what":"...","result":"..."}],
 "answers":{"q1":"...","q2":"...","q3":"...","q4":"...","q5":"...","q6":"...","q7":"...","q8":"...","q9":"..."},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

A `fit_to_accept` with no findings from an author that just fixed six of its own defects would be surprising. Say
exactly what you checked, so a reader can tell a clean result from a shallow one.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"ezek_toolkit_review_t1_a1","execution_id":"ezek_toolkit_review_t1_a1#e2",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "verdict":"...","finding_count":0,
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

`unresolved_uncertainty` is the field most worth having and the easiest to leave empty.
