# Task Handoff

## Task

- task_id: T330
- title: Canonical Corpus QA
- phase: phase_4
- status: complete

## Agent

- agent_name: codex
- mode: qa-reporting
- stage: final
- updated_at: 2026-06-09T02:19:51+00:00
- handoff_id: 54e3351527a85e88

## T328 gate verification

- command: `git fetch origin`
- result: succeeded.
- command: `git checkout main`
- result: succeeded.
- command: `git pull --ff-only origin main`
- result: fast-forwarded to PR #33 merge commit `357cd03`.
- command: `git status --short`
- result: clean output.
- command: `git merge-base --is-ancestor 8498976 main`
- result: success, commit `8498976` present on main.
- command: `gh pr view 33 --json number,title,state,mergedAt,mergeCommit,statusCheckRollup`
- result: PR #33 `T328: add workflow lesson collector updates` is `MERGED`, merged at
  `2026-06-09T01:36:31Z`, merge commit `357cd0337dd1de11ead52880d57827ce088d71f7`, validate check
  `SUCCESS`.
- merge/rebase state: absent.

Because the T328 gate passed, T330 proceeded.

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- ROADMAP_STATE.yaml
- AI_TABLE_OF_CONTENTS.md
- scripts/validate_all.py
- scripts/validate_canonical_66_scope.py
- pipelines/util/canonical_scope.py
- tests/test_t327b_canonical_66_ingest_filter.py
- docs/roadmap/T327F_BOUNDARY_SOURCE_INTAKE_PLANNING.md
- data/canonical/scripture/passages/passages.jsonl
- data/canonical/translations/eng-web/translation_witnesses.jsonl
- data/canonical/translations/eng-web/footnotes.jsonl
- data/canonical/translations/eng-web/boundary_claims.jsonl
- data/canonical/translations/eng-web/section_headings.jsonl
- data/canonical/translations/eng-web/word_tokens.jsonl

## Files changed

- scripts/qa_canonical_corpus.py
- scripts/validate_all.py
- tests/test_qa_canonical_corpus.py
- docs/roadmap/T330_CANONICAL_CORPUS_QA.md
- AI_TABLE_OF_CONTENTS.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/tasks/T330.task.yaml
- .ai/handoffs/T330/handoff.md
- ROADMAP_STATE.yaml

## Decisions made

- Added a read-only canonical corpus QA script rather than regenerating or mutating canonical output.
- Integrated the QA script into `validate_all` only when generated passage/witness outputs are
  present, preserving clean-checkout behavior before regeneration.
- Enforced exact configured 66-book passage presence/order and no excluded-book leakage.
- Enforced passage/witness ID uniqueness and one-to-one passage/witness alignment.
- Enforced sidecar canonical book identity and known passage IDs where sidecars carry
  `passage_id`.
- Treated the five current empty witness records as allowed only because they are known
  textual-variant/omitted-verse locations and have explanatory footnotes:
  `Luke.17.36`, `Acts.8.37`, `Acts.15.34`, `Acts.24.7`, and `Rom.16.25`.
- T327G was not started.
- Boundary import/source acquisition was not started.

## Validation run

- command: `python scripts/validate_canonical_66_scope.py`
- result: passed; canonical 66 scope config validation passed.
- command: `python scripts/qa_canonical_corpus.py`
- result: passed; 66 books, 31,103 passages, 31,103 witnesses, 5 allowed empty textual-variant
  witnesses, 28,165 boundary claims, 340 editorial cross-references, 1,130 footnotes, 0 glossary
  entries, 283 section headings, and 677,688 word tokens.
- command: `python -m pytest -q tests/test_qa_canonical_corpus.py`
- result: passed; `10 passed`.
- command: `python -c "import yaml; yaml.safe_load(open('.ai/tasks/T330.task.yaml', encoding='utf-8')); yaml.safe_load(open('ROADMAP_STATE.yaml', encoding='utf-8')); print('YAML parse passed: .ai/tasks/T330.task.yaml, ROADMAP_STATE.yaml')"`
- result: passed.
- command: `git diff --check`
- result: passed; only a CRLF warning for `.ai/control/handoff_ledger.jsonl`.
- command: `python scripts/validate_all.py`
- result: passed; all validation gates passed, including handoff validation for 35 paths, canonical
  66 scope validation for 8 JSONL files, JSONL validation for 63,959 records, and canonical corpus
  QA.
- command: `python -m pytest -q`
- result: passed; `144 passed in 119.10s`.

## Known risks

- QA validates identity/coherence, not source-text authenticity when fake or altered content is
  mislabeled with an allowed book. That remains a raw source manifest, checksum, provenance, parser
  determinism, and raw immutability concern.
- The allowed empty witness list is explicit and should be revisited if the source edition or
  verse-omission policy changes.
- Future boundary intake remains separate and owner-authorized.

## Open questions

- Whether future QA should add stronger source checksum-to-record provenance reconciliation beyond
  the existing source manifest and raw tripwire.
- Whether intentionally empty witness records should receive first-class generated metadata in a
  later task instead of relying on the T330 QA allow-list plus footnote evidence.

## Next agent instruction

Review and merge if green. Do not start T327G unless separately authorized. Boundary import remains
prohibited. Cross-repo lesson mirrors remain pending until worktrees are clean.
