# Pass 1 chunking — multi-agent A/B verdict (first attempt)

Three variants (A=genre-default, B=genre-tight, C=naive-window) scored two ways:
the deterministic harness (`build/ab/report.md`) + three independent agent reviewers
(retrieval engineer [sonnet], biblical-literature scholar [opus], graph-connections
analyst [opus]).

## Rankings

| Reviewer (lens) | Ranking | One-line reason |
|---|---|---|
| Objective harness | tie on safety; differ on size | all sentence-safe, 0 leaks, 0 book-crossings, gold checks pass |
| Retrieval / RAG | **B > A > C** | B's ~410-tok chunks are the embedding sweet spot; A too big for wisdom; C bloated |
| Biblical-literature | **A > B > C** | A keeps literary units intact; B shatters arguments/parables; C genre-blind |
| Graph / connections | **A > B > C** | A keeps units + carries crossref leads; B mis-anchors Isa 53; C drops all leads |

## Verdict: **Variant A wins Pass 1** (2 of 3 lenses + best graph integrity)

A is the promotion candidate. The precision advantage B showed is real but is better
captured by **fixing A's boundaries in Pass 2** than by shrinking budgets (which
shatters arguments/parables). **C (naive window) is dominated** — it drops every
curated cross-reference/footnote lead (`fn=0/xr=0`) and bloats chunks; this is the
proof that genre-aware boundary-driven chunking beats naive windowing.

> Chunks remain `candidate` (derived, rebuildable) until a human approves the winner
> before any embeddings/graph consume them.

## Pass 2 backlog (consensus failures the agents converged on)

1. **Section headings ignored across the canon (root cause).** `usfm_section_heading`
   fires only in apocrypha (AddDan), 0× in the 66-book canon → over-merges (Isa 53,
   Heb 1 catena, Rev 4-5). **Fix:** promote `\s`/`\ms` to a hard chunk-closing boundary.
2. **Long acrostics not split — Ps 119 worst.** `whole_psalm` *shields* Ps 119 from
   splitting (tok_max=2331, 176 verses, one chunk) while non-"psalm" acrostics (Lam 3)
   do split. **Fix:** acrostic/stanza splitting for outsized poems (Ps 119 = 8-verse
   stanzas; Lam 1-4; Ps 25/34/37/111/112/145), with overlap context packets.
3. **Parable severed from its interpretation** (Matt 13 sower & wheat-tares) — all
   variants. **Fix:** parable-cohesion rule (parable + question + explanation in one
   chunk) or a mandatory ContextPacket linking them.
4. **Isa 52:13–53:12 servant song** mis-bounded (A over-merges 51-54; B cuts 53:2/3) —
   the most NT-quoted OT chapter. **Fix:** follows from #1 (section-heading boundary).
5. **Wisdom budget not enforced** — A's Proverbs collapses to ~1,100-word chunks;
   per-proverb retrieval impossible. **Fix:** apply soft-max within wisdom; saying-cluster units.
6. **Genealogies** (Gen 5, Matt 1) not treated as units. **Fix:** genealogy unit rule (Pass 2/TextSpan).

These map onto Pass 2 (sentence/TextSpan refinement + long-unit splitting) in EXECUTION_PLAN.md.

## Discovery output

The graph-connections reviewer surfaced 8 evidenced, **uncurated** candidate connections
(Gen22→Rom8.32, Exod12→1Cor5.7, Rev4.8→Isa6.3, Rev5.5→Gen49.9/Isa11.1, Joel2→Rev6,
Ps22→Rev5/7, John3.16→Gen22.2, Heb1.3→Col1.15-17). Emitted as candidate edges in
`data/candidate/connections/2026-06-04-ab-review.jsonl` (trust zone `candidate`,
`inferred_ai_candidate`, never auto-promoted; de-dup'd against existing `\x` leads).
