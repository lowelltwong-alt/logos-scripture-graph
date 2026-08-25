# PRIMARY REVIEWER BRIEF — original-language lens (OL), Eccl, m8-mesh-r3 (FULL dual-blind mesh)

You are one of two artifact-blind primaries on your assigned cluster in the
M8_fable Ecclesiastes cycle — candidate-only, NON-AUTHORIZING, adversarially
reviewed research. Your launch message gives: cluster id, row ids, attempt id,
output filename. This brief is binding for everything else. Your review is
fully independent of the LF primary.

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

READ FIRST: SP\Eccl\tools\TOOLKIT.md (book facts, encoding/skeleton notes,
hazard catalog — USE the staged tools, never rebuild); worktree
book_strategy\Eccl.md (§5 parents, §6 owner-gated rulings, §8 register);
SP\Eccl\eccl_device_inventory.json + SP\Eccl\pmarks_Eccl.json; then your
assigned rows.

CRITICAL BOOK FACT: Eccl is NOT an identity book — MT 4:17 = WEB 5:1 and
MT 5:1-19 = WEB 5:2-20 (byte-proven). oshb: refs and pmarks are MT; row
spans and web: refs are WEB. Use eccl_lib/collate.py (they crosswalk
internally); never hand-assume numbering equivalence in chs 4-5.

YOUR LENS (original language — read the OSHB bytes) — for EACH assigned row:
1. EVERY QUOTED HEBREW RUN: re-collate against its cited ref with collate.py —
   pointed runs must reach BYTE tier (nfd = copy-degradation defect;
   unpointed = skeleton grade, must be labeled). A Hebrew claim with no
   quoted form is insufficient engagement.
2. CROSSWALK VERIFICATION (offset zone): for WEB ch-5 rows, verify the
   dual-cited MT refs actually carry the claimed Hebrew (the arithmetic is
   machine-checked; YOU verify the CONTENT lands on the right verse). Any
   argument that reads MT ch-5 bytes under a same-numbered WEB ref is a
   challenge.
3. CLUSTER/COHESION EVIDENCE: verify claimed catchword/shared-token/
   construction evidence directly from consonantal_index.json; re-run
   sweeps yourself (sweep.py). Hazard traps (all byte-verified in this
   book): שבע THREE-way homograph (satisfied/swear/seven), כמה-in-חכמה
   (22/22 false), hevel digit-blending (25 bare-token verses vs 30 family
   verses vs 38 tokens), resh-ayin family (רעות/רעיון/רע/shepherd), עת
   family (bare vs suffixed בעתו/עתו; עתה is ZERO in Eccl), ירא
   prefix-extension, דברי header-vs-genitive (only 1:1 is a header), קהלת
   TWO spellings (plene definite הקוהלת at 12:8 only), טוב-מ
   phrase-extension. Verify OBJECTS, not digits.
4. SEAM EVIDENCE IN THE HEBREW: claimed openers/vocatives/formulas at the
   claimed byte positions? (amar-qohelet at 1:2, 7:27 — FEMININE אמרה —
   and 12:8 only; qohelet 7 sites total.) Byte-true device straddling the
   row's own seam undisclosed (hevel / tachat-hashemesh refrains)?
5. TRANSLATION-DEPENDENT ARGUMENTS: anything that works only in English
   (WEB rendering, "better" texture, ", but") and not in the Hebrew is a
   challenge.
6. K/Q + MARKS: spans touching the 12 K/Q notes must disclose (MT 4:8,
   4:17 — the seam verse, inline unpointed ketiv — 5:8, 5:10, 5:17, 6:10,
   7:22, 9:4, 10:3, 10:10, 10:20, 12:6); PE/SAMEKH validate against pmarks
   (1 PE at MT 1:11 + 3 SAMEKH at 3:1/3:8/9:10 ONLY; tier-3,
   single-witness, never conflated); selah / reversed-nun / suspended /
   ANY small-or-large-letter claims are fabrications in Eccl; paseq is
   count-only (11 verses).
7. LANGUAGE LABELS: all 222 MT verses are Hebrew (2,999 morph codes all
   H-prefixed) — an Aramaic VERSE label is a defect; LBH/Aramaism/Persian-
   loan influence discussion is legitimate.
Genuine adversarial pressure — challenge what the bytes contest; every
challenge carries byte-grounded evidence, tier named, digit-bearing sweeps
naming object + unit. SHELL-TRANSIT HAZARD: pass pointed Hebrew via
file/JSON splices, never through shell arguments.

OUTPUT (your assigned filename in SP\Eccl\reviews\):
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
 "by_severity":{...},"output":"SP/Eccl/reviews/<file>"}
