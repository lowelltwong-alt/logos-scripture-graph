# T399 No-Context Audit Surface

## Scope

Audit `.ai/control/t399_focused_bible_wide_research_queue.yaml` as the Goal 2 focused
Bible-wide research queue.

## Claims To Verify

- T399 uses T398, T386, dossier queues, source metadata, original-language, contextual reading,
  manuscript/source metadata, and Orthodox Hermeneutic Firewall surfaces as inputs.
- T399 contains a scored candidate queue across the high-risk lanes.
- Each queue item records why it may affect chunking, theological/hermeneutical risks,
  variant/source-tradition status, metadata needs, original-language needs, owner decisions, and
  safety status.
- T399 records owner-decision prompts but does not treat recommendations as owner selection.
- T397 remains the separate route-isolated harness prep path.
- T399 authorizes no target selection, reviewed gold, child spans, chunk output, route/evaluator
  behavior, graph/retrieval/vector truth, boundary import, preferred reading/source tradition,
  canon-scope change, source/manuscript rows, whole-Bible output, or theology authority.

## Required Commands

```bash
python scripts/validate_t399_focused_bible_wide_research_queue.py
python -m pytest tests/test_t399_focused_bible_wide_research_queue.py -q
python scripts/validate_all.py
```

## Audit Notes

T399 intentionally keeps high-scoring variant/source-tradition cases visible while marking them
blocked before promotion. A high score is research priority, not authority.
