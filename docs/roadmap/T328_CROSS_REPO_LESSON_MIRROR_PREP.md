# T328 Cross-Repo Lesson Mirror Prep

## Status

- Task: T328_MIRROR_PREP
- Mode: planning / prep report
- Status: complete
- Branch: `t328-mirror-prep-report`
- Other repos edited: no
- Source import: none
- Boundary corpus records: none
- T327G: not started

## Purpose

Prepare, but do not execute, cross-repo lesson mirror updates for:

- `logos-governance-architecture`
- `logos-boundary-literature`
- LawFirm/FMG repos

This report keeps the Scripture-side lesson work from T328 visible while deferring cross-repo edits
until each target repo has a clean worktree, correct branch, and clear source-of-truth decision.

## Lessons To Mirror

| Lesson | Current Scripture-side collector | Mirror need |
| --- | --- | --- |
| `WORKFLOW-LESSON-001` | `docs/methodology/WORKFLOW_LESSONS.md` | Generated artifact corrections must live in generator/config/CI/test gates, not only local output. |
| `T327-LESSON-001` | `docs/methodology/WORKFLOW_LESSONS.md` | Untracked generated outputs shift review burden to generator behavior, validation, count/provenance, and handoff. |
| `BOUNDARY-WORKFLOW-LESSON-001` | `docs/methodology/WORKFLOW_LESSONS.md` | Boundary-source intake starts as planning/authority-scoped metadata, not corpus import. |
| `LAW-FIRM-WORKFLOW-LESSON-001` | `docs/methodology/WORKFLOW_LESSONS.md` | Operational exceptions become candidate records with gates, ledger, approval, and scale package before action. |

## Repo Mirror Matrix

| Repo | Mirror `WORKFLOW-LESSON-001` | Mirror `T327-LESSON-001` | Mirror `BOUNDARY-WORKFLOW-LESSON-001` | Mirror `LAW-FIRM-WORKFLOW-LESSON-001` | Notes |
| --- | --- | --- | --- | --- | --- |
| `logos-governance-architecture` | Yes | Yes | Yes | Maybe as cross-domain analogue | Should eventually be the source of truth for cross-repo workflow lessons and child-repo mirror rules. |
| `logos-boundary-literature` | Yes | Maybe | Yes | No, unless added as a neutral operational analogue | Needs boundary-source intake and contamination-control language, but must not import texts or create corpus records. |
| LawFirm/FMG authoritative repo | Yes | Maybe | No, except as analogy to source/data intake controls | Yes | Needs owner/source-of-truth decision first because multiple local LawFirm/FMG worktrees exist. |

## Why Each Repo Needs The Lessons

### logos-governance-architecture

Needs the generated-artifact and boundary-intake lessons because it owns cross-repo policy,
repository registration, relationship contracts, and AI front-door standards. The governance repo
should eventually become the source of truth for the general lesson collector, with child repos
mirroring repo-local applications.

### logos-boundary-literature

Needs boundary-source intake gating because it will own future boundary/noncanonical/source-intake
governance. It also needs generated-artifact durability if it later creates generated corpora,
manifests, claim indexes, or retrieval surfaces. Any update must preserve the rule that boundary
material cannot override or equal canonical Scripture authority.

### LawFirm/FMG repos

Need the exception-to-action lesson in the operational repo that owns exception/defect/candidate
workflows. The mirror should explain that operational defects, billing/portal/client-carrier deltas,
and workflow failures must become candidate records with evidence, owner, risk, proposed action,
validation gates, run ledger/audit evidence, approval where needed, and a scale package before they
become automation, policy, or client-facing behavior.

## Prerequisites Before Editing Any Target Repo

Every future mirror task must first confirm:

- clean worktree;
- correct branch;
- correct remote/default branch;
- source-of-truth decision for the repo;
- no unrelated dirty files;
- validation command for that repo;
- no source text import;
- no corpus creation unless explicitly authorized in that repo;
- no weakening of `logos-scripture-graph` canonical authority.

## Recommended Future Task Prompts

### Governance Repo Prompt

Create a clean branch in `logos-governance-architecture` to add a cross-repo workflow lesson
collector or registry section. Mirror `WORKFLOW-LESSON-001`, `T327-LESSON-001`, and
`BOUNDARY-WORKFLOW-LESSON-001`; decide whether `LAW-FIRM-WORKFLOW-LESSON-001` belongs as a
cross-domain analogue. Keep language public, repo-neutral, and source-of-truth oriented. Do not edit
child repos in the same task.

### Boundary Repo Prompt

Create a clean branch in `logos-boundary-literature` to mirror boundary-source intake and
generated-artifact durability lessons. Do not import texts, create source corpora, add real boundary
claims, or weaken cross-repo contamination controls. Preserve canonical Scripture authority as owned
by `logos-scripture-graph`.

### LawFirm/FMG Prompt

After selecting the authoritative LawFirm/FMG repo, create a clean branch to add the
exception-to-action lesson. Record candidate, gate, ledger, approval, and scale-package requirements
for operational exceptions and defect clusters. Do not change automation, policy, or client-facing
behavior in the mirror PR.

## Source-Of-Truth Direction

Target direction:

- `logos-governance-architecture` should become the source of truth for general cross-repo workflow
  lesson policy.
- `logos-scripture-graph` should keep Scripture-specific applications.
- `logos-boundary-literature` should mirror boundary/source-intake applications.
- LawFirm/FMG should mirror operational exception-to-action applications in the selected
  authoritative repo.

Child repos should mirror governance rather than redefine it.

## Stop Conditions

Stop before implementation if:

- the target repo is dirty;
- the target branch is unclear;
- the update would change authority hierarchy;
- the update would authorize boundary import or corpus creation;
- the update would alter canonical Scripture outputs;
- the update would create automation or policy changes instead of planning/docs.

## Recommendation

Do not edit other repos until their worktrees are clean and the owner confirms the authoritative
LawFirm/FMG repo. Review and merge this prep report before launching mirror PRs.
