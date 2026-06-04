# ADR-0003: Chunks are derived artifacts

## Status

Accepted

## Decision

Chunks are not canonical text. Chunks are rebuildable retrieval objects derived from canonical source spans and boundary claims.

## Rationale

Bible chunking requires interpretive and editorial judgment. Treating chunks as canonical would confuse address identity, literary structure, translation formatting, and retrieval convenience.

## Consequences

Every chunk must record:

- source text id
- OSIS span
- included text spans
- boundary basis
- chunking policy version
- license
- provenance
- validation status

No chunk should be used as evidence without its source span and translation witness.
