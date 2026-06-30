# T411 Candidate Options Docket

Status: non-authorizing setup material. Cursor must not choose targets.

Claude final audit status: T410 has no P0/P1 blockers. Forward P2-a requires a T411 emitted-artifact validator before Cursor runs; this task supplies that gate.

## Supplied Candidates

| Candidate | Parent Span | Lane | Queue Status | Language Layer | Cursor Authority |
| --- | --- | --- | --- | --- | --- |
| `T402-LC-063` | `2John.1.1-2John.1.3` | epistle opening/greeting | `ready_for_review_packet` | Greek optional | none |
| `T402-LC-057` | `Phlm.1.1-Phlm.1.7` | epistle opening/greeting | `ready_for_review_packet` | Greek optional | none |
| `T402-LC-032` | `Jonah.1.1-Jonah.1.3` | narrative scene/notice | `ready_for_review_packet` | Hebrew optional | none |

## Required Cursor Posture

- Research-only and review-packet prep only.
- Treat paragraph markers, Strong's tags, headings, and raw-source metadata as evidence-only.
- Do not create reviewed gold, child spans, chunk output, route/evaluator behavior, graph/retrieval/vector truth, embeddings/indexes, source rows, canon changes, or theology authority.
- Stop and create an escalation packet for low confidence, doctrinal pressure, textual-variant pressure, speaker ambiguity, identity/ecclesiology claims, slavery/social ethics claims, prophetic typology claims, or any proposed boundary that needs more than text-local evidence.

## Required Preflight Before Cursor Starts

```bash
python scripts/validate_parallel_execution_safety.py --task-id T411 --require-task-branch
python scripts/validate_t411_cursor_batch_artifacts.py
```
