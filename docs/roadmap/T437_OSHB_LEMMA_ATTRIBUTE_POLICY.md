# T437 OSHB Lemma Attribute Policy

Status: implementation.
Trust zone: control and candidate evidence only.

T437 closes the metadata-policy gap found by T436: OSHB canonical source-view XML exposes `w@lemma` attributes and maps them to `Strong`, but this repo must not treat those attributes as local lemma rows, Strong's overlay rows, lexical truth, preferred readings, or theology authority.

## Policy

For `openscriptures_oshb`:

- `contains_source_provided_lemmas: false`
- `contains_source_provided_lemma_attributes: true`
- `contains_source_provided_strong_lookup_hints: true`
- `contains_source_provided_strongs: false`
- `lemma_attribute_interpretation: strong_lookup_hint`
- `lemma_attribute_authority: metadata_only_not_local_lemma_or_strong_authority`

This means OSHB exposes a source XML attribute named `lemma`. It does not mean T437 authorizes local lemma population, Strong's IDs as source text, lexical truth, source-tradition preference, translation judgment, chunking, KG, retrieval, or theology authority.

Plainly: OSHB `w@lemma` is treated as a strong lookup hint, not local lemma authority. T437 creates no theology authority.

## Rust Policy

No Rust expansion is authorized by T437.

T437 only clears the metadata-policy part of the blocker. A later Rust task still needs source-specific UXLC/OSHB parser contracts, no-text generated ledgers, Python authority validation, and parity proof before Hebrew scanning can scale.

## Validator Hardening

T437 adds checks that:

- OSHB allowlist, raw source manifest, canonical source-view manifest, and all 39 included rows agree on the policy.
- OSHB `w@lemma`/`workPrefix` cannot silently contradict the metadata policy.
- T436 parity output is regenerated as policy-covered while still disallowing Rust expansion.
- No source text, lemma values, morphology values, Strong's values, production evidence roots, preferred readings, graph/retrieval truth, or theology authority are created.
