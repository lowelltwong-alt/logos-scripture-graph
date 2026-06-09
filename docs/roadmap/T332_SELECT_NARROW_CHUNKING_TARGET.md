# T332 Select Narrow Chunking Target

## Status

- Task: T332
- Mode: planning / target selection
- Status: complete
- Branch: `t332-select-narrow-chunking-target`
- Implementation: none
- Output-changing work: none
- Raw mutation: none
- Canonical mutation: none
- Evaluator formula change: none
- Boundary import: none
- T327G: not started

## Purpose

T332 selects exactly one narrow next chunking-improvement target for future implementation. It does
not implement the target.

The selected target must be high value, low/moderate risk, measurable against existing gold/stress
evidence, independent of evaluator formula changes, independent of source/corpus changes, and small
enough for a future isolated PR.

## Chosen Target

Chosen target: **Psalms / poetry stanza behavior**.

Future implementation should focus on a narrow Psalm/poetry stanza improvement lane, not a general
poetry rewrite. The initial target should be selected from reviewed or review-ready Psalm evidence,
with no raw/canonical mutation and no evaluator formula change.

## Why This Target

Psalms/poetry stanza behavior is the safest next target because the repo already has the strongest
evidence base here:

- Psalm gold manifest coverage already exists.
- Psalm 78 has a reviewed parent/child structural split decision.
- Psalm 105 and Psalm 106 have reviewed whole-psalm preservation decisions.
- Psalm 119 is already a strong parent/child sectioning precedent.
- The stress atlas and observed behavior audit already track long Psalm and poetry cases.
- The candidate Psalm skill seam already exists and is behavior-preserving.
- The target can be scoped without changing canonical corpus, evaluator formula, or source intake.

The target is still not implementation-ready until T333 cites a reviewed target boundary decision or
adds reviewed gold for the exact change.

## Rejected Alternatives

| Alternative | Why deferred |
| --- | --- |
| Wisdom literature chunk boundaries | Valuable, but needs fresh Proverbs/Ecclesiastes reviewed examples before implementation. |
| Prophetic oracle structures | High value, but higher risk because poetry/prose/oracle headings/source-tradition issues interact. |
| Narrative pericope boundaries | Valuable, but section headings are editorial evidence and need a context-packet policy review first. |
| Epistle argument/paragraph boundaries | Valuable, but argument-boundary gold is not yet ready and paragraphing may be translation-scoped. |
| Genealogy/list handling | Likely safer technically, but lower immediate value than Psalm/poetry and still needs reviewed target cases. |
| Section heading / footnote / cross-reference context packet usage | Important, but should start as context-packet design, not chunk output change. |
| Stress atlas edge cases broadly | Too broad for one PR; individual cases need review packets or reviewed gold first. |
| Candidate skill promotion pathway | Important governance lane, but it is infrastructure rather than a concrete quality target. |
| Gold expansion only | Useful and may be required first, but T332 is selecting the improvement target, not a pure gold pack. |

## Required Evidence Before T333

T333 must cite at least one of:

- reviewed Psalm target gold under `eval/chunking_gold/per_form/`;
- an explicit human-reviewed review packet for the selected Psalm/poetry case;
- a new reviewed gold increment that is committed before any output-changing implementation.

T333 must not rely on:

- aggregate score movement alone;
- weak evaluator upside alone;
- characterization-only evidence;
- proposed stress-atlas entries;
- pending review packets;
- marker evidence without human boundary review.

## Required Tests For T333

Future implementation should include:

- targeted Psalm/poetry gold test for the selected behavior;
- non-target regression controls for existing reviewed cases;
- Psalm 78 parent/child reviewed split preservation or explicit reviewed update;
- Psalm 105 and Psalm 106 reviewed whole-psalm preservation unless a new human decision changes them;
- Psalm 119 22-section behavior preservation;
- route ledger/provenance check if the candidate Psalm skill or routing config changes;
- chunk output SHA or targeted output-delta explanation;
- protected-path checks proving no raw/canonical mutation and no boundary import.

## Expected Files For Future Implementation

Likely T333 touch surfaces, depending on the exact selected Psalm/poetry case:

- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `tests/test_chunker_gold.py`
- `tests/test_chunking_orchestrator.py`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/`
- `config/chunking/` only if a config-level change is selected
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `.ai/handoffs/T333/`
- `.ai/tasks/T333.task.yaml`

Protected unless separately authorized:

- `data/raw/**`
- `data/canonical/**`
- `data/derived/chunks/**` outside ignored/generated validation runs
- `pipelines/chunking/evaluate_chunks.py`
- `pipelines/chunking/leaderboard.py`
- `eval/LEADERBOARD.md`
- `eval/chunking_runs/**`
- boundary repo source/corpus files

## Stop Conditions For T333

Stop before implementation if:

- no reviewed target gold exists for the exact output change;
- the proposed change requires evaluator formula changes;
- the proposed change requires source/corpus changes;
- the proposed change depends on boundary material as authority;
- the proposed change would alter Ps.78, Ps.105, Ps.106, or Ps.119 contrary to reviewed decisions;
- the change is larger than one narrow Psalm/poetry behavior;
- the expected gain is only metric cleanup rather than target-form evidence.

## Claude Review Later

Claude should review T333 for:

- whether target evidence is reviewed gold rather than characterization-only;
- whether the output change is truly narrow;
- whether the evaluator meaning remains unchanged;
- whether current reviewed Psalm decisions remain protected;
- whether score language avoids chunking-improvement claims unless target output evidence supports
  one.

## Recommendation

Proceed to T333 only after a reviewed Psalm/poetry target is named. A gold-first T333 may be safer
than an implementation T333 if the exact stanza target is not yet reviewed.

## T336 Roadmap Clarification

T336 preserves the T332 Psalm selection as the current implementation lane, but clarifies why:
Psalms are first because reviewed evidence, stress surfaces, and the candidate Psalm skill seam
already exist. This does not mean Psalms are necessarily harder than Revelation.

Revelation should receive an early hard-book atlas/review-packet lane, while Revelation
implementation waits until reviewed gold exists. Book-specific Revelation assumptions must not leak
globally into Psalm, prophecy, Gospel discourse, epistle, or monolith fallback behavior.
