# T436 Jonah Hebrew Observation Parity Pilot

Status: implementation.
Trust zone: candidate evidence only.

T436 is the Hebrew counterpart to the T435 Rust observation scanner, but it stays in Python first. It proves how the repo should handle a clean Hebrew source-token source view beside a metadata-rich Hebrew source view before any Rust scanner expands into Hebrew.

## Span

- Full book: Jonah
- Canonical refs expected: 48 verses
- Narrow parity spotlight: `Jonah.1.1`, `Jonah.1.2`, `Jonah.1.3`

## Source Views

- Primary baseline: `tanach_us_uxlc`
  - Clean UXLC Jonah XML from the T431 canonical source view.
  - No source-provided Strong's, morphology, or lemma values.
- Metadata context: `openscriptures_oshb`
  - OSHB Jonah XML from the T431 canonical source view.
  - Provides source morphology attributes and lemma-like attributes.
  - The OSHB `lemma` attribute is policy-covered as Strong lookup-hint metadata while local lemma population remains false.
  - T436 records only counts and hashes for OSHB metadata attributes, not morphology or lemma values.

Future agents should not read the raw archives directly for this pilot. Consume the canonical source views and their included-file ledgers.

## Outputs

All outputs stay under:

```text
data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/
```

Files:

- `manifest.yaml`
- `source_view_file_observations.jsonl`
- `verse_token_observations.jsonl`
- `token_shape_index.jsonl`
- `editorial_metadata_shape_index.jsonl`
- `parity_summary.json`

## Authority Limits

T436 does not authorize:

- source-language truth;
- lexical truth;
- Strong's as source text;
- source text storage in the T436 ledgers;
- lemma or morphology value storage;
- lemma or morphology population outside the pilot;
- preferred readings;
- source-tradition choice;
- textual-critical decisions;
- manuscript witness support;
- translation-faithfulness judgments;
- chunk boundaries, reviewed gold, or chunk output;
- route/evaluator behavior;
- KG, retrieval, embedding, or vector truth;
- theology authority.

## Rust Policy

No Rust is added in T436. This is deliberate.

The Rust-fit slice comes next: deterministic UXLC/OSHB scanning, counting, hashing, and no-text ledger emission after the no-text Hebrew semantics are reviewed. T436 prevents a fast Rust scanner from scaling the wrong Hebrew assumptions.

Rust expansion remains blocked after the OSHB lemma-attribute policy cover until the scanner has source-specific UXLC and OSHB parser expectations rather than SBLGNT assumptions.

## Why This Pilot Matters

Hebrew sources differ from the SBLGNT Philemon path:

- UXLC stores vocalized/accented Hebrew source words without morphology or Strong's IDs.
- OSHB provides morphology and lemma-like attributes but still does not authorize Strong's or lexical truth.
- Hebrew punctuation, maqqef, sof-pasuq, vowel points, accents, and verse/chapter divisions are editorial/source-edition layers unless a later witness policy says otherwise.

T436 makes those distinctions machine-checked before the repo adds a high-volume Hebrew scanner.
