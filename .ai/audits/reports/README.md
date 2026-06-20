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
