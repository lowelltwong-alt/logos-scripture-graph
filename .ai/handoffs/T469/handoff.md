# Task Handoff

## Task

- task_id: T469
- title: Primary Bible Witness Acquisition Waves For Cursor
- phase: phase_5
- status: complete_non_authorizing_plan

## Agent

- agent_name: codex
- mode: plan
- stage: final
- updated_at: 2026-07-08T13:25:24+00:00
- handoff_id: 3e3a9de1367d80de

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- data/raw/original_language/witness_catalogs/manuscript_libraries.yaml
- .ai/control/manuscript_source_catalog_metadata_plan.yaml
- .ai/control/manuscript_source_catalog_research_packet.yaml
- .ai/control/dss_biblical_witness_source_rows.yaml
- .digital-asset/dad-integration.json
- .digital-asset/context-map.json
- .digital-asset/governance-map.yaml
- .ai/tasks/T467.task.yaml
- .ai/tasks/T468.task.yaml

## Files changed

- .ai/tasks/T469.task.yaml
- .ai/control/handoff_ledger.jsonl
- .ai/control/primary_witness_acquisition_waves.yaml
- docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md
- .ai/control/PROJECT_STATUS.md
- .ai/handoffs/T469/handoff.md

## Decisions made

- Used T469 because T468 already exists as an unrelated governance mirror freshness task in the current worktree.
- Kept T469 planning-only: no raw downloads, source text import, image storage, transcription storage, graph/retrieval/vector truth, preferred reading, source-tradition choice, canon change, or theology authority.
- Structured Cursor execution in waves: W0 metadata/rights scaffold, W1 text/transcription review, W2 public-domain/open image sets, W3 public-view/permission-needed source cataloging, and W4 restricted/advanced dataset review.
- Recorded disk estimates from Internet Archive metadata probes where available: public/open image originals are about 11 GB without Aleppo/Cairensis and about 14 GB with those candidates after rights review; full IA derivatives are about 23 GB and about 28 GB respectively.
- Recommended 50 GB free space for near-term acquisition and 100-250 GB if later permissioned high-resolution image expansion is authorized.

## Validation run

- command: python scripts/agent/force_handoff.py --task-id T469 --agent codex --stage start
- result: pass
- failures: none

- command: python scripts/agent/force_handoff.py --task-id T469 --agent codex --stage final
- result: pass
- failures: none

- command: python scripts/validate_task_scope.py --task-id T469 --changed-file .ai/tasks/T469.task.yaml --changed-file .ai/handoffs/T469/handoff.md --changed-file .ai/control/primary_witness_acquisition_waves.yaml --changed-file .ai/control/PROJECT_STATUS.md --changed-file docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md
- result: pass
- failures: none

- command: python scripts/validate_task_scope.py --task-id T469 --changed-file .ai/tasks/T469.task.yaml --changed-file .ai/handoffs/T469/handoff.md --changed-file .ai/control/handoff_ledger.jsonl --changed-file .ai/control/primary_witness_acquisition_waves.yaml --changed-file .ai/control/PROJECT_STATUS.md --changed-file docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md
- result: pass
- failures: none

- command: python scripts/agent/validate_handoffs.py
- result: pass
- failures: none

- command: git diff --check -- .ai/tasks/T469.task.yaml .ai/handoffs/T469/handoff.md .ai/control/handoff_ledger.jsonl .ai/control/primary_witness_acquisition_waves.yaml .ai/control/PROJECT_STATUS.md docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md
- result: pass
- failures: "No whitespace errors. Git warned that .ai/control/handoff_ledger.jsonl CRLF will be replaced by LF when Git next touches it."

- command: python scripts/validate_all.py
- result: fail
- failures: "Existing/concurrent T468 mirror-freshness work and T469 both appear in the dirty worktree; upstream governance commit drift also failed with expected ad338b5c2dc2c8d979843707aaaabb834cf64785 got eb7b399f8b0e61de926468d30c96e4139b9038eb. Most validators passed before final suite failure."

- command: python -m pytest -q
- result: fail
- failures: "2 failed, 903 passed. Failures were test_validate_all_suite, which inherits the validate_all failures above, and test_mirror_freshness_passes due upstream governance commit drift."

## Known risks

- The worktree already contained unrelated dirty/untracked T468/governance freshness changes before T469 began. Do not revert or overwrite them.
- Full-repo validation may be affected by unrelated active T468 work. Use T469's explicit changed-file task-scope command for a focused check if full validation is noisy.
- Some image sources are public-view-only or noncommercial/conditioned, so Cursor must not download them without an execution task and rights decision.
- Internet Archive mirrors are useful but should not replace official holding-institution/project records; preserve both source and mirror provenance.

## Open questions

- Owner must decide whether noncommercial sources such as Aleppo mirror material and Codex Sinaiticus XML may be stored locally and how they may appear in downstream DAD/runtime release artifacts.
- Owner must decide whether future permission requests should be sent to CSNTM, Manchester, Vatican Library, British Library, Israel Museum/IAA, and other holding institutions.
- Cursor should verify source-specific rights again at execution time because public pages and licenses can change.

## Next agent instruction

Cursor should execute Wave 0 only: create metadata-only source catalog and rights review files under `data/candidate/source_catalog/primary_bible_witnesses/` from `.ai/control/primary_witness_acquisition_waves.yaml` and `docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md`. Do not download raw sources, do not store images, do not store transcriptions, do not import source text, and do not create graph/retrieval/vector/canonical/theology truth.
