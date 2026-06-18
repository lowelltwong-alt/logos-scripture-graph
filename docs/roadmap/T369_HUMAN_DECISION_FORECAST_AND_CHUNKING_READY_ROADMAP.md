---
object_type: roadmap_decision_forecast
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T368 after the maintainer asked why the goal was blocked and how to rewrite the roadmap so predictable human decisions happen early."
reason_for_inclusion: "Make the path to chunking readiness explicit, front-load owner decisions, and define what agents may and may not do before output-changing chunking resumes."
---

# T369 Human Decision Forecast And Chunking-Ready Roadmap

## Why The Goal Looked Blocked

The thread goal was marked blocked because the faithful path to chunking the Bible cannot skip
owner decisions. The repo is still able to do non-output-changing prep, but it must stop before
reviewed-gold promotion, route behavior, evaluator behavior, graph/retrieval outputs, textual-
critical policy, boundary import, or chunk output changes.

The fix is not to remove those gates. The fix is to ask the predictable owner decisions early and
record them in durable dockets before agents reach them mid-flight.

Machine-readable forecast:

```text
.ai/control/chunking_human_decision_forecast.yaml
```

## Chunking-Ready Definition

The project is ready for the first new output-changing chunk PR only when all of these are true:

- The owner has selected one exact target and scope.
- Reviewed gold or equivalent governed evidence has been promoted by owner decision.
- Any variant-sensitive case has an explicit textual-critical policy.
- The route is isolated to the selected lane and target.
- Tests cover the exact target and denial cases.
- Non-target output identity is proven.
- Same-baseline evaluation is planned before any improvement claim.
- The decision register is current.
- A no-context audit surface exists.
- The owner has separately authorized implementation.

Until then, agents may prepare packets, dockets, validators, audits, and harnesses, but may not
change chunk output.

## Front-Loaded Human Decisions

### HDF-001 - 1 Corinthians 8-10 Owner Option

Earliest gate: `T369`.

Options:

- `1COR8-10-T369-A`: preserve current overlapping chunks.
- `1COR8-10-T369-B`: approve `1Cor.8.1-1Cor.10.33` as a parent-only review target.
- `1COR8-10-T369-C`: approve parent plus exact child-boundary review targets.
- `1COR8-10-T369-D`: require more research.
- `1COR8-10-T369-E`: reject this case as the next implementation target.

No option authorizes chunk output by itself.

### HDF-002 - Textual-Critical Policy

Needed before any variant-sensitive packet is promoted, implemented, used as reviewed gold, or used
for canon/source-tradition/boundary decisions.

Faithful default if undecided: current canonical source only, variants as evidence only, and stop
before variant-sensitive authority.

### HDF-003 - Reviewed-Gold Promotion Standard

Owner target selection is not reviewed gold. A future promotion standard should require exact
scope, governed evidence, owner confirmation, tests, non-target identity proof, same-baseline
evaluation planning, and decision-register updates.

### HDF-004 - Agent Autonomy Boundary

Already partially decided: agents may continue green, non-output-changing research, prep, harness,
audit, and readiness PRs. They must stop before output-changing or authority-changing work.

### HDF-005 - First Implementation Lane

Best current candidate if owner selects and gold is strengthened: epistle argument, starting with
`1Cor.8.1-1Cor.10.33`.

If 1Cor.8-10 is rejected or needs more research, return to lane selection rather than quietly
implementing another target.

### HDF-006 - Parent-Only Versus Parent-Plus-Child

Faithful default: parent-only review target does not imply child spans. Exact child spans require
owner selection and governed evidence.

### HDF-007 - Systematic Theology Usage

The firewall allows orthodox systematic theology as advisory context, but not as hidden chunk
authority. No liberal-critical, anti-supernatural, anti-canonical, heterodox, or one-denomination
default may become a boundary rule.

### HDF-008 - Words Of Jesus And Speaker Boundaries

John 3 parent-only review is selected. Jesus/narrator boundaries and child spans remain undecided.
WJ/red-letter evidence remains metadata evidence only.

### HDF-009 - Revelation Neutrality

Revelation remains research/prep only under `REV-T344-E`. Do not select chronology, millennium
view, symbolic identities, or an eschatological system through chunking.

### HDF-010 - Graph, Retrieval, And Vector Output

Vectors and graph edges are never truth. No graph, retrieval, vector, or embedding output is
authorized by chunking prep.

### HDF-011 - Source Metadata Authority

Cross-references, Strong's-style numbers, lexical rarity, footnotes, headings, paragraph markers,
red-letter markers, and capitalization are evidence only.

### HDF-012 - Output-Changing Audit

Before the first output-changing PR, require a no-context audit, changed-output manifest,
non-target identity proof, same-baseline evaluation, decision-register update, and exact owner
implementation authorization.

## Roadmap From Here

1. `T369`: owner selects one 1Cor.8-10 option from the docket.
2. `T370`: if selected, build the governed reviewed-gold evidence packet, still no output changes.
3. `T371`: owner decides whether reviewed gold is promoted.
4. `T372`: build route-isolated implementation harness and non-target identity plan, still no output
   changes.
5. `T373`: owner gives exact implementation authorization or stops.
6. `T374`: implement only the authorized route and target.
7. `T375`: same-baseline evaluation and no-context audit.
8. `T376`: select the next lane using the decision forecast.

## What Not To Do

- Do not treat this roadmap or forecast as authorization.
- Do not implement chunks from pending packets.
- Do not treat owner option selection as reviewed-gold promotion.
- Do not infer child spans from parent-only review targets.
- Do not use systematic theology as hidden chunk authority.
- Do not use liberal-critical suspicion as a hidden default.
- Do not use source metadata as graph, retrieval, lexical, or chunk truth.
- Do not select textual-critical policy by implication.
- Do not import boundary material into canonical Scripture.
- Do not claim improvement without same-baseline evaluation.
- Do not merge output-changing work without exact owner authorization.

## Stop Conditions

Stop and ask the owner if any of these appears:

- unanticipated theological downstream risk;
- source metadata would become authority;
- variant-sensitive claim without policy;
- missing reviewed gold;
- evaluator confound;
- non-target output diff;
- route leakage outside the selected lane;
- graph/retrieval/vector output;
- boundary material import;
- theological authority change.
