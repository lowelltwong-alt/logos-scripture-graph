# T438 Alignment Bridge Goal

Status: planning/control gate, evidence-only.
Task: T438.

T438 chooses the next original-language lane after T437: build the Greek/Hebrew-to-English alignment bridge first, while allowing manuscript custody-chain work to continue as catalog-only research in parallel.

This is not source-token population, reviewed gold, chunk output, KG work, source-tradition selection, preferred reading selection, translation-faithfulness judgment, or theology authority.

## Why This Route

The owner's long destination is an integrated evidence workbench that can show:

- Hebrew, Aramaic, and Greek source-token evidence;
- current English WEB alignment evidence;
- manuscript witness and fragment custody-chain metadata;
- textual variants and copying-error transparency;
- translation-faithfulness notes;
- early creed, hymn, confession, or tradition-formula evidence packets.

The safest route is not to build that all at once. The alignment bridge is the first practical spine because later manuscript, variant, translation, KG, and early-creed work all need stable passage/source-token/English-token references.

## Selected Next Lane

Primary lane: **Option 1, Greek/Hebrew-to-English alignment bridge**.

Parallel lane: **Option 2, manuscript custody-chain**, but catalog-only until source/license and witness-row gates are stronger.

Deferred lanes:

- Variant/copying-error ledger waits for textual-critical source and witness gates.
- Early-creed lane waits for citation packets and frontier review.
- Integrated workbench waits until the smaller lanes prove their fields.

## First Sequence

1. **T439 Greek Philemon bridge expansion contract**
   Start from T433 `Phlm.1.1-Phlm.1.3`, use SBLGNT as the clean source-token view, keep UGNT deferred until span-local metadata proof exists, and keep alignment rows candidate/low-confidence until reviewed.

2. **T440 Hebrew Jonah source-specific parser contract**
   Start from T436 Jonah no-text parity and T437 OSHB lemma-attribute policy cover. UXLC and OSHB parser assumptions must be fixture-covered before any Rust expansion.

3. **T441 Rust no-text alignment coverage index**
   Rust is a good fit for deterministic source-view and WEB sidecar scanning, ref coverage, hashes, duplicate IDs, and JSONL ledgers. Python remains the authority validator.

4. **T442 owner-gated production candidate-root opening packet**
   Only after pilots and parity proof should the repo decide whether to open production candidate roots for broader alignment evidence.

## Rust Policy

Rust should be used where it makes sense:

- deterministic XML/USFM/TSV source-view scans;
- no-text token-shape ledgers;
- source-view to WEB reference coverage joins;
- high-volume JSONL shape and duplicate checks;
- stable hash/count/index generation.

Rust should not own:

- theology, translation-faithfulness, or lexical judgment;
- preferred reading or source-tradition choice;
- license/source policy;
- owner gates;
- YAML/control-plane authority;
- reviewed-gold, chunk output, graph/retrieval truth, or KG edges.

Rust output must stay no-text unless a later license and storage policy explicitly authorizes text. Rust speed is not authority.

## Hard Stops

- Do not consume raw archives directly; use canonical source views.
- Do not treat Strong's numbers as Greek/Hebrew source text.
- Do not populate local lemma or morphology rows from package-level flags.
- Do not treat OSHB `w@lemma` as local lemma authority; T437 classifies it as Strong lookup-hint metadata.
- Do not open production roots under `data/candidate/original_language_evidence/source_tokens/`, `strong_alignment/`, `lemma_morphology/`, `textual_variants/`, `witness_support/`, or `editorial_layers/`.
- Do not assert translation faithfulness or theology authority.

## DAD Lesson Candidate

If T438 or follow-on work discovers a reusable pattern, report it to DAD. The main reusable rule is: a repo should separate goal selection, parser semantics, and Rust acceleration into separate gates. Rust should scale already-proven semantics, not discover authority meaning from key names.
