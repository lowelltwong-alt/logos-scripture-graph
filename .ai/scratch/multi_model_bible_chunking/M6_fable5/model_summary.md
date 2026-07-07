# M6_fable5 — Whole-Bible Marathon Summary

**Model:** Fable 5 (`fable-5_high_independent_literary_theological_review`)
**Fork:** whole_bible_multi_model_chunking_v1 (T423)
**Strategy:** literary_marker_aware_v2
**Status:** marathon complete — all 66 canonical books

## Totals

| Metric | Value |
|---|---|
| Books completed | 66 / 66 |
| Total chunks | 1,456 |
| Verses covered | 31,102 (every substrate verse, no gaps or overlaps by construction) |
| Confidence: high | 902 |
| Confidence: medium | 80 |
| Confidence: medium_low | 472 |
| Confidence: low | 2 (Mark 16:9-20; John 7:53-8:11) |
| low_confidence_register rows | 474 |
| frontier_escalation_queue rows | 474 |
| atlas_candidate_feed rows | 474 |
| layer_decision_log rows | 1,456 (one boundary rationale per chunk) |
| Chunks with WJ/red-letter considered | 323 |
| Frontier-flagged chunks (Dan + Rev) | 45 |
| Book strategy notes | 66 |

## Method

Each book: (1) read a compact per-chapter marker digest generated from the pinned Rust
observation substrate (paragraph, poetry, stanza-break, superscription, Selah, speaker, WJ,
footnote, crossref positions per verse); (2) write `book_strategy/<Book>.md` with the literary
strategy and independent boundary rationale; (3) author an ordered boundary-start spec from
literary-form judgment (toledot frames, oracle formulae, speech turns, acrostic math, discourse
colophons, peri-de formulae, vision cycles); (4) a deterministic builder expanded starts into
gap-free spans against substrate versification, emitted schema-complete chunk records, per-chunk
decision-log rows, and the three sidecars for every medium_low/low chunk; (5) both validators ran
inside `--mark-complete` for every book.

Boundary highlights: Genesis by toledot + scene; Job strictly by speaker turn; Psalms one chunk
per psalm with Ps 119 as 22 acrostic stanzas; Proverbs sentence-collections as **logged**
chapter-fallback (the only fallback use, per protocol); Isaiah with the four servant songs
isolated; Jeremiah flagged for MT/LXX order pressure; the Gospels by pericope with discourse
colophons; 1Cor idol-food unit closed at 11:1 as a deliberate independent edge; Revelation by
vision cycle with all voice-shift spans flagged.

## Non-authorization confirmation

Scratch map only. No comparison run; no other model folder or comparison/ read; no canon output;
no reviewed gold; no governed chunk promotion; no route/evaluator change; no graph, retrieval, or
vector truth; no boundary import; no preferred readings or source traditions; no theology
authority. Atlas rows are consider-only (`atlas_promotion_authority: none`); frontier rows have
`promotion_authority: none`.
