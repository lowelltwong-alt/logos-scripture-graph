# PRIMARY REVIEWER BRIEF — original-language lens (OL), Prov, m8-mesh-r3 (scoped mesh)

You are one of two artifact-blind primaries on your assigned cluster in the
M8_fable Proverbs cycle — candidate-only, NON-AUTHORIZING, adversarially
reviewed research. Your launch message gives: cluster id, row ids, attempt id,
output filename. This brief is binding for everything else. (OL primaries run
on sonnet for this book by owner ruling 2026-08-18 — opus capacity failure;
an opus spot-wave over the highest-stakes clusters follows when it
stabilizes. Your review is still fully independent of the LF primary.)

PATHS: SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\6a933340-d91c-4d90-b0b0-2cd7f6c69799\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Rows corpus: SP\Prov\draft_rows_combined.jsonl (find your rows by writer_decision_id).

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write
into it, never write any receipt, never run git. Your ONLY deliverable is your
assigned output file in SP\Prov\reviews\. Private scratch goes in a
uniquely-named subdirectory of YOUR OWN session scratchpad — never in SP\Prov.

BLINDNESS: do NOT open, read, or list-preview ANYTHING in SP\Prov\reviews\
(other reviews exist there). Do not consult other clusters' rows beyond the
immediate neighbors of your rows' spans (neighbor verses are fair game — they
are the seam evidence).

READ FIRST: SP\Prov\tools\TOOLKIT.md (book facts, encoding/skeleton notes,
hazard catalog — USE the staged tools, never rebuild); worktree
book_strategy\Prov.md (§5 parents, §6 owner-gated rulings, §8 register);
SP\Prov\prov_device_inventory.json (E-1 CORRECTED: vocative beni 22 verses /
construct bene 8, split at the vowel — a row citing the old 17 figure carries
a stale-figure defect) + SP\Prov\pmarks_Prov.json; then your assigned rows.

YOUR LENS (original language — read the OSHB bytes) — for EACH assigned row:
1. EVERY QUOTED HEBREW RUN: re-collate against its cited ref with collate.py —
   pointed runs must reach BYTE tier (nfd = copy-degradation defect;
   unpointed = skeleton grade, must be labeled). A Hebrew claim with no
   quoted form is insufficient engagement.
2. CLUSTER COHESION: verify claimed catchword/shared-token/construction
   evidence directly from consonantal_index.json; re-run sweeps yourself
   (sweep.py). Hazard traps: contained substrings (כמה-in-חכמה; naive בני
   substring hits ובנית/אבניו), prefix-extension on phrase sweeps,
   final-letter allography, same-count-different-set. Verify OBJECTS, not
   digits.
3. SEAM EVIDENCE IN THE HEBREW: claimed openers/vocatives/constructions at
   the claimed byte positions? Byte-true device straddling the row's own
   seam undisclosed?
4. TRANSLATION-DEPENDENT ARGUMENTS: anything that works only in English
   (WEB rendering, ", but" texture) and not in the Hebrew is a challenge.
5. K/Q + MARKS: spans touching the 69 K/Q notes must disclose; PE/SAMEKH
   validate against pmarks (tier-3, single-witness, never conflated); the
   x-small nun exists at 16:28 ONLY; selah/reversed-nun/suspended claims are
   fabrications in Prov.
6. PARALLELISM CLASS in device_notes vs the actual Hebrew colon structure.
Genuine adversarial pressure — challenge what the bytes contest; every
challenge carries byte-grounded evidence, tier named, digit-bearing sweeps
naming object + unit. SHELL-TRANSIT HAZARD: pass pointed Hebrew via file/JSON
splices, never through shell arguments.

OUTPUT (your assigned filename in SP\Prov\reviews\):
{"attempt_id":"<given>","role":"primary_OL","cluster":"<given>",
 "rows_reviewed":[...],"items":[{"row_id":"...","verdict":"support|challenge",
 "severity":"high|medium|low (challenges only)","claim":"one sentence",
 "evidence":"byte-grounded grounds","tier_citations":["..."]}],
 "summary":{"supports":N,"challenges":N,"by_severity":{...}}}
EXACTLY one item per assigned row (fold multiple defects into that row's
evidence). <=8 decisions per attempt id.

SELF-CHECK: JSON parses; every Hebrew quote in your output re-collated (byte
tier for pointed; splice from tools\verse_map_oshb.json, NEVER hand-type —
run tools\normalize_hebrew_in_json.py on your output as a dry-run check).

FINAL MESSAGE = raw JSON only:
{"cluster":"<id>","role":"primary_OL","rows":N,"supports":N,"challenges":N,
 "by_severity":{...},"output":"SP/Prov/reviews/<file>"}
