# Luke — M6_fable5 book strategy (literary_marker_aware_v2)

- **Selected strategy:** pericope chunking with Luke's architecture honored: preface (1:1-4),
  infancy diptych with embedded canticles (1-2), Galilee ministry (3:1-9:50), the long travel
  narrative opened at the 9:51 Jerusalem-resolve hinge (9:51-19:27), Jerusalem ministry and
  passion (19:28-23:56), resurrection triptych (24).
- **Literature type / mixed genre:** Gospel narrative with historiographic preface; four embedded
  canticles/hymns (Magnificat 1:46-55; Benedictus 1:68-79; Gloria 2:14; Nunc Dimittis 2:29-32 —
  q1/q2 in c1-c3); genealogy (3:23-38); parable-dense travel section; apocalyptic discourse (21).
- **WJ/red-letter handling:** wj runs confirm speech extents, formatting evidence only; wj-bearing
  chunks set `wj_or_red_letter_considered: true`.
- **Substrate markers considered:** `p` seams; `q1/q2` canticles; `wj` runs; `x` crossrefs and
  footnotes evidence-only — **22:43-44 (agony angel/bloody sweat) and 23:34 (Father, forgive) are
  major textual variants** flagged in their chunks.
- **Strong's/Greek metadata:** evidence-only; `strong_or_hebrew_tags_used: false`.
- **Expected low-confidence regions:** canticle isolation vs narrative-frame retention (I keep
  canticles inside their birth pericopes and flag); 9:51 hinge placement; travel-narrative topical
  seams (11-18 have no marked structure — cuts follow audience/topic shifts); the two passion
  variants; 21 Olivet.
- **Chapter-only fallback:** not used.
- **Frontier/atlas expectations:** rows for canticle policy, variant spans, Olivet, and travel
  seams.
- **Independent boundary rationale:** seams follow Lukan scene formulae ("and it happened...")
  and audience shifts anchored to substrate paragraphs; no template span or other model folder
  used.
