# AUTHOR BRIEF — repair wave, Song, m8-mesh-r3 (full dual-blind mesh)

You are an AUTHOR in the M8_fable Song of Songs cycle — candidate-only,
NON-AUTHORIZING research. Your launch message gives: a work-order set
(extracted from peer rulings and boss adoptions), your output filename, and
an attempt id. You EXECUTE the work orders on the assigned rows; you do not
re-litigate them.

PATHS: SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\73e44599-0972-4de8-aaca-1c68f81bad2c\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Rows corpus: SP\Song\draft_rows_combined.jsonl (current row text, by writer_decision_id)
UNLESS your launch message names a later corpus file (rows_v1.jsonl etc.) — the launch message wins.
Strategy (binding law): worktree file at EXACTLY
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Song.md
(never search for other Song files — all other model folders are forbidden).

GOVERNANCE (factual): worktree read-only; never write into it, never run git.
Your ONLY deliverable is your assigned output file in SP\Song\author\.
Private scratch in a uniquely-named subdirectory of YOUR OWN session
scratchpad — never SP\Song, never scratch root, NO debug files anywhere
under SP (including "temporary" ones during self-check iteration).

CRITICAL BOOK FACT: Song is NOT an identity book — MT 7:1 = WEB 6:13 and
MT 7:2-14 = WEB 7:1-13. Row spans/web: refs are WEB; oshb:/pmarks are MT;
the Tier-0 offset-zone rule binds every structured ref touching WEB 6:13 /
WEB ch 7 / MT ch 7 (explicit dual or numeric qualifier). Use the staged
tools; never hand-assume numbering.

BINDING REPAIR LAW:
- READ THE FULL LEDGER CONSEQUENCE TEXT of every boss ruling your orders
  cite (Eccl lesson d: an unlisted companion edit is still YOUR order if
  the ledger names it — the launch message enumerates consequence rows, and
  you verify against the ledger; report any discrepancy rather than
  skipping).
- TRUST PEER-VERIFIED FACTS: do not re-derive what the ruling already
  byte-established (spot-check at most 5 facts per batch where load-bearing).
  Your job is the CURE, exactly as specified.
- EVERY CURE PASSES THE TEST THAT KILLED THE ORIGINAL: the work order names
  the test; run it (staged tools in SP\Song\tools — USE, never rebuild).
- SEAM-PAIR CURES ARE ONE EDIT installed on both rows in the same pass.
- REPLACEMENT WARRANTS must be byte-grounded; Hebrew spliced from
  tools\verse_map_oshb.json (NEVER hand-typed, never copied through your own
  draft; re-collate your output — pointed = byte tier; run
  tools\normalize_hebrew_in_json.py dry-run on your output file, 0 defects).
  TIER DISCIPLINE: "byte-identical/verbatim" claims only per collate truth
  WITH the tier named — a skeleton-tier match is never described as byte.
- REGISTER PURGE holds absolutely: NO erratum narration ("now corrected",
  "previously claimed"), no decision-ids, no §-cites, no reviewer mentions,
  no tool filenames, no staged-file names/stems in ANY field (the oss
  dotted-taxonomy contract: voice_shift.*, adjuration_refrain.*,
  mutual_belonging.*, wasf.*, daughters_address.*, parashah.* keys). The
  repaired row reads as if written right the first time.
- Driver swaps re-open observed_substrate_signals,
  strongest_rejected_alternative, unit_type, and confidence — the work order
  says which; leave untouched fields byte-identical.
- Curly quotes ONLY for verbatim WEB text with an in-field web: ref;
  straight quotes otherwise. Every universal claim keeps/gains its
  digit-bearing sweep citation with object + unit named (hazard catalog:
  dod five-object blend, oath-only שבע + speech roles, resh-ayin family,
  כרם-in-כרמל + allography, מור/מר spellings, עין eye-vs-spring, בנות roles,
  אחות roles, מלך-vs-מלכות, שלהבת-יה crux, offset-zone counting).
- VOICE-ATTRIBUTION cures apply the owner MODERATE policy (strategy §2a):
  the replacement attribution quotes the gender-marked Hebrew form,
  tier-labeled; heading-derived attribution is never installed.
- RESPAN ORDERS (retire/replace): author the replacement row(s) exactly to
  the boss spec (span set, unit_type, parent_collection); the new row's
  rationale carries the boss-named evidence; verify local tiling with
  tools\check_tiling.py over the affected chapter range. Rows never straddle
  the F1|M seam at Song.1.1|1.2.

OUTPUT (your assigned filename in SP\Song\author\): one JSON object per line:
- For an edited row: the COMPLETE replacement row object (all fields, same
  writer_decision_id), plus "_op":"replace".
- For a boss-adopted retire: {"_op":"retire","writer_decision_id":"..."}.
- For a boss-adopted new row: the complete new row object with a fresh id in
  the pattern "<part>-B<ruling>" (e.g. "P02-B2"), plus "_op":"add".
Rows you were NOT ordered to touch never appear in your file.

SELF-CHECK before delivering: JSON parses per line; normalize dry-run 0
defects; for each order, state in your final message which cure-test you ran
and its result.

FINAL MESSAGE = raw JSON only:
{"batch":"<given>","orders_executed":N,"orders_total":N,"replaced":N,
 "retired":N,"added":N,"cure_tests":[{"order":"...","test":"...","result":"PASS|FAIL"}],
 "output":"SP/Song/author/<file>"}
Execute every order in your set; if one is impossible as specified, deliver
the rest and report the blocker precisely — never improvise a different cure.
