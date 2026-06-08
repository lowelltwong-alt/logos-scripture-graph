# Matthew 5-7 Words-of-Jesus Discourse Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `matt5_7_sermon_on_mount_wj_discourse`
- Decision: pending
- Parent/child candidate: yes
- Proposed parent unit candidate: `Matt.5.1-Matt.7.29`

This packet does not authorize output-changing work.

## Current Chunk Behavior

Confirmed from a temporary current chunker run on 2026-06-07:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Matt.3.15-Matt.5.10` | 709 | `gospels` | `english_sentence`, `usfm_paragraph` | true |
| `Matt.5.11-Matt.5.37` | 720 | `gospels` | `english_sentence`, `usfm_paragraph` | true |
| `Matt.5.38-Matt.6.23` | 723 | `gospels` | `english_sentence`, `usfm_paragraph` | true |
| `Matt.6.24-Matt.7.23` | 733 | `gospels` | `english_sentence`, `usfm_paragraph` | true |
| `Matt.7.24-Matt.8.31` | 765 | `gospels` | `english_sentence`, `usfm_paragraph` | true |

Current behavior does not encode a reviewed Sermon on the Mount parent unit or reviewed child
teaching units. It overlaps Matthew 5-7 with surrounding Gospel material and remains unchanged by
this packet.

## Current `\wj` Evidence

Confirmed local source evidence:

- Raw inventory reports 4,580 `\wj` markers across the corpus.
- Matthew 5-7 has `wj` nesting context in canonical word tokens.
- Current sidecars show 2,184 Matthew 5-7 word tokens with `wj` nesting context across 107 verses.
- Boundary claims in the span include `p` = 26, `q1` = 14, and `q2` = 11.
- Thirteen boundary-claim raw markers in the span include `\wj`, including Beatitude lines and the
  Lord's Prayer lines.
- No section headings were observed inside the span in current canonical sidecars.

`\wj is evidence, not authority`.

## Review Risk

Matthew 5-7 is a long Jesus discourse review case. The review must preserve the distinction between
whole discourse unity and internal teaching units. Headings, paragraphs, poetry lines, and `\wj`
spans are evidence, not automatic boundary authority.

Speaker attribution requires human review before gold.

## Possible Boundary Alternatives

Proposed for human review only:

- Preserve current overlapping Gospel chunks.
- Approve parent `Matt.5.1-Matt.7.29` as a whole discourse with no child chunks.
- Approve parent `Matt.5.1-Matt.7.29` with reviewed child teaching units.
- Record characterization-only evidence first and defer exact parent/child gold.

## Risks Of Preserving Current Behavior

- Current chunks cross both the discourse start and end, which may weaken retrieval for the whole
  Sermon on the Mount.
- Internal teaching units are visible only through paragraph and line evidence, not reviewed
  parent/child gold.

## Risks Of Changing Behavior

- Automatically splitting by headings, paragraphs, `q1`/`q2`, or `\wj` spans could overfit edition
  formatting rather than reviewed discourse structure.
- Over-merging all of Matthew 5-7 could create a large chunk that hides internal teaching units.
- Output changes without exact reviewed gold would encode an unreviewed discourse model.

## Proposed Gold Needed Before Implementation

- Human review of whole discourse scope.
- Human review of whether child teaching units are required.
- Exact child boundaries, if any.
- A statement of how `\wj`, paragraph, and line evidence should be weighed.
- Executable checks before evaluator, chunker, orchestrator, or skill work.

