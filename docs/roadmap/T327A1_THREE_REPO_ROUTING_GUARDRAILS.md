# T327A1 Three-Repo Routing Guardrails

## Status

- Task: T327A1
- Mode: governance/routing documentation
- Status: complete
- Scripture branch: `t327a1-three-repo-routing-guardrails`
- Boundary branch: `t002-three-repo-routing-guardrails`
- Governance branch: not edited because the local governance repo has pre-existing dirty work

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

## Machine-Readable Policies

Added in `logos-scripture-graph`:

- `.ai/control/boundary_material_routing.yaml`

Added in `logos-boundary-literature`:

- `.ai/control/boundary_material_routing.yaml`

## Governance-Repo Follow-Up

The local `logos-governance-architecture` checkout is present but has pre-existing dirty work on
branch `docs/shannon-note-hardening`. T327A1 did not edit it.

Required follow-up changes for `logos-governance-architecture`:

- Add the same three-repo authority hierarchy as a cross-repo policy.
- Register `BOUNDARY-MATERIAL-ROUTING-v1` or a governance-owned successor policy.
- Update repository-link contracts to name:
  - `logos-governance-architecture` as cross-repo policy authority;
  - `logos-scripture-graph` as canonical Scripture authority;
  - `logos-boundary-literature` as boundary/support authority.
- Add validation/update-flow language requiring boundary claims to remain scoped by trust level,
  tradition, profile, and provenance.
- Add the stop rule: if boundary material appears required to modify canonical Scripture outputs,
  stop and report.

## Confirmed / Inferred / Unknown

### Confirmed

- `logos-scripture-graph` front door and routing policy now direct boundary material away from
  canonical Scripture corpus surfaces.
- `logos-boundary-literature` front door and governance docs now state the same hierarchy and
  contamination controls.
- No source text, canonical data, generated output, chunk output, evaluator formula, scorecard, or
  runtime behavior changed.

### Inferred

- Future T327B should remain in `logos-scripture-graph` because it is canonical corpus correction.
- Future boundary source intake belongs in `logos-boundary-literature`, not in Scripture graph.

### Unknown

- Whether `logos-governance-architecture` should use the exact local YAML policy shape or define a
  governance-owned contract schema first.
