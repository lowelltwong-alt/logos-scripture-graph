# FIXUP-2 AUTHOR BRIEF, part W6 (execution #e1): Daniel, ruled row repairs (M8_fable, OW-6b hard-book track)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\fixup2_W6_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\fixup2_W6_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\work\`, created with
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
1. Write nothing outside your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6`: not the scratchpad root, not a sibling OUT, not the worktree. Every
   script you write goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\work\`.
2. Never put code containing a backslash escape (a regex, a byte string, a path with backslashes) through a shell heredoc
   or `python -c`. Write every script to a file in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\work\` with your file-writing tool, then run that file.

## Your role

You are the FIXUP-2 AUTHOR for part W6. Attempt `dan_fixup2_W6_a1`, execution `dan_fixup2_W6_a1#e1`. You authored none of the rows, the
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

## The orders to part W6 (quoted from the rulings file, sha256 43ae72e748fe1e55be3103e826194672a3b317300ff413d690682697b121f940)

### Order 1 (ruling W6-001-WEBREF)

Decision (verbatim): Confirmed row defect (T-WEB-001, MEASURED). The fix places the ref before the quote in the form the corpus uses elsewhere (web:Dan.C.V “…”, as in W4-001 and W4-011) and keeps the (WEB) attribution. The queue's proposed form, “…” (web:Dan.10.2) (WEB), is not used because it produces two adjacent parentheticals. 10:2 lies outside every zone, so no oshb: dual is needed. The residue came from this controlling role's own E1 S1-01 order, which said to change nothing else in the sentence and did not provide for the ref. The FIXUP-1 author followed that order correctly.

Your order (verbatim): Insert the ref before the WEB quote. Nothing else in this field changes.

Exact span, written `"before" -> "after"` (verbatim): ["\"(OSHB/WLC), “In those days” (WEB)\" -> \"(OSHB/WLC), web:Dan.10.2 “In those days” (WEB)\""]

## What you may change (the lander refuses any other difference)

| row | field | licensed by |
|---|---|---|
| W6-001 | strongest_rejected_alternative | W6-001-WEBREF |

The current text of each of those fields, as pinned (JSON strings):

- `W6-001.strongest_rejected_alternative`: "Two candidates were weighed. A one-verse heading at 10:1 (the third-person summary) with the first-person mourning opening at 10:2 was declined: oshb:Dan.10.2 begins בַּיָּמִ֖ים הָהֵ֑ם (OSHB/WLC), “In those days” (WEB), which points back to the time 10:1 has just named, so the heading and the fast read as one setting (INFERRED). Running the unit on to 10:9 was also declined, because the new day and place at 10:4 begin the sighting itself."

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

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\work\`)

1. Copy `SP\Dan\fixup\draft_rows_fixup1_applied.jsonl` byte-identically to `work\rows_base.jsonl` and to
   `work\rows_applied.jsonl`; in the second, replace your part's rows with your revised rows (same order).
2. RUN `run_validator_suite.py` on each copy. The baseline is hard GREEN (MEASURED on these rows). On your rows no
   member may gain a hit; report per member before and after. The web_quotes flag on W6-001 must be gone.
3. RUN `check_placeholders.py` and `ngram7.py` on `work\rows_applied.jsonl`; report their status lines.
4. Confirm by script that every field outside the table is byte-identical (as a JSON value) to the pinned rows.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\fixup2_W6_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_fx2\W6\fixup2_W6_changes.json`:

```
{"attempt_id":"dan_fixup2_W6_a1","execution_id":"dan_fixup2_W6_a1#e1","rows_file_sha256":"<pinned rows digest>",
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
{"attempt_id":"dan_fixup2_W6_a1","execution_id":"dan_fixup2_W6_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup2_W6_rows.jsonl>","changes_sha256":"<sha256 of fixup2_W6_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
