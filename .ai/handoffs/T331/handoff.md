# Task Handoff

## Task

- task_id: T331
- title: Post-T327 Chunking Backlog Reset
- phase: phase_4
- status: complete

## Agent

- agent_name: codex
- mode: planning-reporting
- stage: final
- updated_at: 2026-06-09T03:36:02+00:00
- handoff_id: 96b4d5b5f0a739e2

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- ROADMAP_STATE.yaml
- docs/roadmap/T330_CANONICAL_CORPUS_QA.md
- scripts/qa_canonical_corpus.py
- eval/LEADERBOARD.md
- .ai/control/roadmap_events.jsonl

## Files changed

- docs/roadmap/T331_POST_T327_CHUNKING_BACKLOG_RESET.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/tasks/T331.task.yaml
- .ai/handoffs/T331/handoff.md
- ROADMAP_STATE.yaml

## Decisions made

- Recorded the post-T327 canonical corpus baseline: 66 books, 31,103 passages, 31,103 witnesses.
- Recorded the T327D chunk baseline: 1,131 chunks, SHA-256
  `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`, and score 93.6 under
  unchanged T314 evaluator policy.
- Classified candidate future chunking work by value, risk, evidence, likely tests, gold needs, and
  likely touch surface.
- Recommended T332-T335 as the next planning/implementation sequence.
- Kept the task planning/reporting only.
- Did not start T327G.
- Did not import boundary texts or authorize source acquisition.

## Validation run

- command: `python scripts/validate_canonical_66_scope.py`
- result: passed; canonical 66 scope config validation passed.
- command: `python scripts/qa_canonical_corpus.py`
- result: passed; 66 books, 31,103 passages, 31,103 witnesses, 5 allowed empty textual-variant
  witnesses, 0 glossary entries, and 677,688 word tokens.
- command: `python -c "import yaml; yaml.safe_load(open('.ai/tasks/T331.task.yaml', encoding='utf-8')); yaml.safe_load(open('ROADMAP_STATE.yaml', encoding='utf-8')); print('YAML parse passed: .ai/tasks/T331.task.yaml, ROADMAP_STATE.yaml')"`
- result: passed.
- command: `git diff --check`
- result: passed; only a CRLF warning for `.ai/control/handoff_ledger.jsonl`.
- command: `python scripts/validate_all.py`
- result: passed; all validation gates passed, including handoff validation for 36 paths and
  canonical corpus QA.
- command: `python -m pytest -q`
- result: passed; `144 passed in 71.91s`.

## Known risks

- T331 does not select or implement a target; T332 must still choose a single narrow target.
- Future output-changing work still requires reviewed target gold and must not rely only on aggregate
  score movement.
- The post-T327 baseline must not be compared as if it were the same corpus as pre-T327 baselines.

## Open questions

- Which candidate has the safest first implementation surface after T327: Psalms/poetry stanza
  behavior is likely strongest, but T332 must decide explicitly.
- Whether T333 should be config-only, candidate-skill-only, or gold-first depending on T332.

## Next agent instruction

Proceed to T332 target selection only if this PR is created cleanly and `main` can be restored clean.
Do not merge PRs without owner instruction. Do not start T327G or boundary import.
