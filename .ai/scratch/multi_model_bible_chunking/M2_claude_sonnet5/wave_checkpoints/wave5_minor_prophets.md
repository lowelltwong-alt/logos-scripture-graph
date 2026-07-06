# Wave 5 Checkpoint — Minor Prophets (M2_claude_sonnet5)

**Status:** complete | **Books:** Hos, Joel, Amos, Obad, Jonah, Mic, Nah, Hab, Zeph, Hag, Zech, Mal (39/66 cumulative, 59%)

## Summary

| Book | Chunks | Low-conf | Book | Chunks | Low-conf |
|---|---:|---:|---|---:|---:|
| Hos | 14 | 12 | Hab | 3 | 2 |
| Joel | 4 | 3 | Zeph | 3 | 0 |
| Amos | 8 | 6 | Hag | 2 | 1 |
| Obad | 2 | 0 | Zech | 13 | 5 |
| Jonah (pilot) | 4 | 4 | Mal | 4 | 3 |
| Mic | 7 | 7 | | | |
| Nah | 3 | 0 | **Wave 5 total** | **67** | **43** |

**Cumulative (Waves 1-5): 862 chunks, 459 low-confidence/escalation rows.**

## Validation run

All 12 books passed `validate_whole_bible_chunk_map.py` individually, and
`validate_t423_literary_quality_protocol.py --model-folder <folder> --book Hos --book Joel ... --book Mal --require-artifacts` returned OK.

## Notable content flagged (evidence-only, not adjudicated)

Zechariah concentrates the most heavily NT-cited messianic texts among the Minor Prophets
(9:9 triumphal entry, 11:12-13 thirty pieces of silver, 12:10 "the one they have pierced");
Malachi's coming-messenger/Elijah-return oracles (3:1, 4:5-6) later associated with John the
Baptist; Micah's Bethlehem-ruler oracle (5:2); Habakkuk's "righteous shall live by faith" (2:4).
Jonah (pilot book) forced medium_low on all 4 chunks per the pilot-fragile rule, matching its
established 4-act = 4-chapter structure.

## Owner gate status

`pilot_gate.status` remains `pending`; override remains in effect and logged (Wave 1 checkpoint).

## Next

Wave 6 (Gospels + Acts): Matt, Mark, Luke, John, Acts — requires WJ/red-letter marker handling
(evidence only per CD-021/CD-022, never speaker-attribution or boundary authority).
