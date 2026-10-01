# WRITER BRIEF — draft chunk rows, Jeremiah, m8-mesh-r3 (at-scale hybrid cycle)

You are one of twenty part-writers in the M8_fable Jeremiah cycle —
candidate-only, NON-AUTHORIZING, adversarially reviewed research. Your launch
message gives: part id (pNN), WEB verse range, verse count, parent frame(s),
attempt id, output filename. This brief is binding for everything else.

PATHS (absolute; lesson-c hygiene):
SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\944809d6-3b17-4589-9b47-0662301b3a37\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Strategy (BINDING) = C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Jer.md
Toolkit = SP\Jer\tools\ (TOOLKIT.md FIRST — book facts + hazard catalog; USE the staged tools, never rebuild)
Inventories = SP\Jer\jer_device_inventory.json, SP\Jer\pmarks_Jer.json, SP\Jer\web_mt_offset_map.json, SP\Jer\writer_parts.json
Substrate slices for your range = SP\Jer\span_features.jsonl, SP\Jer\risk_signals.jsonl, SP\Jer\book_observation.jsonl

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write
into it, never write any receipt, never run git. Your ONLY SP write is your
one deliverable: SP\Jer\writer\<given filename>. Private scratch goes in a
uniquely-named subdirectory of YOUR OWN session scratchpad — never in
SP\Jer, never at any scratchpad root; NO debug files anywhere under SP,
INCLUDING in SP output directories during self-check iteration.
Existence-checking your own output file is permitted. FORBIDDEN LANES (never
read, list, or preview): any path under
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\ belonging
to M1_cursor, M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55,
M5_gemini_thinking, M6_fable5, M7_sol, or comparison\.

CRITICAL BOOK FACTS:
1. Jeremiah is NOT an identity book — EXACTLY ONE offset zone, pure
   renumbering, NO SPLIT, INJECTIVE both directions (byte-proven; TOOLKIT
   "Numbering"): **MT 8:23 = WEB 9:1; MT 9:1-25 = WEB 9:2-26** (WEB ch 8 =
   22 vv / MT 23; WEB ch 9 = 26 / MT 25). Row spans and bare/web: refs are
   WEB numbering; oshb:/pmarks are MT. The Tier-0 ONE-ZONE RULE binds: any
   structured ref touching WEB ch 9 or MT 8:23 / MT ch 9 carries an
   explicit dual or numeric qualifier (`web:Jer.9.1 = oshb:Jer.8.23`, or
   "(MT 9:3)" after a web: ref). Use jer_lib.web_to_mt()/mt_to_web() —
   never hand-assume. Jer.N.0 is always invalid. Any per-chapter digit
   touching chs 8-9 NAMES its numbering space.
2. **MT 10:11 = WEB 10:11 is the book's single ARAMAIC verse** (identity
   numbering; morph-code-proven island in the ch-10 idol polemic). Tier-0
   symmetry arm: any row whose span covers WEB 10:11 MUST disclose the
   island in prose. An Aramaic label anywhere else, or a Hebrew label on
   10:11, is a hard error.
3. **The prophetic frame spine is the tier-1 skeleton** (strategy §2a):
   THREE word-event shapes, never blended (vayehi 21 vv / hadavar
   prose-sermon 11 vv / asher-hayah OAN-topical 4 vv); koh-amar onsets
   count ONLY with a frame-owner change — **FRAME-OWNERSHIP TRAP, harder
   than Isa: HANANIAH the false prophet speaks the full divine formula
   (koh amar YHWH tsevaot) at 28:2 and 28:11, and chs 27-29 embed formulas
   inside quoted speech and the ch-29 letter — every koh-amar claim names
   WHOSE MOUTH**; neum-YHWH (162 vv, the OT's densest) is closure
   CORROBORATION only — it closes a unit only where a fresh tier-1 onset
   follows; date-formula onsets and OAN headers per the inventory; hoy is
   role-split BEFORE any digit (woe onset vs funeral cry vs day-alas vs
   sword apostrophe; 34:5 is vav-prefixed ONLY — invisible to bare
   sweeps). Parashah marks (58 PE + 246 SAMEKH over 303 verses — the
   campaign's LARGEST layer) are TIER-3 WEAK corroboration in the
   Prophets: never a driver, single-witness disclosed, PE never conflated
   with SAMEKH, absence never counterevidence.
4. Hazard flagships (read the full TOOLKIT catalog before ANY digit):
   **ירמיהו contains רמיה** — the deceit noun (48:10) is a consonantal
   substring of the prophet's name, and the short spelling ירמיה is a
   substring of the long: token-bound sweeps only, per attested spelling.
   **Nebuchadnezzar has FOUR live spellings** — and **the 49:28 K/Q rides
   on the KING'S NAME** (plene byform beside the usual spelling in the
   SAME verse; check pmarks kq before slicing 49:28). K/Q: **141 notes /
   124 verses — the campaign's LARGEST inventory; ONE inside the zone (MT
   9:7 = WEB 9:8); twelve doubled-note verses** — check pmarks BEFORE
   counting or slicing in ANY of them. Exactly ONE special letter (x-small
   NUN, MT 39:13); NO large letters, NO selah, NO reversed/suspended nun
   (fabrication classes). Jehoiachin = THREE name forms; the 27:1
   DEFECTIVE-Jehoiakim setting crux is HELD OPEN — never silently
   corrected; Shiloh spelling varies BY SITE; shaqed/shoqed (1:11-12 pun)
   vs שקר; the שוב family has NO morphology layer — per-form sweeps with
   the form named; the 51:64 COLOPHON closes ch 51 BEFORE the ch-52
   appendix.
5. Jeremiah is the campaign's FLAGSHIP cross-tradition case: LXX Jer is
   ~one-eighth shorter with the OAN block after 25:13; 4QJer-b/d attest a
   short text type. ALL of it — LXX/OG/versions/DSS incl. 4QJer — is
   metadata in prose only: never in refs, never boundary evidence, never
   counterevidence. The 2 Kgs 24:18-25:30 parallel to ch 52 is
   typed-relation territory — never rearrange, never a seam warrant.

TASK: tile your assigned WEB range EXACTLY (no gaps, no overlaps — verify
with tools\check_tiling.py FILE --range <your range>) into chunk rows per
the strategy: §5 parents (rows NEVER straddle a frame seam; multi-frame
parts carry their internal hadavar seam at 11:1 / 18:1 / 21:1 — a row
stops there), §6 unit_type vocabulary (13 values, closed: superscription,
judgment_oracle, salvation_oracle, woe_oracle, lament_confession,
trial_speech, prose_sermon, narrative_prose, symbolic_act_report,
letter_document, nations_oracle, hymn_doxology, vision_report;
operative-category law: per-bytes deviations allowed with a one-sentence
disclosure in device_notes) and ruled granularity (word-event headers
bound parents; rows cut only at tier-1 internal seams — koh-amar WITH
frame-owner change, addressee/scene shifts, discourse imperatives, date
onsets, vision openings; a symbolic act's command/performance/
interpretation = ONE unit unless a tier-1 seam intervenes; frame + speech
= default larger unit — embedded oracles stay with their narrative frames;
chapter divisions never cut), §7 low-confidence posture (hold honestly at
medium_low/low with bespoke rationale rather than stopping — the 27:1
crux, the confessions' voice edges, the 30-31 seam questions, and the
50-51 stanza seams are NEVER decided), §8 register (binding verbatim).
E-02 IS HARD AT YOUR GATE: any whole-chapter row sits at medium_low/low
WITH frontier_flag_considered true AND a cap disclosure in prose (verse
count + a phrase owning the low-granularity choice).

ROW SCHEMA (JSONL, one row per line, EXACTLY these fields):
decision_id = "PNN-NNN" (your part number, 3-digit ordinal in canonical
order — e.g. "P04-007"); book = "Jer"; model_id = "M8_fable";
chunk_index_in_book = ordinal within your part (int; assembly renumbers);
span = "Jer.a.b-Jer.c.d" (WEB, full X-X form incl. single verses);
boundary_rationale (prose: curly quotes for WEB text ONLY with an inline
web: ref in the SAME field; pointed Hebrew spliced from
tools\verse_map_oshb.json with its oshb: ref and tier named — NEVER
hand-typed, NEVER copied through your own draft; E-01: nfd degradation is
HARD); boundary_evidence_refs (structured refs; one-zone rule;
parashah/paseq/K-Q/special-letter claims validate against pmarks — mind
the fabrication classes: NO selah, NO reversed/suspended nun, NO large
letters, small letter ONLY at MT 39:13); strongest_rejected_alternative
(one sentence; optional second ONLY for a mandated rival);
literature_type_guess (short free phrase); confidence in {high, medium,
medium_low, low}; strong_or_hebrew_tags_used = false;
wj_or_red_letter_considered = "not applicable in the OT substrate";
frontier_flag_considered (bool — true when the row raises a genuine
frontier question); non_authorizing = true; review_status = "draft";
parent_collection in {"F1 Jer.1.1-Jer.1.3", "M1 Jer.1.4-Jer.6.30",
"M2 Jer.7.1-Jer.10.25", "M3 Jer.11.1-Jer.17.27", "M4 Jer.18.1-Jer.20.18",
"M5 Jer.21.1-Jer.24.10", "M6 Jer.25.1-Jer.29.32", "M7 Jer.30.1-Jer.33.26",
"N8 Jer.34.1-Jer.39.18", "N9 Jer.40.1-Jer.45.5", "M10 Jer.46.1-Jer.51.64",
"N11 Jer.52.1-Jer.52.34"} (your launch message names yours; the 50:1-51:64
Babylon complex is ONE nations_oracle parent across p18|p19); unit_type
(13-value vocabulary); writer_part = "pNN"; writer_decision_id =
decision_id; writer_attempt_id = <given>; observed_substrate_signals (list
of short strings; **MANDATED dotted signal-key taxonomy — word_event.*,
speech_formula.*, oan_header.*, date_frame.*, narrative_frame.*,
superscription.*, refrain.*, lament_frame.*, divine_title.*,
symbolic_act.*, vision_report.*, letter_frame.*, trial_speech.*, hymn.*,
colophon.* — naming the signal CLASS actually consulted; parashah.* keys
are BARRED from oss (disclosure in prose only); NO staged-file names or
stems in ANY field**; empty list if none informed the row); device_notes
(texture, frame/formula observations, island/zone disclosures, deviation
disclosures; parallelism classes live HERE, never in unit_type).

EVIDENCE DISCIPLINE: tier-1 text signals drive boundaries (frame onsets
per §2a, discourse imperatives, vocative onsets, explicit scene/addressee
shifts, date frames); parashah = tier-3 corroboration only,
single-witness disclosed; tier-4 metadata (incl. WEB ¶/poetry-line breaks
and the 21 live continuation-folds) never evidence. TIER-LABEL every
recurrence claim at write time; "verbatim/byte-identical" only per collate
truth with the tier named (the B-4 standard is campaign law). Form-class
labels (imperative, jussive, participle, suffix gender) are byte-checkable
claims — same discipline as digits; the staged extract has NO morphology
layer, so argue forms from the pointed bytes plus both witnesses'
renderings. Every universal claim
(only/never/first/last/sole/densest/unique/nowhere/no-other...) carries an
adjacent DIGIT-BEARING sweep citation naming the swept OBJECT and UNIT —
and **E-16: a tier label NEVER substitutes for an exclusivity sweep**.
"(sweep: N verses)" is the one sanctioned shorthand. Quote discipline
(E-15): curly doubles for WEB text only, every curly pair closed, Hebrew
never inside curly quotes, WEB text never in straight quotes. Gloss extent
= splice extent (E-08). Read back every splice in its own sentence before
delivering (E-04 — byte-green but semantically wrong tokens are YOUR
class to catch). Cross-seam cohesion: a byte-true device straddling your
row's own seam (catchword hooks, the doxology twin, formula chains)
argues continuity against the row unless disclosed. Keep adjacent-row
confidences coherent with their shared-seam evidence (E-10).

SELF-CHECK (MANDATORY before delivering; deliver only hard-GREEN):
1. PYTHONIOENCODING=utf-8 python SP\Jer\tools\check_tiling.py <your file> --range <your range>
2. PYTHONIOENCODING=utf-8 python SP\Jer\tools\run_validator_suite.py <your file>
   — the 10-member suite; HARD members: citation_sweep, ngram7, nfd
   (E-01), cap_sweep (E-02). Fix every RED and every fixable flag; re-run
   until hard-GREEN. A flag you believe is a true-but-heuristic false
   positive: leave it, note it in your final message (E-12 triage law —
   never suppress).
3. Re-collate every Hebrew quote in your own output (normalize dry-run is
   part of the suite; cure nfd degradation with
   normalize_hebrew_in_json.py --write, then re-run the suite).

ERRATA: if your byte re-derivation contradicts a staged inventory or
strategy figure, do NOT put the dispute in row prose — record it in your
final message as an erratum with the bytes. The pipeline credits errata.

INFRASTRUCTURE: if you are resumed after a connection loss, FIRST check
whether your deliverable already exists and validate it rather than
re-running work (orphaned deliverables get validated, never re-run).
Trust disk state only.

FINAL MESSAGE = raw JSON only:
{"part":"pNN","attempt_id":"<given>","rows":N,"verses":N,
 "unit_type_spread":{...},"confidence_spread":{...},
 "holds_or_notes":["..."],"errata":["..."],"suite":"hard-GREEN",
 "output":"SP/Jer/writer/<file>"}
