# Psalm 105 Boundary Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `ps105_historical_psalm`
- Decision: pending
- Parent/child candidate: yes
- Proposed parent unit: `Ps.105.1-Ps.105.45`

This packet does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Ps.105.1-Ps.105.45` | 601 | `psalms` | `chapter_boundary`, `whole_psalm` | true |

Current behavior preserves Psalm 105 as one whole-psalm chunk. No child chunks are emitted today.

## Relevant Marker/Form Evidence

Confirmed local source evidence:

- Source file: `20-PSAeng-web.usfm`.
- Boundary claims in span: 90.
- Marker counts in span: `q2` = 46, `q1` = 44.
- No `b` blank-line/stanza markers were observed inside the span in current boundary claims.
- No section headings or footnotes were observed inside the span in current canonical sidecars.

Inferred from the marker pattern: Psalm 105 is formatted as continuous poetry with line-level
evidence throughout, but the current WEB marker data does not expose strong blank-line stanza breaks
inside the psalm.

## Risks

Risks of preserving current behavior:

- A single 601-token whole-psalm chunk may be acceptable under policy, but it can hide internal
  historical episodes for retrieval.
- The historical-recital sequence may be less scannable without child sections.

Risks of changing behavior:

- Splitting only by episode or token preference could lose the parent whole-psalm unity.
- Without reviewed child targets, any split would be an agent inference rather than approved gold.
- No internal `b` markers were observed, so child boundaries would need human literary review rather
  than a simple marker rule.

## Possible Boundary Alternatives

Proposed for human review only:

- Preserve current one-chunk whole-psalm behavior.
- Approve a parent whole-psalm unit with child historical-episode chunks.
- Create characterization-only evidence first, then defer child-boundary approval until a reviewer
  marks episode boundaries.

## Review Questions

- Does Psalm 105 need child retrieval chunks despite being only about 601 tokens?
- If yes, should child boundaries follow historical episodes, poetic lines, or another reviewed
  structure?
- Should Psalm 105 become a lighter parent/child precedent like Psalm 78, or stay whole-psalm like
  shorter settled Psalms?

## Proposed Gold Needed Before Implementation

- A human decision preserving whole-psalm behavior or approving exact child boundaries.
- If child chunks are approved, an explicit parent unit plus exact child spans.
- Executable checks or manifest entries before any evaluator, chunker, orchestrator, or skill work.

