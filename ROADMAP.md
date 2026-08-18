# Execution Roadmap

This roadmap is the human-readable plan. Machine-readable state lives in `ROADMAP_STATE.yaml`. Roadmap changes must be logged to `.ai/control/roadmap_events.jsonl`.

## Public release and MCP maturity track

This cross-phase track packages existing work into honest public releases; it does not
replace the technical phases below. Full criteria and the current capability matrix are
in [`docs/architecture/PUBLIC_PROJECT_OVERVIEW.md`](docs/architecture/PUBLIC_PROJECT_OVERVIEW.md).

- **Pre-Bronze (current):** land the public AI front door; freeze and publish M7 as a
  candidate; preserve active M8 checkpoints while Fable finishes M8; begin M7/M8
  comparison and convergence only after the M8 final checkpoint.
- **Bronze:** reproducible local release, governed source identities, deterministic
  validation, and a documented local read-only query/MCP boundary.
- **Silver:** independently reviewed graph/retrieval integration, measurable evaluation,
  and authenticated read-only staging MCP.
- **Gold:** production remote read-only MCP with versioned releases, monitoring,
  security/privacy review, rollback, incident procedures, and sustained human governance.

These are system release levels. They are distinct from **reviewed-gold**, the existing
narrow label for human-reviewed chunking evidence.

## Phase 0 — Repository control plane

Goal: make the repo safe for many agents.

Deliverables:

- AI front door
- deterministic handoff protocol
- roadmap state file
- schemas for handoff, roadmap, sources, chunks, and relationships
- validation scripts
- GitHub review/CI scaffolding

Exit criteria:

- every task has an owner, status, and handoff requirement
- validation runs locally
- CODEOWNERS and PR template exist

## Phase 1 — Raw source vault and manifests

Goal: make source drops clean, licensed, and reproducible.

Deliverables:

- `data/raw/bible/eng-web/usfm/eng-web_usfm.zip`
- source manifest for WEB Classic
- license metadata
- checksum capture
- immutable raw-file policy

Exit criteria:

- source manifests validate
- no derived files are manually edited in raw source directories

## Phase 2 — USFM ingestion and canonical passage registry

Goal: parse WEB USFM into stable passage and witness records.

Deliverables:

- USFM importer
- book/chapter/verse parser
- OSIS reference normalization
- passage registry
- translation witness export

Exit criteria:

- every verse has an OSIS ref
- source text remains traceable to raw file and line/span

## Phase 3 — Chunking engine v0

Goal: produce sentence-safe, literary-aware English chunks from WEB.

Deliverables:

- boundary candidate generator
- boundary scorer
- genre policies
- context packet generator
- chunk validation tests

Exit criteria:

- no chunk ends mid-sentence
- no psalm superscription is separated from its psalm
- poetry markers are preserved
- every chunk has source span, boundary basis, and license metadata

## Phase 4 — Chunk evaluation and scholar review loop

Goal: prevent beautiful but bad chunking.

Deliverables:

- gold set of manually reviewed chunk boundaries
- disagreement logs
- chunk quality metrics
- review-ready chunk diff reports

Exit criteria:

- known hard cases pass: Psalms, Proverbs, prophetic oracles, Gospel pericopes, Pauline arguments

### Current post-T327 chunking sequence

T336 records the optimized whole-Bible chunking roadmap after the T327 canonical-scope correction
and T331-T335 Psalm guardrail sequence.

Priority:

- canonical 66-book Bible chunking remains the highest-priority substrate;
- Psalms are first for implementation because reviewed evidence and the candidate Psalm seam already
  exist;
- Revelation should receive an early hard-book atlas/review-packet lane but no implementation until
  reviewed gold exists;
- book-specific rules must stay behind router/orchestrator gates and must not leak globally;
- future boundary, noncanonical, legal, commentary, reception, or master-chunker work must remain
  separate from and subordinate to canonical Bible chunking.

Recommended sequence:

1. Psalms / poetry stanza implementation lane.
2. Epistle argument/paragraph lane.
3. Narrative/pericope lane.
4. Wisdom/dialogue lane.
5. Prophetic oracle lane.
6. Gospel discourse / words-of-Jesus lane.
7. Revelation / apocalypse lane.
8. Bible-wide orchestration/promotion pass.

## Phase 5 — Hebrew/Greek source alignment

Goal: align English chunks to source-language references before deep morphology.

Deliverables:

- WLC source manifest
- Greek NT source manifest
- LXX source manifest
- passage-level source alignment
- future morphology hooks

Exit criteria:

- each English chunk can point to Hebrew/Aramaic/Greek source span where available

## Phase 6 — Lexical and morphology layer

Goal: attach lexemes, morphology, syntax, and semantic domains.

Deliverables:

- Lexeme schema
- WordToken schema
- morphology importer
- syntax/span alignment

Exit criteria:

- token-to-lexeme links validate
- source attribution and licenses are explicit

## Phase 7 — Cross-reference and intertextual graph

Goal: import and classify cross-references.

Deliverables:

- cross-reference source manifests
- relationship type registry
- quotation/allusion/echo/typology/fulfillment edge types
- confidence and provenance model

Exit criteria:

- asserted edges are separated from inferred edges
- every relationship has evidence/provenance

## Phase 8 — Retrieval, graph, and view contracts

Goal: expose the same graph through multiple reliable routes.

Deliverables:

- graph neighborhood route
- short synthesis route
- evidence bundle route
- profile comparison route
- JSON sidecar route
- review-ready diff route

Exit criteria:

- retrieval returns normalized object sets with evidence and scope

## Phase 9 — Runtime/orchestration integration

Goal: connect this semantic repo to a separate agent runtime.

Deliverables:

- release artifacts
- API/export contracts
- connector contract for runtime repo
- permission/trust-zone mapping

Exit criteria:

- agent runtime can read published releases without mutating canonical source truth
