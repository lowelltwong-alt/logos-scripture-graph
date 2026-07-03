# Red-Team Pre-Mortem — Multi-Model Whole-Bible Chunking Fork (T423)

**Role:** Independent reviewer. You are NOT the marathon chunker. Your job is to attack the plan, find failure modes, and produce a pre-mortem before anyone runs days-long whole-Bible scratch marathons.

**Output file (required):** `.ai/scratch/multi_model_bible_chunking/redteam/REDTEAM_PREMORTEM_REPORT.md`

**Optional:** Append one JSONL line to `.ai/control/agent_review_ledger.jsonl` with `review_tier: redteam_fork_premortem`.

---

## Independence rules

1. Read the fork policy and scratch scaffold **critically** — assume the plan will fail unless proven otherwise.
2. Do **not** start chunking. Do **not** write `whole_bible_chunk_map.jsonl` entries.
3. You **may** read baseline plan (T410) to compare fork vs original.
4. State clearly: **GO / HOLD / ABANDON_FORK** with conditions.

---

## Mandatory reads (in order)

1. `.ai/control/multi_model_whole_bible_chunking_fork.yaml`
2. `.ai/scratch/multi_model_bible_chunking/manifest.yaml`
3. `.ai/scratch/multi_model_bible_chunking/shared_research_baseline/research_baseline_manifest.yaml`
4. `.ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md`
5. `.ai/control/parallel_chunking_research_program.yaml` (baseline to revert to)
6. `.ai/control/scratch_lane_policy.yaml`
7. `.ai/control/chunking_lesson_index.yaml` — search LSN-040, LSN-041, LSN-039
8. `.ai/scratch/multi_model_bible_chunking/comparison/README.md`
9. `.ai/context/agent_work/T417/model_layers/batch2/` (batch ladder fork running in parallel — leakage risk?)

---

## Pre-mortem scenario (assume this already happened)

> *It is 30 days later. The fork was abandoned. Chunking is slower than before. Models produced incompatible maps. Agreement was useless. Theology smuggled into boundaries. Owner reverted to T410 but lost weeks.*

Your job: explain **how** we got there. List concrete paths from **this plan** to that failure.

---

## Attack surfaces (check every one)

### A. Strategy & speed claims

- Does "continuous marathon days straight" actually speed up chunking vs T410 batch ladder?
- Will 3–10 full Bible passes cost more review time than they save?
- Is "agreement = easy" valid when models share the same training biases?
- Can high agreement be **false consensus** (all wrong the same way)?

### B. Scratch vs canon leakage

- Paths where `whole_bible_chunk_map.jsonl` gets treated as canon
- Paths where agreement ledger auto-promotes to `eval/chunking_gold/` or `data/candidate/chunks/`
- Promotion packet gaps for SUB-012 vs new fork SUB
- LSN-041: standing policy / scratch disposition mistaken for gold authority

### C. Research baseline fairness

- Is `research_baseline_manifest.yaml` complete enough for fair comparison?
- Missing: DSS, variant policy, Revelation deferral, pastoral epistles queue nuance?
- Can one model "extend research" in scratch in ways that invalidate comparison?
- Strong's / wj / red-letter: evidence-only rule — will models violate it at scale?

### D. Schema & comparability

- Is `whole_bible_chunk_map.jsonl` schema sufficient for delta detection?
- Span overlap vs exact match — will comparison miss near-miss disagreements?
- Book order / chunk_index drift across models
- Optional M5 slot — does 4 vs 5 vs up to 10 models break majority rules? (use ceil(0.7 * N))

### E. Theology & chunking errors

- Phlm ethics, Jude noncanonical, Jonah typology — will whole-Bible pass amplify these?
- Gospel discourse / WJ speaker boundaries at scale
- Poetry vs narrative mis-routing across whole Bible
- Apocalyptic (Revelation) — should it be in marathon or excluded?

### F. Operational marathon risks

- Context window / session breaks mid-marathon — progress loss?
- `marathon_progress.yaml` not updated — partial maps compared as complete?
- One model finishes first — others anchor bias if they peek at comparison folder
- Git scratch branch size / JSONL merge conflicts

### G. Parallel path confusion

- T417 batch2 multi-model ladder + T423 fork — can agents confuse the two?
- Does fork starve governed batch2 work?
- Two strategies = double control-plane drift?

### H. Revert conditions

- Are `revert_to_baseline_if` conditions measurable?
- Who declares fork abandoned — owner only?
- What happens to scratch artifacts on revert?

---

## Required report structure

Write `REDTEAM_PREMORTEM_REPORT.md` with these sections:

```markdown
# Red-Team Pre-Mortem — T423 Whole-Bible Multi-Model Chunking Fork

## Executive verdict
GO | HOLD | ABANDON_FORK
(one sentence why)

## Pre-mortem narrative
(How we failed in 30 days — 3–8 paragraphs)

## Findings table
| ID | Severity P0/P1/P2 | Area | Failure mode | Fix before marathon |
|----|-------------------|------|--------------|---------------------|

## Agreement-vs-delta logic audit
(Can agreement/delta actually prioritize work? Counterexamples?)

## Baseline comparison
(Fork vs T410 — when is baseline strictly better?)

## Minimum fixes before M1 marathon
(Numbered list — blockers only)

## Non-blockers to monitor
(P1/P2 watch list)

## Recommended experiment scope
(All 66 books? Pilot 5 books? Which 5?)

## Non-authorizations confirmed
(What reviewer must not authorize)
```

---

## Severity guide

- **P0:** Theology/authority leakage, canon write path, or fork makes chunking less safe than baseline
- **P1:** Comparison invalid, marathon wastes days, or revert path broken
- **P2:** Hygiene, docs, schema polish

---

## Verdict enums

- **GO** — run marathon with listed minimum fixes
- **HOLD** — fix P0/P1 blockers first; pilot scope only
- **ABANDON_FORK** — revert to T410; fork net harmful

---

## Non-authorizations (reviewer)

You must NOT:
- Authorize reviewed gold, chunk output, or canon writes
- Approve the fork as replacing T410 without owner phrase
- Start marathons (M1–M5 initial; M6–M10 optional) in your review session
