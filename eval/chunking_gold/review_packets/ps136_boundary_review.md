# Psalm 136 Boundary Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `ps136_refrain_litany`
- Decision: pending
- Parent/child candidate: yes, pending review
- Proposed parent unit for review: `Ps.136.1-Ps.136.26`
- Approved child chunks: none

This packet does not authorize output-changing work.

## Current Evidence State

Psalm 136 is already present in the stress atlas as a refrain-driven litany. T318 observed current
behavior from a historical pre-T327 temporary chunker run:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Ps.136.1-Ps.136.26` | 346 | `psalms` | `chapter_boundary`, `whole_psalm` | true |

The observed behavior keeps Psalm 136 as one whole-psalm chunk. That observation is diagnostic only:
it is not reviewed gold, not approved expected output, and not a post-T327 chunk regeneration.

## Relevant Marker/Form Evidence

Observed marker evidence from the T318 audit:

- Boundary marker counts in the span: `q1` = 25, `q2` = 26.
- No Selah / `qs` refs were observed in the T318 audit.
- No blank-line / `b` refs were observed in the T318 audit.

Psalm 136's repeated refrain is a literary/form observation that needs human review before it can
become child-boundary authority.

## Review Questions

- Should Psalm 136 remain one whole-psalm chunk because it is only about 346 tokens?
- If child chunks are useful, should they follow creation, exodus, wilderness, land, rescue, and
  praise movements?
- Does the repeated refrain argue for preserving whole-psalm litany unity rather than child chunks?
- Should Psalm 136 serve as a refrain-aware control before any future stanza/refrain behavior
  change?

## Deferred Boundary Alternatives

Deferred for human review only:

- Preserve current one-chunk behavior as reviewed whole-psalm gold.
- Approve a parent `Ps.136.1-Ps.136.26` unit with exact refrain-aware child chunks.
- Keep Psalm 136 as characterization-only while choosing a longer Psalm case for implementation.

## Proposed Gold Needed Before Implementation

Future output-changing work requires:

- an explicit human decision;
- exact approved child spans, if any;
- rationale distinguishing repeated refrain form from automatic split authority;
- executable checks;
- non-target identity proof;
- preservation of existing reviewed Ps.78, Ps.105, Ps.106, and Ps.119 decisions.
