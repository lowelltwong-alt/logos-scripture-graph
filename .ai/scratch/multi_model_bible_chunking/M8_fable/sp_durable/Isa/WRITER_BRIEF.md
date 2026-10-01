# WRITER BRIEF — draft chunk rows, Isaiah, m8-mesh-r3 (at-scale hybrid cycle)

You are one of eighteen part-writers in the M8_fable Isaiah cycle —
candidate-only, NON-AUTHORIZING, adversarially reviewed research. Your launch
message gives: part id (pNN), WEB verse range, verse count, parent frame(s),
attempt id, output filename. This brief is binding for everything else.

PATHS (absolute; lesson-c hygiene):
SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\77f9a816-3d17-41d2-8113-40d8b06e6e47\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Strategy (BINDING) = C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Isa.md
Toolkit = SP\Isa\tools\ (TOOLKIT.md FIRST — book facts + hazard catalog; USE the staged tools, never rebuild)
Inventories = SP\Isa\isa_device_inventory.json, SP\Isa\pmarks_Isa.json, SP\Isa\web_mt_offset_map.json, SP\Isa\writer_parts.json
Substrate slices for your range = SP\Isa\span_features.jsonl, SP\Isa\risk_signals.jsonl, SP\Isa\book_observation.jsonl

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write
into it, never write any receipt, never run git. Your ONLY SP write is your
one deliverable: SP\Isa\writer\<given filename>. Private scratch goes in a
uniquely-named subdirectory of YOUR OWN session scratchpad — never in
SP\Isa, never at any scratchpad root; NO debug files anywhere under SP,
INCLUDING in SP output directories during self-check iteration.
Existence-checking your own output file is permitted. FORBIDDEN LANES (never
read, list, or preview): any path under
C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\ belonging
to M1_cursor, M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55,
M5_gemini_thinking, M6_fable5, M7_sol, or comparison\.

CRITICAL BOOK FACTS:
1. Isaiah is NOT an identity book — TWO offset zones, DIFFERENT shapes
   (byte-proven; TOOLKIT "Numbering"): **ZONE A: MT 8:23 = WEB 9:1; MT
   9:1-20 = WEB 9:2-21. ZONE B (SPLIT): MT 63:19 spans WEB 63:19 + WEB
   64:1; MT 64:1-11 = WEB 64:2-12.** Row spans and bare/web: refs are WEB
   numbering; oshb:/pmarks are MT. The Tier-0 TWO-ZONE + SPLIT RULE binds:
   any structured ref touching WEB ch 9 / WEB ch 64 / WEB 63:19 or MT 8:23
   / MT ch 9 / MT 63:19 / MT ch 64 carries an explicit dual or numeric
   qualifier; any MT-63:19 content claim names WHICH WEB half it lives in.
   Use isa_lib.web_to_mt()/mt_to_web_all() — never hand-assume; web_to_mt
   is NOT injective at the split.
2. **The prophetic frame spine is the tier-1 skeleton** (strategy §2a):
   superscriptions (1:1, 2:1, 13:1 + the 38:9 mikhtav class), the massa
   header series, hoy onsets (role-split — 55:1 is an INVITATION), divine-
   speech frames (**name WHOSE frame: chs 36-37 use כה אמר on BOTH sides**),
   explicit addressee/scene shifts, refrain brackets (the stretched-hand
   refrain closes the 9:7-10:4 stanzas and bridges to 5:25 — disclose the
   rival architecture). Parashah marks (41 PE + 168 SAMEKH — the campaign's
   largest layer) are TIER-3 corroboration only, single-witness disclosed.
3. Hazard flagships: **לםרבה at MT 9:6** (medial final-mem, doubled staged
   token, K/Q, zone A); K/Q 53 notes / 49 verses (check pmarks BEFORE
   slicing any of them); the ONE special letter (small nun MT 44:14); YHWH
   in 394 verses (count-objects still named: tetragrammaton vs adonai
   [courtly-vs-divine role split] vs tsevaot vs Yah [3 sites incl. the
   doubled 38:11]); ישעיהו vs the ישועה salvation family; שאר 4-way;
   צר/צור; רב שקה = two tokens. Read the full TOOLKIT catalog.
4. The 2 Kgs 18-20 parallel and ALL DSS (incl. 1QIsa-a) / LXX / versions
   material is metadata in prose only — never in refs, never boundary
   evidence, never counterevidence. The 38:21-22 displacement is
   typed-relation territory — never rearrange.

TASK: tile your assigned WEB range EXACTLY (no gaps, no overlaps — verify
with tools\check_tiling.py FILE --range <your range>) into chunk rows per
the strategy: §5 parents (rows NEVER straddle a frame seam; 1:1 and 2:1 are
superscription rows; 13:1 stays with its Babylon oracle), §6 unit_type
vocabulary (10 values, closed: superscription, massa_oracle, woe_oracle,
judgment_oracle, salvation_oracle, trial_speech, servant_song,
vision_report, narrative_prose, hymn_doxology; operative-category law:
deviations allowed per-bytes with a one-sentence disclosure in
device_notes) and HYBRID granularity (coherent oracle/speech units bounded
by tier-1 frame signals; massa headers bound parent oracles with internal
tier-1 seams cutting rows; refrains close units with bracket function
argued from bytes; frame + speech = default larger unit; chapter divisions
never cut), §7 low-confidence posture (hold honestly at medium_low/low with
bespoke rationale rather than stopping — the servant referent and the 7:14
construal are NEVER decided), §8 register (binding verbatim).

ROW SCHEMA (JSONL, one row per line, EXACTLY these fields):
decision_id = "PNN-NNN" (your part number, 3-digit ordinal in canonical
order — e.g. "P04-007"); book = "Isa"; model_id = "M8_fable";
chunk_index_in_book = ordinal within your part (int; assembly renumbers);
span = "Isa.a.b-Isa.c.d" (WEB, full X-X form incl. single verses);
boundary_rationale (prose: curly quotes for WEB text ONLY with an inline
web: ref in the SAME field; pointed Hebrew spliced from
tools\verse_map_oshb.json with its oshb: ref and tier named — NEVER
hand-typed, NEVER copied through your own draft);
boundary_evidence_refs (structured refs; two-zone + split rule;
parashah/paseq/K-Q/special-letter claims validate against pmarks — mind the
fabrication classes: NO selah, NO reversed/suspended nun, NO large letters,
small letter ONLY at MT 44:14); strongest_rejected_alternative (one
sentence; optional second ONLY for a mandated rival); literature_type_guess
(short free phrase); confidence in {high, medium, medium_low, low};
strong_or_hebrew_tags_used = false; wj_or_red_letter_considered = "not
applicable in the OT substrate"; frontier_flag_considered (bool — true when
the row raises a genuine frontier question); non_authorizing = true;
review_status = "draft"; parent_collection in {"F1 Isa.1.1-Isa.1.1",
"M1 Isa.1.2-Isa.12.6", "M2 Isa.13.1-Isa.27.13", "M3 Isa.28.1-Isa.35.10",
"N4 Isa.36.1-Isa.39.8", "M5 Isa.40.1-Isa.48.22", "M6 Isa.49.1-Isa.55.13",
"M7 Isa.56.1-Isa.66.24"} (your launch message names yours); unit_type
(10-value vocabulary); writer_part = "pNN"; writer_decision_id =
decision_id; writer_attempt_id = <given>; observed_substrate_signals (list
of short strings; **MANDATED dotted signal-key taxonomy — oracle_frame.*,
speech_formula.*, massa_header.*, woe_series.*, servant_song.*,
narrative_frame.*, superscription.*, refrain.*, remnant_family.*,
divine_title.*, vision_report.*, hymn.*, trial_speech.*, parashah.* —
naming the signal CLASS actually consulted; NO staged-file names or stems
in ANY field**; empty list if none informed the row); device_notes
(texture, frame/refrain observations, deviation disclosures; parallelism
classes live HERE, never in unit_type).

EVIDENCE DISCIPLINE: tier-1 text signals drive boundaries (frame onsets per
§2a, refrain/inclusio brackets, vocative/imperative onsets, explicit
scene/addressee shifts, discourse frames); parashah = tier-3 corroboration
only, single-witness disclosed, PE never conflated with SAMEKH, absence
never counterevidence; tier-4 metadata (incl. the WEB mid-verse paragraph
opens after massa headers) never evidence. TIER-LABEL every recurrence
claim at write time; "verbatim/byte-identical" only per collate truth with
the tier named (the B-4 standard is campaign law). Form-class labels
(imperative, jussive, participle) are byte-checkable claims — same
discipline as digits. Every universal claim
(only/never/first/last/sole/densest/unique...) carries an adjacent
DIGIT-BEARING sweep citation naming the swept OBJECT and UNIT — read the
TOOLKIT hazard catalog before trusting any digit. "(sweep: N verses)" is
the one sanctioned shorthand. Cross-seam cohesion: a byte-true device
straddling your row's own seam (the stretched-hand refrain, the qadosh-
Israel title chains, catchword hooks at oracle joins) argues continuity
against the row unless disclosed.

SELF-CHECK (MANDATORY before delivering; deliver only hard-GREEN):
1. PYTHONIOENCODING=utf-8 python SP\Isa\tools\check_tiling.py <your file> --range <your range>
2. PYTHONIOENCODING=utf-8 python SP\Isa\tools\run_validator_suite.py <your file>
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
 "output":"SP/Isa/writer/<file>"}
