# John 7:53-8:11 Textual Variant Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `john7_53_8_11_pericope_adulterae`
- Decision: pending
- Parent/child candidate: yes
- Proposed review unit: `John.7.53-John.8.11`

This packet does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk overlapping target | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `John.7.20-John.8.6` | 737 | `gospels` | `english_sentence`, `usfm_paragraph` | true |
| `John.8.7-John.8.39` | 713 | `gospels` | `english_sentence`, `usfm_paragraph` | true |

Current behavior splits the `John.7.53-John.8.11` variant zone across two chunks. The first chunk
starts before the variant zone and ends at `John.8.6`; the second starts at `John.8.7` and continues
well past the target to `John.8.39`.

The variant zone is therefore neither isolated nor preserved as one reviewed parent span in current
chunk output.

## Relevant Marker/Form Evidence

Confirmed local source evidence:

- Source file: `73-JHNeng-web.usfm`.
- Boundary claims in target span: 6.
- Marker counts in span: `p` = 6.
- Paragraph markers observed at:
  - `John.8.1`, source line 480.
  - `John.8.6`, source line 486.
  - `John.8.8`, source line 489.
  - `John.8.10`, source line 492.
  - `John.8.11`, source lines 494 and 495.
- Footnote observed inside the span:
  - `John.8.11`, source line 494: existing WEB note says NU includes `John.7.53-John.8.11` but
    brackets it to mark lower confidence in originality.
- The raw marker at `John.8.11` includes `\wj` words-of-Jesus markup.

Confirmed risk fields from the stress atlas:

- Text-critical risk: high.
- Punctuation risk: medium.
- Translation mismatch risk: high.
- Speaker boundary risk: high.

## Risks

Risks of preserving current behavior:

- A major textual-variant zone is split across chunks and mixed with surrounding John material.
- Dialogue and speaker turns inside the passage may be difficult to review when split at
  `John.8.6/8.7`.
- Variant status is present in footnote sidecar evidence but not expressed as chunk policy.

Risks of changing behavior:

- Isolating the passage or approving child dialogue chunks would make textual-critical and
  speaker-boundary decisions that have not been reviewed.
- A variant-aware policy may need source-tradition and translation-display rules before it can drive
  output.
- `\wj` evidence should not by itself authorize a chunk boundary or a theological decision.

## Possible Boundary Alternatives

Proposed for human review only:

- Preserve current chunk behavior and record variant/speaker risks for later.
- Approve `John.7.53-John.8.11` as a parent variant-zone span while deferring child dialogue chunks.
- Approve parent span plus child dialogue/paragraph chunks after textual-criticism and speaker
  review.
- Keep the current chunk boundaries but require future variant-aware diagnostics.

## Review Questions

- Should the full `John.7.53-John.8.11` span be preserved as a parent unit despite current output
  splitting it?
- Should paragraph markers at `John.8.6`, `John.8.8`, `John.8.10`, and `John.8.11` become child
  boundary evidence after review?
- What future policy should govern `\wj` spans inside major textual variants?
- What textual-criticism review is required before any gold entry can approve behavior?

## Proposed Gold Needed Before Implementation

- Textual-criticism review before reviewed gold.
- A decision on whether the parent unit is the full variant zone.
- Exact child boundaries, if any, with speaker and words-of-Jesus evidence explicitly scoped.
- Executable checks or manifest entries before any evaluator, chunker, orchestrator, or skill work.

