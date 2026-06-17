# 1 Corinthians 8-10 Food Offered To Idols Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `1cor8_10_food_offered_to_idols`
- Decision: pending
- Parent/child candidate: yes
- Proposed parent unit for review: `1Cor.8-1Cor.10`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false

This packet does not authorize output-changing work.

## Review Target

`1Cor.8-1Cor.10` tests an epistle argument where knowledge, love, conscience, apostolic example,
Israel examples, idolatry, and table-fellowship ethics interact. The goal is to prepare review
without deciding a sacramental, ethical, or ecclesial framework through boundaries.

## Current Chunk Behavior

Observed behavior is inherited from the T318 diagnostic audit. No fresh chunk regeneration was
performed for T352.

| Observed chunk touching target | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `1Cor.7.25-1Cor.9.2` | 788 | `epistles` | `english_sentence`, `usfm_paragraph` | true |
| `1Cor.9.3-1Cor.10.5` | 703 | `epistles` | `english_sentence`, `usfm_paragraph` | true |
| `1Cor.10.6-1Cor.11.10` | 783 | `epistles` | `english_sentence`, `usfm_paragraph` | true |

The target is split across current chunks and mixed with surrounding context. That observation is
diagnostic only and does not authorize a route change.

## Evidence To Preserve

- Paragraph markers are review evidence only.
- Israel-example and quotation/allusion material must remain evidence, not automatic graph edges.
- Ethical labels must remain text-local and must not become a hidden theological or ecclesial
  position.
- Any future boundary around table language requires review before it can affect chunking.

## Review Risks

- Separating chapters 8, 9, and 10 can sever ethical argument from apostolic example and Israel
  warnings.
- Preserving current behavior may mix adjacent marriage/singleness or worship/head-covering
  material with the target.
- Boundary labels could overstate a sacramental or ecclesial interpretation.
- A Corinthians-specific route could leak into Romans, Hebrews, or Gospel discourse.

## Proposed Review Options

- Preserve current behavior and record only diagnostic concerns.
- Approve parent `1Cor.8.1-1Cor.10.33` with no child chunks.
- Approve reviewed child spans around knowledge/conscience, apostolic example, Israel warning, and
  table/idolatry material only after owner decision.
- Defer implementation until multiple epistle packets have reviewed evidence.

No option above is approved. No reviewed gold is promoted.

## Proposed Gold Needed Before Implementation

- Owner-reviewed parent span and any exact child spans.
- Explicit non-authorization of sacramental, ecclesial, or ethical-system claims from boundaries.
- Non-target identity checks for Ephesians, Romans, Hebrews, Psalms, Revelation, Gospels, and
  narrative controls.
- Same-baseline evaluation before output-changing work.

