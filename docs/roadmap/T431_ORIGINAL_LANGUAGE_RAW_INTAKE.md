# T431 Original-Language Raw Intake

T431 starts the T430 original-language evidence substrate by downloading only license-approved Hebrew and Greek source packages into `data/raw/original_language/`.

## What T431 Does

- Downloads allowlisted raw source archives for UXLC, OSHB, SBLGNT, UGNT, and CNTR-SR.
- Writes one `source_manifest.yaml` beside each archive with checksum, license, source URL, version or commit, attribution, and authority limits.
- Records manuscript libraries as catalog-only metadata until bulk transcription/image reuse is explicitly cleared.
- Adds validators that keep raw source files immutable and stop Strong's overlays from being written into raw.
- Records that the oldest witness is evidence, not automatic authority.
- Requires textual variants to be transparent and cited, never silently normalized.
- Builds a canonical-only candidate source view under `data/candidate/original_language_evidence/canonical_source_views/`.
- Future T432+ processing must consume the filtered source view, not the raw archive directly.
- The filtered view keeps inclusion and exclusion ledgers so docs, PDFs, app files, nested archives, images, duplicate renderings, metadata, and non-selected variants cannot cross-contaminate canonical Bible processing.
- Included canonical source view files explicitly flag whether they retain source-provided morphology, lemmas, or Strong's IDs.
- Check mode validates inclusion and exclusion ledgers against the actual archive member set and rejects duplicate source paths, duplicate included books, duplicate view paths, stale checksums, and scope/count drift.

## What T431 Does Not Do

- No source-language witness rows.
- No tokenization or full original-language reconstruction.
- No Strong's overlay output.
- No manuscript image or transcription imports.
- No direct downstream ingestion from raw source archives that may contain docs, code, images, duplicate renderings, metadata, or non-selected source variants.
- No preferred readings, source-tradition choices, canon changes, reviewed gold, chunks, graph edges, retrieval truth, embeddings, indexes, or theology authority.

## Downstream Path

T432 may harden schemas for source tokens, punctuation/editorial layers, variants, and alignment rows. T433 may run a tiny pilot. T435 may add a Rust-first scanner after schemas stabilize. T436/frontier review handles variant-sensitive or doctrinal-pressure passages. T437 may build a translation-faithfulness atlas from transparent candidate evidence.

See `docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md` for five next-goal options: source-language alignment bridge, manuscript witness chain, variant/copying-error ledger, early creed/tradition-formula research lane, and integrated evidence workbench.
