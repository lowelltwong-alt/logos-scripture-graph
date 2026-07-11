# Task Handoff

## Task

- task_id: T481
- authorization_id: SRC-PILOT-A
- title: SRC-PILOT-A Primary Witness Wave 0 Catalog
- phase: phase_5
- status: wave0_scaffold_complete_pending_pr

## Agent

- agent_name: cursor
- mode: execution_metadata_non_authorizing
- stage: final
- updated_at: 2026-07-10T20:15:00+00:00
- worktree: C:/wt/logos-scripture-src-pilot-a
- branch: cursor/src-pilot-a-t469-wave0

## Files read

- AI_FRONT_DOOR.md
- AI_WORK_START_HERE.md
- AI_TABLE_OF_CONTENTS.md
- .ai/control/MASTER_CONTEXT.md (read-only)
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- .ai/control/primary_witness_acquisition_waves.yaml
- docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md
- .ai/tasks/T469.task.yaml
- .ai/handoffs/T469/handoff.md
- .ai/control/manuscript_source_catalog_research_packet.yaml
- governance/INDEPENDENT_STUDY_SOURCE_AUTHORIZATION.yaml (upstream)
- governance/registry/BIBLE_SOURCE_ACQUISITION_CANDIDATES.yaml (upstream)
- governance/registry/FAMILY_WORK_REGISTRY.yaml (upstream)
- data/raw manifests for eng-web, sblgnt, openscriptures_oshb

## Files changed

- .ai/tasks/T481.task.yaml
- .ai/control/primary_bible_witness_catalog.yaml
- .ai/control/chunking_lesson_index.yaml (LSN-060)
- .ai/control/PROJECT_STATUS.md
- .ai/handoffs/T481/handoff.md
- data/candidate/source_catalog/primary_bible_witnesses/* (Wave 0 scaffold)
- docs/roadmap/T481_SRC_PILOT_A_WAVE0.md
- scripts/validate_primary_bible_witness_catalog.py
- scripts/validate_all.py
- tests/test_primary_bible_witness_catalog.py
- AI_TABLE_OF_CONTENTS.md
- governance/registry/FAMILY_WORK_REGISTRY.yaml (in logos-gov-t469-completion-v2 worktree; pending governance PR)

## Decisions made

- Prerequisites verified merged: governance PR #103, scripture-graph PR #168.
- Used task_id T481 with authorization_id SRC-PILOT-A (handoff schema requires T### task ids).
- Created isolated worktree `C:/wt/logos-scripture-src-pilot-a` on `cursor/src-pilot-a-t469-wave0` from `origin/main`; did not touch dirty root worktree on `codex/w2-2-scripture-mirror-freshness`.
- Registered `WORK-SCR-T481-SRC-PILOT-A` in family work registry with overlap resolution against blocked T468 work.
- Wave 0 only: 24 source catalog rows, rights reviews, empty acquisition ledger, reuse inventory for WEB/SBLGNT/OSHB/WLC without duplication.
- Restricted witnesses (Great Isaiah Scroll, Vaticanus, Alexandrinus, CSNTM papyri, Sinaiticus images) remain metadata/locator only.
- Codex Sinaiticus XML queued for Wave 1 source-specific rights review; no XML downloaded.
- Showcase A (Isa 53:10-12) and Showcase B (Mark 16:8-20) scaffolds created; evidence packets not populated yet (PR 4 scope).
- Permission requests drafted in queue; send_policy blocks automatic sending.

## Validation run

- command: python scripts/validate_primary_bible_witness_catalog.py
- result: pass
- failures: none

- command: python -m pytest tests/test_primary_bible_witness_catalog.py -q
- result: pass (3 passed)
- failures: none

- command: python scripts/validate_task_scope.py --task-id T481
- result: pass (after runtime_language_preflight added)
- failures: none

- command: python scripts/validate_chunking_lesson_index.py
- result: pass (after LSN-060 added)
- failures: none

- command: python scripts/agent/validate_handoffs.py
- result: pass
- failures: none

- command: python scripts/validate_all.py
- result: partial
- failures: validate_t439_phlm_alignment_bridge_expansion.py FileNotFoundError for generated canonical word_tokens.jsonl in fresh worktree without ingested canonical data; unrelated pre-existing gates otherwise passed including validate_primary_bible_witness_catalog.py

- command: python -m pytest -q
- result: not_run_full_suite
- failures: fresh worktree lacks generated canonical data; focused T481 tests passed

## Known risks

- `LOGOS_EXTERNAL_ASSET_ROOT` is not set; external acquisition correctly blocked until owner provides safe path.
- Fresh worktree lacks generated canonical artifacts; full validate_all/pytest may fail on unrelated T439 gates until ingest or run from data-complete worktree.
- Codex Sinaiticus XML CC BY-NC-SA terms need exact snapshot and owner noncommercial decision before any download.
- Governance family-work registry update is in `C:/wt/logos-gov-t469-completion-v2` and needs a small governance PR.
- Primary governance repo checkout has unrelated merge conflicts; not modified.

## Open questions

- Owner: approve noncommercial local storage for Codex Sinaiticus XML under SRC-PILOT-A?
- Owner: set `LOGOS_EXTERNAL_ASSET_ROOT` to a non-Git, non-OneDrive path with ≥50 GB before Wave 1+ downloads?
- Owner: approve sending any permission-request drafts?

## Next agent instruction

Open PR 1 from `cursor/src-pilot-a-t469-wave0` with Wave 0 catalog only. Then PR 2: populate showcase packet structures referencing reuse manifests; PR 3: Sinaiticus XML rights decision; PR 4: authorized evidence population; PR 5: permission packet and audit. Resume from acquisition_manifest and external run journal before any download. Never store restricted images locally without explicit permission.

## Boundary-Hardening Refresh

- task_id: T481
- agent_name: Codex
- mode: execution_boundary_hardening
- updated_at: 2026-07-10T21:30:00+00:00

### Files read

- `.ai/control/primary_bible_witness_catalog.yaml`
- `data/candidate/source_catalog/primary_bible_witnesses/manifest.yaml`
- `scripts/validate_primary_bible_witness_catalog.py`
- `scripts/validate_external_asset_root.py`
- `scripts/guard_primary_witness_acquisition.py`
- focused T481 tests and candidate/graph pipeline references

### Files changed

- `.ai/control/primary_bible_witness_catalog.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/tasks/T481.task.yaml`
- `data/candidate/source_catalog/primary_bible_witnesses/manifest.yaml`
- `scripts/validate_primary_bible_witness_catalog.py`
- `scripts/validate_external_asset_root.py`
- `tests/test_primary_bible_witness_catalog.py`
- `tests/test_external_asset_root.py`
- `.ai/handoffs/T481/handoff.md`

### Decisions and protections

- The primary-witness catalog is mechanically non-admissible to graph, retrieval, embedding, canonical-promotion, source-text, and manuscript-reading paths.
- The validator rejects prohibited text, reading, graph, retrieval, and vector fields; it also rejects Greek/Hebrew-script text in catalog metadata.
- Pipeline and script references to this catalog fail unless they are part of the narrow guarded validation/acquisition surface.
- `LOGOS_EXTERNAL_ASSET_ROOT` must be outside Git, OneDrive, and the shared workspace.

### Validation

- `python scripts/validate_primary_bible_witness_catalog.py`: pass.
- `python -m pytest tests/test_primary_bible_witness_catalog.py tests/test_external_asset_root.py -q`: pass, 10 passed.
- `python scripts/validate_task_scope.py --task-id T481`: pass.
- `python scripts/agent/validate_handoffs.py`: pass.
- `git diff --check`: pass.
- `python scripts/validate_all.py`: timed out after 124 seconds without emitted failure output.
- `python -m pytest -q`: timed out after 184 seconds without emitted failure output.

### Risks and unresolved questions

- Full-repository gates require a longer CI/data-complete environment; their timeout is not evidence of a T481 boundary failure.
- Any future owner-authorized importer must be explicitly added to the guarded admission surface and independently reviewed.

### Exact next action

Run full validation in CI or a data-complete worktree, then update PR #169 with this boundary-hardening commit and request a fresh review.

---

## Handoff refresh: start

- agent_name: Codex
- mode: execution_boundary_hardening
- updated_at: 2026-07-10T21:15:55+00:00
- handoff_id: b24dc8f2ce06a4de

---

## Handoff refresh: final

- agent_name: Codex
- mode: execution_boundary_hardening
- updated_at: 2026-07-10T21:24:49+00:00
- handoff_id: e548ea0a20fdf310
