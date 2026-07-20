# T477 NAS Architecture Revision Receipt

- observed_at: 2026-07-16 America/New_York
- human_owner: Lowell Wong
- change: workspace architecture v1 -> v2 plus provider-neutral `08-AI-Operations`
- private_share: `\\UNAS-Pro\Personal-Drive` (external; AI prohibited by default)
- computer_backup_share: `\\UNAS-Pro\ComputerBackups` (external; AI prohibited by default)
- existing_project_payloads_moved_or_deleted: false
- private_or_backup_share_contents_accessed: false

## Preserved revision hashes

| Preserved file | SHA-256 |
|---|---|
| `root_AI_FRONT_DOOR.md` | `B17CFA4FEA2DF168CB25245D27C05E704DFE57C764C1871F1F45AA07150D7D2D` |
| `root_AI_TABLE_OF_CONTENTS.md` | `63B310CD8DCE3CCFB97088B625F403BECAFD2FCE83E9CF2FC090453F564EBC1B` |
| `WORKSPACE_MANIFEST.yml` | `BC0D32F495ECAD0088D768E24ED2806973A577C970253E460BE8598085F6FB11` |
| `STORAGE_POLICY.md` | `B5BEB22988B359B38AB5FACD0374343931AE870A2F74D687A08867F978C84114` |

## Promoted revision hashes

| Promoted file | SHA-256 |
|---|---|
| `AI_FRONT_DOOR.md` | `E3077DAD0ED43D316FA9C9E20457FD161F1E4F582307115F01C363E5D7E5D6F8` |
| `AI_TABLE_OF_CONTENTS.md` | `78FA33A3F030DD172CA44179CE6088D5EE1636C14757C4AB2EEC1E874E314B45` |
| `00-Governance/WORKSPACE_MANIFEST.yml` | `AD0F70C9BE5E5A8FEA63BED60D3818DB2A3BAAD69A2E62444E85FD4D17874A9D` |
| `00-Governance/STORAGE_POLICY.md` | `2A0D06EBAAF4FDC7522D5A939D16A09C1BC3E49AA4957548B465F4A85A1BE8EB` |
| `00-Governance/AI_WORKSPACE_ARCHITECTURE.md` | `0C929ADA51F5FA6E0C5CA44EFB6EA2F1C5C2B4A36C1F8CAE923F7E2C27A55B10` |
| `00-Governance/PRIVATE_AND_BACKUP_BOUNDARY.md` | `647CD32B48147F2DD89303F95241D5D764C3509A20B70013AE838705044E02CF` |
| `08-AI-Operations/AI_FRONT_DOOR.md` | `6F890520B4938E8386A43FE3DAF5D35B677598F4F835A44ADA7D94D8F727C9B7` |
| `08-AI-Operations/AI_TABLE_OF_CONTENTS.md` | `6E3819AD686AE9D6F73D7D23D5C0BD483EC29217EE1244C9F10A0B8EB43F6C06` |
| `08-AI-Operations/WORKSPACE_MANIFEST.yml` | `26DA68BAC6EEDAC966E06D424547438E26CBD03661E172C9D551C99136C0D25E` |
| `08-AI-Operations/runtime-adapters/codex/README.md` | `1A23B78C6BB8F193DE0733DDABBBC0D3B74C98D1C90CFF4BF6FF9176215E6D19` |

## Validation

- Every promoted source/destination hash matched.
- Both YAML manifests parsed successfully.
- All seven required AI-operations lanes exist.
- Prior governance files remain preserved at `00-Governance/history/2026-07-16-pre-t477/`.

## Learning-loop candidate

- issue_class: UNC share-root parent creation
- observation: `Split-Path -Parent` of a root-level file returned the existing UNC share root, and calling `New-Item` on that share root raised `The path is not of a legal form`.
- correction: create a destination parent only when `Test-Path -LiteralPath $parent` is false.
- outcome: retry promoted all files and produced matching SHA-256 evidence.
- scope_limit: Windows PowerShell UNC promotion scripts; no general filesystem or NAS-server claim.
