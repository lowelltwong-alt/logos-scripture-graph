# DANIEL CLOSE BUILD D4: THE CLOSE TOOL, ITS GATE TESTS AND THE END-REVIEW PACKET GENERATOR

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for a study corpus. This lane ports the book-close tool from Ezekiel to Daniel. The tool is run by the orchestrator, never by a lane.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for Ezekiel and Daniel. Verbatim answers: on authority,
"Yes: Ezekiel, then Daniel"; on recording, "M8 log only". authorization_ref
`lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 807-874
only. You run on claude-opus-5-5 (OW-25: every role runs on this model, a recorded grader_fallback where the role is a
grader's). You read files under the worktree and write only under your OUT directory; the orchestrator lands your
deliverables. You never run git, never write a receipt and never touch the registry.

## Continuation (binding)

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_tool_a1\out_e1
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.

Your units are: (1) read the templates and the gate; (2) the end-review packet generator and its --check; (3) the close tool; (4) the gate tests; (5) run the tests in private mirrors and one --dry-report into OUT, and write the notes. After each unit, and before you start the next, write what you have finished so far and the cursor (the next
unit) to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_tool_a1\out_e1\work\progress.json` (LF). Write early and rewrite: completed work has been lost in this campaign
because it was written only at the end. If you are continued after an interruption, open that exact path and go on
from its cursor; say so in your final message.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_tool_a1\out_e1` already exists, with its `work\` subdirectory. Write your
deliverables directly into it, at the names given below. **Never run any existence check, listing, glob or recursive
search**, on SP, on OUT or anywhere else; a shell wildcard is a glob, and so is a directory scan inside a script.
Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_tool_a1\out_e1\work\`.

**EXACT-PATH LAW:** every path you may read is named in this brief, or in a pinned manifest this brief tells you to
read paths from. Open each by that exact path. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every path that is not pinned below or named by a pinned manifest; every `final_message_*` file;
every `*_attempt_receipts.jsonl`; transcripts. Nothing from another book passes as Daniel's (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run
`python -B`. Write scripts to files in your OUT; do not pass code with escapes through a shell here-document or
`python -c`. Never edit any file under the worktree. Every file you write is UTF-8 with LF line endings (write bytes,
or open with newline="\n").

**Tiers (OW-18):** every claim names its true tier and never a stronger one: MEASURED if a script of yours produced
it, EXTRACTED if you read it in a pinned file at a place you name, TRANSCRIBED if you copied it, REPORTED if a lane
said it, otherwise INFERRED. No hand tallies: count by script or mark the figure REPORTED. Every lane of this book ran
on one model family, so agreement between lanes is one voice (OW-19).

## Your role and its limits

Attempt `dan_close_tool_a1`, execution `dan_close_tool_a1#e1`.

You are a tool builder. You close nothing: you never run the tool's close mode, and you write nothing outside OUT. The orchestrator installs your tools and the owner decides the close.

## What to do

Port Ezekiel's close tool to Daniel as `_close_book.py` (it will be installed at `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Dan\_close_book.py`). Keep every gate Ezekiel's tool has that applies to Daniel, each with its own named gate line and evidence; drop a gate only when its subject does not exist in Daniel (for example Ezekiel's held rows and its hold ruling: Daniel has no held row, and the tool must instead gate that no row carries a hold), and list every dropped or changed gate with the reason. Add no shortcut: a gate that cannot be evaluated is UNMET, never skipped. DEFERRED is never MET (OW-28): the campaign-end review is recorded as deferred with its packet digest, and the transcript audit is recorded as OWED, NOT MET, exactly as Ezekiel's tool records them.

Daniel's facts, to be re-derived from Daniel's bytes and held as verified constants: corpus `rows_v1_final.jsonl` and its sha256; 75 rows; 357 verses over 12 chapters in WEB order (tiling proven with `dan_lib`); numbering zone chapters 3 to 6; a `language` layer (Aramaic 2:4b to 7:28); parents PA..PJ contiguous; assembled `decision_id` of the form `M8-Dan-%03d`; review_status `candidate_review_complete`; hold fields null. Paths: suite report `Dan\rows_v1_final.jsonl.validator_report.json`; parity `Dan\cwo\cwo_parity.rows_v1_final.json`; sidecar source `Dan\sidecar_src_dan.jsonl` and `Dan\deliverables\gen_sidecars.py --check`; scholar record `Dan\scholar_record\` with its checker; merged-close landing manifest `Dan\merged_close\landing_manifest.v1.json` (lanes A and B, each with postcheck.json, final_check.json, items_20_23.json, named_questions.json, lane_meta.json, final_message.md; the final check's transcript_coverage must say reconcile_verdict NOT_RUN and bytes_audited_by_stage1 0); end-review packet `Dan\fable_end_review\Dan_fable_end_packet.v1.json` (your generator, `gen_fable_end_packet.py --check`); retention manifest `Dan\dan_retention_manifest.v1.jsonl`, written at close from the manifest of landed outputs plus the three attempt-receipt files it names, absent before close. Close writes, in Ezekiel's order and with Ezekiel's refusal rules: `book_chunks\Dan\chunks.jsonl`, the retention manifest, `receipts\Dan_completion.json`, the appends to low_confidence_register.jsonl, frontier_escalation_queue.jsonl, whole_bible_chunk_map.jsonl and atlas_candidate_feed.jsonl, and the anchored edits to marathon_progress.yaml (26 to 27) and model_manifest.yaml.

**Modes.** `--dry-report DIR` evaluates every gate and writes previews of every close write into DIR (which must lie outside the M8 tree), changing nothing. `--close` is the only mode that writes into the tree; it refuses unless every gate is met, takes an exclusive lock, writes each file whole with LF bytes through a temporary file and an atomic replace, and rolls back on any failure. You never run `--close`.

**Path rule.** The tool finds the M8 tree from its own location (as Ezekiel's does) and also accepts `--m8-root`, so the gate tests can point it at a private mirror. No script scans a directory: every input is a named path or a path read from a manifest. No clock, no randomness, sorted iteration; the dry report must be byte-identical on a second run.

**Gate tests.** Port `_test_close_book_gates.py`: for each gate, a private mirror in a temporary directory with one planted defect, showing the gate refuses, and one clean mirror showing the intended inputs pass. Several of Daniel's close inputs do not exist yet (the merged-close manifest, the carrier's Daniel shape, the installed D1 and D2 outputs, the end-review packet). Build them in the mirror as fixtures of the right FORM, marked as fixtures; in the real tree your one dry run will show those gates UNMET, and that is the expected and honest result. List them.

**End-review packet generator.** Port Ezekiel's to Daniel: it packs the 46 routed items with their source digests and the corpus digest, records status DEFERRED (OW-28), and has a `--check` that regenerates and compares bytes. It takes `--dan-root` and `--out-root` like the other Daniel tools (defaults: the parent of its own directory).

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Ezek\_close_book.py` | `b569755697c98e54a2965c85015de5da27abd5f587e6a0341ba51bfca357831c` |
| `SP\Ezek\_test_close_book_gates.py` | `d22f7052cae0b504c450c3dccb03f0365bf1fdb7ba3a2d510d50c5955a7f18f6` |
| `SP\Ezek\fable_end_review\gen_fable_end_packet.py` | `ab44ad47fb1738f8ba5e9df81af9b02305985b1e97f806f99927c093cd07178c` |
| `SP\Ezek\repair2\close_check_mirror.py` | `c92e5119d95ca1b53520d78df8c522983a89ea1e56089cfd2e8ce45a081861f4` |
| `SP\Ezek\merged_close\landing_manifest.v1.json` | `642e804db18c4492cae926dda14a5928af6c862af2aad9d492070ffdcd7c46d8` |
| `SP\Dan\rows_v1_final.jsonl` | `783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09` |
| `SP\Dan\rows_v1_final.manifest.json` | `21568cd63a0dc34f1ae9e18bc590907c723eac89565132dcb5354c10c4cb9bdb` |
| `SP\Dan\rows_v1_final.jsonl.validator_report.json` | `dc9e5d1b6f05cd9069d83f580e519eeb501329ae2490e7ff9bb58a31e4f4c811` |
| `SP\Dan\cwo\cwo_parity.rows_v1_final.json` | `9a626802359a9096e507cb1dfcc910e1ac9ed7f9526a6765483a19d3ef1e4250` |
| `SP\Dan\_cwo_parity_dan.py` | `87e9e5679a77ac30bc4135f8e673fe16b6005b456cbbd347f7ab8587059b8f9f` |
| `SP\Dan\tools\dan_lib.py` | `1f397a7a08aba99cad67b0a59378eafa961130559bd8d07a7a9ed9d2f3043361` |
| `SP\Dan\fable_end_review\routed_items.v1.jsonl` | `42efe601b731e212ba60bc9b19fd9b3199d86e8d5a152bb7571f8e956376b0d6` |
| `SP\Dan\close\dan_landed_outputs_manifest.v2.json` | `5fadae2c09ab3bdc9a51184e40f72bc13a1b0e0182a39c070bebde99d9be9449` |
| `SP\Dan\review\boss\dan_boss_audit.v1.json` | `ea70f94e48aed5d24f0adb604c3215a8f6e95ccf940b59da89147de3636a13c3` |
| `SP\Dan\review\boss\supp_e2\dan_boss_audit_b8_b14.json` | `d186bac7af0e1f8763ee307c54955575cdde96625698f182290c30545472672c` |
| `SP\Dan\close\BRIEF_D1.md` | `dbc79e1ca711991285ac2eced4a5d5a28913acf4bfada7daad4828222d9d78f8` |
| `SP\Dan\close\BRIEF_D2.md` | `fa8307dec0adbe6dd0e32dafba84a951418832e5091cd26fa7ca0b4ccce27627` |
| `SP\..\CAMPAIGN_CLOSE_GATE.v1.md` | `e67bac0408f4935bd5a2696f223b893623b6a85fdb703ea68d552eda2ce84d16` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\marathon_progress.yaml` | `58a8dd3bd8d1640b6e6a827a3315a2a3028e2f84172ff212a5961efed2710af5` |
| `SP\..\model_manifest.yaml` | `d4bf9ad52af5b350484af95a5ade4c85bd8d169c0ab1d565c74a9f57d7a7425c` |
| `SP\..\book_chunks\Ezek\chunks.jsonl` | `249036b01ca8bffce76f64c59038f15b6a7af9fc4ee690a2909cc0ef04accc8b` |
| `SP\..\receipts\Ezek_completion.json` | `8110b4ff993940d5d3b3b0ec4ab14b46335f3749fbd8a203cb80479b92c324b6` |
| `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md` | `4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `a78e50d7b8b9aec94955eb74f401b41322790666ef497b5780b16d11e5142216` |

How you may use each input:

- `SP\Ezek\_close_book.py`: READ in full. TEMPLATE: Ezekiel's close tool. Port its gates, its writes and its dry-report mode.
- `SP\Ezek\_test_close_book_gates.py`: READ in full. TEMPLATE: the gate tests (each gate shown to refuse on a planted defect).
- `SP\Ezek\fable_end_review\gen_fable_end_packet.py`: READ in full. TEMPLATE: the end-review packet generator and its --check.
- `SP\Ezek\repair2\close_check_mirror.py`: READ. TEMPLATE: how a private mirror is built for a gate test.
- `SP\Ezek\merged_close\landing_manifest.v1.json`: READ. The FORM of the merged-close landing manifest the close tool gates on (lanes A and B; six files each). Form only: no Ezekiel verdict passes into Daniel (E-65).
- `SP\Dan\rows_v1_final.jsonl`: READ by script. Daniel's 75 final rows (the corpus). Row id `writer_decision_id`; parents PA..PJ in `parent_collection`.
- `SP\Dan\rows_v1_final.manifest.json`: READ. The lineage record of the final file (what it was built from).
- `SP\Dan\rows_v1_final.jsonl.validator_report.json`: READ. The Tier-0 suite report on the corpus (hard_status GREEN).
- `SP\Dan\cwo\cwo_parity.rows_v1_final.json`: READ. The corpus-wide-order parity record (status GREEN, bound to the corpus digest).
- `SP\Dan\_cwo_parity_dan.py`: READ. The parity tool; the close tool may call its --check.
- `SP\Dan\tools\dan_lib.py`: READ lines 1-140. LAST_VERSE, TOTAL_VERSES (357), ZONE_CHAPTERS, web_to_mt, language_of. Import it by adding Dan\tools to sys.path, as the suite tools do.
- `SP\Dan\fable_end_review\routed_items.v1.jsonl`: READ in full. The 46 questions carried to the campaign-end review.
- `SP\Dan\close\dan_landed_outputs_manifest.v2.json`: READ by script. Every landed Daniel output with its digest (the source of the retention manifest: path, bytes, sha256).
- `SP\Dan\review\boss\dan_boss_audit.v1.json`: READ by script. The audit record (REPORTED); the completion receipt cites its digest.
- `SP\Dan\review\boss\supp_e2\dan_boss_audit_b8_b14.json`: READ by script. The audit's second execution (conditions B8 and B14).
- `SP\Dan\close\BRIEF_D1.md`: READ the Deliverables section only: where the scholar record, its generator and checker will stand after install (Dan\scholar_record\...).
- `SP\Dan\close\BRIEF_D2.md`: READ the Deliverables section only: where the atlas rows, sidecar source and their tools will stand after install (Dan\deliverables\..., Dan\sidecar_src_dan.jsonl).
- `SP\..\CAMPAIGN_CLOSE_GATE.v1.md`: READ in full. The close gate: every numbered item the close tool must enforce or record.
- `SP\campaign\grader_models.v1.json`: READ. The grader carrier. `book_close_shapes` lists Ezek only today; the owner has approved the merged-verdict shape for Daniel and the orchestrator will add `book_close_shapes.Dan` through the carrier's generator. Your tool gates on that key being present with shape, directive, transcript_audit and weakness_statement, exactly as Ezekiel's does.
- `SP\..\marathon_progress.yaml`: READ. The progress carrier the close edits (26 books closed today; Daniel makes 27). Find the exact anchors by reading; anchor every edit on a unique expected-before string and refuse on a miss.
- `SP\..\model_manifest.yaml`: READ. The model manifest the close edits; same anchoring rule.
- `SP\..\book_chunks\Ezek\chunks.jsonl`: READ the first 3 lines only: the FORM of an assembled chunk row.
- `SP\..\receipts\Ezek_completion.json`: READ: the FORM of a completion receipt. Form only (E-65).
- `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md`: READ. The neutral continuation contract named in the efficiency block.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only (OW-11, the owner's exception, OW-11-h).

## Deliverables (all in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_tool_a1\out_e1`)

- `_close_book.py`
- `_test_close_book_gates.py`
- `fable_end_review\gen_fable_end_packet.py`
- `fable_end_review\Dan_fable_end_packet.v1.json` (written by the generator with `--out-root C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_tool_a1\out_e1`)
- `gate_test_result.json`: every test by name with pass or fail, and the command that produced it
- `dry_report\dry_report.json`: the one dry run against the real tree, every gate with MET or UNMET and its evidence
- `build_notes.json`: every gate ported, changed, dropped or added with the reason; every constant and where it was measured; the gates UNMET today and what each waits on; every limit.

## Budget

About 80 tool calls; stop and report at 140. Keep printed output small: count and summarise, never print a file whole.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"dan_close_tool_a1","execution_id":"dan_close_tool_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<each deliverable>","why":"..."}]},
 "deliverables":[{"name":"...","sha256":"<sha256 of its bytes>","bytes":0}],
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
