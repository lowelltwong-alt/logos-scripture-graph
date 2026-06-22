---
object_type: audit_report
trust_zone: learning-sidecar
lifecycle_status: active
provenance_note: "Created 2026-06-22 during T388 branch cleanup after PR #104 was merged and live main was confirmed clean."
reason_for_inclusion: "Preserve rediscovery instructions for stale branch signals before deleting or retiring unnecessary branches."
---

# T388 Legacy Branch Discovery Audit

## Review Target

- Reviewer: Codex
- Date: 2026-06-22
- Repo: logos-scripture-graph
- Branch: codex/legacy-branch-discovery-audit
- Base: main at 2c7b0d2
- PR: pending
- Task id: T388

## Verdict

- Verdict: stale branch signals should be preserved as audit memory, not merged directly.
- Merge recommendation: merge this audit note only.
- Owner decision required: no, unless a future task wants to promote candidate data, alter graph behavior, import boundary material, or change governance policy.

## Branch Findings

### feat/scale-connection-discovery-codex-5-5

This branch is an old alternate T308 connection-discovery candidate run from 2026-06-05.
It has one unmerged commit, `97a4bac Scale connection discovery candidates`, and a remote branch.

Do not merge it directly.

Reasons:

- It predates later canonical 66-book cleanup and current control-plane guardrails.
- Its diff against current main is a stale snapshot that would delete many current governance,
  audit, task, roadmap, test, and validation files if merged.
- It modifies `data/candidate/connections/codex-5.5-2026-06-05.jsonl` and the corresponding
  manifest, but current main already has a later/cleaner 500-candidate file for the same named run.
- Prior inspection found the old branch file contains 249 records, with 150 overlapping current
  main, 99 unique stale candidates, and 350 current-main candidates absent from the branch.
- The old branch report includes wider/pre-T327 context, including deuterocanonical references.

When to rediscover:

- During a future T308-style connection-discovery adjudication, rerun, or candidate-batch comparison.
- Only as historical candidate signal, not as graph truth, retrieval truth, canonical Scripture
  evidence, or preferred intertext.
- The right rediscovery action is to rerun current discovery code against current canonical 66-book
  data and compare any old 99-unique signal as candidate-only evidence.

Cleanup decision:

- Delete the local and remote branch after this audit note is safely merged or otherwise preserved.

### t320-t325-boundary-entity-commentary-planning-pack

This branch is a local-only planning branch with three commits:

- `cbe53f8 T320/T325: add entity, boundary, commentary, and score planning`
- `32dfd81 T326: add raw source marker risk discovery plan`
- `1706ab1 T326: integrate raw marker red-team findings`

Do not merge it directly.

Reasons:

- It is a stale pre-T327 planning snapshot and would delete many current control-plane files if
  merged.
- Its useful commentary/reception placement ideas are now mostly superseded by current
  `boundary_material_routing`, `boundary_source_intake_plan`, T327F, T382, T383, T386, T387, and
  the live `logos-boundary-literature` repo direction.
- Its raw marker risk ideas overlap with later source-metadata, contextual reading, original
  language, WJ, textual-variant, coverage, and readiness controls.
- Its added files are valuable historical planning inputs, not current authority.

Potentially useful files to rediscover later:

- `docs/roadmap/T321_BOUNDARY_TEXTS_AND_HETERODOXY_CONTROLS.md`
- `docs/roadmap/T323_BOUNDARY_LITERATURE_REPO_SCAFFOLD_PLAN.md`
- `docs/roadmap/T325_COMMENTARY_AND_RECEPTION_LAYER_PLAN.md`
- `docs/roadmap/T326_RAW_SOURCE_MARKER_RISK_DISCOVERY.md`
- `.ai/handoffs/T320_T325/handoff.md`
- `.ai/handoffs/T326/handoff.md`
- `.ai/tasks/T320_T325.task.yaml`
- `.ai/tasks/T326.task.yaml`

When to rediscover:

- During future Boundary Literature source-intake planning, commentary/reception schema planning,
  or source-marker risk review.
- During future Doctrine Genealogy planning only for routing lessons, not as doctrine authority.
- During future chunking/source-marker work only after reading current T382/T383/T386/T387 and
  current source-metadata/textual-critical policies.

Cleanup decision:

- Keep the local-only branch until this audit note is merged to main, because it is the only full
  pointer to those old files.
- After merge, delete it as superseded historical planning. Do not push it or open a direct PR from it.

## Non-Authorization Check

- raw/canonical mutation: none
- generated chunks: none
- evaluator/leaderboard: none
- reviewed gold: none
- implementation: none
- graph/vector/index: none
- boundary import: none
- source metadata authority: none

## Next Action

- Merge the T388 audit PR.
- Then delete `feat/scale-connection-discovery-codex-5-5` locally/remotely if still present.
- Then delete local `t320-t325-boundary-entity-commentary-planning-pack` after confirming the audit
  note is on main.
