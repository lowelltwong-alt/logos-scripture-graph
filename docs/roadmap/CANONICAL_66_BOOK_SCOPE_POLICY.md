# Canonical 66-Book Scope Policy

## Status

- Status: owner decision recorded for implementation planning
- Applies to: `logos-scripture-graph`
- Recorded by: T327A forensic canonical corpus scope audit
- Implementation status: not implemented in T327A

## Policy

`logos-scripture-graph` canonical Scripture and chunking corpus is scoped to the
66-book canon by owner decision.

Deuterocanonical, apocrypha, boundary, front-matter, glossary, and other
non-Scripture editorial material must not enter canonical passages, canonical
translation witnesses, chunk outputs, scorecards, reviewed gold, stress-atlas
controls, or review queues by default.

Front matter and glossary material are source/editorial artifacts. They are not
Scripture content for canonical chunking.

Any future use of excluded material belongs in `logos-boundary-literature` or
another explicitly scoped boundary/tradition repository, after separate
license/source review and human authorization.

`logos-boundary-literature` may interoperate with this repository, but it is
hierarchically under, or at minimum never above, canonical Scripture authority.
Boundary literature may provide background, comparison, reception history,
refutation targets, commentary/reception claims, and tradition-scoped claims. It
must not override, contaminate, or become equal authority to canonical Scripture.

For cross-repo policy or authority conflicts, route to
`logos-governance-architecture`.

Raw source artifact provenance must be handled carefully. Do not hand-edit raw
archives. If a raw source archive contains excluded material, correct it through
a reviewed source replacement, ingest filter, or migration plan.

Rule phrase: do not hand-edit raw archives.

## Allowed Canonical Books

Allowed books are the standard 66-book Protestant canon:

- Genesis
- Exodus
- Leviticus
- Numbers
- Deuteronomy
- Joshua
- Judges
- Ruth
- 1 Samuel
- 2 Samuel
- 1 Kings
- 2 Kings
- 1 Chronicles
- 2 Chronicles
- Ezra
- Nehemiah
- Esther
- Job
- Psalms
- Proverbs
- Ecclesiastes
- Song of Songs
- Isaiah
- Jeremiah
- Lamentations
- Ezekiel
- Daniel
- Hosea
- Joel
- Amos
- Obadiah
- Jonah
- Micah
- Nahum
- Habakkuk
- Zephaniah
- Haggai
- Zechariah
- Malachi
- Matthew
- Mark
- Luke
- John
- Acts
- Romans
- 1 Corinthians
- 2 Corinthians
- Galatians
- Ephesians
- Philippians
- Colossians
- 1 Thessalonians
- 2 Thessalonians
- 1 Timothy
- 2 Timothy
- Titus
- Philemon
- Hebrews
- James
- 1 Peter
- 2 Peter
- 1 John
- 2 John
- 3 John
- Jude
- Revelation

## Excluded Classes

### Exclude Front Matter

- `FRT`
- `00-FRTeng-web.usfm`

Reason: front matter is source/editorial matter, not Scripture content for
canonical chunking.

### Exclude Glossary

- `GLO`
- `106-GLOeng-web.usfm`

Reason: glossary entries are source/editorial reference material, not Scripture
content for canonical chunking.

### Exclude Deuterocanonical / Apocrypha / Non-66 Material

- Tobit (`Tob`, `41-TOBeng-web.usfm`)
- Judith (`Jdt`, `42-JDTeng-web.usfm`)
- Additions to Esther (`AddEsth`, `43-ESGeng-web.usfm`)
- Wisdom (`Wis`, `45-WISeng-web.usfm`)
- Sirach (`Sir`, `46-SIReng-web.usfm`)
- Baruch (`Bar`, `47-BAReng-web.usfm`)
- 1 Maccabees (`1Macc`, `52-1MAeng-web.usfm`)
- 2 Maccabees (`2Macc`, `53-2MAeng-web.usfm`)
- 1 Esdras (`1Esd`, `54-1ESeng-web.usfm`)
- Prayer of Manasses (`PrMan`, `55-MANeng-web.usfm`)
- Psalm 151 (`Ps151`, `56-PS2eng-web.usfm`)
- 3 Maccabees (`3Macc`, `57-3MAeng-web.usfm`)
- 2 Esdras (`2Esd`, `58-2ESeng-web.usfm`)
- 4 Maccabees (`4Macc`, `59-4MAeng-web.usfm`)
- Additions to Daniel (`AddDan`, `66-DAGeng-web.usfm`)

Reason: these are outside the owner-approved 66-book canonical
Scripture/chunking scope for this repository.

## Non-Implementation Boundary

T327A records policy and audit findings only. It does not implement removal,
filtering, data regeneration, source replacement, chunk regeneration,
scorecard regeneration, evaluator changes, or boundary-repo import.

## Future Implementation Boundary

Future implementation must be isolated:

- one task for the allow-list / ingest filter;
- one task for canonical regeneration;
- one task for chunk and leaderboard re-baselining;
- one task for gold/stress/index cleanup;
- one task for boundary-repo source intake planning if excluded material will be
  used later.

Any score movement after filtering is corpus-scope correction, not chunking
improvement.

## T327B Implementation Note

T327B adds the canonical 66-book allow-list and ingest/build filter mechanism only. Existing
generated outputs may still contain non-66 records until T327C regeneration. T327D handles
chunks, scorecards, leaderboard, and score language. T327E cleans gold/stress/review packet
surfaces.

## T327B.1 Validator Fail-Closed Note

Canonical Scripture output validation must fail closed when a record cannot be classified to a
book. A record in canonical Scripture outputs or canonical Scripture sidecars must expose a valid
66-book identity through `book`, `osis_book`, `usfm_book`, `osis_ref`, or `passage_id`.

Glossary, front-matter, concordance, and source metadata may be preserved only as explicitly scoped
non-scripture supporting/reference artifacts outside canonical Scripture outputs. They must not be
canonical passages, canonical chunks, canonical witness text, leaderboard inputs, scorecard inputs,
or default Scripture retrieval text.

This validator does not prove that text labeled with an allowed book identity is authentic source
content for that book. A fake or altered record labeled `Mark`, for example, is handled by raw source
manifest checksums, provenance, parser determinism, and raw immutability controls, not by the
canonical 66-book scope filter alone.
