# John 3 Words-of-Jesus Speaker-Boundary Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `john3_wj_speaker_boundary`
- Decision: pending
- Parent/child candidate: yes
- Proposed parent unit candidate: `John.3.1-John.3.36`

This packet does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `John.1.40-John.3.2` | 792 | `gospels` | `english_sentence`, `usfm_paragraph` | true |
| `John.3.3-John.4.6` | 765 | `gospels` | `english_sentence`, `usfm_paragraph` | true |

Current behavior does not isolate John 3 as a reviewed discourse or speaker-boundary unit. It
overlaps John 3 with surrounding Gospel material and remains unchanged by this packet.

## Current `\wj` Evidence

Confirmed local source evidence:

- Raw inventory reports 4,580 `\wj` markers across the corpus.
- John 3 has `wj` nesting context in canonical word tokens.
- Current sidecars show 338 John 3 word tokens with `wj` nesting context across 17 verses.
- Boundary claims in the span are paragraph markers (`p` = 8); no line-leading boundary claim in
  this span carries raw `\wj` markup.
- Sample `wj` token evidence begins at `John.3.3`, source line 129.

`\wj is evidence, not authority`.

## Review Risk

John 3 is a speaker-boundary review case. This packet does not decide where Jesus stops speaking and
where narrator/commentary begins. `\wj` markup and punctuation are edition/translation evidence,
not authority for speaker attribution or chunk boundaries.

Speaker attribution requires human review before gold.

## Possible Boundary Alternatives

Proposed for human review only:

- Preserve current overlapping Gospel chunks.
- Approve a John 3 parent unit with no child chunks.
- Approve parent `John.3.1-John.3.36` with child chunks around dialogue, discourse, and narrator or
  commentary sections.
- Approve a narrower reviewed Jesus-speech unit only after explicit speaker-boundary review.

## Risks Of Preserving Current Behavior

- Current chunks cross the John 3 chapter boundary and may blur the Nicodemus dialogue, discourse,
  and following witness material.
- Retrieval may mix John 3 speaker-boundary evidence with adjacent John 1-2 or John 4 material.

## Risks Of Changing Behavior

- Splitting by `\wj` or punctuation could silently encode a disputed speaker attribution decision.
- Splitting by chapter could overstate chapter boundaries as discourse boundaries.
- Any child boundary would be agent inference until reviewed gold records exact spans.

## Proposed Gold Needed Before Implementation

- Human speaker-boundary review.
- Explicit parent unit, if any.
- Exact child boundaries, if any.
- A statement of whether `\wj` evidence is preserved diagnostically only or used in reviewed
  boundary rationale.
- Executable checks before evaluator, chunker, orchestrator, or skill work.

