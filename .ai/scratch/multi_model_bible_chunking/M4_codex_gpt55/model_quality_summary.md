# M4 Model Quality Summary

- model_id: M4_codex_gpt55
- strategy_id: literary_marker_aware_v2
- books_completed: 66/66
- chunk_count: 1319
- low_confidence_register_rows: 986
- frontier_escalation_rows: 986
- atlas_candidate_rows: 986
- raw_usfm_reads: 0
- substrate_first: true
- research_baseline_read: true

## Quality Notes

The pass uses the Rust no-text observation substrate as the first evidence layer and keeps raw USFM closed. Strong's Greek/Hebrew metadata, WJ/red-letter markup, headings, paragraph markers, poetry markers, footnotes, cross-references, and source metadata are evidence only. They are surfaced in chunk records and sidecars without becoming theology, speaker attribution, textual-critical, graph, retrieval, or boundary authority.

Chapter-only fallback is logged through confidence and sidecars when it appears in marker-rich or fragile regions. Daniel and Revelation carry frontier flags on every chunk.
