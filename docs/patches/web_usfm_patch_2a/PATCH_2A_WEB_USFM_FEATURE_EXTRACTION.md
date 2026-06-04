# Patch 2A — WEB USFM embedded feature extraction

This patch is based on the actual uploaded `eng-web_usfm.zip`, not assumptions.

## Actual archive facts

- SHA256: `a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e`
- USFM files: 83
- Content book files excluding FRT/GLO: 81
- Verse markers: 38,058
- Word-level Strong-tagged tokens: 677,688
- Footnotes: 1,855
- Cross-reference spans: 363
- Marker types observed: 58

## Patch purpose

The importer must separate:

1. clean readable translation text,
2. lexical/Strong’s sidecars,
3. footnote/textual-note sidecars,
4. editorial cross-reference sidecars,
5. boundary/formatting marker sidecars,
6. glossary entries,
7. unsupported marker inventory.

## Required new object types

- TranslationWitness
- WordToken or LexemeAlignment
- Footnote
- EditorialCrossReference
- SectionHeading
- BoundaryClaim
- GlossaryEntry
- USFMEvent / UnsupportedUSFMMarker

## Explicit non-goals

- No embeddings.
- No final chunking implementation.
- No Greek/Hebrew source alignment yet.
- No promotion of editorial crossrefs to theological/intertextual claims.
- No inferred doctrine/canon claims.

## Acceptance tests

- Clean text contains no raw USFM markers.
- WordToken count equals observed `\w` + `\+w` count for processed corpus, unless documented exclusions are explicit.
- Footnote count equals observed `\f` count.
- EditorialCrossReference count equals observed `\x` count.
- Parser report lists every marker type and unsupported marker sample.
- Every sidecar carries source_id, source_archive, source_sha256, source_format, license, and status.

See also:

- `WEB_USFM_ACTUAL_ENCODING_INVENTORY.md`
- `web_usfm_inventory.json`
- `CODEX_PROMPT_PATCH_2A_WEB_USFM_FEATURE_EXTRACTION.txt`
