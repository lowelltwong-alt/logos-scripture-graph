# T330 Theological Concept Graph

## Purpose

Plan a later layer that connects entities, doctrines, motifs, concepts, and interpretations while
preserving evidence, scope, and review boundaries.

## Confirmed

- The repo already requires asserted, inferred, and candidate material to remain separated.
- Relationship objects require subject, predicate, object, assertion mode, evidence refs,
  confidence, status, and optional provenance/trust-zone fields.
- The current repo is the Scripture data-plane / knowledge-plane implementation, not a final
  runtime or answer engine.

## Entity Layer vs Concept Graph

The entity layer identifies and normalizes mentions of people, places, nations, spiritual beings,
symbols, events, and related objects.

The concept graph connects those objects and passages to theological concepts, doctrines, motifs,
interpretive claims, and tradition-scoped readings.

Entity example:

- "Babylon" as city, empire, or symbolic power candidate.

Concept graph example:

- A scoped claim that Babylon functions as an image of rebellious empire in a reviewed interpretive
  profile, with evidence refs and tradition scope.

## Concepts As Scoped Claims

Concepts should not be stored as universal truth by default. They should carry:

- assertion mode.
- tradition scope where applicable.
- evidence refs.
- provenance.
- confidence.
- review state.
- source / profile basis.

A concept link can be direct textual support, inferred theological relation, candidate motif link,
or tradition-scoped doctrinal reading. These should not collapse into one predicate.

## Direct Support vs Inferred Relation

Direct textual support:

- The passage explicitly names or teaches the concept.
- Evidence is local and text-grounded.

Inferred theological relation:

- The relation depends on synthesis, typology, systematic theology, reception history, or a profile.
- Evidence must include the inferential basis and reviewer/provenance.

## Tradition-Scoped Readings

Tradition-dependent claims should require explicit scope. Examples include doctrinal formulations,
typological fulfillment, canon status, liturgical use, and contested theological categories.

The graph should support multiple scoped readings without forcing one into canonical data.

## Boundary From Heiser Profile

Heiser-style divine council readings may be represented as an interpretive profile with evidence and
alternatives. The concept graph should make profile membership visible instead of making it an
unlabeled default relation.

Examples:

- `profile:heiser-divine-council` may propose links between Psalm 82, Deuteronomy 32, Daniel 10,
  and spiritual-power concepts.
- Alternative readings remain modelable beside it.

## Boundary From Noesis / Comparative Worldview Work

Comparative worldview or Noesis-style analysis can inform candidate concepts, contrastive lenses,
or external-profile notes. It should not bypass Scripture evidence, tradition scope, or review.

Any comparative-worldview relation should be marked as interpretive or candidate until reviewed.

## Provenance, Evidence, And Review

Every theological concept relation should answer:

- What text or source supports it?
- Is it directly asserted, inferred, candidate, or tradition-scoped?
- Who or what created the claim?
- What profile, doctrine, or review basis is being used?
- What should downstream retrieval/rendering disclose to the user?

## Relation To LawFirm OS Export

Future LawFirm OS export is conceptual only at this stage. Do not export the T330 graph plan as a
finished generalized doctrine or methodology. Export should wait until the repo has reviewed
examples showing how scoped concepts, evidence, profiles, and disputed readings survive real use.

## Proposed Sequencing

1. Define concept-claim maturity labels.
2. Draft a concept relation registry.
3. Seed a small reviewed gold set.
4. Build candidate-only concept extraction/linking.
5. Add review-ready diff reports.
6. Connect retrieval/rendering contracts only after evidence bundles are clear.

## Unknown

- Which concept predicates should be first-class and which should remain profile-local notes.
- What review quorum is required for doctrine-level active assertions.
- How much source-language and reception-history evidence is required before promotion.
