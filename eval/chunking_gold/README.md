# Chunking Gold

Status: executable Psalm gold exists for settled T310 3b-gold cases; Ps.78 is now approved as a
parent whole-psalm unit with reviewed child structural chunks.

This directory is the landing zone for per-form chunking gold evidence. Output-changing chunking
skill work must cite a per-form gold file or manifest before claiming improvement.

## Current Baseline

- Current T314 evaluator-policy baseline: `D_claude_pass2` = 93.5.
- T311 book/chapter evaluator baseline: 93.0.
- Old evaluator baseline: 88.5.
- Provenance: the same D / Claude pass2 chunk output was scored under all three evaluator surfaces.
- Interpretation: T311 and T314 corrected evaluator policy; neither improved chunk output.

## Current Executable Gold

- Psalm manifest: `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- Executable tests: `tests/test_chunker_gold.py`
- Manifest maturity validator: `scripts/validate_chunking_gold.py`
- Reviewed/settled Psalm cases:
  - Ps.23 as one whole-psalm chunk.
  - Ps.119 as 22 intentional sections, reported but not penalized as literal fragmentation.
  - Ps.78 as parent `Ps.78.1-72` with reviewed child chunks `Ps.78.1-69`, `Ps.78.70-71`,
    and `Ps.78.72`.
  - Ps.105 as reviewed `Ps.105.1-45` whole-psalm behavior.
  - Ps.106 as reviewed `Ps.106.1-48` whole-psalm behavior; `b` markers are evidence, not automatic
    split authority.
  - Short Psalm holdouts: Ps.1, Ps.8, Ps.100, Ps.117.
  - Real superscription source evidence for Ps.3 with no orphan title chunk.
  - Non-target poetry controls route-stable on monolith fallback: Song, Lam, PrMan, Ps151.
- Characterization-only cases:
  - None currently in the Psalm manifest.

## Manifest Convention

No formal repository-wide gold manifest schema is committed yet. Until one exists, each per-form
manifest or plan must state:

- target form and route/skill under test;
- passages or controls;
- expected chunk-boundary behavior;
- forbidden diffs;
- evaluator metric used and known risks;
- baseline run or scorecard provenance;
- reviewer or promotion status;
- whether each case is reviewed gold, characterization-only, pending human review, or approved
  structural split under a parent whole unit.

Do not treat characterization-only records as promoted expected boundaries. Promotion requires
explicit review and committed tests or manifests that name the accepted boundaries.
Reviewed parent/child structural split is not bad fragmentation by default.

T315 adds a lightweight semantic validator for per-form manifest maturity. It checks explicit
statuses, keeps characterization-only and pending-human-review cases from carrying promoted-output
flags, and requires approved parent/child structural split cases to name parent and child
boundaries.

## Proposed Stress Atlas

- Stress atlas overview: `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- Stress atlas cases: `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- Stress atlas tests: `tests/test_chunking_stress_atlas.py`

Stress atlas cases are `proposed` and have `implementation_allowed: false`. They are future review
candidates, not reviewed gold and not approved expected output. A stress case must become reviewed
gold, characterization-only evidence, or an explicit pending-human-review packet before it can drive
output-changing work.

## Review Packets

T316b converted five proposed stress-atlas cases into human-readable review packets:

- `eval/chunking_gold/review_packets/ps105_boundary_review.md`
- `eval/chunking_gold/review_packets/ps106_boundary_review.md`
- `eval/chunking_gold/review_packets/isa52_13_53_12_boundary_review.md`
- `eval/chunking_gold/review_packets/mark16_9_20_textual_variant_review.md`
- `eval/chunking_gold/review_packets/john7_53_8_11_textual_variant_review.md`

T317 promoted the Ps.105 and Ps.106 packets to reviewed whole-psalm gold. The Isaiah, Mark, and
John 7:53-8:11 packets remain `pending_human_review`; they are not reviewed gold, do not approve
expected output, and do not authorize output-changing work.

T317 also adds pending marker-sensitive review packets:

- `eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md`
- `eval/chunking_gold/review_packets/matt5_7_wj_discourse_review.md`

These packets are `pending_human_review`. `\wj` is evidence, not authority, and speaker attribution
requires human review before gold or output change.

## Marker-Sensitive Stress Cases

T316c adds proposed marker-sensitive stress-atlas cases for words-of-Jesus `\wj` spans, Selah
`\qs` spans, and related discourse/speaker-boundary passages.

These cases are proposed only. `\wj` and `\qs` are evidence to preserve and review, not authority to
approve speaker attribution, textual-critical status, or chunk boundaries.
