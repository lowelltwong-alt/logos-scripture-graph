# FIXUP-2 AUTHOR BRIEF, part W2 (execution #e1): Daniel, ruled row repairs (M8_fable, OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for a study corpus. You revise a few fields of candidate reading-unit rows under exact orders, slicing quotations byte-for-byte from the Masoretic text (OSHB/WLC) and the World English Bible. The material is ancient scripture and its translation; the task is textual and literary editing.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for Ezekiel and Daniel. Verbatim answers: on authority,
"Yes: Ezekiel, then Daniel"; on recording, "M8 log only". authorization_ref
`lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 807-874
only. You run on claude-opus-5-5 as a recorded grader_fallback (OW-25). You read files under the worktree and write only
under your OUT directory; the orchestrator lands and applies your deliverable. You never run git, never write a receipt
and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\fixup2_W2_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\fixup2_W2_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\work\`, created with
os.makedirs(exist_ok=True) and never tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; every other part's fix-up OUT; the writers', S1's and the
controlling agent's OUT directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`;
transcripts; any file not named in this brief (for example a verse map). Nothing from another book passes as Daniel's
(E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

**HARD STOPS (E-71; both recurred in FIXUP-1):**
1. Write nothing outside your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2`: not the scratchpad root, not a sibling OUT, not the worktree. Every
   script you write goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\work\`.
2. Never put code containing a backslash escape (a regex, a byte string, a path with backslashes) through a shell heredoc
   or `python -c`. Write every script to a file in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\work\` with your file-writing tool, then run that file.

## Your role

You are the FIXUP-2 AUTHOR for part W2. Attempt `dan_fixup2_W2_a1`, execution `dan_fixup2_W2_a1#e1`. You authored none of the rows, the
review or the rulings. The controlling agent (execution dan_controlling_rulings_a2#e1) ruled on the post-FIXUP-1 flags;
its orders to your part are quoted verbatim below. You carry out exactly those orders: nothing outside the named spans
changes. You do not adjudicate a divided reading, select a textual reading or tradition, or move
any seam.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Dan\fixup\draft_rows_fixup1_applied.jsonl` | `2b92198c74bfbd327afa0c0e611dc9c700c097454a0e8ab23663d046e63470df` |
| `SP\Dan\review\dan_controlling_agent_rulings_E2.v1.json` | `43ae72e748fe1e55be3103e826194672a3b317300ff413d690682697b121f940` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\tools\TOOLKIT.md` | `b9e9b59a75721682d5df005e69909cb7e6d7056aab0b1d0a29c7f02cd79269e5` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\tools\run_validator_suite.py` | `5592e8f637dba58542d946dbc8414e350d8c88eea54c6f433eb05303659b348f` |
| `SP\Dan\tools\check_placeholders.py` | `0bb43355a381f44259a4925e953a50c1613afaae74e35ef04fe306427b7e45bb` |
| `SP\Dan\tools\ngram7.py` | `cc6f709c14c85c0d2b8db6bdc0ada37e4dd5b9ae1ce0ecb191a8e281e542c11d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `7357c65c1b7ee1c00a9163e17af42835b0c4c0741f6a615be9e49c4008b3923b` |
| `SP\Dan\web_mt_offset_map.json` | `833d2ce37d015eccaaaac856d52c1931b9fd26bccb343064013fefc1da603da5` |

How you may use each input:

- `SP\Dan\fixup\draft_rows_fixup1_applied.jsonl`: READ your part's rows in full; other rows only where you check a fact. You change ONLY the spans the orders below name, inside the row-fields in the table below.
- `SP\Dan\review\dan_controlling_agent_rulings_E2.v1.json`: READ the rulings quoted below where you check their context (they are quoted verbatim in this brief).
- `SP\Dan\book_strategy_Dan.md`: READ section 8 in full. BINDING.
- `SP\Dan\tools\TOOLKIT.md`: READ where you check a suite member's contract.
- `SP\Dan\Dan_oshb.txt`: READ where you slice Hebrew/Aramaic bytes (OSHB/WLC, MT numbering).
- `SP\Dan\Dan_web_clean.txt`: READ where you slice WEB bytes.
- `SP\Dan\tools\run_validator_suite.py`: RUN on a PRIVATE COPY of the rows in your OUT\work only (it writes its report beside its input). It runs every suite member itself; run no member directly except the two named RUN below.
- `SP\Dan\tools\check_placeholders.py`: RUN on your private copy (it writes nothing).
- `SP\Dan\tools\ngram7.py`: RUN on your private copy (it writes nothing).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only (OW-11, the owner's exception, OW-11-h).
- `SP\Dan\web_mt_offset_map.json`: READ by script to confirm every oshb: dual your orders give (zone rule mt_4_1_to_34 = WEB 4:4-37). If any dual differs, stop and report instead of editing.

## The orders to part W2 (quoted from the rulings file, sha256 43ae72e748fe1e55be3103e826194672a3b317300ff413d690682697b121f940)

### Order 1 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"4.8/4.9 the king's speech\" -> \"web:Dan.4.8 = oshb:Dan.4.5/web:Dan.4.9 = oshb:Dan.4.6 the king's speech\""]

### Order 2 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"open a unit at 4.9;\" -> \"open a unit at web:Dan.4.9 = oshb:Dan.4.6;\""]

### Order 3 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"4.12/4.13 second seeing-and-behold step\" -> \"web:Dan.4.12 = oshb:Dan.4.9/web:Dan.4.13 = oshb:Dan.4.10 second seeing-and-behold step\""]

### Order 4 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"4.17/4.18 recognition formula\" -> \"web:Dan.4.17 = oshb:Dan.4.14/web:Dan.4.18 = oshb:Dan.4.15 recognition formula\""]

### Order 5 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"4.28/4.29 the notice as heading\" -> \"web:Dan.4.28 = oshb:Dan.4.25/web:Dan.4.29 = oshb:Dan.4.26 the notice as heading\""]

### Order 6 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"declined on the mark after 4.28,\" -> \"declined on the mark after web:Dan.4.28 = oshb:Dan.4.25,\""]

### Order 7 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"4.32/4.33 the heavenly voice closes\" -> \"web:Dan.4.32 = oshb:Dan.4.29/web:Dan.4.33 = oshb:Dan.4.30 the heavenly voice closes\""]

### Order 8 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"4.35/4.36 praise closes\" -> \"web:Dan.4.35 = oshb:Dan.4.32/web:Dan.4.36 = oshb:Dan.4.33 praise closes\""]

### Order 9 (ruling CWO03-ZONES)

Decision (verbatim): The 16 zone hits are confirmed and complete. FIXUP-2 W2 rewrites them as 9 exact spans in 7 ref entries of W2-009, W2-010, W2-013, W2-014 and W2-015. A seam pair is written in the strategy's own pair form, each member a web: token with its oshb: dual, in the rows' spaced '=' style. Every bare number in these entries is on the WEB face: each entry's lead token already reads that way (for example web:Dan.4.8 = oshb:Dan.4.5), and the mark after 4.28 is the PE that pmarks_Dan.json records at MT Dan.4.25 and maps to WEB Dan.4.28. Nothing else in the entries changes. No hit is auto-suppressed.

Your order (verbatim): Replace exactly this span and nothing else in the entry. Before writing, confirm each oshb: dual by script through web_mt_offset_map.json (zone rule mt_4_1_to_34 = WEB 4:4-37) or dan_lib.web_to_mt; if any dual differs from the one given here, stop and report instead of editing. The entry's existing lead token and role token stay unchanged.

Exact span, written `"before" -> "after"` (verbatim): ["\"4.35/4.36 end of the praise\" -> \"web:Dan.4.35 = oshb:Dan.4.32/web:Dan.4.36 = oshb:Dan.4.33 end of the praise\""]

The exact entries your orders touch: W2-009.boundary_evidence_refs[4], W2-010.boundary_evidence_refs[5], W2-010.boundary_evidence_refs[6], W2-013.boundary_evidence_refs[4], W2-014.boundary_evidence_refs[6], W2-015.boundary_evidence_refs[4], W2-015.boundary_evidence_refs[5].

## What you may change (the lander refuses any other difference)

| row | field | licensed by |
|---|---|---|
| W2-009 | boundary_evidence_refs | CWO03-ZONES |
| W2-010 | boundary_evidence_refs | CWO03-ZONES |
| W2-013 | boundary_evidence_refs | CWO03-ZONES |
| W2-014 | boundary_evidence_refs | CWO03-ZONES |
| W2-015 | boundary_evidence_refs | CWO03-ZONES |

The current text of each of those fields, as pinned (JSON strings):

- `W2-009.boundary_evidence_refs`: ["web:Dan.4.4 = oshb:Dan.4.1 [WARRANT-onset:near] first-person opener (i_nebuchadnezzar_aram)", "web:Dan.4.3 = oshb:Dan.3.33 [WARRANT-onset:far] doxology closes the prescript", "web:Dan.4.9 = oshb:Dan.4.6 [WARRANT-close:near] address to Belteshazzar requesting dream and interpretation; paseq (single-witness)", "web:Dan.4.10 = oshb:Dan.4.7 [WARRANT-close:far] recital opener: visions of my head; seeing and behold", "web:Dan.4.8 = oshb:Dan.4.5 [WARRANT-rival:far] 4.8/4.9 the king's speech could open a unit at 4.9; declined, it would exceed 9 verses", "oshb:Dan.4.4 = web:Dan.4.7 [DISCLOSURE-kq] K/Q, 2 note(s): reading-form disclosure"]
- `W2-010.boundary_evidence_refs`: ["web:Dan.4.10 = oshb:Dan.4.7 [WARRANT-onset:near] report opener: visions of my head, seeing and behold", "web:Dan.4.9 = oshb:Dan.4.6 [WARRANT-onset:far] the request for the dream closes", "web:Dan.4.18 = oshb:Dan.4.15 [WARRANT-close:near] king's charge closes the recital; paseq twice (single-witness)", "web:Dan.4.19 = oshb:Dan.4.16 [WARRANT-close:far] Daniel's dismay; weak opener then", "web:Dan.4.14 = oshb:Dan.4.11 [DISCLOSURE-device] the watcher's decree opens, heavenly discourse inside the report", "web:Dan.4.13 = oshb:Dan.4.10 [WARRANT-rival:near] 4.12/4.13 second seeing-and-behold step; declined as a scene step inside the report", "web:Dan.4.17 = oshb:Dan.4.14 [WARRANT-rival:far] 4.17/4.18 recognition formula closes the watcher's decree; declined, the charge closes the recital", "oshb:Dan.4.9 = web:Dan.4.12 [DISCLOSURE-kq] ketiv/qere, 1 note(s), disclosed as reading form", "oshb:Dan.4.13 = web:Dan.4.16 [DISCLOSURE-kq] K/Q, 1 note(s): reading-form disclosure", "oshb:Dan.4.14 = web:Dan.4.17 [DISCLOSURE-kq] K/Q (3) at this verse, reading form, not a seam reason", "oshb:Dan.4.15 = web:Dan.4.18 [DISCLOSURE-kq] ketiv/qere, 2 note(s), disclosed as reading form"]
- `W2-013.boundary_evidence_refs`: ["web:Dan.4.28 = oshb:Dan.4.25 [WARRANT-onset:near] narrator's summary notice after the speech", "web:Dan.4.27 = oshb:Dan.4.24 [WARRANT-onset:far] Daniel's counsel closes the speech", "oshb:Dan.4.25 = web:Dan.4.28 [WARRANT-close:near] PE after this verse (single-witness)", "web:Dan.4.29 = oshb:Dan.4.26 [WARRANT-close:far] twelve-months phrase, a month word and not a date", "web:Dan.4.29 = oshb:Dan.4.26 [WARRANT-rival:merge] 4.28/4.29 the notice as heading of the fulfilment account; declined on the mark after 4.28, alternative live"]
- `W2-014.boundary_evidence_refs`: ["web:Dan.4.29 = oshb:Dan.4.26 [WARRANT-onset:near] scene opener with the twelve-months phrase (texture)", "web:Dan.4.28 = oshb:Dan.4.25 [WARRANT-onset:far] PE after this verse (single-witness)", "web:Dan.4.33 = oshb:Dan.4.30 [WARRANT-close:near] fulfilment notice (at_that_moment_aram)", "web:Dan.4.34 = oshb:Dan.4.31 [WARRANT-close:far] return to the king's own voice; raised eyes and blessing", "web:Dan.4.30 = oshb:Dan.4.27 [DISCLOSURE-device] the boast (answered_and_said_aram_loose)", "web:Dan.4.31 = oshb:Dan.4.28 [DISCLOSURE-device] voice from heaven, discourse inside the narrative", "web:Dan.4.32 = oshb:Dan.4.29 [WARRANT-rival:far] 4.32/4.33 the heavenly voice closes; declined, the fulfilment belongs with the decree it executes", "oshb:Dan.4.29 = web:Dan.4.32 [DISCLOSURE-kq] K/Q, 1 note(s): reading-form disclosure"]
- `W2-015.boundary_evidence_refs`: ["web:Dan.4.34 = oshb:Dan.4.31 [WARRANT-onset:near] king's own voice returns; blessing; paseq (single-witness)", "web:Dan.4.33 = oshb:Dan.4.30 [WARRANT-onset:far] fulfilment notice closes the judgment", "web:Dan.4.37 = oshb:Dan.4.34 [WARRANT-close:near] closing praise; PE after this verse (single-witness); parent seam", "web:Dan.5.1 [WARRANT-close:far] new reign and feast (context verse, read and not tiled)", "web:Dan.4.36 = oshb:Dan.4.33 [WARRANT-rival:near] 4.35/4.36 praise closes before the resumed account; declined, the restoration clause repeats", "web:Dan.4.35 = oshb:Dan.4.32 [WARRANT-rival:far] 4.35/4.36 end of the praise", "oshb:Dan.4.31 = web:Dan.4.34 [DISCLOSURE-kq] K/Q, 1 note(s): reading-form disclosure", "oshb:Dan.4.32 = web:Dan.4.35 [DISCLOSURE-kq] K/Q (2) at this verse, reading form, not a seam reason"]

Change only the spans the orders name inside those fields; every other byte of the field stays as it is (for a list
field, every entry the orders do not name stays byte-identical). Any field not in the table stays byte-identical. If an order cannot be carried out as written (a
count differs, a slice does not match, an order would need a field outside the table), do not improvise: leave that
field unchanged and report it in the change log as `blocked` with the measured evidence.

## Suite duties your new text must keep (the suite is the mechanical judge)

- placeholder: no unfilled template placeholder (%s, %(x)s, {name}, {0}, {}) in any field of any row.
- Never hand-type Hebrew: every Hebrew/Aramaic run is SLICED by script from `SP\Dan\Dan_oshb.txt`, byte-identical,
  with its (OSHB/WLC) attribution.
- WEB quotations are SLICED by script from `SP\Dan\Dan_web_clean.txt`, in double curly quotes, attributed (WEB) (the
  A6-b convention).
- register rule: this is a scholar-facing record; no staged file names, internal rule labels, row pointers or process
  talk in row prose.
- single-witness: keep the literal single-witness disclosure wherever a mark, paseq or puncta entry already carries it.
- A mark is cited at the verse it FOLLOWS; do not re-cite marks.
- A categorical claim ("no", "only", "every") stands only if the thing is absent from BOTH inputs (C2-amended); add none.
- 7-gram: add no run of seven words that repeats across rows; where a disclosure recurs, keep at least 4 distinct
  formulations. Context (controlling ruling S1-07, verbatim): "the paseq and K/Q disclosure clusters stand at 7 rows
  each (gate 10), MEASURED on the pre-fix-up rows."
- Language zones: keep the Aramaic island (2:4b-7:28) disclosure, the 2:4a/2:4b half where present, and BOTH faces
  (web: with its oshb: dual) for any reference inside a numbering zone.
- Refs: the DEF-A4-ARGUED entries, each ROLE token, face qualifier and seam pair live in boundary_evidence_refs; keep
  every lead token and role token as it is.
- cap_sweep is out of scope (no seam moves).

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\work\`)

1. Copy `SP\Dan\fixup\draft_rows_fixup1_applied.jsonl` byte-identically to `work\rows_base.jsonl` and to
   `work\rows_applied.jsonl`; in the second, replace your part's rows with your revised rows (same order).
2. RUN `run_validator_suite.py` on each copy. The baseline is hard GREEN (MEASURED on these rows). On your rows no
   member may gain a hit; report per member before and after. The new web: tokens may add refs_mirror worklist entries or citation_sweep items: report each one; they are triaged by the orchestrator, never suppressed.
3. RUN `check_placeholders.py` and `ngram7.py` on `work\rows_applied.jsonl`; report their status lines.
4. Confirm by script that every field outside the table is byte-identical (as a JSON value) to the pinned rows.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\fixup2_W2_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W2\fixup2_W2_changes.json`:

```
{"attempt_id":"dan_fixup2_W2_a1","execution_id":"dan_fixup2_W2_a1#e1","rows_file_sha256":"<pinned rows digest>",
 "changes":[{"row":"<id>","field":"<field>","order":"<ruling id>","before":"<exact removed span>","after":"<exact new span>",
             "tier":"MEASURED|EXTRACTED|TRANSCRIBED|REPORTED|INFERRED","evidence":"<script + input + slice/count output>"}],
 "blocked":[{"order":"<ruling id>","why":"...","evidence":"..."}],
 "suite":{"base":{"<member>":"<status>"},"applied":{"<member>":"<status>"},"hits_on_my_rows_before_after":{}},
 "untouched_fields_identical":true}
```

## Budget

Keep to roughly 35 tool calls. Report exactly what you ran and what it returned.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"dan_fixup2_W2_a1","execution_id":"dan_fixup2_W2_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup2_W2_rows.jsonl>","changes_sha256":"<sha256 of fixup2_W2_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
