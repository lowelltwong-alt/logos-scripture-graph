# Psalms Gold Plan

Status: T310 Psalm gold includes executable settled cases plus the reviewed Psalm 78 parent/child
structural split. The reviewed/executable manifest is
`eval/chunking_gold/per_form/psalms_gold_manifest.json`.

Target form: literal Book of Psalms (`Ps`) routed through the candidate
`psalm-whole-then-stanza-v1` skill.

Baseline: post-T327 canonical-66 D / Claude pass2 output scores 93.6 under the unchanged T314
reviewed-structural-split evaluator policy. The pre-T327 wider-corpus score was 93.5, the T311
book/chapter evaluator score was 93.0, and the old 88.5 score is retained only as provenance.
Movement between pre/post T327 baselines is corpus-scope correction / baseline reset, not chunking
improvement.

## Executable Reviewed Cases

| Case | Expected behavior | Purpose |
| --- | --- | --- |
| `Ps.23.1-Ps.23.6` | One whole-psalm chunk. | Existing hard gate; must not regress. |
| `Ps.3` superscription source evidence | Real `\d` title source evidence exists and no standalone orphan title chunk is emitted. | Prevent orphan title chunks under the current witness/chunk model. |
| `Ps.119` | Parent literary unit `Ps.119.1-176` with exact 22 stanza/section child chunks, reported via `psalm119_section_chunks` and not penalized as fragmentation. | Strong precedent for parent whole-unit plus child-level structural chunks. |
| `Ps.78` | Parent literary unit `Ps.78.1-72` with reviewed child chunks `Ps.78.1-69`, `Ps.78.70-71`, and `Ps.78.72`. | Approved lighter parent/child structural split; preserve current output without metric-chasing a +0.5 merge. |
| `Ps.105.1-Ps.105.45` | One whole-psalm chunk. | Human-approved current behavior; token size is moderate and no child chunks are required. |
| `Ps.106.1-Ps.106.48` | One whole-psalm chunk. | Human-approved current behavior; `b` markers are internal formatting/stanza evidence, not automatic split authority. |
| Short Psalm holdouts: `Ps.1`, `Ps.8`, `Ps.100`, `Ps.117` | One chunk each unless future reviewed gold says otherwise. | Prevent over-fragmenting short Psalms. |
| Non-target controls: `Song`, `Lam` | Remain on monolith fallback / route-stable under the current orchestrator strategy. | Prove the Psalm skill does not rewrite adjacent canonical poetry books. |

## Reviewed Structural Split Cases

| Case | Parent literary unit | Child chunk boundaries | Status |
| --- | --- | --- | --- |
| Psalm 119 | `Ps.119.1-176` | 22 acrostic/stanza sections. | `reviewed_gold`; strong precedent for intentional parent/child sectioning. |
| Psalm 78 | `Ps.78.1-72` | `Ps.78.1-69`; `Ps.78.70-71`; `Ps.78.72`. | `approved_structural_split_under_parent_whole_psalm`; reviewed lighter case. |

Reviewed structural split is not the same as bad fragmentation. Psalm 78 remains a single literary
psalm at the parent level while retaining child-level structural chunks for retrieval.

## Characterization-Only Cases

No current Psalm case remains `pending_human_review` in this manifest. Future unresolved Psalm cases
should be recorded here until reviewed.

## Reviewed Whole-Psalm Cases With Deferred Child Questions

| Case | Reviewed parent unit | Current child chunks | Marker note |
| --- | --- | --- | --- |
| Psalm 105 | `Ps.105.1-45` | None; one whole-psalm chunk. | Current marker evidence does not require child chunks. |
| Psalm 106 | `Ps.106.1-48` | None; one whole-psalm chunk. | `b` markers are evidence, not automatic child-boundary authority. |

These are reviewed whole-psalm gold cases, not reviewed structural splits. Future child chunks for
either psalm would require a new human decision, exact child boundaries, and executable checks before
any output-changing work.

## Hard Gates

- 0 USFM leaks.
- 0 book crossings.
- 100% prose sentence integrity.
- Psalm 23 remains one whole-psalm chunk.
- Genesis 1 remains no mid-sentence.
- Non-target controls remain byte-identical.
- Non-66 material such as `PrMan` and `Ps151` must not be reintroduced as canonical controls.

## Forbidden Diffs

- Changing raw or canonical data.
- Routing non-`Ps` books through the Psalm skill.
- Treating `detect_form` output as routing authority before the increment explicitly allows it.
- Claiming score improvement from evaluator correction or aggregate score movement alone.
- Optimizing only the aggregate composite without target-form output evidence.
- Treating reviewed parent/child structural splits as bad fragmentation in gold docs or tests.

## Current Target Finding

T311 analysis identified the single D / Claude pass2 literal Psalm fragmentation target as `Ps.78`.
Human review has now approved the current `Ps.78` split as a parent whole-psalm unit with child
structural chunks. This records reviewed gold and does not authorize or require an output change.

## Scoring Caveat

The corrected composite still penalizes final `literal_psalms_fragmented` by 0.5 per unit. T314 keeps
`literal_psalms_fragmented_raw=1` for Ps.78, records one `reviewed_structural_splits` diagnostic, and
sets final `literal_psalms_fragmented=0` because the observed child boundaries exactly match reviewed
gold. This is evaluator-policy correction, not output improvement.
