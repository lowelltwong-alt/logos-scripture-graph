# Task Handoff

## Task

- task_id: T564
- title: Publish and merge bounded M7_sol 22-book backup checkpoint
- phase: governed publication
- status: in_progress

## Agent

- agent_name: Codex-M7-sol-publication
- mode: candidate-only, non-authorizing, governed PR lifecycle
- stage: start
- updated_at: 2026-07-30

## Files read

- `AI_FRONT_DOOR.md`, `.ai/control/MASTER_CONTEXT.md`, `.ai/control/PROJECT_STATUS.md`, repository `AGENTS.md`
- M7_sol model manifest, T544-T563 handoffs, local WEB/OSHB/UXLC source manifests
- DAD, peer-review routing, PR publication, and merge-gate policies

## Files changed

- `.ai/scratch/multi_model_bible_chunking/M7_sol/CHECKPOINT_SCOPE_2026-07-30.md` on the remote checkpoint branch
- this handoff

## Decisions made

- User explicitly authorized `push and merge`.
- Publication is limited to the 22 completed corrective books through Job.
- Ecclesiastes/WIP, global aggregates, T550, caches/temp, sibling maps, comparison/T417, and unrelated work remain excluded.
- Candidate-only publication is a backup checkpoint, not campaign completion or promotion.

## Validation performed

- Independent scope review: conditional pass for the bounded checkpoint.
- Independent size/privacy/license review: conditional pass; no high-confidence secrets; no file in the proposed corpus exceeds 50 MiB.
- Local source manifests confirm WEB public-domain/trademark notice, OSHB CC BY 4.0 attribution and redistribution, and UXLC attribution and copying terms.

## Risks introduced

- The checkpoint intentionally omits global aggregates and is not a self-contained whole-Bible replay bundle.
- The local workspace/index cannot be mutated safely; publication is being built with an isolated temporary Git index/object store.

## Unresolved questions

- Final staged-set validation, commit push, PR checks, and unchanged-head merge gate remain pending.

## Exact next action

Build the exact isolated index from the declared allowlist, validate its paths/content, push the checked commit, update this handoff to final evidence, create the PR, and merge only the unchanged approved head.
