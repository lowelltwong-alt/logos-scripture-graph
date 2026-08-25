# PRIMARY REVIEWER BRIEF — literary-form lens (LF), Eccl, m8-mesh-r3 (FULL dual-blind mesh)

You are one of two artifact-blind primaries on your assigned cluster in the
M8_fable Ecclesiastes cycle — candidate-only, NON-AUTHORIZING, adversarially
reviewed research. Your launch message gives: cluster id, row ids, attempt id,
output filename. This brief is binding for everything else.

PATHS: SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\b7303917-7c09-45b6-ad0c-a5b8ab5d6eaa\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Rows corpus: SP\Eccl\draft_rows_combined.jsonl (find your rows by writer_decision_id).

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write
into it, never write any receipt, never run git. Your ONLY deliverable is your
assigned output file in SP\Eccl\reviews\. Private scratch goes in a
uniquely-named subdirectory of YOUR OWN session scratchpad — never in SP\Eccl.
FORBIDDEN LANES: any M1_cursor/ M2_claude_sonnet5/ M3_claude_frontier/
M4_codex_gpt55/ M5_gemini_thinking/ M6_fable5/ M7_sol/ or comparison/ path.

BLINDNESS: do NOT open, read, or list-preview ANYTHING in SP\Eccl\reviews\
(other reviews exist there). Do not consult other clusters' rows beyond the
immediate neighbors of your rows' spans (neighbor verses are fair game — they
are the seam evidence).

READ FIRST: SP\Eccl\tools\TOOLKIT.md (book facts — Eccl is NOT an identity
book: MT 4:17 = WEB 5:1, MT 5:1-19 = WEB 5:2-20; hazard catalog; USE the
staged tools, never rebuild); worktree book_strategy\Eccl.md (§5 3-parent
frame architecture, §6 owner-gated 7-value vocabulary + hybrid-atomic
rulings, §8 register); SP\Eccl\eccl_device_inventory.json +
SP\Eccl\pmarks_Eccl.json; then your assigned rows.

YOUR LENS (literary form) — for EACH assigned row, adversarially assess:
1. SEAM WARRANT: does the cited tier-1 evidence carry BOTH boundaries?
   Re-derive from the text; check for byte-true devices straddling the row's
   own seam undisclosed (cross-seam cohesion — the hevel / tachat-hashemesh
   refrains and the chs 2-3 catchword density make this LIVE).
2. FRAME + PARENTS (owner-ruled): rows never straddle Eccl.1.11|1.12 or
   Eccl.12.7|12.8; parent_collection must be the correct F1/M/F2 value.
3. GRANULARITY (owner-ruled): single_saying default in 7:1-14 and
   9:17-10:20; saying_cluster rows must NAME byte-grounded cohesion
   (anaphora runs like the 7:1-8 tov openers, catchword tokens quoted,
   construction runs) — challenge thin clusters AND wrongly-atomized genuine
   runs. Verify claimed shared tokens sit in the claimed verses (sweep.py /
   consonantal_index.json) — verify OBJECTS, not digits.
4. unit_type: correct value from the closed 7-value vocabulary
   (frame_narration, monologue_unit, wisdom_poem, list_catalogue,
   admonition_unit, single_saying, saying_cluster); operative-category
   deviations need the one-sentence device_notes disclosure; the 3:1-8
   catalogue is ONE list_catalogue row by owner ruling; parallelism class
   lives in device_notes only.
5. RIVAL QUALITY: is strongest_rejected_alternative the STRONGEST real
   rival? A strawman rival is a challenge.
6. QUOTE/GLOSS + REGISTER: curly WEB quotes verbatim with in-field web: ref
   (folds at WEB 7:8 and 10:14 — quotes across them must still be verbatim
   against the folded verse text); quote/gloss same-span; register
   violations (ids, §-cites, erratum narration, positional refs, tool
   filenames) are challenges.
7. OFFSET-ZONE DISCIPLINE (WEB ch 5 rows): duals/qualifiers present and
   arithmetically coherent with the prose's claims; any argument that
   silently treats WEB and MT ch-5 numbers as the same space is a challenge.
8. CONFIDENCE CALIBRATION against the evidence actually cited.
Genuine adversarial pressure — challenge what the bytes contest, never
reflex-support; every challenge rests on bytes/tools with the tier named for
non-textual signals and digit-bearing sweeps naming object + unit. PE/SAMEKH
claims validate against pmarks (1 PE at MT 1:11 + 3 SAMEKH at MT 3:1/3:8/
9:10 ONLY; tier-3, single-witness, never conflated); NO selah, NO
reversed/suspended nun, NO small/large letters exist in WLC Eccl — such
claims are fabrications; tier-4 metadata is never evidence, never
counterevidence.

OUTPUT (your assigned filename in SP\Eccl\reviews\):
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
 "by_severity":{...},"output":"SP/Eccl/reviews/<file>"}
