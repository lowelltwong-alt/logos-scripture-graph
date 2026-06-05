# Design proposal — Chunking Orchestrator + Skill Registry (Claude submission)

**Status:** recommendation / proposal only (not canon, not an ADR yet)
**Author:** Claude (Opus)  ·  **Date:** 2026-06-05
**Mode:** explore/plan — no chunker refactor performed
**Comparison set:** parallel blind designs by Codex and Cursor Composer 2.5 (same 11 sections).
This doc was written BEFORE reading the LawFirm OS repo for sections 1–10; section 11 is the
post-study revision.

> One-line thesis: the orchestrator+skill-registry the owner wants is **mostly already built**
> — primitively here (genre dispatch in `chunker.py`, the bake-off in `leaderboard.py`) and
> fully in the owner's `00_LawFirm_OS` skill-supply-chain. The job is to **port the proven
> LawFirm pattern**, specialize it to chunking skills **typed to literary forms**, and route
> by form. You will NOT need thousands of skills for the Protestant canon — forms are bounded.

---

## 1. Form taxonomy (the routing key)

Route on **literary form**, not on book and not on passage. Forms are a bounded, theologically
grounded set. For the Protestant canon I estimate **~25–40 forms**, organized as an `is_a`
hierarchy so the orchestrator can fall back to a parent when a subtype is uncertain.

Seed taxonomy v0 (parent → subtypes):
- **narrative** → pericope, genealogy, itinerary/travel, dialogue-scene, sign/miracle-account
- **law** → casuistic-law, apodictic-law, covenant-code, ritual-instruction, census/list
- **poetry/psalm** → lament, hymn/praise, royal, wisdom-psalm, **acrostic**, thanksgiving,
  imprecatory, ascent; with sub-units: superscription (`\d`), Selah-bounded strophe (`\qs`),
  poetic colon/line (`\q1`/`\q2`)
- **wisdom** → saying-cluster (Proverbs), instruction-discourse (Job/Eccl), better-than proverb
- **prophecy** → oracle, woe-oracle, judgment-speech, salvation-oracle, vision-report, lawsuit (rib)
- **apocalyptic** → vision-cycle, throne-scene, hymn-insert
- **gospel** → pericope, parable, discourse-block, passion-narrative, genealogy
- **epistle** → opening/greeting, thanksgiving, argument-unit, paraenesis (exhortation),
  vice/virtue-list, household-code, doxology/benediction, travelogue/closing

Scaling claim: adding **early-church writings** (Apostolic Fathers, homilies, conciliar acts,
liturgy) adds *new forms* (homily-unit, creed/symbol, canon/decree, anaphora) — **dozens, not
thousands**. The thousands only appear across `corpora × language × era × translation`, which is
exactly why the registry must scale, but the **per-corpus form count stays disciplined**.

## 2. Form-detection stage (the orchestrator's front)

Pipeline: `unit → marker-driven rules (deterministic) → feature heuristics → optional LLM
tiebreak → form descriptor`.

- **Deterministic first, grounded in real markers.** Detection keys off the USFM markers that
  actually appear (`RAW_SOURCE_INVENTORY.md` / `usfm_marker_coverage.yaml`): `\d` superscription,
  `\qs` Selah, `\q1/\q2` poetic lines, `\b` stanza break, `\wj` words-of-Jesus, `\fqa` alternate
  reading, `\x` cross-ref, paragraph `\p`/`\m`, headings. Plus structural features (verse density,
  line length, refrain detection, citation formulae, vocative openings).
- **LLM only as a tiebreaker** for ambiguous units, and only with a recorded confidence and a
  short evidence string. No silent LLM relabeling.
- **Output is a candidate artifact.** Form descriptor `{form_type, confidence, evidence[],
  detector_version, provenance}` is written to the `candidate` trust zone, **human-correctable**.
  Corrected labels become the curated per-pericope genre layer that `book_genres.yaml` already
  calls "a future curated layer" — so this stage *upgrades* the existing one-genre-per-book map
  to per-unit forms, additively.

## 3. Skill registry (the spine)

A **skill = a versioned, self-describing chunking strategy** for one or more forms. Reuse the
owner's `SKILL_METADATA.json` schema near-verbatim (see §11) so both systems share one vocabulary.

Per-skill metadata (chunking-specialized):
```
skill_id, version, kind:"chunking_skill",
handles_forms: [form_type, ...]      # the routing key
depends_on_markers: [\q, \d, \qs ...] # ties staleness to raw coverage
inputs: [unit, boundary_claims, footnotes, crossrefs]
outputs: [chunk, context_packet]
gold_score: { form_type: float }      # per-form score on the gold set
validated_at_commit: <sha>
lifecycle_state: active|candidate|deprecated|stale
supersedes / superseded_by / combines_with
recommended_update_policy: human_gate
graph_node_ref, quality_score_ref, created_at, updated_at
```
Location: a new plane `skills/chunking/{approved,draft,quarantine}/<skill_id>/` with
`SKILL.md` (method) + `SKILL_METADATA.json` + fixtures. Registry index files mirror LawFirm:
`registry/approved-chunking-skills.json`, `discovered`, `rejected`, `proposed-draft-index`.

## 4. Knowledge graph / TOC

A graph index (port `skill-agent-graph-index.json`) with node types `{form, skill, marker}` and
edges:
- `(form) -handled_by-> (skill)`  ·  `(form) -is_a-> (parent_form)`
- `(skill) -depends_on-> (marker)`  ·  `(skill) -supersedes-> (skill)`  ·  `(skill) -combines-> (skill)`

This is the navigable TOC: the orchestrator answers "do I have a skill for form X? which is best?
is it stale? what does it depend on?" by walking this graph — no full-text scan of skills needed.

## 5. Routing / orchestration

Per unit: `detect form → graph lookup of skills handling that form → select active, non-stale,
highest gold_score skill → apply → emit chunk stamped {skill_id, version, form_type, confidence}`.

Relationship to today's code: this is a **refactor, not a rebuild**. The current
`chunk_book(... genre ...)` branch in `pipelines/chunking/chunker.py` is a primitive router with
inline strategies (whole-psalm, Ps-119 acrostic split, wisdom saying-cluster, prose-heading).
Step 1 is to extract those four strategies into the **seed registry entries v0** behind a stable
`apply(unit, ctx) -> chunks` interface, and replace the `if genre == X` branch with a registry
lookup. Output and gold scores must stay identical through the refactor (no regression below 88.5).

## 6. Gap detection + self-extension (the headline)

A **gap** fires when ANY of:
1. form detected with confidence ≥ θ_form but **no active skill** handles it;
2. best available skill's `gold_score` for the form < quality floor;
3. form confidence < θ_form (unknown/novel form — e.g. first early-church text).

On a gap the orchestrator **must not silently chunk**. It emits a `skill_gap` candidate artifact
`{form_or_features, evidence, example_units, recommended_skill_spec}` and alerts the human —
exactly the owner's `detect-skill-gaps` loop, where the gap source here is **chunking defect
clusters** (low-score forms, unknown forms, unclassified markers) instead of an exceptions lake.

Resolution = the **existing bake-off, scoped to one form**: dispatch Claude/Codex/Cursor to author
competing candidate skills against that form's gold set; `leaderboard.py` (extended to per-form)
ranks them; the human **promotes the winner OR** asks Claude to **fuse** the submissions into one
elegant skill (`combines_with` lineage recorded). Candidate-only → human-gated promotion → install.

## 7. Staleness + lifecycle

A skill flips to `stale` when ANY of:
- a marker in its `depends_on_markers` changes coverage (hook into `validate_raw_coverage`);
- a re-eval at a new HEAD drops its `gold_score` below the quality floor;
- a competing skill scores higher on the same form (→ `superseded_by`).

A CI/scheduled "re-score all skills at HEAD" job flips statuses and emits alerts. Deprecate, never
delete (ADR-0003 + "deprecate instead"). Contract-lock drift (§11) is an additional staleness trip.

## 8. Gold / eval anchor (the underweighted prerequisite)

Gap detection and "pick the best" are meaningless without a **per-form quality anchor**. Generalize
the existing seed (Ps 23, Rom 7–8, John 1) to **≥1 gold passage per seed form**, each with a
hand-verified expected chunking. Gold sets gate: (a) skill scoring, (b) the quality floor in gap
detection, (c) staleness re-eval. This is a gating dependency, built alongside — not after.

## 9. Build sequencing (smallest first increment)

1. **Extract 4 existing strategies → seed registry** behind `apply()` iface; registry lookup
   replaces the genre branch. **Acceptance: leaderboard score stays ≥ 88.5** (pure refactor).
2. **SKILL_METADATA + graph index** for those 4 skills (ported schema).
3. **Per-form gold sets** for the ~8 `book_genres` genres already in use.
4. **Form-detector v0** (marker-driven) emitting candidate descriptors; wire into routing.
5. **Gap detector + alert artifact**; **per-form leaderboard**.
6. Only then: open the first **skill bake-off** for a weak form.

Each step is independently shippable and gate-green; none requires the full vision up front.

## 10. Risks / what I'd delete (question-the-requirement)

- **DELETE "thousands of skills now."** Premature proliferation is the real risk. Start with ~8–12.
- **DELETE heavy malicious-skill scanning for v1** — internal first-party skills don't need the
  full LawFirm quarantine/static/semantic scanner yet. Keep the *hook* for when external skills
  arrive; don't build the scanner on day one.
- **DON'T let LLM form-detection run unbounded** — deterministic markers must dominate; LLM is a
  tiebreaker with recorded confidence, else chunking becomes non-reproducible (violates "chunks are
  derived, deterministic").
- **DON'T spin up 5 repos** like LawFirm OS yet — start as **planes (folders) within this repo**
  (`skills/chunking/`, `config/chunking/forms/`, `pipelines/chunking/orchestrator.py`); split into
  separate repos only if/when it actually needs independent release cadence.
- **Risk: form taxonomy bikeshedding.** Mitigate by sourcing it from established form-criticism
  (Gunkel/form-critical genres) and the governance repo's classification vocabulary, not invented.

## 11. What I'd reuse from LawFirm OS vs. build new for Scripture

**Reuse near-verbatim (port the pattern):**
- `SKILL_METADATA.json` schema — `address` URN, `version`, `lifecycle_state`, `risk_tier`,
  `capabilities/inputs/outputs`, `quality_score_ref`, **`graph_node_ref`**, **`supersedes/
  superseded_by/combines_with`**, `recommended_update_policy: human_gate`, timestamps.
- Registries: `skill-agent-graph-index.json` (the knowledge graph), `skill-agent-lifecycle-
  policy-registry.json`, `skill-agent-quality-scoring-registry.json`, `skill-quality-rubric.json`.
- The supply-chain loop `find → quarantine → scan → grade → approve → install`, with the
  **grade → approve → install** + **candidate-only `draft-skill`** + **`detect-skill-gaps`** parts
  adopted immediately; quarantine/scan deferred until external skills arrive.
- `contracts.lock.json` SHA-pinned contract surface, **fail-closed on drift** — excellent
  staleness/consistency primitive between the form-taxonomy (substrate) and the skills/orchestrator.
- Doctrine: `SKILL_QUALITY_DOCTRINE.md` (10-point standard + rubric), `ALGORITHM_ELEGANCE_DOCTRINE`,
  Musk algorithm (question → delete → simplify → accelerate → automate) as the skill approval bar.
- Three-plane mental model: **substrate (control)** / **skills-registry (definition, candidate)** /
  **orchestrator (execution, read-only consumer)** — but as folders here, not 5 repos (see §10).

**Build new (Scripture-specific):**
- The **form-detector** (USFM-marker-driven; nothing in LawFirm corresponds to literary form).
- The **per-form gold sets** and per-form leaderboard scoring.
- Seeding the registry with the **4 existing chunker strategies**.
- The **form taxonomy** itself (form-critical genres), and the marker→form evidence rules.

**Strongest disagreement with the owner's framing:** "the solution is mass customization /
thousands of skills." For the biblical canon that over-states the cardinality and risks
fragmentation. The real solution is **bounded form-typing + a registry that *can* scale** — route by
a small set of forms, and only let skill count grow when genuinely new corpora/languages/eras
demand new forms. Mass *customization* yes; mass *proliferation* no.
