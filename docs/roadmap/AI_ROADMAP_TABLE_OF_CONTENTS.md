---
object_type: ai_roadmap_table_of_contents
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-17 during T342 after a maintainer observed that the T337A review trail was harder to find than it should have been."
reason_for_inclusion: "Give AI agents a local roadmap and review-packet discovery map that links back to the main AI table of contents."
---

# AI Roadmap Table Of Contents

This local table of contents maps roadmap, selection, review-packet, task, and handoff artifacts
that are easy to miss from file names alone.

Back to main AI table of contents:

```text
AI_TABLE_OF_CONTENTS.md
```

## Current Bible Chunking Path

| Task | Purpose | Primary artifacts |
| --- | --- | --- |
| T336 | Whole-Bible roadmap | `docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md` |
| T337 | Psalm behavior-change selection | `docs/roadmap/T337_SELECT_ONE_PSALM_BEHAVIOR_CHANGE.md` |
| T337A | Psalm 89 human-review packet selection trail | `.ai/tasks/T337A.task.yaml`; `.ai/handoffs/T337A/handoff.md`; `eval/chunking_gold/review_packets/ps89_boundary_review.md` |
| T337B | Psalm 89 owner decision | `docs/roadmap/T337B_PS89_OWNER_DECISION_OPTION_C.md`; `eval/chunking_gold/review_packets/ps89_boundary_review.md` |
| T338 | Psalm 89 route-isolated implementation | `docs/roadmap/T338_PS89_ROUTE_ISOLATED_IMPLEMENTATION.md` |
| T339 | Psalm 89 same-baseline evaluation | `docs/roadmap/T339_PS89_SAME_BASELINE_RISK_EVALUATION.md` |
| T340 | Psalm candidate promotion decision | `docs/roadmap/T340_PSALM_CANDIDATE_PROMOTION_DECISION.md`; `.ai/control/t340_psalm_candidate_promotion_decision.yaml` |
| T341 | Revelation hard-book atlas | `docs/roadmap/T341_REVELATION_HARD_BOOK_ATLAS.md`; `docs/roadmap/T341_REVELATION_OBSERVED_BEHAVIOR_AUDIT.md` |
| T350 | Bible-wide readiness map | `docs/roadmap/T350_BIBLE_WIDE_CHUNKING_READINESS_PLAN.md`; `.ai/control/bible_chunking_readiness_map.yaml` |
| T342 | Revelation review-packet target selection | `docs/roadmap/T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md`; `.ai/tasks/T342.task.yaml`; `.ai/handoffs/T342/handoff.md` |

## Review Packet Surfaces

| Surface | Role |
| --- | --- |
| `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md` | Human-readable index and promotion queue. |
| `eval/chunking_gold/review_packets/review_packet_index.json` | Machine-readable review-packet index. |
| `eval/chunking_gold/per_form/psalms_gold_manifest.json` | Psalm reviewed-gold and structural-split manifest. |
| `.ai/control/chunking_theological_decision_register.yaml` | Decision ledger for chunking choices with possible theological downstream effects. |
| `.ai/control/bible_chunking_readiness_map.yaml` | Lane/readiness map for whole-Bible chunking. |

## Current Next Route

After T342, the next route is:

```text
T343 - Revelation Review Packets and Gold Candidates
```

T343 should create a pending, non-authorizing packet for:

```text
Rev.12.1-Rev.14.20
```

No Revelation implementation, reviewed-gold promotion, chunk regeneration, evaluator change,
boundary import, T327G, embedding/index work, graph-edge generation, or Psalm candidate promotion is
authorized by this table of contents.
