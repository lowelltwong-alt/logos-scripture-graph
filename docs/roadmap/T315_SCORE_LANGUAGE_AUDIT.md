# T315 Score-Language Audit

Status: T315 governance audit after PR #15 / T314 merge.

Official interpretation:

- Same unchanged D / Claude pass2 output scored 88.5 under the old evaluator.
- Same unchanged D / Claude pass2 output scored 93.0 under T311.
- Same unchanged D / Claude pass2 output scores 93.5 under T314.
- T311 and T314 are evaluator-surface or evaluator-policy corrections, not chunking improvement.

## Confirmed Current Baseline References

| Source | Classification | Action |
| --- | --- | --- |
| `eval/LEADERBOARD.md` | Current T314 baseline reference. | Preserved. |
| `eval/chunking_gold/README.md` | Current T314 baseline reference. | Updated with validator note. |
| `eval/chunking_gold/per_form/psalms_gold_plan.md` | Current T314 baseline reference. | Preserved. |
| `eval/chunking_gold/per_form/psalms_gold_manifest.json` | Current T314 baseline and provenance. | Preserved. |
| `eval/chunking_runs/*.json` | Current scorecard metrics and provenance. | Preserved. |

## Confirmed Old-Evaluator Provenance

| Source | Classification | Action |
| --- | --- | --- |
| `docs/architecture/ADR-0011-chunking-orchestrator-skill-registry.md` | Post-T311/T314 provenance note plus historical build context. | Updated prose to name 93.5 as current T314 policy baseline while retaining 88.5 and 93.0 provenance. |
| `.ai/handoffs/T310/handoff.md` | Historical handoff log. | Historical sections preserved; T315 section appended. |
| `.ai/control/roadmap_events.jsonl` | Historical immutable event log. | Preserved. |

## Confirmed T311 Provenance

| Source | Classification | Action |
| --- | --- | --- |
| `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md` | T311 lesson and T314 follow-up. | Updated stale "current corrected baseline" wording to current T314 baseline plus T311 provenance. |
| `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md` | T311/T314 skill-author guidance. | Updated with T315 manifest-validation instruction. |
| `.ai/workflows/chunking-skill-supply-chain.workflow.md` | Workflow guidance. | Updated with T315 manifest-validation checks. |

## Confirmed T314 Policy References

| Source | Classification | Action |
| --- | --- | --- |
| `pipelines/chunking/evaluate_chunks.py` | T314 evaluator policy implementation. | No change; protected from policy churn in T315. |
| `pipelines/chunking/leaderboard.py` | T314 display/provenance behavior. | No change; formula/policy preserved. |
| `tests/test_evaluate_chunks.py` | T314 evaluator policy tests. | No change except separate validator tests added. |
| `tests/test_chunker_gold.py` | Executable gold plus T314 diagnostics. | No behavior change. |

## Misleading Or Stale References Updated

| Source | Issue | Action |
| --- | --- | --- |
| `docs/roadmap/T313_TOKEN_SIZE_EVALUATOR_POLICY_ALIGNMENT.md` | Called 93.0 the current corrected baseline and listed pre-T314 `literal_psalms_fragmented=1` as current final metric. | Updated to T314 current baseline 93.5 with raw/reviewed/final Psalm fragmentation split. |
| `docs/architecture/ADR-0011-chunking-orchestrator-skill-registry.md` | Described 93.0 as the current corrected baseline after T311. | Updated to preserve T311 provenance while naming 93.5 as current T314 policy baseline. |
| `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md` | One incomplete-work bullet still named 93.0 as current corrected baseline. | Updated to T314 current baseline language. |

## Deferred Score-Metadata Reconciliation

The following surfaces still contain 93.0 as T311 skill/registry quality provenance:

- `registry/chunking/approved-skills.json`
- `registry/chunking/skill-graph-index.json`
- `pipelines/chunking/skills/approved/monolith-pass2-v1/SKILL.md`
- `pipelines/chunking/skills/approved/monolith-pass2-v1/SKILL_METADATA.json`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL_METADATA.json`

T315 leaves those untouched because they are skill/registry metadata surfaces, and changing them could
look like skill promotion or quality rebasing rather than documentation hardening. A future explicit
score-metadata reconciliation task can update them if the owner wants T314 to become the registry
quality score of record.

## Historical Immutable Logs

The following should not be rewritten for score-language cleanup:

- `.ai/control/roadmap_events.jsonl`
- historical sections inside `.ai/handoffs/T310/handoff.md`
- previous PR merge commits and commit messages

## Unknown

- Whether active skill metadata should be rebased from T311 93.0 to T314 93.5.
- Whether leaderboard provenance should get a machine-readable evaluator-version registry.
