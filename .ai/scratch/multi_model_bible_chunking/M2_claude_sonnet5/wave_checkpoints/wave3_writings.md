# Wave 3 Checkpoint — Writings (M2_claude_sonnet5)

**Status:** complete | **Books:** 1Chr, 2Chr, Ezra, Neh, Esth, Job, Ps, Prov, Eccl, Song, Lam (23/66 cumulative)

## Summary

| Book | Chunks | Low-conf rows | Notes |
|---|---:|---:|---|
| 1Chr | 28 | 4 | Genealogy blocks (1-9) + narrative; David's psalm (16) substrate-confirmed = 1Chr.16 parallels Ps.105/96/106. |
| 2Chr | 30 | 3 | Reign-based; Temple dedication liturgical refrains (5:13, 7:3) substrate-confirmed as single verses, not whole poems. |
| Ezra | 9 | 4 | Verified ch.4-7's poetry-risk flag is a `\b` blank-line marker (quoted Aramaic decrees), not verse poetry — corrected before use, not overclaimed. |
| Neh | 13 | 1 | Same `\b`-not-poetry verification applied to ch.7. |
| Esth | 10 | 1 | Chapter-per-scene; no poetry markers; book's non-mention of God noted as evidence only. |
| Job | 30 | 19 | Speech-cycle structure; substrate confirms prose/poetry boundary exactly (ch.1-2 prose, 3-42 poetic). Caught and fixed a missed chapter-fallback application (12 chunks corrected post-validator-error). |
| Ps | 150 | 150 | One chunk per psalm (the correct unit); all 150 forced medium_low (pilot-fragile + universally poetry-flagged); real per-psalm substrate data (superscription/Selah) used instead of recalling genre for all 150 from memory. |
| Prov | 20 | 8 | Discourse chunking (1-9) + text-marked collections (22:17, 24:23, 25:1, 30:1, 31:1). |
| Eccl | 12 | 5 | Substrate-confirmed poetry only at ch.3,9,10,11,12 — used directly rather than assumed uniform. |
| Song | 6 | 6 | Refrain-marked cycles (2:7/3:5/8:4 adjuration refrain); speaker-label flag noted, not resolved to per-line attribution. |
| Lam | 5 | 5 | One chunk per chapter = one acrostic poem each (genuinely correct unit). |
| **Wave 3 total** | **313** | **236** | |
| **Cumulative (Waves 1-3)** | **656** | **339** | |

## Validation run (real commands, this session)

All 11 books passed `validate_whole_bible_chunk_map.py` individually, and:
```
python scripts/validate_t423_literary_quality_protocol.py --model-folder <folder> --book 1Chr --book 2Chr --book Ezra --book Neh --book Esth --book Job --book Ps --book Prov --book Eccl --book Song --book Lam --require-artifacts
T423 literary quality protocol: OK
```
One real defect this wave: Job's initial generation omitted the chapter-fallback auto-correction
logic used elsewhere, so 12 chunks needed retroactive confidence downgrade + sidecar rows after
the validator caught it. Fixed and re-validated clean.

## Owner gate status

`pilot_gate.status` remains `pending`; override remains in effect and logged (Wave 1 checkpoint).

## Non-authorizations restated

All 313 new chunks and sidecar rows carry `non_authorizing: true`; `promotion_authority: none`.
Notably: Ps.78 and Ps.89 are kept as single parent-level chunks with no reference to, or
replication of, any existing governed reviewed-gold child-span decisions elsewhere in this repo.

## Next

Wave 4 (Major Prophets): Isa, Jer, Ezek, Dan. Dan requires `frontier_flag_considered: true` on
every chunk per the fork policy's frontier-books rule.
