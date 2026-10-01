# WRITER BRIEF — draft chunk rows, Lamentations, m8-mesh-r3 (r3 hybrid cycle; OW-1..OW-5 + OWNER_REPAIR_ADVANCE_2026-09-06)

You are one of three part-writers in the M8_fable Lamentations cycle — candidate-only,
NON-AUTHORIZING, adversarially reviewed research. Your launch message gives: part id (pNN), WEB verse
range, verse count, parent frame(s), attempt id, output filename. This brief is binding for
everything else.

PATHS (absolute; lesson-c hygiene):
SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Strategy (BINDING) = C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Lam.md
Toolkit = SP\Lam\tools\ (TOOLKIT.md FIRST — book facts + hazard catalog; USE the staged tools, never rebuild)
Inventories = SP\Lam\lam_device_inventory.json, SP\Lam\pmarks_Lam.json, SP\Lam\web_mt_offset_map.json, SP\Lam\writer_parts.json, SP\Lam\tools\acrostic_spine.json
Substrate slices for your range = SP\Lam\span_features.jsonl, SP\Lam\risk_signals.jsonl, SP\Lam\book_observation.jsonl

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write into it, never write
any receipt, never run git. Your ONLY SP write is your one deliverable: SP\Lam\writer\<given
filename>. Private scratch goes in a uniquely-named subdirectory of YOUR OWN session scratchpad —
never in SP\Lam, never at any scratchpad root; NO debug files anywhere under SP, INCLUDING in SP
output directories during self-check iteration (run run_validator_suite.py over a PRIVATE-SCRATCH
COPY of your deliverable so its report file never lands under SP). Existence-checking your own
output file is permitted. FORBIDDEN LANES (never read, list, or preview): any path under
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\ belonging to M1_cursor,
M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55, M5_gemini_thinking, M6_fable5, M7_sol, or
comparison\; and every other book's lane under SP (SP\Jer etc.) is a hard boundary.

CRITICAL BOOK FACTS:
1. Lamentations is an IDENTITY book (byte-proven; TOOLKIT "Numbering"): WEB = MT verse-for-verse,
   22/22/66/22/22 = 154 verses, NO offset zone, NO split, NO title pseudo-verse (Lam.N.0 is always
   invalid). Row spans and bare/web: refs are WEB numbering; oshb:/pmarks are MT — the SAME numbers.
   Written duals must still be arithmetically right (identity). Hebrew THROUGHOUT (0 Aramaic morph
   codes): an Aramaic verse label anywhere is a hard error.
2. **THE ACROSTIC SPINE is the tier-1 skeleton** (strategy §2a): chs 1, 2, 4 = 22-verse alphabetic
   acrostics (one verse per letter); ch 3 = 66-verse TRIPLE acrostic (three verses per letter,
   uniform triplets byte-verified); ch 5 = 22 verses, NOT acrostic. LETTER ORDER IS A BYTE FACT:
   ch 1 runs ayin-then-pe (standard); chs 2, 3, 4 run PE-THEN-AYIN (reversed) — never "correct"
   it, never call the ch-1 order reversed. verse_map_oshb.json carries acrostic_letter /
   acrostic_position per verse; acrostic_spine.json carries the per-chapter letter strings. RULES:
   a row seam in chs 1, 2, 4 falls ON a letter boundary (= verse boundary); a row seam in ch 3
   falls ON a TRIPLET boundary (3:1, 3:4, 3:7 … 3:64) unless a disclosed tier-1 reason cuts inside a
   triplet; every ch 1-4 row DISCLOSES the letters its span covers (letter names, in the witness's
   order; ch-3 triplets named as triplets) — the mark-symmetry principle applied to the acrostic.
3. **Voice and address are the internal seam classes** (strategy §2b): there is no messenger
   formula and no divine voice in Lamentations; seams are argued by SPEAKER (the narrator's
   third-person description vs the personified city's first person vs the geber's "I" vs the
   communal "we") and ADDRESSEE (to YHWH; to the daughter of Zion/Jerusalem; to the wall; to Edom).
   Byte censuses to consume (never re-derive): eikhah verse-initial at 1:1, 2:1, 4:1; ani ha-gever
   3:1; bat-Tsiyon 8 vv / bat-ammi 5 / bat-Yehudah 3 / bat-Yerushalam 2 / betulat-bat 2 / bat-Edom
   2; ein menachem contiguous 1:9, 1:17, 1:21 (family 5 vv) — REFRAINS CLOSE UNITS and a
   refrain-side seam is weighed from BOTH sides (OW-3); yom af 1; YHWH 32 vv / Adonai 13; zekhor 3 /
   reeh 6 / habitah 2. Parashah marks (5 PE + 84 SAMEKH over 89 verses: EVERY verse of chs 1-4
   marked, PE at 1:22, 2:22, 3:66, 4:22; ch 5 only the PE at 5:18) are TIER-3 WEAK corroboration in
   the Writings: never a driver, single-witness disclosed at EVERY span-relevant verse (front seam
   start-1, interior, end — the symmetry arm is heavy here), PE never conflated with SAMEKH, absence
   never counterevidence.
4. Hazard flagships (read the full TOOLKIT catalog before ANY digit): prefix tolerance is an explicit
   per-length test, never a blind stripper; bat- formulas are two-token phrase tests; the bare el
   token collides with the preposition (never a divine-name count); af = anger vs "also"; defective
   spellings live (betulot without vav at 5:11) — sweep per attested spelling; the acrostic letter is
   the verse's FIRST CONSONANT including any prefix. K/Q: 22 notes / 20 verses (doubled 4:3, 5:7) —
   check pmarks BEFORE counting or slicing in ANY of them. NO special letters of any class, NO selah
   (fabrication classes); paseq 11 segs / 10 verses, count-only.
5. Cross-tradition: the LXX prose Jeremiah-ascription before 1:1, 4QLam/3QLam/5QLam, Targum/
   Peshitta/Vulgate = metadata in prose only: never in refs, never boundary evidence, never
   counterevidence. Jeremianic authorship and the Megillot liturgical setting are NON-AUTHORIZING
   positions — never argued, never assumed as a seam warrant.

TASK: tile your assigned WEB range EXACTLY (no gaps, no overlaps — verify with
tools\check_tiling.py FILE --range <your range>) into chunk rows per the strategy: §5 parents (rows
NEVER straddle a poem seam; multi-poem parts carry their internal seam at 2:1 / 5:1 — a row stops
there), §6 unit_type vocabulary (8 values, closed: city_lament, personified_city_speech,
individual_lament, hope_meditation, communal_confession, communal_petition_close,
apostrophe_address, acrostic_stanza; operative-category law: per-bytes deviations allowed with a
one-sentence disclosure in device_notes) and ruled granularity (multi-stanza rows bounded by
voice/addressee seams and refrain closes inside the poem parents; seams on letter/triplet
boundaries; a single acrostic verse is never its own row without a disclosed tier-1 reason; poem
seams always cut; chapter divisions never cut except as poem seams), §7 low-confidence posture (hold
honestly at medium_low/low with bespoke rationale rather than stopping — the 1:9c/1:11c interjection
edges, the 2:11-13 transition, the ch-3 quadripartite seams, the 4:17 "we" onset, the 4:21-22 pair,
the 5:19-22 close and the voice of 3:1 are NEVER decided), §8 register (binding verbatim). E-02 IS
HARD AT YOUR GATE: any whole-chapter row (a whole poem as one row) sits at medium_low/low WITH
frontier_flag_considered true AND a cap disclosure in prose (verse count + a phrase owning the
low-granularity choice) — expected RARE.

ROW SCHEMA (JSONL, one row per line, EXACTLY these fields):
decision_id = "PNN-NNN" (your part number, 3-digit ordinal in canonical order — e.g. "P02-004");
book = "Lam"; model_id = "M8_fable"; chunk_index_in_book = ordinal within your part (int; assembly
renumbers); span = "Lam.a.b-Lam.c.d" (WEB, full X-X form incl. single verses); boundary_rationale
(prose: curly quotes for WEB text ONLY with an inline web: ref in the SAME field; pointed Hebrew
spliced from tools\verse_map_oshb.json with its oshb: ref and tier named — NEVER hand-typed, NEVER
copied through your own draft; E-01: nfd degradation is HARD); boundary_evidence_refs (structured
refs; parashah/paseq/K-Q claims validate against pmarks — mind the fabrication classes: NO selah, NO
special letters of any class); strongest_rejected_alternative (one sentence; optional second ONLY
for a mandated rival); literature_type_guess (short free phrase); confidence in {high, medium,
medium_low, low}; strong_or_hebrew_tags_used = false; wj_or_red_letter_considered = "not applicable
in the OT substrate"; frontier_flag_considered (bool — true when the row raises a genuine frontier
question); non_authorizing = true; review_status = "draft"; parent_collection in {"F1
Lam.1.1-Lam.1.22", "F2 Lam.2.1-Lam.2.22", "F3 Lam.3.1-Lam.3.66", "F4 Lam.4.1-Lam.4.22", "F5
Lam.5.1-Lam.5.22"} (your launch message names yours); unit_type (8-value vocabulary); writer_part =
"pNN"; writer_decision_id = decision_id; writer_attempt_id = <given>; observed_substrate_signals
(list of short strings; **MANDATED dotted signal-key taxonomy — acrostic.*, voice.*, address.*,
refrain.*, petition.*, closure.*, divine_title.*, personification.*, lament_frame.*, hymn.* — naming
the signal CLASS actually consulted; parashah.* keys are BARRED from oss (disclosure in prose only);
NO staged-file names or stems in ANY field; empty list if none informed the row; NOTE that oss key
SEQUENCES are tokenized by the 7-gram gate — vary key ORDER across rows as the facts warrant, never
paste one key template into every row**); device_notes (texture, acrostic/letter disclosures,
refrain observations, deviation disclosures; parallelism classes live HERE, never in unit_type).

EVIDENCE DISCIPLINE: tier-1 text signals drive boundaries (acrostic letter boundaries and poem
onsets per §2a, speaker/addressee shifts, refrain closes, petition imperatives, vocative
apostrophes); parashah = tier-3 corroboration only, single-witness disclosed; tier-4 metadata
(incl. WEB ¶/poetry-line breaks, punctuation, capitalization, chapter divisions) never evidence
(E-23). TIER-LABEL every recurrence claim at write time; "verbatim/byte-identical" only per collate
truth with the tier named. Form-class labels (imperative, jussive, participle, person, gender) are
byte-checkable claims — same discipline as digits; the staged extract has NO morphology layer, so
argue forms from the pointed bytes plus both witnesses' renderings. Every universal claim
(only/never/first/last/each/sole/densest/unique/nowhere/no-other...) carries an adjacent
DIGIT-BEARING sweep citation naming the swept OBJECT and UNIT — and **E-16: a tier label NEVER
substitutes for an exclusivity sweep**. "(sweep: N verses)" is the one sanctioned shorthand. Quote
discipline (E-15): curly doubles for WEB text only, every curly pair closed, Hebrew never inside
curly quotes, WEB text never in straight quotes. Gloss extent = splice extent (E-08). Read back every
splice in its own sentence before delivering (E-04). Cross-seam cohesion: a byte-true device
straddling your row's own seam (a refrain, a catchword hook, a triplet) argues continuity against
the row unless disclosed. Keep adjacent-row confidences coherent with their shared-seam evidence
(E-10). MANDATED DISCLOSURE SENTENCES SHIP WITH VARIATION (the Jeremiah CWO-1 lesson): no two of
your rows may carry the same seven-word run for the parashah / paseq / K-Q / acrostic disclosures —
vary the shape while keeping every fact, ref, tier and digit.

SELF-CHECK (MANDATORY before delivering; deliver only hard-GREEN):
1. PYTHONIOENCODING=utf-8 python SP\Lam\tools\check_tiling.py <your file> --range <your range>
2. PYTHONIOENCODING=utf-8 python SP\Lam\tools\run_validator_suite.py <PRIVATE-SCRATCH COPY of your file>
   — the 10-member suite; HARD members: citation_sweep, ngram7, nfd (E-01), cap_sweep (E-02). Fix
   every RED and every fixable flag; re-run until hard-GREEN. A flag you believe is a
   true-but-heuristic false positive: leave it, note it in your final message (E-12 triage law —
   never suppress).
3. Re-collate every Hebrew quote in your own output (normalize dry-run is part of the suite; cure
   nfd degradation by re-splicing from verse_map_oshb.json, then re-run the suite).

ERRATA: if your byte re-derivation contradicts a staged inventory or strategy figure, do NOT put
the dispute in row prose — record it in your final message as an erratum with the bytes. The
pipeline credits errata.

INFRASTRUCTURE: if you are resumed after a connection loss, FIRST check whether your deliverable
already exists and validate it rather than re-running work (orphaned deliverables get validated,
never re-run). Trust disk state only. Model: claude-sonnet-5; effort ORDERED session-default, NOT
VERIFIED (recorded honestly).

FINAL MESSAGE = raw JSON only:
{"part":"pNN","attempt_id":"<given>","rows":N,"verses":N,
 "unit_type_spread":{...},"confidence_spread":{...},
 "holds_or_notes":["..."],"errata":["..."],"suite":"hard-GREEN",
 "output":"SP/Lam/writer/<file>"}
