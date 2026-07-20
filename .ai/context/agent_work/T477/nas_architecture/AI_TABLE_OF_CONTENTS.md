# AI Workspace Table of Contents

| Path | Role | Use when |
|---|---|---|
| `AI_FRONT_DOOR.md` | Workspace entrypoint and authority boundary | Starting any AI task |
| `00-Governance\WORKSPACE_MANIFEST.yml` | Machine-readable structure and policy | Resolving storage or permissions |
| `00-Governance\AI_WORKSPACE_ARCHITECTURE.md` | Four-dimensional authority/data/lifecycle architecture | Designing or changing the workspace |
| `00-Governance\PRIVATE_AND_BACKUP_BOUNDARY.md` | Separation from private and computer-backup shares | Handling private data or backup questions |
| `01-Projects\LawFirm-OS\AI_FRONT_DOOR.md` | LawFirm data routing | Working on public ATS or Nevada Bar data |
| `01-Projects\Logos\AI_FRONT_DOOR.md` | Logos data routing | Working on Scripture Graph data |
| `02-Shared-Corpora` | Authorized cross-project corpora | Referencing shared source families |
| `03-Shared-Tools` | Shared deterministic tools and validators | Running approved tooling |
| `04-Experiment-Ledger` | Run manifests and evidence | Recording reproducible runs |
| `05-Releases-and-Exports` | Human-approved cross-project outputs | Publishing approved artifacts |
| `06-Backups` | AI-workspace snapshots and restore staging | Workspace recovery only |
| `07-Incoming` | Human-controlled untrusted intake | Routing newly received material |
| `08-AI-Operations\AI_FRONT_DOOR.md` | Provider-neutral AI operations home | Cross-project AI workflow and runtime adapters |
| `99-Quarantine` | Isolated unsafe or unresolved material | Provenance, integrity, sensitivity, or rights problems |

External shares `\\UNAS-Pro\Personal-Drive` and `\\UNAS-Pro\ComputerBackups` are not part of `AI.Workspace` and are out of AI scope by default.
