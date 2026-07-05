# T432 Original-Language Schema Contracts

Status: implementation, non-authorizing.
Task family: T430-T437.

T432 hardens the schema contracts that future original-language evidence rows must satisfy. It does not populate source-language tokens, Strong's overlays, lexeme rows, morphology rows, variants, witness-support rows, manuscript transcriptions, manuscript images, translation judgments, KG edges, retrieval truth, chunks, reviewed gold, or theology authority.

## Purpose

T431 downloaded allowlisted raw source packages and built canonical-only source views. T432 now defines the contracts future tasks must obey before any source-language evidence can be generated from those views.

The contracts are intentionally conservative:

- source-language tokens are observations from licensed source views, not replacement Scripture authority;
- Strong's numbers are lookup and alignment hints, not Greek/Hebrew text or theology authority;
- lemmas and morphology require phrase, clause, syntax, discourse, genre, and canonical context;
- variants expose uncertainty and witness support without choosing a preferred reading;
- oldest-known witness and highest-confidence witness are separate evidence claims;
- punctuation, capitalization, accents, vowel points, paragraphing, headings, versification, and red-letter/WJ formatting are editorial or transmission layers unless later evidence proves otherwise.

## Schemas

T432 adds or hardens:

- `schemas/source_language_token.schema.json`
- `schemas/editorial_layer.schema.json`
- `schemas/lexeme.schema.json`
- `schemas/alignment_record.schema.json`
- `schemas/textual_variant.schema.json`
- `schemas/witness.schema.json`

Each candidate evidence schema must require provenance, confidence or rights/context fields as applicable, non-authorizations, and authority flags that deny source-language truth, preferred reading, source-tradition preference, canon change, chunk authority, graph/retrieval truth, translation-faithfulness judgment, and theology authority.

## Rust Boundary

T432 does not add Rust. This is deliberate.

Rust is the right tool later for T435 when the repo needs deterministic high-volume scanners and validators over stable source-token, alignment, variant, or witness ledgers. T432 is a semantic contract layer, so Python validators and JSON Schema are the right first gate.

## Next Route

After T432 validates, the next safe implementation route is T433: a tiny candidate evidence pilot, preferably Philemon for Greek or Jonah for Hebrew, using T431 canonical source views and T432 schemas. T433 must stay candidate/evidence-only unless a later owner gate authorizes promotion.
