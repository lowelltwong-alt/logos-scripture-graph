# Chunking Skill Creation Playbook

Proprietary chunking methodology: see `pipelines/chunking/LICENSE`.

This playbook is for future authors of chunking skills under the T310/T311 supply chain. It is
operational guidance, not final doctrine. Keep it aligned with
`docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`.

## Naming a Skill

- Use lowercase kebab-case.
- Start with the handled form or narrow form family.
- Add the strategy in plain language.
- End with a version suffix.
- Example: `psalm-whole-then-stanza-v1`.

Use `variant_id` in `SKILL_METADATA.json` for budget profiles, source adapters, or parameterized
behavior. Do not create a new skill id for every parameter choice.

## Lifecycle States

Use the lifecycle states in `config/chunking/skill_lifecycle_policy.yaml`:

- `draft`: author-local and not routable.
- `candidate`: metadata/tests pass and eligible for A/B work, not default.
- `active`: human-approved and routable.
- `preferred`: default when several active skills match.
- `deprecated`: still reproducible but not selected for new runs.
- `superseded`: replaced by a better approved skill.
- `retired`: unavailable except for provenance replay.
- `quarantined`: failed a hard safety or boundary gate.

No skill self-promotes to active or preferred.

## Candidate vs Active/Preferred

Candidate skills may be tested, scored, and recorded in the registry graph. They are not the default
fallback and must not silently replace the monolith or an active skill.

Active/preferred skills require human approval, gold or evaluator-risk evidence, route-ledger proof,
and methodology review. Preferred status means the skill is the normal route for its form, not that
the methodology is final.

## Metadata Requirements

Every skill package must include:

- `SKILL.md`
- `SKILL_METADATA.json`
- algorithm entrypoint when code exists
- stable `id`, `version`, `lifecycle_state`, `role`, and `risk_tier`
- handled forms and overlays
- source profile
- input and output contracts
- required evidence
- forbidden actions
- dependencies
- parameters / `variant_id`
- evaluation references
- relationships
- staleness triggers
- approval policy

Metadata must never grant authority to write `data/raw/` or `data/canonical/`.

## Gold-Set Requirements

A dedicated form skill needs a per-form gold anchor before promotion. If a gold set is not available,
the handoff must explain the gap and keep the skill as candidate or lower.

Before any output-changing skill work, cite the relevant per-form gold file or manifest under
`eval/chunking_gold/`. For Psalm work after T310 3b-gold, start from
`eval/chunking_gold/per_form/psalms_gold_manifest.json` and
`eval/chunking_gold/per_form/psalms_gold_plan.md`.

Gold has maturity states:

- `scaffold` or plan: analysis and task framing only; not promoted gold.
- `characterization_only`: observed current behavior and risk evidence; not approved expected output.
- `pending_human_review`: unresolved boundary or policy decision; do not implement against it.
- `reviewed_gold`: settled expected behavior captured in a manifest and/or executable tests.
- `approved_structural_split_under_parent_whole_psalm`: reviewed parent whole-unit plus child
  structural chunks; not bad fragmentation by default.

Output-changing skill work requires executable/reviewed gold first. A scaffold, plan, or
characterization-only record can support investigation but cannot authorize a behavior change or
skill promotion.

Gold evidence should cover the form's hard cases, not only the easiest passage. Before a skill author
optimizes for any score-moving metric, verify that the evaluator is measuring the intended
target-form output behavior and not a confounded proxy.

Gold manifests must pass semantic maturity validation before they authorize output-changing work.
Run `python scripts/validate_chunking_gold.py` or rely on `python scripts/validate_all.py` after
editing `eval/chunking_gold/per_form/*_manifest.json`.

Weak evaluator levers must not drive implementation without target-form evidence. Psalm 78 is the
reference case: eliminating its current fragmentation was only a +0.5 composite lever, and human
review approved preserving the current child boundaries under a parent whole-psalm unit.

Parent whole-unit + child structural chunks is the preferred model for long structured text when
both unity and internal structure matter. Psalm 119 is the strong precedent; Psalm 78 is now a
reviewed lighter case. Similar future cases should be reviewed through gold before evaluator or
chunker changes.

T314 lesson: evaluator policy can exclude exact manifest-reviewed structural splits from final bad
fragmentation only while preserving raw diagnostics such as `literal_psalms_fragmented_raw` and
`reviewed_structural_splits`. Score movement from that exclusion is evaluator-policy correction, not
chunking improvement.

T317 lesson: reviewed gold can also approve preserving a current whole-unit behavior. Psalm 105 and
Psalm 106 are reviewed whole-psalm cases, not structural splits; Psalm 106 `\b` markers are evidence
but not automatic split authority. Words-of-Jesus packets such as John 3 and Matthew 5-7 remain
pending until human speaker-boundary review. Token-size analysis is not authorization to retune
chunking.

T311 lesson: the old `psalms_fragmented` metric grouped Psalm-like chunks by bare chapter number,
causing cross-book collisions such as `Ps.3`, `Song.3`, and `Lam.3`. The same chunk output moved
from 88.5 to 93.0 after T311 fixed grouping to `(book, chapter)`. That was evaluator correction,
not skill improvement.

If a score target is wrong, stop and fix the evaluator in a separate PR before claiming a skill
improvement.

## Route-Ledger Requirements

Route ledgers must record:

- route mode
- selected skill id and lifecycle state
- fallback reason, if any
- registry surface SHA
- input, output, and context hashes where applicable
- route unit identifiers
- whether detector output was consumed
- whether form-based routing was enabled

Route facts belong in the route ledger only. They must not be added to chunk or context records.

## Byte-Identity Requirements

Registry, detector, shim, and behavior-preserving extraction increments must not change chunk/context
outputs. Prove byte identity by comparing direct chunker output to orchestrated or extracted output.

If byte identity fails, stop and identify the drift before continuing. Do not hide drift behind a
leaderboard score.

## Fallback Behavior

Every skill route must have an explicit fallback:

- normal fallback: `monolith-pass2-v1`
- declared-gap fallback: monolith if the form is biblical and currently covered only by interim logic
- no fallback: alert/gap record when a form is genuinely unhandled

Fallback use should be visible in the route ledger and handoff.

## Promotion Criteria

A skill can be promoted only when:

- package metadata is complete
- tests and validation gates pass
- target-form gold or evaluator-risk evidence is present
- output-changing work cites a per-form gold file or manifest
- cited gold is executable/reviewed for the target behavior, not merely scaffold or
  characterization-only evidence
- evaluator signals are trustworthy for the claim
- any evaluator fix needed to trust the claim has already landed separately
- fallback is beaten without non-target regressions
- score movement is backed by target-form output evidence
- hard gates pass
- route-ledger evidence is recorded
- staleness triggers are recorded
- human review approves the promotion
- human-gated boundary decisions have been explicitly reviewed
- reviewed structural splits are not treated as bad fragmentation without a separate
  evaluator-policy review
- the methodology is updated or reviewed with a no-change rationale

Corrected evaluator score movement is not a chunk-output improvement claim. Record it as evaluator
surface correction and re-baseline before the next skill attempt.

## Staleness Triggers

Re-evaluate and review affected skills when any of these change:

- raw inventory SHA
- marker coverage
- chunking policy
- form detector
- form registry
- skill registry / TOC / graph
- approved-skill set
- evaluator/leaderboard logic
- per-form gold set
- route ledger
- schema or output contract
- fallback or incumbent score evidence

## Required Methodology Update

Any chunking-related skill work must update
`docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md` or document why no update is needed.

Use one of these PR notes:

- `Methodology updated: yes`
- `Methodology reviewed: no change required - <rationale>`

Keep evaluator fixes, skill changes, and methodology updates in separate branches or PRs unless the
task explicitly calls for a combined patch.
