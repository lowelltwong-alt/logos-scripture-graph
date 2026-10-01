# CAPTURE CONTRACT v2 — owner directives OW-7 and OW-8 (2026-09-07)

Supersedes v1, which is retained beside this file. v2 changes **what layer C is**; OW-7's separation, lineage,
retry and blindness rules are unchanged and restated here in full so this file stands alone.

Binding on **every** attempt from the first brief of Ezekiel: the Fable lanes and every subagent of every role —
writers, primaries, peers, boss, authors, order-execution, spot, cure, fix, sweep, sidecar, postcheck, transcript
auditors, final checkers — and every **nested** subagent.

## The three layers, and why they are never merged

| Layer | What it is | Who authored it | Trust |
|---|---|---|---|
| **A — runtime actions** | tool calls, arguments, results, file writes, the final message | the runtime | not self-authored, so it is the only layer that can catch an agent concealing something |
| **B — exposed thinking** | thinking summaries the runtime surfaced | the runtime | sporadic, summary-level, **never a full chain of thought** |
| **C — evidence-and-decision record** | an accountable work summary | **the agent itself** | self-reported, and **neither chain of thought nor independent proof** |

**A layer that does not exist is written `UNAVAILABLE` with its reason.** Never blank, never omitted, never filled
from another layer. Records **supplement** transcripts and never replace them: where layer A exists it is the
superior evidence and a checker weighs it accordingly.

## Layer C — what OW-8 actually ratified

An **accountable work summary**. The owner's words are the guard, and they cut both ways: it is *not chain of
thought*, so it is never presented to the owner as reasoning; and it is *not independent proof*, so it never
stands as evidence on its own. Its value is that its claims are checkable against artifacts.

Required fields:

```
{"attempt_id":"...",
 "sources":["<exact paths / artifacts read>"],
 "outcome":{"changed":[{"what":"...","why":"..."}]}        // OR
 "outcome":{"no_change":true,"why":"..."},                  // an explicit no-change outcome is a real outcome
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

**`unresolved_uncertainty` is the field most worth having and the easiest to leave empty.** An attempt that resolved
everything either had a trivial task or is not saying. An empty list is permitted and is itself a claim the checker
may test.

**Mechanical attempts may use a compact machine-receipt pointer** instead of prose. A mechanical attempt is a
deterministic tool run whose inputs, outputs and digests already speak for it:

```
{"attempt_id":"...","mechanical":true,
 "receipt":{"tool":"...","args":[...],"inputs":[{"path":"...","sha256":"..."}],
            "outputs":[{"path":"...","sha256":"..."}],"exit":0,"verdict":"..."},
 "unresolved_uncertainty":[],
 "limit":"machine receipt; the digests are the evidence"}
```

## Identity, lineage and retries (unchanged from OW-7)

Every attempt carries `book`, `task`, `agent_id`, `parent_agent_id`, `role`, `model_ordered`, `model_actual`,
`attempt_id`, `retry_of`.

- **`model_actual` is read, never inferred.** No runtime record means `UNAVAILABLE`. Inferring a model from what a
  lane usually runs put five wrong models into this campaign's receipts and is a recorded error.
- **A nested subagent's records belong to the child** and are never attributed to the parent.
- **A retry is its own record** carrying `retry_of`; the original is never overwritten, including when it failed or
  was stopped.

## The index and reviewer blindness (unchanged from OW-7)

`SP/campaign/capture_index.v1.jsonl` links the records and **never holds their content**.

**Collecting records does not authorize sharing them.** A lane still under a blindness constraint is never given the
index, another lane's records, or any conclusion drawn from them, before its own independent review has landed. The
index is a permitted read for the orchestrator and for post-review lanes only: final checkers, transcript auditors,
and the end-of-campaign re-check. The tool refuses on `--for-blind-lane`.

## What OW-8 bounds — the audit scope

OW-6 and OW-6c audit **what exists**: available deliverables, evidence records, receipts, observable actions and
retained transcripts. Two prohibitions, both cutting against this campaign's own instincts:

- **Do not fabricate missing historical records.** An absent record is reported as absent. It is never
  reconstructed into something that reads as though it were written at the time.
- **Do not restart a completed audit merely because transcripts are absent.** A finished audit stands on what it
  actually read.

**Missing logs are not a stop condition.** An evidence gap and a defect are different things. Demonstrated material
defects still require containment and repair; that licence is about missing logs, not about known defects.
