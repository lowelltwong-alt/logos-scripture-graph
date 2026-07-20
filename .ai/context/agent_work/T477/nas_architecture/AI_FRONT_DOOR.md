# AI Workspace Front Door

This NAS was provisioned primarily as a governed AI project, corpus, artifact, evaluation, and recovery workspace. Start here for every AI task on this workspace.

## Read order

1. `AI_TABLE_OF_CONTENTS.md`
2. `00-Governance\WORKSPACE_MANIFEST.yml`
3. `00-Governance\AI_WORKSPACE_ARCHITECTURE.md`
4. `00-Governance\PRIVATE_AND_BACKUP_BOUNDARY.md`
5. The relevant project or AI-operations front door and table of contents
6. The relevant project/run manifest before reading or writing data

## Authority

Lowell is the human owner and approval authority. Local Git repositories on the SSD remain code authority. The NAS stores authorized corpora, immutable source snapshots, repository mirrors, derived data, evaluations, run evidence, backups, and approved releases.

AI may write freely only inside task-authorized `staging`, `derived-data`, `evaluations`, and `rejected-outputs` lanes. Never overwrite `source-originals`. Never promote into `releases` or `publications` without human approval. Do not store secrets, credentials, authentication material, API keys, private client data, or full computer images in `AI.Workspace`.

## Routes

- LawFirm-OS: `01-Projects\LawFirm-OS\AI_FRONT_DOOR.md`
- Logos: `01-Projects\Logos\AI_FRONT_DOOR.md`
- Provider-neutral AI operations: `08-AI-Operations\AI_FRONT_DOOR.md`

## External privacy boundary

- `\\UNAS-Pro\Personal-Drive` is the existing private human-data share. AI has no access authority by default.
- `\\UNAS-Pro\ComputerBackups` is the existing machine-backup share. AI has no access authority by default.

Use UNC paths. Do not assume `Z:` exists in every process context.
