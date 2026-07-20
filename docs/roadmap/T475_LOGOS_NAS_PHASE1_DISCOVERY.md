# T475 — Logos NAS Phase 1 Read-Only Discovery

**Date:** 2026-07-16  
**Status:** complete — no NAS mutation, copying, mirroring, scheduling, enrollment, or release action was performed.

## Decision summary

`\\UNAS-Pro\AI.Workspace\01-Projects\Logos` is reachable and has the requested 20-folder structure, but every folder is empty. There is no destination conflict, existing corpus, release, vector index, or NAS manifest to merge with. Local Git worktrees remain the source authority.

The local family must not be treated as one copyable directory. `logos-scripture-graph-repo` has a shared Git object store with many linked worktrees; a normal Git mirror or bundle does **not** preserve raw assets, ignored/generated material, untracked changes, or detached worktree heads. Any later backup must separate Git history from approved filesystem snapshots.

## Read-only scope and evidence

- Read the local project front door, master context, status, data map, raw-source inventory, DAD integration/context map, and existing subagent-family plan.
- DAD preflight found DAD available only as candidate routing memory. Its available reusable records concern validation and subagent patterns, not NAS storage. No DAD enrollment, outbox write, or authority transfer occurred.
- Used three bounded, read-only scouts: repository/Git topology; NAS inventory; and source-routing classification. The third scout was stopped before completion rather than allowing an unbounded scan; the lead completed its limited classification from local manifests and metadata.
- No source text or private file contents were reported. No source, credential, or browser-profile path was copied or read.

## Current inventory

### NAS destination

| Area | Files | Status | Phase 2 implication |
|---|---:|---|---|
| All 20 specified Logos folders | 0 | Empty skeleton | Create only expressly approved child paths; no conflicts now. |
| `source-originals`, `repos`, `releases`, `publications` | 0 | Protected destinations | Require separate owner approval; do not use for staging. |
| `knowledge-graph`, `vector-indexes` | 0 | No current NAS graph/index truth | Keep empty unless a later, separately authorized task opens those lanes. |

### Local Scripture Graph data surface

| Local family | Approx. files / size | Provenance or sensitivity signal | Proposed NAS destination (proposal only) |
|---|---:|---|---|
| `data/raw/bible/eng-web` | raw source manifest + WEB USFM ZIP; raw family total is ~62 MB | Source manifest present | `source-originals/biblical-texts/eng-web/` plus `manifests/logos-scripture-graph/` and `provenance/`. |
| `data/raw/original_language` | Greek/Hebrew source ZIPs and manifests | Source manifests present | `source-originals/original-languages/<family>/` plus matching manifests/provenance. |
| Leipzig Codex Sinaiticus showcase | three web JPEG derivatives (~3.3 MB) + source manifest | Permission/provenance is scoped to Leipzig-held digitized images | `source-originals/manuscript-witnesses/codex-sinaiticus/leipzig/`; preserve manifest, permission record, IIIF identity, and checksums. |
| `data/canonical` | ~552 MB generated canonical outputs | Generated/rebuildable; canonical-66 governed locally | `derived-data/logos-scripture-graph/canonical/` only if an approved snapshot is needed; never replace local authority or call it a release. |
| `data/processed` | ~89 MB | Reproducible pipeline output | `derived-data/logos-scripture-graph/processed/` only. |
| `data/candidate` | ~61 MB | Candidate evidence, not truth | `derived-data/logos-scripture-graph/candidate/`, with candidate/trust-zone metadata; not `knowledge-graph`. |
| `data/derived` | ~33 MB | Rebuildable derivative | `derived-data/logos-scripture-graph/derived/` only. |
| Task plans, source manifests, source catalog, rights/provenance records | small control/metadata surfaces | Candidate evidence and governance metadata | `manifests/logos-scripture-graph/` and `provenance/logos-scripture-graph/`; do not mix with source bitstreams. |
| Future patristics / non-66 / archaeology materials | no authorized local corpus in this scan | Boundary/supporting material; rights and canon lane unresolved | Separate later owner-approved lanes under `theological-corpus/`, `archaeology/`, and `source-originals/`; never mix with canonical 66 data. |

### Git family and shared-object topology

| Repository / checkout | Approx. footprint | State observed | Phase 2 repository treatment |
|---|---:|---|---|
| `logos-scripture-graph-repo` | ~7.37 GiB working tree; shared `.git` ~163 MiB | Dirty (10 tracked, 40 untracked paths at scan) | `repos/`: bare mirror **and** bundle; separate owner-approved non-destructive filesystem snapshot if current assets/changes must be preserved. |
| Linked Scripture Graph worktrees `t487`, `t493`, `t494`, `t495`, `t497`, `t498` | ~5.55 GiB combined | t493–t495 dirty; shared object store | Do not duplicate into `repos/`. Record worktree/head mapping; only snapshot a named worktree if approved. |
| `logos-governance-architecture` | ~198 MiB | Dirty (37 tracked paths) | Bare mirror + bundle; a separate approved snapshot is needed to preserve uncommitted state. |
| `logos-boundary-literature` | ~726 KiB | Clean | Bare mirror. |
| `logos-doctrine-genealogy` | ~436 KiB | Clean | Bare mirror. |
| `noesis-atlas` | ~220 KiB | Dirty (3 untracked paths) | Treat as adjacent, not automatically Logos scope; only include after owner confirmation. |

There are additionally many registered `_codex_worktrees` (about 26.2 GiB apparent size) and worktrees outside the scanned `03_World_View` directory. They are not safe to copy as a group and were not inspected as source content. At least two registered worktrees were detached at the time of scan; a mirror/bundle can omit unreachable detached commits unless a later plan records/protects them first.

## Phase 2 exclusions

- Other active worktrees and their uncommitted files, unless Lowell names them for a snapshot.
- `node_modules`, `.venv`, Python caches, Rust `target/`, build directories, editor state, browser profiles, credential stores, `.env`, secrets, and private client data.
- Rebuildable generated output unless an approved recovery snapshot has a stated retention purpose.
- Any automatic graph/vector index, release/publication package, OCR/transcription, or source import.

## Proposed workstream assignments

| Workstream | Role and effort | Output | Independent check |
|---|---|---|---|
| Repository topology | Luna / low metadata scout | Git-root, common-object-store, worktree/head map | Deterministic `git worktree` and `git count-objects` replay. |
| Corpus and artifact classification | Luna / medium source-catalog scout | Source/derived/candidate classification and candidate destination map | `governance_evidence_reviewer` checks scope and trust zones. |
| Rights and provenance | `rights_provenance_scout`, Luna / medium | Permission and attribution matrix before any source copy | Manifest/rights evidence check; no implied AI or redistribution rights. |
| NAS copy design | Terra / medium planner | Exact source/destination/exclusion/retention/checksum plan | Independent Terra/medium routing review before owner approval. |
| Execution, only after approval | Main agent owns all writes | Resumable, non-destructive copy receipt and checksum verification | Post-copy file-count/checksum/residual check. |

These assignments reuse the existing repository-local subagent briefs. They are not persistent agents, live automations, or delegated authority. Ultra effort is not authorized or needed.

## Human gate for Phase 2

Before any NAS write, Lowell must approve an exact plan specifying:

1. Which named repositories receive a bare mirror, bundle, and/or a current-worktree snapshot.
2. Which raw source families and derived artifacts are copied, with exact child destinations and retention purpose.
3. Conflict behavior (`skip`, preserve-and-report; never overwrite or delete), projected storage use, and checksum method.
4. Whether to create the proposed NAS navigation and manifest files; they were deliberately not created in Phase 1.
5. Whether adjacent repositories such as `noesis-atlas` and any external worktrees are in scope.

Until that approval, the next allowed action is only to refine this proposed routing table or answer questions about it.
