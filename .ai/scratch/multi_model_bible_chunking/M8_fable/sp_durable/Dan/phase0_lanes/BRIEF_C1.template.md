# DANIEL PHASE 0 - LANE C1: STRATEGY CHECK, BYTES AND ARCHITECTURE (blind; claude-opus-5-5, OW-25)

Attempt `dan_strategy_check_c1_a1`, execution `dan_strategy_check_c1_a1#e1`. A lane in the controlling role
(claude-opus-5-5 as a recorded `grader_fallback`, OW-25) wrote Daniel's book strategy. The candidate is pinned below as
`book_strategy_Dan.a1.md` with its plan `strategy_plan_Dan.a1.json`. OW-19 makes two blind check lanes the floor. You are
one of them. The other works by a different method; you will not see it, and it will not see you. Do not try to find
it. You AUDIT the candidate; you do not rewrite it. Fable reviews every book at the campaign's end (OW-28); your
findings are an input to that, not a substitute for it.

`SP` below is `{{SP}}`. Your output directory, `OUT`, is `{{OUT}}`.

Your method is the bytes. Every statement of fact the candidate makes about Daniel's text, counts, numbering, language,
devices or marks is re-measured by a script of yours against the pinned witnesses and inventories. You do not judge
its reading of the book's argument; the other lane does that.

## Your authority, and what is not yours (OW-11)

You write in `OUT`, and nowhere else. You never commit, push, merge, clean or prune; never run git; never write
receipts or touch any registry; never modify, re-serialise, re-generate or run any pinned file except as its use line
allows. Set `PYTHONUTF8=1` for anything that prints Hebrew or Aramaic. Your scripts live in `OUT`, run from there with
`python -B`, and open pinned files read-only by exact path. Never print a whole witness, inventory or the candidate;
print counts and short slices.

## What you verify, recorded in `strategy_check_c1.json`

1. **The validator, then without it.** Run `_validate_strategy_dan.py` once on the two candidate files and record its
   verdict and problems. Then do not rely on it: with a script of yours, re-derive from `verse_inventory.json` every
   parent and part span in the md tables and the plan, its verse count, contiguity, and the tiling of all 357 WEB
   verses exactly once; and measure the internal parent seams of each part against the ones declared and disclosed.
2. **Numbering and duals.** Every `web:` / `oshb:` token pair on a line converts through `web_mt_offset_map.json`
   (never by arithmetic from memory), and every span that starts or ends on a zone verse carries its dual. List every
   wrong or missing pair.
3. **Language.** Every statement of language extent (the runs, the mixed verse 2:4, the per-language verse totals)
   agrees with `dan_language_zones.json`. The md states how rows over the Aramaic run carry their language, and no row
   boundary is placed inside a verse.
4. **Devices and marks.** Every count and device statement in section 2 agrees with `dan_device_inventory.json`,
   converted to the face the md uses. Each named seam's evidence on BOTH sides exists at the verse named: slice it. Every
   claim about parashah marks agrees with `pmarks_Dan.json`, and PE is never conflated with SAMEKH. No chapter or verse
   division, WEB paragraphing, capitalization or punctuation is used to drive or corroborate a boundary (E-23).
5. **Numbers and quotations (E-65).** Every number of two or more digits in the md that is not a verse reference:
   classify it `daniel_measured` (re-measure it and name your script), `lineage` (labelled in the md as another book's
   figure), or `neither`. Every `neither` is a DEFECT. Every opening-words quotation in the parent table is a byte slice
   of `Dan_web_clean.txt` at that verse; every Hebrew or Aramaic quotation is a byte slice of `Dan_oshb.txt`.
6. **Coverage.** Each of the readiness file's prepared scrutiny targets and each of the device inventory's
   `for_fable_end_review` items is disposed in the section the plan names, and the disposition says something (not
   only "noted"). Every boundary risk in the hardness file's Daniel entry appears in section 7.
7. **Provenance (OW-18).** Each count and claim carries its tier. Flag a MEASURED claim that names no script, and any
   word stronger than its evidence: implication is assertion.
8. **Plan and md agree.** Parents, parts, internal parent seams, the lens record and `cal_no_onset` in the plan match
   the md's tables and its sections 2 and 11.

## Verdict

`fit_to_accept` only if no DEFECT stands; otherwise `not_fit`. Every DEFECT carries one of:

- an EXACT correction: the file, the text to find (unique in that file) and the text to replace it with, so the
  orchestrator can apply it by a guarded edit and re-verify; or
- where no exact correction is yours to make, `judgement`: the evidence and the options, for adjudication.

## Budget

About 50 tool calls. At most 2 validator runs. Measure what the candidate states; do not survey the book beyond it.

## Pinned inputs

{{PINS}}

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. **`OUT\final_message.md`**, at most 20 lines, written FIRST and rewritten at the end: the verdict, the DEFECT count
   by kind, the sha256 of `strategy_check_c1.json`, and the statement that you ran no listing and no glob.
2. **`OUT\strategy_check_c1.json`**, one object: `verdict`, `validator`, `tiling`, `numbering_and_duals`, `language`,
   `devices_and_marks`, `numbers_audit`, `coverage`, `provenance`, `plan_md_agreement`, `defects` (each: `id`,
   `section`, `finding`, `evidence`, and `exact_correction` {`file`, `find`, `replace`} or `judgement` {`options`}),
   `what_i_could_not_verify`, `e19_selfreport`, `tool_calls_used`, `limit`.

## Hard stops

A pinned digest that differs from the table: record both and stop. Never list, glob or search a directory; a shell
wildcard is a glob, even inside `OUT`. Never write outside `OUT`.
