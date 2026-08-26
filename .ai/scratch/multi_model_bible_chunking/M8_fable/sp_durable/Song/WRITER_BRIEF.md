# WRITER BRIEF — draft chunk rows, Song, m8-mesh-r3 (full dual-blind cycle)

You are one of two part-writers in the M8_fable Song of Songs cycle —
candidate-only, NON-AUTHORIZING, adversarially reviewed research. Your launch
message gives: part id (pNN), WEB verse range, verse count, attempt id, output
filename. This brief is binding for everything else.

PATHS (absolute; lesson-c hygiene):
SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\73e44599-0972-4de8-aaca-1c68f81bad2c\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Strategy (BINDING) = C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Song.md
Toolkit = SP\Song\tools\ (TOOLKIT.md FIRST — book facts + hazard catalog; USE the staged tools, never rebuild)
Inventories = SP\Song\song_device_inventory.json, SP\Song\pmarks_Song.json, SP\Song\web_mt_offset_map.json, SP\Song\speaker_headings_web.json (TIER-4 audit catalog — see below)
Substrate slices for your range = SP\Song\span_features.jsonl, SP\Song\risk_signals.jsonl, SP\Song\book_observation.jsonl

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write
into it, never write any receipt, never run git. Your ONLY SP write is your
one deliverable: SP\Song\writer\<given filename>. Private scratch goes in a
uniquely-named subdirectory of YOUR OWN session scratchpad — never in
SP\Song, never at any scratchpad root; NO debug files anywhere under SP,
INCLUDING in SP output directories during self-check iteration.
Existence-checking your own output file is permitted. FORBIDDEN LANES (never
read, list, or preview): any path under
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\ belonging
to M1_cursor, M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55,
M5_gemini_thinking, M6_fable5, M7_sol, or comparison\.

CRITICAL BOOK FACTS:
1. Song is NOT an identity book — **MT 7:1 = WEB 6:13 and MT 7:2-14 = WEB
   7:1-13** (byte-proven; TOOLKIT "Numbering"). Row spans and bare/web:
   refs are WEB numbering; oshb:/pmarks are MT. The Tier-0 OFFSET-ZONE
   RULE binds: any structured ref touching WEB 6:13 / WEB ch 7 / MT ch 7
   carries an explicit dual or numeric qualifier. Use
   song_lib.web_to_mt()/mt_to_web() — never hand-assume.
2. **The WEB extract carries [SPEAKER: ...] voice headings — they are
   TIER-4 MODERN EDITORIAL METADATA, NEVER voice evidence, NEVER
   counterevidence.** Voice attribution follows the owner-ruled MODERATE
   policy (strategy §2a): tier-1 = in-verse gender/vocative markers + the
   attested formula anchors; continuity-inferred attribution = tier-2
   corroboration, never sole driver; every voice-shift seam claim QUOTES
   the gender-marked Hebrew form (spliced, tier-labeled). Reviewers will
   audit your rows against heading-leaning using the catalog.
3. Divine names: YHWH ZERO, Elohim ZERO (citable absences WITH the sweep);
   the MT 8:6 shalhevet-yah token pair is a held crux (strategy §7).

TASK: tile your assigned WEB range EXACTLY (no gaps, no overlaps — verify
with tools\check_tiling.py FILE --range <your range>) into chunk rows per
the strategy: §5 parents (rows NEVER straddle Song.1.1|1.2), §6 unit_type
vocabulary (7 values, closed: superscription, lyric_address,
dialogue_exchange, narrative_sequence, wasf_poem, adjuration_refrain,
epigram_unit; operative-category law: deviations allowed per-bytes with a
one-sentence disclosure in device_notes) and HYBRID granularity (maximal
single-voice lyric runs bounded by tier-1 voice-shift markers; refrain
verses close units with bracket function argued from bytes; dialogue zones
held whole — never atomize per voice-line), §7 low-confidence posture (hold
honestly at medium_low/low with bespoke rationale rather than stopping),
§8 register (binding verbatim).

ROW SCHEMA (JSONL, one row per line, EXACTLY these fields):
decision_id = "PNN-NNN" (your part, 3-digit ordinal in canonical order);
book = "Song"; model_id = "M8_fable"; chunk_index_in_book = ordinal within
your part (int; assembly renumbers); span = "Song.a.b-Song.c.d" (WEB, full
X-X form incl. single verses); boundary_rationale (prose: curly quotes for
WEB text ONLY with an inline web: ref in the SAME field; pointed Hebrew
spliced from tools\verse_map_oshb.json with its oshb: ref and tier named —
NEVER hand-typed, NEVER copied through your own draft);
boundary_evidence_refs (structured refs; offset-zone rule; parashah/paseq/
K-Q claims validate against pmarks — mind the fabrication classes: NO
selah, NO reversed/suspended nun, NO small/large letters, NO plain divine
names exist in Song); strongest_rejected_alternative (one sentence;
optional second ONLY for a mandated rival); literature_type_guess (short
free phrase); confidence in {high, medium, medium_low, low};
strong_or_hebrew_tags_used = false; wj_or_red_letter_considered = "not
applicable in the OT substrate"; frontier_flag_considered (bool — true when
the row raises a genuine frontier question); non_authorizing = true;
review_status = "draft"; parent_collection in {"F1 Song.1.1-Song.1.1",
"M Song.1.2-Song.8.14"}; unit_type (7-value vocabulary); writer_part =
"pNN"; writer_decision_id = decision_id; writer_attempt_id = <given>;
observed_substrate_signals (list of short strings; **MANDATED dotted
signal-key taxonomy — voice_shift.*, adjuration_refrain.*,
mutual_belonging.*, wasf.*, daughters_address.*, parashah.*, qol_dodi.*,
mi_zot.*, refrain.* — naming the signal CLASS actually consulted; NO
staged-file names or stems in ANY field**; empty list if none informed the
row); device_notes (texture, refrain/voice observations, deviation
disclosures; parallelism classes live HERE, never in unit_type).

EVIDENCE DISCIPLINE: tier-1 text signals drive boundaries (voice-shift
markers per the §2a policy, refrain/inclusio brackets, vocative/imperative
onsets, scene/addressee shifts, discourse frames); parashah = tier-3
corroboration only, single-witness disclosed, PE never conflated with
SAMEKH, absence never counterevidence — note the SAMEKH layer SHADOWS the
refrain skeleton and its tier does NOT rise for that; tier-4 metadata
(incl. the [SPEAKER] headings) never evidence. TIER-LABEL every recurrence
claim at write time; "verbatim/byte-identical" only per collate truth with
the tier named (the B-4 standard is campaign law). Every universal claim
(only/never/first/last/sole/densest/unique...) carries an adjacent
DIGIT-BEARING sweep citation naming the swept OBJECT and UNIT — read the
TOOLKIT hazard catalog (dod five-object blend, oath-only שבע + speech
roles, resh-ayin family, כרם-in-כרמל, מור/מר, allography classes) before
trusting any digit. "(sweep: N verses)" is the one sanctioned shorthand.
Cross-seam cohesion: a byte-true device straddling your row's own seam
(refrains especially) argues continuity against the row unless disclosed.

SELF-CHECK (MANDATORY before delivering; deliver only hard-GREEN):
1. PYTHONIOENCODING=utf-8 python SP\Song\tools\check_tiling.py <your file> --range <your range>
2. PYTHONIOENCODING=utf-8 python SP\Song\tools\run_validator_suite.py <your file>
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
 "output":"SP/Song/writer/<file>"}
