# Chunking Skill Supply Chain

## Status

- Status: Living / provisional
- Owner: T310/T311 chunking workstream
- Export status: Not ready for LawFirm OS final export
- Last reviewed: 2026-06-07
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
  and initially left Ps.78 as characterization-only pending human review.
- Human review then approved Psalm 78's current child chunks as a structural split under a parent
  whole-psalm literary unit.
- T314 preserved raw Psalm-fragmentation diagnostics while excluding exact manifest-reviewed
  structural splits from the final bad-fragmentation penalty.
- T315 added semantic validation for per-form gold manifests so maturity labels and approved
  structural split metadata fail closed before output-changing work can cite them.

Unknown or unfinished:

- Any true Psalm quality improvement still depends on reviewed target-boundary evidence beyond the
  now-reviewed Psalm 78 parent/child structural split.
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
6. T310 Ps.78 human decision: preserve current child boundaries as a reviewed structural split under
   the parent whole-psalm unit.
7. T314 evaluator-policy correction: report `literal_psalms_fragmented_raw`, report
   `reviewed_structural_splits`, and exclude exact reviewed structural splits from final
   `literal_psalms_fragmented`.
8. Pending true Psalm improvement after reviewed target-form boundary evidence identifies a new
   output-changing target.
9. Later form skills, per-form gold sets, staleness enforcement, promotion, and export.

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
9. Validate gold manifest maturity before relying on it for evaluator or output-changing work.
10. When both whole-unit unity and internal structure matter, model parent literary units plus child
   structural chunks instead of forcing a merge-or-fragmentation binary.
11. Sanity-check the evaluator against target-form evidence.
12. If the evaluator is confounded, fix it in a separate evaluator PR and re-baseline before any
   score-moving skill attempt.
13. Attempt one narrow improvement only after executable/reviewed gold covers the target behavior and
   non-target controls.
14. Promote only if target-form output evidence beats fallback without regressions.
15. Record provenance, route ledger, and staleness triggers.
16. Update this methodology.
17. Repeat for next form.

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
- `python scripts/validate_chunking_gold.py` is included in `validate_all.py` when per-form gold
  manifests are present.
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
- Reviewed structural split is not bad fragmentation by default. Psalm 119 is the strong precedent;
  Psalm 78 is now a reviewed lighter case.
- Evaluator policy may exclude exact manifest-reviewed structural splits from the final
  bad-fragmentation penalty only while preserving raw diagnostics.
- Weak evaluator levers must not drive implementation by themselves. Example: merging Ps.78 offered
  only +0.5 composite upside and was rejected as metric-chasing after human review.
- Human-gated boundary decisions must stay `pending_human_review` until explicitly reviewed.
- Evaluator fixes must land in separate PRs from skill extraction or skill-improvement PRs.
- Corrected evaluator scores must be labeled as score-surface corrections, not chunk-output
  improvements.
- Hard gates remain: 0 USFM leaks, 0 book crossings, prose sentence integrity, no orphan Psalm
  superscriptions, and Psalm 23 as one whole-psalm chunk.

The pre-T311 recorded 88.5 score was an old-evaluator baseline, not final quality. After T311, the
unchanged D / Claude pass2 output scores 93.0 under the corrected evaluator. That is an evaluator
correction, not evidence that the chunker improved.

After T314, the same unchanged output scores 93.5 because the evaluator keeps
`literal_psalms_fragmented_raw=1`, records Ps.78 in `reviewed_structural_splits`, and excludes that
exact reviewed structural split from final `literal_psalms_fragmented`. That is also
evaluator-policy correction, not chunk-output improvement.

## 8. What is still incomplete

- T310 methodology is not complete.
- Current corrected policy baseline is D / Claude pass2 = 93.5 under T314. The T311 93.0 score
  remains provenance for the same unchanged output, not final quality.
- Increment 1 and 2 were intentionally non-scoring.
- Increment 3a is behavior-preserving extraction, not quality improvement.
- T310 3b-gold added executable Psalm gates for settled cases but did not change output.
- A true score-moving skill still needs target-form output evidence after evaluator sanity checks.
- Psalm 78 is now reviewed as a parent whole-psalm unit with child structural chunks; it does not
  authorize an output-changing merge.
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
route controls now have executable gold gates. Ps.78 has moved from characterization-only to
approved structural split under a parent whole-psalm unit.

## 10b. Parent whole-unit plus child structural chunks

Long structured text can require both a parent whole-unit claim and child retrieval chunks. When
literary unity and internal structure both matter, prefer an explicit parent/child model over a
forced binary of "one chunk" versus "bad fragmentation."

Rules:

- Parent whole-unit + child structural chunks is the preferred model for long structured text when
  both unity and internal structure matter.
- Reviewed structural split is not the same as bad fragmentation.
- Psalm 119 is the strong precedent: a parent whole Psalm with 22 reviewed acrostic/stanza child
  chunks.
- Psalm 78 is now a reviewed lighter case: a parent whole Psalm with child chunks `Ps.78.1-69`,
  `Ps.78.70-71`, and `Ps.78.72`.
- Similar future cases should be reviewed through gold before evaluator or chunker changes.
- If the current evaluator still counts a reviewed structural split as fragmentation, handle that in
  a separate evaluator-policy PR; do not use it to justify an output change.
- T314 is the reference implementation: exact reviewed child-boundary match required; missing,
  malformed, or under-specified gold falls back to raw counting and excludes nothing.

## 10c. Future lane categorization rule

When roadmap work identifies a future lane adjacent to chunking, categorize it before implementation
or promotion work begins. Use one primary lane:

- chunking
- evaluator
- entity layer
- concept graph
- retrieval/rendering
- methodology
- external export

This prevents roadmap notes from smuggling output-changing chunking work, evaluator changes, graph
schema work, retrieval contracts, and export doctrine into one ambiguous task. If a future task spans
multiple lanes, name the primary lane and the deferred lanes in the handoff before editing runtime or
schema files.

## 10d. Gold manifest validation rule

T315 added a lightweight semantic validator for per-form gold manifests:
`scripts/validate_chunking_gold.py`.

Rules:

- Reviewed cases must carry an explicit status.
- Cases under `reviewed_gold` may be `reviewed_gold` or
  `approved_structural_split_under_parent_whole_psalm`; characterization-only and
  pending-human-review cases cannot live there.
- Characterization-only and pending-human-review cases must not carry promoted-output flags such as
  `reviewed_structural_split`, `not_bad_fragmentation_gold`, or `authorizes_output_change`.
- Approved parent/child structural split cases must include a parent literary unit, non-empty child
  boundaries, `reviewed_structural_split: true`, and `not_bad_fragmentation_gold: true`.

This is a maturity/metadata gate only. It does not change chunk output, evaluator formula, or review
status by itself.

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
- A reviewed parent/child structural split is treated as bad fragmentation without a separate
  evaluator-policy review.
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
- 2026-06-06: Added the future lane categorization rule for post-3b roadmap work. New lanes must be
  categorized as chunking, evaluator, entity layer, concept graph, retrieval/rendering, methodology,
  or external export before implementation or promotion work begins.
- 2026-06-06: Added the Psalm 78 parent/child structural-split lesson. Reviewed structural splits are
  not bad fragmentation by default; Psalm 119 is the strong precedent and Psalm 78 is now a reviewed
  lighter case.
- 2026-06-06: Added the T314 evaluator-policy lesson. Raw literal Psalm fragmentation diagnostics
  remain visible, while exact manifest-reviewed structural splits can be excluded from final bad
  fragmentation without changing chunk output or claiming chunking improvement.
- 2026-06-07: Added the T315 gold manifest validation lesson. Per-form gold manifests now have a
  semantic validation gate for maturity labels and approved structural split metadata.
