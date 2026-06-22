# T386 Bible-Wide Verse/Passage Coverage Audit

## Scope

T386 adds non-output-changing coverage surfaces before new chunk-output work resumes. It accounts
for all canonical 66-book passage records and records review, owner-decision, and blocked-authority
needs.

## Primary Artifacts

- `.ai/control/bible_verse_passage_coverage_inventory.jsonl`
- `.ai/control/bible_verse_passage_coverage_taxonomy.yaml`
- `.ai/control/bible_verse_passage_coverage_summary.yaml`
- `.ai/control/bible_verse_passage_readiness_matrix.yaml`
- `.ai/control/bible_verse_passage_gap_register.yaml`
- `.ai/control/bible_verse_passage_human_review_docket.yaml`
- `scripts/validate_bible_verse_passage_coverage_inventory.py`
- `tests/test_bible_verse_passage_coverage_inventory.py`
- `.ai/control/test_runtime_preflight.yaml`
- `scripts/validate_test_runtime_preflight.py`

## Audit Claims

- Every canonical passage record must appear exactly once in the inventory.
- Missing, duplicate, noncanonical, or mismatched passage coverage must fail validation.
- The summary, readiness matrix, and gap register must match the inventory hash and counts.
- The human-review docket must list T386-HDM-001 through T386-HDM-008 with faithful options,
  repercussions, recommendations, and stop conditions.
- The decision register records `CD-062`.
- The lesson index records `LSN-014`.
- The test-runtime preflight records `LSN-015` and `WORKFLOW-LESSON-010`, including that
  `python -m pytest -q` can exceed the default 5-minute tool timeout and should be run with at
  least `600000` ms or split/focused strategy plus a full-suite rerun.
- The next non-output step remains T385 using both T384 and T386 inputs.

## Non-Authorizations

T386 does not authorize target selection, reviewed-gold promotion, child spans, chunk output,
route/evaluator behavior, graph edges, retrieval truth, embedding/vector work, boundary import,
preferred reading or source-tradition selection, canon-scope change, whole-Bible output, or
denominational systematic theology as chunk authority.

## Validation

Required commands:

```bash
python scripts/validate_bible_verse_passage_coverage_inventory.py
python scripts/validate_test_runtime_preflight.py
python scripts/validate_task_scope.py --task-id T386
python scripts/agent/validate_handoffs.py
python scripts/validate_all.py
python -m pytest -q  # use at least 600000 ms timeout in this worktree
```
