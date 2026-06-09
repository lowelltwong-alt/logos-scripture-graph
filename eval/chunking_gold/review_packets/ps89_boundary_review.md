# Psalm 89 Boundary Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `ps89_royal_lament`
- Decision: pending
- Parent/child candidate: yes, pending review
- Proposed parent unit for review: `Ps.89.1-Ps.89.52`
- Approved child chunks: none

This packet does not authorize output-changing work.

## Current Evidence State

Psalm 89 is already present in the stress atlas as a long royal/lament Psalm with covenant memory,
lament, petition, and liturgical marker evidence. T318 observed current behavior from a historical
pre-T327 temporary chunker run:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Ps.89.1-Ps.89.52` | 823 | `psalms` | `chapter_boundary`, `whole_psalm` | true |

The observed behavior keeps Psalm 89 as one whole-psalm chunk. That observation is diagnostic only:
it is not reviewed gold, not approved expected output, and not a post-T327 chunk regeneration.

## Relevant Marker/Form Evidence

Observed marker evidence from the T318 audit:

- Boundary marker counts in the span: `q1` = 53, `q2` = 55, `b` = 4.
- Selah / `qs` sample refs: `Ps.89.4`, `Ps.89.37`, `Ps.89.45`, `Ps.89.48`.
- Blank-line / `b` sample refs: `Ps.89.2`, `Ps.89.18`, `Ps.89.37`, `Ps.89.51`.

Marker evidence is evidence only. `\qs`, `\b`, and poetic line markers do not automatically approve
child chunk boundaries.

## Review Questions

- Should Psalm 89 remain one whole-psalm chunk despite the long royal/lament structure?
- If child chunks are useful, what exact spans preserve the parent whole-psalm unit while exposing
  praise, covenant/oracle memory, lament, petition, and doxology turns?
- Do the Selah / `\qs` markers identify review-worthy section candidates, or are they only
  liturgical/rubric evidence?
- Should Psalm 89 become the next reviewed parent/child structural-split candidate after Psalm 78?

## Deferred Boundary Alternatives

Deferred for human review only:

- Preserve current one-chunk behavior as reviewed whole-psalm gold.
- Approve a parent `Ps.89.1-Ps.89.52` unit with exact child structural chunks.
- Keep Psalm 89 as characterization-only while choosing a narrower Psalm case for implementation.

## Proposed Gold Needed Before Implementation

Future output-changing work requires:

- an explicit human decision;
- exact approved child spans, if any;
- rationale distinguishing literary structure from marker-only evidence;
- executable checks;
- non-target identity proof;
- preservation of existing reviewed Ps.78, Ps.105, Ps.106, and Ps.119 decisions.
