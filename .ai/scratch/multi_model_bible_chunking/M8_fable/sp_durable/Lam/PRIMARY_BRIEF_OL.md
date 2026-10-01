# PRIMARY REVIEWER BRIEF — original-language lens (OL), Lamentations, m8-mesh-r3 + OW-1..OW-5 (FULL dual-blind mesh)

You are one of two artifact-blind primaries on your assigned cluster in the M8_fable Lamentations cycle —
candidate-only, NON-AUTHORIZING, adversarially reviewed research. Your launch message gives: cluster id,
row ids, attempt id, output filename. This brief is binding for everything else.

PATHS: SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Rows corpus: SP\Lam\draft_rows_combined.jsonl (find your rows by writer_decision_id — the PNN-NNN ids in
your launch message).

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write into it, never write any
receipt, never run git. Your ONLY deliverable is your assigned output file in SP\Lam\reviews\. Private
scratch goes in a uniquely-named subdirectory of YOUR OWN session scratchpad — never in SP\Lam, never at
any scratchpad root; NO debug files anywhere under SP. Scope any self-check or cleanup sweep
(find/ls/glob) to your OWN private scratch directory — never traverse or list SP\Lam\reviews\ or any
shared SP directory (even a filename listing breaches blindness). SP\Lam\reviews\ ALREADY EXISTS — write
your deliverable directly to your assigned path; never run any existence check, ls, dir, or glob against
it, before or after writing. EXACT-PATH LAW: every staged input you need is named by exact path in this
brief or your launch message — address files by those exact paths ONLY; glob, wildcard, or recursive
listing/search of ANY directory outside your own private scratch is banned (SP, the worktree,
everywhere); a path you cannot resolve is REPORTED in your final message, never searched for. FORBIDDEN
LANES (never read, list, or preview): any path under
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\ belonging to M1_cursor,
M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55, M5_gemini_thinking, M6_fable5, M7_sol, or
comparison\; every other book's lane under SP (SP\Jer etc.) is a hard boundary.

BLINDNESS: do NOT open, read, or list-preview ANYTHING in SP\Lam\reviews\ (other reviews exist there).
Your review is fully independent of the LF primary. Do not consult other clusters' rows beyond the
immediate neighbors of your rows' spans (neighbor verses are fair game — they are the seam evidence).
Register: NO strategy §-citations, decision-ids, reviewer names, or tool filenames in your packet prose —
state grounds by content.

READ FIRST: SP\Lam\tools\TOOLKIT.md (MANDATORY pre-read — book facts, identity proof, the acrostic
spine, hazard catalog; USE the staged tools, never rebuild); the strategy file at its EXACT path
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Lam.md (acrostic
+ voice/address evidence policy, five-poem parent architecture, 8-value vocabulary + ruled granularity,
low-confidence forecast, register rules); SP\Lam\lam_device_inventory.json + SP\Lam\pmarks_Lam.json +
SP\Lam\web_mt_offset_map.json + SP\Lam\tools\acrostic_spine.json; then your rows.

CRITICAL BOOK FACTS: Lamentations is an IDENTITY book (byte-proven): WEB = MT verse-for-verse,
22/22/66/22/22 = 154, NO zone, NO split, Lam.N.0 always invalid; Hebrew throughout (any Aramaic verse
label is a defect). THE ACROSTIC SPINE: chs 1, 2, 4 one verse per letter; ch 3 three verses per letter
(uniform triplets); ch 5 22 verses NOT acrostic; ch 1 ayin-then-pe (standard), chs 2, 3, 4 PE-THEN-AYIN
(reversed) — a byte fact never to be "corrected". A row seam in chs 1, 2, 4 falls on a letter boundary;
in ch 3 on a TRIPLET boundary unless a disclosed tier-1 reason cuts inside; every ch 1-4 row discloses
the letters its span covers. Parashah marks: 5 PE + 84 SAMEKH over 89 verses (EVERY verse of chs 1-4
marked; PE at 1:22, 2:22, 3:66, 4:22; ch 5 only the PE at 5:18) — TIER-3 WEAK single-witness
corroboration in the Writings, disclosed at every span-relevant verse, PE never conflated with SAMEKH,
absence never counterevidence. K/Q 22 notes / 20 verses (doubled 4:3, 5:7); paseq 11 / 10 verses
count-only; NO special letters, NO selah (fabrications). WEB quote fidelity judges against the STAGED
FOLDED text (tools\verse_map_web.json) — zero continuation folds exist in Lam.

YOUR LENS (original language — read the OSHB bytes) — for EACH assigned row:
1. EVERY QUOTED HEBREW RUN: re-collate against its cited ref with collate.py — pointed runs must reach
   BYTE tier (nfd = copy-degradation defect; unpointed = skeleton grade, must be labeled). A Hebrew claim
   with no quoted form is insufficient engagement. SHELL-TRANSIT HAZARD: pass pointed Hebrew via
   file/JSON splices, never through shell arguments.
2. ACROSTIC VERIFICATION (the byte arm of the spine policy): for every verse in the row's span, the
   verse-initial consonant of the skeleton (INCLUDING any prefix letter — that is how the acrostic is
   built) must match the pinned sequence (tools\acrostic_spine.json; verse_map_oshb.json carries
   acrostic_letter / acrostic_position per verse): ch 1 ayin-then-pe, chs 2, 3, 4 PE-THEN-AYIN, ch 3 in
   uniform triplets, ch 5 no acrostic. A row that names a wrong letter, a wrong order, a triplet cut
   without a disclosed tier-1 reason, or an acrostic claim about ch 5 is a challenge; a ch 1-4 row with
   no letter disclosure is a challenge.
3. VOICE + ADDRESS FORM VERIFICATION: every speaker/addressee claim must stand on the pointed bytes —
   person, number and gender of finite verbs and pronominal suffixes (the 1cs "I" of the geber, the 1cp
   "we/us" of the communal sections, the 2fs address to the personified city, the 3fs description of
   the city as widow/daughter, the 2ms address to YHWH), imperatives (zekhor / reeh / habitah forms at
   their sites), vocatives and apostrophes at the claimed byte positions. No morphology layer is
   staged — form-class claims stand on the pointed bytes and both witnesses' renderings; an unverifiable
   form claim is held, not asserted. There is NO messenger formula and NO divine speech in the book: any
   koh-amar / neum / word-event claim is a fabrication.
4. CLUSTER/COHESION EVIDENCE: verify claimed refrain/shared-token/construction evidence directly from
   consonantal_index.json; re-run sweeps yourself (sweep.py — finals-normalized; counts are VERSE counts
   unless --tokens). Hazard traps (all byte-verified in this book): PREFIX TOLERANCE is a per-length test
   behind exactly one of vav/he/bet/lamed/kaf/mem/shin, never a blind stripper; bat- formulas are
   two-token phrase tests (bat-Tsiyon 8 vv, bat-ammi 5, bat-Yehudah 3, bat-Yerushalam 2, betulat-bat 2,
   bat-Edom 2) — "bat" alone is not a formula; ein menachem contiguous at 1:9, 1:17, 1:21 vs the
   menachem family in 5 verses of ch 1 — name which you count; the bare el token collides with the
   preposition (9 vv; never a divine-name count); af = anger vs "also" (4 vv token census, a review
   list); defective spellings live (betulot without vav at 5:11) — sweep per attested spelling;
   eikhah verse-initial exactly 1:1, 2:1, 4:1 (the token stands non-initially once more); ani ha-gever
   only at 3:1 (ani token 4 vv); YHWH 32 vv / Adonai 13 vv (ch 2: 7 each) — WEB renders Adonai "the
   Lord" and YHWH "Yahweh": digits name their Hebrew object, never the English. Verify OBJECTS, not
   digits.
5. SEAM EVIDENCE IN THE HEBREW: claimed openers/vocatives/imperatives/refrains at the claimed byte
   positions? Byte-true devices straddling the row's own seam undisclosed (a refrain closing the unit
   before the seam — REFRAINS CLOSE UNITS, weigh BOTH sides; a ch-3 triplet cut; the bat-address chain;
   the petition chain of ch 5)? The PE marks at 1:22, 2:22, 3:66, 4:22, 5:18 — byte-check any engagement.
6. TRANSLATION-DEPENDENT ARGUMENTS: anything that works only in English (WEB rendering choices, "How"
   capitalization, English wordplay, sentence punctuation, the WEB paragraph/poetry layout) and not in
   the Hebrew is a challenge (E-23: translation punctuation / paragraphing / capitalization never drive
   or corroborate a boundary).
7. K/Q + MARKS + DISCLOSURE SYMMETRY: spans touching any of the 22 K/Q notes / 20 verses must disclose
   (doubled-note verses 4:3, 5:7; check pmarks BEFORE any counting or slicing claim in a K/Q verse).
   PE/SAMEKH validate against pmarks (5 PE + 84 SAMEKH over 89 verses; EVERY verse of chs 1-4 marked,
   PE at the four poem ends; ch 5 only the PE at 5:18; tier-3 single-witness, never conflated; absence
   never counterevidence; span-relevant symmetry — one engaged mark owes the others in the span, and
   in chs 1-4 EVERY verse in the span is a marked verse). Paseq count-only (11 segs / 10 verses; position
   claims unsourceable). FABRICATIONS: selah, reversed/inverted nun, suspended letters, ALL large- and
   small-letter claims (WLC Lam carries NO special-letter seg of any class). The OSHB KJV-variance layer
   is inventory only.
8. LANGUAGE LABELS + CROSS-TRADITION: Lam is Hebrew throughout (0 A-prefixed morph codes) — any
   Aramaic verse label is a defect. ALL cross-tradition material (the LXX prose Jeremiah-ascription
   before 1:1, 4QLam/3QLam/5QLam, versions, the Megillot setting, Jeremianic authorship) is metadata in
   prose only — never in refs, never boundary evidence, never counterevidence.
Genuine adversarial pressure — challenge what the bytes contest; every challenge carries byte-grounded
evidence, tier named, digit-bearing sweeps naming object + unit. E-16: a tier label NEVER substitutes for
an exclusivity sweep. E-02 IS HARD: whole-poem spans above medium_low, or lacking frontier flag + cap
disclosure, are calibration challenges.
DECLARED-FP QUEUES (pressure-test them): SP\Lam\flags_by_row.json lists writer-declared heuristic false
positives. For every entry touching YOUR rows: CONFIRM the disposition or REFUTE it (a real defect waved
through) — a refutation is a challenge on that row with the evidence stated. Do NOT spend challenges on
cross-row phrasing convergence (the 7-gram gate handles it); DO challenge factual defects inside any
such sentence.

OUTPUT (your assigned filename in SP\Lam\reviews\):
{"attempt_id":"<given>","role":"primary_OL","cluster":"<given>",
 "rows_reviewed":[...],"items":[{"row_id":"...","verdict":"support|challenge",
 "severity":"high|medium|low (challenges only)","claim":"one sentence",
 "evidence":"byte-grounded grounds","tier_citations":["..."]}],
 "summary":{"supports":N,"challenges":N,"by_severity":{...}}}
EXACTLY one item per assigned row (fold multiple defects into that row's evidence). <=8 decisions per
attempt id.

SELF-CHECK: JSON parses; every Hebrew quote in your output re-collated (byte tier for pointed; splice
from tools\verse_map_oshb.json, NEVER hand-type — run tools\normalize_hebrew_in_json.py on your output as
a dry-run check, over a private copy); straight quotes except verbatim WEB text; no register violations
in your own packet prose. Model/effort as ordered in your launch message; effort ORDERED, NOT VERIFIED
(recorded honestly).

INFRASTRUCTURE: if you are resumed after a connection loss, FIRST check whether your deliverable already
exists and validate it rather than re-running work. Trust disk state only.

FINAL MESSAGE = raw JSON only:
{"cluster":"<id>","role":"primary_OL","rows":N,"supports":N,"challenges":N,
 "by_severity":{...},"output":"SP/Lam/reviews/<file>"}
