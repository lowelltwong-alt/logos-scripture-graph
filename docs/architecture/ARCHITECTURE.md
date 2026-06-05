# Architecture

## System boundary

This repository is the **knowledge plane** and semantic control plane for the Bible graph. It owns source manifests, canonical passage identity, translation witnesses, boundary claims, chunk policies, schemas, validation, and release artifacts.

The future agent runtime should be separate. It may read this repo, run pipelines, propose changes, and consume release artifacts, but it should not become the source of truth.

Cross-repo role: this repository is the scripture data-plane implementation under
the upstream `logos-governance-architecture` governance architecture. The link is
`governance_contract`, not submodule and not runtime coupling. The local contract
surface is `config/governance/repository_link_contract.yaml`; paired GitHub issues
track coordination in `logos-governance-architecture#54` and `logos-scripture-graph#7`.

## Three-plane model

```mermaid
flowchart TB
  UG[Upstream Governance Architecture\nlogos-governance-architecture\nsource authority, derivation logic, review obligations]
  KP[Knowledge Plane\nsource manifests, passages, witnesses, chunks, graph claims]
  CP[Control Plane\nroadmap, handoffs, schemas, validation, governance]
  EP[Execution Plane\nseparate agent runtime, tools, orchestration, approvals]
  UG -->|governance_contract| CP
  KP --> CP
  CP --> KP
  CP --> EP
  EP --> CP
```

## Canonical vs derived

| Layer | Examples | Rule |
|---|---|---|
| Raw source | `eng-web_usfm.zip`, WLC files, Greek NT files | Immutable; never hand edit. |
| Canonical model | `ScripturePassage`, `TranslationWitness`, source manifests | Generated or curated with provenance. |
| Derived evidence | chunks, embeddings, indexes, context packets | Rebuildable; never treated as canonical source. |
| Claims/edges | cross-references, theme links, doctrine links | Asserted/inferred separation required. |
| Runtime artifacts | retrieval traces, answers, agent logs | Separate from canonical truth. |

## Source identity model

```text
ScriptureWork
  -> ScripturePassage
     -> TranslationWitness
        -> TextSpan
           -> BoundaryClaim
              -> RetrievalChunk
                 -> ContextPacket
```

## Relationship model

Important relationships are first-class objects when they need metadata:

```text
RelationshipObject:
  subject_id
  predicate
  object_id
  evidence_refs
  provenance
  confidence
  assertion_mode: asserted | inferred | candidate
  trust_zone
```

## Trust zones

| Zone | Purpose |
|---|---|
| raw | untouched source artifacts |
| canonical | passage registry, source manifests, translation witness records |
| asserted | human-reviewed edges/claims |
| inferred | rebuildable machine-derived closure/inference |
| candidate | AI- or bulk-import-suggested claims pending review |
| derived | chunks, embeddings, search indexes |

## Build flow

```text
raw source drop
  -> source manifest
  -> parser/importer
  -> canonical passage registry
  -> text spans and translation witnesses
  -> boundary claims
  -> retrieval chunks and context packets
  -> graph claims / relationship objects
  -> indexes and release artifacts
```

## Cross-Repo Data Flow

```text
logos-governance-architecture
  -> approved governance/source-trust/review contract
  -> logos-scripture-graph control plane
     -> raw source manifests
     -> canonical Scripture passage and witness records
     -> derived chunks/context packets
     -> candidate/asserted graph claims with trust-zone separation
     -> validated release artifacts
  -> future runtime consumers
```

Downstream Scripture artifacts may reference upstream governance meaning, but they
must not silently redefine it. Any new authority concept, trust-zone rule, or
relationship vocabulary starts as an upstream proposal before becoming a local
data-plane contract.
