# Psalm 78 Boundary Review Packet

## Status

- Status: `pending_human_review`
- Purpose: prepare the human decision on whether Psalm 78 should remain split or become one
  whole-psalm chunk.
- Decision: pending

This packet is evidence for review only. It does not encode a merge or preserve decision.

## Confirmed

- Current D / Claude pass2 output has three Psalm 78 chunks:
  - `Ps.78.1-69`, 1109 tokens.
  - `Ps.78.70-71`, 35 tokens.
  - `Ps.78.72`, 21 tokens.
- Merged Psalm 78 token count would be 1165.
- Chunking policy values:
  - soft max: 1100 tokens.
  - hard max: 1600 tokens.
- Merging would remove the current `literal_psalms_fragmented=1` penalty for a direct composite
  upside of +0.5.
- Regenerated current D/pass2 chunks in ignored output:
  - `build/post-3b-planning-pack/chunks.jsonl`
  - SHA-256: `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`
- The regenerated chunks match the committed D/pass2 chunk-output hash when generated with footnote
  and editorial-cross-reference sidecars.

## Evidence

Generated chunk evidence:

| Current chunk | Tokens | Boundary basis |
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
- The last two small chunks may represent a real David-shepherd coda boundary, but that is a review
  question, not an agent decision.

## Alternatives

1. Preserve current split.
   - Keeps the current stanza-sensitive long-Psalm output.
   - Leaves `literal_psalms_fragmented=1`.
2. Merge entire Psalm 78.
   - Treats Psalm 78 as one whole-psalm unit.
   - Removes the +0.5 fragmentation penalty.
   - Exceeds the configured soft max while staying under hard max.
3. Adjust evaluator treatment for structurally valid long-Psalm splits.
   - Separate evaluator PR only.
   - Requires evidence that the current split is structurally valid and should not be counted as
     literal Psalm fragmentation.

## Risks Of Merging

- Metric-chasing a weak +0.5 lever.
- Overriding possible real stanza / David-shepherd coda boundary evidence.
- Exceeding the 1100-token soft max.
- Encoding an output-changing Psalm policy before human review.

## Risks Of Preserving

- Keeps `literal_psalms_fragmented=1`.
- May split a whole-psalm unit if human review decides whole Psalm integrity is the higher priority.
- Leaves Psalm 78 as a visible unresolved exception in the Psalm gold lane.

## Proposed Review Question

Should Psalm 78 be treated as:

- one whole-psalm retrieval chunk despite soft-max excess, or
- a structurally valid long-Psalm split that should remain split and perhaps be handled by evaluator
  policy separately?

## Unknown

- Whether the `Ps.78.70-72` David-shepherd ending should be preserved as a distinct retrieval unit.
- Whether future Hebrew/source-language boundary evidence would strengthen or weaken the current
  split.
- Whether evaluator policy should distinguish invalid Psalm fragmentation from reviewed long-Psalm
  structural splits.
