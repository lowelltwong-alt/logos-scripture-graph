# Mark — M6_fable5 book strategy (literary_marker_aware_v2)

- **Selected strategy:** pericope chunking on Mark's fast episodic narrative, hinged at the
  Caesarea Philippi confession (8:27) between the Galilee and way-to-Jerusalem halves, with the
  Olivet discourse (13) and passion sequence chunked by scene. The disputed longer ending
  (16:9-20) is isolated as its own variant-flagged unit.
- **Literature type / mixed genre:** Gospel narrative; intercalated ("sandwich") episodes
  (3:20-35; 5:21-43; 11:12-25; 14:1-11; 14:53-72) kept whole because the intercalation is the
  literary point; one apocalyptic discourse (13); parable cluster (4:1-34).
- **WJ/red-letter handling:** wj runs confirm speech extents; per policy they are formatting
  evidence, not speaker-boundary authority; all wj-bearing chunks set
  `wj_or_red_letter_considered: true`.
- **Substrate markers considered:** `p` seams; `wj` runs; `x` crossrefs evidence-only; footnotes
  — **16:8-9,19 footnotes mark the longer-ending variant**, the dossier queue's flagship case.
- **Strong's/Greek metadata:** evidence-only; `strong_or_hebrew_tags_used: false`.
- **Expected low-confidence regions:** 16:9-20 longer ending (textual-variant pressure —
  variant-policy-first per dossier; my chunk isolates it precisely so downstream policy can act);
  intercalation units (models may split the sandwiches); 8:27-9:1 hinge extent; 1:14-45 day-one
  seam placement.
- **Chapter-only fallback:** not used.
- **Frontier/atlas expectations:** rows for the longer ending, Olivet, and sandwich units.
- **Independent boundary rationale:** episode seams follow Mark's kai-euthys scene shifts and
  intercalation frames anchored to substrate paragraphs; no template span or other model folder
  used.
