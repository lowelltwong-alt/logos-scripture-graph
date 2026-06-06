# Chunking Skill Supply Chain

## Status

- Status: Living / provisional
- Owner: T310/T311 chunking workstream
- Export status: Not ready for LawFirm OS final export
- Last reviewed: 2026-06-06
- Must update when:
  - chunking algorithm changes
  - form detector changes
  - orchestrator routing changes
  - skill registry changes
  - evaluator/leaderboard changes
  - gold sets change
  - promotion/staleness logic changes
  - route ledger changes

## 1. Purpose

This artifact records the working methodology for turning the current chunker into a governed
Chunking Skill Supply Chain. It exists so future agents can preserve the evidence trail while the
system evolves from a monolith, to a form detector, to a byte-identical orchestrator, to
per-form skills with gold-backed promotion.

The methodology is a workflow record, not final doctrine. It should be revised as the T310/T311
workstream learns which skill boundaries, evaluator fixes, and promotion rules actually hold up.

IMPORTANT: before optimizing a skill, verify that the evaluator is not measuring a confounded
proxy. If an evaluator signal is wrong, fix the evaluator in a separate PR before claiming skill
improvement.

## 2. Why this is a living artifact

The chunking system is still being extracted and tested. A static design document would hide the
critical uncertainty: the current supply chain is partly implemented, partly behavior-preserving,
and partly blocked on evaluator trust.

Confirmed:

- Increment 0 established the registry stub, form taxonomy, lifecycle policy, and monolith wrapper.
- Increment 1 added a read-only candidate textual-form detector.
- Increment 2 added a byte-identical orchestrator shim and route ledger.
- Increment 3a added a behavior-preserving Psalm skill extraction seam.
- T311 fixed the `psalms_fragmented` evaluator grouping from bare chapter to `(book, chapter)`.
- Increment 3b-gold converted the Psalm scaffold into executable tests/manifest for settled cases
  while leaving Ps.78 as characterization-only pending human review.

Unknown or unfinished:

- Any true Psalm quality improvement still depends on reviewed target-boundary evidence, especially
  the unresolved Ps.78 merge-vs-preserve-`\b` decision.
- Later increments still need more skills, per-form gold sets, staleness enforcement, promotion
  rules, and final export.

## 3. Current known increments

0. Registry stub / form taxonomy / monolith wrapper.
1. Candidate textual-form detector.
2. Byte-identical orchestrator shim plus route ledger.
3. Behavior-preserving Psalm skill extraction.
4. T311 evaluator correction for `psalms_fragmented`: group by `(book, chapter)`, report literal
   Psalm fragmentation separately from broader poetry-book fragmentation, and expose Psalm 119
   sectioning as a non-penalty signal.
5. T310 3b-gold conversion: executable Psalm gold manifest/tests for settled cases; Ps.78 captured
   as characterization-only, not approved expected output.
6. Pending true Psalm improvement after reviewed target-form boundary evidence is trustworthy.
7. Later form skills, per-form gold sets, staleness enforcement, promotion, and export.

Increment 1 and Increment 2 were intentionally non-scoring. Increment 3a is behavior-preserving
extraction, not a quality improvement. T311 changed the evaluator surface, not chunk output. T310
3b-gold added gold gates, not chunk-output improvement. The T310 methodology is not complete.

## 4. Core principle

Protect raw and canonical source truth, then improve derived chunking only through reversible,
evidence-backed steps. Detect textual form as candidate metadata, route through explicit skills,
prove byte identity before claiming extraction success, and promote only when trusted evaluation
beats the fallback without regressions.

No skill, detector, route, or evaluator patch may rewrite raw source text, mutate canonical records,
or treat route metadata as chunk/context content.

## 5. Current workflow algorithm

0. Protect raw/canonical source.
1. Establish trusted baseline.
2. Capture baseline hashes and scorecard.
3. Detect text form as candidate metadata.
4. Build skill registry / TOC / graph.
5. Add byte-identical orchestrator shim.
6. Extract candidate skill without changing output.
7. Add per-form gold/eval anchors and label their maturity: scaffold, reviewed executable gold,
   characterization-only, or pending human review.
8. Promote only settled cases into executable/reviewed gold. Keep characterization-only evidence out
   of approved expected-output assertions.
9. Sanity-check the evaluator against target-form evidence.
10. If the evaluator is confounded, fix it in a separate evaluator PR and re-baseline before any
   score-moving skill attempt.
11. Attempt one narrow improvement only after executable/reviewed gold covers the target behavior and
   non-target controls.
12. Promote only if target-form output evidence beats fallback without regressions.
13. Record provenance, route ledger, and staleness triggers.
14. Update this methodology.
15. Repeat for next form.

## 6. Required artifacts

- Raw and canonical protection references: `.ai/control/RAW_SOURCE_INVENTORY.md`,
  `config/ingest/usfm_marker_coverage.yaml`, source manifests, and validation outputs.
- Baseline evidence: committed scorecards, byte hashes, and leaderboard snapshots when leaderboard
  behavior is intentionally in scope.
- Detector artifacts: `pipelines/chunking/detect_form.py`, emitted candidate ClassificationAssignment
  records, and detector tests.
- Registry artifacts: `config/chunking/form_registry.yaml`,
  `config/chunking/skill_lifecycle_policy.yaml`, `registry/chunking/skill-toc.json`,
  `registry/chunking/skill-graph-index.json`, and `registry/chunking/approved-skills.json`.
- Skill package artifacts: `SKILL.md`, `SKILL_METADATA.json`, algorithm entrypoint, tests, fixtures,
  lifecycle state, handled forms, forbidden actions, and staleness triggers.
- Route artifacts: route ledger, registry surface SHA, input/output/context hashes, selected skill,
  fallback reason, and proof that route facts did not enter chunk/context records.
- Evaluation artifacts: per-form gold plans/manifests with explicit maturity status, executable
  reviewed-gold tests, characterization-only records, scorecards, evaluator-risk notes, regression
  reports, and promotion/rejection rationale.
- Coordination artifacts: task handoff, project status update, PR methodology note, and this
  methodology update or no-change rationale.

## 7. Current gates

- `python scripts/validate_all.py`
- `python -m pytest -q`
- Raw and canonical data remain untouched.
- No runtime behavior change unless the task explicitly targets a behavior-changing increment.
- No evaluator/leaderboard change unless the task explicitly targets evaluator behavior.
- No chunk output change for detector, registry, shim, or behavior-preserving extraction increments.
- Byte-identical proof is required for shims and behavior-preserving extractions.
- Route metadata stays in the route ledger only.
- Before any score-moving skill, prove the evaluator is measuring the target output behavior and not
  a confounded proxy.
- Before any output-changing skill work, cite executable/reviewed per-form gold under
  `eval/chunking_gold/`. A scaffold or characterization-only record can start analysis but cannot
  authorize output changes or promotion.
- Weak evaluator levers must not drive implementation by themselves. Example: Ps.78 offers only
  +0.5 composite upside and remains blocked until target-form boundary evidence is reviewed.
- Human-gated boundary decisions must stay `pending_human_review` until explicitly reviewed.
- Evaluator fixes must land in separate PRs from skill extraction or skill-improvement PRs.
- Corrected evaluator scores must be labeled as score-surface corrections, not chunk-output
  improvements.
- Hard gates remain: 0 USFM leaks, 0 book crossings, prose sentence integrity, no orphan Psalm
  superscriptions, and Psalm 23 as one whole-psalm chunk.

The pre-T311 recorded 88.5 score was an old-evaluator baseline, not final quality. After T311, the
unchanged D / Claude pass2 output scores 93.0 under the corrected evaluator. That is an evaluator
correction, not evidence that the chunker improved.

## 8. What is still incomplete

- T310 methodology is not complete.
- Current corrected baseline is D / Claude pass2 = 93.0 under the T311 evaluator, not final quality.
- Increment 1 and 2 were intentionally non-scoring.
- Increment 3a is behavior-preserving extraction, not quality improvement.
- T310 3b-gold added executable Psalm gates for settled cases but did not change output.
- A true score-moving skill still needs target-form output evidence after evaluator sanity checks.
- Ps.78 still needs a human-gated boundary decision before any output-changing Psalm skill can use it
  as expected-output gold.
- Final LawFirm OS export should wait until at least one true score-moving skill is safely promoted
  or rejected with documented evidence.

## 9. Evaluator sanity rule and T311 lesson

T311 proved that evaluator bugs can masquerade as skill gaps. The old `psalms_fragmented` metric
grouped every `genre == "psalms"` chunk by bare chapter number. That caused cross-book collisions
such as `Ps.3`, `Song.3`, and `Lam.3`, plus related collisions involving poetry-like books.

T311 fixed the evaluator by grouping fragmentation as `(book, chapter)`. It added
`literal_psalms_fragmented`, `poetry_books_fragmented`, and `psalm119_section_chunks`, while keeping
legacy `psalms_fragmented` as an alias for literal Psalm fragmentation. The unchanged D / Claude
pass2 chunk output moved from 88.5 to 93.0 under the corrected evaluator.

Rules:

- Before optimizing a skill, verify that the evaluator is not measuring a confounded proxy.
- If the evaluator is wrong, fix the evaluator in a separate PR before claiming skill improvement.
- A corrected evaluator score is not the same thing as chunk-output improvement.
- A score-moving skill must show target-form output evidence, not only aggregate score movement.
- Output-changing skill work must cite a per-form gold file or manifest before implementation
  proceeds beyond planning.
- Keep evaluator, skill, and methodology workstreams on separate branches/PRs unless a task
  explicitly says otherwise.
- Stop if non-target output drifts during a target-form improvement attempt.

## 10. Promotion rules

A skill may move toward active/preferred only when all of these are true:

- The skill has a valid package, metadata, lifecycle state, tests, and handled-form declaration.
- The target form has a per-form gold anchor or an explicit evaluator-risk analysis.
- The output-changing proposal cites executable/reviewed gold, not merely a scaffold or
  characterization-only record.
- The evaluator signal used for promotion is trusted for that form.
- The skill beats the fallback on the target form without regressing hard gates or non-target output.
- Any evaluator correction needed to trust the score already landed separately.
- The improvement claim is backed by target-form output evidence, not only corrected score movement.
- Byte-identity requirements are satisfied when the increment claims behavior preservation.
- Route ledger evidence shows what routed where and why.
- No route metadata enters chunk/context records.
- Staleness triggers are recorded.
- Human review approves the promotion.
- This methodology is updated or a no-change rationale is documented.

No skill self-promotes. Metric gaming is a failure mode, not a promotion path.

## 10a. Gold maturity rule and T310 3b-gold lesson

T310 3b-gold established a stricter gold maturity ladder:

1. `scaffold` or plan: useful for analysis and task framing, but not promoted gold.
2. `characterization_only`: observed current behavior, evaluator context, and risk evidence. This is
   not an approved expected-output assertion.
3. `pending_human_review`: a decision point that must remain unresolved until explicit review.
4. `reviewed_gold`: settled expected behavior named in a manifest and/or executable tests.

Rules:

- Gold scaffold is not promoted gold.
- Characterization-only evidence is not the same as approved expected output.
- Output-changing skill work requires executable/reviewed gold first.
- Weak evaluator levers, such as Ps.78's +0.5 composite upside, must not drive implementation
  without target-form evidence.
- Human-gated boundary decisions must remain pending until explicitly reviewed.

For Psalm work, Ps.23, Ps.119, short Psalm holdouts, Ps.3 superscription behavior, and non-target
route controls now have executable gold gates. Ps.78 remains characterization-only pending human
review of whether to merge the Psalm or preserve the `\b` boundary.

## 11. Staleness rules

Re-evaluate affected skills and update this methodology when any of these change:

- raw inventory SHA
- marker coverage
- chunking policy
- form registry
- skill registry / TOC / graph
- approved-skill set
- evaluator or leaderboard logic
- per-form gold set
- route ledger schema/content
- source schema or chunk/context contract
- incumbent skill quality evidence
- age threshold defined by skill metadata or lifecycle policy

Stale skills may remain reproducible, but stale-only routing must not be promoted as preferred.

## 12. Failure modes

- Raw or canonical data is touched.
- A detector emits authoritative form labels instead of candidate metadata.
- A skill PR discovers or depends on an evaluator bug.
- The evaluator appears to measure a confounded proxy.
- Non-target output drifts during an extraction.
- Non-target output drifts during a target-form improvement.
- Route metadata enters chunk or context records.
- Score improves because the metric is gamed or broken.
- Score improves without target-form output evidence.
- Output-changing skill work starts without citing a per-form gold file or manifest.
- A scaffold or characterization-only record is treated as reviewed expected-output gold.
- A weak aggregate evaluator lever drives implementation without target-form evidence.
- A human-gated boundary decision is silently resolved by an agent or metric.
- A skill lacks gold, route-ledger proof, or fallback behavior.
- A methodology update is skipped without rationale.
- LawFirm OS export is treated as final doctrine before the workflow is tested.

## 13. Cross-domain transfer notes

The transferable pattern is a detect-then-route supply chain:

- bounded form taxonomy
- candidate form detection
- explicit skill packages
- registry TOC and graph index
- route ledgers
- per-form gold/evaluator anchors
- staleness triggers
- human-gated promotion

The Bible-specific details, especially USFM markers, Psalm handling, canon profiles, and raw-source
immutability, should not be copied into other domains as universal rules. Cross-domain reuse should
extract the pattern and then rebuild the domain-specific evidence model.

## 14. LawFirm OS export plan

Do not export as final doctrine yet.

Later export should go to LawFirm OS as a generalized "detect-then-route skill supply chain."

Export only after the methodology has been tested through at least:

- one detector increment
- one byte-identical orchestrator shim
- one behavior-preserving skill extraction
- one evaluator correction or evaluator-risk analysis
- one scaffold-to-executable-gold conversion with characterization-only evidence kept separate
- one true improvement attempt or documented rejected attempt
- a documented branch-hygiene pattern that keeps evaluator, skill, and methodology changes separate

The export should identify what is confirmed by T310/T311 evidence, what is inferred from the
Scripture chunking domain, what is proposed for broader use, and what remains unknown.

## 15. Change log

- 2026-06-05: Initial living methodology artifact created for T310/T311. Captures the current
  non-final workflow, evaluator risk, promotion constraints, staleness triggers, and deferred
  LawFirm OS export conditions.
- 2026-06-05: Added the T311 evaluator lesson. Score-moving skills must sanity-check evaluator
  signals first; evaluator fixes are separate PRs; corrected evaluator scores are not chunk-output
  improvement claims.
- 2026-06-06: Added the T310 3b-gold lesson. Gold scaffolds are not promoted gold;
  characterization-only evidence is not approved expected output; output-changing skill work needs
  executable/reviewed gold first; weak evaluator levers cannot drive implementation without
  target-form evidence; human-gated boundary decisions stay pending until reviewed.
