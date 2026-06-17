# Chunking Gold

Status: executable Psalm gold exists for settled T310 3b-gold cases; Ps.78 is now approved as a
parent whole-psalm unit with reviewed child structural chunks.

This directory is the landing zone for per-form chunking gold evidence. Output-changing chunking
skill work must cite a per-form gold file or manifest before claiming improvement.

## Current Baseline

- Current post-T327 canonical-66 corpus baseline: `D_claude_pass2_post_t327` = 93.6 under the
  unchanged T314 evaluator policy.
- Pre-T327 wider-corpus T314 evaluator-policy baseline: `D_claude_pass2` = 93.5.
- T311 book/chapter evaluator baseline: 93.0.
- Old evaluator baseline: 88.5.
- Provenance: T311 and T314 corrected evaluator policy; T327D resets the corpus baseline after T327C
  removed non-66 canonical outputs.
- Interpretation: evaluator corrections and corpus-scope resets are not chunking improvement.

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
  - Non-target poetry controls route-stable on monolith fallback: Song, Lam.
- Characterization-only cases:
  - None currently in the Psalm manifest.

T327D removed `PrMan` and `Ps151` from canonical controls because they are outside the
owner-approved 66-book corpus.

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

T343 adds a pending Revelation review packet:

- `eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md`

This packet is `pending_human_review` for `Rev.12.1-Rev.14.20`. T344 owner-selected
`REV-T344-E`, so the next allowed step is Revelation research/prep only until stronger governed
evidence exists. It records gold candidates and review questions only. It does not authorize
Revelation implementation, reviewed-gold promotion, output-changing work, route behavior,
evaluator changes, generated chunk regeneration, boundary import, T327G, embedding/index/edge
work, graph-edge generation, whole-Bible output-changing work, or Psalm candidate promotion.

## Marker-Sensitive Stress Cases

T316c adds proposed marker-sensitive stress-atlas cases for words-of-Jesus `\wj` spans, Selah
`\qs` spans, and related discourse/speaker-boundary passages.

These cases are proposed only. `\wj` and `\qs` are evidence to preserve and review, not authority to
approve speaker attribution, textual-critical status, or chunk boundaries.

## Observed Stress Behavior

T318 adds diagnostic current-behavior observations for every stress-atlas case:

- `eval/chunking_gold/stress_atlas/observed_stress_behavior.json`
- `eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`

These observations are triage evidence only. They do not promote stress cases to reviewed gold, do
not approve current output as expected output, do not change evaluator policy, and do not authorize
output-changing work. A future implementation must still pass through human review and reviewed
gold for the selected target behavior.

## Review Packet Index

T319 adds the review packet index and promotion queue:

- `eval/chunking_gold/review_packets/review_packet_index.json`
- `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md`

The index ties together existing review packets, reviewed Psalm manifest cases, and observed
stress-audit cases. It is diagnostic/control infrastructure only. Queue entries are review
candidates with `implementation_allowed: false`; they are not authorization for output-changing
work.
