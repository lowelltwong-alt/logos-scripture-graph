# Project Status — Single Source of Truth

**Last updated:** 2026-06-09
**Updated by:** T327E old-corpus eval surface cleanup (Codex)
**Active task:** -> **T327E** old-corpus eval surface cleanup completed as corpus-scope baseline cleanup; stress-atlas and observed-audit baseline language now points to the post-T327 canonical-66 D / Claude pass2 93.6 baseline, the T318 observed audit is explicitly labeled as historical pre-T327 diagnostic evidence requiring refresh before implementation, and the Psalm candidate skill metadata/docs now keep only canonical `Song`/`Lam` as non-target controls while stating `PrMan`/`Ps151` must not be reintroduced as canonical controls; no raw mutation, canonical passage/witness mutation, chunk regeneration, evaluator formula change, chunking algorithm change, leaderboard scoring change, boundary repo work, T327F/G work, or text import occurred; **T308** connection discovery + **T309** chunking bake-off still open

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

> **Post-3b roadmap planning pack (2026-06-06):** T310 3b-gold is complete and remains a gold-gate
> increment, not a chunking improvement claim. The next T310 action is human review of the Ps.78
> boundary packet, followed by an explicit merge-vs-preserve decision before any output-changing 3b
> work. T313 token-size evaluator/policy alignment, T320 biblical entity/spiritual realm layer, T330
> theological concept graph, and T340 retrieval/rendering contracts are separate future lanes. No
> output-changing 3b work has started.

> **Ps.78 parent/child gold decision (2026-06-06):** Human review approved preserving the current
> Psalm 78 child chunks under a parent whole-psalm literary unit. Parent: `Ps.78.1-72`; children:
> `Ps.78.1-69`, `Ps.78.70-71`, and `Ps.78.72`. This records reviewed gold and the parent/child
> structural-split lesson; it does not change chunk output, evaluator formula, raw/canonical data,
> runtime chunking code, or skill promotion. Current evaluator policy may still report
> `literal_psalms_fragmented=1`; any change to that treatment is a separate evaluator-policy task.

> **T314 reviewed structural split evaluator policy (2026-06-06):** Evaluator policy now preserves
> raw literal Psalm fragmentation diagnostics while excluding exact manifest-reviewed parent/child
> structural splits from final bad-fragmentation scoring. For unchanged D / Claude pass2 output,
> `literal_psalms_fragmented_raw=1`, `reviewed_structural_splits=1`, final
> `literal_psalms_fragmented=0`, and composite is 93.5. Score provenance chain is now 88.5 old
> evaluator -> 93.0 T311 book/chapter evaluator -> 93.5 T314 reviewed-structural-split policy. This
> is evaluator-policy correction, not chunk-output improvement.

> **T315 gold/evaluator/roadmap hardening (2026-06-07):** Added semantic validation for
> `eval/chunking_gold/per_form/*_manifest.json`, wired it into `validate_all`, added focused tests,
> created `GOLD_COVERAGE_INVENTORY.md`, audited score-language references, updated stale T313/ADR
> baseline prose to the T314 93.5 policy baseline, and created future-target / roadmap-registration
> plans. Broad future task registration is deferred until those tasks have real handoffs. No chunk
> output, evaluator formula, raw/canonical data, chunker/orchestrator behavior, runtime skill code, or
> skill promotion changed. Next possible work: T316 Biblical Chunking Stress Atlas, T313 token-size
> policy alignment, or T320/T321 planning. No output-changing chunk work is currently authorized.

> **T316 Biblical Chunking Stress Atlas (2026-06-07):** Created a proposed-only stress atlas under
> `eval/chunking_gold/stress_atlas/` with structured JSON cases and tests covering long structured
> units, long verses/lists, short context-dependent units, Greek long sentences, punctuation risk,
> major textual variants, DSS/LXX/MT divergence, speaker ambiguity, prophetic oracles, apocalyptic
> visions, legal/covenant blocks, genealogies/lists, parallel accounts, rhetorical arguments, hard
> exegesis, and parent/child candidates. All cases are `status: proposed` with
> `implementation_allowed: false`. This does not change chunk output, evaluator formula,
> raw/canonical data, chunker/orchestrator behavior, runtime skill code, or skill promotion. Stress
> cases must become reviewed gold or review packets before implementation.

> **T316b stress-case review packets (2026-06-07):** Created pending review packets for Ps.105,
> Ps.106, Isa.52.13-53.12, Mark.16.9-20, and John.7.53-8.11. Packets record current chunk behavior
> and local marker/footnote evidence only. All decisions remain `pending_human_review`; no packet is
> reviewed gold, no selected case is approved expected output, and no output-changing work is
> authorized. Ps.105 and Ps.106 are prioritized as long-Psalm parent/child candidates; textual
> variant packets require textual-criticism review before gold.

> **T316c words-of-Jesus marker stress cases (2026-06-07):** Added proposed stress-atlas coverage
> for words-of-Jesus `\wj` spans, Selah / `\qs` mid-psalm markers, John 3 speaker-boundary
> ambiguity, Matthew 5-7, John 13-17, Matthew 24-25 / Mark 13, and John 7:53-8:11 as a textual
> variant plus `\wj` speech issue. All cases remain `status: proposed` with
> `implementation_allowed: false`. `\wj` and `\qs` are recorded as marker evidence, not authority
> for speaker attribution, theological/text-critical decisions, or chunk boundaries. No reviewed
> gold, output change, evaluator change, raw/canonical mutation, runtime skill change, or skill
> promotion occurred.

> **T317 Psalm gold, WJ packets, token policy (2026-06-07):** Human review approved current Ps.105
> and Ps.106 whole-psalm behavior as reviewed gold: `Ps.105.1-45` remains one 601-token chunk and
> `Ps.106.1-48` remains one 721-token chunk. Ps.106 `b` markers are recorded as internal
> formatting/stanza evidence, not automatic child-boundary authority. Added pending WJ review
> packets for John 3 and Matthew 5-7; `\wj` and punctuation are evidence, not speaker attribution
> authority, and both packets remain `pending_human_review`. Updated T313 analysis to state that
> the p50 metric headroom is an evaluator/policy alignment risk, not authorization to retune
> chunking. No chunk output, evaluator formula, raw/canonical data, chunker/orchestrator behavior,
> runtime skill code, or skill promotion changed.

> **T318 observed stress atlas behavior audit (2026-06-08):** Added a diagnostic-only observed
> behavior surface for every T316/T316c stress-atlas case. The audit records current chunks touching
> each case, containment, splitting, extra-context mixing, marker evidence, review-packet status, and
> recommended next review steps. It preserves Ps.105/Ps.106 as already reviewed current behavior and
> keeps pending packets pending. All observed entries have `implementation_allowed: false`. This is
> triage evidence only: no reviewed gold was added, no evaluator policy changed, no chunk output
> changed, and no output-changing work is authorized.

> **T319 review packet index and promotion queue (2026-06-08):** Added
> `eval/chunking_gold/review_packets/review_packet_index.json` and
> `REVIEW_PACKET_INDEX.md` as a single diagnostic/control surface over 8 existing review packet
> files, 8 Psalm manifest reviewed cases, and all 44 observed stress-audit cases. The index has 60
> entries and a review queue for pending/policy-required/manual-investigation work. Every entry keeps
> `implementation_allowed: false` and `output_change_authorized: false`. T319 does not add reviewed
> gold, approve pending packets, change evaluator policy, change chunk output, mutate raw/canonical
> data, change runtime skill code, or authorize output-changing work.

> **T327A forensic canonical corpus scope audit (2026-06-08):** Owner decision recorded:
> `logos-scripture-graph` canonical Scripture/chunking scope is the 66-book canon. The current raw
> WEB archive has 83 USFM files: 66 canonical files, 15 deuterocanonical/apocrypha/non-66 files,
> front matter, and glossary. Current generated passages/witnesses contain 81 books and 6,955
> excluded non-66 records; local generated chunk variants and committed scorecards/leaderboard
> lineage were produced against the wider corpus. T327A is audit/planning only: no raw/canonical
> data, generated output, parser/chunker/orchestrator/evaluator behavior, scorecards, or boundary
> repo content changed. Next: T327B explicit 66-book allow-list / ingest filter before any
> T320/T325/T326 implementation work continues.

> **T327A1 three-repo routing guardrails (2026-06-08):** Added Scripture-side AI front-door routing
> and `.ai/control/boundary_material_routing.yaml`. `logos-scripture-graph` owns canonical 66-book
> Scripture truth and canonical chunking/evaluator/gold surfaces; `logos-boundary-literature` owns
> boundary, deuterocanonical/apocrypha, heterodox, disputed, forged, commentary/reception, and
> supporting literature as scoped background/comparison/refutation material; `logos-governance-
> architecture` owns the cross-repo registry / relationship-contract source of truth. Boundary
> material must not override, contaminate, or become equal authority to canonical Scripture.
> Scripture-side routing mirrors the governance registry locally for agent routing. No data, output,
> evaluator, scorecard, runtime, text-import, or T327B work occurred.

> **T327A2 boundary governance stop rules (2026-06-08):** Added Scripture-side mirrors of
> `BOUNDARY-GOV-001 - Governance Is Constraint, Not Obstacle` and `BOUNDARY-GOV-002 -
> Owner-Reserved Authorization for Boundary-Originated Higher-Layer Changes`. Boundary-originated
> requests that conflict with governance-layer policy, canonical Scripture authority,
> repository-link contracts, routing policy, trust hierarchy, or canonical scope must stop and be
> reviewed in the higher-authority repo. Only Lowell Wong, as project owner, may authorize
> boundary-originated changes to higher-authority governance, canonical Scripture authority,
> repository-link contracts, canonical scope, trust hierarchy, or cross-repo policy. Contributor
> consensus, contributor volume, automated recommendation, agent routing, and boundary-layer
> operational need are not sufficient authority. No data, output, evaluator, scorecard, runtime,
> text-import, or T327B work occurred.

> **T327B canonical 66-book ingest filter (2026-06-08):** Confirmed T327A.1 routing guardrails and
> T327A.2 stop-rule mirror are live on main, then added `config/canon/canonical_66_books.yaml`,
> `pipelines/util/canonical_scope.py`, and `scripts/validate_canonical_66_scope.py`. Future WEB
> USFM importer now has an explicit `--canonical-66-filter` flag that gates canonical passages,
> witnesses, and canonical sidecars to the owner-approved 66-book allow-list while preserving raw
> USFM event observation. Existing generated outputs may still contain non-66 records until T327C
> regeneration. T327D handles chunks,
> scorecards, leaderboard, and score language; T327E cleans gold/stress/review packet surfaces. No
> raw/canonical data, generated output, chunks, evaluator formula, leaderboard, scorecards, source
> texts, or T327C/D/E/F/G work changed.

> **T327B.1 canonical scope validator fail-closed hardening (2026-06-08):** Hardened
> `scripts/validate_canonical_66_scope.py` / `pipelines/util/canonical_scope.py` so optional
> canonical JSONL validation fails closed when a record has no resolvable `book`, `osis_book`,
> `usfm_book`, `osis_ref`, or `passage_id`. Valid 66-book records pass; excluded books, `GLO`,
> `FRT`, and glossary-like unclassified records fail. Glossary/front-matter/concordance/source
> metadata may be preserved only as separately scoped non-scripture supporting/reference artifacts,
> not canonical passages/chunks/witness text/leaderboard inputs/default retrieval text. The validator
> does not prove content authenticity if fake or altered text is falsely labeled with an allowed
> book such as `Mark`; that remains a raw source manifest, checksum, provenance, parser determinism,
> and raw immutability concern. No raw/canonical data, generated output, chunks, evaluator formula,
> leaderboard, scorecards, source texts, or T327C/D/E/F/G work changed.

> **T327C regenerate canonical 66 outputs (2026-06-08):** Regenerated local ignored canonical
> Scripture outputs with `python pipelines/ingest/usfm_importer.py --canonical-66-filter
> --processed-root build/t327c_processed/usfm`. Passage/witness outputs now contain exactly 66
> books and 31,103 records, down from 81 books and 38,058 records; 6,955 non-66
> deuterocanonical/apocrypha records were removed from generated canonical passage/witness outputs.
> `GLO` glossary entries are now zero in canonical outputs, and `FRT`/`GLO` are not canonical
> Scripture content. Canonical sidecars now carry book identity where needed for fail-closed
> validation. CI regeneration now uses `--canonical-66-filter`, and `validate_all` runs
> canonical-scope validation over regenerated canonical outputs and sidecars. This is corpus-scope
> correction, not chunking improvement. No data/raw mutation, chunk regeneration, evaluator formula
> change, leaderboard/scorecard update, gold/stress/review packet index update, source-text import,
> boundary repo change, or T327D/E/F/G work occurred. T327D owns chunk regeneration, scorecards,
> leaderboard, baseline language, and gold test hash/token updates.

> **T327D regenerate chunks for canonical 66 baseline (2026-06-08):** Regenerated D / Claude
> pass2 chunks from the corrected 66-book canonical outputs in ignored derived space. The
> post-T327 canonical-66 chunk baseline is 1,131 chunks with SHA-256
> `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`, token p50 728,
> token p90 898, token max 1,152, and composite 93.6 under unchanged T314 evaluator policy. The
> previous 1,374-chunk / 93.5 row is now explicitly labeled as `pre_t327_wider_corpus`; the new
> row is `post_t327_canonical_66_corpus`. Removed temporary T327C xfails and removed `PrMan` /
> `Ps151` from canonical Psalm gold controls. This is corpus-scope correction / baseline reset,
> not chunking improvement. No raw data, canonical passage/witness outputs, evaluator formula,
> chunking algorithm, boundary repo, T327E/F/G, or text import work occurred. T327E owns broader
> gold/stress/observed/index cleanup.

> **T327E old-corpus eval surface cleanup (2026-06-09):** Searched old-corpus terms across
> gold/stress/observed/review-packet/governance surfaces and classified occurrences as active
> controls, stale baseline language, historical audit/provenance, exclusion tests, boundary-routing
> policy, or unclear review. Updated stress-atlas baseline wording to the post-T327 canonical-66
> 93.6 baseline, labeled the T318 observed audit as historical pre-T327 wider-corpus diagnostic
> evidence rather than current post-T327 behavior, and updated the Psalm candidate skill docs/metadata
> so active canonical non-target controls are only `Song` and `Lam`. Historical T327A/T327B/T327C
> audit evidence, exclusion tests/config, raw source inventories, and boundary-routing policy were
> preserved. This is corpus-scope cleanup, not chunking improvement. No raw data, canonical
> passage/witness outputs, chunk regeneration, evaluator formula, chunking algorithm, leaderboard
> scoring, boundary repo, T327F/G, or text import work occurred.

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
