# Project Status — Single Source of Truth

**Last updated:** 2026-06-06
**Updated by:** T310 3b-gold methodology update (Codex)
**Active task:** → **T310** 3b-gold implemented with methodology updated for executable gold maturity; Ps.78 output change remains human-gated and unresolved; **T308** connection discovery + **T309** chunking bake-off still open

> **T310 (new, 2026-06-05):** Four blind design proposals (Claude/Codex/Cursor/Composer) for a
> form-routed chunking orchestrator + skill registry were reconciled with the owner into **ADR-0011**
> (`docs/architecture/ADR-0011-…`). Decisions D1–D8 + B+ locked (marker-evidenced form routing +
> LLM-adjudicator shadow records; full ~40-form map flagged active/declared-gap; parametric skills;
> 8-state lifecycle; committed `registry/chunking/`; incremental per-form gold; deferred contract-lock
> gate). Build is a **byte-identical extraction** of the current chunker. Pre-T311 steps were gated at
> old-evaluator composite **≥ 88.5**; after T311, the unchanged D / Claude pass2 output is the
> corrected-evaluator baseline **93.0**. The chunking subtrees (`pipelines/chunking/`,
> `config/chunking/`, `registry/chunking/`)
> are now **proprietary / All Rights Reserved** (`pipelines/chunking/LICENSE`, carved out of root MIT).
> Source designs + reconciliation: `.ai/context/recommendations/`. Next: finish pre-3b readiness,
> then plan T310 3b against corrected baseline and per-form gold evidence.

> **T310 3b target selection (2026-06-06):** Planning-only investigation recommends **3b-gold**.
> Current D/pass2 chunks were located/regenerated in ignored space and byte-match SHA-256
> `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`; corrected score remains 93.0.
> `Ps.78` is the single literal Psalm fragmentation target, currently split into `Ps.78.1-69`,
> `Ps.78.70-71`, and `Ps.78.72` (1165 tokens if merged). Direct composite upside is only +0.5, and
> the split reflects soft-token/stanza evidence rather than a clear hard-gate bug. Before any output
> change, convert `eval/chunking_gold/per_form/psalms_gold_plan.md` into executable/reviewed Psalm
> gold covering Ps 23, Ps 119, Ps 78, short-Psalm holdouts, and non-target poetry controls.

> **T310 3b-gold implemented (2026-06-06):** Added executable Psalm gold manifest/tests for settled
> cases without changing output: Ps.23 one chunk, Ps.119 22 sections and not penalized, short Psalm
> holdouts (`Ps.1`, `Ps.8`, `Ps.100`, `Ps.117`), real Ps.3 superscription source evidence with no
> orphan title chunk, and non-target route controls (`Song`, `Lam`, `PrMan`, `Ps151`) staying on
> monolith fallback. Ps.78 is recorded as characterization-only with current boundaries/token counts
> and `pending_human_review`; no merge/preserve decision was promoted.

> **Methodology update (2026-06-06):** Living methodology, workflow checklist, skill playbook, and
> methodology control rule now distinguish scaffold/plan, executable reviewed gold,
> characterization-only evidence, and pending human review. Output-changing skill work now explicitly
> requires executable/reviewed gold first; weak evaluator levers like Ps.78's +0.5 upside cannot drive
> implementation without target-form evidence.

> Every agent reads this file **after** `ROADMAP_STATE.yaml` and **before** starting work.  
> Read **`.ai/control/MASTER_CONTEXT.md`** first for architecture authority (AI read-only).
> New/lower-level agents: start with `.ai/handoffs/AGENT_ROUTING_GUIDE.md`.

---

## Navigation (always start at the front door)

```text
AI_FRONT_DOOR.md
  -> MASTER_CONTEXT.md  (theory, human-gated, read-only)
  -> PROJECT_STATUS.md  (this file, current state)
  -> DATA_MAP.md        (data + pipeline endpoints, generated)
  -> ROADMAP_STATE.yaml -> handoffs/T###/handoff.md (your task)
```

`AGENT_ROUTING_GUIDE.md` = full step-by-step for any agent.

---

## Control plane (CI enforced)

| Gate | Command | Enforces |
|------|---------|----------|
| All gates | `python scripts/validate_all.py` | repo + control plane + handoffs |
| Master context lock | `validate_control_plane.py` | human-approved SHA256; AI cannot drift master |
| Front-door routing | same | AI_FRONT_DOOR, README, CLAUDE, AGENTS reference master context |
| Handoffs | `validate_handoffs.py` | active tasks have valid handoff sections |
| Tests | `python -m pytest -q` | 9 tests including control plane |

**CI:** `.github/workflows/validate.yml` runs validate_all + pytest on every push/PR.

> Every agent reads this file **after** `ROADMAP_STATE.yaml` and **before** starting work.  
> Read **`.ai/control/MASTER_CONTEXT.md`** first for architecture authority (AI read-only).

---

## Authority files

| File | Role |
|------|------|
| [`.ai/control/MASTER_CONTEXT.md`](MASTER_CONTEXT.md) | Human-gated design theory — AI must not edit |
| This file | Operational status — agents update after tasks |
| [`.ai/handoffs/T301/handoff.md`](../handoffs/T301/handoff.md) | Active sprint queue |

---

## Executive verdict (T302)

| Layer | Grade |
|-------|-------|
| Architecture docs | **A** |
| Ingest pipeline | **A-** |
| Chunking design | **A** |
| Chunking implementation | **F** |
| CI / testing | **D / D+** |
| Release readiness | **F** |

**Ingest complete. Phase 3 not ready until P0 blockers cleared.**

Full review: `.ai/handoffs/T302/handoff.md`

---

## Current phase

| Field | Value |
|-------|-------|
| Phase | **phase_7** — Cross-reference and intertextual graph (T308 run 1 active alongside phase_3 chunking work) |
| Ingest | **COMPLETE** ✓ |
| T302 review | **COMPLETE** ✓ |
| Connection discovery | **RUN 1 EMITTED** — 500 candidate-only edges under `data/candidate/connections/`; no promotion |
| Next | Human runs additional A/B agents, then compares agreement/disagreement for adjudication |

## T308 connection discovery status (2026-06-05)

- Codex 5.5 run 1 emitted `data/candidate/connections/codex-5.5-2026-06-05.jsonl` plus manifest/report.
- Comparison harness ran against `data/candidate/connections/2026-06-04-ab-review.jsonl`; current overlap is 0 agreement triples and 508 disagreement triples.
- All emitted edges are candidate-only (`assertion_mode=status=trust_zone=candidate`) and remain outside canonical promotion.

---

## Blocker status (resolved in T305 unless noted)

| ID | Issue | Status |
|----|-------|--------|
| GIT-1 | Zero git commits | **RESOLVED** — repo is its own git root; first commit made; generated data gitignored |
| CHK-4 | Chunker crashed on passage shape | **RESOLVED** — chunker joins passages+witnesses; smoke tests added; 0 USFM leaks |
| CANON-1 | Passages lacked CanonProfile | **RESOLVED** — importer emits `canon_profiles`+`testament`; 38,058/38,058 covered; ADR-0005; `--require-canon` gate |
| MODEL-GAP | Missing TextSpan/ContextPacket schemas | **RESOLVED (contracts)** — `schemas/text_span.schema.json`, `schemas/context_packet.schema.json` added (generators are Sprint 3) |
| CP-1 | Master-context gate locally bypassable | **PARTIAL** — `approved_commit` + tamper-evidence docs + CODEOWNERS entries (ADR-0009); **human must enable branch protection** |
| CP-2 | Active-task handoff regex fails open | **RESOLVED** — structural PyYAML parser, fail-closed |
| CI-GAP | JSONL/manifest/chunker ungated | **RESOLVED** — `validate_all` + workflow now gate manifest, JSONL+canon, schemas, chunker, DATA_MAP freshness, raw tripwire, pytest |
| GOV-STALE | T000/T001 stale in_progress | **RESOLVED** (T304) — closed; phase_0 complete |
| PRED-GAP | No predicate registry | **RESOLVED (stub)** — `config/governance/predicate_registry.yaml` |
| PROV-1 | Inline SHA256 dup | **DEFERRED** — ADR-0007 accepted-direction; migration is its own task |
| LIC-GAP | No LICENSE / CODEOWNERS placeholder | **RESOLVED** — root `LICENSE` (MIT); CODEOWNERS has real entries (handle still `@owner` to set) |

**Post-T305 state:** all gates green (`validate_all` 5 gates + 11 pytest). Phase 3 chunker is
un-broken (v0 join); boundary-driven chunker + TextSpan generator + gold set remain (Sprint 3).
Reviews: `.ai/handoffs/T304/handoff.md` (findings) → `.ai/handoffs/T305/handoff.md` (remediation).

---

## Sprint plan (from T302 review)

### Sprint 1 — Codex (start now)

1. Fix chunker (passages + witnesses join)
2. Extend CI (pytest, validate_jsonl, validate_manifest)
3. `.gitignore` + first commit
4. Fix INGESTION_WORKFLOW.md drift
5. force_handoff.py fixes

### Sprint 2 — Claude (after 4a)

1. ADR-0005 CanonProfile
2. TextSpan + ContextPacket schemas
3. `config/chunking/book_genres.yaml`

### Sprint 3 — Pair

1. TextSpan generator
2. Boundary-driven chunker v0
3. Gold set (Ps 23, Rom 7-8, John 1)

---

## Validation baseline

manifest ✓ | JSONL 864,904 ✓ | pytest 5/5 ✓ | chunker ✗

---

## Active handoffs

1. **`.ai/handoffs/T301/handoff.md`** — Codex/Claude task queue (Sprint 1-3)
2. **`.ai/handoffs/T302/handoff.md`** — Full senior review (complete)
3. `.ai/handoffs/T201/handoff.md` — Ingest deliverables

---

## Agent routing

| Agent | Scope |
|-------|-------|
| **Codex** | Sprint 1 mechanical work only |
| **Claude** | Sprint 2 ADRs + schemas (after chunker fix) |
| **Lower-tier** | Subtasks in T301 only; no architecture |

---

## Update rules

When finishing work, update: this file → task handoff → ROADMAP_STATE.yaml → current_focus.yaml → roadmap_events.jsonl
