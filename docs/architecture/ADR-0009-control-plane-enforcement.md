# ADR-0009: Control-plane enforcement model

## Status

Accepted (2026-06-03) — partial implementation; forge configuration pending human action

## Context

T303 introduced a human-gated `MASTER_CONTEXT.md` protected by a SHA256 lock
(`MASTER_CONTEXT.lock.yaml`), checked by `scripts/validate_control_plane.py` and
written by `scripts/agent/approve_master_context.py`. T304 found the gate is
**locally bypassable** (CP-1): the approve script's only guard is a name blocklist
(`{ai, agent, codex, claude, ...}`), so an agent can edit master context and run
`--approved-by Lowell` to regenerate a matching lock; CI then passes. A script that
runs inside the agent's own sandbox cannot gate that agent.

T304 also found CP-2: the active-task handoff validator used a fragile multi-line
regex that mis-associated a planned task's id with a later in_progress task's
handoff, allowing a genuinely missing handoff to pass (fail-open).

## Decision

1. **The lock is tamper-EVIDENCE, not access control.** Documented as such in
   `approve_master_context.py` and `MASTER_CONTEXT.lock.yaml`.
2. **Real enforcement lives on the forge:** `CODEOWNERS` assigns
   `MASTER_CONTEXT.md` and its lock to a human owner, and the default branch must
   enable branch protection with "Require review from Code Owners". This is the only
   layer an in-repo agent cannot bypass. (ACTION REQUIRED: set a real handle in
   `.github/CODEOWNERS` and enable branch protection.)
3. **The lock records `approved_commit`** so CI can later verify the lock change
   landed via a reviewed commit, not merely a name string.
4. **CP-2 fixed:** `validate_active_task_handoff` now parses tasks structurally
   (PyYAML when available, deterministic block scan otherwise) and fails closed.

## Consequences

- Until branch protection is enabled, treat master context as trusted-by-convention.
- Agents must never run `approve_master_context.py` (added to AGENT_ROUTING_GUIDE
  "Never" list); it is a human command.
- Future hardening (optional): require signed commits from an allowlisted human key
  for any change to master context or its lock.

## Status of follow-ups

- [x] CP-2 structural parser
- [x] approved_commit in lock
- [x] CODEOWNERS entries for master + lock
- [ ] Branch protection enabled on default branch (human, forge-side)
- [ ] Optional: signed-commit verification in CI
