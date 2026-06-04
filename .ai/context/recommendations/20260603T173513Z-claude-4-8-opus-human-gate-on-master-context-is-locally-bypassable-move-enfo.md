# Master Context Change Proposal

- proposed_by: claude-4.8-opus
- proposed_at: 2026-06-03T17:35:13+00:00
- summary: Human gate on master context is locally bypassable; move enforcement to CODEOWNERS+branch protection
- status: pending_human_review

## Proposed change

## Problem — the human gate on MASTER_CONTEXT.md is locally bypassable (CP-1)

The control plane treats `MASTER_CONTEXT.md` as human-only and enforces it with a SHA256 lock
(`MASTER_CONTEXT.lock.yaml`) checked by `scripts/validate_control_plane.py`. The lock is (re)written
by `scripts/agent/approve_master_context.py`, whose ONLY guard is a name blocklist
(`FORBIDDEN_APPROVERS = {ai, agent, codex, claude, gpt, opus, auto}`).

Verified 2026-06-03 (T304, sandbox — real lock untouched):

- `approve_master_context.py --approved-by claude`  → REJECTED
- `approve_master_context.py --approved-by Lowell`  → WROTE LOCK; control-plane CI green = True
- same for `Human`, `L`, `the-human`

Any AI agent with repo write + shell can therefore (1) edit `MASTER_CONTEXT.md`, (2) run the approve
script with any human-sounding name, (3) regenerate a matching lock, and CI goes green. The
"human-gated" guarantee in MASTER_CONTEXT.md §"Human gates master context" and §"Explicit rejections"
is not actually enforceable by a script that lives inside the agent's own sandbox.

## Why this matters

This is the keystone of the whole governance model. If master context can be silently rewritten and
self-approved, every downstream guarantee (immutability doctrine, canon policy, trust zones) inherits
the same weakness, because they all defer to master context as the authority layer.

## Recommended remediation (enforcement must move to the forge, not a local script)

1. **CODEOWNERS + branch protection** on `.ai/control/MASTER_CONTEXT.md` and
   `.ai/control/MASTER_CONTEXT.lock.yaml`. Require human review on any PR touching them. This is the
   only layer an in-repo agent cannot bypass.
2. **Lock records the approving git commit + verifies authorship in CI.** Store `approved_commit` and
   have CI assert the lock change landed via a CODEOWNER-approved PR (GitHub API / required reviews),
   not merely a non-blocklisted name string.
3. **Signed commits** (optional, stronger): require GPG/sigstore signature from an allowlisted human
   key for any commit that changes master context or its lock.
4. **Treat the local check as tamper-evidence only**, and document it as such in MASTER_CONTEXT.md so
   no one mistakes the blocklist for an access control.

## Secondary finding (CP-2) — fail-open active-task handoff gate

`validate_control_plane.validate_active_task_handoff` uses a multi-line regex that mis-associates a
planned task's id with a later in_progress task's handoff. Verified: with a planned `T002`
(handoff missing) before an in_progress `T304`, the regex returned `('T002', 'T304/handoff.md')` —
silently skipping the missing handoff. A real in_progress task with a missing handoff can pass.
Fix: parse `ROADMAP_STATE.yaml` with PyYAML (optional dep) and iterate tasks structurally.

## Suggested human action

Adopt items 1–2 as the enforcement model and add a sentence to MASTER_CONTEXT.md
§"Engineering principles" clarifying that the lock is tamper-evidence and that true human-gating is
enforced by CODEOWNERS + branch protection on the forge.

## Human action if approved

1. Review this proposal
2. Edit `.ai/control/MASTER_CONTEXT.md` manually
3. Run: `python scripts/agent/approve_master_context.py --approved-by "Your Name" --note "Human gate on master context is locally bypassable; move enforcement to CODEOWNERS+branch protection"`
4. Mark this proposal status: promoted | rejected
