# Psalms Gold Plan

Status: planning scaffold for T310 3b; not promoted gold.

Target form: literal Book of Psalms (`Ps`) routed through the candidate
`psalm-whole-then-stanza-v1` skill.

Baseline: unchanged D / Claude pass2 output scores 93.0 under the corrected T311 evaluator. The
old 88.5 score is retained only as old-evaluator provenance.

## Minimum Planned Cases

| Case | Expected behavior | Purpose |
| --- | --- | --- |
| `Ps.23.1-Ps.23.6` | One whole-psalm chunk. | Existing hard gate; must not regress. |
| Psalm superscriptions with `\d` title material | Superscription/title remains attached to its Psalm. | Prevent orphan title chunks. |
| `Ps.119` | Exact 22 stanza/section chunks, reported via `psalm119_section_chunks` and not penalized as fragmentation. | Preserve intentional structure. |
| Short Psalm holdouts: `Ps.1`, `Ps.8`, `Ps.23`, `Ps.100`, `Ps.117` | One chunk each unless future reviewed gold says otherwise. | Prevent over-fragmenting short Psalms. |
| Current literal fragmentation target: `Ps.78` | Investigate current split and propose reviewed expected boundary behavior before changing output. | The only current `literal_psalms_fragmented=1` D target. |
| Non-target controls: `Song`, `Lam`, `PrMan`, `Ps151` | Remain on monolith fallback and byte-identical to the baseline output. | Prove the Psalm skill does not rewrite adjacent poetry books. |

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
The clean checkout does not commit the generated D chunk output, so T310 3b must first regenerate or
capture the current `Ps.78` split and review the intended boundary before implementing an output
change.

## Scoring Caveat

The corrected composite penalizes `literal_psalms_fragmented` by 0.5 per unit. Fixing the current
single Psalm fragmentation target can move at most 0.5 composite points unless it also improves
other formula terms. Current planning evidence says the larger remaining lever is size fitness
around `tok_p50`; do not overfit 3b to a weak metric without gold evidence.
