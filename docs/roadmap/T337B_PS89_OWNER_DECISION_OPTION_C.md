# T337B Psalm 89 Owner Decision Option C

**Date:** 2026-06-10
**Task type:** human-reviewed gold/authorization update
**Status:** complete

## Decision

The owner approved Psalm 89 Option C.

Approved parent:

- `Ps.89.1-Ps.89.52`

Approved child retrieval spans:

- `Ps.89.1-Ps.89.4`
- `Ps.89.5-Ps.89.18`
- `Ps.89.19-Ps.89.37`
- `Ps.89.38-Ps.89.45`
- `Ps.89.46-Ps.89.48`
- `Ps.89.49-Ps.89.52`

Option C keeps `Ps.89.49-Ps.89.52` as one final retrieval child while explicitly labeling
`Ps.89.52` as the Book III doxology. `Ps.89.52` must not be treated as an ordinary continuation of
the lament appeal, and it must not be split into a one-verse orphan child.

## Authorization

Psalm 89 is now reviewed-gold approved.

This authorizes future T338 planning and implementation for exactly this route-isolated Psalm 89
target only.

T337B does not implement chunking behavior, regenerate chunks, change evaluator formulas, update
leaderboards or scorecards, mutate raw or canonical data, import boundary texts, start T327G, or
start Revelation implementation.

## Scope Limits

This decision does not authorize:

- broad Psalm rewrites;
- non-Psalm route leakage;
- a global Selah rule;
- a global blank-line rule;
- a global doxology rule;
- a global poetry rule;
- splitting Psalm 136;
- changing Psalm 78, Psalm 105, Psalm 106, Psalm 119, short Psalm, or superscription reviewed
  decisions;
- Revelation implementation;
- boundary import;
- T327G.

## T338 Gate

T338 may now be planned as a route-isolated Psalm 89 implementation PR.

T338 must:

- implement only the approved Psalm 89 Option C target;
- preserve non-target chunk identity or explain and block every diff;
- keep Psalm-specific behavior behind the Psalm route or candidate skill seam;
- add executable checks for the exact approved spans;
- prove `Ps.89.52` remains in final child `Ps.89.49-Ps.89.52`;
- not change evaluator formula, leaderboard, scorecards, raw data, canonical data, boundary imports,
  T327G, or Revelation implementation.

Claude Opus high review is recommended before or during T338 because output-changing behavior is now
authorized.
