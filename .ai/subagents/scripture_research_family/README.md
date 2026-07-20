# Scripture Research Subagent Family

Status: reusable role-brief scaffold. These briefs are invocation material, not live automations.

Use this family when the project touches manuscripts, rights, OCR, source cataloging, biblical scholarship, archaeology/material culture, or unknown-unknown discovery.

## Required Rules

- Read `AI_FRONT_DOOR.md`, `.ai/control/MASTER_CONTEXT.md`, `.ai/control/PROJECT_STATUS.md`, `.ai/control/subagent_family_knowledge_base_plan.yaml`, and `.ai/control/unknown_unknowns_radar.yaml`.
- Keep every result candidate-only unless a later owner-gated task says otherwise.
- Do not download sources, run OCR, store transcriptions, build embeddings, create graph/retrieval truth, select preferred readings, change canon scope, or authorize theology.
- Every material worker output needs an independent checker, usually `governance_evidence_reviewer`.
- Ultra effort requires explicit Lowell approval for that exact attempt.

## Roles

- `rights_provenance_scout.md`
- `source_cataloger.md`
- `ocr_paleography_pipeline_scout.md`
- `biblical_scholarship_librarian.md`
- `archaeology_material_culture_scout.md`
- `unknown_unknowns_radar.md`
- `governance_evidence_reviewer.md`

## Normal Routing

Use one role for narrow work. Use two roles only when the task has separate independent surfaces, such as rights plus source cataloging. Use `unknown_unknowns_radar` before broad expansion or public claims. Use `governance_evidence_reviewer` before any result becomes a task recommendation.
