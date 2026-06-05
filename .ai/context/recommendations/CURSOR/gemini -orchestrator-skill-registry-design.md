# Chunking Orchestrator + Skill Registry — Cursor Composer 2.5 Design

**Author:** Cursor Composer 2.5 (independent; blind to CLAUDE/CODEX parallel designs)  
**Date:** 2026-06-05  
**Mode:** explore/plan — proposal only; no chunker refactor, no canonical/raw mutation  
**Baseline to protect:** `eval/LEADERBOARD.md` composite **88.5** (claude-opus-4.8 pass 2)

---

## Design thesis

The current `chunker.py` is a **single dispatch function** (`chunk_book`) keyed by nine book-level genres. That works for Pass 2 (88.5) but conflates three separable concerns:

1. **What shape is this passage?** (form — evidenced by USFM markers + local context)
2. **Which algorithm handles that shape?** (skill — patchwork, competing implementations)
3. **Did the output pass gates?** (eval — hard gates + composite, human promotion)

The orchestrator is a **thin, deterministic routing shell** around existing chunk logic. It does not become an agent runtime (per `MASTER_CONTEXT.md` three-plane separation). Skills live in-repo as versioned, eval-scored packages; the orchestrator reads a pinned registry, classifies each **chunking unit** (not whole books), invokes the winning skill, and emits provenance-rich **candidate** chunks.

**Question the requirement, then delete:** We do not need thousands of chunking skills for Protestant WEB. We need a **bounded form taxonomy (~35–45 forms)**, a **small competing set per form (2–8 skills)**, and **scale in the index/graph metadata** — not skill explosion. Real growth pressure is multi-translation witnesses and source-language boundaries (WLC/SBLGNT), not literary micro-genres.

---

## 1. Form taxonomy

### Principle

Forms are **routing labels backed by USFM marker evidence**, not free-form literary criticism. Each form maps to one or more chunking skills. Forms are registered in an allowlist (orchestrator fail-closed pattern); unknown compositions trigger gap detection (§6).

### Tier A — Marker-composition profiles (primary, deterministic)

Derived from markers that **actually appear** in `RAW_SOURCE_INVENTORY.md` / `usfm_marker_coverage.yaml`:

| Form ID | USFM / structural signature | Approx. prevalence (WEB) | Notes |
|---------|----------------------------|--------------------------|-------|
| `prose_paragraph` | `\p`/`\m`/`\mi`/`\pi1` dominant, no `\q*` | ~60% of verses | Default prose |
| `prose_heading_bounded` | `\ms1`/`\s1` + prose | section-scoped | Strong boundary |
| `prose_list` | `\li1`/`\ili` | 170 markers | Legal/genealogy lists |
| `poetry_single_colon` | `\q1` only, short chapter | many psalms | Whole-unit candidate |
| `poetry_indented` | `\q1` + `\q2` | 23k+ lines | Two-level poetry |
| `poetry_stanzaed` | `\q*` + `\b` stanza breaks | 1,070 `\b` | Ps 119-style splits |
| `poetry_acrostic_sectioned` | `\q*` + interior `\d` (not v1) | Ps 119, Lam | Pass-2 split logic |
| `psalm_with_superscription` | `\d` at chapter open + `\q*` | 139 `\d` | Superscription glued |
| `poetry_with_selah` | `\qs` inline | 148 | Rubric metadata carry |
| `speaker_dialogue` | `\sp` | 33 | Job-style |
| `words_of_jesus_block` | `\wj` span ≥N verses | 4,580 wj tokens | Gospel red-letter units |
| `gospel_pericope_heading` | `\s1` in gospels + narrative `\p` | gospel books | Pericope boundary |
| `footnote_dense` | `\f`/`\fqa` density > threshold | 3,710+519 | Variant/footnote carry |
| `crossref_annotated` | `\x` present | 726 | Editorial, not graph edge |
| `intro_block` | `\is1`/`\ip` | book fronts | Usually excluded from chunks |
| `major_title_block` | `\mt1`/`\mt2`/`\mt3` | 132 | Book front matter |

### Tier B — Book-genre overlays (secondary, curated)

Reuse `book_genres.yaml` keys as **weak priors** when Tier A is ambiguous:

| Overlay | Books (examples) | Refines Tier A into |
|---------|------------------|---------------------|
| `overlay_psalms` | Ps, Song, PrMan, Ps151, Lam | poetry_* forms |
| `overlay_wisdom_saying` | Prov, Eccl, Sir, Wis | `wisdom_saying_cluster` |
| `overlay_law_statute` | Lev, Deut (law sections) | `law_statute_unit` |
| `overlay_prophet_oracle` | Isa–Mal, Bar | `prophet_oracle_unit` |
| `overlay_epistle_argument` | Rom–Jude | `epistle_argument_unit` |
| `overlay_apocalypse_vision` | Rev, 2Esd | `apocalypse_vision_cycle` |
| `overlay_narrative_scene` | Gen–Esth, Macc | `narrative_scene_unit` |
| `overlay_gospel_discourse` | Matt–John | `gospel_discourse_unit` |

### Tier C — Extension bucket (early-church / future corpora)

| Form ID | Trigger | Status |
|---------|---------|--------|
| `patristic_homily` | non-USFM TEI / no `\q*` poetry profile | gap until skill authored |
| `patristic_letter` | epistolary structure without OSIS book map | gap |
| `apocryphon_vision` | apocalyptic without standard `\c` rhythm | gap |
| `uncovered_marker_profile` | `validate_raw_coverage.py` new marker | **hard gap** |

### Realistic counts

| Corpus scope | Distinct forms | Competing skills per form (patchwork) | Total skill packages (upper bound) |
|--------------|----------------|---------------------------------------|-------------------------------------|
| WEB Protestant + deuterocanonical (now) | **38–42** registered forms | 1–4 early; 2–8 mature | **80–200** |
| + WLC / SBLGNT witnesses (phase 2) | +8–12 forms | 2–5 per form | +40–80 |
| + early-church writings | +10–15 forms | 1–3 until gold exists | +30–60 |
| **Mature Protestant-focused** | ~45 | ~3 avg | **~150** — not thousands |

Thousands of registry **nodes** (eval runs, draft variants, deprecated versions) yes; thousands of **distinct chunking algorithms** no — that is over-engineering unless each verse gets its own skill (rejected).

---

## 2. Form-detection stage

### Pipeline (deterministic-first)

```text
TextSpan window (verse-grained today; clause-grained later)
  → USFM marker profile (from BoundaryClaim sidecar)
  → marker-composition classifier (Tier A rules)
  → optional book-genre overlay (Tier B prior from book_genres.yaml)
  → FormDetectionCandidate record (trust_zone=candidate)
  → orchestrator routing (§5)
```

### Deterministic rules (v0)

1. **Window:** For routing, use a sliding **section window** — from prior heading/` \ms1`/` \s1` or chapter start to next heading or budget overflow point. Verse-grained units from `build_units()` remain the atomic text carriers.
2. **Marker profile:** Count chunker-relevant markers in window per `usfm_marker_coverage.yaml`.
3. **Decision tree (ordered):**
   - If `\q1`/`\q2`/`\q3` ≥ 50% of structural markers → poetry branch (`poetry_*`).
   - If `\d` at window start → `psalm_with_superscription`.
   - If interior `\d` + `\b` → `poetry_acrostic_sectioned`.
   - If `\b` without acrostic `\d` → `poetry_stanzaed`.
   - If `\sp` → `speaker_dialogue`.
   - If `\wj` spans ≥ 3 consecutive verses in gospels → `words_of_jesus_block`.
   - If `\li1`/`\ili` dominant → `prose_list`.
   - Else if `\s1`/`\ms1` bounded → `prose_heading_bounded`.
   - Else → `prose_paragraph`.
4. **Overlay refinement:** If `book_genres.yaml` says `wisdom` and window < 400 tokens with parallelism markers → upgrade to `wisdom_saying_cluster`.
5. **Confidence:** `confidence = 1.0` when exactly one Tier A rule fires unambiguously; `0.7–0.9` when overlay breaks tie; `< 0.6` → emit multiple `FormDetectionCandidate` rows (top-2 forms) and flag `needs_review`.

### LLM judgment (exception path only)

- **When:** `confidence < 0.6`, or competing forms within 0.1 score, or new marker profile (Tier C).
- **Output:** Additional `FormDetectionCandidate` with `generation_method: llm-v1`, `trust_zone: candidate`, never merged into asserted routing without human correction.
- **Forbidden:** LLM may not invent form IDs outside registry allowlist; must pick from registered forms or emit `form_id: UNKNOWN` → gap (§6).

### Provenance record (`FormDetectionCandidate`)

Emitted to `data/candidate/form_detections/<run_id>.jsonl`:

```json
{
  "id": "form-det--eng-web--Ps.23.1--Ps.23.6--001",
  "type": "FormDetectionCandidate",
  "osis_start": "Ps.23.1",
  "osis_end": "Ps.23.6",
  "form_id": "poetry_single_colon",
  "confidence": 1.0,
  "detection_method": "deterministic_marker_profile_v1",
  "marker_evidence": {"q1": 6, "d": 1, "b": 0},
  "book_genre_prior": "psalms",
  "alternates": [],
  "trust_zone": "candidate",
  "status": "active"
}
```

Human correction: edit `form_id` or approve → promoted to `data/candidate/form_detections/approved/` (still candidate until chunk promotion). Never writes to `data/canonical/`.

---

## 3. Skill registry

### Location (knowledge + control plane, not execution)

```text
config/chunking/skills/                    # registry root (pinned)
  registry/
    chunking-skill-toc.yaml                # human TOC (form → skill ids)
    chunking-skill-graph-index.json        # machine graph (LawFirm pattern)
    chunking-skill-lifecycle-policy.json
    chunking-skill-quality-scoring.json
    contracts.lock.json                    # SHA-pinned registry bundle
  approved/
    <skill_id>/
      SKILL.md                             # agent instructions + method
      SKILL_METADATA.json                  # ported schema (adapted)
      algorithm.py                         # deterministic chunk fn entrypoint
      policy_overlay.yaml                  # optional budget/boundary overrides
      tests/
        fixtures.jsonl
        gold_expectations.yaml             # per-skill micro-gold
  candidate/
    <skill_id>/                            # multi-agent bake-off drafts
  quarantine/
    <skill_id>/                            # failed eval / stale
  deprecated/
    <skill_id>/                            # superseded, retained for audit
```

Big chunk outputs stay gitignored under `data/derived/chunks/variants/` (existing pattern). Only scorecards + registry metadata commit (matches `eval/chunking_runs/` today).

### `SKILL_METADATA.json` (one chunking skill)

Port LawFirm `SKILL_METADATA.json` **verbatim in shape**, Scripture-specific in content:

```json
{
  "id": "psalm-whole-then-stanza-v2",
  "kind": "chunking_skill",
  "name": "Psalm whole-then-stanza split",
  "owning_repo": "logos-scripture-graph",
  "owning_plane": "knowledge_plane",
  "address": "logos.chunking.psalm.whole-then-stanza.v2.candidate",
  "version": "0.2.0",
  "lifecycle_state": "candidate",
  "risk_tier": "low",
  "capabilities": ["chunk_psalm", "preserve_superscription", "stanza_split_at_b"],
  "inputs": ["form_detection", "text_spans", "boundary_claims", "chunking_policy"],
  "outputs": ["retrieval_chunks", "context_packets"],
  "side_effect_class": "derived_emit_only",
  "data_classes": ["scripture_text_derived"],
  "approval_required": true,
  "form_ids": ["poetry_stanzaed", "poetry_acrostic_sectioned", "psalm_with_superscription"],
  "source_markers_required": ["q1", "b", "d"],
  "book_genre_overlays": ["overlay_psalms"],
  "eval_scorecard_ref": "eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json",
  "quality_score_ref": "chunking-skill-quality-score://psalm-whole-then-stanza-v2/latest",
  "graph_node_ref": "chunking-skill-graph://skill/psalm-whole-then-stanza-v2",
  "supersedes": ["psalm-whole-only-v1"],
  "superseded_by": null,
  "combines_with": [],
  "recommended_update_policy": "human_gate",
  "staleness_triggers": ["chunking_policy_version_bump", "gold_regression", "marker_registry_change"],
  "created_at": "2026-06-05T00:00:00+00:00",
  "updated_at": "2026-06-05T00:00:00+00:00"
}
```

### Skill body contract

Each `algorithm.py` exposes:

```python
def chunk_unit(
    units: list[dict],          # build_units() shape
    form_detection: dict,
    policy: dict,
    budgets: dict,
) -> tuple[list[dict], list[dict]]:  # chunks, context_packets
    ...
```

Skills are **pure**: no raw USFM mutation, no canonical writes, deterministic given inputs.

---

## 4. Knowledge graph / TOC

### TOC (`chunking-skill-toc.yaml`)

Human-navigable, versioned, small enough to read in review:

```yaml
version: 0.1.0
forms:
  poetry_stanzaed:
    description: "Poetry with \\b stanza breaks"
    preferred_skills: [psalm-whole-then-stanza-v2, psalm-whole-then-stanza-v1]
    fallback_skill: prose-paragraph-safe-v1
  prose_paragraph:
    preferred_skills: [prose-heading-paragraph-v1]
    fallback_skill: prose-paragraph-safe-v1
```

### Graph index (`chunking-skill-graph-index.json`)

Port LawFirm `skill-agent-graph-index.json` structure:

- **Node kinds:** `chunking_skill`, `form`, `evaluator`, `gold_set`, `policy_bundle`
- **Edge types:** `recommended_for`, `handles_form`, `supersedes`, `superseded_by`, `combines_with`, `fills_gap`, `validated_by`, `stale_after`
- **Sharding:** enabled when nodes > 500 (not 10k — Scripture scope is smaller)
- **Minimum node fields:** same as LawFirm (`id`, `kind`, `owning_plane`, `address`, `version`, `lifecycle_state`, `quality_score_ref`)

### Navigation algorithm

```text
1. Load contracts.lock.json → verify registry SHA (fail-closed)
2. Lookup form_id in TOC → preferred_skills ordered by quality_score desc, lifecycle_state (preferred > active > candidate)
3. Graph expand: include `combines_with` only for post-processors (e.g., context-packet-emitter)
4. Filter: lifecycle_state ∉ {quarantined, retired, superseded}
5. Filter: skill.form_ids contains form_id
6. Return ordered candidate list for §5 selection
```

Orchestrator never invents skill IDs — allowlist from graph index only (LawFirm route allowlist pattern).

---

## 5. Routing / orchestration

### Unit flow

```text
corpus iteration (book order)
  → section windows
  → form detection (§2) → FormDetectionCandidate
  → skill enumeration (§4)
  → skill selection (eval winner per form, or explicit override)
  → skill.chunk_unit() → RetrievalChunk candidates + ContextPackets
  → append routing ledger line
  → evaluate_chunks.py scorecard
```

### Skill selection (patchwork winner)

For each `(form_id, source_text_id)` tuple:

1. **Default:** Highest `quality_score` among `lifecycle_state ∈ {preferred, active}` skills that handle `form_id`.
2. **A/B override:** Human or CI can pin `skill_pin.yaml` for regression (`skill_id: psalm-whole-then-stanza-v2` for form `poetry_stanzaed`).
3. **Tie-break:** Lower `psalms_fragmented` from last scorecard, then closer `tok_p50` to 600.
4. **Per-text override:** If skill A beats B on gold set for Psalms but B wins on Romans, registry holds per-form winners — **not** one global chunker.

### Relation to existing `chunker.py` — **refactor, not rebuild**

| Keep | Extract | Add |
|------|---------|-----|
| `build_units()`, `make_chunk()`, `make_context_packet()` | `chunk_book()` psalm branch → `skills/approved/psalm-whole-then-stanza-v1/` | `pipelines/chunking/orchestrator.py` |
| `load_genres()`, `load_budgets()`, marker constants | prose branch → `skills/approved/prose-heading-paragraph-v1/` | `pipelines/chunking/detect_form.py` |
| Genre dispatch as **overlay prior** | `effective_budgets()` wisdom scale → skill `policy_overlay.yaml` | `config/chunking/skills/registry/*` |
| CLI `--passages --witnesses --boundary-claims` | | append-only `data/candidate/chunking_ledger/<run_id>.jsonl` |

**Compatibility shim:** `chunker.py` main() calls orchestrator with a single skill pin matching current monolith behavior → **byte-identical output** for pass-2 regression until skills extracted.

### Routing ledger (LawFirm append-only JSONL)

```json
{
  "run_id": "orch-20260605T120000Z",
  "osis_start": "Ps.23.1",
  "osis_end": "Ps.23.6",
  "form_id": "poetry_single_colon",
  "form_confidence": 1.0,
  "skill_id": "psalm-whole-then-stanza-v2",
  "skill_version": "0.2.0",
  "selection_reason": "quality_score_rank_1",
  "alternates_considered": ["psalm-whole-only-v1"],
  "chunking_policy_version": "chunk-policy-v0.1.0",
  "trust_zone": "candidate"
}
```

---

## 6. Gap detection + self-extension

### Exact triggers ("no skill fits")

| Trigger ID | Condition | Severity |
|------------|-----------|----------|
| `GAP-NO-SKILL` | TOC returns empty `preferred_skills` for `form_id` | high |
| `GAP-UNKNOWN-FORM` | Detection yields `UNKNOWN` or confidence < 0.4 | high |
| `GAP-EVAL-FAIL` | All candidate skills for form fail hard gates on evaluate_chunks | high |
| `GAP-MARKER` | `validate_raw_coverage.py` adds `UNHANDLED` marker | **blocking** |
| `GAP-GOLD` | No gold set covers `form_id` (cannot score new skill) | medium |
| `GAP-STALE` | Only skills for form are `quarantined`/`stale` | medium |
| `GAP-REGRESSION` | Active skill loses >5 composite points vs incumbent | medium |

### Alert artifact (`ChunkingSkillGapCandidate`)

`data/candidate/chunking_gaps/<gap_id>.json`:

```json
{
  "schema_version": "1.0",
  "record_type": "chunking_skill_gap_candidate",
  "candidate_only": true,
  "requires_human_approval": true,
  "gap_id": "gap-poetry_stanzaed-001",
  "form_id": "poetry_stanzaed",
  "trigger": "GAP-EVAL-FAIL",
  "observed_pattern": "Ps 119 tok_max=4847 exceeds OVERSIZE_LIMIT; psalms_fragmented=10",
  "osis_exemplars": ["Ps.119.1", "Ps.119.176"],
  "marker_evidence": {"b": 22, "d": 22, "q1": 176},
  "why_existing_skills_insufficient": "No active skill passes hard gates with acceptable tok_max",
  "support_count": 3,
  "recommended_skill_id": "psalm-acrostic-stanza-v3-draft",
  "skill_need_type": "new_skill_variant"
}
```

Human alert: open GitHub issue / handoff task — **no auto-promote**.

### Multi-agent bake-off (author new skill)

Port LawFirm `detect-skill-gaps` + `draft-skill` loop:

```text
ChunkingSkillGapCandidate
  → draft-skill (N agents, N ∈ {2,3}, configured in handoff)
      each emits skills/candidate/<agent>_<skill_id>/
  → evaluate_chunks.py on each variant (same inputs, scorecard-dir)
  → leaderboard.py ranks
  → human picks winner OR fuse
```

**Pick-best:** Promote one candidate to `approved/` after human `--approve` (LawFirm `approve_skill` explicit flag pattern).

**Fuse:** If agent A wins stanza splits and agent B wins superscription handling, human authors `psalm-fused-v1` combining proven code paths — not LLM-merge of prompts. Fusion is a **new skill package** with `combines_with` edges to parents, re-evaluated on full gold.

### Auto-forbidden (LawFirm lifecycle policy)

- `activate` without human approval
- `promote_preferred` without gold pass
- Delete deprecated skills (deprecate only)
- Write to `data/canonical/`

---

## 7. Staleness + lifecycle

### Lifecycle states (port LawFirm registry)

`draft` → `candidate` → `active` → `preferred` → `deprecated` → `superseded` → `retired`  
Plus: `quarantined` (eval/security/hard-gate failure)

Transitions: `candidate→active` requires human; `active→quarantined` automatic on hard-gate fail.

### Precise staleness conditions

| Signal | Makes skill stale when | Auto-action |
|--------|------------------------|-------------|
| `chunking_policy_version` bump | skill.policy_overlay pins old version | mark `stale_policy`; block `preferred` |
| `usfm_marker_coverage.yaml` change | `source_markers_required` no longer satisfied | `quarantined` |
| Gold regression | any hard gate flips false on committed gold | `quarantined` |
| Incumbent beat | new scorecard beats by ≥3 composite on same corpus pin | recommend `supersedes` edge |
| Age | no eval run in 90 days for `preferred` skill | `stale_recency` flag (not quarantine) |
| Form registry change | `form_id` deprecated or split | `stale_form_mapping` |

### Re-eval cadence

- **Every chunker PR:** full `evaluate_chunks.py` + `leaderboard.py` on pinned corpus build.
- **Weekly (CI optional):** recency check only.
- **On `chunking_policy.yaml` or marker registry change:** mandatory re-eval all `active`+ skills touching affected `form_ids`.
- **On new raw source drop:** `scan_raw_sources.py` → marker gap check → targeted re-eval.

Stale skills remain in registry (audit trail); orchestrator skips them in routing.

---

## 8. Gold / eval anchor

### Why gold gates gap detection

Without per-form gold, new skills cannot be distinguished from regressions — gap detection would false-positive constantly. Gold sets are the **objective anchor** for patchwork winner selection.

### Gold tiers

| Tier | Set | Purpose | Gates |
|------|-----|---------|-------|
| **G0 — global hard** (existing) | Ps 23 one chunk; Gen 1 no mid-sentence; 0 USFM leaks; 0 book crossings; 100% sentence integrity | Leaderboard eligibility | **blocking** |
| **G1 — form micro** | Per-form 1–3 OSIS windows in `skills/approved/*/tests/gold_expectations.yaml` | Skill-level CI | blocking for `candidate→active` |
| **G2 — book review** | Psalms, Prov, Job, Isa, Dan, Matt, John, Rom, Heb, Rev (per CHUNKING_DESIGN) | Human review loop | advisory |
| **G3 — corpus pin** | Frozen passage subset hash in `eval/corpus_pins/web-v1.json` | Regression composite | blocking for `active→preferred` |

### Minimum gold to enable gap closure

Before accepting a `ChunkingSkillGapCandidate` bake-off for form `F`:

1. At least **one G1 micro-gold** exemplar with `marker_evidence` matching `F`
2. G0 hard gates wired in `evaluate_chunks.py` (already true)
3. Scorecard committed to `eval/chunking_runs/`

### Metrics inheritance

Keep existing `evaluate_chunks.py` metrics + add per-form slices:

- `gold_<form_id>_pass: bool`
- `form_skill_fit: float` (fraction of form windows where boundary_basis matches skill contract)

---

## 9. Build sequencing

Smallest increments that **do not regress 88.5**:

### Increment 0 — Documentation + registry stub (this proposal)

- Add `config/chunking/skills/registry/` with TOC, graph index, lifecycle policy
- Register **one** skill metadata wrapping current monolith (`monolith-v1-pass2`)
- No pipeline change; gates stay green

### Increment 1 — Ledger + form detection (read-only sidecar)

- `detect_form.py` emits `FormDetectionCandidate` JSONL alongside existing chunker
- `chunker.py` unchanged; orchestrator not in hot path
- Validate: form detections cover ≥95% of chunks with confidence ≥0.7

### Increment 2 — Orchestrator shim

- `orchestrator.py` calls existing `chunk_book()` via `monolith-v1-pass2` skill pin
- Prove byte-identical chunks vs current pass-2 output on corpus pin
- **Gate:** composite ≥ 88.5, all hard gates pass

### Increment 3 — Extract psalm skill

- Move psalm branch to `psalm-whole-then-stanza-v2` (already Pass 2 logic)
- Prose stays in monolith temporarily
- **Gate:** composite ≥ 88.5 (expect match; psalms_fragmented ≤ 10)

### Increment 4 — Extract prose + wisdom skills

- `prose-heading-paragraph-v1`, `wisdom-saying-cluster-v1`
- Remove inline `chunk_book` branches
- Add G1 micro-gold per form

### Increment 5 — Gap factory + bake-off harness

- `detect_chunking_gaps.py` (port LawFirm gap detector patterns)
- `draft_chunking_skill.py` for candidate scaffolding
- Wire to handoff / human approval

### Increment 6 — Multi-translation readiness

- Form detection reads witness-specific marker profiles
- Skills declare `source_text_id` compatibility

**Do not start** with LLM form detection, full graph UI, or thousands-entry registry.

---

## 10. Risks / what I'd delete

### Over-engineered / premature (delete or defer)

| Owner vision element | Verdict | Alternative |
|---------------------|---------|-------------|
| Thousands of chunking skills | **Delete as goal** | ~150 skills max; version/eval nodes scale, not algorithms |
| LLM-first form detection | **Defer** | Deterministic marker profiles cover WEB; LLM for Tier C only |
| Full knowledge graph UI | **Defer** | YAML TOC + JSON index sufficient until >100 active skills |
| Multi-agent bake-off on every PR | **Delete** | Bake-off only on `ChunkingSkillGapCandidate` triggers |
| Skill fusion via LLM | **Delete** | Human-authored code fusion with new skill package + re-eval |
| Orchestrator as agent runtime | **Reject** | Stays in knowledge plane; execution plane is separate per ADR |
| Per-verse form detection records | **Delete** | Section-window granularity matches chunk units |
| Auto-promote winning skill | **Reject** | Human promotes; matches existing leaderboard pattern |

### Risks

1. **Form/book-genre double-counting** — mitigated by Tier A markers trumping Tier B overlay.
2. **Regression during extract** — mitigated by byte-identical shim (Increment 2) before branch extraction.
3. **Gold set lag** — blocks skill velocity; accept intentional friction.
4. **Registry drift** — mitigated by `contracts.lock.json` fail-closed validation in CI.
5. **Scope creep to early-church** — Tier C forms registered but quarantined until raw source + gold exist.

### Strongest "question requirements" delete

**Delete the assumption that literary form is the primary routing axis independent of USFM.** For WEB, routing should be **marker-composition first**; literary labels (oracle, pericope, argument unit) are overlays on prose/poetry profiles, not a parallel taxonomy. This avoids duplicating `book_genres.yaml` at pericope level without new evidence.

---

## 11. What I'd reuse from LawFirm OS vs. build new for Scripture

### Port verbatim (or near-verbatim)

| LawFirm artifact | Scripture destination | Adaptation |
|------------------|----------------------|------------|
| `SKILL_METADATA.json` field shape | `config/chunking/skills/approved/*/SKILL_METADATA.json` | `kind: chunking_skill`, `form_ids`, `source_markers_required` |
| `skill-agent-graph-index.json` structure | `chunking-skill-graph-index.json` | Smaller shard threshold (500) |
| `skill-agent-lifecycle-policy-registry.json` | `chunking-skill-lifecycle-policy.json` | Remove security quarantine triggers; add eval hard-gate quarantine |
| `skill-agent-quality-scoring-registry.json` | `chunking-skill-quality-scoring.json` | Swap legal metrics for chunk metrics (sentence_integrity, psalms_fragmented, tok_p50 fitness) |
| `contracts.lock.json` pinning pattern | `config/chunking/skills/registry/contracts.lock.json` | Pin registry bundle SHA, not external substrate repo |
| `detect-skill-gaps` → gap candidate JSONL | `detect_chunking_gaps.py` | Cluster source = eval failures + routing misses, not Exception Lake |
| `draft-skill` scaffolding | `draft_chunking_skill.py` | Algorithm.py stub + gold_expectations template |
| `approve_skill --approve` explicit gate | human promotion script | No skill reaches `active` without human flag |
| Append-only audit ledger | `data/candidate/chunking_ledger/` | Routing decisions, not installs |
| Orchestrator **allowlist + fail-closed** | form_id + skill_id allowlists in orchestrator | No invented forms/skills |
| `find → quarantine → scan → grade → approve` | `discover → candidate → eval → approve → active` | Skip malicious-code scan; add chunk eval grade |

### Build new for Scripture (not portable from LawFirm)

| Concern | Scripture-specific build |
|---------|-------------------------|
| Form detection | USFM marker-composition classifier from `RAW_SOURCE_INVENTORY.md` |
| Skill algorithm | `chunk_unit()` on TextSpan/boundary claims, not legal artifact parsers |
| Gold sets | OSIS-anchored per-form windows (Ps 23, Rom 7–8, John 1, Ps 119 acrostic) |
| Staleness | `chunking_policy_version`, marker registry, USFM scan drift |
| Quality metrics | `evaluate_chunks.py` / `leaderboard.py` composite (existing) |
| Trust zones | `candidate` chunks; no asserted promotion from skill output |
| Concordance carry | footnote/crossref/`has_lexeme_alignment` in chunk records |
| Canon | `CanonProfile` on passages — skills must not assert canon |
| Source-language path | Future WLC/SBLGNT forms — LawFirm has no equivalent |

### Do NOT port

- Malicious-skill security scanner / semantic intent scan (irrelevant to deterministic chunk algorithms)
- Legal bundled-reference freshness validator (Scripture staleness is policy/marker/gold-based)
- Exception Lake / route_id / event_class taxonomy (different domain)
- Skill installation to `.agents/skills` (chunk skills are Python modules in-repo, not Cursor agent skills)
- Substrate write prohibition → already matches logos `MASTER_CONTEXT` knowledge-plane ownership

### Revised sections after LawFirm study

- **§3:** Added explicit `contracts.lock.json`, quarantine/candidate/approved directory layout matching LawFirm supply chain.
- **§4:** Graph index ported with LawFirm edge types; added `validated_by` for eval scorecards.
- **§6:** Gap factory explicitly ports `detect_skill_gaps` + `draft_skill` candidate-only pattern; fusion clarified as human code merge.
- **§7:** Lifecycle states and auto-actions copied from `skill-agent-lifecycle-policy-registry.json`; removed legal freshness.
- **§8:** Quality scoring weights adapted from `skill-agent-quality-scoring-registry.json` (task_success → gold pass rate, evidence_completeness → boundary_basis_cov).
- **§9:** Increment 0 now includes registry stub matching LawFirm `approved-skills.json` index pattern.

---

## Appendix: Mapping today’s monolith → initial skill registry

| Current `chunker.py` branch | Form(s) | Initial skill ID | Pass-2 scorecard |
|----------------------------|---------|------------------|------------------|
| `chunk_book` psalm/`is_poetry` | `poetry_*`, `psalm_with_superscription` | `psalm-whole-then-stanza-v2` | 88.5 composite |
| prose heading-bounded | `prose_heading_bounded`, `gospel_pericope_heading` | `prose-heading-paragraph-v1` | (shared) |
| `effective_budgets` wisdom | `wisdom_saying_cluster` | `wisdom-saying-cluster-v1` | (shared) |
| epistle context packets | `epistle_argument_unit` | `epistle-context-packet-v1` (post-processor) | (shared) |
| fallback / no boundary claims | `prose_paragraph` | `prose-paragraph-safe-v1` | v0 fallback |

---

*End of proposal. No canonical data mutated. Validation gates not run (markdown-only change).*
