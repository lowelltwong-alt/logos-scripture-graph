# 1 CORINTHIANS - CYCLE STATE (immutable, append-only)

The live book's log. Daniel closed at 27/66 on 2026-10-14; its own log carries that close and points here.
This file is append-only: entries are added, never edited, and a correction is itself an appended entry.

1 Corinthians is first in the owner's hardest-first order (1 Corinthians, John, Romans, Revelation, Hebrews, Matthew;
OW-34, continuing OW-32's queue). It is the campaign's first New Testament book and depends on the Greek substrate
(OW-31: Byzantine RP primary, SBLGNT secondary). OW-25's model rule, OW-28's tracked-not-enforced ceilings and OW-30's
no-Fable-call rule stand. OW-33's merged-verdict close shape was Daniel's only.

## 2026-10-14 - log opened at Daniel's close

Daniel's close is evidenced: receipts/Dan_completion.json sha256 8151f9a9ec35c3fcd28274982f8ba6a117725f1d01f95fa693312b94c165565f, 75 chunks, --acf item22 after a dry run of the same arguments showed 101 gates and 0 unmet. marathon_progress.yaml reads books_completed: 27, current_book: 1Cor. Opening this log records what has already happened; it advances nothing and invents no state. Phase 0 has not started.
- First job (OW-34): resolve the Greek source's licensing and provenance for M8_fable/greek_substrate/ (each source's licence terms, origin and the staged files' digests). Nothing there is committed or published until that is resolved; every download needs a per-file owner yes.
- Then 1 Corinthians Phase 0 under the playbook. Launch messages cite OW-34 as the owner's order for this book (OW-11's verbatim scope named Ezekiel and Daniel).

## 2026-10-14 - durability checkpoint at Daniel's close

- Daniel closed (27/66), OW-34 recorded, Daniel's proposals in the shared log, carriers re-bound by this checkpoint. Next: Resolve the Greek source's licensing and provenance for greek_substrate/ (OW-31 sources; record licence terms, origin and staged-file digests; nothing committed until resolved; per-file yes for any download), then open 1 Corinthians Phase 0 under the playbook (OW-34).
- CURSOR: phase = DAN_CLOSED_1COR_GREEK_LICENSING_NEXT.

## 2026-10-14 - Greek licensing and provenance resolved (OW-34 first job)

- Record: sp_durable/campaign/greek_substrate_licensing_provenance.v1.json sha256 555634cef2bda4ac33c0684dd69413fe884b6e9753d9a31e41c7483be1f1e467, drafted from a fresh read of STAGING_RECEIPT.v1.json (a086b7c30ffd...), the three licence files and the tracked SBLGNT source_manifest.yaml.
- Re-verified 2026-10-14 (MEASURED): stray_sweep GREEN, greek_lib selftest GREEN, _stage_and_verify GREEN (A 32, B 29, B2 27 files blob-matched at the pins).
- Licences (EXTRACTED): A Byzantine RP = Unlicense/public domain; B and B2 SBLGNT = CC BY 4.0 with attribution; C Swete = CC BY-SA 4.0, reference-only under the owner's 2026-09-29 terms and not needed for 1 Corinthians.
- Publication of greek_substrate/ is NOT decided; nothing there is committed. One owner question asked.
- CURSOR: phase = 1COR_GREEK_LICENSING_RECORDED_OWNER_PUBLICATION_QUESTION.

## 2026-10-14 - OW-35: Greek publication scope decided

- The owner chose "Commit A+B+tools (Recommended)". Commit A, B (with LICENSE and attribution), tools/, derived/, fixture/, the README, the receipt and the staging scripts. Keep B2 and C local. Ledger OW-35.
- Disclosure (near-miss): a scratch edit of the record generator was first attempted through a heredoc carrying backslash escapes, against the standing rule. Its exact-match assert refused, and nothing was written. It was redone with the Edit tool. This is the same class as E-71; it is a candidate for the next E entry.
- CURSOR: phase = 1COR_GREEK_PUBLICATION_DECIDED_OW35.

## 2026-10-14 - OW-35 scope staged for commit; EOL conversion; two gaps found

- Before git add (E-73), the CRLF files in OW-35's committable greek_substrate scope were converted to LF. The change was proven EOL-only, and each original was kept byte-exact (E-44). No campaign record cited a CRLF digest of these files (searched outside transcripts). Conversions:
  - STAGING_RECEIPT.v1.json: CRLF 8d1cbcdc229c... -> LF a086b7c30ffd...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/STAGING_RECEIPT.v1.json.pre_8d1cbcdc229c
  - _build_receipt.py: CRLF feffb56e5f83... -> LF 8b939f10ecb9...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/_build_receipt.py.pre_feffb56e5f83
  - derived/crosswalk.v1.json: CRLF c0825466057e... -> LF 511f9a990108...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/derived/crosswalk.v1.json.pre_c0825466057e
  - fixture/rows.bad.jsonl: CRLF b0801d7c7793... -> LF ca65cd952ea4...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/fixture/rows.bad.jsonl.pre_b0801d7c7793
  - fixture/rows.bad.jsonl.validator_report.json: CRLF a0a58fbfacad... -> LF 2212848065a7...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/fixture/rows.bad.jsonl.validator_report.json.pre_a0a58fbfacad
  - fixture/rows.good.jsonl: CRLF 8999f6665f61... -> LF 80b4c1e5025f...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/fixture/rows.good.jsonl.pre_8999f6665f61
  - fixture/rows.good.jsonl.validator_report.json: CRLF e612821db19d... -> LF 2ecc9c6f79ac...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/fixture/rows.good.jsonl.validator_report.json.pre_e612821db19d
  - fixture/rows.bad.jsonl.validator_report.json: CRLF a0a58fbfacad... -> LF 2212848065a7...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/fixture/rows.bad.jsonl.validator_report.json.pre_a0a58fbfacad
  - fixture/rows.good.jsonl.validator_report.json: CRLF e612821db19d... -> LF 2ecc9c6f79ac...; original kept at sp_durable/orchestrator_scratch/greek_eol_pre/fixture/rows.good.jsonl.validator_report.json.pre_e612821db19d
- After conversion: stray_sweep GREEN; run_suite selftest GREEN; the good fixture GREEN and the bad fixture RED (expected); _stage_and_verify GREEN (A 32, B 29, B2 27 blob-matched); workspace validator pass with blocking_failures []; _eol_digest_audit --tree LF_CLEAN.
- Gap 1 (E-75 candidate): run_suite.py writes its fixture validator_report files in Windows text mode, so every run turns them back into CRLF. The two reports were converted a second time after the re-run. The tool is not edited here.
- Gap 2 (E-75 candidate): _eol_digest_audit --tree does not scope greek_substrate/, so it reported LF_CLEAN while the two reports held CRLF. A staged-file CR count (0 across all 79 greek files) caught it.
- Staged by explicit path only. A mechanical check of the staged list found 0 paths under sblgnt_apparatus, swete, __pycache__, transcripts, shell_outputs or orchestrator_scratch.
- CURSOR: phase = 1COR_GREEK_OW35_COMMITTED_PHASE0_NEXT.
