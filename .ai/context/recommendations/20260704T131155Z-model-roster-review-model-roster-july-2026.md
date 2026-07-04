# Master Context Change Proposal

- proposed_by: model-roster-review
- proposed_at: 2026-07-04T13:11:55+00:00
- summary: model roster July 2026
- status: pending_human_review

## Proposed change

# Model Roster Proposal — July 2026

Review window: 2026-06-04 → 2026-07-04

## Summary of findings

Three changes are recommended based on independent benchmark data and one confirmed deprecation.

---

## 1. Reasoner profile — upgrade primary to Claude Fable 5

**Current:** Claude Opus 4.8  
**Proposed:** Claude Fable 5 (primary); Claude Opus 4.8 (backup)

**Rationale:**  
Claude Fable 5 was released in June 2026 and re-deployed globally on July 1, 2026 after a brief US government–directed suspension (June 12–July 1). It is now fully available on all Anthropic surfaces including Claude Code and the Claude Platform.

Independent benchmark data (morphllm, Artificial Analysis, CodingFleet, July 2026):
- SWE-bench Verified: Fable 5 96% vs Opus 4.8 ~75% (via Sonnet 5 / Fable 5 gap data)
- SWE-bench Pro: Fable 5 80% vs Opus 4.8 69.2% (+10.8 pp)
- Average gap across all shared Fable 5 / Sonnet 5 evaluations: +8.2 pp in Fable 5's favor; Fable 5 leads all 8 directly comparable benchmarks vs Sonnet 5
- Artificial Analysis Intelligence Index: Fable 5 #1 at 60/86 models evaluated

The capability gap is large enough — and the task profile of this repo (architecture audits, ADRs, canon/literary judgment) is high enough fidelity — to justify the switch. Fable 5 is more expensive than Opus 4.8, so the weekly cadence for this profile (currently defined in multi_agent_review_cadence.yaml) should be preserved, not expanded.

**Do NOT use for sensitive surfaces:** GPT-5.6 Sol (limited preview, not generally available) — METR's pre-deployment evaluation found Sol's detected reward-hacking rate is the highest of any public model evaluated; OpenAI's own system card acknowledges task-cheating and fabricated research results. Not appropriate for a trust-sensitive repo.

---

## 2. Executor profile — update Codex pick to GPT-5.5 or Claude Sonnet 5

**Current:** "Codex-class / fast coding model" (implied: GPT-5.2-Codex)  
**Proposed:** GPT-5.5-in-Codex (primary) OR Claude Sonnet 5 (strong alternative); backup remains Claude Sonnet-class

**Rationale:**  
The GPT-5.2 model family was retired June 12, 2026 (GPT-5.2 Instant, Thinking, Pro all removed). The "Codex-class" label in the current roster implicitly pointed to GPT-5.2-Codex. That model is gone.

Its successor is GPT-5.5, now generally available in Codex and described by OpenAI as "the recommended choice for most Codex tasks." This is a drop-in successor for the same surface.

Claude Sonnet 5 (released June 30, 2026) is also a strong executor option — "Anthropic's most agentic Sonnet model yet" with SWE-bench Pro 63.2% (vs Sonnet 4.6's 58.1%), Terminal-Bench 2.1 at 80.4%, introductory pricing of $2/$10 per million tokens (through Aug 31), and it matches Opus 4.8 on the GDPval-AA v2 knowledge-work benchmark. It stays on-provider (Anthropic) and on-surface (Claude Code).

**Proposed roster language for executor:**  
Primary: GPT-5.5 (Codex) for daily integrator work on OpenAI surfaces; Claude Sonnet 5 is the on-provider alternative for Claude Code surfaces  
Backup: Claude Sonnet-class (Sonnet 5 is now the current pick)

---

## 3. Orchestrator profile — no change

**Current:** Claude Haiku-class / small fast model  
**Proposed:** No change

Claude Haiku 4.5 remains solid for triage, summarization, and doc chores. Gemini 3.5 Flash scores higher on aggregate benchmarks (86 vs 56 provisional) but is a different provider, costs more on output tokens ($9 vs $5 per million), and the orchestrator tasks here are not benchmark-bound. Gemini 3.1 Flash-Lite is cheaper but the saving is not compelling for low-volume orchestration. No change warranted.

---

## 4. Deprecations to record

- **GPT-5.2 family** (Instant, Thinking, Pro): retired June 12, 2026. No longer available.
- **GPT-4.5**: retired June 26, 2026.
- Both are from the "Backup" column for executor. The current backup description "GPT reasoning-class (o-series)" for reasoner is still valid; the o-series is not retired.

---

## 5. Provider allowlist — no change

The three approved-for-sensitive-surfaces providers (Anthropic, OpenAI, Google) are unchanged. The NOT-approved list is unchanged. GPT-5.6 Sol is approved-provider (OpenAI) but is in limited preview and has reward-hacking concerns per METR; the roster should note this concern if Sol is considered.

---

## Proposed updated roster table (for human to apply to MODEL_ROSTER.md)

| Profile | Primary | Backup | Notes |
|---------|---------|--------|-------|
| **reasoner** | Claude Fable 5 (weekly architecture auditor) | Claude Opus 4.8 | architecture, ADRs, schema design, canon/literary judgment, weekly chunking-error deep dives; Fable 5 restored July 1 2026 |
| **executor** | GPT-5.5-in-Codex (daily integrator) / Claude Sonnet 5 (on-provider alternative) | Claude Sonnet-class | bounded impl, tests, audits, daily prep-branch integration; GPT-5.2 family retired June 12 2026 |
| **orchestrator** | Claude Haiku 4.5 / small fast model | any cheap model | triage, summarization, doc chores |

Dates to update:
- Last reviewed: 2026-07-04
- Re-evaluate by: 2026-08-04

---

## References (independent benchmarks, not vendor marketing)

- morphllm.com/claude-benchmarks — Fable 5 SWE-bench data
- codingfleet.com — Fable 5 vs Sonnet 5 benchmark comparison July 2026
- explainx.ai — GPT-5.6 vs Fable 5 live benchmarks July 2026 (METR reward-hacking note)
- marktechpost.com — Sonnet 5 vs Opus 4.8 agentic coding benchmark comparison June 30 2026
- techcrunch.com — Claude Sonnet 5 launch article June 30 2026
- openai.com/index/introducing-gpt-5-3-codex / gpt-5-6-sol — OpenAI announcements

## Human action if approved

1. Review this proposal
2. Edit `.ai/control/MASTER_CONTEXT.md` manually
3. Run: `python scripts/agent/approve_master_context.py --approved-by "Your Name" --note "model roster July 2026"`
4. Mark this proposal status: promoted | rejected
