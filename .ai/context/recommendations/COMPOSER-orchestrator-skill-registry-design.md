# Chunking Orchestrator + Skill Registry Design

**Author:** Cursor Composer 2.5  
**Date:** 2026-06-05  
**Mode:** explore/plan — proposal only; no chunker refactor in this task  
**Grounding:** `RAW_SOURCE_INVENTORY.md` (eng-web scan 2026-06-04), `chunker.py` v1 Pass-2 (88.5 leaderboard), LawFirm OS skill-registry + orchestrator patterns

---

## Design thesis

The current `chunker.py` already implements **nine book-level genre dispatch paths** with marker-aware Pass-2 logic (whole-psalm + `\b`/interior-`\d` stanza splits, heading-bounded prose, epistle context packets). The right move is **not** a monolith replacement or a thousand-skill explosion. It is a **thin orchestration shell** that:

1. Detects **literary form per segment** from real USFM markers (not book labels alone).
2. Selects the **best eligible chunking skill** from a registry via deterministic routing + eval scores.
3. Emits chunks with **form assignment + skill provenance** as candidate artifacts.
4. Detects gaps when routing fails or gold eval regresses, then runs the existing **multi-agent bake-off** (`evaluate_chunks.py` → `leaderboard.py`) to draft and rank new skills.

Skills are **parametric algorithms + instructions**, not one-off patches per passage. Scale comes from **form taxonomy × budget variants × source-family adapters**, not unbounded skill count.

---

## 1. Form taxonomy

### Principle

Route on **structural literary form** — the smallest set that changes chunking algorithm or forbidden-split rules. Forms are declared in a bounded registry; they are not invented at runtime.

### Protestant canon (WEB eng-web, marker-grounded)

Based on markers that **actually appear** in `RAW_SOURCE_INVENTORY.md` and `usfm_marker_coverage.yaml`:

| Form ID | Primary markers / signals | Books / prevalence | Chunking unit |
|---------|---------------------------|-------------------|---------------|
| `prose_paragraph` | `\p`, `\m`, `\mi`, `\pi1`, `\pc`, `\nb` | Default prose (narrative, law narrative, Acts) | Paragraph + sentence under budget |
| `prose_section` | `\ms1`, `\s1` heading opens section | Exodus–Kings, prophets, gospels | Heading-bounded section |
| `poetry_psalm_unit` | `\q1`/`\q2`/`\q3` dominant; chapter = psalm | Ps, Song, Lam, PrMan | Whole psalm; superscription kept |
| `poetry_stanza` | `\b` stanza break within psalm | Long psalms (esp. Ps 119) | Stanza at `\b` or interior `\d` |
| `poetry_acrostic_section` | Interior `\d` titles between stanzas | Ps 119, Lam acrostics | Section at interior `\d` (not v1 opening `\d`) |
| `wisdom_saying_cluster` | Short `\p` units, parallelism | Prov, Eccl, Sir, Wis | Tight budget (~0.45× policy scale) |
| `law_statute_block` | Dense legal `\p`/`\li1` | Lev, Deut | Legal unit; list-aware |
| `list_block` | `\ili`, `\li1` | Legal + epistolary lists | List item / cluster |
| `dialogue_speaker_turn` | `\sp` speaker label | Job (33×), limited elsewhere | Speaker-bounded turn |
| `gospel_pericope` | `\s1`/`\ms1` + narrative `\p` | Matt–John | Pericope / discourse block |
| `prophetic_oracle` | Section heading + oracle prose/poetry mix | Isa–Mal, Bar | Oracle or vision report |
| `epistle_argument` | Epistle book + `\p`; connector at chunk start | NT epistles | Argument / exhortation unit |
| `apocalyptic_vision` | Mixed prose + `\q*` in cycles | Dan, Rev, 2Esd | Vision cycle |
| `narrative_episode` | Book genre narrative + scene headings | Historical books | Scene / episode |

**Modifier annotations** (do not change primary router; attach to chunk metadata):

| Modifier | Marker | Handling |
|----------|--------|----------|
| `superscription_attached` | `\d` (139×) | Keep with psalm; never orphan |
| `words_of_jesus_span` | `\wj` (4,580×) | Tag chunk; optional sub-boundary hint in gospels |
| `selah_rubric` | `\qs` (148×) | Inline liturgical; carry in metadata |
| `variant_reading_sidecar` | `\fqa` (519×) | Textual-variant seed; never split driver |
| `footnote_carry` | `\f` (3,710×) | Refs per verse; no boundary effect |
| `editorial_crossref` | `\x` (726×) | Refs per verse; not graph edge |

### Early-church / patristic extension (+12–18 forms)

When non-USFM or lightly-USFM corpora land, add forms without collapsing into "generic prose":

| Form ID | Examples | Notes |
|---------|----------|-------|
| `patristic_homily` | Chrysostom, Augustine sermons | Section = pericope / lemma |
| `apologetic_treatise` | Justin, Athenagoras | Argument chapter |
| `pastoral_letter` | Ignatius, Polycarp | Epistle-like but different heading density |
| `martyrology` | Acts of martyrs | Episode + speech |
| `creed_confession` | Rule of Faith fragments | Short whole-unit |
| `dialogue_treatise` | Justin *Dialogue* | `\sp`-like speaker turns |
| `catena_commentary` | Chain citations | Citation-block boundaries |
| `lectionary_pericope` | Liturgical units | Pre-scoped addresses |
| `pseudepigrapha_vision` | Enoch, Jubilees | Apocalyptic cycle reuse |
| `gnostic_logion_collection` | Gospel of Thomas | Saying-per-line |
| `apocryphal_narrative` | Tob, Jdt (already in WEB) | Reuse narrative_episode |
| `prayer_liturgy` | Didache prayers | Short whole-unit |

### Realistic counts

| Corpus scope | Primary routing forms | Skill variants (budget/source) | Total installable skills |
|--------------|----------------------|-------------------------------|--------------------------|
| WEB Protestant + deuterocanonical (now) | **14** primary + **6** modifiers | 2–3 variants per primary form | **~35–45** at maturity |
| + early-church / patristic | +12–18 forms | 1–2 variants each | **~60–90** at maturity |
| "Thousands" scenario | Only if every form × translation × tradition × budget × experimental agent run is counted as a distinct skill — **discouraged** | Parametric `skill_id` + `variant_id` instead | Registry sharding at **>500 nodes** (LawFirm pattern) |

**Target:** ~40 approved skills for Protestant canon; ~80 after patristic expansion. Parametric variants collapse what would otherwise look like "thousands."

---

## 2. Form-detection stage

### Pipeline position

```text
canonical passages + witnesses + boundary_claims
  → segment builder (heading / chapter / book scopes)
  → form detector (deterministic)
  → [optional] form adjudicator (LLM, candidate-only)
  → FormAssignment artifact (candidate)
  → human promotion → canonical form assignments (future)
  → orchestrator routing
```

### Deterministic detector (required path)

Input per segment: ordered verse units with `markers` set (already built in `chunker.py` `build_units()`).

**Rule precedence** (first match wins; record all signals in `detection_evidence`):

1. **Book override table** — `config/chunking/book_genres.yaml` sets *prior* only, not final form.
2. **Marker dominance:**
   - `poetry_line` ratio > 0.6 of verses → `poetry_psalm_unit` if Ps/Song/Lam/PrMan else `poetry_stanza` candidate
   - `\sp` present → `dialogue_speaker_turn`
   - `\ili`/`\li1` majority → `list_block` or `law_statute_block` (book in Lev/Deut)
3. **Structure:**
   - `\ms1`/`\s1` at segment start → `prose_section` / `gospel_pericope` / `prophetic_oracle` (book-aware)
   - Epistle book sans poetry dominance → `epistle_argument`
   - Rev/Dan apocalypse book flag → `apocalyptic_vision`
4. **Fallback:** `prose_paragraph` or `narrative_episode` from book genre.

**Confidence:** deterministic rules emit `confidence: 1.0` with `method: "usfm_marker_rules_v1"`. Mixed-marker segments emit `confidence: 0.7–0.9` with explicit `ambiguity_flags[]` (e.g. `poetry_in_prose_book` for Isa, `\wj` density in gospels).

**Provenance fields** (every `FormAssignment`):

```json
{
  "type": "FormAssignment",
  "id": "form-assign--eng-web--Ps.23.1--Ps.23.6--candidate",
  "osis_start": "Ps.23.1",
  "osis_end": "Ps.23.6",
  "primary_form": "poetry_psalm_unit",
  "modifiers": ["superscription_attached"],
  "confidence": 1.0,
  "method": "usfm_marker_rules_v1",
  "detection_evidence": {
    "markers_present": ["q1", "q2", "d"],
    "book_prior": "psalms",
    "rule_id": "marker_poetry_dominance_v1"
  },
  "assertion_mode": "candidate",
  "trust_zone": "candidate",
  "status": "active"
}
```

### LLM adjudicator (optional, gated)

- **Trigger:** `confidence < 0.85` OR `ambiguity_flags` non-empty OR human-flagged gold disagreement.
- **Output:** revised `primary_form` as **separate** `FormAssignment` with `method: "llm_adjudication_v1"` — never overwrites deterministic record; human picks winner.
- **Forbidden:** LLM-only form with no deterministic shadow record (asserted/inferred separation).

### Human correction

- Artifacts live: `data/candidate/form_assignments/*.jsonl` (generated).
- Human promotes corrected rows to `data/canonical/form_assignments.jsonl` (future schema).
- Orchestrator reads canonical assignments first, else deterministic, never promotes automatically.

---

## 3. Skill registry

### What is a chunking skill?

A **reusable chunking method** = deterministic Python algorithm + `SKILL.md` instructions + metadata + gold fixtures. Not an LLM prompt alone.

### Repo layout

```text
config/chunking/
  form_registry.yaml              # bounded form taxonomy (§1)
  skill_lifecycle_policy.yaml     # ported states/transitions (§7)
  skill_quality_weights.yaml      # scoring weights (§7)

registry/chunking/
  skill-toc.json                  # human/agent TOC (flat index)
  skill-graph-index.json          # KG index (edges, sharding policy)
  approved-skills.json            # install list (LawFirm pattern)
  contracts.lock.json             # SHA-pinned policy + form registry surface

pipelines/chunking/skills/
  approved/
    <skill_id>/
      SKILL.md                    # agent instructions + output contract
      SKILL_METADATA.json         # port LawFirm schema (adapted)
      algorithm.py                # implements ChunkingSkill protocol
      tests/
        fixtures.jsonl            # mini gold per skill
  draft/                          # candidate skills from bake-off
  quarantine/                     # failed scan / boundary violation

data/candidate/chunking/
  skill_gap_alerts.jsonl
  skill_bakeoff_manifests/
```

### SKILL_METADATA.json schema (one skill)

Port LawFirm `SKILL_METADATA.json` **verbatim where possible**, Scripture-specific extensions marked:

```json
{
  "id": "chunk-skill-poetry-psalm-whole-v1",
  "kind": "chunking_skill",
  "name": "Whole psalm with stanza fallback",
  "owning_repo": "logos-scripture-graph",
  "owning_plane": "knowledge",
  "address": "logos.chunk.skill.poetry.psalm_whole.v1.approved",
  "version": "1.0.0",
  "lifecycle_state": "active",
  "risk_tier": "low",
  "capabilities": ["chunk", "boundary_emit"],
  "inputs": ["segment_units", "boundary_claims", "chunking_policy"],
  "outputs": ["retrieval_chunks", "context_packets"],
  "side_effect_class": "none",
  "data_classes": ["canonical_read", "derived_write"],
  "approval_required": true,

  "supported_forms": ["poetry_psalm_unit", "poetry_stanza", "poetry_acrostic_section"],
  "required_markers_any": ["q1", "q2", "q3"],
  "forbidden_split_markers": ["d"],
  "book_priors": ["Ps", "Song", "Lam", "PrMan", "Ps151"],
  "budget_profile": "default",
  "boundary_basis_emit": ["whole_psalm", "poetic_stanza", "psalm_superscription"],

  "quality_score_ref": "eval/chunking_runs/<latest-scorecard>",
  "graph_node_ref": "chunk-skill-graph://skill/chunk-skill-poetry-psalm-whole-v1",
  "supersedes": [],
  "superseded_by": null,
  "combines_with": [],

  "eval_gold_sets": ["gold/psalm23_one", "gold/psalm119_stanza"],
  "last_eval_at": "2026-06-05T12:21:44+00:00",
  "staleness_policy_ref": "config/chunking/skill_lifecycle_policy.yaml",

  "created_at": "2026-06-05T00:00:00+00:00",
  "updated_at": "2026-06-05T12:21:44+00:00",
  "notes": "Extracted from chunker.py Pass-2 poetry path; human-approved."
}
```

**Scripture-specific fields:** `supported_forms`, `required_markers_any`, `forbidden_split_markers`, `book_priors`, `budget_profile`, `boundary_basis_emit`, `eval_gold_sets`.

---

## 4. Knowledge graph / TOC

### TOC (`registry/chunking/skill-toc.json`)

Flat, agent-readable index — "table of contents" for orchestrator boot:

```json
{
  "registry_id": "chunking-skill-toc.v1",
  "forms": [
    {"form_id": "poetry_psalm_unit", "description": "...", "default_skill": "chunk-skill-poetry-psalm-whole-v1"}
  ],
  "skills": [
    {"skill_id": "chunk-skill-poetry-psalm-whole-v1", "path": "pipelines/chunking/skills/approved/chunk-skill-poetry-psalm-whole-v1", "lifecycle_state": "active"}
  ],
  "routing_policy": "best_eligible_by_eval_score"
}
```

### Knowledge graph (`registry/chunking/skill-graph-index.json`)

Port `skill-agent-graph-index.json` structure:

**Node kinds:** `form`, `chunking_skill`, `eval_gold_set`, `chunking_policy`, `boundary_marker`

**Edge types (subset):**

| Edge | Meaning |
|------|---------|
| `recommended_for` | skill → form |
| `requires` | skill → marker/policy |
| `validates` | gold_set → skill |
| `supersedes` / `superseded_by` | skill versioning |
| `combines_with` | skill fusion result |
| `fills_gap` | draft skill → gap alert |
| `bounded_by` | skill → `chunking_policy.yaml` version |

**Sharding:** enable at **>500 nodes** (`shard_path_pattern: registry/chunking/graph-shards/{form_id}.json`).

**Navigation algorithm:**

1. Load TOC + graph index + `contracts.lock.json` (fail closed on SHA drift).
2. Given `primary_form`, traverse `recommended_for` edges to eligible skills.
3. Filter: `lifecycle_state ∈ {active, preferred}`, not `superseded`, markers satisfied.
4. Rank by `quality_score_ref` composite (leaderboard), then policy tie-break (preferred > active > newest eval).

---

## 5. Routing / orchestration

### Flow

```text
verse units (document order)
  → segment (book/chapter/heading scopes)
  → FormAssignment (§2)
  → skill selector (graph + eval scores)
  → skill.algorithm.chunk(segment) → RetrievalChunk[] + ContextPacket[]
  → append orchestration ledger record
```

### Relation to existing `chunker.py` — **refactor, not rebuild**

| Layer | Action |
|-------|--------|
| `build_units()` | **Keep** — marker attachment unchanged |
| `chunk_book()` / `chunk_corpus()` | **Extract** into `skills/approved/*/algorithm.py` (one skill per genre path) |
| `chunker.py` CLI | **Thin wrapper** — default path calls orchestrator for backward compatibility |
| `book_genres.yaml` | **Demote** to book-level *prior* in form detector, not sole router |
| New `orchestrator.py` | **Add** — form detect → skill select → dispatch → provenance |

**Chunk provenance extensions** (additive fields on `RetrievalChunk`):

```json
{
  "primary_form": "poetry_psalm_unit",
  "chunking_skill_id": "chunk-skill-poetry-psalm-whole-v1",
  "chunking_skill_version": "1.0.0",
  "form_assignment_id": "form-assign--eng-web--Ps.23.1--Ps.23.6--candidate",
  "orchestration_run_id": "orch--20260605T120000Z"
}
```

### Orchestrator ledger (LawFirm pattern)

Append-only JSONL: `build/chunking/orchestration_ledger.jsonl`

Each record: `segment_id`, `form_assignment`, `skills_considered[]`, `skill_selected`, `reason_codes`, `policy_version`, `contract_sha`.

Deterministic classifier only in v1 — no LLM in orchestrator hot path.

### Skill selection tie-break

1. Hard eligibility (form match, markers, lifecycle).
2. Highest leaderboard composite on skill's `eval_gold_sets` (must pass hard gates).
3. `preferred` lifecycle over `active`.
4. Lowest `psalms_fragmented` for poetry forms.
5. Human override file: `config/chunking/skill_overrides.yaml` (osis ranges → skill_id).

---

## 6. Gap detection + self-extension

### Triggers for "no skill fits"

| Trigger ID | Condition | Severity |
|------------|-----------|----------|
| `NO_ELIGIBLE_SKILL` | Form detected but zero skills pass marker/lifecycle filter | high |
| `ROUTING_CONFLICT` | Multiple skills tie; override missing | medium |
| `GOLD_REGRESSION` | Selected skill fails hard gate on form's gold set | high |
| `UNKNOWN_FORM` | Detector returns `form_id: unknown` (future corpus) | high |
| `MARKER_UNCLASSIFIED` | Segment has marker not in `usfm_marker_coverage.yaml` | critical (CI should preclude) |
| `EVAL_DIVERGENCE` | Top-2 skills differ on gold boundary IDs | medium |

### Alert artifact (`data/candidate/chunking/skill_gap_alerts.jsonl`)

Port LawFirm `skill_gap_candidate` record shape:

```json
{
  "record_type": "skill_gap_alert",
  "candidate_only": true,
  "requires_human_approval": true,
  "gap_id": "gap--poetry_acrostic--Ps119--20260605",
  "trigger_id": "GOLD_REGRESSION",
  "primary_form": "poetry_acrostic_section",
  "osis_start": "Ps.119.1",
  "osis_end": "Ps.119.176",
  "observed_pattern": "Acrostic interior \\d sections split mid-stanza",
  "skills_tried": ["chunk-skill-poetry-psalm-whole-v1"],
  "recommended_skill_id": "chunk-skill-poetry-acrostic-v1-draft",
  "support_count": 1,
  "severity": "high",
  "created_at": "2026-06-05T12:00:00+00:00"
}
```

Human notification: append to `.ai/control/handoff_ledger.jsonl` + optional Slack (future).

### Multi-agent bake-off (reuse existing harness)

```text
skill_gap_alert
  → draft-skill (scaffold under skills/draft/<id>/)
  → N agents implement competing algorithm.py variants
  → each runs chunker CLI → evaluate_chunks.py --scorecard-dir
  → leaderboard.py ranks
  → human promotes winner to skills/approved/ + updates graph edges
```

**Pick-best-or-fuse:**

- **Pick-best:** default — highest eligible composite wins.
- **Fuse:** when top-2 are complementary (e.g. one wins Ps 23 whole-psalm, other wins Ps 119 stanza), emit `chunk-skill-fused-*` with `combines_with` edges and delegated sub-call per sub-form. Fusion is human-gated, not automatic.

**Forbidden:** draft skills self-promote; gap alerts do not mutate canonical source or `data/canonical/`.

---

## 7. Staleness + lifecycle

### Lifecycle states (port `skill-agent-lifecycle-policy-registry.json`)

`draft` → `candidate` → `active` → `preferred` → `deprecated` → `superseded` → `retired`  
Any → `quarantined` on hard safety/eval failure.

| Transition | Approval |
|------------|----------|
| draft → candidate | tests pass |
| candidate → active | **human required** |
| active → preferred | **human required** |
| active → superseded | **human required** |
| any → quarantined | hard gate fail / boundary violation |

### Staleness conditions (skill becomes `stale` flag, not auto-retired)

| Condition | Stale reason |
|-----------|--------------|
| `chunking_policy.yaml` version bump | `policy_drift` |
| `form_registry.yaml` form definition change | `form_taxonomy_drift` |
| `usfm_marker_coverage.yaml` new chunker-relevant marker | `marker_registry_drift` |
| `contracts.lock.json` surface SHA change | `contract_drift` |
| No eval run in **90 days** | `eval_recency` |
| Gold set expanded and skill fails new case | `gold_coverage_gap` |
| Source manifest SHA change (eng-web re-drop) | `source_drift` |
| Higher-scoring skill supersedes on same form | `score_superseded` |

### Re-eval cadence

| Skill state | Cadence |
|-------------|---------|
| `preferred` | weekly on full gold suite |
| `active` | monthly on form-specific gold |
| `candidate` | on every bake-off run |
| `draft` | on author commit only |

**Quality scoring** (port weights from `skill-agent-quality-scoring-registry.json`):

- `task_success_rate` (25) — gold pass rate
- `evidence_completeness` (20) — boundary_basis present
- `schema_conformance` (15) — RetrievalChunk schema
- `boundary_compliance` (15) — no forbidden splits
- `eval_coverage` (10) — fraction of form gold sets run
- `recency_health` (5)
- `reuse_fit` (5) — routing frequency vs failures
- `cost_efficiency` (5) — chunk count / token p50 fitness

Hard penalties: `boundary_violation: -100`, `gold_hard_gate_fail: -100`, `missing_metadata: -50`.

---

## 8. Gold / eval anchor

### Why gold gates gap detection

Without per-form gold, "no skill fits" is indistinguishable from "skill is bad." Gold sets are the **objective anchor** that makes gap alerts actionable and bake-offs fair.

### Gold suite structure

```text
eval/chunking_gold/
  manifest.json                 # lists all gold sets + form mapping
  per_form/
    poetry_psalm_unit/
      psalm23.boundaries.json   # exactly 1 chunk
      psalm1.boundaries.json
    poetry_stanza/
      psalm119.boundaries.json  # stanza splits at \b / interior \d
    prose_paragraph/
      gen1.boundaries.json      # sentence-complete
    epistle_argument/
      rom7-8.boundaries.json
    gospel_pericope/
      matt5-7.boundaries.json
    ...
```

### Hard gates (inherit from `leaderboard.py` — must not regress 88.5)

- `usfm_leaks == 0`
- `book_crossings == 0`
- `sentence_integrity_pct == 100`
- `gold_psalm23_one_chunk == true`

### Gap-detection gating

A `skill_gap_alert` with `trigger_id: GOLD_REGRESSION` fires only when:

1. Hard gates pass globally BUT
2. Form-specific gold fails OR composite drops **>5 points** from champion run.

Prevents alert noise from broken builds.

### Manual gold (from `EVALUATION_PLAN.md`)

Human-curated boundaries for: Gen 1–3, Ps 1/23/51/119, Prov 1–3, Isa 6/40/53, Matt 5–7, John 1, Rom 1/3/7–8, Heb 1–2, Rev 1/12/21–22 — mapped to forms in `eval/chunking_gold/manifest.json`.

---

## 9. Build sequencing

Smallest increments that preserve **88.5 composite** (claude-opus-4.8 pass2):

| Step | Deliverable | Regression risk |
|------|-------------|-----------------|
| **0** | Document + registries only (this file, `form_registry.yaml` stub, empty graph) | None |
| **1** | Extract `chunk_book()` poetry + prose paths into two `skills/approved/` packages; `chunker.py` imports them — **byte-identical output** | Low — mechanical extract |
| **2** | Add `orchestrator.py` that calls same skills using book_genre as form prior (behavior unchanged) | Low |
| **3** | Add `FormAssignment` emission to `data/candidate/` (sidecar only) | None on chunks |
| **4** | Wire `skill-toc.json` + provenance fields on chunks | Additive metadata |
| **5** | Marker-aware form detector overrides (e.g. Job `\sp` → dialogue skill) behind feature flag | Medium — flag default off |
| **6** | `skill_gap_alerts.jsonl` + bake-off scaffold for one gap (acrostic) | None until flag on |
| **7** | `contracts.lock.json` for chunking registry surface | CI gate only |

**Do not** enable form-detector overrides until step 1–4 prove scorecard parity on existing 4 leaderboard runs.

---

## 10. Risks / what I'd delete

### Question the requirement, then delete

| Owner vision element | Verdict |
|---------------------|---------|
| **Thousands of skills** | **Delete as goal.** Replace with ~40–90 parametric skills. Thousands = registry sharding scenario, not design target. |
| **LLM as primary form detector** | **Delete from hot path.** USFM markers cover WEB completely; LLM only for candidate adjudication. |
| **Knowledge graph as runtime reasoner** | **Delete.** Graph is an index + lifecycle doc, not an inference engine. Routing is deterministic filter + eval score. |
| **Separate orchestrator repo** | **Delete.** Knowledge plane owns chunking; execution-plane agents call repo CLI. |
| **Auto-fuse competing skills** | **Delete default.** Human-gated fusion only. |
| **Per-passage skill patches** | **Delete.** Violates rebuildability; skills must generalize by form. |

### Over-engineering risks

1. **Premature TextSpan dependency** — orchestrator can run on verse-grained units (current v1) until TextSpan generator lands.
2. **Canonical form assignments too early** — candidate-only is sufficient for months.
3. **Full LawFirm quarantine/security scan** — overkill for first-party chunking algorithms; keep `boundary_compliance` eval as safety gate.
4. **Book-level genre as skill selector** — already proven insufficient (Isa poetry, Job dialogue, Dan apocalypse); form detector must supersede.

### What to keep from owner framing

- Orchestrator before monolith skills ✓
- Best skill wins per text ✓ (via eval scores, not opinion)
- Human promotes everything ✓
- Multi-agent bake-off ✓ (already built)
- Staleness tracking ✓ (simplified conditions)
- Alert on unknown forms ✓ (for patristic future)

---

## 11. What I'd reuse from LawFirm OS vs. build new for Scripture

### Port verbatim (or near-verbatim)

| LawFirm artifact | Scripture destination | Notes |
|------------------|----------------------|-------|
| `SKILL_METADATA.json` core fields | `pipelines/chunking/skills/*/SKILL_METADATA.json` | Add Scripture extensions (§3) |
| `skill-agent-graph-index.json` shape | `registry/chunking/skill-graph-index.json` | Node kinds adapted |
| `skill-agent-lifecycle-policy-registry.json` | `config/chunking/skill_lifecycle_policy.yaml` | Same states/transitions |
| `skill-agent-quality-scoring-registry.json` weights | `config/chunking/skill_quality_weights.yaml` | Swap legal penalties → boundary violations |
| `skill-quality-rubric.json` | `docs/chunking/SKILL_QUALITY_DOCTRINE.md` | Biblical retrieval criteria |
| `approved-skills.json` TOC pattern | `registry/chunking/approved-skills.json` | |
| `detect-skill-gaps` → `skill_gap_candidate` record | `skill_gap_alerts.jsonl` | Trigger on gold/regression not Exception Lake |
| `draft-skill` scaffold | `pipelines/chunking/skills/draft/` | `not_canonical_truth: true` contract |
| Orchestrator **ledger + reason codes** | `build/chunking/orchestration_ledger.jsonl` | No route/event_class — use `form_id`/`skill_id` |
| `contracts.lock.json` SHA-pin pattern | `registry/chunking/contracts.lock.json` | Pin policy + form registry + graph index |
| find→quarantine→grade→approve loop | Simplified: draft→eval→human approve | Skip malicious scan for first-party |

### Build Scripture-specific (do not port)

| Concern | Scripture approach |
|---------|-------------------|
| Form detection | USFM marker rules from `RAW_SOURCE_INVENTORY.md` + `usfm_marker_coverage.yaml` |
| Gold sets | Per-form biblical boundaries (Ps 23, Rom 7–8, Matt 5–7) not legal matter fixtures |
| Routing keys | `primary_form` + `book_prior`, not `route_id`/`event_class` |
| Skill algorithm | Deterministic Python on `TranslationWitness` text, not LLM tool plans |
| Gap signals | `evaluate_chunks.py` + `leaderboard.py` regressions, not Exception Lake clusters |
| Trust zones | `candidate` chunks/form assignments; no privilege/confidentiality plane |
| Concordance carry-through | `\w` Strong's, `\f`, `\x`, `\wj` metadata on chunks (already in chunker) |
| Canon | `CanonProfile` on passages — skills do not assert theology |

### Orchestrator boundary (LawFirm `ORCHESTRATOR_BOUNDARY.md` adapted)

- **Knowledge plane (this repo):** owns forms, skills, policies, gold, chunk output, ledger.
- **Execution plane (future agent runtime):** may run `orchestrator.py`, propose draft skills, **no writes to `data/canonical/`**.
- **Human:** promotes skills, form corrections, chunk variants to production.

---

## Appendix: Initial skill catalog (v0 — maps to current `chunker.py`)

| skill_id | Form(s) | Source in chunker.py |
|----------|---------|---------------------|
| `chunk-skill-poetry-psalm-whole-v1` | poetry_psalm_unit, poetry_stanza, poetry_acrostic_section | `chunk_book()` poetry branch |
| `chunk-skill-prose-section-v1` | prose_section, narrative_episode, gospel_pericope, prophetic_oracle | prose heading-bounded loop |
| `chunk-skill-wisdom-tight-v1` | wisdom_saying_cluster | `GENRE_TARGET_SCALE wisdom 0.45` |
| `chunk-skill-epistle-argument-v1` | epistle_argument | epistle + context packet pass |
| `chunk-skill-law-statute-v1` | law_statute_block, list_block | future — flag off until gold exists |
| `chunk-skill-dialogue-speaker-v1` | dialogue_speaker_turn | future — Job `\sp` |

Steps 1–2 implement the first two rows only; others follow gold set availability.

---

*End of proposal. No code changes. Validation gates untouched.*
