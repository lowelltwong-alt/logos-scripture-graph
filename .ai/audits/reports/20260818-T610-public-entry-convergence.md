# T610 A/B Convergence — Public Entry and PR 194

“A/B convergence” in this report means convergence of the two blind architecture
designs. It does not mean M7/M8 content convergence.

## Review Target

- Converger: Codex-root
- Date: 2026-08-18
- Base: `origin/main@b71b291aaabe20717b5fec8d2eb01209167aaec2`
- PR 194 head: `5c6c36106c49e2ac5795cb98956129cb4fab0620`
- M7 local head: `eaf31a940d3166b49c38ca26eb279392e0a3b25b`
- Task id: `T610`
- Frozen A/B brief SHA-256: `9ee36d08a68b3df0909f3565253ac60636a8d165a3a64d41ded9b821bc322dc4`

## Converged Decision

Both blind Sol/high designs independently reject merging PR 194 as a flattened unit.
The adopted design is:

```text
clean-main public entry PR
  -> reconciled, hash-bound M7 candidate publication
  -> Fable and its subagents complete M8 under the existing owner boundary
  -> first independent M7/M8 comparison and convergence
  -> small metadata convergence/index PR
  -> PR 194 closed as superseded only after durable replacement links
```

## Shared Findings

- The first page needs mission, repository-family routing, current versus planned
  capability, technical depth, ministry limits, maturity, and exact next gates.
- Candidate research and shipped capability must be visibly different.
- Release Bronze/Silver/Gold must not be confused with reviewed-gold chunk evidence.
- The current MCP claim is local stdio read-only. A remote server and write tools are
  future work, not current capability.
- M7 requires a reconciled freeze; M8 remains active and protected; PR 194 must preserve
  provenance without becoming the integration unit.

Owner sequencing clarification: no M7/M8 comparison or content convergence has started.
It begins only after M8 is complete.

## Differences Reconciled

- Lane A emphasized release sequencing and immutable candidate packages.
- Lane B emphasized the authority/data-flow graph and retaining failed-attempt provenance.
- The implementation adopts both: a compact entry router, a deeper public overview, two
  candidate publication units, and a metadata-only convergence index.

## Merge Gate

This design record does not itself authorize merging any research lane. The clean entry
PR may merge only after task-scope, repository, test, privacy, and independent-review
gates pass on the unchanged head. M7 and M8 each require their own hash-bound checks.

## Independence Claim

The lanes were blind to each other and received the same frozen neutral brief. They are
independent-context same-tier reviews. No claim of provider, model-family, or toolchain
diversity is made.
