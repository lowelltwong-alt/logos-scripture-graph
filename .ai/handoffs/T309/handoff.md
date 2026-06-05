# Task Handoff — T309: Multi-agent chunking bake-off (standing runbook)

## Task

- task_id: T309
- title: Multi-agent chunking bake-off — many agents chunk, namespaced, compared on a leaderboard
- phase: phase_3
- status: in_progress

## Agent

- agent_name: any-chunking-agent
- mode: build
- stage: start
- updated_at: 2026-06-05T03:42:14+00:00
- handoff_id: de4120723e2b2d3b

---

## What this is

A **standing runbook**, not a one-shot task. ANY agent/model may submit a chunking
attempt. Each leaves a namespaced run; `leaderboard.py` ranks all runs so we converge on
the best chunking ("get it perfect"). This is the chunking analogue of the connection-
discovery bake-off (T308). Run it as many times / with as many models as you like.

## Goal of THIS round (Pass 2)

Beat the current leader (`A_genre_default`, composite 84.8) by fixing the failures the
first multi-agent A/B review found (see `docs/chunking/AB_FIRST_PASS_VERDICT.md`):

1. **Section headings (`\s`/`\ms`) ignored across the canon** — promote them to chunk-closing
   boundaries (fixes Isa 52:13–53:12, Heb 1 catena over-merges).
2. **Long acrostics not split — Ps 119 (tok_max≈2331) shielded by `whole_psalm`.** Add
   acrostic/stanza splitting (Ps 119 = 8-verse stanzas; Lam 1–4; Ps 25/34/37/111/112/145)
   with overlap context packets.
3. **Parable severed from its interpretation** (Matt 13) — parable+question+explanation in
   one chunk, or a mandatory ContextPacket linking them.
4. **Wisdom budget not enforced** (Proverbs collapses to ~1100-word chunks) — apply soft-max
   within wisdom; saying-cluster units.
5. **Genealogies** (Gen 5, Matt 1) as units.

You do NOT have to fix all five. Fix what you can, keep the hard gates, and submit.

## Setup (raw zip is committed — do NOT unzip manually)

```bash
pip install -e ".[validate,test]"
python pipelines/ingest/usfm_importer.py     # regenerates canonical data from the committed zip (~60s)
```

## Produce your run (namespaced — name/id + pass + time)

Pick a `run_id = <agent>__pass<N>__<variant>__<UTCstamp>` (see eval/chunking_runs/README.md).

```bash
python pipelines/chunking/chunker.py \
  --passages data/canonical/scripture/passages/passages.jsonl \
  --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl \
  --boundary-claims data/canonical/translations/eng-web/boundary_claims.jsonl \
  --footnotes data/canonical/translations/eng-web/footnotes.jsonl \
  --crossrefs data/canonical/translations/eng-web/editorial_cross_references.jsonl \
  --out data/derived/chunks/variants/<run_id>/chunks.jsonl
# score it -> writes the COMMITTED scorecard
python pipelines/chunking/evaluate_chunks.py <variant>=data/derived/chunks/variants/<run_id>/chunks.jsonl \
  --scorecard-dir eval/chunking_runs --agent <agent> --pass-num <N>
python pipelines/chunking/leaderboard.py     # updates eval/LEADERBOARD.md
```

If you improve the chunker, edit `pipelines/chunking/chunker.py` (it is genre-aware /
boundary-driven). Keep `tests/test_chunker_gold.py` green.

## HARD RULES

- **Hard gates (or your run is ineligible):** 0 USFM leaks, 0 book crossings, 100% prose
  sentence integrity, Psalm 23 = one whole-psalm chunk. Never split mid-sentence / mid-colon /
  psalm superscription (CHUNKING_RULES.md).
- Chunks are **derived/candidate** — never canonical. The human promotes the winner.
- Big `chunks.jsonl` stays under `data/derived/chunks/variants/<run_id>/` (gitignored);
  **commit only your scorecard** in `eval/chunking_runs/`.
- Design against the REAL markers in `.ai/control/RAW_SOURCE_INVENTORY.md` (e.g. `\d`, `\qs`,
  `\wj`, `\fqa`) — `validate_raw_coverage.py` must still pass.
- If you hit a literary judgment call you can't ground, keep the conservative behavior, log it
  in Open questions, and submit anyway.

## Acceptance

- `python scripts/validate_all.py && python -m pytest -q` green.
- Your scorecard exists in `eval/chunking_runs/`; `leaderboard.py` ranks it.
- Open a PR titled "Chunking run: <agent> pass<N> <variant>"; do NOT merge; do NOT promote.

## Compare & resolve (the human, after N runs)

`leaderboard.py` ranks all committed scorecards. The human inspects the top runs on the
hard-passage set (Gen 1, Gen 5, Ps 23, Ps 119, Prov 10, Isa 53, Matt 13, Rom 7-8, Heb 1,
Rev 4-5), picks the winner, and promotes it to `data/derived/chunks/eng-web/chunks.jsonl`.
Disagreements between agents on specific passages are the signal for where chunking is hard.

## Paste prompt (any chunking agent)

```text
Read AI_FRONT_DOOR.md, then .ai/handoffs/T309/handoff.md IN FULL and
docs/chunking/{CHUNKING_DESIGN.md,CHUNKING_RULES.md,AB_FIRST_PASS_VERDICT.md}.
The raw zip is committed — do NOT unzip it; run `python pipelines/ingest/usfm_importer.py`.
Produce an improved Bible chunking that beats the current leader by fixing as many Pass-2
targets as you can (section-heading boundaries, Ps 119 acrostic splitting, parable cohesion,
wisdom budget, genealogy units) WITHOUT breaking the hard gates (0 USFM leaks, 0 book
crossings, 100% prose sentence integrity, Psalm 23 = one whole-psalm chunk; never split
mid-sentence/colon/superscription). Write chunks to
data/derived/chunks/variants/<your-agent-id>__pass1__<variant>__<UTCstamp>/chunks.jsonl,
score with `evaluate_chunks.py --scorecard-dir eval/chunking_runs --agent <id> --pass-num 1`,
run `leaderboard.py`, keep tests green, open a PR, do NOT merge or promote. If a literary
call is unclear, stay conservative and log it — do not guess.
```

## Files read
- (agent: fill in)
## Files changed
- (agent: fill in)
## Decisions made
- (agent: fill in — which Pass-2 targets you fixed + how)
## Validation run
- (agent: paste outputs + your leaderboard line)
## Known risks
- English-only structure; true Hebrew/Greek colometry awaits Phase 5.
## Open questions
- (agent: log conservative calls)

## Next agent instruction

Another agent/model: run this same runbook (new run_id). After several runs, the human
compares via leaderboard.py + hard-passage inspection and promotes the winner. Seeded runs:
the first A/B (A_genre_default leads at 84.8) are already in eval/chunking_runs/.
