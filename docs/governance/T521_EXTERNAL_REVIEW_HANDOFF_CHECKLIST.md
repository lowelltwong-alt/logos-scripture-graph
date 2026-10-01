# T521 external-review handoff checklist

This checklist is candidate-only and non-authorizing.

1. Run `python scripts/build_m7_sol_whole_bible_candidate_map.py` and verify the full-Bible map validator passes.
2. Run `python scripts/build_t521_external_convergence_request.py`.
3. Run `python scripts/build_t521_external_review_packet_index.py` and `python scripts/refresh_t521_packet_index_with_copy_prompt.py`.
   Also run `python scripts/build_t521_scaffold_hold_queue.py` and `python scripts/validate_t521_external_review_packet_index.py`.
4. Give the external reviewer only the packet index, its allowed inputs, and `docs/governance/T521_EXTERNAL_REVIEWER_COPY_PASTE_PROMPT.md`. Withhold sibling maps, Sol role reports, and boss rulings until the review is frozen.
5. Require a JSON receipt conforming to `config/agents/families/scripture-first-biblical-chunking/t521_external_review_receipt.schema.v1.json`, with all 66 books, literary findings, original-language risks, cross-reference leads, red-team tests, and preserved dissent/appeals.
6. Run `python scripts/validate_t521_external_review_receipt.py <receipt-path>` against the current map and prompt. A missing, stale, non-blind, incomplete, or self-attested receipt must fail.
7. Preserve the receipt as immutable evidence. Do not alter candidate chunks or promote boundaries based on agreement alone.
8. If the map changes after the receipt, discard its qualification for the new map and repeat from step 1.

The current readiness report is process evidence only. It does not count as independent literary validation.
