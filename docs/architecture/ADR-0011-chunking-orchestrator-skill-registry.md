# ADR-0011: Chunking orchestrator + skill registry (form-routed, self-extending)

## Status

Accepted (design; phased implementation) — 2026-06-05.
Proprietary subtree — see **Licensing** below.

Source proposals (four independent blind designs) and their reconciliation:
`.ai/context/recommendations/{CLAUDE,CODEX,CURSOR,COMPOSER}-orchestrator-skill-registry-design.md`
and `.ai/context/recommendations/ADJUDICATION-orchestrator-skill-registry.md`.

## Post-T311 / T314 scoring note

ADR-0011 originally protected the Pass-2 leaderboard score of 88.5. T311 later showed this was
old-evaluator provenance: Psalm-like chunks were grouped by bare chapter number, causing cross-book
collisions such as `Ps.3`, `Song.3`, and `Lam.3`. T311 corrected fragmentation grouping to
`(book, chapter)`.

The same D / Claude pass2 chunk output scored 93.0 under the T311 book/chapter evaluator. T314 then
preserved raw Psalm-fragmentation diagnostics while excluding exact manifest-reviewed parent/child
structural Psalm splits from the final bad-fragmentation penalty; the same unchanged output now
scores 93.5 under T314 policy. References below to 88.5 and 93.0 are historical evaluator
provenance, not chunk-output improvement claims.

## Context

- The chunker (`pipelines/chunking/chunker.py`) is a single genre-dispatch function keyed on nine
  book-level genres. Pass-2 scores 93.5 under the T314 policy baseline but conflates three separable concerns:
  (1) what literary **shape** a passage is, (2) which **algorithm** should chunk it, (3) whether the
  output **passed gates**.
- Vision (repo owner): an **orchestrator** that detects a passage's form, routes it to the best-fit
  chunking **skill**, knows all its skills via a **table of contents + knowledge graph**, **alerts
  when no skill fits**, runs a **multi-agent bake-off** to author the missing skill, and tracks
  **staleness** — scaling across corpora (eventually early-church writings) without becoming
  unmanageable ("mass customization", not skill sprawl).
- Four independent ("blind") proposals (Claude, Codex, Cursor, Composer) converged on ~80% of an
  architecture; the residual disagreements were decided interactively (see Decision).
- The owner's `00_LawFirm_OS` already implements this exact pattern (skill registry, orchestrator,
  graph index, lifecycle + quality-scoring registries, gap factory, SHA-pinned contract lock).
  It is adopted as the template; chunking-specific parts are built new.

## Decision

Build a **form-routed chunking orchestrator + skill registry** as a **refactor** of the existing
chunker (not a rebuild). Locked decisions:

1. **Routing key = marker-evidenced structural form.** `book_genres.yaml` is demoted to a *prior*.
   Overlays (`\wj`, `\fqa`, `\x`, `\qs`, `\d`) are **metadata modifiers / post-processors via
   `combines_with`**, never separate routing skills. [D1/D7]
2. **Form detection = deterministic USFM-marker rules + an LLM adjudicator.** The adjudicator fires
   only on low-confidence/ambiguous segments and emits a **separate candidate shadow `FormAssignment`**
   (method + prompt/version stamped) that **never overwrites** the deterministic record; the human
   picks the winner. All form assignments are `candidate`/human-correctable; nothing auto-promotes. [D1]
3. **Form taxonomy registered as a full ~40-form map**, each flagged `active` (skill + gold exist) or
   `declared-gap` (known, unbuilt). Declared-gaps are first-class graph nodes the orchestrator can
   alert on. ~15 active at start; grow with gold. **No form is `active` without a skill + a gold set.** [D2]
4. **Skills = versioned, self-describing packages** (`algorithm.py` + `SKILL.md` + `SKILL_METADATA.json`
   + fixtures) with **parametric variants** (`skill_id` + `variant_id`; `budget_profile` / source
   adapter) so scale = form × variant, **not** skill count. [B+1]
5. **8-state lifecycle:** draft → candidate → active → preferred → deprecated → superseded → retired,
   plus `quarantined`. Promotion is **human-gated**; `active→quarantined` is automatic on hard-gate fail. [D5]
6. **Layout:** code under `pipelines/chunking/`; human-edited policy YAML under `config/chunking/`;
   **committed** registry index + knowledge-graph + `contracts.lock` under `registry/chunking/`. Big
   chunk outputs and route ledgers stay ephemeral/gitignored. [D3]
7. **Routing unit = section windows** (heading→heading / chapter→budget); verse units remain the
   atomic text carriers (no per-verse form records). [D6]
8. **Skill selection** = highest gold-scored eligible non-stale skill for the form; ties broken by
   lifecycle priority, form specificity, score, recency, stable id; **human override** via
   `config/chunking/skill_overrides.yaml` (OSIS range → skill_id) as lowest-priority tie-break. [B+2]
9. **Gap loop:** triggers (no-skill-for-form / unknown-form / all-skills-fail-gates / uncovered-marker
   / no-gold / stale-only / regression) → **candidate** gap record → multi-agent bake-off
   (`evaluate_chunks.py` + `leaderboard.py`) → human **picks best or fuses** (fusion = human code merge
   with `combines_with`, not an LLM prompt merge). Nothing self-promotes.
10. **Gold sets** = per-form quality anchor under `eval/chunking_gold/per_form/`, **seeded incrementally**
    from the existing Ps 23 / Rom 7–8 / John 1 seed (one case added per form as built). Gold gates both
    gap-acceptance and promotion. [Gold]
11. **Staleness** = raw-inventory SHA change / marker-coverage change / policy-version bump / schema
    change / gold change / incumbent-beaten / age (~90d). **Lock enforcement deferred:** record the
    registry-surface SHA in the route ledger now; enable the fail-closed `contracts.lock` gate once the
    registry surface stabilizes. [D4]
12. **Quality scoring** weights live in `config/chunking/skill_quality_weights.yaml`; a
    `docs/chunking/SKILL_QUALITY_DOCTRINE.md` and a knowledge/execution/human `ORCHESTRATOR_BOUNDARY`
    document the bar and the guardrails. [B+3/B+4]
13. **The orchestrator is a thin, fail-closed, deterministic router in the knowledge plane — NOT an
    agent runtime.**

**Build by byte-identical extraction:** registry stub → read-only form detector (sidecar) →
orchestrator shim (byte-identical to current Pass-2) → extract psalm skill → extract prose/wisdom
skills → gap factory. Output-changing work is now gated against the current T314 evaluator-policy
baseline of composite ≥ 93.5 plus hard gates unless a task explicitly reviews an older evaluator
surface; the earlier ≥ 88.5 and ≥ 93.0 gates were old/T311 evaluator provenance.

## Licensing (proprietary carve-out)

The chunking method is proprietary. The subtrees `pipelines/chunking/`, `config/chunking/`, and
`registry/chunking/` are licensed **All Rights Reserved** under `pipelines/chunking/LICENSE` (the
Logos Chunker Proprietary License — no use, copying, modification, or derivative works without the
copyright holder's prior, express, written authorization). They are **carved out** of the repository
root MIT License (see root `LICENSE` and `config/chunking/NOTICE`). Copyright (c) 2026 Lowell Wong.

## Consequences

- The chunker becomes a pluggable, self-aware, governed system; new corpora add forms/skills, not
  rewrites. Self-aware gap detection + the multi-agent skill factory become first-class.
- Real upfront work: per-form **gold curation** (the critical path) and the extraction refactor —
  both incremental and gated so the current T314 93.5 baseline never regresses.
- The proprietary carve-out restricts reuse of the method; the rest of the repository stays MIT.
- Adds new committed surfaces (`registry/chunking/`, `config/chunking/*`, `eval/chunking_gold/`) that
  need freshness/validation wiring as they land (sequenced in T310).

## Relation to other ADRs

- Extends **ADR-0003** (chunks are derived artifacts) and honors **ADR-0007** (provenance
  canonicalization); depends on **ADR-0005** (canon profiles). The future **ADR-0006** (source-language
  boundary precedence) will add Hebrew/Greek colometry forms once real source text lands (Phase 5).
