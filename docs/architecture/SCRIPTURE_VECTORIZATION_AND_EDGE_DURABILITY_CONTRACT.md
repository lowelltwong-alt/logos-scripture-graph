# Scripture Vectorization And Graph-Edge Durability Contract

## Status

- Task: T348
- Mode: planning
- Contract status: active as planning/governance contract
- Embedding runs: not authorized (`embedding_runs_allowed: false`)
- Index builds: not authorized
- Model-inferred edge generation: not authorized
- Machine-readable flags: `.ai/control/scripture_vectorization_plan.yaml`
- MASTER_CONTEXT gate: TextSpan, ContextPacket, SourceLanguageWitness, and
  AlignmentRecord must be implemented before any embedding work; "Do not skip
  to embeddings or graph edges."

This document defines the contracts under which the Bible will eventually be
vectorized and graphed. It authorizes no embedding run, no index build, no
backend selection, no retrieval behavior, and no edge generation.

## 1. The One Law

Vectors and edges are never the truth. The truth is:

```text
source text + stable IDs + span maps + provenance + human-reviewed decisions
```

Embeddings, vector indexes, graph databases, entity/community summaries, and
reranker scores are build products. Every one of them must be reproducible
from committed files plus a committed manifest. If an artifact cannot be
deleted and rebuilt from pinned inputs with equivalent records/manifests, it
must not live in a vector database or graph store.

Durable vs derived layers are enumerated machine-readably in
`scripture_vectorization_plan.yaml` (`durable_layers`,
`derived_rebuildable_layers`).

## 2. Identity Rules

- Every durable object addresses Scripture by OSIS reference.
- Chunk IDs remain deterministic functions of span + policy version, so a
  rebuilt chunk set yields identical IDs and every vector, edge, and citation
  re-attaches cleanly after any rebuild. Chunk IDs must never become random
  UUIDs.
- Boundary/supporting corpora (in their own repos) point INTO Scripture by
  OSIS reference. Scripture records never depend on boundary IDs.

## 3. Vector Rules

- One embedding model per index. Vector spaces never mix
  (`vector_space_mixing_allowed: false`). Query embeddings must use the same
  registered model as the index they search.
- Every model is registered in `config/retrieval/embedding_models.yaml`
  (schema: `schemas/embedding_model.schema.json`) before use. Registry records
  are never deleted; retired models keep their entries so old manifests stay
  interpretable.
- Every index has a committed manifest
  (`schemas/vector_index_manifest.schema.json`) pinning: embedding model id,
  embedding model version, dimension, normalization, distance metric, exact
  chunk-set SHA-256, chunk-policy version, and corpus baseline. The manifest is
  the durable artifact; the index is disposable.
- Canonical and non-canonical corpora never share an index
  (`shared_index_with_non_bible_corpora_allowed: false`).

## 4. Graph-Edge Taxonomy (three durability classes)

Schema: `schemas/graph_edge_record.schema.json`.

1. `structural_deterministic` — containment, parent/child chunk relations,
   cross-reference sidecar edges. Survive as committed generator code; never
   stored as truth; regenerated on demand from a derivation rule/generator and
   source policy version.
2. `reviewed_semantic` — human-reviewed claims with evidence, reviewer, date,
   and scope. These are the most expensive artifacts the project produces;
   human review does not re-run. They are committed records; any graph
   database row is a disposable projection.
3. `model_inferred_candidate` — GraphRAG entities, community summaries,
   LLM-extracted relations. Always carry generator model, prompt version, and
   rebuild provenance; always `candidate_unreviewed`; never promoted to
   reviewed without a human gate; never feed canonical conclusions; rebuilt or
   discarded at will.

## 5. Retrieval Profiles And Backends

- Retrieval behavior lives in named, versioned profiles
  (`config/retrieval/retrieval_profiles.yaml`,
  `schemas/retrieval_profile.schema.json`). Promotion and rollback happen by
  switching profiles, never by editing live behavior.
- At most one profile is `default_for_scripture: true`; it must exclude
  boundary material; changing it requires an owner decision.
- Backends (Pinecone, pgvector, LightRAG, future systems) are adapters fed by
  one export contract (chunks + manifest + edge records). Any backend-specific
  feature behavior depends on must be recorded in the index manifest
  (`backend_specific_features_used`) or it must not be used.

## 6. Migration And Retirement (adapted playbook)

When a model is to be replaced or retires:

1. Freeze the production index (manifest status `frozen`).
2. Register the candidate model.
3. Re-embed the SAME SHA-pinned chunk set into a separate candidate index.
4. Run golden retrieval questions and red-team queries against both.
5. Compare retrieved chunks; review high-risk differences.
6. Promote by switching the retrieval profile; keep the rollback profile.
7. Never re-embed in place; never delete the retired model's registry entry.

Golden retrieval questions derive from existing reviewed gold (for example:
a Psalm 23 query returns the one whole-psalm chunk; a Psalm 89 lament query
returns the reviewed 38-45 child; no default-profile query ever returns
GLO/FRT/non-66 or boundary content).

## 7. The 100-Year Survival Kit

Six things live in git; everything else is rebuildable:

1. source archive + checksums;
2. ID registry and span maps;
3. cleaning/chunking policy + generators;
4. reviewed decisions (gold, claim/edge records, decision boxes) — the only
   irreplaceable layer;
5. build manifests + model/profile registries;
6. golden retrieval questions + red-team queries.

## 8. What This Contract Does Not Authorize

- embedding runs, index builds, or backend selection;
- model-inferred edge generation;
- any retrieval behavior or default retrieval definition;
- chunk policy or chunk boundary changes (reviewed-gold lane only;
  `chunk_policy_tuning_from_retrieval_eval_allowed: false`);
- boundary text import or boundary-repo work;
- evaluator/leaderboard/scorecard changes;
- T327G or Revelation implementation;
- any claim of chunking or retrieval improvement.

## 9. RISK-GATE-001 Map

What could this change accidentally authorize, weaken, contaminate, overfit,
globalize, or make harder to reverse?

### Confirmed risks

- A planning contract can be misread as implementation permission. Mitigated:
  fail-closed flags, this section, and validator enforcement.
- Retrieval-quality pressure could push chunk-boundary changes around the
  reviewed-gold gate. Mitigated: forbidden flow
  `retrieval_eval_pressure_to_chunk_policy`.

### Plausible risks

- A future profile quietly includes boundary material in default Scripture
  retrieval. Mitigated: schema flag + validator rule + owner gate.
- Indexes built from unlabeled corpus baselines get compared as improvement.
  Mitigated: manifest requires `corpus_baseline` (T327D lesson).
- A backend feature becomes load-bearing and blocks migration. Mitigated:
  `backend_specific_features_used` must be recorded.

### Unlikely but high-impact risks

- Model-inferred edges leak into canonical theological conclusions. Mitigated:
  edge-class schema constraints; promotion requires human gate.
- A shared optimization objective forms across Bible and non-Bible corpora
  via a shared index or shared eval. Mitigated: per-corpus indexes/profiles;
  T336 master-chunker boundary.

### Watch-later conditions

- Any PR flipping a plan flag without an owner decision reference.
- Any embedding/index artifact appearing while flags are false.
- Any profile with `default_for_scripture: true` and
  `includes_boundary_material: true`.

### Owner decisions needed (future)

- Embedding model selection and approval.
- First index build authorization (after MASTER_CONTEXT gaps close).
- Default Scripture retrieval profile designation.

## 10. Deferred Sequence

Per `future_tasks_before_embedding` in the plan file: substrate gaps
(TextSpan, ContextPacket, SourceLanguageWitness, AlignmentRecord) first; then
owner-approved model selection; golden retrieval questions; red-team suite;
manifest validator dry run; then a separate owner-gated embedding-run task.
