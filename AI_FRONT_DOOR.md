# AI Front Door

This file is the required entry point for every AI agent and human contributor.

## Mandatory read order

Read these files before making changes:

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` — **human-gated architecture authority (READ ONLY for AI)**
3. `.ai/control/PROJECT_STATUS.md` — **current operational state**
4. `.ai/control/DATA_MAP.md` — **data artifacts + pipeline endpoints (generated)**
5. `.ai/control/RAW_SOURCE_INVENTORY.md` — **the ACTUAL raw documents to be processed** (generated). **Mandatory before any ingest/chunking/graph work** — see "Raw source inspection" below.
6. `ROADMAP.md`
6. `ROADMAP_STATE.yaml`
7. `HANDOFF_PROTOCOL.md`
8. `docs/architecture/ARCHITECTURE.md`
9. `docs/chunking/CHUNKING_DESIGN.md`
10. For chunking-related work: `.ai/control/METHODOLOGY_UPDATE_RULES.md` and
    `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
10. For any ingest, chunking, review-packet, evaluator, route, graph, or retrieval work:
    `.ai/control/chunking_agent_preflight.yaml` and
    `docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md` rule `CHUNK-METADATA-001`.
    Source metadata is evidence, not authority. The source-metadata research atlas,
    apocalyptic/prophetic intertext dossier queue, epistle argument theological issue queue,
    wisdom/dialogue/poetry dossier queue, prophetic/oracle/vision dossier queue,
    textual-variant/source-tradition dossier queue,
    divine-name/title capitalization and WJ/red-letter markers, WJ speaker/discourse policy,
    and John 3 owner-review docket are evidence/review policy, not authority.
    The Bible-wide research registry is a canonical 66-book research queue, not chunk/gold/graph
    authority.
11. For chunking, evaluator, gold, route, or default-behavior decisions with possible theological
    downstream effects: `.ai/control/chunking_theological_decision_register.yaml`
12. For Bible-wide chunking readiness, lane sequencing, algorithm readiness, and next safe route:
    `.ai/control/bible_chunking_readiness_map.yaml`
12. For pre-chunking Bible-wide research triage:
    `.ai/control/bible_chunking_research_triage_map.yaml`
13. For high-leverage authority, routing, evaluator, default-behavior, corpus-scope, generated
    artifact, automation, cross-repo, workflow-rule, or master-chunker work:
    `docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md`
14. `config/agents/agent_roles.yaml`
15. `.ai/handoffs/<active_task_id>/handoff.md` — see `PROJECT_STATUS.md` for active task
16. The specific files in the task scope.

New or lower-capability agents: read `.ai/handoffs/AGENT_ROUTING_GUIDE.md` for full step-by-step routing.

Independent reviewers or no-context A/B/red-team agents: after this front door, read
`.ai/audits/README.md` and `.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md`. Those files define the
repo-resident audit path, required changelogs, review report location, validation commands, harness
script, future harness-upgrade roadmap, and stop conditions. Reviewers must prove claims from repo
files, git/PR state, logs, handoffs, decision registers, readiness maps, review packets, and
validators rather than chat memory.

## Cross-repo governance

This repository is the governed Scripture data-plane / knowledge-plane implementation
for the upstream [logos-governance-architecture](https://github.com/lowelltwong-alt/logos-governance-architecture)
repo. The link type is `governance_contract`, recorded in
`config/governance/repository_link_contract.yaml`.
The governance repo's `governance/LOGOS_REPO_REGISTRY.yaml` is the source of
truth for cross-repo registry and repository relationship contracts.

The hierarchy is:

```text
logos-governance-architecture
  -> upstream governance / theological architecture authority
  -> logos-scripture-graph
     -> deterministic Scripture data-plane implementation
     -> validated release artifacts for future runtime consumers
```

Agents must read `AI_TABLE_OF_CONTENTS.md`, `config/governance/repository_link_contract.yaml`,
and `config/agents/agent_hostile_policy.yaml` when work touches cross-repo project structure,
authority, trust zones, release contracts, or GitHub coordination.

Agents must not treat GitHub issues, Project-board fields, or generated model output
as canonical governance truth. They are coordination surfaces. Governance meaning
comes from the upstream contract and this repo's human-gated control plane.

## Canonical Scripture entry point

`logos-scripture-graph` owns the canonical 66-book Scripture graph.

Use this repo for:

- canonical 66-book Scripture passage records;
- canonical Scripture chunking;
- canonical Scripture gold/evaluator surfaces;
- Scripture stress atlas and review packets;
- canonical Scripture graph outputs.

Bible-first chunking priority:

- The highest chunking priority is a highly reliable, near-perfect / perfectly governed chunker for
  the canonical 66-book Bible.
- Psalms are the current implementation lane because reviewed evidence and a candidate-skill seam
  already exist, not because Psalms are necessarily the hardest book.
- T351 through T356 keep the current route non-output-changing: Bible-wide triage is complete,
  T352 epistle packets remain pending review packets, T355 selected John 3 for owner review, and
  T356 records pending owner options for `John.3.1-John.3.36` / `john3_wj_speaker_boundary`.
  Do not move from packet/docket prep to implementation without later owner-reviewed gold and
  exact authorization.
- Revelation is a future hard-book atlas/review-packet lane for implementation and is currently in
  research/prep-only mode under selected `REV-T344-E`; Revelation implementation must wait until
  reviewed gold exists, stronger governed evidence is recorded, and a later owner implementation
  decision exists, and must route to apocalypse/Revelation-specific rules.
- Book-specific and genre-specific chunking rules must not leak globally.
- Future boundary, noncanonical, legal, commentary, reception, or master-chunker work must remain
  separate from and subordinate to canonical Bible chunking. If adaptation would degrade the Bible
  chunker, split or rebuild a separate chunker/harness instead.
- A future master chunker must not use a single shared global optimization objective across Bible
  and non-Bible corpora, and non-Bible training/eval cases must not tune canonical Bible behavior.
  It must isolate corpora, routes, skills, objectives, eval sets, default retrieval policy, and
  authority/trust profiles.
- The chunking theological decision register at
  `.ai/control/chunking_theological_decision_register.yaml` is a required governance surface for
  chunking/evaluator/gold/route/default-behavior decisions. It records owner decisions, theological
  risks, dependencies, non-authorizations, and supersession history; it does not authorize output
  changes by itself.
- The Bible chunking readiness map at `.ai/control/bible_chunking_readiness_map.yaml` records the
  whole-Bible destination, current algorithm readiness, lane sequence, lesson-storage surfaces, and
  next safe route. It is non-authorizing and currently points to T356 John 3 owner review, with
  T355 preserved as the prior WJ speaker/discourse policy selection.
- The Bible chunking research triage map at `.ai/control/bible_chunking_research_triage_map.yaml`
  classifies canonical lanes before more algorithm work. It is non-authorizing; `review_packet_ready`
  means ready for review packets, not ready to chunk. T352 creates pending epistle argument packets,
  not reviewed gold.
- Divine-name/title capitalization is a `research_first` lane. `God/god`, `LORD/Lord/lord`,
  `Spirit/spirit`, `Father/father`, `Son/son`, `Word/word`, `Christ/christ`,
  `Holy Spirit/holy spirit`, and divine-pronoun capitalization are translation/editorial evidence
  only. They do not by themselves authorize divine identity, Trinitarian relation, speaker
  attribution, graph edges, chunk boundaries, retrieval truth, or output changes.
- The divine capitalization inventory at `.ai/control/divine_capitalization_inventory.yaml`
  records observed token and phrase casing from canonical `eng-web` word tokens and translation
  witnesses. Read it before graph, retrieval, route, evaluator, review-packet, or chunk work cites
  capitalization. It is evidence only, validated by
  `scripts/validate_divine_capitalization_inventory.py`, and never authorizes identity, theology,
  graph edges, chunk boundaries, retrieval truth, or output changes.
- The words-of-Jesus marker inventory at `.ai/control/wj_marker_inventory.yaml` records observed
  WJ/red-letter token runs from canonical `eng-web` word tokens. Read it before Gospel discourse,
  speaker-boundary, graph, retrieval, route, evaluator, review-packet, or chunk work cites WJ/red
  lettering. It is evidence only, validated by `scripts/validate_wj_marker_inventory.py`, and
  never authorizes Jesus speaker attribution, speaker boundaries, discourse boundaries, graph
  edges, chunk boundaries, retrieval truth, reviewed gold, or output changes.
- The WJ speaker/discourse policy at `.ai/control/wj_speaker_discourse_policy.yaml` records how
  WJ/red-letter, punctuation, paragraphing, and narrative evidence may be weighed before speaker
  or discourse review. It selects `John.3.1-John.3.36` / `john3_wj_speaker_boundary` as the next
  exact owner-review target, but it does not authorize Jesus speaker attribution, speaker
  boundaries, discourse boundaries, reviewed gold, graph edges, chunk boundaries, retrieval truth,
  or output changes. It is validated by `scripts/validate_wj_speaker_discourse_policy.py`.
- The John 3 WJ owner-review docket at `.ai/control/john3_wj_owner_review_docket.yaml` records
  pending owner options for `John.3.1-John.3.36` / `john3_wj_speaker_boundary`. It does not select
  an option, approve parent or child spans, decide Jesus/narrator boundaries, promote reviewed
  gold, authorize graph edges, authorize chunk boundaries, authorize retrieval truth, or change
  output. It is validated by `scripts/validate_john3_owner_review_docket.py`.
- The Bible-wide chunking research registry at
  `.ai/control/bible_wide_chunking_research_registry.yaml` records a canonical 66-book research
  queue with use-when routing, book-level theological risks, source-metadata watchpoints, and
  future review-packet candidates. It does not authorize chunks, reviewed gold, route behavior,
  graph edges, retrieval truth, embeddings, source metadata authority, speaker attribution,
  boundary import, or implementation. It is validated by
  `scripts/validate_bible_wide_chunking_research_registry.py`.
- The source-metadata research atlas at `.ai/control/source_metadata_research_atlas.yaml` records
  observed metadata families and canonical surfaces for internal cross-references, Strong's-style
  numbers, lexical rarity, footnotes, headings, boundary markers, WJ/red-letter markers, speaker
  labels, formatting, and divine capitalization. It does not authorize Scripture truth, lexical
  truth, intertext truth, speaker attribution, graph edges, retrieval truth, reviewed gold, chunk
  boundaries, output changes, boundary import, or algorithm work. It is validated by
  `scripts/validate_source_metadata_research_atlas.py`.
- The apocalyptic/prophetic intertext dossier queue at
  `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml` records Revelation, Daniel,
  prophetic, Olivet discourse, cosmic-sign, temple-city, Psalm 2, and Zechariah intertext research
  cases while preserving multiple orthodox hermeneutic options. It does not authorize intertext
  truth, graph edges, retrieval truth, reviewed gold, chunk boundaries, output changes,
  Revelation implementation, boundary import, or an eschatological system. It is validated by
  `scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py`.
- The epistle argument theological issue dossier queue at
  `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml` records T352 pending epistle
  packet risks and future epistle issue candidates for election, covenant, law/gospel, assurance,
  sacramental language, faith/works, 1 Peter/Jude source-sensitive questions, and related
  argument-boundary risks. It preserves orthodox options without authorizing doctrine, reviewed
  gold, route behavior, graph edges, retrieval truth, chunk boundaries, output changes, boundary
  import, or epistle implementation. It is validated by
  `scripts/validate_epistle_argument_theological_issue_dossier_queue.py`.
- The Gospel/WJ discourse dossier queue at
  `.ai/control/gospel_wj_discourse_dossier_queue.yaml` records John 3, Sermon on the Mount,
  Farewell Discourse, Olivet discourse, textual-variant WJ, Revelation voice-shift, and non-Gospel
  WJ/dominical quotation risks. It preserves Jesus-speech, narrator-commentary, unresolved,
  parent-only, parent-with-child, variant-policy-first, Revelation-research-first, synoptic, and
  dominical-quotation review options without authorizing Jesus speaker attribution, speaker
  boundaries, discourse boundaries, reviewed gold, route behavior, graph edges, retrieval truth,
  chunk boundaries, output changes, boundary import, or Gospel/WJ implementation. It is validated
  by `scripts/validate_gospel_wj_discourse_dossier_queue.py`.
- The narrative/legal covenant dossier queue at
  `.ai/control/narrative_legal_covenant_dossier_queue.yaml` records Genesis, Sinai, Levitical
  ritual law, Deuteronomy, Joshua allotment, Samuel-Kings, Chronicles/Ezra/Nehemiah, and
  Matthew/Luke genealogy/birth narrative risks. It preserves scene, cycle, genealogy/list,
  law-code, covenant-speech, ritual, royal-annal, embedded-document, and Gospel narrative review
  options without authorizing covenant theology, law/gospel frameworks, typology, harmonization,
  source-critical partition, reviewed gold, route behavior, graph edges, retrieval truth, chunk
  boundaries, output changes, boundary import, or implementation. It is validated by
  `scripts/validate_narrative_legal_covenant_dossier_queue.py`.
- The wisdom/dialogue/poetry dossier queue at
  `.ai/control/wisdom_dialogue_poetry_dossier_queue.yaml` records Job dialogue cycles, Proverbs
  wisdom speeches, Proverbs 31, Ecclesiastes refrains, Song speaker-boundary and genre risks,
  Lamentations acrostics, and Psalm 119. It preserves local-poem, parent-cycle,
  parent-with-child-stanza, dialogue-speech-cycle, acrostic, refrain, speaker-boundary,
  wisdom-argument, and lament review options without authorizing wisdom theology, speaker
  attribution, speaker boundaries, allegorical/literal readings, liturgical use, reviewed gold,
  route behavior, graph edges, retrieval truth, chunk boundaries, output changes, boundary import,
  or implementation. It is validated by
  `scripts/validate_wisdom_dialogue_poetry_dossier_queue.py`.
- The prophetic/oracle/vision dossier queue at
  `.ai/control/prophetic_oracle_vision_dossier_queue.yaml` records Isaiah servant/comfort oracles,
  Jeremiah restoration/new covenant material, Ezekiel restoration and temple visions, Daniel
  prophetic-apocalyptic visions, Hosea sign-act/covenant metaphor, Joel day-of-Yahweh/Spirit
  material, and Zechariah night visions. It preserves local-oracle, parent-oracle-cycle,
  vision-report, symbolic-action, judgment/hope-pair, servant-song, temple-vision,
  day-of-Yahweh, and prophetic-book-frame review options without authorizing fulfillment theology,
  eschatological systems, covenant systems, Israel/church relations, messianic identification,
  temple theology, reviewed gold, route behavior, graph edges, retrieval truth, chunk boundaries,
  output changes, boundary import, intertext truth, or implementation. It is validated by
  `scripts/validate_prophetic_oracle_vision_dossier_queue.py`.
- The textual-variant/source-tradition dossier queue at
  `.ai/control/textual_variant_source_tradition_dossier_queue.yaml` records Mark 16 longer-ending,
  John 7:53-8:11 pericope adulterae, Acts empty witnesses, Romans doxology, Deuteronomy 32,
  Jeremiah MT/LXX, Jude noncanonical references, Daniel/Esther boundary routing, and 1 John 5:7
  risks. It preserves variant-policy-first, canonical-text-only, source-tradition comparison,
  footnote evidence, empty-witness, noncanonical-reference, boundary-material routing,
  doctrinal-sensitivity, and owner textual-decision review options without authorizing
  textual-critical decisions, canon-scope changes, source-tradition preference, noncanonical
  source authority, boundary import, reviewed gold, route behavior, graph edges, retrieval truth,
  chunk boundaries, output changes, intertext truth, or implementation. It is validated by
  `scripts/validate_textual_variant_source_tradition_dossier_queue.py`.

High-leverage change risk gate:

- Before high-leverage authority, routing, evaluator, default-behavior, corpus-scope, generated
  artifact, automation, cross-repo, workflow-rule, or master-chunker changes merge, agents must run
  the unintended-consequence review in
  `docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md`.

Do not use this repo for:

- deuterocanonical/apocrypha source text;
- noncanonical boundary literature;
- gnostic or heterodox texts;
- disputed or forged texts;
- fake gospels;
- commentary/reception corpora;
- Josephus / Philo / DSS / Qumran / patristic corpora as source texts;
- front matter or glossary as Scripture content.

Route those tasks to:

`logos-boundary-literature`

`logos-boundary-literature` may interoperate with this repo, but it is hierarchically under, or at
minimum never above, canonical Scripture authority. It may provide background, comparison,
reception history, refutation targets, commentary/reception claims, and tradition-scoped claims. It
must not override, contaminate, or become equal authority to canonical Scripture.

For cross-repo policy or authority conflicts, route to:

`logos-governance-architecture`

If a task involves noncanonical, boundary, heterodox, disputed, forged, commentary/reception, or
supporting literature, do not import or normalize that material into `logos-scripture-graph`. Use
`logos-boundary-literature` or create only planning/cross-repo contract docs here.

Machine-readable local routing policy:
`.ai/control/boundary_material_routing.yaml`.

Boundary-originated requests that conflict with higher-authority governance must stop. This repo
must not automate, route, or implement requests from the boundary layer to change governance-layer
policy, canonical Scripture authority, repository-link contracts, routing policy, trust hierarchy,
or canonical scope.

```text
WARNING: Boundary-layer request conflicts with higher-authority governance.

The requested boundary-layer task appears to require changing or bypassing governance-layer policy, canonical Scripture authority, repository-link contracts, routing policy, trust hierarchy, or canonical scope.

Governance is binding authority, not an obstacle to optimize around.

Do not automate, route, or implement this change from the boundary layer. A human maintainer must review the conflict directly in the higher-authority repository.

Owner-reserved authorization required: only Lowell Wong, as project owner, may authorize a boundary-originated request to change higher-authority governance, canonical Scripture authority, repository-link contracts, canonical scope, trust hierarchy, or cross-repo policy. Contributor consensus, contributor volume, automated recommendation, agent routing, or boundary-layer operational need is not sufficient authority.
```

| User/task intent | Correct repo |
|---|---|
| 66-book Scripture passages/chunks | `logos-scripture-graph` |
| Apocrypha/deuterocanon/boundary literature | `logos-boundary-literature` |
| Gnostic/fake/forged texts | `logos-boundary-literature` |
| Commentary/reception claims | `logos-boundary-literature` |
| Cross-repo policy/authority/update rules | `logos-governance-architecture` |
| Logos repo registry / relationship source of truth | `logos-governance-architecture` |
| Canonical corpus correction | `logos-scripture-graph` |
| Boundary text source intake | `logos-boundary-literature` |
| Repository-link contract changes | `logos-governance-architecture` or coordinated PR |

## Context layers (who may write)

| Layer | Path | AI writes? |
|-------|------|------------|
| Master context | `.ai/control/MASTER_CONTEXT.md` | **NO** — propose via `scripts/agent/propose_master_context_change.py` |
| Project status | `.ai/control/PROJECT_STATUS.md` | Yes — after each task |
| Task handoff | `.ai/handoffs/T###/handoff.md` | Yes — task agent only |
| Audit reports | `.ai/audits/reports/` | Yes — independent review outputs; not authorization |
| Agent work notes | `.ai/context/agent_work/` | Yes — non-authoritative |
| Recommendations | `.ai/context/recommendations/` | Yes — proposals only |

Human promotes master context changes via `scripts/agent/approve_master_context.py`.

## Validation gates (CI green/red)

Before stopping work, run:

```bash
python scripts/validate_all.py
python -m pytest -q
```

Individual gates:

```bash
python scripts/validate_repo.py
python scripts/validate_control_plane.py   # master context lock + front-door routing
python scripts/validate_repository_link_contract.py
python scripts/agent/validate_handoffs.py
python scripts/validate_task_scope.py
python scripts/validate_chunking_theological_decision_register.py
python scripts/validate_bible_chunking_readiness_map.py
python scripts/validate_chunking_agent_preflight.py
python scripts/validate_source_metadata_research_atlas.py
python scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py
python scripts/validate_epistle_argument_theological_issue_dossier_queue.py
python scripts/validate_gospel_wj_discourse_dossier_queue.py
python scripts/validate_narrative_legal_covenant_dossier_queue.py
python scripts/validate_wisdom_dialogue_poetry_dossier_queue.py
python scripts/validate_prophetic_oracle_vision_dossier_queue.py
python scripts/validate_textual_variant_source_tradition_dossier_queue.py
python scripts/validate_audit_surface_map.py
python scripts/validate_owner_selection_implementation_gate.py
python scripts/validate_source_metadata_authority.py
```

**CI fails red** if any gate fails. Agents must not mark tasks complete with failing validation.

A merged PR does not automatically authorize the next task. Read the next task file, roadmap state,
and handoff before creating a branch or making changes.

## Raw source inspection (HARD RULE — mandatory before processing)

The whole pipeline exists to ingest, chunk, and graph the **raw source documents**
under `data/raw/`. The actual job is defined by what those files really contain
(USFM markers, Strong's lexeme tags, words-of-Jesus `\wj`, alternate readings
`\fqa`, superscriptions `\d`, poetry `\q*`, footnotes, cross-references).

For any ingest, chunking, review-packet, evaluator, route, graph, or retrieval work, agents must
first read `.ai/control/chunking_agent_preflight.yaml`. Source metadata is evidence, not authority:
internal cross-references, Strong's-style word numbers, lexeme tags, footnotes, headings, red-letter
or `\wj` markers, paragraph/poetry markers, alternate readings, and edition formatting may be
preserved and surfaced for review, but they do not automatically authorize Scripture truth, lexical
truth, intertext claims, speaker attribution, graph edges, chunk boundaries, or output changes.
The same rule applies to divine-name/title capitalization such as `God/god`, `Spirit/spirit`,
`Father/father`, `Word/word`, `LORD/Lord/lord`, and divine-pronoun capitalization.
`python scripts/validate_source_metadata_authority.py` fails closed if governed surfaces drift
toward source metadata authority.
`python scripts/validate_divine_capitalization_inventory.py` rebuilds the capitalization inventory
from canonical word tokens and translation witnesses and fails closed if it becomes stale or
authorizing.
`python scripts/validate_wj_marker_inventory.py` rebuilds/checks the WJ/red-letter inventory from
canonical word tokens and fails closed if it becomes stale or authorizing.
`python scripts/validate_wj_speaker_discourse_policy.py` fails closed if the WJ speaker/discourse
policy becomes authorizing, loses the John 3 selected target, or stops being mandatory preflight
context.
`python scripts/validate_john3_owner_review_docket.py` fails closed if the John 3 owner-review
docket becomes authorizing, selects an option before owner review, or stops being mandatory
preflight context.
`python scripts/validate_bible_wide_chunking_research_registry.py` fails closed if the Bible-wide
research registry loses canonical 66 coverage, becomes authorizing, or drops sensitive book-level
watchpoints.
`python scripts/validate_source_metadata_research_atlas.py` fails closed if the source-metadata
research atlas loses required metadata families, stale canonical source-surface counts, priority
cases, or evidence-only non-authorizations.
`python scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py` fails closed if the
apocalyptic/prophetic dossier queue becomes authorizing, loses required hermeneutic options,
misstates source cross-reference counts, drops required dossiers, or omits non-authorization
guards.
`python scripts/validate_epistle_argument_theological_issue_dossier_queue.py` fails closed if the
epistle argument issue queue becomes authorizing, loses required orthodox options, drops T352
pending-packet dependencies, treats pending packets as approved, or omits non-authorization guards.
`python scripts/validate_gospel_wj_discourse_dossier_queue.py` fails closed if the Gospel/WJ
discourse queue becomes authorizing, loses required WJ inventory counts, drops pending packet
dependencies, drops required Gospel/Revelation/non-Gospel WJ dossiers, treats WJ metadata as
speaker authority, or omits non-authorization guards.
`python scripts/validate_narrative_legal_covenant_dossier_queue.py` fails closed if the
narrative/legal covenant queue becomes authorizing, loses required narrative/legal evidence
channels, drops required dossiers, treats covenant/law/list/scene evidence as boundary authority,
or omits non-authorization guards.
`python scripts/validate_wisdom_dialogue_poetry_dossier_queue.py` fails closed if the
wisdom/dialogue/poetry queue becomes authorizing, loses required wisdom/poetry evidence channels,
drops required dossiers, treats dialogue/acrostic/refrain/speaker/parallelism evidence as boundary
authority, or omits non-authorization guards.
`python scripts/validate_prophetic_oracle_vision_dossier_queue.py` fails closed if the
prophetic/oracle/vision queue becomes authorizing, loses required prophetic/oracle/vision evidence
channels, drops required dossiers, treats oracle/vision/servant/temple/day-of-Yahweh/canonical-echo
evidence as fulfillment, graph, retrieval, or chunk-boundary authority, or omits
non-authorization guards.
`python scripts/validate_textual_variant_source_tradition_dossier_queue.py` fails closed if the
textual-variant/source-tradition queue becomes authorizing, loses required evidence channels,
drops Mark 16, John 7:53-8:11, Acts empty witnesses, Romans doxology, Deuteronomy 32, Jeremiah
MT/LXX, Jude, Daniel/Esther, or 1 John 5:7 dossiers, treats variant/source-tradition evidence as
textual-critical, canon, boundary-import, graph, retrieval, or chunk-boundary authority, or omits
non-authorization guards.

**Before designing or changing any ingest, chunking, or graph-processing logic, you MUST:**

1. Read `.ai/control/RAW_SOURCE_INVENTORY.md` (the generated first-pass inventory of the real raw documents).
2. Re-scan if data/raw changed: `python scripts/scan_raw_sources.py`.
3. Confirm every marker in the raw source is classified in `config/ingest/usfm_marker_coverage.yaml`.

Enforcement (these run in `validate_all.py` and CI — fail red):

```bash
python scripts/validate_raw_coverage.py     # fails if raw has an unclassified marker
python scripts/scan_raw_sources.py --check  # fails if the inventory is stale vs data/raw
```

A chunking/processing change is **not acceptable** unless it is demonstrably designed
against the markers that actually appear in `RAW_SOURCE_INVENTORY.md`.

## Operating modes

Agents must declare one mode at task start:

| Mode | Allowed actions |
|---|---|
| `explore` | Read, inspect, summarize, propose. No file mutations except handoff notes. |
| `plan` | Create or revise roadmap, ADRs, task plans, schema proposals. |
| `build` | Implement files/scripts/configs within assigned scope. |
| `validate` | Run checks, report failures, propose fixes. |
| `review` | Evaluate architecture/chunking/schema and recommend corrections. |

## Required task state

Every non-trivial task must have:

```text
.ai/tasks/<task_id>.task.yaml
.ai/handoffs/<task_id>/handoff.md
```

Use:

```bash
python scripts/agent/force_handoff.py --task-id T000 --agent "agent-name" --stage start
```

Then update the same handoff at the end of the task.

## Required completion checklist

Before stopping work, every agent must:

1. Read `MASTER_CONTEXT.md` and `PROJECT_STATUS.md` at task start.
2. Update its handoff file.
3. Record files changed.
4. Record architectural decisions or open questions (recommend master context changes if architectural).
5. Update `PROJECT_STATUS.md` if task status or blockers changed.
6. Update `ROADMAP_STATE.yaml` if task status changed.
7. Append to `.ai/control/roadmap_events.jsonl` if roadmap scope/status changed.
8. Regenerate the data/endpoint map if data, schemas, or pipelines changed: `python scripts/generate_data_map.py`.
9. Run `python scripts/validate_all.py` and `python -m pytest -q` — or explain why they could not run.
10. Leave the repo in a state another agent can resume.
11. For chunking-related paths, update `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
    or document the no-change rationale required by `.ai/control/METHODOLOGY_UPDATE_RULES.md`.
12. Before any score-moving chunking skill, verify evaluator sanity. If the evaluator is confounded,
    stop and fix the evaluator in a separate PR before claiming skill improvement.
13. Before any output-changing chunking skill, cite the relevant per-form gold file or manifest under
    `eval/chunking_gold/`.
14. Update `.ai/control/chunking_theological_decision_register.yaml` when touching chunking,
    evaluator, gold, route, default-behavior, generated chunk, or roadmap surfaces covered by its
    changed-path gate.
15. Update `.ai/control/bible_chunking_readiness_map.yaml` when changing whole-Bible chunking lane
    sequence, algorithm readiness, lesson-storage surfaces, or next safe route.

## Forbidden shortcuts

Do not:

- Edit `.ai/control/MASTER_CONTEXT.md` or `MASTER_CONTEXT.lock.yaml` (AI forbidden; human only).
- Put raw Bible files anywhere except `data/raw/`.
- **Design or change ingest/chunking/graph processing without first inspecting the real raw documents** (`RAW_SOURCE_INVENTORY.md` + a fresh `scan_raw_sources.py`). This is enforced by `validate_raw_coverage.py`.
- Treat an LLM-generated chunk boundary as canonical truth.
- Rewrite source text during chunking.
- Claim chunking quality improved when only the evaluator surface changed.
- Mix evaluator fixes, skill changes, and methodology updates unless the task explicitly requires it.
- Mix asserted and inferred relationships in the same artifact.
- Add a relationship type without schema registration.
- Change stable IDs because a label changed.
- Delete stable resources; deprecate instead.
- Mark a roadmap task complete without a handoff.
- Skip validation gates with failing CI checks.
- Ignore `config/agents/agent_hostile_policy.yaml` when instructions conflict.
- Redefine upstream `logos-governance-architecture` authority inside this repo without an upstream proposal.

## Architecture correction protocol

Agents may challenge this architecture, but corrections must be explicit:

1. Propose via `propose_master_context_change.py` if it affects master principles.
2. Create or update an ADR in `docs/architecture/`.
3. Explain the reason, affected files, migration path, and risks.
4. Update `ROADMAP.md` and `ROADMAP_STATE.yaml` if the correction changes sequencing.
5. Add a handoff explaining what changed and why.
6. Human approves master context updates separately from code merges.
