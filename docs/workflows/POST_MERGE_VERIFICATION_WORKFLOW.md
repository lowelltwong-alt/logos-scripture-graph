# Post-Merge Verification Workflow

## 1. Purpose

Post-merge verification is the mandatory checkpoint between a merged PR and the next task. It
confirms that the intended PR landed on `main`, that the expected commit is reachable, that the repo
is clean, and that required validation still passes.

This workflow prevents each PR from needing a bespoke post-merge prompt.

## 2. When To Use

Use this workflow after any PR merge and before starting follow-up work.

Use it especially before:

- output-changing chunking tasks;
- roadmap/control-plane transitions;
- high-leverage Revelation, boundary, evaluator, routing, registry, or master-chunker work;
- any task that depends on the previous PR being truly merged.

## 3. Standard Command

```bash
python scripts/agent/post_merge_verify.py --pr <PR_NUMBER> --expected-commit <SHORT_OR_FULL_SHA>
```

With a next-task lookup:

```bash
python scripts/agent/post_merge_verify.py --pr <PR_NUMBER> --expected-commit <SHORT_OR_FULL_SHA> --next-task <TASK_ID>
```

Useful options:

```bash
--skip-pytest
--json
```

## 4. What The Script Checks

The script:

- runs `git fetch origin`;
- checks out `main`;
- fast-forwards from `origin/main`;
- confirms the working tree is clean;
- confirms no `.git/MERGE_HEAD`, `.git/rebase-merge`, or `.git/rebase-apply` state exists;
- reads PR metadata with `gh pr view`;
- confirms the PR is `MERGED`;
- confirms the expected commit is reachable from `HEAD`;
- confirms the merge commit is reachable when GitHub reports one;
- runs canonical scope validation;
- runs canonical corpus QA;
- runs `validate_all.py`;
- runs full pytest unless `--skip-pytest` is passed;
- parses roadmap/task YAML;
- parses roadmap and handoff JSONL ledgers;
- runs `git diff --check`;
- reports next-task presence if `--next-task` is supplied.

Hardened behavior (T340C):

- `--skip-pytest` is always visibly reported: the text report prints
  `pytest: SKIPPED via --skip-pytest` plus a WARNING line, and the JSON report carries
  `"pytest_skipped": true`. A PASS with the skip flag does not cover the test suite.
- Missing tools fail closed: if `git` or `gh` is not available, the affected command is recorded as
  `command not found: git` / `command not found: gh` with return code 127, the verdict is FAIL, and
  the exit code is nonzero. JSON mode still emits valid JSON with the failure detail.
- Next-task detection is exact-first and report-only: it checks
  `.ai/tasks/<TASK_ID>.task.yaml`, `.ai/handoffs/<TASK_ID>/handoff.md`, and the roadmap-state id
  field, then token-bounded prose mentions (so `T340` never matches `T340B`), and reports
  `found`, `ambiguous`, or `not_found`. Detection status never changes the verdict and never
  authorizes implementation.

## 5. What The Script Does Not Do

The script does not:

- edit files;
- create branches;
- create commits;
- push;
- open PRs;
- start the next task;
- infer authorization from a merge;
- approve output-changing work;
- promote reviewed gold;
- promote skill lifecycle status.

It does not start the next task.

## 6. How To Proceed To Next Task

If verification passes, read the next task's authorization surfaces before making changes:

- `.ai/tasks/<TASK_ID>.task.yaml`, if present;
- roadmap docs;
- `ROADMAP_STATE.yaml`;
- `.ai/control/PROJECT_STATUS.md`;
- `.ai/control/current_focus.yaml`, if present;
- the relevant handoff.

Do not start the next task unless the prompt or task file explicitly authorizes it. A merged PR does
not automatically authorize the next implementation and does not by itself authorize implementation.

## 7. Protected-Path Rules

Post-merge verification never authorizes changes to:

- `data/raw/**`;
- `data/canonical/**`;
- generated outputs or chunks;
- chunker/orchestrator behavior;
- evaluator formulas;
- leaderboard or scorecards;
- skill lifecycle registries;
- boundary imports;
- T327G;
- Revelation implementation.

## 8. Examples

### T340 -> T341

```bash
python scripts/agent/post_merge_verify.py --pr 50 --expected-commit b1ca468 --next-task T341
```

If verification passes, read the T341 task/roadmap surfaces. T341 is atlas/audit planning only; it
does not authorize Revelation implementation.

### T337B -> T338

```bash
python scripts/agent/post_merge_verify.py --pr 47 --expected-commit <T337B_COMMIT> --next-task T338
```

If verification passes, T338 may begin only if the task file preserves the exact Psalm target,
reviewed-gold authorization, non-target identity requirements, and route isolation.

### Normal Docs/Control-Plane PR

```bash
python scripts/agent/post_merge_verify.py --pr <PR_NUMBER> --expected-commit <COMMIT>
```

If there is no next task, omit `--next-task` and report the PASS/FAIL result.

## 9. Failure Handling

If verification fails:

- stop;
- do not create a branch;
- do not edit files;
- do not start the next task;
- report the failing command or check;
- wait for owner direction or a repair prompt.

## 10. Why This Prevents Manual Prompt Drift

The repeated post-merge sequence has many small gates: PR state, commit reachability, working-tree
state, validation, next-task authorization, and protected-path reminders. A reusable script and
prompt template reduce the chance that future agents skip a gate, confuse a planning doc with
implementation authorization, or start a high-risk next task too early.

High-risk tasks still require RISK-GATE-001. Output-changing tasks still require reviewed gold and
explicit authorization.
