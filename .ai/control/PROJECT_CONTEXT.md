# Project Context — place in the Logos architecture

This repository is **not** a standalone project. It is one **surface** of the
Logos architecture (per the upstream principle: *"one architecture with multiple
surfaces, not separate projects"*).

## Upstream (theological source)

- **[logos-governance-architecture](https://github.com/lowelltwong-alt/logos-governance-architecture)**
  — the theological source architecture: canon/doctrine/scripture/boundary
  *taxonomy, ontology, ordering, and weighting logic*. It defines *what* the
  governed objects are and *why*.

## This repository (data-plane substrate)

`logos-scripture-graph` is the **deterministic, machine-readable implementation**
of the upstream's scripture/source/graph layers — i.e. the data plane for:

| Upstream layer (repository-integration-map.md) | Implemented here |
|---|---|
| 3. Scripture | passages registry, OSIS ids, translation witnesses |
| 4. Original-language / translation / manuscript | WordToken Strong's bridge; future WLC/SBLGNT/LXX witnesses |
| 6. Boundary-source | canon profiles (deuterocanonical tagging, ADR-0005) |
| 7. Graph / concordance | boundary claims, retrieval chunks, relationship objects |
| 8. Primary-sources (future) | source manifests + provenance chain |

## Coupling

Loose, by **contract** — not by submodule or merge. The upstream consumes this
repo's **validated release artifacts** (generated, provenance-stamped JSONL +
schemas), consistent with this repo's ADR-0001 (standalone semantic repo) and
the three-plane model in `MASTER_CONTEXT.md`. The shells differ in format; the
ontology stays continuous.

## Registration

This linkage is registered upstream in
`logos-governance-architecture/docs/roadmap/repository-integration-map.md`.
