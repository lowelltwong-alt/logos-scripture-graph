# T450 Handoff - Bible Edge Taxonomy Research Program

## Task

- Task id: T450
- Agent: Codex
- Mode: planning/control-plane, non-authorizing
- Branch: `codex/t450-bible-edge-taxonomy`

## Files Read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `config/governance/predicate_registry.yaml`
- `schemas/relationship_object.schema.json`
- `schemas/graph_edge_record.schema.json`
- existing dossier queue validators and chunking/original-language control surfaces

## Files Changed

- `.ai/tasks/T450.task.yaml`
- `.ai/control/bible_edge_taxonomy_research_program.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/context/agent_work/T450/bible_edge_family_draft.md`
- `.ai/handoffs/T450/handoff.md`
- `docs/roadmap/T450_BIBLE_EDGE_TAXONOMY_RESEARCH_PROGRAM.md`
- `scripts/validate_t450_bible_edge_taxonomy.py`
- `tests/test_t450_bible_edge_taxonomy.py`
- `scripts/validate_all.py`
- `.digital-asset/mail/outbox.jsonl`

## Decisions Made

- T450 is planning-only and does not expand the predicate registry; it creates no theology authority or graph edge authority.
- CD-087 records this taxonomy in the theological decision register because the roadmap path is a watched governance surface.
- LSN-042 records the reusable lesson that edge taxonomy vocabulary is not graph authority.
- New predicate names are future proposals only.
- Edge families are separated by assertion mode: deterministic structure, reviewed semantic claims, and model-inferred candidates.
- High-risk theology, prophecy, apocalyptic, WJ/speaker, variant, covenant, and apologetic-polemic claims require frontier review plus owner gate before implementation.
- Rust is recommended only for deterministic high-volume edge hygiene, never for theological or hermeneutical decisions.
- DAD receives candidate-only lessons about the T450 taxonomy and dirty central-DAD coordination during parallel Rust rollouts.

## Validation Performed

Completed:

- `python scripts/validate_t450_bible_edge_taxonomy.py` - passed
- `python -m pytest tests/test_t450_bible_edge_taxonomy.py -q` - 4 passed
- `python scripts/validate_task_scope.py --task-id T450` - passed
- `python scripts/agent/validate_handoffs.py` - passed
- `python scripts/validate_all.py` - passed after seeding ignored generated canonical data into the worktree
- `python -m pytest -q` - 721 passed
- `python scripts/generate_data_map.py --check` - current
- `git diff --check` - passed

## Risks Introduced

- The taxonomy is intentionally broad. The validator keeps it non-authorizing, but later tasks must avoid treating this as a ready predicate registry.
- Apologetic and polemic lanes are useful, but high-risk. They must remain transparent, reviewed, and free from hostile caricature or hidden theology.
- Calendar, chronology, source-tradition, and manuscript lanes can create false precision if future data does not preserve uncertainty.

## Unresolved Questions

- Which edge family should be first for a production predicate proposal: deterministic structural edges or reviewed direct quotation/intertext edges?
- Should future edge candidates live under `data/candidate/graph/` or a new scratch-first edge lane before promotion?
- What exact frontier review prompt should be used for prophecy/apocalyptic and apologetic-polemic edge proposals?

## Next Action

Run the T450 validator suite. If green, open a planning-only PR. Do not generate graph edges or expand the predicate registry until a later owner-gated task authorizes exact predicates and data paths.
