# T340 Retrieval / Rendering Contracts

## Purpose

Plan future retrieval and rendering over the graph without implementing runtime behavior.

## Confirmed

- This repo owns governed source truth, derived chunks, candidate/asserted graph claims, schemas,
  validation, and release artifacts.
- Runtime/orchestration is a separate future consumer.
- Chunks, entities, concept claims, and relationship objects must preserve provenance and trust-zone
  boundaries.

## Same Graph, Different Entry Points

The same normalized graph should support several entry points:

- passage-first.
- entity-first.
- concept-first.
- relationship-first.
- evidence-first.
- review-first.

Entry points should change retrieval shape, not underlying truth.

## Retrieval Separate From Rendering

Retrieval should return normalized objects, evidence, scopes, and ranked neighborhoods.

Rendering should decide how to present those objects for a user, reviewer, or downstream runtime.

Do not make the renderer responsible for inventing evidence, collapsing assertion modes, or hiding
interpretive scope.

## Normalized Object Set

A retrieval result should be able to return a normalized object set such as:

- Scripture passages / spans.
- Translation witnesses.
- Retrieval chunks.
- Context packets.
- Entity mentions and entity registry records.
- Relationship objects.
- Concept claims.
- Evidence refs.
- Interpretive profiles.
- Review state.

## Proposed View Contracts

Evidence bundle view:

- Shows passages, witnesses, evidence refs, provenance, assertion mode, confidence, and review state.
- Best for audit, review, and contested claims.

Graph neighborhood view:

- Shows local nodes and edges around a passage, entity, concept, or relationship.
- Must preserve asserted / inferred / candidate / interpretive boundaries.

Short synthesis view:

- Produces a concise summary from retrieved evidence.
- Must cite the evidence bundle and disclose profile/tradition scope.

Review-ready diff view:

- Compares candidate, inferred, and asserted states.
- Shows added/removed/changed claims and the evidence behind each change.

## Asserted / Inferred / Interpretive Separation

Every view must preserve:

- asserted textual facts.
- inferred machine or rule outputs.
- candidate AI outputs.
- tradition-scoped readings.
- interpretive profile claims.
- external/background context.

Rendering may group them for readability, but must not merge their authority.

## Proposed Sequencing

1. Define object-set shape and required provenance fields.
2. Draft view contracts as docs or schema proposals.
3. Validate with a small evidence bundle.
4. Add review-ready diff examples.
5. Only then wire runtime or UI consumers.

## Unknown

- Which views should be release artifacts versus runtime-only projections.
- Whether synthesis belongs in this repo or only in a downstream runtime.
- How much profile comparison should be available in first-pass rendering.
