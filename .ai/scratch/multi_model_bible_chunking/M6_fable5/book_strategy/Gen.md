# Gen — M6_fable5 book strategy (literary_marker_aware_v2)

- **Selected strategy:** toledot-frame narrative pericope chunking. Genesis is structured by the
  eleven toledot ("these are the generations") headings (2:4; 5:1; 6:9; 10:1; 11:10; 11:27; 25:12;
  25:19; 36:1; 37:2), with scene/episode boundaries inside each cycle. Chunks follow scene and
  cycle boundaries, not chapters, except where a scene legitimately fills exactly one chapter.
- **Literature type / mixed genre:** narrative dominant; embedded genealogy lists (5; 10; 11:10-26;
  25:12-18; 36), covenant ceremonies (15; 17), and embedded poetry (3:14-19 curses; 4:23-24 Lamech;
  9:25-27 Noah's oracle; 27:27-29,39-40 blessings; 49:2-27 blessing of Jacob, q1x35/q2x43 + b stanza
  breaks in the substrate).
- **Substrate markers considered:** paragraph `p` positions per verse (primary boundary evidence),
  `q1/q2` poetry runs (c3, c4, c9, c25, c27, c48, c49), `b` stanza breaks in c49, `nb` at 49:33,
  footnote `f` positions as variant/translation pressure (evidence only). WEB carries no `s`
  section headings, so paragraph + literary knowledge carry the boundary load.
- **Strong's/Hebrew metadata:** considered strictly evidence-only (`strong_h` tags present on all
  verses); no Strong's number was used as boundary authority; `strong_or_hebrew_tags_used: false`
  on all chunks.
- **WJ/red-letter:** not applicable (no `wj` markers in Gen); divine-speech boundaries are treated
  as narrative-internal speech, not speaker-chunk boundaries.
- **Expected low-confidence regions:** 2:4 toledot hinge (2:4a/2:4b source-boundary debate);
  6:1-8 (sons-of-God unit: attaches to Adam toledot or flood prologue); 26:34-28:9 blessing-deception
  complex (Esau's wives frame); 49:2-27 embedded tribal-blessing poetry (stanza subdivision
  possible); genealogy/list chapters (10; 36) where list seams are internal; all chunks whose span
  coincides with a full chapter (Gen is a pilot-fragile book, so chapter-coincident spans are
  capped at medium_low and fed to the three sidecars even when the literary unit genuinely equals
  the chapter, e.g. Gen 23 burial of Sarah, Gen 24 would otherwise but is subdivided into scenes).
- **Chapter-only fallback:** not used as a strategy. Chapter-coincident spans that remain are
  deliberate literary units, logged with medium_low confidence per protocol, never silent fallback.
- **Frontier/atlas expectations:** escalation rows for the 2:4 hinge, 6:1-8, 49:2-27 poetry, and
  every chapter-coincident unit; no frontier book flags (Gen not in Dan/Rev set), and
  `frontier_flag_considered` left false.
- **Independent boundary rationale:** boundaries were drawn from the toledot skeleton plus
  scene-change evidence (place/time/actor shifts) anchored to substrate paragraph markers; the
  template example span was not used as a boundary recommendation; no other model folder was read.
