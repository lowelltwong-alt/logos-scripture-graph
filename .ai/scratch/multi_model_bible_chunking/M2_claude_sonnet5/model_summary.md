# M2 Claude Sonnet 5 — Whole-Bible Chunk Marathon Summary

**Status:** `marathon_complete` | **Books:** 66/66 | **Total chunks:** 1,135

## Result

All 66 canonical books chunked independently into `book_chunks/<Book>/chunks.jsonl`, merged into
`whole_bible_chunk_map.jsonl` (1,135 chunks), and validated:

```
python scripts/validate_whole_bible_chunk_map.py .ai/scratch/multi_model_bible_chunking/M2_claude_sonnet5 --require-full-bible
OK

python scripts/validate_t423_literary_quality_protocol.py --model-folder .ai/scratch/multi_model_bible_chunking/M2_claude_sonnet5 --require-artifacts
T423 literary quality protocol: OK
```

## Method

Every chunk boundary is grounded in one or more of: (a) real Rust observation-substrate data
(chapter verse-counts, paragraph/poetry/Selah/superscription marker positions, WJ/red-letter
marker presence, chapter-level risk flags), cross-checked verse-by-verse against known content
where the substrate flagged something notable (poetic insets, liturgical refrains, textual-
variant-adjacent formatting); (b) well-established literary/compositional structure (toledot
formulas, epistolary argument shape, prophetic oracle/vision cycles, Gospel discourse units,
Revelation's own explicit septet/interlude structure); or (c) the book's own internal markers
(e.g., Proverbs' explicit collection headings, the recurring refrain in Song of Songs).

No chunk uses a silent chapter-only default: where a chunk happens to match one chapter exactly,
that is because the chapter genuinely is the natural unit for that content (e.g., each Psalm,
each Lamentations acrostic, Ruth's four acts), not an unexamined fallback — and the literary
quality protocol's chapter-fallback rule (forcing `medium_low` confidence on marker-rich or
pilot-fragile exact-chapter matches) was applied throughout and caught one real omission (Job,
Wave 3), which was fixed and re-validated.

## Aggregate statistics

| Metric | Count |
|---|---:|
| Total chunks | 1,135 |
| Low-confidence register rows | 580 |
| Frontier escalation queue rows | 580 |
| Atlas candidate feed rows | 580 |
| Pilot books complete | Gen, Ps, Phlm, Jonah, Rev (all 5) |
| Frontier books complete | Dan, Rev (both, `frontier_flag_considered: true` on every chunk) |

## Owner gate override

`pilot_gate.status` remained `pending` throughout this marathon. The owner explicitly authorized
continuing past the pilot-book set into the full 66-book marathon before the gate flipped to
`go` (recorded as an `owner_gate_override` in `layer_decision_log.jsonl`). This means
`scripts/validate_t423_pilot_gate.py` will report this model folder as out of compliance with
the pilot-only restriction until `pilot_gate.status` is set to `go` or the override is otherwise
formally recorded in the fork policy itself — this is the expected, previously-disclosed
consequence of that decision, not a new problem.

## Parallel-model observation (discovered at completion, not sought out)

Running `scripts/t423_marathon_status.py` after finishing showed that three other model slots
(M3_claude_frontier, M4_codex_gpt55, M6_fable5) also report `marathon_status: complete` with
66/66 books — apparently completed by separate sessions running in parallel while this marathon
was in progress. Per the fork's isolation rules, this model's marathon proceeded without reading
any other model's folder, `comparison/` outputs, or T417 batch2 material at any point. Per
`t423_marathon_status.py`: `complete_model_count: 4`, `ready_for_batch_compare: true` (minimum 3
met), `ready_for_default_compare: false` (initial target of 5 not yet met — M1_cursor and
M5_gemini_thinking remain `pending`/`optional_pending`). Whether and when to run
`compare_multi_model_bible_chunk_maps.py` is an owner/integrator decision, not made here.

## Non-authorizations restated

Every one of the 1,135 chunks and all 580×3 sidecar rows carry `non_authorizing: true`;
`promotion_authority: none` and `atlas_promotion_authority: none` throughout. This marathon does
not create reviewed gold, canon output, child-span authority, route/evaluator behavior,
graph/retrieval/vector truth, atlas promotions, or theology authority. No WJ/red-letter marker
ever authorizes speaker or discourse attribution (CD-021/CD-022). No boundary, literature-type
label, or intertextual note anywhere in this map resolves any messianic, eschatological,
election/predestination, textual-variant, or other disputed doctrinal question — all such content
is flagged for downstream awareness only. Revelation and Daniel chunking remains structural
observation only and does not constitute Revelation implementation under the repo's existing
REV-T344-E research/prep-only governance.
