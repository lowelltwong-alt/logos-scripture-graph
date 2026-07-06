# Wave 1 Checkpoint — Torah (M2_claude_sonnet5)

**Status:** complete | **Books:** Gen, Exod, Lev, Num, Deut (5/66) | **Owner gate:** pilot_gate override authorized (see `layer_decision_log.jsonl`)

## Summary

| Book | Chunks | Chapters | Verses | Low-conf rows | Notes |
|---|---:|---:|---:|---:|---|
| Gen | 69 | 50 | 1,533 | 39 | Pilot book. Toledot-formula seams + poetic insets cross-checked against substrate. |
| Exod | 40 | 40 | 1,213 | 5 | Plague cycle + Tabernacle instruction/execution blocks grouped by scene, not chapter. |
| Lev | 25 | 27 | 859 | 6 | Per-topic legal chunking; most chunks legitimately chapter-exact (text's own structure). |
| Num | 39 | 36 | 1,288 | 11 | Census/list chunks + 4 substrate-confirmed poetic oracle insets (Priestly Blessing, Balaam). |
| Deut | 41 | 34 | 959 | 12 | Discourse-structure chunking; Song of Moses / Blessing of Moses kept as compositional units. |
| **Total** | **214** | **187** | **5,852** | **73** | |

## Validation run (this session, real commands)

```
python scripts/validate_whole_bible_chunk_map.py <folder>/book_chunks/<Book>/chunks.jsonl --model-id M2_claude_sonnet5 --book <Book>
  -> OK for Gen, Exod, Lev, Num, Deut

python scripts/validate_t423_literary_quality_protocol.py --model-folder <folder> --book Gen --book Exod --book Lev --book Num --book Deut --require-artifacts
  -> T423 literary quality protocol: OK
```

One real defect was caught and fixed during Genesis: several chunks had a malformed
`confidence` value, and 23 chunks whose spans exactly matched a full chapter needed
`medium_low` confidence forced (Genesis is pilot-fragile) even though the boundary
reflected genuine narrative judgment. Fixed by regenerating with the substrate's exact
chapter spans cross-referenced against every chunk.

## Owner gate status

`pilot_gate.status` is still `pending`. `scripts/validate_t423_pilot_gate.py` now reports
(expected, pre-disclosed before Exodus started):

```
ERROR: M2_claude_sonnet5: books outside pilot set while pilot_gate.status=pending: Deut, Exod, Lev, Num
```

This is the explicit, owner-authorized consequence of continuing Wave 1 past Genesis before
the pilot gate flips to `go` — recorded in `layer_decision_log.jsonl` as `owner_gate_override`.

## Non-authorizations restated

All 214 chunks and all sidecar rows carry `non_authorizing: true`. No reviewed gold, canon
output, child-span authority, route/evaluator behavior, graph/retrieval/vector truth, atlas
promotion, or theology authority is created by this wave. `promotion_authority: none` /
`atlas_promotion_authority: none` on every escalation/atlas row.

## Next

Wave 2 (History): Josh, Judg, Ruth, 1Sam, 2Sam, 1Kgs, 2Kgs.
