# Hebrews 7-10 Priesthood Argument Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `heb7_10_priesthood_argument`
- Decision: pending
- Parent/child candidate: yes
- Proposed parent unit for review: `Heb.7-Heb.10`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false

This packet does not authorize output-changing work.

## Review Target

`Heb.7-Heb.10` tests a sustained epistle argument with priesthood, covenant, sacrifice, warning,
and exhortation movements. It is review-packet-ready, but it is not implementation-ready.

## Current Chunk Behavior

Observed behavior is inherited from the T318 diagnostic audit. No fresh chunk regeneration was
performed for T352.

| Observed chunk touching target | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Heb.5.11-Heb.7.10` | 745 | `epistles` | `english_sentence`, `usfm_paragraph` | true |
| `Heb.7.11-Heb.8.12` | 758 | `epistles` | `english_sentence`, `usfm_paragraph` | true |
| `Heb.8.13-Heb.10.7` | 865 | `epistles` | `english_sentence`, `usfm_paragraph` | true |
| `Heb.10.8-Heb.11.4` | 713 | `epistles` | `english_sentence`, `usfm_paragraph` | true |

The target is split across current chunks and mixed with surrounding context. That observation is
diagnostic only and does not approve or condemn current behavior.

## Evidence To Preserve

- Paragraph and quotation markers are evidence only.
- Old Testament quotations and priesthood/covenant terminology must not become automatic graph
  edges or chunk boundaries.
- Warning and exhortation material must not be severed from theological grounds without review.
- Labels must not choose among covenant-theology, sacramental, perseverance, or typological systems.

## Review Risks

- Boundary choices could imply a covenant-system reading or sacrifice/fulfillment scope claim.
- Splitting warning/exhortation away from argument could distort retrieval context.
- Current behavior may blur argument units by mixing material before Hebrews 7 and after Hebrews 10.
- Hebrews-specific decisions could leak into Pauline epistles or legal/covenant lanes.

## Proposed Review Options

- Preserve current behavior and record only diagnostic concerns.
- Approve parent `Heb.7.1-Heb.10.39` with no child chunks.
- Approve reviewed child spans around priesthood, covenant, sacrifice, and exhortation movements
  only after exact owner decision.
- Defer implementation until route tests cover non-Hebrews epistles.

No option above is approved. No reviewed gold is promoted.

## Proposed Gold Needed Before Implementation

- Owner-reviewed parent span and any exact child spans.
- Explicit non-authorization of covenant-system, typology, or perseverance claims from boundaries.
- Non-target identity checks for Ephesians, Romans, Corinthians, Psalms, Revelation, Gospels, and
  legal/covenant controls.
- Same-baseline evaluation before output-changing work.

