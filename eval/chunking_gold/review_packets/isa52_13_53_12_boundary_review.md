# Isaiah 52:13-53:12 Boundary Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `isa52_13_53_12_servant_song`
- Decision: pending
- Parent/child candidate: yes
- Proposed parent unit for review: `Isa.52.13-Isa.53.12`

This packet does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk containing target | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Isa.51.20-Isa.54.9` | 1141 | `prophets` | `english_sentence`, `token_budget` | true |

Current behavior does not split at the Isaiah 52/53 chapter boundary. It also does not isolate
`Isa.52.13-Isa.53.12`; the target cross-chapter unit is embedded inside a larger `Isa.51.20-Isa.54.9`
chunk.

If chapter-based segmentation were observed here, it would be unsafe for this target because the
candidate literary unit crosses from Isaiah 52 into Isaiah 53.

## Relevant Marker/Form Evidence

Confirmed local source evidence:

- Source file: `24-ISAeng-web.usfm`.
- Boundary claims in target span: 62.
- Marker counts in span: `q2` = 34, `q1` = 25, `b` = 3.
- Observed blank-line/stanza markers:
  - `Isa.53.3`, source line 3292.
  - `Isa.53.6`, source line 3307.
  - `Isa.53.9`, source line 3324.
- No section headings were observed inside the span in current canonical sidecars.
- Footnotes observed inside the span:
  - `Isa.52.15`, source line 3272: alternate rendering note.
  - `Isa.53.11`, source line 3334: existing note says Dead Sea Scrolls and Septuagint include
    wording omitted by the Masoretic Text.

Confirmed risk fields from the stress atlas:

- Text-critical risk: medium.
- Punctuation risk: high.
- Translation mismatch risk: high.
- Speaker boundary risk: high.

## Risks

Risks of preserving current behavior:

- The target unit is not isolated and is merged with preceding and following Isaiah material.
- Retrieval for the servant-song candidate may include too much adjacent context.
- Speaker/stanza transitions inside the target span are not exposed as child boundaries.

Risks of changing behavior:

- Isolating the target span could overfit a disputed literary/exegetical unit without explicit
  human review.
- Child splits could encode speaker decisions that are not yet reviewed.
- Text-critical and translation-layout risks make this unsafe as an automatic rule.

## Possible Boundary Alternatives

Proposed for human review only:

- Preserve the current larger chunk and record only a context-packet concern.
- Approve parent `Isa.52.13-Isa.53.12` as a cross-chapter literary unit.
- Approve child stanza boundaries inside that parent, potentially using `b` markers only as evidence.
- Defer boundary approval until prophetic-poetry gold has a broader policy.

## Review Questions

- Should `Isa.52.13-Isa.53.12` become a reviewed parent literary unit?
- If yes, should current `b` markers inside Isaiah 53 influence child chunks?
- How should speaker-risk annotations be represented without making an exegetical decision?
- Should the existing `Isa.53.11` DSS/LXX/MT note block any output-changing work until textual
  review is complete?

## Proposed Gold Needed Before Implementation

- A human decision on whether the cross-chapter unit is an approved parent span.
- Exact child boundaries, if any, with speaker-risk notes clearly marked as review evidence rather
  than final interpretation.
- Text-critical review for the `Isa.53.11` note before any source-tradition-aware policy change.
- Executable checks or manifest entries before any evaluator, chunker, orchestrator, or skill work.

