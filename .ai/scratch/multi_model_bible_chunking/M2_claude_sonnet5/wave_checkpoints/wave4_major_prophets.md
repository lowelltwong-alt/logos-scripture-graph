# Wave 4 Checkpoint — Major Prophets (M2_claude_sonnet5)

**Status:** complete | **Books:** Isa, Jer, Ezek, Dan (27/66 cumulative)

## Summary

| Book | Chunks | Low-conf rows | Notes |
|---|---:|---:|---|
| Isa | 54 | 32 | Oracle/section structure; 4 Servant Songs, Immanuel/messianic texts, Cyrus-as-anointed all flagged. |
| Jer | 41 | 17 | Sign-act narratives + oracle cycles + Book of Consolation (New Covenant 31:31-34) flagged. |
| Ezek | 32 | 16 | Vision/oracle-cycle structure; two marriage allegories, Gog/Magog, dry bones, Temple vision flagged. |
| Dan | 12 | 12 | Frontier book: `frontier_flag_considered: true` on every chunk; pilot-fragile forced medium_low on all 12. |
| **Wave 4 total** | **139** | **77** | |
| **Cumulative (Waves 1-4)** | **795** | **416** | |

## Validation run (real commands, this session)

All 4 books passed `validate_whole_bible_chunk_map.py` individually, and:
```
python scripts/validate_t423_literary_quality_protocol.py --model-folder <folder> --book Isa --book Jer --book Ezek --book Dan --require-artifacts
T423 literary quality protocol: OK
```
No validator errors this wave (chapter-fallback logic applied correctly from the start, unlike
the Job miss in Wave 3).

## Owner gate status

`pilot_gate.status` remains `pending`; override remains in effect and logged (Wave 1 checkpoint).
Daniel's `frontier_flag_considered: true` requirement (fork policy `frontier_flag_books`) was
applied correctly and verified by the literary quality protocol validator.

## Non-authorizations restated

All 139 new chunks and sidecar rows carry `non_authorizing: true`; `promotion_authority: none`.
No apocalyptic-identification, messianic-reading, or eschatological-chronology question is
resolved anywhere in this wave — all are flagged for awareness only.

## Next

Wave 5 (Minor Prophets, 12 books): Hos, Joel, Amos, Obad, Jonah, Mic, Nah, Hab, Zeph, Hag, Zech,
Mal. Jonah is a pilot book. This wave has many short books (Obad = 1 chapter, Joel/Nah/Hab/Zeph/
Hag = 2-3 chapters each) alongside longer ones (Hos 14 ch, Zech 14 ch).
