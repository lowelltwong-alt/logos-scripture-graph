# T521 external blind-review batch plan

Status: candidate-only handoff aid. This schedule does not authorize chunk
changes, promotion, theology decisions, or independent-model claims.

The packet index remains the authority for the exact map and allowed inputs.
Before dispatch, regenerate and validate the packet index and scaffold queue;
record their current digests in the external receipt. Do not send sibling maps,
Sol role reports, boss rulings, or prior convergence results before the batch is
frozen.

## Batches

The batches are intentionally grouped by literary/language pressure so an
external reviewer can review a coherent family while still returning one row
for every assigned book and every challenged span.

| Batch | Books | Primary pressure |
|---|---|---|
| OT-PROPHECY | Isa, Jer | Hebrew oracle/prose/song/sign-act transitions; formula and wordplay risk |
| OT-POETRY | Job, Prov, Eccl, Song, Lam | speaker changes, collections, refrains, parallelism, voice shifts |
| NT-APOCALYPTIC | Rev | Koine vision cycles, epistolary framing, quotation/echo boundaries |
| NT-PAULINE | Rom, 1Cor, 2Cor, Gal, Eph, Phil, Col, 1Thess, 2Thess, 1Tim, 2Tim, Titus, Phlm | argument, citation, exhortation, discourse-particle transitions |
| NT-CATHOLIC | Heb, Jas, 1Pet, 2Pet, 1John, 2John, 3John, Jude | homily/epistle argument, citation, paraenesis, compressed Greek |
| CROSS-FORM-REMAINDER | all other books represented in the packet | calibration check across narrative, law, wisdom, poetry, prophecy, Gospel, and history |

The packet index and queue, rather than this table, determine exact row
membership. A batch may be split for reviewer capacity, but a split must retain
the same map digest, queue digest, and blind-input allowlist.

## Required batch receipt

Each external reviewer must return a machine-readable receipt conforming to
`config/agents/families/scripture-first-biblical-chunking/t521_external_review_receipt.schema.v1.json`.
The receipt must include:

- provider/model and execution identity;
- exact map, packet-index, queue, and prompt digests;
- explicit statement that sibling maps and Sol conclusions were not read first;
- every assigned book, including a clean-result row when no issue is found;
- literary/form challenges, Hebrew/Aramaic/Koine translation risks, and
  evidence-only internal cross-reference leads;
- red-team tests, counterevidence, uncertainty, source gaps, and unresolved
  dissent or appeals;
- `candidate_only: true`, `non_authorizing: true`, and
  `promotion_authorized: false`.

No batch receipt clears a hold by itself. The root may only update a candidate
artifact after receipt validation, preserving the original row, challenge, and
appeal lineage. Any unresolved reasoned disagreement remains a hold for human
or another independent reviewer.

## Dispatch commands

```text
python scripts/build_t521_scaffold_hold_queue.py
python scripts/build_t521_external_review_packet_index.py
python scripts/refresh_t521_packet_index_with_copy_prompt.py
python scripts/validate_t521_external_review_packet_index.py
```

The current packet index is the only permitted handoff bundle. The absence of a
valid independent receipt keeps the T521 convergence status at
`awaiting_external_provider_or_human_receipt`.
