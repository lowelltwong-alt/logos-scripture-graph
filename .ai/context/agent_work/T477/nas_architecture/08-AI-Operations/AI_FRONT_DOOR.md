# AI Operations Front Door

This is the provider-neutral operating home for AI-mediated work across the NAS workspace. It stores compact manifests, handoffs, evaluations, proposals, derived artifacts, and runtime adapters—not private payloads, credentials, raw conversations, active Git worktrees, or project source authority.

## Read order

1. `\\UNAS-Pro\AI.Workspace\AI_FRONT_DOOR.md`
2. `\\UNAS-Pro\AI.Workspace\00-Governance\AI_WORKSPACE_ARCHITECTURE.md`
3. `AI_TABLE_OF_CONTENTS.md`
4. `WORKSPACE_MANIFEST.yml`
5. The relevant runtime adapter and task/run manifest

## Authority

Lowell retains human authority. Project repositories and source-original lanes retain local authority. AI operations coordinates and records work; it does not own project canon, client data, rights decisions, releases, or private shares.

## Write lanes

- `staging`: incomplete and unreviewed work.
- `derived-data`: reproducible cross-project AI artifacts.
- `evaluations`: validation and compatibility evidence.
- `rejected-outputs`: rejected artifacts retained for audit/evaluation.
- `manifests`: compact run, dependency, authority, checksum, and lineage descriptions.
- `handoffs`: compact task transitions without private payloads.
- `runtime-adapters`: provider/runtime-specific compatibility material.
