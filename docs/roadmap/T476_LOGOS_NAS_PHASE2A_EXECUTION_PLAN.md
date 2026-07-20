# T476 — Logos NAS Phase 2A Approved Execution Plan

**Owner authorization:** 2026-07-16, Lowell Wong.  
**Write boundary:** only the NAS paths listed below. New destinations only; if a destination exists, skip and report. Never overwrite or delete.

## Repository preservation

For each source repository, create one bare mirror and one all-ref bundle under `\\UNAS-Pro\AI.Workspace\01-Projects\Logos\repos\`:

| Source repository | Mirror | Bundle |
|---|---|---|
| `logos-scripture-graph-repo` | `logos-scripture-graph-repo.git` | `logos-scripture-graph-repo-2026-07-16.bundle` |
| `logos-governance-architecture` | `logos-governance-architecture.git` | `logos-governance-architecture-2026-07-16.bundle` |
| `logos-boundary-literature` | `logos-boundary-literature.git` | `logos-boundary-literature-2026-07-16.bundle` |
| `logos-doctrine-genealogy` | `logos-doctrine-genealogy.git` | `logos-doctrine-genealogy-2026-07-16.bundle` |

## Sanitized worktree snapshots

Create only these snapshots under `archive/worktree-snapshots/2026-07-16/`:

- `logos-scripture-graph-repo/`
- `logos-governance-architecture/`

Exclude `.git`, `data/raw`, generated `data/canonical`, `data/processed`, `data/derived`, `data/candidate`, build outputs, dependencies, virtual environments, caches, Rust targets, `.env*`, credential stores, browser profiles, and editor state. Raw source artifacts are copied only through the explicit list below.

## Named raw source artifacts

| Local source | NAS destination |
|---|---|
| `data/raw/bible/eng-web/usfm/eng-web_usfm.zip` | `source-originals/biblical-texts/eng-web/eng-web_usfm.zip` |
| `data/raw/original_language/greek/cntr_sr/raw/cntr_sr-4be18e67c687.zip` | `source-originals/original-languages/greek/cntr_sr/cntr_sr-4be18e67c687.zip` |
| `data/raw/original_language/greek/sblgnt/raw/sblgnt-c4d241a9c1c4.zip` | `source-originals/original-languages/greek/sblgnt/sblgnt-c4d241a9c1c4.zip` |
| `data/raw/original_language/greek/ugnt/raw/ugnt-6377ea89a718.zip` | `source-originals/original-languages/greek/ugnt/ugnt-6377ea89a718.zip` |
| `data/raw/original_language/hebrew/openscriptures_oshb/raw/openscriptures_oshb-3d15126fb1ef.zip` | `source-originals/original-languages/hebrew/openscriptures_oshb/openscriptures_oshb-3d15126fb1ef.zip` |
| `data/raw/original_language/hebrew/tanach_us_uxlc/raw/Tanach.xml.zip` | `source-originals/original-languages/hebrew/tanach_us_uxlc/Tanach.xml.zip` |
| Three named Leipzig showcase JPEGs | matching filename under `source-originals/manuscript-witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/web/` |

Copy the seven matching `source_manifest.yaml` files under `manifests/logos-scripture-graph/phase2a/2026-07-16/`, preserving their source-relative folder structure. Generate a SHA-256 and copy/provenance receipt under `provenance/logos-scripture-graph/phase2a/2026-07-16/`.

## Verification and stop conditions

- Verify each mirror with `git fsck --full` and each bundle with `git bundle verify`.
- Hash each named raw source locally and at the NAS; source and destination SHA-256 must match.
- Stop the affected copy on inaccessible source, existing destination conflict, copy failure, or checksum mismatch. Continue only with unrelated approved items and report every skipped/failed item.
- Do not create NAS navigation files, store generated data, copy any additional worktree, or write under releases, publications, knowledge-graph, or vector-indexes.

## Execution result — blocked before copy

Execution began on 2026-07-16 and stopped at the first write attempt because the mapped NAS volume reported **9,719,808 bytes (9.3 MB) free of 8,000,000,000 bytes (7.5 GB)**. This is far below the required capacity for even the first Git mirror.

- All four `git clone --mirror` attempts failed with `No space left on device`.
- All four bundle attempts failed before creation with `No space left on device`.
- The first raw-source destination directory could not be created; no raw source file was copied.
- Read-only inspection after the failure found no files under `repos/`, `archive/`, or `source-originals/`; no partial destination needs cleanup.
- No overwrite, delete, snapshot copy, source copy, checksum generation, OCR, source import, graph/vector operation, release, or publication occurred.

**Resume condition:** Lowell must provide or approve a NAS destination/quota with sufficient free space. The minimum safe capacity should exceed the selected snapshot and source scope plus working headroom; the original full Phase 2A selection cannot fit on the currently mapped 7.5 GB volume.
