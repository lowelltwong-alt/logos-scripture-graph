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
  `sermon-on-mount`, `farewell-discourse`, `dominical-quotation`, `narrative`, `legal`,
  `covenant`, `genealogy`, `lists`, `typology`, `harmonization`, `wisdom`, `dialogue`,
  `poetry`, `acrostic`, `refrain`, `job`, `song`, `lamentations`, `ps119`, `prophetic`,
  `oracle`, `vision`, `servant-song`, `temple-vision`, `day-of-yahweh`, `fulfillment`,
  `israel-church`, `messianic`, `zechariah`, `textual-variant`, `source-tradition`,
  `canon-scope`, `boundary-routing`, `mark16`, `pericope-adulterae`, `deut32`, `jude`,
  `comma-johanneum`, `orthodox-hermeneutic-firewall`, `anti-smuggling`,
  `orthodoxy-boundary`, `canon-authority`, `textual-critical-policy`, `variant-sensitive`,
  `1cor8-10`, `evidence-packet`, `reviewed-gold-promotion`, `human-decision`, `chunking-ready`, `goal-blocked`, `stop-conditions`,
  `owner-projection`, `projected-owner-pattern`, `conflict-scan`, `governance-memory`,
  `original-language`, `grammar-overlay`, `greek`, `hebrew`, `non-orthodox`, `lds`,
  `watch-tower`, `nwt`, `trinity`, `christology`, `divine-plurality`,
  `owner-options`, `case-by-case`, `1cor9-20`, `1cor10-9`, `reviewed-gold-blocker`,
  `case-policy`, `selected-policy`, `owner-confirmation`, `ODP-005`, `T379`, `T380`,
  `variant-dependency`, `owner-decision-packet`, `T371-A`, `variant-non-dependent`,
  `harness-next`, `T372`, `route-isolation`, `non-target-identity`, `T373`,
  `implementation-authorization`, `T374`, `child-span-denial`, `decision-presentation`,
  `baseline-overlap`, `additive-overlay`, `output-manifest`, `same-baseline`, `T375`, `post-pilot-review`, `child-necessity-review`, `T376`, `next-lane-selection`, `replacement-split`, `target-widening`, `dry-run`,
  `T381`, `phrase/context`, `isolated word`, `lemma`, `syntax`, `discourse`,
  `T382`, `lessons-learned`, `lesson-index`, `lesson-graph`, `preflight`, `midflight`,
  `postflight`, `workflow-governance`, `T383`, `contextual-reading`, `prooftexting`,
  `immediate-context`, `paragraph-context`, `chapter-context`, `book-context`,
  `canonical-context`, `historical-context`, `research-runway`, `research-autonomy`,
  `authority-boundary`, `target-options`, `T384`, `T385`, `bible-wide-readiness`,
  `research-synthesis`, `human-decision-map`, `ready-lanes`, `blocked-authority`,
  `T386`, `verse-passage-coverage`, `coverage-inventory`, `coverage-taxonomy`,
  `readiness-matrix`, `gap-register`, `human-review-docket`, `target-passage-lookup`,
  `test-runtime`, `pytest-timeout`, `long-running-tests`, `focused-tests`, `split-tests`,
  `T387`, `manuscript-witness`, `reliability`, `provenance`, `oldest-fragments`,
  `dead-sea-scrolls`, `nt-papyri`, `codices`, `copy-abundance`, `discovery-timeline`,
  `T389`, `launch-readiness`, `clean-trunk`,
  `T390`, `source-catalog`, `metadata-plan`, `sqlite-plan`, `major-codices`,
  `holding-institutions`, `source-trust`, `anti-guessing`, `owner-decision-packet`,
  `recommendation-not-selection`, `goal4`, `ephesians`

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
| T356 | John 3 WJ owner-review docket | `john3`, `owner-review`, `speaker-boundary` | Checking the `john3_wj_speaker_boundary` owner-review options and the later selected parent-only target. | `docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md`; `.ai/control/john3_wj_owner_review_docket.yaml`; `scripts/validate_john3_owner_review_docket.py`; `.ai/tasks/T356.task.yaml`; `.ai/handoffs/T356/handoff.md` |
| T358 | Bible-wide chunking research registry | `whole-bible-research`, `canonical-66`, `research-registry`, `non-authorizing` | Preparing future research packets across all 66 books without starting chunk implementation. | `docs/roadmap/T358_BIBLE_WIDE_CHUNKING_RESEARCH_REGISTRY.md`; `.ai/control/bible_wide_chunking_research_registry.yaml`; `scripts/validate_bible_wide_chunking_research_registry.py`; `.ai/tasks/T358.task.yaml`; `.ai/handoffs/T358/handoff.md` |
| T359 | Source metadata research atlas | `source-metadata-atlas`, `cross-references`, `strongs`, `wj`, `capitalization`, `non-authorizing` | Checking metadata families before future chunking, graph, retrieval, or review-packet work. | `docs/roadmap/T359_SOURCE_METADATA_RESEARCH_ATLAS.md`; `.ai/control/source_metadata_research_atlas.yaml`; `scripts/validate_source_metadata_research_atlas.py`; `.ai/tasks/T359.task.yaml`; `.ai/handoffs/T359/handoff.md` |
| T360 | Apocalyptic prophetic intertext dossier queue | `apocalyptic-prophetic`, `revelation`, `daniel`, `intertext`, `hermeneutic-neutrality`, `non-authorizing` | Preparing Revelation/Daniel/prophetic intertext dossiers without selecting a hermeneutic system. | `docs/roadmap/T360_APOCALYPTIC_PROPHETIC_INTERTEXT_DOSSIERS.md`; `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml`; `scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py`; `.ai/tasks/T360.task.yaml`; `.ai/handoffs/T360/handoff.md` |
| T361 | Epistle argument theological issue dossier queue | `epistle`, `argument-boundary`, `election`, `law-gospel`, `faith-works`, `assurance`, `non-authorizing` | Preparing epistle issue dossiers without selecting a doctrinal system or treating pending packets as reviewed gold. | `docs/roadmap/T361_EPISTLE_ARGUMENT_THEOLOGICAL_ISSUE_DOSSIERS.md`; `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml`; `scripts/validate_epistle_argument_theological_issue_dossier_queue.py`; `.ai/tasks/T361.task.yaml`; `.ai/handoffs/T361/handoff.md` |
| T362 | Gospel WJ discourse dossier queue | `gospel-discourse-wj`, `red-letter`, `speaker-boundary`, `john3`, `sermon-on-mount`, `farewell-discourse`, `non-authorizing` | Preparing Gospel/WJ discourse dossiers without selecting speaker, discourse, reviewed-gold, or chunk authority. | `docs/roadmap/T362_GOSPEL_WJ_DISCOURSE_DOSSIERS.md`; `.ai/control/gospel_wj_discourse_dossier_queue.yaml`; `scripts/validate_gospel_wj_discourse_dossier_queue.py`; `.ai/tasks/T362.task.yaml`; `.ai/handoffs/T362/handoff.md` |
| T363 | Narrative legal covenant dossier queue | `narrative`, `legal`, `covenant`, `genealogy`, `lists`, `typology`, `harmonization`, `non-authorizing` | Preparing narrative/legal/covenant dossiers without selecting covenant systems, law/gospel, typology, harmonization, reviewed-gold, or chunk authority. | `docs/roadmap/T363_NARRATIVE_LEGAL_COVENANT_DOSSIERS.md`; `.ai/control/narrative_legal_covenant_dossier_queue.yaml`; `scripts/validate_narrative_legal_covenant_dossier_queue.py`; `.ai/tasks/T363.task.yaml`; `.ai/handoffs/T363/handoff.md` |
| T364 | Wisdom dialogue poetry dossier queue | `wisdom`, `dialogue`, `poetry`, `acrostic`, `refrain`, `speaker-boundary`, `job`, `song`, `lamentations`, `ps119`, `non-authorizing` | Preparing wisdom/dialogue/poetry dossiers without selecting wisdom theology, speaker boundaries, Song readings, reviewed-gold, or chunk authority. | `docs/roadmap/T364_WISDOM_DIALOGUE_POETRY_DOSSIERS.md`; `.ai/control/wisdom_dialogue_poetry_dossier_queue.yaml`; `scripts/validate_wisdom_dialogue_poetry_dossier_queue.py`; `.ai/tasks/T364.task.yaml`; `.ai/handoffs/T364/handoff.md` |
| T365 | Prophetic oracle vision dossier queue | `prophetic`, `oracle`, `vision`, `servant-song`, `temple-vision`, `day-of-yahweh`, `fulfillment`, `israel-church`, `messianic`, `zechariah`, `non-authorizing` | Preparing prophetic/oracle/vision dossiers without selecting fulfillment theology, eschatology, covenant systems, Israel/church relation, messianic identification, temple theology, reviewed-gold, or chunk authority. | `docs/roadmap/T365_PROPHETIC_ORACLE_VISION_DOSSIERS.md`; `.ai/control/prophetic_oracle_vision_dossier_queue.yaml`; `scripts/validate_prophetic_oracle_vision_dossier_queue.py`; `.ai/tasks/T365.task.yaml`; `.ai/handoffs/T365/handoff.md` |
| T366 | Textual variant source tradition dossier queue | `textual-variant`, `source-tradition`, `canon-scope`, `boundary-routing`, `mark16`, `pericope-adulterae`, `deut32`, `jude`, `comma-johanneum`, `non-authorizing` | Preparing textual-variant/source-tradition dossiers without selecting textual-critical policy, canon scope, source-tradition preference, boundary import, noncanonical authority, reviewed-gold, or chunk authority. | `docs/roadmap/T366_TEXTUAL_VARIANT_SOURCE_TRADITION_DOSSIERS.md`; `.ai/control/textual_variant_source_tradition_dossier_queue.yaml`; `scripts/validate_textual_variant_source_tradition_dossier_queue.py`; `.ai/tasks/T366.task.yaml`; `.ai/handoffs/T366/handoff.md` |
| T367 | Owner decision firewall and next target | `owner-decision`, `orthodox-hermeneutic-firewall`, `anti-smuggling`, `textual-critical-policy`, `john3`, `1cor8-10`, `non-authorizing` | Auditing JOHN3-T356-B, the orthodox firewall, textual-critical policy requirement, and the next review-only epistle target. | `docs/roadmap/T367_OWNER_DECISION_FIREWALL_AND_NEXT_TARGET.md`; `.ai/control/orthodox_hermeneutic_firewall_docket.yaml`; `.ai/control/textual_critical_policy_docket.yaml`; `.ai/tasks/T367.task.yaml`; `.ai/handoffs/T367/handoff.md` |
| T368 | 1 Corinthians 8-10 packet strengthening | `1cor8-10`, `epistle`, `owner-review`, `conscience`, `idol-food`, `sacramental`, `christian-liberty`, `non-authorizing` | Auditing the strengthened 1Cor.8-10 packet, pending owner options, and non-authorizing evidence. | `docs/roadmap/T368_1COR8_10_PACKET_STRENGTHENING.md`; `.ai/control/1cor8_10_epistle_owner_review_docket.yaml`; `eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md`; `scripts/validate_1cor8_10_owner_review_docket.py`; `.ai/tasks/T368.task.yaml`; `.ai/handoffs/T368/handoff.md` |
| T369 | 1Cor.8-10 projected parent-only review selection | `1cor8-10`, `human-decision`, `chunking-ready`, `goal-blocked`, `stop-conditions`, `owner-gate`, `owner-projection`, `projected-owner-pattern`, `conflict-scan`, `non-authorizing` | Auditing the parent-only projected owner-pattern decision and conflict scan that unblocks T370 evidence prep without output authority. | `docs/roadmap/T369_HUMAN_DECISION_FORECAST_AND_CHUNKING_READY_ROADMAP.md`; `.ai/control/chunking_human_decision_forecast.yaml`; `.ai/control/owner_decision_projection_policy.yaml`; `.ai/control/governance_memory_durability_policy.yaml`; `.ai/control/1cor8_10_epistle_owner_review_docket.yaml`; `scripts/validate_chunking_human_decision_forecast.py`; `scripts/validate_owner_decision_projection_policy.py`; `scripts/validate_governance_memory_durability.py`; `.ai/tasks/T369.task.yaml`; `.ai/handoffs/T369/handoff.md` |
| T370 | 1Cor.8-10 parent-only evidence packet | `1cor8-10`, `evidence-packet`, `reviewed-gold-promotion`, `source-metadata`, `parent-only`, `non-authorizing` | Auditing the governed parent-only evidence packet before any owner reviewed-gold promotion decision. | `eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml`; `scripts/validate_1cor8_10_parent_evidence_packet.py`; `.ai/tasks/T370.task.yaml`; `.ai/handoffs/T370/handoff.md` |
| T377 | Orthodox original-language pressure passage queue | `original-language`, `grammar-overlay`, `greek`, `hebrew`, `non-orthodox`, `lds`, `watch-tower`, `nwt`, `trinity`, `christology`, `divine-plurality`, `non-authorizing` | Preparing ahead-of-time pressure-passage dossiers before future chunk, graph, retrieval, route, evaluator, or reviewed-gold work touches Greek/Hebrew grammar-sensitive passages. | `docs/roadmap/T377_ORTHODOX_ORIGINAL_LANGUAGE_PRESSURE_DOSSIERS.md`; `.ai/control/orthodox_original_language_pressure_dossier_queue.yaml`; `scripts/validate_orthodox_original_language_pressure_dossier_queue.py`; `.ai/tasks/T377.task.yaml`; `.ai/handoffs/T377/handoff.md` |
| T381 | Original-language phrase/context policy | `original-language`, `phrase/context`, `greek`, `hebrew`, `isolated word`, `lemma`, `strongs`, `syntax`, `discourse`, `root-fallacy`, `semantic-range`, `interlinear`, `greek-article`, `hebrew-plural`, `lxx`, `textual-variant`, `punctuation`, `poetry`, `non-authorizing` | Future packets include Greek/Hebrew words, lemmas, Strong's-style tags, lexical rarity, morphology, grammar labels, roots, article claims, Hebrew plural claims, LXX/NT quotations, punctuation/capitalization, discourse markers, or poetic structure and must preserve phrase/clause/syntax/discourse/textual/genre/canonical context. | `docs/roadmap/T381_ORIGINAL_LANGUAGE_PHRASE_CONTEXT_POLICY.md`; `.ai/control/original_language_phrase_context_policy.yaml`; `scripts/validate_original_language_phrase_context_policy.py`; `.ai/tasks/T381.task.yaml`; `.ai/handoffs/T381/handoff.md` |
| T378 | Textual-critical policy owner options | `textual-critical-policy`, `owner-options`, `variant-sensitive`, `case-by-case`, `1cor9-20`, `1cor10-9`, `reviewed-gold-blocker`, `non-authorizing` | T371 or another packet needs textual-critical owner policy before variant-sensitive reviewed-gold promotion. | `docs/roadmap/T378_TEXTUAL_CRITICAL_POLICY_OWNER_OPTIONS.md`; `.ai/control/textual_critical_policy_owner_options.yaml`; `scripts/validate_textual_critical_policy_owner_options.py`; `.ai/tasks/T378.task.yaml`; `.ai/handoffs/T378/handoff.md` |
| T379 | Textual-critical case-by-case policy selection | `textual-critical-policy`, `case-policy`, `selected-policy`, `owner-confirmation`, `ODP-005`, `variant-dependency`, `non-authorizing` | Owner selected `TCP-T378-B`; future agents need the process pattern without treating it as preferred-reading, promotion, or output authority. | `docs/roadmap/T379_TEXTUAL_CRITICAL_CASE_POLICY_SELECTION.md`; `.ai/control/textual_critical_case_policy.yaml`; `scripts/validate_textual_critical_case_policy.py`; `.ai/tasks/T379.task.yaml`; `.ai/handoffs/T379/handoff.md` |
| T380 | T371 owner decision packet | `t371`, `variant-dependency`, `owner-decision-packet`, `reviewed-gold-promotion`, `1cor9-20`, `1cor10-9`, `parent-only`, `non-authorizing` | Owner or auditor needs the exact T371 options before parent-only reviewed-gold promotion. | `docs/roadmap/T380_T371_VARIANT_DEPENDENCY_OWNER_DECISION_PACKET.md`; `.ai/control/t371_variant_dependency_owner_decision_packet.yaml`; `scripts/validate_t371_variant_dependency_owner_decision_packet.py`; `.ai/tasks/T380.task.yaml`; `.ai/handoffs/T380/handoff.md` |
| T371 | T371-A parent-only reviewed-gold promotion | `t371-a`, `reviewed-gold`, `parent-only`, `variant-non-dependent`, `1cor8-10`, `1cor9-20`, `1cor10-9`, `harness-next` | Auditing the owner-confirmed parent-only reviewed-gold promotion or preparing T372 harness work. | `docs/roadmap/T371_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md`; `.ai/control/t371_parent_only_reviewed_gold_promotion.yaml`; `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json`; `scripts/validate_t371_parent_only_reviewed_gold_promotion.py`; `.ai/tasks/T371.task.yaml`; `.ai/handoffs/T371/handoff.md` |
| T372 | Route-isolation harness plan | `t372`, `route-isolation`, `non-target-identity`, `harness`, `owner-gate`, `1cor8-10`, `non-authorizing` | Auditing the completed harness plan before the T373 owner implementation gate. | `docs/roadmap/T372_ROUTE_ISOLATION_HARNESS_PLAN.md`; `.ai/control/t372_route_isolation_harness_plan.yaml`; `scripts/validate_t372_route_isolation_harness_plan.py`; `.ai/tasks/T372.task.yaml`; `.ai/handoffs/T372/handoff.md` |
| T373 | Owner implementation authorization | `t373`, `implementation-authorization`, `t374-next`, `parent-only`, `parent-first-pilot`, `post-pilot-review`, `child-necessity-review`, `child-span-denial`, `1cor8-10`, `output-changing`, `owner-options` | Auditing the exact T373-A owner authorization, parent-first pilot pattern, and post-pilot child review gate before the first route-isolated output-changing pilot. | `docs/roadmap/T373_OWNER_IMPLEMENTATION_AUTHORIZATION.md`; `.ai/control/t373_owner_implementation_authorization.yaml`; `.ai/control/owner_decision_option_presentation_policy.yaml`; `scripts/validate_t373_owner_implementation_authorization.py`; `scripts/validate_owner_decision_option_presentation_policy.py`; `.ai/tasks/T373.task.yaml`; `.ai/handoffs/T373/handoff.md` |
| T374 | Additive parent overlay implementation | `t374`, `baseline-overlap`, `owner-selection`, `selected-semantics`, `non-target-identity`, `additive-overlay`, `output-manifest`, `preserve-baseline`, `same-baseline`, `1cor8-10`, `audit` | Auditing the selected `T374-OVERLAP-B` additive parent overlay semantics, completed output manifest, and remaining non-authorizations before T375 review. | `docs/roadmap/T374_BASELINE_OVERLAP_OWNER_DECISION_PACKET.md`; `.ai/control/t374_baseline_overlap_owner_decision_packet.yaml`; `.ai/control/t374_additive_parent_overlay_manifest.yaml`; `scripts/validate_t374_baseline_overlap_owner_decision_packet.py`; `scripts/validate_t374_additive_parent_overlay.py`; `.ai/tasks/T374.task.yaml`; `.ai/handoffs/T374/handoff.md` |
| T375 | Post-pilot review | `t375`, `post-pilot-review`, `child-necessity-review`, `same-baseline`, `no-context-audit`, `t376-next`, `1cor8-10`, `non-authorizing` | Auditing the completed T374 post-pilot review and why child spans are not necessary now. | `docs/roadmap/T375_POST_PILOT_REVIEW.md`; `.ai/control/t375_post_pilot_review.yaml`; `.ai/audits/reports/20260620-T375-post-pilot-review.md`; `scripts/validate_t375_post_pilot_review.py`; `.ai/tasks/T375.task.yaml`; `.ai/handoffs/T375/handoff.md` |
| T376 | Epistle research runway | `t376`, `t384`, `research-runway`, `research-autonomy`, `authority-boundary`, `epistle`, `target-options`, `non-authorizing` | Auditing the selected T376-A epistle argument research/prep runway or preparing the next T384 options matrix without authorizing target selection or output. | `.ai/control/t376_epistle_research_runway.yaml`; `docs/roadmap/T376_EPISTLE_RESEARCH_RUNWAY.md`; `.ai/audits/reports/20260621-T376-epistle-research-runway.md`; `scripts/validate_t376_epistle_research_runway.py`; `.ai/tasks/T376.task.yaml`; `.ai/handoffs/T376/handoff.md` |
| T384 | Bible-wide research readiness synthesis | `t384`, `t385`, `bible-wide-readiness`, `research-synthesis`, `human-decision-map`, `ready-lanes`, `blocked-authority`, `chunking-ready`, `non-authorizing` | Auditing the completed Bible-wide research/readiness synthesis or preparing the next T385 owner decision packet without authorizing target selection, reviewed gold, child spans, output, graph/retrieval/vector truth, route/evaluator behavior, boundary import, or theology authority. | `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`; `docs/roadmap/T384_BIBLE_WIDE_RESEARCH_READINESS_SYNTHESIS.md`; `.ai/audits/reports/20260621-T384-bible-wide-research-readiness.md`; `scripts/validate_t384_bible_wide_research_readiness.py`; `.ai/tasks/T384.task.yaml`; `.ai/handoffs/T384/handoff.md` |
| T386 | Bible-wide verse/passage coverage inventory | `t386`, `t385`, `verse-passage-coverage`, `coverage-inventory`, `coverage-taxonomy`, `readiness-matrix`, `gap-register`, `human-review-docket`, `canonical-66`, `source-metadata-sensitive`, `textual-variant`, `intertext-risk`, `wj-risk`, `non-orthodox-pressure`, `blocked-authority`, `non-authorizing` | Proving every canonical passage is accounted for at triage depth before chunking resumes, or preparing T385 with coverage gaps, owner decisions, and target-passage risk flags. | `.ai/control/bible_verse_passage_coverage_summary.yaml`; `.ai/control/bible_verse_passage_coverage_inventory.jsonl`; `.ai/control/bible_verse_passage_gap_register.yaml`; `.ai/control/bible_verse_passage_human_review_docket.yaml`; `docs/roadmap/T386_BIBLE_VERSE_PASSAGE_COVERAGE_INVENTORY.md`; `scripts/validate_bible_verse_passage_coverage_inventory.py`; `.ai/tasks/T386.task.yaml`; `.ai/handoffs/T386/handoff.md` |
| T387 | Manuscript witness reliability scaffold | `t387`, `manuscript-witness`, `reliability`, `provenance`, `oldest-fragments`, `dead-sea-scrolls`, `nt-papyri`, `codices`, `copy-abundance`, `discovery-timeline`, `non-authorizing` | Planning canonical Scripture manuscript-witness metadata, variants, discovery timeline, and reliability evidence without importing text, selecting preferred readings, changing canonical records, or creating graph/retrieval/vector truth. | `.ai/control/manuscript_witness_reliability_scaffold.yaml`; `docs/roadmap/T387_MANUSCRIPT_WITNESS_RELIABILITY_SCAFFOLD.md`; `scripts/validate_manuscript_witness_reliability_scaffold.py`; `.ai/tasks/T387.task.yaml`; `.ai/handoffs/T387/handoff.md` |
| T389 | Chunking launch readiness report | `t389`, `t390`, `t385`, `launch-readiness`, `clean-trunk`, `chunking-ready`, `next-route`, `blocked-authority`, `non-authorizing` | Auditing the current go/no-go state after branch reconciliation and T390 manuscript source-catalog metadata planning, or preparing the T385 owner decision packet without authorizing target selection, output, reviewed gold, child spans, route/evaluator behavior, graph/retrieval/vector truth, boundary import, preferred readings, source-tradition preference, canon-scope change, database creation, row population, or theology authority. | `docs/roadmap/T389_CHUNKING_LAUNCH_READINESS_REPORT.md`; `.ai/tasks/T389.task.yaml`; `.ai/handoffs/T389/handoff.md`; `.ai/control/manuscript_source_catalog_metadata_plan.yaml` |
| T390 | Manuscript source catalog metadata plan | `t390`, `source-catalog`, `metadata-plan`, `sqlite-plan`, `manuscript-witness`, `dead-sea-scrolls`, `nt-papyri`, `major-codices`, `holding-institutions`, `source-trust`, `anti-guessing`, `non-authorizing` | Planning SQLite-ready biblical manuscript source-catalog metadata before DSS/NT papyri/codices population, while routing church fathers, commentaries, reception, non-biblical DSS, theologian writings, and doctrine lineage outside Scripture Graph. | `.ai/control/manuscript_source_catalog_metadata_plan.yaml`; `docs/roadmap/T390_MANUSCRIPT_SOURCE_CATALOG_METADATA_PLAN.md`; `scripts/validate_manuscript_source_catalog_metadata_plan.py`; `.ai/tasks/T390.task.yaml`; `.ai/handoffs/T390/handoff.md` |
| T385 | Owner decision packet | `t385`, `owner-decision-packet`, `recommendation-not-selection`, `goal4`, `owner-gate`, `epistle`, `ephesians`, `target-selection`, `non-authorizing` | Auditing the completed T385 options packet or deciding whether Goal 4 can start. Use when a future agent needs the exact recommendation, all serious faithful options, or the stop rule that recommendation is not owner selection. | `.ai/control/t385_owner_decision_packet.yaml`; `docs/roadmap/T385_OWNER_DECISION_PACKET.md`; `scripts/validate_t385_owner_decision_packet.py`; `.ai/tasks/T385.task.yaml`; `.ai/handoffs/T385/handoff.md` |
| T382 | Chunking lesson index | `t382`, `lessons-learned`, `lesson-index`, `lesson-graph`, `preflight`, `midflight`, `postflight`, `workflow-governance`, `non-authorizing` | A reusable lesson must be discovered, tagged, routed into preflight/workflow/register surfaces, or validated after lesson/preflight/methodology/TOC/audit changes. | `docs/roadmap/T382_CHUNKING_LESSON_INDEX.md`; `.ai/control/chunking_lesson_index.yaml`; `scripts/validate_chunking_lesson_index.py`; `.ai/tasks/T382.task.yaml`; `.ai/handoffs/T382/handoff.md` |
| T383 | Contextual reading policy | `t383`, `contextual-reading`, `context`, `prooftexting`, `immediate-context`, `paragraph-context`, `chapter-context`, `book-context`, `canonical-context`, `historical-context`, `non-authorizing` | Future Bible reading, chunking, review packets, intertexts, historical/cultural notes, or source-metadata observations need layered context before use. | `docs/roadmap/T383_CONTEXTUAL_READING_POLICY.md`; `.ai/control/contextual_reading_policy.yaml`; `scripts/validate_contextual_reading_policy.py`; `.ai/tasks/T383.task.yaml`; `.ai/handoffs/T383/handoff.md` |

## Review Packet Surfaces

| Surface | Tags | Use when | Role |
| --- | --- | --- | --- |
| `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md` | `review-packet`, `promotion-queue`, `human-readable` | A reviewer needs the packet queue and human-facing packet status. | Human-readable index and promotion queue. |
| `eval/chunking_gold/review_packets/review_packet_index.json` | `review-packet`, `machine-readable`, `validator` | A validator or agent needs structured packet status. | Machine-readable review-packet index. |
| `eval/chunking_gold/per_form/psalms_gold_manifest.json` | `reviewed-gold`, `psalms`, `manifest` | Work touches approved Psalm reviewed-gold spans. | Psalm reviewed-gold and structural-split manifest. |
| `.ai/control/chunking_theological_decision_register.yaml` | `theology-risk`, `decision-register`, `downstream-risk` | A chunking/evaluator/gold/route/default decision may affect theological interpretation. | Decision ledger for chunking choices with possible theological downstream effects. |
| `.ai/control/governance_memory_durability_policy.yaml` | `governance-memory`, `decision-register-protection`, `protected-paths` | An agent needs to prove the decision register remains discoverable, canonical, active, protected, and validator-enforced. | Register durability policy; no register deletion, downgrade, output, gold, or owner authority. |
| `.ai/control/owner_decision_projection_policy.yaml` | `owner-projection`, `projected-owner-pattern`, `conflict-scan`, `theology-risk` | A future decision may be the same shape as a prior owner decision or may conflict with a prior decision for the target text. | Projection policy; allows only high-confidence conservative non-output projections and stops for conflicts. |
| `.ai/control/bible_chunking_readiness_map.yaml` | `readiness`, `next-route`, `whole-bible` | A future agent needs the active route and lane readiness. | Lane/readiness map for whole-Bible chunking. |
| `.ai/control/chunking_agent_preflight.yaml` | `preflight`, `source-metadata`, `required-reading` | Any chunking-related work starts or a lesson must be encoded. | Mandatory preflight for chunking agents; source metadata is evidence, not authority. |
| `.ai/control/chunking_lesson_index.yaml` | `lessons-learned`, `lesson-index`, `lesson-graph`, `preflight`, `midflight`, `postflight`, `workflow-governance` | Future agents need to find applicable lessons by tag/category/use-when trigger, or a task changes lesson/preflight/methodology/register/audit/TOC surfaces. | Tagged lesson TOC/graph; routes lessons to preflight/workflow/register surfaces and authorizes no output, reviewed gold, graph/retrieval truth, route/evaluator behavior, or theology claims. |
| `.ai/control/contextual_reading_policy.yaml` | `contextual-reading`, `context`, `prooftexting`, `immediate-context`, `paragraph-context`, `chapter-context`, `book-context`, `canonical-context`, `historical-context` | A future agent needs layered context before reading, chunking, reviewing, linking, or citing a passage. | Contextual reading policy; requires context layers as evidence and authorizes no doctrine, reviewed gold, chunk boundary, graph/retrieval truth, output change, or history repo. |
| `.ai/control/divine_capitalization_inventory.yaml` | `divine-capitalization`, `source-metadata`, `evidence-only` | Work touches God/god, Spirit/spirit, Father/father, Word/word, or capitalization evidence. | Observed divine-name/title/pronoun capitalization variants; evidence only, not graph/chunk/retrieval authority. |
| `.ai/control/wj_marker_inventory.yaml` | `wj`, `red-letter`, `source-metadata`, `evidence-only` | Work touches words-of-Jesus markers or red-letter formatting. | Observed WJ/red-letter marker token runs; evidence only, not speaker/chunk/graph/retrieval authority. |
| `.ai/control/wj_speaker_discourse_policy.yaml` | `wj-speaker`, `john3`, `policy`, `owner-review` | Work weighs WJ/speaker/discourse evidence before owner review. | Policy for weighing WJ/speaker/discourse evidence; selects John 3 for owner review only. |
| `.ai/control/john3_wj_owner_review_docket.yaml` | `john3`, `owner-review`, `current-route`, `non-authorizing` | Owner needs John 3 options or an agent needs to know what is still pending. | Pending John 3 owner-review options; no parent/child/speaker/chunk approval. |
| `.ai/control/bible_wide_chunking_research_registry.yaml` | `whole-bible-research`, `canonical-66`, `research-registry`, `book-watchpoints` | Future agents need book-level research prompts before exact review packets or algorithms. | Canonical 66-book research queue; no chunk/gold/graph/output authority. |
| `.ai/control/source_metadata_research_atlas.yaml` | `source-metadata-atlas`, `cross-references`, `strongs`, `wj`, `capitalization` | Future agents need source metadata families, observed surfaces, and non-authorizations before chunk/graph/retrieval work. | Metadata research atlas; no Scripture/lexical/intertext/speaker/graph/chunk/retrieval/output authority. |
| `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml` | `apocalyptic-prophetic`, `revelation`, `daniel`, `intertext`, `hermeneutic-neutrality` | Future agents need Revelation/Daniel/prophetic intertext dossiers before exact packets or algorithm work. | Dossier queue; no intertext/graph/retrieval/chunk/output authority. |
| `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml` | `epistle`, `argument-boundary`, `election`, `law-gospel`, `faith-works`, `assurance` | Future agents need epistle theological issue dossiers before exact packet review, route, graph, retrieval, or algorithm work. | Dossier queue; no doctrine/reviewed-gold/graph/retrieval/chunk/output authority. |
| `.ai/control/gospel_wj_discourse_dossier_queue.yaml` | `gospel-discourse-wj`, `red-letter`, `speaker-boundary`, `john3`, `sermon-on-mount`, `farewell-discourse`, `dominical-quotation` | Future agents need Gospel/WJ discourse dossiers before exact packet review, route, graph, retrieval, or algorithm work. | Dossier queue; no speaker/discourse/reviewed-gold/graph/retrieval/chunk/output authority. |
| `.ai/control/narrative_legal_covenant_dossier_queue.yaml` | `narrative`, `legal`, `covenant`, `genealogy`, `lists`, `typology`, `harmonization` | Future agents need narrative/legal/covenant dossiers before exact packet review, route, graph, retrieval, or algorithm work. | Dossier queue; no covenant/law-gospel/typology/graph/retrieval/chunk/output authority. |
| `.ai/control/wisdom_dialogue_poetry_dossier_queue.yaml` | `wisdom`, `dialogue`, `poetry`, `acrostic`, `refrain`, `speaker-boundary`, `job`, `song`, `lamentations`, `ps119` | Future agents need wisdom/dialogue/poetry dossiers before exact packet review, route, graph, retrieval, or algorithm work. | Dossier queue; no wisdom/speaker/graph/retrieval/chunk/output authority. |
| `.ai/control/prophetic_oracle_vision_dossier_queue.yaml` | `prophetic`, `oracle`, `vision`, `servant-song`, `temple-vision`, `day-of-yahweh`, `fulfillment`, `israel-church`, `messianic`, `zechariah` | Future agents need prophetic/oracle/vision dossiers before exact packet review, route, graph, retrieval, or algorithm work. | Dossier queue; no fulfillment/eschatology/covenant/Israel-church/messianic/temple/graph/retrieval/chunk/output authority. |
| `.ai/control/textual_variant_source_tradition_dossier_queue.yaml` | `textual-variant`, `source-tradition`, `canon-scope`, `boundary-routing`, `mark16`, `pericope-adulterae`, `deut32`, `jude`, `comma-johanneum` | Future agents need textual-variant/source-tradition dossiers before exact packet review, route, graph, retrieval, boundary, or algorithm work. | Dossier queue; no textual-critical/canon/source-tradition/boundary-import/noncanonical/graph/retrieval/chunk/output authority. |
| `.ai/control/orthodox_original_language_pressure_dossier_queue.yaml` | `original-language`, `grammar-overlay`, `greek`, `hebrew`, `non-orthodox`, `lds`, `watch-tower`, `nwt`, `trinity`, `christology`, `divine-plurality` | Future agents need Greek/Hebrew pressure-passage dossiers before exact packet review, route, graph, retrieval, boundary, or algorithm work. | Dossier queue; no source-language, translation, non-orthodox source, external-source, doctrine, graph, retrieval, reviewed-gold, chunk, canon, boundary, vector, or output authority. |
| `.ai/control/original_language_phrase_context_policy.yaml` | `original-language`, `phrase/context`, `greek`, `hebrew`, `isolated word`, `lemma`, `syntax`, `discourse`, `root-fallacy`, `semantic-range`, `interlinear`, `greek-article`, `hebrew-plural`, `lxx`, `textual-variant`, `punctuation`, `poetry` | Future agents include Greek/Hebrew word evidence and need to avoid isolated-word, one-gloss, root, article, plural-form, LXX, punctuation, or discourse-marker prooftexting. | Policy surface; requires phrase, clause, syntax, discourse, textual, genre, and canonical context while authorizing no doctrine, graph, retrieval, chunk, reviewed-gold, route/evaluator, or output authority. |
| `.ai/control/orthodox_hermeneutic_firewall_docket.yaml` | `orthodox-hermeneutic-firewall`, `anti-smuggling`, `orthodoxy-boundary`, `canon-authority` | Future epistle, graph, retrieval, or chunking work might smuggle hidden anti-orthodox defaults. | Firewall docket; affirms Nicene/Chalcedonian and canonical Scripture commitments; no denominational-system/chunk/output authority. |
| `.ai/control/textual_critical_policy_docket.yaml` | `textual-critical-policy`, `variant-sensitive`, `canon-scope-gate`, `source-tradition-gate` | Variant-sensitive packets might be promoted, implemented, used as reviewed gold, or used for canon/source-tradition/boundary decisions. | Policy requirement docket; records selected `TCP-T378-B` case-by-case policy while denying preferred-reading/canon/boundary/output authority. |
| `.ai/control/textual_critical_policy_owner_options.yaml` | `textual-critical-policy`, `owner-options`, `variant-sensitive`, `case-by-case`, `1cor9-20`, `1cor10-9`, `reviewed-gold-blocker` | T371 or another variant-sensitive packet needs owner policy options before promotion. | Owner options docket; records T379 selection of `TCP-T378-B` but no preferred reading, source-tradition preference, reviewed gold, graph/retrieval truth, chunk boundary, or output authority. |
| `.ai/control/textual_critical_case_policy.yaml` | `textual-critical-policy`, `case-policy`, `selected-policy`, `owner-confirmation`, `ODP-005`, `variant-dependency` | Future agents need the selected case-by-case process policy for variant-sensitive gates. | Selected `TCP-T378-B` process policy; no preferred reading, source-tradition preference, dependency projection, reviewed gold, graph/retrieval truth, route/evaluator behavior, chunk boundary, implementation, or output authority. |
| `.ai/control/t371_variant_dependency_owner_decision_packet.yaml` | `t371`, `variant-dependency`, `owner-decision-packet`, `reviewed-gold-promotion`, `1cor9-20`, `1cor10-9`, `parent-only` | Owner or auditor needs the exact T371 options before parent-only reviewed-gold promotion. | Owner decision packet; conditionally recommends T371-A only if the owner confirms variant non-dependency and preserves T371-B as the conservative hold; no dependency finding, reviewed gold, output, route, graph, retrieval, or implementation authority. |
| `.ai/control/t371_parent_only_reviewed_gold_promotion.yaml` | `t371-a`, `reviewed-gold`, `variant-non-dependent`, `parent-only`, `1cor8-10` | T372 harness work or an audit needs the exact owner-confirmed promotion boundary and its limits. | T371-A promotion record; authorizes only parent-only reviewed gold for `1Cor.8.1-1Cor.10.33` and denies child, route, graph, retrieval, implementation, and output authority. |
| `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json` | `reviewed-gold`, `epistle`, `manifest`, `1cor8-10`, `parent-only` | A future implementation or audit needs the machine-readable epistle argument reviewed-gold case. | Reviewed-gold manifest; currently records the T371-A parent-only case without child-span, route, evaluator, graph, retrieval, implementation, or output authority. |
| `.ai/control/t372_route_isolation_harness_plan.yaml` | `t372`, `route-isolation`, `non-target-identity`, `harness-plan`, `owner-gate` | T373 gate work or an audit needs the non-output-changing implementation requirements before any T374 work. | Harness plan; requires owner authorization, non-target identity, same-baseline planning, and source-metadata denial while authorizing no implementation or output. |
| `.ai/control/t373_owner_implementation_authorization.yaml` | `t373`, `implementation-authorization`, `t374-next`, `parent-only`, `parent-first-pilot`, `post-pilot-review`, `child-necessity-review`, `child-span-denial`, `output-changing` | T374 implementation work or an audit needs exact owner authorization, parent-first pilot pattern, post-pilot child review gate, and the limits on child spans, scope, and output authority. | Authorization record; authorizes only the exact parent-only `1Cor.8.1-1Cor.10.33` pilot and the reusable parent-first pilot/post-pilot child review pattern; requires non-target identity, same-baseline evaluation, changed-output manifest, decision-register update, validators/tests, no-context audit surface, and post-pilot child-necessity review gate. |
| `.ai/control/t374_baseline_overlap_owner_decision_packet.yaml` | `t374`, `baseline-overlap`, `owner-selection`, `selected-semantics`, `non-target-identity`, `additive-overlay`, `preserve-baseline`, `no-replacement` | T374 implementation work or an audit needs the selected additive parent overlay semantics before any chunk change. | Owner selection packet; records the current baseline overlap across `1Cor.7.25-1Cor.9.2`, `1Cor.9.3-1Cor.10.5`, and `1Cor.10.6-1Cor.11.10`; records selected `T374-OVERLAP-B`; authorizes no output in the selection record. |
| `.ai/control/t374_additive_parent_overlay_manifest.yaml` | `t374`, `output-manifest`, `additive-overlay`, `preserve-baseline`, `same-baseline`, `no-context-audit`, `cd-056`, `t375-next` | T375 review or an audit needs the actual output-change proof and hashes. | Implementation manifest; records one appended parent-only overlay, preserved baseline-prefix hash, same-baseline metrics, audit report, decision-register entry, and non-authorizations. |
| `.ai/control/t375_post_pilot_review.yaml` | `t375`, `post-pilot-review`, `child-necessity-review`, `same-baseline`, `no-context-audit`, `cd-057`, `t376-next` | T376 work or an audit needs to know why child spans are not necessary now and why owner lane selection is next. | Post-pilot review; records same-baseline/no-context audit review, child-span non-promotion, and no output/route/evaluator/graph/retrieval authority. |
| `.ai/control/t376_epistle_research_runway.yaml` | `t376`, `t384`, `research-runway`, `research-autonomy`, `authority-boundary`, `epistle`, `target-options` | T384 work or an audit needs to know why epistle research/options may continue and where authority-changing work must stop. | T376-A runway; authorizes non-output research/prep only and denies target selection, reviewed gold, child spans, output, graph/retrieval/vector truth, route/evaluator behavior, boundary import, and theology authority. |
| `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml` | `t384`, `t385`, `bible-wide-readiness`, `research-synthesis`, `human-decision-map`, `ready-lanes`, `blocked-authority`, `chunking-ready` | T385 owner-packet work or an audit needs the compiled ready lanes, research gaps, human decisions, blocked authority changes, and exact next step. | T384 synthesis; records HDM-001 through HDM-007 and points to T385 while denying target selection, reviewed gold, child spans, output, graph/retrieval/vector truth, route/evaluator behavior, boundary import, source-tradition preference, canon-scope change, and theology authority. |
| `.ai/control/manuscript_witness_reliability_scaffold.yaml` | `manuscript-witness`, `reliability`, `provenance`, `oldest-fragments`, `dead-sea-scrolls`, `nt-papyri`, `codices`, `copy-abundance`, `discovery-timeline` | A future agent plans manuscript-witness metadata, variants, discovery timeline, or reliability reports. | T387 scaffold; plans `scripture_*` and `evidence_*` database surfaces while denying source-text import, canonical record changes, preferred readings, boundary imports, graph/retrieval/vector truth, and apologetic authority. |
| `.ai/control/manuscript_source_catalog_metadata_plan.yaml` | `source-catalog`, `metadata-plan`, `sqlite-plan`, `manuscript-witness`, `dead-sea-scrolls`, `nt-papyri`, `major-codices`, `holding-institutions`, `source-trust`, `anti-guessing` | A future agent plans or audits biblical manuscript source-catalog metadata, official source anchors, SQLite-ready fields, or future DSS/NT papyri/codices population. | T390 plan; defines metadata-only `scripture_*` and `evidence_*` tables, source trust rules, review statuses, and future goal prompts while denying SQLite creation, row population, text import, preferred readings, graph/retrieval/vector truth, boundary import, and apologetic authority. |
| `.ai/control/t385_owner_decision_packet.yaml` | `owner-decision-packet`, `recommendation-not-selection`, `t385`, `goal4`, `epistle`, `ephesians`, `non-authorizing` | A future agent needs to know which target is recommended next, whether the owner has selected it, or what is blocked before Goal 4. | T385 packet; recommends T385-A Eph.1.3-Eph.1.14 but keeps owner selection pending and denies review-packet strengthening, reviewed gold, child spans, output, route/evaluator behavior, graph/retrieval/vector truth, preferred readings/source traditions, canon scope, and theology authority. |
| `.ai/control/owner_decision_option_presentation_policy.yaml` | `owner-options`, `decision-presentation`, `human-decision`, `recommendation`, `non-authorizations` | A future owner gate needs options, repercussions, risks, and recommendations before the owner decides. | Presentation policy; requires serious faithful options and repercussions while authorizing no output by itself. |
| `.ai/control/1cor8_10_epistle_owner_review_docket.yaml` | `1cor8-10`, `epistle`, `owner-review`, `conscience`, `idol-food`, `sacramental` | Work touches 1 Corinthians 8-10 or the projected parent-only selection after packet strengthening. | Owner-review docket; no child/doctrine/gold/chunk/output authority. |
| `eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml` | `1cor8-10`, `evidence-packet`, `reviewed-gold-promotion`, `source-metadata`, `parent-only` | Work audits T370 evidence or prepares the T371 owner promotion decision. | Parent-only evidence packet; not reviewed gold and no child/route/evaluator/graph/retrieval/output authority. |
| `.ai/control/chunking_human_decision_forecast.yaml` | `human-decision`, `chunking-ready`, `goal-blocked`, `stop-conditions`, `owner-gate` | Work needs to know which predictable owner decisions can be made early before chunk-output work starts. | Decision forecast; defines readiness and stop conditions without authorizing output. |

## Current Next Route

After T344 owner decision, T351 Bible-wide triage, T367 owner firewall guidance, T368 packet
strengthening, T369 projected parent-only owner-pattern selection, T370 parent-only evidence
prep, T380 T371 owner-decision packet prep, T371-A parent-only reviewed-gold promotion, and T372
route-isolation harness planning, T373-A owner implementation authorization selected the exact
parent-only implementation pilot. T374 implemented the exact additive parent overlay, T375
completed the post-pilot review, and T376-A selected the epistle argument research/prep runway.
T384 completed the Bible-wide research/readiness synthesis and did not authorize output or target
selection. T385 completed the owner decision packet and did not authorize owner selection.
The next gate is:

```text
Owner must explicitly select one T385 option before Goal 4 review-packet strengthening
```

T367 records `JOHN3-T356-B` as the selected parent-only `John.3.1-John.3.36` review target,
adds the Orthodox Hermeneutic Firewall and textual-critical policy docket requirement, and points
the epistle lane to 1Cor.8-10. T368 strengthens the packet and creates
`.ai/control/1cor8_10_epistle_owner_review_docket.yaml`. T369 selects parent-only
`1Cor.8.1-1Cor.10.33` by projected owner pattern after a no-conflict scan. T370 builds the
parent-only evidence packet. T380 adds `.ai/control/t371_variant_dependency_owner_decision_packet.yaml`.
T371-A then records the owner response in `.ai/control/t371_parent_only_reviewed_gold_promotion.yaml`
and `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json`: the parent-only boundary
and reviewed-gold claim are variant-non-dependent for `1Cor.9.20` and `1Cor.10.9`, and only
`1Cor.8.1-1Cor.10.33` is promoted as parent-only reviewed gold. T372 then records
`.ai/control/t372_route_isolation_harness_plan.yaml` as a non-output-changing harness plan; it
requires T373 owner authorization, non-target identity proof, and same-baseline planning before
T374 can start. T373 records that authorization in
`.ai/control/t373_owner_implementation_authorization.yaml`: T374 may implement only the exact
parent-only `1Cor.8.1-1Cor.10.33` pilot. Child spans remain disallowed unless later exact reviewed
child-span evidence and owner promotion authorize them. T374 then found the baseline overlap,
recorded selected `T374-OVERLAP-B` in `.ai/control/t374_baseline_overlap_owner_decision_packet.yaml`,
and implemented one exact additive parent overlay recorded in
`.ai/control/t374_additive_parent_overlay_manifest.yaml`. T375 records
`.ai/control/t375_post_pilot_review.yaml`: same-baseline/no-context audit review is complete,
child spans are not necessary now, and T376 then selected the epistle argument research/prep runway.
T384 records `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`: ready lanes,
research gaps, human decisions `HDM-001` through `HDM-007`, blocked authority changes, and T385 as
the next owner decision packet.
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
route behavior, or output changes. T367 does not authorize John 3 child spans, Jesus/narrator
boundary decisions, reviewed-gold promotion, route behavior, graph/retrieval truth, textual-critical
policy selection, or output changes.
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
T363 does not authorize covenant theology, law/gospel framework selection, typology,
harmonization, source-critical partition, pending packet approval, reviewed-gold promotion, route
behavior, evaluator changes, graph edges, retrieval truth, chunk boundaries, output changes,
boundary import, or T345.
T364 does not authorize wisdom theology, Job theodicy selection, Ecclesiastes frame selection, Song
allegorical/literal system selection, speaker attribution, speaker boundaries, liturgical use,
pending packet approval, reviewed-gold promotion, route behavior, evaluator changes, graph edges,
retrieval truth, chunk boundaries, output changes, boundary import, or T345.
T365 does not authorize fulfillment theology, eschatological system selection, covenant system
selection, Israel/church relation, messianic identification, temple theology, prophetic chronology,
pending packet approval, reviewed-gold promotion, route behavior, evaluator changes, graph edges,
retrieval truth, intertext truth, chunk boundaries, output changes, boundary import, or T345.
T366 does not authorize textual-critical decision selection, canon-scope change, source-tradition
preference, noncanonical source authority, boundary import, pending packet approval,
reviewed-gold promotion, route behavior, evaluator changes, graph edges, retrieval truth,
intertext truth, chunk boundaries, output changes, or T345.
T368 may only strengthen the existing `1Cor.8-1Cor.10` packet as review prep; it may not promote
reviewed gold, implement chunks, change route/evaluator behavior, generate graph edges, assert
retrieval truth, select textual-critical policy, or change output.
T369 selected parent-only `1Cor.8.1-1Cor.10.33` by projected owner pattern; it did not select
child spans and did not authorize reviewed gold, chunks, route/evaluator behavior, graph edges,
retrieval truth, textual-critical policy, or output changes. T370 prepared governed parent-only
evidence only; it did not promote reviewed gold, implement chunks, project child spans, ignore
conflicting prior owner decisions, change route/evaluator behavior, generate graph edges, assert
retrieval truth, select textual-critical policy, or change output. T371-A promotes only parent-only
reviewed gold; it still cannot implement chunks, select child spans, treat the parent as a chunk
boundary, change route/evaluator behavior, create graph/retrieval/vector output, or change output.
T372 records only the route-isolation harness plan; it cannot implement chunks, select child spans,
treat parent-only gold as an output boundary, change route/evaluator behavior, create
graph/retrieval/vector output, or change output. T373 records the owner-selected T373-A exact
parent-only implementation authorization; T374 implemented the route-isolated additive parent overlay
limited to 1Cor.8.1-1Cor.10.33 with no child spans. T373 also records the owner-authorized
parent-first pilot pattern: run the exact parent-only pilot, then review whether child spans are
necessary before any later child-span work. T374 records a baseline-overlap selection and a separate
implementation manifest; T375 is complete, T376 selected the epistle argument research/prep runway,
and T384 completed the Bible-wide research/readiness synthesis. T385 owner decision packet is now
the next non-output step.
T377 records original-language pressure-passage review memory; it does not authorize Greek/Hebrew
as automatic truth, translation preference, non-orthodox source authority, extra-canonical source
authority, doctrine selection, graph/retrieval truth, reviewed gold, chunk boundaries, canon-scope
changes, boundary import, route/evaluator changes, vectors, or output changes.
T378 records textual-critical policy owner options and recommends case-by-case owner policy for
variant-sensitive promotion gates. T379 records owner selection of `TCP-T378-B` as the standing
case-by-case process policy and adds `ODP-005` so future agents remember the pattern. It does not
select preferred readings, source-tradition preference, dependency findings, reviewed gold,
graph/retrieval truth, chunk boundaries, route/evaluator changes, implementation, or output
changes. T371 now asks the narrower owner question: whether the parent-only boundary and
reviewed-gold claim are variant-non-dependent for `1Cor.9.20` and `1Cor.10.9`, and whether
parent-only promotion is authorized.
