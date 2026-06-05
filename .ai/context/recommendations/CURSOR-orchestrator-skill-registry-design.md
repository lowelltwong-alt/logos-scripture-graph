# Chunking Orchestrator + Skill Registry Design

**Author:** Cursor Gemini 3.1 Pro
**Date:** 2026-06-05

## 1. Form taxonomy
The taxonomy must be a bounded, finite set of literary forms that dictate structural chunking rules.
- **Protestant Canon (~8 forms):** Narrative, Law/Code, Poetry/Psalms, Wisdom/Proverb, Prophetic Oracle, Gospel Pericope, Epistle/Discourse, Apocalyptic Vision.
- **Extended/Early-Church (+4-6 forms):** Apology, Homily/Sermon, Martyrdom, Liturgy, Commentary.
- **Realistic Count:** 12-15 forms total. We do not need thousands of micro-forms; chunking algorithms only diverge when the structural markers and semantic flow fundamentally change.

## 2. Form-detection stage
Form detection must be deterministic first, falling back to LLMs only for ambiguity.
- **Deterministic Rules:** Driven by the actual USFM markers documented in `RAW_SOURCE_INVENTORY.md`. For example, `\q*` blocks are Poetry; blocks bounded by `\d` are Psalms; blocks with dense `\wj` are Gospel Discourse.
- **LLM Judgment:** Used for un-marked transitions (e.g., shifting from Narrative to Discourse inside an Epistle without a `\s` heading).
- **Artifact:** Outputs a `ClassificationAssignment` record in the `candidate` trust zone.
- **Human-correctable:** These assignments live in `data/candidate/classification/` and are promoted to `data/canonical/` by humans. The orchestrator reads the canonical assignments first, falling back to candidate or real-time detection if missing.

## 3. Skill registry
A chunking skill is a discrete package containing the algorithm and its contract.
- **Location:** `pipelines/chunking/skills/<skill_id>/`
- **Components:** `algorithm.py` (the logic) and `SKILL_METADATA.json`.
- **Metadata Schema:**
  - `id`: e.g., `chunk-skill-psalms-v1`
  - `supported_forms`: `["poetry", "psalms"]`
  - `required_markers`: `["\q1", "\q2", "\b"]`
  - `forbidden_markers`: `[]`
  - `quality_score_ref`: Link to the latest `evaluate_chunks.py` scorecard.
  - `lifecycle_state`: `active`
  - `author`: `claude-opus-4.8`

## 4. Knowledge graph / TOC
The orchestrator needs a fast, deterministic way to enumerate skills without scanning the filesystem dynamically at runtime.
- **Artifact:** `registry/chunking-skill-index.json`.
- **Function:** A machine-readable table of contents mapping `Form -> List[Skill ID]`.
- **Navigation:** The orchestrator loads this index into memory at startup. It filters for skills in the `active` or `preferred` lifecycle states.

## 5. Routing/orchestration
The orchestrator replaces the monolithic `chunker.py` script.
- **Flow:**
  1. **Input:** A raw text unit (e.g., a heading-bounded section).
  2. **Form Detection:** Query canonical assignments or run the detector.
  3. **Skill Selection:** Lookup the form in `chunking-skill-index.json`. Select the `active` skill with the highest quality score.
  4. **Execution:** Pass the unit to the selected skill's `algorithm.py`.
  5. **Validation:** The orchestrator validates the emitted `RetrievalChunk` against `chunking_policy.yaml` (e.g., no mid-sentence splits).
- **Refactor vs Rebuild:** Refactor. The existing `chunker.py` already has genre-dispatch logic. We extract the `chunk_book` inner loops into separate skill files and turn `chunker.py` into the pure router/validator.

## 6. Gap detection + self-extension
The system must detect when it lacks the capability to chunk a text safely.
- **Triggers for "No skill fits":**
  1. Form detector returns `unknown`.
  2. Orchestrator finds no `active` skill for the detected form.
  3. The chosen skill repeatedly fails orchestrator validation (e.g., cannot meet token budgets without breaking sentences).
- **Alert Artifact:** Appends a record to `reports/skill_gap_candidates.jsonl`.
- **Multi-agent Bake-off:** Agents are dispatched to author new skills (`draft` state). They run against the eval harness.
- **Pick-best-or-fuse:** The system automatically promotes the highest-scoring `draft` to `candidate`. *Fusing* algorithms automatically is highly dangerous and should be avoided; humans pick the best discrete algorithm.

## 7. Staleness + lifecycle
Skills decay when their underlying assumptions change.
- **Staleness Conditions:**
  1. `config/chunking/chunking_policy.yaml` is updated (e.g., token budgets change).
  2. The gold set for the skill's supported form is updated.
  3. `config/ingest/usfm_marker_coverage.yaml` introduces a new marker relevant to the form.
- **Re-eval Cadence:** CI automatically re-runs `evaluate_chunks.py` for all `active` skills when dependencies change. If the score drops below the threshold, the skill is downgraded to `quarantined` or `deprecated`.

## 8. Gold/eval anchor
Gap detection and skill grading are impossible without ground truth.
- **Gold Sets:** We need per-form gold sets (e.g., `eval/gold_psalms.jsonl`, `eval/gold_epistles.jsonl`).
- **Gating:** You cannot detect a "gap" in chunking quality unless a gold set proves the current skill is failing. If a new form (e.g., `homily`) is introduced, a human MUST author a gold set for it before agents can compete to write a skill for it.

## 9. Build sequencing
Smallest increment to avoid regressing the current 88.5 leaderboard score:
1. **Define Contracts:** Create `SKILL_METADATA.json` schema and `chunking-skill-index.json`.
2. **Extract Existing Logic:** Move the current `chunker.py` Pass-2 logic into two static skills: `chunk-skill-prose-v1` and `chunk-skill-poetry-v1`.
3. **Refactor Orchestrator:** Update `chunker.py` to route to these two skills based on the existing `book_genres.yaml`. Verify the leaderboard score remains 88.5.
4. **Add Form Detector:** Introduce the per-pericope form detector to override book-level genres.

## 10. Risks / what you'd delete
- **Delete "Thousands of Skills":** This is a massive over-engineering risk. The Bible and early church texts have a finite, small set of literary forms (~15). We need dozens of skills, not thousands. Building a sharded, highly complex discovery graph for 20 Python scripts is wasted effort.
- **Delete "Automated Fusing":** LLMs are notoriously bad at safely merging complex, deterministic Python algorithms without introducing edge-case bugs. Keep the multi-agent bake-off, but have the system present the top 3 candidates for a human to select or manually merge.

## 11. What I'd reuse from LawFirm OS vs. build new for Scripture
**Reuse Verbatim from LawFirm OS:**
- **The Lifecycle Loop:** The strict `draft -> candidate -> active -> quarantined` state machine from `skill-agent-lifecycle-policy-registry.json`.
- **Metadata Schema:** The `SKILL_METADATA.json` structure, specifically the context discipline, forbidden types, and trust status fields.
- **Deterministic Orchestrator Pattern:** The orchestrator acts as a strict, read-only client of the substrate, validating outputs against a route allowlist and appending to a local ledger without mutating canonical data.

**Build New for Scripture:**
- **Form Detection:** LawFirm OS relies on semantic intent classification. Scripture requires deterministic, USFM marker-driven form detection (e.g., `\q1` vs `\p`).
- **Per-Form Gold Sets:** Legal contexts might tolerate "good enough" semantic retrieval. Scripture chunking requires exact boundary matching (e.g., never splitting a Psalm superscription). Gold sets must be highly specific to the literary form.
- **The Algorithms:** The actual chunking logic (handling acrostics, Hebrew poetry colas, epistolary connectors) is entirely unique to this domain and cannot be ported.
