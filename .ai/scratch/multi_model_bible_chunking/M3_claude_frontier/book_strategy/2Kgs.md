# 2 Kings — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Narrative (`genre_narrative`): the Elisha cycle (1–13), the parallel decline of Israel and
Judah (14–17, ending in Samaria's fall), and Judah to the exile (18–25). Substrate adds
`has_crossref` (synchronistic cross-references) — evidence only. No poetry markers.

## Local marker signals (Rust substrate)
- High `p` density on the Elisha miracle scenes (ch4 p=38, ch9 p=30). `has_footnote` and
  `has_crossref` — evidence only. `has_strong_h` — Strong's **evidence only**.

## Boundary handling (independent rationale)
- **Elisha cycle** chunked by miracle/episode (ascension 2; Moab 3; miracles 4; Naaman 5;
  siege 6–7). Jehu's revolt (9–10) by scene.
- **Regnal narrative** by reign/episode; the fall of Samaria (17) kept whole for its
  theological summary; Hezekiah–Sennacherib (18–19) and Josiah's reform (22–23) as arcs of
  scenes; the fall of Jerusalem (24–25) as the closing units.

## Strong's / WJ handling
Strong's Hebrew = evidence only. Cross-references = evidence only. `wj_or_red_letter` n/a.

## Low-confidence & frontier escalation triggers
- ch17 (the Deuteronomistic explanation of the exile of Israel) flagged as a theological
  crux — surfaced for review, not encoded in the boundary. No poetry flags (none present).

## Why this is not silent chapter-only
Miracle/episode and reign units drive boundaries; several are arcs. Evidence/strategy cite
the substrate paragraph and cross-reference markers.
