# Gold Coverage Inventory

Status: T315 inventory after T314 evaluator-policy merge.

This inventory distinguishes reviewed executable gold, reviewed parent/child structural splits,
non-target controls, uncovered areas, and proposed future gold. It records coverage only; it does
not authorize output-changing chunk work.

## Confirmed Reviewed Coverage

| Case | Gold status | Protects |
| --- | --- | --- |
| Ps.23 | `reviewed_gold` | Whole-psalm hard gate; Psalm 23 remains one chunk. |
| Ps.119 | `reviewed_gold` | Parent whole Psalm with 22 intentional acrostic/stanza child sections; not bad fragmentation. |
| Ps.1 | `reviewed_gold` | Short Psalm holdout remains one whole-psalm chunk. |
| Ps.8 | `reviewed_gold` | Short Psalm holdout remains one whole-psalm chunk. |
| Ps.100 | `reviewed_gold` | Short Psalm holdout remains one whole-psalm chunk. |
| Ps.117 | `reviewed_gold` | Short Psalm holdout remains one whole-psalm chunk. |
| Ps.3 superscription | `reviewed_gold` | Real `\d` source evidence exists; no orphan title/superscription chunk is emitted. |
| Ps.78 | `approved_structural_split_under_parent_whole_psalm` | Parent `Ps.78.1-72` with child chunks `Ps.78.1-69`, `Ps.78.70-71`, and `Ps.78.72`; not bad fragmentation when exact boundaries match. |
| Ps.105 | `reviewed_gold` | Current `Ps.105.1-45` whole-psalm chunk is approved; no output change. |
| Ps.106 | `reviewed_gold` | Current `Ps.106.1-48` whole-psalm chunk is approved; `b` markers are evidence, not automatic split authority. |
| Song | non-target control | Stays on `monolith-pass2-v1` fallback; not absorbed by Psalm route. |
| Lam | non-target control | Stays on `monolith-pass2-v1` fallback; not absorbed by Psalm route. |
| PrMan | non-target control | Stays on `monolith-pass2-v1` fallback; not absorbed by Psalm route. |
| Ps151 | non-target control | Stays on `monolith-pass2-v1` fallback; not absorbed by literal Book of Psalms route. |

Executable anchors:

- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `tests/test_chunker_gold.py`
- `tests/test_evaluate_chunks.py`
- `scripts/validate_chunking_gold.py`

## Confirmed Validator Coverage

T315 adds semantic manifest validation for `eval/chunking_gold/per_form/*_manifest.json`.

The validator checks:

- reviewed cases have explicit status;
- characterization-only and pending-human-review cases are not promoted expected output;
- pending-human-review cases do not carry output-authorizing flags;
- approved parent/child structural splits have an explicit parent unit and child boundaries;
- approved structural splits explicitly opt into reviewed split and not-bad-fragmentation semantics.

## Inferred Coverage Gaps

- Psalm coverage is focused on settled cases and one reviewed long-Psalm structural split, not a
  complete Psalm boundary atlas.
- Current gold protects the Psalm route and adjacent poetry controls; it does not yet validate
  prophecy, long discourse, Job speeches, Gospel pericopes, or Pauline argument sections.
- Psalm 119 is the strong parent/child precedent; Psalm 78 is a lighter reviewed case. More long
  poems need review before using the pattern as broad policy.

## Proposed Future Gold

| Candidate | Why it matters | Required gold before output change |
| --- | --- | --- |
| Ps.89 | Long royal/lament Psalm with structural turns. | Parent unit plus reviewed child boundary targets. |
| Ps.105 future child sections | Long historical Psalm; tests narrative-poetry compression if the approved whole-psalm behavior is revisited. | New human decision, exact child spans, and non-fragmentation diagnostics. |
| Ps.106 future child sections | Long historical confession Psalm with `b` marker evidence if the approved whole-psalm behavior is revisited. | New human decision, exact child spans, and merge/preserve rationale. |
| Ps.136 | Refrain-driven Psalm; tests repeated liturgical structure. | Refrain-aware boundary expectations. |
| Lamentations 1-4 | Acrostic poems outside literal Psalms. | Parent/child acrostic section gold and non-target route controls. |
| Proverbs 31:10-31 | Acrostic wisdom poem. | Poem-level and stanza-level boundary review. |
| Job speech | Speaker-label and discourse-unit preservation. | Reviewed speech spans and `\sp` evidence. |
| Prophetic oracle | Oracle/woe/vision boundaries. | Reviewed oracle units with marker/source evidence. |
| Gospel discourse | Long discourse/pericope structure. | Reviewed discourse spans and sentence/pericope controls. |
| Pauline argument section | Sustained argument chains. | Reviewed argument units and context-packet requirements. |

## T316 Proposed Stress Atlas

T316 adds a proposed-only stress atlas:

- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`

These cases are future review candidates. They are not reviewed gold, not approved expected output,
and not authorization for output-changing work.

## T316b Pending Review Packets

T316b created review packets for selected stress-atlas cases. T317 later promoted Ps.105 and
Ps.106 to reviewed whole-psalm gold; the other T316b packets remain pending.

| Case | Packet | Status | Current behavior summary |
| --- | --- | --- | --- |
| Ps.105 | `eval/chunking_gold/review_packets/ps105_boundary_review.md` | `reviewed_gold` | Current output keeps the whole psalm as one chunk; approved by human review. |
| Ps.106 | `eval/chunking_gold/review_packets/ps106_boundary_review.md` | `reviewed_gold` | Current output keeps the whole psalm as one chunk; `b` markers are evidence, not automatic split authority. |
| Isa.52.13-53.12 | `eval/chunking_gold/review_packets/isa52_13_53_12_boundary_review.md` | `pending_human_review` | Current output embeds the cross-chapter target in a larger Isaiah chunk. |
| Mark.16.9-20 | `eval/chunking_gold/review_packets/mark16_9_20_textual_variant_review.md` | `pending_human_review` | Current output embeds the variant zone in a larger Mark ending chunk. |
| John.7.53-8.11 | `eval/chunking_gold/review_packets/john7_53_8_11_textual_variant_review.md` | `pending_human_review` | Current output splits and mixes the variant zone across two larger John chunks. |

Pending packets are not reviewed gold, not approved expected output, and not authorization for
output-changing work. They preserve current evidence so a human can later decide whether any case
should become reviewed gold, characterization-only evidence, or an approved parent/child structural
split.

## T317 Reviewed Psalm Gold And WJ Packets

T317 promotes the Psalm 105 and Psalm 106 review packets to reviewed whole-psalm gold:

| Case | Packet | Status | Reviewed behavior |
| --- | --- | --- | --- |
| Ps.105 | `eval/chunking_gold/review_packets/ps105_boundary_review.md` | `reviewed_gold` | Current `Ps.105.1-45` whole-psalm chunk is approved. |
| Ps.106 | `eval/chunking_gold/review_packets/ps106_boundary_review.md` | `reviewed_gold` | Current `Ps.106.1-48` whole-psalm chunk is approved; `b` markers are internal evidence only. |

T317 also adds pending words-of-Jesus review packets:

| Case | Packet | Status | Marker risk |
| --- | --- | --- | --- |
| John.3 | `eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md` | `pending_human_review` | `\wj` and punctuation cannot silently decide the speaker boundary. |
| Matt.5-Matt.7 | `eval/chunking_gold/review_packets/matt5_7_wj_discourse_review.md` | `pending_human_review` | Whole discourse unity and child teaching units require human review. |

The John 3 and Matthew 5-7 packets are not reviewed gold, not approved expected output, and not
authorization for output-changing work.

## T316c Proposed Marker-Sensitive Stress Cases

T316c adds proposed stress cases for USFM marker-sensitive review:

| Case | Status | Marker risk |
| --- | --- | --- |
| Gospels / Acts / Rev words-of-Jesus spans | `proposed` | `\wj` is evidence, not speaker authority. |
| Psalms with Selah / `\qs` markers | `proposed` | `\qs` is liturgical-rubric evidence, not an automatic boundary. |
| John.3 | `proposed` | Speaker boundary cannot be silently decided from red-letter markup. |
| Matt.5-Matt.7 | `proposed` | Long Jesus discourse needs parent/child review before output changes. |
| John.13-John.17 | `proposed` | Discourse/prayer/speaker boundaries need review despite `\wj` evidence. |
| Matt.24-Matt.25 / Mark.13 | `proposed` | Apocalyptic discourse and parallel-account scope need review. |
| John.7.53-John.8.11 | `proposed` | Major textual variant plus `\wj` speech evidence needs textual and speaker review. |

These are not reviewed gold, not approved expected output, and not authorization for
output-changing work.

## T318 Observed Stress Behavior Audit

T318 adds a diagnostic-only observed behavior audit for every stress-atlas case:

- `eval/chunking_gold/stress_atlas/observed_stress_behavior.json`
- `eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`

The audit maps proposed cases to current chunks and records containment, splitting, extra-context
mixing, marker evidence, review-packet status, and recommended next review steps. It does not add
reviewed gold, approve expected output, change evaluator policy, or authorize output-changing work.

Observed behavior maturity:

- `reviewed_gold_preserves_current_behavior` is limited to already reviewed Ps.105 and Ps.106
  whole-psalm gold.
- `review_packet_pending` means the existing packet remains pending and non-authorizing.
- `needs_review_packet`, `speaker_review_required`, `variant_policy_required`,
  `source_tradition_review_required`, and `unknown_needs_human_review` are triage states only.
- `implementation_allowed` remains `false` for the audit root and every observed entry.

## Unknown

- Whether future gold should use one cross-form schema or per-form manifest schemas.
- Whether reviewed parent/child structural splits need separate diagnostics beyond
  `reviewed_structural_splits`.
- How much human review is needed before a Biblical Chunking Stress Atlas can authorize
  output-changing work.
