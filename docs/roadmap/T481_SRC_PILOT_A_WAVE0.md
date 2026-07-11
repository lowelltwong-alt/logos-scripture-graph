# T481 SRC-PILOT-A Wave 0

Status: execution metadata-only, non-authorizing  
Date: 2026-07-10  
Authorization: SRC-PILOT-A (after governance PR #103 and scripture-graph PR #168)

## Purpose

Implement T469 Wave 0: metadata, rights, provenance, storage scaffold, and non-authorizing showcase shells for primary Bible witness comparison. No downloads, no restricted-image local storage, no source text import.

## Catalog root

`data/candidate/source_catalog/primary_bible_witnesses/`

## Validation

```bash
python scripts/validate_primary_bible_witness_catalog.py
python -m pytest tests/test_primary_bible_witness_catalog.py -q
```

## Non-authorizations

This wave does not authorize raw downloads, image storage, transcription import, preferred readings, direct ancestry claims, canonical changes, or graph/retrieval truth.
