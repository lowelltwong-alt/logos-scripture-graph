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
| T343 | Revelation review packet and gold candidates | `docs/roadmap/T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md`; `.ai/tasks/T343.task.yaml`; `.ai/handoffs/T343/handoff.md`; `eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md` |
| T344 | Revelation owner-selection docket, selected `REV-T344-E` | `docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md`; `.ai/tasks/T344.task.yaml`; `.ai/handoffs/T344/handoff.md` |
| T351 | Bible-wide chunking research triage before more chunking work | `docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md`; `.ai/control/bible_chunking_research_triage_map.yaml`; `.ai/tasks/T351.task.yaml`; `.ai/handoffs/T351/handoff.md` |

## Review Packet Surfaces

| Surface | Role |
| --- | --- |
| `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md` | Human-readable index and promotion queue. |
| `eval/chunking_gold/review_packets/review_packet_index.json` | Machine-readable review-packet index. |
| `eval/chunking_gold/per_form/psalms_gold_manifest.json` | Psalm reviewed-gold and structural-split manifest. |
| `.ai/control/chunking_theological_decision_register.yaml` | Decision ledger for chunking choices with possible theological downstream effects. |
| `.ai/control/bible_chunking_readiness_map.yaml` | Lane/readiness map for whole-Bible chunking. |
| `.ai/control/chunking_agent_preflight.yaml` | Mandatory preflight for chunking agents; source metadata is evidence, not authority. |

## Current Next Route

After T344 owner decision and the later owner guidance to research the whole Bible first, the next
route is:

```text
T351 - Bible-Wide Chunking Research Triage Atlas
```

T351 should triage the canonical 66 before more chunking work. Revelation remains research/prep
only for the pending, non-authorizing packet for:

```text
Rev.12.1-Rev.14.20
```

Lowell Wong selected `REV-T344-E` on 2026-06-17:

```text
Research/triage the whole Bible first.
Classify lanes as review_packet_ready, research_first, governed_hold, or implementation_blocked.
Then choose one review-packet-ready lane; do not implement chunks.
```

No Revelation implementation, reviewed-gold promotion, chunk regeneration, evaluator change,
boundary import, T327G, embedding/index work, graph-edge generation, Psalm candidate promotion, or
source-metadata authority is authorized by this table of contents.
