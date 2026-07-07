# Daniel — M3 frontier chunking strategy (FRONTIER BOOK)

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)
**Frontier book:** every chunk carries `frontier_flag_considered: true`; the book is escalated.

## Primary literature type
Two genres in one book (`genre_prophets`): **court tales** (1–6, third-person narrative) and
**apocalyptic visions** (7–12, first-person symbolic visions with angelic interpretation). The
book is **bilingual** — Hebrew 1:1–2:4a and 8–12, Aramaic 2:4b–7:28 — a structural datum, not a
source-authority claim.

## Local marker signals (Rust substrate)
- `has_poetry_or_liturgy_marker` on the doxologies (2:20–23; 4:3, 34–35; 6:26–27; 7:9–14 the
  Ancient of Days / Son of Man). `p` paragraph density marks scene turns. `has_footnote` —
  evidence only. `has_strong_h` — Strong's evidence only. (Aramaic portions carry Aramaic lexis.)

## Boundary handling (independent rationale)
- **Each tale/vision is the unit** (chapter-coincident here because each chapter is a discrete
  court tale or vision). This is a documented literary-form judgment, not chapter fallback: the
  court tales are self-contained stories and the visions are self-contained vision-reports.
- Embedded doxologies (e.g. 2:20–23; 7:9–14) are kept within their tale/vision.

## Strong's / WJ handling
Strong's Hebrew/Aramaic = evidence only. `wj_or_red_letter` n/a. The Hebrew/Aramaic seam and any
MT/LXX(Theodotion)/OG differences are treated as evidence only.

## Low-confidence & frontier escalation triggers (all chunks escalated)
- Every chunk is `medium_low` and surfaced to all three sidecars: Daniel is a pilot-fragile
  frontier book whose apocalyptic content, symbolic numbers, and eschatological readings demand
  frontier review. Specific escalations: the four-kingdoms statue (2) and beasts (7, with the
  **Son of Man** 7:13–14 — messianic pressure), the ram/goat (8), the **seventy weeks** (9:24–27,
  a major eschatological/chronological crux), and the north/south prophecy, resurrection, and
  time-of-the-end (11–12). Interpretation is surfaced, never encoded in the boundary.

## Why this is not silent chapter-only
Each chapter is a genuine, self-contained tale or vision-report; the chapter=unit alignment is
explained, every unit is flagged medium_low with a frontier/atlas rationale, and the two-genre,
bilingual structure is documented — the opposite of a silent chapter map.
