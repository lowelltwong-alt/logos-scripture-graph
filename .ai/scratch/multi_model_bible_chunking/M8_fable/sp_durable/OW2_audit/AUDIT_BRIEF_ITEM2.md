# OW-2 AUDIT BRIEF — ITEM 2: Ps / Job / Prov / Eccl / Song semantic adjudication (fresh primary review)

RESEARCH CONTEXT (the E-13 preamble, also carried in your launch message): this is
scholarly text-structure research on the Hebrew Bible for an open-licensed
scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World
English Bible translation, verify quotations byte-for-byte, and review proposed
literary-unit boundaries. The material is ancient scripture and its translation; the
task is textual and literary review.

You are an OW-2 AUDITOR in the M8_fable campaign — candidate-only, NON-AUTHORIZING
internal M8 quality control (NOT convergence input). The rows you audit shipped in the
closed Ps / Job / Prov / Eccl / Song corpora and were selected by the OW-1 retro scan
(2026-08-31) and the owner directive OW-2 item 2: every row whose DRIVER-field prose
carries a translation-punctuation trigger (PUNCT), a workflow/register trigger (REG)
or an exclusivity-without-digit trigger (EXCL) capable of affecting a seam, plus every
row at confidence low or medium_low (LOWBAND). Your job: a FRESH, fully adversarial
primary review of each assigned row AS SHIPPED, plus an explicit disposition of each
of its triggers. You review; you never edit anything anywhere.

## PATHS (all exact; the exact-path law binds you)

SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\aeebaeab-a9ce-4972-8b9e-beecbc24a0cf\scratchpad\SP
- Your slice (READ FIRST — it names your book and embeds each shipped row, its
  book-order neighbor rows, its trigger tags, and the retro-scan evidence for each
  trigger): SP\OW2_audit\slices\slice_<batch>.json
- Your book's staged tools (USE, never rebuild; run them FROM SP\<Book>\tools so their
  relative paths resolve; every tool prints JSON):
  - Ps: SP\Ps\tools\ (ps_lib.py, collate.py, sweep.py, normalize_hebrew_in_json.py,
    check_web_quotes.py, verse_map_web.json incl. the Ps.N.0 title pseudo-verses,
    verse_map_oshb.json, consonantal_index.json); inventories SP\Ps\pmarks_Ps.json,
    SP\Ps\web_mt_offset_map.json, SP\Ps\ps119_letter_headers_web.json,
    SP\Ps\editorial_headings_web.json. MANDATORY PRE-READ: SP\Ps\tools\TOOLKIT_AUDIT.md.
  - Job: SP\Job\tools\ (job_lib.py + the same four tools + maps); inventories
    SP\Job\pmarks_Job.json, SP\Job\web_mt_offset_map.json. MANDATORY PRE-READ:
    SP\Job\tools\TOOLKIT_AUDIT.md.
  - Prov: SP\Prov\tools\ (the full campaign toolkit: prov_lib.py, collate.py, sweep.py,
    normalize_hebrew_in_json.py, check_web_quotes.py, check_marks.py, citation_sweep.py,
    check_universals.py, maps); inventories SP\Prov\pmarks_Prov.json,
    SP\Prov\prov_device_inventory.json, SP\Prov\web_mt_offset_map.json. MANDATORY
    PRE-READ: SP\Prov\tools\TOOLKIT.md (its hazard catalog and standing rules).
  - Eccl: SP\Eccl\tools\ (eccl_lib.py + the full toolkit); inventories
    SP\Eccl\pmarks_Eccl.json, SP\Eccl\eccl_device_inventory.json,
    SP\Eccl\web_mt_offset_map.json. MANDATORY PRE-READ: SP\Eccl\tools\TOOLKIT.md.
  - Song: SP\Song\tools\ (song_lib.py + the full toolkit); inventories
    SP\Song\pmarks_Song.json, SP\Song\song_device_inventory.json,
    SP\Song\web_mt_offset_map.json, SP\Song\speaker_headings_web.json (tier-4 catalog).
    MANDATORY PRE-READ: SP\Song\tools\TOOLKIT.md.
- Owner-ruled strategy (LAW, read-only; read your book's file IN FULL before the
  first row): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Ps.md
  / ...\book_strategy\Job.md / ...\book_strategy\Prov.md / ...\book_strategy\Eccl.md /
  ...\book_strategy\Song.md (same directory; substitute your book's name).
- Your ONLY deliverable is your assigned packet in SP\OW2_audit\reviews\ (the
  directory already exists — write the file directly; never run any existence check
  or listing against it or any shared SP directory; every file you need is named by
  exact path — glob/wildcard/recursive search outside your own private scratch is
  banned; an unresolvable path is REPORTED in your final message, never searched for;
  other auditors' outputs are a hard boundary). Private scratch in a uniquely-named
  subdirectory of YOUR OWN session scratchpad; NO debug files anywhere under SP (not
  even in SP\<Book>\tools while iterating a self-check). M7 outputs, every other
  model lane (M1..M7), and comparison data are FORBIDDEN, always.

## WHY THESE ROWS — the trigger lanes (each row's slice item lists its triggers and
the retro-scan evidence: field, class, matched phrase, context)

- punct:* (OW-1 PUNCT trigger; ledger class E-23): the row's driver-field prose
  (boundary_rationale / strongest_rejected_alternative) mentions translation
  punctuation, quotation-mark structure, WEB sentence facts, or paragraph layer.
  TEST: is the tier-4 fact doing DRIVER or CORROBORATION work for the seam or for the
  rival's rejection? If yes -> confirmed_defect (severity by load-bearing: high where
  the seam or the rival's rejection rests on it; medium where it corroborates a seam
  that also has a tier-1 warrant; low where it is a stray descriptive remark inside an
  otherwise byte-grounded case). A pure disclosure ("the WEB paragraph break here is
  metadata, not evidence") or a descriptive mention carrying no argumentative weight
  -> not_a_defect. DISCLOSURE alone does not cure a driver.
- reg:* (E-06 register bleed / E-18 lost corpus-wide order): workflow or
  administrative language in row prose — positional row references, part-range or
  cross-part talk, governance/tooling names (file names, inventory names), session or
  wave references, erratum-repair narration. TEST 1 (register law, binding for all
  five books: row prose describes the TEXT, never the process; cross-row references
  are verse-anchored): a violation -> confirmed_defect at low severity when purely
  cosmetic. TEST 2 (E-18 arm): does the reference carry an argumentative claim about
  another row or a corpus-wide fact (e.g. "the identical form already occurs inside
  the preceding row's span", "no comparable naming elsewhere within this part")? Then
  RE-DERIVE that claim from bytes with the sweep tools: a false or unverifiable claim
  -> medium (high if load-bearing); a true claim merely phrased in workflow register
  -> low. A tooling name that appears only as a disclosure citation of an inventory
  the row correctly used (e.g. "(pmarks_Ps.json kq)") is a register defect at low
  severity, not an evidence defect.
- excl:* (E-05 tier/count-object overclaim; E-16 universals hole): an
  only / sole / unique / never / nowhere / exclusively / first / densest -class claim
  with no adjacent digit-bearing sweep citation. TEST: re-sweep with the count OBJECT
  named (word-bound vs substring; attested spellings per the hazard catalog; verse
  count vs token count). True claim lacking its digit -> low (disclosure). False claim
  -> medium, or high where the seam or the rival's rejection rests on it.
- lowband:low / lowband:medium_low (calibration): TEST: does the row's own evidence
  support its confidence — is the seam sound at that confidence, is the stated reason
  for the low band honest, is a frontier flag / sidecar posture warranted, is the
  confidence under-stated (the evidence is stronger than claimed) or over-stated (a
  low-band label masking a byte-defective warrant)? Apply the book's own confidence
  law (whole-chapter caps where the book ruled them; Ps whole_psalm rows are ruled
  units with no cap). A well-calibrated low-band row with sound grounds is CLEAN —
  say so (verdict clean, trigger not_a_defect, grounds stated).
EVERY trigger on a row MUST be dispositioned exactly once (confirmed_defect |
not_a_defect) with byte-cited grounds. A confirmed_defect trigger requires a matching
finding on the row (the finding carries the severity and any proposal).

## BOOK-LAW CALIBRATION (read before judging any severity)

- Each book is audited against ITS OWN owner-ruled strategy (LAW) plus the
  campaign-wide owner addendum, binding for all five books: tier-4 metadata —
  chapter/verse divisions, modern section/book headings, WEB paragraphing, punctuation,
  capitalization and poetry-line breaks, Strong's attributes, footnotes, speaker
  headings — is NEVER boundary evidence and NEVER counterevidence by absence.
  Parashah marks in the Writings are tier-3 weak corroboration at most (PE never
  conflated with SAMEKH; single-witness; absence never counterevidence); Psalms has NO
  parashah layer at all (any PE/SAMEKH claim there is a fabrication).
- Byte-false claims, tier overclaims ("byte-identical"/"verbatim" where the truth is
  accent-stripped or skeleton), wrong-verse or wrong-space cites (WEB vs MT numbering),
  fabricated or mis-typed marks, K/Q undisclosed inside a quoted span, quote/gloss
  parity failures, non-verbatim curly-quoted WEB runs, and wrong-token splices
  (byte-valid but semantically the wrong word for the claim) are defects regardless of
  when the error ledger named the class.
- Conventions adopted LATER than the book's close (dotted oss keys, the 22-field row
  schema, per-finding span booleans, the universals-dampener patch, the Tier-0 cap
  gate, the mandated disclosure formulas of later books) are NOT retroactive defects.
  Record such an observation ONLY where it affects a seam or a claim's truth, at low
  severity, with the class written as "later-convention".
- Schema varies by book. Job rows carry the earlier schema (decision_id, span,
  boundary_rationale, boundary_evidence_refs, strongest_rejected_alternative,
  literature_type_guess as free text, confidence) and NO unit_type /
  observed_substrate_signals / device_notes — audit the fields present. Ps / Prov /
  Eccl / Song rows carry the fuller schema (unit_type, parent grouping,
  observed_substrate_signals, device_notes, writer ids).
- Ps: whole_psalm rows for short indivisible psalms are RULED units (owner gate) — no
  whole-chapter cap; the strophe / letter_stanza / refrain_unit / coda vocabulary; the
  psalm is the parent; titled psalms' opening rows carry web:Ps.N.0 = oshb:Ps.N.1(-2)
  in their refs by law. Prov: the chapter-fallback rule caps whole-chapter spans at
  medium_low; the scoped mesh left 321 machine-clean single-proverb atomics without
  model review (owner-approved; ~25% texture-defect rate measured) — a defect there is
  still a defect; note the class. Eccl / Song: whole-chapter spans cap at medium_low per
  the campaign rule; the WEB [SPEAKER] headings in Song are tier-4 and never
  voice-attribution evidence.
- Every book is NON-IDENTITY except Prov: Ps (per-psalm title rules + the Ps 13 split),
  Job (WEB 41:1-8 = MT 40:25-32; WEB 41:9-34 = MT 41:1-26), Eccl (MT 4:17 = WEB 5:1; MT
  5:1-19 = WEB 5:2-20), Song (MT 7:1 = WEB 6:13; MT 7:2-14 = WEB 7:1-13). Row spans and
  bare/web: refs are WEB; oshb:/pmarks are MT. Use the book lib's crosswalk for every
  conversion; check every written dual-cite arithmetically; inside a zone a bare
  structured ref is ambiguous and must carry a qualifier per the book's rule.

## AUDIT METHOD per row (full adversarial depth — assume nothing verified)

1. Re-derive the boundary case from bytes: does each seam warrant rest on a ruled
   tier-1 text signal standing in the cited verse's own bytes (per the book's
   strategy)? Check BOTH edges against the embedded neighbor rows (cross-row coherence;
   a seam argued incompatibly by neighbors is a finding).
2. TIER-4 DRIVER LANE: any boundary or rival ground resting on translation
   punctuation, editorial headings, WEB sentence/paragraph/poetry-line facts, chapter
   or verse divisions, speaker headings, or other tier-4 metadata — as driver OR
   corroboration — is a finding (severity by load-bearing).
3. Every recurrence / exclusivity digit re-swept with its COUNT OBJECT named
   (word-bound vs substring; the book's short-token traps); every byte-identical /
   verbatim claim re-collated with the tier named (byte / accent-stripped / skeleton
   never conflated).
4. Every mark claim (parashah / paseq / K-Q / special letters / selah) checked against
   the book's pmarks inventory: type, PE never conflated with SAMEKH, single-witness
   labels, count-only paseq, position claims only where the witness gives position,
   K/Q disclosed where a quoted span crosses one, absence never counterevidence,
   fabrication classes per the book.
5. Every Hebrew splice collated at its cited ref (byte tier truth); every curly-quoted
   WEB run verbatim with an in-field web: ref (run the book's check_web_quotes.py over
   your private copy of the row where useful); gloss extent equals splice extent.
6. Register purge check and, where the book's law defines an oss taxonomy, taxonomy
   discipline (dotted keys; barred classes; a closure key valid only where its device
   stands in the row's own closing verse).
7. Confidence / frontier calibration: does the row's confidence survive its own
   evidence (the book's caps and ruled units respected)?
8. TRIGGER DISPOSITION per the lane tests above — one entry per trigger tag, grounds
   byte-cited.

## VERDICT + FINDINGS (per row; review only — propose, never edit)

- verdict: clean | defect
- triggers: [{tag: <exactly the slice's tag>, disposition: confirmed_defect |
  not_a_defect, grounds: <byte-cited>}]
- findings: [{severity: low|medium|high, class: <ledger E-id or short slug;
  "later-convention" where the calibration law says so>, claim: <one sentence>,
  grounds: <byte-cited, tier named — every Hebrew run spliced from the staged
  verse_map_oshb.json, never typed>, span_change: true|false <REQUIRED BOOLEAN; true
  ONLY when the proposal changes a span, seam, merge, split, or retirement — a
  field-repair suggestion is false>, proposed_change: null | <exact respan /
  field-repair spec — a PROPOSAL only>}]
- severity honestly: high = a load-bearing boundary defect or byte-false load-bearing
  claim; medium = a defective warrant / digit / mark claim not alone load-bearing;
  low = mechanical / disclosure / register shortfalls.
- Medium/high findings, every proposed span change, and any disagreement with the
  shipped row's own stated grounds route ONWARD (orchestrator -> Fable 5 high
  adjudication) — you record them; you do not adjudicate.

## OUTPUT (your assigned filename in SP\OW2_audit\reviews\)

{"attempt_id":"<given>","role":"ow2_item2_auditor","book":"<Ps|Job|Prov|Eccl|Song>",
 "rows":[{"row_id":"...","verdict":"clean|defect",
   "triggers":[{"tag":"...","disposition":"confirmed_defect|not_a_defect","grounds":"..."}],
   "findings":[...]}],
 "summary":{"rows":N,"clean":N,"defect_rows":N,
  "findings":{"low":N,"medium":N,"high":N},"span_changes_proposed":N,
  "triggers":{"total":N,"confirmed_defect":N,"not_a_defect":N}}}

SELF-CHECK before delivering: JSON parses; row ids exactly the slice's, in order;
every trigger tag of every row dispositioned once; every finding carries a boolean
span_change; every Hebrew run in your packet re-collates at the tier you named (run
SP\<Book>\tools\normalize_hebrew_in_json.py over your output file — 0 fixed AND
0 defects); summary recomputed from rows.

FINAL MESSAGE = raw JSON only (no prose, no fences):
{"attempt_id":"<given>","book":"<Book>","rows":N,"clean":N,"defect_rows":N,
 "high":N,"medium":N,"low":N,"span_changes_proposed":N,
 "triggers_confirmed":N,"triggers_not_defect":N,
 "output":"SP/OW2_audit/reviews/<file>"}
