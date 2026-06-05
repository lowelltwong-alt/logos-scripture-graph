# Chunking Skill Supply Chain Workflow

AI-operational checklist for chunking-related work. Use with
`.ai/control/METHODOLOGY_UPDATE_RULES.md` and
`docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`.

## Explore

- Read `AI_FRONT_DOOR.md`, `.ai/control/MASTER_CONTEXT.md`, `.ai/control/PROJECT_STATUS.md`,
  `.ai/control/DATA_MAP.md`, `.ai/control/RAW_SOURCE_INVENTORY.md`, and the active handoff.
- Read ADR-0011, `docs/chunking/CHUNKING_DESIGN.md`, the relevant skill metadata, registry files,
  evaluator notes, and gold/eval artifacts for the target form.
- Confirm whether the task is detector, registry, orchestrator, skill, evaluator, gold, staleness,
  route-ledger, or methodology work.

## Plan

- State the exact increment and whether it is non-scoring, behavior-preserving, evaluator-only, or a
  true improvement attempt.
- Identify baseline evidence: hashes, scorecard, route ledger, evaluator-risk note, and fallback.
- Before any score-moving skill, verify that the evaluator is not measuring a confounded proxy.
- If the evaluator is wrong, plan a separate evaluator PR before any skill-improvement PR.
- Define target output drift expectations before editing.
- Decide whether the methodology must change or can be reviewed with no change.

## Implement

- Keep raw and canonical data untouched.
- Keep candidate metadata separate from derived chunk/context records.
- Keep route facts in the route ledger.
- Make the narrowest change that satisfies the increment.
- Do not mix evaluator fixes with skill extraction or skill improvement work unless the task scope
  explicitly says to do so.
- Keep evaluator, skill, and methodology workstreams on separate branches unless the task explicitly
  requires a combined branch.

## Verify

- Run focused tests for the touched surface.
- Run `python scripts/validate_all.py`.
- Run `python -m pytest -q`.
- For behavior-preserving work, prove byte identity against the baseline.
- For evaluator work, document before/after score meaning.
- For true improvements, compare target-form output against fallback and check non-target
  regressions.
- Treat corrected evaluator score movement as an evaluator-surface correction, not a chunk-output
  improvement claim.

## Commit

- Include the task id and handoff path.
- Include the required chunking methodology PR note.
- Do not commit generated chunk outputs unless the task explicitly requires committed scorecards or
  review artifacts.

## Review

- Confirm changed files match the task scope.
- Confirm no raw/canonical mutation.
- Confirm route metadata did not enter chunk/context records.
- Confirm evaluator signals are trustworthy for the claim being made.
- Confirm any score movement is supported by target-form output evidence.
- Confirm the handoff names risks, validation, and exact next action.

## Update Methodology

- Update `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md` when the change touches a trigger listed
  in `.ai/control/METHODOLOGY_UPDATE_RULES.md`.
- If no methodology change is needed, document the rationale in the handoff and PR note.

## Export When Mature

- Do not export to LawFirm OS as final doctrine during T310/T311 provisional work.
- Export later only after the workflow has evidence from detector, shim, extraction, evaluator-risk,
  and true improvement or documented rejected-improvement increments.

## Stop Conditions

- Stop if raw/canonical would be touched.
- Stop if evaluator bug is discovered inside a skill PR.
- Stop if the evaluator appears to measure a confounded proxy.
- Stop if non-target output drifts.
- Stop if route metadata enters chunk/context records.
- Stop if score improves by metric gaming.
- Stop if score improves without target-form output evidence.
- Stop if methodology was not reviewed.
