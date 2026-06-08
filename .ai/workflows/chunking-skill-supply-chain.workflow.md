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
- Classify gold artifacts by maturity: scaffold/plan, executable reviewed gold,
  characterization-only evidence, pending human review, or approved structural split under a parent
  whole unit.
- If using a stress-atlas observed behavior audit, classify it as diagnostic triage only. It is not
  reviewed gold, not a review-packet decision, and not implementation authorization.

## Plan

- State the exact increment and whether it is non-scoring, behavior-preserving, evaluator-only, or a
  true improvement attempt.
- Identify baseline evidence: hashes, scorecard, route ledger, evaluator-risk note, and fallback.
- Before any score-moving skill, verify that the evaluator is not measuring a confounded proxy.
- If the evaluator is wrong, plan a separate evaluator PR before any skill-improvement PR.
- Before any output-changing skill work, cite the per-form gold file or manifest under
  `eval/chunking_gold/`.
- Confirm that cited gold is executable/reviewed for the target behavior. A scaffold or
  characterization-only record is enough for analysis, not for output-changing implementation.
- For reviewed whole-unit preservation cases, confirm the human decision explicitly approves the
  current behavior and does not merely characterize it.
- Confirm the cited per-form gold manifest passes semantic maturity validation.
- If a target is characterization-only, state the human-gated decision that remains pending.
- If a target is a reviewed structural split, record the parent whole unit and child boundaries and
  do not treat it as bad fragmentation without a separate evaluator-policy review.
- Treat weak evaluator levers as planning signals only until target-form evidence supports an
  implementation.
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
- For gold-only increments, convert settled cases into executable checks and keep unresolved cases
  characterization-only. Do not change chunk output as part of gold conversion.
- For long structured text, prefer parent whole-unit + child structural chunks when review confirms
  both unity and internal structure. Psalm 119 is the strong precedent; Psalm 78 is now a reviewed
  lighter case.

## Verify

- Run focused tests for the touched surface.
- Run `python scripts/validate_all.py`.
- Run `python -m pytest -q`.
- For behavior-preserving work, prove byte identity against the baseline.
- For evaluator work, document before/after score meaning.
- For reviewed-structural-split evaluator work, preserve raw diagnostics, require exact reviewed
  child-boundary matches, and label score movement as evaluator-policy correction.
- For marker-sensitive packets, confirm `\wj`, `\qs`, paragraph, heading, and punctuation evidence
  are not treated as automatic speaker or boundary authority.
- For token-size policy work, confirm analysis does not authorize retuning unless reviewed target
  gold and policy alignment are present.
- For observed stress behavior audits, confirm every entry remains non-authorizing, every stress
  case is covered, reviewed-current-behavior claims cite existing reviewed gold, and pending packets
  remain pending.
- For true improvements, compare target-form output against fallback and check non-target
  regressions.
- Confirm the cited per-form gold plan or manifest covers the target behavior and non-target
  controls.
- Confirm `python scripts/validate_chunking_gold.py` passes directly or through
  `python scripts/validate_all.py` when manifest semantics are in scope.
- Confirm characterization-only evidence is not asserted as approved expected output.
- Confirm pending human-review decisions remain pending in manifests, tests, handoffs, and status.
- Confirm reviewed structural splits are locked as parent/child gold, not confused with bad
  fragmentation.
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
- Confirm output-changing skill work cites per-form gold evidence.
- Confirm the cited evidence is executable/reviewed gold, not merely a scaffold or
  characterization-only record.
- Confirm weak evaluator levers did not drive implementation without target-form output evidence.
- Confirm unresolved human-gated boundaries remain explicitly pending.
- Confirm reviewed parent/child structural splits cite gold before evaluator or chunker changes.
- Confirm observed current behavior is not treated as approved expected output.
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
- Stop if output-changing skill work lacks cited executable/reviewed per-form gold.
- Stop if a scaffold or characterization-only record is treated as approved expected output.
- Stop if a weak evaluator lever becomes the sole reason for output-changing implementation.
- Stop if a human-gated boundary decision is resolved without explicit review.
- Stop if a reviewed parent/child structural split is treated as bad fragmentation without a
  separate evaluator-policy review.
- Stop if an observed stress behavior entry is treated as reviewed gold or used to authorize
  output-changing work.
- Stop if methodology was not reviewed.
