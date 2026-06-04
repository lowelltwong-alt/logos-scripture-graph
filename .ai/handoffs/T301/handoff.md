# Task Handoff — Next work queue (post-ingest)

## Task

- task_id: T301
- title: Post-ingest hardening and Phase 3 chunking kickoff
- phase: phase_3
- status: planned

## Agent

- agent_name: claude
- mode: plan
- stage: start
- updated_at: 2026-06-03T17:15:00+00:00
- handoff_id: T301-queue-handoff
- context: Ingest complete (T100 + T201 + T002). Chunker broken. Full review in T300.

## Files read

- .ai/handoffs/T300/handoff.md
- .ai/handoffs/T201/handoff.md
- .ai/handoffs/T100/handoff.md
- docs/chunking/CHUNKING_DESIGN.md
- pipelines/chunking/chunker.py

## Files changed

- .ai/handoffs/T301/handoff.md (this file)
- ROADMAP_STATE.yaml
- .ai/control/current_focus.yaml

## Decisions made

- **Ingest is complete** for WEB Classic. Do not re-run full ingest unless manifest or importer changes.
- Downstream work splits by agent strength (see below).
- Patch order from T300 still applies, minus Patch 1 (manifest) and Patch 2 (importer).

## Validation run

- Ingest closure verified 2026-06-03: manifest, importer, JSONL (864904 records), pytest (5/5).

## Known risks

- Chunker crashes on T201 passage shape until Patch 4a.
- Zero git commits — all artifacts untracked.
- 6,213 deuterocanonical verses lack CanonProfile metadata.
- CI shallow (no pytest, no JSONL validator in workflow).

---

## Agent assignment guide

### Give to **Codex** (build — mechanical, well-scoped, testable)

These have clear acceptance criteria and minimal design judgment:

| ID | Task | Effort | Acceptance |
|----|------|--------|------------|
| **4a** | Fix chunker to join passages + witnesses by `passage_id` | Low | CLI exits 0; smoke test; no `KeyError` |
| **CI** | Extend `.github/workflows/validate.yml`: pytest, validate_jsonl, validate_manifest | Low | CI fails on broken ingest/chunker |
| **GIT** | `.gitignore` extracted/, `.pytest_cache/`; first commit | Low | `git status` clean for ignored paths |
| **GOV** | Fix `force_handoff.py` mode substitution; enforce task ID pattern | Low | Handoff template gets correct mode |
| **4a-tests** | Chunk validation smoke tests (sentence end, book boundary) | Low | Tests pass on fixed chunker |

**Codex prompt starter:**

```text
Read AI_FRONT_DOOR.md and .ai/handoffs/T301/handoff.md.
Execute Codex queue items 4a, CI, GIT, GOV in order.
Do not implement boundary-driven chunking or new schemas.
Run force_handoff.py and pytest before stopping.
```

---

### Give to **Claude** (architecture — judgment, ADRs, literary design)

These need biblical-literary reasoning, schema design, or cross-cutting tradeoffs:

| ID | Task | Effort | Why Claude |
|----|------|--------|------------|
| **CANON** | ADR-0005 CanonProfile + tag 15 deuterocanonical books | Medium | Tradition-scoped canon is a design decision, not a script |
| **SCHEMA** | TextSpan, ContextPacket, ProvenanceRecord schemas | Medium | Must align with ARCHITECTURE.md identity chain |
| **4-full** | Boundary-driven chunker (boundary_claims + chunking_policy.yaml + genre) | Extra-high | Literary form rules, psalm/oracle/epistle logic |
| **GOLD** | Curate gold-set boundaries (Ps 23, Rom 7–8, John 1, etc.) | Medium | Scholar-facing quality bar |
| **HEB-GRK** | Phase 5 alignment architecture ADR (WLC, SBLGNT, Strong bridge) | Medium | Multilingual boundary precedence |
| **PRED** | Relationship predicate registry (editorial vs asserted intertextual) | Medium | Trust zone + evidence model |

**Claude prompt starter:**

```text
Read AI_FRONT_DOOR.md, T300 handoff, T301 handoff, CHUNKING_DESIGN.md.
Start with ADR-0005 CanonProfile (CANON-1 from T300) before any publish of data/canonical/.
Then draft TextSpan + ContextPacket schemas aligned to the boundary stack.
Do not implement chunker assembly until schemas are reviewed.
```

---

### Either agent (coordinate first)

| Task | Notes |
|------|-------|
| First git commit | Codex can execute; human should review what gets committed (zip likely excluded) |
| Book genre registry YAML | Claude designs mapping; Codex can implement file once approved |

---

## Open questions

1. Default CanonProfile for WEB deuterocanonical books? (See T300 § Open questions)
2. Unified vs split JSONL for canon scopes? (Recommendation: unified + metadata)
3. Should chunker consume only BoundaryClaim or also usfm_events? (Recommendation: BoundaryClaim only)

## Next agent instruction

**T302 review complete.** Full report: `.ai/handoffs/T302/handoff.md`

### Sprint 1 — Codex (start now)

| # | Task | File(s) | Acceptance |
|---|------|---------|------------|
| 1 | Patch 4a: chunker join | `pipelines/chunking/chunker.py` | `--passages` + `--witnesses` CLI; exits 0; smoke test |
| 2 | CI extension | `.github/workflows/validate.yml` | pytest + validate_jsonl + validate_manifest |
| 3 | Gitignore | `.gitignore` | `data/processed/**/extracted/`, `.pytest_cache/` |
| 4 | Doc fix | `docs/workflows/INGESTION_WORKFLOW.md` | Correct canonical paths |
| 5 | First commit | git | Manifest + schemas + scripts; zip policy documented |
| 6 | Handoff fix | `scripts/agent/force_handoff.py` | `--mode` interpolated; task ID enforced |

### Sprint 2 — Claude (after Sprint 1 item 1)

| # | Task | File(s) |
|---|------|---------|
| 1 | CanonProfile ADR | `docs/architecture/ADR-0005-canon-profiles.md` |
| 2 | TextSpan schema | `schemas/text_span.schema.json` |
| 3 | ContextPacket schema | `schemas/context_packet.schema.json` |
| 4 | Book genres | `config/chunking/book_genres.yaml` |

### Sprint 3 — Pair (after Sprint 2)

TextSpan generator → boundary-driven chunker → gold set (Ps 23, Rom 7-8, John 1)

**Lower-tier agents:** Sprint 1 subtasks only if explicitly assigned. No ADRs. No chunker design.
