# Psalms Gold Plan

Status: T310 3b-gold executable settled cases plus Ps.78 characterization. The reviewed/executable
manifest is `eval/chunking_gold/per_form/psalms_gold_manifest.json`.

Target form: literal Book of Psalms (`Ps`) routed through the candidate
`psalm-whole-then-stanza-v1` skill.

Baseline: unchanged D / Claude pass2 output scores 93.0 under the corrected T311 evaluator. The
old 88.5 score is retained only as old-evaluator provenance.

## Executable Reviewed Cases

| Case | Expected behavior | Purpose |
| --- | --- | --- |
| `Ps.23.1-Ps.23.6` | One whole-psalm chunk. | Existing hard gate; must not regress. |
| `Ps.3` superscription source evidence | Real `\d` title source evidence exists and no standalone orphan title chunk is emitted. | Prevent orphan title chunks under the current witness/chunk model. |
| `Ps.119` | Exact 22 stanza/section chunks, reported via `psalm119_section_chunks` and not penalized as fragmentation. | Preserve intentional structure. |
| Short Psalm holdouts: `Ps.1`, `Ps.8`, `Ps.100`, `Ps.117` | One chunk each unless future reviewed gold says otherwise. | Prevent over-fragmenting short Psalms. |
| Non-target controls: `Song`, `Lam`, `PrMan`, `Ps151` | Remain on monolith fallback / route-stable under the current orchestrator strategy. | Prove the Psalm skill does not rewrite adjacent poetry books. |

## Characterization-Only Cases

| Case | Observed behavior | Status |
| --- | --- | --- |
| Current literal fragmentation target: `Ps.78` | `Ps.78.1-Ps.78.69` (1109 tokens), `Ps.78.70-Ps.78.71` (35 tokens), `Ps.78.72-Ps.78.72` (21 tokens); merged Psalm would be 1165 tokens; `\b` marker at `Ps.78.72`. | `pending_human_review`; merge-vs-preserve-`\b` boundary is unresolved and human-gated. |

## Hard Gates

- 0 USFM leaks.
- 0 book crossings.
- 100% prose sentence integrity.
- Psalm 23 remains one whole-psalm chunk.
- Genesis 1 remains no mid-sentence.
- Non-target controls remain byte-identical.

## Forbidden Diffs

- Changing raw or canonical data.
- Routing non-`Ps` books through the Psalm skill.
- Treating `detect_form` output as routing authority before the increment explicitly allows it.
- Claiming score improvement from evaluator correction or aggregate score movement alone.
- Optimizing only the aggregate composite without target-form output evidence.

## Current Target Finding

T311 analysis identified the single D / Claude pass2 literal Psalm fragmentation target as `Ps.78`.
T310 3b-gold captured the current `Ps.78` split as characterization-only evidence. It is not a
promoted expected boundary and does not authorize an output change.

## Scoring Caveat

The corrected composite penalizes `literal_psalms_fragmented` by 0.5 per unit. Fixing the current
single Psalm fragmentation target can move at most 0.5 composite points unless it also improves
other formula terms. Current planning evidence says the larger remaining lever is size fitness
around `tok_p50`; do not overfit 3b to a weak metric without gold evidence.
