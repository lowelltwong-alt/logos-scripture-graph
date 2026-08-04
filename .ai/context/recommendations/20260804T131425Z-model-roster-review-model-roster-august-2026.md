# Master Context Change Proposal

- proposed_by: model-roster-review
- proposed_at: 2026-08-04T13:14:25+00:00
- summary: model roster August-2026
- status: pending_human_review

## Proposed change

# Model Roster Change Proposal — August 2026

**Review period:** 2026-06-04 → 2026-08-04 (two months; July review was missed; catching up now)  
**Reviewer:** model-roster-review (scheduled automated agent)  
**Approved providers checked:** Anthropic, OpenAI, Google

---

## Summary of findings

### 1. Reasoner profile — PRIMARY pick: update Opus 4.8 → Opus 5

**Evidence:**

- Anthropic released **Claude Opus 5** on July 24, 2026 as the direct successor to Opus 4.8 at the same price tier.
- Independent benchmark data (BenchLM, Codersera, MindStudio — not vendor marketing):
  - SWE-bench Verified: Opus 5 **96.0%** vs Opus 4.8 88.6%
  - SWE-bench Pro: Opus 5 **79.2%** vs Opus 4.8 69.2%
  - Frontier-Bench v0.1 (agentic coding): Opus 5 **43.3%** — more than doubles Opus 4.8's score
  - IMO 2026 mathematical reasoning: Opus 5 perfect 42/42 (gold medal) with no agent harness
  - Anthropic reasoning eval (Max effort): Opus 5 60.7 vs Fable 5 59.9
- Cost: Opus 5 ships at same $5/$25 per million token pricing as Opus 4.8; faster (2.5×) Fast mode available.
- Capability profile fit: architecture audits, ADR authoring, canon/literary judgment, chunking policy — all reasoner-profile work — benefit directly from improved reasoning and agentic coding scores.

**Recommendation:** Change reasoner primary from `Claude Opus 4.8` to `Claude Opus 5`.

---

### 2. Reasoner profile — BACKUP pick: update from o-series to GPT-5-class

**Evidence:**

- OpenAI o3 was retired from ChatGPT August 26, 2026.
- OpenAI announced o-series API shutdown on **October 23, 2026** (deprecation notice June 11, 2026).
- Migration path from OpenAI's own docs: "GPT-5 is better at basically everything the o-series did; API format identical."
- GPT-5.x models (5.6 Sol, 5.6 Luna, 5.6 Terra, 5.4) are current and active on the API.
- Keeping "GPT reasoning-class (o-series)" in the backup slot creates a broken reference after October 23.

**Recommendation:** Change reasoner backup from `GPT reasoning-class (o-series)` to `GPT-5-class reasoning model (e.g. GPT-5.6 Sol)`. Provider allowlist (OpenAI) unchanged.

---

### 3. Executor profile — no change recommended

- "Codex-class / fast coding model" remains accurate; Codex received active updates (Goal mode GA, Appshots) in July 2026.
- Backup "Claude Sonnet-class" is still valid; Sonnet 5 is the current model in that tier.
- No deprecations affecting this slot.

---

### 4. Orchestrator profile — no change recommended

- "Claude Haiku-class / small fast model" remains valid; Haiku 4.5 is the current representative.
- Google's new Gemini 3.5 Flash-Lite (released July 21) is a viable orchestrator-profile option but does not displace the current pick; it could be added as a note in a future review.
- No deprecations affecting this slot.

---

### 5. Provider allowlist — no change recommended

- Anthropic, OpenAI, Google all remain approved for sensitive surfaces.
- No new providers reached a threshold warranting allowlist entry.
- No approved providers have been acquired or materially changed provenance.

---

## Proposed MODEL_ROSTER.md diff (for human to apply)

```diff
-| **reasoner** | Claude Opus 4.8 (weekly architecture auditor) | GPT reasoning-class (o-series) | architecture, ADRs, schema design, canon/literary judgment, weekly chunking-error deep dives |
+| **reasoner** | Claude Opus 5 (weekly architecture auditor) | GPT-5-class reasoning model (e.g. GPT-5.6 Sol) | architecture, ADRs, schema design, canon/literary judgment, weekly chunking-error deep dives |
```

Also update header dates:
```diff
-**Last reviewed:** 2026-06-04
-**Re-evaluate by:** 2026-07-04 (monthly cadence)
+**Last reviewed:** 2026-08-04
+**Re-evaluate by:** 2026-09-04 (monthly cadence)
```

And the multi-agent cadence note:
```diff
-**Multi-agent cadence (T420):** executor-profile Codex runs daily integrator review on prep branches;
-reasoner-profile Claude Opus 4.8 runs weekly architecture and chunking-error audits.
+**Multi-agent cadence (T420):** executor-profile Codex runs daily integrator review on prep branches;
+reasoner-profile Claude Opus 5 runs weekly architecture and chunking-error audits.
```

And add changelog row:
```diff
+| 2026-08-04 | Reasoner → Opus 5 (Opus 4.8 superseded); backup → GPT-5-class (o-series deprecated Oct 2026) | model-roster-review (proposed) / @lowelltwong-alt (policy owner) |
```

---

## Sources consulted

- BenchLM.ai Claude Opus 5 benchmark page (independent)
- MindStudio Claude Opus 5 benchmark analysis (independent)
- Codersera Claude Opus 5 benchmarks explained (independent)
- OpenAI Deprecations page / deprecation notice June 11 2026
- OpenAI Changelog July–August 2026 (Codex, API pricing)
- TechCrunch: Google releases three new Gemini models July 21 2026
- Releasebot Anthropic July 2026 updates

## Human action if approved

1. Review this proposal
2. Edit `.ai/control/MASTER_CONTEXT.md` manually
3. Run: `python scripts/agent/approve_master_context.py --approved-by "Your Name" --note "model roster August-2026"`
4. Mark this proposal status: promoted | rejected
