# T465 Harness Triage

Status: non-authorizing reconciliation evidence only.

No reviewed gold, no chunk output, no child spans, and no route or evaluator changes are authorized by this triage.

Source: `.ai/scratch/multi_model_bible_chunking/comparison/harness_improvement_queue.md` and T464 summary artifacts.

T464 reported 78 `harness_fix_or_rerun_required` rows. The dominant pattern is a literature-routing split: `M1_cursor` and `M5_gemini_thinking` often over-split or use smaller local units where `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, and `M6_fable5` preserve larger literary units. This is a prompt/harness signal, not an automatic model-ranking decision.

## Book Concentration

- Exod: 13 rows
- 2Chr: 10 rows
- 1Sam: 9 rows
- 2Sam: 7 rows
- Josh: 6 rows
- Num: 6 rows
- 2Kgs: 5 rows
- Gen: 5 rows
- 1Chr: 4 rows
- 1Kgs: 4 rows
- Col: 2 rows
- Neh: 2 rows
- Phil: 2 rows
- 1John: 1 row
- 2Thess: 1 row
- Judg: 1 row

## Likely Prompt Failures

### Narrative, legal, and list material

Exodus, Numbers, Joshua, Samuel, Kings, Chronicles, and Nehemiah rows suggest the harness needs stronger guidance for preserving legal-list, census, tribal-allotment, battle-report, temple-service, and administrative-register units when they function as a single literary or covenantal unit.

Likely failure: smaller marker-aware splits were allowed to outrun larger discourse/literary coherence.

Needed fix before rerun: require the strategy file to name whether the book section is legal list, census, allocation, worship/temple register, battle report, succession narrative, or covenant renewal before choosing local boundaries.

### Epistle closings and dense exhortation

Colossians, Philippians, 1 John, and 2 Thessalonians rows suggest the harness needs more explicit epistle-argument and closing-instruction handling.

Likely failure: local paragraph boundaries were treated as enough evidence without testing whether a paraenetic unit, warning, command cluster, or closing commission should remain intact.

Needed fix before rerun: require each epistle strategy to identify greeting, thanksgiving, body argument, exhortation, household/mission instructions, travel notes, final greetings, doxology, and benediction if present.

### Original-language metadata noise

Most T464 routes include `strongs_original_language_metadata`. Strong's, lemma, and morphology indicators are evidence and lookup hints. They do not by themselves create risk, select boundaries, or authorize a theological reading.

Needed fix before rerun: require models to distinguish observed source metadata from boundary authority in every strategy note.

## Recommended Harness Changes

1. Add a pre-boundary checklist for literary form before chunking each book section.
2. Add explicit "do not over-split lists/registers unless the list changes function" language.
3. Add epistle-argument and closing-unit checks.
4. Require sidecar explanation whenever a model rejects a larger `M2/M3/M4/M6` unit in favor of smaller `M1/M5` splits.
5. Keep every low-confidence, frontier, and atlas row tied to a concrete reason, not merely a model name.

## Non-Authorizations

This triage does not authorize reviewed gold, chunk output, child spans, target selection, route/evaluator behavior, graph/retrieval/vector truth, source-tradition preference, canon change, Mark 16 inspiration status, or theology authority.
