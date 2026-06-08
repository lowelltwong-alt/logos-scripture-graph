# Psalm 106 Boundary Review Packet

## Status

- Status: `reviewed_gold`
- Stress atlas case ID: `ps106_historical_confession`
- Decision: approved_preserve_current_whole_psalm
- Parent/child candidate: no for current approved behavior
- Approved parent unit: `Ps.106.1-Ps.106.48`
- Approved child chunks: none; one whole-psalm chunk is reviewed gold

This reviewed decision does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Ps.106.1-Ps.106.48` | 721 | `psalms` | `chapter_boundary`, `whole_psalm` | true |

Current behavior preserves Psalm 106 as one whole-psalm chunk. No child chunks are emitted today.

## Human Decision

The owner approves the current whole-psalm chunk as reviewed gold:

- Approved boundary: `Ps.106.1-Ps.106.48`.
- Approved chunk count: 1.
- Current output preserves whole-psalm unity.
- Token size is acceptable at approximately 721 tokens.
- `b` markers may reflect internal formatting/stanza hints.
- `b` markers alone do not require child chunks without stronger human-reviewed literary evidence.
- No output change is needed.

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

T317 decision: those `b` markers are preserved as evidence, but they are not automatic split
authority for this reviewed case.

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

## Deferred Boundary Alternatives

Deferred for future review only:

- Approve parent `Ps.106.1-Ps.106.48` with child chunks around reviewed confession/rebellion/mercy
  cycles.
- Use current `b` markers as evidence candidates, not as automatic child-boundary targets.

## Deferred Review Questions

- Do the `b` markers at `Ps.106.5`, `Ps.106.12`, `Ps.106.46`, and `Ps.106.47` identify useful
  child boundaries?
- Should the review model follow Psalm 78's parent/child structural split pattern, or does the
  721-token length make one whole-psalm chunk preferable?
- What exact child spans, if any, should be approved?

## Proposed Gold Needed Before Implementation

- Current whole-psalm behavior is now reviewed gold and is locked in
  `eval/chunking_gold/per_form/psalms_gold_manifest.json`.
- Future child chunks would require a new human decision, exact child spans and rationale, and
  executable checks before any evaluator, chunker, orchestrator, or skill work.
