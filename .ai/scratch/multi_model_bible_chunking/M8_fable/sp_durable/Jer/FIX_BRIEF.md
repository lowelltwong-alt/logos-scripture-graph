# FIX BRIEF — Jeremiah bounded fix round after the first postcheck (m8-mesh-r3 + OW-1/OW-2/OW-3/OW-5)

You are a FIX AUTHOR in the M8_fable Jeremiah cycle — candidate-only, NON-AUTHORIZING research. The first
postcheck (opus, independent) returned not_fit with residuals that this bounded round cures. EVERYTHING in
SP\Jer\MICRO_BRIEF.md binds you (read it FIRST), with these overrides:

PATHS: SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
- Corpus (READ-ONLY; your edits go to your OWN output file): SP\Jer\rows_v5.jsonl (275 rows; every row carries
  review_status candidate_review_complete — that field is now IMMUTABLE along with span, chunk_index_in_book,
  parent_collection, unit_type, confidence and every writer_* field).
- Your orders: SP\Jer\spot\orders_fix_<NN>.json (schema jer_fix_orders.v1: per row the current_row from rows_v5,
  the postcheck residual(s) with their byte evidence and proposed cure, and the instruction).
- Your deliverable: SP\Jer\spot\fix_<NN>.jsonl — one COMPLETE replacement row per ordered row, in orders order,
  "_op":"replace", the full 22-field row (rows_v5 schema) — nothing else under SP.
- Open fields: boundary_rationale, strongest_rejected_alternative, device_notes, observed_substrate_signals,
  boundary_evidence_refs, literature_type_guess, strong_or_hebrew_tags_used.

E-15 LAW FOR THIS ROUND (WEB quotes): every quoted WEB run stands VERBATIM inside ONE closed curly pair. When the
translation's own text carries a nested double quotation mark inside the run, the cure is to RE-CUT the run so it
stops before the nested opening mark (and, if the rest is needed, quote it as a second run that opens after the
nested mark), exactly as the Jer.41.6 run was re-cut; never alter the translation's own characters, never leave an
empty pair, never wrap the translation's own unmatched closing mark inside a second pair. Re-cut from
tools\verse_map_web.json, never by hand. E-07 seg-layer law: a parashah/paseq citation is a seg-layer object (MT
key + single-witness disclosure); the word "byte" is collate.py's Hebrew quote-collation tier and never attaches
to a seg-layer citation. E-17 refs law: prose and boundary_evidence_refs agree — a verse range argued in prose is
either mirrored into the refs or restated without the range.

Self-check as in the micro brief (private copy only; the 7-gram gate over rows_v5 with your rows swapped in;
NFD dry-run fixed=0 defects=0; every re-cut WEB run re-verified against verse_map_web.json; run
tools\check_web_quotes.py over your private copy and confirm the ordered rows carry no e15 flag).

FINAL MESSAGE = raw JSON only (no prose, no fences): {"agent":"<given>","attempt_id":"<given>","rows_ordered":N,
"rows_emitted":N,"items":[{"row":"...","finding":"<e_class>","action":"cured|reported","reason":"..."}],
"cure_tests":[{"test":"...","result":"..."}],"output":"SP/Jer/spot/fix_<NN>.jsonl"}
