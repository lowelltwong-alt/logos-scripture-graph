# DANIEL CLOSE BUILD D1: THE SCHOLAR-FACING RECORD (CLOSE-GATE ITEM 20), ITS GENERATOR AND ITS CHECKER

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for a study corpus. This lane builds a generated document for future scholars about where the book's unit boundaries were hard to set.

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
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_scholar_record_a1\out_e1
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.

Your units are: (1) read the templates and the item; (2) inventory Daniel's landed packets by script; (3) the generator; (4) the checker; (5) run both, fix until the checker passes, and write the check record. After each unit, and before you start the next, write what you have finished so far and the cursor (the next
unit) to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_scholar_record_a1\out_e1\work\progress.json` (LF). Write early and rewrite: completed work has been lost in this campaign
because it was written only at the end. If you are continued after an interruption, open that exact path and go on
from its cursor; say so in your final message.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_scholar_record_a1\out_e1` already exists, with its `work\` subdirectory. Write your
deliverables directly into it, at the names given below. **Never run any existence check, listing, glob or recursive
search**, on SP, on OUT or anywhere else; a shell wildcard is a glob, and so is a directory scan inside a script.
Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_scholar_record_a1\out_e1\work\`.

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

Attempt `dan_close_scholar_record_a1`, execution `dan_close_scholar_record_a1#e1`.

You are a builder, not a reviewer of the rows: you change no row and judge no boundary. Two blind lanes will later grade what you build against the primary sources, so state limits plainly; a record that hides a gap fails later.

## What to do

Build Daniel's scholar record as close-gate item 20 demands (read the item's own words in the gate file). Port Ezekiel's generator and checker to Daniel. The record speaks in scripture references and never in campaign vocabulary (row ids, lane names, rule codes, process nouns); the checker enforces a blocklist. Every factual sentence about the text is composed from a landed packet's fields, verbatim or by mechanical transformation, and every structural sentence comes from a listed template string. The checker must test: every landed review packet represented; every high-severity finding present; every cross-lane disagreement surfaced; nothing asserted that is not in a packet; the 46 open questions present as open; regeneration byte-identical. Include the witnesses' licence and attribution terms as the Ezekiel record states them for OSHB and WEB, checked against what Daniel's own files say.

**Path rule for every tool you write.** Each script takes `--dan-root` (where inputs are read; default: the parent of the script's own directory) and `--out-root` (where outputs are written; default: the same as `--dan-root`). In this run you call them with `--dan-root C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Dan --out-root C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_scholar_record_a1\out_e1`, so nothing is written under the worktree. After landing, the orchestrator installs your scripts at the same relative place under `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Dan` and re-runs each `--check` with the defaults; the bytes must come out identical, so use no clock, no randomness and sorted iteration, and hold every input digest as a constant the script verifies. No script scans a directory: every input is a named path or a path read from the manifest of landed outputs.

**The Ezekiel tools pinned below are templates for the form of the code and of the output only.** No Ezekiel finding, sentence, id, count or rating passes into Daniel's deliverable (E-65); Daniel differs (Aramaic chapters 2:4b to 7:28, a `language` field, no held row, its own ruling ids E1 to E12, row ids like W3-010), so port the logic and re-derive every constant from Daniel's bytes.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Dan\rows_v1_final.jsonl` | `783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09` |
| `SP\Dan\rows_v1_final.manifest.json` | `21568cd63a0dc34f1ae9e18bc590907c723eac89565132dcb5354c10c4cb9bdb` |
| `SP\Dan\close\dan_landed_outputs_manifest.v1.json` | `316676f61170822036032027b1a635ff7a7ee1ad229318b56a7d267b3a1fe378` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\fable_end_review\routed_items.v1.jsonl` | `42efe601b731e212ba60bc9b19fd9b3199d86e8d5a152bb7571f8e956376b0d6` |
| `SP\Dan\review\boss\dan_boss_audit.v1.json` | `ea70f94e48aed5d24f0adb604c3215a8f6e95ccf940b59da89147de3636a13c3` |
| `SP\..\CAMPAIGN_CLOSE_GATE.v1.md` | `e67bac0408f4935bd5a2696f223b893623b6a85fdb703ea68d552eda2ce84d16` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\review\dan_controlling_agent_rulings_E1.v1.json` | `541e3c1958d0bbf723d1537a0a00f62e16f207bf54d12ec11ae86f7d4bd9da30` |
| `SP\Dan\review\dan_controlling_agent_rulings_E2.v1.json` | `43ae72e748fe1e55be3103e826194672a3b317300ff413d690682697b121f940` |
| `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json` | `680b621d178e1f1c173204d504131c7c80f0de6a78bfe93dd52a10a060c318c0` |
| `SP\Dan\review\dan_controlling_agent_rulings_E4.v1.json` | `ff21977a7c635f5104c810053f773a5f7c74a03a548bdd39f16d1f04f7adc6e1` |
| `SP\Dan\review\dan_controlling_agent_rulings_E5.v1.json` | `a447f1412ca0e56d7ab55b31ed5c1edd3ce34898b4904a462d5b9b03e702f97d` |
| `SP\Dan\review\dan_controlling_agent_rulings_E6.v1.json` | `d1626dea516a88039fbc6124934994f973b99c7d1e615b4ce435e31feb646759` |
| `SP\Dan\review\dan_controlling_agent_rulings_E7.v1.json` | `0648ec2988fac5d25cb48026bf0ff4268674910c2c62dd684435b2bf8fbca9ef` |
| `SP\Dan\review\dan_controlling_agent_rulings_E8.v1.json` | `2e1877aa81f32b6e35d0154b5e196cc33393fe24c18a0c850cb38570b851f42c` |
| `SP\Dan\review\dan_controlling_agent_rulings_E9.v1.json` | `73a482ab17232319f3c4384cd57d56f5207423953538f1b56db12947605f7e13` |
| `SP\Dan\review\dan_controlling_agent_rulings_E10.v1.json` | `ef7a3e0028eca463fbe011e5c166b6ea38d825ded7abd12fc1a832413db9b85d` |
| `SP\Dan\review\dan_controlling_agent_rulings_E11.v1.json` | `54c547cdec3fe96e2a3ba000326c801e87dcd0c306bf21d3bd5cc6e141c71fc8` |
| `SP\Dan\review\dan_controlling_agent_rulings_E12.v1.json` | `8bc16d34306a990deeb39637e6314b5465da6865dbd647fb4b456a905a2285e1` |
| `SP\Ezek\scholar_record\gen_scholar_record.py` | `8a8d81b7225c413594c5eef04b4263432dff768385e6fc61b4e81257ab47872e` |
| `SP\Ezek\scholar_record\check_scholar_record.py` | `422b27b64a38b0443b80ea903bc3343246379bb56575b98cfeefbf68b767bb4a` |
| `SP\Ezek\scholar_record\EZEKIEL_SCHOLAR_RECORD.v2.md` | `4da575a6dec674108efca72e1927563d20b7f35bfb93737f15a4cff45db48aa9` |
| `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md` | `4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `a78e50d7b8b9aec94955eb74f401b41322790666ef497b5780b16d11e5142216` |

How you may use each input:

- `SP\Dan\rows_v1_final.jsonl`: READ in full by script. Daniel's 75 final rows (the corpus). Row id `writer_decision_id`.
- `SP\Dan\rows_v1_final.manifest.json`: READ. What the final file is built from and what changed.
- `SP\Dan\close\dan_landed_outputs_manifest.v1.json`: READ in full by script. THE MANIFEST OF LANDED OUTPUTS: every path in its `outputs` list is a landed Daniel artefact you may open by that exact path, after checking its sha256 against the manifest's, EXCEPT any path whose file name begins `final_message`. Paths are relative to SP's parent (they begin `sp_durable/`).
- `SP\Dan\book_strategy_Dan.md`: READ. The book's strategy (the standing rules the rows were written under).
- `SP\Dan\fable_end_review\routed_items.v1.jsonl`: READ in full. The 46 questions carried open to the end review.
- `SP\Dan\review\boss\dan_boss_audit.v1.json`: READ. The audit of the final rows (REPORTED).
- `SP\..\CAMPAIGN_CLOSE_GATE.v1.md`: READ lines 448-516 only (close-gate items 20 to 23, the demands your deliverable must meet).
- `SP\campaign\grader_models.v1.json`: READ. The grader carrier (OW-25).
- `SP\Dan\Dan_oshb.txt`: READ by script. The Hebrew and Aramaic witness (OSHB), the primary source.
- `SP\Dan\Dan_web_clean.txt`: READ by script. The WEB English witness.
- `SP\Dan\pmarks_Dan.json`: READ by script. The section-mark layer.
- `SP\Dan\dan_device_inventory.json`: READ by script. The device inventory.
- `SP\Dan\review\dan_controlling_agent_rulings_E1.v1.json`: READ. Controlling ruling E1 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E2.v1.json`: READ. Controlling ruling E2 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E3.v1.json`: READ. Controlling ruling E3 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E4.v1.json`: READ. Controlling ruling E4 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E5.v1.json`: READ. Controlling ruling E5 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E6.v1.json`: READ. Controlling ruling E6 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E7.v1.json`: READ. Controlling ruling E7 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E8.v1.json`: READ. Controlling ruling E8 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E9.v1.json`: READ. Controlling ruling E9 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E10.v1.json`: READ. Controlling ruling E10 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E11.v1.json`: READ. Controlling ruling E11 (the adjudicating record for the disputes it rules).
- `SP\Dan\review\dan_controlling_agent_rulings_E12.v1.json`: READ. Controlling ruling E12 (the adjudicating record for the disputes it rules).
- `SP\Ezek\scholar_record\gen_scholar_record.py`: READ. TEMPLATE for the form of the generator only (E-65).
- `SP\Ezek\scholar_record\check_scholar_record.py`: READ. TEMPLATE for the form of the checker only.
- `SP\Ezek\scholar_record\EZEKIEL_SCHOLAR_RECORD.v2.md`: READ the first 120 lines only: the form of the output and the licence wording.
- `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md`: READ. The neutral continuation contract named in the efficiency block.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only (OW-11, the owner's exception, OW-11-h).

## Deliverables (all in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_close\dan_close_scholar_record_a1\out_e1`)

- `scholar_record\gen_scholar_record.py`
- `scholar_record\check_scholar_record.py`
- `scholar_record\DANIEL_SCHOLAR_RECORD.v1.md` (written by the generator)
- `scholar_record\scholar_record_check.v1.json` (written by the checker; it must say PASS with every sub-check and its count, or you report honestly which sub-check fails and why)
- `build_notes.json`: what you ported, what you changed for Daniel and why, every packet class you found with its count, and every limit.

## Budget

About 60 tool calls; stop and report at 110. Keep printed output small: count and summarise, never print a packet whole.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"dan_close_scholar_record_a1","execution_id":"dan_close_scholar_record_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<each deliverable>","why":"..."}]},
 "deliverables":[{"name":"...","sha256":"<sha256 of its bytes>","bytes":0}],
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
