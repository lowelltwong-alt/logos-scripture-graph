# Chunking Orchestrator + Skill Registry Design

Author: Codex 5.5
Mode: design proposal
Status: recommendation only
Target repo: logos-scripture-graph

This proposal is intentionally constrained by the repository's current authority model:
raw source is immutable, chunks are derived retrieval objects, form detection is evidence
with provenance, and no generated artifact promotes itself into canonical truth. The
first implementation should refactor the current chunker into registered deterministic
skills; it should not introduce a separate agent runtime inside this repo.

Basis read before design: `AI_FRONT_DOOR.md`, `.ai/control/MASTER_CONTEXT.md`,
`.ai/control/PROJECT_STATUS.md`, `.ai/control/DATA_MAP.md`,
`.ai/control/RAW_SOURCE_INVENTORY.md`, `ROADMAP.md`, `ROADMAP_STATE.yaml`,
`HANDOFF_PROTOCOL.md`, `docs/chunking/CHUNKING_DESIGN.md`,
`docs/architecture/ARCHITECTURE.md`, `config/chunking/book_genres.yaml`,
`config/chunking/chunking_policy.yaml`, `config/ingest/usfm_marker_coverage.yaml`,
`pipelines/chunking/chunker.py`, `pipelines/chunking/boundary_scorer.py`,
`pipelines/chunking/evaluate_chunks.py`, `pipelines/chunking/leaderboard.py`, and
`eval/LEADERBOARD.md`. After the Scripture-first design pass, I reviewed the requested
LawFirm OS skill-registry, orchestrator, and semantic-substrate registry patterns and
revised this document in place.

## 1. Form taxonomy - the bounded set of literary forms you'd route on, and how big it realistically gets for the Protestant canon vs. once early-church texts are added.

The orchestrator should route on a bounded form taxonomy, not on thousands of one-off
forms. Thousands of skills may eventually exist because skills can be alternate
algorithms, versions, experiments, or source-specific implementations. The form set
itself should stay small enough for humans to audit.

For the Protestant canon, I would start with these form IDs:

| Form ID | Evidence basis | Typical skill family |
|---|---|---|
| `narrative_scene` | narrative books, paragraph markers, headings, speaker shifts | scene/episode chunking |
| `genealogy_or_list` | repeated formulaic clauses, `ili`/`li1`, long name lists | list-preserving chunking |
| `legal_unit` | law books, headings, paragraph clusters, formulaic commands | statute/covenant-section chunking |
| `poetic_line_or_stanza` | `q1`, `q2`, `q3`, `b` | line/stanza-preserving chunking |
| `whole_psalm_or_poem` | Psalms/Song/Lam/PrMan/Ps151, chapter boundary, `d`, `qs`, `b`, `q*` | whole-poem with stanza fallback |
| `wisdom_saying_cluster` | Proverbs/Ecclesiastes/Sir/Wis, sentence parallelism, paragraph markers | compact saying clusters |
| `dialogue_speech` | `sp`, direct-speech runs, Job/Song/Gospels/Acts | speaker-boundary chunking |
| `prophetic_oracle` | prophets, `s1`/`ms1`, "word of Yahweh" formulas, paragraphs | oracle/woe/vision chunking |
| `vision_report` | Daniel/Ezekiel/Revelation/2Esd, vision formulas, headings | vision-cycle chunking |
| `gospel_pericope` | Gospel genre, headings, paragraph/sentence boundaries | pericope chunking |
| `parable_or_teaching_unit` | Gospel discourse text, section headings, Jesus speech | discourse/parable chunking |
| `words_of_jesus_speech` | `wj` inline marker, discourse spans | red-letter speech preservation |
| `acts_speech_or_episode` | Acts, speech formulas, headings, paragraphs | speech/episode chunking |
| `epistle_argument_unit` | epistles, discourse connectors, paragraph chains | argument/exhortation chunking |
| `epistle_opening_closing` | greetings, doxologies, final greetings | formulaic epistle-bound chunking |
| `apocalyptic_oracle_cycle` | Revelation/2Esd/Daniel, visions, oracles, sevens | cycle/oracle chunking |
| `variant_sensitive_span` | `fqa`, footnotes | preserve and flag alternate-reading context |
| `cross_reference_dense_span` | `x`, `xo`, `xt` density | carry-through crossref context; not graph promotion |

Some of these are primary route forms; others are overlays. For example, `words_of_jesus_speech`,
`variant_sensitive_span`, and `cross_reference_dense_span` should modify routing and metadata,
but should not always choose a completely separate skill. This avoids a combinatorial explosion
like `gospel_pericope_with_wj_and_x_and_fqa`.

Realistic size:

- Protestant canon: about 14-20 primary forms plus 4-8 overlays.
- WEB's current broader corpus with deuterocanonical books: about 18-24 primary forms, because
  2Esd/AddDan/PrMan/Ps151/AddEsth introduce apocalyptic, prayer, and addition-specific cases.
- Early-church texts: add perhaps 10-15 primary forms, not hundreds. Likely additions are
  `homily`, `apology`, `theological_treatise`, `church_order`, `martyrdom_narrative`,
  `patristic_letter`, `creed_or_rule_of_faith`, `liturgy_or_prayer`, `commentary_scholion`,
  `catena_excerpt`, `dialogue_treatise`, and `hagiography`.

The important design correction is that "form" is not "book genre." The current
`book_genres.yaml` is a useful coarse prior, but a book-level genre cannot see Job speaker labels,
Psalm superscriptions, Selah, words-of-Jesus spans, variant readings, or local discourse shifts.
The orchestrator should use book genre as one evidence feature, then refine by marker-driven
local form detection.

## 2. Form-detection stage - deterministic marker-driven rules vs. LLM judgment; how confidence + provenance are recorded; how a detected form becomes a candidate (human-correctable) artifact.

The first form detector should be deterministic and marker-driven. It should operate after ingest,
using canonical and processed artifacts already produced by the USFM importer:

- `data/canonical/scripture/passages/passages.jsonl`
- `data/canonical/translations/eng-web/translation_witnesses.jsonl`
- `data/canonical/translations/eng-web/boundary_claims.jsonl`
- `data/canonical/translations/eng-web/section_headings.jsonl`
- `data/canonical/translations/eng-web/footnotes.jsonl`
- `data/canonical/translations/eng-web/editorial_cross_references.jsonl`
- `data/canonical/translations/eng-web/word_tokens.jsonl`
- `data/processed/bible/eng-web/usfm/usfm_events.jsonl` when line-order marker evidence is needed

Rules should reference actual markers present in `.ai/control/RAW_SOURCE_INVENTORY.md` and
classified in `config/ingest/usfm_marker_coverage.yaml`:

- `q1`, `q2`, `q3`: poetry line or colon evidence.
- `b`: stanza break evidence.
- `d`: superscription evidence, especially Psalms and Psalm-like prayers.
- `qs`: Selah/liturgical rubric evidence; use as an internal poetic/liturgical cue.
- `sp`: speaker-label evidence, especially Job dialogue and dramatic poetry.
- `wj`: words-of-Jesus overlay evidence.
- `fqa`: variant-sensitive overlay evidence.
- `f`, `fr`, `ft`, `fq`, `fl`: footnote context evidence.
- `x`, `xo`, `xt`: cross-reference context evidence; never promote to theological relationship.
- `s1`, `ms1`, `mt*`: heading and major section evidence.
- `p`, `m`, `mi`, `pi1`, `pc`, `nb`: paragraph and continuation evidence.
- `ili`, `li1`: list evidence.

The detector should emit a candidate, human-correctable artifact, not mutate canonical text:

```json
{
  "id": "form-assignment--eng-web--Ps.23.1--Ps.23.6--whole_psalm_or_poem--v1",
  "type": "ClassificationAssignment",
  "assignment_kind": "literary_form",
  "subject_ref": {
    "source_text_id": "eng-web",
    "osis_start": "Ps.23.1",
    "osis_end": "Ps.23.6"
  },
  "candidate_form_id": "whole_psalm_or_poem",
  "overlays": ["poetic_line_or_stanza"],
  "confidence": 0.96,
  "evidence_refs": [
    "boundary_claim:Ps.23.1:d",
    "boundary_claim:Ps.23.1:q1",
    "book_genre:Ps=psalms",
    "raw_inventory:eng-web_usfm.zip#a745365f53ab9557"
  ],
  "provenance": {
    "created_by": "form_detector.v0",
    "policy_version": "chunk-policy-v0.1.0",
    "marker_coverage_version": "0.1.0",
    "created_at": "ISO-8601"
  },
  "status": "candidate",
  "trust_zone": "candidate"
}
```

Suggested output path:

- `data/candidate/chunking/form_assignments/<source_text_id>-<detector-version>.jsonl`
- `build/chunking/form_detection/<run-id>-report.md`

Confidence should be rule-derived:

- 0.95-1.00: direct marker plus matching book/form prior, such as `d` + `q*` in Psalms.
- 0.85-0.94: strong marker evidence without perfect book prior, such as `sp` in Job.
- 0.70-0.84: section/paragraph/formula evidence with known genre prior.
- 0.50-0.69: fallback book-level genre only; should route to conservative fallback skill.
- Below 0.50: no route; emit a gap alert.

LLM judgment should not be in the first routing path. Later, an LLM can propose a candidate
assignment only when deterministic evidence is ambiguous, but it must produce evidence refs,
abstain when evidence is missing, and land in `data/candidate/`, never `data/canonical/`.

## 3. Skill registry - the schema/metadata for one chunking skill (id, version, which forms it handles, dependencies, score, status, supersedes/combines, etc.), and where it lives in the repo.

The registry should borrow the LawFirm `SKILL_METADATA.json` shape but change the domain fields.
Each chunking skill should be a small package, not just a prompt. Recommended layout:

```text
pipelines/chunking/skills/
  approved/
    psalm-stanza-v1/
      SKILL.md
      SKILL_METADATA.json
      skill.py
      tests/
  candidate/
    job-dialogue-v0/
      SKILL.md
      SKILL_METADATA.json
      skill.py
      fixtures/
  quarantine/
registry/generated only:
build/chunking/skill_registry/index.json
build/chunking/skill_registry/graph.json
build/chunking/skill_registry/toc.md
config/chunking/skill_registry/lifecycle_policy.yaml
config/chunking/skill_registry/quality_scoring.yaml
config/chunking/skill_registry/form_registry.yaml
```

I would keep the human-maintained policy files under `config/chunking/skill_registry/`.
The generated TOC/graph belongs under `build/` until the team decides it should be committed.
Approved skill packages can be code, because they are the executable pipeline. Candidate skills
may be proposal packages until accepted.

Recommended `SKILL_METADATA.json`:

```json
{
  "schema_version": "scripture-chunking-skill.v1",
  "id": "psalm-stanza-v1",
  "kind": "chunking_skill",
  "name": "Psalm stanza chunker",
  "owning_repo": "logos-scripture-graph",
  "owning_plane": "knowledge_plane",
  "address": "logos.chunking.skill.psalm-stanza.v1.approved",
  "version": "1.0.0",
  "lifecycle_state": "approved",
  "risk_tier": "medium",
  "handles_forms": ["whole_psalm_or_poem", "poetic_line_or_stanza"],
  "handles_overlays": ["variant_sensitive_span", "cross_reference_dense_span"],
  "source_profiles": ["eng-web_usfm"],
  "input_contracts": [
    "ScripturePassage",
    "TranslationWitness",
    "BoundaryClaim",
    "ClassificationAssignment"
  ],
  "output_contracts": ["RetrievalChunk", "ContextPacket"],
  "required_evidence": ["osis_span", "boundary_basis", "source_manifest", "license"],
  "forbidden_actions": [
    "write_data_raw",
    "write_data_canonical",
    "rewrite_source_text",
    "promote_candidate_form",
    "split_mid_sentence",
    "orphan_psalm_superscription"
  ],
  "dependencies": [
    "config/chunking/chunking_policy.yaml",
    "pipelines/chunking/boundary_scorer.py"
  ],
  "parameters": {
    "target_tokens": 700,
    "soft_max_tokens": 1100,
    "hard_max_tokens": 1600,
    "split_basis": ["poetic_stanza", "usfm_poetry_boundary"]
  },
  "eval": {
    "gold_sets": ["eval/gold/chunking/psalms.jsonl"],
    "latest_score_ref": "eval/chunking_runs/latest",
    "minimum_score": 90
  },
  "quality": {
    "score": 0,
    "score_version": "scripture-chunking-skill-quality.v1",
    "last_evaluated_at": null
  },
  "relationships": {
    "supersedes": [],
    "superseded_by": null,
    "combines_with": [],
    "conflicts_with": []
  },
  "staleness": {
    "reevaluate_on": [
      "raw_inventory_sha_change",
      "marker_coverage_change",
      "chunking_policy_change",
      "schema_change",
      "gold_set_change"
    ],
    "max_days_without_eval": 90
  },
  "approval_required": true,
  "recommended_update_policy": "human_gate",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "notes": ""
}
```

This ports LawFirm's useful metadata fields almost verbatim: `id`, `kind`, `owning_repo`,
`owning_plane`, `address`, `version`, `lifecycle_state`, `risk_tier`, `inputs`, `outputs`,
`quality_score_ref`, graph refs, `supersedes`, `combines_with`, and update policy. Scripture-specific
fields are `handles_forms`, `handles_overlays`, `source_profiles`, `required_evidence`,
`forbidden_actions`, and the chunking eval/gold-set block.

Lifecycle states should be:

- `draft`: local or agent-proposed, not routable.
- `candidate`: tests exist; can be run in A/B, not default production.
- `approved`: human-approved and routable.
- `preferred`: default when multiple approved skills match a form.
- `deprecated`: still runnable for reproducibility, not selected for new runs.
- `superseded`: replaced by another skill.
- `retired`: unavailable except for provenance replay.
- `quarantined`: failed safety, schema, or boundary gate.

Automatic actions allowed: score, detect gap, draft candidate, quarantine on hard failure, generate
recommendation. Automatic actions forbidden: promote to approved/preferred, expand write authority,
write raw/canonical, delete stable resources, or weaken validation.

## 4. Knowledge graph / TOC - how the orchestrator enumerates and navigates its skills.

The orchestrator needs both a table of contents and a graph, but they should be generated from
skill metadata. The graph is for navigation, audit, and route explanation; it is not part of the
Scripture intertextual graph.

Generated files:

```text
build/chunking/skill_registry/toc.md
build/chunking/skill_registry/index.json
build/chunking/skill_registry/graph.json
build/chunking/skill_registry/route_matrix.md
```

The graph index should use LawFirm's edge discipline but with Scripture names:

Node kinds:

- `chunking_skill`
- `literary_form`
- `form_overlay`
- `source_profile`
- `gold_set`
- `schema_contract`
- `policy_file`
- `validator`
- `pipeline`

Edge types:

- `handles`
- `requires`
- `produces`
- `validates`
- `evaluated_by`
- `bounded_by`
- `supersedes`
- `superseded_by`
- `combines_with`
- `conflicts_with`
- `fills_gap`
- `recommended_for`

Minimum node fields:

```json
{
  "id": "psalm-stanza-v1",
  "kind": "chunking_skill",
  "address": "logos.chunking.skill.psalm-stanza.v1.approved",
  "version": "1.0.0",
  "lifecycle_state": "approved",
  "quality_score_ref": "chunking-skill-quality://psalm-stanza-v1/latest"
}
```

Minimum edge fields:

```json
{
  "from": "psalm-stanza-v1",
  "to": "whole_psalm_or_poem",
  "edge_type": "handles",
  "evidence_ref": "pipelines/chunking/skills/approved/psalm-stanza-v1/SKILL_METADATA.json"
}
```

At thousands of skills, copy LawFirm's sharding policy: shard the graph when nodes exceed 10,000,
using `build/chunking/skill_registry/shards/{kind}/{prefix}.json`. But do not build sharding first.
The first useful TOC is a single generated Markdown table:

| Skill | State | Forms | Score | Last eval | Supersedes | Stale? |
|---|---|---|---:|---|---|---|

Route lookup should be deterministic: load approved/preferred metadata, filter by form and required
input contracts, reject stale or quarantined skills, sort by lifecycle priority, form specificity,
quality score, recency health, and stable skill ID.

## 5. Routing/orchestration - unit -> form -> skill selection -> emit chunk w/ provenance; how this relates to the existing genre dispatch in chunker.py (refactor vs rebuild).

The orchestrator should be a thin deterministic control loop:

```text
canonical/processed source artifacts
-> candidate route units
-> form detector
-> ClassificationAssignment candidates
-> skill registry filter
-> deterministic skill selection
-> chunk skill execution
-> RetrievalChunk + ContextPacket + route ledger
-> evaluation scorecard
```

Route units should initially be book-local ordered spans built from existing verse units plus
boundary claims. Later, TextSpan generation can replace the internal verse-grained unit model.
The route unit is not the final chunk; it is the span under consideration for form assignment.

Proposed CLI:

```bash
python pipelines/chunking/orchestrator.py \
  --passages data/canonical/scripture/passages/passages.jsonl \
  --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl \
  --boundary-claims data/canonical/translations/eng-web/boundary_claims.jsonl \
  --footnotes data/canonical/translations/eng-web/footnotes.jsonl \
  --crossrefs data/canonical/translations/eng-web/editorial_cross_references.jsonl \
  --genres config/chunking/book_genres.yaml \
  --policy config/chunking/chunking_policy.yaml \
  --skill-registry pipelines/chunking/skills \
  --out data/derived/chunks/eng-web/chunks.jsonl \
  --context-out data/derived/chunks/eng-web/context_packets.jsonl \
  --route-ledger build/chunking/orchestrator/route_ledger.jsonl
```

Route decision record:

```json
{
  "route_id": "route--eng-web--Ps.23.1--Ps.23.6",
  "source_text_id": "eng-web",
  "osis_start": "Ps.23.1",
  "osis_end": "Ps.23.6",
  "form_assignment_id": "form-assignment--eng-web--Ps.23.1--Ps.23.6--whole_psalm_or_poem--v1",
  "selected_skill_id": "psalm-stanza-v1",
  "selected_skill_version": "1.0.0",
  "selection_reason": "preferred approved skill for whole_psalm_or_poem with exact source profile",
  "rejected_skill_ids": [
    {"skill_id": "generic-prose-v1", "reason": "form_mismatch"}
  ],
  "registry_surface_sha256": "sha256:...",
  "policy_version": "chunk-policy-v0.1.0",
  "evidence_refs": ["boundary_claim:Ps.23.1:d", "book_genre:Ps=psalms"],
  "created_at": "ISO-8601"
}
```

Relationship to `chunker.py`: refactor, do not rebuild. The current file already contains hidden
skills:

- `emit_psalm`: whole-psalm/stanza handling.
- prose heading/paragraph/sentence flushing.
- wisdom budget scaling.
- epistle discourse-connector context packet generation.
- boundary scoring through `boundary_scorer.py`.

First extract those into skill functions behind a shared interface:

```python
class ChunkingSkill(Protocol):
    skill_id: str
    def can_handle(self, assignment: FormAssignment, context: RouteContext) -> bool: ...
    def chunk(self, units: list[RouteUnit], context: RouteContext) -> SkillResult: ...
```

The old CLI can call the orchestrator internally once parity tests pass. During transition, keep
`chunker.py` as a compatibility facade so existing validation and Data Map references do not churn.

Selection should fail closed:

- Unknown form ID: no skill selected; emit gap alert.
- Unknown skill lifecycle state: reject skill.
- Stale skill with no approved override: reject skill.
- Missing required evidence: reject skill.
- Boundary violation in output: quarantine recommendation and fail run.

## 6. Gap detection + self-extension - exact trigger conditions for "no skill fits"; the alert artifact; the multi-agent bake-off to author a new skill; pick-best-or-fuse.

The gap detector should use concrete triggers, not a vague sense that chunking could be better.

Trigger a `ChunkingSkillGap` when any of these conditions hold:

- `no_form_detected`: form detector confidence below 0.50 for a route unit.
- `no_skill_for_form`: no approved/preferred skill handles the detected primary form.
- `missing_required_marker_handling`: a marker appears in raw inventory or boundary evidence but is not covered
  by the selected skill's declared inputs.
- `skill_abstained`: selected skill returns abstain with missing evidence or unsupported structure.
- `route_conflict`: top two skills tie within a small score margin and produce materially different chunks.
- `gold_failure`: a skill fails a hard gold gate for the form it claims to handle.
- `stale_only`: all matching skills are stale or quarantined.
- `fallback_pressure`: fallback generic skill handles more than a threshold, for example 5 percent of spans
  in a book or any span in a gold-critical book.
- `new_source_profile`: a source family arrives without matching source profile, such as early-church TEI,
  Markdown, HTML, or PDF-derived text.

Alert artifact:

```text
data/candidate/chunking/skill_gaps/<date>-<gap-id>.json
build/chunking/skill_gaps/<date>-report.md
.ai/context/recommendations/chunking_skill_gaps/<date>-<gap-id>.md
```

Candidate gap record:

```json
{
  "schema_version": "chunking-skill-gap.v1",
  "record_type": "chunking_skill_gap",
  "gap_id": "gap--eng-web--Job.3.1--Job.3.26--dialogue_speech",
  "candidate_only": true,
  "requires_human_approval": true,
  "source_text_id": "eng-web",
  "osis_start": "Job.3.1",
  "osis_end": "Job.3.26",
  "detected_form_id": "dialogue_speech",
  "trigger": "no_skill_for_form",
  "evidence_refs": ["boundary_claim:Job.3.1:sp", "book_genre:Job=wisdom"],
  "recommended_skill_family": "speaker_dialogue_chunker",
  "support_count": 1,
  "severity": "medium",
  "status": "candidate"
}
```

Self-extension should copy the LawFirm loop:

```text
detect gap
-> draft candidate skill package
-> run fixture/gold tests
-> static safety and authority scan
-> A/B chunk run
-> scorecard and leaderboard
-> human picks best or requests fusion
-> approved skill becomes routable
```

Multi-agent bake-off:

1. Generate one candidate package per agent under `pipelines/chunking/skills/candidate/<agent>-<gap-id>/`.
2. Each package must include `SKILL.md`, `SKILL_METADATA.json`, code or precise algorithm notes, fixtures,
   expected outputs, and forbidden actions.
3. Run the same source spans and gold sets for all candidates.
4. Use `evaluate_chunks.py --scorecard-dir eval/chunking_runs`.
5. Use `leaderboard.py` for objective ordering.
6. Human reviews route ledgers and chunk diffs.
7. If two candidates each solve different cases, create a fused candidate skill with explicit `combines_with`
   refs and rerun the full suite.

No candidate skill approves itself. No candidate form assignment becomes authoritative without human review.

## 7. Staleness + lifecycle - precise conditions that make a skill stale; re-eval cadence.

A skill becomes stale when any of these conditions are true:

- Raw source inventory SHA changes for a source profile the skill handles.
- `config/ingest/usfm_marker_coverage.yaml` changes for a marker the skill handles.
- `config/chunking/chunking_policy.yaml` version changes.
- `config/chunking/book_genres.yaml` changes for a book the skill handles.
- Any schema in its `input_contracts` or `output_contracts` changes.
- The form registry changes for a form or overlay it handles.
- A gold set it declares changes.
- It has not been evaluated in `max_days_without_eval`, initially 90 days.
- Its latest score falls below active threshold.
- It fails any hard gate: raw/canonical write attempt, source text mutation, mid-sentence split,
  orphan superscription, missing OSIS span, missing boundary basis, missing license, or schema-invalid output.
- A preferred successor supersedes it.

Lifecycle policy:

| From | To | Gate |
|---|---|---|
| `draft` | `candidate` | tests and metadata pass |
| `candidate` | `approved` | human required |
| `approved` | `preferred` | human required plus score threshold |
| `approved` | `deprecated` | replacement approved or human decision |
| `approved` | `quarantined` | automatic on hard safety/boundary failure |
| `deprecated` | `retired` | human required |
| `any` | `quarantined` | automatic on raw/canonical mutation attempt or contract violation |

Cadence:

- Per PR: evaluate touched skills and all skills affected by changed config/schema/gold files.
- Nightly or weekly local/CI job: smoke route all forms, validate registry, generate TOC.
- Monthly: full-chunk corpus A/B scorecard if active development continues.
- On new raw source family: run raw scan, marker coverage, then form detection in report-only mode before
  any chunking skill is approved for that source.

Scoring should adapt LawFirm weights but replace legal concerns with Scripture chunking concerns:

```yaml
score_version: scripture-chunking-skill-quality.v1
metric_weights:
  hard_gate_pass_rate: 25
  boundary_compliance: 20
  gold_set_success: 20
  evidence_completeness: 15
  schema_conformance: 10
  form_specificity: 4
  recency_health: 3
  simplicity_reuse_fit: 3
hard_penalties:
  raw_or_canonical_write: -100
  source_text_mutation: -100
  schema_invalid_output: -50
  missing_boundary_basis: -40
  stale_registry_surface: -30
thresholds:
  preferred_min_score: 90
  approved_min_score: 80
  improve_below: 75
  quarantine_below: 40
```

## 8. Gold/eval anchor - what gold sets are needed and why they gate gap detection.

Gold sets make gap detection honest. Without gold anchors, "no skill fits" can become a loophole
for agents to create a skill whenever output looks imperfect. The first gold sets should cover
forms and markers that the raw inventory proves are present:

| Gold set | Why it matters |
|---|---|
| `psalms_core.jsonl`: Ps 1, 23, 51, 119 | Whole psalm, superscription, stanza, acrostic, long psalm split |
| `poetry_liturgy.jsonl`: selected Psalms with `qs` | Selah must not disappear or become a boundary bug |
| `job_dialogue.jsonl`: Job 3-5, 38-42 | `sp` speaker labels and speech boundaries |
| `proverbs_wisdom.jsonl`: Prov 1, 10, 25 | saying clusters, compact chunks, parallelism |
| `prophetic_oracles.jsonl`: Isa 6, Isa 40, Amos 5, Zech 9 | oracle/vision/woe structure |
| `gospel_discourse.jsonl`: Matt 5-7, John 1, John 14-17 | Jesus speech, discourse units, no prooftext isolation |
| `gospel_pericope.jsonl`: Mark 4, Luke 15 | parables and pericope boundaries |
| `acts_speeches.jsonl`: Acts 2, 7, 17 | speech/episode handling |
| `epistle_argument.jsonl`: Rom 7-8, Gal 3, Heb 1-4 | argument-chain and context packet gates |
| `apocalypse_vision.jsonl`: Rev 1, 12-13, 21-22 | vision-cycle chunking |
| `variant_note_sensitive.jsonl`: spans with `fqa` and dense footnotes | preserve textual-variant and note context |
| `crossref_dense.jsonl`: spans with `x` density | carry editorial crossrefs without promoting graph edges |

Each gold row should include:

- source text ID
- OSIS start/end
- expected allowed chunk boundaries
- forbidden splits
- required context packet refs, when relevant
- marker evidence refs
- reviewer notes

Gold gates should decide:

- Is the skill eligible for `approved` or `preferred`?
- Is a gap real or merely an untested preference?
- Did a source/config/schema change stale an existing skill?
- Did a proposed fused skill improve the affected form without regressing other forms?

Gap detection should be conservative when no gold set exists. It may emit a candidate gap, but severity
should be lower and the alert should say "gold coverage missing" rather than recommending immediate
skill creation.

## 9. Build sequencing - smallest first increment that beats the current 88.5 chunker leaderboard without a full rewrite.

The current leaderboard winner scores 88.5 with 1,374 chunks, p50 729 tokens, 10 fragmented psalms,
100 percent prose sentence integrity, 0 USFM leaks, and 0 book crossings. The smallest useful increment
is not a new orchestrator from scratch; it is a registry-backed extraction of the existing hidden skills
plus better form evidence around the hardest cases.

Recommended sequence:

1. Add `config/chunking/skill_registry/form_registry.yaml`, lifecycle policy, and scoring YAML.
2. Add `pipelines/chunking/form_detector.py` in report-only mode. Emit candidate `ClassificationAssignment`
   rows and a marker/form coverage report. Do not change chunk output yet.
3. Add a generated skill TOC/index from metadata for the current behaviors, even if the skills still call
   functions inside `chunker.py`.
4. Extract existing behaviors into approved initial skills:
   `generic-prose-v1`, `psalm-stanza-v1`, `wisdom-cluster-v1`, `epistle-context-v1`.
5. Wrap `chunker.py` with `orchestrator.py`, but keep current output stable while route ledgers are emitted.
6. Add gold fixtures for Ps 23/Ps 119/Job dialogue/John 1/Rom 7-8/Revelation 12.
7. Improve only the highest-leverage form-specific failure: reduce psalm fragmentation and monster chunks by
   using `d`, `b`, and `q*` as explicit stanza/acrostic evidence, while preserving superscriptions.
8. Add a `dialogue-speech-v1` candidate for Job `sp` labels only after gold fixtures exist.
9. Run `evaluate_chunks.py` and `leaderboard.py`; compare against the 88.5 baseline.

Why this can beat 88.5: the score already passes hard gates, so improvement must come from fewer
fragmented psalms, better size fitness, and higher boundary/metadata confidence without breaking sentence
integrity. A form detector plus extracted psalm/wisdom skills gives targeted pressure on exactly those
metrics. Do not try to solve early-church routing or all possible discourse forms before moving the
score from 88.5.

## 10. Risks / what you'd delete - apply "question the requirement, then delete" - call out anything in this vision that is over-engineered or premature.

Question the requirement: "Thousands of skills" is not a first-principles requirement. The real requirement is
that a bounded set of literary forms can be routed to the best tested algorithm, with provenance and a human
review loop when coverage fails. Thousands of skill packages may emerge over years, but designing for that
on day one risks burying the chunker under registry machinery.

Delete or defer:

- Delete LLM-first form detection for the current WEB corpus. The raw USFM markers are strong enough for v0.
- Delete a separate agent runtime inside this repo. The repo is the knowledge/control plane; execution-plane
  automation belongs elsewhere.
- Delete "skill per book" as a default. Use form plus overlays.
- Delete automatic skill fusion. Generate a fusion proposal and require human approval.
- Delete canonical promotion of form assignments. They remain candidate/reviewable evidence.
- Defer sharded skill graph until there are thousands of nodes.
- Defer contract-lock tooling until the registry surface stabilizes; record a registry SHA in route ledgers first.
- Defer early-church source support until raw source formats and marker inventories exist.
- Defer a full `TextSpan` rewrite until a small orchestrator can wrap the current verse-grained chunker.
- Defer fancy graph visualization. A generated TOC and JSON graph are enough.

Risks:

- Marker-driven form detection may overfit WEB USFM. Mitigation: source profiles and raw inventory hashes.
- Book genre priors may hide local genre shifts. Mitigation: overlays and marker evidence beat book-level prior.
- Candidate skills may proliferate. Mitigation: lifecycle thresholds, quarantine, and human approval for routing.
- Registry metadata can rot. Mitigation: generated TOC, stale checks, and per-PR validation.
- A skill graph can be mistaken for the Scripture graph. Mitigation: keep it under chunking/build/control surfaces,
  not `data/canonical` or relationship objects.
- Over-optimizing for leaderboard score can hurt reviewer trust. Mitigation: hard gates and gold-set diffs lead;
  composite score follows.

## 11. What I'd reuse from LawFirm OS vs. build new for Scripture

Reuse from LawFirm OS, mostly verbatim:

- The operating lifecycle: `find -> quarantine -> static scan -> semantic/authority review -> grade -> approve -> install`.
  For Scripture, "install" means "make routable by the chunking orchestrator," not install into an agent runtime.
- `SKILL_METADATA.json` as the per-skill metadata unit beside `SKILL.md`.
- Lifecycle states: draft, candidate, approved/active, preferred, deprecated, superseded, retired, quarantined.
- The graph-index pattern: machine-readable nodes and edges with minimum fields and evidence refs.
- The quality-scoring registry as a separate policy surface rather than scoring logic hidden in code.
- The gap factory pattern: repeated defects or unsupported routes become candidate-only gap records, then draft skills
  with fixtures.
- Human-gated approval for promotion to routable/preferred.
- Quarantine on hard safety or authority failure.
- Append-only JSONL ledger for route decisions.
- Contract-surface provenance: record the registry/policy hash consumed by a run.

Adapt from LawFirm OS:

- Replace legal "exception clusters" with chunking failures, unknown forms, unsupported markers, stale skills,
  fallback pressure, and gold-set regressions.
- Replace route/event allowlists with form/skill allowlists.
- Replace "malicious skill" security concerns with pipeline authority concerns: no raw/canonical writes, no source
  text mutation, no schema drift, no unreviewed promotion. Keep static scans for scripts if candidate skills include code.
- Replace `data_classes` with Scripture source profiles and trust zones.
- Replace LawFirm's algorithm-elegance rubric with a chunking-specific rubric that prizes boundary compliance,
  evidence completeness, gold-set success, and simplicity.
- Replace model-centric prompt integrity with deterministic rule/version integrity for v0. If LLM-assisted detection
  arrives later, then prompt hashes become relevant.

Build new for Scripture:

- The form taxonomy and overlays, grounded in actual USFM markers and biblical literary forms.
- The form detector and `ClassificationAssignment` output contract.
- Marker-aware source profiles for WEB USFM, future WLC/SBLGNT/LXX, and eventually early-church formats.
- Per-form gold sets for Psalms, Job, Prophets, Gospels, Epistles, Revelation, variant-sensitive spans, and
  cross-reference-dense spans.
- Chunk-specific hard gates: sentence integrity, superscription preservation, poetic line preservation, OSIS span,
  source manifest, license, and boundary basis.
- Context-packet rules for prooftext-sensitive chunks, especially epistles and discourses.
- The bridge from current `chunker.py` behavior into skill packages without breaking existing validation.

Strongest design stance: the orchestrator should not aspire to be a clever judge of biblical literature. It should
be a boring, fail-closed router over explicit source evidence, and it should make uncertainty cheap to review.
