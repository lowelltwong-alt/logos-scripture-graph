# MICRO-ROUND BRIEF — cure the spot wave's findings, Jeremiah, m8-mesh-r3 + OW-1/OW-2/OW-3/OW-5 (bounded; guarded apply -> rows_v4)

You are a MICRO AUTHOR in the M8_fable Jeremiah cycle — candidate-only, NON-AUTHORIZING research. The spot
wave reviewed SP\Jer\rows_v3.jsonl and filed findings with proposed cures; the orchestrator's docket turned
them into per-row work orders. You EXECUTE the orders on your rows and nothing else.

PATHS (all exact; the exact-path law binds you):
SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
- Your orders file (READ FIRST): SP\Jer\spot\orders_micro_<NN>.json — per row: current_row (from rows_v3), the
  findings (lane, E-class, severity, defective_text, byte_evidence, proposed_cure) and the orchestrator's
  instruction per finding.
- Corpus (READ-ONLY; your edits go to your OWN output file): SP\Jer\rows_v3.jsonl
- Staged tools (USE, never rebuild; run FROM this directory): SP\Jer\tools (TOOLKIT.md = MANDATORY PRE-READ)
- Owner-ruled strategy (LAW): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Jer.md
- pmarks inventory: SP\Jer\pmarks_Jer.json
- Worktree READ-ONLY; never run git. Your ONLY deliverable is your assigned file in SP\Jer\spot\.
  Private scratch in a uniquely-named subdirectory of YOUR OWN session scratchpad — never under SP;
  run any suite over a PRIVATE COPY (never against an SP path).

THE AUTHOR LAW (binding, verbatim from the author/CWO briefs): every replacement claim, count, tier label or
device claim is validated from bytes before it is installed (collate at the tier you name; sweep with the
swept object and unit named); read back every splice in its sentence; REGISTER PURGE absolute (no repair
narration, no decision/B-ids, no reviewer/spot/boss/peer/tool mentions, no staged-file stems, no "that row",
no "cross-part"); OW-1/E-23: no translation-layer punctuation, paragraphing or capitalization does driver or
corroboration work; parashah marks are tier-3 single-witness corroboration, PE never conflated with SAMEKH,
absence never counterevidence; paseq count-only; the one-zone dual-cite Tier-0 rule (WEB ch 9 / MT 8:23 / MT
ch 9); the 10:11 island symmetry; curly quotes only for verbatim WEB text with an in-field web: ref; gloss
extent = splice extent; every universal claim keeps its adjacent digit-bearing sweep citation (E-16); OW-3
BOTH-SIDES SEAM LAW on any seam you re-argue; NO unexpanded {placeholder} tokens; every string field ONE
STRING; schema parity with rows_v3 (same 22 keys, same types). SPAN, chunk_index_in_book, parent_collection,
unit_type and confidence are NOT yours unless your orders file explicitly names the field on that row (an
accepted span proposal or a calibration order) — otherwise a finding that would need one is executed only in
prose and REPORTED. The 7-gram gate binds: no cure may create a seven-word run shared by 10+ rows (verify
with ngram7.py --gate 10 --full-ids over rows_v3 with your rows swapped in, in private scratch).
HONEST REPORTING: claude-sonnet-5, effort ORDERED session-default, NOT VERIFIED. M7, other model lanes, A/B
lanes and comparison data FORBIDDEN.

OUTPUT (your assigned file in SP\Jer\spot\micro_<NN>.jsonl): one JSON object per line: the COMPLETE replacement
row (all 22 fields, decision_id and chunk_index_in_book unchanged) plus "_op":"replace"; one line per ordered
row, in order; rows not in your orders never appear. A finding you judge NOT curable as ordered (the cure would
install a false claim, or needs a field you may not touch) is REPORTED with its byte reason, never silently
skipped — the row is still emitted with every other finding cured.

SELF-CHECK before delivering: JSON parses per line; normalize_hebrew_in_json.py dry-run over your file: 0
defects, 0 fixed; every pointed run re-collates at its cited ref (collate.py); run_validator_suite.py over a
private copy (hard members GREEN); ngram7 pooled gate as above.

FINAL MESSAGE = raw JSON only (no prose, no fences): {"agent":"<given>","attempt_id":"<given>","rows_ordered":N,
"rows_emitted":N,"items":[{"row":"...","finding":"<lane:e_class>","action":"cured|reported","reason":"..."}],
"cure_tests":[{"test":"...","result":"..."}],"output":"SP/Jer/spot/micro_<NN>.jsonl"}
