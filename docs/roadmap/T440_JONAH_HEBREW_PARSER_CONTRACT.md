# T440 Jonah Hebrew Parser Contract

Status: source-specific parser contract, non-authorizing.
Task: T440.

T440 defines the UXLC and OSHB Jonah parser contracts needed before any Hebrew Rust expansion. It consumes the T436 no-text Jonah parity pilot and the T437 OSHB lemma-attribute policy cover.

This is not a source-token population task, Strong's overlay task, morphology task, alignment task, witness task, preferred-reading task, translation-faithfulness task, KG task, chunking task, reviewed-gold task, or theology authority task.

## Contract Scope

T440 covers only Jonah, only from the T431 canonical source views:

- `tanach_us_uxlc/files/Jonah.xml`
- `openscriptures_oshb/files/Jonah.xml`

It records:

- expected Jonah counts: 4 chapters, 48 verses per source, 688 tokens per source;
- UXLC XML shape and no local lemma/morph/Strong attribute semantics;
- OSHB OSIS XML shape and metadata semantics;
- OSHB `w@lemma` as Strong lookup-hint metadata, not local lemma or Strong authority;
- OSHB `w@morph` as source morphology metadata, not local morphology-row authority;
- negative fixture requirements for T441.

## Rust Policy

No Rust is added in T440.

T440 makes T441 design possible by proving the parser contracts Rust must obey. T441 may separately add a no-text Rust scanner/checker for deterministic work:

- source-view file checksum checks;
- Jonah ref and token-count coverage;
- duplicate source-token IDs;
- no-text output enforcement;
- field-name semantic guardrails;
- production-root closure checks.

Rust must not decide source-language truth, lexical truth, word-level alignment truth, preferred readings, source traditions, translation faithfulness, KG/retrieval truth, chunks, reviewed gold, or theology.

## Why Count Parity Is Not Enough

T436 proved UXLC and OSHB have matching Jonah refs and per-verse token counts. It also recorded that exact token hashes do not all match. That is useful coverage evidence, but not semantic authority.

T440 therefore records parser-specific meaning before acceleration:

- UXLC token words have no local lemma, morphology, or Strong source attributes.
- OSHB exposes `id`, `lemma`, and `morph` attributes.
- OSHB `lemma` is policy-covered as a Strong lookup hint.
- OSHB `morph` is source metadata, not local morphology-row population.

## Non-Authorizations

T440 authorizes no visible Hebrew text storage, raw archive direct consumption, production original-language roots, source-token rows, alignment rows, Strong's overlay rows, local lemma/morphology rows, variants, witness support, preferred readings, source-tradition choices, translation judgments, KG/retrieval truth, chunks, reviewed gold, embeddings/indexes, or theology authority.
