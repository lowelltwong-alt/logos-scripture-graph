# CAPTURE CONTRACT v1 — owner directive OW-7 (2026-09-07)

Binding on **every** attempt in the M8_fable campaign from the first brief of the book after Lamentations: the Fable
lanes and every subagent of every role — writers, primaries, peers, boss, authors, order-execution, spot, cure, fix,
sweep, sidecar, postcheck, transcript auditors, final checkers — and every **nested** subagent.

## The three layers, and why they are never merged

An attempt's record has three layers. They come from three different places, they carry three different trust
levels, and **a record that presents them as one thing manufactures a chain of thought that does not exist.** That
misrepresentation is the reason this contract exists, so it is the one rule that has no exception.

| Layer | What it is | Who authored it | Trust |
|---|---|---|---|
| **A — runtime actions** | tool calls, their arguments, their results, file writes, the final message | the runtime, not the agent | can catch an agent concealing something, because the agent did not write it |
| **B — exposed thinking** | thinking summaries the runtime surfaced | the runtime, from the agent's reasoning | partial by construction: sporadic, summary-level, **never a full chain of thought** |
| **C — evidence note** | what the attempt verified, changed, and still doubts | **the agent itself** | self-reported; an agent that conceals a breach in its final message can conceal it here |

Layer C does not replace layer A. It exists because layer A is written for roughly one attempt in eight and layer B
almost never. Where layer A exists it is the superior evidence and the checker weighs it accordingly.

**A layer that does not exist is written as `UNAVAILABLE` with the reason.** Never omitted, never left blank, and
never filled in from another layer. "No transcript was written for this attempt" is a fact the record must carry.

## Identity, lineage and retries

Every attempt record carries: `book`, `task`, `agent_id` (the runtime id), `parent_agent_id`, `role`,
`model_ordered`, `model_actual`, `attempt_id` (unique across the campaign), and `retry_of`.

- **`model_actual` is read, never inferred.** Where no runtime record shows it, write `UNAVAILABLE`. Inferring a
  model from what a lane "usually" runs put five wrong models into this campaign's receipts and is a recorded error.
- **A nested subagent's records belong to the child.** Never attribute a child's work, or its layer C, to its parent.
  `parent_agent_id` records the relationship; it does not transfer authorship.
- **A retry is its own attempt record**, with its own `attempt_id`, carrying `retry_of` pointing at the original.
  The original is never overwritten and never deleted, including when it failed or was stopped.

## The index

`SP/campaign/capture_index.v1.jsonl` links the separate records. It carries identity, layer availability and paths.
**It never carries layer content**, so reading the index tells you what exists and where, not what an agent found.

## Reviewer blindness survives the index

Collecting records does not authorize showing them. **A lane still under a blindness constraint may not be given the
index, another lane's records, or any conclusion drawn from them, before its own independent review has landed.**

- Blind lanes include the dual-blind primaries with respect to each other, and any reviewer whose value is that it
  reached its finding without seeing another's.
- The index is a permitted read for the orchestrator and for **post-review** lanes: final checkers, transcript
  auditors, and the end-of-campaign re-check.
- A launch message for a blind lane never names the index, and never names another lane's records. The exact-path
  law already does this work; this clause states the reason so it is not weakened by someone who thinks the index is
  harmless because it holds no content. It holds *pointers*, and a pointer to a rival lane's conclusion is the thing
  blindness exists to prevent.

## What every brief must now order

One extra deliverable per attempt: the **evidence note**, layer C, written by the agent, in its own file beside its
main deliverable. Short. It is not a narrative and not a defence.

```
{"attempt_id":"...","role":"...","book":"...","task":"...",
 "verified_from_bytes":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "changed":[{"what":"...","why":"..."}],
 "still_doubted":[{"what":"...","why_it_matters":"..."}],
 "read_but_not_used":["..."],
 "reversals":[{"first_thought":"...","what_changed_it":"..."}],
 "self_reported_breaches":["..."],
 "layer_c_limit":"self-authored; not a transcript and not chain of thought"}
```

`still_doubted` and `reversals` are the fields worth the most and the easiest to leave empty. An attempt that
doubted nothing and reversed nothing either had a trivial task or is not telling you. The final checker reads them
against layer A wherever layer A exists, and a note that claims a verification the runtime record does not show is a
claim/act divergence of exactly the kind this campaign already catches.
