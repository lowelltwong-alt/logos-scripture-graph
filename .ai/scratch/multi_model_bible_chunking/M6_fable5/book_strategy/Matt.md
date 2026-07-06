# Matt — M6_fable5 book strategy (literary_marker_aware_v2)

- **Selected strategy:** pericope chunking honoring Matthew's five-discourse architecture
  (Sermon on the Mount 5-7; mission 10; parables 13; community 18; woes+Olivet 23-25), with long
  discourses subdivided at recognized internal turns and narrative sections chunked per pericope.
- **Literature type / mixed genre:** Gospel narrative with embedded discourses, genealogy
  (1:1-17), fulfillment-quotation formulae (x-marked editorial crossrefs at 1:23; 2:6,15,18;
  4:15-16; 8:17; 12:18-21; 13:35; 21:5; 27:9-10), parables, and apocalyptic discourse (24).
- **WJ/red-letter handling:** `wj` markers are dense (5-7; 10; 13; 18; 23-25 nearly continuous).
  Per the WJ marker policy, red-letter runs are translation formatting evidence, **not** speaker
  attribution or discourse-boundary authority; I use them to confirm discourse extents, and every
  chunk containing wj markers sets `wj_or_red_letter_considered: true` (builder detects from
  span signals).
- **Substrate markers considered:** `p` pericope seams; `wj` runs; `x` editorial crossrefs
  (evidence-only, never promoted to intertext truth); `q1/q2` in quoted-Scripture poetry;
  footnotes (variant pressure at 6:13 doxology; 17:21; 18:11; 23:14 traditional-verse issues) —
  evidence-only.
- **Strong's/Greek metadata:** evidence-only; `strong_or_hebrew_tags_used: false`.
- **Expected low-confidence regions:** discourse-edge placement (does 10:1-4 apostle list open
  the mission discourse; 13:53 seam; 23 as separate woe discourse vs Olivet prelude); 16:13-28
  Caesarea confession (Petrine-primacy theology pressure); 24 Olivet (eschatology pressure;
  synoptic parallel Mark 13/Luke 21); 27:9-10 Jeremiah-attribution citation puzzle; 28:19
  baptismal formula (orthodox-pressure passage list).
- **Chapter-only fallback:** not used; pericope seams cut within chapters throughout.
- **Frontier/atlas expectations:** rows for the confession, Olivet, citation-puzzle, and
  commission units plus discourse-edge decisions.
- **Independent boundary rationale:** the five-fold "when Jesus had finished these sayings"
  colophons (7:28; 11:1; 13:53; 19:1; 26:1) anchor the discourse frame; pericope seams follow
  scene/audience shifts confirmed by substrate paragraphs; no template span or other model
  folder used.
