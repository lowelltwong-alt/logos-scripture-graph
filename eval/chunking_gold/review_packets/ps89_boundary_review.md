# Psalm 89 Boundary Review Packet

## Status

- Status: `pending_human_review`
- Stress atlas case ID: `ps89_royal_lament`
- T337A selection: selected as the single Psalm target for human review
- Decision: pending
- Parent/child candidate: yes, pending review
- Proposed parent unit for review: `Ps.89.1-Ps.89.52`
- Approved child chunks: none

This packet does not authorize output-changing work.

## 1. Review Target

Review target: Psalm 89, `Ps.89.1-Ps.89.52`.

T337A selects Psalm 89 as the one Psalm target for human review. This is a review/evidence packet
only. It does not promote Psalm 89 to reviewed gold, does not start T338, and does not implement new
Psalm boundaries.

## 2. Why This Target Was Selected

Psalm 89 is the strongest pending Psalm review candidate because it is:

- long enough to plausibly benefit from parent/child retrieval structure;
- already characterized as a royal/lament Psalm with covenant memory, lament, petition, and
  doxology turns;
- supported by existing marker/form evidence (`q1`, `q2`, `b`, and `qs` / Selah evidence);
- narrow enough for exact span review inside one Psalm;
- less likely than a broad Psalm rule to create non-target regressions;
- more likely than Psalm 136 to unlock a behavior-changing review decision, because Psalm 136 is
  shorter and its refrain form may argue for whole-psalm preservation.

Psalm 136 remains pending and non-authorizing. It was not selected for T337A because its 346-token
litany structure is more likely to become a reviewed whole-psalm control or refrain-aware control
than the next narrow behavior-change target.

## 3. Current Status

- Current status: `pending_human_review`.
- Implementation authorization: none.
- Output-change authorization: none.
- Reviewed-gold promotion: none.

The existing observation is historical diagnostic evidence from T318, not current post-T327
reviewed gold. It must not be treated as approved expected output.

## 4. Exact Passage And Span References

- Parent candidate: `Ps.89.1-Ps.89.52`
- Proposed child-span set for human review:
  - `Ps.89.1-Ps.89.4`
  - `Ps.89.5-Ps.89.18`
  - `Ps.89.19-Ps.89.37`
  - `Ps.89.38-Ps.89.45`
  - `Ps.89.46-Ps.89.48`
  - `Ps.89.49-Ps.89.52`

These proposed child spans are not approved. They exist so the reviewer can approve, reject, or
replace one exact span set without inventing boundaries during implementation.

## 5. Current Chunker Behavior, If Available

T318 observed current behavior from a historical pre-T327 temporary chunker run:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Ps.89.1-Ps.89.52` | 823 | `psalms` | `chapter_boundary`, `whole_psalm` | true |

The observed behavior keeps Psalm 89 as one whole-psalm chunk. That observation is diagnostic only:
it is not reviewed gold, not approved expected output, and not a post-T327 chunk regeneration.

No fresh chunk regeneration was performed for T337A.

## 6. Proposed Reviewed Target Behavior

If the reviewer approves a behavior-changing target, the proposed target behavior is:

```text
Parent literary unit:
  Ps.89.1-Ps.89.52

Reviewed child structural chunks:
  Ps.89.1-Ps.89.4
  Ps.89.5-Ps.89.18
  Ps.89.19-Ps.89.37
  Ps.89.38-Ps.89.45
  Ps.89.46-Ps.89.48
  Ps.89.49-Ps.89.52
```

The parent unit must remain the whole Psalm. Child chunks, if approved, are retrieval children under
the parent whole-psalm literary unit.

## 7. Proposed Exact Spans And Boundaries

| Proposed child span | Review label | Boundary evidence to review |
| --- | --- | --- |
| `Ps.89.1-Ps.89.4` | Opening praise and covenant promise | Ends at a recorded Selah / `qs` sample ref (`Ps.89.4`). |
| `Ps.89.5-Ps.89.18` | Hymnic praise of Yahweh's rule and blessed people | T318 records a blank-line / `b` sample ref at `Ps.89.18`. |
| `Ps.89.19-Ps.89.37` | Davidic covenant oracle and promise | Ends at recorded Selah / `qs` and `b` sample refs (`Ps.89.37`). |
| `Ps.89.38-Ps.89.45` | Lament over apparent covenant rejection | Ends at a recorded Selah / `qs` sample ref (`Ps.89.45`). |
| `Ps.89.46-Ps.89.48` | Mortality plea and urgent petition | Ends at a recorded Selah / `qs` sample ref (`Ps.89.48`). |
| `Ps.89.49-Ps.89.52` | Closing plea and doxology | Preserves the Psalm's closing appeal and doxology together. |

Marker evidence is evidence only. `\qs`, `\b`, `q1`, and `q2` do not automatically approve child
chunk boundaries.

## 8. Rationale

Psalm 89 is a better T337A review target than Psalm 136 because it offers a clearer test of the
parent/child Psalm model:

- it is long enough that child retrieval chunks may be useful;
- it contains multiple structural turns that can be reviewed with exact spans;
- it has existing Selah and blank-line evidence at possible turn points;
- it follows the Psalm 78 precedent in needing a parent whole-psalm unit plus possible reviewed
  children;
- it can be evaluated without a broad Psalm rewrite or a global poetry heuristic.

The proposal intentionally does not derive a rule such as "split every Selah" or "split every long
Psalm." The only review question is whether this exact Psalm 89 span set should be promoted.

## 9. What This Would Authorize If Approved

If and only if the human review decision below is changed from pending/false to an explicit approval,
this packet would authorize a future T338 implementation task to:

- implement or guard exactly the approved Psalm 89 parent/child target;
- add executable checks for the approved Psalm 89 spans;
- require non-target chunk identity preservation;
- keep the rule isolated to the Psalm route or Psalm candidate skill seam;
- cite this packet as the human-reviewed authority for the exact Psalm 89 target.

## 10. What This Does Not Authorize

This packet does not authorize:

- T338 before human approval;
- any chunking behavior change while decision remains pending;
- a global Psalm, Selah, `\qs`, `\b`, refrain, or poetry heuristic;
- changing Psalm 78, Psalm 105, Psalm 106, Psalm 119, short Psalm, or superscription reviewed
  decisions;
- splitting Psalm 136;
- evaluator formula changes;
- leaderboard or scorecard updates;
- chunk output regeneration;
- raw or canonical data mutation;
- source text or boundary text imports;
- T327G;
- Revelation implementation;
- chunking improvement claims.

## 11. Required Executable Gold Checks

If approved, a future T338 PR must add focused executable checks that prove:

- Psalm 89 has parent `Ps.89.1-Ps.89.52`.
- Psalm 89 child spans exactly match the human-approved span set.
- The implementation does not split or merge reviewed Psalm 78 child spans.
- Psalm 105 remains one reviewed whole-psalm chunk.
- Psalm 106 remains one reviewed whole-psalm chunk.
- Psalm 119 remains its exact 22-section reviewed behavior.
- Short Psalm and superscription guardrails remain stable.
- Non-target canonical poetry controls (`Song`, `Lam`) remain on the monolith fallback.
- No pending-only packet is promoted by code path or test fixture.

## 12. Non-Target Identity Requirement

A future output-changing implementation must preserve non-target chunk identity outside the approved
Psalm 89 target. Any diff outside the approved Psalm 89 spans must be explained as either:

- a direct consequence of the exact approved Psalm 89 parent/child change; or
- a blocker that stops the implementation PR.

No aggregate score, token-budget preference, or marker-only evidence can override this requirement.

## 13. RISK-GATE-001 Map

Required question: What could this change accidentally authorize, weaken, contaminate, overfit,
globalize, or make harder to reverse?

### Confirmed Risks

- Promoting this packet without human approval would turn pending characterization into behavior
  authority.
- Treating Selah / `\qs` or `\b` markers as automatic split authority would weaken the reviewed-gold
  gate.
- Calling this a chunking improvement before implementation and same-baseline evaluation would
  overstate the result.

### Plausible Risks

- A future implementation may generalize the Psalm 89 span proposal into a global Selah or long-Psalm
  rule.
- A Psalm-specific behavior may leak into Song, Lam, Job, prophecy, Gospel discourse, or Revelation
  if route isolation is weakened.
- T338 may be started with this packet still pending because the exact spans are already written
  here.

### Unlikely But High-Impact Risks

- Boundary or noncanonical source material could be imported as supposed support for the Psalm 89
  decision.
- A master chunker could use this review packet as training pressure for non-Bible corpora or global
  poetry behavior.
- Revelation or other hard-book implementation could cite this Psalm review packet as precedent for
  non-Psalm output changes.

### Watch-Later Conditions

- Any PR that flips implementation allowance to true without a human reviewer, date, and approval
  notes.
- Any PR that changes chunks, evaluator, orchestrator, leaderboard, scorecards, raw data, or canonical
  data while claiming to be T337A.
- Any implementation that changes non-target Psalm or non-Psalm output without explicit explanation.

### Tests Or Guards Needed

- A deterministic test should keep this packet selected, pending, and non-authorizing until human
  review changes the decision box.
- Future T338 tests must assert the exact approved spans and non-target identity.
- Existing tests must continue to reject pending packet promotion and global route leakage.

### Owner Decisions Needed

- Approve, reject, or replace the proposed Psalm 89 child-span set.
- Decide whether approval should authorize T338 implementation or only create reviewed gold.
- Decide whether Psalm 136 remains pending, becomes a whole-psalm control, or receives a later
  separate review packet.

## 14. Human Review Decision Box

```yaml
human_review_decision:
  reviewer:
  date:
  decision: pending
  implementation_allowed: false
  output_change_authorized: false
  reviewed_gold_promoted: false
  notes:
```

## 15. Current Non-Authorizing Rule

Until the decision box is updated by a human reviewer, Psalm 89 remains pending and non-authorizing.
T338 remains blocked.
