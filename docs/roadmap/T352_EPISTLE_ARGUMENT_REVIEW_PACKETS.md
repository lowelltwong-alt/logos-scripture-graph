# T352 Epistle Argument Review Packets

## Status

T352 is the first review-packet-ready lane selected after T351 Bible-wide triage. It creates
non-authorizing epistle argument review packets only.

This task does not implement chunks, promote reviewed gold, regenerate generated data, change
evaluator policy, create route behavior, create graph/vector/index outputs, or start T345.

## Selected Lane

Lane: `epistle_argument`

Reason:

- T351 classifies epistle argument as `review_packet_ready`.
- T344 owner guidance selected epistle argument boundaries as the next review lane after Revelation
  research/prep.
- The review-packet index already had observed diagnostic entries for all four targets with
  `recommended_next_action: create_review_packet`.

## Created Review Packets

| Packet | Case ID | Passage | Status |
| --- | --- | --- | --- |
| `eval/chunking_gold/review_packets/eph1_3_14_argument_review.md` | `eph1_3_14_greek_sentence` | `Eph.1.3-Eph.1.14` | `pending_human_review` |
| `eval/chunking_gold/review_packets/rom9_11_argument_review.md` | `rom9_11_argument` | `Rom.9-Rom.11` | `pending_human_review` |
| `eval/chunking_gold/review_packets/heb7_10_priesthood_argument_review.md` | `heb7_10_priesthood_argument` | `Heb.7-Heb.10` | `pending_human_review` |
| `eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md` | `1cor8_10_food_offered_to_idols` | `1Cor.8-1Cor.10` | `pending_human_review` |

## Non-Authorization Boundary

T352 does not authorize:

- output-changing chunking;
- reviewed-gold promotion;
- route or skill implementation;
- evaluator formula, leaderboard, or scorecard changes;
- generated chunk regeneration;
- graph edges, embeddings, vector indexes, or retrieval truth claims;
- source metadata, cross-reference, paragraphing, punctuation, or original-language authority;
- Revelation implementation or T345;
- broad epistle, Pauline, Hebrews, covenant, sacramental, election, Israel/church, perseverance, or
  ethical-system assumptions.

## Review Questions

- Which targets should become owner-reviewed parent units, if any?
- Are child chunks needed for any target, or is a parent-only review enough?
- What non-target identity checks are required before any epistle route implementation?
- Which labels are safe retrieval labels, and which labels risk theological overclaiming?
- Should long-sentence and quotation/catena evidence require separate original-language policy
  before implementation?

## RISK-GATE-001 Map

Required question:

```text
What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?
```

### Confirmed Risks

- Creating packets could be misread as approving parent spans or child boundaries.
- Argument labels could become doctrinal labels if later route code treats them as truth.
- Updating observed entries from `needs_review_packet` to `review_packet_pending` could be mistaken
  for reviewed gold.

### Plausible Risks

- Romans 9-11 boundaries could imply election or Israel/church conclusions.
- Hebrews 7-10 boundaries could imply covenant, sacrifice, typology, or perseverance claims.
- 1 Corinthians 8-10 boundaries could imply sacramental, ecclesial, or ethical-system claims.
- Ephesians 1:3-14 labels could imply Trinitarian or election-system conclusions.

### Tests Or Guards Needed

- A T352 validator must assert all four packet files exist, remain pending, and keep implementation
  and output flags false.
- Review-packet indexes and observed behavior surfaces must list these cases as pending review, not
  reviewed gold.
- HARN-012 must keep Revelation implementation blocked while epistle packet work proceeds.

## Next Step

Human review may select one exact epistle target for owner decision later. Do not implement an
epistle route, promote reviewed gold, or start output-changing chunking until a later task records
exact reviewed evidence and owner authorization.

