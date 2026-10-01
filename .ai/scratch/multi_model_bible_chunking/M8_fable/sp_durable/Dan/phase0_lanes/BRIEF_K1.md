# DANIEL PHASE 0 - LANE K1: TOOLKIT REVIEW, BYTES (blind; claude-opus-5-5, OW-25)

Attempt `dan_toolkit_review_k1_a1`, execution `dan_toolkit_review_k1_a1#e1`. The orchestrator wrote Daniel's shared
verification toolkit, `TOOLKIT.md`, pinned below. Every later lane that annotates Daniel reads it and trusts its "Book
facts" as settled, so a wrong figure or rule in it reaches every one of them. OW-19 makes two blind review lanes the
floor. You are one of them. The other works by a different method; you will not see it, and it will not see you. Do not
try to find it. You AUDIT the toolkit; you do not rewrite it. Fable reviews every book at the campaign's end (OW-28);
your findings are an input to that, not a substitute for it.

`SP` below is `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`. Your output directory, `OUT`, is `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\dan_p0\lane_K1`.

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

| input | sha256 |
|---|---|
| `SP\Dan\tools\TOOLKIT.md` | `d9bc3a0a17fb8aacfbaf4b84303b15e01560eb57e10c76cacd90f9d497c8abd2` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\Dan_web.usfm` | `b5a967cabbfbec9b90763a5dd788956bccbe5293b313f9207158e9dda1ea94a9` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\dan_language_zones.json` | `903cf551acd9fc7a4e2a3721bb1431435eeb52141cb0429799f19ad566f70a6b` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\web_mt_offset_map.json` | `833d2ce37d015eccaaaac856d52c1931b9fd26bccb343064013fefc1da603da5` |
| `SP\Dan\web_mt_verse_check.json` | `eae814951c13e31815d78312bca0439067f871066fbbc3940df8bd0b4ff39a6d` |
| `SP\Dan\verse_inventory.json` | `de3dcac0f4649981a1c4c342add61c65fa7fb8b537261078695e30007924658b` |
| `SP\Dan\dan_stage_report.json` | `8e4b41373ad95a7088fcbd41509a82d9ec4c19e9da04768c0f2655cfcac3d00c` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\strategy_plan_Dan.json` | `a35acfb997ce8c659fc840ae638fc2cd88d7eb3eb13f0bbe481c7d588d418ef4` |
| `SP\Dan\tools\verse_map_web.json` | `ee286bc3ffe95f3547fc5d30d6b076e0bddafe4db7b11850519167f476658bb5` |
| `SP\Dan\tools\verse_map_oshb.json` | `10d0d143486bb332595a17e50ef0dff88af0db4a264a5fab2eebd7a7a244795e` |
| `SP\Dan\tools\dan_lib.py` | `1f397a7a08aba99cad67b0a59378eafa961130559bd8d07a7a9ed9d2f3043361` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `8a9b0b431b35c39fa022818a653f80a32fc6241ef636b4b11ec1682d80b7ee11` |

How you may use each input:

- `SP\Dan\tools\TOOLKIT.md`: READ whole. The toolkit under review.
- `SP\Dan\Dan_oshb.txt`: READ, through scripts of yours. The witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering.
- `SP\Dan\Dan_web_clean.txt`: READ, through scripts of yours. The WEB text, cleaned, one verse per line, WEB numbering.
- `SP\Dan\Dan_web.usfm`: READ, through scripts of yours. The WEB member, verbatim.
- `SP\Dan\pmarks_Dan.json`: READ, through scripts of yours. Daniel's paratextual marks and notes.
- `SP\Dan\dan_language_zones.json`: READ, through scripts of yours. Hebrew and Aramaic by verse and by word run; the mixed verse 2:4.
- `SP\Dan\dan_device_inventory.json`: READ, through scripts of yours. Daniel's device inventory, MT face.
- `SP\Dan\web_mt_offset_map.json`: READ. The WEB/MT crosswalk.
- `SP\Dan\web_mt_verse_check.json`: READ. The per-chapter verse counts on both faces.
- `SP\Dan\verse_inventory.json`: READ. The verse counts per chapter, declared on the WEB face.
- `SP\Dan\dan_stage_report.json`: READ. The staging report: sources, digests and counts.
- `SP\Dan\book_strategy_Dan.md`: READ, through scripts of yours. The reconciled book strategy.
- `SP\Dan\strategy_plan_Dan.json`: READ. The reconciled strategy plan.
- `SP\Dan\tools\verse_map_web.json`: READ, through scripts of yours. Verse map, WEB.
- `SP\Dan\tools\verse_map_oshb.json`: READ, through scripts of yours. Verse map, OSHB.
- `SP\Dan\tools\dan_lib.py`: READ; you may import it, running python -B. Daniel's library: zones, faces, verse order and the skeleton.
- `SP\campaign\grader_models.v1.json`: READ. The grader carrier: the OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only. The M8 ledger: OW-11, the owner's exception, and OW-11-h.

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
