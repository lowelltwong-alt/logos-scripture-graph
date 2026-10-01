# T610 Blind Design A — Public AI/MCP Entry and PR 194

## Review Target

- Reviewer: Sol/high blind lane A
- Date: 2026-08-18
- Repo: `lowelltwong-alt/logos-scripture-graph`
- Branch inspected: `origin/main`, `scratch/t423-m7-sol`, `scratch/t423-m8-fable`
- PR: `#194`
- Task id: `T610`
- Committed frozen brief core:
  [`20260818-T610-public-entry-frozen-brief.md`](20260818-T610-public-entry-frozen-brief.md)
- Committed core SHA-256: `42bea86a4125f75942486da94bcc52fd35e7eed0ff0339be2081d83fda48aafc`

## Verdict

- Verdict: hold PR 194; publish a small clean-main orientation PR first
- Merge recommendation: do not merge PR 194 as one unit
- Owner decision required: only if replacement refs would later be closed, deleted, or promoted

## Design

1. Put a concise public orientation at the top of `AI_FRONT_DOOR.md` and route deeper
   detail to one public overview.
2. Separate current capabilities from planned graph, retrieval, runtime, and remote MCP
   capabilities.
3. Define release Bronze/Silver/Gold separately from chunking reviewed-gold.
4. Preserve M7 and M8 as independent, immutable candidate releases with exact hashes,
   manifests, limitations, and audit receipts.
5. Land a small convergence/index PR after the candidates are published. Close PR 194
   as superseded only after all valuable commits are durable and linked.

Owner sequencing clarification after the blind review: M8 remains active under Fable and
its subagents. “Convergence” here is a future architecture stage, not completed M7/M8
analysis; no M7/M8 content comparison begins until M8 is complete.

## Key Evidence

- PR 194 is conflict-reported, review-required, has no checks, and contains 5,923 files
  with more than 1.2 million added lines.
- M7 has contradictory aggregate and corrective-review status surfaces; neither should
  be silently selected as the release truth.
- M8 is an active, clean, owner-bound 19/66 checkpoint and should not be rewritten by
  an integration task.
- The repository declares local stdio read-only MCP only. Remote MCP and writes are off.

## Non-Authorization Check

- raw/canonical mutation: not authorized
- generated chunks: candidate publication only; no production promotion
- evaluator/leaderboard: not changed
- reviewed gold: not changed
- implementation: documentation and release routing only
- graph/vector/index: not authorized as truth
- boundary import: not authorized
- source metadata authority: not changed

## Independence Note

Lane A was blind to lane B's output and made no repository writes. Both lanes used the
same Sol capability tier and runtime family, so this is independent-context A/B review,
not cross-provider diversity.
