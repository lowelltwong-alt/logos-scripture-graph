# Book Strategy — Genesis (M2_claude_sonnet5)

- **model_id:** M2_claude_sonnet5
- **strategy_id:** literary_marker_aware_v2
- **book:** Gen
- **pilot_book:** true (Gen is in the T423 pilot set; must not use silent chapter-only fallback)

## Selected strategy

Pericope/section-level narrative chunking, not chapter-only and not per-USFM-paragraph.
Genesis contains 50 chapters, 1,533 verses, and 497 `\p` paragraph markers observed in the
Rust substrate (`book_observations.jsonl`, `Gen` row) — an average of one paragraph break
every ~3 verses. Treating every `\p` as a chunk boundary would produce roughly 450+ trivial
fragments and would violate CD-002 (paragraph markers are editorial evidence, not automatic
boundary authority). Chapter-only chunking (50 chunks) would also be a silent fallback,
which this pilot book must not use per the literary-marker quality protocol.

Instead I used narrative-unit / pericope divisions attested by (a) the Hebrew *toledot*
("these are the generations of...") formula, which is an explicit textual structuring
device recurring at Gen.2.4, 5.1, 6.9, 10.1, 11.10, 11.27, 25.12, 25.19, 36.1, 36.9, 37.2;
(b) scene/character shifts in continuous narrative; (c) genealogy/list form; and
(d) poetic insets identified in the substrate's `q1`/`q2` marker positions, which line up
with the well-attested poetic units at Gen.3.14-19, 4.23-24, 9.25-27, 25.23, 27.27-29,
27.39-40, 48.15-16, and 49.1-27.

## Literature type / mixed genre

Primarily narrative, with embedded: genealogical lists (ch. 5, 10, 11.10-32, 25.12-18,
36), a creation liturgy-adjacent account (1.1-2.3), and several short-to-extended poetic
oracles/blessings (see above). `literature_type_guess` is set per chunk to `narrative`,
`genealogy_list`, or `narrative_with_poetic_inset` accordingly.

## Substrate markers considered

- Paragraph-start verse list extracted from `verse_observations.jsonl` (453 verses with
  `marker_counts.p > 0`) — used as corroborating evidence for scene breaks where it
  coincides with the chosen boundary, but not treated as authority by itself.
- Poetry marker verse list (`q1`/`q2`/`q3` present) — 46 verses, matching the known poetic
  units listed above; used to flag `narrative_with_poetic_inset` and to raise confidence
  scrutiny at those spans.
- Book-level `feature_flags`: `genre_narrative`, `has_footnote`, `has_heading_marker`,
  `has_poetry_or_liturgy_marker`, `has_strong_h` (Strong's Hebrew tags: 32,002 in Genesis;
  used only as evidence that lexical apparatus exists, never as boundary or theology
  authority — e.g., at *toledot* seams the Hebrew formulaic wording is cited as textual
  evidence of a structuring device, not as a lexical-truth claim).
- `has_footnote` true in 46/50 chapters — WEB alternate-reading footnotes exist throughout;
  none were used as boundary authority; noted for awareness only.

## Strong's metadata — considered evidence only

Genesis carries 32,002 Hebrew Strong's tags and zero Greek tags per the substrate. I cite
Strong's/Hebrew evidence (`strong_or_hebrew_tags_used: true`) only at the *toledot* seams,
where the recurring formulaic Hebrew phrase is itself the structural evidence. I did not
use Strong's numbers to resolve lexical meaning, doctrine, or any interpretive dispute.

## Chapter-only fallback

Not used. Every chunk boundary is justified by a toledot seam, genealogy-list form, scene
shift, or poetic-inset boundary rather than a bare chapter break. Some units do coincide
with chapter boundaries where the toledot/scene shift happens to fall there (e.g., Gen.1.1-
2.3 vs. Gen.2.4-2.25 both occur near the ch.1/ch.2 seam) — this is coincidental convergence
of narrative and chapter structure, not a chapter-only default.

## Expected low-confidence / doctrinally sensitive regions

The following spans carry historically significant cross-tradition doctrinal or ethical
freight. The chunk *boundary* itself is not generally disputed in scholarship, but the
theological weight of the content is high enough that I flag these at `medium_low`
confidence and log low-confidence / frontier-escalation / atlas-candidate rows so a human
or frontier reviewer can independently assess whether any downstream review packet built
from this scratch map risks smuggling a doctrinal position through boundary or literature-
type labeling:

- **Gen.1.1-2.3** — creation-days interpretation (young-earth / old-earth / framework /
  literary-day views) is a live intramural debate; chunk boundary itself is standard.
- **Gen.2.4-2.25** — relationship between the two creation accounts (documented as a
  historic source-critical debate); noted as evidence, not adjudicated.
- **Gen.3.1-3.24** — Gen.3.15 ("he will bruise your head") carries a major historic
  Christian typological/messianic reading (the "protoevangelium"); flagged, not asserted.
- **Gen.9.18-9.29** — the oracle on Canaan (9.25-27) has a well-documented history of
  being misused for racialized/ethnic-supremacist readings; I have kept the chunk framing
  strictly structural (poetic tricolon embedded in a post-flood family narrative) and do
  **not** adopt, repeat, or imply any such reading.
- **Gen.14.1-14.24** — Melchizedek's later typological significance (Ps.110, Heb.7) is
  intertextual evidence only; not resolved here.
- **Gen.15.1-15.21 / Gen.17.1-17.27** — Abrahamic covenant ceremonies carry significant
  covenant-theology freight (covenant continuity/discontinuity debates); boundary is
  uncontroversial, content weight flagged.
- **Gen.19.1-19.29** — Sodom and Gomorrah narrative carries live contemporary ethical/
  interpretive controversy; framed purely as narrative-unit boundary, no ethical or
  doctrinal verdict rendered.
- **Gen.22.1-22.19** — the Akedah carries very high cross-tradition doctrinal/typological
  weight (Christological typology in some traditions, Aqedah theology in Judaism).
- **Gen.25.19-25.34** — Gen.25.23 ("the older shall serve the younger") is the textual
  basis for Rom.9's election argument; flagged for awareness of downstream doctrinal use.
- **Gen.27.1-27.40** — poetic blessings (27.27-29, 27.39-40) carry the same downstream
  election/inheritance theology pressure as Gen.25.23.
- **Gen.38.1-38.30** — Judah and Tamar; sexual content and levirate-marriage custom;
  Tamar's inclusion in the Matt.1 genealogy is intertextual evidence only.
- **Gen.48.1-48.22 / Gen.49.1-49.28** — Jacob's blessing of the twelve sons is the single
  highest doctrinal-pressure unit in Genesis: Gen.49.10 ("Shiloh"/scepter from Judah) has
  a long history of divergent messianic readings across and within traditions. This is
  escalated to the frontier queue even though Genesis is not on the auto-frontier book
  list (only Dan/Rev are), because the trigger signals (poetry + theology_pressure +
  intertext) clearly apply.

## Frontier / atlas candidate expectations

I expect roughly 8-10 frontier-escalation rows and a similar number of atlas-candidate
rows for Genesis, concentrated at the spans listed above. These are non-authorizing
observations only (`promotion_authority: none`, `atlas_promotion_authority: none`,
`proposed_atlas_action: consider_only`); they do not resolve any doctrinal question and do
not imply that the T423 fork or M2 has decided a theological position.

## Non-authorizations restated

This chunk map is a scratch suggestion only. It does not create reviewed gold, canon
output, child-span authority, route/evaluator behavior, graph/retrieval/vector truth,
atlas promotions, or theology authority.
