# Next-Task Handoff Checklist

Use this checklist before beginning a task that follows a merged PR.

- [ ] Prior PR merged and verified.
- [ ] Expected commit reachable from `main`.
- [ ] Working tree clean.
- [ ] No merge/rebase state.
- [ ] Validation passed.
- [ ] Full pytest gate actually ran (verification was not run with `--skip-pytest`).
- [ ] Next task reported `found` (not `ambiguous`/`not_found`) in roadmap/control state.
- [ ] Task scope read.
- [ ] Hard prohibitions copied from task.
- [ ] Protected paths identified.
- [ ] RISK-GATE-001 applied if high leverage.
- [ ] No implementation authorization inferred from planning docs.
- [ ] Owner decisions required listed.

Do not start the next task if verification fails or if the next-task authorization surface is
missing, ambiguous, or blocked.
