# Mark 16:9-20 Textual Variant Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `mark16_9_20_longer_ending`
- Decision: pending
- Parent/child candidate: no
- Proposed review unit: `Mark.16.9-Mark.16.20`

This packet does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk containing target | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Mark.15.40-Mark.16.20` | 620 | `gospels` | `book_boundary` | true |

Current behavior embeds the `Mark.16.9-Mark.16.20` variant zone in a larger chunk that starts at
`Mark.15.40` and runs to the end of Mark. The variant zone is not isolated as a chunk or annotated
as variant-aware output by the current chunker.

## Relevant Marker/Form Evidence

Confirmed local source evidence:

- Source file: `71-MRKeng-web.usfm`.
- Boundary claims in target span: 3.
- Marker counts in span: `p` = 3.
- Paragraph markers observed at:
  - `Mark.16.11`, source line 987.
  - `Mark.16.13`, source line 990.
  - `Mark.16.18`, source line 996.
- Footnotes observed inside the span:
  - `Mark.16.9`, source line 984: existing WEB note discusses omission in a few manuscripts and
    the WEB translators' reliability judgment for verses 9-20.
  - `Mark.16.19`, source line 997: existing short textual note.

Confirmed risk fields from the stress atlas:

- Text-critical risk: high.
- Punctuation risk: medium.
- Translation mismatch risk: high.
- Speaker boundary risk: medium.

## Risks

Risks of preserving current behavior:

- Retrieval can treat a major textual-variant zone as ordinary continuation without surfacing
  variant status.
- The current chunk includes preceding passion/resurrection-context material and the longer ending
  together, which may be useful for context but unclear for variant-aware review.

Risks of changing behavior:

- Isolating or reclassifying the ending without textual-criticism review would make a policy
  decision the repo has not approved.
- Chunking should not encode a theological or textual-critical decision about originality,
  reliability, inclusion, or exclusion.
- External textual-critical data must not be imported into this packet; only existing repo evidence
  is cited.

## Possible Boundary Alternatives

Proposed for human review only:

- Preserve current larger chunk and add no output behavior.
- Create future variant-aware metadata while preserving chunk boundaries.
- Isolate `Mark.16.9-Mark.16.20` only after a reviewed textual-variant policy exists.
- Create a parent context packet that keeps `Mark.15.40-Mark.16.20` available while marking the
  variant zone.

## Review Questions

- Should major textual-variant zones be isolated as chunks, metadata overlays, or context packets?
- Should the existing WEB footnote be surfaced as variant evidence in chunk diagnostics later?
- What minimal textual-criticism review is required before any gold entry can approve behavior?

## Proposed Gold Needed Before Implementation

- Textual-criticism review before reviewed gold.
- A variant-aware chunking policy that distinguishes inclusion/annotation from boundary selection.
- Exact expected behavior, if any, for current chunk boundaries and sidecar metadata.
- Executable checks or manifest entries before any evaluator, chunker, orchestrator, or skill work.

