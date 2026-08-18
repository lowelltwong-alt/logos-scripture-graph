# OWNER CHECKPOINT — first commit/push of the M8_fable lane (2026-08-18)

Authorization: Lowell Wong, in chat, 2026-08-18
(`lowell_chat_2026-08-18_commit_push_authorization`) — scope confirmed as
"worktree + durable SP set". This is a durability checkpoint, not a
publication or integration event.

## What this commit contains
- The complete M8_fable candidate campaign state through 19/66 books
  (Gen→Job per the pre-existing worktree files; Ps closed 2026-08-18 with
  492 sha-verified rows, sidecar mirrors incl. the conflict-D
  hold-for-convergence at M8-Ps-433, receipts, whole-map at 3039 rows).
- The Prov cycle through the Phase-1 boundary: byte-proven identity offset
  map, staged toolkit (smoke-tested), book_strategy/Prov.md carrying the
  2026-08-18 owner gate rulings (hybrid atomic default granularity, 8-value
  unit_type vocabulary, r3-scaled wave plan). No writer has launched yet.
- The continuation receipt (cold session, owner checkpoint applied) and the
  four shared control files in the registered allowlist.
- `sp_durable/` — the campaign scratchpad's durable set (Ps freeze +
  deliverables; complete Prov staging), provenance in its README.

## PR-lifecycle record (ai_pr_lifecycle_policy.v1 draft-exit fields)
- branch_name: `scratch/t423-m8-fable`
- task_id: T423 / M8_fable lane
- pr_url_or_reason_no_pr: NO PR — long-running candidate research lane;
  candidate-only, non-authorizing output; PR deferred until marathon
  completion / T521 convergence, per owner.
- validation_status: campaign validators GREEN at Ps close (chunk-map +
  quality-protocol via mark-complete; Prov toolkit smoke test PASS);
  full repo `validate_all`/pytest NOT run for this checkpoint.
- merge_permission_status: NOT granted; merge/comparison remain
  non-authorized.
- next_action_state: hold_with_findings_owner_visible — next action is the
  Prov writer wave per the gated strategy.
- owner_or_integrator_alert: owner authorized and was alerted live in chat.

## Governance machinery supersession (recorded exception)
The registry resume gate pinned pre-resume HEAD
9186bdfeeb74e2d2f6baeb2b9d11e7cb747ed5be and a 161-artifact Temp snapshot.
This commit MOVES HEAD, so `validate_workspace_policy.ps1`'s m8_resume_probe
will read stale/fail from now on. By owner authorization this git commit
(and its successors on `scratch/t423-m8-fable`, pushed to origin) SUPERSEDES
the Temp snapshot as the durable resume basis. Future sessions: treat the
failed m8 probe as this recorded, owner-approved exception — resume from the
committed state plus `sp_durable/` + `book_strategy/Prov.md` +
`sp_durable/Prov/freeze/CYCLE_STATE.md`; all other workspace-policy
protections stay in force. Commit, push, merge, cleanup, and comparison
authority remain NOT granted beyond this exact checkpoint action (and
equivalent owner-authorized checkpoint pushes at future phase boundaries).
