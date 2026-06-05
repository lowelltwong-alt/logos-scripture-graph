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

## Build plan (corrected baseline >= 93.0 for output-changing work; byte-identical until extraction proven)

T311 corrected the evaluator after the early increments. Historical entries below that say 88.5 are
old-evaluator provenance for the same D / Claude pass2 output. T310 3b and later output-changing
work must plan against the corrected 93.0 baseline and cite per-form gold evidence before claiming
improvement.

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

## Increment 0 — COMPLETED (2026-06-05)

Registry stub landed, marker-grounded against `RAW_SOURCE_INVENTORY.md` (note: `\s1`/`\ms1` headings
are RARE in WEB Classic — 5 each — so routing leans on `\p`/`\q*`/`\b`/chapter, not headings). Files:
- `config/chunking/form_registry.yaml` — 33 forms (21 biblical w/ `interim_skill: monolith-pass2-v1`
  + 12 early-church Tier-C declared-gaps) + 7 overlays. `status: declared-gap` everywhere (no dedicated
  skill+gold yet at Inc 0).
- `config/chunking/skill_lifecycle_policy.yaml` (8 states), `skill_quality_weights.yaml` (converged),
  `skill_overrides.yaml` (empty).
- `registry/chunking/{skill-toc.json,skill-graph-index.json,approved-skills.json,NOTICE}` (committed,
  proprietary).
- `pipelines/chunking/skills/approved/monolith-pass2-v1/{SKILL.md,SKILL_METADATA.json}` — wraps current
  Pass-2 (88.5) as the interim fallback default; NO behavior change.

Validation: `validate_all` all gates green; pytest 32 passed; leaderboard still **88.5** (unchanged).
Registry JSON/YAML all parse. The registry files are hand-authored stubs — a generator (from skill
metadata + form_registry) replaces them in a later increment.

## Increment 1 — COMPLETED (2026-06-05, Composer 2.5)

Read-only deterministic form detector landed. Emits **candidate-zone `ClassificationAssignment`**
records (`axis: textual_form`, `assertion_mode: inferred_rule`, `trust_zone: candidate`) — no new
schema; reuses `schemas/classification_assignment.schema.json`. No LLM path. No routing. No chunker
behavior change.

Files:
- `pipelines/chunking/detect_form.py` — marker-first detector; imports `build_units()` read-only from chunker
- `scripts/chunking/emit_form_assignments.py` — CLI → `data/candidate/chunking/form_assignments/`
- `tests/test_detect_form.py` + `tests/fixtures/chunking/form_detect_units.jsonl`
- `.gitignore` — ignores `data/candidate/chunking/`
- `scripts/generate_data_map.py` + regenerated `.ai/control/DATA_MAP.md`

Validation: `validate_all` all gates green; pytest **40 passed** (+8 new); leaderboard still **88.5**
(claude-opus-4.8 pass2 / D). `chunker.py`, `evaluate_chunks.py`, `leaderboard.py` **not edited**.

## Increment 2 - COMPLETED (2026-06-05, Codex)

Byte-identical orchestrator shim landed. `pipelines/chunking/orchestrator.py` delegates to the existing
Pass-2 chunker functions (`read_policy_version`, `load_budgets`, `load_genres`, `index_by_osis`,
`build_units`, `chunk_corpus`) and writes chunks/context with the same JSONL serialization as
`chunker.py`. It emits a separate JSONL route ledger only when `--route-ledger` is passed.

Files:
- `pipelines/chunking/orchestrator.py` - monolith Pass-2 shim pinned to `monolith-pass2-v1`
- `tests/test_chunking_orchestrator.py` - smoke, context, real-corpus, ledger, no-routing, and no-mutation tests
- `scripts/generate_data_map.py` + regenerated `.ai/control/DATA_MAP.md`
- `.ai/handoffs/T310/handoff.md`

Route ledger:
- `type: ChunkingRouteLedger`
- `route_mode: monolith_pass2`
- `skill_id: monolith-pass2-v1`
- `form_based_routing_enabled: false`
- `detect_form_consumed: false`
- includes input/output/context hashes and `registry_surface_sha`

Byte-identity proof against current full corpus:
- chunks direct/orchestrator SHA-256:
  `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`
- context direct/orchestrator SHA-256:
  `f3128daba9d9be91aa02e8e53dc6baba9bd9fb3b89ae3eeff031b96e6d2c76ab`
- raw bytes matched for both streams

Validation:
- `python -m pytest -q tests/test_chunking_orchestrator.py` -> 7 passed
- `python scripts/validate_all.py` -> all validation gates passed
- `python -m pytest -q` -> 48 passed
- `python pipelines/chunking/leaderboard.py` -> D / claude-opus-4.8 pass2 still rank 1 at 88.5

Protected files not edited: `chunker.py`, `evaluate_chunks.py`, `leaderboard.py`, `detect_form.py`,
`schemas/*`, `registry/chunking/*`, `config/chunking/*`, `data/raw/*`, `data/canonical/*`.

## Increment 3a - COMPLETED (2026-06-05, Codex)

Behavior-preserving Psalm skill extraction seam landed. This is **not** a scoring improvement
increment. The candidate `psalm-whole-then-stanza-v1` skill routes literal Book of Psalms (`book == Ps`)
only, delegates to existing monolith Psalm behavior, and preserves chunk/context bytes exactly.

Files:
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/{SKILL.md,SKILL_METADATA.json,algorithm.py}`
- `pipelines/chunking/orchestrator.py` - literal-Ps route seam + per-book route ledger records
- `registry/chunking/{skill-toc.json,skill-graph-index.json}` - candidate metadata only; `approved-skills.json` unchanged
- `tests/test_chunking_orchestrator.py` - byte identity, route ledger, fallback, no-metadata-leak tests
- `.ai/handoffs/T310/handoff.md`

Route behavior:
- literal `Ps` -> `psalm-whole-then-stanza-v1`
- `Song`, `Lam`, `PrMan`, `Ps151`, and all other non-Ps books -> `monolith-pass2-v1`
- `detect_form_consumed: false`
- `form_based_routing_enabled: false`
- route facts live only in route ledger; chunk/context records remain unchanged

Byte-identity proof against current full corpus:
- chunks direct/routed SHA-256:
  `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`
- context direct/routed SHA-256:
  `f3128daba9d9be91aa02e8e53dc6baba9bd9fb3b89ae3eeff031b96e6d2c76ab`
- raw bytes matched for both streams

Validation:
- `python -m pytest -q tests/test_chunking_orchestrator.py` -> 8 passed
- `python scripts/validate_all.py` -> all validation gates passed
- `python -m pytest -q` -> 49 passed
- `python pipelines/chunking/leaderboard.py` -> D / claude-opus-4.8 pass2 still rank 1 at 88.5

Important evaluator note: do **not** use `psalms_fragmented` or composite movement as the success signal
for this increment. `evaluate_chunks.py` currently groups every `genre == "psalms"` chunk by bare
chapter number without book key, so `Ps`, `Song`, `Lam`, `PrMan`, and `Ps151` can collide. Increment 3a
intentionally leaves evaluator/leaderboard unchanged and claims no quality improvement.

## Living methodology artifact - COMPLETED (2026-06-05, Codex)

Created a living methodology artifact for the Chunking Skill Supply Chain and added a forced
methodology update/review rule for future chunking-related work. This is documentation and
coordination only: no runtime behavior, evaluator logic, chunk output, raw data, or canonical data
was intentionally changed by this checkpoint.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `ROADMAP.md`
- `ROADMAP_STATE.yaml`
- `HANDOFF_PROTOCOL.md`
- `docs/architecture/ARCHITECTURE.md`
- `docs/architecture/ADR-0011-chunking-orchestrator-skill-registry.md`
- `docs/chunking/CHUNKING_DESIGN.md`
- `docs/workflows/*`
- `config/agents/agent_roles.yaml`
- `config/chunking/form_registry.yaml`
- `config/chunking/skill_lifecycle_policy.yaml`
- `pipelines/chunking/skills/*/SKILL_METADATA.json`
- `registry/chunking/*`
- `scripts/validate_all.py`
- `scripts/agent/force_handoff.py`
- `scripts/agent/validate_handoffs.py`
- `.github/pull_request_template.md`
- `.ai/handoffs/T310/handoff.md`
- `.ai/handoffs/T311/handoff.md`

Files changed:
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md` - new living methodology
- `.ai/workflows/chunking-skill-supply-chain.workflow.md` - new AI-operational checklist
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md` - new skill author playbook
- `.ai/control/METHODOLOGY_UPDATE_RULES.md` - new forced update/review rule
- `AI_FRONT_DOOR.md` - references the chunking methodology rule for future agents
- `.github/pull_request_template.md` - adds required methodology PR note
- `.ai/control/PROJECT_STATUS.md` - records the methodology rule checkpoint
- `.ai/handoffs/T310/handoff.md` - records this checkpoint
- `.ai/control/handoff_ledger.jsonl` - updated by `force_handoff.py`

Decisions made:
- Created the requested `.ai/workflows/` path because the workflow is AI-operational and does not
  conflict with the existing lightweight `docs/workflows/` convention.
- Kept the rule lightweight: markdown control-plane rule, front-door discoverability, PR-template
  note, and handoff documentation. No new validator or governance subsystem was added.
- Treated T310/T311 methodology as provisional and explicitly blocked final LawFirm OS export until
  the required detector, shim, extraction, evaluator-risk, and improvement/rejected-improvement
  evidence exists.
- Recorded `Methodology updated: yes` for this checkpoint.

Validation run:
- command: `python scripts/validate_all.py`
- result: green
- output:
  - `Repo validation passed.`
  - `Control plane validation passed.`
  - `Cross-repo governance contract validation passed.`
  - `Handoff validation passed for 17 referenced handoff path(s).`
  - `Raw coverage OK: 46 distinct markers across 1 archive(s), all classified.`
  - `RAW_SOURCE_INVENTORY.md is current.`
  - `Manifest validation passed.`
  - `JSONL validation passed for 78742 records.`
  - `All validation gates passed.`
- command: `python -m pytest -q`
- result: green, `54 passed in 34.58s`
- failures: none

Known risks:
- The rule is documentation/coordination-enforced today, not script-enforced.
- T311 has now landed as a separate evaluator-surface correction. The unchanged D / Claude pass2
  output scores 93.0 under the corrected evaluator instead of 88.5 under the old evaluator.
- Future score-moving skill work must still prove target-form output improvement; corrected
  evaluator score movement is not a chunker improvement claim.

Open questions:
- Whether a future increment should add a CI validator for methodology PR-note compliance.
- Whether a future increment should add script-enforced branch hygiene for evaluator, skill, and
  methodology workstreams.

## Pre-3b readiness baseline/gold scaffold - COMPLETED (2026-06-05, Codex)

This checkpoint prepares T310 3b planning. It does not implement 3b, change chunk output, mutate
raw/canonical data, or change evaluator scoring behavior.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `ROADMAP.md`
- `ROADMAP_STATE.yaml`
- `HANDOFF_PROTOCOL.md`
- `docs/architecture/ADR-0011-chunking-orchestrator-skill-registry.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `.github/pull_request_template.md`
- `.ai/context/agent_work/T311_psalms_fragmented_before_after.md`
- `tests/test_chunker_gold.py`
- `tests/test_evaluate_chunks.py`

Files changed:
- `AI_FRONT_DOOR.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/tasks/T310.task.yaml`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `.github/pull_request_template.md`
- `docs/architecture/ADR-0011-chunking-orchestrator-skill-registry.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `eval/LEADERBOARD.md`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `pipelines/chunking/leaderboard.py`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `pipelines/chunking/skills/approved/monolith-pass2-v1/SKILL.md`
- `pipelines/chunking/skills/approved/monolith-pass2-v1/SKILL_METADATA.json`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL_METADATA.json`
- `registry/chunking/approved-skills.json`
- `registry/chunking/skill-graph-index.json`
- `.ai/handoffs/T310/handoff.md`

Decisions made:
- Active metadata now treats 93.0 as the corrected T311 evaluator baseline.
- 88.5 is retained only as old-evaluator provenance for the same D / Claude pass2 output.
- Added a planning-only `eval/chunking_gold/` scaffold; no promoted gold assertions were added.
- T310 3b and later output-changing skill work must cite per-form gold evidence before claiming
  improvement.
- T311 analysis identifies the current D literal Psalm fragmentation target as `Ps.78`; generated D
  chunks are not committed, so 3b must regenerate/capture the split before editing output.

Validation run:
- `python scripts/validate_all.py` -> all validation gates passed.
- `python -m pytest -q` -> 54 passed.
- `python pipelines/chunking/leaderboard.py` -> D / claude-opus-4.8 pass2 rank 1 at corrected 93.0.

Known risks:
- The gold scaffold is a plan, not reviewed/promoted gold.
- The per-form gold gate is documentation/control-plane visible, not a new CI validator.
- The single current literal Psalm fragmentation penalty is only 0.5 composite points; 3b must avoid
  overfitting to a weak aggregate lever.

Open questions:
- Whether future work should add a formal `eval/chunking_gold/` manifest schema.
- Whether a CI validator should require per-form gold citations for output-changing skill PRs.

## Next agent instruction

Review and merge the pre-3b readiness patch. Then plan T310 3b only after the corrected 93.0
baseline and per-form Psalm gold scaffold are acknowledged. Do not implement 3b, do not claim chunker
improvement from T311, and do not export the methodology to LawFirm OS as final doctrine yet.

<!-- superseded instruction below kept for history -->
<!--
Start **Increment 1** (read-only form detector). Add `pipelines/chunking/detect_form.py` that emits
candidate `FormAssignment` JSONL to `data/candidate/chunking/form_assignments/` using DETERMINISTIC
marker rules over `build_units()` marker sets (decision tree grounded in `form_registry.yaml` +
`usfm_marker_coverage.yaml`). Define — but leave default-OFF behind a flag — the LLM-adjudicator path
that writes a SEPARATE shadow `FormAssignment` (never overwrites deterministic). Change NO chunker
output. Validate ≥95% of chunks get a form at confidence ≥0.7; gates green; leaderboard still 88.5. Open
a PR "T310 Increment 1: read-only form detector"; do not merge/promote. Then update this handoff.
-->

---

## Handoff refresh: start

- agent_name: Codex
- mode:
- updated_at: 2026-06-05T20:07:01+00:00
- handoff_id: 3ca46ac50ebb6e9e

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-05T20:14:46+00:00
- handoff_id: 807fb27628ea5a91
