# Task Handoff

## Task

- task_id: T391
- title: Manuscript Source Catalog Research Packet
- phase: phase_5
- status: complete_non_output_changing_research_packet

## Agent

- agent_name: codex
- mode: plan
- stage: final
- updated_at: 2026-06-22T21:10:00+00:00
- handoff_id: 88eb85dc9a5279a9

## Files read

- AGENTS.md
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- .ai/control/MASTER_CONTEXT.md (read-only)
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/current_focus.yaml
- .ai/control/manuscript_witness_reliability_scaffold.yaml
- .ai/control/manuscript_source_catalog_metadata_plan.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_lesson_index.yaml
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- .ai/tasks/T390.task.yaml
- scripts/validate_manuscript_source_catalog_metadata_plan.py
- scripts/validate_chunking_theological_decision_register.py
- scripts/validate_chunking_lesson_index.py
- scripts/validate_all.py
- tests/test_manuscript_source_catalog_metadata_plan.py
- Official source anchors reviewed via browser: IAA/Leon Levy DSS, Israel Museum Great Isaiah Scroll anchors, INTF/NTVMR/Liste/ECM/CBGM, CSNTM P52, Manchester Greek P 457, Codex Sinaiticus Project, Vatican Library Vat.gr.1209, British Library Royal MS 1 D V

## Files changed

- .ai/control/manuscript_source_catalog_research_packet.yaml
- docs/roadmap/T391_MANUSCRIPT_SOURCE_CATALOG_RESEARCH_PACKET.md
- scripts/validate_manuscript_source_catalog_research_packet.py
- tests/test_manuscript_source_catalog_research_packet.py
- .ai/tasks/T391.task.yaml
- .ai/handoffs/T391/handoff.md
- scripts/validate_all.py
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/roadmap_events.jsonl

## Decisions made

- T391 is source-metadata-only research. It does not create SQLite files, populate source rows, populate witness rows, import source text, store transcriptions, store Bible text, select readings, or authorize graph/retrieval/vector/chunk/apologetic authority.
- Curated source families are DSS biblical witness catalogs, NT manuscript catalogs, major codex project catalogs, holding institution catalogs, and critical apparatus method profiles.
- Confirmed facts are source-scoped and must carry source, method, confidence, provenance, and review status.
- Candidate claims and blocked claims are separated so future agents cannot accidentally promote them by vibe.
- Patristic/church father/commentary/reception/creed/theologian material remains Boundary Literature; doctrine lineage remains future Doctrine Genealogy.
- Next manuscript-reliability goal should be T392 SQLite source-catalog schema shell plus curated source/source-family/method/trust-rule rows only. Do not populate witness rows yet.

## Validation run

- command: python scripts/validate_manuscript_source_catalog_research_packet.py
- result: passed - 18 curated sources, 6 DSS confirmed facts, 10 NT confirmed facts
- command: python scripts/validate_chunking_theological_decision_register.py --changed-file docs/roadmap/T391_MANUSCRIPT_SOURCE_CATALOG_RESEARCH_PACKET.md --changed-file .ai/control/chunking_theological_decision_register.yaml --register-updated true
- result: passed
- command: python scripts/validate_chunking_lesson_index.py --changed-file AI_TABLE_OF_CONTENTS.md --changed-file docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md --changed-file .ai/control/chunking_lesson_index.yaml --index-updated true
- result: passed
- command: python scripts/validate_task_scope.py --task-id T391
- result: passed
- command: python scripts/agent/validate_handoffs.py
- result: passed
- command: python pipelines/ingest/usfm_importer.py --canonical-66-filter --processed-root build/t391_processed/usfm
- result: passed - regenerated ignored local canonical validation artifacts
- command: python scripts/validate_all.py
- result: passed
- command: python -m pytest -q
- result: passed - 558 passed in 439.97s
- failures: none

## Known risks

- Official source pages can be dynamic. The packet records source anchors and source-scoped claims, but later row population must re-check source pages, access/rights, and dates.
- Israel Museum Great Isaiah detailed witness metadata is conservatively treated as located but not extracted into row-level claims.
- P45/P46/P66/P75 are priority candidates, not populated records; official source bundles still need curation.
- Copy-abundance and reliability reports remain blocked until variant units, witness distribution, and method profiles exist.

## Open questions

- Which official holding-institution pages should be preferred for P45/P46/P66/P75?
- Should T392 seed only source_catalog/source_family/method/trust-rule rows, or also create empty witness tables with fail-closed validators?
- Which source rights/access fields should become mandatory before any image-derived metadata or minimal source excerpts are stored?

## Next agent instruction

Start T392 only from live origin/main. Read AI_FRONT_DOOR.md, MASTER_CONTEXT.md read-only, PROJECT_STATUS.md, DATA_MAP.md, T387 scaffold, T390 metadata plan, and T391 research packet. Build the SQLite source-catalog schema shell and seed only curated source_catalog/source_family/method_profile/trust-rule metadata rows from T391 official source anchors. Do not populate witness rows, import source text, store manuscript transcription or Bible text, select preferred readings/source traditions, create graph/retrieval/vector output, or state apologetic conclusions as authority.

---

## Handoff refresh: final

- agent_name: codex
- mode: plan
- updated_at: 2026-06-22T21:12:28+00:00
- handoff_id: 829f0cf0c6b27645
