# Task Handoff — T310: Chunking orchestrator + skill registry (ADR-0011)

## Task

- task_id: T310
- title: Chunking orchestrator + skill registry (ADR-0011) — phased build
- phase: phase_3
- status: in_progress

## Agent

- agent_name: claude-opus-4.8
- mode: plan
- stage: start
- updated_at: 2026-06-05T14:38:09+00:00
- handoff_id: 4340e7c2d627f688

---

## What this is

Turn the single genre-dispatch chunker into a **form-routed orchestrator + skill registry**: detect
each passage's literary form (from real USFM markers), route it to the best-fit chunking **skill**,
expose every skill via a committed **TOC + knowledge graph**, **alert when no skill fits**, and run
the existing multi-agent bake-off to author the missing skill. Full design + rationale: **ADR-0011**.
Decisions were locked with the owner (D1–D8 + B+); the four source designs and their reconciliation
live in `.ai/context/recommendations/` (`{CLAUDE,CODEX,CURSOR,COMPOSER}-…` + `ADJUDICATION-…`).

## Locked decisions (build to these — do not relitigate)

1. Route on **marker-evidenced structural form**; `book_genres.yaml` is a prior. Overlays
   (`\wj`/`\fqa`/`\x`/`\qs`/`\d`) are **metadata**, not skills.
2. Form detection = **deterministic marker rules + LLM adjudicator**; the LLM writes a **separate
   candidate shadow FormAssignment** (never overwrites deterministic); human picks. All candidate.
3. Register the **full ~40-form taxonomy**, each `active` (skill+gold) or `declared-gap`. No form is
   `active` without a skill **and** a gold case.
4. Skills are versioned packages with **parametric variants** (`skill_id`+`variant_id`).
5. **8-state lifecycle** (draft→candidate→active→preferred→deprecated→superseded→retired, +quarantined),
   human-gated promotion.
6. Layout: code in `pipelines/chunking/`; policy YAML in `config/chunking/`; **committed**
   index/graph/`contracts.lock` in `registry/chunking/`; big outputs + ledgers ephemeral.
7. Routing unit = **section windows**; verse units stay atomic.
8. Selection = best gold-scored eligible non-stale skill; **human override** via
   `config/chunking/skill_overrides.yaml`.
9. Gap loop → candidate gap record → bake-off (`evaluate_chunks.py`+`leaderboard.py`) → human picks
   best or **fuses** (human code merge, `combines_with`). Nothing self-promotes.
10. Per-form gold under `eval/chunking_gold/per_form/`, **seeded incrementally** from Ps 23 / Rom 7-8 / John 1.
11. Staleness recorded now (registry SHA in route ledger); **fail-closed `contracts.lock` gate deferred**.
12. Quality weights in `config/chunking/skill_quality_weights.yaml`; add `SKILL_QUALITY_DOCTRINE.md`
    + an `ORCHESTRATOR_BOUNDARY` (knowledge/execution/human).
13. Orchestrator is a **thin, fail-closed, deterministic router in the knowledge plane** — not an agent runtime.

## Licensing (enforce)

`pipelines/chunking/`, `config/chunking/`, and `registry/chunking/` are **proprietary, All Rights
Reserved** under `pipelines/chunking/LICENSE` (carved out of root MIT; see `config/chunking/NOTICE`).
When you create `registry/chunking/`, drop a `NOTICE` there pointing to `pipelines/chunking/LICENSE`.
Copyright (c) 2026 Lowell Wong.

## Build plan (each increment gated at composite >= 88.5; byte-identical until extraction proven)

- **Increment 0 — registry stub.** `config/chunking/form_registry.yaml` (full ~40-form map, `status:
  active|declared-gap`), `config/chunking/skill_lifecycle_policy.yaml`, `config/chunking/skill_quality_weights.yaml`,
  `config/chunking/skill_overrides.yaml` (empty), committed `registry/chunking/{skill-toc.json,
  skill-graph-index.json,approved-skills.json}` + `NOTICE`, and a `SKILL_METADATA.json` wrapping the
  current monolith as `monolith-pass2-v1`. No pipeline change. Gates green.
- **Increment 1 — read-only form detector.** `pipelines/chunking/detect_form.py` emits candidate
  `FormAssignment` JSONL (deterministic rules; LLM-adjudicator shadow contract defined, path behind a
  flag, default off). Chunker output unchanged. Validate coverage/confidence.
- **Increment 2 — orchestrator shim.** `pipelines/chunking/orchestrator.py` reproduces current Pass-2
  output **byte-identically** via a single skill pin; emits the route ledger (with registry SHA).
- **Increment 3 — extract psalm skill** (`psalm-whole-then-stanza`); prose stays in monolith; add its
  gold case. **Increment 4 — extract prose + wisdom skills**, remove inline branches, add gold.
- **Increment 5 — gap factory + bake-off harness** wired to candidate gap records + handoff alerts.

Do NOT start LLM-first detection, sharding, early-church forms, or a graph UI.

## HARD RULES

- Hard gates every increment: 0 USFM leaks, 0 book crossings, 100% prose sentence integrity, Ps 23 =
  one whole-psalm chunk; never split mid-sentence/colon/superscription.
- Design against the REAL markers in `.ai/control/RAW_SOURCE_INVENTORY.md`; `validate_raw_coverage.py`
  must stay green. Re-read it before any detector/chunker change.
- Chunks + form assignments are **candidate/derived** — never canonical; human promotes.
- Do not write `data/raw` or `data/canonical`. Do not edit `MASTER_CONTEXT.md` / its lock.
- Run `python scripts/validate_all.py && python -m pytest -q` before stopping; regenerate DATA_MAP if
  data/schemas/pipelines changed.

## Files read

- AI_FRONT_DOOR.md; .ai/control/{MASTER_CONTEXT.md,PROJECT_STATUS.md}; pipelines/chunking/chunker.py;
  config/chunking/{book_genres.yaml,chunking_policy.yaml}; the four design proposals + ADJUDICATION;
  00_LawFirm_OS (skills-registry, orchestrator, semantic-substrate registries).

## Files changed (this planning task)

- docs/architecture/ADR-0011-chunking-orchestrator-skill-registry.md (new)
- .ai/tasks/T310.task.yaml (new); .ai/handoffs/T310/handoff.md (this)
- .ai/context/recommendations/{CLAUDE-,ADJUDICATION-}orchestrator-skill-registry*.md (Claude submission + diff)
- pipelines/chunking/LICENSE (new, proprietary); LICENSE (root carve-out); config/chunking/NOTICE (new)
- ROADMAP_STATE.yaml; .ai/control/PROJECT_STATUS.md; .ai/control/roadmap_events.jsonl

## Decisions made

- See "Locked decisions" above (D1–D8 + B+ + gold + license), all owner-approved 2026-06-05.

## Validation run

- command: python scripts/validate_all.py && python -m pytest -q
- result: green (validate_all all gates; 30 pytest) at planning checkpoint
- failures: none

## Known risks

- Per-form gold curation is the critical path (human review); kept incremental.
- LLM adjudicator adds non-determinism — confined to candidate shadow records, default-off until Increment 1+.
- Extraction refactor risks drift — mitigated by the byte-identical shim gate (Increment 2) before any extraction.

## Open questions

- Exact composite-metric deltas a new skill must clear to supersede an incumbent (propose in Increment 3).
- Whether `registry/chunking/` freshness gets its own freshness gate (like DATA_MAP) at Increment 0 or 2.

## Next agent instruction

Start **Increment 0** (registry stub) only. Create `config/chunking/form_registry.yaml` (full ~40-form
map with `status: active|declared-gap`, grounded in `RAW_SOURCE_INVENTORY.md` markers), the lifecycle +
quality-weights + empty overrides YAML, the committed `registry/chunking/` stub + `NOTICE`, and a
`SKILL_METADATA.json` wrapping the current monolith as `monolith-pass2-v1`. Change NO pipeline behavior.
Run `validate_all` + pytest; confirm leaderboard composite is still 88.5. Open a PR "T310 Increment 0:
chunking registry stub"; do not merge, do not promote. Then update this handoff.
