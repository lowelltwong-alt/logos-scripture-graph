# T384 No-Context Audit Surface

## Scope

T384 records the Bible-wide research/readiness synthesis for faithful chunking prep:

- `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`
- `docs/roadmap/T384_BIBLE_WIDE_RESEARCH_READINESS_SYNTHESIS.md`
- `.ai/tasks/T384.task.yaml`
- `.ai/handoffs/T384/handoff.md`

The task is governance/readiness only. It does not change raw Scripture, canonical Scripture,
generated chunk output, reviewed-gold data, route runtime behavior, evaluator behavior, graph edges,
retrieval truth, vector/embedding output, or pipeline code.

## What To Verify

- `CD-061` exists in `.ai/control/chunking_theological_decision_register.yaml`.
- `LSN-013` exists in `.ai/control/chunking_lesson_index.yaml`.
- `.ai/control/chunking_agent_preflight.yaml` requires the T384 synthesis before future chunking work.
- `.ai/control/bible_chunking_readiness_map.yaml` records T384 as completed synthesis and points to
  `T385` as the next non-output owner decision packet.
- `ROADMAP_STATE.yaml`, `AI_FRONT_DOOR.md`, `AI_TABLE_OF_CONTENTS.md`, and
  `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md` route future agents to the T384 synthesis.

## Expected Findings

Expected green finding:

- T384 completes the research-first goal by mapping ready lanes, research gaps, human decisions,
  blocked authority changes, and the exact next non-output step.

Expected non-authorizations:

- No exact target selection.
- No reviewed-gold promotion.
- No child spans.
- No chunk output change.
- No route/evaluator behavior change.
- No graph, retrieval, vector, or edge truth.
- No boundary import.
- No preferred reading, source-tradition preference, canon-scope change, or whole-Bible output.
- No liberal-critical, anti-supernatural, heterodox, anti-canonical, or one-denomination systematic
  theology default as chunk authority.

## Validation

Required commands:

```bash
python scripts/validate_t384_bible_wide_research_readiness.py
python scripts/validate_chunking_agent_preflight.py
python scripts/validate_chunking_lesson_index.py
python scripts/validate_bible_chunking_readiness_map.py
python scripts/validate_chunking_theological_decision_register.py
python scripts/validate_task_scope.py --task-id T384
python scripts/agent/validate_handoffs.py
python scripts/validate_all.py
python -m pytest -q
```

## Next Step

T385 is the next step: Owner Decision Packet From T384 Research Readiness Synthesis.

T385 must present `HDM-001` through `HDM-007` with options, repercussions, recommendations, and
non-authorizations for owner review before any target selection, promotion, implementation, output,
graph/retrieval/vector, or authority-changing work.
