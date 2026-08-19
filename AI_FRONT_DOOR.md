# AI Front Door

This file is the required entry point for every AI agent and human contributor.
It is the stable operating-rules surface. Task-specific T3xx/T4xx history lives in `docs/roadmap/TASK_LEDGER.md`; searchable tag/use-when routing lives in `AI_TABLE_OF_CONTENTS.md` and `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`.

## Public Orientation — Read This First

**Mission:** build a governed, provenance-first Scripture knowledge/data plane for
Christian study, teaching, discipleship, search, and future AI-assisted ministry tools.
This repository is not an autonomous theological authority or the future agent runtime.

**Current reality:** source ingestion, canonical passage/witness identities, schemas,
validation, reviewed chunking pilots, candidate knowledge-graph evidence, and a
metadata-only learning-loop adapter exist. Whole-Bible M7/M8 chunk maps remain research
candidates. Production graph/retrieval serving and a remote MCP server do not yet exist.

**MCP boundary:** `.digital-asset/dad-integration.json` declares local stdio read-only
MCP only. Remote MCP and repository-write tools are disabled. A future server belongs in
the separate runtime plane and must consume versioned validated releases.

**Public project map:** read
[`docs/architecture/PUBLIC_PROJECT_OVERVIEW.md`](docs/architecture/PUBLIC_PROJECT_OVERVIEW.md)
for the repository family, current/planned capability matrix, engineering portfolio,
release Bronze/Silver/Gold ladder, M7/M8 state, and PR 194 publication plan. Release
Gold is not the same as the repo's narrow **reviewed-gold** chunk-evidence label.

**Research publication state (2026-08-18):** PR 194's 5,923-file conflicting research
container was closed without merge after the clean public-entry PR 195 merged. Do not
recreate that combined diff. Use the separate M7 candidate publication, continued
owner-bound M8 checkpoints, and M7/M8 comparison only after M8 is complete.

**M7 transparency:** read
[`docs/architecture/M7_SOL_AGENT_SYSTEM.md`](docs/architecture/M7_SOL_AGENT_SYSTEM.md)
for the Sol role mesh, control/campaign agents, literary-form specialists, all-66-book
strategy routing, per-decision review flow, provenance graph, validation, and honest
independence limits. Then read the hash-bound
[`M7 Sol candidate publication`](docs/publications/m7-sol-candidate-v1/README.md) for
separate coverage measures, immutable evidence pointers, Psalm failure/repair history,
the Job worked example, and the gate that keeps M8 and convergence out of this task.

## Mandatory Read Order

Read these before making changes:

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` - human-gated architecture authority, read only for AI
3. `.ai/control/PROJECT_STATUS.md` - current operational state
4. `.ai/control/DATA_MAP.md` - generated data and pipeline endpoint map
5. `.ai/control/RAW_SOURCE_INVENTORY.md` - actual raw documents; mandatory before ingest/chunking/graph work
6. `ROADMAP.md`
7. `ROADMAP_STATE.yaml`
8. `HANDOFF_PROTOCOL.md`
9. `docs/architecture/ARCHITECTURE.md`
10. `docs/chunking/CHUNKING_DESIGN.md`
11. `AI_TABLE_OF_CONTENTS.md` - functional tag index and routing surface
12. `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md` - roadmap/task tag index
13. `docs/roadmap/TASK_LEDGER.md` - T3xx/T4xx task-history ledger and moved front-door narrative
14. `.ai/control/chunking_agent_preflight.yaml` before any ingest, chunking, review-packet, evaluator, route, graph, or retrieval work
15. `.ai/control/contextual_reading_policy.yaml` before context-sensitive Bible reading, chunking, review packets, intertexts, historical/cultural background, or proof-texting risk
16. `.ai/control/chunking_lesson_index.yaml` before reusable lesson discovery or lesson/preflight/methodology/TOC/register/audit changes
17. `.ai/control/test_runtime_preflight.yaml` before repo-wide validation, `python scripts/validate_all.py`, `python -m pytest -q`, Rust-backed validators, or after timeout/temp/Cargo access failures
18. `.ai/control/coding_runtime_language_preflight.yaml` before adding validators, scanners, importers, build scripts, CI hot paths, high-resource deterministic code, or Rust-first runtime decisions
19. `.ai/control/ai_pr_lifecycle_policy.yaml` before leaving any AI-created draft branch, staged work, or PR unmerged
20. `config/agents/agent_roles.yaml`
21. `.ai/control/llos_v1_adapter.yaml` before any Logos Learning Loop Operating Standard (LLOS) reference, DAD coordination, or proposed delivery into Logos
22. `.ai/handoffs/<active_task_id>/handoff.md` - see `.ai/control/PROJECT_STATUS.md`
23. The specific files in the task scope

New or lower-capability agents: read `.ai/handoffs/AGENT_ROUTING_GUIDE.md` after this front door.

Independent reviewers or no-context A/B/red-team agents: read `.ai/audits/README.md` and `.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md` after this front door. Those files define the repo-resident no-context A/B/red-team audit path, changelogs, report location, validators, harness roadmap, and stop conditions.

## Cross-repo governance

This repository is the governed Scripture data-plane / knowledge-plane implementation for upstream `logos-governance-architecture`. The link type is `governance_contract`, recorded in `config/governance/repository_link_contract.yaml`. The upstream registry source of truth is `logos-governance-architecture/governance/LOGOS_REPO_REGISTRY.yaml`.

This repo also keeps a non-authorizing governance dependency-map mirror at `.ai/control/governance_dependency_map_mirror.yaml`, validated by `scripts/validate_governance_dependency_map_mirror.py`. The upstream source of truth remains `logos-governance-architecture/governance/GOVERNANCE_DEPENDENCY_MAP.yaml`; the local mirror cannot override upstream governance, weaken governance, change Scripture data, import boundary material, or create graph/retrieval/vector truth.

Hierarchy:

```text
logos-governance-architecture
  -> upstream governance / theological architecture authority
  -> logos-scripture-graph
     -> deterministic Scripture data-plane implementation
     -> validated release artifacts for future runtime consumers
```

Agents must read `config/governance/repository_link_contract.yaml` and `config/agents/agent_hostile_policy.yaml` when work touches cross-repo structure, authority, trust zones, release contracts, or GitHub coordination. GitHub issues, project fields, generated model output, and DAD mail are coordination or candidate surfaces, not canonical governance truth.

The Scripture LLOS v1 adapter at `.ai/control/llos_v1_adapter.yaml` is metadata-only. It conceptually pins `logos-governance-architecture/governance/LOGOS_LEARNING_LOOP_OPERATING_STANDARD.yaml` surface `1.0.0`; upstream remains the source of truth. Communication is two-way with asymmetric writes: Logos-local tooling may write its own outbox and read or pull DAD central candidates; DAD may read approved Logos outboxes and write central DAD records. DAD may never push or write any file, including an inbox, into Logos; fresh approval cannot relax that boundary. The adapter does not authorize Scripture/canonical data changes, runtime output, or upstream governance changes.

## Canonical Scripture entry point

`logos-scripture-graph` owns canonical 66-book Scripture truth for the default Logos Scripture Graph scope. Use this repo for canonical 66-book Scripture passage records, canonical Scripture chunking, Scripture stress atlas and review packets, canonical Scripture gold/evaluator surfaces, and canonical Scripture graph outputs.

Standing Bible-first rule: the highest chunking priority is a highly reliable, near-perfect governed chunker for the canonical 66-book Bible. Chunks are retrieval objects with boundary evidence, not canonical text. LLM-proposed boundaries are candidates unless reviewed and governed.

Boundary/supporting material routes to `logos-boundary-literature`; cross-repo policy routes to `logos-governance-architecture`; future denominational/theological development over time routes to planned `logos-doctrine-genealogy` only after governance registration. Boundary text source intake belongs in `logos-boundary-literature`.

Boundary material may support background, reception, comparison, refutation, or scoped evidence, but it must not override, contaminate, or become equal authority to canonical Scripture.

Machine-readable local routing policy: `.ai/control/boundary_material_routing.yaml`.

```text
WARNING: Boundary-layer request conflicts with higher-authority governance.

The requested boundary-layer task appears to require changing or bypassing governance-layer policy, canonical Scripture authority, repository-link contracts, routing policy, trust hierarchy, or canonical scope.

Governance is binding authority, not an obstacle to optimize around.

Do not automate, route, or implement this change from the boundary layer. A human maintainer must review the conflict directly in the higher-authority repository.

Owner-reserved authorization required: only Lowell Wong, as project owner, may authorize a boundary-originated request to change higher-authority governance, canonical Scripture authority, repository-link contracts, canonical scope, trust hierarchy, or cross-repo policy. Contributor consensus, contributor volume, automated recommendation, agent routing, or boundary-layer operational need is not sufficient authority.
```

## Standing Non-Authorizations

Unless an exact later owner-gated task says otherwise, do not authorize: Scripture data mutation; raw text mutation; reviewed-gold promotion; chunk output; child spans; route/evaluator behavior; graph/retrieval/vector truth; embeddings/indexes; boundary import; source/manuscript rows; preferred readings or source-tradition preference; canon-scope change; theology authority; one-denomination systematic theology as chunk authority; anti-supernatural, anti-canonical, heterodox, liberal-critical, or hidden default assumptions.

Low-complexity means review eligibility only. Research autonomy is not authority autonomy. Recommendation is not owner selection. Source metadata is evidence, not authority. Internal cross-references, Strong's-style tags, footnotes, headings, WJ/red-letter markers, paragraph/poetry markers, alternate readings, edition formatting, and divine-name/title capitalization are evidence for review, not automatic chunk, graph, lexical, intertext, speaker, retrieval, or output authority.

Revelation is a future hard-book atlas/review-packet lane. Revelation implementation must wait until reviewed gold exists and must not leak globally. Non-Bible training/eval cases must not tune canonical Bible behavior; isolate corpora, routes, skills, objectives, eval sets, default retrieval policy. No boundary import. No T327G.

## Required Chunking And Review Anchors

Before chunking/review work, read `.ai/control/chunking_agent_preflight.yaml` and `docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md` rule `CHUNK-METADATA-001`.

Mandatory anchor strings preserved for validators and no-context routing: divine-name/title capitalization; divine_capitalization_inventory.yaml; God/god; Spirit/spirit; Word/word; graph edges; wj_marker_inventory.yaml; wj_speaker_discourse_policy.yaml; john3_wj_owner_review_docket.yaml; bible_wide_chunking_research_registry.yaml; source_metadata_research_atlas.yaml; Source metadata is evidence, not authority; scripts/validate_source_metadata_authority.py; internal cross-references; Strong's-style word numbers; apocalyptic_prophetic_intertext_dossier_queue.yaml; epistle_argument_theological_issue_dossier_queue.yaml; gospel_wj_discourse_dossier_queue.yaml; narrative_legal_covenant_dossier_queue.yaml; wisdom_dialogue_poetry_dossier_queue.yaml; prophetic_oracle_vision_dossier_queue.yaml; textual_variant_source_tradition_dossier_queue.yaml; orthodox_original_language_pressure_dossier_queue.yaml; original_language_phrase_context_policy.yaml; validate_original_language_phrase_context_policy.py; phrase/context; original-language; isolated word; root-fallacy; contextual_reading_policy.yaml; validate_contextual_reading_policy.py; contextual-reading; historical-context; chapter-context; orthodox_hermeneutic_firewall_docket.yaml; textual_critical_policy_docket.yaml; textual_critical_policy_owner_options.yaml; textual_critical_case_policy.yaml; TCP-T378-B; case-by-case; ODP-005; owner confirmation; validators/tests; t371_variant_dependency_owner_decision_packet.yaml; t371_parent_only_reviewed_gold_promotion.yaml; T371 owner-decision packet; T371-A; review_status: ready_for_owner_promotion_review; reviewed_gold_promoted: false; t372_route_isolation_harness_plan.yaml; T372 route-isolation harness plan; validate_t372_route_isolation_harness_plan.py; t373_owner_implementation_authorization.yaml; T373-A; post-pilot child-necessity review gate; validate_t373_owner_implementation_authorization.py; owner_decision_option_presentation_policy.yaml; serious faithful options; t374_baseline_overlap_owner_decision_packet.yaml; baseline overlap; T374-OVERLAP-B; t374_additive_parent_overlay_manifest.yaml; T374 additive parent overlay implementation manifest; validate_t374_additive_parent_overlay.py; t375_post_pilot_review.yaml; T376 owner lane selection; validate_t375_post_pilot_review.py; t376_epistle_research_runway.yaml; validate_t376_epistle_research_runway.py; T384 Bible-wide research/readiness synthesis; t384_bible_wide_research_readiness_synthesis.yaml; validate_t384_bible_wide_research_readiness.py; T385 owner decision packet; T385 owner decision packet is complete; t385_owner_decision_packet.yaml; T392; T393; T394; Eph.1.3-Eph.1.14; Goal 5; reviewed-gold promotion decision packet; validate_t392_eph1_review_packet_strengthening.py; t393_eph1_reviewed_gold_promotion_decision_packet.yaml; validate_t393_eph1_reviewed_gold_promotion_decision_packet.py; t394_eph1_parent_only_reviewed_gold_promotion.yaml; Goal 6 route-isolated harness; t397_eph1_route_isolation_harness.yaml; T397 Eph.1.3-Eph.1.14 route-isolation harness; scripts/chunking/route_isolation_harness.py; t398_bible_wide_phase_one_research_synthesis.yaml; T398 phase-one whole-corpus research synthesis; validate_t398_bible_wide_phase_one_research_synthesis.py; Goal 2 focused Bible-wide research; Do not select targets; Do not select preferred readings/source traditions; t399_focused_bible_wide_research_queue.yaml; T399 focused Bible-wide research queue; validate_t399_focused_bible_wide_research_queue.py; Goal 2 focused; t401_eph1_output_pilot_manifest.yaml; T401 Eph.1.3-Eph.1.14 output pilot; validate_t401_eph1_output_pilot.py; --disable-t401-eph1-overlay; post-pilot review; currently records T401 as the completed exact; post-pilot review as the next; t402_eph1_post_pilot_review.yaml; whole_bible_low_complexity_chunking_candidate_queue.yaml; T402 low-complexity candidate runway; validate_t402_low_complexity_chunking_runway.py; Low-complexity means review; ready for the first new output-changing chunk PR; cursor_low_risk_chunking_handoff.yaml; T404 Cursor low-risk; validate_cursor_low_risk_chunking_handoff.py; Cursor may not choose the target; low_risk_chunking_multi_pass_plan.yaml; parallel_chunking_research_program.yaml; validate_parallel_chunking_prompt_pack.py; all_66_book_candidate_triage; bible_verse_passage_coverage_inventory.jsonl; bible_verse_passage_human_review_docket.yaml; T386 Bible-wide verse/passage coverage; test_runtime_preflight.yaml; coding_runtime_language_preflight.yaml; Rust-first; high-resource deterministic code; python -m pytest -q; 900000; chunking_lesson_index.yaml; validate_chunking_lesson_index.py; docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md; epistle_argument_gold_manifest.json; 1cor8_10_epistle_owner_review_docket.yaml; 1cor8_10_parent_only_evidence_packet.yaml; validate_1cor8_10_parent_evidence_packet.py; chunking_human_decision_forecast.yaml; .ai/control/chunking_theological_decision_register.yaml; governance_memory_durability_policy.yaml; owner_decision_projection_policy.yaml; conflicting prior owner decisions; projected owner pattern; predictable owner decisions.

Full-path anchor bank for legacy validators: `.ai/control/orthodox_original_language_pressure_dossier_queue.yaml`; `.ai/control/original_language_phrase_context_policy.yaml`; `.ai/control/textual_critical_policy_owner_options.yaml`; `.ai/control/textual_critical_case_policy.yaml`; `.ai/control/t371_variant_dependency_owner_decision_packet.yaml`; `.ai/control/t371_parent_only_reviewed_gold_promotion.yaml`; `.ai/control/t372_route_isolation_harness_plan.yaml`; `.ai/control/owner_decision_option_presentation_policy.yaml`; `.ai/control/t373_owner_implementation_authorization.yaml`; `.ai/control/t374_baseline_overlap_owner_decision_packet.yaml`; `.ai/control/t374_additive_parent_overlay_manifest.yaml`; `.ai/control/t375_post_pilot_review.yaml`; `.ai/control/t376_epistle_research_runway.yaml`; `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`; `.ai/control/manuscript_witness_reliability_scaffold.yaml`; `.ai/control/manuscript_source_catalog_metadata_plan.yaml`; `.ai/control/manuscript_source_catalog_research_packet.yaml`; `.ai/control/manuscript_source_catalog_sqlite_shell.yaml`; `.ai/control/dss_biblical_witness_source_rows.yaml`; `.ai/control/t385_owner_decision_packet.yaml`; `.ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml`; `.ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml`; `.ai/control/t397_eph1_route_isolation_harness.yaml`; `.ai/control/t398_bible_wide_phase_one_research_synthesis.yaml`; `.ai/control/t399_focused_bible_wide_research_queue.yaml`; `.ai/control/t401_eph1_output_pilot_manifest.yaml`; `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`; `.ai/control/cursor_low_risk_chunking_handoff.yaml`; `.ai/control/parallel_chunking_research_program.yaml`; `scripts/validate_t393_eph1_reviewed_gold_promotion_decision_packet.py`; `scripts/validate_t394_eph1_parent_only_reviewed_gold_promotion.py`; `scripts/validate_t397_eph1_route_isolation_harness.py`; `scripts/validate_t401_eph1_output_pilot.py`; `scripts/validate_source_metadata_authority.py`.

Additional compatibility anchors: textual-critical; non-orthodox; grammar; T379; eval/chunking_gold/per_form/epistle_argument_gold_manifest.json; T373 owner implementation authorization; scripts/validate_owner_decision_option_presentation_policy.py; scripts/validate_t374_additive_parent_overlay.py; scripts/validate_t375_post_pilot_review.py; scripts/validate_t376_epistle_research_runway.py; scripts/validate_t384_bible_wide_research_readiness.py; scripts/validate_t385_owner_decision_packet.py; scripts/validate_dss_biblical_witness_source_rows.py; scripts/validate_t398_bible_wide_phase_one_research_synthesis.py; scripts/validate_t399_focused_bible_wide_research_queue.py; scripts/validate_t402_low_complexity_chunking_runway.py; scripts/validate_cursor_low_risk_chunking_handoff.py; T387 manuscript witness reliability scaffold; T390 manuscript source catalog metadata plan; T391 source-catalog research packet; T395 SQLite source-catalog shell; T396 DSS biblical witness source rows.

## Context Layers

Master context, project status, roadmap state, task handoff, audit reports, agent work notes, recommendations, task ledger, and DAD mail have different authority. Human promotes master context changes via `scripts/agent/approve_master_context.py`. Agents must not edit `.ai/control/MASTER_CONTEXT.md` or `.ai/control/MASTER_CONTEXT.lock.yaml`.

## Validation Gates

Before stopping work, run the appropriate focused validators, then:

```bash
python scripts/validate_all.py
python -m pytest -q
```

Use `.ai/control/test_runtime_preflight.yaml` timeout ceilings: `python scripts/validate_all.py` needs at least 900000 ms; full local pytest may need up to 2400000 ms or guarded splits. Do not treat timeout as green or hide it from the handoff.

Core individual gates include `python scripts/validate_repo.py`, `python scripts/validate_control_plane.py`, `python scripts/validate_repository_link_contract.py`, `python scripts/validate_governance_dependency_map_mirror.py`, `python scripts/agent/validate_handoffs.py`, `python scripts/validate_task_scope.py`, `python scripts/validate_chunking_theological_decision_register.py`, `python scripts/validate_chunking_agent_preflight.py`, `python scripts/validate_task_ledger.py`, and the task-specific validators named in `docs/roadmap/TASK_LEDGER.md`.

CI fails red if any gate fails. A merged PR does not automatically authorize the next task. Read the next task file, roadmap state, task ledger, and handoff before creating a branch or making changes.

## Raw Source Inspection

Before designing or changing ingest, chunking, or graph-processing logic, inspect the real raw documents: read `.ai/control/RAW_SOURCE_INVENTORY.md`, re-scan if `data/raw` changed with `python scripts/scan_raw_sources.py`, and confirm markers in `config/ingest/usfm_marker_coverage.yaml`. Enforcement: `python scripts/validate_raw_coverage.py` and `python scripts/scan_raw_sources.py --check`.

USFM markers, Strong's-style tags, words-of-Jesus `\wj`, alternate readings, superscriptions, poetry, footnotes, cross-references, headings, and capitalization may be preserved and surfaced for review. They do not automatically authorize Scripture truth, lexical truth, intertext claims, speaker attribution, graph edges, chunk boundaries, output change, or retrieval truth. Detailed moved raw-source validator anchors live in `docs/roadmap/TASK_LEDGER.md`.

## Operating Modes

Agents must declare one mode at task start: `explore`, `plan`, `build`, `validate`, or `review`.

## Required Task State

Every non-trivial task must have `.ai/tasks/<task_id>.task.yaml` and `.ai/handoffs/<task_id>/handoff.md`.

```bash
python scripts/agent/force_handoff.py --task-id <TASK_ID> --agent <AGENT_NAME> --stage start
python scripts/agent/force_handoff.py --task-id <TASK_ID> --agent <AGENT_NAME> --stage final
python scripts/agent/validate_handoffs.py
```

## Required Completion Checklist

Update handoff, files changed, decisions/open questions, `PROJECT_STATUS.md`, `ROADMAP_STATE.yaml` if task status changed, `.ai/control/roadmap_events.jsonl` if roadmap scope/status changed, and `DATA_MAP.md` if data/schema/pipeline endpoints changed. For chunking-related paths, update `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md` or document the no-change rationale required by `.ai/control/METHODOLOGY_UPDATE_RULES.md`. Before output-changing chunking, cite reviewed gold/equivalent governed evidence, prove non-target identity and same-baseline, update decision/register/lesson/handoff/audit surfaces, and run the gates.

## Forbidden Shortcuts

Do not edit master context; put raw Bible files outside `data/raw`; design ingest/chunking/graph logic without raw inspection; treat an LLM boundary as canonical truth; rewrite source text during chunking; claim improvement from evaluator-only change; mix asserted and inferred relationships; add relationship types without schema registration; change stable IDs because labels changed; delete stable resources instead of deprecating; mark tasks complete without handoff; skip validation gates with failing CI; ignore `config/agents/agent_hostile_policy.yaml`; or redefine upstream governance authority inside this repo without an upstream proposal.

## Architecture Correction Protocol

Propose master-principle changes with `propose_master_context_change.py`, create/update ADRs when architecture changes, explain reason/affected files/migration/risks, update roadmap state when sequencing changes, and record handoff. Human approval is separate.

## Digital Asset Directory Enrollment

Contract: `.digital-asset/dad-integration.json`; context map: `.digital-asset/context-map.json`; mailbox: `.digital-asset/mail/`; governance map: `.digital-asset/governance-map.yaml`; data map: `.digital-asset/data-map.yaml`; skill checkout: `.digital-asset/skills/checkout.json`; coding asset pointer: `.ai-assets.json`.

Use these surfaces when work involves AI-assisted coding, repo governance, lessons, reusable assets, templates, agent skills, or cross-repo suggestions. DAD mail is candidate-only and local review controls adoption for `logos-scripture-graph`. Runtime `.digital-asset/mail/*.jsonl` files are local and gitignored; immutable historical candidate-envelope evidence lives under `tests/fixtures/dad/` and is never transport input. Validate the versioned read-only boundary with `scripts/validate_dad_transport_contract.py`. Required DAD anchors: .digital-asset/mail/; lessons; reusable assets; msg-20260703-t424-rust-validation-layer.
