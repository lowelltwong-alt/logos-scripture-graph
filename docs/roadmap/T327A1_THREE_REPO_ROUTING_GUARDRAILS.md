# T327A1 Three-Repo Routing Guardrails

## Status

- Task: T327A1
- Mode: governance/routing documentation
- Status: complete
- Scripture branch: `t327a1-routing-guardrails-main`
- Boundary branch: `t002-three-repo-routing-guardrails`
- Governance registry: merged in `logos-governance-architecture` and authoritative for repo
  registry / relationship contracts

T327A1 does not mutate data, regenerate outputs, import texts, move texts between repos, change
chunk output, change evaluator formulas, change parser/chunker/orchestrator behavior, change
scorecards, or start T327B.

## Three-Repo Authority Hierarchy

Confirmed:

1. `logos-governance-architecture` owns cross-repo policy, authority contracts, update rules,
   validation patterns, and repository-link governance.
2. `logos-scripture-graph` owns canonical 66-book Scripture truth: passage records, canonical
   chunking, Scripture gold/evaluator surfaces, stress/review packet surfaces, and canonical
   Scripture graph outputs.
3. `logos-boundary-literature` owns supporting boundary literature metadata, source status, trust
   profiles, reception/background/refutation relationships, and tradition-scoped claims.

Boundary literature may interoperate with canonical Scripture, but it is hierarchically under, or at
minimum never above, canonical Scripture authority.

## Routing Rule

| User/task intent | Correct repo |
|---|---|
| 66-book Scripture passages/chunks | `logos-scripture-graph` |
| Apocrypha/deuterocanon/boundary literature | `logos-boundary-literature` |
| Gnostic/fake/forged texts | `logos-boundary-literature` |
| Commentary/reception claims | `logos-boundary-literature` |
| Cross-repo policy/authority/update rules | `logos-governance-architecture` |
| Logos repo registry / relationship source of truth | `logos-governance-architecture` |
| Canonical corpus correction | `logos-scripture-graph` |
| Boundary text source intake | `logos-boundary-literature` |
| Repository-link contract changes | `logos-governance-architecture` or coordinated PR |

## Data-Flow Guardrails

Allowed:

- Scripture refs may point outward to boundary/reception materials as background or comparison.
- Boundary literature may reference Scripture.
- Commentary may discuss Scripture and boundary literature.
- Claims may exist when scoped by trust level, tradition, profile, and provenance.

Forbidden:

- Boundary claims must not become canonical Scripture claims.
- Noncanonical sources must not become default Scripture meaning.
- Commentary/reception claims must not mutate canonical Scripture records.
- Heterodox/forged/fake material must not enter canonical retrieval by default.
- Boundary repo material must not be treated as equal or superior authority to canonical Scripture.

If a task appears to require boundary material to modify canonical Scripture outputs, stop and
report.

## Boundary-Originated Governance Stop Rules

T327A.2 adds local Scripture-side mirrors of the governance stop rules:

- `BOUNDARY-GOV-001 - Governance Is Constraint, Not Obstacle`
- `BOUNDARY-GOV-002 - Owner-Reserved Authorization for Boundary-Originated Higher-Layer Changes`

If a boundary-originated request appears to require changing or bypassing governance-layer policy,
canonical Scripture authority, repository-link contracts, routing policy, trust hierarchy, or
canonical scope, agents must stop and emit the warning in `.ai/control/boundary_material_routing.yaml`.

Only Lowell Wong, as project owner, may authorize a boundary-originated request to change
higher-authority governance, canonical Scripture authority, repository-link contracts, canonical
scope, trust hierarchy, or cross-repo policy. Contributor consensus, contributor volume, automated
recommendation, agent routing, and boundary-layer operational need are not sufficient authority.

## Machine-Readable Policies

Added in `logos-scripture-graph`:

- `.ai/control/boundary_material_routing.yaml`

Added in `logos-boundary-literature`:

- `.ai/control/boundary_material_routing.yaml`

## Governance Registry Source Of Truth

`logos-governance-architecture` has now landed the Logos repo registry and future architecture
control plane. Its `governance/LOGOS_REPO_REGISTRY.yaml` is the source of truth for repo registry
entries and cross-repo relationship contracts.

This Scripture-side policy mirrors the governance registry locally for routing only. If local
Scripture wording conflicts with the governance registry, the governance registry wins and this repo
should be updated by coordinated PR.

The governance registry names:

- `logos-governance-architecture` as cross-repo policy / registry authority;
- `logos-scripture-graph` as canonical Scripture data-plane authority;
- `logos-boundary-literature` as supporting boundary / reception authority.

## Confirmed / Inferred / Unknown

### Confirmed

- `logos-scripture-graph` front door and routing policy now direct boundary material away from
  canonical Scripture corpus surfaces.
- `logos-boundary-literature` front door and governance docs now state the same hierarchy and
  contamination controls.
- `logos-governance-architecture` is the source of truth for the Logos repo registry and
  relationship contracts.
- No source text, canonical data, generated output, chunk output, evaluator formula, scorecard, or
  runtime behavior changed.

### Inferred

- Future T327B should remain in `logos-scripture-graph` because it is canonical corpus correction.
- Future boundary source intake belongs in `logos-boundary-literature`, not in Scripture graph.

### Unknown

- Whether a future registry-specific validator should be mirrored into child repos or stay only in
  `logos-governance-architecture`.
