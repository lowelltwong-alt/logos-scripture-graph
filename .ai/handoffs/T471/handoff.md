# Task Handoff

## Task

- task_id: T471
- title: Leipzig Codex Sinaiticus Split-Corpus Start Plan
- phase: phase_5
- status: complete_non_authorizing_plan

## Agent

- agent_name: codex
- mode: plan
- stage: final
- updated_at: 2026-07-15T13:22:00+00:00
- handoff_id: 581fc1454ef0ee86

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/boundary_material_routing.yaml
- .ai/control/primary_witness_acquisition_waves.yaml
- docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md
- .ai/tasks/T469.task.yaml
- .ai/handoffs/T469/handoff.md
- Leipzig University Library IIIF manifest metadata at https://iiif.ub.uni-leipzig.de/0000061851/manifest.json
- Codex Sinaiticus official content page at https://www.codexsinaiticus.org/en/codex/content.aspx

## Files changed

- .ai/tasks/T471.task.yaml
- .ai/control/leipzig_sinaiticus_split_corpus_plan.yaml
- docs/roadmap/T471_LEIPZIG_SINAITICUS_SPLIT_CORPUS_START_PLAN.md
- .ai/control/PROJECT_STATUS.md
- .ai/handoffs/T471/handoff.md

## Decisions made

- Created T471 as planning-only because Lowell wants to start with the Leipzig Codex Sinaiticus permission grant while also retaining books not in the default Protestant 66-book Bible.
- Treated Leipzig as one rights-cleared source but not one undifferentiated corpus.
- Split the plan into a canonical_66 biblical witness lane for logos-scripture-graph and a boundary_non_66 lane for deuterocanonical/apocrypha and other non-66 material.
- Required the first future execution step to be metadata-only canvas classification from the IIIF manifest before any image download.
- Preserved the boundary rule: non-66 material may be studied and preserved, but not imported into canonical Scripture authority or default Scripture retrieval.

## Validation run

- command: python scripts/agent/force_handoff.py --task-id T471 --agent codex --stage start
- result: pass
- failures: none

- command: python scripts/validate_task_scope.py --task-id T471 --changed-file .ai/tasks/T471.task.yaml --changed-file .ai/handoffs/T471/handoff.md --changed-file .ai/control/handoff_ledger.jsonl --changed-file .ai/control/PROJECT_STATUS.md --changed-file .ai/control/leipzig_sinaiticus_split_corpus_plan.yaml --changed-file docs/roadmap/T471_LEIPZIG_SINAITICUS_SPLIT_CORPUS_START_PLAN.md
- result: pass
- failures: none

- command: git diff --check -- .ai/tasks/T471.task.yaml .ai/handoffs/T471/handoff.md .ai/control/handoff_ledger.jsonl .ai/control/PROJECT_STATUS.md .ai/control/leipzig_sinaiticus_split_corpus_plan.yaml docs/roadmap/T471_LEIPZIG_SINAITICUS_SPLIT_CORPUS_START_PLAN.md
- result: pass
- failures: "No whitespace errors. Git warned that .ai/control/handoff_ledger.jsonl CRLF will be replaced by LF when Git next touches it."

## Known risks

- The Leipzig permission grant covers Leipzig-held/digitized images only; it does not cover British Library, Vatican, St Catherine's, Russian National Library, or the shared Codex Sinaiticus project assets.
- The official Codex Sinaiticus content page describes the wider surviving codex, not only Leipzig's 43 leaves; future execution must classify exact Leipzig canvas coverage before assuming which works are present.
- Full validation was not run for this small planning turn; prior local state had unrelated governance mirror drift risks.

## Open questions

- Lowell still needs to authorize a separate acquisition task before downloading Leipzig images.
- Future execution must choose the quarantine storage path outside Git and cloud sync.
- If the boundary lane needs actual source storage, decide whether that belongs in logos-boundary-literature or a local quarantined boundary profile first.

## Next agent instruction

Start with T471 L0 only: parse the Leipzig IIIF manifest metadata and create a metadata-only canvas coverage map. Classify every canvas as canonical_66, boundary_non_66, mixed_or_uncertain, or non_text_artifact. Do not download images, store transcriptions, import text, create embeddings, build vector indexes, change canon scope, or create graph/retrieval/canonical truth.

---

## Handoff refresh: final

- agent_name: codex
- mode: 
- updated_at: 2026-07-15T13:20:48+00:00
- handoff_id: 11b5a742c1581ae7
