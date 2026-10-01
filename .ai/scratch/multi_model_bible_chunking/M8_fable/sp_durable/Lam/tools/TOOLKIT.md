# Lam shared verification toolkit (m8-mesh-r3, built Phase 0 by the orchestrator, 2026-09-07)

Every agent brief points here. USE these tools; do NOT rebuild them. Run every tool FROM this
directory (relative paths). Hebrew is SPLICED from verse_map_oshb.json, never hand-typed.

## Book facts (Phase 0 verified from bytes - trust these; do not re-derive)

### Numbering: IDENTITY (byte-PROVEN, never assumed)
WEB and MT agree verse-for-verse in all five chapters: 22 / 22 / 66 / 22 / 22 = **154 verses in
BOTH witnesses**. Proof (../web_mt_offset_map.json): per-chapter counts in both witnesses; 38
content anchors -> 163 identity hits / 4 misses (all byte-reviewed: 3 lexeme renderings + 1
defective spelling, ZERO numbering discrepancies) versus 146 / 144 misses under +1 / -1 verse
shifts (identity DISCRIMINATED, not defaulted). NO split verse, NO offset zone, NO title
pseudo-verse (Lam.N.0 is ALWAYS invalid; Lam 1:1 is an ordinary counted verse). `lam_lib`'s
web_to_mt()/mt_to_web() are the identity, range-guarded - use them anyway for API parity. Single-verse
spans use the full X-X form (`Lam.3.1-Lam.3.1`) - machine-checked. Dual refs are OPTIONAL everywhere
but a WRITTEN dual must be arithmetically right (`web:Lam.2.5 = oshb:Lam.2.5`).

### Cross-tradition note
LXX Lamentations carries a prose Jeremiah-ascription BEFORE 1:1 that MT/WLC and WEB do NOT carry;
the Hebrew canon places the book in the Writings (Megillot). All LXX / Old Greek / Vulgate /
Peshitta / Targum / DSS (4QLam, 3QLam, 5QLam) material is cross-tradition METADATA in prose, never
boundary evidence, never counterevidence, never a boundary_evidence_refs entry
(`citation_sweep.py` guards). Jeremianic authorship is a canon/authorship position and is
NON-AUTHORIZING: never argued, never assumed as a boundary ground.

### LANGUAGE - Hebrew throughout
Every OSHB morph code is H-prefixed (1,564 codes; 0 A-prefixed). There is NO Aramaic island and NO
language zone. `check_language_zones.py` flags any "Aramaic" / "Syrian" verse label near a Lam ref
(Aramaism / Aramaic-influence discussion is legitimate).

### THE ACROSTIC SPINE (tier-1 text signal: inclusio_refrain_acrostic) - byte-pinned
- chs 1, 2, 4: 22 verses, ONE verse per letter, alef..tav.
- ch 3: 66 verses, THREE consecutive verses per letter (22 x 3), byte-verified uniform triplets.
- ch 5: 22 verses, NOT acrostic (its first letters follow no order) - the 22-count is a formal
  echo, never an acrostic claim.
- LETTER ORDER: ch 1 runs **ayin then pe** (the standard order); chs 2, 3 and 4 run **PE THEN
  AYIN** (the reversed order) - a byte fact of this witness (pinned in `acrostic_spine.json` and
  per verse in verse_map_oshb.json as `acrostic_letter` / `acrostic_position`); never "correct" it,
  never call the ch-1 order "reversed" or the ch-2/3/4 order "standard".
- The acrostic letter is the primary structural spine of chs 1-4: every verse (chs 1, 2, 4) or
  triplet (ch 3) is a formally marked stanza. Verse divisions themselves stay tier-4 metadata; the
  LETTER (a text signal) is what carries evidence. A row seam that falls INSIDE a ch-3 triplet
  contradicts the spine and needs a disclosed tier-1 reason.

### PARASHAH LAYER (MT-keyed = WEB-keyed)
WLC Lam: **5 PE + 84 SAMEKH over 89 marked verses** - every verse of chs 1-4 carries a mark (ch 1:
1:1-1:21 SAMEKH, 1:22 PE; likewise 2:1-21 SAMEKH / 2:22 PE; 3:1-65 SAMEKH / 3:66 PE; 4:1-21 SAMEKH /
4:22 PE); ch 5 carries ONE mark, the PE at 5:18, and NO samekh. The mark layer therefore mirrors the
acrostic stanza layout - it is TIER-3 WEAK single-witness corroboration under the owner addendum
(parashah_in_prophets_or_writings), never a driver; PE never conflated with SAMEKH; absence never
counterevidence; every citation single-witness-disclosed. The SYMMETRY arm (`check_marks.py`) is
heavy here: a row over chs 1-4 must disclose the mark at every span-relevant verse (front seam
start-1, interior, end).

### Fabrication classes for Lam (hard errors)
- SELAH anywhere (Psalter device; zero occurrences).
- ANY special letter (small / large / suspended / reversed nun): WLC Lam carries NO special-letter
  seg of any class (other_segs is EMPTY).
- A paseq at a verse the inventory does not list; a K/Q claim at a verse the kq inventory does not
  list; a petuchah claim at a SAMEKH verse or vice versa.
- Any Aramaic verse label.
- Any Jeremianic-authorship or LXX-superscription claim as boundary evidence.

### Disclosure inventories (../pmarks_Lam.json, MT-keyed)
- paseq: 11 segs over 10 verses (1:1, 1:15, 1:16 x2, 2:1, 2:5, 2:6, 2:7, 2:8, 2:19, 5:21) - seg
  layer, NOT quotable verse bytes, COUNT-ONLY (no intra-verse position).
- kq: 22 variant notes over 20 verses; doubled-note verses 4:3 and 5:7. Check kq BEFORE counting or
  slicing in ANY K/Q verse; a Hebrew splice from a K/Q verse carries the ketiv/qere disclosure.

### STRUCTURAL SPINE beyond the acrostic (../lam_device_inventory.json - byte censuses)
- eikhah ("How ...") opens 1:1, 2:1 and 4:1 (verse-initial: exactly these three; the token also
  stands non-initially once) - the aleph-line onset of three poems.
- 3:1 ani ha-gever ("I am the man") opens the first-person lament (ani token: 4 verses).
- Personification / address formulas (verse censuses, prefix-tolerant): bat-Tsiyon 8, bat-ammi 5,
  bat-Yehudah 3, bat-Yerushalam 2, betulat-bat 2, bat-Edom 2.
- Refrain: ein menachem ("no comforter") contiguous at 1:9, 1:17, 1:21; the menachem token stands
  in 5 verses of ch 1 (the family incl. the "none to comfort her" forms) - REFRAINS CLOSE UNITS
  under the owner-ruled seam law; a refrain-side diagnosis weighs BOTH sides of the seam.
- yom af (day of anger) 1 verse; af token 4 verses.
- Divine names: YHWH 32 verses; Adonai 13 verses (ch 2 densest: 7 each); bare el token 9 verses
  (includes the preposition homograph - a review list, NOT a divine-name count).
- Petition onsets to YHWH: zekhor 3 verses (ch 5 opens with zekhor YHWH), reeh 6, habitah 2 -
  candidate discourse-frame signals.
- Chapter texture: poetry lines open every verse of chs 1, 2, 4, 5 and 57/66 of ch 3; paseq sits in
  chs 1-2 and 5:21 only; K/Q per chapter 3/3/4/6/6.

## SWEEP HAZARD CATALOG (E-11 discipline - every needle finals-normalized, every class byte-verified)
- PREFIX TOLERANCE is an explicit per-length test (needle behind exactly one of vav/he/bet/lamed/
  kaf/mem/shin) - never a blind prefix stripper (the Jer root-letter bug).
- bat- formulas: the two-token phrase test; "bat" alone is not a formula.
- ein menachem: the contiguous two-token form (3 sites) vs the family (5 verses): name which you
  count.
- el: the bare token collides with the preposition; only a pointed/contextual reading separates
  them - never cite the bare-token count as a divine-name count.
- af: "nose/anger" vs the particle "also" - the 4-verse token census is a review list.
- Defective spellings live (e.g. betulot without vav at 5:11): sweep per attested spelling.
- Acrostic letter = the FIRST CONSONANT of the verse skeleton; prefixes (vav etc.) count as the
  letter (that is how the acrostic is built) - do not strip them when reading the spine.
- LETTER vs MARK are different layers and must never be conflated: the acrostic LETTER name of a
  verse (tier-1, from the verse's own bytes) is not a parashah MARK of the same name (tier-3, from
  pmarks_Lam.json). In ch 3 the pe triplet is 3:46-3:48 by letter, while the MARK at 3:48 is
  SAMEKH and the only PE mark of the chapter stands at 3:66 - read the mark from the inventory
  before naming it, and never let a letter name imply a mark (or the reverse).
- DIVINE-NAME CENSUSES take a per-hit byte read-back (the E-04 read-back law applied to
  inventories): elohim_any is EMPTY in this book - the Phase-0 substring sweep had named 1:16 and
  5:17, where the bytes carry the bare demonstrative elleh, not the divine name (corrected in
  lam_device_inventory.json 2026-09-07; the class is the same substring/prefix hazard as bare el).

## Data files (consume directly)
../Lam_web.usfm, ../Lam_web_clean.txt, ../Lam_oshb.txt (maqaf-free extract), ../verse_inventory.json,
../web_mt_offset_map.json (identity proof), ../web_mt_verse_check.json, ../pmarks_Lam.json,
../lam_device_inventory.json, verse_map_web.json, verse_map_oshb.json (with acrostic_letter /
acrostic_position), consonantal_index.json, acrostic_spine.json.

## Tools
lam_lib.py (library; identity crosswalk API), collate.py (byte / nfd / accent_stripped / skeleton
tiers), sweep.py, normalize_hebrew_in_json.py (dry-run = E-01 HARD gate), check_tiling.py,
run_validator_suite.py (10 members: citation_sweep, hebrew_normalize_dryrun, web_quotes,
refs_mirror, mark_symmetry, universals, language_zones, ngram7, cap_sweep, register),
citation_sweep.py, check_marks.py, check_web_quotes.py (E-15 arms), check_refs_mirror.py,
check_universals.py (E-16 exclusivity never dampened), check_language_zones.py, ngram7.py
(--gate 10; --full-ids opt-in), cap_sweep.py (E-02 whole-chapter cap, HARD), check_register.py
(E-06/E-18 residual arms), check_atomic_isolation.py (STAGED, NOT ARMED), _punct_boundary_sweep.py
(E-23 flags), builders build_offset_map.py / build_pmarks.py / build_verse_maps.py / lam_devices.py.

### NO MORPHOLOGY LAYER in the staged extract
Lam_oshb.txt carries text only; morph codes were read at Phase 0 from the XML (language census)
and are not staged - grammatical claims are argued from the pointed bytes, never from a code.

## Encoding + skeleton notes (READ before quoting Hebrew)
Only 'byte' tier is quotation-grade for pointed text; 'nfd' = copy degradation (cure by re-splicing);
'accent_stripped' and 'skeleton' are citation/mention grade and must be labeled. skeleton() maps maqaf
to SPACE (the extract is maqaf-free: 0 x U+05BE; 165 x-maqqef segs serialized to spaces).
accent_stripped retains meteg. Curly double quotes are for verbatim WEB English ONLY with an in-field
web: ref; Hebrew is spliced bare; tool wording uses straight quotes.

## Standing rules (campaign governance; the prior books' lessons applied)
E-01 nfd HARD; E-02 whole-chapter cap Tier-0 HARD (a whole-chapter row sits at medium_low/low +
frontier + cap disclosure); E-06/E-18 register purge (no repair narration, ids, reviewer/boss/peer/
tool mentions, staged-file stems, "that row"/"cross-part"); E-11 finals-normalized needles; E-13
research preamble in every launch; E-14 ladder; E-15 quote-pairing arms; E-16 exclusivity claims
keep their adjacent digit-bearing sweep citation; E-17 second-generation checklist after every
repair; E-18 explicit corpus_wide_orders + execution parity; E-19 exact-path law; E-23 translation
punctuation / paragraphing / capitalization never drive or corroborate a boundary; OW-3 both-sides
seam law (refrains close units); B-8 LF-support audit lane by default; every digit names its count
object and unit; unexpanded {placeholder} tokens are rejected; M7, other model lanes, A/B lanes and
comparison data FORBIDDEN.


---

## ERRATUM 2026-09-07 (recorded during the OW-6 fix round; raised by the stage-2 final checker)

**The parashah paragraph above is WRONG where it says every verse of chapters 1-4 carries a mark, and specifically
where it writes "3:1-65 SAMEKH".** The original sentence is left standing above rather than edited, because this is
a file agents are told to trust and not re-derive: an agent that already quoted the old text must be able to find
out that it moved.

**The fact, from `pmarks_Lam.json`:** chapter 3 carries marks at **22 verses only** - a SAMEKH at every third verse,
3:3, 3:6, 3:9 … 3:63, and a PE at 3:66. Chapter 3's marks track the acrostic TRIPLETS, one mark per triplet, not one
per verse.

**This is what the toolkit's own digits already require.** The 5 PE / 84 SAMEKH / 89 marked-verse totals recorded
above are only reachable with chapter 3 at 22, not at 66; the paragraph contradicted the digits three lines above
it. Tier is unchanged: the parashah layer stays **tier-3, single-witness**, and never drives a boundary.

**Shipped impact: none.** No corpus row carries the false prose. One primary reviewer and the boss each re-derived
the layer from `pmarks_Lam.json` rather than trusting the paragraph, and corrected it inside their own work - which
is the behaviour the hazard catalog asks for, and the reason this stayed an erratum instead of a defect.
