# Task Handoff

## Task

- task_id: T610
- title: Public AI front door and PR 194 publication routing
- phase: phase_0
- status: complete_pending_merge

## Agent

- agent_name: Codex-root
- mode: build
- stage: final
- updated_at: 2026-08-18T16:50:14+00:00
- handoff_id: 586f45782256d8a5

## Files read

- Required workspace lifecycle policy, Windows adapter, active-worktree registry, and
  M8 owner resume/checkpoint protocol.
- `AI_FRONT_DOOR.md`, `.ai/control/MASTER_CONTEXT.md` read-only,
  `.ai/control/PROJECT_STATUS.md`, `ROADMAP.md`, `ROADMAP_STATE.yaml`, architecture,
  task-scope, handoff, audit, PR-lifecycle, cross-repo, DAD/LLOS, and MCP contracts.
- Local M7 and M8 hash-bound state, prior cleanup-task reports, and GitHub PR 194
  metadata/diff statistics.

## Files changed

- Public entry and orientation: `README.md`, `AI_FRONT_DOOR.md`,
  `AI_TABLE_OF_CONTENTS.md`, `docs/architecture/PUBLIC_PROJECT_OVERVIEW.md`.
- Release/governance status: `ROADMAP.md`, `ROADMAP_STATE.yaml`,
  `.ai/control/PROJECT_STATUS.md`, `.ai/control/current_focus.yaml`, and event ledgers.
- Review evidence: two blind T610 design reports, their architecture-convergence report,
  their committed frozen shared brief, and the audit index.
- Transparency and method: `docs/architecture/M7_SOL_AGENT_SYSTEM.md`, the new workflow
  lesson, and the refreshed portable-family manifest/catalog hashes.
- Task/handoff/security/test isolation: `.ai/tasks/T610.task.yaml`, this handoff,
  `SECURITY.md`, the negative release fixture, and
  `tests/test_t475_generated_transition_state.py`.

## Decisions made

- Do not merge or conflict-flatten PR 194 as one 5,923-file integration unit.
- Publish a small clean-main public entry first, then a reconciled M7 candidate while
  Fable continues M8. Do not start M7/M8 content comparison or convergence until M8 is
  complete.
- Keep M7's 66/66 aggregate versus 22/66 corrective-review contradiction visible and
  block release use until it is reconciled.
- Keep M8 active, owner-bound, and unmodified by T610.
- Describe current MCP as a local stdio read-only contract only; remote MCP and writes
  remain future, separately governed work.

## Validation run

- `python scripts/validate_all.py`: passed.
- `python -m pytest -q`: 1,110 passed, 55 skipped in 400.42 seconds.
- focused scripture-first family tests: 68 passed; family validator passed with 7
  controls, 14 formal specialist packs, 19 routed forms, and 31,103 passages.
- `python scripts/validate_task_scope.py --task-id T610`: passed.
- `python scripts/agent/validate_handoffs.py`: passed for all referenced handoffs.
- `git diff --cached --check`: passed.
- repository-wide privacy audit: reported inherited legacy-baseline review findings and
  oversized-file skips; it found no untracked candidates. An exact staged-patch scan
  found no credentials, private keys, personal Windows paths, email addresses, or
  secret-pattern values in added lines or changed path names.
- independent read-only checker: found one role-taxonomy/routing overclaim in the M7
  transparency document; the wording was corrected to distinguish formal specialist
  packs, campaign roles, evidence identities, expected book strategies, and actual
  per-decision execution. The checker then returned publication PASS conditional only on
  this final validation/handoff refresh.
- GitHub automated review: identified that the A/B brief digest could not be recalculated
  without the brief. Both lane contexts independently returned the same shared input;
  that exact core is now committed and hash-linked from both reports. The earlier
  report-only pre-dispatch digest is retained as history but is not used as audit proof.

## Known risks

- M7 remains a large dirty recovery-held local research lane with contradictory progress
  surfaces and known defective untracked artifacts. Its remote branch trails the local
  immutable head by eight commits; the newer committed snapshot also contains pytest
  scratch trees and personal local-path strings, so direct push is blocked pending a
  separate scrubbed, manifest-first publication task.
- M8 is an active 19/66 owner lane; later commits can make PR 194 metadata stale.
- PR 194 remains open and conflicting until replacement publication links are durable.
- The repository-wide privacy tool remains conservative on inherited baseline paths and
  skips oversized tracked files; T610's exact patch was separately checked and introduces
  no new flagged content.
- Generated canonical sidecars are absent in this clean worktree, so only the
  lifecycle-declared optional full-data gates were skipped; aggregate validation and the
  complete available test suite passed.

## Open questions

- Exact M7 reconciliation and candidate-release schema belong to the next separately
  scoped publication task.
- A remote MCP implementation repository and hosting/authentication design are not yet
  selected.

## Next agent instruction

Publish the exact T610 head, wait for required GitHub checks and review, re-read the head
SHA, and merge only if the unchanged head is conflict-free and green. Keep PR 194 open
and unmerged until durable scoped successors exist. Open M7 cleanup/publication as a
separate registered task and worktree; never edit or clean the recovery-held M7 checkout
or the Fable-owned M8 lane.

---

## Handoff refresh: final

- agent_name: Codex-root
- mode: build
- updated_at: 2026-08-18T16:50:14+00:00
- handoff_id: 586f45782256d8a5
