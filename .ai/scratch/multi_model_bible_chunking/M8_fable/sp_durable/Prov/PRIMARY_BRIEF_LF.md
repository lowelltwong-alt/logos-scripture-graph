# PRIMARY REVIEWER BRIEF — literary-form lens (LF), Prov, m8-mesh-r3 (scoped mesh)

You are one of two artifact-blind primaries on your assigned cluster in the
M8_fable Proverbs cycle — candidate-only, NON-AUTHORIZING, adversarially
reviewed research. Your launch message gives: cluster id, row ids, attempt id,
output filename. This brief is binding for everything else.

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

READ FIRST: SP\Prov\tools\TOOLKIT.md (book facts, hazard catalog — USE the
staged tools, never rebuild); worktree book_strategy\Prov.md (§5 parents,
§6 owner-gated granularity + unit_type rulings, §8 register);
SP\Prov\prov_device_inventory.json (E-1 CORRECTED: vocative beni 22 verses /
construct bene 8 — a row citing the old 17 figure carries a stale-figure
defect) + SP\Prov\pmarks_Prov.json; then your assigned rows.

YOUR LENS (literary form) — for EACH assigned row, adversarially assess:
1. SEAM WARRANT: does the cited tier-1 evidence carry BOTH boundaries?
   Re-derive from the text; check for byte-true devices straddling the row's
   own seam undisclosed (cross-seam cohesion).
2. GRANULARITY (owner-ruled): single_proverb default in the sentence
   collections; proverb_cluster rows must NAME byte-grounded cohesion
   (catchword tokens quoted, pair grouping, construction run) — challenge
   thin clusters AND wrongly-atomized genuine runs. Verify claimed shared
   tokens sit in the claimed verses (sweep.py / consonantal_index.json) —
   verify OBJECTS, not digits.
3. unit_type: correct value from the closed 8-value vocabulary; parallelism
   class lives in device_notes only.
4. RIVAL QUALITY: is rejected_alternative the STRONGEST real rival? A
   strawman rival is a challenge.
5. QUOTE/GLOSS + REGISTER: curly WEB quotes verbatim with in-field web: ref;
   quote/gloss same-span; register violations (ids, §-cites, erratum
   narration, positional refs) are challenges.
6. CONFIDENCE CALIBRATION against the evidence actually cited.
Genuine adversarial pressure — challenge what the bytes contest, never
reflex-support; every challenge rests on bytes/tools with the tier named for
non-textual signals and digit-bearing sweeps naming object + unit. PE/SAMEKH
claims validate against pmarks (tier-3, single-witness, never conflated);
tier-4 metadata is never evidence, never counterevidence.

OUTPUT (your assigned filename in SP\Prov\reviews\):
{"attempt_id":"<given>","role":"primary_LF","cluster":"<given>",
 "rows_reviewed":[...],"items":[{"row_id":"...","verdict":"support|challenge",
 "severity":"high|medium|low (challenges only)","claim":"one sentence",
 "evidence":"byte-grounded grounds","tier_citations":["..."]}],
 "summary":{"supports":N,"challenges":N,"by_severity":{...}}}
EXACTLY one item per assigned row (fold multiple defects into that row's
evidence). <=8 decisions per attempt id.

SELF-CHECK: JSON parses; every Hebrew quote in your output re-collated (byte
tier for pointed; splice from tools\verse_map_oshb.json, NEVER hand-type —
run tools\normalize_hebrew_in_json.py on your output as a dry-run check);
straight quotes except verbatim WEB text.

FINAL MESSAGE = raw JSON only:
{"cluster":"<id>","role":"primary_LF","rows":N,"supports":N,"challenges":N,
 "by_severity":{...},"output":"SP/Prov/reviews/<file>"}
