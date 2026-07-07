# T467 Chunking Harness Hardening

T467 hardens the T423 multi-model scratch chunking harness after T465 found 78 harness-fix rows. The active overlay is `T467_literary_coherence_v1`. It does not rerun any model, compare outputs, promote reviewed gold, or write chunk output.

## Problem

T465 found a recurring pattern: `M1_cursor` and `M5_gemini_thinking` often chose smaller local units where `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, and `M6_fable5` preserved larger literary units.

The most common risk areas were:

- legal lists
- census and genealogy units
- tribal allotments
- battle reports
- worship or temple-service registers
- royal/administrative registers
- covenant-renewal units
- epistle closings and dense exhortation
- Strong's/original-language metadata being treated as a signal without enough literary reason

## Fix

T467 adds a future-rerun policy overlay:

- Preserve larger coherent units unless a function change is logged.
- Name the function of list/register material before splitting it.
- Require epistle-unit checks for greetings, thanksgivings, body argument, exhortation, travel notes, final greetings, doxology, and benediction where present.
- Treat Strong's, lemma, morphology, WJ/red-letter, headings, footnotes, and cross-references as evidence only.
- Require sidecar rows to name the concrete uncertainty rather than merely saying a model was low-confidence.

## Boundaries

This is harness policy only. It does not retroactively invalidate M1-M6. It does not run a new marathon. It does not authorize reviewed gold, chunk output, child spans, route/evaluator behavior, graph/retrieval/vector truth, source-tradition preference, canon change, Mark 16 inspiration decisions, or theology authority.

No T467 artifact authorizes output promotion or theological authority.

## Next Use

Future model reruns or new model slots must read the T467 overlay before chunking. A later task can decide whether to rerun M1/M5 or add M7 after the owner chooses the next comparison strategy.
