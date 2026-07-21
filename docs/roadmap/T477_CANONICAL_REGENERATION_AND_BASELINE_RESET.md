# T477 — Owner-Approved Canonical Regeneration And Baseline Reset

**Status:** in_progress  
**Authority:** T476 Option A (`authorize_T477_canonical_regeneration: true`)  
**Predecessor:** T475 independent audit PASS + T476 owner decision A

## Purpose

Regenerate local ignored eng-web canonical/processed surfaces with the post-T519
importer (`--canonical-66-filter`), then treat the audited candidate counts as the
new corpus baseline. This is a **source-integrity / baseline reset**, not a
chunking improvement.

## In scope

1. Run `python pipelines/ingest/usfm_importer.py --canonical-66-filter`
2. Refresh `.ai/control/DATA_MAP.md` to the new counts
3. Retire the T475 transitional “candidate while baseline held” DATA_MAP / focus hack
4. Keep gold/chunker/pilot migrations deferred until T478–T479 where required
5. Full `validate_all` + pytest under the new baseline rules

## Out of scope / non-authorizations

- `data/raw/` mutation
- reviewed gold edits (T478–T479)
- chunk output / child spans (T480+)
- route or evaluator behavior changes
- graph / retrieval / vector / index truth
- preferred reading, canon scope, theology authority
- T500 pilot activation

## Expected corpus delta vs pre-T474 baseline

| Surface | Expected |
|---|---|
| Footnotes | 1130 (unchanged count; heading footnotes preserved) |
| Word tokens | 677686 (2 bogus Ps.119 heading tokens removed) |
| Passages | 31103 |
| Cross-refs | 340 |

## Follow-on

- **T478:** Psalm 119 / Psalm 78 reviewed-gold re-review (no gold edits yet)
- **T479:** Owner-approved gold / guardrail correction
- **T480:** Route-isolated consumer repair
- Then T500 candidate-only controlled pilots
