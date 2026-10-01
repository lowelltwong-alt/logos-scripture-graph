# WRITER BRIEF: candidate chunk rows for Daniel, part {{PART}} (M8_fable, m8-mesh-r3)

You are one of SIX part-writers in the M8_fable Daniel cycle. The work is candidate-only, NON-AUTHORIZING research that
will be reviewed adversarially. This brief is binding. Attempt `{{ATTEMPT}}`, execution `{{EXECUTION}}`.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `{{OUT}}` already exists. Write your deliverable directly to
`{{OUT}}\{{DELIVERABLE}}`. **Never run any existence check, listing, glob or recursive search against it or any other
directory.** A shell wildcard is a glob.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No directory
listing, no glob, no recursive search, no looking around. State in your final message that you ran no listing and no
glob.

## GOVERNANCE

- SP is `{{SP}}`. It is read-only for you. Write nothing under SP, not even a debug file.
- Every file you write goes under `{{OUT}}`: the deliverable at the exact path above, and your own scripts, private
  copies and tool reports under `{{OUT}}\work\`. Nothing anywhere else.
- Never run git, never write a receipt, never touch any registry.
- **FORBIDDEN LANES:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
  `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
  `comparison\`, every other book's directory under SP, and every other writer's OUT. Never read another model's
  output; never seek convergence.
- **Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` in the
  environment and run `python -B`. The environment variable is required because the validator suite starts its members
  as child processes, and `-B` alone does not reach them; without it a child process writes bytecode into
  `SP\Dan\tools\`, which is a write under SP.
- **The tools you may RUN** are exactly these, each only on a PRIVATE COPY of your rows under `{{OUT}}\work\`:
  `SP\Dan\tools\check_tiling.py`, `SP\Dan\tools\run_validator_suite.py` (it writes `<copy>.validator_report.json`
  beside its input, so it must only ever see a copy in your `work\`), and
  `SP\Dan\writer_lanes\_validate_writer_part_dan.py` (it writes nothing). You may import `SP\Dan\tools\dan_lib.py`
  from your own scripts. Every other pinned tool is READ ONLY. Never run any other tool: several tools under
  `SP\Dan\tools\` overwrite files in SP when run.

## PINNED INPUTS

Verify nothing you read has changed: these are the sha256 digests of the files as this brief was built.

{{PINS}}

**Read first:** `SP\Dan\tools\TOOLKIT.md` (book facts, hazards, the tools' contracts) and `SP\Dan\book_strategy_Dan.md`
whole. The strategy is BINDING; where this brief and the strategy seem to differ, follow the strategy and say so in
`unresolved_uncertainty`. Where the toolkit and a tool's code differ, the code is the contract.

## YOUR PART

{{PART_FACTS}}

## CRITICAL BOOK FACTS (all from Daniel's own files; read the strategy for the evidence)

1. **Two languages.** Hebrew 1:1 to 2:4 word 4; Aramaic 2:4 word 5 to 7:28; Hebrew 8:1-12:13. MT 2:4 is the one mixed
   verse. Every row carries `language` from `dan_language_zones.json` `verse_language`: `H`, `A` or `mixed` (a row
   whose verses are all one language takes that language; any other row is `mixed`). A row covering 2:4 carries
   `mixed` and states: "covers the 2:4 word-level switch (Hebrew words 1-4, Aramaic words 5 onward)". A quotation
   from 2:4 names its half. Aramaic material is quoted from the OSHB/WLC Aramaic and labelled Aramaic, never Hebrew.
   Language never moves a seam, and no row boundary falls inside a verse.
2. **Numbering is not identity in four zones.** MT 3:31-33 = WEB 4:1-3; MT 4:1-34 = WEB 4:4-37; MT 6:1 = WEB 5:31;
   MT 6:2-29 = WEB 6:1-28. Every other verse is identity. Row spans and plain C:V refs are WEB. **Every mention of a
   zone verse, in any field except `span`, is written as a pair on the same line:** `web:Dan.4.1`=`oshb:Dan.3.31`,
   or for a range `web:Dan.6.25`-`web:Dan.6.28`=`oshb:Dan.6.26`-`oshb:Dan.6.29`. Never a bare `4:5`, never a bare
   `Dan.4.5`, never a bare MT number such as `3:31` or `6:29`. Convert only through `web_mt_offset_map.json` or
   `dan_lib.web_to_mt` / `dan_lib.mt_to_web`, never by arithmetic from memory. The device inventory, the parashah
   marks and the K/Q layer are on the MT face.
3. **The 8 datelines** (MT 1:1, 2:1, 7:1, 8:1, 9:1, 9:2, 10:1, 11:1) and the other devices are EXTRACTED in
   `dan_device_inventory.json`; consume it, do not re-derive. **10:4 carries the single calendar date** and is
   not one of the eight dateline entries; its status as a seam is left open by the strategy (§2 disclosure objects,
   §7(n)), so weigh it there. 9:2 resumes the 9:1 frame and 11:1 stands inside the messenger's direct speech: both are
   texture, never tier-1 (§2 D2).
4. **Marks.** 30 parashah marks, 22 PE and 8 SAMEKH, each after a verse on the MT face. They are single-witness
   evidence: they inform and never decide. Cite PE or SAMEKH by name, never "a mark". Paseq is count-only; a K/Q note
   enters a row only as a reading-form disclosure. The validator warns on a covered K/Q verse the row never names.
5. **Fabrication classes.** Daniel's text has no selah, no large, small, suspended or reversed letter and no puncta
   (U+05C4/U+05C5). A claim of any of these is a fabrication. The extract `Dan_oshb.txt` carries no maqaf, no paseq,
   no sof-pasuq and no morpheme `/`, so a pattern written with them matches nothing.
6. **Cross-tradition material** (Old Greek, Theodotion, the Greek additions, Qumran, 4Q242, Targum, Peshitta,
   Vulgate) is prose metadata only: never a `boundary_evidence_refs` entry, never evidence. The Greek insertion
   point at 3:23/3:24 is never a reason for a seam.
7. **No other book's figures.** Nothing measured in another book passes as Daniel's (E-65); do not name another
   book's counts at all.
8. **Never quote Hebrew or Aramaic from TOOLKIT.md or the strategy**, which carry citation forms. Row bytes come from
   `Dan_oshb.txt`, always.

## TASK

Tile your part's WEB range **exactly** (no gap, no overlap, no verse outside it) with chunk rows per the strategy:

- **§5 parents.** A row never straddles a parent seam. Your part's internal parent seams are listed above.
  `parent_collection` opens with the parent id, then its title in parentheses, as listed under YOUR PART.
- **§6 unit_type**, the closed vocabulary of 8: `narrative`, `dialogue`, `royal_proclamation`, `doxology_or_prayer`,
  `dream_or_vision_report`, `interpretation`, `heavenly_discourse`, `summary_notice`. A row takes exactly one, and the
  row names its evidence. A per-bytes deviation from the plain reading is disclosed in one sentence in `device_notes`.
- **§6 granularity.** 2 to 9 verses. A one-verse row only for a `summary_notice` or a zone or mixed-verse disclosure
  you justify. Above 9 only for a single speech act with no internal tier-2 signal, and the row says so. Obey the
  over-split guards (a)-(d) and the under-split guard of §6.
- **Seams from both sides.** A refrain or doxology is close-side evidence for the unit before it; it does not by itself
  fix the next edge. Every edge is weighed on both sides, from the bytes. Read the verse on either side of your part
  as read-only context.
- **§7 low-confidence posture.** Hold honestly at `medium_low` or `low` with a bespoke rationale rather than force a
  boundary. A seam with one-sided evidence, or evidence only from a mark, is `low` or `medium_low`. Never round up.
- **§8 register and hygiene**, reproduced verbatim below from the pinned strategy, is binding.

{{SECTION8}}

## OUTPUT: one JSONL row per chunk, 23 fields, in span order, to `{{OUT}}\{{DELIVERABLE}}`

```
decision_id            "{{PART}}-001", "{{PART}}-002", ... in span order
book                   "Dan"
model_id               "M8_fable"
chunk_index_in_book    1, 2, 3, ... in span order within your part (the orchestrator renumbers book-wide)
span                   "Dan.C.V-Dan.C.V" on the WEB face; a one-verse row is written X-X
boundary_rationale     prose: the onset evidence and the close evidence, BOTH SIDES of each edge, byte-cited
boundary_evidence_refs list of strings, each a ref with its disclosure in parentheses, for example
                       "oshb:Dan.8.1 (dateline; return to Hebrew at word 1)" or
                       "web:Dan.4.1 = oshb:Dan.3.31 (epistolary prescript; zone dual)"; the suite checks the grammar
strongest_rejected_alternative  the best boundary you did NOT take, and why
literature_type_guess  free label
confidence             high | medium | medium_low | low
strong_or_hebrew_tags_used      list of strings; any Hebrew or Aramaic in it is spliced from Dan_oshb.txt
wj_or_red_letter_considered     boolean: whether you considered a words-of-Jesus / red-letter layer
frontier_flag_considered        true when the row carries a question for Fable's end review
non_authorizing        true
review_status          "pending"
parent_collection      "PA".."PJ" then the title in parentheses
unit_type              one of the 8
writer_part            "{{PART}}"
writer_decision_id     "{{PART}}-<n>"
writer_attempt_id      "{{ATTEMPT}}"
observed_substrate_signals  list of strings: the device ids from dan_device_inventory.json and the marks you weighed
device_notes           disclosures: category deviations, K/Q, paseq, zone pairs, the 2:4 switch, Greek metadata
language               "H" | "A" | "mixed"
```

## HEBREW AND ARAMAIC: SPLICE IT, NEVER TYPE IT

Build every Hebrew or Aramaic string by reading it programmatically out of `Dan_oshb.txt` and splicing it in. Never
hand-type it and never write it as unicode escapes: hand-typed Hebrew is the E-01 failure class, and it is avoidable
because the source is in front of you. A **Qere** is the one exception to "it must be in the verse bytes": it lives
in the K/Q note layer of `pmarks_Dan.json` (`kq`). Cite it from there with the morpheme separators `/` removed, and
disclose it as a Qere. Quotations are short and carry their attribution (OSHB/WLC; WEB).

## SELF-CHECK BEFORE YOU RETURN (on a private copy in `{{OUT}}\work\`)

1. `check_tiling.py <copy> --range {{RANGE}}` (it prints its verdict).
2. `_validate_writer_part_dan.py <copy> --part {{PART}} --attempt {{ATTEMPT}}`: it must say GREEN. Read its warnings
   and either cure each or answer it in the row (a one-verse row's justification, a long row's single-speech-act
   statement, a K/Q verse named).
3. `run_validator_suite.py <copy>`: read `summary` in the report it writes beside the copy. Cure every HARD failure.
   Report the FLAGS you left and why.
4. Your own programmatic check, on the finished file, that every Hebrew and Aramaic run is a substring of
   `Dan_oshb.txt` or a Qere from the K/Q layer.
5. Copy the cured copy to the deliverable path, then re-run steps 1 and 2 on a fresh copy of the deliverable.

Report exactly what you ran and what it returned. A claimed tool run that did not happen is the worst thing you can
put in a record. The orchestrator re-runs all three tools on your deliverable independently. They are deterministic
and prove form, not judgment: your seams are judged by the review lanes and by Fable at the campaign's end.

## YOUR FINAL MESSAGE (evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"{{ATTEMPT}}","execution_id":"<the execution id named at the top of this brief>",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<rows written>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "rows_written":0,"span_covered":"...","tiling_check":"PASS|FAIL","validator_verdict":"GREEN|RED",
 "suite_hard_status":"GREEN|RED","suite_flags_left":["..."],
 "deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

`unresolved_uncertainty` is the field most worth having and the easiest to leave empty. **Held low confidence is a
result, not a failure**: this campaign would far rather have an honest `low` with a bespoke rationale than a forced
`high`.
