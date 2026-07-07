# T433 Philemon Original-Language Evidence Pilot

Status: implementation.
Mode: candidate evidence pilot, non-authorizing.

## Purpose

T433 proves the first tiny Option 1 alignment-bridge slice from `docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md`: connect Greek source-token evidence to the current English WEB token layer without turning the connection into source-language truth, lexical authority, translation judgment, preferred reading, chunk authority, KG truth, retrieval truth, or theology authority.

The pilot span is exactly `Phlm.1.1-Phlm.1.3`.

## Source Choice

Primary source view: SBLGNT `Phlm.xml` from the T431 canonical source view.

SBLGNT is first because it exposes explicit XML `<w>` token elements for Philemon and its manifest records no source-provided Strong's, lemma, or morphology metadata. That keeps the first row-shape proof boring and auditable.

UGNT is deferred. The source package is metadata-rich at the manifest level, but the selected `Phlm.SFM` canonical source view does not visibly expose per-token Strong's or morphology fields. T433 therefore does not merge UGNT into pilot rows.

## Outputs

All pilot output stays under:

```text
data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/
```

Files:

- `manifest.yaml`
- `source_language_tokens.jsonl`
- `editorial_layers.jsonl`
- `alignment_records.jsonl`

The T432 production roots remain blocked:

- `data/candidate/original_language_evidence/source_tokens/`
- `data/candidate/original_language_evidence/strong_alignment/`
- `data/candidate/original_language_evidence/lemma_morphology/`
- `data/candidate/original_language_evidence/textual_variants/`
- `data/candidate/original_language_evidence/witness_support/`
- `data/candidate/original_language_evidence/editorial_layers/`

## Evidence Semantics

Source-language token rows are observed from the SBLGNT canonical source view. Surface Greek text is stored only because the SBLGNT license permits storage and this pilot records the source view lineage and checksum.

Alignment rows are verse-level, many-to-many, low-confidence bridge records from WEB word-token IDs to SBLGNT source-token IDs. They are not word-for-word alignment truth.

WEB Strong's IDs are recorded only as translation-side hints. They are not written into SBLGNT token rows and are not source text, lexical truth, translation-faithfulness proof, or theology authority.

Editorial-layer rows record paragraphing, versification, punctuation, and source-edition sigla as editorial evidence. They are not autograph certainty and do not authorize chunk boundaries or speaker/theology claims.

## Non-Authorizations

T433 authorizes no source-language truth, lexical truth, Strong's-as-source-text claim, preferred reading, source-tradition preference, textual-critical decision, canon-scope change, translation judgment, chunk boundary, reviewed gold, chunk output, route/evaluator behavior, graph edge, retrieval truth, embeddings/indexes, or theology authority.

## Rust Decision

No Rust is added in T433. The task is a three-verse semantic/schema pilot where Python is easier to inspect and review. Rust remains preferred for T435 once high-volume source-token, alignment, variant, and witness scanner row shapes are stable enough for parity fixtures.

## Next Route

After T433 validates, the next safe route is a Codex/Claude review of whether this pilot row shape is sufficient for a broader T435 Rust scanner/index lane or whether one more small Hebrew pilot, likely Jonah, is needed first.
