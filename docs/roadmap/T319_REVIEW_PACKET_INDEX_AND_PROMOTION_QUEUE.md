# T319 Review Packet Index And Promotion Queue

Status: complete as diagnostic/control infrastructure. No chunking implementation authorized.

## Purpose

T319 creates one control surface for reviewed Psalm gold, review packets, observed stress-audit
cases, policy-required cases, and the next review/promotion queue.

This is not reviewed-gold promotion, not evaluator policy, and not a chunking improvement claim.

## Confirmed

- Current official baseline remains D / Claude pass2 = 93.5 under T314 reviewed-structural-split
  evaluator policy.
- That score is evaluator-policy correction for unchanged output, not chunking improvement.
- T319 does not change chunk output.
- T319 does not change evaluator formula, leaderboard logic, raw/canonical data,
  chunker/orchestrator behavior, runtime skill code, or skill promotion.
- T319 does not mark any pending packet as approved.
- T319 does not add new reviewed gold.

## Deliverables

- `eval/chunking_gold/review_packets/review_packet_index.json`
- `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md`
- `tests/test_review_packet_index.py`

## Index Summary

- total entries: 60;
- reviewed gold entries: 13;
- pending human review: 11;
- needs review packet: 25;
- variant policy required: 2;
- speaker review required: 5;
- source/tradition review required: 3;
- manual investigation required: 1.

The index covers:

- 8 existing review packet files;
- 8 Psalm manifest reviewed cases;
- all 44 observed stress behavior cases.

## Promotion Queue

The promotion queue is a review queue, not an implementation backlog. Queue entries keep
`implementation_allowed: false` and `output_change_authorized: false`.

High-priority gates include:

- manual investigation for `jeremiah_mt_lxx_divergence`;
- variant policy before variant-zone gold;
- speaker-boundary review before words-of-Jesus gold;
- source/tradition review before source-tradition gold;
- review-packet creation before any output-changing work for observed hard cases.

## Governance Boundary

- Pending review packets remain pending.
- Observed audit cases remain diagnostic evidence.
- Current containment is not automatically approved preservation.
- Current splitting is not automatically bad fragmentation.
- Textual-variant cases are not reviewed gold unless explicitly reviewed.
- Words-of-Jesus and Selah marker evidence is not authority.
- No output-changing work is authorized.

## Proposed Next Use

Use T319 to select the next human-review or planning lane:

1. review the highest-risk pending textual-variant and WJ packets;
2. create review packets for selected `needs_review_packet` cases;
3. run T320/T321/T322 planning without changing chunk output.

## Unknown

- Whether future review-packet indexing should be generated automatically from packet front matter.
- Whether promotion-queue priority should become a reviewed policy field.
- Whether future packet decisions should update this index manually or through a validator command.
