# Task Handoff — T307: Model routing policy (capability-based) + roster + cadence

## Task

- task_id: T307
- title: Capability-based model routing, dated roster, tiered provider policy, monthly review
- phase: phase_3
- status: complete

## Agent

- agent_name: claude-opus-4.8
- mode: plan
- stage: final
- updated_at: 2026-06-04T13:44:29+00:00
- handoff_id: fd366c63ccaa5131

## Files read

- config/agents/agent_roles.yaml, AGENT_ROUTING_GUIDE.md, MASTER_CONTEXT.md, .github/CODEOWNERS

## Files changed

- `config/agents/model_routing.yaml` (new) — capability profiles + task→profile routing + tiered security policy
- `.ai/control/MODEL_ROSTER.md` (new) — dated profile→model picks, execution surfaces (incl. Cursor), provider allowlist, monthly review checklist, changelog
- `.ai/handoffs/AGENT_ROUTING_GUIDE.md` — added "Step 2.5 — Use the right model"
- `.github/CODEOWNERS` — added config/agents/ + MODEL_ROSTER.md (human-gated)
- ROADMAP_STATE.yaml, PROJECT_STATUS.md, current_focus.yaml, roadmap_events.jsonl

## Decisions made

- **Route by capability profile, not model name** (reasoner / executor / orchestrator). Versions
  churn; profiles don't. The dated name→profile mapping is isolated in MODEL_ROSTER.md so model
  changes touch ONE file.
- **Tiered security policy** (user decision): approved-provider models required for sensitive
  surfaces (pipelines/scripts/CI/schemas/config/data-raw/.ai-control) + human CODEOWNER review;
  general surfaces (docs/handoffs) open. Gate-enforcement (CI + candidate trust zone + CODEOWNERS)
  is mandatory for ALL models regardless of origin.
- **Provider allowlist** reflects the policy owner's supply-chain caution (China-based providers not
  approved for sensitive surfaces). Framed as provenance policy, not a capability claim; editable.
- **Monthly review cadence** (user decision): re-evaluate by date + checklist in MODEL_ROSTER.md;
  AI proposes roster changes via propose_master_context_change.py, human approves.
- **Cursor ($20 Pro)** recorded as an execution *surface* for executor-profile work, not a model.

## Validation run

- command: `python scripts/validate_all.py`
- result: passed (5 gates)
- command: `python -m pytest -q`
- result: passed (11 tests)
- failures: none

## Known risks

- A static roster cannot auto-track the frontier; the monthly checklist needs a human or
  web-enabled agent to actually scan releases + bench candidates.
- Provider allowlist reduces one vector only; it never replaces CI + human review (an approved
  model can still be wrong or prompt-injected).
- Scheduled monthly reminder is set up via the scheduling system; if that infra is unavailable,
  the Re-evaluate-by date in MODEL_ROSTER.md is the fallback trigger.

## Open questions

- None blocking. Policy owner may tune the allowlist tiers anytime (CODEOWNERS-gated edit).

## Next agent instruction

- Monthly: on/after the MODEL_ROSTER "Re-evaluate by" date, run the review checklist, update the
  roster, propose via `propose_master_context_change.py`, human approves, log a
  `model_roster_reviewed` event.
- Any contributor/agent: read `config/agents/model_routing.yaml` + `MODEL_ROSTER.md` at task start
  (now referenced from AGENT_ROUTING_GUIDE Step 2.5). Executor-profile models escalate design
  decisions to a reasoner-profile model instead of guessing.
