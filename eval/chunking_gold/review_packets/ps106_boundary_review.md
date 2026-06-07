# Psalm 106 Boundary Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `ps106_historical_confession`
- Decision: pending
- Parent/child candidate: yes
- Proposed parent unit: `Ps.106.1-Ps.106.48`

This packet does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Ps.106.1-Ps.106.48` | 721 | `psalms` | `chapter_boundary`, `whole_psalm` | true |

Current behavior preserves Psalm 106 as one whole-psalm chunk. No child chunks are emitted today.

## Relevant Marker/Form Evidence

Confirmed local source evidence:

- Source file: `20-PSAeng-web.usfm`.
- Boundary claims in span: 110.
- Marker counts in span: `q2` = 64, `q1` = 42, `b` = 4.
- Observed blank-line/stanza markers:
  - `Ps.106.5`, source line 5882.
  - `Ps.106.12`, source line 5906.
  - `Ps.106.46`, source line 6012.
  - `Ps.106.47`, source line 6018.
- No section headings or footnotes were observed inside the span in current canonical sidecars.

Inferred from the marker pattern: Psalm 106 has stronger internal stanza evidence than Psalm 105,
including `b` markers near confession/praise and closing petition material.

## Risks

Risks of preserving current behavior:

- A single 721-token whole-psalm chunk is within policy but may flatten repeated confession,
  rebellion, mercy, and petition cycles.
- The existing `b` markers suggest internal structure that current whole-psalm chunking does not
  expose as retrieval children.

Risks of changing behavior:

- Splitting only because `b` markers exist could overstate marker authority; USFM formatting is
  translation evidence, not ancient canonical boundary.
- Child boundaries could fragment the confession-cycle logic without a reviewed parent claim.
- Psalm 106 should not be marked as a reviewed structural split until a human approves exact spans.

## Possible Boundary Alternatives

Proposed for human review only:

- Preserve current one-chunk whole-psalm behavior.
- Approve parent `Ps.106.1-Ps.106.48` with child chunks around reviewed confession/rebellion/mercy
  cycles.
- Use current `b` markers as evidence candidates, not as automatic child-boundary targets.

## Review Questions

- Do the `b` markers at `Ps.106.5`, `Ps.106.12`, `Ps.106.46`, and `Ps.106.47` identify useful
  child boundaries?
- Should the review model follow Psalm 78's parent/child structural split pattern, or does the
  721-token length make one whole-psalm chunk preferable?
- What exact child spans, if any, should be approved?

## Proposed Gold Needed Before Implementation

- A human decision preserving whole-psalm behavior or approving exact child boundaries.
- If child chunks are approved, an explicit parent unit plus exact child spans and rationale.
- Executable checks or manifest entries before any evaluator, chunker, orchestrator, or skill work.

