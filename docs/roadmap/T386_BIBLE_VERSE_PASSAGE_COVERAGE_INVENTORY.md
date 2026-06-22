---
object_type: roadmap_task_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-22 during T386 to document the Bible-wide verse/passage coverage gate before T385 owner decisions."
reason_for_inclusion: "Give future agents and auditors a human-readable explanation of the T386 coverage inventory, docket, validator, and non-authorizations."
---

# T386 Bible-Wide Verse/Passage Coverage Inventory

## Purpose

T386 adds a deterministic coverage layer before any new chunk-output work resumes. It accounts for
all 31,103 canonical 66-book passage records at triage depth and records which passages are routine
under existing policy, which need deeper research or review packets, which need owner decisions,
and which authority-changing uses remain blocked.

## Machine-Readable Surfaces

- `.ai/control/bible_verse_passage_coverage_inventory.jsonl` - one record per canonical passage.
- `.ai/control/bible_verse_passage_coverage_taxonomy.yaml` - status, flag, and decision taxonomy.
- `.ai/control/bible_verse_passage_coverage_summary.yaml` - corpus-wide counts and inventory hash.
- `.ai/control/bible_verse_passage_readiness_matrix.yaml` - book and lane readiness counts.
- `.ai/control/bible_verse_passage_gap_register.yaml` - unresolved risk/gap flags with samples.
- `.ai/control/bible_verse_passage_human_review_docket.yaml` - owner decisions, options,
  repercussions, recommendations, and stop conditions.

## Coverage Signals

T386 flags source metadata, Strong's-style metadata, Greek/Hebrew phrase/context needs,
textual-variant/source-tradition sensitivity, editorial cross-reference and intertext risk,
WJ/red-letter and speaker/discourse risk, divine-name/title capitalization sensitivity, known
non-orthodox pressure passages, theological downstream risk, owner-decision requirements, and
blocked authority actions.

## Next Step

The exact next non-output step remains T385, now using both T384 and T386:

- `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`
- `.ai/control/bible_verse_passage_coverage_summary.yaml`
- `.ai/control/bible_verse_passage_gap_register.yaml`
- `.ai/control/bible_verse_passage_human_review_docket.yaml`

## Non-Authorizations

T386 does not authorize target selection, reviewed-gold promotion, child spans, chunk output,
route/evaluator behavior, graph edges, retrieval truth, embedding/vector work, boundary import,
preferred readings, source-tradition preference, canon-scope change, whole-Bible output, or
denominational systematic theology as chunk authority.

## Validation

Run:

```bash
python scripts/validate_bible_verse_passage_coverage_inventory.py
python scripts/validate_all.py
python -m pytest -q
```
