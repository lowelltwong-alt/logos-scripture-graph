# T318 Observed Stress Atlas Behavior Audit

Status: complete as diagnostic observation. No chunking implementation authorized.

## Purpose

T318 adds an observation-only layer over the T316 stress atlas. It records how current chunk output
touches each proposed stress case so future review packets can be selected from evidence instead of
from aggregate score pressure.

This is not reviewed gold, not an evaluator change, and not a chunking improvement claim.

## Confirmed

- Current official baseline remains D / Claude pass2 = 93.5 under T314 reviewed-structural-split
  evaluator policy.
- That score is evaluator-policy correction for unchanged output, not chunking improvement.
- T318 does not change chunk output.
- T318 does not change evaluator formula, leaderboard logic, raw/canonical data,
  chunker/orchestrator behavior, runtime skill code, or skill promotion.
- T318 does not mark any stress case as reviewed gold.

## Deliverables

- `eval/chunking_gold/stress_atlas/observed_stress_behavior.json`
- `eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`
- `tests/test_observed_stress_behavior.py`

## Observed Audit Summary

The audit covers every current T316/T316c stress-atlas case:

- stress cases audited: 44;
- fully contained in one current chunk: 16;
- split across current chunks: 25;
- mixed with extra context: 34;
- reviewed gold preserving current behavior: 2;
- pending review packet: 6;
- needs review packet: 25;
- variant-policy required: 2;
- speaker-review required: 5;
- source-tradition review required: 3;
- unknown/manual investigation required: 1.

## Governance Boundary

Observed behavior is evidence triage only.

- `implementation_allowed` remains `false` for the audit root and every entry.
- Current chunk observations are not approved expected output.
- A fully contained case is not automatically good gold.
- A split case is not automatically bad fragmentation.
- Marker evidence such as `\wj`, `\qs`, `\sp`, paragraph markers, and `\b` is diagnostic evidence,
  not authority for speaker attribution, textual-critical status, theology, or boundaries.
- Textual-critical, source-tradition, speaker-attribution, theological, and canon/boundary-text
  decisions remain human-gated.

## Proposed Next Use

Use T318 to select narrow follow-up review work:

1. create or review packets for high-risk split/mixed textual-variant cases;
2. review speaker-boundary packets for John 3 and Matthew 5-7;
3. create review packets for long structured cases with no packet yet;
4. avoid output-changing work until reviewed gold explicitly authorizes it.

## Unknown

- Whether future observed audits should be regenerated automatically in CI.
- Whether broad marker-class cases should gain dedicated sampling manifests.
- Whether future review packets should consume observed audit entries directly or copy them into
  packet-local evidence sections.
