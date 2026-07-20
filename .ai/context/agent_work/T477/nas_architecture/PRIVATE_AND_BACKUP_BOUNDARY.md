# Private And Computer-Backup Boundary

Status: Human-authorized workspace boundary, 2026-07-16.

## Existing external shares

- `\\UNAS-Pro\Personal-Drive`: private human files. This is the private area; do not duplicate it inside `AI.Workspace`.
- `\\UNAS-Pro\ComputerBackups`: computer and system backups. This is the machine-backup area; do not store full-drive images in `AI.Workspace`.

## Default AI rule

AI agents and AI-triggered automation have no authority to enumerate, read, index, copy, rename, delete, summarize, embed, or publish content from either external share unless Lowell explicitly authorizes the exact share, path, metadata/body scope, operation, destination, and time window.

Do not put secrets, credentials, authentication material, private client data, or filenames that disclose sensitive personal/legal/medical/financial facts in `AI.Workspace`. Sensitive filename metadata belongs behind the private-share boundary.

## Backup separation

`06-Backups` is for snapshots and restore staging of `AI.Workspace` itself. It is not a whole-computer backup target. Backups on the same NAS are not failure-independent; critical material also needs a separate device, system, or offsite copy.
