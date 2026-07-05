# T450 Bible Edge Taxonomy Research Program

T450 is a planning-only control plane for future Bible graph edges. It does not generate edges, expand the predicate registry, populate candidate graph files, run retrieval/vector work, or authorize theology. It gives agents a shared map of edge families, evidence floors, escalation rules, and future validator work.

## Why This Exists

The Bible can support many useful connection types: direct quotations, allusions, prophecy, typology, covenant development, sacrifice and temple patterns, historical background, original-language relations, manuscript witnesses, Jewish calendar features, literary forms, discourse flow, apologetic uses, and polemic contexts.

Those are not all the same kind of claim. A deterministic occurrence edge is very different from a fulfillment edge or an apologetic argument. T450 separates the lanes so future agents do not smuggle theology, harmonization, source-tradition choices, or retrieval authority into graph structure.

## Current Predicate Boundary

The current registry is still limited to:

- `editorial_cross_reference`
- `quotesFrom`
- `alludesTo`
- `echoes`
- `fulfills`
- `typifies`
- `parallelTo`
- `thematicallyRelatedTo`
- `groundedIn`
- `renders`
- `occursIn`

Every additional predicate name in T450 is a proposal for research only. A later owner-gated task must review schema shape, registry wording, authority boundaries, and validator coverage before any new predicate can be used.

## Edge Family Lanes

The control file defines these future lanes:

- Structural source and occurrence
- Editorial metadata
- Intertext and canonical relations
- Prophecy and apocalyptic
- Orthodox creedal theology
- Covenant and biblical theology
- Sacrifice, temple, and priesthood
- Literary, discourse, and genre
- Chronology, calendar, and geography
- Linguistic and original-language evidence
- Manuscript and textual witness evidence
- Historical, cultural, and reception evidence
- Apologetic and polemic use

Each lane has a risk level, candidate predicate names, required evidence, escalation triggers, and non-authorizations. High-risk lanes require frontier review before any owner decision can promote them.

## Review Conveyor

Future edge work should follow this order:

1. Worker models propose candidate edge-family notes in scratch paths only.
2. Codex reviews the taxonomy, evidence quality, governance fit, and validator gaps.
3. Claude Opus or another frontier reviewer checks hard theology, prophecy, apocalyptic, WJ/speaker, variant, and apologetic-polemic cases.
4. The owner approves any exact predicate-registry expansion, candidate-row population, or reviewed graph-edge promotion.
5. Implementation happens in a separate narrow PR with validators.

## Orthodox And Non-Smuggling Guardrails

The program is intentionally credal and Scripture-centered. It rejects anti-supernatural or liberal-critical defaults as hidden assumptions, but it also does not let a model choose a denominational system. If theology must be represented, the claim must be explicit, traceable, reviewed, and limited in scope.

Source metadata is evidence only. Strong's numbers, WJ/red-letter formatting, headings, footnotes, cross-references, modern punctuation, capitalization, manuscript witness age, and model consensus cannot silently become authority.

## Rust Fit

Rust is a good fit later for deterministic high-volume edge hygiene:

- endpoint reference validation
- duplicate edge-key detection
- predicate registry membership checks
- provenance/evidence field presence
- large JSONL candidate scans
- no-authority leakage scans

Rust must not decide theology, fulfillment, typology, textual variants, source-tradition preference, apologetic force, or retrieval truth.

## DAD Lessons

T450 sends two candidate-only DAD messages:

- a reusable pattern for Bible-edge taxonomy lanes
- a dirty central-DAD coordination lesson for many repos reporting Rust rollout issues in parallel

DAD can help share assets, but local repo governance remains authoritative.

## Explicit Non-Authorization

T450 creates no theology authority and no graph edge authority. It is a planning-only taxonomy until a later owner-gated task authorizes exact predicates and data paths.
