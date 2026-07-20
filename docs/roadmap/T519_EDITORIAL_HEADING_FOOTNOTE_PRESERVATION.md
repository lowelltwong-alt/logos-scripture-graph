# T519 — Editorial Heading Footnote Preservation

## Intent

Owner-authorized narrow repair for the T475 HOLD finding: three WEB Psalm `\d` heading footnotes (Ps.46, Ps.90, Ps.145) must remain typed `footnotes.jsonl` sidecars.

## Repair

`pipelines/ingest/usfm_importer.py` adds `emit_editorial_inline_sidecars`:

- Runs when `body_disposition == editorial_only` and the body is non-empty.
- Emits footnotes and crossrefs only.
- Uses `osis_ref=None` / `passage_id=None` so IDs stay `footnote:eng-web:<file>:<line>:<index>`.
- Does **not** append heading prose to `TranslationWitness.text`.
- Does **not** emit heading-embedded `\w` tokens as `WordToken`s.

## Proof

- Fixture: `test_editorial_heading_footnotes_are_typed_sidecars_without_witness_or_tokens`
- Full-archive verify: footnote count **1130**; exact baseline IDs restored for `46:0`, `90:0`, `145:0`

## Still gated

- Committed canonical/processed regeneration
- T475 formal shadow re-freeze + independent Claude audit
- T476 owner packet and all downstream gold/chunk work

## Decisions / lessons

- CD-124
- LSN-070
