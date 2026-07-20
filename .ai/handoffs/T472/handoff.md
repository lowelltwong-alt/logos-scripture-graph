# Task Handoff

## Task

- task_id: T472
- title: Leipzig Sinaiticus Public Showcase Starter Pack
- phase: phase_5
- status: complete_limited_showcase

## Agent

- agent_name: codex
- mode: build
- stage: final
- updated_at: 2026-07-15T13:50:00+00:00
- handoff_id: 2e29f9d4131c4b1d

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- ROADMAP.md
- ROADMAP_STATE.yaml
- .digital-asset/dad-integration.json
- .digital-asset/context-map.json
- data/raw/original_language/greek/sblgnt/source_manifest.yaml
- schemas/source_manifest.schema.json
- Leipzig University Library IIIF manifest at https://iiif.ub.uni-leipzig.de/0000061851/manifest.json

## Files changed

- .ai/tasks/T472.task.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- docs/public/LOGOS_SCRIPTURE_GRAPH_PUBLIC_SHOWCASE.md
- data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/source_manifest.yaml
- data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/web/codex_sinaiticus_leipzig_canvas_00000001_web.jpg
- data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/web/codex_sinaiticus_leipzig_canvas_00000043_web.jpg
- data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/web/codex_sinaiticus_leipzig_canvas_00000086_web.jpg
- .ai/handoffs/T472/handoff.md

## Decisions made

- Treated Lowell's request as explicit authorization for a tiny public-facing image acquisition, not bulk source acquisition.
- Downloaded exactly three web-sized JPEG derivatives from the Leipzig IIIF image service: canvases 1, 43, and 86.
- Stored images under `data/raw/primary_witnesses/.../showcase/web/` to honor the raw-source vault rule.
- Added a raw source manifest with rights basis, IIIF URLs, canvas labels, file sizes, checksums, and non-authorizations.
- Created a contributor-facing public showcase page explaining what the project is building, what can be built on top, and what still does not exist in integrated/governed form.
- Kept this starter pack separate from OCR, transcription, source text import, graph/retrieval/vector truth, canon changes, and boundary-material import.

## Validation run

- command: python scripts/agent/force_handoff.py --task-id T472 --agent codex --stage start
- result: pass
- failures: none

- command: python scripts/scan_raw_sources.py
- result: pass
- failures: none

- command: python scripts/generate_data_map.py
- result: pass
- failures: none

- command: python scripts/agent/force_handoff.py --task-id T472 --agent codex --stage final
- result: pass
- failures: none

- command: python scripts/scan_raw_sources.py --check
- result: pass
- failures: none

- command: python scripts/generate_data_map.py --check
- result: pass
- failures: none

- command: python scripts/validate_task_scope.py --task-id T472 --changed-file .ai/tasks/T472.task.yaml --changed-file .ai/handoffs/T472/handoff.md --changed-file .ai/control/handoff_ledger.jsonl --changed-file .ai/control/PROJECT_STATUS.md --changed-file .ai/control/DATA_MAP.md --changed-file .ai/control/RAW_SOURCE_INVENTORY.md --changed-file docs/public/LOGOS_SCRIPTURE_GRAPH_PUBLIC_SHOWCASE.md --changed-file data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/source_manifest.yaml --changed-file data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/web/codex_sinaiticus_leipzig_canvas_00000001_web.jpg --changed-file data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/web/codex_sinaiticus_leipzig_canvas_00000043_web.jpg --changed-file data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/web/codex_sinaiticus_leipzig_canvas_00000086_web.jpg
- result: pass
- failures: none

- command: python scripts/agent/validate_handoffs.py
- result: pass
- failures: none

- command: git diff --check -- .ai/tasks/T472.task.yaml .ai/handoffs/T472/handoff.md .ai/control/handoff_ledger.jsonl .ai/control/PROJECT_STATUS.md .ai/control/DATA_MAP.md .ai/control/RAW_SOURCE_INVENTORY.md docs/public/LOGOS_SCRIPTURE_GRAPH_PUBLIC_SHOWCASE.md data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/showcase/source_manifest.yaml
- result: pass
- failures: "No whitespace errors. Git warned that .ai/control/DATA_MAP.md and .ai/control/handoff_ledger.jsonl CRLF will be replaced by LF when Git next touches them."

## Known risks

- This is a public showcase sampler, not a complete Leipzig acquisition and not a full-resolution archive.
- The images are web-sized derivatives chosen for orientation and contributor communication.
- Broader acquisition still requires a separate task with storage path, bulk policy, checksums, and lane classification.
- Boundary/non-66 material remains excluded from default Scripture authority and default retrieval.

## Open questions

- Decide where the eventual public website or landing page should live if Lowell wants this surfaced outside the repository.
- Decide whether the next step is a full Leipzig metadata canvas map or a polished website/visual explainer.
- Decide whether to request/record a standard public attribution sentence in README-level docs.

## Next agent instruction

Use `docs/public/LOGOS_SCRIPTURE_GRAPH_PUBLIC_SHOWCASE.md` as the public-facing orientation artifact. If continuing acquisition, do not download more images until a new task authorizes either a full Leipzig canvas metadata map or a broader image acquisition. Keep canonical_66 and boundary_non_66 lanes separated, and do not run OCR, embeddings, vector indexes, graph creation, retrieval promotion, source-text import, canon-scope changes, or textual-critical decisions without a later explicit task.

---

## Handoff refresh: final

- agent_name: codex
- mode: 
- updated_at: 2026-07-15T13:42:18+00:00
- handoff_id: 65674c00a76e9453
