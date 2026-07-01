# Model Roster — current models per capability profile (DATED; review monthly)

<!--
  This is the ONE file you update when models change. The routing logic lives in
  config/agents/model_routing.yaml and references profiles, not names.
  Roster changes: agent may PROPOSE (propose_master_context_change.py or a
  recommendation); a human approves. Profiles + security tiers are human-gated.
-->

**Last reviewed:** 2026-06-04
**Re-evaluate by:** 2026-07-04 (monthly cadence)
**Routing policy:** `config/agents/model_routing.yaml`

> Model version names move fast and are not all verifiable from inside the repo.
> The profile→model picks below MUST be confirmed against vendor docs at each
> monthly review. Treat any name here as "best known as of Last reviewed".

---

## Profile → current pick

| Profile | Primary | Backup | Notes |
|---------|---------|--------|-------|
| **reasoner** | Claude Opus 4.8 (weekly architecture auditor) | GPT reasoning-class (o-series) | architecture, ADRs, schema design, canon/literary judgment, weekly chunking-error deep dives |
| **executor** | Codex-class / fast coding model (daily integrator) | Claude Sonnet-class | bounded impl, tests, audits, daily prep-branch integration |
| **orchestrator** | Claude Haiku-class / small fast model | any cheap model | triage, summarization, doc chores |

Domain reviewers (human or reasoner-profile + human): biblical-literature, Hebrew,
Greek reviewers per `config/agents/agent_roles.yaml` for canon / chunking policy / gold sets.

**Multi-agent cadence (T420):** executor-profile Codex runs daily integrator review on prep branches;
reasoner-profile Claude Opus 4.8 runs weekly architecture and chunking-error audits. See
`.ai/control/multi_agent_review_cadence.yaml`.

---

## Execution surfaces (not models — where contributors drive models)

| Surface | Best for | Notes |
|---------|----------|-------|
| **Cursor (Pro, $20/mo)** | executor-profile work, human-in-the-loop edits | metered access to frontier models; great for T306-style bounded tasks; confirm which models the plan currently exposes at review time |
| Claude Code / CLI agents | reasoner + executor; multi-step governed tasks | this repo's primary agent surface |
| Local runners (Ollama, etc.) | offline executor/orchestrator on open-weight models | output is `candidate` trust zone until human-promoted; see allowlist |

---

## Provider allowlist (tiered policy — see model_routing.yaml security_policy)

Policy owner: @lowelltwong-alt. This expresses a **supply-chain risk posture**, not a
quality ranking. Edit freely; it is your call. Gate-enforcement (CI + CODEOWNERS +
candidate trust zone) applies to **every** provider regardless of tier.

### Approved for SENSITIVE surfaces
(pipelines, scripts, CI, schemas, config, data/raw, .ai/control — also require human CODEOWNER review)

- Anthropic (Claude)
- OpenAI (GPT / o-series / Codex)
- Google (Gemini)

### Approved for GENERAL surfaces only
(docs, handoffs, notes — still CI + review; NOT for sensitive surfaces)

- Mistral
- Meta Llama (local/open-weight) — and other open-weight models run locally
- Cohere

### NOT approved (per current policy — contributor's stated supply-chain caution)
(do not use to author code that lands on sensitive surfaces)

- China-based providers, e.g. DeepSeek, Qwen/Alibaba, Zhipu/GLM, 01.AI/Yi
  - Rationale recorded by policy owner: code-injection / supply-chain caution.
  - This is a provenance policy, not a capability claim. It reduces one vector
    only; it never replaces CI + human review.

> Honest caveat: an "approved" model can still emit wrong or prompt-injected code.
> The allowlist is defense-in-depth, layered ON TOP of mandatory gate-enforcement.

---

## Monthly capability-review checklist

Run on/after the **Re-evaluate by** date (human or web-enabled agent):

1. **Scan releases** since Last reviewed for each approved provider (new frontier /
   coding / cheap models, deprecations, pricing changes).
2. **Re-rank profiles**: does a new model better fill reasoner / executor /
   orchestrator? Check independent coding + reasoning evals, not vendor marketing.
3. **Bench on a fixed repo task** (apples-to-apples): e.g. run the T306 mechanical
   fixes or a chunker change with each candidate; compare correctness + speed + cost.
4. **Update this roster** (profile picks, surfaces, allowlist) and bump both dates.
5. **Propose, don't self-approve** if AI-driven:
   `python scripts/agent/propose_master_context_change.py --agent <name> --summary "model roster <month>" --body-file <notes>`
   then a human reviews + merges (CODEOWNERS gate).
6. **Log it**: append a `model_roster_reviewed` event to
   `.ai/control/roadmap_events.jsonl`.

---

## Changelog

| Date | Change | By |
|------|--------|----|
| 2026-06-04 | Initial roster + tiered provider allowlist; monthly cadence | claude-opus-4.8 (proposed) / @lowelltwong-alt (policy owner) |
