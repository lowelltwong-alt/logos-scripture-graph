# Task Handoff

## Task

- task_id: T487
- title: DAD transport 1.0.0 read-only spool cutover
- phase: phase_4
- status: complete_pending_merge

## Agent

- agent_name: codex
- mode: build
- stage: start
- updated_at: 2026-07-11T21:32:18+00:00
- handoff_id: cfc812fa55e2d87c

## Files read

- `.digital-asset/mail/outbox.jsonl` and every executable consumer
- DAD transport contract/schema, write-policy marker, mail ignore rules
- T442/T450/T472 and AI-agnostic Rust candidate-message validators

## Files changed

- Added the versioned read-only DAD contract and local transport validator.
- Moved 24 historical candidate envelopes to a count/hash-manifested test fixture.
- Removed the runtime outbox from Git while preserving optional generic runtime validation.
- Updated front-door, TOC, lesson-index, task, tests, and aggregate validator wiring.

## Decisions made

- Historical candidate rows are immutable test evidence, never runtime transport.
- Empty or absent runtime caches are valid; nonempty runtime envelopes remain strict.
- The rollout approval installs this cutover once and grants no standing DAD write authority.

## Validation run

- command: `python scripts/validate_all.py`
- result: passed after generated canonical sidecars were built
- command: `python -m pytest -q`
- result: 972 passed, 25 skipped
- command: focused transport/outbox/semantic validators and DAD schema validation
- result: passed; direct DAD detector classification `current`
- failures: initial aggregate run exposed two cutover references, both fixed; absent generated sidecars were rebuilt exactly as CI does

## Known risks

- The central DAD transport audit still points to the paused primary worktree until the branch merges and DAD receives a separate audit-control-path update.
- DAD journal fallback is due but the journal repo is not configured in the scheduled cycle.

## Open questions

- None for the repo cutover. Central mirror freshness and journal configuration remain DAD-side work.

## Next agent instruction

Merge the green T487 PR, refresh the central Scripture control mirror, point DAD transport auditing at that mirror without changing the live mail root, and verify the central report has zero `upgrade_required` rows.

---

## Handoff refresh: final

- agent_name: codex
- mode: build
- updated_at: 2026-07-11T21:52:22+00:00
- handoff_id: 6405942a775736ae
