# Session Continuation Handoff — for a fresh chat window

**Repo:** `logos-scripture-graph` (local: `C:\Users\lowel\OneDrive\Desktop\Git Projects\03_World_View\logos-scripture-graph-repo`)
**Remote:** https://github.com/lowelltwong-alt/logos-scripture-graph — **everything is on `main`** (local == origin/main == `0935494`).
**Upstream project:** https://github.com/lowelltwong-alt/logos-governance-architecture (theological source; this repo is its data-plane substrate).
**Paste this file to the new window first.** Then read `AI_FRONT_DOOR.md`.

---

## 1. Where we are (all merged to main, gates green: `validate_all` + 30 pytest)

Built & merged across PRs #1–#6:
- **Ingest** (committed raw zip → canonical; the importer reads the zip directly, no manual unzip).
- **Chunker v1 + Pass-2** (genre-aware, boundary-driven): whole-psalm, **Ps 119 → 22 acrostic stanzas**, wisdom saying-clusters, 0 mid-sentence, 0 USFM leaks, metadata carry-through.
- **Hard raw-source rule**: `scan_raw_sources.py` → `RAW_SOURCE_INVENTORY.md` + `usfm_marker_coverage.yaml` + `validate_raw_coverage.py` gate (CI fails on any unclassified marker). Enforced in AI_FRONT_DOOR + CLAUDE.md + CI.
- **Taxonomy v0.2** split: structural schemas here (witness, textual_variant, lexeme, semantic_domain, translation_note, alignment_record, extra_biblical_source [fenced], classification_assignment); classification vocabulary promoted to the governance repo.
- **Control plane**: human-gated MASTER_CONTEXT + lock, branch protection on main (CODEOWNER review + `validate` check; admin break-glass), model routing + roster, CONTRIBUTING.
- **Multi-agent A/B framework**:
  - Chunking: `evaluate_chunks.py --scorecard-dir` + `leaderboard.py`; runs in `data/derived/chunks/variants/<agent>__pass<N>__<variant>__<UTCstamp>/` (gitignored); committed scorecards in `eval/chunking_runs/`; `eval/LEADERBOARD.md`.
  - Connection discovery: `pipelines/graph/discover_connections.py` + `compare_candidate_batches.py`; candidates in `data/candidate/connections/` (trust zone `candidate`, never promoted).

### Current leaderboard (chunking)
`claude pass2 (D)` **88.5** > A_genre_default 81.4 > B_genre_tight 78.7 > C_naive_window 63.2.

### Connection discovery status (T308)
- **Codex 5.5 run 1 = MERGED** (PR #5). 500 candidate edges in `data/candidate/connections/codex-5.5-2026-06-05.jsonl`. Audited: 100% candidate-zone, all evidenced, predicates registered, **55 de-duped vs editorial `\x`**, schema-valid, genuinely-correct top quotes (Luke 4:10→Ps 91:11, 1Pet 1:16→Lev 11:44, Matt 27:9→Zech 11:13). Methods: rare Strong's co-occurrence, rare 4–7-gram phrase overlap, citation-formula.
- Claude seed batch = 8 hand-picked typology edges (`2026-06-04-ab-review.jsonl`).
- Codex(500) vs Claude(8) overlap = **0 agreement** (different methods) → need run 2+ before adjudication is meaningful.

### Standing handoffs (the runbooks for dispatching agents)
- `.ai/handoffs/T308/handoff.md` — connection discovery (Codex-style), has a paste-prompt.
- `.ai/handoffs/T309/handoff.md` — chunking bake-off, has a paste-prompt + Pass-2 targets.
- `.ai/handoffs/CONNECTION_DISCOVERY_AGENT.md` — governing brief (candidate-only, evidence, never auto-promote).

---

## 2. The user's open question (answer it / act on it next)

> "What should Codex and Claude do next? Is Codex looking at the actual raw files? Narrow on troublesome passages, or broad, or both? Maybe a first run on the whole corpus in batches, both agents, then feed back and restart from the same place?"

**Recommended answer (give this, then execute if approved):**
- **Is Codex looking at the real raw files?** Effectively yes — Codex regenerates canonical data from the committed zip (`usfm_importer.py`) and mines `word_tokens.jsonl` (Strong's) + witness text. It is grounded in the real corpus, not assumptions. (Raw-coverage gate guarantees the markers are all classified.)
- **Narrow vs broad → BOTH, in this order:**
  1. **Broad first pass already exists** (Codex's 500 corpus-wide). Add a **second broad run by a different model** (Claude or another) using the SAME `discover_connections.py` so outputs are comparable → `compare_candidate_batches.py` gives the agreement set (high-precision, promote-worthy) and disagreement set (adjudicate).
  2. **Then narrow/deep passes on troublesome passages** — the hard-passage set (Isa 53, Ps 22, Ps 110, Gen 22, Exod 12, Heb 1 catena, Rev 4-5, Joel 2, Matt 13) where the broad lexical methods are weak (typology, allusion, theology) and human/reasoner judgment matters. Narrow runs catch what scale misses.
- **Batched whole-corpus + "restart from same place":** yes — the design already supports it. Each agent's run is namespaced + scorecard/manifest committed, so after feedback everyone re-runs from the same `main` commit with tuned params. For chunking, that's the `eval/chunking_runs/` leaderboard; for connections, `compare_candidate_batches.py`. No new infra needed — just dispatch run 2.

**Concrete next dispatch (pick one or more):**
- A) **Connection discovery run 2** — point a *different* model at `.ai/handoffs/T308/handoff.md` paste-prompt; it writes `data/candidate/connections/<model>-<date>.jsonl`; then run
  `python pipelines/graph/compare_candidate_batches.py data/candidate/connections/*.jsonl` → agreement set for the human.
- B) **Chunking bake-off** — point models at `.ai/handoffs/T309/handoff.md`; they try to beat **88.5**; `python pipelines/chunking/leaderboard.py` ranks them.
- C) **Narrow deep-dive** — a reasoner pass on the hard-passage set for typology/allusion (candidate edges), to complement Codex's lexical breadth.
- D) **Promote Pass-2 chunks to production** (`data/derived/chunks/eng-web/chunks.jsonl`) so downstream (embeddings/retrieval) has a real baseline.

---

## 3. How to run things (commands)

```bash
pip install -e ".[validate,test]"
python pipelines/ingest/usfm_importer.py            # regen canonical (~60s; gitignored; reads committed zip)
python scripts/validate_all.py && python -m pytest -q   # must be green (30 tests)
# chunking variant + score + rank:
python pipelines/chunking/chunker.py --passages data/canonical/scripture/passages/passages.jsonl \
  --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl \
  --boundary-claims data/canonical/translations/eng-web/boundary_claims.jsonl \
  --footnotes data/canonical/translations/eng-web/footnotes.jsonl \
  --crossrefs data/canonical/translations/eng-web/editorial_cross_references.jsonl \
  --out data/derived/chunks/variants/<run_id>/chunks.jsonl
python pipelines/chunking/evaluate_chunks.py <variant>=<path> --scorecard-dir eval/chunking_runs --agent <id> --pass-num <N>
python pipelines/chunking/leaderboard.py
# connection discovery + compare:
python pipelines/graph/discover_connections.py --agent <id> --out data/candidate/connections/<id>-<date>.jsonl ...
python pipelines/graph/compare_candidate_batches.py data/candidate/connections/*.jsonl
```

## 4. Governance rules the new window MUST keep

- `main` is branch-protected (CODEOWNER = @lowelltwong-alt + `validate` check). Land work via PR; admin-merge is the human's call (this session used `gh pr merge --squash --admin` on the user's behalf when asked).
- Never edit `MASTER_CONTEXT.md`/lock; never write `data/raw` or `data/canonical` by hand; chunks/edges are derived/candidate — **human promotes**, nothing auto-promotes.
- Before any chunking/ingest change: re-read `RAW_SOURCE_INVENTORY.md` + run `validate_raw_coverage.py`.
- Regenerate `DATA_MAP.md` after data/pipeline/schema changes; keep gates green before stopping.
- **Known cross-platform gotcha:** writers use `newline="\n"`; sort by `as_posix()`; `git cat-file -e origin/main:path` MANGLES on Windows (`/`→`\`, `:`→`;`) — use `git ls-tree` instead.

## 5. Loose ends / cleanups (non-blocking)
- Codex committed `build/discovery/*.md` (build/ should be ephemeral) → `git rm --cached` later.
- A few Codex evidence labels have tokenization artifacts (cosmetic).
- `relationship_object` assertion_mode enum {asserted,inferred,candidate} vs `classification_assignment` 5-mode enum — harmonize (tracked).
- Issue #50 in governance repo (monthly architecture review) is the user's, left open.
- Open human action: confirm branch protection settings + CODEOWNERS handle are as intended.
