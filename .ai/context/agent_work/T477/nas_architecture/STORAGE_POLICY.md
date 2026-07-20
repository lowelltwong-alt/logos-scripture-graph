# Storage Policy

Status: Human-authorized workspace policy, revision 2, 2026-07-16.

## Purpose

This NAS workspace was provisioned primarily as a governed AI project, corpus, artifact, evaluation, and recovery surface. It is not the preferred location for active Git working trees, dependency environments, build caches, private human files, whole-computer images, or secrets.

## Core placement rules

- `repos` holds repository mirrors, bare repositories, Git bundles, or intentionally synchronized copies. Active development normally happens on a local SSD.
- `source-originals` holds immutable acquired source files. Every source family requires provenance, license or rights information, acquisition date, review state, and SHA-256 before downstream use.
- `staging` holds new, incomplete, or unreviewed work.
- `manifests` holds machine-readable descriptions of sources, runs, outputs, dependencies, authority, and checksums.
- `derived-data` holds rebuildable OCR, parsed data, chunks, graphs, embeddings, indexes, and other generated artifacts.
- `evaluations` holds test corpora, scorecards, comparison results, and validation evidence.
- `releases` and `publications` hold only human-approved artifacts.
- `archive` holds superseded but intentionally retained material.
- `08-AI-Operations` holds provider-neutral cross-project AI operating contracts, compact evidence, and runtime adapters.

## AI operations placement

`08-AI-Operations` is a portable core, not a provider-owned home directory. Stable authority, privacy, effects, lifecycle, and evidence rules live at its root. Provider/runtime bindings belong only under `runtime-adapters/`.

- Use `staging`, `derived-data`, `evaluations`, and `rejected-outputs` for task-authorized AI writes.
- Use `manifests` and `handoffs` for compact metadata and transitions; do not store private payloads or raw conversations.
- Do not duplicate project source authority, active Git worktrees, client data, or credentials in AI Operations.
- A runtime adapter cannot override workspace governance, project authority, source custody, or human promotion gates.

## Logos data placement

Store one authoritative physical copy of each raw text, archive, or manuscript image under `source-originals`; other Logos folders should normally contain catalogs, manifests, governed records, or references rather than duplicate binaries.

- `biblical-texts`, `manuscript-witnesses`, `original-languages`, `theological-corpus`, and `archaeology` are domain catalog and curated-record namespaces.
- `chunking`, `knowledge-graph`, and `vector-indexes` are governed projections and definitions. Large generated payloads belong under `derived-data`.
- `provenance` holds checksums, acquisition records, rights/license evidence, lineage, and source-to-output links.
- `human-review` holds decisions, adjudication records, and approval evidence.
- `rejected-outputs` holds failed or rejected AI results retained for evaluation or audit.

Do not copy local worktrees or their build, cache, virtual-environment, dependency, or test-temporary directories into NAS repository mirrors. A repository mirror and content-addressed artifact record should replace repeated worktree copies.

## Private and computer-backup shares

- `\\UNAS-Pro\Personal-Drive` is the existing private human-data share and is outside `AI.Workspace` and AI authority by default.
- `\\UNAS-Pro\ComputerBackups` is the existing machine-backup share and is outside `AI.Workspace` and AI authority by default.
- Do not create a redundant private-data or full-computer-image lane inside `AI.Workspace`.
- `06-Backups` is for AI-workspace snapshots and restore staging only. A same-NAS copy is not an independent backup.

## Capacity planning

Reserve at least 50 GB for initial Logos manuscript-image acquisition waves. Future permissioned high-resolution images may require 100–250 GB before OCR and derivatives. Maintain at least 500 GB free growth capacity while those lanes are active. Capacity reservations are planning controls, not acquisition authority.

## Integrity, lineage, and naming

- Preserve stable source, artifact, run, and capability IDs across revisions.
- Prefer SHA-256-addressed manifests and verification over filename trust.
- Never silently replace an object. Create a new revision and preserve lineage and rollback information.
- Record license, rights, sensitivity, trust zone, review status, created/observed time, validity, and retention class separately from location.
- Treat `07-Incoming` and `99-Quarantine` as untrusted until reviewed.

## Prohibited content

Secrets, credentials, API keys, authentication material, private client data, and full computer images must not be stored in `AI.Workspace`.
