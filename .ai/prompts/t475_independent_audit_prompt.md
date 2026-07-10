# T475 Independent Shadow-Delta Audit Prompt

You are the independent checker for T475. The task-local roster binds this role
to Claude Opus 4.8, outside the GPT-5.6 Sol/Terra/Luna implementation hierarchy.
Audit only the frozen evidence bundle. Do not implement fixes, mutate evidence,
regenerate data, authorize committed data replacement, promote reviewed gold,
or produce chunk output.

## Read First

1. AI_FRONT_DOOR.md
2. .ai/control/MASTER_CONTEXT.md (read only)
3. .ai/tasks/T475.task.yaml
4. .ai/control/t475_usfm_shadow_delta_gate.yaml
5. .ai/control/t474_usfm_marker_anchor_contract.yaml
6. .ai/handoffs/T475/handoff.md
7. every file named by frozen_evidence_manifest.json

## Audit Questions

1. Did Sol, Terra, and Luna stay inside their task-local authority boundaries?
2. Could correlated GPT-5.6 assumptions have omitted outputs, accepted a faulty
   stable key, hidden a mismatch, or misclassified a pass?
3. Are baseline/candidate refs, raw/config inputs, commands, output families,
   and environment pinned?
4. Are three runs deterministic, and do aggregate counts reconcile exactly to
   machine-readable ledgers?
5. Is Scripture text absent from reports while hashes and safe metadata retain
   enough traceability to reproduce every delta?
6. Did any ignored output become committed data, reviewed gold, chunk output,
   route/evaluator behavior, graph/retrieval/vector truth, preferred reading,
   canon scope, or theology authority?
7. Does the balanced-value gate have correctness/parity plus at least one
   measurable performance, deployment, operability, failure-isolation, or
   compute-cost gain? Speed alone is never sufficient.

## Return

- PASS, HOLD_WITH_FINDINGS, or ESCALATE_OWNER
- P0/P1/P2 findings with exact evidence references
- parity verdict
- authority-leakage verdict
- balanced-value verdict
- exact required fixes

The verdict is evidence for T476. It cannot authorize T477 regeneration or any
reviewed-gold/chunk-output change.
