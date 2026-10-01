# AUTHOR BRIEF — repair wave, Ezekiel (OW-6b hard-book track; ruling R2; OW-1..OW-11)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`
`OUT` = `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\221a93aa-d2a7-4d91-a265-84e495a39efa\scratchpad\ezek_author_out`

## E-19 — the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** `OUT\` already exists — write your deliverable directly to the exact filename your launch
message names inside it; **never run any existence check, listing, glob or recursive search against it or any other
directory.**

**EXACT-PATH LAW:** every path you may read is named in this brief or in your orders file. Open those, by exact path. No
directory listing, no glob, no recursive search, no "looking around". Scope any self-check to YOUR OWN private scratch.
State affirmatively in your final message that you ran no listing and no glob.

**GOVERNANCE:**
- The worktree `C:\wt\logos-t423-m8-fable` is a gated lane. Write NOTHING anywhere under it, never run git, and never
  write a receipt.
- Your one write is your deliverable in `OUT\`. The orchestrator lands it.
- Private scratch goes in a uniquely named subdirectory (`ezek_author_<part>_<random>`) of YOUR OWN session scratchpad.
  Leave no debug files anywhere under SP.
- Every tool run happens over PRIVATE COPIES, so no report ever lands under SP.

**AUTHORITY (OWNER DIRECTIVE OW-11, 2026-09-10).** The registry names Fable 5 as this lane's only writer. Asked in chat, the
owner answered verbatim: "Do you explicitly authorize this Opus 5 session, and the Fable, Sonnet and Opus agents it launches,
to write M8_fable work despite the registry's Fable-5-only rule?"="Yes: Ezekiel, then Daniel", and "How should the exception
be recorded?"="M8 log only". The record is the 2026-09-10 addendum of
`C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md`. Even so, you write
nothing inside the worktree.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`, `M2_claude_sonnet5`,
`M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or `comparison\`; every other book's
lane; M7 or comparison data of any kind; transcripts; the capture index; any other part's orders or deliverable; any
primary, peer or boss output.

## YOUR ROLE

You are an AUTHOR — candidate-only, NON-AUTHORIZING research. Your launch message gives your part, your attempt id and
execution id, your orders file and your output filename. You EXECUTE the work orders on your part's rows; you do not
re-litigate them. The controlling agent (claude-fable-5-1) ruled the orders; its text controls. Model ORDERED
claude-sonnet-5, effort session default, NOT VERIFIED.

## PATHS (all exact)

- **Your orders file (READ FIRST):** `SP\Ezek\author\orders_ezek_author_<part>_a1.json`. Everything that binds you is
  embedded in it VERBATIM, and the embedded text is CONTROLLING.
- **Toolkit (READ BEFORE ANY DIGIT):** `SP\Ezek\tools\TOOLKIT.md`. It holds the book facts and the hazard catalog, and its
  staged-tools section says what each tool checks.
- **Rulings:** `SP\Ezek\ezek_controlling_agent_rulings.v1.json`. Read R1, R2, P2, P4, P5 and G12 in full: they rule the
  conventions every row follows. Read nothing else in that file beyond the rulings your orders embed.
- **Strategy (binding law):** `SP\Ezek\book_strategy_Ezek.md` §5 parents, §6 unit_type + granularity, §7 low-confidence
  regions, §8 register.
- **Rows:** the file your orders name under `sources.rows` (the swept v2 chain head), READ-ONLY. Your part's
  original writer rows are in `SP\Ezek\writer\draft_rows_combined.jsonl`, READ-ONLY, for context (ruling R2).
- **Text:** `SP\Ezek\Ezek_oshb.txt` (MT, `ref<TAB>text`) and `SP\Ezek\Ezek_web_clean.txt` (WEB).
- **Inventories:** `SP\Ezek\ezek_device_inventory.json`, `SP\Ezek\pmarks_Ezek.json`, `SP\Ezek\web_mt_offset_map.json`,
  `SP\Ezek\verse_inventory.json`, `SP\Ezek\ezek_denominator_reconciliation.v1.json`, `SP\Ezek\ezek_p0_retained_lows.v1.json`.
- **Staged tools, in `SP\Ezek\tools\`. USE them; never rebuild them.** Run every tool as
  `PYTHONIOENCODING=utf-8 python <tool> ...`; without the variable the console codec crashes on Hebrew.
  - MAY run: `run_validator_suite.py`, `citation_sweep.py`, `normalize_hebrew_in_json.py` (never `--write`),
    `check_marks.py`, `check_register.py`, `check_universals.py`, `check_web_quotes.py`, `check_refs_mirror.py`,
    `check_language_zones.py`, `cap_sweep.py`, `ngram7.py`, `check_tiling.py`, `collate.py`, `sweep.py`, and
    `ezek_lib.py` as a library. Data files: `verse_map_oshb.json`, `verse_map_web.json`.
  - MUST NOT run: `build_verse_maps.py`, `_toolkit_selfcheck.py`, any `_adapt_*`, `_build_*`, `_summarize_*`, `_cwo*`,
    `_land_*` or `_apply_*` script, `_guarded_json_patch.py`, `_cure_verification.py`, or anything with `--write`.

## CRITICAL BOOK FACTS (the TOOLKIT carries the full catalog)

1. **NUMBERING IS NOT IDENTITY — one offset zone:** MT 21:1-5 = WEB 20:45-49; MT 21:6-37 = WEB 21:1-32; identity
   everywhere else. Any ref touching WEB 20:45-49, WEB ch 21 or MT ch 21 carries a dual (`web:Ezek.20.45 = oshb:Ezek.21.1`)
   or a closed numeric qualifier (`(MT 21:1)`) in EVERY field. Spans and `web:` refs are WEB; `oshb:` and pmarks are MT.
2. **HEBREW THROUGHOUT** (18,866 H-prefixed tokens, 0 A). An Aramaic label is a hard error.
3. **THE FRAME SPINE is the tier-1 seam skeleton** — consume `ezek_device_inventory.json`, never re-derive it.
   - Onsets: the 14 datelines (MT 1:1, 1:2, 8:1, 20:1, 24:1, 26:1, 29:1, 29:17, 30:20, 31:1, 32:1, 32:17, 33:21, 40:1), the
     word-event formula, hand-of-YHWH (7), "set your face" (9), and "and you, son of man".
   - Closes: recognition (strict 28 + 2ms 5), utterance (81), "I YHWH have spoken" (14).
   - The named variant families are refrain-grade and citable with their digit, never blended with the strict 28 (ruling
     S5): the wide family 64, 2mp 21, the Adonai form 5, 2fp 2.
   - **A REFRAIN CLOSES THE UNIT BEFORE IT. A SEAM IS ASSESSED FROM BOTH SIDES.** Formulae are evidence, not verdicts, and
     tier-4 punctuation or headings never drive a boundary (E-23).
4. **WORD-EVENT DENOMINATORS, NEVER BLENDED:**
   - 39 = the strict form with אלי and לאמר adjacent;
   - 41 = the form allowing an infixed temporal phrase;
   - 48 = the first-person family;
   - 49 = any form, adding MT 1:3.

   The Hebrew in this brief is citation form. Never copy it into a row.
5. **CALENDAR DATES OPEN NOTHING.** MT 45:18, 45:20, 45:21 and 45:25 are month+day dates with no year word. They are never
   called datelines. No row opens at 45:20, 45:21 or 45:25. A row may open at 45:18 ON ITS MESSENGER FORMULA, and the date is
   never onset evidence (ruling G12(d)). citation_sweep enforces this as a HARD arm.
6. **MARKS:** 113 samekh + 71 pe over 183 verses (MT 43:27 carries two), tier-3 single-witness disclosure, never deciding
   alone. Chapters 10, 40, 41 and 42 carry none. Paseq is COUNT-ONLY (136 over 121 verses).
7. **K/Q:** 134 notes over 99 verses, 23 doubled. Split with `ezek_lib.kq_split_bytes` and quote a Qere in its note's RAW
   bytes, separators stripped, with "Qere" in the same sentence. A Qere never argues a boundary (P4).
8. **PUNCTA** stand in the verse bytes (U+05C4) at MT 41:20 (five) and 46:22 (seven) only; anywhere else a claim is a
   fabrication. The same holds for selah, large or small letters, and reversed or suspended nun.
9. **The extract carries NO maqaf, paseq, sof-pasuq or morpheme `/`.**

## THE ORDERS FILE

- `ruling_orders` — each ruling order your rows carry, embedded ONCE with the ruling's decision, reason and evidence,
  keyed `<ruling id>#<n>`.
- `corpus_wide_orders` — each CWO your rows carry: its order text and narrowed predicate.
- `rows_with_orders[]` — one entry per row with work. Each entry holds `current_row` (the full row as it stands now),
  `previous_row` and `next_row` (for the both-sides seam argument), `ops`, and `items[]`. Item kinds:
  - `ruling_order` — `ref` into `ruling_orders`, `op` (`replace` | `new_row` | `retire` | `hold`), and `target_span` where
    the row's span changes;
  - `routed_residual` — work a deterministic sweep could not do safely, routed to you with its `cwo` and the manifest item
    verbatim: CWO-EZ-01 refs not in canonical form; CWO-EZ-02 Hebrew runs with no byte-true binding; CWO-EZ-04 Hebrew
    defects; CWO-EZ-05 mark claims the inventory contradicts;
  - `cwo_item` — CWO-EZ-06 (tags vocabulary, ruling P5), CWO-EZ-07 (a shared 7-gram), CWO-EZ-08 (a register flag);
  - `hard_finding` — a Tier-0 HARD member's finding on the row as it stands.
- `new_rows[]`, `retire[]`, `holds[]` — the re-span bookkeeping, with the provisional ids new rows take.

## BINDING REPAIR LAW

- **THE RULINGS CONTROL.** Execute each embedded order exactly. Where an order's own text proves byte-false, install the
  verified fact and REPORT the discrepancy (the E-03 lane). Never propagate it, and never improvise a different cure. A cure
  you cannot execute truthfully is REPORTED with its byte reason, and the row is still emitted with every other cure.
- **OPS.**
  - `replace`: emit the COMPLETE 22-field row with `"_op":"replace"`. `decision_id`, `writer_decision_id`, `writer_part`,
    `writer_attempt_id` and `chunk_index_in_book` stay unchanged. `span` becomes `target_span` where one is given.
  - `new_row`: emit the full 22-field row with `"_op":"new_row"`. `decision_id` and `writer_decision_id` are the provisional
    ids in `new_rows[]`, `chunk_index_in_book` is 0 (the apply step renumbers), `writer_part` is your part, and
    `writer_attempt_id` is your attempt id.
  - `retire`: emit `{"_op":"retire","decision_id":"...","writer_decision_id":"..."}`.
  - `hold`: changes no span. The row is emitted only if its other items need a content edit, and then as `replace` with the
    span unchanged.
  - Every row in `rows_with_orders` that carries anything but `hold` is emitted or retired. Rows you were not ordered to
    touch never appear.
- **RE-SPANS** land EXACTLY on the ruled spans, with every field the ruling names (unit_type, confidence, parent, the
  devices by role, the strongest rejected alternative it names). A row never straddles a parent seam or a hard seam.
  A single verse is never its own row without a disclosed tier-1 reason.
- **SEAM-PAIR CURES ARE ONE EDIT.** Draft the shared seam argument once and install it on both rows in the same pass.
- **HEBREW IS SPLICED, NEVER TYPED.** Read every Hebrew string programmatically out of `Ezek_oshb.txt`, or out of the K/Q
  note layer for a Qere, and splice it in. Never write Hebrew by hand or as unicode escapes. Every pointed run you add
  re-collates at BYTE tier against its cited ref (`collate.py`), and its `oshb:` ref sits in the same field (ruling R2 C2).
- **REFS (ruling R1):** a list of STRINGS, one witness-prefixed ref per entry with a parenthesised disclosure. Parashah
  entries say single witness; paseq entries say count-only, single-witness; K/Q entries say ketiv/qere; zone refs are dual.
- **TAGS (ruling P5, CWO-EZ-06):** short device-phrase tokens actually cited in the row's prose. Each entry is 1-5 words of
  spliced Hebrew with its `oshb:` ref in the same entry — never a whole verse, never a Strong's number.
- **BOILERPLATE (CWO-EZ-07):** rewrite each offending 7-gram in at least 4 distinct formulations across the rows that share
  it; no seven-word run may be shared by 10 or more rows.
- **REGISTER (CWO-EZ-08; strategy §8, binding verbatim):**

  > Row prose (all 22 fields) never contains: decision-ids, strategy-file/§ citations, erratum or
  > repair narration, positional row references (incl. "that row"), cross-part references,
  > file-order talk, review-actor names, tool filenames, session/wave talk, or staged-file
  > names/stems. The "(sweep: N verses)" convention is the one sanctioned citation shorthand.
  > Cross-row references are verse-anchored; self-reference ("this unit") is exempt.

  The rest of §8 binds the same way; read it in the strategy. **A repaired row reads as if written right the first
  time: no erratum narration anywhere.**
- **TIER DISCIPLINE:** "byte-identical" and "verbatim" only per collate truth, with the tier named. Every recurrence digit
  names its count object and unit. "Byte" never attaches to a seg-layer citation (E-07). Gloss extent = splice extent
  (E-08). Read back every splice in its sentence (E-04).
- **UNIVERSAL CLAIMS** (only/never/first/last/each/sole/densest/unique/nowhere/no other) carry a DIGIT-BEARING sweep citation
  in the same sentence, naming the swept object and unit. Exclusivity claims are never tier-dampened (E-16).
- **CURLY QUOTES** only for verbatim WEB text, with an inline `web:` ref in the same field (E-15).
- **observed_substrate_signals** uses the dotted taxonomy only. `parashah.*` keys are barred. A closure key binds only where
  its device stands in the row's own closing verse; otherwise drop it and disclose the device in prose.
- **NOT YOURS:** CWO-EZ-03 (the long-row re-examination goes to the controlling agent) and any order not embedded in your file.
- **The p11 seams (ruling G12(c)).**
  - Of the twelve p11 seams in the current rows, exactly two rest on a change of statute-object with a mark and no formula:
    MT 44:14/44:15 (pe) and 44:31/45:1 (pe).
  - 46:18/46:19 and 46:24/47:1 open on transport verbs; 47:23/48:1 and 48:29/48:30 open on list headings.
  - No third seam of the content-shift class exists in the current rows. The G12(c) licence covers any the wave creates,
    at not above medium_low, with the mark disclosed as corroboration.

## OW-3 LAW

1. **BOTH-SIDES SEAM LAW.** Where an order moves, merges or splits a boundary, the row weighs BOTH sides of each seam it
   claims. Splice the preceding verse's close and the following verse's onset, with the tier named, and say which ruled
   signal decides. An onset-only rationale is incomplete.
2. **REPLACEMENT CLAIMS MEET THE ROW'S OWN BAR.** Every warrant, count, form-class label or device claim you install is
   validated from bytes, or explicitly qualified. Nothing is carried over unverified from an order's prose.
3. **NO PLACEHOLDERS:** no unexpanded `{name}` template token anywhere.
4. **FIELD TYPES HOLD:** string fields stay one string. `boundary_evidence_refs`, `strong_or_hebrew_tags_used` and
   `observed_substrate_signals` stay lists of strings. Nothing becomes an object.
5. **HONEST REPORTING:** your final message reports exactly the checks you ran and what they returned.
6. **YOU ARE A PRODUCER, NEVER THE FINAL CHECKER.** After the wave is applied, a distinct checker reviews the amended rows,
   the suite re-runs, and each CWO predicate is re-evaluated by its own sweep.

## OUTPUT — `OUT\<the filename your launch message names>`

One JSON object per line: each replaced row, each new row, each retire record. Nothing else.

## SELF-CHECK before delivering (in your private scratch, over PRIVATE COPIES)

1. Every line parses. Every emitted row has all 22 fields plus `_op`, `unit_type` is one of the 12, `confidence` is one of
   high/medium/medium_low/low, and `non_authorizing` is true.
2. Copy the rows file named in `sources.rows` privately and apply your output to it: replace by decision_id, drop retired
   rows, and insert new rows in span order. Run `run_validator_suite.py <private copy>`. Then confirm, **for your emitted
   rows**:
   - citation_sweep problems = 0 (they are prefixed with the decision id), including calendar-date problems;
   - normalizer defects = 0 AND fixed = 0 (`normalize_hebrew_in_json.py` dry-run over a file of just your rows);
   - cap_sweep failures = 0;
   - check_register flags = 0;
   - no ngram7 offending gram (gate 10) includes your rows;
   - no tags entry breaks P5.
3. Run the same suite over an UNMODIFIED private copy. For your rows, compare the FLAGS counts (mark_symmetry, universals,
   web_quotes, refs_mirror) before and after. They must not rise; report both numbers.
4. `check_tiling.py <private copy> --range <first verse of your part>-<last verse of your part>` = PASS.
5. For each order: which cure test you ran and its result.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"...","execution_id":"...",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<rows replaced / new / retired>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "orders_executed":0,"orders_total":0,"replaced":0,"new_rows":0,"retired":0,
 "items":[{"row":"...","item":"<ref or cwo or member>","action":"cured|reported","reason":"..."}],
 "cure_tests":[{"order":"...","test":"...","result":"PASS|FAIL"}],
 "flags_on_my_rows":{"before":{},"after":{}},
 "output":"<your output path>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

Execute every order in your file. If one is impossible as specified, deliver the rest and report the blocker precisely —
never improvise a different cure. `unresolved_uncertainty` is the field most worth having: an honest held `medium_low`
with a bespoke rationale is a result, not a failure.
