# T344 Revelation Owner Selection Docket

## 1. Status

T344 is an owner-selection docket for the pending Revelation review packet:

```text
eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md
```

Target:

```text
Rev.12.1-Rev.14.20
```

Machine target id:

```text
rev12_14_symbolic_scenes
```

Owner selection status:

```yaml
owner_selection_status: pending
implementation_allowed: false
output_change_authorized: false
reviewed_gold_promoted: false
```

T344 does not implement Revelation chunking, promote reviewed gold, regenerate chunks, create a
Revelation route, change evaluator policy, create graph edges, or import boundary material.

## 2. Faithful Selection Rule

The owner selection must choose an exact behavior target without forcing a Revelation interpretive
school. A selected target must preserve orthodox interpretive possibilities and remain descriptive
and text-local.

Do not let the selected option decide:

- linear or non-linear chronology;
- premillennial, amillennial, postmillennial, preterist, historicist, futurist, or idealist
  readings;
- whether `Rev.12-Rev.14` is a standalone cycle, interlude, recapitulation, or chronological unit;
- symbolic identities for the woman, dragon, beasts, 144,000, Babylon, harvesters, or marked
  worshipers;
- whether Daniel or other cross-references control Revelation structure;
- speaker attribution from formatting, punctuation, headings, red-letter/WJ markers, or metadata.

## 3. Owner Selection Options

Only one option may be selected.

| Option id | Selection | Future effect if selected | Implementation now? |
| --- | --- | --- | --- |
| `REV-T344-A` | Preserve current committed Revelation behavior. | No reviewed gold is promoted; T345 remains blocked or should be skipped. | No |
| `REV-T344-B` | Promote parent-only reviewed gold for `Rev.12.1-Rev.14.20`. | A future T345 may implement only the exact parent span after executable reviewed-gold checks are added. | No |
| `REV-T344-C` | Promote parent plus exact child spans. | A future T345 may implement only the exact parent and child spans after executable reviewed-gold checks are added. | No |
| `REV-T344-D` | Mark the packet characterization-only. | Revelation implementation remains blocked; evidence may inform later review but not output. | No |
| `REV-T344-E` | Require more research before selection. | T344 stays pending; future research must remain non-authorizing unless separately governed. | No |

## 4. Exact Candidate For Option C

If the owner selects `REV-T344-C`, the exact child-span candidate from T343 is:

| Candidate span | Descriptive retrieval label | Non-authorizing guardrail |
| --- | --- | --- |
| `Rev.12.1-Rev.12.17` | Woman, dragon, child, and conflict scene | Label must not decide symbolic identity or chronology. |
| `Rev.13.1-Rev.13.18` | Beast imagery and worship/mark material | Label must not decide beast, empire, or eschatological school. |
| `Rev.14.1-Rev.14.5` | Lamb and 144,000 scene | Label must not decide identity or scope claims for the 144,000. |
| `Rev.14.6-Rev.14.13` | Angelic proclamations and perseverance call | Speaker/voice shifts remain reviewed evidence, not automatic authority. |
| `Rev.14.14-Rev.14.20` | Harvest and judgment imagery | Boundary must not prove chronology or recapitulation. |

These spans are not approved unless the owner selects `REV-T344-C`.

## 5. Recommended Posture

If the owner is ready to authorize a future Revelation implementation target, `REV-T344-C` is the
most implementation-useful option because it preserves a parent unit while making exact scene-shift
retrieval children reviewable.

If the owner is not ready to approve exact reviewed gold, choose `REV-T344-D` or `REV-T344-E`.
That is more faithful than letting an unreviewed Revelation model drift into algorithm work.

## 6. Required Updates After Owner Selection

If `REV-T344-A`, `REV-T344-D`, or `REV-T344-E` is selected:

- update this docket with the selected option and rationale;
- keep the Revelation packet pending or characterization-only;
- keep all implementation/output/reviewed-gold flags false;
- update the readiness map and decision register;
- decide whether T345 is blocked, skipped, or replaced by more review.

If `REV-T344-B` or `REV-T344-C` is selected:

- update the Revelation packet human decision box;
- update this docket with the exact owner decision and rationale;
- add or update reviewed-gold/equivalent governed evidence with executable checks;
- update the decision register with the exact selected parent/child behavior;
- update the readiness map so T345 can be considered;
- keep T345 route-isolated and non-global;
- require non-target identity proof before any output-changing implementation;
- keep source metadata, internal cross-references, Strong's-style numbers, lexical rarity, headings,
  footnotes, WJ/red-letter markers, paragraph/poetry markers, and formatting as evidence only.

## 7. Independent Audit Harness

T344 also adds a repo-resident no-context audit path so a separate AI or human reviewer can check
this branch after commit and push without relying on chat history.

Audit entry:

```text
.ai/audits/README.md
```

Protocol:

```text
.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md
```

Machine-readable surface map:

```text
.ai/control/audit_surface_map.yaml
```

Future harness upgrade roadmap:

```text
.ai/control/harness_upgrade_roadmap.yaml
```

Harness:

```bash
python scripts/agent/no_context_audit_harness.py --task-id T344 --base-ref origin/main --print
```

Validator:

```bash
python scripts/validate_audit_surface_map.py
```

The audit path is non-authorizing. Review reports can block, question, or recommend changes, but
they do not authorize owner decisions, reviewed gold, output changes, boundary import, graph edges,
or master-context changes.

## 8. Non-Authorizations

This docket does not authorize:

- Revelation implementation;
- output-changing Revelation chunking;
- reviewed-gold promotion;
- parent or child span approval;
- a Revelation route or route behavior;
- global apocalypse, prophecy, chronology, recapitulation, interlude, symbolic-identity, Babylon, or
  millennium rules;
- source metadata as authority;
- internal cross-references as intertext authority;
- Strong's-style numbering as lexical authority;
- Greek lexical rarity as original-language authority;
- boundary, apocalyptic, apocryphal, or noncanonical material import;
- raw or canonical data mutation;
- generated chunk regeneration;
- evaluator formula changes;
- leaderboard or scorecard changes;
- embedding runs, vector index builds, or graph-edge generation;
- Psalm candidate promotion;
- T327G.

## 9. RISK-GATE-001 Map

Required question:

```text
What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?
```

### Confirmed Risks

- A selection docket could be mistaken for reviewed gold.
- Listing exact Option C child spans could be mistaken for owner approval.
- Recommending Option C could be overread as an agent-made theological or output decision.

### Plausible Risks

- Parent/child spans could encode chronology, recapitulation, interlude status, or symbolic identity.
- Cross-reference or Strong's-style metadata could become hidden boundary authority.
- Future implementation could leak a Revelation-specific rule into prophets, Daniel, Gospel
  discourse, Psalm poetry, or the monolith fallback.

### Unlikely But High-Impact Risks

- Boundary/apocalyptic or noncanonical literature could be imported to settle Revelation structure.
- A whole-Bible orchestration layer could treat one Revelation selection as a global apocalypse rule.

### Watch-Later Conditions

- Any PR that sets implementation, output-change, or reviewed-gold flags true without an owner
  selection.
- Any PR that changes chunker, route, evaluator, generated chunks, vector/edge, or graph behavior
  while citing this docket alone.
- Any PR that treats labels as symbolic-identity claims.

### Tests Or Guards Needed

- T344 tests must assert owner selection is pending and all authorization flags are false.
- Future owner-selected reviewed gold must have exact executable checks.
- Future implementation must prove non-Revelation output identity.

### Owner Decisions Needed

- Select exactly one option: `REV-T344-A`, `REV-T344-B`, `REV-T344-C`, `REV-T344-D`, or
  `REV-T344-E`.
- If selecting `REV-T344-C`, confirm whether the exact listed child spans are approved.
- Decide whether speaker/voice policy is needed before Revelation implementation.

## 10. Owner Decision Box

```yaml
owner_selection:
  reviewer: null
  date: null
  selected_option: pending
  selected_parent: null
  selected_children: []
  rationale: null
  implementation_allowed: false
  output_change_authorized: false
  reviewed_gold_promoted: false
  notes: >
    T344 opens the owner-selection docket only. No Revelation reviewed gold, implementation,
    route behavior, output change, evaluator change, generated output, boundary import,
    T327G, embedding/index/edge work, graph-edge generation, whole-Bible output-changing pass,
    or Psalm candidate promotion is authorized until the owner selects one exact option and the
    required governed evidence is updated.
```
