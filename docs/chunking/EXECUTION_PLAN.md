# Chunking Execution Plan — multi-pass + multi-agent A/B

How we actually turn the raw files into graph-ready chunks, evaluate quality, and
improve it across passes. Pairs with `CHUNKING_DESIGN.md` (the why) and
`EVALUATION_PLAN.md` (the metrics).

## Pipeline (raw → derived)

```text
data/raw/**.zip
  → scan_raw_sources.py        (first-pass marker inventory; HARD gate via validate_raw_coverage)
  → usfm_importer.py           (canonical: passages, witnesses, word_tokens, boundary_claims, ...)
  → chunker.py                 (derived: chunks.jsonl, context_packets.jsonl)
  → evaluate_chunks.py         (A/B metrics + comparison report)
```

Run it:

```bash
python scripts/scan_raw_sources.py && python scripts/validate_raw_coverage.py
python pipelines/ingest/usfm_importer.py
python pipelines/chunking/chunker.py \
  --passages data/canonical/scripture/passages/passages.jsonl \
  --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl \
  --boundary-claims data/canonical/translations/eng-web/boundary_claims.jsonl \
  --footnotes data/canonical/translations/eng-web/footnotes.jsonl \
  --crossrefs data/canonical/translations/eng-web/editorial_cross_references.jsonl \
  --out data/derived/chunks/eng-web/chunks.jsonl \
  --context-out data/derived/chunks/eng-web/context_packets.jsonl
```

## Passes (each pass is reviewable; do not skip ahead)

| Pass | Adds | Status |
|------|------|--------|
| **1. Structural / genre** | genre-aware boundary-driven chunks (whole-psalm, heading-bounded prose, no mid-sentence), metadata carry-through | **DONE (this PR family)** |
| **2. Sentence / TextSpan refinement** | TextSpan records (sentence/clause spans), long-unit splitting (Ps 119 acrostic, genealogies), better stanza detection | next |
| **3. Context packets + retrieval** | ContextPacket for all fragile chunks, retrieval-overlap windows, prooftext warnings | next |
| **4. Source-language alignment** | align chunks to Hebrew/Greek (WLC/SBLGNT), clause boundaries override English convenience | Phase 5 |
| **5. Connection discovery** | candidate intertextual/lexical/thematic/extra-biblical edges (see connection-discovery role) | parallel, candidate-zone |

First pass before multi-pass: **always** validate Pass 1 against the gold set and the
A/B harness before adding Pass 2+. Each pass is its own PR + A/B comparison vs the prior winner.

## Multi-agent A/B protocol

The first attempt at any pass uses **multiple competing variants scored two ways**:

1. **Objective (deterministic):** `evaluate_chunks.py` scores every variant on
   sentence integrity, psalm fragmentation, book crossings, USFM leaks, size
   distribution, boundary-basis coverage, metadata carry-through, and gold checks.
2. **Subjective (multi-agent):** ≥2 independent agents (different models/roles per
   `config/agents/model_routing.yaml`) review the SAME variants on a fixed hard-passage
   set and rank them, flagging literary failures + undiscovered connections the
   metrics miss.

### Variant slots (first run)

| Variant | Strategy | Owner |
|---------|----------|-------|
| A | genre-aware, default budgets (700/1100) | reasoner-profile agent |
| B | genre-aware, tight budgets (350/550) — retrieval precision | executor-profile agent |
| C | naive sentence-window (no genre/boundaries) — baseline | control |

Hard-passage review set: **Gen 1 (narrative), a genealogy (Gen 5 / Matt 1), Ps 23
(short psalm), Ps 119 (long acrostic), Prov 10 (proverb cluster), Isa 53 (oracle),
Matt 13 (parables), Rom 7:14–8:11 (argument), Heb 1 (catena), Rev 4–5 (vision).**

### Decision rule

- Reject any variant with `usfm_leaks > 0`, `book_crossings > 0`, or
  `sentence_integrity_pct < 100` (prose).
- Among survivors, pick by the pass's goal (precision vs context completeness),
  using objective metrics + the agents' ranking consensus.
- The winner is promoted to `data/derived/chunks/eng-web/chunks.jsonl` (derived,
  rebuildable). Losers are archived under `build/ab/`. **A human approves the winner**
  before any downstream (embeddings/graph) consumes it — chunks stay `candidate` until then.

### First-run objective result (Pass 1)

See `build/ab/report.md`. Summary: A/B/C all sentence-safe, 0 leaks, 0 book-crossings,
gold checks pass. They differ on size (A p50≈745, B≈410, C≈1109) and psalm handling.
Open issue surfaced: a long unit hits `tok_max≈2331` (Ps 119) — Pass 2 long-unit splitting.
