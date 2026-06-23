---
object_type: roadmap_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-23 during T398 from T384/T386 whole-corpus research evidence and the owner's request to complete phase-one research before tighter focused research."
reason_for_inclusion: "Give humans and no-context agents a readable summary of what phase one proves, what it does not prove, and which human decisions Goal 2 should prepare."
---

# T398 Bible-Wide Phase-One Research Synthesis

T398 completes a phase-one whole-corpus research synthesis. It does not claim every verse has been deeply exegeted. It does prove that every canonical 66-book passage is accounted for at T386 triage depth, every canonical book is present in the research registry, and the remaining human decisions can now be queued from evidence instead of chat memory.

Primary control surface:

```text
.ai/control/t398_bible_wide_phase_one_research_synthesis.yaml
```

## What Phase One Proves

- `66` canonical books are present in the Bible-wide research registry.
- `31,103` canonical passage records are accounted for in the T386 coverage inventory.
- `16,377` passage records are routine under existing policy.
- `12,625` passage records need deeper review.
- `1,940` passage records are blocked before chunking.
- `161` passage records require human decisions at pressure-passage depth.
- `13,061` passage records carry review-packet/theological downstream risk flags.

## What Phase One Does Not Prove

- It is not deep verse-by-verse exegesis.
- It does not select the next target.
- It does not promote reviewed gold.
- It does not authorize child spans.
- It does not authorize chunk output, route/evaluator behavior, graph/retrieval/vector truth, boundary import, preferred readings, source-tradition preference, canon-scope change, source/manuscript rows, or theology authority.

## Human Decision Prompts

T398 records `T398-HDP-001` through `T398-HDP-009`:

- Goal 2 focused research scope and ordering.
- Torah/narrative/legal candidates.
- Prophetic/source-tradition candidates.
- Gospel/WJ research order.
- Acts as a distinct narrative/speech transition lane.
- Wisdom/dialogue/poetry research order.
- Metadata/original-language evidence-only handling.
- Variant/source-tradition timing.
- Whole-Bible output remains blocked until multiple lane pilots mature.

## Recommended Next Goal Prompt

```text
New goal: Run Goal 2 focused Bible-wide research using T398 as the phase-one synthesis. Build a scored, non-output-changing focused research queue across high-risk lanes and candidate passages, starting from T398-HDP prompts, T386 passage flags, and existing dossier queues. Produce owner decision packets for which focused packets should be strengthened next. Do not select targets, promote reviewed gold, implement chunks, add child spans, change routes/evaluators, create graph/retrieval/vector truth, import boundary material, change canon scope, create source/manuscript rows, or authorize theology authority. Do not select preferred readings/source traditions.
```

T397 remains the current next route for `Eph.1.3-Eph.1.14` harness prep only. T398 does not supersede T397.

## Validation

T398 is enforced by:

```text
scripts/validate_t398_bible_wide_phase_one_research_synthesis.py
tests/test_t398_bible_wide_phase_one_research_synthesis.py
```
