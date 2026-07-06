# Genesis — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Narrative (`genre_narrative` in substrate) organized by the **tôlēdôt** ("these are
the generations of…") formula, which is the book's own structural seam: primeval
history (1:1–11:26) then the patriarchal cycles of Abraham, Isaac/Jacob, and Joseph.
Embedded poetry and genealogical lists interrupt the prose at known points.

## Local marker signals (from Rust observation substrate)
- `p` paragraph counts vary widely (e.g. ch18 p=23, ch27 p=30, ch24 p=23), signalling
  internal scene shifts I use to split long chapters (24, 31, 37, 41).
- `has_poetry_or_liturgy_marker` + `q1/q2` runs at 3 (judgment oracles), 4 (Lamech's
  taunt-song), 9 (Noah's oracle), 25, 27 (Isaac/Jacob blessings), 48, and **49**
  (blessing of the twelve tribes: q1=35, q2=43, b=11 — the densest poetry in the book).
- `has_footnote` on most chapters (textual/translation notes) — evidence only.
- `has_strong_h` (strong_h≈32002) — **Strong's Hebrew tags are evidence only**; I did
  not use them to set any boundary.

## Boundary handling (independent rationale)
- **Scene/episode** is the unit, not the chapter. Many units cross chapter lines
  (1:1–2:3 creation; 7:17–8:5 flood; 27:41–28:9 flight to Laban; 49:29–50:14 burial)
  and several chapters are split at paragraph seams (24, 31, 35, 37, 38, 39, 41).
- **Genealogy/tôlēdôt lists** (5; 10; 11:10–26; 25:12–18; 36) are kept as their own
  units and flagged, because list material is a distinct literary form.
- **Embedded poetry** (3:14–24; 4:17–26; 9:18–29; 27; 48; 49:1–28) is kept intact with
  the surrounding oracle/blessing frame and flagged for stanza review.
- I did **not** split in the middle of a direct-speech oracle, a blessing poem, or a
  genealogical formula.

## Strong's / WJ handling
- Strong's Hebrew: **evidence only**, not consulted for boundaries. `wj`/red-letter:
  not applicable (OT); `wj_or_red_letter_considered=false`.

## Low-confidence & frontier escalation triggers
- Any unit whose span coincides exactly with a received chapter division (Genesis is a
  pilot-fragile book) is marked `medium_low` and surfaced to all three sidecars, so the
  editorial chapter seam is never treated as a silent, high-confidence boundary.
- Embedded poetry, genealogies, and **theological-pressure** passages (6:1–8 "sons of
  God"; 9:18–29 curse of Canaan; 15:6 faith reckoned as righteousness; 22 the Aqedah)
  are flagged. Theological weight is made transparent, never smuggled into the boundary.

## Why this is not silent chapter-only
Of 76 units, the majority are multi-chapter arcs or sub-chapter scene splits; only a
minority coincide with a single chapter, and each of those is explicitly flagged
`medium_low` with a sidecar rationale rather than asserted as a confident boundary.
