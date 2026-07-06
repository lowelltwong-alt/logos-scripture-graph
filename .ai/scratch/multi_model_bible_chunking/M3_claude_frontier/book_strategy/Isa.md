# Isaiah — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Prophetic poetry and oracle (`genre_prophets`), with a prose historical interlude (36–39).
Macro-structure: Judah/Jerusalem oracles (1–12), oracles against the nations (13–23), the
"Isaiah apocalypse" (24–27), woes and hope (28–35), the Hezekiah narrative (36–39), the book of
comfort and Servant Songs (40–55), and restoration (56–66).

## Local marker signals (Rust substrate)
- `has_poetry_or_liturgy_marker` + dense q1/q2 across most chapters (prose at 7–8; 13–25 mixed;
  36–39). `b` strophe breaks throughout. `has_footnote` — evidence only. `has_strong_h` —
  Strong's Hebrew **evidence only**.

## Boundary handling (independent rationale)
- Chunked by **oracle / poem / vision unit**, following the "burden/massa" headings for the
  nations (13–23), scene shifts in the apocalypse (24–27), and the individual Servant Songs
  (42:1–9; 49:1–6; 50:4–9; 52:13–53:12), which are isolated within their surrounding oracles.
- **Source-critical partitions** (First/Second/Third Isaiah) are treated as scholarly *evidence
  only*, never as boundary authority; the canonical oracle structure sets the seams.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- **Messianic pressure** passages (7:14 Immanuel; 9:1–7; 11:1–10; 61:1–3, cf. Luke 4) and the
  **Servant Songs** flagged — surfaced, interpretation not decided by the boundary.
- The **Day Star / "Lucifer" taunt** (14:12–15) flagged for its interpretive/theological history.
- The **apocalyptic** units (24–27, incl. Leviathan 27:1) and the eschatological close (66:24)
  flagged. Single-chapter poetic oracles are marked `medium_low` and surfaced for strophe review.

## Why this is not silent chapter-only
Boundaries follow oracle/poem/vision seams — many multi-chapter arcs (3:1–4:1; 9:8–10:4;
13:1–14:27; 15:1–16:14; 30:1–31:9; 51:1–52:12; 63:7–64:12) and sub-chapter isolations (4:2–6;
9:1–7; 42:1–17; 52:13–53:12) — never a flat chapter map.
