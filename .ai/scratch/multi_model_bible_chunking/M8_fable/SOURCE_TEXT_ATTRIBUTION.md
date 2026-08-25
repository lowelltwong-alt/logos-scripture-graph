# Source Text Attribution and Licensing — M8_fable lane

This lane quotes and, for some books, redistributes two open-licensed source
texts. This notice supplies the attribution those licenses require.

It governs only the source-text material inside
`.ai/scratch/multi_model_bible_chunking/M8_fable/`. It does not change the
repository's root `LICENSE` (MIT, software only) and does not alter
`LICENSE_POLICY.md`.

## Open Scriptures Hebrew Bible (OSHB) — CC BY 4.0

- **Title:** Open Scriptures Hebrew Bible
- **Attribution:** Open Scriptures Hebrew Bible Project; text based on the
  Westminster Leningrad Codex.
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Full license text:** [`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt)
- **License URL:** https://github.com/openscriptures/morphhb/blob/master/LICENSE.md
- **Source:** https://github.com/openscriptures/morphhb
- **Pinned commit:** `3d15126fb1ef74867fc1434be1942e837932691f`
- **Source archive sha256:** `f56c150708b5d74719ecb709c712c31eae9855bca7b111fd82ec91b5d177b4c7`
- **Cited in this lane as:** the `oshb:` reference prefix

### Indication of modification (CC BY 4.0 §3(a)(1)(B))

OSHB material in this lane is **modified**. Modifications made:

- extraction of per-book plain-text and JSON views from the upstream XML
  (`sp_durable/<Book>/<Book>_oshb.txt`, `sp_durable/<Book>/tools/verse_map_oshb.json`,
  `sp_durable/<Book>/author/_oshb_dump.txt`);
- derivation of paragraph-marker, span-feature, and crosswalk files;
- short verbatim quotation of Hebrew spans inside chunk boundary rationales.

These modifications are the research product of this lane. They are not endorsed
by, and carry no approval from, the Open Scriptures Hebrew Bible Project.

## World English Bible (WEB) — Public Domain

- **Title:** World English Bible Classic
- **License:** Public domain
- **Source:** https://ebible.org/find/details.php?id=eng-web
- **Source sha256:** `a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e`
- **Cited in this lane as:** the `web:` reference prefix
- **Trademark notice (from the source manifest):** "World English Bible is a
  trademark of eBible.org. If modified, do not call the result World English
  Bible."

Derived and cleaned WEB views in this lane
(`sp_durable/<Book>/<Book>_web_clean.txt`, `<Book>_web.usfm`, crosswalks) are
modified extracts and are therefore **not** presented as "the World English
Bible."

## No restricted translations

No restricted-license translation is quoted or redistributed anywhere in this
lane. A full scan of the subtree found only the `web:` and `oshb:` source
prefixes. NIV, ESV, NASB, NRSV, NKJV, CSB, HCSB, NLT, LEB, and NET do not
appear.

## Scope of the license

CC BY 4.0 applies to the OSHB-derived source-text material identified above.
It does **not** convert this lane's own research output — chunk boundaries,
rationales, reviews, receipts, and registers — into an authority of any kind.
Those remain candidate-only and non-authorizing, as recorded in
`model_manifest.yaml` and `M8_PUBLIC_TRANSPARENCY_README.md`. The upstream
source manifest likewise records that OSHB
`authorizes_chunk_boundaries: false` and `authorizes_reviewed_gold: false`.
