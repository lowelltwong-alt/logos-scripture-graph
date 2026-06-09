# Workflow Lessons

Status: living control-plane lesson collector
Owner: methodology / roadmap governance
Last updated: 2026-06-09

This file collects reusable workflow lessons that apply across generated artifacts, control-plane
surfaces, boundary-source intake, and adjacent operational systems. It is not canonical Scripture
truth, not boundary corpus approval, and not authorization for output-changing work.

Expanded rule registry: see
[`LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md`](LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md) for rule
IDs, importance levels, enforcement notes, T327 root-cause lessons, and LawFirm transfer patterns.
This file remains the compact workflow lesson collector.

## How To Use This Collector

- Cite the relevant lesson in task handoffs when a task follows or updates one of these patterns.
- Update this file when a completed task exposes a reusable workflow rule that should survive the
  immediate PR.
- Keep implementation authority in the appropriate task, repo, and reviewed evidence surface.
- Do not use a lesson as a substitute for source review, owner authorization, tests, validation, or
  explicit downstream handoff.

## WORKFLOW-LESSON-001 - Generated Artifact Corrections Require Durable Generator + Gate

When a correction affects generated artifacts, ignored build outputs, derived evidence, chunks,
scores, sidecars, or workflow outputs, the correction is not durable merely because a local run
produced the right result.

The durable correction must live in committed generator behavior, committed policy/config,
fail-closed validation, CI regeneration, and task-scoped tests. If a downstream test fails because
the correction changes the corpus or baseline, that failure must be explicitly staged into the next
task with temporary quarantine or documented owner decision. Do not silently re-baseline in the wrong
task.

Applies to:

- Scripture canonical output regeneration.
- Chunk regeneration.
- Scorecard / leaderboard baseline resets.
- Boundary source intake.
- LawFirm exception-to-automation workflows.
- Agent harness outputs.
- Any system where generated artifacts are not committed as source truth.

## T327-LESSON-001 - Untracked Generated Outputs Move the Burden to Generator and CI

T327C showed that `data/canonical/**` can be intentionally gitignored generated output. In that
model, correctness cannot be reviewed by committed JSONL diffs. It must be reviewed through exact
regeneration command, committed generator flags, fail-closed scope validator, CI regeneration path,
DATA_MAP count deltas, protected-path checks, and explicit downstream fallout handoff.

If full pytest fails because downstream gold/chunk baselines still reflect the prior corpus, do not
silently re-baseline. Either quarantine exactly the known fallout with a task-bound xfail, or require
explicit owner decision to merge red. The next task must remove the quarantine and perform the real
re-baseline.

Outcome from T327:

- T327C corrected canonical generated outputs.
- T327D performed the real chunk/gold/score re-baseline.
- T327E cleaned residual eval/stress/review surfaces.
- T327F documented planning-only boundary intake controls.

## BOUNDARY-WORKFLOW-LESSON-001 - Boundary Source Intake Requires Planning, Authority Scope, and Owner Authorization

Boundary-source intake must begin as planning and control metadata, not corpus import. Listing a
source family as a future candidate does not approve source acquisition, normalization,
corpus-record creation, default retrieval, or canonical claim promotion.

Future boundary intake requires:

- Owner authorization.
- Source identity.
- License review.
- Provenance.
- Trust level.
- Tradition scope.
- Profile scope.
- Contamination controls.
- Retrieval-default policy.
- Explicit cross-repo contract with `logos-boundary-literature`.

Boundary material must not override, equal, contaminate, or silently reinterpret canonical Scripture
authority. `logos-scripture-graph` remains the canonical 66-book Scripture graph.

## BIBLE-CHUNKING-WORKFLOW-LESSON-001 - Bible-First Chunker Priority and Route Isolation

The canonical 66-book Bible chunker is the highest-priority chunking substrate. Future
noncanonical, boundary, commentary/reception, legal-document, or master-chunker adaptations must be
separate from and subordinate/non-superior to that priority.

The optimized post-T327 roadmap teaches structural primitives behind route-specific skills instead
of one global heuristic pile. Psalms are the current implementation lane because reviewed evidence
and a candidate-skill seam already exist. Revelation is likely a harder interpretive book and should
receive an early hard-book atlas/review-packet lane, but no Revelation implementation should begin
until reviewed gold exists.

If adapting the chunker for boundary or noncanonical material would degrade canonical Bible
chunking quality, split or rebuild a separate chunker/harness rather than compromising the Bible
chunker.

## LAW-FIRM-WORKFLOW-LESSON-001 - Exception-to-Action Requires Candidate, Gate, Ledger, and Scale Package

Operational exceptions, defect clusters, billing/portal/client-carrier deltas, and workflow failures
must first become normalized candidate records with root-cause tags, owner, risk, evidence, and
proposed action. They must not directly become automation, policy, or client-facing behavior.
Promotion requires validation gates, run ledger/audit evidence, approval where needed, and a scale
package.

This Scripture-side collector records the analogue because local LawFirm/FMG worktrees were present
but not safe to update in this PR: at least one candidate repo was on an unrelated branch, and other
candidate repos had untracked or modified local files. Cross-repo LawFirm/FMG updates should be a
separate, repo-scoped PR after selecting the authoritative repo and confirming a clean worktree.

## T327 Application Notes

- Generated canonical outputs were corrected by generator/config/CI validation, not by committing
  raw JSONL diffs as source truth.
- T327D was the correct task for chunk/gold/score re-baselining after the corpus-scope correction.
- T327E cleaned live eval/governance surfaces after the baseline reset.
- T327F kept boundary-source intake as planning/control metadata only.
- T327G remains separate and must not begin unless explicitly authorized.
