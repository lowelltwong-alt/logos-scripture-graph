# Wave 6 Checkpoint — Gospels + Acts (M2_claude_sonnet5)

**Status:** complete | **Books:** Matt, Mark, Luke, John, Acts (44/66 cumulative, 67%)

## Summary

| Book | Chunks | Low-conf | Notes |
|---|---:|---:|---|
| Matt | 24 | 18 | Discourse-unit chunking (Sermon on Mount, Mission/Community/Olivet Discourses); WJ markers cited as evidence only per CD-021/CD-022. |
| Mark | 16 | 9 | Narrative-cycle chunking; longer ending (16:9-20) flagged as a major textual-variant question. |
| Luke | 25 | 13 | Canticles (Magnificat/Benedictus/Nunc Dimittis) substrate-confirmed poetic. |
| John | 19 | 9 | Farewell Discourse + High Priestly Prayer (14-17) kept as one unit. John.3 chunk deliberately does NOT reference or resolve the existing T355/T411 owner-review docket for the John.3.10-21 speaker-boundary question — independent parent-level observation only. |
| Acts | 25 | 11 | WJ markers noted at conversion narratives and the otherwise-unrecorded saying at 20:35, evidence only. |
| **Wave 6 total** | **109** | **60** | |

**Cumulative (Waves 1-6): 1,038 chunks, 519 low-confidence/escalation rows.**

## Validation run

All 5 books passed `validate_whole_bible_chunk_map.py` individually, and
`validate_t423_literary_quality_protocol.py --model-folder <folder> --book Matt --book Mark --book Luke --book John --book Acts --require-artifacts` returned OK.

## Important non-authorization note

Every WJ/red-letter marker citation in this wave is evidence-only per CD-021/CD-022 — no chunk
resolves Jesus speaker attribution, speaker boundaries, or discourse boundaries. The woman-caught-
in-adultery pericope (John.7:53-8:11) and Mark's longer ending (16:9-20) are flagged as major
textual-variant questions, not adjudicated. The John.3 chunk is explicitly isolated from the
existing governed owner-review docket for that exact span.

## Owner gate status

`pilot_gate.status` remains `pending`; override remains in effect and logged (Wave 1 checkpoint).

## Next

Wave 7 (final): Epistles + Revelation, 22 books (Rom through Rev). Phlm is a pilot book;
Revelation is a frontier book requiring `frontier_flag_considered: true` on every chunk.
