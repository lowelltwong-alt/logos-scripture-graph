# T315 Next Target Inventory

Status: planning inventory only. No target below is authorized for output-changing implementation in
T315.

## Confirmed

- T314 establishes reviewed structural split policy: raw fragmentation remains visible, exact
  manifest-reviewed parent/child splits can be excluded from final bad-fragmentation scoring.
- Chunk output is unchanged from D / Claude pass2.
- Current T314 baseline is D / Claude pass2 = 93.5.
- T311 93.0 and old 88.5 are provenance for the same unchanged output.

## Candidate Targets

| Target | Expected benefit | Risk | Required gold | Evaluator sanity check needed | Output-changing work allowed now |
| --- | --- | --- | --- | --- | --- |
| Reviewed structural split policy follow-up | More precise diagnostics for approved parent/child cases. | Overusing exceptions could hide real fragmentation. | Exact reviewed parent/child cases beyond Ps.119/Ps.78. | Yes, before any score movement. | No. |
| Token-size evaluator/policy mismatch (T313) | Align p50 scoring with policy or clarify distinct retrieval vs assembly targets. | Broad retune could damage discourse and literary units. | Representative cases where smaller chunks help and where they hurt. | Yes. | No. |
| Long Psalm parent/child model | Generalize Ps.119/Ps.78 lessons to other long Psalms. | Treating all long Psalms as approved splits without review. | Ps.89, Ps.105, Ps.106, Ps.136 reviewed boundary packets. | Yes. | No. |
| Prophetic oracle chunking | Better oracle/vision/woe units. | Oracle boundaries are interpretive and may cross chapter/heading convenience. | Reviewed oracle cases with source-marker evidence. | Yes. | No. |
| Long discourse chunking | Better Gospel discourse and epistle argument retrieval. | Smaller chunks may lose discourse context; larger chunks may hurt retrieval. | Gospel discourse and Pauline argument gold. | Yes. | No. |
| Entity-layer interaction (T320) | Future chunks can carry entity/spiritual-realm references cleanly. | Entity modeling could smuggle interpretive claims into chunk boundaries. | Entity schema/review plan after T320 approval. | Not for chunk scoring yet. | No. |
| Concept graph interaction (T330) | Future concept packets can reference chunk evidence. | Theological concepts can overrun asserted/inferred/candidate boundaries. | Concept graph governance and reviewed examples. | Not for chunk scoring yet. | No. |
| Boundary-literature repo lane | Keep non-Bible boundary texts separate from this repo's Scripture data plane. | Scope creep and cross-repo authority confusion. | Separate repo plan and governance contract. | Unknown. | No. |

## Proposed T316 Stress Atlas

T316 should build a Biblical Chunking Stress Atlas before any broad output-changing pass. The atlas
would collect reviewed or review-ready cases across Psalms, Lamentations, Proverbs, Job, prophets,
Gospels, and epistles.

Minimum stress-atlas fields:

- passage or parent unit;
- current observed chunk boundaries;
- proposed target boundaries, if reviewed;
- source-marker and discourse evidence;
- evaluator metric at risk;
- whether the case is reviewed, characterization-only, or pending human review;
- non-target controls.

## Inferred Sequencing

1. T316: build stress atlas and candidate gold packets.
2. T313: decide evaluator/policy alignment for token-size scoring.
3. Output-changing chunk work only after reviewed target-form gold exists.
4. T320/T321/T330/T340 stay separate planning lanes until schemas/runtime are explicitly approved.

## Unknown

- Which future long Psalm should be reviewed first.
- Whether T313 should move evaluator target p50, chunk policy target, or both.
- Whether boundary-literature work belongs in a sibling repository or a future upstream governance
  package.
