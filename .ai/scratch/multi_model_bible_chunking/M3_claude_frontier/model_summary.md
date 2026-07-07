# M3 Claude Frontier — Whole-Bible Marathon Summary

**Model:** `M3_claude_frontier` (Claude Opus 4.8, high effort) · **Strategy:** `literary_marker_aware_v2`
**Status:** `complete` — all 66 books · **Scratch, non-authorizing.** Not canon, gold, graph, retrieval,
or theology authority. Merge is offline; compare was **not** run (owner-only, batch, after all models finish).

## Totals
- **1242 chunks** across all 66 canonical books, merged to `whole_bible_chunk_map.jsonl`.
- Confidence mix: **high 336 · medium 394 · medium_low 509 · low 3**.
- **512 flagged** chunks (medium_low/low), each with a matching row in all three sidecars
  (`low_confidence_register.jsonl`, `frontier_escalation_queue.jsonl`, `atlas_candidate_feed.jsonl`).
- `wj_or_red_letter_considered: true` on **128** chunks (Gospels/Acts/Rev, evidence-only).
- `frontier_flag_considered: true` on **38** chunks (all of Dan + Rev, the two frontier books).
- The **3 low-confidence** chunks are my highest-uncertainty calls: **Mark 16:9–20** (longer ending),
  **John 7:53–8:11** (pericope adulterae), and **Rev 20** (the millennium crux).

## Method (frontier discipline)
- **Substrate-first.** Every boundary was informed by the Rust observation substrate
  (`build/observation_substrate/current/`, pinned in the manifest): per-chapter verse counts,
  `marker_counts` (paragraph `p`, poetry `q1/q2/d/b/qs`, discourse `s/m`, list `li1`, WJ `wj`, speaker `sp`,
  crossref `x`), and `risk_flags`. **No raw USFM was read** — no span exception was needed.
- **Independent literary judgment.** I authored every boundary myself; a serialization helper only
  enforced the schema, checked verse ranges/ordering/non-overlap against the substrate, and derived the
  three sidecar rows for each flagged chunk. It decided no boundaries. I did not read any other model's
  output, the comparison folder, or T417 batch2.
- **Genre-appropriate units, never silent chapter-only:** narrative scene/tôlēdôt (Torah, histories,
  Gospels, Acts); legal/ritual code-units (Lev, Deut, Exod); whole-psalm units + Ps 119 as 22 acrostic
  stanzas; speech/discourse units for the Job dialogue and the Gospel discourses; oracle/vision units for
  the prophets and the two apocalypses; epistolary greeting/thanksgiving/body-argument/paraenesis/closing
  units (with the Greek sentence and rhetorical seams, e.g. the Eph 1:3–14 eulogy, the Christ hymns, the
  love chapter). Many units are multi-chapter arcs or sub-chapter splits.

## Evidence-only discipline (as required)
- **Strong's Greek/Hebrew** tags, footnotes, cross-references, paragraph/poetry markers, headings, chapter
  divisions, superscription author-labels, and **WJ/red-letter** markers were all treated as **evidence
  only** — never as boundary, speaker, or theology authority. Red-letter density never set a boundary; the
  John 3 Jesus/narrator seam is left flagged, not resolved.
- **No theology was smuggled into a boundary.** Where a boundary sat under doctrinal/typological/
  messianic/fulfillment/textual-variant/source-tradition/speaker pressure, the chunk was marked low or
  `medium_low` and the pressure was made transparent in the frontier/atlas sidecars, with the interpretation
  explicitly *surfaced, not decided*. No liberal-critical or anti-supernatural default was assumed; e.g.
  First/Second/Third Isaiah and the 2 Peter/Jude relationship are labelled *evidence only*.

## Frontier priorities covered
- **Textual variants:** Mark 16:9–20, John 7:53–8:11, the Comma Johanneum (1 John 5:7–8), the Rev 13:18
  666/616 variant, Rom 16 doxology placement, and Acts 8:37 / 15 / 2 Thess 2 / 2 Cor 4 variant flags.
- **Apocalyptic/prophetic:** Daniel (frontier book, all 12 escalated), Revelation (frontier book, all 26
  escalated), the Isaiah apocalypse (24–27), Ezekiel's visions, Zechariah's visions/oracles, the Olivet
  discourses, and Gog/Magog.
- **Gospel discourse & WJ boundaries:** the five Matthean discourses, the Sermon on the Plain, the Johannine
  discourses and High-Priestly Prayer, the John 3 speaker crux.
- **Dense epistle argument & doxology:** Romans and Galatians justification units, the Christ hymns
  (Phil 2; Col 1; 1 Tim 3:16), Hebrews' warning passages and Melchizedek/new-covenant/atonement units, the
  Trinitarian benediction (2 Cor 13:14) and Great Commission formula (Matt 28:19).
- **Poetry/acrostic/lament:** whole-psalm units + Ps 119 stanzas, Lamentations' acrostics, Job's strophes,
  the Song of the Sea/Deborah/Moses, and the Lukan canticles.

## Non-authorizations
Scratch chunk map only. No reviewed gold, canon chunks, child-span authority, route/evaluator changes,
graph/retrieval/vector truth, atlas promotion, or theology authority. `non_authorizing: true` on every row;
sidecar `promotion_authority` / `atlas_promotion_authority` = `none`; `proposed_atlas_action` = `consider_only`.
Per repo policy, Revelation remains research/prep-only.

## Artifacts
`book_strategy/<Book>.md` (66) · `book_chunks/<Book>/chunks.jsonl` (66) · `whole_bible_chunk_map.jsonl`
(merged) · the three sidecars (512 rows each) · `layer_decision_log.jsonl` (per-book) · `model_quality_summary.md`.
