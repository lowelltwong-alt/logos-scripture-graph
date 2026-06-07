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

## Increment 3b target selection plan - COMPLETED (2026-06-06, Codex)

Planning-only investigation completed on branch `t310-3b-plan-target-selection`. No implementation,
chunk output, raw/canonical data, evaluator formula, skill promotion, or broad routing change was made.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `ROADMAP.md`
- `ROADMAP_STATE.yaml`
- `HANDOFF_PROTOCOL.md`
- `config/agents/agent_roles.yaml`
- `.ai/tasks/T310.task.yaml`
- `.ai/handoffs/T310/handoff.md`
- `eval/LEADERBOARD.md`
- `eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `config/chunking/chunking_policy.yaml`
- `config/chunking/book_genres.yaml`
- `registry/chunking/approved-skills.json`
- `registry/chunking/skill-toc.json`
- `registry/chunking/skill-graph-index.json`
- `pipelines/chunking/chunker.py`
- `pipelines/chunking/orchestrator.py`
- `pipelines/chunking/evaluate_chunks.py`
- `pipelines/chunking/leaderboard.py`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/{SKILL.md,SKILL_METADATA.json,algorithm.py}`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.github/pull_request_template.md`

Files changed:
- `.ai/handoffs/T310/handoff.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/handoff_ledger.jsonl` (updated by `force_handoff.py`)

Ignored/generated analysis outputs:
- `build/t310-3b-plan/orchestrator/chunks.jsonl`
- `build/t310-3b-plan/orchestrator/context_packets.jsonl`
- `build/t310-3b-plan/orchestrator/route_ledger.jsonl`
- `build/t310-3b-plan/eval_report.md`
- `build/t310-3b-plan/eval_scores.json`
- `build/t310-3b-plan/LEADERBOARD.md`

Decisions made:
- Recommended T310 3b path: **3b-gold**, convert the Psalm gold scaffold into executable/reviewed
  Psalm gold before any Ps.78 output change.
- Rationale: current `Ps.78` fragmentation is real but direct score upside is only +0.5 composite;
  the current split is partly token-budget and partly real `\b` stanza evidence, so merging is a
  policy/gold decision rather than a safe mechanical bug fix.
- Size fitness has much larger formula headroom (+6.5 from p50 alone) but requires broad output
  changes and should not be the first output-changing increment without a corpus-level gold/eval plan.
- Methodology reviewed: no change required - planning confirmed the existing supply-chain rule that
  output-changing skill work must cite reviewed per-form gold and should not optimize a weak aggregate
  score without target-form evidence.

Validation / investigation run:
- `git fetch origin main`; `git pull --ff-only origin main`; branch created from updated `main`.
- Regenerated current orchestrator chunks into ignored `build/t310-3b-plan/`.
- Existing D/pass2 chunks and regenerated orchestrator chunks share SHA-256
  `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`.
- Fresh evaluation of existing D/pass2 and regenerated current output matched: 1374 chunks, p50 729,
  literal Psalm fragmentation 1, Psalm 119 section chunks 22, no leaks/crossings, 100% sentence integrity.
- Fresh leaderboard in ignored `build/` still ranks D / Claude pass2 first at corrected composite 93.0.
- Current route ledger uses `psalm-whole-then-stanza-v1` for literal `Ps` only; `Song`, `Lam`,
  `PrMan`, `Ps151`, and all other books stay on `monolith-pass2-v1`.

Known risks:
- `Ps.78` is the only current literal Psalm fragmentation target, but reviewed expected boundaries do
  not yet exist.
- Current `eval/chunking_gold/per_form/psalms_gold_plan.md` is a scaffold, not promoted gold.
- A narrow Ps.78 merge would likely pass hard token/sentence/book gates but could ignore real stanza
  evidence and encode an unreviewed Psalm policy decision.
- Token p50 improvement is the largest formula lever, but it is broad and likely crosses many forms.

Open questions:
- Should reviewed Psalm gold define Psalm 78 as one whole-psalm chunk because 1165 tokens is under
  hard max, or preserve the final `\b` stanza split?
- Should the next gold artifact be markdown-plus-tests first, or a formal manifest schema plus tests?
- What minimum target-form evidence should be required before promoting the Psalm candidate skill from
  `candidate` toward `active`?

## Increment 3b-gold - COMPLETED (2026-06-06, Codex)

Executable Psalm gold checks landed for settled cases. This increment is intentionally
non-output-changing: no chunking behavior, evaluator formula, raw/canonical data, skill promotion,
or broad routing changed.

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
- `docs/chunking/CHUNKING_DESIGN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `config/agents/agent_roles.yaml`
- `tests/test_chunker_gold.py`
- `tests/test_evaluate_chunks.py`
- `tests/test_chunking_orchestrator.py`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json`
- `config/chunking/chunking_policy.yaml`

Files changed:
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `tests/test_chunker_gold.py`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T310/handoff.md`
- `.ai/control/handoff_ledger.jsonl` (updated by `force_handoff.py`)

Gold checks added:
- `Ps.23.1-Ps.23.6` remains exactly one whole-psalm chunk.
- `Ps.119` remains exactly 22 chunks/sections and is reported, not penalized, by the corrected
  evaluator surface.
- Short Psalm holdouts `Ps.1`, `Ps.8`, `Ps.100`, and `Ps.117` remain one chunk each.
- Real `Ps.3` `\d` superscription source evidence is checked, and no standalone orphan title chunk is emitted.
- Non-target poetry controls `Song`, `Lam`, `PrMan`, and `Ps151` remain route-stable on
  `monolith-pass2-v1` fallback with `detect_form_consumed: false`.
- The generated chunk stream is checked against baseline SHA-256
  `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`.

Ps.78 characterization:
- Current observed chunks are captured only as characterization: `Ps.78.1-Ps.78.69` (1109 tokens),
  `Ps.78.70-Ps.78.71` (35 tokens), and `Ps.78.72-Ps.78.72` (21 tokens).
- Merged Ps.78 would be 1165 tokens, exceeding soft max 1100 by 65 and staying below hard max 1600.
- Structural evidence includes q1/q2 throughout and a `b` marker at `Ps.78.72`.
- Status remains `pending_human_review`; the merge-vs-preserve-`\b` decision is not made here.

Decisions made:
- Added a lightweight JSON manifest under `eval/chunking_gold/per_form/` instead of introducing a
  repository-wide formal manifest schema.
- Kept Ps.78 out of `reviewed_gold`; it lives under `characterization_only`.
- Methodology reviewed: no change required - this patch follows the existing supply-chain rule by
  adding per-form gold gates without changing runtime behavior, evaluator logic, or promotion state.

Validation run:
- `python -m pytest -q tests/test_chunker_gold.py` -> 13 passed.
- `python scripts/validate_all.py` -> all validation gates passed.
- `python -m pytest -q` -> 60 passed.
- `python pipelines/chunking/leaderboard.py` -> D / Claude pass2 remains rank 1 at corrected
  composite 93.0; command rewrote only generated timestamp/newline churn in `eval/LEADERBOARD.md`,
  which was restored so no leaderboard artifact change remains.

Known risks:
- The Ps.3 superscription check verifies source evidence and absence of an orphan title chunk under
  the current witness/chunk model; title text inclusion is not newly modeled in this increment.
- Ps.78 remains unresolved and must not be treated as reviewed expected-boundary gold.
- The manifest schema is intentionally lightweight and may need formalization later.

Open questions:
- Human review must decide whether Ps.78 should merge under hard-max tolerance or preserve the final
  `\b` stanza boundary.
- Future work should decide whether `eval/chunking_gold/` needs a formal schema validator.

## Increment 3b-gold methodology update - COMPLETED (2026-06-06, Codex)

The methodology requirement triggered by scaffold-to-executable-gold conversion was handled. This is
documentation/control-plane only: no runtime, evaluator formula, chunk output, raw/canonical data, or
skill promotion changed.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`

Files changed:
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T310/handoff.md`
- `.ai/control/handoff_ledger.jsonl` (updated by `force_handoff.py`)

Decisions made:
- Methodology updated: yes.
- Gold maturity is now explicit: scaffold/plan, executable reviewed gold, characterization-only, and
  pending human review.
- Gold scaffold is not promoted gold.
- Characterization-only evidence is not approved expected output.
- Output-changing skill work requires executable/reviewed gold first.
- Weak evaluator levers, such as Ps.78's +0.5 upside, cannot drive implementation without
  target-form evidence.
- Human-gated boundary decisions remain pending until explicitly reviewed.

Validation run:
- `python scripts/validate_all.py` -> all validation gates passed.
- `python -m pytest -q` -> 60 passed.
- `git diff --check` -> clean; only CRLF normalization warnings on handoff/control-plane files.

Known risks:
- Methodology now names a lightweight maturity ladder but no formal manifest schema validator exists yet.

Open questions:
- Whether future work should add CI validation for gold maturity labels in `eval/chunking_gold/`.

## Post-3b roadmap planning pack - COMPLETED (2026-06-06, Codex)

Roadmap-preparation pass completed on branch `roadmap/post-3b-planning-pack`. This pass is
non-output-changing: no chunk output, evaluator formula, raw/canonical data, skill runtime, skill
promotion, or T320/T330/T340 implementation changed.

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
- `docs/chunking/CHUNKING_DESIGN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `config/agents/agent_roles.yaml`
- `.ai/tasks/T310.task.yaml`
- `.ai/handoffs/T310/handoff.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json`
- `eval/LEADERBOARD.md`
- `config/chunking/chunking_policy.yaml`
- `pipelines/chunking/leaderboard.py`
- `pipelines/chunking/evaluate_chunks.py`
- `schemas/relationship_object.schema.json`
- `schemas/classification_assignment.schema.json`
- `docs/architecture/ADR-0010-source-language-witness-and-extra-biblical-layers.md`
- `docs/architecture/OBJECT_CONTRACT.md`

Files changed:
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `docs/roadmap/T313_TOKEN_SIZE_EVALUATOR_POLICY_ALIGNMENT.md`
- `docs/roadmap/T320_BIBLICAL_ENTITY_AND_SPIRITUAL_REALM_LAYER.md`
- `docs/roadmap/T330_THEOLOGICAL_CONCEPT_GRAPH.md`
- `docs/roadmap/T340_RETRIEVAL_RENDERING_CONTRACTS.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T310/handoff.md`
- `.ai/control/handoff_ledger.jsonl` (updated by `force_handoff.py`)

Ignored/generated analysis outputs:
- `build/post-3b-planning-pack/chunks.jsonl`
- `build/post-3b-planning-pack/context_packets.jsonl`
- `build/post-3b-planning-pack/route_ledger.jsonl`
- `build/post-3b-planning-pack/eval_report.md`
- `build/post-3b-planning-pack/eval_scores.json`

Decisions made:
- Created a Ps.78 boundary review packet with `Decision: pending`; no merge or preserve decision was
  encoded.
- Confirmed regenerated D/pass2 chunks match SHA-256
  `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7` when generated with footnote
  and editorial-cross-reference sidecars.
- Recorded T313 as evaluator/policy alignment work, not token-size implementation.
- Recorded T320 as an entity/spiritual-realm planning lane only; no schemas implemented.
- Recorded T330 as concept graph planning only; no predicates or graph claims implemented.
- Recorded T340 as retrieval/rendering contract planning only; no runtime or view implementation.
- Methodology updated: yes. Added a small future-lane categorization rule so adjacent roadmap work is
  categorized as chunking, evaluator, entity layer, concept graph, retrieval/rendering, methodology,
  or external export before implementation begins.
- No output-changing 3b work started.

Validation run:
- `python scripts/validate_all.py` -> all validation gates passed:
  - `Repo validation passed.`
  - `Control plane validation passed.`
  - `Cross-repo governance contract validation passed.`
  - `Handoff validation passed for 17 referenced handoff path(s).`
  - `Raw coverage OK: 46 distinct markers across 1 archive(s), all classified.`
  - `RAW_SOURCE_INVENTORY.md is current.`
  - `Manifest validation passed.`
  - `JSONL validation passed for 78742 records.`
  - `All validation gates passed.`
- `python -m pytest -q` -> 60 passed.

Known risks:
- Ps.78 remains human-gated and unresolved.
- T313 p50 target/policy alignment could become a broad output-changing task if not scoped first.
- T320/T330/T340 are roadmap plans only and still need schemas/gold/review before implementation.

Open questions:
- Should Ps.78 merge under hard-max tolerance, preserve the `\b`/stanza-sensitive split, or trigger
  a separate evaluator-policy PR for reviewed long-Psalm splits?
- Should T313 reconcile leaderboard target p50=600 with policy `target_tokens=700`, or intentionally
  keep separate retrieval-median and assembly-policy targets?
- Which T320 interpretive profiles beyond the Heiser divine council profile should be seeded first?

## Ps.78 parent/child gold decision - COMPLETED (2026-06-06, Codex)

Human decision recorded: preserve the current Psalm 78 split, but mark it as an approved structural
split under a parent whole-psalm unit. This is gold/methodology work only: no chunk output,
evaluator formula, raw/canonical data, runtime chunking code, orchestrator route behavior, or skill
promotion changed.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `ROADMAP.md`
- `ROADMAP_STATE.yaml`
- `HANDOFF_PROTOCOL.md`
- `config/agents/agent_roles.yaml`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `tests/test_chunker_gold.py`
- `.ai/handoffs/T310/handoff.md`

Files changed:
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `tests/test_chunker_gold.py`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T310/handoff.md`
- `.ai/control/handoff_ledger.jsonl` (updated by `force_handoff.py`)

Decisions made:
- Methodology updated: yes.
- Parent whole-psalm unit: `Ps.78.1-72`.
- Reviewed child structural chunks: `Ps.78.1-69`, `Ps.78.70-71`, and `Ps.78.72`.
- Status recorded as `approved_structural_split_under_parent_whole_psalm`.
- Psalm 119 remains the stronger precedent for parent whole-unit plus child sectioning; Psalm 78 is
  now a reviewed lighter case.
- Reviewed structural split is not the same as bad fragmentation.
- Similar future cases should be reviewed through gold before evaluator or chunker changes.
- Current evaluator formula remains unchanged and may still report `literal_psalms_fragmented=1`.
- This is not a chunking improvement claim.

Validation run:
- `python -m pytest -q tests/test_chunker_gold.py` -> 13 passed.
- `python scripts/validate_all.py` -> all validation gates passed:
  - `Repo validation passed.`
  - `Control plane validation passed.`
  - `Cross-repo governance contract validation passed.`
  - `Handoff validation passed for 17 referenced handoff path(s).`
  - `Raw coverage OK: 46 distinct markers across 1 archive(s), all classified.`
  - `RAW_SOURCE_INVENTORY.md is current.`
  - `Manifest validation passed.`
  - `JSONL validation passed for 78742 records.`
  - `All validation gates passed.`
- `python -m pytest -q` -> 60 passed.
- `python pipelines/chunking/leaderboard.py` -> D / Claude pass2 remains rank 1 at corrected
  composite 93.0; current evaluator still reports `literal_psalms_fragmented=1`.

Known risks:
- Current evaluator policy may still count reviewed Psalm 78 child chunks as
  `literal_psalms_fragmented=1`.
- Future evaluator-policy work should decide whether reviewed structural splits are excluded from
  bad-fragmentation scoring or reported separately.

Open questions:
- Should a future evaluator-policy PR exempt reviewed structural splits such as Psalm 119 and Psalm
  78 from bad-fragmentation scoring?
- Should the parent whole-unit object become explicit in a future schema rather than gold metadata?

## T314 reviewed structural split evaluator policy - COMPLETED (2026-06-06, Codex)

Evaluator-policy correction implemented. This does not change chunk output, raw/canonical data,
chunker/orchestrator behavior, runtime skill code, skill promotion, or composite weighting.

Files read:
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `tests/test_chunker_gold.py`
- `tests/test_evaluate_chunks.py`
- `pipelines/chunking/evaluate_chunks.py`
- `pipelines/chunking/leaderboard.py`
- `eval/LEADERBOARD.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/handoffs/T310/handoff.md`

Files changed:
- `pipelines/chunking/evaluate_chunks.py`
- `pipelines/chunking/leaderboard.py`
- `tests/test_evaluate_chunks.py`
- `tests/test_chunker_gold.py`
- `eval/chunking_runs/*.json`
- `eval/LEADERBOARD.md`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T310/handoff.md`
- `.ai/control/handoff_ledger.jsonl` (updated by `force_handoff.py`)

Decisions made:
- Methodology updated: yes.
- Added `literal_psalms_fragmented_raw` as the raw diagnostic before reviewed structural-split
  exclusions.
- Added `reviewed_structural_splits` diagnostics for exact manifest-reviewed parent/child splits.
- Final `literal_psalms_fragmented` now excludes only qualifying reviewed structural splits.
- Qualification is defensive: approved/reviewed status, explicit parent, explicit child chunks,
  `reviewed_structural_split: true`, `not_bad_fragmentation_gold: true`, and exact observed
  start/end boundary match.
- Missing, malformed, or under-specified manifest falls back to raw counting and excludes nothing.
- Psalm 119 remains handled separately as `psalm119_section_chunks`.
- Unreviewed multi-chunk literal Psalms still count as bad fragmentation.
- Score provenance chain is now 88.5 old evaluator -> 93.0 T311 book/chapter evaluator -> 93.5
  T314 reviewed-structural-split evaluator policy, all for unchanged D / Claude pass2 output.

Validation run:
- `python scripts/validate_all.py` -> all validation gates passed:
  - `Repo validation passed.`
  - `Control plane validation passed.`
  - `Cross-repo governance contract validation passed.`
  - `Handoff validation passed for 17 referenced handoff path(s).`
  - `Raw coverage OK: 46 distinct markers across 1 archive(s), all classified.`
  - `RAW_SOURCE_INVENTORY.md is current.`
  - `Manifest validation passed.`
  - `JSONL validation passed for 78742 records.`
  - `All validation gates passed.`
- `python -m pytest -q` -> 64 passed.
- `python pipelines/chunking/leaderboard.py` -> D / Claude pass2 remains rank 1 at composite 93.5,
  with `literal_psalms_fragmented_raw=1`, `reviewed_structural_splits=1`, and final
  `literal_psalms_fragmented=0`.

Known risks:
- The evaluator now consumes optional gold metadata defensively; malformed or missing gold excludes
  nothing, but formal manifest schema validation remains deferred.
- Overusing reviewed structural split exceptions could hide real fragmentation if future reviews are
  loose; exact boundary matching and raw diagnostics mitigate this.

Open questions:
- Should a future manifest schema validator formalize reviewed structural split fields?
- Should additional reviewed long-Psalm split classes get separate diagnostics beyond the current
  `reviewed_structural_splits` list?

## T315 gold/evaluator/roadmap hardening - COMPLETED (2026-06-07, Codex)

Gold/evaluator/roadmap hardening completed on branch `t315-gold-evaluator-roadmap-hardening`. This
is governance and validation hardening only: no chunk output, evaluator formula, raw/canonical data,
chunker/orchestrator behavior, runtime skill code, or skill promotion changed.

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
- `docs/chunking/CHUNKING_DESIGN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `tests/test_chunker_gold.py`
- `tests/test_evaluate_chunks.py`

Files changed:
- `scripts/validate_chunking_gold.py`
- `scripts/validate_all.py`
- `tests/test_validate_chunking_gold.py`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`
- `docs/roadmap/T315_SCORE_LANGUAGE_AUDIT.md`
- `docs/roadmap/T315_NEXT_TARGET_INVENTORY.md`
- `docs/roadmap/T315_ROADMAP_REGISTRATION_PLAN.md`
- `docs/roadmap/T313_TOKEN_SIZE_EVALUATOR_POLICY_ALIGNMENT.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T315/handoff.md`
- `.ai/handoffs/T310/handoff.md`

Decisions made:
- Methodology updated: yes.
- Implemented minimal semantic gold manifest validation instead of deferring.
- Added a coverage inventory for reviewed Psalm gold, non-target controls, uncovered areas, and
  candidate future gold.
- Updated stale score-language docs so T314 93.5 is the current policy baseline while 93.0 remains
  T311 provenance and 88.5 remains old-evaluator provenance.
- Deferred broad future roadmap registration to a plan because the state convention expects real
  handoff references.

Validation run:
- `python scripts/validate_chunking_gold.py` -> passed.
- `python -m pytest -q tests/test_validate_chunking_gold.py tests/test_chunker_gold.py tests/test_evaluate_chunks.py` -> 27 passed.
- `python scripts/validate_all.py` -> all validation gates passed.
- `python -m pytest -q` -> 69 passed.

Known risks:
- Active skill/registry score metadata still references T311 93.0 provenance and should be rebased
  only in an explicit metadata reconciliation task.
- Future output-changing work still needs reviewed target-form gold beyond the current Psalm set.

Open questions:
- Should future gold manifests also get a formal JSON Schema?
- Should T316 stress atlas precede T313 policy changes, or run alongside them?

## T316 Biblical Chunking Stress Atlas - COMPLETED (2026-06-07, Codex)

Created a proposed-only Biblical Chunking Stress Atlas. This is planning/gold-target inventory only:
no chunk output, evaluator formula, raw/canonical data, chunker/orchestrator behavior, runtime skill
code, or skill promotion changed.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`
- `tests/test_chunker_gold.py`
- `docs/roadmap/T315_NEXT_TARGET_INVENTORY.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`

Files changed:
- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- `docs/roadmap/T316_BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `tests/test_chunking_stress_atlas.py`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T316/handoff.md`

Decisions made:
- Methodology updated: yes.
- Stress atlas cases are future candidates only: `status: proposed` and
  `implementation_allowed: false`.
- Covered all required stress categories, including long structured units, long verses/lists, short
  context-dependent units, Greek long sentences, punctuation risk, major textual variants,
  DSS/LXX/MT divergence, speaker ambiguity, prophetic/apocalyptic material, legal blocks,
  genealogies/lists, parallel accounts, rhetorical arguments, hard exegesis, and parent/child needs.
- Stress cases must become reviewed gold or review packets before implementation.

Validation run:
- `python -m pytest -q tests/test_chunking_stress_atlas.py` -> 5 passed.
- `python scripts/validate_all.py` -> all validation gates passed.
- `python -m pytest -q` -> 74 passed.

Known risks:
- Atlas entries are planning-level risk notes, not formal exegesis or reviewed boundary decisions.
- Text-critical/source-tradition cases likely need future source-language/tradition policy before
  output-changing work.

Open questions:
- Which atlas packet should become reviewed gold first?
- Should future stress atlas JSON get a dedicated schema/validator?

## T316b stress-case review packets - COMPLETED (2026-06-07, Codex)

Created pending review packets for selected T316 stress-atlas cases. This is gold-review
infrastructure only: no chunk output, evaluator formula, raw/canonical data, chunker/orchestrator
behavior, runtime skill code, or skill promotion changed.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `tests/test_chunker_gold.py`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`

Files changed:
- `eval/chunking_gold/review_packets/ps105_boundary_review.md`
- `eval/chunking_gold/review_packets/ps106_boundary_review.md`
- `eval/chunking_gold/review_packets/isa52_13_53_12_boundary_review.md`
- `eval/chunking_gold/review_packets/mark16_9_20_textual_variant_review.md`
- `eval/chunking_gold/review_packets/john7_53_8_11_textual_variant_review.md`
- `tests/test_stress_review_packets.py`
- `eval/chunking_gold/README.md`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`
- `docs/roadmap/T316_BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/tasks/T316b.task.yaml`
- `.ai/handoffs/T316b/handoff.md`
- `.ai/handoffs/T310/handoff.md`

Decisions made:
- Methodology updated: yes.
- Ps.105, Ps.106, Isa.52.13-53.12, Mark.16.9-20, and John.7.53-8.11 remain
  `pending_human_review`.
- No selected case was marked as reviewed gold, approved output, or an approved structural split.
- Textual-variant packets cite only existing local WEB footnote evidence and require future
  textual-criticism review before gold.
- The packets do not authorize output-changing work.

Validation run:
- `python scripts/validate_all.py` -> all validation gates passed.
- `python -m pytest -q` -> 76 passed.

Known risks:
- Review packets are not reviewed gold and must not drive implementation by themselves.
- T316b uses a suffix task id requested by the owner; the current force-handoff helper only accepts
  numeric `T###` IDs.

Open questions:
- Which pending packet should receive human review first?
- Should text-critical packets wait for source-language/tradition policy before any gold promotion?

## T316c words-of-Jesus marker stress cases - COMPLETED (2026-06-07, Codex)

Added proposed marker-sensitive stress cases for words-of-Jesus `\wj`, Selah `\qs`, and related
speaker-boundary/discourse risks. This is stress-atlas planning only: no chunk output, evaluator
formula, raw/canonical data, chunker/orchestrator behavior, runtime skill code, reviewed gold, or
skill promotion changed.

Files read:
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `eval/chunking_gold/review_packets/`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`
- `tests/test_chunking_stress_atlas.py`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `data/canonical/translations/eng-web/boundary_claims.jsonl`
- `data/canonical/translations/eng-web/word_tokens.jsonl`

Files changed:
- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `tests/test_chunking_stress_atlas.py`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`
- `eval/chunking_gold/README.md`
- `docs/roadmap/T316_BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/control/METHODOLOGY_UPDATE_RULES.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/tasks/T316c.task.yaml`
- `.ai/handoffs/T316c/handoff.md`
- `.ai/handoffs/T310/handoff.md`

Decisions made:
- Methodology updated: yes.
- Added proposed stress cases for `\wj` spans, `\qs` Selah markers, John 3, Matthew 5-7,
  John 13-17, Matthew 24-25 / Mark 13, and John 7:53-8:11 as a variant-plus-`wj` issue.
- `\wj` is evidence, not speaker-attribution authority.
- `\qs` is liturgical-rubric evidence, not an automatic chunk boundary.
- Marker-sensitive cases remain `status: proposed` and `implementation_allowed: false`.
- No output-changing work is authorized.

Validation run:
- `python scripts/validate_all.py` -> all validation gates passed.
- `python -m pytest -q` -> 79 passed.

Known risks:
- Marker-sensitive cases are not reviewed gold.
- Future speaker/textual/boundary decisions require human review before implementation.

Open questions:
- Which marker-sensitive case should become a review packet first?
- Should future `\wj` or `\qs` diagnostics be separate from chunk boundaries?

## Next agent instruction

Review/accept the T316c proposed marker-sensitive stress cases. Treat the 93.5 score as T314
evaluator-policy correction for unchanged output, not chunking improvement. Do not implement
output-changing chunk work unless a selected packet/case is explicitly promoted by human review into
reviewed gold, characterization-only evidence, or an approved parent/child structural split.

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

---

## Handoff refresh: start

- agent_name: Codex
- mode:
- updated_at: 2026-06-06T03:54:25+00:00
- handoff_id: 3ca46ac50ebb6e9e

---

## Handoff refresh: final

- agent_name: Codex
- mode: plan
- updated_at: 2026-06-06T04:02:57+00:00
- handoff_id: 807fb27628ea5a91

---

## Handoff refresh: start

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T04:12:48+00:00
- handoff_id: 3ca46ac50ebb6e9e

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T04:23:51+00:00
- handoff_id: 807fb27628ea5a91

---

## Handoff refresh: start

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T04:28:42+00:00
- handoff_id: 3ca46ac50ebb6e9e

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T04:34:47+00:00
- handoff_id: 807fb27628ea5a91

---

## Handoff refresh: start

- agent_name: Codex
- mode: plan
- updated_at: 2026-06-06T13:14:14+00:00
- handoff_id: 3ca46ac50ebb6e9e

---

## Handoff refresh: final

- agent_name: Codex
- mode: plan
- updated_at: 2026-06-06T13:22:54+00:00
- handoff_id: 807fb27628ea5a91

---

## Handoff refresh: start

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T18:13:30+00:00
- handoff_id: 3ca46ac50ebb6e9e

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T18:22:21+00:00
- handoff_id: 807fb27628ea5a91

---

## Handoff refresh: start

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T18:50:26+00:00
- handoff_id: 3ca46ac50ebb6e9e

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-06T19:00:43+00:00
- handoff_id: 807fb27628ea5a91
