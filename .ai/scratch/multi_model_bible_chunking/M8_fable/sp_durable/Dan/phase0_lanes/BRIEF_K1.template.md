# DANIEL PHASE 0 - LANE K1: TOOLKIT REVIEW, BYTES (blind; claude-opus-5-5, OW-25)

Attempt `dan_toolkit_review_k1_a1`, execution `dan_toolkit_review_k1_a1#e1`. The orchestrator wrote Daniel's shared
verification toolkit, `TOOLKIT.md`, pinned below. Every later lane that annotates Daniel reads it and trusts its "Book
facts" as settled, so a wrong figure or rule in it reaches every one of them. OW-19 makes two blind review lanes the
floor. You are one of them. The other works by a different method; you will not see it, and it will not see you. Do not
try to find it. You AUDIT the toolkit; you do not rewrite it. Fable reviews every book at the campaign's end (OW-28);
your findings are an input to that, not a substitute for it.

`SP` below is `{{SP}}`. Your output directory, `OUT`, is `{{OUT}}`.

Your method is the bytes. Every statement of fact `TOOLKIT.md` makes about Daniel's text, numbering, language, marks,
notes, devices, data files and strategy is re-measured by a script of yours against the pinned witnesses and
inventories. You do not judge the tools' code; the other lane does that.

## Your authority, and what is not yours (OW-11)

You write in `OUT`, and nowhere else. You never commit, push, merge, clean or prune; never run git; never write
receipts or touch any registry; never modify, re-serialise, re-generate or run any pinned file except as its use line
allows. Set `PYTHONUTF8=1` for anything that prints Hebrew or Aramaic. Your scripts live in `OUT`, run from there with
`python -B`, and open pinned files read-only by exact path. A script of yours that reads Hebrew or Aramaic imports
`dan_lib.skeleton` for any consonantal comparison (E-66). Never print a whole witness, inventory or the toolkit; print
counts and short slices.

## What you verify, recorded in `toolkit_review_k1.json`

1. **Book facts.** Every figure and every factual sentence in the sections "Book facts" through "DEVICE SPINE"
   (numbering and the four zones, language, the parashah layer, the fabrication classes, the disclosure inventories,
   the device spine): re-measure it from the file the toolkit names for it and record `confirmed` or `defect`, with
   your script's name and its measured value. Every "NONE" or "0" absence claim is re-swept on the bytes.
2. **Data files and encoding notes.** Every figure in the "Data files" table and in "Encoding + skeleton notes"
   (line counts and their classes, the word and token totals, the maqaf and seg counts, NFC, the skeleton behaviour on
   a maqaf) is re-measured the same way. The WEB extract's classes must sum to its line count.
3. **Strategy section.** Every figure and structural statement in "Reconciled strategy" agrees with the pinned
   strategy md and plan.
4. **Numbers (E-65).** E-65 bans any Ezekiel figure from a Daniel artifact. The toolkit's automated guard is blind in
   three ways: it ignores every number below 100, it cannot flag a number that is also a true Daniel figure, and it
   cannot see a non-integer. So audit every number in `TOOLKIT.md`, of ANY size, integer or not, that is not a verse or
   chapter reference, a date, a digest or a ledger identifier (E-nn, OW-nn, L-nnnn): classify it `daniel_measured`
   (re-measured by a named script of yours, with the value), `lineage` (labelled in the text as another book's figure)
   or `neither`. Every `neither` is a DEFECT, and so is a `daniel_measured` number whose re-measurement differs.
5. **Rules against the bytes.** Each rule the toolkit states about the data (for example which face a file is keyed
   to, where a disclosure is required, what counts as a fabrication in Daniel) is consistent with the pinned files.
   Flag a rule the bytes contradict.
6. **Provenance (OW-18).** A figure stated as verified or byte-proven that you cannot reproduce from the pinned bytes
   is a DEFECT; any word stronger than its evidence is flagged: implication is assertion.

## Verdict

`fit_to_accept` only if no DEFECT stands; otherwise `not_fit`. Every DEFECT carries one of:

- an EXACT correction: the text to find (unique in `TOOLKIT.md`) and the text to replace it with, so the orchestrator
  can apply it by a guarded edit and re-verify; or
- where no exact correction is yours to make, `judgement`: the evidence and the options, for adjudication.

## Budget

About 50 tool calls. Measure what the toolkit states; do not survey the book beyond it.

## Pinned inputs

{{PINS}}

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. **`OUT\final_message.md`**, at most 20 lines, written FIRST and rewritten at the end: the verdict, the DEFECT count
   by section, the sha256 of `toolkit_review_k1.json`, and the statement that you ran no listing and no glob.
2. **`OUT\toolkit_review_k1.json`**, one object: `verdict`, `book_facts`, `data_files_and_encoding`, `strategy`,
   `numbers_audit` (every number: `text`, `line`, `class`, `script`, `measured`), `rules`, `provenance`, `defects`
   (each: `id`, `section`, `finding`, `evidence`, and `exact_correction` {`find`, `replace`} or `judgement`
   {`options`}), `what_i_could_not_verify`, `e19_selfreport`, `tool_calls_used`, `limit`.

## Hard stops

A pinned digest that differs from the table: record both and stop. Never list, glob or search a directory; a shell
wildcard is a glob, even inside `OUT`. Never write outside `OUT`.
