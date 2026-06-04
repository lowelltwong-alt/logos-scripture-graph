# Task Handoff

## Task

- task_id: T100
- title: Drop WEB Classic USFM archive and create source manifest
- phase: phase_1
- status: complete

## Agent

- agent_name: claude
- mode: build
- stage: final
- updated_at: 2026-06-03T17:15:00+00:00
- handoff_id: T100-claude-final

## Files read

- AI_FRONT_DOOR.md
- data/raw/bible/eng-web/source_manifest.example.yaml
- pipelines/validate/validate_manifest.py
- pipelines/ingest/usfm_importer.py
- config/sources/sources.yaml

## Files changed

- data/raw/bible/eng-web/source_manifest.yaml (created)
- pipelines/validate/validate_manifest.py (checksum verification + line-anchored key parse)
- pipelines/ingest/usfm_importer.py (manifest archive override only on default --archive; manifest-driven SHA check)
- config/sources/sources.yaml (eng-web.status → present)
- ROADMAP_STATE.yaml
- .ai/control/roadmap_events.jsonl
- .ai/control/current_focus.yaml
- .ai/handoffs/T100/handoff.md

## Decisions made

- Created verified source manifest with SHA256 `a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e` matching on-disk zip (3,249,612 bytes).
- Upgraded `validate_manifest.py` to verify archive exists and SHA256 matches manifest (fixes VAL-1 false-positive risk).
- Fixed importer so explicit `--archive` (pytest fixtures) is not overridden by manifest; default CLI ingest still resolves archive from manifest.
- Phase 1 raw vault gate is closed for WEB Classic.

## Validation run

- command: `python pipelines/validate/validate_manifest.py data/raw/bible/eng-web/source_manifest.yaml`
- result: passed
- command: `python pipelines/ingest/usfm_importer.py --manifest data/raw/bible/eng-web/source_manifest.yaml`
- result: passed; regenerated canonical + processed outputs
- command: `python scripts/validate_jsonl.py` (10 JSONL paths)
- result: passed; 864904 records
- command: `python scripts/validate_repo.py`
- result: passed
- command: `python -m pytest -q`
- result: passed; 5 passed

## Known risks

- Raw zip is local-only unless committed or documented as external drop; manifest is the reproducibility anchor.
- Full corpus re-ingest is slow (~60s); CI should cache or smoke-test on fixture only.

## Open questions

- Should `source_manifest.yaml` be committed while zip stays gitignored/LFS? (Recommended: yes for manifest, no for zip unless LFS.)

## Next agent instruction

Phase 1 complete. Proceed to Phase 3 chunking per `.ai/handoffs/T301/handoff.md`. Do not re-run full ingest unless manifest or importer changes.
