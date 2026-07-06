# Joshua — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Narrative (`genre_narrative`): conquest narrative (1–12) then tribal **allotment lists**
(13–21) and a covenant-renewal close (22–24). No poetry markers in the substrate, but
10:12–13 embeds a poetic quotation from the Book of Jashar.

## Local marker signals (Rust substrate)
- `p` paragraph density marks scenes; ch12 `m`=32 and ch15 `m`=9 mark list/margin
  material (defeated-kings list; boundary descriptions). `has_footnote` on textual notes —
  evidence only. `has_strong_h` — Strong's Hebrew **evidence only**.

## Boundary handling (independent rationale)
- **Conquest narrative** by scene/campaign (Jericho, Achan/Ai, Gibeon, southern & northern
  campaigns), several arcs (3:1–4:24 crossing; 8 Ai+Ebal).
- **Allotment section** chunked by tribal-group unit as list arcs (14:1–15:63 Judah;
  16:1–17:18 Joseph tribes; 18:1–19:51 remaining seven), not one-per-chapter.
- **Covenant close** (23 farewell; 24 Shechem) as speech/ceremony units.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- ch10 flagged `medium_low`: the sun-stands-still episode quotes the poetic Book of Jashar
  (10:12–13) and is a supernatural/textual crux worth review; the citation is treated as
  evidence, not as a source-tradition authority.

## Why this is not silent chapter-only
Boundaries follow campaign-scene and tribal-allotment form; several units are multi-chapter
arcs. Evidence/strategy cite the substrate paragraph and list markers.
