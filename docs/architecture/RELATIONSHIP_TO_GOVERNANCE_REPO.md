# Relationship to logos-governance-architecture (and the taxonomy scaffold)

The `bible-kg-taxonomy-scaffold` review (v0.2) found three parallel ontologies.
This repo's role in the split is recorded here so they reconcile instead of forking.

## The split (decided 2026-06-04)

| Concern | Home | Why |
|---------|------|-----|
| **Classification taxonomy** (TextualForm/SpeechAct/RedemptiveHistory/AffectiveTone/LiturgicalUse/EthicalDomain/MoralUse/Typology), tradition + canon-scope vocabulary | **logos-governance-architecture** (tag-registry) | It is shared theological/literary vocabulary, governed upstream. |
| **Structural schemas + data** (passages, witnesses, variants, lexemes, alignments, extra-biblical sources, classification assignments) + ingest/chunking/CI | **logos-scripture-graph** (this repo) | This is the deterministic, data-backed, CI-enforced substrate. |

## What this repo provides (the structural half of v0.2)

- `schemas/classification_assignment.schema.json` — assigns a governance-taxonomy
  value to a scripture object **with enforced assertion_mode + provenance** (interpretive
  axes can never be `asserted_textual`; doctrine/canon/typology require `tradition_scope`).
- `schemas/witness.schema.json`, `schemas/textual_variant.schema.json` — critical apparatus
  (DSS/LXX/papyri growth path).
- `schemas/lexeme.schema.json`, `semantic_domain.schema.json`, `translation_note.schema.json`,
  `alignment_record.schema.json` — original-language + lost-in-translation layer (ADR-0010).
- `schemas/extra_biblical_source.schema.json` — fenced non-canonical context.
- `docs/architecture/OBJECT_CONTRACT.md` — DNA contract + 8-layer address.

## What the governance repo provides (the vocabulary half)

The multi-axis classification taxonomy (with the missing genres: genealogy,
superscription/colophon, ANE covenant-treaty form, Selah/rubric, annals/regnal,
etiology, qinah, Aramaic-section flag) and the asserted/inferred/tradition rules,
landed as a tag-registry extension. `ClassificationAssignment.axis`/`value` here
reference those controlled values.

## The scaffold itself

`bible-kg-taxonomy-scaffold.zip` is preserved as a **proposal record** and marked
superseded by this split. Its strongest contribution (the multi-axis taxonomy) is
promoted to the governance repo; its object/schema layer is superseded by the
schemas here (which are deterministic, data-backed, and CI-validated).

## Non-negotiable

Do not re-introduce a third ontology. New scripture object types land here; new
classification vocabulary lands in the governance tag-registry; the two reference
each other by stable id.
