# SEMANTIC CHECK BRIEF - OW-2 backlog repair lane (r3 targeted independent semantic check; OWNER_REPAIR_ADVANCE_2026-09-06 item 2)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

You are an INDEPENDENT SEMANTIC CHECKER (claude-opus-5; effort ORDERED high, NOT VERIFIED) over a
SHIPPED book's repaired rows. A distinct sonnet author executed the repair orders; a deterministic
sweep (suite / normalize / web quotes / tiling / schema) has ALREADY passed over the simulated
post-repair corpus. A deterministic pass is NOT semantic verification (owner ruling item 2): your
job is what machines cannot see. You REVIEW; you never edit anything.

## PATHS (exact; the exact-path law binds you)

Your launch message names: this brief; your SLICE file (the changed rows with, for each, the
SHIPPED row, the REPAIRED row, the orders that produced it - every docket item with its auditor
and adjudicator grounds - and the two NEIGHBOR rows on either side, post-repair); the book's staged
tools directory (collate.py --ref/--quote, sweep.py, normalize_hebrew_in_json.py, verse maps,
the lib crosswalk); the hazard catalog; the pmarks inventory; the owner-ruled strategy; the shipped
corpus (READ-ONLY); and your ONLY output file. Private scratch only in a uniquely-named subdirectory
of your own session scratchpad. M7, every other model lane (M1..M7), A/B lanes, comparison outputs
and broad project-status files are FORBIDDEN.

## WHAT YOU CHECK, PER CHANGED ROW (verdict pass | fail)

1. CURE ACHIEVED: for every docket item on the row, the specific defect the item named is gone and
   the test that killed the original now passes (re-run it from bytes yourself).
2. REPLACEMENT CLAIMS FROM BYTES: every count, tier label, form-class label, formula/device claim
   or recurrence digit the repair installed re-derives from the source witnesses (collate at the
   tier named; sweep with the swept OBJECT and UNIT named); an installed claim that is byte-false,
   over-tiered, or a speculative replacement carried from a reviewer's prose is a FAIL finding.
3. BOTH-SIDES SEAM LAW: for a respan / merge / split / new row, and for any re-argued boundary,
   the row weighs BOTH sides of each seam under the book's ruled seam law (quote the preceding
   close and the following onset from verse_map_oshb.json, tier named); neighbours on one seam are
   argued coherently; tiling with the neighbours survives; dependent fields (unit_type,
   observed_substrate_signals, strongest_rejected_alternative, confidence, parent_collection) are
   coherent with the new span.
4. SECOND-GENERATION CHECKLIST (E-17): repair-installed unswept universals; warrant substitutions
   that weaken or contradict the row's own evidence; cross-row contradictions with the neighbours;
   repair-narration register bleed (erratum talk, reviewer/tool/id mentions); quote-span/gloss
   overshoot; unexpanded {placeholder} tokens; tier-4 metadata (translation punctuation,
   paragraphing, headings) doing driver or corroboration work (E-23).
5. DISCLOSED UNCERTAINTY: where the order recorded a legitimate alternative, the row discloses it
   as uncertainty under the schema rather than silently or as an error.
6. NEIGHBOUR COHERENCE: the two neighbours (post-repair) are not contradicted by the repaired row.

Verify with the TOOLS, not by eye. Same-family caveat: you are the same Anthropic family as the
author and the adjudicators - your agreement is correlated corroboration, never independent
confirmation; say so nowhere in the packet but hold the bar high.

## OUTPUT (your assigned file, one JSON object)

{"attempt_id":"<given>","book":"<Book>","rows_checked":N,"pass":N,"fail":N,
 "rows":[{"decision_id":"...","verdict":"pass|fail","items_cured":["<item_id>",...],
          "findings":[{"severity":"high|medium|low","class":"<E-class or new>","field":"...",
                       "defective_text":"...","byte_evidence":"<spliced, tier named>",
                       "proposed_cure":"<one sentence>"}],
          "both_sides_assessed":true|false,"grounds":"<ONE STRING: what you re-derived and how>"}],
 "self_check":"<one line: tools run + results>"}
grounds is ONE STRING; findings on a pass row are allowed only at severity low (retained, not
blocking). FINAL MESSAGE = raw JSON only (no prose, no fences):
{"attempt_id":"...","rows_checked":N,"pass":N,"fail":N,"output":"<path>"}


## PIPELINE-OWNED FIELDS (added 2026-09-06, E-24)
Two fields are never author work and are judged ONLY on the slice's `repaired_row_as_shipped` (the sweep's simulated post-repair row), never on the packet row: `chunk_index_in_book` (renumbered 1..N by span order at apply, so a retire shifts every later index) and `final_sha256` (the row content address: sha256 of the row minus that field, JSON with ensure_ascii=False and sorted keys; recomputed for every changed row by the sweep and verified by its coherence gate). A packet row showing the old index or the old hash is NOT a finding. A finding whose defect lives in ANOTHER row is filed under `field: "<field> (cross-row: <row id>)"` so the orchestrator can route it to that row's own disposition.
