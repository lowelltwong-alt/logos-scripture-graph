# M1_cursor — model quality summary (pilot books)

**Model:** M1_cursor
**Strategy:** literary_marker_aware_v2
**Worktree:** scratch/t423-M1-cursor
**Substrate pin:** 9cfc4d0d0f1a2a215463ace6cb2ff179e4d94c835b7f81119a01a7dc890ae797
**Pilot books completed:** Gen, Ps, Phlm, Jonah, Rev

## Chunk counts

| Book | Chunks | Approach |
|------|--------|----------|
| Gen | 496 | Paragraph (`p`) + chapter boundaries; narrative/poetry heuristics |
| Ps | 171 | 149 psalm-per-chapter units + 22 acrostic stanzas for Ps 119 |
| Phlm | 8 | Epistle sections via paragraph markers |
| Jonah | 26 | Scene/paragraph splits; hymn unit in ch 2 |
| Rev | 147 | Paragraph + chapter; all chunks `frontier_flag_considered: true` |

## Sidecar totals (cumulative)

See validation run for exact counts in `low_confidence_register.jsonl`, `frontier_escalation_queue.jsonl`, `atlas_candidate_feed.jsonl`.

## Non-authorizations

Scratch compare input only. No canon output, reviewed gold, atlas promotion, frontier verdict, or theology authority.
