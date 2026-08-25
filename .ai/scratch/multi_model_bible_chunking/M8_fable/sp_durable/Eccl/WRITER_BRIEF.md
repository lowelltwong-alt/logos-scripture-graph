# WRITER BRIEF — draft chunk rows, Eccl, m8-mesh-r3 (full dual-blind cycle)

You are one of three part-writers in the M8_fable Ecclesiastes cycle —
candidate-only, NON-AUTHORIZING, adversarially reviewed research. Your launch
message gives: part id (pNN), WEB verse range, verse count, attempt id, output
filename. This brief is binding for everything else.

PATHS (absolute; lesson-c hygiene):
SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\b7303917-7c09-45b6-ad0c-a5b8ab5d6eaa\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Strategy (BINDING) = C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Eccl.md
Toolkit = SP\Eccl\tools\ (TOOLKIT.md FIRST — book facts + hazard catalog; USE the staged tools, never rebuild)
Inventories = SP\Eccl\eccl_device_inventory.json, SP\Eccl\pmarks_Eccl.json, SP\Eccl\web_mt_offset_map.json
Substrate slices for your range = SP\Eccl\span_features.jsonl, SP\Eccl\risk_signals.jsonl, SP\Eccl\book_observation.jsonl

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write
into it, never write any receipt, never run git. Your ONLY SP write is your
one deliverable: SP\Eccl\writer\<given filename>. Private scratch goes in a
uniquely-named subdirectory of YOUR OWN session scratchpad — never in
SP\Eccl, never at any scratchpad root; NO debug files anywhere under SP.
Existence-checking your own output file is permitted. FORBIDDEN LANES (never
read, list, or preview): any path under
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\ belonging
to M1_cursor, M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55,
M5_gemini_thinking, M6_fable5, M7_sol, or comparison\.

CRITICAL BOOK FACT: Eccl is NOT an identity book — MT 4:17 = WEB 5:1 and
MT 5:1-19 = WEB 5:2-20 (byte-proven; TOOLKIT "Numbering"). Row spans and
bare/web: refs are WEB numbering; oshb:/pmarks are MT. The Tier-0
OFFSET-ZONE RULE binds: any structured ref touching WEB ch 5 or MT
4:17-5:19 carries an explicit dual or numeric qualifier. Use
eccl_lib.web_to_mt()/mt_to_web() — never hand-assume.

TASK: tile your assigned WEB range EXACTLY (no gaps, no overlaps — verify
with tools\check_tiling.py FILE --range <your range>) into chunk rows per
the strategy: §5 parents (rows NEVER straddle Eccl.1.11|1.12 or
Eccl.12.7|12.8), §6 unit_type vocabulary (7 values, closed; operative-
category law: deviations allowed per-bytes with a one-sentence disclosure
in device_notes) and granularity (single_saying default in 7:1-14 and
9:17-10:20; saying_cluster only with byte-named cohesion), §7 low-confidence
posture (hold honestly at medium_low/low with bespoke rationale rather than
stopping), §8 register (binding verbatim).

ROW SCHEMA (JSONL, one row per line, EXACTLY these fields):
decision_id = "PNN-NNN" (your part, 3-digit ordinal in canonical order);
book = "Eccl"; model_id = "M8_fable"; chunk_index_in_book = ordinal within
your part (int; assembly renumbers); span = "Eccl.a.b-Eccl.c.d" (WEB, full
X-X form incl. single verses); boundary_rationale (prose: curly quotes for
WEB text ONLY with an inline web: ref in the SAME field; pointed Hebrew
spliced from tools\verse_map_oshb.json with its oshb: ref and tier named —
NEVER hand-typed, NEVER copied through your own draft);
boundary_evidence_refs (structured refs; offset-zone rule; parashah/paseq/
K-Q/small-letter claims validate against pmarks — mind the fabrication
classes: NO selah, NO reversed/suspended nun, NO small/large letters exist
in Eccl); strongest_rejected_alternative (one sentence; optional second
ONLY for a mandated rival); literature_type_guess (short free phrase);
confidence in {high, medium, medium_low, low};
strong_or_hebrew_tags_used = false; wj_or_red_letter_considered = "not
applicable in the OT substrate"; frontier_flag_considered (bool — true when
the row raises a genuine frontier question); non_authorizing = true;
review_status = "draft"; parent_collection in {"F1 Eccl.1.1-Eccl.1.11",
"M Eccl.1.12-Eccl.12.7", "F2 Eccl.12.8-Eccl.12.14"}; unit_type (7-value
vocabulary); writer_part = "pNN"; writer_decision_id = decision_id;
writer_attempt_id = <given>; observed_substrate_signals (list of short
strings naming substrate signals you actually consulted for this row's
zone, from the staged slices; empty list if none informed the row);
device_notes (texture, refrain/catchword observations, deviation
disclosures; parallelism classes live HERE, never in unit_type).

EVIDENCE DISCIPLINE: tier-1 text signals drive boundaries (discourse
frames, refrain/inclusio, vocative/imperative onsets, scene shifts,
list/register formulas); parashah = tier-3 corroboration only,
single-witness disclosed, PE never conflated with SAMEKH, absence never
counterevidence; tier-4 metadata never evidence. Every universal claim
(only/never/first/last/sole/densest/unique...) carries an adjacent
DIGIT-BEARING sweep citation naming the swept OBJECT and UNIT — read the
TOOLKIT hazard catalog before trusting any short-token digit. "(sweep: N
verses)" is the one sanctioned shorthand. Cross-seam cohesion: a byte-true
device straddling your row's own seam argues continuity against the row
unless disclosed.

SELF-CHECK (MANDATORY before delivering; deliver only hard-GREEN):
1. PYTHONIOENCODING=utf-8 python SP\Eccl\tools\check_tiling.py <your file> --range <your range>
2. PYTHONIOENCODING=utf-8 python SP\Eccl\tools\run_validator_suite.py <your file>
   — fix every RED and every fixable flag; re-run until hard-GREEN. A flag
   you believe is a true-but-heuristic false positive: leave it, note it in
   your final message.
3. Re-collate every Hebrew quote in your own output (normalize dry-run is
   part of the suite; cure nfd degradation with
   normalize_hebrew_in_json.py --write, then re-run the suite).

ERRATA: if your byte re-derivation contradicts a staged inventory or
strategy figure, do NOT put the dispute in row prose — record it in your
final message as an erratum with the bytes. The pipeline credits errata.

FINAL MESSAGE = raw JSON only:
{"part":"pNN","attempt_id":"<given>","rows":N,"verses":N,
 "unit_type_spread":{...},"confidence_spread":{...},
 "holds_or_notes":["..."],"errata":["..."],"suite":"hard-GREEN",
 "output":"SP/Eccl/writer/<file>"}
