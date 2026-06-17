# No-Context Review Protocol

## 1. Ground Rules

Assume chat context is unavailable and non-authoritative. Review only what can be proven from:

- files in the checked-out branch;
- git history and diffs;
- GitHub PR metadata/checks, when available;
- validation output;
- repo-resident logs, handoffs, decision registers, and roadmap state.

If a claim is only present in chat or a final assistant message, treat it as unproven.

## 2. Establish State

Run:

```bash
git status -sb
git branch --show-current
git fetch origin --prune --tags
git log --oneline --decorate -n 8
```

If reviewing a PR:

```bash
gh pr view <PR_NUMBER> --json number,title,state,isDraft,mergedAt,mergeable,headRefName,baseRefName,url,statusCheckRollup
gh pr diff <PR_NUMBER> --name-only
```

If reviewing a local branch:

```bash
git merge-base HEAD origin/main
git diff --name-status origin/main...HEAD
git diff --stat origin/main...HEAD
```

Stop and report if the worktree is dirty in ways unrelated to the review.

## 3. Reconstruct Intent

Read:

```text
ROADMAP_STATE.yaml
.ai/control/PROJECT_STATUS.md
.ai/control/current_focus.yaml
.ai/tasks/<task_id>.task.yaml
.ai/handoffs/<task_id>/handoff.md
.ai/control/roadmap_events.jsonl
.ai/control/handoff_ledger.jsonl
.ai/control/harness_upgrade_roadmap.yaml
```

Then answer:

- What task is active or being reviewed?
- What did the task claim to change?
- What did it explicitly not authorize?
- Which files were in scope?
- Which validators/tests were required?
- What is the exact next action?
- Did the review reveal a repeated issue that should be added to the future harness roadmap?

## 4. Inspect Changed Files

For every changed file, classify it:

- control plane;
- roadmap/doc;
- methodology/lesson;
- decision register/readiness map;
- review packet/gold/evaluator;
- code/config;
- raw/canonical/generated data;
- graph/vector/retrieval;
- tests.

Flag any changed file outside the task scope or any protected path touched without explicit
authorization.

## 5. Red-Team Questions

Ask these before accepting the work:

- Does the diff match the stated task and no more?
- Are all owner decisions recorded in durable files rather than chat?
- Does any pending packet, docket, index, or roadmap note accidentally authorize reviewed gold?
- Does any chunk boundary, label, route, evaluator, or metadata rule imply a theological position?
- Did source metadata become authority instead of evidence?
- Did cross-references, Strong's-style numbers, Greek lexical rarity, headings, footnotes, WJ
  markers, or formatting become hidden boundary authority?
- Did any Revelation language choose chronology, recapitulation, symbolic identity, millennium
  view, or eschatological school?
- Did any Psalm-specific or Revelation-specific rule leak globally?
- Did any change touch raw/canonical/generated chunk/evaluator/vector/edge surfaces?
- If watched paths changed, did the decision register/readiness map update?
- Do tests prove the actual broad claim, or only a narrow string check?
- Does validation pass locally and in GitHub checks when available?
- Is the handoff precise enough for a no-context next agent?
- Does `.ai/control/harness_upgrade_roadmap.yaml` already cover any repeated issue discovered in
  this review?

## 6. Required Validation

Run the task-specific validation listed in `.ai/tasks/<task_id>.task.yaml`, then run:

```bash
python scripts/validate_all.py
python -m pytest -q
```

For chunking-related review, also run:

```bash
python scripts/validate_chunking_agent_preflight.py
python scripts/validate_chunking_theological_decision_register.py
python scripts/validate_bible_chunking_readiness_map.py
python scripts/validate_audit_surface_map.py
```

If a validation command cannot run, record why and treat any dependent claim as unproven.

## 7. Report Format

Use findings-first format:

```text
P0/P1/P2/P3 - Title
File/line:
Evidence:
Risk:
Recommended fix:
```

Then include:

- open questions;
- validation run;
- files inspected;
- whether the work can be merged, needs changes, or needs owner decision.

Use `.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md` for a durable report.

## 8. Stop Conditions

Stop and report immediately if:

- raw or canonical Scripture data changed without explicit task authorization;
- generated chunks, evaluator policy, leaderboard, vector/index, or graph edges changed without
  explicit task authorization;
- a pending review packet or owner-selection docket is treated as reviewed gold;
- a chunking decision with theological downstream risk lacks a decision-register entry;
- a governance or workflow lesson is discovered but not routed to a durable surface;
- `MASTER_CONTEXT.md` or its lock changed without human approval.
