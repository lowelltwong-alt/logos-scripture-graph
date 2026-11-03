# D4: THE BOOK-AGNOSTIC CLOSE TOOL, ITS BUILDERS AND ITS GATE TESTS (M8_fable, 1 Corinthians close kit, hard-book track)

You are lane D4 of the 1 Corinthians close. The work is candidate-only, NON-AUTHORIZING research. This brief is
binding. Attempt `cor_close_tool_d4_a1`, execution `cor_close_tool_d4_a1#e1`. You run on claude-opus-5-5 (OW-25).

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D4

Your OUT is the only place you write. After each unit of the work below, write what is finished and the cursor (the next
unit) to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D4\work\progress.json` (LF). If you are continued after an interruption, open that exact path and go on
from its cursor, and say so in your final message.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D4` already exists, and so does its `work\` subdirectory. Write
your deliverables directly into it at the names given below. **Never run any existence check, listing, glob or recursive
search against it or any other directory.** A shell wildcard is a glob, and so is a directory scan inside a script.

**EXACT-PATH LAW:** every path you may read is named in this brief, or in a pinned manifest this brief tells you to read
paths from. Open each by that exact path. State in your final message that you ran no listing and no glob. **Never open
any session or agent transcript, `.output` file or compaction summary path, including your own, even if your context
names one; if your context is compacted, rebuild from your OUT working files only.**

## GOVERNANCE

- SP is `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`. It is read-only for you. Write nothing under SP, not even a debug file.
- Never run git, never write a receipt, never touch any registry.
- **FORBIDDEN:** every path not named in this brief, including other models' directories, the Greek apparatus and Swete
  directories, and all final-message files. Nothing from another book passes as 1 Corinthians' evidence (E-65): where
  this brief pins another book's file, it is a template of FORM only.
- **Running Python:** set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`, and run `python -B`.
  Write scripts to files in OUT. Do not pass code through a shell here-document or `python -c`. Every file you write is
  UTF-8 with LF line endings (write bytes, or open with newline="\n").
- **Tiers (OW-18):** every claim names its true tier and never a stronger one: MEASURED if a script of yours produced it,
  EXTRACTED if you read it in a pinned file at a place you name, TRANSCRIBED if you copied it, REPORTED if a lane said it,
  otherwise INFERRED. No hand tallies. Every lane of this book ran on one model family, so agreement between lanes is one
  voice (OW-19).
- Record the sha256 of each pinned input as you read it. A mismatch is a hard stop: report it and stop.

## The work

You are a tool builder. You close nothing: you never run a close mode against the real tree, and the orchestrator
installs what you build. Daniel's close kit is hard-coded to Daniel; the owner's standing rule (TE-7) is that this port
is done ONCE, so 1 Corinthians and every later book run the same tools from a parameter file and port nothing.

**Units:** (1) read the templates; (2) the close tool; (3) the parameter maker and both parameter files; (4) the
builders and the packet generator; (5) the gate tests; (6) the regression and the dry run; (7) the result.

**1. `campaign/_close_book.py`, book-agnostic.** It takes `--book BOOK` and reads every constant now at lines 59-114 of
Daniel's tool from `<BOOK>/close/close_params.v1.json`. Keep the gates, the writes, the write order, the refusal rules,
the modes (`--dry-report DIR`, `--close`, `--acf`, `--next-book`, `--m8-root`, `--fixture-landed`, `@usage.json`) and
the OW-28 DEFERRED and OWED records exactly. **Add no shortcut. A gate that cannot be evaluated is UNMET, never
skipped. DEFERRED is never MET.** A gate family that does not apply to a book is switched off only by a named parameter
carrying its reason, and the switch prints as a gate line of its own with that reason: the language layer and the
numbering zone have no subject in 1 Corinthians. A book-specific library (Daniel's `dan_lib`) becomes a parameter
naming a module path, or a pure lookup in the parameters. The close-shape gate reads the carrier path and its generator
from the parameters: for 1 Corinthians `campaign/grader_models.v3.json` and `campaign/gen_grader_models_v3.py`, which the
orchestrator is building now and which do not exist yet, so that gate is UNMET in your dry run.

**The boss gate.** 1 Corinthians is on the hard track and a boss audit lane will run on the final rows after this lane.
Its record is `1Cor/review/1cor_boss_audit.v1.json`, in the same form as Daniel's, and its condition ids come from the
parameters. There may be one record or two, so `BOSS`, `BOSS_E2_SUPERSEDES` and the condition list are parameters and
"e2 answers exactly these" applies only when a second record is named. A NOT_TESTABLE or NOT_MET on any condition stays
UNMET, as it does in Daniel's tool. The lineage gate's `boss_audit_<tag>` names follow the parameter.

**2. `campaign/_make_close_params.py --book BOOK [--allow-pending]`.** Reads a short hand-written spec
`<BOOK>/close/close_spec.v1.json` (paths and facts) and writes `close_params.v1.json` with every pin MEASURED from disk at
the run. An absent input is refused, or with `--allow-pending` recorded as the literal `"PENDING"`, and the close tool
treats `"PENDING"` as UNMET. Write `close_spec.1Cor.v1.json` and `close_spec.Dan.v1.json`, and the parameter files
each produces when run with `--m8-root` pointing at the real tree and output into OUT.

1 Corinthians facts, each to be re-derived from the bytes and never taken from this brief: rows from
`1Cor/fixup/draft_rows_fixup4_applied.jsonl`; 16 chapters and 437 verses in WEB order (`1Cor/verse_inventory.json`); no
numbering zone; no language layer (the book is Greek); witnesses Byzantine RP primary and SBLGNT secondary (OW-31);
`decision_id` of the form `M8-1Cor-%03d`; books closed before and after 27 and 28; final corpus
`1Cor/rows_v1_final.jsonl`; the next book John, per OW-36. Close inputs at the same relative places as Daniel's:
`1Cor/scholar_record/`, `1Cor/deliverables/`, `1Cor/sidecar_src_1cor.jsonl`, `1Cor/merged_close/landing_manifest.v1.json`,
`1Cor/fable_end_review/`, `1Cor/cwo/`, `1Cor/1cor_retention_manifest.v1.jsonl`. The merged-verdict shape is granted by
OW-37 in place of OW-33; the close act is OW-37 point 3, not the owner's reservation.

**3. Builders, each book-agnostic, each with a `--check` that regenerates and compares bytes:**
- `campaign/_build_final_rows.py --book BOOK --from REL [--write]`: writes `<BOOK>/rows_v1_final.jsonl` and its manifest
  in the form of `Dan/rows_v1_final.manifest.json`, so that the lineage gates pass. No such tool exists: Daniel's were
  written by hand. Read `Dan/_close_book.py` lines 249-272 and the manifest. A value the tool cannot measure is a named
  argument, never a default.
- `campaign/_build_landed_manifest.py --book BOOK [--write]`: from the three receipt files named below, writes
  `<BOOK>/close/<book>_landed_outputs_manifest.v1.json` in the form of Daniel's v2, re-hashing each output and listing
  what does not match in `not_matching`.
- `campaign/_cwo_parity.py --book BOOK`: port of `Dan/_cwo_parity_dan.py`. The sweep tool's path is a parameter; for 1
  Corinthians it is `1Cor/review/cwo_sweep_1cor.py`.
- `campaign/gen_fable_end_packet.py --book BOOK [--check]`: port of Daniel's. It reads routed items, sidecars and the
  corpus from the parameters and records status DEFERRED (OW-28).

**4. `campaign/_test_close_book_gates.py --book BOOK`.** Port Daniel's: for each gate a private mirror with one planted
defect showing the gate refuses, and one clean mirror showing the intended inputs pass. Inputs that do not exist yet are
built in the mirror as fixtures of the right FORM, marked as fixtures. Add tests for what the port adds: a `"PENDING"`
pin refuses; a gate-family switch without a reason refuses; `--close` refuses on any unmet gate.

**5. Regression: the proof that nothing was weakened.** Run Daniel's installed tool `Dan/_close_book.py --dry-report` and
your tool `--book Dan --dry-report`, each into its own directory under OUT, and compare. Daniel is already closed, so
its target gates will not pass: that is expected and must be the same in both. Measure by script and record in
`regression`: every gate name in the old report and whether the new one has it, the verdict of each in both, and every
difference with its reason. Any gate lost, or any verdict that moved from UNMET to MET, is a defect to fix, not a note.

**6. One dry run for 1 Corinthians** with `--m8-root` the real tree and every output in OUT. Most gates are UNMET today
(no final rows, no merged lanes, no scholar record). List them in `gates_unmet_today`, each with what it waits on.

**Path rule.** The tools find the M8 tree from their own location and also accept `--m8-root`. No script scans a
directory: every input is a named path or a path read from a manifest or a parameter. No clock and no randomness in any
gate or preview; a second dry run must be byte-identical. `--close` writes whole files with LF bytes through a temporary
file and an atomic replace, under an exclusive lock, and rolls back on any failure.

**Deliverables, in OUT, at these names** (`campaign\` is a subdirectory of OUT that you create by writing into it):
`campaign\_close_book.py`, `campaign\_make_close_params.py`, `campaign\_build_final_rows.py`,
`campaign\_build_landed_manifest.py`, `campaign\_cwo_parity.py`, `campaign\gen_fable_end_packet.py`,
`campaign\_test_close_book_gates.py`, `close_spec.1Cor.v1.json`, `close_spec.Dan.v1.json`, `close_params.1Cor.v1.json`,
`close_params.Dan.v1.json`, `gate_test_result.json`, `regression\`, `dry_report\dry_report.json`, `build_notes.json`
(every gate ported, changed or switched, and every parameter with where it was measured), and the result JSON.

## PINNED INPUTS

| input | sha256 |
|---|---|
| `SP\Dan\_close_book.py` | `48f2337e25ae7155e362349933b812d29e5577402dbcb9ac2e230a5f95adb9e5` |
| `SP\Dan\_test_close_book_gates.py` | `9bd0c657e7a179fd277b5c5dab1f3261b6d4818abec9dac20674394597ec3344` |
| `SP\Dan\fable_end_review\gen_fable_end_packet.py` | `dd88e22315f169d8039f4078ab13cfa121827bc04e5171656ecf7485e87aa968` |
| `SP\Dan\_cwo_parity_dan.py` | `87e9e5679a77ac30bc4135f8e673fe16b6005b456cbbd347f7ab8587059b8f9f` |
| `SP\Dan\tools\dan_lib.py` | `1f397a7a08aba99cad67b0a59378eafa961130559bd8d07a7a9ed9d2f3043361` |
| `SP\Dan\rows_v1_final.manifest.json` | `21568cd63a0dc34f1ae9e18bc590907c723eac89565132dcb5354c10c4cb9bdb` |
| `SP\Dan\close\dan_landed_outputs_manifest.v2.json` | `5fadae2c09ab3bdc9a51184e40f72bc13a1b0e0182a39c070bebde99d9be9449` |
| `SP\Dan\merged_close\landing_manifest.v1.json` | `b24f6b5c7ebb2e56c67f3cac2c7edfe28c9264cd80f9bfdf66b534974b2b18f3` |
| `SP\..\receipts\Dan_completion.json` | `8151f9a9ec35c3fcd28274982f8ba6a117725f1d01f95fa693312b94c165565f` |
| `SP\..\book_chunks\Dan\chunks.jsonl` | `d3f4e39560fc8e210a67ad2c3dbe41d92b15fd52fe5a6a6713240163869964b8` |
| `SP\..\CAMPAIGN_CLOSE_GATE.v1.md` | `e67bac0408f4935bd5a2696f223b893623b6a85fdb703ea68d552eda2ce84d16` |
| `SP\campaign\grader_models.v2.json` | `efd78773fd122566ad923c6ae95a178385fff637344ed5272c7f79aa71214727` |
| `SP\..\marathon_progress.yaml` | `10c70cf5159249daa5863a8db49ef757c5172d2a7ccc19115ade89b73d7e9e67` |
| `SP\..\model_manifest.yaml` | `cf5364bb5664409fd4434c8611bcc4fa6c919f73fc862a5338d09cc5386e7579` |
| `SP\1Cor\fixup\draft_rows_fixup4_applied.jsonl` | `1aa03b08817c7b007796223b9a6921a81643db35ffa81e2f06e2c33821990562` |
| `SP\1Cor\verse_inventory.json` | `6d61f7911cdfca32c7da7b279964bd41dab283e32e760705af0f70210382f410` |
| `SP\1Cor\review\cwo_sweep_1cor.py` | `6f6578ea5958ee580493dbf56edec56bd0ee2cd6daf99c26fc9353cfba2ee92f` |
| `SP\1Cor\1cor_phase0_attempt_receipts.jsonl` | `2ef98c608a21f67dacca422d3f6f626c2c33c42cf15dc3496d0635700c83789d` |
| `SP\1Cor\1cor_writer_attempt_receipts.jsonl` | `ee4b521b993f19e4a636803fc07dd40412cfa34e476aa418cd53cdd137aa0c91` |

How you may use each input:

- `SP\Dan\_close_book.py`: READ in full; you may also RUN its --dry-report with every output in OUT, never --close. TEMPLATE: the close tool.
- `SP\Dan\_test_close_book_gates.py`: READ in full. TEMPLATE: the gate tests.
- `SP\Dan\fable_end_review\gen_fable_end_packet.py`: READ in full. TEMPLATE: the end-review packet generator.
- `SP\Dan\_cwo_parity_dan.py`: READ in full. TEMPLATE: the parity tool.
- `SP\Dan\tools\dan_lib.py`: READ lines 1-140. Daniel's book library, which the close tool imports.
- `SP\Dan\rows_v1_final.manifest.json`: READ. FORM of the final-rows manifest.
- `SP\Dan\close\dan_landed_outputs_manifest.v2.json`: READ by script. FORM of the landed-outputs manifest.
- `SP\Dan\merged_close\landing_manifest.v1.json`: READ. FORM of the merged-close manifest.
- `SP\..\receipts\Dan_completion.json`: READ. FORM of the completion receipt.
- `SP\..\book_chunks\Dan\chunks.jsonl`: READ the first 3 lines only. FORM of an assembled chunk row.
- `SP\..\CAMPAIGN_CLOSE_GATE.v1.md`: READ lines 237-272 and 608-628; other lines only where a gate of the tool cites them. The close gate.
- `SP\campaign\grader_models.v2.json`: READ. The grader carrier in force. Form of a close shape.
- `SP\..\marathon_progress.yaml`: READ. The progress carrier the close edits, anchored.
- `SP\..\model_manifest.yaml`: READ. The model manifest the close edits, anchored.
- `SP\1Cor\fixup\draft_rows_fixup4_applied.jsonl`: READ by script. The current rows, for the facts. Not yet final.
- `SP\1Cor\verse_inventory.json`: READ by script. The verse inventory.
- `SP\1Cor\review\cwo_sweep_1cor.py`: READ. The corpus-wide-order sweep tool the parity tool calls.
- `SP\1Cor\1cor_phase0_attempt_receipts.jsonl`: READ by script. Receipts, phase 0.
- `SP\1Cor\1cor_writer_attempt_receipts.jsonl`: READ by script. Receipts, writers.

The live receipt file `SP\1Cor\review\1cor_review_attempt_receipts.jsonl` grows while you run, so it is not pinned: read it by script, record the digest you read, and do not treat growth as a mismatch.

## Budget

About 90 tool calls; stop and report at 140. Keep printed output small: count and summarise, never print a file whole.

## YOUR FINAL MESSAGE

Write the result to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D4\D4_result.json`, then return the same JSON as your final message: one object with exactly
these keys: `attempt_id`, `execution_id`, `verdict`, `deliverables`, `verification`, `regression`, `gates_unmet_today`, `unresolved_uncertainty`. `deliverables` lists every file with name, sha256 and bytes. `verification` lists each claim with
how it was checked and the result. Add `e19_selfreport` as a note inside `verification`. This is an accountable work
summary, not chain of thought and not independent proof.
