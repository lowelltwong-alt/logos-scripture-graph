# Unintended Consequence Review

Status: active methodology
Owner: methodology / roadmap governance
Last updated: 2026-06-09

This methodology is a deterministic gate for high-leverage changes. It is documentation and
control-plane guidance only; it does not authorize runtime changes, output changes, boundary
imports, T327G, T337, or Revelation implementation.

## 1. Purpose

High-leverage changes can succeed at their intended goal while accidentally creating a permission
path, weakening an existing guard, contaminating a trust zone, overfitting a metric, globalizing a
local heuristic, or making a bad direction harder to reverse.

This review forces the agent to map those risks before merge. The map should be concrete enough for
reviewers to decide whether to block now, patch now, add a test, watch later, defer to the owner, or
create a future task.

## 2. Trigger Conditions

Run this review before merging changes that touch any of these areas:

- authority hierarchy;
- canonical or boundary scope;
- routing or orchestrator behavior;
- chunker or evaluator behavior;
- default retrieval;
- score or leaderboard policy;
- generated artifact behavior;
- workflow rules;
- cross-repo contracts;
- automation permissions;
- master-chunker or reusable architecture;
- client-facing or legal-facing automation.

For authority, routing, default-behavior, evaluator, corpus-scope, boundary, or master-chunker
changes, treat this as a P0 stop-line gate. For roadmap/control-plane changes, treat this as a P1
required review gate unless the task explicitly escalates it.

## 3. Required Review Question

What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?

## 4. Required Map Format

Every review must record these categories:

- confirmed risks;
- plausible risks;
- unlikely but high-impact risks;
- watch-later conditions;
- tests or guards needed;
- owner decisions needed.

Suggested YAML template:

```yaml
unintended_consequence_review:
  change_id:
  change_type:
  high_leverage_trigger:
  intended_effect:
  confirmed_risks: []
  plausible_risks:
    - risk:
      why_plausible:
      severity:
      likelihood:
      warning_sign:
      mitigation:
      follow_up:
  unlikely_high_impact_risks:
    - risk:
      why_high_impact:
      watch_condition:
      owner_decision_required:
  tests_or_guards_needed: []
  owner_decisions_needed: []
  defer_until:
```

## 5. Severity And Likelihood Rubric

Severity:

- P0 critical: could weaken authority, contaminate canonical/boundary scope, authorize runtime or
  output changes, alter default retrieval, change evaluator/leaderboard meaning, or create legal /
  client-facing automation without review.
- P1 high: could mislead roadmap sequencing, create stale next-task pointers, broaden a workflow
  rule, or make an implementation lane look more authorized than it is.
- P2 medium: could create documentation drift, reviewer confusion, or missing follow-up tests.
- P3 low: minor wording or discoverability risk with no behavior or authority effect.

Likelihood:

- confirmed: already present in the diff or known repo state.
- plausible: credible based on the changed surface and project history.
- unlikely: not expected, but high-impact enough to document a watch condition.

## 6. Follow-Up Handling

Use one of these outcomes for each risk:

- block now;
- patch now;
- add test;
- add watchlist item;
- defer with owner decision;
- record as future task.

Do not use "watch later" for a risk that already creates authority leakage, output authorization,
canonical/boundary contamination, or unsafe automation.

## 7. Examples

### Bible-First / Master-Chunker Risk

Risk: a future master chunker could treat Bible, boundary, commentary, and legal corpora as one
shared optimization problem.

Why it matters: a single shared cross-corpus optimization objective across Bible and non-Bible
corpora is forbidden. Non-Bible training/eval cases must not tune canonical Bible behavior.

Mitigation: keep the canonical Bible chunker as the highest-priority substrate. The master chunker
may coordinate separate harnesses, but it must not collapse authority layers or optimize canonical
Bible behavior against non-Bible cases.

### Revelation Rule Leakage Risk

Risk: Revelation/apocalypse rules could become global heuristics for prophecy, Psalms, Gospel
discourse, or the monolith fallback.

Mitigation: keep Revelation work in atlas/review-packet lanes until reviewed gold exists. Route
Revelation-specific rules through explicit route gates and fail closed when evidence is insufficient.

### Boundary Import / Backdoor Authorization Risk

Risk: a planning doc about boundary material could be read as permission to import noncanonical
texts or create boundary corpus records in `logos-scripture-graph`.

Mitigation: state that boundary work is planning-only unless separately owner-authorized in the
correct repo. Do not mutate `data/raw/**`, `data/canonical/**`, default retrieval, chunks, evaluator
inputs, scorecards, or review-packet indexes with boundary material.

### Generated Artifact Durability Risk

Risk: a local regeneration could make outputs appear corrected while the committed generator,
validator, or CI path still permits drift.

Mitigation: commit the durable generator/config/validator change, add a fail-closed test, and record
the exact validation path. Do not treat ignored generated output as source truth.

### LawFirm Exception-To-Automation Risk

Risk: a recurring legal-workflow exception could become direct automation without evidence, review,
or an audit ledger.

Mitigation: convert exceptions into reviewed candidates with evidence, owner, risk, proposed action,
approval gate, run ledger, and scale package before any client-facing or legal-facing automation.
