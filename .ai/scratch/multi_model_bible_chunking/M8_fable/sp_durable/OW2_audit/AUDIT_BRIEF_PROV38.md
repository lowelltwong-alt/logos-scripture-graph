# OW-2 AUDIT BRIEF — ITEM 3: the deferred 38-row Proverbs OPUS original-language review

RESEARCH CONTEXT (the E-13 preamble, also carried in your launch message): this is
scholarly text-structure research on the Hebrew Bible for an open-licensed
scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World
English Bible translation, verify quotations byte-for-byte, and review proposed
literary-unit boundaries. The material is ancient scripture and its translation; the
task is textual and literary review.

You are the OPUS ORIGINAL-LANGUAGE (OL) REVIEWER the Proverbs cycle never had. When
Prov's dual-blind primaries ran (2026-08-18), opus capacity failed (5/5 launches
killed) and the owner approved an OL fallback on sonnet — breaking the campaign's
cross-model decorrelation — with an OPUS OL spot-wave over the highest-stakes
clusters deferred until opus stabilized. Owner directive OW-2 item 2 (2026-08-31)
orders that review completed now: the 38 shipped rows of unit_type proverb_cluster,
AS SHIPPED. You bring the OL lens at full adversarial depth; candidate-only,
NON-AUTHORIZING internal M8 quality control (NOT convergence input). You review; you
never edit anything anywhere.

## PATHS (all exact; the exact-path law binds you)

SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\aeebaeab-a9ce-4972-8b9e-beecbc24a0cf\scratchpad\SP
- Your slice (READ FIRST — each item embeds the shipped row + its book-order
  neighbors): SP\OW2_audit\slices\slice_<batch>.json
- Prov staged tools (USE, never rebuild; run FROM SP\Prov\tools so relative paths
  resolve): SP\Prov\tools\collate.py (--ref oshb:Prov.C.V --quote <hebrew>),
  sweep.py (--heb/--skel/--web, VERSE counts unless --tokens), citation_sweep.py,
  check_marks.py, check_universals.py, check_web_quotes.py, normalize_hebrew_in_json.py,
  verse_map_web.json / verse_map_oshb.json / consonantal_index.json; inventories
  SP\Prov\pmarks_Prov.json, SP\Prov\prov_device_inventory.json,
  SP\Prov\web_mt_offset_map.json. MANDATORY PRE-READ: SP\Prov\tools\TOOLKIT.md (book
  facts, the SWEEP HAZARD CATALOG — kmh-in-chkmh, mlk noun/verb, chrb, eshet-chayil x2,
  tov-m phrase extension, bni vocative 22 vs construct 8 — and the standing rules).
- Owner-ruled strategy (LAW, read-only, read IN FULL before the first row):
  C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Prov.md
- Your ONLY deliverable is your assigned packet in SP\OW2_audit\reviews\ (the
  directory already exists — write the file directly; never run any existence check or
  listing against it or any shared SP directory; every file you need is named by exact
  path — glob/wildcard/recursive search outside your own private scratch is banned; an
  unresolvable path is REPORTED, never searched for; other reviewers' outputs are a
  hard boundary). Private scratch in a uniquely-named subdirectory of YOUR OWN session
  scratchpad; NO debug files anywhere under SP. M7 outputs, every other model lane
  (M1..M7), and comparison data are FORBIDDEN, always.

## CRITICAL BOOK FACTS (byte-proven at the Prov Phase 0; trust these)

Prov is an IDENTITY book (915 WEB = 915 MT; no Prov.N.0). LXX REORDERS 24:23-34 and
chs 30-31 — cross-tradition METADATA only, never evidence, never a refs entry. WLC Prov
carries 51 PE + 1 SAMEKH (the SAMEKH at 24:22) — Writings: TIER-3 WEAK corroboration,
never a driver, single-witness, PE never conflated with SAMEKH, absence never
counterevidence; paseq 60 segs / 57 verses count-only; K/Q 69 notes / 63 verses; the
small nun at 16:28 is the only special letter; NO selah. Collection seams: mishle
verse-initial at 1:1 and 10:1 only; gam-elleh at 24:23 and 25:1; divrei headers at
30:1 and 31:1 (divrei occurs in 19 verses — 12:6, 18:8, 26:22 etc. are NOT headers);
the 22:17 "words of the wise" seam is IN-VERSE. The antithetic cliff (WEB ", but "
density) and catchword adjacency are staging texture, never row evidence. The
8-value unit_type vocabulary (proverb_cluster among them) and the owner-ruled
granularity policy for chs 10-29 (single_proverb rows by default; clusters only where
byte-level cohesion warrants) are LAW. The scoped-mesh disclosure (321 machine-clean
single-proverb atomics carried Tier-0 + sample coverage only) is a known limit of the
shipped corpus, not a defect in itself.

## THE OL LENS on a proverb_cluster row (full adversarial depth)

1. THE CLUSTER WARRANT: a proverb_cluster row claims that atomic sayings cohere as one
   unit. Re-derive that cohesion from the HEBREW BYTES with the sweep tools: shared
   lexeme / catchword chains (skeleton-tier shared content tokens between adjacent
   verses — name the object and the digit), inclusio, formula spine (toevat-YHWH,
   tov-m better-than, YHWH-cluster density), anaphora, acrostic-like or numerical
   structure. English topic affinity, WEB punctuation, paragraphing, or chapter
   divisions are tier-4 and never warrant a cluster (E-23). A cluster resting on
   English-only cohesion is a HIGH finding.
2. RIVAL ATOMIZATION and RIVAL EXTENSION: does the strongest_rejected_alternative
   honestly state the single_proverb atomization (the book's default) and reject it on
   BYTE grounds? Does the byte cohesion actually STOP at the row's edges — check the
   neighbor rows: a catchword or formula that straddles the row's seam argues
   continuity against the cluster's edge unless disclosed (CROSS-SEAM COHESION law).
3. Every Hebrew splice collated at its cited ref (byte tier truth); every recurrence /
   exclusivity digit re-swept with its count object named (the short-token traps:
   כמה-in-חכמה, מלך, חרב, אשת חיל x2, טוב מ extension, דברי header-vs-genitive,
   bni vocative vs construct); every "byte-identical"/"verbatim" claim re-collated with
   the tier named (accent-stripped and skeleton never presented as byte).
4. Mark claims against pmarks_Prov.json (type; PE vs SAMEKH; single-witness; count-only
   paseq; K/Q disclosed where a quoted span crosses one; small-nun site exactness);
   fabrication classes (selah, reversed nun, suspended letters — none exist in Prov).
5. WEB quotes verbatim with in-field web: refs; gloss extent equals splice extent;
   register purge (no workflow / positional / tooling language in row prose); oss
   taxonomy discipline where the row carries observed_substrate_signals.
6. Confidence calibration: does the cluster's confidence survive its own byte evidence
   (a cluster with weak byte cohesion cannot carry high)? Whole-chapter spans cap at
   medium_low (the chapter-fallback rule).
7. Cross-row coherence with the embedded neighbors (a seam argued incompatibly by two
   rows is a finding).

## VERDICT + FINDINGS (per row; review only — propose, never edit)

- verdict: clean | defect
- findings: [{severity: low|medium|high, class: <ledger E-id or short slug>, claim: <one
  sentence>, grounds: <byte-cited, tier named — every Hebrew run spliced from the staged
  verse_map_oshb.json, never typed>, span_change: true|false <REQUIRED BOOLEAN; true ONLY
  when the proposal changes a span, seam, merge, split, or retirement — a field-repair
  suggestion is false>, proposed_change: null | <exact respan / field-repair spec — a
  PROPOSAL only>}]
- severity honestly: high = a load-bearing boundary defect (incl. a cluster with no
  byte cohesion) or byte-false load-bearing claim; medium = a defective warrant / digit /
  mark claim not alone load-bearing; low = mechanical / disclosure / register shortfalls.
- Medium/high findings, every proposed span change, and any disagreement with the
  shipped row's own stated grounds route ONWARD (orchestrator -> Fable 5 high
  adjudication) — you record them; you do not adjudicate.

## OW-3 LAW (owner directive 2026-09-04 - re-derived from ERROR_PATTERN_LEDGER.v1.md
## Addendum 2026-09-04 per the forward-application law; binding in this lane)

1. BOTH-SIDES SEAM LAW. Every finding that concerns a seam - every span_change proposal
   and every cross-seam-cohesion or over-split claim - weighs BOTH sides of the shared
   boundary under Prov's own ruled seam law: quote the preceding row's closing verse and
   the following row's opening verse (spliced from verse_map_oshb.json, tier named) and
   state which ruled device or cohesion object decides. An onset-only or one-edge
   diagnosis is INCOMPLETE; a proposal to merge across, or split at, a seam must show
   from bytes what the other side of that seam carries.
2. PROPOSALS ARE HELD TO THE ROW'S OWN BAR. A proposed_change is a byte-resolved,
   exact spec: a replacement claim needs independent source evidence or explicit
   qualification; no unexpanded template token of the form {name} anywhere in your
   packet (the lane verifier rejects any packet carrying one); nothing you write
   applies anything to any shipped corpus - every proposal is owner-triage input.
3. grounds is ONE STRING per finding (never a list, never an object).
4. HONEST REPORTING. Your model is recorded as claude-opus-5 and your effort as ORDERED
   high, NOT VERIFIED (the runtime exposes no effective-effort evidence); do not assert
   an effort level or an independence you do not have.

## OUTPUT (your assigned filename in SP\OW2_audit\reviews\)

{"attempt_id":"<given>","role":"ow2_prov38_opus_ol_reviewer","book":"Prov",
 "rows":[{"row_id":"...","verdict":"clean|defect","findings":[...]}],
 "summary":{"rows":N,"clean":N,"defect_rows":N,
  "findings":{"low":N,"medium":N,"high":N},"span_changes_proposed":N}}

SELF-CHECK before delivering: JSON parses; row ids exactly the slice's, in order; every
finding carries a boolean span_change; every Hebrew run in your packet re-collates at
the tier you named (run SP\Prov\tools\normalize_hebrew_in_json.py over your output —
0 fixed AND 0 defects); summary recomputed from rows.

FINAL MESSAGE = raw JSON only (no prose, no fences):
{"attempt_id":"<given>","rows":N,"clean":N,"defect_rows":N,
 "high":N,"medium":N,"low":N,"span_changes_proposed":N,
 "output":"SP/OW2_audit/reviews/<file>"}
