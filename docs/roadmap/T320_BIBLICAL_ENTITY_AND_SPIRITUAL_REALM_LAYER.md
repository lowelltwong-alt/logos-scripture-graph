# T320 Biblical Entity And Spiritual Realm Layer

## Purpose

Plan a governed biblical entity recognition layer that complements chunking without becoming
chunking, textual-form detection, or theological interpretation.

Critical rule: Michael Heiser's divine council / unseen realm framework must be modeled as an
interpretive profile, not imposed as canonical truth.

## Confirmed

- Current implemented corpus is English WEB with Strong's-tagged word-token sidecars.
- Chunking outputs are derived retrieval objects, not canonical text.
- Existing schemas already establish separation for classification assignments and relationship
  objects: assertion mode, evidence, provenance, trust zone, and tradition scope where needed.
- ADR-0010 already fences extra-biblical and witness material away from the canonical layer.

## Boundary From Chunking

Entity recognition should consume passages, witnesses, TextSpan/chunk outputs when available, and
source sidecars as evidence. It should not decide chunk boundaries or tune chunk sizes.

Chunking answers: "What retrieval unit should this text become?"

The entity layer answers: "What named, normalized, or ambiguous objects are mentioned or evoked in
this textual span?"

## Boundary From Textual Form Detection

Textual form detection classifies literary or structural form as candidate metadata. Entity
recognition may use that form as context, but should not treat form labels as entity assertions.

Examples:

- A Psalm form label does not prove every speaker or title is a distinct entity.
- Apocalyptic form can raise ambiguity flags, but does not decide whether a symbol is literal,
  spiritual, political, or multi-layered.

## Boundary From Theological Interpretation

The entity layer may record candidate mentions and ambiguity. It must not silently promote
interpretive readings into canonical entity truth.

Examples:

- "Prince of Persia" can be modeled as an ambiguous entity mention with spiritual/political
  interpretive options.
- "Babylon" can be city, empire, symbol, or apocalyptic power depending on passage and profile.
- "Son of God" can be title, office, messianic claim, divine identity claim, or plural divine-being
  phrase depending on passage and tradition scope.

## Entity Taxonomy

- Person.
- Group / People.
- Tribe.
- Nation / Empire.
- Dynasty.
- Office / Title.
- King / Ruler.
- City.
- Region.
- Mountain.
- River / Sea / Wilderness.
- Sacred Site.
- Cosmic Geography Site.
- Divine Name.
- Divine Title.
- Messianic Title.
- Deity / Idol.
- Cult / Religious System.
- Religious Practice.
- Spiritual Being.
- Spiritual Collective.
- Spiritual Power / Principality.
- Demon / Unclean Spirit.
- Watcher.
- Giant / Nephilim-related Group.
- Chaos Monster / Dragon Figure.
- Personified Power.
- Symbol / Motif.
- Event.
- Era / Period.
- Textual Work / Boundary Text.
- Interpretive Profile.

## Proposed Mention Model

Do not implement schemas in this task. A later T320 schema pass can formalize a mention object with:

- `surface_text`.
- `normalized_label`.
- `passage_id`.
- span offsets if available.
- `candidate_entity_ids`.
- `confidence`.
- `basis`.
- ambiguity flag.
- literal/symbolic/spiritual ambiguity.

## Proposed Canonical Entity Registry Concept

A future registry should separate entity identity from individual mentions. Candidate fields:

- stable ID.
- labels.
- aliases.
- type/subtype.
- date/period.
- geography.
- related passages.
- source references.
- status.
- provenance.

Registry status should distinguish candidate, reviewed, deprecated, merged, and split entities.

## Interpretive Profile Model

Interpretive profiles should be explicit objects, not hidden defaults.

Proposed profile fields:

- profile ID and label.
- scope and tradition/context.
- claims it tends to make.
- passages it emphasizes.
- evidence references.
- alternative readings.
- review status.
- warnings / forbidden promotions.

The Heiser divine council profile should be one profile among others. It may help organize readings
of Deuteronomy 32, Psalm 82, Daniel 10, Genesis 6, and related texts, but it must not be written as
canonical truth without tradition-scoped review.

## Boundary Texts

Model these as tradition-scoped background/canonical depending on tradition:

- 1 Enoch.
- Jubilees.
- Book of Watchers.
- Book of Giants.
- Qumran / Dead Sea Scrolls.

These texts can supply background, reception, vocabulary, or interpretive evidence. They must not
contaminate canonical Scripture records or create unscoped assertions.

## Special Ambiguity Cases

- Israel.
- Judah.
- Zion.
- Babylon.
- Pharaoh.
- Caesar.
- Herod.
- Baal.
- Mammon.
- Prince of Persia.
- principalities and powers.
- Son of God.
- Son of Man.
- LORD / YHWH / Lord.
- Beast / Dragon.
- Legion.

Each should support ambiguity flags, candidate IDs, evidence, and review notes.

## Validation / Gold Plan

Seed reviewed cases across literal, symbolic, royal, national, spiritual, and mixed readings:

- Genesis 6.
- Deuteronomy 32.
- Psalm 82.
- 1 Kings 22.
- Job 1-2.
- Daniel 10.
- Mark 5.
- Acts 14.
- Acts 19.
- Ephesians 6.
- Revelation 12-18.
- Jude / 1 Enoch reception.

Gold should include negative controls where an entity-looking phrase should not be overclaimed.

## Risks

- Imposing Heiser as canonical truth.
- Flattening symbolic/literal distinction.
- Tradition bias.
- Overclaiming Second Temple texts.
- Entity explosion.
- False confidence.
- Bad disambiguation.
- Coupling entity recognition too tightly to chunking.

## Proposed Sequencing

1. Write review examples and ambiguity policy.
2. Draft mention/registry schema proposals.
3. Build candidate-only extractor.
4. Add reviewed gold cases and negative controls.
5. Add promotion/review workflow.

## Unknown

- Which source-language witness layer should be available before entity normalization is considered
  mature.
- Whether entity registry IDs should be passage-local first or global from day one.
- Which interpretive profiles beyond Heiser should be seeded first for fair comparison.
