# Delta Compare — Multi-Model Whole-Bible Chunk Maps (T423)

**Role:** Comparison auditor. You compare **completed** (or interim) `whole_bible_chunk_map.jsonl` files across model folders and produce agreement vs delta artifacts.

**Do NOT** chunk the Bible in this session. **Do NOT** write canon surfaces.

---

## When to run

- **After** at least **3** model marathons have maps (minimum to compare)
- **Initial target:** 5 models (M1–M5)
- **Maximum:** 10 models (add M6–M10 from `models/_TEMPLATE/`)

---

## Mandatory reads

1. `.ai/control/multi_model_whole_bible_chunking_fork.yaml` — note `model_count` and `comparison_rules`
2. `.ai/scratch/multi_model_bible_chunking/manifest.yaml` — list all **active** model folders
3. `.ai/scratch/multi_model_bible_chunking/comparison/README.md`
4. Every model folder with `marathon_progress.yaml` status `complete` (or interim books):
   - `M1_cursor/`, `M2_claude_sonnet5/`, `M3_claude_frontier/`, `M4_codex_gpt55/`, `M5_gemini_thinking/` (initial)
   - `M6_*` … `M10_*` (if owner added slots)

---

## Comparison rules

### Agreement (easy chunks)

Let `N` = number of **complete** models in this batch offline compare run.
Let `majority = ceil(0.7 * N)` (e.g. N=5 → 4, N=10 → 7).

Primary metric: **verse-coverage agreement rate** (`overall_verse_coverage_agreement_rate` in matrix).

- **Full consensus:** exact same `span` across **all N** complete models
- **Easy bucket:** exact same `span` across **≥ majority** models
- Write each to `comparison/agreement_chunks.jsonl` with `models_agreeing` list and `complete_model_count: N`

### Delta (focus queue)

Record disagreement when **any** of:

- Different span boundaries for same region (overlap but not exact match)
- Different **chunk count** per book between models
- Same verses covered by different split patterns
- One model defers/splits where another keeps a larger parent span
- Literature-type guess differs **and** boundary differs (flag both)

Write each to `comparison/disagreement_delta.jsonl`

### Near-miss (important)

Do not only compare exact strings. For each book, check:

- Span overlap percentage when boundaries differ by 1–3 verses
- "Shifted boundary" vs "completely different structure"

---

## Required outputs

| File | Content |
|------|---------|
| `comparison/agreement_chunks.jsonl` | Consensus spans — one JSON line per agreed chunk |
| `comparison/disagreement_delta.jsonl` | Disagreements — one JSON line per delta item |
| `comparison/model_agreement_matrix.yaml` | Per-book agreement rate, chunk counts per model |
| `comparison/delta_focus_queue.yaml` | Prioritized list for governed T410 work |
| `comparison/delta_summary.md` | Executive summary for owner and DAD |

### agreement_chunks.jsonl line format

```json
{
  "book": "Jude",
  "span": "Jude.1.1-Jude.1.2",
  "models_agreeing": ["M1_cursor", "M2_claude_sonnet5", "M3_claude_frontier", "M4_codex_gpt55"],
  "complete_model_count": 5,
  "agreement_tier": "full_consensus|easy_majority",
  "literature_type_guess": "epistle_greeting",
  "easy_chunk": true,
  "non_authorizing": true
}
```

### disagreement_delta.jsonl line format

```json
{
  "delta_id": "DELTA-JONAH-001",
  "book": "Jonah",
  "region": "Jonah.1.1-Jonah.1.5",
  "models": {
    "M1_cursor": "Jonah.1.1-Jonah.1.3",
    "M2_claude_sonnet5": "Jonah.1.1-Jonah.1.4",
    "M3_claude_frontier": "Jonah.1.1-Jonah.1.2"
  },
  "delta_kind": "boundary_shift|split_count_mismatch|literature_routing_disagreement",
  "priority": "high|medium|low",
  "theology_risk_note": "prophetic_typology region",
  "governed_work_recommended": true,
  "non_authorizing": true
}
```

---

## delta_summary.md structure

```markdown
# Delta Summary — Multi-Model Whole-Bible Chunk Comparison

## Scope
(which models compared — list all M1..M10 active; N = complete model count; majority = ceil(0.7*N))

## Headline metrics
- Overall agreement rate
- Easy chunk count
- Delta span count
- Highest-disagreement books (top 10)

## Easy chunks (sample)
(table — do not list entire Bible if huge)

## Delta focus queue (top priorities)
(numbered — these go to T410 governed work)

## False consensus warnings
(where all models agree but research baseline suggests risk)

## Recommendations
- adopt_consensus_for_books: [...]
- require_owner_review_for: [...]
- revert_fork_signal: yes|no

## Non-authorizations
(agreement does not promote gold or output)
```

---

## DAD follow-up

If comparison is materially complete, append to `.digital-asset/mail/outbox.jsonl`:

- `message_type: experiment_interim_result` or use template `msg-t423-delta-summary` from `.digital-asset/mail/outbox_followup_templates.yaml`

Update `.digital-asset/lessons/t423_multi_model_whole_bible_chunking_fork.yaml` with interim metrics if fork still running.

---

## Non-authorizations

- No `eval/chunking_gold/` writes
- No `data/candidate/chunks/` writes
- Agreement does not auto-promote reviewed gold
- Do not delete or edit model source maps — compare read-only
