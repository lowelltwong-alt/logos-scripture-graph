# Task Handoff

## Task

- task_id: T611
- title: Sanitized immutable M7 Sol candidate publication
- phase: phase_0
- status: complete_pending_merge

## Agent

- agent_name: Codex root
- mode: build
- stage: final
- updated_at: 2026-08-19T02:29:03+00:00
- handoff_id: fa93ba96e82e0ff8

## Files read

- Mandatory repository entry files and workspace-lifecycle policy/registry.
- Immutable Git objects at M7 commit `eaf31a940d3166b49c38ca26eb279392e0a3b25b`.
- M7 role, routing, strategy, receipt, review, Job, Psalm, progress, provenance, and license evidence through Git object reads only.
- No M8 content was read.

## Files changed

- Public entry/status: `AI_FRONT_DOOR.md`, `ROADMAP_STATE.yaml`, `.ai/control/{PROJECT_STATUS.md,current_focus.yaml,roadmap_events.jsonl,handoff_ledger.jsonl}`.
- Publication contract: `config/publications/m7_sol_candidate_v1.json`, `schemas/multi-model-candidate-publication.schema.json`.
- Public evidence: `docs/publications/m7-sol-candidate-v1/{README.md,ARTIFACT_MANIFEST.json}`, `docs/architecture/PUBLIC_PROJECT_OVERVIEW.md`.
- Reproducibility: `scripts/{build_candidate_publication.py,validate_candidate_publication.py,validate_all.py}`, `tests/test_candidate_publication.py`.
- Governed records: `.ai/tasks/T611.task.yaml`, `.ai/context/agent_work/T611/agent_mesh_manifest.v{1,2}.json`, this handoff.
- Test-fixture SHA refresh: `tests/fixtures/scripture_first_biblical_chunking_family/negative/release.owner_ready_fake_validation.json`.

## Decisions made

- Publish metadata and hashes only; embed zero M7 payload bytes because file-level privacy/license authority is incomplete.
- Report 66/66 book strategies, 66 books/1,178 candidate rows, and 22/66 corrective rereview as separate measurements.
- Keep replay-qualified and release-qualified false; forbid automatic gold promotion.
- Preserve appeals, holds, dissent, limitations, Psalm failure/repair history, and Job as a detailed held example.
- Treat the Sol mesh as one correlated model voice and distinguish formal packs, campaign roles, evidence identities, and aliases.
- Defer M7/M8 comparison until a separately frozen M8 publication exists and Lowell authorizes comparison.

## Validation run

- `python scripts/validate_candidate_publication.py`: passed; 279 immutable pointers, zero embedded bytes.
- `python -m pytest -q tests/test_candidate_publication.py`: 13 passed after fail-closed canonical-set, contract, coverage, membership, and hash-envelope hardening.
- Deterministic package rebuild/check: passed; archive SHA-256 `a88e5a5aeeba8941bbeddb9e4b1d86caa93caf63ad56a853c27e038ee4c75e1a`.
- `python scripts/validate_all.py`: passed on the final postflight state after source-independent validator hardening.
- `python -m pytest -q`: 1,123 passed, 55 skipped in 409.28s on the same final code state.
- Workspace validator: passed; M8 remained protected at its registered active delta.
- Exact changed-file privacy/secret scan: no actual personal path, email, token, or key; deny-list examples only.
- Codex Security diff scan `72a8146d-97e2-49b3-b17c-d9febcf22b85`: complete, 9/9 source/config review items, zero findings. That formal receipt predates the source-independent validator hardening; the independent frozen-diff checker reviewed those exact validation-only code changes, and 13 focused tests passed.
- Independent release checker: PASS; decomposition grade A- with an explicit upgrade condition to A after final postflight and current-state aggregate replay, both now satisfied. Draft PR and the exact metadata-only draft release are allowed. Merge, final release, payload publication, and M7/M8 convergence remain blocked.

## Known risks

- The broad repo privacy scanner remains `blocked_candidate` on legacy baseline paths; this is why M7 payload publication is held.
- The source snapshot contains personal paths, duplicates, and mixed-rights material outside the metadata package.
- Corrective rereview is incomplete at 22/66, Psalm retains 36 active holds/appeals, and the Sol mesh is correlated rather than provider-independent.
- TAC status could not be verified because the Codex Security Access connector was not connected.

## Open questions

- Lowell retains PR merge and final-release authority.
- File-level provenance clearance is required before any M7 payload asset can be published.
- M8 comparison and convergence remain deferred.

## Next agent instruction

After the draft PR and metadata-only draft release are published, Lowell reviews the exact head and artifacts. Do not merge, publish a final release or M7 payload, or begin M7/M8 comparison without the separate required approvals and M8 freeze.

---

## Handoff refresh: final

- agent_name: Codex root
- mode: build
- updated_at: 2026-08-19T02:29:03+00:00
- handoff_id: fa93ba96e82e0ff8
