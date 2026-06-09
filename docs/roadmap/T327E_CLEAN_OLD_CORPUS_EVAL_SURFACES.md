# T327E Clean Old-Corpus Eval Surfaces

## Status

- Task: T327E
- Mode: cleanup
- Status: complete
- Branch: `t327e-clean-old-corpus-eval-surfaces`
- Raw mutation: none
- Canonical passage/witness mutation: none
- Chunk regeneration: none
- Evaluator formula change: none
- Chunking algorithm change: none
- T327F/G: not started

## Summary

T327E cleans residual pre-T327 wider-corpus references from evaluation and governance surfaces after
the canonical 66-book reset. This is corpus-scope correction / baseline cleanup, not chunking
improvement.

## Search Inventory

Search covered `eval/chunking_gold`, `docs`, `.ai`, `tests`, `pipelines`, `config`, and `scripts`
for:

| Term | Matches |
| --- | ---: |
| `PrMan` | 51 |
| `Ps151` | 53 |
| `Tob` | 31 |
| `Jdt` | 20 |
| `AddEsth` | 23 |
| `Wis` | 35 |
| `Sir` | 27 |
| `Bar` | 28 |
| `1Macc` | 19 |
| `2Macc` | 19 |
| `1Esd` | 20 |
| `2Esd` | 25 |
| `3Macc` | 19 |
| `4Macc` | 19 |
| `AddDan` | 24 |
| `81` | 37 |
| `38,058` | 27 |
| `38058` | 7 |
| `6,955` | 8 |
| `6955` | 0 |
| `apocrypha` | 52 |
| `deuterocanonical` | 120 |
| `non-66` | 36 |
| `wider corpus` | 5 |

Counts include historical audit files, exclusion validators, old handoffs, and false positives such
as ordinary words containing `Wis` and token counts containing `781`.

## Classification Summary

| Category | Count/group | Disposition |
| --- | --- | --- |
| ACTIVE_CONTROL_TO_REMOVE | 2 surfaces | Updated Psalm candidate skill metadata/docs so active non-target controls are canonical-only `Song` and `Lam`. |
| STALE_BASELINE_TO_UPDATE | 4 surfaces | Updated stress atlas and observed audit JSON/Markdown baseline wording to post-T327 canonical-66 baseline. |
| HISTORICAL_AUDIT_TO_KEEP | T327A/T327B/T327C docs, old handoffs, patch inventories, source inventories, older design notes | Preserved as provenance and audit evidence. |
| EXCLUSION_TEST_TO_KEEP | Canonical 66 config, validator script, T327A/T327B tests | Preserved because they assert non-66 material stays excluded. |
| BOUNDARY_ROUTING_POLICY_TO_KEEP | Boundary routing/governance policy references | Preserved because they route noncanonical material away from canonical Scripture outputs. |
| UNCLEAR_REVIEW | 0 | No unclear live canonical controls remained after cleanup. |

## Updated Surfaces

### Stress Atlas

- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`

Updated baseline wording from the pre-T327 93.5 row to the post-T327 canonical-66 93.6 baseline.
The prior 93.5 row remains provenance only.

### Observed Stress Audit

- `eval/chunking_gold/stress_atlas/observed_stress_behavior.json`
- `eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`

Marked the T318 observed audit as a historical pre-T327 wider-corpus observation. The row data was
not regenerated. It remains diagnostic triage evidence only and must be refreshed before future
output-changing work cites current post-T327 behavior.

### Psalm Candidate Skill Governance

- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL.md`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL_METADATA.json`

Removed `PrMan` and `Ps151` from active canonical non-target controls. Preserved `Song` and `Lam`
as canonical non-target controls. Updated score provenance to the post-T327 canonical-66 baseline.
No algorithm or runtime skill behavior changed.

## Intentionally Preserved

T327E intentionally preserves:

- T327A forensic audit references to the prior 81-book / 38,058-record wider corpus;
- T327B/T327B.1 excluded-book allow-list and fail-closed validator references;
- tests that assert excluded material remains excluded;
- raw source inventories documenting the original WEB archive;
- historical handoffs and agent-design notes;
- boundary routing and contamination-control policy;
- score provenance explaining old evaluator and pre/post corpus baselines.

## Non-66 Status

`PrMan`, `Ps151`, and other non-66 material remain excluded from live canonical controls. Remaining
mentions are historical audit/provenance, exclusion tests/config, boundary-policy routing, or
explicit "do not reintroduce" cleanup language.

## Scope Boundary

T327E did not:

- mutate `data/raw/**`;
- mutate canonical passage/witness outputs;
- regenerate chunks;
- change the chunking algorithm;
- change evaluator formula;
- change leaderboard scoring logic;
- import texts;
- move excluded material to `logos-boundary-literature`;
- start T327F/G.

## Follow-Up

T327F remains boundary-source intake planning only. It must not import or move boundary texts without
separate source/license review and explicit authorization.
