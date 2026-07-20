# AI Workspace Architecture

Status: Human-authorized architecture revision 2, 2026-07-16.

## Mission and boundary

`AI.Workspace` is primarily a governed AI project, corpus, artifact, evaluation, and recovery workspace. It is not a personal home directory, active-development disk, credential store, private-client repository, or full-computer backup destination.

Lowell owns decisions. Local Git repositories own active code. Project source originals own acquired payload authority. Manifests and provenance support claims; generated outputs remain derived or candidate until reviewed and promoted.

## Four-dimensional mesh

### Vertical authority

`Lowell -> workspace governance -> project/AI-operations front door -> task/run manifest -> artifact -> evaluation -> human promotion`.

Lower-level evidence may challenge a higher-level assumption but cannot silently change authority. Releases and publications require a human promotion record.

### Horizontal interfaces

Projects connect to shared corpora, tools, experiment evidence, and AI operations through stable IDs, manifests, checksums, and typed references. Do not duplicate authoritative binaries across projects merely for convenience.

### Depth and trust layers

`incoming/quarantine -> source-originals + provenance -> derived-data -> evaluations/human-review -> release/publication`.

Secrets and private client data have no permitted layer inside this workspace. External private and computer-backup shares remain separate trust zones.

### Time and lineage

Material records should identify created/observed time, source and code revision, validity/review state, retention class, supersession, rollback, and next freshness trigger. Existing objects are never silently replaced; new revisions preserve lineage.

## AI operations portability

`08-AI-Operations` is the provider-neutral core. Runtime/provider bindings live only in `runtime-adapters/`. A runtime adapter may not redefine workspace authority, privacy, source custody, release gates, or project truth.

## Recovery

Repository mirrors, source originals, rights/provenance, human decisions, and approved releases are critical. Same-NAS snapshots help restore operations but are not independent backups. Maintain a separate device or offsite copy and periodically test restoration.
