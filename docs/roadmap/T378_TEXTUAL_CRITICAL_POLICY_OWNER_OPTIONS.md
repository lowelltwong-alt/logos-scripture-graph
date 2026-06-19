---
object_type: roadmap_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-19 during T378 after T371 review found that the 1Cor.8.1-1Cor.10.33 parent-only evidence packet contains variant-sensitive footnotes."
reason_for_inclusion: "Document the owner textual-critical policy options needed before variant-sensitive reviewed-gold promotion can proceed."
---

# T378 Textual-Critical Policy Owner Options

T378 adds `.ai/control/textual_critical_policy_owner_options.yaml` as a non-authorizing owner
decision surface. It exists because T371 cannot faithfully promote the `1Cor.8.1-1Cor.10.33`
parent-only evidence packet while `1Cor.9.20` and `1Cor.10.9` remain variant-sensitive and no
project textual-critical policy has been selected.

## Recommendation

The recommended policy is `TCP-T378-B`: case-by-case owner policy before each variant-sensitive
promotion.

That path is most faithful for this project because it:

- refuses hidden source-tradition preference;
- refuses liberal-critical or anti-canonical defaults;
- avoids turning one denomination's textual policy into chunk authority;
- keeps canonical Scripture authority primary;
- allows non-variant-dependent boundaries to continue only after explicit owner confirmation.

## What T378 Does Not Authorize

T378 does not select a textual-critical policy, preferred reading, source-tradition preference,
canon-scope change, boundary import, reviewed gold, route behavior, evaluator behavior, graph edge,
retrieval truth, chunk boundary, vector work, or output change.

## Required Owner Decision Before T371 Promotion

Before T371 reviewed-gold promotion can continue, the owner must either:

- select `TCP-T378-B` or another textual-critical policy option; or
- explicitly hold variant-sensitive promotion and choose a different non-variant-sensitive route.

If `TCP-T378-B` is selected, the next T371 question can be narrowed to whether
`1Cor.8.1-1Cor.10.33` is a parent-only boundary whose reviewed-gold status does not depend on the
`1Cor.9.20` or `1Cor.10.9` readings.
