# Project Status — Single Source of Truth

**Last updated:** 2026-06-03  
**Updated by:** T304 complete (Claude 4.8 full review)  
**Active task:** → **Codex Sprint 1 (T301)**; T304 review complete

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
| Phase | **phase_3** — Chunking engine v0 |
| Ingest | **COMPLETE** ✓ |
| T302 review | **COMPLETE** ✓ |
| Chunking | **NOT STARTED** (broken skeleton) |
| Next | Sprint 1 → Codex |

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
