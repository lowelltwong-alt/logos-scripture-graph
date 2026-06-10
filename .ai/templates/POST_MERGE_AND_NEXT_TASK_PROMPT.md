# Post-Merge Verification And Next-Task Prompt Template

```text
You are Codex in `logos-scripture-graph`.

TASK:
Run standard post-merge verification for PR #{PR_NUMBER} / {TASK_ID}. If and only if verification
passes, proceed to {NEXT_TASK_ID} using the task file / roadmap state.

First run:
python scripts/agent/post_merge_verify.py --pr {PR_NUMBER} --expected-commit {EXPECTED_COMMIT} --next-task {NEXT_TASK_ID}

If verification fails:
- stop;
- do not create a branch;
- do not edit files;
- report failure.

Notes:
- Missing-tool failures (`command not found: git` / `command not found: gh`) are FAIL, not retries.
- Do not pass --skip-pytest for gated next-task work; if it was passed, the report says
  `pytest: SKIPPED via --skip-pytest` and the PASS does not cover the test suite.
- The next-task field reports `found`, `ambiguous`, or `not_found`; it is report-only and never
  authorizes implementation.

If verification passes:
- read `.ai/tasks/{NEXT_TASK_ID}.task.yaml` if it exists;
- read the relevant roadmap doc;
- create or switch to branch `{NEXT_BRANCH}` only if the next task authorizes work;
- follow `{NEXT_TASK_TITLE}` scope and prohibitions;
- do not infer authorization beyond the task file, roadmap state, handoff, and owner decision surfaces.

Placeholders:
- {PR_NUMBER}
- {TASK_ID}
- {EXPECTED_COMMIT}
- {NEXT_TASK_ID}
- {NEXT_BRANCH}
- {NEXT_TASK_TITLE}
```
