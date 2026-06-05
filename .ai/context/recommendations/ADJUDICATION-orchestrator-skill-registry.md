# Adjudication — Chunking Orchestrator + Skill Registry (3 designs)

**Author:** Claude (Opus)  ·  **Date:** 2026-06-05  ·  **Mode:** review (diff only; no decision made)
**Inputs:** `CLAUDE-…`, `CODEX-…`, `CURSOR-…`, `COMPOSER-…` orchestrator-skill-registry-design.md
**Note:** **four** distinct designs (Claude, Codex, Cursor, Composer). `CURSOR/gemini -…md` is
byte-identical to `CURSOR-…md` (a duplicate, not a 5th). `COMPOSER-…md` also carries the
"Cursor Composer 2.5" byline but is genuinely distinct, more detailed content.

> Purpose: neutral side-by-side so the human decides per-point, OR green-lights synthesis into
> `ADR-0011` + task `T310`. Each disagreement lists the three positions + Claude's recommendation
> with a one-line reason. **No decision is recorded here.**

---

## A. Where all three AGREE (treat as settled unless you object)

1. **Refactor, not rebuild.** Extract the existing `chunk_book` branches (psalm/poetry, prose-heading,
   wisdom budget, epistle context-packet) into registered skills behind a common interface; keep a
   **compatibility shim that produces byte-identical output** until extraction is proven. Protect 88.5.
2. **Deterministic marker-driven form detection first.** LLM only on the exception path (low confidence
   / ambiguous / new marker), candidate-only, evidence-bearing, may not invent form IDs, never writes
   `data/canonical/`.
3. **Form assignment is a candidate, human-correctable artifact** (`ClassificationAssignment` /
   `FormDetectionCandidate`) written under `data/candidate/`. Nothing auto-promotes.
4. **Port the LawFirm `SKILL_METADATA.json` shape near-verbatim**, add Scripture fields
   (`handles_forms`/`form_ids`, `source_markers_required`, eval/gold refs, `staleness_triggers`,
   `forbidden_actions`). Port the graph-index, lifecycle-policy, and quality-scoring registries.
5. **Orchestrator = thin, fail-closed, deterministic router in the knowledge plane** — explicitly NOT
   an agent runtime. Append-only **routing ledger** records form, confidence, selected skill, rejected
   alternates, selection reason, and the registry-surface SHA.
6. **Gap loop:** triggers (no skill for form / unknown form / all-skills-fail-gates / new uncovered
   marker / no gold / stale-only / regression) → candidate gap record → **multi-agent bake-off** via
   `evaluate_chunks.py` + `leaderboard.py` → human **picks best or fuses**. Fusion = human code merge
   with `combines_with` edges, **not** an LLM prompt merge. Nothing self-approves.
7. **Per-form gold sets gate the loop** — both gap-acceptance and promotion. Tiered gold: global hard
   gates (exist) → per-form micro-gold → book-review → frozen corpus pin.
8. **Staleness triggers:** raw-inventory SHA change, marker-coverage change, policy-version bump, schema
   change, gold change, incumbent-beaten, age (~90d). Re-eval every chunker PR + on config/marker change.
9. **"Thousands of skills" rejected as a goal.** Bounded forms; thousands only as registry *nodes*
   (versions, eval runs, deprecated variants) — not thousands of distinct algorithms.
10. **Defer:** malicious-skill scanner, graph sharding, early-church support, LLM-first detection, graph UI.
11. **Parametric skill variants (named by Composer).** Scale = `form × budget-variant × source-family
    adapter`, expressed as `skill_id` + `variant_id` — NOT unbounded skill count. Thousands of
    *variants / registry nodes*, dozens of *algorithms*. This is the cleanest answer to your
    "thousands of skills" instinct, and all four designs reject thousands of distinct algorithms.

That convergence from **four** blind designs is strong evidence the architecture is right. The 4th
(Composer) did not overturn any decision below — it reinforced the consensus and added three useful
pieces (see **B+**).

---

## B. The real DISAGREEMENTS (your decisions)

### D1 — Primary routing axis  ★ most important
| Design | Position |
|---|---|
| **Cursor** | **Marker-composition profiles are the primary key.** Literary labels (oracle, pericope, argument-unit) are *overlays* on prose/poetry profiles. Explicitly: "delete literary-form-as-primary-axis." |
| **Codex** | Middle: a bounded form taxonomy, but "form ≠ book genre"; ~14–20 primary forms + overlays; `\wj`/`\fqa`/`\x` are overlays, not separate skills. |
| **Claude** | Literary form (form-critical: lament, oracle, pericope…) is the primary axis; markers are evidence for it. |
| **Composer** | "Structural literary form" detected **from markers**, with `book_genres.yaml` demoted to a **prior only**, and overlay markers as **metadata modifiers**. |
| **→ Rec** | **Near-consensus — the disagreement is mostly naming.** All four route on **marker-evidenced structural form** with book-genre as a prior only. Adopt: markers route v0 (deterministic, reproducible); literary form is a **curated overlay/refinement** layer (human-correctable). Composer collapses the Cursor-vs-Claude tension. |

### D2 — Taxonomy size
| Claude ~25–40 · Codex ~14–20 primary +4–8 overlays · Cursor ~38–45 (3 tiers) |
| **→ Rec:** start at **Codex's ~15 primary + overlays**, grow toward Cursor's ~40 only as gold sets justify. **Rule: do not register a form without a gold set + a skill for it.** |

### D3 — Where skills physically live  (interacts with the license decision)
| Design | Position |
|---|---|
| **Codex** | `pipelines/chunking/skills/{approved,candidate,quarantine}/` (skills are executable code); human policy under `config/chunking/skill_registry/`; generated TOC/graph under `build/`. |
| **Cursor** | `config/chunking/skills/` as registry root, with `algorithm.py` inside it. |
| **Claude** | `skills/chunking/` + `config/chunking/forms/`. |
| **Composer** | 3-way: code in `pipelines/chunking/skills/`, policy YAML in `config/chunking/`, and a **committed** `registry/chunking/` for the TOC + graph-index + `approved-skills.json` + `contracts.lock`. |
| **→ Rec** | **Codex layout + Composer's committed registry.** Code (skills, orchestrator, detector) under **`pipelines/chunking/`**; human policy YAML under `config/chunking/`; **commit the registry index/graph/`contracts.lock` under `registry/chunking/`** (auditable source-of-truth for routing — better than `build/`); route ledgers + big chunk outputs stay ephemeral/gitignored. `pipelines/chunking/` is the licensed subtree (see the license added this session). |

### D4 — `contracts.lock.json` timing
| Cursor + Claude: lock now · **Codex: defer** — record the registry-surface SHA in the route ledger first, add full lock validation once the surface stabilizes. |
| **→ Rec:** **Codex.** SHA in the ledger from day 1 (provenance now); full lock tooling later. |

### D5 — Lifecycle-state granularity
| **Codex + Cursor independently converged on 8 states**: draft → candidate → approved → preferred → deprecated → superseded → retired, plus quarantined. Claude proposed 4. |
| **→ Rec:** **adopt the 8-state model** (two designs converged; `preferred` = default when several approved skills match a form). |

### D6 — Routing-unit granularity
| Codex: book-local spans (verse units + boundary claims). Cursor: **section windows** (heading→heading / chapter→budget), verse units stay atomic carriers, reject per-verse records. Claude: per-unit. |
| **→ Rec:** **section-window** (Cursor); verse units remain the atomic text carriers. |

### D7 — Overlays (`\wj`, `\fqa`, `\x`) as skills vs metadata
| **Unanimous (Codex, Cursor, Composer):** `\wj`/`\fqa`/`\x`/`\qs`/`\d` are **metadata modifiers / post-processors via `combines_with`**, NOT separate routing skills (avoids `gospel_pericope_with_wj_and_x` explosion). Claude didn't separate cleanly. |
| **→ Rec:** **Settled** — overlays modify metadata / post-process; never multiply the form set. |

### D8 — Sharding threshold (minor)
| Codex 10k nodes · Cursor 500 · Composer 500. **→ Rec:** defer sharding (all agree defer); when needed, **500** (Scripture scope is small). |

---

## B+. What the 4th design (Composer) uniquely adds — fold into the synthesis

1. **Parametric skill variants** (`skill_id` + `variant_id`; `budget_profile`, source-family adapter).
   The right mechanism for "scale without skill explosion." → adopt in the registry schema.
2. **Human per-passage escape hatch:** `config/chunking/skill_overrides.yaml` mapping OSIS ranges →
   `skill_id`, as the lowest-priority tie-break. Lets you force a skill on a hard passage. → adopt.
3. **LLM adjudicator emits a *separate* shadow `FormAssignment`** (`method: llm_adjudication_v1`) that
   **never overwrites** the deterministic record — human picks the winner. Cleanly honors the repo's
   asserted/inferred separation rule. → adopt as the LLM-path contract.
4. **Concrete per-form gold layout:** `eval/chunking_gold/per_form/<form>/<case>.boundaries.json` +
   a `manifest.json` mapping forms→gold, seeded from the existing manual list (Gen 1–3, Ps 1/23/51/119,
   Prov 1–3, Isa 6/40/53, Matt 5–7, John 1, Rom 1/3/7–8, Heb 1–2, Rev 1/12/21–22). → adopt as the gold
   plan (resolves the §8 "build gold" dependency concretely).
5. **Concrete quality-scoring weights** (Codex + Composer converge): task_success/gold-pass,
   evidence/boundary-basis, schema conformance, boundary compliance, eval coverage, recency, reuse-fit,
   cost-efficiency; hard penalties for boundary/gold-gate violations. → land in
   `config/chunking/skill_quality_weights.yaml`.
6. **Port the doctrine + boundary docs:** `docs/chunking/SKILL_QUALITY_DOCTRINE.md` (from
   `skill-quality-rubric.json`) and a knowledge/execution/human `ORCHESTRATOR_BOUNDARY` split. → adopt.

None of these change D1–D8; they make the synthesis more concrete.

---

## C. Net synthesized design (if you green-light)

Marker-evidenced structural-form routing, book-genre as prior only (all four) · ~15 primary forms +
overlays growing to ~40 with gold (Codex) · **parametric `skill_id`+`variant_id`** so scale = form ×
budget × source-adapter, not skill count (Composer) · code under `pipelines/chunking/`, policy under
`config/chunking/`, **committed registry/graph/lock under `registry/chunking/`** (Codex+Composer) ·
8-state lifecycle (Codex/Cursor/Composer) · section-window units (Cursor) · overlays-as-metadata
(unanimous) · `skill_overrides.yaml` OSIS→skill escape hatch (Composer) · LLM adjudicator writes a
**separate** shadow form-assignment, never overwrites deterministic (Composer) · registry SHA in
ledger now, full `contracts.lock` once the surface stabilizes (Codex) · per-form gold under
`eval/chunking_gold/per_form/` (Composer) · quality weights in `skill_quality_weights.yaml`
(Codex+Composer) · literary form as a curated overlay layer (Claude). Build order (all four agree):
registry stub → read-only form detector (sidecar) → byte-identical orchestrator shim → extract psalm
skill → extract prose/wisdom → gap factory. Every step gated at composite ≥ 88.5.

## D. Two ways forward (your call, per your message)
- **You decide per-point** above (override any `→ Rec`), then I write `ADR-0011` + `T310` to match; **or**
- **Green-light synthesis** — I write `ADR-0011` + `T310` using the `→ Rec` column as defaults, flagging
  every place I overrode a design so you can veto in review.
