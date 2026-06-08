# T327A Forensic Canonical Corpus Scope Audit

## Status

- Task: T327A
- Mode: planning / forensic audit
- Status: complete
- Branch: `t327a-forensic-canonical-corpus-scope-audit`
- Base: `main` at `91328d1`
- Implementation status: audit only

T327A does not implement removal, filtering, regeneration, scorecard changes, or
runtime changes. It records the current corpus scope issue and proposes isolated
future remediation tasks.

## Confirmed Owner Scope Decision

`logos-scripture-graph` canonical Scripture and chunking corpus is scoped to the
66-book canon by owner decision.

Deuterocanonical, apocrypha, boundary, front-matter, glossary, and other
non-Scripture editorial material must not enter canonical passages/chunks by
default.

Future use of excluded material belongs in `logos-boundary-literature` or another
explicitly scoped boundary/tradition repository, after separate source/license
review and human authorization.

Raw source artifact provenance must be handled carefully. Do not hand-edit raw
archives without a source replacement or migration plan.

## Audit Inputs

### Confirmed

Read-only surfaces inspected:

- `data/raw/bible/eng-web/usfm/eng-web_usfm.zip`
- `data/raw/bible/eng-web/source_manifest.yaml`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `.ai/control/DATA_MAP.md`
- `data/processed/bible/eng-web/usfm/usfm_events.jsonl`
- `data/canonical/scripture/passages/passages.jsonl`
- `data/canonical/translations/eng-web/translation_witnesses.jsonl`
- `data/canonical/translations/eng-web/boundary_claims.jsonl`
- `data/canonical/translations/eng-web/word_tokens.jsonl`
- `data/canonical/translations/eng-web/footnotes.jsonl`
- `data/canonical/translations/eng-web/section_headings.jsonl`
- `data/canonical/translations/eng-web/editorial_cross_references.jsonl`
- `data/canonical/translations/eng-web/glossary_entries.jsonl`
- `data/derived/chunks/variants/*/chunks.jsonl`
- `eval/chunking_runs/*.json`
- `eval/LEADERBOARD.md`
- `eval/chunking_gold/**`
- `tests/**`
- Git history and PR metadata through local git and `gh`

No files under `data/raw/**`, `data/canonical/**`, `data/processed/**`, or
`data/derived/**` were mutated.

## Allowed 66-Book OSIS Scope

Allowed OSIS books:

```text
Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh
Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic
Nah Hab Zeph Hag Zech Mal Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil
Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John
Jude Rev
```

Song and Lamentations are canonical and stay.

## Current Corpus Inventory

### Raw Archive

### Confirmed

Raw archive:

- path: `data/raw/bible/eng-web/usfm/eng-web_usfm.zip`
- source manifest SHA-256:
  `a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e`
- archive entries: 87
- USFM files: 83
- non-USFM ancillary files:
  - `copr.htm`
  - `gentiumplus.css`
  - `keys.asc`
  - `signature.txt.asc`

Raw USFM classification:

- 66 canonical USFM files
- 15 deuterocanonical/apocrypha/non-66 USFM files
- 1 front matter USFM file
- 1 glossary USFM file

Excluded raw USFM files:

| Source file | OSIS | Classification |
|---|---:|---|
| `00-FRTeng-web.usfm` | `FRT` | `exclude_front_matter` |
| `41-TOBeng-web.usfm` | `Tob` | `exclude_deuterocanonical_apocrypha` |
| `42-JDTeng-web.usfm` | `Jdt` | `exclude_deuterocanonical_apocrypha` |
| `43-ESGeng-web.usfm` | `AddEsth` | `exclude_deuterocanonical_apocrypha` |
| `45-WISeng-web.usfm` | `Wis` | `exclude_deuterocanonical_apocrypha` |
| `46-SIReng-web.usfm` | `Sir` | `exclude_deuterocanonical_apocrypha` |
| `47-BAReng-web.usfm` | `Bar` | `exclude_deuterocanonical_apocrypha` |
| `52-1MAeng-web.usfm` | `1Macc` | `exclude_deuterocanonical_apocrypha` |
| `53-2MAeng-web.usfm` | `2Macc` | `exclude_deuterocanonical_apocrypha` |
| `54-1ESeng-web.usfm` | `1Esd` | `exclude_deuterocanonical_apocrypha` |
| `55-MANeng-web.usfm` | `PrMan` | `exclude_deuterocanonical_apocrypha` |
| `56-PS2eng-web.usfm` | `Ps151` | `exclude_deuterocanonical_apocrypha` |
| `57-3MAeng-web.usfm` | `3Macc` | `exclude_deuterocanonical_apocrypha` |
| `58-2ESeng-web.usfm` | `2Esd` | `exclude_deuterocanonical_apocrypha` |
| `59-4MAeng-web.usfm` | `4Macc` | `exclude_deuterocanonical_apocrypha` |
| `66-DAGeng-web.usfm` | `AddDan` | `exclude_deuterocanonical_apocrypha` |
| `106-GLOeng-web.usfm` | `GLO` | `exclude_glossary` |

### Processed USFM Events

### Confirmed

`data/processed/bible/eng-web/usfm/usfm_events.jsonl`:

- total events: 74,297
- canonical 66-book events: 60,960
- excluded/front/glossary events: 13,337

Excluded event counts:

| Book | Events |
|---|---:|
| `1Esd` | 542 |
| `1Macc` | 1,135 |
| `2Esd` | 1,155 |
| `2Macc` | 707 |
| `3Macc` | 261 |
| `4Macc` | 564 |
| `AddDan` | 812 |
| `AddEsth` | 287 |
| `Bar` | 251 |
| `FRT` | 37 |
| `GLO` | 101 |
| `Jdt` | 505 |
| `PrMan` | 27 |
| `Ps151` | 32 |
| `Sir` | 4,898 |
| `Tob` | 406 |
| `Wis` | 1,617 |

### Canonical Passage And Witness Outputs

### Confirmed

`data/canonical/scripture/passages/passages.jsonl`:

- total records: 38,058
- books: 81
- canonical 66-book records: 31,103
- excluded deuterocanonical/apocrypha records: 6,955

`data/canonical/translations/eng-web/translation_witnesses.jsonl`:

- total records: 38,058
- books: 81
- canonical 66-book records: 31,103
- excluded deuterocanonical/apocrypha records: 6,955

Excluded passage/witness record counts:

| Book | Records |
|---|---:|
| `1Esd` | 448 |
| `1Macc` | 924 |
| `2Esd` | 944 |
| `2Macc` | 555 |
| `3Macc` | 228 |
| `4Macc` | 484 |
| `AddDan` | 530 |
| `AddEsth` | 205 |
| `Bar` | 213 |
| `Jdt` | 339 |
| `PrMan` | 15 |
| `Ps151` | 7 |
| `Sir` | 1,383 |
| `Tob` | 244 |
| `Wis` | 436 |

### Canonical Sidecars

### Confirmed

Generated sidecar surfaces include excluded material in some files:

| Surface | Total | Canonical 66 records | Excluded records | Notes |
|---|---:|---:|---:|---|
| `boundary_claims.jsonl` | 34,177 | 26,838 | 5,694 | 1,645 source/editorial records did not map to a Scripture book in the audit count. |
| `word_tokens.jsonl` | 677,688 | 677,688 | 0 | Strong-token sidecar observed across 66 books only. |
| `footnotes.jsonl` | 1,855 | 1,127 | 723 | 5 records did not map to a Scripture book in the audit count. |
| `section_headings.jsonl` | 314 | 50 | 2 | 262 records did not map to a Scripture book in the audit count. |
| `editorial_cross_references.jsonl` | 363 | 340 | 23 | Excluded origins include `1Esd`, `2Esd`, `Sir`, `Tob`, `Wis`. |
| `glossary_entries.jsonl` | 94 | 0 | 0 | Glossary-source entries; not Scripture-book records. |

### Chunk Outputs

### Confirmed

Local generated chunk variants include 81 books and excluded books. These outputs
are generated/ignored, but they informed committed scorecards.

| Variant | Chunks | Excluded chunks | Excluded books present |
|---|---:|---:|---|
| `A_genre_default` | 1,271 | 204 | `1Esd`, `1Macc`, `2Esd`, `2Macc`, `3Macc`, `4Macc`, `AddDan`, `AddEsth`, `Bar`, `Jdt`, `PrMan`, `Ps151`, `Sir`, `Tob`, `Wis` |
| `B_genre_tight` | 2,174 | 368 | same 15 excluded books |
| `C_naive_window` | 983 | 160 | same 15 excluded books |
| `D_claude_pass2` | 1,374 | 243 | same 15 excluded books |

### Scorecards And Leaderboard

### Confirmed

Committed scorecards under `eval/chunking_runs/*.json` and
`eval/LEADERBOARD.md` were produced against the wider 81-book generated corpus.

The current official score language remains:

```text
D / Claude pass2 = 93.5 under T314 reviewed-structural-split evaluator policy.
```

After a 66-book filter is implemented and generated outputs are regenerated,
scorecards and leaderboard must be regenerated and relabeled as corpus-scope
correction, not chunking improvement.

T327A did not run the leaderboard.

## Git / PR Forensic Findings

### Initial Raw And Canonical Scope

### Confirmed

- commit: `63d74b4ff919c3f9e27e98e25518d51f54dd458b`
- message: `Initial commit: governed Scripture graph substrate + T304 remediation`
- PR: none identified; root publication commit
- introduced or preserved:
  - `data/raw/bible/eng-web/usfm/eng-web_usfm.zip`
  - `data/raw/bible/eng-web/source_manifest.yaml`
  - `config/canon/canon_profiles.yaml`
  - `pipelines/ingest/usfm_importer.py`
  - generated-count assumptions for 38,058 passages

What entered: WEB Classic raw archive containing 83 USFM files, including 66
canonical books, 15 excluded non-66 books, front matter, and glossary. The
source manifest records the raw archive SHA.

Commands for later inspection:

```bash
git show --stat 63d74b4
git show --name-status 63d74b4 -- data/raw data/canonical config/canon pipelines/ingest
git show 63d74b4 -- data/raw/bible/eng-web/source_manifest.yaml config/canon/canon_profiles.yaml
git blame data/raw/bible/eng-web/source_manifest.yaml
git blame config/canon/canon_profiles.yaml
```

### Raw Inventory And Chunker V1

### Confirmed

- commit: `e1914207787d0ce20820e6f03043da0c70707227`
- message: `Genre-aware boundary-driven chunker v1 + hard raw-source inspection rule`
- PR: #1
- URL: `https://github.com/lowelltwong-alt/logos-scripture-graph/pull/1`
- introduced or preserved:
  - `.ai/control/RAW_SOURCE_INVENTORY.md`
  - `config/ingest/usfm_marker_coverage.yaml`
  - `scripts/scan_raw_sources.py`
  - `scripts/validate_raw_coverage.py`
  - chunker consumption of generated canonical boundary evidence

What entered: the raw inventory recorded 83 USFM files and 38,058 verses from
the full archive, without a 66-book exclusion policy.

Commands for later inspection:

```bash
git show --stat e191420
git show --name-status e191420
git show e191420 -- .ai/control/RAW_SOURCE_INVENTORY.md config/ingest/usfm_marker_coverage.yaml
gh pr view 1 --json number,title,url,baseRefName,headRefName,mergedAt,commits,files
gh pr diff 1
```

### A/B Evaluator Surface

### Confirmed

- commit: `1a8c3fde3dad988da34e6e3472e30ea4f3915fdf`
- message: `Chunking A/B harness + multi-pass plan + first multi-agent A/B verdict + connection discovery`
- PR: #3
- URL: `https://github.com/lowelltwong-alt/logos-scripture-graph/pull/3`
- introduced:
  - `pipelines/chunking/evaluate_chunks.py`
  - A/B scoring surfaces against wider generated chunks

Commands for later inspection:

```bash
git show --stat 1a8c3fd
git show --name-status 1a8c3fd
gh pr diff 3
```

### Leaderboard And Initial Scorecards

### Confirmed

- commit: `5313b0f49602bb3b8d044cd1d7c7ec17465f1607`
- message: `Multi-agent chunking bake-off (namespaced runs + leaderboard) + T308 handoff to main`
- PR: #4
- URL: `https://github.com/lowelltwong-alt/logos-scripture-graph/pull/4`
- introduced:
  - `eval/LEADERBOARD.md`
  - `eval/chunking_runs/*.json`
  - `pipelines/chunking/leaderboard.py`

What entered: committed scorecards/leaderboard were based on wider-corpus chunk
runs.

Commands for later inspection:

```bash
git show --stat 5313b0f
git show --name-status 5313b0f -- eval pipelines/chunking
gh pr diff 4
```

### D / Claude Pass2 Scorecard

### Confirmed

- commit: `e8d9993962c28f1975cd0231bfb7db6fb6a3514a`
- message: `Pass-2 reference chunker: Ps 119 acrostic splitting + per-genre budgets (new leaderboard leader)`
- PR: #6
- URL: `https://github.com/lowelltwong-alt/logos-scripture-graph/pull/6`
- introduced:
  - `eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json`
  - updated `eval/LEADERBOARD.md`

What entered: the current baseline lineage includes a D/pass2 run over generated
chunks that include excluded books.

Commands for later inspection:

```bash
git show --stat e8d9993
git show --name-status e8d9993 -- eval pipelines/chunking
gh pr diff 6
```

### Psalm Gold Non-Target Controls

### Confirmed

- commit: `d64ea59d73b2dcf48bf8c84d8bf32391373d2e58`
- message: `T310 3b-gold: add executable Psalm gold checks`
- PR: #13
- URL: `https://github.com/lowelltwong-alt/logos-scripture-graph/pull/13`
- introduced:
  - `eval/chunking_gold/per_form/psalms_gold_manifest.json`
  - Psalm gold tests/docs with non-target poetry controls

What entered: `PrMan` and `Ps151` were retained as non-target controls. Under
the new owner scope decision, those controls must be removed from canonical
Scripture-repo gold/control surfaces or re-scoped as boundary-literature
planning notes.

Commands for later inspection:

```bash
git show --stat d64ea59
git show --name-status d64ea59 -- eval tests
gh pr diff 13
```

### Stress Atlas And Gold Inventory

### Confirmed

- commit: `7c5dbb0641d22d855def52cb64f4b757abfce1a1`
- message: `T316: add biblical chunking stress atlas`
- PR: #17
- URL: `https://github.com/lowelltwong-alt/logos-scripture-graph/pull/17`
- introduced:
  - stress atlas surfaces under `eval/chunking_gold/stress_atlas/`
  - gold inventory references

What entered: stress/gold inventory surfaces preserved excluded-book controls
and need cleanup after the 66-book filter decision.

Commands for later inspection:

```bash
git show --stat 7c5dbb0
git show --name-status 7c5dbb0 -- eval tests docs
gh pr diff 17
```

### Review Packet Index

### Confirmed

- commit: `72e9c14b316d4645dc010cd2dbafe1c3c531e724`
- message: `T319: add review packet index and promotion queue`
- PR: #22
- URL: `https://github.com/lowelltwong-alt/logos-scripture-graph/pull/22`
- introduced:
  - `eval/chunking_gold/review_packets/review_packet_index.json`
  - `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md`

What entered: index/control surfaces now organize existing gold/stress/review
cases and must be updated after excluded controls are removed or re-scoped.

Commands for later inspection:

```bash
git show --stat 72e9c14
git show --name-status 72e9c14 -- eval tests
gh pr diff 22
```

## Affected Artifact Analysis

### Confirmed

Affected by future exclusion/removal:

- raw source inventory:
  - current inventory records the full archive and 83 USFM files;
  - future source replacement or ingest filter must update inventory language.
- processed USFM outputs:
  - `usfm_events.jsonl` contains front matter, glossary, and 15 excluded books.
- canonical passages:
  - current passage count is 38,058 across 81 books;
  - future 66-book canonical passage count is expected to be 31,103, unless the
    importer or source changes alter counting.
- translation witnesses:
  - current witness count mirrors 38,058 passages across 81 books.
- canonical sidecars:
  - boundary claims, footnotes, section headings, and editorial crossrefs include
    excluded-book records or source/editorial records.
- chunk outputs:
  - local generated variants include excluded chunks in all variants.
- scorecards/leaderboard:
  - committed runs and current `D / Claude pass2 = 93.5` baseline were produced
    against wider generated chunks.
- gold controls:
  - `PrMan` and `Ps151` must not remain canonical non-target controls after the
    66-book decision.
- stress atlas:
  - any excluded-book controls or cases must be removed or re-scoped.
- observed behavior audit:
  - observed audit may include current behavior over excluded chunks and must be
    revalidated after 66-book filtering.
- review packet index:
  - index and queue must remove or re-scope excluded-material entries.
- tests:
  - tests that expect non-66 controls must be rewritten as 66-book controls or
    boundary-scope planning checks.
- handoffs/status docs:
  - prior baseline language must be relabeled as pre-corpus-scope-correction.
- raw marker coverage:
  - coverage may still need to classify all markers present in raw if the full
    archive remains in raw; if source is replaced, coverage must be rechecked.

## Proposed Future Implementation Sequence

### T327B - Canonical 66-Book Allow-List / Ingest Filter

Add an explicit 66-book allow-list gate to ingest/canonical generation planning
and implementation. The gate should fail closed for excluded books, front matter,
and glossary. It should preserve raw provenance and avoid hand-editing the raw
archive.

Protected until approved: do not mutate raw archives; do not regenerate canonical
outputs in the same change unless the task explicitly authorizes it.

### T327C - Regenerate Canonical Outputs After 66-Book Filter

Regenerate processed/canonical outputs from raw plus the approved filter. Confirm
passages, witnesses, and sidecars contain only allowed 66-book Scripture content.

This task should update `DATA_MAP.md`, `RAW_SOURCE_INVENTORY.md` if needed, and
validation expectations.

### T327D - Regenerate Chunks, Scorecards, Leaderboard, And Score Language

Regenerate chunk variants, scorecards, and leaderboard against the 66-book corpus.
Any score movement is corpus-scope correction, not chunking improvement.

This task should explicitly preserve the T314 evaluator-policy provenance while
creating a new corpus-corrected baseline.

### T327E - Clean Gold / Stress / Observed / Index Surfaces

Remove or re-scope `PrMan`, `Ps151`, AddDan/AddEsth, and other excluded-material
controls from canonical Scripture-repo gold, stress, observed behavior, review
packet index, and tests. Replace non-target controls with canonical alternatives
where needed.

### T327F - Boundary Repo Source-Intake Plan

Plan any future use of excluded material in `logos-boundary-literature`. Do not
import source text until license/source review and repository-specific governance
are approved.

### T327G - Optional Raw Source Artifact Replacement / Migration Plan

If the raw archive itself must leave `logos-scripture-graph`, plan a safe source
replacement or migration. Do not delete or hand-edit raw archives without a
reviewed source-provenance plan.

## Confirmed / Inferred / Unknown

### Confirmed

- Raw WEB archive contains 83 USFM files, including 15 excluded books, front
  matter, and glossary.
- Generated canonical passages and translation witnesses currently contain 81
  books and 6,955 excluded non-66 passage/witness records.
- Local generated chunk variants contain excluded chunks.
- Current committed scorecards/leaderboard lineage was produced against wider
  generated chunks.
- T327A changed no raw, canonical, generated, runtime, evaluator, or scorecard
  files.

### Inferred

- A future 66-book filter will require regenerating canonical outputs, chunks,
  scorecards, and several gold/control surfaces.
- The safest first implementation step is an explicit allow-list/filter before
  any regeneration.
- Existing `PrMan` and `Ps151` non-target controls should be replaced with
  canonical controls rather than retained as Scripture-repo gold controls.

### Unknown

- Whether the raw WEB archive should stay as immutable provenance with an ingest
  filter, be replaced by a 66-book source artifact, or be migrated later.
- Whether `logos-boundary-literature` should ingest these texts, and from which
  source/license package.
- The final corpus-corrected D / Claude pass2 score after 66-book filtering and
  regenerated scorecards.

## No-Output-Change Boundary

T327A does not:

- mutate `data/raw/**`;
- mutate `data/canonical/**`;
- regenerate canonical outputs;
- change chunk output;
- change parser, chunker, orchestrator, evaluator, or leaderboard behavior;
- change scorecards;
- delete raw archives;
- import or move texts into `logos-boundary-literature`;
- create boundary-repo content from excluded texts;
- claim chunking improvement.

## T326 Raw Source / Marker Risk Discovery

This T327A audit reuses read-only source/marker inspection surfaces but does not
continue T326 implementation work.

Summary:

- raw/source surfaces inspected: raw WEB USFM ZIP, source manifest, raw source
  inventory, processed USFM event outputs, canonical sidecars, generated chunks,
  gold/stress/index surfaces, tests, and git/PR history.
- marker risks found: front matter, glossary, deuterocanonical/apocrypha books,
  AddDan/AddEsth, `PrMan`, and `Ps151` enter downstream generated/corpus
  surfaces unless filtered; raw marker evidence from excluded material can
  contaminate chunking and review controls.
- missing stress cases proposed: no new stress cases were added in T327A. Future
  T327E should replace excluded non-target controls with canonical 66-book
  controls and re-audit marker-sensitive cases after filtering.
- no raw/canonical mutation: confirmed.

## Red-Team Findings

### Contamination Risks

- Canonical passage and witness counts currently include excluded material.
- Chunk scorecards and leaderboard language are corpus-scope contaminated until
  regenerated after a 66-book filter.
- Non-target controls using `PrMan` and `Ps151` can make excluded material look
  legitimate inside the Scripture repo.

### Semantic-Smuggling Risks

- Keeping deuterocanonical/apocrypha texts in canonical chunking surfaces can
  silently encode canon/tradition decisions.
- AddDan/AddEsth can blur canonical Daniel/Esther scope if not filtered by
  explicit OSIS allow-list.
- Front matter and glossary can smuggle editorial commentary into Scripture
  retrieval if treated as chunkable corpus content.

### Evaluator / Score Risks

- The current 93.5 score is valid only as the pre-corpus-scope-correction T314
  evaluator-policy baseline.
- Re-baselining after filtering may move scores due to corpus composition, not
  chunker quality.
- Scorecards should record raw corpus scope and allowed-book policy version.

### Boundary / Commentary Contamination Risks

- Glossary and front matter can become retrieval context if future filters only
  check canon profiles and not source/editorial classes.
- Footnotes, section headings, and crossrefs from excluded books can remain in
  sidecars if filtering is not applied consistently across all generated outputs.

### Recommended Named Rules

- Canonical 66-book scope rule.
- Front matter / glossary exclusion rule.
- Boundary-literature quarantine rule.
- Corpus-scope score-provenance rule.
- Raw archive provenance migration rule.

### Future PRs That Should Be Isolated

- T327B allow-list / ingest filter.
- T327C canonical regeneration.
- T327D chunk/scorecard/leaderboard re-baseline.
- T327E gold/stress/index cleanup.
- T327F boundary repo source-intake planning.
- T327G optional raw source replacement or migration.
