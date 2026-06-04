# WEB Classic USFM actual encoding inventory

## Confirmed from uploaded archive

- Archive: `/mnt/data/eng-web_usfm.zip`
- SHA256: `a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e`
- Size: 3,249,612 bytes
- Entries: 87 files
- USFM files: 83
- Non-USFM support files: copr.htm, keys.asc, signature.txt.asc, gentiumplus.css
- Scripture/content book files excluding FRT/GLO: 81
- Verse markers: 38,058

## Book scope

This archive is the full ecumenical WEB Classic set: Protestant OT/NT plus Tobit, Judith, Greek Esther, Wisdom, Sirach, Baruch, 1–2 Maccabees, 1 Esdras, Prayer of Manasses, Psalm 151, 3 Maccabees, 2 Esdras, 4 Maccabees, and Greek Daniel portions, plus FRT preface and GLO glossary.

## Marker inventory

| Marker | Count | Primary capture use |
|---|---:|---|
| `w` | 639,570 | word-level Strong-tagged token |
| `w*` | 639,570 | capture as unsupported/USFMEvent until classified |
| `+w` | 38,118 | nested word-level Strong-tagged token |
| `+w*` | 38,118 | capture as unsupported/USFMEvent until classified |
| `v` | 38,058 | verse marker |
| `q2` | 13,237 | poetry line level 2 |
| `q1` | 10,094 | poetry line level 1 |
| `p` | 9,254 | paragraph boundary |
| `wj` | 2,290 | words-of-Jesus character span |
| `wj*` | 2,290 | capture as unsupported/USFMEvent until classified |
| `f` | 1,855 | footnote start |
| `fr` | 1,855 | footnote reference |
| `f*` | 1,855 | capture as unsupported/USFMEvent until classified |
| `ft` | 1,785 | footnote text |
| `c` | 1,402 | chapter marker |
| `b` | 1,070 | blank/stanza break |
| `fqa` | 519 | alternate reading quotation/addition |
| `x` | 363 | cross-reference start |
| `xo` | 363 | cross-reference origin |
| `xt` | 363 | cross-reference target text |
| `x*` | 363 | capture as unsupported/USFMEvent until classified |
| `d` | 139 | descriptive title/superscription, mostly Psalms |
| `ili` | 98 | intro/glossary list item |
| `k` | 94 | keyword/glossary term |
| `k*` | 94 | capture as unsupported/USFMEvent until classified |
| `mt1` | 84 | major title |
| `id` | 83 | book identity |
| `h` | 83 | running/display heading |
| `toc1` | 83 | long table-of-contents title |
| `toc2` | 83 | short title |
| `toc3` | 83 | abbrev title |
| `m` | 83 | flush paragraph/continuation paragraph |
| `+wh` | 80 | capture as unsupported/USFMEvent until classified |
| `+wh*` | 80 | capture as unsupported/USFMEvent until classified |
| `qs` | 74 | poetic selah/selection marker |
| `qs*` | 74 | capture as unsupported/USFMEvent until classified |
| `li1` | 72 | list item |
| `ide` | 67 | encoding metadata |
| `pi1` | 64 | indented paragraph |
| `mt2` | 41 | major title secondary |
| `ip` | 37 | intro paragraph |
| `bk` | 36 | book title character style |
| `bk*` | 36 | capture as unsupported/USFMEvent until classified |
| `sp` | 33 | speaker label, Song of Songs |
| `fl` | 33 | footnote label |
| `+bk` | 11 | nested book title |
| `+bk*` | 11 | capture as unsupported/USFMEvent until classified |
| `is1` | 9 | intro section heading |
| `mt3` | 7 | major title tertiary |
| `mi` | 7 | indented flush paragraph |
| `q3` | 7 | poetry line level 3 |
| `nb` | 6 | no-break marker |
| `fq` | 6 | footnote quoted text |
| `ms1` | 5 | major section heading, Psalms books |
| `s1` | 5 | section heading |
| `cl` | 1 | chapter label |
| `pc` | 1 | centered paragraph |
| `cp` | 1 | published chapter number |

## Word-level Strong’s/concordance payload

- Total word-level tags: 677,688
- Direct `\w`: 639,570
- Nested `\+w`: 38,118
- Attribute keys observed: strong
- Strong values total: 677,688
- Unique Strong IDs: 10,477
- Hebrew-tagged occurrences: 514,990; unique Hebrew Strong IDs: 6,542
- Greek-tagged occurrences: 162,698; unique Greek Strong IDs: 3,935

Important: Strong tags are present in the 39-book OT and 27-book NT, but not in the Deuterocanonical/Apocrypha/Greek-addition book files. Preserve them as `WordToken` / `LexemeAlignment` sidecars; do not leave the raw `\w...\w*` markup inside clean translation text.

## Footnotes

- Footnote spans: 1,855
- Footnote submarkers: `fr`=1,855, `ft`=1,785, `fqa`=519, `+wh`=80, `+wh*`=80, `fl`=33, `+bk`=11, `+bk*`=11, `fq`=6

Footnotes include translator notes, textual variants, LXX/Hebrew notes, name/measure explanations, alternate readings (`\fqa`, `\fq`), labels (`\fl`), Hebrew word spans (`\+wh`), and nested book-title styling (`\+bk`). They should become `Footnote` / `TextualNote` records, not inline retrieval text.

## Cross-references

- Cross-reference spans: 363
- Books with most crossrefs: ROM:59, MAT:55, HEB:49, JHN:33, ACT:27, LUK:25, MRK:24, 1ES:19, 1CO:18, 2CO:10, GAL:10, 1PE:10

Crossrefs use `\x + \xo <origin> \xt <target-text> \x*`. Treat these as `EditorialCrossReference` records. Do not promote them directly to `quotesFrom`, `alludesTo`, or `fulfills` without review.

## Structural / chunking payload

- Paragraph markers `\p`: 9,254
- Poetry lines `\q1`/`\q2`/`\q3`: 10,094/13,237/7
- Stanza/blank breaks `\b`: 1,070
- Psalm superscriptions `\d`: 139
- Selah/poetic tags `\qs`: 74
- Speaker labels `\sp`: 33
- Words-of-Jesus spans `\wj`: 2,290

These markers should drive `BoundaryClaim` records and later chunking policy. They are edition/translation formatting evidence, not original-language boundaries.

## Capture decision

The importer must produce clean text plus sidecars, not one flattened text stream. Minimum outputs: `TranslationWitness`, `WordToken`, `Footnote`, `EditorialCrossReference`, `SectionHeading`, `BoundaryClaim`, `GlossaryEntry`, and `UnsupportedUSFMMarker`/`USFMEvent`.
