# Task Handoff — Senior Architecture & Software Engineering Review

## Task

- task_id: T302
- title: Claude Opus architecture and chunking design review (post-ingest)
- phase: phase_3
- status: complete

## Agent

- agent_name: claude-opus-4.8 (session review)
- mode: review
- stage: final
- updated_at: 2026-06-03T19:00:00+00:00
- handoff_id: T302-senior-review-final

## Files read

- `.ai/control/PROJECT_STATUS.md`, `AI_FRONT_DOOR.md`, `ROADMAP.md`, `ROADMAP_STATE.yaml`
- `docs/architecture/ARCHITECTURE.md`, ADR-0001..0004
- `docs/chunking/CHUNKING_DESIGN.md`, `CHUNKING_RULES.md`, `LITERARY_POLICIES.md`, `EVALUATION_PLAN.md`
- `config/chunking/chunking_policy.yaml`, `config/governance/trust_zones.yaml`, `config/sources/sources.yaml`, `config/agents/agent_roles.yaml`
- `pipelines/ingest/usfm_importer.py`, `usfm_inline_parser.py`, `pipelines/chunking/chunker.py`, `boundary_scorer.py`
- `pipelines/validate/validate_manifest.py`, `scripts/validate_repo.py`, `scripts/validate_jsonl.py`
- `scripts/agent/force_handoff.py`, `validate_handoffs.py`
- `.github/workflows/validate.yml`, `pyproject.toml`, `.gitignore`
- `schemas/*.json` (15 files)
- `.ai/handoffs/T300/handoff.md`, `T301/handoff.md`, `T201/handoff.md`
- `docs/workflows/INGESTION_WORKFLOW.md`

## Files changed

- `.ai/handoffs/T302/handoff.md` (this file — full review)
- `.ai/control/PROJECT_STATUS.md`
- `.ai/handoffs/T301/handoff.md` (revised agent queue)

## Decisions made

- **Verdict:** Architecture vision is **production-grade**; implementation is **early-stage** (~25% of designed system). Safe to proceed Phase 3 only after P0 blockers below.
- Ingest layer is **shippable** for WEB Classic as internal canonical data (not public release until CanonProfile + git baseline).
- Chunking design is **scholarly and correct**; chunking **implementation is not started** despite policy/docs implying v0 exists.
- Recommend **TextSpan as mandatory next schema** before any chunker rewrite — it is the linchpin for literary units and Hebrew/Greek alignment.
- Recommend **ProvenanceRecord canonicalization** to dedupe 864k inline SHA256 copies.
- **BoundaryClaim-only** input for chunker (not raw usfm_events) — confirmed as correct layering.

## Validation run

- command: `python pipelines/chunking/chunker.py --input data/canonical/scripture/passages/passages.jsonl --out build/test_chunks.jsonl`
- result: **failed** — `KeyError: 'translation_witness'` (CHK-4 confirmed)
- command: `python -m pytest -q`
- result: passed (5/5)
- command: `python scripts/validate_repo.py`
- result: passed
- command: `python scripts/agent/validate_handoffs.py`
- result: passed (8 handoffs)

---

# SENIOR REVIEW REPORT

## Executive verdict

This repo has ** unusually strong governance and domain architecture** for a Bible knowledge graph — immutability doctrine, trust zones, sidecar ingest, boundary stack chunking, asserted/inferred separation, and multi-agent handoffs are all correct choices.

As **software engineering**, it is a **well-documented scaffold with one production-quality pipeline (USFM ingest)** and **critical gaps** in testing, CI, schema enforcement, git hygiene, and downstream pipeline wiring. The chunker is not merely incomplete — it is **broken** relative to the data model T201 shipped.

**Readiness:**

| Layer | Grade | Notes |
|-------|-------|-------|
| Architecture docs | A | Coherent three-plane model, ADRs, chunking design |
| Agent governance | B- | Good protocol; stale T000/T001; no task YAMLs |
| Ingest pipeline | A- | Deterministic, tested, sidecar separation correct |
| Data model | B | Passage/witness split good; TextSpan missing; canon gap |
| Chunking | F (impl) / A (design) | Design excellent; code is skeleton + crash |
| Validation | D+ | Custom invariants only; no JSON Schema in CI |
| CI/CD | D | 2 checks; no pytest, no JSONL, no manifest |
| Multilingual path | B (plan) | Sources configured; schemas block expansion |
| Release readiness | F | No commits, no LICENSE, no CanonProfile |

**Bottom line:** Do not build embeddings, graph edges, or RAG on chunks until Phase 3 chunker + gold-set validation exist. Ingest is done; everything else is foundation work.

---

## Architecture strengths (preserve)

1. **Knowledge / control / execution separation** — prevents agent runtime from becoming source of truth.
2. **Raw immutability + manifest checksums** — reproducible provenance chain.
3. **Sidecar ingest pattern** — `\w`, `\f`, `\x`, structural markers extracted; clean witness text. Critical for graph quality.
4. **Boundary stack** — verse-as-weak-boundary, literary layer, future source-language override. Correct for biblical literature.
5. **BoundaryClaim with `is_canonical_ancient_boundary: false`** — distinguishes USFM editorial structure from Hebrew/Greek ancient boundaries. Subtle and essential.
6. **Editorial crossrefs quarantined** — `\x` → `editorial_cross_reference`, not auto-promoted to theological edges.
7. **Trust zones + assertion modes** — asserted/inferred/candidate separation for graph edges.
8. **677k Strong-tagged WordTokens** — ready-made v0 alignment bridge to Hebrew/Greek lexicon work.
9. **Role-based path allowlists** — `agent_roles.yaml` is a real governance mechanism.

---

## Architecture flaws (fix)

### P0 — Blockers

| ID | Flaw | Impact |
|----|------|--------|
| **CHK-4** | Chunker reads embedded `translation_witness` on passage; T201 split models | Pipeline dead |
| **CANON-1** | 6,213 deuterocanonical verses without `canon_profiles` | Publishing canonical data = implicit canon claim |
| **MODEL-GAP** | TextSpan, ContextPacket, ProvenanceRecord, ScriptureWork absent | Cannot implement designed chunking or alignment |
| **GIT-1** | Zero commits; parent workspace git root | Total loss risk on `git clean` |

### P1 — High

| ID | Flaw | Impact |
|----|------|--------|
| **PROV-1** | SHA256 duplicated 864,904× inline; no canonical ProvenanceRecord | Manifest change = full re-ingest with no join key |
| **SCHEMA-LOCK** | 8 schemas hardcode `translation_id: eng-web` | Blocks WLC/SBLGNT without schema fork |
| **CI-2** | CI skips pytest, validate_jsonl, validate_manifest | Regressions invisible |
| **VAL-GAP** | No JSON Schema validation in pipeline | Schemas are documentation only |
| **PRED-GAP** | RelationshipObject.predicate is free string; no registry | Graph edge sprawl, trust zone violations |

### P2 — Medium

| ID | Flaw | Impact |
|----|------|--------|
| **GENRE-GAP** | No `book_genres.yaml`; genre policies in chunking_policy unused | Psalms/epistles will chunk as prose |
| **DOC-DRIFT** | INGESTION_WORKFLOW.md wrong paths for importer/chunker | Agent confusion |
| **GOV-DRIFT** | T000/T001 handoffs stale; no `.ai/tasks/*.task.yaml` | Protocol non-compliance |
| **RAW-GIT** | `data/processed/**/extracted/` not gitignored | Bloated commits |
| **LIC-GAP** | No root LICENSE; CODEOWNERS placeholder | Not open-source ready |

---

## Software engineering review

### Code quality — Ingest (B+)

**Strengths:**
- Deterministic inline parser with explicit unsupported-marker audit trail
- Safe zip extraction with path traversal check
- Duplicate ID detection via `ImportState.unique()`
- Clean separation of passage registry vs translation witness
- Importer fix for manifest/archive override (test isolation)

**Weaknesses:**
- `usfm_importer.py` is 650 lines monolith — acceptable for v1 but needs module split before Hebrew/Greek importers
- Custom YAML writer in importer — should share with manifest tooling
- `parse_manifest()` is ad-hoc string split — works but fragile
- No streaming JSONL writer backpressure for 677k tokens (loads all in memory during parse — works but ~864k records is memory-heavy)
- Hardcoded `SOURCE_SHA256` in inline_parser constants duplicates manifest

**Recommendation:** Extract `pipelines/ingest/common.py` for JsonlWriter, manifest parse, provenance fields. Add `ProvenanceRecord` and reference by ID.

### Code quality — Chunking (F)

- `chunker.py` ignores `--policy` flag entirely
- `boundary_scorer.py` never imported by chunker
- Sentence detection: regex on `.!?` — insufficient for Bible text
- `included_text_span_ids` stores OSIS refs, not TextSpan IDs — misaligned with architecture
- No validation module for the 10 rules in EVALUATION_PLAN.md
- No genre lookup, no boundary_claims consumption, no context packets

### Testing (D+)

| Area | Coverage |
|------|----------|
| Inline parser | 4 unit tests — good |
| E2E ingest fixture | 1 test — good |
| Full corpus smoke | None |
| Chunker | None |
| Manifest validator | None |
| JSON Schema | None |
| Handoff scripts | None |
| Gold-set boundaries | None |

**5 tests for 864k-record pipeline is dangerously thin.** Minimum bar before Phase 3:
- Corpus marker-count smoke test (footnotes=1855, word_tokens=677688, etc.)
- Chunker smoke test after 4a fix
- Psalm 23 / Romans 8 gold-boundary fixtures (even 2 cases)

### CI/CD (D)

Current CI:
```yaml
validate_repo.py  # file existence only
validate_handoffs.py  # section headers only
```

Missing:
- pytest
- validate_jsonl on canonical outputs
- validate_manifest on all manifests
- Raw mutation tripwire (`git diff data/raw/`)
- Optional: JSON Schema via jsonschema package

### Data engineering (B- ingest / F downstream)

**Good:**
- JSONL as interchange format — correct for large corpus
- Canonical vs processed vs derived directory separation
- parser_report.yaml with marker inventory

**Bad:**
- No partitioning by book (single 677k-line word_tokens.jsonl)
- No incremental rebuild contract (full re-ingest only)
- No release artifact versioning (`build/releases/`)
- Derived directory empty — no chunks despite Phase 3 active

### Security & reliability

- Zip slip protection: **present** ✓
- Raw mutation policy: **documented**, not CI-enforced
- No secrets in repo ✓
- OneDrive + large JSONL: **operational risk** for concurrent agent writes
- Importer 60s runtime: acceptable; needs idempotent rebuild docs

### Maintainability & operability

- Dependency-free by design — good for bootstrap, bad for YAML/JSON Schema validation at scale
- Recommend adding optional `[project.optional-dependencies] validate = ["jsonschema", "pyyaml"]` without making them required
- `pyproject.toml` has `[tool.logos]` — good convention hook, unused by scripts

---

## Chunking design review

### Design grade: A

The boundary stack, genre policies, forbidden splits, context packet concept, and v0→v1 source-language path are **correct and necessary**. This is not over-engineering — generic RAG chunking would destroy this corpus.

### Implementation grade: F

Zero of the 10 CHUNKING_DESIGN v0 algorithm steps are implemented except step 1 (via ingest) and partial step 2 (verse-level only, not TextSpan).

### Literary form risks (if current skeleton chunker ships)

| Form | Risk |
|------|------|
| Psalms | Whole-psalm policy violated; `\d` superscriptions orphanable |
| Poetry | `\q1`/`\q2` flattened to prose space-join |
| Prophets | Oracle boundaries ignored; verse windows break oracles |
| Epistles | "Therefore" units split; no ContextPacket |
| Law | Case-law if/then blocks split at verses |
| Gospels | Pericope structure lost |
| Revelation | Vision cycles split arbitrarily |
| Quotations | No LXX/Hebrew context linkage |

### Source-language risks (Hebrew/Greek path)

**Ready:**
- Strong tags on 514k Hebrew + 162k Greek occurrences
- BoundaryClaim schema has `is_canonical_ancient_boundary` flag
- sources.yaml plans WLC, SBLGNT, RP, LXX

**Blocking:**
- No SourceLanguageWitness schema
- No AlignmentRecord schema
- No TextSpan at clause/word level
- WordToken schema locked to eng-web
- No ADR on source-language boundary precedence
- Deuterocanonical books lack Strong tags — alignment gap must be explicit

**Recommendation:** Phase 5 order should be:
1. SourceLanguageWitness + AlignmentRecord schemas
2. Passage-level OSIS alignment (already stable)
3. Strong-bridge LexemeAlignment from existing WordTokens
4. WLC/SBLGNT importers (verse-level first)
5. BoundaryClaim from Hebrew cantillation / Greek syntax
6. Chunk alignment fields on RetrievalChunk

---

## Missing contracts (must exist before scale)

| Contract | Status | Priority |
|----------|--------|----------|
| TextSpan | Missing | P0 |
| ContextPacket | Missing | P0 |
| ProvenanceRecord | Missing | P1 |
| CanonProfile | Missing | P0 |
| BookGenreRegistry | Missing | P1 |
| PredicateRegistry | Missing | P1 |
| SourceLanguageWitness | Missing | P2 |
| AlignmentRecord | Missing | P2 |
| ChunkValidationReport | Missing | P1 |
| ReleaseArtifact manifest | Missing | P2 |

---

## ADRs to write

| ADR | Title | Decision needed |
|-----|-------|-----------------|
| ADR-0005 | Canon profiles for multi-tradition corpus | How deuterocanonical books are tagged |
| ADR-0006 | Source-language boundary precedence | When Hebrew/Greek overrides English/USFM |
| ADR-0007 | Provenance canonicalization | provenance_id vs inline SHA256 |
| ADR-0008 | Chunk identity stability | Content-addressed vs positional chunk IDs |

---

## Prioritized remediation plan

### Sprint 1 — Codex (mechanical, 1-2 sessions)

1. Patch 4a: Fix chunker passage+witness join
2. `.gitignore`: extracted/, .pytest_cache/, optionally `data/raw/**/*.zip`
3. CI: pytest + validate_jsonl + validate_manifest
4. Fix INGESTION_WORKFLOW.md paths
5. First git commit (exclude raw zip or use LFS policy doc)
6. force_handoff.py: interpolate `--mode`; enforce task ID pattern

### Sprint 2 — Claude (architecture, 1-2 sessions)

1. ADR-0005 CanonProfile + tag deuterocanonical passages in schema/importer
2. TextSpan + ContextPacket JSON Schema
3. `config/chunking/book_genres.yaml` (66+15 books)
4. ADR-0006 source-language precedence (draft)
5. Chunk validation module spec (implement in Sprint 3)

### Sprint 3 — Codex + Claude pair

1. TextSpan generator from usfm_events + boundary_claims
2. Boundary-driven chunker v0 (consume BoundaryClaim + policy YAML + genres)
3. Gold set: Psalm 23, Romans 7:14-8:11, John 1:1-18
4. 10 automated checks from EVALUATION_PLAN.md

### Sprint 4+ — Phase 5 prep

1. Generalize schemas (remove eng-web const)
2. ProvenanceRecord + migration
3. Predicate registry
4. WLC/SBLGNT manifest stubs

---

## Known risks

1. Publishing `data/canonical/` before CanonProfile = silent canon theology decision
2. Chunker crash blocks any Phase 3 demo
3. No git history = total artifact loss
4. Schema const locks delay Hebrew/Greek by forcing rework
5. 864k-record JSONL in git without LFS = repo bloat (decide commit policy)

## Open questions

1. Commit canonical JSONL to git or generate in CI from raw zip? **Recommend:** commit manifest + schemas + scripts; generate canonical in CI or release step unless team wants frozen snapshots in repo.
2. Partition word_tokens by book now or at 2M+ tokens? **Recommend:** defer until second translation lands.
3. jsonschema as required dep or optional extra? **Recommend:** optional `[validate]` extra, required in CI.

## Next agent instruction

**Codex — start Sprint 1** (see updated T301 handoff):
1. `pipelines/chunking/chunker.py` — join passages + witnesses
2. `.github/workflows/validate.yml` — extend CI
3. `.gitignore` + first commit

**Claude — start Sprint 2** after Codex 4a lands:
1. `docs/architecture/ADR-0005-canon-profiles.md`
2. `schemas/text_span.schema.json`, `schemas/context_packet.schema.json`
3. `config/chunking/book_genres.yaml`

**Lower-tier agents:** Only subtasks explicitly listed in T301 after Sprint 1-2 complete. No ADRs, no chunker design.
