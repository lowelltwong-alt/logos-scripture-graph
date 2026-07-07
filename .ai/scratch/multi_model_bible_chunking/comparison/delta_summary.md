# Delta Summary — Multi-Model Whole-Bible Chunk Comparison

## Scope
- Models: M1_cursor, M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55, M5_gemini_thinking, M6_fable5
- N = 6; majority = ceil(0.7×N) = 5
- Books compared: 66

## Headline metrics
- Overall verse-coverage agreement rate: 6.17%
- Legacy exact-span rate (audit only): 0.93%
- Easy chunk count: 144
- Delta span count: 1048
- Frontier review queue rows: 1095
- Fork threshold signal: FULL_FAIL (minimum 50.00%)

## Highest-disagreement books (top 10)
- 1Chr: 0.00%
- 1Cor: 0.00%
- 1John: 0.00%
- 1Kgs: 0.00%
- 1Pet: 0.00%
- 1Sam: 0.00%
- 1Thess: 0.00%
- 1Tim: 0.00%
- 2Chr: 0.00%
- 2Cor: 0.00%

## False consensus warnings
- none flagged

## Decision routing
- `agreement_chunks.jsonl` contains non-authorizing consensus/easy-majority evidence.
- `disagreement_delta.jsonl` contains non-authorizing deltas with M4/M6 alignment fields.
- `owner_decision_docket.yaml` assigns every agreement/delta row a docket status.
- `frontier_review_queue.jsonl` carries high-risk/low-confidence rows for Claude/frontier review.
- `harness_improvement_queue.md` collects likely harness/rerun issues.

## Non-authorizations
- Agreement does not promote gold or chunk output
- promotion_authority: none
