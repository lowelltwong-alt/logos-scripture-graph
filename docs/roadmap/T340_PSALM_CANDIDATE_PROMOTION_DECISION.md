# T340 - Psalm Candidate Promotion Decision

## Status

- Status: complete
- Decision: `hold`
- Subject skill: `psalm-whole-then-stanza-v1`
- Scope: governance/status/metadata decision only

## Stage A Verification

T340 began only after PR #49 / T339 post-merge verification passed.

Confirmed:

- PR #49 state: `MERGED`
- PR #49 merge commit: `bd221478c01314bcd452a7d8fe6ca0dab869a956`
- T339 commit: `fabb268`
- GitHub validate for PR #49: success
- local `main`: clean and fast-forwarded
- no merge/rebase state
- Stage A validation passed:
  - `python scripts/validate_canonical_66_scope.py`
  - `python scripts/qa_canonical_corpus.py`
  - YAML parse checks
  - JSONL parse checks
  - `git diff --check`
  - `python scripts/validate_all.py`
  - `python -m pytest -q`

Protected paths were clean. PR #49 did not touch raw/canonical/derived data, runtime chunking code,
skill code, evaluator formula, leaderboard, scorecards, boundary imports, or Revelation
implementation.

## Evidence Reviewed

T337B:

- Owner approved Psalm 89 Option C as reviewed gold.
- Approval is Psalm 89 only.
- `Ps.89.52` remains inside final child `Ps.89.49-Ps.89.52`.
- No global Selah, blank-line, doxology, poetry, or long-Psalm rule was authorized.

T338:

- Implemented the exact Psalm 89 Option C behavior only in the literal Psalm candidate route.
- Direct monolith chunker output remained unchanged.
- Non-Psalm-89 routed records were preserved.
- Tests enforce exact Psalm 89 spans and no orphan `Ps.89.52`.

T339:

- Same-baseline evaluation confirmed direct chunker bytes unchanged.
- Routed output changed only Psalm 89.
- Routed count moved `1131 -> 1136`, exactly one parent replaced by six reviewed children.
- Non-Psalm-89 routed records were identical.
- Metric movement was documented as Psalm 89 reviewed structural correction only.
- RISK-GATE-001 identified promotion risk, marker-heuristic risk, and broad-improvement overclaim
  risk.

Current skill metadata/registry:

- `psalm-whole-then-stanza-v1` remains `lifecycle_state: candidate`.
- `approved-skills.json` contains only `monolith-pass2-v1`.
- `skill-toc.json` lists `psalm-whole-then-stanza-v1` as a candidate skill for `psalm_whole`.
- `skill-graph-index.json` lists the Psalm skill as candidate.

## Decision

Decision: `hold`.

T337B/T338/T339 provide strong evidence for retaining the exact Psalm 89 Option C behavior behind
the literal Psalm route. They do not yet provide enough evidence to promote
`psalm-whole-then-stanza-v1` as an approved or active Psalm skill.

Reasons:

- The skill has one output-changing reviewed-gold case.
- Existing reviewed Psalm evidence mostly acts as preservation or fail-closed guardrails.
- Promotion could be overread as broad Psalm optimization.
- T339 explicitly warned against hidden global Psalm, marker, and doxology behavior.
- No owner decision in T337B/T338/T339 explicitly approved lifecycle promotion.

## Authorization Scope

T340 authorizes:

- keeping `psalm-whole-then-stanza-v1` as a candidate skill;
- retaining T338's route-isolated Psalm 89 Option C behavior;
- using T337B/T338/T339 evidence in a future promotion review;
- continuing fail-closed reviewed Psalm guardrails.

T340 does not authorize:

- lifecycle promotion to approved or active;
- adding the Psalm skill to `approved-skills.json`;
- moving the skill into `pipelines/chunking/skills/approved/`;
- global Psalm behavior;
- global poetry behavior;
- global Selah behavior;
- global blank-line behavior;
- global doxology behavior;
- long-Psalm rules;
- marker-only boundary authority;
- Psalm 136 changes;
- Psalm 78, 105, 106, or 119 behavior changes;
- evaluator formula changes;
- leaderboard or scorecard changes;
- raw/canonical/derived data mutation;
- boundary import;
- T327G;
- Revelation implementation;
- whole-Bible improvement claims.

## Promotion Requirements Before Reconsideration

A future promotion review should have:

- explicit owner/reviewer approval for limited promotion;
- rerun same-baseline identity checks;
- continued non-Psalm fallback controls for Song and Lamentations;
- no route leakage into non-Psalm books;
- clear language that marker evidence remains subordinate to reviewed gold;
- no leaderboard/scorecard claim unless separately authorized.

## Watch-Later Notes

Stage A observed two cosmetic watch-later items already identified by review:

- `ROADMAP_STATE.yaml` top-level `last_updated` and `current_phase` were stale. T340 refreshes them.
- `.ai/control/handoff_ledger.jsonl` had T339 entries out of chronological order. T340 leaves the
  historical order intact and appends new T340 entries rather than rewriting ledger history.

## Next Recommendation

Do not promote the Psalm candidate skill yet. Either collect additional reviewed Psalm evidence
before reconsidering promotion, or continue the roadmap with T341 as a Revelation hard-book atlas
lane only. Do not start Revelation implementation, T327G, boundary import, or global marker rules.
