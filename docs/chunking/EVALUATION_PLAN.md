# Chunking Evaluation Plan

## Evaluation goals

The chunker is successful only if it produces chunks that are:

- text-faithful
- sentence-safe
- format-preserving
- context-aware
- genre-aware
- provenance-complete
- useful for retrieval

## Automated checks

1. No chunk ends mid-sentence.
2. Every chunk has OSIS start/end.
3. Every chunk has source text id and source artifact id.
4. Every chunk cites chunking policy version.
5. Every chunk has at least one boundary basis.
6. No chunk crosses book boundary.
7. No raw source file is modified.
8. No heading is orphaned.
9. No psalm superscription is orphaned.
10. Poetry markers are preserved in metadata.

## Manual gold set

Create gold boundaries for:

- Genesis 1-3
- Psalm 1, Psalm 23, Psalm 51, Psalm 119
- Proverbs 1-3
- Isaiah 6, Isaiah 40, Isaiah 53
- Matthew 5-7
- John 1
- Romans 1, 3, 7-8
- Hebrews 1-2
- Revelation 1, 12, 21-22

## Reviewer roles

- chunking architect
- biblical literature reviewer
- Hebrew reviewer
- Greek reviewer
- retrieval evaluator
- provenance validator

## Metrics

| Metric | Description |
|---|---|
| sentence_integrity_rate | percent chunks not ending mid-sentence |
| boundary_basis_coverage | percent chunks with explicit boundary evidence |
| genre_policy_coverage | percent chunks assigned correct genre policy |
| orphan_marker_count | headings/superscriptions/poetry markers detached from unit |
| retrieval_context_precision | percent retrieved chunks that include enough context for answer |
| reviewer_disagreement_rate | gold set disagreement across human reviewers |
