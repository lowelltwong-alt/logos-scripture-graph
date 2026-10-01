# CAPTURE CONTRACT v3 — owner directives OW-7, OW-8 and OW-10 (2026-09-08)

Supersedes v2, which is retained beside it (and v1 beside that). v3 changes **identity**: it separates the stable
logical job from each physical execution, so that OW-7 and E-14 stop contradicting each other. Everything v2 said
about the three layers, blindness, and the audit scope is unchanged and restated here so this file stands alone.

Binding on **every** attempt from the first brief of Ezekiel: the Fable lanes and every subagent of every role —
writers, primaries, peers, boss, authors, order-execution, spot, cure, fix, sweep, sidecar, postcheck, transcript
auditors, final checkers — and every **nested** subagent.

## What v3 changes: two identifiers, because there are two things

OW-7 requires that "a retry is its own attempt record" and that an original is "never overwritten". E-14 requires
that when a deliverable is ABSENT the job is re-launched as a **fresh agent under the same attempt id**, appending
to the same deliverable. Read as one rule about one identifier, those contradict. They are two rules about two
different things, and v3 names both:

| | what it identifies | who keys off it | may it change? |
|---|---|---|---|
| **`attempt_id`** | the **stable logical job** | the E-14 resume ladder, the deliverable path, every historical receipt | **never** |
| **`execution_id`** | **one physical run** of that job, `<attempt_id>#e<N>` | OW-7's per-attempt capture, the index, layer attribution | new id per launch |

- **`previous_execution_id`** links run *N* to run *N−1* of the same job. First run: `null`.
- **`retry_of`** is a **different relation and is unchanged**: it points at another **job** this one corrects.
  Re-running a job is `previous_execution_id`; correcting a different job is `retry_of`. They are never conflated.
- **Historical ids are never renamed.** `execution_id` is additive; every historical `attempt_id` stays verbatim.
  Ordinals are derived deterministically from receipt order, so a rebuild is stable and no completed work is
  duplicated or re-run.

**Why this was not merely a wording problem.** Under one identifier, `_capture_index.py` kept the first receipt per
`attempt_id` and silently dropped the rest. The four Lamentations transcript auditors each ran twice — a wave-1
execution the orchestrator stopped before any deliverable was written, then a wave-2 execution that did the whole
audit. The index kept the **stopped** runs and dropped the ones that **did the work**. The receipts had both all
along; the loss was in the index built from them, which is exactly where a reviewer would look. Rebuilt under v3:
131 rows → 135, four executions recovered, `--check` GREEN.

## The three layers, and why they are never merged

| Layer | What it is | Who authored it | Trust |
|---|---|---|---|
| **A — runtime actions** | tool calls, arguments, results, file writes, the final message | the runtime | not self-authored, so it is the only layer that can catch an agent concealing something |
| **B — exposed thinking** | thinking summaries the runtime surfaced | the runtime | sporadic, summary-level, **never a full chain of thought** |
| **C — evidence-and-decision record** | an accountable work summary | **the agent itself** | self-reported, and **neither chain of thought nor independent proof** |

**Layers attach to the EXECUTION, not to the job.** Run 1 and run 2 of one job had different agents doing different
things; merging their layers would manufacture a chain of thought no agent ever had.

**A layer that does not exist is written `UNAVAILABLE` with its reason.** Never blank, never omitted, never filled
from another layer — and never borrowed from a sibling execution. Where a manifest maps a transcript to a *job*
and cannot say which *run* produced it, layer A is UNAVAILABLE **with the ambiguity named**; it is not handed to
whichever run happened to be first. Records **supplement** transcripts and never replace them.

## Layer C — what OW-8 ratified

An **accountable work summary**. The owner's words are the guard and they cut both ways: it is *not chain of
thought*, so it is never presented to the owner as reasoning; and it is *not independent proof*, so it never stands
as evidence on its own. Its value is that its claims are checkable against artifacts.

```
{"attempt_id":"...", "execution_id":"...",
 "sources":["<exact paths / artifacts read>"],
 "outcome":{"changed":[{"what":"...","why":"..."}]}        // OR
 "outcome":{"no_change":true,"why":"..."},                  // an explicit no-change outcome is a real outcome
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

Evidence notes are written to `SP/<Book>/evidence_notes/<execution_id>.json`. **`unresolved_uncertainty` is the
field most worth having and the easiest to leave empty.** An attempt that resolved everything either had a trivial
task or is not saying.

**Mechanical attempts may use a compact machine-receipt pointer** instead of prose — a deterministic tool run whose
inputs, outputs and digests already speak for it:

```
{"attempt_id":"...","execution_id":"...","mechanical":true,
 "receipt":{"tool":"...","args":[...],"inputs":[{"path":"...","sha256":"..."}],
            "outputs":[{"path":"...","sha256":"..."}],"exit":0,"verdict":"..."},
 "unresolved_uncertainty":[],
 "limit":"machine receipt; the digests are the evidence"}
```

## Identity and lineage

Every execution carries `book`, `task`, `agent_id`, `parent_agent_id`, `role`, `model_ordered`, `model_actual`,
`attempt_id`, `execution_id`, `execution_of`, `execution_ordinal`, `previous_execution_id`, `retry_of`.

- **`model_actual` is read, never inferred.** No runtime record means `UNAVAILABLE`. Inferring a model from what a
  lane usually runs put five wrong models into this campaign's receipts and is a recorded error.
- **A nested subagent's records belong to the child** and are never attributed to the parent.
- **An execution's record is never overwritten**, including when it failed or was stopped. A stopped run is a real
  run with a real record; it is not erased by the run that replaced it.

## A cure is not cured because its author says so (OW-10)

**Before a repair is accepted as cured, verification results must be bound to the exact resulting artifact, and a
distinct checker must have reviewed it. A self-reported "passed" is not sufficient.** Enforced by
`SP/campaign/_cure_verification.py` (selftest: 8 vectors, GREEN).

Three digests must agree — what was verified, what the claim pins, and what is on disk right now:

```
{"cure_id":"...", "author_attempt_id":"...", "author_execution_id":"...",
 "artifact_path":"...", "artifact_sha256":"<the bytes that shipped>",
 "verification":[{"tool":"...","artifact_sha256_at_run":"<must equal the shipped digest>",
                  "exit":0,"output_sha256":"...","counts":{...}}],
 "distinct_checker":{"attempt_id":"<not the author>","execution_id":"...","verdict":"...",
                     "evidence_path":"..."}}
```

Refused outright: a verification entry with no machine result; a result whose `artifact_sha256_at_run` does not
match the shipped artifact (it proves something about bytes that did not ship); a `distinct_checker` naming the
author's own attempt or execution; and the bare words *passed / cured / verified* standing in for any of these.

This does not replace the distinct-checker second-generation sweep. It asserts that the review **happened**, that
someone **else** did it, and it adds the artifact binding that the review alone never provided.

## The index and reviewer blindness

`SP/campaign/capture_index.v1.jsonl` links the records — **one row per execution** — and **never holds their
content**.

**Collecting records does not authorize sharing them.** A lane still under a blindness constraint is never given
the index, another lane's records, or any conclusion drawn from them, before its own independent review has landed.
The index is a permitted read for the orchestrator and for post-review lanes only: final checkers, transcript
auditors, and the end-of-campaign re-check. The tool refuses on `--for-blind-lane`.

## Audit scope — what OW-8 bounds

OW-6 and OW-6c audit **what exists**: available deliverables, evidence records, receipts, observable actions and
retained transcripts. Two prohibitions, both cutting against this campaign's own instincts:

- **Do not fabricate missing historical records.** An absent record is reported as absent, never reconstructed into
  something that reads as though it were written at the time.
- **Do not restart a completed audit merely because transcripts are absent.** A finished audit stands on what it
  actually read.

**Missing logs are not a stop condition.** An evidence gap and a defect are different things. Demonstrated material
defects still require containment and repair; that licence is about missing logs, not about known defects.

**Coverage is reported from a census, never from prose** (OW-10): `SP/campaign/_transcript_coverage_census.py`
counts `attempts`, `transcript_retained` and `observed` per book and never adds them together. Producing the census
is not authority to launch another blanket audit.
