# M3 Claude Frontier — Model Quality Summary

**Model:** `M3_claude_frontier` (Claude Opus 4.8, high effort) · **Strategy:** `literary_marker_aware_v2`
**Status:** in progress (marathon). Scratch, non-authorizing. Do not treat as canon, gold, or graph truth.

## Method
1. Read the Rust observation substrate (`build/observation_substrate/current/`) per book —
   chapter verse-counts, `marker_counts` (paragraph `p`, poetry `q1/q2/d/b`, discourse `s/m`),
   and `risk_flags`. Raw USFM was **not** read (substrate-first; no logged span exceptions needed so far).
2. For each book, wrote `book_strategy/<Book>.md` naming the literature type, marker signals,
   Strong's-as-evidence-only handling, WJ handling, and low-confidence/frontier triggers **before** chunking.
3. Authored boundaries independently at **literary-form granularity** — narrative scene/arc,
   legal/ritual code-unit, poetic stanza/whole-poem, genealogy/list, oracle/vision, and (for the NT)
   epistle greeting/thanksgiving/body/closing and Gospel pericope/discourse units — never a silent
   one-chunk-per-chapter map.
4. A serialization helper enforced schema, verse-range validity against the substrate, strict
   ordering/non-overlap, and derived the three sidecar rows for every flagged chunk. **I authored
   every boundary; the helper decides nothing.**

## Evidence-only discipline
- **Strong's Greek/Hebrew** tags, footnotes, cross-references, paragraph/poetry markers, WJ/red-letter,
  headings, and chapter divisions are treated as **evidence only**, never as boundary or theology authority.
- Where a boundary touches **theological pressure** (typology, messianic readings, textual variants,
  speaker attribution, source tradition), the chunk is marked low/`medium_low` and the pressure is made
  transparent in the frontier/atlas sidecars — never encoded into the boundary itself.

## Progress log — MARATHON COMPLETE (66/66)
- **Wave 1 Torah:** Gen 76, Exod 43, Lev 26, Num 34, Deut 32.
- **Wave 2 History:** Josh 20, Judg 20, Ruth 5, 1Sam 30, 2Sam 26, 1Kgs 21, 2Kgs 25.
- **Wave 3 Writings:** 1Chr 22, 2Chr 24, Ezra 9, Neh 13, Esth 10, Job 30, **Ps 171** (whole-psalm units +
  Ps 119 as 22 acrostic stanzas), Prov 33, Eccl 13, Song 13, Lam 5.
- **Wave 4 Major Prophets:** Isa 60, Jer 37, Ezek 32, **Dan 12** (frontier).
- **Wave 5 Minor Prophets:** Hos 10, Joel 4, Amos 8, Obad 3, Jonah 4, Mic 7, Nah 3, Hab 3, Zeph 3, Hag 4,
  Zech 16, Mal 7.
- **Wave 6 Gospels + Acts:** Matt 38, Mark 23, Luke 31, John 23, Acts 33.
- **Wave 7 Epistles + Revelation:** Rom 19, 1Cor 20, 2Cor 12, Gal 6, Eph 11, Phil 6, Col 6, 1Thess 6,
  2Thess 3, 1Tim 6, 2Tim 4, Titus 3, Phlm 4, Heb 13, Jas 8, 1Pet 7, 2Pet 3, 1John 8, 2John 3, 3John 3,
  Jude 3, **Rev 26** (frontier).

**Totals:** 1242 chunks · 512 flagged (all with rows in all three sidecars) · confidence high 336 /
medium 394 / medium_low 509 / low 3. The 3 low-confidence calls: Mark 16:9–20, John 7:53–8:11, Rev 20.
Merged to `whole_bible_chunk_map.jsonl`; full-bible + literary-quality validators pass for all 66 books.
