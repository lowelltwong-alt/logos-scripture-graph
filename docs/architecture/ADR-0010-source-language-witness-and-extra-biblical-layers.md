# ADR-0010: Source-language, textual-witness, and extra-biblical layers

## Status

Accepted (contracts defined; population deferred) — 2026-06-04

## Context

The bible-kg-taxonomy-scaffold review (v0.2) surfaced gaps the substrate must be
*able to grow into* without rework:

- original-language reality: today's data is English (WEB) + **Strong's numbers only**
  (no morphology, no lemmas) — 514,990 Heb + 162,698 Grk tags;
- lost-in-translation: English surface wording hides original distinctions;
- textual witnesses/variants: the corpus already carries 519 `\fqa` alternate
  readings + 1,855 footnotes — a variant seed — and the project intends to grow
  toward DSS, LXX witnesses, papyri, codices, and manuscript variants;
- extra-biblical context: ANE texts, Second Temple lit, Greco-Roman background,
  inscriptions, archaeology, apologetics — which must attach **without contaminating
  the canonical biblical layer**.

## Decision

Define the contracts now (schemas), populate later. Five new schemas:

1. `lexeme.schema.json` — source-language lemma; Strong's is an explicit **v0 bridge, not morphology**.
2. `semantic_domain.schema.json` — Louw-Nida / SDBH domains.
3. `translation_note.schema.json` — structured lost-in-translation flags (idiom, ambiguity, gender/number, wordplay, gloss caveat).
4. `alignment_record.schema.json` — English token ↔ source token/lexeme (Strong's-bridged now; WLC/SBLGNT/MACULA later).
5. `witness.schema.json` + `textual_variant.schema.json` — critical-apparatus model (siglum, date-range, provenance, confidence; competing readings with witness support).
6. `extra_biblical_source.schema.json` — fenced non-canonical sources.

### The fence (anti-contamination)

- Every `ExtraBiblicalSource` MUST declare `layer: context` and a non-canonical
  `trust_zone`. It can never be `canonical`.
- Scripture↔extra-biblical links exist **only** as `RelationshipObject`s with
  `assertion_mode` + `tradition_scope` + evidence — never as properties of a
  `ScripturePassage`.
- Source-language witnesses (WLC/SBLGNT/LXX) are **separate** witnesses, not merged
  into English `TranslationWitness` (consistent with MASTER_CONTEXT multilingual path).

## Consequences

- The model can grow toward fragment/witness/provenance detail (DSS/LXX/papyri)
  and extra-biblical context without touching the canonical layer.
- Confidence is ordinal and dates are ranges — the apparatus never asserts more
  certainty than the evidence allows.
- Population (real lexical data, alignments, witnesses, ANE corpora) is sequenced
  after the English MVP; these schemas are the forward-compatible contracts.

## Relation to other ADRs

- Complements ADR-0003 (chunks derived), ADR-0005 (canon profiles), ADR-0007
  (provenance canonicalization). A future ADR-0006 will set source-language
  *boundary precedence* for chunking once real Hebrew/Greek text lands.
