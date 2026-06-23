# T398 No-Context Audit Surface

## Scope

Task: `T398` Bible-wide phase-one research synthesis.

Primary artifact:

```text
.ai/control/t398_bible_wide_phase_one_research_synthesis.yaml
```

## Audit Claim

T398 records a deterministic phase-one synthesis from existing whole-corpus evidence. It proves corpus accounting and decision forecasting, not deep exegesis of every verse and not chunking/output authority.

## Evidence To Check

- `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`
- `.ai/control/bible_verse_passage_coverage_summary.yaml`
- `.ai/control/bible_verse_passage_readiness_matrix.yaml`
- `.ai/control/bible_verse_passage_gap_register.yaml`
- `.ai/control/bible_verse_passage_human_review_docket.yaml`
- `.ai/control/bible_wide_chunking_research_registry.yaml`
- `.ai/control/t398_bible_wide_phase_one_research_synthesis.yaml`
- `docs/roadmap/T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md`
- `scripts/validate_t398_bible_wide_phase_one_research_synthesis.py`

## Expected Findings

- Canonical scope remains `canonical_66`.
- The synthesis records `66` books and `31,103` canonical passages.
- The synthesis states `every_verse_deeply_researched: false`.
- The synthesis includes `T398-HDP-001` through `T398-HDP-009`.
- `T397` remains the current next route.
- The synthesis denies output, reviewed-gold, child-span, route/evaluator, graph/retrieval/vector, boundary-import, source-tradition, canon-scope, source-row, and theology authority.

## Validation

Run:

```bash
python scripts/validate_t398_bible_wide_phase_one_research_synthesis.py
python scripts/validate_all.py
python -m pytest -q
```

Before running full pytest, read `.ai/control/test_runtime_preflight.yaml` and use a timeout of at least `600000` ms.

