# Deuteronomy — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Covenant address / law (`genre_law`) framed as Moses' farewell **speeches**: historical
retrospect (1–4), covenant exhortation (5–11), the Deuteronomic Code (12–26), covenant
ceremony and blessings/curses (27–28), renewal (29–30), and a poetic close — the **Song
of Moses** (32) and the **Blessing of Moses** (33).

## Local marker signals (Rust substrate)
- Poetry (`has_poetry_or_liturgy_marker` + heavy q1/q2) at 32 (q1=59,q2=85) and 33
  (q1=40,q2=56); minor at 31. ch27 p=26 (liturgical curses). `has_strong_h` — evidence only.

## Boundary handling (independent rationale)
- **Speeches/exhortation** chunked by rhetorical unit, several as arcs (2:1–3:29;
  4:44–5:33 covenant+Decalogue; 9:1–10:11; 10:12–11:32).
- **Shema** (6) kept as its own unit given its centrality.
- **Deuteronomic Code** (12–26) by legal topic (worship centralization, idolatry, tithes,
  release, feasts, offices, warfare, social law).
- **Song of Moses** kept as the cross-chapter poetic arc 31:30–32:47 and flagged; the
  **Blessing of Moses** (33) flagged; the Nebo-command (32:48–52) and death (34) as
  narrative units.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- The two poems (Song 31:30–32:47; Blessing 33) are flagged for stanza review. The
  prophet-like-Moses unit (18:15–22) carries messianic-reading pressure, surfaced in the
  sidecars rather than encoded in the boundary.

## Why this is not silent chapter-only
Rhetorical speech-units and legal topics set the boundaries; many are arcs, and the
poetry is isolated. Evidence/strategy cites the substrate poetry and paragraph seams.
