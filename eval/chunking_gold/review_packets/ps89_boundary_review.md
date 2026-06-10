# Psalm 89 Boundary Review Packet

## Status

- Status: `approved_structural_split_under_parent_whole_psalm`
- Stress atlas case ID: `ps89_royal_lament`
- T337A selection: selected as the single Psalm target for human review
- T337B owner decision: Option C
- Decision: approved_with_scope_note
- Parent/child candidate: approved for Psalm 89 only
- Approved parent unit: `Ps.89.1-Ps.89.52`
- Approved child chunks:
  - `Ps.89.1-Ps.89.4`
  - `Ps.89.5-Ps.89.18`
  - `Ps.89.19-Ps.89.37`
  - `Ps.89.38-Ps.89.45`
  - `Ps.89.46-Ps.89.48`
  - `Ps.89.49-Ps.89.52`

This packet records reviewed gold and authorizes a future route-isolated T338 implementation for
Psalm 89 only. It does not implement chunking behavior.

## 1. Review Target

Review target: Psalm 89, `Ps.89.1-Ps.89.52`.

T337A selected Psalm 89 as the one Psalm target for human review. T337B records the owner's Option C
decision and promotes Psalm 89 to reviewed gold. This is still a human-reviewed gold/authorization
update only: it does not start T338 and does not implement new Psalm boundaries.

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

- Current status: `approved_structural_split_under_parent_whole_psalm`.
- Implementation authorization: true for a future route-isolated Psalm 89 implementation only.
- Output-change authorization: true for the exact approved Psalm 89 target only.
- Reviewed-gold promotion: true for Psalm 89 only.

The existing chunk observation remains historical diagnostic evidence from T318. The authority in
this packet is the owner's 2026-06-10 Option C decision, not the historical observation.

## 4. Exact Passage And Span References

- Approved parent: `Ps.89.1-Ps.89.52`
- Approved child-span set:
  - `Ps.89.1-Ps.89.4`
  - `Ps.89.5-Ps.89.18`
  - `Ps.89.19-Ps.89.37`
  - `Ps.89.38-Ps.89.45`
  - `Ps.89.46-Ps.89.48`
  - `Ps.89.49-Ps.89.52`

`Ps.89.52` is the Book III doxology. Option C keeps `Ps.89.49-Ps.89.52` as one final retrieval
child to avoid a one-verse orphan and preserve canonical/final-form usefulness. `Ps.89.52` must not
be treated as an ordinary continuation of the lament appeal, but it also must not be split into a
one-verse orphan child.

## 5. Current Chunker Behavior, If Available

T318 observed current behavior from a historical pre-T327 temporary chunker run:

| Observed chunk | Approx tokens | Genre | Boundary basis | Sentence ended |
| --- | ---: | --- | --- | --- |
| `Ps.89.1-Ps.89.52` | 823 | `psalms` | `chapter_boundary`, `whole_psalm` | true |

The observed behavior keeps Psalm 89 as one whole-psalm chunk. That observation is diagnostic only:
it is not reviewed gold, not approved expected output, and not a post-T327 chunk regeneration.

No fresh chunk regeneration was performed for T337A.

## 6. Approved Reviewed Target Behavior

The approved target behavior is:

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

The parent unit must remain the whole Psalm. Child chunks are retrieval children under the parent
whole-psalm literary unit.

## 7. Approved Exact Spans And Boundaries

| Approved child span | Review label | Boundary evidence and scope note |
| --- | --- | --- |
| `Ps.89.1-Ps.89.4` | Opening praise and covenant promise | Ends at a recorded Selah / `qs` sample ref (`Ps.89.4`). |
| `Ps.89.5-Ps.89.18` | Hymnic praise of Yahweh's rule and blessed people | T318 records a blank-line / `b` sample ref at `Ps.89.18`. |
| `Ps.89.19-Ps.89.37` | Davidic covenant oracle and promise | Ends at recorded Selah / `qs` and `b` sample refs (`Ps.89.37`). |
| `Ps.89.38-Ps.89.45` | Lament over apparent covenant rejection | Ends at a recorded Selah / `qs` sample ref (`Ps.89.45`). |
| `Ps.89.46-Ps.89.48` | Mortality plea and urgent petition | Ends at a recorded Selah / `qs` sample ref (`Ps.89.48`). |
| `Ps.89.49-Ps.89.52` | Closing plea plus Book III doxology | Keeps `Ps.89.52` with the final retrieval child; no one-verse orphan split. |

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

The approval intentionally does not derive a rule such as "split every Selah" or "split every long
Psalm." It approves only the exact Psalm 89 span set.

## 9. What This Authorizes

This packet authorizes a future T338 implementation task to:

- implement or guard exactly the approved Psalm 89 parent/child target;
- add executable checks for the approved Psalm 89 spans;
- require non-target chunk identity preservation;
- keep the rule isolated to the Psalm route or Psalm candidate skill seam;
- cite this packet as the human-reviewed authority for the exact Psalm 89 target.

## 10. What This Does Not Authorize

This packet does not authorize:

- a global Psalm, Selah, `\qs`, `\b`, refrain, or poetry heuristic;
- a global doxology rule;
- splitting `Ps.89.52` into a one-verse orphan child;
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

A future T338 PR must add focused executable checks that prove:

- Psalm 89 has parent `Ps.89.1-Ps.89.52`.
- Psalm 89 child spans exactly match the human-approved span set.
- `Ps.89.52` is treated as the Book III doxology within final child `Ps.89.49-Ps.89.52`.
- `Ps.89.52` is not split into a one-verse orphan child.
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

- Treating Selah / `\qs` or `\b` markers as automatic split authority would weaken the reviewed-gold
  gate.
- Calling this a chunking improvement before implementation and same-baseline evaluation would
  overstate the result.

### Plausible Risks

- A future implementation may generalize the Psalm 89 span proposal into a global Selah or long-Psalm
  rule.
- A Psalm-specific behavior may leak into Song, Lam, Job, prophecy, Gospel discourse, or Revelation
  if route isolation is weakened.
- T338 may generalize beyond the exact Psalm 89 approval because the exact spans are now
  implementation-authorizing.

### Unlikely But High-Impact Risks

- Boundary or noncanonical source material could be imported as supposed support for the Psalm 89
  decision.
- A master chunker could use this review packet as training pressure for non-Bible corpora or global
  poetry behavior.
- Revelation or other hard-book implementation could cite this Psalm review packet as precedent for
  non-Psalm output changes.

### Watch-Later Conditions

- Any PR that changes chunks, evaluator, orchestrator, leaderboard, scorecards, raw data, or canonical
  data while claiming to be T337A.
- Any implementation that changes non-target Psalm or non-Psalm output without explicit explanation.

### Tests Or Guards Needed

- Deterministic tests should keep this packet scoped to Psalm 89 Option C and forbid global Selah,
  blank-line, doxology, or poetry rules.
- Future T338 tests must assert the exact approved spans and non-target identity.
- Existing tests must continue to reject pending packet promotion and global route leakage.

### Owner Decisions Needed

- No owner decision remains for Psalm 89 Option C.
- The owner must authorize any future change beyond the exact Psalm 89 target separately.
- The owner must decide separately whether Psalm 136 remains pending, becomes a whole-psalm control,
  or receives a later separate review packet.

## 14. Human Review Decision Box

```yaml
human_review_decision:
  reviewer: Lowell Wong
  date: 2026-06-10
  decision: approved_with_scope_note
  implementation_allowed: true
  output_change_authorized: true
  reviewed_gold_promoted: true
  notes: >
    Approved Psalm 89 parent/child reviewed-gold target using Option C.
    Keep Ps.89.49-Ps.89.52 as one final retrieval child while explicitly
    labeling Ps.89.52 as the Book III doxology. Ps.89.52 must not be treated
    as an ordinary continuation of the lament appeal, and must not be split
    into a one-verse orphan child. This approval authorizes only this Psalm 89
    reviewed-gold target and a future route-isolated Psalm implementation task.
    It does not authorize broad Psalm rewrites, global poetry rules, automatic
    Selah splitting, automatic blank-line splitting, automatic doxology splitting,
    Revelation implementation, boundary import, T327G, or non-Psalm route leakage.
```

## 15. Current Authorizing Rule

Psalm 89 is now reviewed-gold approved for Option C. T338 may now be planned as a route-isolated
implementation of exactly this Psalm 89 target, but T338 has not started in this task.
