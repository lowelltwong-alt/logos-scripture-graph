# B01 typed evidence contract (revision boundary)

This contract is deliberately separate from the selected revision-7 B00 receipt. It records how a future B01 run must be replayable without silently turning candidate analysis into an authorized chunk map.

Every controller assignment/result, role report, synthesis, red-team report, challenge, appeal, and boss authorization is a typed artifact. Each artifact binds `book`, `run_id`, `stage_attempt_id`, execution/assignment/agent identity, exact input-manifest digests, and controller-observed event IDs. Agent self-attested clocks are not evidence of execution.

Role input closure is exact, not a subset: the original-language scout, literary scout, canonical/premortem scout, and bounded ancient-context scout each receive only their declared manifest IDs. The packet hash covers the immutable input manifest, all controller receipts, every role report, synthesis lineage, red-team report, and append-only challenge/appeal ledgers.

Red-team findings cannot be erased by synthesis. A reasoned disagreement remains a challenge; if the boss rejects it, an appeal records the claim, evidence, context, and requested human/external review. Any unresolved appeal blocks promotion, but does not erase the candidate evidence or prevent a separately governed next-book run.

The B01 verdict is receipt-only (`GO_B01_RECEIPT_ONLY` or `NO_GO`). It never authorizes a final boundary, chunk map, or theological conclusion. B02 remains disabled until a separately versioned migration passes adversarial tests for hash binding, identity separation, chronology, source closure, payload smuggling, and appeal preservation.

Replay sequence: freeze inputs under lock → issue controller assignments → record controller results → validate role reports → synthesize with lineage → freeze packet → run independent red-team → boss reviews the frozen packet → write receipt and ledgers. Any stale digest, duplicate physical path, missing role input, shared identity, or post-freeze mutation fails closed.
