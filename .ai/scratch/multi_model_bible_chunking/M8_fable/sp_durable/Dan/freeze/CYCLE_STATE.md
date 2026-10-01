# DANIEL — CYCLE STATE (immutable, append-only)

The live book's log. Ezekiel closed at 26/66 on 2026-09-23; its own log carries that close and points here.
This file is append-only: entries are added, never edited, and a correction is itself an appended entry.

Daniel is owner-named HARD. Every role runs on claude-opus-5-5 (OW-25); a Fable role is recorded as grader_fallback.
No Fable call is made without a new owner authorization (OW-30), and the atlas-hold precedent P1-P3 from Ezekiel's
ruling applies. Daniel's ceiling is 25,000,000 in the notification unit, counted from Daniel's first launch, tracked
and not enforced (OW-28). The Opus orchestration authority exception covers Daniel and expires at Daniel's close.

## 2026-09-23 - log opened at Ezekiel's close

Ezekiel's close is evidenced: receipts/Ezek_completion.json sha256 8110b4ff993940d5d3b3b0ec4ab14b46335f3749fbd8a203cb80479b92c324b6, 138 chunks, --acf item22 after a dry run of the same arguments showed 122 gates and 0 unmet (OW-29). marathon_progress.yaml reads books_completed: 26, current_book: Dan. The durability checkpoint appended its entry and cursor to sp_durable/Ezek/freeze/CYCLE_STATE.md, but this book had no log, so the checker's cursor resolver fell back to the CLOSED Jeremiah log and refused the prompt re-bind. This is the same fault recorded at Ezekiel's own log opening on 2026-09-08. Opening this log records what has already happened; it advances nothing on its own and invents no state.

- Cure: `sp_durable/Ezek/repair2/checkpoint_carriers.py` is amended (`.pre_1cdd981d57b3` kept) to resolve the live book's log from marathon_progress.yaml current_book, as the checker does, and to refuse rather than fall back when that log is missing.
- Phase 0 has not started. The next job is Daniel's Phase 0 per sp_durable/campaign/daniel_start_readiness.v2.json (phase0_must_produce: Dan_oshb.txt, Dan_web_clean.txt, verse_inventory.json, pmarks_Dan.json, book_strategy_Dan.md, web_mt_offset_map.json, tools/check_language_zones.py). The Aramaic section is located from the OSHB morph codes at Phase 0, never from memory. Readiness v2 step 2 (the OW-9 stop) is superseded by OW-29, and RESUME_PROMPT_CURRENT.md says to open Daniel's Phase 0 without stopping.
- CURSOR: phase = EZEK_CLOSED_DAN_PHASE0_NEXT.

## 2026-09-23 - Ezekiel receipt identity amended; receipt readers owed before Daniel's first runs

- The 7 Ezekiel launch rows that recorded the lane's runtime id in `parent_agent_id` are amended, and no line was edited: +2 rows in `Ezek/ezek_merged_close_attempt_receipts.jsonl`, +5 rows in `Ezek/ezek_close_audit_attempt_receipts.jsonl`, and +7 keys in `Ezek/_transcript_map.ezek.json`. The receipt is `Ezek/repair2/amend_identity_E55s1.receipt.json`. The first apply collided on a shared attempt id and was rolled back to the exact preimages (ledger E-60).
- `campaign/_guarded_json_patch.py` now refuses a plan that addresses one key twice, and rolls back its own RED write (`.pre_254a43bd2199` kept). `campaign/test_guarded_json_patch.py` passes 4/4 on the fix and fails 4/4 on the preimage.
- `campaign/_orchestration_metrics.py` now folds amending rows into the execution they name (`.pre_0a6a9e325815` kept). `orchestration_metrics.v1.json` was regenerated (sha256 prefix 44b4c5c35d50): 514 rows, 467 executions, and all 47 amending rows applied to a unique target. Notification-unit tokens total 117,835,959. The 1,431,971 spend-unit tokens (the two OW-26 merged-close amendments) are reported apart and no longer mixed in. Previous file kept as `orchestration_metrics.v1.json.pre_1337016a4b5d`.
- OWED, each triggered before Daniel's first run of that tool. Status: MEASURED by grep, where 0 means `amends_execution_id` never occurs in the file.
  - `campaign/_capture_index.py`: 0, and it copies `parent_agent_id` from the row at lines 191-192.
  - `campaign/_census_tf6_candidate.py`: 0.
  - `campaign/_transcript_coverage_census.py`: 0.
  - `campaign/_book_close_status_ow12.py`: partly aware. It buckets amending rows by book at line 73, but it sums every row's tokens, so it counts amending rows as executions and adds spend-unit amendments to notification-unit figures.
  - Census v4's map join also does not read `previous_executions[].agent_id`, which affects 11 Ezekiel attempts.
  - The rule for each tool, with `_orchestration_metrics.py` `fold()` as the precedent: an amending row is never an execution; it applies to the one execution it names; the notification unit and the spend unit are kept apart.
- FINDING for the owner's Ezekiel figures (INFERRED, not recomputed). Census v4 records the two merged-close lanes at their spend-unit amendments (576,419 and 855,552; the code's SELFTEST pins them), where the notification figures are 101,506 and 148,182, and 148,182 covers one segment only. If census v4's recorded total is the 70.94M notification-unit figure, that total carries about 1,182,283 spend-unit tokens. This changes no gate: ceilings are tracked, not enforced (OW-28).
- Forward rule for Daniel: a launch row puts the runtime id in `agent_id` and `"orchestrator"` in `parent_agent_id`.
- CURSOR: phase = EZEK_CLOSED_DAN_PHASE0_NEXT (unchanged).

## 2026-09-23 - provenance of the entry above (E-59 recurrence, caught)

- The entry above was written right after a compaction, and three of its claims came from recall before any source was read. They were then checked against a fresh read, and each holds:
  - `Ezek/ezek_merged_close_attempt_receipts.jsonl` gives lane_b 101,506 (completion) against 576,419 (spend-unit amendment), and lane_a 148,182 (completion, token_note "SEGMENT ONLY") against 855,552 (spend-unit amendment).
  - `Ezek/repair2/census_ow15_v4.py:38` SELFTEST pins 576419 and 855552.
  - `campaign/_book_close_status_ow12.py:80-84` counts every row as an execution and adds every row's integer tokens.
  - These are now EXTRACTED; the 70.94M conditional stays INFERRED.
- Observed impact: nil. It was caught before any reuse, and the recalled values happened to be right. Counterfactual: a wrong figure in this log would feed the owner's OW-12 status. This recurs E-59's pattern: order is read, then write. It is routed with E-59 at the next DAD ingest.
- CURSOR: phase = EZEK_CLOSED_DAN_PHASE0_NEXT (unchanged).

## 2026-09-23 - owed pre-Daniel records landed; Phase 0 next

- Done:
  - DAD delta E-52..E-58 + OW-25..OW-30 was ingested earlier on 2026-09-23.
  - The 7 identity amendments and 7 map keys, including the two OW-26 merged-close lanes a2040ee3f85015b45 and a75da61617c35aca9.
  - The guarded-tool hardening and its test.
  - The metrics fold, with the metrics regenerated.
  - E-60 ledgered.
  - See the two entries above.
- OWED, not done, each with its own before-first-run trigger in the entry above:
  - teach the capture index, the tf6 candidate census, the transcript coverage census and the OW-12 status tool the amend fold;
  - teach census v4's map join to read `previous_executions`.
- DAD pending: E-59, E-60 and the E-59 recurrence note. The cursor is still after E-58.
- CURSOR: phase = DAN_PHASE0_NEXT.

## 2026-09-23 - Daniel Phase 0 under way: staging done, small tools ported, toolkit port next

- Disclosed: Phase 0 began without a CURSOR line; this section is the first one since `DAN_PHASE0_NEXT`.
- Done (MEASURED):
  - staging: `dan_lib.py` selftest 48/48, language-zones fixture 27/27;
  - 12 smaller Ezekiel tools adapted by `Dan/tools/_adapt_tools_dan.py` with the `_adapt_tools_dan_spec.py` spec and installed, 0 residuals;
  - selftests: check_role_tokens 14/14 (6 planted defects flagged), check_register 53 vectors GREEN, check_universals 2/2;
  - inventory face declared by `Dan/_declare_inventory_face_dan.py`: 356f4427f7d4 -> de3dcac0f464, pre-image kept;
  - E-61 ledgered, with a same-day correction note.
- OWED, in order:
  - port citation_sweep, check_web_quotes, check_refs_mirror, check_marks and build_verse_maps, and port `_test_zone_tools_ezek.py` to `_test_zone_tools_dan.py` (the normalize docstring already claims it);
  - build the verse maps, then smoke-run the suite and check_brief_vs_suite;
  - write TOOLKIT.md and `_toolkit_selfcheck.py`, including the E-61 parity audit and face assertion;
  - write the Phase 0 receipts;
  - the strategy lane, then the two blind toolkit review lanes;
  - the amend fold for the receipt readers (still owed from the entry above).
- DAD pending: E-59, E-60, E-61 and the E-59 recurrence note. The cursor is still after E-58.
- CURSOR: phase = DAN_PHASE0_TOOLKIT_PORT.

## 2026-09-23 - toolkit port split into lanes; E-62 and its launch gate

- DONE this segment:
  - `Dan/tools/_adapt_tools_dan.py` gained `--extra-spec PATH`, with RENAME and a clash refusal (pre-copy `.pre_8acea10b313e`, now 37580b05cbbb). The base stage is unchanged: 12 tools, 0 residuals.
  - E-62 ledgered: 42 of 207 launches carried none of the required launch-message strings. The cure is the new `campaign/_launch_message_check.py`. Amendment 1 made that checker also require `_brief_pin_check.py` MATCH on the named brief, because the v10 lanes launched on NO_TABLE. The checker is now 7bdd3cb3e52b (pre `.pre_2a04d014f107`), and its selftest passes 15/15. Ledger ad6783316d04, 2620 lines.
  - The sibling audit found that `_inflight_pin_guard.py` reads any line carrying a path and a digest, so it never failed open on a 4-column table. Its documented limit still stands: absolute-path pins are invisible to it.
  - Decided: Daniel needs its own language-aware device inventory. Ezekiel's calendar-arm constants came from Ezekiel's ruling G12(d). Daniel has no such ruling, so its CAL_NO_ONSET is empty, with that reason stated.
  - Lane tooling, in `Dan/phase0_lanes/`:
    - `build_launch.py` builds each brief from its template, with the pin rows measured, plus the launch-message file, and runs both checkers;
    - `append_launch_row.py` writes the launch rows into `Dan/dan_phase0_attempt_receipts.jsonl`, carrying `launch_message_sha256`.
- IN FLIGHT (launched 2026-09-23T21:51-21:52Z; both briefs and both messages returned MATCH, and the workspace validator passed):
  - lane D `dan_p0_device_inventory_a1#e1`: `BRIEF_D.md` a760ce12e1d7;
  - lane T2 `dan_p0_toolport_t2_a1#e1`: `BRIEF_T2.md` a778400debf3.
  - While they run, the M8 ledger, `dan_lib.py` and the other pinned inputs are PINNED. Write none of them until both land.
- NEXT, at landing:
  - review each OUT;
  - install T2 through `--install ... --extra-spec` and run the Daniel `_audit_book_token_transform`;
  - install D's builder and inventory at `Dan/`;
  - then brief lane T1 (citation_sweep and `_test_zone_tools_dan.py`, bound to D's constants), through `build_launch.py` after adding a T1 entry.
- The owed list above stands otherwise. Carrier item: the next checkpoint names `_launch_message_check.py` in the work-state bullet (E-62 cure 4).
- CURSOR: phase = DAN_PHASE0_TOOLKIT_PORT_LANES_D_T2_IN_FLIGHT.

## 2026-09-24 - lane D #e1 stalled; relaunched as #e2

- Lane D `dan_p0_device_inventory_a1#e1` (agent a1586d02295dfea45) was stopped by the runtime watchdog: "Agent stalled: no progress for 600s (stream watchdog did not recover)". It landed no deliverable. Its notification carried no usage block, so its model and tokens are UNAVAILABLE.
- Its 7 partial scratch files (input mirror copies, inputs_verified.json, an inspection script) were moved unchanged to `scratch\dan_p0\lane_D_e1_residue\`, with digests in its landing row. They are not reviewed, not installed and not given to #e2.
- Receipts (`Dan/dan_phase0_attempt_receipts.jsonl`):
  - the #e1 landing row (record_kind completion, outcome FAILED_BY_RUNTIME_WATCHDOG) was written by the new `Dan/phase0_lanes/append_landing_row.py`;
  - the #e2 launch row (agent a5670ae5a0b0c1f12, previous_execution_id and retry_of `#e1`) followed. Receipts now 0b54699ce4ff.
- Tooling amended so that a relaunch cannot carry the earlier execution's id or shadow an unlanded one:
  - `build_launch.py --execution N` writes `BRIEF_<L>_e<N>.md` and `launch_message_<L>_e<N>.txt`, naming `#e<N>` (pre `.pre_7727531f741c`);
  - `append_launch_row.py --execution N --retry-reason` refuses unless `#e<N-1>` has both a launch row and a landing row (pre `.pre_2b6ed4fbd25d`).
- `BRIEF_D_e2.md` is 62954b39020b and its message is e874f1e89b28. It is identical to `BRIEF_D.md` except line 3, the execution id plus the relaunch note. Pin check MATCH, launch-message check MATCH, workspace validator pass.
- IN FLIGHT: D #e2 and T2 #e1. The ledger, `dan_lib.py` and the other pinned inputs stay PINNED until both land.
- Landing rows for T2 and D #e2 go through `append_landing_row.py` (both token units, model_actual from the usage block).
- CURSOR: phase = DAN_PHASE0_TOOLKIT_PORT_LANES_D_E2_T2_IN_FLIGHT.

## 2026-09-24 - the amend fold reaches every receipt reader; the capture index is rebuilt

Every figure in this entry was re-read from its source after the last compaction (E-59).

- **The shared fold.** `campaign/_receipt_fold.py` (NEW) is the one amend fold. `--selftest` PASSES 17 checks. Its parity check against `_orchestration_metrics.fold()` covers all 470 executions. The only differences are the 5 executions whose landing rows carry `tokens_notification_unit` / `tokens_spend_unit`: the v9 author, v9 lanes a and b, and v10 lanes a and b.
- **CAUSE (my own schema drift).** I wrote those 5 landing rows with two new unit fields and taught no reader to read them.
- **Metrics.** `campaign/_orchestration_metrics.py` now uses the shared fold (`.pre_163d1816b81b` kept). `orchestration_metrics.v1.json` was regenerated (sha256 prefix 3eb25643c0ee):
  - 518 rows, 470 executions, 48/48 amending rows applied;
  - notification-unit total 118,508,034, up from 117,835,959 (+672,075);
  - spend-unit total 2,623,577, up from 1,431,971 (+1,191,606).
- **OW-12 status tool.** `campaign/_book_close_status_ow12.py` now folds (`.pre_363647ad56e8` kept). This CORRECTS the owner's OW-12 figures:
  - Ezekiel is 70,428,450 tokens over 231 executions, not 71,188,346 over 278. Three things account for the change:
    - 47 amending rows are no longer counted as executions;
    - −1,431,971 spend-unit amendment tokens that had been added to a notification-unit figure;
    - +672,075 unit-field notification tokens.
  - Daniel has 3 executions, not 4.
  - Dates are unchanged.
- **Capture index.** `campaign/_capture_index.py` now folds, and takes a receipt's own `execution_id` where the receipt names one (`.pre_2aa34f6616c2` kept). Before this, two things went wrong:
  - every amending row became a phantom run: 7 in Ezekiel, 1 in Daniel;
  - 4 Ezekiel job pairs had their runs swapped: `ezek_pr_LF_c21`, `LF_c22`, `OL_c20` and `OL_c21`. Each #e1 watchdog-failure row was back-filled into the file after its #e2 landed row, so path-order derivation indexed the landed run as #e1.
- **The index rebuild.** The index was rebuilt for Jer, Lam and Ezek (`capture_index.v1.jsonl.pre_8bcf19a6c96d` kept; now sha256 prefix a5559ac3c901). `--check` is GREEN: 366 rows, 330 jobs, 0 problems.

  | Book | Rows before | Rows after |
  |---|---|---|
  | Jer | 74 | 74 |
  | Lam | 61 | 61 |
  | Ezek | 126 (stale since 2026-09-15) | 231 |

  - Layer A stays at 5. Layer C is 126, up from 122. No coverage was lost.
  - Every changed Ezekiel row is explained: 4 re-ordered, 20 amended, 0 unexplained.
  - Daniel is indexed at the Phase 0 landings.
- **Censuses.** `_census_tf6_candidate.py` and `_transcript_coverage_census.py` are unedited. They use receipts only as the set of distinct attempt_ids per book, and the fold leaves those sets identical (MEASURED): Dan 2, Ezek 199, Jer 74, Lam 57, OW2_audit 93, REPAIR 8.
- **Census v4.** `Ezek/repair2/census_ow15_v4.py` is bound to Ezekiel (hard-coded Ezekiel paths and output). Its `previous_executions[].agent_id` join, which covers 11 Ezekiel attempts, is OWED to the Daniel census port. That port is written against the shared fold and reads `previous_executions`. Ezekiel's v4 position is not re-measured here; that is left to the campaign-end review.
- **parent_agent_id.** `append_launch_row.py` now writes "orchestrator" (`.pre_63ec7fd63682` kept).
  - The 3 Daniel launch rows already written carry None, and `_capture_index.py:213` folds None to "orchestrator".
  - They are NOT amended. The in-flight guard (`_inflight_pin_guard.py:93-95`) takes any non-launch row naming an execution as that execution's landing, so amending a running execution would falsely land it and unpin its inputs. This is a HAZARD; it follows from the guard's rule as read.
- **OWED to the ledger** once both lanes land (the ledger is pinned now): one entry for the token-field schema drift and its cure, the amend-lands-in-flight hazard, and the parent_agent_id deviation. A DAD candidate goes with it.
- CURSOR: phase = DAN_PHASE0_TOOLKIT_PORT_LANES_D_E2_T2_IN_FLIGHT (unchanged; the fold work is done).

## 2026-09-24 - lane D #e2 landed and installed; T2 #e1 still in flight

Every figure below was read after the notification, from the lane's OUT and from my own runs (E-59).

- **Landing.** `dan_p0_device_inventory_a1#e2` (agent a5670ae5a0b0c1f12) COMPLETED. Its landing row is in `Dan/dan_phase0_attempt_receipts.jsonl`, which moved from 0b54699ce4ff to 52c5ab05fc80. It records 135,670 notification-unit tokens and 35 tool uses. The spend unit and model_actual are UNAVAILABLE at landing, because the usage block names neither.
- **Outputs** (digests MEASURED, and each matches the lane's report):
  - builder 46a069200fdd;
  - `dan_device_inventory.json` 466d7e6e91a6;
  - `final_message.md` 80c4ad78f11f, 25 lines;
  - `report.json` 9d015d7d62b9.
- **Review (MEASURED).** The builder's `--selftest` passes. Run with `--root SP/Dan` and `--out` pointing at scratch, it reproduces the inventory byte-identically.
- **Installed** at SP/Dan by write-once copy: `_build_device_inventory_dan.py` and `dan_device_inventory.json`. The installed builder, run in place with `--out` pointing at scratch, reproduces the installed inventory byte-identically. Pin guard CLEAR and workspace validator PASS came first.
- **Constants for citation_sweep** (MT face; none in a numbering zone; REPORTED by the lane and reproduced by my run):
  - DATELINE_PAIRS: 1:1, 2:1, 7:1, 8:1, 9:1, 9:2, 10:1, 11:1;
  - CAL_DATE_PAIRS: 10:4;
  - CAL_NO_ONSET: empty, with its reason.
  Daniel dates by regnal year only, so Ezekiel's year-plus-month rule finds 0 datelines. The Daniel rule is a logic change the lane states.
- **For the Fable end review** (OW-28):
  - 1:21 as a regnal end point (it would give 9 datelines);
  - 11:1, a dateline inside direct speech;
  - 10:4, a date continuing 10:1's year;
  - interval clauses;
  - the Opus fallback.
- **E-19 BREACH (the lane's own report).** After a shell heredoc failed to parse, the lane ran one read-only existence check (`wc -l` and `test -f`) on two exact OUT paths. No state changed. Its cause, in the lane's words: it checked for a partial write instead of reasoning from the parse error. This goes into the owed ledger entry as a recurrence class: a check after a failed write is still an existence check.
- **T1 depends on T2.** `_test_zone_tools_ezek.py` runs `check_marks.py` (9 calls), `check_web_quotes.py` (1) and `check_register.py` (2) as subprocesses, alongside citation_sweep (13) and `normalize_hebrew_in_json.py` (4). Two of those, check_marks and check_web_quotes, are T2's. So lane T1 is built and launched only after T2 is installed.
- The Dan capture index is rebuilt once T2 lands, so both landings go in one rebuild.
- CURSOR: phase = DAN_PHASE0_LANE_D_LANDED_INSTALLED_T2_IN_FLIGHT.

## 2026-09-24 - T2 #e1 landed FAILED (session limit); T2 #e2 in flight; the pin guard lands only on an outcome

Every figure below was read or measured in this session after the notification (E-59).

- **T2 #e1 landed FAILED.** `dan_p0_toolport_t2_a1#e1` (agent ada2bfae5a3be3dc8) was stopped by the account's API session limit (HTTP 429 rate_limit, request id req_011CfMNHTqsZrNJvENVkr7tx). The same limit stopped the orchestrator. It is not a watchdog stall. Its landing row moved the receipts from 52c5ab05fc80 to a06b457cfdff, with outcome FAILED_BY_API_SESSION_LIMIT. Tokens, model and the lane's last text are UNAVAILABLE: the notification carried no usage block, and the last text survives only in a compaction summary, so it is not recorded.
- **Residue.** 99 files, with mtimes from 2026-09-23T21:52Z to 2026-09-24T01:06Z, were moved unchanged to scratch `dan_p0/lane_T2_e1_residue`. Their digests are in the row. They include a spec_t2.py, a stage and a verify_1.json, so the lane got well past pin verification. The files are kept as evidence, unreviewed, and are not given to #e2. The mtime gap from 17:52 to 20:35 local falls inside the owner's earlier usage-limit pause.
- **Relaunch reason, now read and not typed.** `build_launch.py` hard-coded "stopped by the runtime watchdog" for every relaunch, which is false for T2 #e1. It now reads the stop from #e(N-1)'s landing row outcome. It refuses when that execution is unlanded or its outcome names no known stop. Pre copy `.pre_41c964399817`. Regression: a T2 #e3 build refuses while #e2 is in flight, and a D #e3 build refuses because D #e2 COMPLETED.
- **T2 template.** Its line "A second lane (D) runs at the same time" was false for #e2. It now reads "Other lanes may run at the same time on other jobs". Pre copy `.pre_4ea170fed510`. The first #e2 build, which had never been launched, was set aside as `BRIEF_T2_e2.md.unlaunched_318697869180` and `launch_message_T2_e2.txt.unlaunched_1246a84fef21`.
- **T2 #e2 launched.** Agent ace50afb8c95fdb7a runs brief `BRIEF_T2_e2.md` (bda4fe47bcb2) with message dcaab9f0a581. Both `_brief_pin_check` and `_launch_message_check` returned MATCH. The workspace validator passed, and 22 pins are in place. The launch row carries the retry fields and moved the receipts from a06b457cfdff to 31f1ca1c877b. The ledger is PINNED again until #e2 lands.
- **Pin guard cured (the amend-lands-in-flight hazard).** In `campaign/_inflight_pin_guard.py`, a row now lands an execution only if it is not a launch record and carries an outcome that is non-empty and not RUNNING. Before, any non-launch row did, so an outcome-less amendment of a running execution would have released its pins. The pre copy is `.pre_44f8c26e8924`, and the file is now bffd294c0716.
  - MEASURED before the change, over every book directory: 0 executions would flip.
  - The selftest is 24/24 GREEN, including 2 new vectors.
  - With the old rule swapped back in, those 2 vectors go RED.
  - `in_flight` is identical before and after for all 16 SP directories.
- **Siblings.** Three scripts carried the same any-non-launch-row rule. All three now import the guard's `lands()`:
  - `append_launch_row.py`: the risky one. It would have accepted a relaunch over an execution that was only amended. Pre `.pre_f6ca5034d292`, now a9052bc26ca1.
  - `append_landing_row.py`: it would have refused a true landing after an amendment. Pre `.pre_1df4a10d77b2`, now 6f4f738021eb.
  - `build_launch.py`: pre `.pre_8a8b6e41ce83`, now 9b6c45924c8a.
  In a temp tree, an amended-only execution now lands once and refuses a second landing. append_launch_row's relaunch refusal was NOT run end to end, because its message path is fixed to the real scratch.
- **Orchestrator slip, contained.** `python -m py_compile` wrote `Dan/phase0_lanes/__pycache__/build_launch.cpython-312.pyc` into SP at 09:13 local. py_compile writes the pyc whatever `-B` says. I removed it, since the directory held only that file. The ast.parse check replaces it. This belongs in the owed ledger entry.
- CURSOR: phase = DAN_PHASE0_T2_E1_LANDED_FAILED_T2_E2_IN_FLIGHT_GUARD_CURED.

## 2026-09-24 - T2 #e2 landed, amended and installed; the Dan capture index rebuilt; T1 next

Every figure below was read or measured in this session after the compaction (E-59).

- **T2 #e2 landed COMPLETED.** `dan_p0_toolport_t2_a1#e2` (agent ace50afb8c95fdb7a): five tools staged at residual 0; selftests GREEN. Its landing row (scratch `dan_p0/landing_T2_e2.json`, 9754fc6da34a) moved the receipts from 31f1ca1c877b to 7e2f8496eaff, 8 rows. It records 95,521 notification-unit tokens, 53 tool uses and 1,511,763 ms; the spend unit and model_actual are UNAVAILABLE (the usage block names neither). It lists 11 outputs with digests and 6 items for Fable's end review.
- **Orchestrator review.** An independent restage from the lane's `spec_t2.py` (6c206a9a7144) is byte-identical to its stage. A copy of the lane's mirror reran every selftest and synthetic check with identical results.
- **E-19 breach by the lane, disclosed by it.** One shell glob, `stage/*.py`, inside its own OUT. It read nothing outside OUT. Recorded in the landing row's `e19_breach`; owed to the ledger.
- **Orchestrator amendment (a half-truth caught at landing).** As staged, check_refs_mirror's legacy-aggregate comment and emitted note named the predecessor book's 444 / 131 / 817 as the figures to compare with, so every Daniel run would have emitted them. `spec_t2.orch_v2.py` (1490b8bee98a) is the lane's spec unchanged plus two appended exact-once substitutions. Restage residual 0; only check_refs_mirror.py differs, in 2 hunks; the lane's suite reran on a mirror copy with identical results.
- **Installed** by `_adapt_tools_dan.py --install` with the amended spec, after the pin guard (CLEAR) and the workspace validator (pass). Report `install_T2.report.json` (4da028017339), residual 0. Now in `Dan/tools`: check_web_quotes fadb6cff6647, check_refs_mirror d03d0449717c, check_marks df1818f72467, _punct_boundary_sweep 00e04c87e070, _audit_book_token_transform c5a6a5248920. The Dan census went from 69 to 74 files, exactly those 5 added.
- **In place**, with TEMP in scratch (left empty): check_web_quotes --selftest GREEN; --a6-selftest 7/7; check_refs_mirror --a4-selftest 32/32; check_marks --marks3d-selftest 12/12.
- **Token-transform audit** (`audit_token_transform_dan.json`, caae51888dc4): 18 files, 212 source-token lines, 210 changed, 2 kept verbatim, 21 Daniel lines naming the source book, 9 with a lineage word. Every one was read as true lineage.
- **Seventeen tools, MEASURED.** The 12 in `_adapt_tools_dan_spec.TOOLS` plus the 5 T2 tools are all in `Dan/tools`, which matches the T1 brief's "Seventeen tools are already ported and installed". The four tools T1's test runs are present.
- **`append_launch_row.py` docstring** now says the runtime id goes in `agent_id` and "orchestrator" in `parent_agent_id`. Pre `.pre_a9052bc26ca1`, now cfbef95a5caa, AST OK.
- **Dan capture index rebuilt.** Pin guard CLEAR; pre copy `campaign/capture_index.v1.jsonl.pre_a5559ac3c901`. It indexes 4 Daniel executions over 2 jobs (D #e1, D #e2, T2 #e1, T2 #e2). `--check` is GREEN: 370 rows, 332 jobs, 0 problems. The 366 non-Daniel rows are byte-identical. The index is now 5abc52f06e20.
- **Ledger.** It is unpinned. Entries E-63 and E-64 are drafted at scratch `ledger_E63_E64_draft.md`, not yet written.
- CURSOR: phase = DAN_PHASE0_T2_LANDED_INSTALLED_T1_NEXT.

## 2026-09-24 - ledger E-63..E-65 written; T1 brief amended (E-65, E-19); T1 #e1 in flight

Every figure below was measured in this session (E-59).

- **Ledger.** E-63, E-64 and E-65 were appended to `M8/ERROR_PATTERN_LEDGER.v1.md` under the pin guard (CLEAR), a digest precondition and an atomic replace. The ledger went from ad6783316d04 at 2,620 lines to 9b4721664571 at 2,815 lines. The pre copy is `.pre_ad6783316d04`. E-63 was confirmed free first: 0 mentions of E-63..E-69.
  - E-63: receipts schema drift, the amend fold, and the pin-guard landing rule. It now also records today's Dan capture index rebuild.
  - E-64: three slips on an unread assumption about a tool. Its sibling audit adds T2 #e2's own E-19 glob and the cure.
  - E-65 (new): a ported tool would have emitted the predecessor's 444 / 131 / 817 in every Daniel run. Root cause: the adapter's `FACT` residual pattern (line 49) is a fixed list, so residual 0 means only that no LISTED fact survived. Sibling audit: 2 lineage mentions of 444 remain in the #e14 comment block of `check_refs_mirror.py` (lines 364 and 367), never emitted; 6 "shipped/member's" hits in other installed tools, all inside module docstrings (by ast). OWED: the two blind toolkit review lanes must name "any number in an emitted string or note that is not a Daniel fact" as a review item.
- **T1 template amended twice** (pin guard CLEAR each time, pre copies kept).
  - E-19: "A shell wildcard such as `stage/*.py` in any command is a glob, even inside `OUT`: name every file" (pre `.pre_2e9e45162ad4`).
  - E-65: Task 2 now orders a tokenize-based scan of every two-or-more-digit number in each staged file's strings and comments, each classified as daniel_measured, lineage or neither, with a new `predecessor_figures` report key (pre `.pre_dedd45b06f07`).
- **First T1 build set aside, unlaunched.** It was built before the E-65 clause, as `BRIEF_T1.md.unlaunched_445564eb7d47` and `launch_message_T1.txt.unlaunched_d825ae0fe176`.
- **Seventeen tools verified before the build.** The 12 in `_adapt_tools_dan_spec.TOOLS` plus the 5 from T2 are all in `Dan/tools`.
- **T1 #e1 launched.** `dan_p0_toolport_t1_a1#e1` is agent abe7e67a91ec68b19, launched 2026-09-24T13:55:21Z. It runs brief `BRIEF_T1.md` (15e5c49af775) with 25 pins, and message `launch_message_T1.txt` (8e433a1e3bb3). `_brief_pin_check` and `_launch_message_check` both returned MATCH, and the workspace validator passed. The launch row moved the receipts from 7e2f8496eaff to e181e35efa0b.
- **The ledger is PINNED** until T1 lands. CYCLE_STATE, CURRENT_STATE, the resume prompt and the capture index are CLEAR.
- CURSOR: phase = DAN_PHASE0_LEDGER_E63_E65_T1_E1_IN_FLIGHT.

## 2026-09-24 - Daniel Phase 0: the strategy lane S launched (T1 #e1 still in flight)

- **Strategy validator written.** `SP/Dan/_validate_strategy_dan.py` (7e2bbbd67d3d, 251 lines) is read-only and orchestrator-written, so the author cannot weaken the tiling check. It reads the WEB-face `verse_inventory.json` (357 verses), `dan_device_inventory.json` and `campaign/daniel_start_readiness.v2.json`. It checks: face; contiguous forward parents and parts summing to 357; each span written as `C:V-C:V`; an `oshb:Dan.` dual on every line whose span touches a zone verse (ch 4, ch 6, 5:31); declared internal parent seams equal to the measured seams and each disclosed; `## §N` headings 1..11; the lens record (>=2, reason >=40 chars, a third lens's kind drawn from the readiness kinds); and exact, verbatim, once-only coverage of the 8 scrutiny targets and 5 device review items, each with a section and a disposition. Its `--selftest` passes 19/19, each RED case naming its expected problem.
- **Brief template written.** `SP/Dan/phase0_lanes/BRIEF_S.template.md` (41ae289a4703). It covers attempt `dan_strategy_a1`, the Opus-in-Fable-role downgrade (grader_fallback, OW-25), both macro-shapes tested (genre and language), ten binding campaign rules, ranged reading of the Ezekiel v2 strategy and method v6, an md with sections 1..11, the plan JSON, and a GREEN validator. The budget is about 70 tool calls and at most 4 validator runs. The Ezekiel v1 strategy brief was never persisted, so this one is designed from Ezekiel's strategy, its validator and the readiness data.
- **build_launch.py amended** (pre `.pre_9b6c45924c8a`; now f3c3b73676a5). The E-13 work phrase is per-lane, with the toolkit phrase as the default. LANES["S"] carries 16 pins. A scratch check shows the D, D_e2, T2, T2_e2 and T1 messages reproduce byte-identically.
- **append_launch_row.py amended** (pre `.pre_cfbef95a5caa`; now 0206dce0c349). It adds LANES["S"] (lane `phase0_book_strategy`) and per-lane producer and catcher, keeping the toolkit text as the default. It passed ast.parse.
- **S #e1 launched.** `dan_strategy_a1#e1` is agent adf1cd7065c18a7b6. Its brief is `BRIEF_S.md` (b0daab9c336c, 300 lines, 16 pins) and its message is `launch_message_S.txt` (4851fe78e496). `_brief_pin_check` and `_launch_message_check` both returned MATCH, and the scoped workspace validator passed. The launch row moved the receipts from e181e35efa0b to 58d1385c3a4f.
- **Pinned now.** T1's 25 pins, including the ledger, and S's 16 pins, including `_validate_strategy_dan.py`, the ledger range, Ezekiel's v2 strategy, method v6 and Daniel's inventories. Pin-guard every write.
- CURSOR: phase = DAN_PHASE0_STRATEGY_S_E1_AND_T1_E1_IN_FLIGHT.

## 2026-09-24 - Daniel Phase 0: the two blind strategy check lanes prepared (S #e1 and T1 #e1 still in flight)

- **Templates written.** `SP/Dan/phase0_lanes/BRIEF_C1.template.md` (d5a614f7baf4) is the bytes-and-architecture check. It runs the validator once and then re-derives the tiling without it, and checks the duals through the offset map, the language claims, the device and mark claims (both sides of each seam; PE never SAMEKH; E-23), E-65's numbers audit with slice-checked quotations, coverage of the readiness scrutiny targets and the device review items, OW-18 tiers, and plan-md agreement. `BRIEF_C2.template.md` (a95e26f3916c) is the text-first check. Stage A is a pre-registered independent reading (`c2_independent_reading.json`, its digest recorded before Stage B) made BEFORE it opens the candidate, the hardness file or the readiness file. Stage B grades every seam, the macro-shape, row pre-decision, reception neutrality, cross-tradition scope, low-confidence regions, the section 8 register, part balance and calendar onsets. C2 never sees the device inventory or the validator, so the two methods stay decorrelated (OW-19). Both return fit_to_accept or not_fit, with each DEFECT carrying an exact find/replace correction or a judgement for adjudication. The brief was ported in shape from `Ezek/repair2/strategy_v2/STRATEGY_V2_CHECK_BRIEF.md`.
- **Launch tools amended** (pin guard CLEAR). `build_launch.py` (pre `.pre_f3c3b73676a5`, now 5059a036431b) has LANES C1 (16 pins) and C2 (13 pins). Both pin the candidate at `SP/Dan/strategy_candidate/book_strategy_Dan.a1.md` and `strategy_plan_Dan.a1.json`, so neither can be built before S lands. `append_launch_row.py` (pre `.pre_0206dce0c349`, now 07d35b01e93c) has C1 and C2 with per-lane producer and catcher. Both passed ast.parse. The scratch check shows D, D_e2, T2, T2_e2, T1 and S messages still reproduce byte-identically.
- **Dry render** (scratch `dry_render_check_lanes.py`, writes only in scratch). No unfilled placeholder; `#e1` appears once; `_brief_pin_check` drift [] with only the two candidate files missing; the launch message gate's only gap is that missing-pin DRIFT.
- **DAD ingest of E-59..E-65 deferred** until after T1 and S land and a compaction, so that the landings do not re-read its context. It stays owed. The harness to port is `Ezek/repair2/dad_ingest_E52_E58.py` with `gen_dad_ingest_E52_E58.py` and `dad_records_E52_E58.py`. The DAD front door (preflight, midflight acks before writes, postflight with explicit --file) is run by hand around it.
- CURSOR: phase = DAN_PHASE0_CHECK_LANES_PREPARED_S_T1_IN_FLIGHT.

## 2026-09-24 - Daniel Phase 0: T1 #e1 and S #e1 landed FAILED (API session limit); both relaunched as #e2

- **Both #e1 executions were stopped by the account's API session limit** (HTTP 429, rate_limit, 'resets 1:10pm (America/New_York)'). S #e1 (request req_011CfNQpkijZG6nPYGzxYnVF) last reported 'Digest matches. Reading the brief.' T1 #e1 (request req_011CfNRagkM7Wikt9GnmjDVW) last reported 'The digest matches. Reading the brief.' Every value was re-read from the runtime notifications at lines 32065 (S) and 32070 (T1) of the session transcript, never from the compaction summary (E-59). Neither lane landed a deliverable.
- **Landed FAILED_BY_API_SESSION_LIMIT** through scratch `land_session_limit_e1.py` (one generator, the lane a parameter, ported from `land_T2_e1.py`; dry-run first) and `append_landing_row.py`, pin guard CLEAR. Each OUT was moved unchanged, with a census and digests in its row, to `dan_p0/lane_T1_e1_residue` (15 files, 13:56Z-14:30Z) and `dan_p0/lane_S_e1_residue` (8 files, 14:12Z-14:20Z, including the early final_message.md the brief orders; no md, no plan). The residue is not reviewed, not installed and not given to #e2. Tokens and model_actual are UNAVAILABLE: the failure notifications carried no usage block. Receipts 58d1385c3a4f -> 572984167b09 -> 4d590cda2e40.
- **Relaunched as #e2.** `build_launch.py --lane T1 --execution 2` wrote BRIEF_T1_e2.md 4ccf65103ebb (25 pins) and a message 187c377e7bfa. `--lane S --execution 2` wrote BRIEF_S_e2.md 52c7c4ada383 (16 pins) and a message 818550c35fbc. `_brief_pin_check` and `_launch_message_check` both returned MATCH, each brief names #e1 exactly once with the session-limit relaunch sentence, and `validate_workspace_policy.ps1 -ScopeWorktreeId logos-t423-m8-fable` passed with no blocking failures. Both were launched at 2026-09-24T17:16:24Z with the message files' exact text (general-purpose, opus, background). Launch rows were appended with --execution 2 and a session-limit retry reason. Receipts 4d590cda2e40 -> 4275333d44dc -> af471af07394 (14 rows).
- CURSOR: phase = DAN_PHASE0_T1_S_E2_IN_FLIGHT.

## 2026-09-28 - Daniel Phase 0: T1 #e2 and S #e2 landed FAILED (API weekly limit); both relaunched as #e3

- **Both #e2 executions were stopped by the account's API weekly limit** (HTTP 429, rate_limit, 'resets Sep 28, 10am (America/New_York)'). This is a different limit from the #e1 session limit. S #e2 (request req_011CfNgo6PETQvN6r7i6c3UD) last reported the start of 'Survey 2: formula census, datelines, calendar dates, language switches and self-assertions from the device inventory'. T1 #e2 (request req_011CfNhuQEoeuMod1RE3y6Yq) last reported 'Digest matches. Reading the brief.' Both values come from the runtime notifications as delivered, read in context (E-59). The owner said 'Try again' after the reset; the orchestrator confirmed the clock was past it (14:08Z) before relaunching.
- **Landed FAILED_BY_API_WEEKLY_LIMIT** through scratch `land_api_limit.py` (generalises land_session_limit_e1.py to any execution; dry-run first) and `append_landing_row.py`, pin guard CLEAR. The generator REFUSED T1 at first because OUT held a `final_message.md`. The orchestrator read both early final messages whole: T1's (65b09a26a14d, 'IN PROGRESS (E-29 early write)') and S's (cdcc8bdd7442, 'PROVISIONAL, written first'; it names a planned genre shape of tales 1:1-6:28 and visions 7:1-12:13, 10 parents, 6 parts and 3 lenses, not reviewed). Neither holds a result or an escalation. Each is exempted by its exact digest only. Each OUT was moved unchanged, with a census in its row, to `dan_p0/lane_T1_e2_residue` (25 files, 17:17Z-17:44Z on 09-24) and `dan_p0/lane_S_e2_residue` (9 files, 17:17Z-17:49Z). Tokens and model_actual are UNAVAILABLE. Receipts af471af07394 -> 1811fca07124 (16 rows).
- **build_launch.py amended** (pin guard CLEAR; pre `.pre_5059a036431b`, now a776a1e6d188; ast.parse OK). STOPS gains `FAILED_BY_API_WEEKLY_LIMIT` -> 'stopped by the account's API weekly limit', so that a relaunch brief never calls a weekly stop a session stop (OW-18). Only build_launch.py keys on the prefix; the other hits are test fixtures. The scratch check shows D, D_e2, T2, T2_e2, T1 and S messages still reproduce byte-identically.
- **Relaunched as #e3.** BRIEF_T1_e3.md is 7f807d16c930 (25 pins), message 6f6db3006c5e. BRIEF_S_e3.md is 4f2a5af4d50a (16 pins), message 3be3e6b78a4e. Both returned MATCH on `_brief_pin_check` and `_launch_message_check`, and each names the #e2 weekly-limit stop. Each message differs from #e2's only on its BRIEF line. The workspace validator passed with no blocking failures. Both were launched at 2026-09-28T14:11:43Z with the files' exact text (general-purpose, opus, background). Receipts 1811fca07124 -> e3ec02ab3458 -> fe32dc0c2cde (18 rows).
- **Forecast note.** Two Opus lanes in parallel have now been stopped twice by account limits (session, then weekly) before landing anything. If #e3 is stopped too, report to the owner before a fourth attempt, rather than relaunching blind.
- CURSOR: phase = DAN_PHASE0_T1_S_E3_IN_FLIGHT.

## 2026-09-28 - Daniel Phase 0: S #e3 LANDED (strategy candidate a1); blind check lanes C1 and C2 launched

- **S #e3 landed COMPLETED** (row `dan_p0/landing_S_e3.json` 8681fa21cefe from scratch `land_S_e3.py`; `append_landing_row.py`, pin guard CLEAR; receipts fe32dc0c2cde -> 23c3805c8deb). Usage from the notification's usage block, read by targeted extraction (`read_usage.py`, transcript lines 32389/32391): 120,887 notification-unit tokens, 50 tool uses, 1,806,908 ms; model_actual and the spend unit UNAVAILABLE. The lane's validator run 1 of 4 was GREEN (0 problems).
- **Orchestrator review (MEASURED):** an independent rerun of `SP/Dan/_validate_strategy_dan.py` on the md and plan returned rc 0 and problems []; `--selftest` rc 0; every reported output digest matches; numbers_audit 'neither' is empty (E-65); parents PA-PJ and parts W1-W6 each tile all 357 WEB verses contiguously; the Cyrus verses are 1:21, 6:28 and 10:1; the lane's first-person pattern hits 9 verses, all in chapters 7-12 (7:15, 7:28, 8:1, 8:15, 8:27, 9:2, 10:2, 10:7, 12:5).
- **Reserved finding (a wording defect, withheld from C1/C2 so that it tests whether they catch it):** md line 23 says the first-person "I, Daniel" occurs in 9 verses. The literal WEB string occurs in 5 (8:27, 9:2, 10:2, 10:7, 12:5); 7:15, 7:28 and 8:1 read 'me, Daniel' and 8:15 'I, even I Daniel'. The count is right; the wording overstates the literal string (OW-18). Correct the wording at reconciliation.
- **Shape:** the genre frame, court tales 1:1-6:28 (196) and vision reports 7:1-12:13 (161); 10 parents, 6 parts (70, 67, 59, 55, 27, 79), four parts crossing a parent seam, all disclosed (1:21/2:1, 3:30/4:1, 5:30/5:31, 7:28/8:1); 3 lenses. No calendar-onset rule was stated (cal_no_onset rule null; 10:4 is listed for Fable), so CAL_NO_ONSET stays. Nine Fable end-review items are carried in the row. The lane's four Phase 0 defect notes (device inventory 'four zones' wording; vision_noun_mareh_heb counts the 'appearance' sense; readiness v2 carries OW-25-superseded entries; the strategy validator checks neither cal_no_onset nor parts whose edges fall inside a parent) are notes only.
- **Candidate placed write-once** (scratch `copy_S_candidate.py`, pin guard CLEAR on both targets, re-hashed after write): `SP/Dan/strategy_candidate/book_strategy_Dan.a1.md` 92981befa96c and `strategy_plan_Dan.a1.json` a4dd192d0a56.
- **C1 and C2 launched blind** at 2026-09-28T14:49:32Z with the message files' exact text (general-purpose, opus, background). BRIEF_C1.md 30edb3d4ee5b (message 6776c1c57512), BRIEF_C2.md 25c278c2b618 (message 303a92f40990); both MATCH on `_brief_pin_check` and `_launch_message_check`; neither brief nor message mentions the reserved finding. The workspace validator passed (0 blocking). Receipts 23c3805c8deb -> fdac3c85864b -> 2ac9612b06b1 (21 rows). T1 #e3 is still in flight.
- CURSOR: phase = DAN_PHASE0_S_LANDED_C1_C2_IN_FLIGHT.

## 2026-09-28 - Daniel Phase 0: T1 #e3 landed and installed; C1 landed (reserved finding CAUGHT); C2 landed FAILED (API session limit), its relaunch awaits the owner

Every figure below was read or measured in session af84b702 after the compaction (E-59).

- **T1 #e3 LANDED COMPLETED** (`dan_p0_toolport_t1_a1#e3`, agent a43bba2088701ee49). Landing row scratch `dan_p0/landing_T1_e3.json` (5ac1b8f574f1); receipts 2ac9612b06b1 -> 61da103eb556 (22 rows). 77,232 notification-unit tokens, 48 tool uses, 2,820,994 ms; spend unit and model_actual UNAVAILABLE. 7 items for Fable's end review. Orchestrator review: independent restage byte-identical (residual 0); a copy of the lane's mirror reran the test (GREEN 263) and the synthetic sweep (the 5 planted rows) with identical output; the named_interior vector change is the inherited Ezekiel MARKS-3D ruling (Ezek check_marks lines 633-647).
- **T1 INSTALLED** by `_adapt_tools_dan.py --install dan_p0/restage_T1 --extra-spec dan_p0/lane_T1/spec_t1.py` (1691a5f85c7d) after the pin guard (CLEAR on both targets and the capture index) and the workspace validator (pass, 0 blocking). Report `install_T1.report.json` (a0268eaf3db4), residual 0. Now in `Dan/tools`: citation_sweep d5bd9b33a9c0 and _test_zone_tools_dan a3aa391251b9. The Dan census went from 93 to 95 files, exactly those 2 added, nothing removed or changed. The landing row's `install: PENDING` is discharged by this entry (the row is not edited).
- **In place**, TEMP in scratch (left empty): `_test_zone_tools_dan.py` exit 0, GREEN 263/263, stdout identical to the lane's run_test.txt (`inplace_test_zone_tools_dan.txt`, 711679979e6d).
- **Token-transform audit** rerun (`audit_token_transform_dan_T1.json`, 4825d96851ed): 19 files (was 18), 268 source-token lines, 266 changed, 2 kept verbatim, 23 Daniel lines naming the source book, 15 with a lineage word; the new file is citation_sweep.py (56 lines, all changed; 2 naming the source, 6 lineage). **Coverage gap:** the audit pairs a Daniel tool with the same-named source tool, so the renamed `_test_zone_tools_dan.py` (from `_test_zone_tools_ezek.py`) is not audited. Covered by hand: its 37 source-book lines are 27 lines carrying the kept rule id `puncta_claim_in_ezek` (KEEP in spec_t1.py with its reason) and 10 lineage ids (rulings, the ported-from line, a ported vector id, the inventory's crosswalk key). OWED: teach the audit the adapter's RENAME map.
- **C1 LANDED COMPLETED** (`dan_strategy_check_c1_a1#e1`, agent afa5acb8873ed42df). Landing row `dan_p0/landing_C1_e1.json` (44a51acffe0c); receipts -> a596ff316d3b (23 rows). 135,114 notification-unit tokens, 39 tool uses, 997,878 ms. Verdict not_fit: 10 defects, D1-D8 and D10 with an exact correction, D9 a judgement. **Reserved finding CAUGHT**: C1 found the withheld md line 23 defect blind, as D6. The corrections are not applied until both check lanes land.
- **C2 LANDED FAILED_BY_API_SESSION_LIMIT** (`dan_strategy_check_c2_a1#e1`, agent ac7e0e3e96f591c77, request req_011CfW3skv48C3QaBwVeXch5). The notification was re-read fresh from session 910cbe15's transcript line 32966 (record timestamp 2026-09-28T15:10:21.830Z). Landing row `dan_p0/landing_C2_e1.json` (727eb314043a) by scratch `land_api_limit.py` (extended for C2: a SESSION limit key and an exact-digest partial exemption; pre copy `.pre_b2adfe72e98b`), dry run first; receipts -> 90213bc7b4c8 (24 rows). OUT moved unchanged to `dan_p0/lane_C2_e1_residue` (12 files, 14:50Z-15:06Z). It holds a frozen Stage A reading `c2_independent_reading.json` (188a232adf8b, 71 seams; structure and escalation checked only, 0 hits) and an early final_message.md (f7ced05bb1d9, read whole: Stage B in progress, no result). Kept as evidence, not given to any later execution.
- **Dan capture index rebuilt.** Pin guard CLEAR; pre copy `campaign/capture_index.v1.jsonl.pre_5abc52f06e20`. 12 Daniel executions over 6 jobs. `--check` GREEN: 378 rows, 0 problems. The non-Daniel rows are byte-identical. The index is now 79f1aa041576.
- **No agent result is un-landed.** Reconciliation needs two blind lanes (OW-19), so it waits on C2 #e2. The orchestrator committed to report a limit stop to the owner before any relaunch; that report is the next act.
- CURSOR: phase = DAN_PHASE0_T1_INSTALLED_C1_LANDED_C2_LIMIT_AWAITS_OWNER.

## 2026-09-28 - Daniel Phase 0: C2 relaunched as #e2 on the owner's go

- **Owner's go.** The orchestrator reported C2 #e1's session-limit stop and asked how to relaunch. The owner chose a fresh relaunch (same brief template, empty OUT, no reuse of #e1's frozen Stage A reading).
- **Built** by `build_launch.py --lane C2 --execution 2` (a776a1e6d188): `Dan/phase0_lanes/BRIEF_C2_e2.md` (a90e6e3ed9ba), 13 pins, brief pin check MATCH; scratch `dan_p0/launch_message_C2_e2.txt` (d7bd10c4f0f2), E-62 launch-message check MATCH, 0 gaps. The brief differs from BRIEF_C2.md only in its execution line, which names #e2 and states that #e1 landed no deliverable and nothing of it is the lane's to use. OUT `dan_p0/lane_C2` is empty (0 entries).
- **Launched** at 2026-09-28T21:55:14Z (the orchestrator's clock just after the launch) with the message file's exact text, after the workspace validator (pass, 0 blocking). Agent a5bbd44e74ce92595, execution `dan_strategy_check_c2_a1#e2`. Launch row by `append_launch_row.py` with --execution 2 and a retry reason, pin guard CLEAR; receipts 90213bc7b4c8 -> e0dea843963a (25 rows).
- CURSOR: phase = DAN_PHASE0_C2_E2_IN_FLIGHT.

## 2026-09-28 - DAD ingest of ledger E-59..E-65 landed while C2 #e2 runs

- **Drafted from a fresh read** (E-59's cure) of `ERROR_PATTERN_LEDGER.v1.md` lines 2380-2815, each record checked clause by clause against its entry before the write. Records `Ezek/repair2/dad_records_E59_E65.py` (4df77b5150d5); generator `gen_dad_ingest_E59_E65.py` (2ef8420e1588, built from the E52_E58 harness by exact-once anchors, `--check` MATCH); harness `dad_ingest_E59_E65.py` (0237d2686569). Pin guard CLEAR on all five targets before the writes.
- **Pre-run checks:** ast OK on the three files; 7 records with no split characters and each with its scope and danger lines; every heading found exactly once; dedupe re-scan 0 hits; forward-marker lint CLEAR.
- **Ran:** 7 candidate error-pattern records written, files 1894 -> 1901, read-back identical, problems none; no control marker allocated; ledger 9b47216645716d2d pinned and unchanged. Result `dad_ingest_E59_E65.result.json` (e09cb769ea68).
- **Postflight** (DAD session 17469fab, handoff eacdf45f) sent only after the forward-marker lint cleared its own text; the three required review lanes ran as checklists. Lesson reindex and graph stay QUEUED (not re-ruled). The E-59 recurrence note in this file is still a candidate and was not ingested. Next delta: ledger entries after E-65.
- CURSOR: phase = DAN_PHASE0_C2_E2_IN_FLIGHT_DAD_E59_E65_INGESTED.

## 2026-09-28 - C2 #e2 LANDED; token-transform audit fixed (E-66); toolkit selfcheck built; learning log L-0078/L-0079

- **Token-transform audit fixed (E-66).** `Dan/tools/_audit_book_token_transform.py` now pairs by name, then by the
  adapter's filename token (`_dan` to `_ezek`). It declares `_toolkit_selfcheck.py` AUTHORED and lists every other
  unsourced file as `unpaired`. It is at a3b030a9f1b0, with pre-image `.pre_c5a6a5248920` kept. Its diff against the
  pre-fix run: `_test_zone_tools_dan.py` added (148 source-token lines, 16 lineage lines, all read and all true
  lineage), the selfcheck moved to authored, 0 other rows changed.
- **E-61 item 2 built.** `Dan/tools/_toolkit_selfcheck.py` (1784d851b5c6) runs `--artifacts-only` GREEN, and 11 of 11
  planted defects were caught. The full scope stays RED only on its two TOOLKIT.md checks until Daniel's TOOLKIT.md is
  written. Its section 5 is the E-65 floor (integers of 100 or more).
- **C2 #e2 LANDED** (dan_strategy_check_c2_a1#e2) with verdict not_fit and 8 defects: 5 exact (DEF-2, DEF-4, DEF-6,
  DEF-7, DEF-8) and 3 judgement (DEF-1, DEF-3, DEF-5). The reserved finding was MISSED; C1 had caught it as D6. Every
  claim was measured by `dan_p0/review_C2.py`. C1's 9 then C2's 5 exact corrections, applied jointly in memory, are
  14 of 14 unique, and the plan still parses. Receipts are at 59ac6f99a44e (26 rows); the capture index is at
  c1855809a302.
- **Ledger E-66** was appended: 85dbdda709d1 (2902 lines), pre copy `.pre_9b4721664571`. It also discloses the
  review script's Hebrew-strip misread, caught before any record used it. The rule now: a review script that reads
  Hebrew imports `dan_lib.skeleton`.
- **Learning log.** L-0078 records the lens-multiplicity datum; L-0079 records that 7 of 13 Phase 0 executions failed
  on runtime limits. The log is at 5778b005331b (79 rows), pre copy `.pre_0708bd43c95f`; metrics were rebuilt at
  705ffabd3375 (pre copy `.pre_3eb25643c0ee`).
- **OWED.** Learning-log rows for the D, T2, T1 and S landings, drafted from the landing rows and ledger E-60..E-65,
  never from a summary. The DAD ingest of E-66 (the next delta after E-65). The census `previous_executions` join and
  the unknown-token-field refusal, at the Daniel census port.
- CURSOR: phase = DAN_PHASE0_C2_E2_LANDED_RECONCILE_NEXT.

## 2026-09-28 - Daniel strategy RECONCILED and placed (C1 + C2); validator requires plan MT duals

- **Validator amended (C1 D9).** `Dan/_validate_strategy_dan.py` is at dd5fa70a5bb2 (pre copy `.pre_7e2bbbd67d3d`). Every
  zone-touching span in the plan must carry `mt_dual`, checked against `tools/verse_map_web.json`, and the script
  refuses if any `web_mt_offset_map.json` anchor disagrees with that map. Selftest 23 of 23; on the `.a1` pair it was
  RED with exactly the 4 expected mt_dual problems (PD, PF, W2, W3).
- **Reconciled strategy placed** at `SP/Dan/book_strategy_Dan.md` (158e517af36d, 529 lines), `SP/Dan/strategy_plan_Dan.json`
  (a35acfb997ce) and `M8/book_strategy/Dan.md` (identical). The generator is scratch `reconcile_dan_strategy.py`
  (185c5b4bb4fd); every target was pin-guarded CLEAR and was absent before an exclusive create with a byte check. The
  validator is GREEN on the placed pair. The `.a1` candidate is unchanged (92981befa96c, a4dd192d0a56).
- **Applied:** C1's exact D1-D8 and D10, then C2's DEF-2, DEF-4, DEF-6, DEF-7 and DEF-8, straight from the lane files,
  each find unique at its turn. **Ruled** on claude-opus-5-5 (OW-25 grader_fallback): C1 D9 options (b) and (c) (plan
  `mt_dual` fields; MT duals in four plan strings); C2 DEF-1 (a) (D1 becomes a weighing rule; new section 7 items (o)
  and (p) name the rival edges after 2:20-2:23 and after WEB 4:34-4:35); DEF-3 (a) (the succession formula at 11:7,
  11:20 and 11:21 is a text signal; no mark stands in chapter 11); DEF-5 (a) and (b) (2:4 quotations and counts by
  half). Plan for_fable items FF9-FF12 list the four rulings for Fable to re-rule. The md ends with "What changed from
  a1": 19 items, each naming the lane item it executes; the lane-fix summaries are cut from the lane files' own findings.
- **Near-miss (E-59 class), caught.** The compaction summary said the `.a1` plan does not round-trip through
  `json.dumps`. A fresh probe showed it does with `indent=1, ensure_ascii=False` and no final newline, so the plan was
  edited structurally with a round-trip assertion. The generator's first draft also cut one lane summary inside a
  quotation; the review of the added lines caught it, and the fix refuses an open quotation.
- CURSOR: phase = DAN_PHASE0_STRATEGY_RECONCILED_TOOLKIT_NEXT.

## 2026-09-28 - Daniel TOOLKIT.md placed and pinned; E-67 recorded; toolkit receipt appended

- **TOOLKIT.md placed** at `SP/Dan/tools/TOOLKIT.md` (d9bc3a0a17fb). It names kjv_variance_crosscheck and zone_pairs,
  never content_anchors.
- **Selfcheck amended** to 3fe5e2e50e03 (pre copies `.pre_b7638621a252`, `.pre_1784d851b5c6`): 15 TOOLKIT_PINS, each
  figure formatted from the artifact it came from, plus the E-65 guard. Full scope 232/232 GREEN,
  `--artifacts-only` 157/157 GREEN (re-measured by this checkpoint's generator). The pins discriminate: on scratch
  copies, an empty TOOLKIT fails every pin but the E-65 guard, and each planted defect fails exactly its own pin.
- **CORRECTION (E-67).** The claim in the entry "C2 #e2 LANDED; token-transform audit fixed (E-66)" above that `_toolkit_selfcheck.py` (1784d851b5c6) runs
  `--artifacts-only` GREEN went stale when `strategy_plan_Dan.json` was placed: that pre-image gives 155/157 on the
  current tree. It is superseded by the figures here; the older entry is left as written (amend, never edit).
- **E-67 recorded** in the M8 ledger (8a9b0b431b35, 2,983 lines): a smoke run of `check_brief_vs_suite.py` on
  Ezekiel's brief wrote a Daniel-named report into SP (moved to scratch evidence; the tool, 2a37dd83f84e, now writes
  only for a brief inside SP/Dan, and its `--selftest` exits 0). Cures: read a tool's write sites before smoke-running
  it in SP; run tools on foreign inputs only from scratch copies; re-run every gate that scans a directory after
  placing a file into it.
- **Receipt.** `dan_toolkit_a1#e1` appended (receipts e461d5a65e72, 27 rows): "LANDED - Daniel TOOLKIT.md written
  and pinned; Phase 0 closes when the two blind toolkit review lanes land".
- CURSOR: phase = DAN_PHASE0_TOOLKIT_PLACED_REVIEW_LANES_NEXT.

## 2026-09-28 - K1 and K2 (blind toolkit review lanes) IN FLIGHT; learning rows and DAD E-66/E-67 done

- **Launched** on claude-opus-5-5, both at 2026-09-29T03:29:01Z: `dan_toolkit_review_k1_a1#e1` (by the bytes) and
  `dan_toolkit_review_k2_a1#e1` (by the code; runs no pinned file). E-62 MATCH and the workspace validator passed
  before launch. `phase0_lanes/build_launch.py` is at 0447c396af9c (pre copy `.pre_a776a1e6d188`);
  `append_launch_row.py` at b50fd297291b (pre copy `.pre_07d35b01e93c`). Receipts b3644bbbd828 (29 rows; rows 28
  and 29 are the two launch rows).
- **E-41 hold.** Until both land, do not modify TOOLKIT.md, the Dan data files, the 13 Dan tools K2 reads,
  `campaign/grader_models.v1.json` or the ledger lines the lanes pin.
- **Learning log** L-0080..L-0085 appended (D #e2, T2 #e2, T1 #e3 with E-66, S #e3, the reconciliation, TOOLKIT with
  E-67), drafted from the receipts and the ledger: e1af0177b423 (85 rows).
- **DAD ingest of E-66 and E-67 done** (session dad:session:ce4feb13): 2 candidate E records from ledger lines
  2817-2983 (8a9b0b431b35 pinned and unchanged), files 1902 to 1904, problems none, no marker allocated; postflight
  sent (lint CLEAR). Harness `Ezek/repair2/gen_dad_ingest_E66_E67.py` -> `dad_ingest_E66_E67.py`. Reindex and graph
  stay QUEUED. The next DAD delta is every ledger entry after E-67.
- The census `previous_executions` join and the unknown-token-field refusal stay OWED at the Daniel census port
  (trigger: before that port's first run).
- CURSOR: phase = DAN_PHASE0_K1_K2_IN_FLIGHT.

## 2026-09-29 - DANIEL PHASE 0 CLOSED: K1 and K2 landed and reconciled; suite fails closed (E-68); TOOLKIT corrected

- **Landed** (receipts ee123126c1c3, 31 rows; rows 30-31 are the completions): K1 by the bytes, fit_to_accept,
  0 DEFECTS (105 re-measurement checks, 0 failed); K2 by the code, not_fit, 13 DEFECTS (11 exact corrections,
  2 judgements), each confirmed by the orchestrator against the cited code lines.
- **Rulings on opus, to list for Fable (OW-28):** K2 D1 -> the suite fails closed: any ERROR member is HARD and is
  listed in `summary.dead_members`; K2 D2 -> the suite runs the normalizer once per review file and sums its counts;
  K1 flag 1 -> TOOLKIT line 13 now gives the owner's OW-28 words and labels the low/medium_low reading INFERRED.
- **Suite** `tools/run_validator_suite.py` 3760fd45d5a6 -> f5d1fc5a526c (pre copy `.pre_3760fd45d5a6`); scratch-only
  regression test 4/4 PASS. Sibling audit: 7 of 8 suites under M8 lack the rule; 0 of 115 recorded validator reports
  GREEN with a dead member. Closed books are not reopened.
- **TOOLKIT.md** d9bc3a0a17fb -> c05b81466651 (pre copy `.pre_d9bc3a0a17fb`), 13 fixes, every find matched once.
  `_toolkit_selfcheck.py` (3fe5e2e50e03) re-run after placement: GREEN 232/232 full and 157/157 `--artifacts-only`;
  both zone fixture tests exit 0.
- **Ledger E-68** appended: 102a4050c406 (3,036 lines). **Learning log** L-0086 and L-0087: d5f9cd458cd6 (87 rows).
- **Noted, not changed:** `dan_stage_report.json` records `verse_inventory.json` at 356f4427..., while the pinned file
  is de3dcac0f464 (K1). `--reviews` with several files for web_quotes, universals and language_zones is not exercised.
- **OWED:** the DAD ingest of E-68 (the next delta is every ledger entry after E-67); at the Daniel census port, the
  `previous_executions` join and the unknown-token-field refusal (trigger: before that port's first run).
- CURSOR: phase = DAN_PHASE0_CLOSED.

## 2026-09-29 - DANIEL WRITER WAVE LAUNCHED: six parts W1-W6 on claude-opus-5-5 (OW-25), RUNNING

- **Launched** 2026-09-29T04:03:50Z: attempts dan_writer_W1_a1..dan_writer_W6_a1, execution #e1 each; receipts `Dan/dan_writer_attempt_receipts.jsonl` 5fa23328049d (6 launch rows, all RUNNING). Briefs: W1 101f6f16f38e, W2 c48eef4a7026, W3 4c02349908ff, W4 e9d8e2dbf951, W5 13af24a73a93, W6 d0d20a4f3a9a.
- **Tooling** in `Dan/writer_lanes/`: BRIEF_W.template.md 33e8d8b40da3, build_writer_launch.py 38c0c04a0a3f, _validate_writer_part_dan.py 7d9415df76bd, append_launch_row.py 9483e2f834cb, append_landing_row.py 3fabcc95b0d6. Every brief and message MATCHed _brief_pin_check and _launch_message_check --book Dan (E-62); workspace validator pass before launch.
- **Writers run** check_tiling, the suite and _validate_writer_part_dan.py only on private copies in OUT\work, with PYTHONDONTWRITEBYTECODE=1 and -B. At landing re-list Dan/tools/__pycache__: baseline 3 pre-existing files.
- **Pinned while running:** the Daniel face files, the tools, TOOLKIT, strategy, plan, grader_models and the ledger (COMMON). No ledger append until every writer lands (E-41).
- CURSOR: phase = DAN_WRITER_WAVE_RUNNING.

## 2026-09-29 - DANIEL WRITER #e1 x6 LANDED FAILED (session limit); #e2 x6 RELAUNCHED, RUNNING

- **#e1 landed** FAILED_BY_API_SESSION_LIMIT for all six parts, no deliverable; W3-W6 partial work files moved unchanged to scratch dan_w/residue/W<n>_e1 (digests in each landing row); residue .py files name no directory-listing call; Dan/tools/__pycache__ unchanged. Reported to the owner, who reported the limit reset and said to continue.
- **#e2 launched** 2026-09-29T08:04:47Z: receipts `Dan/dan_writer_attempt_receipts.jsonl` 719d7a58e7bb (18 rows: 6 launch #e1, 6 FAILED landings, 6 launch #e2 RUNNING). Briefs: W1 44488a774d08, W2 af68bf37dc55, W3 f92dded7bb88, W4 b3810f127321, W5 8829b081d982, W6 0bae9107d531.
- **Tooling** in `Dan/writer_lanes/`: BRIEF_W.template.md 33e8d8b40da3, build_writer_launch.py 38c0c04a0a3f, _validate_writer_part_dan.py 7d9415df76bd, append_launch_row.py 9483e2f834cb, append_landing_row.py 3fabcc95b0d6. Every brief and message MATCHed _brief_pin_check and _launch_message_check --book Dan (E-62); workspace validator pass before launch.
- **Writers run** check_tiling, the suite and _validate_writer_part_dan.py only on private copies in OUT\work, with PYTHONDONTWRITEBYTECODE=1 and -B. At landing re-list Dan/tools/__pycache__: baseline 3 pre-existing files.
- **Pinned while running:** the Daniel face files, the tools, TOOLKIT, strategy, plan, grader_models and the ledger (COMMON). No ledger append until every writer lands (E-41).
- CURSOR: phase = DAN_WRITER_WAVE_E2_RUNNING.

## 2026-09-29 - DANIEL WRITER #e2 x6 LANDED FAILED (session limit again); #e3 WAVE A (W1-W3) RUNNING

- **#e2 landed** FAILED_BY_API_SESSION_LIMIT for all six parts; partial work moved unchanged to scratch dan_w/residue/W<n>_e2 (digests in each landing row). W4 had left an UNFINISHED W4_rows.jsonl in OUT; it was never reported and is NOT ACCEPTED (residue only). Residue .py files name no directory-listing call. The landing script first refused W4 on a list-order bug in its own move check (no row written, files intact); fixed and resumed, and the W4 row says its census was taken in residue.
- **Owner** reported the limit reset and said to continue.
- **#e3 in waves of three** so a limit stop loses at most three lanes' in-flight work. Wave A W1-W3 launched 2026-09-29T13:17:01Z; receipts `Dan/dan_writer_attempt_receipts.jsonl` 2cfd5a787975 (27 rows: 6 launch #e1, 6 FAILED, 6 launch #e2, 6 FAILED, 3 launch #e3 RUNNING). Wave B W4-W6: briefs and messages built and MATCHed, NOT launched (messages W4 bf777857be47, W5 c0b2919b0d02, W6 9060fbcbd904). Briefs: W1 8afbee8b3fba, W2 26ef1e26349b, W3 318133252254, W4 d223d9e324f6, W5 9bac1cd8169c, W6 417e44125eed.
- **Pinned while running:** the Daniel face files, the tools, TOOLKIT, strategy, plan, grader_models and the ledger (COMMON). No ledger append until every writer lands (E-41).
- CURSOR: phase = DAN_WRITER_E3_WAVE_A_RUNNING.

## 2026-09-29 - DANIEL WRITER #e3 ROLLING (at most three in flight); receipts 958e8c706f64

- **#e1 and #e2** landed FAILED_BY_API_SESSION_LIMIT for all six parts; partial work moved unchanged to scratch dan_w/residue/W<n>_e1 and W<n>_e2. W4 #e2 left an UNFINISHED W4_rows.jsonl, NOT ACCEPTED (residue only). The #e2 landing script first refused W4 on a list-order bug in its own move check (no row written, files intact); fixed and resumed. Owner reported the limit reset and said to continue.
- **#e3 state:** W1 COMPLETED; W2 RUNNING since 2026-09-29T13:17:01Z; W3 RUNNING since 2026-09-29T13:17:01Z; W4 RUNNING since 2026-09-29T13:24:38Z; W5 BUILT, NOT LAUNCHED; W6 BUILT, NOT LAUNCHED. Receipts `Dan/dan_writer_attempt_receipts.jsonl` 958e8c706f64 (29 rows). A new lane launches when one lands, keeping at most three in flight.
- **Briefs** W1 8afbee8b3fba, W2 26ef1e26349b, W3 318133252254, W4 d223d9e324f6, W5 9bac1cd8169c, W6 417e44125eed; **messages** (scratch dan_w) W1 a8219652a09e, W2 f75ef3cbdf7a, W3 dabd7618903a, W4 bf777857be47, W5 c0b2919b0d02, W6 9060fbcbd904, all MATCHed E-62 checks.
- **Pinned while running:** the Daniel face files, the tools, TOOLKIT, strategy, plan, grader_models and the ledger (COMMON). No ledger append until every writer lands (E-41).
- CURSOR: phase = DAN_WRITER_E3_ROLLING.

## 2026-09-30 - DANIEL: writers landed, S1, E1, tool fixes, FIXUP-1 applied, triage; controlling E2 RUNNING; review receipts 3319fc8bf0c9

- **Writers #e3:** all six parts COMPLETED (writer receipts 1f726d0cd312); combined and installed into SP/Dan/writer/ (draft_rows_combined.jsonl 693e468fd4b1).
- **Review lanes (latest landing per execution):** dan_writer_wave_spot_review_s1_a1#e1 FAILED_BY_API_SESSION_LIMIT; dan_writer_wave_spot_review_s1_a1#e2 COMPLETED; dan_controlling_rulings_a1#e1 FAILED_STOPPED_BY_ORCHESTRATOR; dan_controlling_rulings_a1#e2 FAILED_HARD_STOP_PINNED_INPUT_DIGEST_MIS; dan_controlling_rulings_a1#e3 COMPLETED;; dan_fixup1_W4_a1#e1 LANDED; dan_fixup1_W6_a1#e1 LANDED; dan_fixup1_W1_a1#e1 LANDED; dan_fixup1_W2_a1#e1 LANDED; dan_controlling_rulings_a2#e1 RUNNING.
- **Tool fixes installed by receipt:** S1-02, S1-07, S1-08+U-QUOTE-LABEL (evidence SP/Dan/review/tool_fixes/). S1-08 is FLAG/WARN tier only; its first draft of paseq_false_presence flagged an absence statement ('no paseq at 8:27') and the negation guard was added before install (fixture covers it).
- **FIXUP-1** W1, W2, W4, W6 landed and applied: SP/Dan/fixup/draft_rows_fixup1_applied.jsonl 2b92198c74bf; suite on a scratch copy hard GREEN, no dead member.
- **Triage** of all 138 post-S1-08 flags: {"REG:neither": 64, "REG:tool_false_positive": 5, "UNI:row_defect": 1, "UNI:tool_false_positive": 67, "WEB:row_defect": 1}; installed with the CWO-03 dispositions, coverage and suite report in SP/Dan/review/e2_evidence/ by an evidence_install receipt. Proposed row_defects: W6-001 missing web:Dan.10.2 beside the S1-01 quote; W4-003 superlative. CWO-DAN-03 left 16 zone hits in W2 rows for a FIXUP-2 order.
- **Incidents (ledger candidates, not yet appended; E-41 while E2 is in flight):** the orchestrator ran the suite on an SP path and it wrote a report into SP (E-67 recurrence; contained to scratch, wrapper run_suite_scratch.py plus a regression test now mandatory); W2 wrote a build script outside OUT (scratch root, moved to evidence); W4's heredoc lost a backslash; the pin guard prints its verdict twice, which broke a shell comparison; check_register prints unpadded ids (W4-1), INFERRED cause of W4's REPORTED 4/0 register count vs 69 MEASURED; the checkpoint re-used cursor DAN_WRITER_E3_ROLLING, so CYCLE_STATE fell behind while the resume prompt advanced.
- **Pinned while E2 runs:** its 24 brief inputs including the applied rows, E1, the e2_evidence files, strategy, TOOLKIT and the ledger. No ledger append until E2 lands (E-41).
- OWNER RULING 2026-09-29 (ledger OW-32): after Daniel the stress-first queue: 1 Corinthians, John, Romans, Revelation, Hebrews, Matthew (NT, gated on the Greek substrate from the separate session; if late take the first OT book in the queue not closed), then Genesis, Isaiah, Daniel, Deuteronomy, Acts, Job, Mark, Luke, Galatians, Exodus, Jeremiah, Psalms, 1 Peter, Ephesians, Colossians, Proverbs, 1 John, Zechariah, Ecclesiastes. Closed books' stress passages are audited when the queue reaches them. Re-read AI_FRONT_DOOR.md and .ai/control before each book.
- CURSOR: phase = DAN_CTL_E2_RUNNING.

## 2026-09-30 - DANIEL: controlling E2 LANDED; FIXUP-2 opened on W2/W4/W6; review receipts f386878adfe8

- **E2** dan_controlling_rulings_a2#e1 COMPLETED;: 12/12 rulings installed byte-identical as SP/Dan/review/dan_controlling_agent_rulings_E2.v1.json (43ae72e748fe). Gate: fixup2_may_launch true, parts ["W2", "W4", "W6"], 8 s2_conditions (E1's seven amended to eight), primaries_may_launch false.
- **Correction to the previous entry:** its register-id sentence is REFUTED by E2 (REGISTER-ID rejected: the rows' writer_decision_id values are themselves unpadded and the tool prints that field). The cause of W4's REPORTED register count gap is UNKNOWN and does not gate.
- **Ledger:** E-70 (orchestrator: E-67 recurrence, re-used checkpoint cursor, wrong inference in a queue) and E-71 (FIXUP-1 lane and tool-fix gaps) appended; ledger 7357c65c1b7e. New control: scratch check_cycle_state_fresh.py must print FRESH after every checkpoint.
- **Still OWED as ledger candidates, source not yet re-read (E-59):** the heredoc-then-ls E-19 pattern, W6's verse_map read, the book-wide-only ngram7 gate, the cwo_sweep misclassification.
- OWNER RULING 2026-09-29 (ledger OW-32): after Daniel the stress-first queue: 1 Corinthians, John, Romans, Revelation, Hebrews, Matthew (NT, gated on the Greek substrate from the separate session; if late take the first OT book in the queue not closed), then Genesis, Isaiah, Daniel, Deuteronomy, Acts, Job, Mark, Luke, Galatians, Exodus, Jeremiah, Psalms, 1 Peter, Ephesians, Colossians, Proverbs, 1 John, Zechariah, Ecclesiastes. Closed books' stress passages are audited when the queue reaches them. Re-read AI_FRONT_DOOR.md and .ai/control before each book.
- CURSOR: phase = DAN_CTL_E2_LANDED.

## 2026-09-30 - DANIEL: FIXUP-2 landed, applied and closed; review receipts 963095c58d5a

- **FIXUP-2 lanes:** dan_fixup2_W2_a1#e1 LANDED; dan_fixup2_W4_a1#e1 LANDED; dan_fixup2_W6_a1#e1 LANDED. Lander land_fx2_dan.py reconstructs each licensed field from the pinned value plus E2's exact spans and requires equality; strays check (E-71) clean.
- **Applied:** SP/Dan/fixup/draft_rows_fixup2_applied.jsonl d731d8559d10; suite on a scratch copy {"hard_status": "GREEN", "nfd_hard_e01": false, "triage_flags": 137, "dead_members": []}. T-UNI-031 and T-WEB-001 gone; the one new register flag (artifact_referent 'the device inventory', from E2's verbatim W4-003 words) is tool_false_positive under the triage_s108 class rule; refs_mirror worklist +2 FAR_SIDE (Dan.7.2, Dan.7.7), 42 far-side citations.
- **CWO:** 01/02/04 at 0; CWO-DAN-03 124 hits, corrected counts {"plain": 61, "seam_pair": 57, "verse_only_read": 3, "other_book": 3} after E2's W6-013 relabel, zone 0. Close record, REGISTER-ID statement and copies in SP/Dan/review/fx2_close/ (evidence_install receipt); S1-09 routed to SP/Dan/fable_end_review/routed_items.v1.jsonl (OWED; no Fable call, OW-30).
- **Orchestrator slip (ledger candidate):** the W4 launch receipt carried a placeholder agent id and an unobserved launched_at. Contained by 1 launch_correction row (E-44 amend; true id EXTRACTED from the launch result, launched_at UNAVAILABLE with a MEASURED bracket). Control: record_fx2_launch.py refuses a non-agent id or a launched_at outside [-60s, 900s] of now (selftest passes); sibling audit of both Dan receipt files found no other row.
- **Still OWED as ledger candidates (E-59, draft from a fresh read):** the W4 receipt slip, the heredoc-then-ls E-19 pattern, W6's verse_map read, the book-wide-only ngram7 gate, the cwo_sweep misclassification.
- OWNER RULING 2026-09-29 (ledger OW-32): after Daniel the stress-first queue: 1 Corinthians, John, Romans, Revelation, Hebrews, Matthew (NT, gated on the Greek substrate from the separate session; if late take the first OT book in the queue not closed), then Genesis, Isaiah, Daniel, Deuteronomy, Acts, Job, Mark, Luke, Galatians, Exodus, Jeremiah, Psalms, 1 Peter, Ephesians, Colossians, Proverbs, 1 John, Zechariah, Ecclesiastes. Closed books' stress passages are audited when the queue reaches them. Re-read AI_FRONT_DOOR.md and .ai/control before each book.
- CURSOR: phase = DAN_FX2_APPLIED.
