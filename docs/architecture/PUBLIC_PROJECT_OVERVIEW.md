# Logos Scripture Graph: Public Project Overview

- **Status date:** 2026-08-18
- **Repository role:** governed Scripture knowledge/data plane
- **Audience:** ministry collaborators, software and knowledge-graph engineers, AI
  agents, reviewers, and prospective employers

This document is the public orientation layer. It explains what the project is, what
is working now, what remains research, and how an AI or human should enter the wider
Logos repository family. It does not replace the human-gated architecture authority in
`.ai/control/MASTER_CONTEXT.md` or the exact operational records linked below.

## One-minute description

Logos Scripture Graph is an engineering system for turning licensed Scripture sources
into traceable, machine-readable evidence for study, teaching, discipleship, search,
and future AI-assisted ministry tools. It models passages, translation witnesses,
literary units, source evidence, claims, and relationships without allowing a model,
an embedding, or a convenient chunk boundary to become theological authority.

The central engineering idea is separation of concerns:

```text
governance and authority
  -> source and provenance contracts
  -> canonical Scripture identities and witnesses
  -> reviewed or candidate literary units and claims
  -> graph, retrieval, and MCP release surfaces
  -> separate AI/runtime consumers
```

This is a Christian ministry-oriented project, but it is not a church, creed, pastor,
or autonomous theological authority. It is infrastructure that helps people and tools
work from Scripture with explicit provenance, uncertainty, review, and human gates.

## Repository family and authority flow

| Surface | Role | Authority boundary |
|---|---|---|
| `logos-governance-architecture` | Upstream governance, source-trust, review, and theological architecture | Defines meaning and obligations; downstream repos cannot silently weaken it. |
| `logos-scripture-graph` | This repository: canonical-66 Scripture substrate, schemas, chunking evidence, graph/retrieval contracts, validation, and releases | Owns governed Scripture data-plane artifacts; candidate model output is not canonical truth. |
| `logos-boundary-literature` | Supporting and boundary literature | May inform background, comparison, reception, or refutation; cannot override canonical Scripture. |
| `logos-doctrine-genealogy` | Planned doctrine-development and influence graph | Remains a planned, separately governed surface; it is not silently implemented here. |
| Future runtime / remote MCP service | Agents, tools, orchestration, approvals, and serving | Consumes validated releases through contracts; it must not become the source of truth. |

The binding local relationship is
`config/governance/repository_link_contract.yaml`. GitHub issues, chats, model output,
and project dashboards coordinate work; they are not the governance source of truth.

## What exists today

| Capability | Current state | Evidence / qualification |
|---|---|---|
| Source ingestion and identity | Implemented | Source manifests, canonical passage identities, translation witnesses, schemas, and deterministic validators are present. |
| Canonical-66 Scripture substrate | Implemented on the governed baseline | The repository records complete 66-book passage coverage and keeps raw, canonical, candidate, asserted, inferred, and derived trust zones distinct. |
| Provenance-aware data engineering | Implemented as contracts and validation | Claims and relationship objects carry evidence, provenance, confidence, assertion mode, and trust zone. |
| Literary chunking | Working engine plus reviewed pilots and large research programs | Some parent-only cases are reviewed-gold evidence; whole-Bible M7/M8 maps remain candidate research and are not production chunk output. |
| Knowledge-graph engineering | Architecture and candidate evidence implemented; production graph incomplete | Predicate, relationship, trust-zone, and cross-repo durability contracts exist. Broad asserted graph publication is still gated. |
| Retrieval and vectorization | Planned/contracted, not a production release | Chunks and context packets are designed as rebuildable derived artifacts. Embeddings and retrieval truth are not silently authorized. |
| Learning loops | Metadata-only local adapter exists | The LLOS/DAD adapter supports approved candidate metadata and asymmetric writes; DAD cannot push into Logos or change Scripture authority. |
| MCP | Contract declared, server not implemented in this repo | `.digital-asset/dad-integration.json` declares `local_stdio_read_only`; remote MCP and write tools are disabled. |
| Runtime agent | Deliberately separate | This repository is the knowledge/control plane, not the autonomous runtime. |

“Implemented” means the cited contract or governed artifact exists and is validated. It
does not mean that every research lane is merged, every data product is public, or a
production service is operating.

## Engineering capabilities demonstrated

The repository is also a portfolio of technical practice:

- knowledge-graph modeling with first-class relationship objects, provenance, trust
  zones, assertion modes, and cross-repository authority edges;
- data engineering from immutable source drops through manifests, canonical identities,
  derived views, schemas, fingerprints, and reproducible release gates;
- literary and semantic chunking with model isolation, blind proposals, dissent,
  explicit holds, review packets, route isolation, and non-target identity checks;
- graph/retrieval design that separates canonical evidence, asserted claims, inferred
  relationships, candidate model output, and rebuildable indexes;
- multi-agent evaluation with bounded roles, frozen briefs, independent lanes,
  reconciliation, and durable audit evidence;
- learning-loop governance that records surprises and reusable evidence without giving
  an external directory authority to write back into Scripture repositories;
- release engineering through task-scoped diffs, handoffs, deterministic validators,
  privacy checks, protected branches, and merge gates.

These controls are part of the product. In a high-consequence ministry domain, knowing
what a model must not claim is as important as generating a useful answer.

## Two different uses of “gold”

The repository already uses **reviewed-gold** for a narrow class of human-reviewed
chunking evidence. The following Bronze/Silver/Gold ladder is instead a **release
maturity ladder** for the whole system. The terms are intentionally not interchangeable.

| Release level | Exit criteria | Current position |
|---|---|---|
| Bronze | Reproducible local build; governed source identities; deterministic validation; documented local read-only query/MCP boundary; candidates clearly separated from releases | Foundation substantially exists, but no Bronze release is declared until a versioned packet explicitly includes or excludes active research lanes. |
| Silver | Independent integration review; versioned graph/retrieval contracts; measurable quality/evaluation gates; authenticated read-only staging MCP; operational and privacy checks | Planned. |
| Gold | Production remote read-only MCP; monitored service levels; security review; rollback and incident procedures; stable versioned release artifacts; sustained human governance | Planned. Write-capable MCP would require a separate explicit authority design and is not implied. |

## M7, M8, and PR 194

The two whole-Bible lanes are valuable research evidence, not merge-ready product:

| Item | Hash-bound state on 2026-08-18 | Meaning |
|---|---|---|
| M7 Sol | local branch `scratch/t423-m7-sol` at `eaf31a940d3166b49c38ca26eb279392e0a3b25b` | The aggregate progress file says 66/66 candidate coverage, while the model manifest says 22/66 corrective re-review and 1,426 unresolved appeals. It requires a reconciled freeze before release use. |
| M8 Fable | published branch `scratch/t423-m8-fable` at `5c6c36106c49e2ac5795cb98956129cb4fab0620` | Clean owner checkpoint: 19/66 books closed through Psalms; Proverbs staged; candidate-only and still active. |
| PR 194 | open at the M8 hash above; 5,923 files and more than 1.2 million added lines; GitHub reports `CONFLICTING` / `DIRTY` | It combines inherited M7 material and active M8 research. It must not be conflict-flattened into `main`. |

No M7/M8 content comparison or convergence has started. M8 is still being produced by
Fable and its subagents; the owner has directed that convergence begin only after M8 is
complete. The A/B “convergence” referenced by T610 means only that two blind design
reviewers agreed on this publication architecture.

The safe publication sequence is:

1. Land this small clean-main orientation and audit PR.
2. Reconcile M7's status surfaces and publish its current work as a hash-bound,
   candidate-only unit with a manifest, limitations, and review receipts. The recorded
   role/subagent system is described in
   [`M7_SOL_AGENT_SYSTEM.md`](M7_SOL_AGENT_SYSTEM.md).
3. Let Fable and its subagents finish M8. Preserve only owner-authorized checkpoints;
   do not use T610 to rewrite, compare, or converge the active lane.
4. After M8 is complete, freeze both heads and begin the first independent M7/M8
   comparison and convergence work.
5. Only then create a small convergence/index PR that links the candidates and records
   decisions; do not copy their entire scratch trees into the index.
6. Close PR 194 as superseded only after every valuable commit has a durable GitHub ref,
   the replacement links are visible, and the post-M8 disposition is recorded.

This preserves the work and its failed attempts while keeping `main` reviewable.

## MCP front door

The current machine-readable MCP declaration is:

```text
.digital-asset/dad-integration.json
  mcp.mode = local_stdio_read_only
  mcp.remote_mcp_enabled = false
  mcp.vendor_sdk_required = false
  mcp.write_tools_enabled = false
```

There is no remote MCP server implementation in this repository today. The planned
service belongs in the separate execution/runtime plane and should consume a versioned,
validated release rather than read mutable scratch branches. A minimal remote read-only
surface should eventually expose tools such as:

- passage/source lookup with provenance;
- candidate versus asserted relationship lookup;
- literary-unit and context-packet retrieval;
- release/status and evidence-receipt inspection.

Every response should identify release version, source refs, assertion mode, trust zone,
confidence, and applicable holds. Repository writes, reviewed-gold promotion, preferred
readings, canon changes, and theological rulings are outside the default MCP authority.

## Near-term plan

1. Complete the clean public entry and merge-gate it independently.
2. Freeze, reconcile, validate, and publish M7 without the known defective local files,
   including transparent documentation of its Sol role mesh and per-book strategies.
3. Let Fable and its subagents complete M8; publish only owner-authorized checkpoints.
4. After M8 completes, run the first M7/M8 comparison and convergence and decide the
   final PR 194 replacement/index shape.
5. Declare Bronze only after a reproducible release packet and local read-only query
   contract exist.
6. Build Silver retrieval/graph evaluation and authenticated staging MCP.
7. Build Gold production operations only after security, privacy, monitoring, rollback,
   and ministry-governance review are satisfied.

## Where to go next

- AI/human operating entry: [`../../AI_FRONT_DOOR.md`](../../AI_FRONT_DOOR.md)
- Searchable repository map: [`../../AI_TABLE_OF_CONTENTS.md`](../../AI_TABLE_OF_CONTENTS.md)
- Current operational record: [`../../.ai/control/PROJECT_STATUS.md`](../../.ai/control/PROJECT_STATUS.md)
- Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- M7 Sol role/subagent design: [`M7_SOL_AGENT_SYSTEM.md`](M7_SOL_AGENT_SYSTEM.md)
- Roadmap: [`../../ROADMAP.md`](../../ROADMAP.md)
- A/B convergence audit: [`../../.ai/audits/reports/20260818-T610-public-entry-convergence.md`](../../.ai/audits/reports/20260818-T610-public-entry-convergence.md)
- Security reporting: [`../../SECURITY.md`](../../SECURITY.md)
