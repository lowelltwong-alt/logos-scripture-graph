# T331 Post-T327 Chunking Backlog Reset

## Status

- Task: T331
- Mode: planning / reporting
- Status: complete
- Branch: `t331-post-t327-chunking-backlog-reset`
- Output-changing work: none
- Raw mutation: none
- Canonical mutation: none
- Canonical regeneration: none
- Chunk regeneration: none
- Evaluator / leaderboard / scorecard change: none
- Boundary import: none
- T327G: not started

## Purpose

T331 resets the post-T327 chunking backlog so future chunking improvements start from the corrected
canonical-66 corpus baseline rather than the pre-T327 wider-corpus baseline.

This is planning/reporting only. It does not select or implement a chunking improvement.

## Current Canonical Corpus Baseline

Post-T327 canonical generated outputs are:

- Canonical books: 66.
- Passage records: 31,103.
- Translation witness records: 31,103.
- Canonical corpus QA: passes with five explicit textual-variant empty witnesses:
  `Luke.17.36`, `Acts.8.37`, `Acts.15.34`, `Acts.24.7`, and `Rom.16.25`.

## Current Chunk Baseline

Post-T327D chunk baseline:

- Chunk run: D / Claude pass2, post-T327 canonical-66 corpus.
- Chunk count: 1,131.
- Chunk SHA-256: `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`.
- Token p50: 728.
- Token p90: 898.
- Token max: 1,152.
- Score baseline: 93.6 under unchanged T314 evaluator policy.

This is a corpus-scope correction / baseline reset, not a chunking improvement claim.

## What T327 Fixed

T327 fixed the active corpus and downstream baseline surfaces:

- Recorded the owner-approved 66-book canonical scope.
- Added an explicit 66-book allow-list and ingest filter.
- Hardened canonical-scope validation to fail closed on missing book identity.
- Regenerated canonical outputs under the 66-book filter.
- Regenerated chunks from corrected canonical outputs.
- Re-baselined chunk/gold/score/leaderboard surfaces for the canonical-66 corpus.
- Cleaned old-corpus eval/stress/review surfaces.
- Added planning-only boundary-source intake controls.

## What T327 Did Not Improve

T327 did not:

- improve chunking quality;
- change the chunking algorithm;
- change the evaluator formula;
- promote a chunking skill;
- add new reviewed target gold for output-changing work;
- authorize boundary import;
- start T327G.

Future chunking improvements must be measured against the post-T327 canonical-66 baseline.

## Candidate Future Work Areas

| Candidate area | Expected value | Risk | Required evidence | Likely tests | Needs new gold? | Likely touch surface |
| --- | --- | --- | --- | --- | --- | --- |
| Psalms / poetry stanza behavior | High for long poetic retrieval and parent/child structure | Moderate: marker evidence can become metric chasing or over-splitting | Reviewed Psalm/poetry cases beyond Ps.78/Ps.105/Ps.106, stress atlas evidence, route ledger | Per-form gold tests, chunk SHA/route tests, non-target poetry controls | Yes | candidate skill/config; maybe evaluator diagnostics only |
| Wisdom literature chunk boundaries | Medium-high for Proverbs/Ecclesiastes scanability | Moderate-high: sentence literature may resist stable units | Reviewed Proverbs/Ecclesiastes samples, sentence/paragraph evidence | Gold windows, token distribution checks, non-regression route tests | Yes | candidate skill/config |
| Prophetic oracle structures | High for Isaiah/Jeremiah/Ezekiel retrieval | High: oracle headings, poetry, prose, and source-tradition issues interact | Review packets for oracle units and embedded poems | Stress/gold packet tests, boundary sidecar checks | Yes | candidate skill/config; maybe context packet design |
| Narrative pericope boundaries | High for Gospel/OT narrative retrieval | Moderate: headings may be editorial and not authority | Reviewed pericope samples and section-heading evidence | Target chapter windows, hard-gate regressions | Yes | config/candidate skill; context packet usage |
| Epistle argument/paragraph boundaries | Medium-high for discourse retrieval | Moderate: paragraphing can be translation/editorial | Reviewed epistle paragraph/argument cases | Gold windows, token distribution, sentence integrity | Yes | candidate skill/config |
| Genealogy/list handling | Medium for long-list readability | Low-moderate: lists are marker-heavy but easy to over-specialize | Reviewed genealogy/list stress cases | Synthetic/list fixtures, token and no-book-crossing checks | Some | config/candidate skill |
| Section heading / footnote / cross-reference context packet usage | High for retrieval context quality | High: commentary/editorial evidence must not enter chunk text or authority | Context packet contract review and non-contamination tests | Context packet tests, source/authority separation tests | Maybe | context packet generation, not chunk output first |
| Stress atlas edge cases | High as review queue input | Moderate-high depending on case | Review packet promotion from T316/T318/T319 queue | Case-specific gold and non-authorizing status tests | Yes | review packets/gold before implementation |
| Candidate skill promotion pathway | High for governed iteration | Moderate: promotion can outrun evidence | Valid package metadata, reviewed gold, route ledger, staleness triggers | Skill lifecycle tests, promotion gate tests | Indirectly | registry/config/tests |
| Gold expansion needs | High for all future implementation | Low-moderate: can remain non-output-changing | Human-reviewed target examples and controls | Manifest validation, per-form gold tests | Yes | gold/test docs only |

## Recommended Task Sequence

1. T332: select one narrow chunking target.
2. T333: implement one candidate skill/config improvement only after reviewed target evidence exists.
3. T334: evaluate against the post-T327 canonical-66 baseline.
4. T335: expand gold/stress coverage if needed.

## Stop Conditions For Future Work

Stop before implementation if a proposed task:

- lacks reviewed target gold or a reviewed review-packet decision;
- requires raw/canonical mutation;
- requires canonical or chunk regeneration outside the task scope;
- changes evaluator formula before evaluator-policy review;
- uses boundary material as default Scripture meaning;
- tries to claim score movement as chunking improvement when it is corpus-scope or evaluator-policy
  correction;
- starts T327G or boundary import without separate authorization.

## Recommendation

Use T332 to choose one narrow target. Psalms/poetry stanza behavior is a strong candidate because the
repo already has Psalm gold, stress cases, reviewed Psalm 78 parent/child behavior, and reviewed
Ps.105/Ps.106 preservation. T332 should still compare alternatives and document why the selected
target is safer than the rest.
