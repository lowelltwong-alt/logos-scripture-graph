# T3 — SUPPLEMENTARY DISTINCT-CHECKER REVIEW of the Ezekiel toolkit (ruling T1's widened scope; OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## E-19 — the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\` already exists — write your deliverable directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_supplementary_review_T3.json`; **never run any existence check, listing, glob or recursive search
against it or any other directory.**

**EXACT-PATH LAW:** every path you may read is named in this brief. Open those, by exact path. No directory listing, no
glob, no recursive search, no "looking around". Scope any self-check to YOUR OWN private scratch. State affirmatively in
your final message that you ran no listing and no glob.

**GOVERNANCE:** the worktree `C:\wt\logos-t423-m8-fable` is a gated lane. You write NOTHING anywhere under it; never run
git; never write a receipt. Your one write is the deliverable named above, outside the worktree. Private scratch goes in a
uniquely-named subdirectory (`ezek_t3_<random>`) of YOUR OWN session scratchpad.

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

You are a FRESH distinct checker. Attempt id `ezek_toolkit_supplementary_review_t3_a1`, execution id `ezek_toolkit_supplementary_review_t3_a1#e1` (first execution; previous_execution_id null). You
did not write the toolkit, any repair, or any review it answers. The controlling agent (ruling T1 in
`SP\Ezek\ezek_controlling_agent_rulings.v1.json`) found the first toolkit review NECESSARY BUT NOT SUFFICIENT, and ordered a
supplementary distinct review of seven named items under its own execution id. You are that review. Your verdicts decide
whether cure claims close (OW-10), and a follow-on controlling execution ratifies R4 (i)-(iii) one by one from your answers.

Since the second review (T2, `SP\Ezek\ezek_toolkit_repair_review_T2.json`, fit_with_changes), the orchestrator (claude-opus-5)
changed the following. Every change is its own claim, and none is cured because its author says so:
- T2-01/T2-02: a puncta claim binds to EVERY verse number in its own clause (a sentence stop, `;` or a parenthesis ends it)
  within 60 characters, ranges expanded: all sites = true, none = false, a mix = `ambiguous` (RED in citation_sweep, a flag
  in check_marks). Only a claim naming no number falls back to span or range coverage.
- T2-03: a negator anywhere earlier in the comma-delimited clause makes a denial; two adjacent negators cancel.
- T2-04: a Qere quote passes only when a ketiv/qere keyword stands in the quote's OWN sentence and within 160 characters.
- T2-05: only a CLOSED `(MT c:v)` / `(WEB c:v)` is read as a numbering qualifier.
- D3 (found by the orchestrator): the Qere tier compared the NFD form of the note. 66 of the 134 notes store marks in
  non-canonical order, so a byte-true Qere quote could be refused. `ezek_lib.kq_split_bytes` now returns the note's RAW
  slices, used by the normalizer and citation_sweep.
- A NEW calendar-date arm in citation_sweep (strategy section 10 as clarified by ruling G12(d)); the staged suite had none.
- TOOLKIT.md: LOW-1 and LOW-2 folded in (ruling Q3), and the staged-tools section rewritten to describe all of the above.
- `SP\campaign\_cure_verification.py`: supersession records retire a stale cure claim (R5); a claim on a `.md` artifact
  must carry `sibling_sweep` (R6).

## Inputs (read by exact path; the digests bind what you reviewed)

| path | sha256 at launch |
|---|---|
| `SP\Ezek\tools\TOOLKIT.md` | `3fcd774a042925557a9f3ae73669395221eca46da42a767f6c6455dd23626c94` |
| `SP\Ezek\tools\citation_sweep.py` | `6c3b31eaf1318dd3cc911df73ff895b1723c10157f823fd11d31651332131fdf` |
| `SP\Ezek\tools\check_marks.py` | `7b80cdae2048894ef4f549cb289621d02864db1137834e7900bc769e2cf4f557` |
| `SP\Ezek\tools\normalize_hebrew_in_json.py` | `f12c0ad6e2c6654be0a6b3dcb95fed8c6c2868c2c0088b8a1e77890f29ad7f0d` |
| `SP\Ezek\tools\check_universals.py` | `198e0c4cd20ca495b4e33a3df639b9e1e61320286a88db870ff5797a640dc341` |
| `SP\Ezek\tools\_adapt_zone_tools_ezek.py` | `5a4fe65f0e01610508d739fdb51de24c63d065503ad8a9e3258fcf1e055e6363` |
| `SP\Ezek\tools\_test_zone_tools_ezek.py` | `eff3169dcda09bfd9ca63a4c8da115d5d0a91c58257585b4ac20cbc0efe478a9` |
| `SP\Ezek\tools\ezek_lib.py` | `cca2c0232b9010f76712077c1d6f736366b338f2bed7ca72f7445b40f9bf151c` |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` |
| `SP\Ezek\tools\verse_map_oshb.json` | `408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\ezek_device_inventory.json` | `0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142` |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` |
| `SP\Ezek\ezek_p0_retained_lows.v1.json` | `7391a57cafb82804eba3a9967273256603774847dc3e9df3916fbec549808cba` |
| `SP\Ezek\ezek_toolkit_review_T1.json` | `2a341d583b3d8d68d8f2f1a953bc40150d8ace090e66b70b1616ef13bbc96a0b` |
| `SP\Ezek\ezek_toolkit_repair_review_T2.json` | `c2c8350c52a8fd09a2f650b10706e2b0fd1d6bc1b8355996fb36eb9cae717976` |
| `SP\Ezek\ezek_controlling_agent_rulings.v1.json` | `d9c54100570edca3e84694703ad294e92c068788eae614e0fb38184168c80d1e` |
| `SP\Ezek\repair\rows_v2_swept_r3.jsonl` | `b526aeb9ad3a950329ae731871b9d9356db27a1aa235d3ae7db80916b728748c` |
| `SP\Ezek\writer\draft_rows_combined.suite_view.manifest.json` | `0233ed2b4f97f6636882f9e77db6a1d7f262d76c8f355cf2f655f17efac24c37` |
| `SP\campaign\_cure_verification.py` | `4c87bc0ec34ad4551195c634d6c7d3cd3d1c848beebd43a59ee6233c0c68917b` |
| `SP\Ezek\ezek_cure_claims.v1.jsonl` | `c79df845fe7142a42daabe6dc6c12f56460f4cd5f61b336d02a67d4f59411e6d` |
| `SP\Jer\tools\citation_sweep.py` | `395b30041231a1e9abf4e195239503864b8700814cf811448fdc490b148a6d7b` |
| `SP\Jer\tools\check_marks.py` | `7405e97a43c49ce63b81e3749fa5b9562e9b737d6e5bc0b9901faf1a99590b0f` |
| `SP\Jer\tools\normalize_hebrew_in_json.py` | `2b324774e1ed8b7a0b463fd36b77e48edb22672f7bc2217c4556f2898feb982e` |

In the rulings file read only rulings T1, R4, S5, G12, Q2, Q3 and Q8 and corpus-wide order CWO-EZ-01. In the strategy read
only section 10 and the recognition-family paragraph of section 2a.

## Questions — answer every one, from the bytes and from your own runs

1. **The FULL TOOLKIT.md** (item 1; this closes rulings Q2 and R5 and carries Q3's fold-ins). Read the whole file at its
   digest. Check every factual statement you can check against the named bytes: counts, verse lists, the ch-40 K/Q entry,
   the frame-spine table (including the MT 8:1 parenthetical), the MT 11:19 note, the flagged regions, and the staged-tools
   section against the code it describes. A corrected fact is often restated elsewhere, so sweep the file for SIBLING
   statements. Report the key phrases you swept and how many statements you reviewed. Give a verdict for the file.
2. **Calendar-date arm** (item 2). Confirm three behaviours. A row opening at MT 45:18, on the messenger formula, passes.
   A dateline claim naming 45:18, 45:20, 45:21 or 45:25 fails, in prose and in refs. A row opening at 45:20, 45:21 or 45:25
   fails. Check the constants against the inventory. Then attack it: negation forms, lists across commas, parentheses,
   ranges covering 45:17-25, a real dateline in the same clause, web: against oshb: refs, and a prose dateline claim naming
   no number. That last case is not judged BY DESIGN; say whether the design leaves a hole that matters.
3. **Recognition-variant families** (item 3). Re-derive from the bytes the wide family 64, 2mp 21, the Adonai form 5 and
   2fp 2, on a consonantal skeleton, using ruling S5's definitions. Confirm that check_universals accepts citations such as
   "refrain-grade, Adonai form (sweep: 5 verses)" for all four families as digit-bearing sweeps in the same sentence, and
   that citation_sweep raises nothing on them.
4. **kq_split losslessness** (item 4) over all 134 notes, with `kq_split` and with `kq_split_bytes`, including the MT 41:8
   backtrack and the MT 48:16 ketiv-only note. Also confirm the non-canonical count of 66.
5. **U+05C4** (item 5). A pointed quote from MT 41:20 or 46:22 that keeps its U+05C4 marks reaches byte tier in
   citation_sweep and is neither a defect nor "fixed" in the normalizer. Is a quote with the marks dropped caught?
6. **The suite reads the chain head directly** (item 6). Run the suite over a PRIVATE COPY of `repair\rows_v2_swept_r3.jsonl`.
   Report every HARD and FLAGS count you get. The orchestrator's runs reported citation_sweep 126, normalizer 2, ngram7 3,
   cap_sweep 2 and mark_symmetry 154, with no puncta or calendar-date problems. Confirm or refute each count. Read the
   `known_side_effect` in the suite-view manifest and confirm that double counting cannot happen on a direct run.
7. **R4 (i)-(iii)** (item 7), one verdict each (ratify / ratify_with_changes / reverse), with the vectors you ran named:
   (i) the QERE tier; (ii) the PUNCTA arms; (iii) the editorial-note tier for K/Q claims. For each, compare with the Jer
   source and say whether the difference is documented and tested.
8. **T2 cure status**: T2-01..T2-05 and D3, each cured / not_cured / partially_cured / no_change_needed. Re-run T2's own
   attacks first (they are described in the T2 deliverable), then variants.
9. **Cure-gate controls (R5, R6)**: run `SP\campaign\_cure_verification.py --selftest` and
   `--claims SP\Ezek\ezek_cure_claims.v1.jsonl --root SP\Ezek`. Does a `.md` claim without `sibling_sweep` get refused? Does
   the supersession record retire EZEK-P0-CURE-toolkit? Is a malformed supersession record refused? Can any path let a
   stale claim read ACCEPTED?

## What you may run, and what you must not

- MAY run: `ezek_lib.py`, `_test_zone_tools_ezek.py` (temp dirs only), `_cure_verification.py` (`--selftest` and `--claims`
  only), and `citation_sweep.py`, `check_marks.py`, `check_universals.py`, `normalize_hebrew_in_json.py` (never `--write`)
  and `run_validator_suite.py`, over PRIVATE COPIES in your own scratch (the suite writes its report beside its input).
- MUST NOT run: `build_verse_maps.py`, either `_adapt_*.py`, `_build_suite_view_ezek.py`, `_summarize_tier0_suite_ezek.py`,
  `_toolkit_selfcheck.py`, any `_cwo*.py` sweep, `_guarded_json_patch.py`, or anything with `--write`. Read those instead.
  Never edit any file anywhere under the worktree.

## Deliverable — `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_rulings_out\ezek_toolkit_supplementary_review_T3.json`

```
{"attempt_id":"ezek_toolkit_supplementary_review_t3_a1","execution_id":"ezek_toolkit_supplementary_review_t3_a1#e1",
 "verdict":"fit_to_accept|fit_with_changes|not_fit",
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest of the bytes you ran and read>"}],
 "toolkit_md":{"verdict":"fit_to_accept|fit_with_changes|not_fit","findings":["<ids from new_findings>"],
               "sibling_sweep":{"key_phrases":["..."],"statements_reviewed":0}},
 "items":{"item2_calendar_arm":{"verdict":"confirmed|refuted|partially_confirmed","vectors_run":["..."],"result":"..."},
          "item3_families":{"verdict":"...","derived_counts":{"wide":0,"2mp":0,"adonai":0,"2fp":0},"vectors_run":["..."],"result":"..."},
          "item4_kq_split":{"verdict":"...","notes_checked":0,"non_canonical":0,"result":"..."},
          "item5_u05c4":{"verdict":"...","vectors_run":["..."],"result":"..."},
          "item6_suite_direct":{"verdict":"...","counts":{"citation_sweep":0,"normalizer":0,"ngram7":0,"cap_sweep":0,"mark_symmetry":0},"result":"..."}},
 "r4":{"i_qere_tier":{"verdict":"ratify|ratify_with_changes|reverse","vectors_run":["..."],"evidence":"..."},
       "ii_puncta_arms":{"verdict":"...","vectors_run":["..."],"evidence":"..."},
       "iii_editorial_note_tier":{"verdict":"...","vectors_run":["..."],"evidence":"..."}},
 "t2_cure_status":[{"item":"T2-01","status":"cured|not_cured|partially_cured|no_change_needed","vector_run":"...","result":"...","evidence":"..."}],
 "cure_gate":{"verdict":"confirmed|refuted|partially_confirmed","runs":["..."],"result":"..."},
 "new_findings":[{"id":"T3-01","severity":"blocker|major|minor|note","artifact":"...","claim":"...","evidence":"...","how_verified":"...","suggested_fix":"..."}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"ezek_toolkit_supplementary_review_t3_a1","execution_id":"ezek_toolkit_supplementary_review_t3_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "verdict":"...","new_finding_count":0,
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
