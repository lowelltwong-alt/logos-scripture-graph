# T477 — UNAS AI Workspace Architecture

## Outcome

The NAS is primarily a governed AI project and artifact workspace. Active Git development remains on local SSD worktrees; the NAS stores source originals, repository mirrors, reproducible artifacts, evaluations, run evidence, and approved releases.

The architecture adds `08-AI-Operations` as a provider-neutral AI operations home. Runtime-specific material is isolated under `runtime-adapters/`, beginning with `runtime-adapters/codex`, so the workspace does not depend on one model or host product.

## Mesh

- **Vertical authority:** Lowell -> workspace governance -> project front doors -> task manifests -> generated artifacts.
- **Horizontal interfaces:** projects reference shared corpora, shared tools, experiment evidence, and AI operations through manifests rather than duplicated payloads.
- **Depth:** source original -> provenance/manifest -> derived artifact -> evaluation -> human gate -> release/publication.
- **Time:** every material artifact has revision, observed/created time, lineage, retention class, and supersession or rollback path.

## Privacy and backup boundary

- `\\UNAS-Pro\Personal-Drive` already exists and is the private human-data share. It is not an AI workspace and is out of AI scope by default.
- `\\UNAS-Pro\ComputerBackups` already exists and is the machine-backup share. It is not an AI workspace and is out of AI scope by default.
- `\\UNAS-Pro\AI.Workspace` must not contain secrets, authentication material, private client data, or full computer images.
- `06-Backups` remains for AI-workspace snapshots and restore staging only; same-NAS copies are not independent backups.

## AI operations home

`08-AI-Operations` contains provider-neutral operating contracts and these lanes:

- `staging`: incomplete task material and proposals.
- `derived-data`: reproducible cross-project AI artifacts.
- `evaluations`: capability and workflow evidence.
- `rejected-outputs`: rejected artifacts retained for audit/evaluation.
- `manifests`: run, dependency, authority, and checksum descriptions.
- `handoffs`: compact cross-task handoffs without private payloads.
- `runtime-adapters/codex`: Codex-specific invocation and compatibility material.

It is not a home directory, credential store, chat archive, or replacement for local Git worktrees.

## Existing data

No existing project, LawFirm source snapshot, Logos folder, backup share, release surface, or private share is moved or deleted by T477.
