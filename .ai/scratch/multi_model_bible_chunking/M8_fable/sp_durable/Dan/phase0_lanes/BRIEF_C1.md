# DANIEL PHASE 0 - LANE C1: STRATEGY CHECK, BYTES AND ARCHITECTURE (blind; claude-opus-5-5, OW-25)

Attempt `dan_strategy_check_c1_a1`, execution `dan_strategy_check_c1_a1#e1`. A lane in the controlling role
(claude-opus-5-5 as a recorded `grader_fallback`, OW-25) wrote Daniel's book strategy. The candidate is pinned below as
`book_strategy_Dan.a1.md` with its plan `strategy_plan_Dan.a1.json`. OW-19 makes two blind check lanes the floor. You are
one of them. The other works by a different method; you will not see it, and it will not see you. Do not try to find
it. You AUDIT the candidate; you do not rewrite it. Fable reviews every book at the campaign's end (OW-28); your
findings are an input to that, not a substitute for it.

`SP` below is `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`. Your output directory, `OUT`, is `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\dan_p0\lane_C1`.

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

| input | sha256 |
|---|---|
| `SP\Dan\strategy_candidate\book_strategy_Dan.a1.md` | `92981befa96c7651ab814a4894eddd35ba44b9966c8e41fdd11c01bfd5f91c79` |
| `SP\Dan\strategy_candidate\strategy_plan_Dan.a1.json` | `a4dd192d0a56d354c373df3245c30774f483df2f381e0a1439cff0d417840eb5` |
| `SP\Dan\_validate_strategy_dan.py` | `7e2bbbd67d3d2c3403251f55c2008d0a1da23a6a71542e253aa66c12dd80e779` |
| `SP\Dan\verse_inventory.json` | `de3dcac0f4649981a1c4c342add61c65fa7fb8b537261078695e30007924658b` |
| `SP\Dan\web_mt_offset_map.json` | `833d2ce37d015eccaaaac856d52c1931b9fd26bccb343064013fefc1da603da5` |
| `SP\Dan\web_mt_verse_check.json` | `eae814951c13e31815d78312bca0439067f871066fbbc3940df8bd0b4ff39a6d` |
| `SP\Dan\dan_language_zones.json` | `903cf551acd9fc7a4e2a3721bb1431435eeb52141cb0429799f19ad566f70a6b` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\tools\dan_lib.py` | `1f397a7a08aba99cad67b0a59378eafa961130559bd8d07a7a9ed9d2f3043361` |
| `SP\campaign\daniel_start_readiness.v2.json` | `df6bdba79bec81bffcaac11238e019b6750b4b2578c2aa75bc4238877ae9596b` |
| `SP\campaign\hardness_batch_01.json` | `06eb2a7c6ee5707a409b63a172cd9f808f11a6b7643fc10db475f2d659e40c27` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `9b47216645716d2db5f76e7306185a89849ac04bfc9991fa4dd389bd1a4b2889` |

How you may use each input:

- `SP\Dan\strategy_candidate\book_strategy_Dan.a1.md`: READ, through scripts of yours. The candidate strategy.
- `SP\Dan\strategy_candidate\strategy_plan_Dan.a1.json`: READ. The candidate's plan.
- `SP\Dan\_validate_strategy_dan.py`: RUN `python -B ... --md <the candidate md> --plan <the candidate plan>` only (it writes nothing); READ. The strategy validator.
- `SP\Dan\verse_inventory.json`: READ. The verse counts per chapter, declared on the WEB face.
- `SP\Dan\web_mt_offset_map.json`: READ. The WEB/MT crosswalk.
- `SP\Dan\web_mt_verse_check.json`: READ. The per-chapter verse counts on both faces.
- `SP\Dan\dan_language_zones.json`: READ, through scripts of yours. Hebrew and Aramaic by verse and by word run; the mixed verse 2:4.
- `SP\Dan\dan_device_inventory.json`: READ, through scripts of yours. Daniel's device inventory, MT face.
- `SP\Dan\pmarks_Dan.json`: READ, through scripts of yours. Daniel's paratextual marks.
- `SP\Dan\Dan_oshb.txt`: READ, through scripts of yours. The witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering.
- `SP\Dan\Dan_web_clean.txt`: READ, through scripts of yours. The WEB text, cleaned, one verse per line, WEB numbering.
- `SP\Dan\tools\dan_lib.py`: READ; you may import it, running python -B. Daniel's zones, faces and verse order.
- `SP\campaign\daniel_start_readiness.v2.json`: READ whole. The prepared scrutiny targets.
- `SP\campaign\hardness_batch_01.json`: READ lines 66-94 only. Daniel's hardness entry and boundary risks.
- `SP\campaign\grader_models.v1.json`: READ. The grader carrier: the OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only. The M8 ledger: OW-11, the owner's exception, and OW-11-h.

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
