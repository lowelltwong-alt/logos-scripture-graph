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

## AI Routing Tags

Use this local TOC when an agent is working on roadmap, chunking, review-packet, owner-decision,
audit, or validation context and needs to know which numbered task artifacts matter.

Common tags in this file:

- `current-route`, `next-route`, `owner-review`, `owner-decision`
- `review-packet`, `reviewed-gold`, `gold-gate`, `non-authorizing`
- `theology-risk`, `hermeneutic-neutrality`, `source-metadata`
- `audit`, `handoff`, `task-scope`, `validator`, `harness`
- `psalms`, `revelation`, `epistle`, `gospel-discourse-wj`, `john3`, `divine-capitalization`,
  `whole-bible-research`, `canonical-66`, `research-registry`, `source-metadata-atlas`,
  `apocalyptic-prophetic`, `intertext`, `hermeneutic-neutrality`, `argument-boundary`,
  `election`, `law-gospel`, `faith-works`, `assurance`, `red-letter`, `speaker-boundary`,
  `sermon-on-mount`, `farewell-discourse`, `dominical-quotation`

## Current Bible Chunking Path

| Task | Purpose | Tags | Use when | Primary artifacts |
| --- | --- | --- | --- | --- |
| T336 | Whole-Bible roadmap | `chunking`, `whole-bible`, `roadmap` | Planning or auditing the full Bible chunking destination. | `docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md` |
| T337 | Psalm behavior-change selection | `psalms`, `selection`, `non-authorizing` | Checking why no Psalm behavior-change target was selected at that point. | `docs/roadmap/T337_SELECT_ONE_PSALM_BEHAVIOR_CHANGE.md` |
| T337A | Psalm 89 human-review packet selection trail | `psalms`, `review-packet`, `handoff` | Reconstructing the Psalm 89 review trail. | `.ai/tasks/T337A.task.yaml`; `.ai/handoffs/T337A/handoff.md`; `eval/chunking_gold/review_packets/ps89_boundary_review.md` |
| T337B | Psalm 89 owner decision | `psalms`, `owner-decision`, `reviewed-gold` | Auditing the owner-approved Psalm 89 option and exact spans. | `docs/roadmap/T337B_PS89_OWNER_DECISION_OPTION_C.md`; `eval/chunking_gold/review_packets/ps89_boundary_review.md` |
| T338 | Psalm 89 route-isolated implementation | `psalms`, `implementation`, `route-isolation` | Checking the one-route implementation constraints and non-target identity proof. | `docs/roadmap/T338_PS89_ROUTE_ISOLATED_IMPLEMENTATION.md` |
| T339 | Psalm 89 same-baseline evaluation | `psalms`, `evaluation`, `same-baseline` | Reviewing score/evaluation claims after the Psalm 89 implementation. | `docs/roadmap/T339_PS89_SAME_BASELINE_RISK_EVALUATION.md` |
| T340 | Psalm candidate promotion decision | `psalms`, `promotion`, `owner-decision` | Understanding why Psalm candidates were or were not promoted. | `docs/roadmap/T340_PSALM_CANDIDATE_PROMOTION_DECISION.md`; `.ai/control/t340_psalm_candidate_promotion_decision.yaml` |
| T341 | Revelation hard-book atlas | `revelation`, `hard-book`, `hermeneutic-neutrality` | Preparing Revelation research without choosing an interpretive system. | `docs/roadmap/T341_REVELATION_HARD_BOOK_ATLAS.md`; `docs/roadmap/T341_REVELATION_OBSERVED_BEHAVIOR_AUDIT.md` |
| T350 | Bible-wide readiness map | `readiness`, `whole-bible`, `next-route` | Checking lane order, readiness, and non-authorizing algorithm status. | `docs/roadmap/T350_BIBLE_WIDE_CHUNKING_READINESS_PLAN.md`; `.ai/control/bible_chunking_readiness_map.yaml` |
| T342 | Revelation review-packet target selection | `revelation`, `target-selection`, `review-packet` | Verifying the exact Revelation packet target selected for review prep. | `docs/roadmap/T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md`; `.ai/tasks/T342.task.yaml`; `.ai/handoffs/T342/handoff.md` |
| T343 | Revelation review packet and gold candidates | `revelation`, `review-packet`, `metadata-evidence` | Auditing Revelation review packets, metadata lessons, and non-authorizations. | `docs/roadmap/T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md`; `.ai/tasks/T343.task.yaml`; `.ai/handoffs/T343/handoff.md`; `eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md` |
| T344 | Revelation owner-selection docket, selected `REV-T344-E` | `revelation`, `owner-decision`, `research-only` | Checking why Revelation remains research/prep only and T345 is blocked. | `docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md`; `.ai/tasks/T344.task.yaml`; `.ai/handoffs/T344/handoff.md` |
| T351 | Bible-wide chunking research triage before more chunking work | `whole-bible`, `triage`, `theology-risk` | Deciding which Bible lanes need research, packets, holds, or implementation blocks. | `docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md`; `.ai/control/bible_chunking_research_triage_map.yaml`; `.ai/tasks/T351.task.yaml`; `.ai/handoffs/T351/handoff.md` |
| T352 | Epistle argument review-packet prep | `epistle`, `review-packet`, `pending-human-review` | Working on epistle argument packets without treating them as reviewed gold. | `docs/roadmap/T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md`; `.ai/tasks/T352.task.yaml`; `.ai/handoffs/T352/handoff.md`; `eval/chunking_gold/review_packets/eph1_3_14_argument_review.md`; `eval/chunking_gold/review_packets/rom9_11_argument_review.md`; `eval/chunking_gold/review_packets/heb7_10_priesthood_argument_review.md`; `eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md` |
| T353 | Divine capitalization inventory harness | `divine-capitalization`, `source-metadata`, `harness` | Checking God/god, Spirit/spirit, Father/father, Word/word evidence-only handling. | `docs/roadmap/T353_DIVINE_CAPITALIZATION_INVENTORY_HARNESS.md`; `.ai/control/divine_capitalization_inventory.yaml`; `scripts/validate_divine_capitalization_inventory.py`; `.ai/tasks/T353.task.yaml`; `.ai/handoffs/T353/handoff.md` |
| T354 | WJ/red-letter marker inventory harness | `wj`, `red-letter`, `source-metadata`, `harness` | Checking words-of-Jesus marker evidence without authorizing speaker/chunk behavior. | `docs/roadmap/T354_WJ_MARKER_INVENTORY_HARNESS.md`; `.ai/control/wj_marker_inventory.yaml`; `scripts/validate_wj_marker_inventory.py`; `.ai/tasks/T354.task.yaml`; `.ai/handoffs/T354/handoff.md` |
| T355 | WJ speaker/discourse policy and target selection | `wj-speaker`, `gospel-discourse-wj`, `john3`, `policy` | Understanding why John 3 was selected for owner review only. | `docs/roadmap/T355_WJ_SPEAKER_POLICY_AND_TARGET_SELECTION.md`; `.ai/control/wj_speaker_discourse_policy.yaml`; `scripts/validate_wj_speaker_discourse_policy.py`; `.ai/tasks/T355.task.yaml`; `.ai/handoffs/T355/handoff.md` |
| T356 | John 3 WJ owner-review docket | `john3`, `owner-review`, `speaker-boundary`, `current-route` | Presenting owner options before any John 3 parent/child/speaker/chunk approval. | `docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md`; `.ai/control/john3_wj_owner_review_docket.yaml`; `scripts/validate_john3_owner_review_docket.py`; `.ai/tasks/T356.task.yaml`; `.ai/handoffs/T356/handoff.md` |
| T358 | Bible-wide chunking research registry | `whole-bible-research`, `canonical-66`, `research-registry`, `non-authorizing` | Preparing future research packets across all 66 books without starting chunk implementation. | `docs/roadmap/T358_BIBLE_WIDE_CHUNKING_RESEARCH_REGISTRY.md`; `.ai/control/bible_wide_chunking_research_registry.yaml`; `scripts/validate_bible_wide_chunking_research_registry.py`; `.ai/tasks/T358.task.yaml`; `.ai/handoffs/T358/handoff.md` |
| T359 | Source metadata research atlas | `source-metadata-atlas`, `cross-references`, `strongs`, `wj`, `capitalization`, `non-authorizing` | Checking metadata families before future chunking, graph, retrieval, or review-packet work. | `docs/roadmap/T359_SOURCE_METADATA_RESEARCH_ATLAS.md`; `.ai/control/source_metadata_research_atlas.yaml`; `scripts/validate_source_metadata_research_atlas.py`; `.ai/tasks/T359.task.yaml`; `.ai/handoffs/T359/handoff.md` |
| T360 | Apocalyptic prophetic intertext dossier queue | `apocalyptic-prophetic`, `revelation`, `daniel`, `intertext`, `hermeneutic-neutrality`, `non-authorizing` | Preparing Revelation/Daniel/prophetic intertext dossiers without selecting a hermeneutic system. | `docs/roadmap/T360_APOCALYPTIC_PROPHETIC_INTERTEXT_DOSSIERS.md`; `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml`; `scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py`; `.ai/tasks/T360.task.yaml`; `.ai/handoffs/T360/handoff.md` |
| T361 | Epistle argument theological issue dossier queue | `epistle`, `argument-boundary`, `election`, `law-gospel`, `faith-works`, `assurance`, `non-authorizing` | Preparing epistle issue dossiers without selecting a doctrinal system or treating pending packets as reviewed gold. | `docs/roadmap/T361_EPISTLE_ARGUMENT_THEOLOGICAL_ISSUE_DOSSIERS.md`; `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml`; `scripts/validate_epistle_argument_theological_issue_dossier_queue.py`; `.ai/tasks/T361.task.yaml`; `.ai/handoffs/T361/handoff.md` |
| T362 | Gospel WJ discourse dossier queue | `gospel-discourse-wj`, `red-letter`, `speaker-boundary`, `john3`, `sermon-on-mount`, `farewell-discourse`, `non-authorizing` | Preparing Gospel/WJ discourse dossiers without selecting speaker, discourse, reviewed-gold, or chunk authority. | `docs/roadmap/T362_GOSPEL_WJ_DISCOURSE_DOSSIERS.md`; `.ai/control/gospel_wj_discourse_dossier_queue.yaml`; `scripts/validate_gospel_wj_discourse_dossier_queue.py`; `.ai/tasks/T362.task.yaml`; `.ai/handoffs/T362/handoff.md` |

## Review Packet Surfaces

| Surface | Tags | Use when | Role |
| --- | --- | --- | --- |
| `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md` | `review-packet`, `promotion-queue`, `human-readable` | A reviewer needs the packet queue and human-facing packet status. | Human-readable index and promotion queue. |
| `eval/chunking_gold/review_packets/review_packet_index.json` | `review-packet`, `machine-readable`, `validator` | A validator or agent needs structured packet status. | Machine-readable review-packet index. |
| `eval/chunking_gold/per_form/psalms_gold_manifest.json` | `reviewed-gold`, `psalms`, `manifest` | Work touches approved Psalm reviewed-gold spans. | Psalm reviewed-gold and structural-split manifest. |
| `.ai/control/chunking_theological_decision_register.yaml` | `theology-risk`, `decision-register`, `downstream-risk` | A chunking/evaluator/gold/route/default decision may affect theological interpretation. | Decision ledger for chunking choices with possible theological downstream effects. |
| `.ai/control/bible_chunking_readiness_map.yaml` | `readiness`, `next-route`, `whole-bible` | A future agent needs the active route and lane readiness. | Lane/readiness map for whole-Bible chunking. |
| `.ai/control/chunking_agent_preflight.yaml` | `preflight`, `source-metadata`, `required-reading` | Any chunking-related work starts or a lesson must be encoded. | Mandatory preflight for chunking agents; source metadata is evidence, not authority. |
| `.ai/control/divine_capitalization_inventory.yaml` | `divine-capitalization`, `source-metadata`, `evidence-only` | Work touches God/god, Spirit/spirit, Father/father, Word/word, or capitalization evidence. | Observed divine-name/title/pronoun capitalization variants; evidence only, not graph/chunk/retrieval authority. |
| `.ai/control/wj_marker_inventory.yaml` | `wj`, `red-letter`, `source-metadata`, `evidence-only` | Work touches words-of-Jesus markers or red-letter formatting. | Observed WJ/red-letter marker token runs; evidence only, not speaker/chunk/graph/retrieval authority. |
| `.ai/control/wj_speaker_discourse_policy.yaml` | `wj-speaker`, `john3`, `policy`, `owner-review` | Work weighs WJ/speaker/discourse evidence before owner review. | Policy for weighing WJ/speaker/discourse evidence; selects John 3 for owner review only. |
| `.ai/control/john3_wj_owner_review_docket.yaml` | `john3`, `owner-review`, `current-route`, `non-authorizing` | Owner needs John 3 options or an agent needs to know what is still pending. | Pending John 3 owner-review options; no parent/child/speaker/chunk approval. |
| `.ai/control/bible_wide_chunking_research_registry.yaml` | `whole-bible-research`, `canonical-66`, `research-registry`, `book-watchpoints` | Future agents need book-level research prompts before exact review packets or algorithms. | Canonical 66-book research queue; no chunk/gold/graph/output authority. |
| `.ai/control/source_metadata_research_atlas.yaml` | `source-metadata-atlas`, `cross-references`, `strongs`, `wj`, `capitalization` | Future agents need source metadata families, observed surfaces, and non-authorizations before chunk/graph/retrieval work. | Metadata research atlas; no Scripture/lexical/intertext/speaker/graph/chunk/retrieval/output authority. |
| `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml` | `apocalyptic-prophetic`, `revelation`, `daniel`, `intertext`, `hermeneutic-neutrality` | Future agents need Revelation/Daniel/prophetic intertext dossiers before exact packets or algorithm work. | Dossier queue; no intertext/graph/retrieval/chunk/output authority. |
| `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml` | `epistle`, `argument-boundary`, `election`, `law-gospel`, `faith-works`, `assurance` | Future agents need epistle theological issue dossiers before exact packet review, route, graph, retrieval, or algorithm work. | Dossier queue; no doctrine/reviewed-gold/graph/retrieval/chunk/output authority. |
| `.ai/control/gospel_wj_discourse_dossier_queue.yaml` | `gospel-discourse-wj`, `red-letter`, `speaker-boundary`, `john3`, `sermon-on-mount`, `farewell-discourse`, `dominical-quotation` | Future agents need Gospel/WJ discourse dossiers before exact packet review, route, graph, retrieval, or algorithm work. | Dossier queue; no speaker/discourse/reviewed-gold/graph/retrieval/chunk/output authority. |

## Current Next Route

After T344 owner decision, T351 Bible-wide triage, and the later owner guidance to review one lane
at a time, the next
route is:

```text
T356 - John 3 WJ Owner Review Docket
```

T356 records pending owner-review options for `John.3.1-John.3.36` /
`john3_wj_speaker_boundary` before any future Gospel discourse, speaker-boundary, graph,
retrieval, reviewed-gold, or chunk work can cite red-letter metadata for behavior.
Revelation remains research/prep only for the
pending, non-authorizing packet for:

```text
Rev.12.1-Rev.14.20
```

Lowell Wong selected `REV-T344-E` on 2026-06-17:

```text
Research/triage the whole Bible first.
Classify lanes as review_packet_ready, research_first, governed_hold, or implementation_blocked.
Then create review packets or evidence inventories for one reviewed lane at a time; do not implement chunks.
```

No Revelation implementation, reviewed-gold promotion, chunk regeneration, evaluator change,
boundary import, T327G, embedding/index work, graph-edge generation, Psalm candidate promotion, or
source-metadata authority is authorized by this table of contents. T352 does not authorize epistle
route implementation or output changes. T353 does not authorize capitalization-driven graph edges,
chunk boundaries, retrieval truth, speaker attribution, lexical truth, or output changes. T354 does
not authorize Jesus speaker attribution, speaker boundaries, discourse boundaries, WJ-driven graph
edges, chunk boundaries, retrieval truth, reviewed gold, or output changes. T355 does not authorize
John 3 speaker boundaries, discourse boundaries, reviewed gold, WJ-driven route behavior, graph
edges, retrieval truth, or output changes. T356 does not authorize John 3 parent spans, child
spans, Jesus speaker attribution, narrator boundaries, reviewed gold, graph edges, retrieval truth,
route behavior, or output changes.
T358 does not authorize any book-level research prompt or future review-packet candidate as
reviewed gold, route behavior, graph truth, retrieval truth, source-metadata authority, or output
change.
T359 does not authorize internal cross-references, Strong's-style numbers, lexical rarity,
footnotes, headings, boundary markers, WJ/red-letter markers, speaker labels, formatting, or
capitalization as Scripture truth, lexical truth, intertext truth, speaker attribution, graph
edges, retrieval truth, reviewed gold, chunk boundaries, output changes, boundary import, or
algorithm behavior.
T360 does not authorize Revelation implementation, Daniel/Revelation chronology, hermeneutic
system selection, graph edges, retrieval truth, reviewed gold, chunk boundaries, output changes,
boundary import, or T345.
T361 does not authorize epistle implementation, doctrinal system selection, pending packet
approval, reviewed-gold promotion, route behavior, evaluator changes, graph edges, retrieval truth,
chunk boundaries, output changes, boundary import, or T345.
T362 does not authorize Jesus speaker attribution, speaker boundaries, discourse boundaries,
pending packet approval, reviewed-gold promotion, route behavior, evaluator changes, graph edges,
retrieval truth, chunk boundaries, output changes, boundary import, Gospel/WJ implementation, or
T345.
