# T330 Canonical Corpus QA

## Status

- Task: T330
- Mode: QA / reporting
- Status: complete
- Branch: `t330-canonical-corpus-qa`
- Raw mutation: none
- Canonical mutation: none
- Generated output regeneration: none
- Chunk regeneration: none
- Evaluator / leaderboard / scorecard change: none
- Boundary source import: none
- T327G: not started

## Purpose

T330 adds a read-only corpus-health QA layer after the T327A-F canonical-scope correction sequence
and T328 workflow lesson capture.

The goal is to verify that the generated canonical outputs now behave as a coherent 66-book corpus
without regenerating them, rewriting them, re-baselining chunks, changing evaluator policy, or
starting boundary-source intake.

## Scope

T330 is QA/reporting only.

T330 does not:

- mutate `data/raw/**`;
- mutate `data/canonical/**`;
- regenerate canonical outputs;
- regenerate chunks;
- change chunk output;
- change evaluator formula;
- change leaderboard or scorecards;
- change chunker or orchestrator behavior;
- import texts;
- move excluded material to `logos-boundary-literature`;
- create boundary corpus records;
- start T327G;
- authorize boundary import or source acquisition;
- claim chunking improvement.

## QA Script

The read-only QA script is:

```bash
python scripts/qa_canonical_corpus.py
```

It reads existing generated canonical outputs under `data/canonical/` and prints a corpus-health
summary. It writes no files and performs no regeneration.

`scripts/validate_all.py` runs the QA script conditionally when generated passage and witness files
are present. This keeps clean checkouts safe while preserving CI coverage after the validate workflow
regenerates canonical data.

## Checks Implemented

The QA script verifies:

- expected canonical book set contains exactly the configured 66 books;
- passage first-seen book order matches the configured canonical book order;
- no excluded/non-66 books appear in checked canonical outputs, including `Tob`, `Jdt`, `AddEsth`,
  `Wis`, `Sir`, `Bar`, `1Macc`, `2Macc`, `1Esd`, `PrMan`, `Ps151`, `3Macc`, `2Esd`, `4Macc`,
  and `AddDan`;
- `FRT` and `GLO` do not appear as Scripture content;
- canonical records checked by the QA layer expose resolvable book identity;
- passage records have non-empty passage IDs through their `id` field;
- translation witness records have non-empty `passage_id` values;
- passage IDs are unique;
- witness `passage_id` values are unique;
- translation witnesses align count-wise and passage-id-wise with passages;
- translation witness text is non-empty except for explicitly enumerated current
  textual-variant/omitted-verse witnesses with explanatory footnotes: `Luke.17.36`, `Acts.8.37`,
  `Acts.15.34`, `Acts.24.7`, and `Rom.16.25`;
- passage records do not carry empty `text` fields if a text field is present;
- boundary claims, footnotes, editorial cross-references, and section headings contain only
  canonical book identities;
- sidecar `passage_id` values, when present, point to known passage IDs;
- glossary entries are empty or explicitly marked non-Scripture;
- word tokens, when checked, contain only canonical book identities and known passage IDs.

## Relationship To T327

T327A-F corrected corpus scope and downstream baselines:

- T327A audited the prior wider corpus.
- T327B and T327B.1 established fail-closed 66-book scope policy.
- T327C regenerated canonical outputs under the 66-book filter.
- T327D reset chunk/gold/score/leaderboard baselines for the corrected corpus.
- T327E cleaned residual old-corpus eval surfaces.
- T327F documented boundary-source intake as planning only.

T330 does not move the baseline again. It adds a read-only health check over the corrected corpus.
The T327 sequence remains corpus-scope correction / baseline reset, not chunking improvement.

## Boundary Intake Boundary

T330 does not import boundary texts, create boundary corpus records, or move excluded material into
`logos-boundary-literature`.

Future boundary intake remains owner-authorized and planning-gated. Boundary material must not
override, equal, contaminate, or silently reinterpret canonical Scripture authority.

## Validation

Expected validation for T330:

```bash
python scripts/validate_canonical_66_scope.py
python scripts/qa_canonical_corpus.py
python scripts/validate_all.py
python -m pytest -q
git diff --check
```

YAML parse checks should cover `.ai/tasks/T330.task.yaml` and `ROADMAP_STATE.yaml`.

## Next

Review and merge if green. Do not start T327G unless separately authorized. Boundary import remains
prohibited.
