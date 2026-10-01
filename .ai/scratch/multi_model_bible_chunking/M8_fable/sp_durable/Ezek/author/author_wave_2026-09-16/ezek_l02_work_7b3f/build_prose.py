# -*- coding: utf-8 -*-
import json
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_02_worklist.json'
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}

def rep(row_id, field, pairs):
    cur = ROWS[row_id][field]
    out = cur
    for old, new in pairs:
        n = out.count(old)
        if n != 1:
            raise SystemExit("FAIL %s.%s: old occurs %d times: %r" % (row_id, field, n, old))
        out = out.replace(old, new, 1)
    if out == cur:
        raise SystemExit("FAIL %s.%s: no change" % (row_id, field))
    return cur, out

EDITS = []
def add(row_id, field, pairs, items, sweep, why, tier, value=None, expected=None, op='set'):
    if value is None:
        cur, new = rep(row_id, field, pairs)
    else:
        cur, new = expected, value
    EDITS.append(dict(row_id=row_id, field=field, op=op, expected_before=cur, value=new,
                      worklist_item_ids=items, sweep=sweep, why=why, tier=tier))

# ---------------- P01-013 boundary_rationale : I08, I09, I10 (a6) ----------------
add('P01-013', 'boundary_rationale', [
 ("('the Lord Yahweh says: a disaster, a unique disaster, behold, it comes')",
  "\u201cThe Lord Yahweh says: 'A disaster! A unique disaster! Behold, it comes.\u201d (web:Ezek.7.5)"),
 ("('then you will know that I, Yahweh, strike')",
  "\u201cThen you will know that I, Yahweh, strike.\u201d (web:Ezek.7.9)"),
 ("this recognition member also carries the doubled 'my eye will not spare' refrain shared with 7:4 (sweep: 5 verses book-wide \u2014 5:11, 7:4, 7:9, 8:18, 9:10), the same refrain the close at 7:4 already carries,",
  "this recognition member also carries the doubled \u201cmy eye will not spare\u201d (web:Ezek.7.4) refrain \u2014 MEASURED at 5 verses book-wide (5:11, 7:4, 7:9, 8:18, 9:10) by a consonantal-skeleton sweep of \u05dc\u05d0 \u05ea\u05d7\u05d5\u05e1 \u05e2\u05d9\u05e0\u05d9 over Ezek_oshb.txt at its pinned digest, the WEB contracting the clause at every one of those verses except 7:4, which is why the delimited five-word run is referenced to web:Ezek.7.4 \u2014 the same refrain the close at 7:4 already carries,"),
], ['L02-I08', 'L02-I09', 'L02-I10'], 'a6',
 "A6 INSTALL at three runs this field publishes. The 12-word run at web:Ezek.7.5 and the 8-word run at web:Ezek.7.9 are content, not the fixed rendering of a counted device, so each takes the double-curly delimiter and an in-field web: reference. The 5-word run 'my eye will not spare' is MEASURED at web:Ezek.7.4 only (5:11, 7:9, 8:18 and 9:10 read \"won't spare\"), so it is delimited and referenced to 7:4 and the refrain claim is restated on the Hebrew sweep rather than on the WEB wording.",
 "MEASURED (WEB runs re-measured over tools/verse_map_web.json; the Hebrew refrain re-swept over Ezek_oshb.txt at its pinned digest)")

# ---------------- P01-013 device_notes : I15 (grounds, A10) ----------------
add('P01-013', 'device_notes', [
 ("No samekh or pe is recorded after 7:9; the absence is disclosed here rather than left unstated.",
  "MARKS-3D, MEASURED from pmarks_Ezek.json at its pinned digest on the convention that a mark is recorded ON the verse it follows: onset seam \u2014 a pe is recorded on MT 7:4, so the witness breaks immediately before this row's first verse; interior 7:5-7:8 \u2014 no mark; close seam \u2014 no samekh and no pe is recorded on MT 7:9. A10, the witness's sectioning read against this row: the next mark after the pe on MT 7:4 is the pe on MT 7:22, so the witness's own open section runs 7:5-7:22 and this row's close at 7:9 falls inside it. That sectioning corroborates the longer rival rather than this row, and it is disclosed for the alternative it corroborates. It does not unseat the row: a closed-section boundary is weak corroboration that never outranks a licensed text signal, and the near face of this close carries one \u2014 the 2mp recognition clause at 7:9, whose only word after the formula is the dependent participle \u05de\u05db\u05d4 (MEASURED: the consonantal skeleton carries \u05d5\u05d9\u05d3\u05e2\u05ea\u05dd \u05db\u05d9 \u05d0\u05e0\u05d9 \u05d9\u05d4\u05d5\u05d4 at characters 62-80 of 84, with \u05de\u05db\u05d4 filling the remainder), so it is verse-final in effect and grades as an ordinary licensed near-face signal rather than the weak mid-verse shape. The absence of a mark at 7:9 is disclosed and is never read as counter-evidence."),
], ['L02-I15'], 'grounds',
 "A10 order: disclose the witness's sectioning AGAINST the row. Measured three-direction disclosure replaces a bare absence sentence - pe on MT 7:4 behind the onset, nothing in the interior, nothing on MT 7:9, next mark at the pe on MT 7:22 - so the witness sections 7:5-7:22 as one petuchah and this row's close sits inside it. Disclosed for the rival it corroborates, with the precedence rule and the #e14 Q2 dependent-completion test stated.",
 "MEASURED (pmarks_Ezek.json marks layer; Ezek_oshb.txt consonantal-skeleton positions)")

# ---------------- P01-014 boundary_rationale : I16 (a6) ----------------
add('P01-014', 'boundary_rationale', [
 ("('behold, the day! behold, it comes!')",
  "\u201cBehold, the day! Behold, it comes!\u201d (web:Ezek.7.10)"),
], ['L02-I16'], 'a6',
 "A6 INSTALL: the 6-word run is MEASURED at web:Ezek.7.10, this row's own onset verse, and is content rather than a counted-device rendering, so it takes the double-curly delimiter plus the in-field web: reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json, one occurrence)")

# ---------------- P01-014 strongest_rejected_alternative : I18 (a6) ----------------
add('P01-014', 'strongest_rejected_alternative', [
 ("the doubled 'my eye will not spare' refrain at oshb:Ezek.7.9",
  "the doubled eye-not-sparing refrain at oshb:Ezek.7.9, whose five-word WEB rendering \u201cmy eye will not spare\u201d (web:Ezek.7.4) stands at 7:4 and is contracted at 7:9"),
], ['L02-I18'], 'a6',
 "A6 INSTALL with the attribution corrected: the five-word run is MEASURED at web:Ezek.7.4 and nowhere else, so quoting it against oshb:Ezek.7.9 attributed 7:4's wording to a different verse. The delimiter and in-field reference now point at the verse whose words are quoted; the Hebrew refrain claim at 7:9 stands.",
 "MEASURED (single WEB occurrence of the five-word run, tools/verse_map_web.json)")

# ---------------- P02-001 boundary_rationale : I22 (a6) ----------------
add('P02-001', 'boundary_rationale', [
 ("the prophet's first sight of the image of jealousy and",
  "the prophet's first sight of \u201cthe seat of the image of jealousy\u201d (web:Ezek.8.3) and"),
], ['L02-I22'], 'a6',
 "A6 INSTALL: the 5-word run 'of the image of jealousy' is MEASURED once book-wide, at web:Ezek.8.3, which is in span. The delimiter is set to the WEB's own phrase at 8:3 so the whole measured run falls inside the quotation, with the in-field web: reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json; WEB wording read at 8:3)")

# ---------------- P02-001 literature_type_guess : I23 (a6) ----------------
add('P02-001', 'literature_type_guess', [
 ("the first sight of the image of jealousy",
  "what the prophet is first shown, the \u201cseat of the image of jealousy, which provokes to jealousy\u201d (web:Ezek.8.3)"),
], ['L02-I23'], 'a6',
 "A6 INSTALL of the same run where this field publishes it; same delimiter and same in-field reference as the boundary_rationale install.",
 "MEASURED (run re-measured over tools/verse_map_web.json)")

# ---------------- P02-002 strongest_rejected_alternative : I27 (arithmetic) ----------------
add('P02-002', 'strongest_rejected_alternative', [
 ("but a fourteen-verse row",
  "but a twelve-verse row (MEASURED: web:Ezek.8.7-Ezek.8.18 is 12 verses, counted on the declared WEB face from verse_inventory.json)"),
], ['L02-I27'], 'vocab',
 "The rival span 8:7-8:18 was re-counted before writing: 12 verses on the declared WEB face, not fourteen. peer_02's figure is confirmed, and the count now carries its own basis instead of standing as a bare word.",
 "MEASURED (verse_inventory.json, WEB face; chapter 8 carries 18 verses)")

# ---------------- P02-003 boundary_rationale : I33 (grounds, the quoted phrase) ----------------
add('P02-003', 'boundary_rationale', [
 ("because no refrain or mark separates 8:16-18 from what precedes it",
  "because the over-split guard bars the shorter row a cut before 8:16 would leave \u2014 that ground is stated and weighed in the rejected alternative, and no mark-absence is offered for or against any seam here"),
], ['L02-I33'], 'grounds',
 "The order names this exact phrase, 'no refrain or mark separates 8:16-18', as a mark-absence ground the contract forbids as counter-evidence. MEASURED: the phrase is a unique substring of THIS field and does not occur in the rejected-alternative field, so the drop is applied where the bytes are and the positive ground, the over-split guard, replaces it.",
 "MEASURED (exact substring located in boundary_rationale; the guard is quoted from book_strategy_Ezek.md at its pinned digest)")

# ---------------- P02-003 strongest_rejected_alternative : I29 + I33 ----------------
_p0203 = (
 "The live rival is a seam at 8:15/8:16, weighed here under A9/A16 and held. Its near face is the pointer close at "
 "oshb:Ezek.8.15, the third of this tour's forward-pointing 'you will again see' transitions (8:6, 8:13, 8:15); its far "
 "face is oshb:Ezek.8.16, a transport verse that is a member of the strategy's closed transport list and a scene seam "
 "\u00a77 names by verse (8:5, 8:7, 8:14, 8:16). The rival is therefore licensed on both faces and it is not dismissed. The "
 "row holds because the over-split guard governs what a licensed driver may yield: a cut before 8:16 leaves 8:14-8:15, "
 "and MEASURED against verse_inventory.json, whose declared face is WEB, that is only 2 verses while the remainder "
 "8:16-8:18 has 3 \u2014 the guard allows a row under three verses only when it is a complete word-event unit, and 8:14-8:15 "
 "is not one. The samekh recorded on MT 8:14 is entered as support for the alternative it favours and no wider: this "
 "inventory keys a mark to the verse it stands after, so honouring it as a close would stop the row at 8:14 by itself, "
 "which the guard bars outright, and a section break carries corroborating weight only, ranking below every licensed "
 "driver."
)
add('P02-003', 'strongest_rejected_alternative', None,
 ['L02-I29', 'L02-I33'], 'grounds',
 "Executes the ruling's four named elements - the 8:16 transport as a class member and a section-7-named scene seam, the 8:15 pointer close, the over-split guard as the stated ground for holding, and the 8:14 samekh as corroborating only a non-viable one-verse alternative - and drops this field's own mark-absence ground ('8:16-18 has no formula or transport-verb-adjacent close of its own'), which was also measured false since 8:16 is a transport verse. The arithmetic order is discharged in the same edit: the remainder is 3 verses, not four, and the shorter row would be 2.",
 "MEASURED (verse_inventory.json for both counts; pmarks_Ezek.json for the samekh on MT 8:14; ezek_device_inventory.v2.json relation_to_the_strategy_closed_20 for 8:16's membership in the unchanged 20; book_strategy_Ezek.md section 7 for the named scene seams and the over-split guard)",
 value=_p0203, expected=ROWS['P02-003']['strongest_rejected_alternative'])

# ---------------- P02-004 boundary_rationale : I34 (a6) ----------------
add('P02-004', 'boundary_rationale', [
 ("the man clothed in linen reporting",
  "\u201cthe man clothed in linen\u201d (web:Ezek.9.11) reporting"),
], ['L02-I34'], 'a6',
 "A6 INSTALL: the 5-word run is MEASURED at web:Ezek.9.3, 9.11, 10.2 and 10.6. This clause glosses 9:11, so the delimiter carries the in-field reference web:Ezek.9.11, the verse the sentence is about.",
 "MEASURED (run re-measured over tools/verse_map_web.json: 4 occurrences book-wide, 2 of them inside this span)")

# ---------------- P02-005 strongest_rejected_alternative : I37 (arithmetic) ----------------
add('P02-005', 'strongest_rejected_alternative', [
 ("would produce a sixteen-verse row",
  "would produce a seventeen-verse row (MEASURED: web:Ezek.10.1-Ezek.10.17 runs to 17 verses by a count over verse_inventory.json on its WEB face)"),
], ['L02-I37'], 'vocab',
 "The rival span 10:1-10:17 was re-counted before writing: 17 verses on the declared WEB face, not sixteen. peer_02's figure is confirmed and the count now carries its own basis.",
 "MEASURED (verse_inventory.json, WEB face)")

# ---------------- P02-007 boundary_rationale : I43 + I44 (a6) ----------------
add('P02-007', 'boundary_rationale', [
 ("('the faces which I saw by the river Chebar\u2026 they each went straight forward')",
  "\u201cthe faces which I saw by the river Chebar \u2026 They each went straight forward.\u201d (web:Ezek.10.22)"),
], ['L02-I43', 'L02-I44'], 'a6',
 "A6 INSTALL: both runs, 9 words and 5 words, are MEASURED at web:Ezek.10.22, in span, and both sit inside this one elided gloss, so one double-curly delimiter with one in-field web: reference discharges both; the elision is kept and marked.",
 "MEASURED (both runs re-measured over tools/verse_map_web.json, one occurrence each, both at 10:22)")

# ---------------- P02-008 boundary_rationale : I47 (a6) ----------------
add('P02-008', 'boundary_rationale', [
 ("('Yahweh's Spirit fell on me, and he said to me, Speak\u2026')",
  "\u201cYahweh's Spirit fell on me, and he said to me, 'Speak \u2026\u201d (web:Ezek.11.5)"),
], ['L02-I47'], 'a6',
 "A6 INSTALL: the 11-word run is MEASURED at web:Ezek.11.5, in span, and is narrative content rather than a counted-device rendering, so it takes the delimiter and the in-field reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json, one occurrence)")

# ---------------- P02-009 boundary_rationale : I49 (a6) ----------------
add('P02-009', 'boundary_rationale', [
 ("('this land is given to us for a possession,' oshb:Ezek.11.15)",
  "(oshb:Ezek.11.15, which the WEB renders \u201cThis land has been given to us for a possession.\u201d (web:Ezek.11.15))"),
], ['L02-I49'], 'a6',
 "A6 INSTALL with the wording corrected: the 6-word run is MEASURED at web:Ezek.11.15, in span, and the WEB reads 'has been given', not 'is given', so the delimited quotation now reproduces the verse it cites and carries the in-field web: reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json; WEB wording read at 11:15)")

# ---------------- P02-009 strongest_rejected_alternative : I52 part 1 ----------------
_p0209_add = (
 " A second rival sits inside this row, and A9/A16 weighing of it follows: a seam at 11:16/11:17. Read off the pinned "
 "pmarks_Ezek.json, a samekh sits on MT 11:15 and another on MT 11:16, and because each mark is keyed to the verse it "
 "stands after, both fall immediately before a verse that the pinned v2 inventory records as carrying the long "
 "messenger formula \u05db\u05d4 \u05d0\u05de\u05e8 \u05d0\u05d3\u05e0\u05d9 \u05d9\u05d4\u05d5\u05d4 \u2014 oshb:Ezek.11.16 and oshb:Ezek.11.17, two of that class's 122 verses. "
 "CUT-RULE licenses neither seam. The addressee holds steady: the son-of-man address and the scattered exiles are named "
 "at 11:15 and nothing readdresses the oracle before 11:21. Nor does either preceding verse finish on a close-role "
 "formula \u2014 MEASURED on the skeleton of the pinned witness, MT 11:15 finishes \u05dc\u05e0\u05d5 \u05d4\u05d9\u05d0 \u05e0\u05ea\u05e0\u05d4 \u05d4\u05d0\u05e8\u05e6 \u05dc\u05de\u05d5\u05e8\u05e9\u05d4 and "
 "MT 11:16 finishes \u05d1\u05d0\u05e8\u05e6\u05d5\u05ea \u05d0\u05e9\u05e8 \u05d1\u05d0\u05d5 \u05e9\u05dd, while in 11:16 and in 11:17 alike the messenger formula stands at the "
 "verse's head after \u05dc\u05db\u05df \u05d0\u05de\u05e8 rather than at its end. No mark can satisfy that limb by itself, so the two samekhs are "
 "disclosed for the paragraph structure they corroborate within the row, and the row rests on its strict word-event "
 "onset at 11:14 and its verse-final utterance close at 11:21 (MEASURED: \u05e0\u05d0\u05dd \u05d0\u05d3\u05e0\u05d9 \u05d9\u05d4\u05d5\u05d4 closes MT 11:21)."
)
add('P02-009', 'strongest_rejected_alternative', None,
 ['L02-I52'], 'grounds',
 "A9/A16 weighing of the 11:16/11:17 rival as ordered, naming the samekh and both messenger formulae and stating on measured grounds why CUT-RULE does not license it: no addressee change, neither 11:15 nor 11:16 ends on a verse-final close-role formula, and a mark alone never satisfies limb (b). The field's existing weighing of the 11:1-21 rival is preserved byte-for-byte and the new weighing is appended after it.",
 "MEASURED (pmarks_Ezek.json marks; ezek_device_inventory.v2.json messenger-class membership and count; Ezek_oshb.txt consonantal skeletons of MT 11:15, 11:16, 11:17 and 11:21)",
 value=ROWS['P02-009']['strongest_rejected_alternative'] + _p0209_add,
 expected=ROWS['P02-009']['strongest_rejected_alternative'])

# ---------------- P02-009 device_notes : I52 part 2 ----------------
add('P02-009', 'device_notes', [
 ("(gather and return is not stated here, but the \u201cone heart\u2026 heart of flesh\u201d (web:Ezek.11.19) promise is the same device family)",
  "(the earlier denial that gather-and-return is stated here was measured FALSE against the witness and is withdrawn: MEASURED at oshb:Ezek.11.17 the oracle both gathers and gives the land \u2014 the consonantal skeleton carries \u05d5\u05e7\u05d1\u05e6\u05ea\u05d9 \u05d0\u05ea\u05db\u05dd \u05de\u05df \u05d4\u05e2\u05de\u05d9\u05dd \u05d5\u05d0\u05e1\u05e4\u05ea\u05d9 \u05d0\u05ea\u05db\u05dd \u05de\u05df \u05d4\u05d0\u05e8\u05e6\u05d5\u05ea and \u05d5\u05e0\u05ea\u05ea\u05d9 \u05dc\u05db\u05dd \u05d0\u05ea \u05d0\u05d3\u05de\u05ea \u05d9\u05e9\u05e8\u05d0\u05dc, which the WEB renders \u201cI will gather you from the peoples, and assemble you out of the countries where you have been scattered, and I will give you the land of Israel.\u201d (web:Ezek.11.17) \u2014 and the \u201cone heart\u2026 heart of flesh\u201d (web:Ezek.11.19) promise stands alongside it, so the salvation_oracle filing rests on the device the unit actually carries)"),
], ['L02-I52'], 'grounds',
 "The order names 'the unit-type field' for this correction. MEASURED: the unit_type field holds only the token 'salvation_oracle' and carries no denial at all; the measured-false device denial is a unique substring of device_notes, the field that carries this row's unit-type justification. The correction is therefore applied there and unit_type is left at salvation_oracle, which 11:17 now supports rather than undercuts. The field-name mismatch is reported in escalations rather than resolved silently.",
 "MEASURED (Ezek_oshb.txt consonantal skeleton of MT 11:17; tools/verse_map_web.json for the WEB rendering)")

# ---------------- P02-010 boundary_rationale : I53 + I54 + I57 (a6) ----------------
add('P02-010', 'boundary_rationale', [
 ("(the return transport at 11:24 'the Spirit lifted me up\u2026 into Chaldea, to the captives' plus the pe after 11:25)",
  "(the return transport at 11:24 \u2014 \u201cThe Spirit lifted me up, and brought me in the vision by the Spirit of God into Chaldea, to the captives.\u201d (web:Ezek.11.24) \u2014 plus the pe after 11:25)"),
], ['L02-I53', 'L02-I54', 'L02-I57'], 'a6',
 "A6 INSTALL: the two boss-sweep runs ('the Spirit lifted me up', 'into Chaldea, to the captives') and the peer-named union run ('and brought me in the vision by the Spirit of God into Chaldea') are all MEASURED at web:Ezek.11.24 and all lie inside the one clause, so quoting that clause whole under one double-curly delimiter with one in-field web: reference discharges all three, and the elision that had spliced two non-adjacent phrases is removed.",
 "MEASURED (all three runs re-measured over tools/verse_map_web.json; each occurs at 11:24, and the union run occurs once book-wide)")

# ---------------- P02-014 literature_type_guess : I63 (a6) ----------------
add('P02-014', 'literature_type_guess', [
 ("'the days are prolonged, and every vision fails'",
  "\u201cThe days are prolonged, and every vision fails\u201d (web:Ezek.12.22)"),
], ['L02-I63'], 'a6',
 "A6 INSTALL: the 8-word run is MEASURED at web:Ezek.12.22, in span; it is the quoted proverb the disputation answers, not a counted-device rendering, so it takes the delimiter and the in-field reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json, one occurrence)")

# ---------------- P02-016 literature_type_guess : I66 (a6) ----------------
add('P02-016', 'literature_type_guess', [
 ("foxes in the waste places",
  "\u201cfoxes in the waste places\u201d (web:Ezek.13.4)"),
], ['L02-I66'], 'a6',
 "A6 INSTALL: the 5-word run is MEASURED at web:Ezek.13.4, in span, and is image content rather than a counted-device rendering, so it takes the delimiter and the in-field reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json, one occurrence)")

# ---------------- P02-016 boundary_rationale : I67 (grounds) ----------------
add('P02-016', 'boundary_rationale', [
 ("it is disclosed here as an observed byte-true variant rather than claimed as a member of either counted sweep",
  "under ezek_device_inventory.v2.json at its pinned digest this is a counted class in its own right, the adonai-form recognition close: 5 verses (MT 13:9, 23:49, 24:24, 28:24, 29:16), every one of them verse-final and none of them a member of the 28-verse or the 21-verse family. MEASURED against Ezek_oshb.txt the clause \u05d5\u05d9\u05d3\u05e2\u05ea\u05dd \u05db\u05d9 \u05d0\u05e0\u05d9 \u05d0\u05d3\u05e0\u05d9 \u05d9\u05d4\u05d5\u05d4 ends MT 13:9 (characters 108-131 of 131), so this close carries a licensed verse-final close-role signal, and the counts are still never blended"),
 ("though the close's divine-name form keeps this row from the higher confidence a strict-formula close would earn",
  "what holds this row below high is the far side of the close seam rather than the divine-name form: oshb:Ezek.13.10 opens \u05d9\u05e2\u05df \u05d5\u05d1\u05d9\u05e2\u05df and carries no word-event, messenger, set-your-face or transport onset, and MEASURED in the pinned parashah inventory neither a samekh nor a pe stands on MT 13:9 (this chapter's marks fall on 13:7, 13:12, 13:16 and 13:19), so the far face of this close is empty, which is the medium limb of CONF-CAL and the grade already carried here"),
], ['L02-I67'], 'grounds',
 "The ruling orders the divine-name-form ground replaced with the far-side ground. Both halves of the old ground are corrected in the one edit: v2 now carries the adonai-form recognition as a counted 5-verse class, all verse-final, so the close IS a licensed near-face signal and the old ground was stale against the pinned inventory; and the measured reason the row is not high is the empty far face at 13:10 together with the absence of any mark on 13:9.",
 "MEASURED (ezek_device_inventory.v2.json recognition_formula_adonai_variant; Ezek_oshb.txt clause position at MT 13:9 and the head of MT 13:10; pmarks_Ezek.json chapter-13 marks)")

# ---------------- P02-017 boundary_rationale : I68 (a6) ----------------
add('P02-017', 'boundary_rationale', [
 ("('because\u2026 they have seduced my people, saying, Peace; and there is no peace')",
  "\u201cBecause, even because they have seduced my people, saying, 'Peace;' and there is no peace.\u201d (web:Ezek.13.10)"),
], ['L02-I68'], 'a6',
 "A6 INSTALL: the 13-word run is MEASURED at web:Ezek.13.10, this row's onset verse. The elision is replaced by the verse's own wording so the delimited quotation reproduces what it cites, with the in-field web: reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json; WEB wording read at 13:10)")

# ---------------- P02-018 boundary_rationale : I70 (a6) ----------------
add('P02-018', 'boundary_rationale', [
 ("women who prophesy \u201cout of their own heart\u201d (web:Ezek.13.17)",
  "women \u201cwho prophesy out of their own heart\u201d (web:Ezek.13.17)"),
], ['L02-I70'], 'a6',
 "A6 INSTALL by extension of an existing delimiter: the row already quoted four words of this run, but the MEASURED run is seven words ('who prophesy out of their own heart') and its first two words sat outside the quotation marks, so the opening delimiter is moved left to cover the whole run. The in-field reference is unchanged and correct.",
 "MEASURED (run re-measured over tools/verse_map_web.json: 2 occurrences, web:Ezek.13.2 and web:Ezek.13.17, the latter in span)")

# ---------------- P02-019 strongest_rejected_alternative : I72 (grounds, C1) ----------------
_p0219 = (
 "Opening the row at 14:2, the word-event proper, rather than at 14:1 is the rival that matters, and it is weighed "
 "below as A9/A16 requires. Its far face is strong: oshb:Ezek.14.2 carries the strict word-event formula, one of that "
 "class's 39 verses in the v2 device inventory at its pinned digest. Its near face is the elders' scene at "
 "oshb:Ezek.14.1, which carries no formula of its own. The parashah layer speaks for the RIVAL and not for this row, "
 "and it is written up that way: MEASURED in the pinned mark inventory pmarks_Ezek.json a pe stands on MT 14:1, and "
 "that layer keys a break to the verse it follows, so the witness parts 14:1 from 14:2 \u2014 exactly where the rival would "
 "cut. Since no mark licenses a seam on its own, the corroboration is disclosed and left unadopted. The row opens at "
 "14:1 all the same, on two stated grounds. First, book_strategy_Ezek.md at its pinned digest settles this chapter "
 "division by verse: the elders' scene at 14:1 comes before the word-event at 14:2, and the row opens at 14:1. Second, "
 "the over-split guard forbids the one-verse row at 14:1 that the rival's cut would leave behind, 14:1 being no "
 "complete word-event unit. A licensed two-faced rival held on stated grounds falls under CONF-CAL's second limb, and "
 "medium is the grade this row now takes."
)
add('P02-019', 'strongest_rejected_alternative', None,
 ['L02-I72'], 'grounds',
 "C1 rewrite as ordered. The old text read the pe as corroborating the ROW ('the pe following 14:1 corroborates keeping the elders'-scene verse inside this row'); MEASURED, the mark is recorded on MT 14:1 and therefore marks a break between 14:1 and 14:2, which is precisely the rival's cut. It is now disclosed for the alternative it corroborates, the 14:2 word-event onset is named with its class membership, and the row's holding grounds are the strategy's named division plus the over-split guard.",
 "MEASURED (pmarks_Ezek.json pe on MT 14:1; ezek_device_inventory.v2.json word_event_formula membership of Ezek.14.2; book_strategy_Ezek.md chapter-division paragraph at its pinned digest)",
 value=_p0219, expected=ROWS['P02-019']['strongest_rejected_alternative'])

# ---------------- P02-019 confidence : I71 ----------------
EDITS.append(dict(row_id='P02-019', field='confidence', op='set_confidence',
  expected_before=ROWS['P02-019']['confidence'], value='medium',
  worklist_item_ids=['L02-I71'], sweep='confidence',
  why="#e13 confidence_rulings set this row to medium. 'medium' is on the corpus's four-value scale (high, medium, medium_low, low), so no off-scale defect arises, and it is consistent with the C1 rewrite: the 14:1/14:2 rival is licensed and two-faced (pe on MT 14:1 on the near side, the strict word-event at 14:2 on the far side) and is held on stated grounds, which is CONF-CAL's second limb.",
  tier="EXTRACTED from the ruling; the grade is validated against the four-value scale and cross-checked against CONF-CAL's medium limb"))

# ---------------- P02-020 strongest_rejected_alternative : I74 part 1 ----------------
_p0220 = (
 "Splitting at oshb:Ezek.14.20, where a pe falls after the fourth triad refrain and immediately before the oracle turns "
 "from the hypothetical four scourges to their explicit application to Jerusalem (14:21-23), is the standing rival, and "
 "it is weighed under A9/A16 rather than passed over. This field's earlier denial that 14:21 introduces a messenger "
 "onset was measured FALSE and is withdrawn: MEASURED on the pinned witness's consonantal skeleton, oshb:Ezek.14.21 "
 "begins \u05db\u05d9 \u05db\u05d4 \u05d0\u05de\u05e8 \u05d0\u05d3\u05e0\u05d9 \u05d9\u05d4\u05d5\u05d4, and against the pinned ezek_device_inventory.v2.json that verse is one of the 122 "
 "verses of the long messenger-formula class. A paragraph is nonetheless what it is, not a sub-onset, since CUT-RULE "
 "grants a messenger sub-onset only where the addressee changes or where the verse just before it ENDS on a close-role "
 "formula, and neither limb is available. Nothing marks a new addressee at 14:21 \u2014 MEASURED, the son-of-man address "
 "falls at MT 14:3 and MT 14:13 and at no other verse of this chapter, chapter 14 carries no set-your-face verse at "
 "all, and 14:21 is not opened by 'and you, son of man' \u2014 so what turns there is the subject, from a hypothetical land "
 "to Jerusalem, and not the person addressed. As for the other limb, the utterance formula in MT 14:20 does NOT reach "
 "the verse end: MEASURED, \u05e0\u05d0\u05dd \u05d0\u05d3\u05e0\u05d9 \u05d9\u05d4\u05d5\u05d4 sits at characters 28-41 of an 81-character skeleton, and the independent "
 "clause \u05d0\u05dd \u05d1\u05df \u05d0\u05dd \u05d1\u05ea \u05d9\u05e6\u05d9\u05dc\u05d5 \u05d4\u05de\u05d4 \u05d1\u05e6\u05d3\u05e7\u05ea\u05dd \u05d9\u05e6\u05d9\u05dc\u05d5 \u05e0\u05e4\u05e9\u05dd runs from there to the sof pasuq. So the pe on MT 14:20 is "
 "entered as support for the rival it favours and for no more than that: this witness records a break against the verse "
 "before it, limb (b) cannot be supplied by a mark, and paragraph evidence informs while every licensed driver outranks "
 "it. The row carries on to its own verse-final utterance close at oshb:Ezek.14.23."
)
add('P02-020', 'strongest_rejected_alternative', None,
 ['L02-I74'], 'grounds',
 "Executes the ruling's first two elements: the denial is corrected to state that 14:21 IS a messenger formula, and the reason it is nevertheless a paragraph is derived from CUT-RULE on measured bytes - no addressee-marking device at 14:21, and the utterance formula at 14:20 measured mid-verse with an independent clause after it, so limb (b) fails and the pe cannot supply it. The 14:20 pe is weighed as A9 requires and disclosed for the rival it corroborates.",
 "MEASURED (Ezek_oshb.txt consonantal skeletons and formula positions at MT 14:20 and MT 14:21; ezek_device_inventory.v2.json messenger-class membership plus the son_of_man_address and set_your_face lists; pmarks_Ezek.json pe on MT 14:20)",
 value=_p0220, expected=ROWS['P02-020']['strongest_rejected_alternative'])

# ---------------- P02-020 device_notes : I74 part 3 (A7 length disclosure) ----------------
add('P02-020', 'device_notes', [
 ("oshb:Ezek.15.1 is cited above only as forward-side onset evidence for the seam; it is not a row here.",
  "oshb:Ezek.15.1 is cited above only as forward-side onset evidence for the seam; it is not a row here. A7 length disclosure: this row is 12 verses (MEASURED: web:Ezek.14.12-Ezek.14.23, tallied from verse_inventory.json on the WEB face it declares) against the strategy's 7-10 verse target density. The over-length is disclosed and carried rather than hidden: the four-scourge refrain list is never cut inside itself, and the one internal seam a reader might take, the messenger paragraph at 14:21, is weighed and held in the rejected alternative."),
], ['L02-I74'], 'grounds',
 "Executes the ruling's third element, the A7 length disclosure, in the row's disclosure field: 12 verses against the 7-10 target, re-counted rather than carried from any report, with the stated reason the row is held at that length.",
 "MEASURED (verse_inventory.json, WEB face: chapter 14 carries 23 verses, so 14:12-14:23 is 12)")

# ---------------- P03-003 boundary_rationale : I79 (a6) ----------------
add('P03-003', 'boundary_rationale', [
 ("('you trusted in your beauty and played the whore')",
  "\u2014 the WEB reads \u201cBut you trusted in your beauty, and played the prostitute because of your renown\u201d (web:Ezek.16.15) \u2014"),
], ['L02-I79'], 'a6',
 "A6 INSTALL with the wording corrected: the 8-word run is MEASURED at web:Ezek.16.15, in span, and the WEB reads 'played the prostitute', not 'played the whore', so the delimited quotation now reproduces the verse it cites and carries the in-field web: reference.",
 "MEASURED (run re-measured over tools/verse_map_web.json; WEB wording read at 16:15)")

json.dump(EDITS, open('prose_edits.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("OK %d prose/confidence edits built" % len(EDITS))
for e in EDITS:
    print("  %s.%s op=%s items=%s" % (e['row_id'], e['field'], e['op'], e['worklist_item_ids']))
