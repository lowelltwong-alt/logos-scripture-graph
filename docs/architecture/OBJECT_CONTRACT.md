# Object Contract (DNA fields) + address spine

Every governed object in this substrate — across scales (work → book → pericope →
passage → token → variant → claim → extra-biblical link) — should answer the same
DNA questions. This is the fractal contract from the project's architecture note
(`fractal_taxonomy_ontology_address_system`), applied here (taxonomy-scaffold v0.2 Patch 7).

## Minimal object contract

```yaml
id:            unique deterministic identifier
address:       8-layer semantic location (see below)
type:          taxonomy classification (object type)
meaning:       ontology reference (concept/relation), where applicable
relations:     linked objects (often via RelationshipObject)
lineage:       source / derived_from
evidence:      supporting source references
trust_zone:    canonical | asserted | inferred | candidate | derived | context
state:         candidate | active | deprecated | archived
ai_usage:      allowed | restricted | prohibited
provenance:    {created_by, created_at, basis, license}
version:       semantic or date version
```

If an object cannot answer these at the appropriate level, it is immature.

## Address spine

Use the 8-layer address as the canonical identity spine (the governance repo's
`docs/governance/eight-layer-address-system.md` is the authority):

```text
/<system>/<layer>/<domain>/<module>/<object_type>/<object_id>@<version>#<state>
```

Example (a passage):

```text
/logos-scripture-graph/knowledge/bible/scripture/passage/Ps.51@v1#active
```

The 9th "view/projection" layer is a retrieval parameter, not permanent identity.

## How this maps to existing records

The substrate's existing records already carry most DNA fields under different
names (`id`, `source_id`/`source_sha256` = lineage/evidence, `license`,
`generation_method` = provenance basis, `status` = state, `canon_profiles` =
tradition scope). New objects (Witness, TextualVariant, Lexeme, SemanticDomain,
TranslationNote, AlignmentRecord, ExtraBiblicalSource, ClassificationAssignment)
adopt the contract explicitly.

## Why it matters for growth

Because each object self-declares `layer` + `trust_zone` + `assertion_mode`,
extra-biblical, witness, and inferred material can attach **fractally** to the
graph without contaminating the canonical biblical layer — the fence is carried by
every object, not enforced by location alone.
