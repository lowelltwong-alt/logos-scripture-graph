# Audit Reports

Store durable no-context review, A/B-check, and red-team reports here.

Recommended filename:

```text
YYYYMMDD-<task-id>-<reviewer-or-agent>.md
```

Use `.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md`.

## Reports

- `20260617-T344-codex-post-merge.md` - Codex post-merge no-context audit report for PR #60 /
  T344 audit-harness readiness; records no P0-P2 findings and one stale-focus wording fix.
- `20260617-T344-HARN-012-codex-post-merge.md` - Codex post-merge no-context audit report for PR
  #62 / HARN-012 owner-selection-to-implementation gate readiness; records no findings and the
  remaining required owner selection.
- `20260617-T344-HARN-006-codex-post-merge.md` - Codex post-merge no-context audit report for PR
  #64 / HARN-006 source-metadata authority scanner readiness; records no findings and the
  remaining required owner selection.
- `20260620-T374-additive-parent-overlay.md` - No-context audit surface for the T374 output
  implementation; verifies one exact additive parent overlay, baseline-prefix identity,
  non-authorizations, validator coverage, and T375 review-only next route.
- `20260620-T375-post-pilot-review.md` - No-context audit review for the T375 post-pilot gate;
  records same-baseline/audit review, child spans not necessary now, and T376 owner lane selection
  as the next gate.
- `20260620-T382-chunking-lesson-index.md` - No-context audit surface for the T382 lesson-index
  governance task; records the tagged lesson TOC/graph, CD-058, validator coverage, and the
  non-authorizing boundary.
- `20260621-T383-contextual-reading-policy.md` - No-context audit surface for the T383 contextual
  reading policy; records layered context preflight, CD-059, LSN-011, validator coverage, no history
  repo creation, and non-authorizations.
- `20260621-T376-epistle-research-runway.md` - No-context audit surface for the T376-A epistle
  argument research runway; records CD-060, LSN-012, T384 as the next non-output-changing
  research/options route, and the boundary between research autonomy and authority autonomy.
- `20260621-T384-bible-wide-research-readiness.md` - No-context audit surface for the T384
  Bible-wide research/readiness synthesis; records CD-061, LSN-013, human decisions HDM-001 through
  HDM-007, blocked authority changes, T385 as the next owner packet, and the non-output-changing
  boundary.
- `20260622-T386-bible-verse-passage-coverage.md` - No-context audit surface for the T386
  Bible-wide verse/passage coverage gate; records CD-062, LSN-014, one coverage record for every
  canonical passage, coverage taxonomy, readiness matrix, gap register, human-review docket, T385
  as the next owner packet, the LSN-015 test-runtime preflight lesson, and the non-output-changing
  boundary.
- `20260622-T388-legacy-branch-discovery-audit.md` - Branch cleanup audit for stale
  `feat/scale-connection-discovery-codex-5-5` and local-only
  `t320-t325-boundary-entity-commentary-planning-pack`; records that neither branch should be
  merged directly and when their historical signal should be rediscovered.
- `20260623-T398-bible-wide-phase-one-research-synthesis.md` - T398 no-context audit surface for
  the Bible-wide phase-one research synthesis; records whole-corpus triage coverage, Goal 2
  focused-research prompts, T397 preservation, and the non-output-changing boundary.
- `20260624-T399-focused-bible-wide-research-queue.md` - T399 no-context audit surface for the
  Goal 2 focused Bible-wide research queue; records the scored candidate queue, owner-decision
  map, blocked variant/source-tradition statuses, T397 preservation, and the non-output-changing
  boundary.
- `20260624-T397-eph1-route-isolation-harness.md` - T397 no-context audit surface for the
  Eph.1.3-Eph.1.14 route-isolation harness; records executable non-target identity, exact-parent
  target, spillover denial, child-span denial, report-shape proof, and the future owner output-gate
  boundary.
- `20260625-T401-eph1-output-pilot.md` - T401 no-context audit surface for the exact
  Eph.1.3-Eph.1.14 output pilot; records one additive parent-only overlay, baseline/non-target byte
  identity, route-isolation proof, same-baseline metrics, CD-076/LSN-030, and the post-pilot stop
  before child spans or broader behavior.
- `20260625-T402-low-complexity-runway.md` - T402 no-context audit surface for the post-pilot
  review and whole-Bible low-complexity candidate runway; records one candidate per canonical book,
  status buckets, metadata evidence-only handling, CD-077/LSN-031, and the rule that
  low-complexity means review eligibility only.
- `20260818-T610-public-entry-design-a.md` and
  `20260818-T610-public-entry-design-b.md` - blind same-tier Sol/high architecture lanes for the
  public AI/MCP entry, M7/M8 publication boundary, and PR 194 replacement route. These are
  independent-context reviews, not a claim of provider diversity. Their exact shared input is
  committed as `20260818-T610-public-entry-frozen-brief.md` so outside reviewers can inspect and
  recompute the published core digest.
- `20260818-T610-public-entry-convergence.md` - blind-design convergence record adopting a
  clean-main entry PR, separate M7 publication, continued owner-bound M8 work, and an explicit
  stop before any M7/M8 content convergence until M8 is complete.
