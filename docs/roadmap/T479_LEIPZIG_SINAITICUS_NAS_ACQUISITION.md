# T479 — Leipzig Sinaiticus NAS IIIF Acquisition

**Status:** complete_verified
**Date:** 2026-07-18
**Agent:** Cursor
**Branch:** `codex/t479-leipzig-sinaiticus-acquisition`
**Worktree:** `../logos-scripture-graph-t479-worktree`

## Outcome

Governed acquisition of all Leipzig-held Codex Sinaiticus IIIF captures (reproduction + raking light) to NAS `Z:` storage, plus rights-gated metadata catalog for tracked witnesses.

| Metric | Value |
|--------|-------|
| Manifest SHA-256 | `af6a5f27302be89e8746a547db092a8650478db82c11ad7ea4b358b1072d91c8` |
| Canvases | 86 |
| Resources acquired | 172 |
| Failed | 0 |
| Total image bytes | ~877 MB (0.817 GiB) |
| Completion | `complete_verified` |

## NAS paths

- Source originals: `Z:\01-Projects\Logos\source-originals\manuscript-witnesses\greek_codices\codex_sinaiticus\leipzig\0000061851\`
- Catalog/evidence: `Z:\01-Projects\Logos\manuscript-witnesses\catalog\T479\`
- Provenance: `Z:\01-Projects\Logos\provenance\logos-scripture-graph\codices\T479\`
- Ops manifests: `Z:\08-AI-Operations\manifests\T479\`

## Resume / verify commands

```bash
python scripts/acquisition/run_acquisition.py --task-id T479 --mode status \
  --rights-ledger Z:/01-Projects/Logos/manuscript-witnesses/catalog/T479/rights_ledger.yaml \
  --nas-root Z:/01-Projects/Logos \
  --config scripts/acquisition/config/leipzig_0000061851.yaml

python scripts/acquisition/run_acquisition.py --task-id T479 --mode verify \
  --rights-ledger Z:/01-Projects/Logos/manuscript-witnesses/catalog/T479/rights_ledger.yaml \
  --nas-root Z:/01-Projects/Logos \
  --config scripts/acquisition/config/leipzig_0000061851.yaml

python scripts/acquisition/run_acquisition.py --task-id T479 --mode resume \
  --rights-ledger Z:/01-Projects/Logos/manuscript-witnesses/catalog/T479/rights_ledger.yaml \
  --nas-root Z:/01-Projects/Logos \
  --config scripts/acquisition/config/leipzig_0000061851.yaml
```

## Non-authorizations (unchanged)

No OCR, transcription, embeddings, canon changes, boundary import into default Scripture authority, publication, or redistribution.
