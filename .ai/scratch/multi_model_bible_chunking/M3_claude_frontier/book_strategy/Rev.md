# Revelation — M3 frontier chunking strategy (FRONTIER + pilot-fragile book)

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)
**Frontier book:** every chunk carries `frontier_flag_considered: true`; the book is escalated.

## Primary literature type
Apocalypse (`genre_apocalypse`) framed as a circular prophecy/letter: a prologue and inaugural
vision (1), seven messages to the churches (2–3), and a series of interlocking heptads and vision
cycles (throne/scroll 4–5; seals 6–8:1; trumpets 8:2–11; the dragon/beasts signs 12–14; bowls
15–16; Babylon's fall 17–18; the parousia and judgment 19–20; the new creation 21–22). Symbolic
numbers, Old Testament allusion (Daniel, Ezekiel, Zechariah, Exodus), and hymns run throughout.

## Local marker signals (Rust substrate)
- `has_wj` in the seven messages (ch2 wj=74; ch3 wj=56) and the framing words of Christ (1; 16;
  21; 22) — **evidence only**. `has_poetry_or_liturgy_marker` on the heavenly **hymns** (5; 7; 15).
  `has_variant_reading` at **ch13** (the number of the beast, 666/616). `has_crossref`/`x` — the
  dense OT allusion, evidence only. `has_strong_g` — Strong's **Greek evidence only**.

## Boundary handling (independent rationale)
- Chunked by **vision cycle / scene / message unit**. The **seven messages** (2:1–3:22) are chunked
  as seven discrete oracles (each with the same "to the angel of… he who has an ear" form). The
  heptads are chunked by cycle, with arcs where a cycle spans chapters (8:1–9:21; 10:1–11:14;
  15:1–16:21). The interludes (7; 10–11) are kept as their own units.
- Symbolic imagery and numbers are treated as **evidence** to be surfaced, never resolved into an
  eschatological system by the boundary.

## Strong's / WJ handling (evidence only)
WJ (Christ's messages and the "I am coming" sayings) and Strong's Greek are **evidence only** —
never used to set a boundary or decide christology/eschatology; the message boundaries follow the
sevenfold epistolary form, not the red letters.

## Low-confidence & frontier escalation triggers (every chunk escalated)
- Every chunk is `medium_low` (Revelation is a pilot-fragile frontier book) and surfaced to all
  three sidecars. Specific escalations: the **Son of Man** vision (1); the throne/Lamb hymns (4–5);
  the **seals/trumpets/bowls** heptads; the **woman, dragon, and the two beasts** with **666**
  (12–13, incl. the 666/616 textual variant); the harvest (14); **Babylon** (17–18); the **rider on
  the white horse** (19); the **millennium and the great white throne** (20 — the amillennial/
  premillennial/postmillennial crux); and the **New Jerusalem** and epilogue (21–22). Interpretation
  is surfaced, never encoded in the boundary. Per repo policy, Revelation remains research/prep-only.

## Why this is not silent chapter-only
Boundaries follow the apocalypse's vision-cycle and message structure — the seven messages are
seven units, the heptads are cycles (several arcs), and the interludes are isolated — with every
unit flagged and escalated. This is the opposite of a silent chapter map.
