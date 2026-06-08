# T327A.2 Boundary Governance Stop Rules

## Status

- Task: T327A2
- Mode: governance/routing documentation
- Status: complete
- Scripture branch: `t327a2-boundary-governance-stop-rules`
- Data mutation: none
- Output change: none
- T327B: not started

T327A.2 mirrors the governance and boundary-repo stop rules inside `logos-scripture-graph` so an
agent entering the Scripture repo can recognize boundary-originated higher-layer conflicts.

## Named Rules

- `BOUNDARY-GOV-001 - Governance Is Constraint, Not Obstacle`
- `BOUNDARY-GOV-002 - Owner-Reserved Authorization for Boundary-Originated Higher-Layer Changes`

## Policy

Boundary-originated requests must not change or bypass governance-layer policy, canonical Scripture
authority, repository-link contracts, routing policy, trust hierarchy, or canonical scope from the
boundary layer.

Only Lowell Wong, as project owner, may authorize a boundary-originated request to change
higher-authority governance, canonical Scripture authority, repository-link contracts, canonical
scope, trust hierarchy, or cross-repo policy.

Contributor consensus, contributor volume, automated recommendation, agent routing, and
boundary-layer operational need are not sufficient authority.

## Required Warning

The exact warning text is stored in `.ai/control/boundary_material_routing.yaml` and repeated in
`AI_FRONT_DOOR.md`.

## Scope

- No raw/canonical data mutation.
- No generated output regeneration.
- No chunk output change.
- No evaluator/leaderboard/scorecard change.
- No parser/chunker/orchestrator runtime change.
- No source text import.
- No T327B work.

## Next

Review and merge T327A.2 if validation is green. Then T327B may proceed as an isolated 66-book
allow-list / ingest-filter task.
