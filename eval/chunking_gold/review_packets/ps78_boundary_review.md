# Psalm 78 Boundary Review Packet

## Status

- Status: `approved_structural_split_under_parent_whole_psalm`
- Purpose: record the human decision for Psalm 78 after review.
- Decision: approved preserve-current-structural-split.
- Parent literary unit: `Ps.78.1-72`.
- Child chunk boundaries:
  - `Ps.78.1-69`
  - `Ps.78.70-71`
  - `Ps.78.72`

This records a gold/methodology decision only. It is not a chunking improvement claim, does not
change chunk output, and does not change the evaluator formula.

## Confirmed

- Human decision: preserve the current Psalm 78 split under a parent whole-psalm literary unit.
- Human rationale:
  - Psalm 78 is one literary psalm.
  - The current internal split is structurally plausible.
  - `Ps.78.70-72` functions as a David/shepherd coda.
  - Current split has marker/token evidence.
  - Merging would produce only +0.5 composite upside.
  - Merging only to eliminate `literal_psalms_fragmented=1` would be metric-chasing.
  - The correct model is parent whole-psalm unity plus child-level structural chunks.
- Current D / Claude pass2 output has three Psalm 78 child chunks:
  - `Ps.78.1-69`, 1109 tokens.
  - `Ps.78.70-71`, 35 tokens.
  - `Ps.78.72`, 21 tokens.
- Merged Psalm 78 token count would be 1165.
- Chunking policy values:
  - soft max: 1100 tokens.
  - hard max: 1600 tokens.
- Merging would remove the current `literal_psalms_fragmented=1` penalty for a direct composite
  upside of +0.5, but that is not sufficient target-form evidence for an output change.
- Regenerated current D/pass2 chunks in ignored output:
  - `build/post-3b-planning-pack/chunks.jsonl`
  - SHA-256: `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`
- The regenerated chunks match the committed D/pass2 chunk-output hash when generated with footnote
  and editorial-cross-reference sidecars.

## Evidence

Generated chunk evidence:

| Current child chunk | Tokens | Boundary basis |
|---|---:|---|
| `Ps.78.1` to `Ps.78.69` | 1109 | `poetic_stanza`, `token_budget`, `whole_psalm_split` |
| `Ps.78.70` to `Ps.78.71` | 35 | `poetic_stanza`, `whole_psalm_split` |
| `Ps.78.72` to `Ps.78.72` | 21 | `poetic_stanza`, `whole_psalm_split` |

Source marker evidence from `data/processed/bible/eng-web/usfm/usfm_events.jsonl`:

| OSIS ref | Source line | Marker | Note |
|---|---:|---|---|
| `Ps.78.1` | 4091 | `q2` | Poetry line evidence near the Psalm opening. |
| `Ps.78.1` | 4092 | `q1` | Poetry line evidence near the Psalm opening. |
| `Ps.78.70` | 4312 | `q2` | Poetry line evidence in the David-shepherd ending. |
| `Ps.78.70` | 4313 | `q1` | Poetry line evidence in the David-shepherd ending. |
| `Ps.78.71` | 4315 | `q2` | Poetry line evidence in the David-shepherd ending. |
| `Ps.78.71` | 4316 | `q2` | Poetry line evidence in the David-shepherd ending. |
| `Ps.78.71` | 4317 | `q1` | Poetry line evidence immediately before the final verse. |
| `Ps.78.72` | 4319 | `q2` | Poetry line evidence in the final verse. |
| `Ps.78.72` | 4320 | `b` | Blank-line/stanza marker at the end of Psalm 78. |

## Inferred

- The current split is not a simple hard-gate bug. It reflects both token-budget pressure and
  poetic-stanza / whole-psalm split basis.
- A full merge is legal under the hard max but exceeds the soft max by 65 tokens.
- The parent/child model preserves literary unity without erasing a plausible coda boundary.

## Reviewed Outcome

The approved model is:

```text
Parent literary unit:
  Ps.78.1-72

Reviewed child structural chunks:
  Ps.78.1-69
  Ps.78.70-71
  Ps.78.72
```

This reviewed structural split is not the same as bad fragmentation. It remains possible that the
current evaluator will count `literal_psalms_fragmented=1` until a separate evaluator-policy PR
distinguishes reviewed long-Psalm structural splits from unreviewed fragmentation.

## Future Evaluator-Policy Question

Should reviewed parent/child structural splits, such as Psalm 119 and now Psalm 78, be excluded from
the bad-fragmentation signal or reported separately?

That is a separate evaluator-policy task. This packet does not change the evaluator.

## Unknown

- Whether future Hebrew/source-language boundary evidence would strengthen or refine the current
  child boundaries.
- Whether evaluator policy should distinguish invalid Psalm fragmentation from reviewed long-Psalm
  structural splits.
