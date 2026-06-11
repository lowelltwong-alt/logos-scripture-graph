# Task Handoff

## Task

- task_id: T348
- title: Scripture vectorization and graph-edge durability contracts (planning-only)
- phase: phase_4
- status: complete

## Agent

- agent_name: fable
- mode: planning
- stage: final
- updated_at: 2026-06-11T20:30:00+00:00
- handoff_id: 9095b83251b2fda3

## Files read

- AI_FRONT_DOOR.md, .ai/control/MASTER_CONTEXT.md (embedding gate at line 114), .ai/control/PROJECT_STATUS.md
- .ai/control/boundary_source_intake_plan.yaml (pattern source for fail-closed plan flags)
- docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md (master-chunker boundary)
- docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md, scripts/validate_all.py, ROADMAP_STATE.yaml
- External lesson source (read-only, not copied): legal_retrieval_architecture_pack.zip
  (model registry / index manifest / retrieval profile / migration playbook patterns)

## Files changed

- .ai/control/scripture_vectorization_plan.yaml (new) — machine-readable fail-closed plan:
  embedding_runs_allowed/index_builds_allowed/model_inferred_edge_generation_allowed/
  vector_space_mixing_allowed/shared_index_with_non_bible_corpora_allowed all false;
  owner gates true; durable vs derived layers; three graph-edge classes; forbidden flows;
  stop triggers; future_tasks_before_embedding.
- docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md (new) — the
  contract: one law (vectors/edges never truth), identity rules (OSIS + deterministic chunk
  IDs), one-model-per-index, manifest pinning (chunk SHA + policy version + corpus_baseline),
  three-class edge taxonomy, profile-switch migration/rollback playbook, 100-year survival
  kit, explicit non-authorization section, RISK-GATE-001 map.
- schemas/embedding_model.schema.json, schemas/vector_index_manifest.schema.json,
  schemas/retrieval_profile.schema.json, schemas/graph_edge_record.schema.json (new).
- config/retrieval/embedding_models.yaml, config/retrieval/retrieval_profiles.yaml (new,
  empty skeletons; no approved models, no production profiles).
- scripts/validate_vectorization_plan.py (new) — fail-closed validator; wired into
  scripts/validate_all.py as an unconditional gate.
- tests/test_t348_vectorization_contracts.py (new, 43 tests after Codex hardening) — flag
  checks, validator pass/fail-closed simulations via --plan/--models/--profiles,
  schema-backed registry validation, index-manifest compatibility checks, graph-edge
  predicate/provenance/status checks, substrate-gate tamper checks, and contract
  non-authorization strings.
- Governance: ROADMAP_STATE.yaml, .ai/control/PROJECT_STATUS.md,
  .ai/control/current_focus.yaml, .ai/control/roadmap_events.jsonl,
  .ai/tasks/T348.task.yaml, AI_TABLE_OF_CONTENTS.md, this handoff.

## Decisions made

- Adopt the legal pack's resilience spine (model registry, index manifest, retrieval
  profiles, shadow migration) as Logos-native contracts; copy no pack files; no legal
  vocabulary imported.
- Planning-only, T327F-style: all authorization flags fail closed; embedding runs blocked
  behind the MASTER_CONTEXT substrate gate (TextSpan, ContextPacket,
  SourceLanguageWitness, AlignmentRecord) plus a future owner decision.
- Graph edges classed by durability: structural_deterministic (survive as generator code),
  reviewed_semantic (committed human-judgment records — the irreplaceable layer),
  model_inferred_candidate (disposable; never canonical without human gate).
- Vector spaces never mix: one embedding model per index (schema makes the field a single
  string); query model must match index model; canonical and non-Bible corpora never share
  an index; retrieval-eval pressure on chunk policy is a named forbidden flow.
- Indexes/backends are adapters: manifests pin model id/version, dimension, normalization,
  distance metric, exact chunk-set SHA, policy version, and corpus_baseline so any index is
  rebuildable and comparisons stay same-baseline (T327D lesson extended to embeddings).
- T340D context honored: post-merge verification tooling was removed by owner decision
  (PR #54); this task references no removed workflow surfaces.

## Validation run

- command: python scripts/validate_vectorization_plan.py
- result: passed (planning-only, fail closed)
- command: python -m pytest -q tests/test_t348_vectorization_contracts.py
- result: 43 passed after Codex post-review hardening
- command: python scripts/validate_all.py
- result: All validation gates passed (includes new vectorization gate)
- command: python -m pytest -q
- result: full suite passed (see PR body for count)
- failures: none

## Known risks

- A planning contract can be misread as implementation permission; mitigated by the
  explicit non-authorization section, fail-closed flags, validator, and tests.
- Boundary/theology corpora (church fathers, councils, confessions) need a mirrored
  contract in their own repo lane when intake planning begins; this task deliberately did
  not touch logos-boundary-literature.
- Golden retrieval questions and red-team query suites are named but not yet authored;
  they are listed in future_tasks_before_embedding.

## Open questions

- Owner: which embedding model families to evaluate first when the gate eventually opens
  (cloud vs local vs hybrid)?
- Owner: where index manifests will live when authorized (config/retrieval/index_manifests
  is reserved and validated-empty for now).

## Next agent instruction

Open/merge the T348 PR after review. Do not run embeddings, build indexes, or generate
edges — all flags in .ai/control/scripture_vectorization_plan.yaml are false and must stay
false until MASTER_CONTEXT substrate gaps (TextSpan, ContextPacket, SourceLanguageWitness,
AlignmentRecord) are implemented and the owner authorizes a separate embedding task. Next
chunking-lane work remains T342 (Revelation review-packet candidate selection, gated).
Do not start T327G; do not import boundary texts; do not promote the Psalm candidate skill.

---

## Handoff refresh: start

- agent_name: Codex
- mode: build
- updated_at: 2026-06-11T20:27:35+00:00
- handoff_id: 8d35c0b7dacfe2db

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-11T20:46:40+00:00
- handoff_id: 7737e70af1fc85a3

### Codex post-review hardening update

- Files read: PR #55/T348 patch request attachment; AI front door; MASTER_CONTEXT; PROJECT_STATUS; DATA_MAP; RAW_SOURCE_INVENTORY; ROADMAP; ROADMAP_STATE; HANDOFF_PROTOCOL; architecture/chunking/methodology docs; agent roles; predicate registry; T348 handoff/task; pyproject dependency config.
- Files changed: `.ai/control/scripture_vectorization_plan.yaml`, `.ai/control/DATA_MAP.md`, `.ai/control/PROJECT_STATUS.md`, `.ai/control/current_focus.yaml`, `.ai/control/handoff_ledger.jsonl`, `.ai/handoffs/T348/handoff.md`, `.ai/tasks/T348.task.yaml`, `ROADMAP_STATE.yaml`, `docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md`, `schemas/graph_edge_record.schema.json`, `schemas/retrieval_profile.schema.json`, `schemas/vector_index_manifest.schema.json`, `scripts/validate_vectorization_plan.py`, `tests/test_t348_vectorization_contracts.py`.
- Decisions made: patched only the Codex P1 fail-closed gaps; kept registries empty; reused `config/governance/predicate_registry.yaml`; kept `embedding_runs_allowed`, `index_builds_allowed`, `model_inferred_edge_generation_allowed`, `vector_space_mixing_allowed`, and `shared_index_with_non_bible_corpora_allowed` false.
- Validation performed: `python scripts/validate_vectorization_plan.py` passed; `python -m pytest -q tests/test_t348_vectorization_contracts.py` passed with 43 tests; `python scripts/validate_all.py` passed; `python -m pytest -q` passed with 229 tests.
- Risks introduced: future graph-edge records are more tightly constrained to current governance predicates; future structural edge predicates will need an explicit predicate-registry update before use.
- Unresolved questions: none for this hardening patch; owner decisions for embedding model selection, first index build, and default Scripture retrieval profile remain future-gated.
- Exact next action: review the hardened PR diff; do not run embeddings, build indexes, generate edges, import boundary texts, promote profiles, start T327G, implement Revelation, or promote the Psalm candidate skill.
