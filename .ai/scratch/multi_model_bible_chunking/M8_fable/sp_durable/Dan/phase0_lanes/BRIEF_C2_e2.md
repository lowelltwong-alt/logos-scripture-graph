# DANIEL PHASE 0 - LANE C2: STRATEGY CHECK, TEXT FIRST (blind; claude-opus-5-5, OW-25)

Attempt `dan_strategy_check_c2_a1`, execution `dan_strategy_check_c2_a1#e2`. This is a relaunch: execution #e1 was stopped by the account's API session limit and landed no deliverable, so OUT starts empty and nothing of #e1's is yours to use. A lane in the controlling role
(claude-opus-5-5 as a recorded `grader_fallback`, OW-25) wrote Daniel's book strategy. The candidate is pinned below as
`book_strategy_Dan.a1.md` with its plan `strategy_plan_Dan.a1.json`. OW-19 makes two blind check lanes the floor. You are
one of them. The other works by a different method; you will not see it, and it will not see you. Do not try to find
it. You AUDIT the candidate; you do not rewrite it. Fable reviews every book at the campaign's end (OW-28); your
findings are an input to that, not a substitute for it.

`SP` below is `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`. Your output directory, `OUT`, is `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\dan_p0\lane_C2`.

Your method is the text, read before the plan. You form your own view of where Daniel's units turn, and only then
open the candidate and test it against that view. The other lane re-measures the candidate's counts; you need not.

## Your authority, and what is not yours (OW-11)

You write in `OUT`, and nowhere else. You never commit, push, merge, clean or prune; never run git; never write
receipts or touch any registry; never modify, re-serialise, re-generate or run any pinned file except as its use line
allows. Set `PYTHONUTF8=1` for anything that prints Hebrew or Aramaic. Your scripts live in `OUT`, run from there with
`python -B`, and open pinned files read-only by exact path. Never print a whole witness; print counts and short
slices. Quotations are short, sliced by script, and carry their attribution (OSHB/WLC; WEB).

## Stage A - your own reading, BEFORE you open the candidate, its plan, the hardness file or the readiness file

Read the witnesses, the language zones and the parashah marks, through scripts of yours. Write
`OUT\c2_independent_reading.json`:

- `seams`: every place you judge a unit of the book turns, on the WEB face (with the MT dual where the numbering
  differs), each with the text's own signal on BOTH sides and your confidence (high, medium, low);
- `macro_shapes`: the candidate macro-structures you see in the text, with the evidence for and against each;
- `hard_places`: where you expect a careful writer to be unsure, and why.

The text's own signals drive. Parashah marks are single-witness evidence: they inform and never decide. Chapter and
verse divisions, WEB paragraphing, capitalization and punctuation never drive or corroborate a boundary (E-23).
Record the file's sha256 in `final_message.md` before Stage B. Never edit it after that; a later change of mind goes
into Stage B's findings.

## Stage B - test the candidate against the text, recorded in `strategy_check_c2.json`

1. **Seams.** Grade every parent seam and every internal part seam: SUPPORTED (a text signal on both sides), ARGUABLE
   (name the rival reading, and whether the md names it), or UNSUPPORTED (a DEFECT). Then compare with Stage A: each of
   your seams the candidate lacks, and each of its seams you lacked, with whether the md argues the difference.
2. **Macro-shape.** Was the rival shape tested with evidence both ways, and is the adopted one argued from the text?
   Does any shape let a boundary fall inside a verse?
3. **Not a segmentation.** Flag any place the md pre-decides rows instead of naming the evidence and the rivals a
   writer must weigh, and any grade or class question it settles that belongs in `for_fable_end_review`.
4. **Reception neutrality.** Read the hardness file's Daniel entry (lines 66-94 only). Every place the md touches a
   contested reading reports it neutrally and attributes it to its tradition; none moves a seam. A sentence that adopts
   a dating, identification or interpretive position is a DEFECT.
5. **Cross-tradition scope.** The Greek versions and additions, the Qumran fragments and the versions appear as
   metadata in prose only: never as boundary evidence or counterevidence. The insertion point of the Greek additions is
   disclosed and is never a reason for a seam.
6. **Low-confidence regions.** Read the readiness file whole. Name every region your reading and its prepared scrutiny
   targets expect to yield low or medium_low rows that section 7 omits.
7. **Register and hygiene.** Section 8 is copied verbatim into every writer brief. Is it self-contained, free of
   dangling references, and in the register of a planning record for scholars?
8. **Writer part plan.** Does any part concentrate several hard seams so one reviewer carries too much? Is the part
   count justified?
9. **Calendar onsets.** If the md states a working rule on whether a calendar date may open a unit, is it drawn from
   Daniel's own text, are its verses listed on the WEB face with MT duals, and is it in `for_fable_end_review`? If it
   states none, does it say so?

## Verdict

`fit_to_accept` only if no DEFECT stands; otherwise `not_fit`. Every DEFECT carries one of:

- an EXACT correction: the file, the text to find (unique in that file) and the text to replace it with, so the
  orchestrator can apply it by a guarded edit and re-verify; or
- where no exact correction is yours to make, `judgement`: the evidence and the options, for adjudication.

## Budget

About 60 tool calls: about 30 for Stage A, the rest for Stage B.

## Pinned inputs

| input | sha256 |
|---|---|
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\dan_language_zones.json` | `903cf551acd9fc7a4e2a3721bb1431435eeb52141cb0429799f19ad566f70a6b` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\web_mt_offset_map.json` | `833d2ce37d015eccaaaac856d52c1931b9fd26bccb343064013fefc1da603da5` |
| `SP\Dan\verse_inventory.json` | `de3dcac0f4649981a1c4c342add61c65fa7fb8b537261078695e30007924658b` |
| `SP\Dan\tools\dan_lib.py` | `1f397a7a08aba99cad67b0a59378eafa961130559bd8d07a7a9ed9d2f3043361` |
| `SP\Dan\strategy_candidate\book_strategy_Dan.a1.md` | `92981befa96c7651ab814a4894eddd35ba44b9966c8e41fdd11c01bfd5f91c79` |
| `SP\Dan\strategy_candidate\strategy_plan_Dan.a1.json` | `a4dd192d0a56d354c373df3245c30774f483df2f381e0a1439cff0d417840eb5` |
| `SP\campaign\hardness_batch_01.json` | `06eb2a7c6ee5707a409b63a172cd9f808f11a6b7643fc10db475f2d659e40c27` |
| `SP\campaign\daniel_start_readiness.v2.json` | `df6bdba79bec81bffcaac11238e019b6750b4b2578c2aa75bc4238877ae9596b` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `9b47216645716d2db5f76e7306185a89849ac04bfc9991fa4dd389bd1a4b2889` |

How you may use each input:

- `SP\Dan\Dan_web_clean.txt`: READ, through scripts of yours, in Stage A. The WEB text, cleaned, one verse per line, WEB numbering.
- `SP\Dan\Dan_oshb.txt`: READ, through scripts of yours, in Stage A. The witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering.
- `SP\Dan\dan_language_zones.json`: READ, through scripts of yours, in Stage A. Hebrew and Aramaic by verse and by word run; the mixed verse 2:4.
- `SP\Dan\pmarks_Dan.json`: READ, through scripts of yours, in Stage A. Daniel's paratextual marks.
- `SP\Dan\web_mt_offset_map.json`: READ. The WEB/MT crosswalk.
- `SP\Dan\verse_inventory.json`: READ. The verse counts per chapter, declared on the WEB face.
- `SP\Dan\tools\dan_lib.py`: READ; you may import it, running python -B. Daniel's zones, faces and verse order.
- `SP\Dan\strategy_candidate\book_strategy_Dan.a1.md`: READ in Stage B only, through scripts of yours. The candidate strategy.
- `SP\Dan\strategy_candidate\strategy_plan_Dan.a1.json`: READ in Stage B only. The candidate's plan.
- `SP\campaign\hardness_batch_01.json`: READ lines 66-94 only, in Stage B only. Daniel's hardness entry, with its divided readings.
- `SP\campaign\daniel_start_readiness.v2.json`: READ whole, in Stage B only. The prepared scrutiny targets.
- `SP\campaign\grader_models.v1.json`: READ. The grader carrier: the OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only. The M8 ledger: OW-11, the owner's exception, and OW-11-h.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. **`OUT\final_message.md`**, at most 20 lines, written FIRST and rewritten at each stage: the sha256 of
   `c2_independent_reading.json` (recorded before Stage B), the verdict, the DEFECT count by kind, the sha256 of
   `strategy_check_c2.json`, and the statement that you ran no listing and no glob.
2. **`OUT\c2_independent_reading.json`**, as Stage A defines it.
3. **`OUT\strategy_check_c2.json`**, one object: `verdict`, `stage_a_sha256`, `seams`, `stage_a_comparison`,
   `macro_shape`, `not_a_segmentation`, `reception_neutrality`, `cross_tradition`, `low_confidence_regions`,
   `register`, `part_plan`, `calendar_onsets`, `defects` (each: `id`, `section`, `finding`, `evidence`, and
   `exact_correction` {`file`, `find`, `replace`} or `judgement` {`options`}), `what_i_could_not_verify`,
   `e19_selfreport`, `tool_calls_used`, `limit`.

## Hard stops

A pinned digest that differs from the table: record both and stop. Never list, glob or search a directory; a shell
wildcard is a glob, even inside `OUT`. Never write outside `OUT`. Never open the candidate, its plan, the hardness file
or the readiness file before `c2_independent_reading.json` is written and its digest recorded.
