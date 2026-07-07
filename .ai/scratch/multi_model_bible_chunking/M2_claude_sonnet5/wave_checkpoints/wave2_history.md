# Wave 2 Checkpoint — History (M2_claude_sonnet5)

**Status:** complete | **Books:** Josh, Judg, Ruth, 1Sam, 2Sam, 1Kgs, 2Kgs (12/66 cumulative)

## Summary

| Book | Chunks | Low-conf rows | Notes |
|---|---:|---:|---|
| Josh | 21 | 4 | Campaign/scene chunking; herem-conquest chapters (6,8,10,11) flagged. |
| Judg | 14 | 4 | Judge-cycle chunking (cycles span chapters); Song of Deborah (4-5) substrate-confirmed. |
| Ruth | 4 | 0 | Book's own 4 chapters = its 4 acts; no forced downgrade (not pilot-fragile, no poetry markers). |
| 1Sam | 27 | 5 | Hannah's Song (2:1-10) and 3 victory-song quotations (18:7, 21:11, 29:5) substrate-confirmed. |
| 2Sam | 21 | 9 | Highest concentration: Davidic covenant (7), Bathsheba/Uriah (10-12), 3 poetic units (1,22,23:1-7). |
| 1Kgs | 20 | 3 | Reign/prophetic-cycle chunking; Temple dedication (8), Carmel contest (18) flagged. |
| 2Kgs | 22 | 5 | Two national-fall theodicy chapters (17, 25) and severe-content episodes (3:27, 6:24-7:20) flagged. |
| **Wave 2 total** | **129** | **30** | |
| **Cumulative (Waves 1-2)** | **343** | **103** | |

## Validation run (real commands, this session)

```
python scripts/validate_whole_bible_chunk_map.py <folder>/book_chunks/<Book>/chunks.jsonl --model-id M2_claude_sonnet5 --book <Book>
  -> OK for Josh, Judg, Ruth, 1Sam, 2Sam, 1Kgs, 2Kgs

python scripts/validate_t423_literary_quality_protocol.py --model-folder <folder> --book Josh --book Judg --book Ruth --book 1Sam --book 2Sam --book 1Kgs --book 2Kgs --require-artifacts
  -> T423 literary quality protocol: OK (clean pass, no fix-up needed this wave)
```

All poetry-marker chapters flagged by the substrate were individually verse-checked and
cross-confirmed against known content before use (Song of Deborah, Hannah's Song, the three
victory-song quotations, David's Lament, David's Song of Deliverance, David's Last Words).

## Owner gate status

`pilot_gate.status` remains `pending`; override remains in effect and logged (see Wave 1
checkpoint / `layer_decision_log.jsonl`). No new gate events this wave.

## Non-authorizations restated

All 129 new chunks and sidecar rows carry `non_authorizing: true`; `promotion_authority: none`
/ `atlas_promotion_authority: none` throughout. No canon, gold, route/evaluator, graph/vector,
or theology authority created.

## Next

Wave 3 (Writings): 1Chr, 2Chr, Ezra, Neh, Esth, Job, Ps, Prov, Eccl, Song, Lam. Psalms (150
chapters) and Job (42 chapters of poetic dialogue) will use a more substrate-data-driven
approach for accuracy at scale rather than hand-authored per-unit rationale for all 150 psalms
individually.
