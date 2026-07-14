# Task Handoff

## Task

- task_id: T498
- title: Canonical changed-path engine core
- phase: phase_9
- status: complete_pending_merge

## Agent

- agent_name: Codex
- mode: tooling
- stage: start
- updated_at: 2026-07-13T15:25:40+00:00
- handoff_id: 70d5be4a5d1013b3

## Files read

- Required front door, master context, project status, T497 owner decisions, Fable O2 specification, runtime preflight, DAD asset/skill guidance, and existing task-scope Git logic.

## Files changed

- Additive root `logos_validation` package, versioned JSON schema, technical documentation, fixture repositories/tests, task/status/roadmap records, and DAD preflight evidence.
- No existing validator, hook, CI job, or consumer changed.

## Decisions made

- Used a root package because this repository has no `src/` import layout and runs modules directly from the repository root.
- Kept all four layers independent and made profile selection control only the union.
- Required explicit `--no-fetch --allow-stale`; all other base resolution fetches and fails closed.
- Shallow fetches update the exact remote-tracking ref before bounded deepening.
- Python remains the reference because Git subprocess latency dominates; Rust is deferred pending consumer profiling.

## Validation run

- command: `python -m pytest tests/test_changed_paths.py -q`
- result: 27 passed in 33.67 seconds on the final source; the 18-test baseline was 64.65 seconds and immutable shallow-remote reuse reduced repeated setup while later regressions expanded coverage.
- command: `python scripts/validate_all.py`
- result: passed on final source in 194.6 seconds.
- command: `python -m pytest -q`
- result: 1046 passed on final source in 658.69 seconds.
- failures: Initial shallow test proved plain fetch populated only FETCH_HEAD; fixed with an explicit remote-tracking refspec. An initial aggregate run exposed a missing directory-prefix scope declaration. A full-suite nested aggregate first exited -1, then exposed content-identical validator line-ending/stat noise in two unrelated catalog files; both blobs matched HEAD, were refreshed without staged deltas, the isolated nested test passed, and the final full run passed cleanly.
- GitHub CI failure: the new output schema made generated `.ai/control/DATA_MAP.md` stale (schema count 33 to 34 and one schema row). Added only that generated map to task scope, preserved the CI-proven two-line semantic delta, reran the workflow's canonical ingest, and confirmed `python scripts/generate_data_map.py --check`, task scope, and parallel safety all pass.
- GitHub CI portability failure: run `29277008930` used Git 2.54 and failed only `test_shallow_clone_deepens_until_merge_base` because the explicit base refspec deepened `origin/main` without deepening the checked-out feature tip. The approved correction requests the already-validated exact `HEAD` object alongside the base during each bounded deepen round; it creates no temporary ref and preserves fail-closed behavior.
- command: `python -m pytest tests/test_changed_paths.py -q`
- result after the CI correction: 27 passed in 63.69 seconds.
- command: Linux Git 2.43 manual shallow fixture using the patched CLI
- result: merge-base resolved with `method=deepened`, union was exactly `feature.txt`, `HEAD^` materialized, and the repository became unshallow.
- command: `python scripts/validate_task_scope.py --task-id T498`
- result: passed. The untargeted command selected legacy current-focus task T475 and was rejected as non-authoritative for T498.
- command: `python scripts/validate_all.py`
- result after the CI correction: all gates passed in 169.7 seconds.
- command: `python -m pytest -q`
- result after corrected temp routing: 1021 passed, 25 skipped in 542.44 seconds.
- environment note: the first full rerun used a deep repository-local TMP path and produced four false negatives from Windows path length and a T441 repository-relative build-output guard. All four passed under short external `C:\\tmp\\t498-focused`; the complete suite then passed under `C:\\tmp\\t498-full`. The failed run is environment evidence, not hidden validation.

## Known risks

- Later consumers could ignore a non-null `fail`; every migration must treat it as exit-2 validation failure.
- Git path names with invalid UTF-8 fail closed because the JSON contract requires interoperable Unicode strings; byte-exact path support is not claimed.
- Rename/copy paths are both listed, which may require consumer deduplication during shadow migration.
- A shallow remote that refuses the exact `HEAD` object request cannot be repaired safely; the fetch returns a machine-readable failure rather than silently using incomplete ancestry.

## Open questions

- No open architecture question in LSG-O2A. Consumer order and parity periods remain owned by LSG-O2B.
- No chunking lesson-index change: the reusable shallow-ref rule is encoded in the engine, regression tests, technical documentation, and DAD postflight candidate; it is not required chunking preflight before O2B adoption.

## Next agent instruction

Publish the additive PR, verify GitHub checks and protected review, merge, then start LSG-O3A as the next separate kernel PR.

## Review lanes

- Red-team/premortem checklist: passed. Checked option/refspec injection, missing and ambiguous bases, fetch failure, no merge-base, shallow exhaustion, invalid UTF-8 failure, stale-base opt-in, rename dual paths, consumer misuse of non-null failure, and rollback. Residual: callers must supply task scope rules to classify `out_of_scope_dirty` and later O2B migrations must prove parity before cutover.
- Lesson/asset/harness checklist: the engine, schema, golden fixture, and Git integration matrix are a concrete reusable local asset, but cross-repo adoption is unproven; keep it repository-local and candidate-only until O2B demonstrates consumers and parity.
- Learning-loop checklist: explicit remote-tracking refspec fixed the shallow-clone surprise; the regression changed the observable result from two shallow failures to passing success/exhaustion cases. Directory-level untracked scope and content-identical validator rewrites are recorded as workflow limits, not authority changes.
- CI-correction learning-loop checklist: Git 2.54 demonstrated that an explicit base refspec may deepen only the requested base; the fix now carries the exact verified `HEAD` object as a second fetch source and the regression asserts both the call contract and materialized parent. Final closure requires the fresh GitHub Git 2.54 run to pass. Short external Windows temp paths avoid both `MAX_PATH` expansion and repository-relative temp misclassification.
- Digital-asset pattern checklist: deduplicated against DAD preflight offerings; no narrower reviewed changed-path engine existed and no Rust asset was adopted without profiling.
- Conversation/prompt checklist: T498 stores only the approved technical contract and privacy-safe evidence; it does not copy raw conversation or Fable reasoning into DAD.

---

## Handoff refresh: final

- agent_name: Codex
- mode: tooling
- updated_at: 2026-07-13T18:55:16+00:00
- handoff_id: 9b29c12d2a183ea7

---

## Handoff refresh: start

- agent_name: Codex
- mode: tooling
- updated_at: 2026-07-13T19:18:11+00:00
- handoff_id: 70d5be4a5d1013b3

---

## Handoff refresh: final

- agent_name: Codex
- mode: tooling
- updated_at: 2026-07-13T19:40:34+00:00
- handoff_id: 9b29c12d2a183ea7
