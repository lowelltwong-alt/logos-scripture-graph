# ADR-0007: Provenance canonicalization

## Status

Accepted (direction) — migration deferred to a dedicated task

## Context

Every generated record currently carries inline provenance fields (`source_id`,
`source_archive`, `source_sha256`, `source_format`, `license`, `generation_method`).
The WEB ingest duplicates the same `source_sha256` across ~864,904 records (PROV-1).
If a manifest checksum is ever corrected, every record diverges with no join key,
forcing a full re-ingest with no way to diff "what provenance changed".

## Decision

1. Introduce a `ProvenanceRecord` (future `schemas/provenance_record.schema.json`):
   a single record per `(source_id, source_sha256, generation_method)` triple with a
   stable `provenance_id`.
2. Generated records reference `provenance_id` instead of repeating all provenance
   fields inline. A small denormalized subset (`source_id`, `license`) may remain for
   convenience, but `source_sha256` lives canonically in the ProvenanceRecord.
3. The importer emits the ProvenanceRecord once and stamps `provenance_id` on outputs.

## Consequences

- A manifest correction updates one ProvenanceRecord; record→provenance joins stay valid.
- Smaller records; the 432 MB `word_tokens.jsonl` shrinks materially.
- Requires a one-time migration of existing canonical data (deterministic, scriptable).

## Why deferred

This is a P1 "before scale" change, not a "before next step" blocker. Rushing an
864k-record migration alongside the CANON-1 re-ingest risks two concurrent data
rewrites. Sequence it as its own task after the canon re-ingest is committed and green.
