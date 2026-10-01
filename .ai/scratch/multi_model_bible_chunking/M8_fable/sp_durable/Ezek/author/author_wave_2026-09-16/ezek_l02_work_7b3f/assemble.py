# -*- coding: utf-8 -*-
import json, hashlib, os

D = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l02_work_7b3f'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_02_worklist.json'
BRIEF = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\AUTHOR_WAVE_BRIEF.v1.md'
LAUNCH = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\ezek_author_l02_LAUNCH.md'
B = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'

lane = json.load(open(LANE, encoding='utf-8'))
ITEMS = lane['your_worklist_items']
IDS = ['L02-I%02d' % i for i in range(len(ITEMS))]

prose = json.load(open(os.path.join(D, 'prose_edits.json'), encoding='utf-8'))
refs = json.load(open(os.path.join(D, 'refs_edits.json'), encoding='utf-8'))
EDITS = prose + refs

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

SOURCES = [
 dict(path=LAUNCH, sha256=sha(LAUNCH), read='the whole launch brief, first, by exact path'),
 dict(path=BRIEF, sha256=sha(BRIEF), read='the whole controlling brief: CUT-RULE and its precedence clause, CONF-CAL with the #e14 Q2 refinement, DEF-A4-ARGUED and the eleven ROLE tokens, A6-b, C2-amended, A12-b, D11, the A9/A16 weighing duty, the rotation rule, the ch 20/21 dual-writing rule, the OW-18 tiers, MARKS-3D, the execution order and section 12 on the v2 inventory'),
 dict(path=LANE, sha256=sha(LANE), read='the whole lane file: all 27 rows at their complete current bytes, all 83 worklist items, the role vocabulary, the rows-file digest and the reminder'),
 dict(path=os.path.join(B, 'Ezek_oshb.txt'), sha256=sha(os.path.join(B, 'Ezek_oshb.txt')),
      read='the whole witness, loaded verse-keyed; consonantal-skeleton sweeps for the eye-not-sparing refrain, kevod-YHWH, nehar-Kevar, be-marot-elohim, bet-(ha-)meri and the wheel vocabulary; exact formula positions and verse-final tests at MT 6:10, 6:14, 7:4, 7:9, 7:27, 11:15, 11:16, 11:17, 11:21, 12:20, 13:9, 13:10, 13:23, 14:13, 14:20, 14:21, 15:8, 16:14, 16:19'),
 dict(path=os.path.join(B, 'pmarks_Ezek.json'), sha256=sha(os.path.join(B, 'pmarks_Ezek.json')),
      read='marks for chapters 6-17 (all 42 mark-bearing verses in that stretch), the marks_note direction convention, marks_tally, the paseq LIST (one entry per occurrence, counted per verse for chs 6-16), the kq dict whose values are LISTS of K-Q pair strings, kq_tally, other_segs (empty) and notes_other for chs 6-16'),
 dict(path=os.path.join(B, 'book_strategy_Ezek.md'), sha256=sha(os.path.join(B, 'book_strategy_Ezek.md')),
      read='section 2f disclosure objects, section 4 marker policy, the arithmetic guard, the chapter-division paragraph, the 7-10 target density, the over-split guard and all of section 7'),
 dict(path=os.path.join(B, 'ezek_device_inventory.v2.json'), sha256=sha(os.path.join(B, 'ezek_device_inventory.v2.json')),
      read='v2 as the governing inventory: word_event_formula 39 and its verse list, word_event_vayehi_any 41, son_of_man_address 93, recognition_formula 28, recognition_formula_2mp 21, recognition_formula_2fp 2, recognition_formula_adonai_variant 5 with verse_final_in_all_five, recognition_family_64, thus_says_the_lord_yhwh 122, messenger_formula_variant_census 126 in three shapes, utterance_of_the_lord_yhwh 81, utterance_short_yhwh 4, hand_of_yhwh_upon_me 7 with the single adonai-form verse, set_your_face 9, and vision_transport 33/46 with relation_to_the_strategy_closed_20'),
 dict(path=os.path.join(B, 'verse_inventory.json'), sha256=sha(os.path.join(B, 'verse_inventory.json')),
      read='numbering_face = WEB and the per-chapter verse counts, used for every span count in this deliverable'),
 dict(path=os.path.join(B, 'web_mt_offset_map.json'), sha256=sha(os.path.join(B, 'web_mt_offset_map.json')),
      read='rule.identity_outside_the_zone = true, the zone definition, zone_pairs and verification; MEASURED digest reported because the launch pinned none'),
 dict(path=os.path.join(B, 'tools', 'verse_map_web.json'), sha256=sha(os.path.join(B, 'tools', 'verse_map_web.json')),
      read='the whole WEB map, loaded verse-keyed on the clean field, for every A6 run measurement and for every quotation installed'),
 dict(path=os.path.join(B, 'ezek_device_inventory.json'), sha256='0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142',
      read='NOT OPENED. v1 is superseded for counts and list membership under C2-amended, so no figure in this deliverable comes from it. Its digest here is TRANSCRIBED from the launch table, not measured by me.'),
 dict(path=os.path.join(B, 'tools', 'verse_map_oshb.json'), sha256='408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901',
      read='NOT OPENED. Its digest here is TRANSCRIBED from the launch table, not measured by me. It was not needed: no row or citation in this lane falls in the ch 20/21 zone, the MT-keyed facts came from Ezek_oshb.txt and pmarks_Ezek.json directly, and the offset map states identity outside the zone.'),
]

A6_NO_EDIT = [
 dict(item='L02-I00', row='P01-011', field='boundary_rationale', run='know that i am yahweh the',
      judgement='A6-b EXEMPT, no edit',
      found="MEASURED: the 6-word run occurs once book-wide in the WEB, at web:Ezek.39.7. Two independent grounds for exemption. (1) The row NAMES the device: the clause it glosses is called 'the strict recognition formula' in the same sentence, so the run is the fixed rendering of a counted device and is a gloss of a census object, not a quotation. (2) The run is an artefact of crossing the row's own punctuation: the field reads \"...know that I am Yahweh'), the strict recognition formula\", so the 5th and 6th words of the matched run are the row's connective, not quoted material. The row's gloss also reads 'shall know' where web:Ezek.6.14 reads 'will know', so it is not a WEB quotation at all."),
 dict(item='L02-I01', row='P01-011', field='strongest_rejected_alternative', run='to the mountains of israel',
      judgement='coincidental collocation, not a quotation, no edit',
      found="MEASURED: the 5-word run occurs once book-wide in the WEB, at web:Ezek.36.1, thirty chapters from this row. The row's sentence is its own description of the addressee of the preceding unit ('turns from the oracle to the mountains of Israel to a gesture command'), and that addressee is MEASURED in span-adjacent bytes: web:Ezek.6.2 reads 'set your face toward the mountains of Israel' and web:Ezek.6.3 addresses the mountains. The row makes no claim about 36:1 and reproduces nothing of it beyond the addressee title, which is also the second limb of A6-b. No convention is owed."),
 dict(item='L02-I03', row='P01-012', field='boundary_rationale', run="moreover yahweh's word came to me saying",
      judgement='A6-b EXEMPT, no edit',
      found="MEASURED: the 7-word run occurs at 7 WEB verses - 7:1, 12:17, 17:11, 22:1, 28:11, 35:1, 36:16 - one of which, web:Ezek.7.1, is this row's own onset verse and is already cited as oshb:Ezek.7.1 immediately before the gloss. The row NAMES the device in the same clause ('a strict word-event'), and the run is nothing but the WEB's fixed rendering of that counted class, so A6-b exempts it. The boss sweep's cited verse set omitted 7:1; that omission is recorded, not acted on."),
 dict(item='L02-I04', row='P01-012', field='boundary_rationale', run='then you will know that i am yahweh',
      judgement='A6-b EXEMPT, no edit',
      found="MEASURED: the 8-word run occurs at 17 WEB verses, one of them web:Ezek.7.4, this row's own close verse. The row NAMES the device in the same clause ('the 2mp wider-family recognition close'), so the run is the fixed rendering of a counted device and A6-b exempts it."),
 dict(item='L02-I17', row='P01-014', field='boundary_rationale', run='then they will know that i am yahweh',
      judgement='A6-b EXEMPT, no edit',
      found="MEASURED: the 8-word run occurs at 22 WEB verses, one of them web:Ezek.7.27, this row's own close verse. The row NAMES the device in the same clause ('the strict recognition formula'), so A6-b exempts it."),
 dict(item='L02-I36', row='P02-005', field='boundary_rationale', run='to the threshold of the house',
      judgement='coincidental collocation, not a quotation, no edit',
      found="MEASURED, and this one matters: the 6-word run occurs once book-wide in the WEB, at web:Ezek.9.3, which is OUTSIDE this row's span. The sentence carrying it is the row's own paraphrase of oshb:Ezek.10.4, and web:Ezek.10.4 does NOT read that way - it reads 'and stood OVER the threshold of the house', where 9:3 reads 'TO the threshold of the house'. So the row is describing 10:4 and is not quoting 9:3; installing an in-field reference to 9:3 would assert a quotation the row does not make and attach it to the wrong verse. No convention is owed, and the measured divergence between 10:4 and 9:3 is reported here rather than silently paraphrased away."),
 dict(item='L02-I58', row='P02-011', field='boundary_rationale', run='on the other side of the',
      judgement='coincidental collocation, not a quotation, no edit',
      found="MEASURED: the 6-word run occurs once book-wide in the WEB, at web:Ezek.45.7, a land-allotment verse. The row's phrase is its own metaphor - 'the 12:8 re-onset on the other side of the seam' - and shares no content word with 45:7's subject matter. The row makes no claim about 45:7. No convention is owed."),
]

DISCHARGED = sorted(set(
  [i for e in EDITS for i in e['worklist_item_ids']] + [j['item'] for j in A6_NO_EDIT]))
NOT_DISCHARGED = []

missing = [i for i in IDS if i not in DISCHARGED and i not in [n['item'] for n in NOT_DISCHARGED]]
dupe = [i for i in DISCHARGED if i in [n['item'] for n in NOT_DISCHARGED]]
assert not missing, 'SILENT DROP: %s' % missing
assert not dupe, 'item in both lists: %s' % dupe
assert len(DISCHARGED) + len(NOT_DISCHARGED) == len(IDS), (len(DISCHARGED), len(NOT_DISCHARGED), len(IDS))

ESC = [
 dict(row='P02-003', what="device_notes reads 'No K/Q and no paseq beyond the one already disclosed at oshb:Ezek.8.14 sit in 8:14-18'. That is MEASURED FALSE: pmarks_Ezek.json's paseq layer is a LIST with one entry per occurrence, and chapter 8's entries are Ezek.8.1, 8.3, 8.6 and 8.10 only - there is no paseq at MT 8:14. What this row discloses at 8:14 is a SAMEKH. The true statement is that 8:14-8:18 carries no paseq and no K/Q at all.",
      why_i_did_not_write_it="No worklist item of mine names P02-003's device_notes, and the correction belongs to the disclosure sweep (execution step 6), not to the grounds sweep my two P02-003 edits sit in. Writing it would put an unruled disclosure change into a pooled grounds mutation and could collide with a disclosure lane."),
 dict(row='P02-006', what="strongest_rejected_alternative claims the wheel vocabulary 'does not recur outside 10:6-17 and 1:15-21'. MEASURED FALSE against Ezek_oshb.txt at its pinned digest: the aleph-vav-pe stem occurs on 15 verses - 1:15, 1:16, 1:19, 1:20, 1:21, 3:13, 10:6, 10:9, 10:10, 10:12, 10:13, 10:16, 10:19, 11:22, 23:43 - so MT 3:13, 10:19, 11:22 and 23:43 all fall outside the two named ranges; and gimel-lamed-gimel-lamed occurs on 5 verses - 10:2, 10:6, 10:13, 23:24, 26:10 - so 23:24 and 26:10 also fall outside. The distinctness claim the row rests part of its case on does not reproduce.",
      why_i_did_not_write_it="All five of my P02-006 items are A4 citation installs, which touch boundary_evidence_refs only. No item orders a grounds rewrite on this row, and rewriting a rejected-alternative field unasked would be an unruled grounds change."),
 dict(row='P02-018', what="device_notes calls the two 2fp recognition clauses (13:21, 13:23) 'an observed gender variant outside the two counted recognition families named in the book-wide inventories' and claims 'no digit count is claimed for this variant'. Under C2-amended the inventory governs counts and list membership, and ezek_device_inventory.v2.json at its pinned digest now carries recognition_formula_2fp as a counted class: count 2, verses MT 13:21 and 13:23, tier MEASURED, and a disjoint member of the 64-verse family decomposition. The sentence is therefore stale against the governing input.",
      why_i_did_not_write_it="My only P02-018 item is the A6 install in boundary_rationale. No item orders this field, and v2-alignment of disclosure prose is not in this lane's worklist."),
 dict(row='P02-016', what="After the ordered I67 rewrite of boundary_rationale, two places in this row still describe the 13:9 close on the superseded basis: device_notes ('The recognition-type clause at 13:9 is deliberately not tagged with a recognition.* signal key tied to either counted family, since its divine-name form differs from both'), and the existing refs entry for oshb:Ezek.13.9 ('an observed variant, disclosed but not claimed as a member of either the 28- or the 21-verse counted sweeps'). v2 makes the adonai-form recognition a counted 5-verse class, all five verse-final, MT 13:9 among them.",
      why_i_did_not_write_it="The order names only the ground, which lives in boundary_rationale and is where I wrote. The brief states that existing refs entries are NOT re-tokenised in this wave, and no item names device_notes on this row, so the residue is reported rather than rewritten. The row is internally inconsistent until it is."),
 dict(row='P02-009', what="Worklist item L02-I52 orders 'correct the measured-false device denial in the unit-type field'. MEASURED: the unit_type field of this row holds exactly the token 'salvation_oracle' and contains no denial of any kind; the measured-false denial - '(gather and return is not stated here, ...)' - is a unique substring of device_notes, the field that carries this row's unit-type justification. The order's field name does not match the bytes.",
      why_i_did_not_write_it="I did write the correction, in device_notes, where the bytes are, and I left unit_type at 'salvation_oracle' - which oshb:Ezek.11.17 now supports rather than undercuts. The field-name mismatch is raised so the controlling agent can confirm that reading rather than have it inferred from my edit."),
 dict(row='P01-011', what="The onset ground names 'the pe-marked recognition close that precedes it stands at oshb:Ezek.6.10'. MEASURED against Ezek_oshb.txt: the recognition clause at MT 6:10 is NOT verse-final - the consonantal skeleton carries it at characters 0-17 of 53, with the independent clause 'lo el chinam dibarti la'asot lahem hara'ah hazot' filling the rest of the verse. Under CUT-RULE limb (b), which requires the preceding verse to END on a close-role formula, VERSE-FINAL and not mid-verse, 6:10 cannot license the messenger sub-onset at 6:11; and under #e14 Q2 that shape is the weak mid-verse one, since the words after the formula are an independent clause and not a dependent completion. The row's onset does stand, on CUT-RULE limb (a): the addressee changes from the mountains of Israel to the prophet's gesture command, which the row's prose already argues.",
      why_i_did_not_write_it="My only P01-011 items are one A4 install and two A6 judgements; no item orders a grounds change on this row, and restating an onset ground unasked is a grounds change. The pe on MT 6:10 is real (MEASURED from pmarks_Ezek.json) and the row's conclusion is unaffected, but the stated route to it leans on a limb the bytes do not supply."),
 dict(row='P02-003', what="Confidence consequence of the ordered rewrite. Having weighed the 8:15/8:16 rival as CUT-RULE-licensed on both faces (the 8:15 pointer close on the near face, the 8:16 transport on the far face) and held it on stated grounds, the row now matches CONF-CAL's second limb exactly - 'a two-faced rival is held on stated grounds' - which is MEDIUM. The row carries medium_low.",
      why_i_did_not_write_it="No CONFIDENCE item exists for P02-003, and CONF-CAL states that no row's confidence is raised unasked. The grade is left untouched and the mismatch is raised for the controlling agent."),
 dict(row='P01-013', what="Pooling note, not a defect. This row's boundary_evidence_refs needed BOTH an in-place amendment (item L02-I11, an A6 delimiter inside an existing entry) and three A4 appends. Mixing one set edit with append_ref edits against the same expected_before is undefined, so I emitted ONE set edit carrying the complete final list. Its sweep is labelled 'a4' (execution step 4) but it also carries one a6 component (step 5).",
      why_i_did_not_write_it="Nothing is withheld - the edit is in the deliverable. It is flagged so the orchestrator can re-pool or split it deliberately rather than discover the mixed sweep at landing."),
]

VER = [
 "Digests verified before reading, by exact path. The two required files matched their launch-pinned values exactly (AUTHOR_WAVE_BRIEF.v1.md ccb7026f..., lane_02_worklist.json 74477513...). Of the other inputs, Ezek_oshb.txt, pmarks_Ezek.json, book_strategy_Ezek.md, ezek_device_inventory.v2.json, verse_inventory.json and tools/verse_map_web.json all matched their pinned values. web_mt_offset_map.json had no pinned digest and MEASURES b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887.",
 "MARKS, MEASURED from pmarks_Ezek.json: chapters 6-17 carry marks on exactly these 42 verses - PE on 6:10, 6:14, 7:4, 7:22, 7:27, 11:1, 11:6, 11:13, 11:25, 12:7, 12:16, 12:20, 12:25, 13:16, 14:1, 14:11, 14:20, 14:23, 15:8, 16:35, 17:10, 17:24; SAMEKH on 8:6, 8:14, 9:3, 9:11, 11:15, 11:16, 12:28, 13:7, 13:12, 13:19, 14:3, 14:5, 14:8, 15:5, 16:50, 16:58, 16:63, 17:8, 17:18, 17:21. Every mark claim in my 27 rows reproduces. Four absence claims reproduce as stated: no mark on MT 7:9 (P01-013), none anywhere in 8:7-8:13 (P02-002), none anywhere in chapter 10 (P02-005/006/007), none between 16:1 and 16:14 and none in 16:15-16:19 (P03-002/003). Two more reproduce: no mark at 13:23 (P02-018) and none at 14:4 (P02-019).",
 "PASEQ, MEASURED from the pmarks paseq LIST, which carries one entry per occurrence so a verse can repeat: chapters 6-16 carry 6:13 x1, 7:11 x1, 8:1 x1, 8:3 x1, 8:6 x1, 8:10 x1, 9:2 x2, 9:3 x1, 9:11 x1, 10:2 x1, 12:25 x1, 13:11 x1, 13:18 x2, 13:20 x1, 14:4 x1, 14:6 x1, 14:21 x1, 16:14 x1, 16:43 x1, 16:52 x1. Every per-verse paseq count in my rows reproduces, including the doubles at 9:2 and 13:18. ONE paseq claim does NOT reproduce: P02-003's device_notes implies a paseq at MT 8:14, and there is none - escalated.",
 "KETIV/QERE, MEASURED from the pmarks kq dict, whose values are LISTS of concatenated K-Q pair strings and NOT dicts (the trap the brief names). Every K/Q disclosure in my rows reproduces, including the doubled-note verses MT 9:5 (two notes) and MT 16:13 (two notes), and the shared triad note at MT 14:14 and MT 14:20. The absence claims reproduce too: no K/Q in 8:7-8:13, 10:9-10:17, 10:18-10:22, 11:1-11:13, 11:14-11:21, 11:22-11:25, 12:1-12:7, 12:17-12:20, 12:26-12:28, 13:1-13:9 or 15:1-15:8.",
 "EDITORIAL NOTES, MEASURED from pmarks notes_other: chapters 6-16 carry notes on exactly 9 verses - 9:11 (vowel), 12:10 (vowel), 12:12 (accent), 13:16, 13:19, 14:14, 14:20 (the Qere-adaptation class), 16:24 and 16:54. Every note claim in my rows reproduces, and so do the silences claimed for 15:1-15:8, 16:1-16:14 and 16:15-16:19.",
 "A6 RUNS. First pass, my own normalizer returned ZERO WEB hits for three INSTALL runs - L02-I08 at 7:5, L02-I16 at 7:10 and L02-I63 at 12:22. That was MY defect, not an absence: my normalizer kept apostrophes as word characters, and all three verses open a nested quotation with a single quote, so 'A disaster' tokenised as \"'a disaster\". After dropping apostrophes at word boundaries, all three measure exactly one hit at exactly the cited verse. Reporting what I found rather than a boolean is the point: the correct response was to fix the reader, not to declare the claims unsupported.",
 "A6 RUNS, MEASURED over tools/verse_map_web.json after the fix: all 28 A6 and A6_UNION runs exist in the WEB, and every cited verse is a genuine occurrence. Occurrence counts: 1 hit for I00, I01, I08, I09, I10, I11, I16, I18, I22, I23, I36, I43, I44, I47, I49, I54, I57, I58, I63, I66, I68, I79; 2 for I70; 4 for I34; 5 for I53; 7 for I03; 17 for I04; 22 for I17. The boss sweep's web_refs omitted in-span occurrences in three cases (I03 omits 7:1, I04 omits 7:4, I17 omits 7:27 and 6:14); recorded, and it does not change any judgement.",
 "FOUR MISQUOTATIONS FOUND while installing the A6 convention, each corrected to the verse's own wording: P02-009 wrote 'this land is given to us for a possession' where web:Ezek.11.15 reads 'has been given'; P03-003 wrote 'played the whore' where web:Ezek.16.15 reads 'played the prostitute'; P01-013 and P01-014 both attributed the five-word run 'my eye will not spare' to 7:9, and that wording is MEASURED at web:Ezek.7.4 only, 7:9 reading \"won't spare\". The underlying Hebrew refrain does stand at both: a consonantal-skeleton sweep of lo-tachos-eini over Ezek_oshb.txt returns exactly 5 verses, MT 5:11, 7:4, 7:9, 8:18 and 9:10, which reproduces P01-013's list verse for verse.",
 "OTHER PROSE SWEEPS RE-DERIVED from Ezek_oshb.txt and all reproducing as the rows state them: kevod-YHWH 9 verses (1:28, 3:12, 3:23, 10:4, 10:18, 11:23, 43:4, 43:5, 44:4) for P02-005; nehar-Kevar 8 verses (1:1, 1:3, 3:15, 3:23, 10:15, 10:20, 10:22, 43:3) with three inside chapter 10 for P02-006/007; be-marot-elohim 3 verses (1:1, 8:3, 40:2) for P02-001; the rebellious-house device 12 verses as the union of bet-meri (7) and bet-ha-meri (6) less the shared MT 12:2, none of them in chapters 4-11, for P02-011. ONE sweep does NOT reproduce: P02-006's wheel-vocabulary distinctness claim - escalated.",
 "INVENTORY FIGURES taken from ezek_device_inventory.v2.json only, never v1, and cross-checked where a row cites them: word-event strict 39 (P01-012, P02-009, P02-011), vayehi-any 41 with exactly MT 12:8 and 24:1 as the infixed pair (P02-011, P02-012), strict recognition 28 and the 2mp family 21 kept unblended (P02-012, P02-013, P02-016), utterance long form 81 (P02-009, P02-014), hand-of-YHWH 7 with MT 8:1 the only adonai-form verse (P02-001), set-your-face 9 including MT 13:17 (P02-018), and the messenger long form 122 of 126 total messenger verses in three shapes.",
 "TRANSPORT CLASS handled under section 12's hold. MEASURED from v2's relation_to_the_strategy_closed_20: every transport verse this lane touches - MT 8:3, 8:7, 8:14, 8:16, 11:1 and 11:24 - is in the strategy's UNCHANGED closed 20, and none of the 13 verses the v2 predicate adds (3:12, 3:14, 37:2, 40:2, 40:3, 40:24, 40:48, 42:15, 43:1, 44:1, 46:21, 47:3, 47:4) falls anywhere in my span or in any citation of mine. So the held 20-versus-33 question is not engaged by any word I wrote: my one transport-membership claim, 8:16 in the P02-003 rewrite, is written against the strategy's closed list and does not resolve the hold.",
 "CH 20/21 ZONE: not engaged, and checked rather than assumed. My rows span web:Ezek.6.11-Ezek.16.19 and my citations run web:Ezek.6.14 to web:Ezek.16.20, so no row and no citation touches WEB 20:45-49, WEB chapter 21 or MT chapter 21. web_mt_offset_map.json states rule.identity_outside_the_zone = true with verification GREEN and equal totals of 1273, so the WEB face I wrote the A4 entries on is verse-for-verse the MT face for every entry. No dual writing is owed; none is omitted.",
 "ARITHMETIC re-counted from verse_inventory.json on its declared WEB face, never from the MT chapter sizes: 8:7-8:18 = 12 (item I27 confirmed, 'fourteen' was wrong), 8:16-8:18 = 3 (item I29 confirmed, 'four' was wrong), 10:1-10:17 = 17 (item I37 confirmed, 'sixteen' was wrong), and 14:12-14:23 = 12 for the A7 disclosure. Two further counts used in the P02-003 rewrite: 8:14-8:15 = 2 and 14:21-14:23 = 3.",
 "CUT-RULE derivations behind the grounds rewrites, each from a verse-final test on the consonantal skeleton. MT 14:20's utterance formula is NOT verse-final (characters 28-41 of 81, followed by an independent conditional clause), and no addressee-marking device stands at MT 14:21 (son-of-man falls at 14:3 and 14:13 only, no set-your-face anywhere in chapter 14), so both CUT-RULE limbs fail and 14:21's messenger formula - MEASURED as one of the 122 - is a paragraph, which is what item I74 ordered stated. MT 11:15 and MT 11:16 likewise end on no close-role formula, and the messenger formula in each of 11:16 and 11:17 stands at the verse head after lakhen emor, so the twin samekhs on 11:15 and 11:16 cannot license the 11:16/11:17 rival. MT 13:9's adonai-form recognition IS verse-final (characters 108-131 of 131), confirming v2's verse_final_in_all_five. MT 7:9's 2mp recognition is followed only by the participle makkeh, a dependent completion, so under #e14 Q2 it is verse-final in effect and is NOT the weak mid-verse shape.",
 "EVERY expected_before in this deliverable was taken programmatically from the lane file's your_rows and never retyped. The 25 prose set edits were produced by exact-substring replacement on the current value with an assertion that each target substring occurs EXACTLY ONCE in that field; the builder aborts otherwise, and it did not abort. The two whole-field replacements (P02-003 and P02-019 strongest_rejected_alternative) and the two append-style rewrites (P02-009 strongest_rejected_alternative, P02-020 strongest_rejected_alternative) carry the unmodified current value as expected_before by direct reference. The 42 append_ref edits on one row all share that row's current list as expected_before, as the brief requires.",
 "ROLE TOKENS: all 45 ruled A4 citations carry exactly one token from the eleven, checked against the lane file's role_vocabulary by assertion. Distribution: WARRANT-close 14, WARRANT-rival 13, WARRANT-onset 8, ANCHOR 5, DISCLOSURE-mark 2, QUOTE 2, WARRANT-absence-over-range 1. Each entry's citation string was asserted equal to the ruled citation, so no range was expanded into per-verse entries and no single verse was written as a range. No existing entry was re-tokenised.",
 "ROTATION RULE: all 45 free-text annotations are at most 6 words and all 45 are DISTINCT from one another, so no 7-gram form can arise from repetition. The at-least-4-formulations floor is met for WARRANT-close (14 of 14), WARRANT-rival (13 of 13), WARRANT-onset (8 of 8) and ANCHOR (5 of 5). It is unreachable for DISCLOSURE-mark (2 entries), QUOTE (2 entries) and WARRANT-absence-over-range (1 entry), because a lane cannot carry 4 distinct formulations of an annotation it uses fewer than 4 times; every one of those is still distinct and under the ceiling, so the rule's purpose holds. Stated rather than padded.",
 "SEVEN-GRAM SELF-CHECK, run over my own output before landing rather than left for the gate. For every prose edit I diffed the 7-word shingles the new value adds against the shingles of the value it replaces, then compared every pair of edited fields. The first draft collided on 22 pairs, and almost all of it was my own boilerplate repeated across rows - 'a mark is recorded on the verse it follows', 'a closed-section boundary is weak corroboration that never outranks a licensed text signal', 'counted on the declared WEB face from verse_inventory.json', 'is the live rival and is weighed here under A9/A16'. I applied the rotation rule's principle to the prose as well as to the annotations, varying the formulation and never the fact, and the count is now 2 pairs. Both remaining pairs ARE the mandated A6 quotation plus its reference and cannot be rotated without falsifying a quotation: the run 'my eye will not spare' with (web:Ezek.7.4), installed on P01-013 and on P01-014 under two separate items, and the 8:3 quotation installed in two fields of P02-001 under two separate items. Reported, not mangled.",
 "NO SEAM MOVED. All 83 items are marked moves_seam = false in the lane file, and no edit in this deliverable touches span, osis_start, osis_end, decision_id, chunk_index_in_book, writer_part, writer_decision_id, writer_attempt_id or any other writer-identity field. The fields touched are boundary_rationale, strongest_rejected_alternative, device_notes, literature_type_guess, boundary_evidence_refs and confidence, and confidence moves on exactly one row, P02-019, under exactly one ruled item.",
]

UNRES = [
 "ITEM IDS ARE MINE. The lane file's your_worklist_items array carries NO id field on any item, so I minted stable ids from position: L02-I00 through L02-I82, zero-padded, index into your_worklist_items in the file as delivered. The item_id_scheme block below maps every id to its row, class, field and action so the mechanical check against my edits can be re-keyed if the orchestrator uses different ids.",
 "Seven of the 83 items are discharged by a no-edit author judgement (five A6-b exemptions or coincidental-collocation findings, two of which I record as measured divergences) and so produce no edit. They are L02-I00, I01, I03, I04, I17, I36 and I58, and every one is set out with its measurement in the a6_judgements_no_edit block. If the mechanical check requires an edit per discharged item, these seven will read as unmatched: they are judgements the worklist asked for, not work left undone.",
 "Two worklist items name a field that does not hold what the item describes. L02-I15 carries no field at all (A10 disclosure of the witness's sectioning) and I placed it in device_notes, which brief section 0 lists as a grounds field and which already held the row's mark-absence sentence. L02-I52 names 'the unit-type field' for a denial that is MEASURED to live in device_notes; I corrected it there. Both placements are judgements a reviewer may reverse.",
 "P02-003's confidence and P02-016's residual v2-stale sentences are left as they stand, for the reasons in escalations. Both leave a row internally inconsistent with its own repaired grounds until a further item covers them.",
 "The P01-013 refs edit is a set rather than a chain of append_ref edits, because that one row needed an in-place amendment alongside its appends. If the orchestrator's applier expects append_ref only on that field, this edit must be split by hand - and splitting it cannot be done by expected_before alone, since the second half would have to pin a list that does not exist until the first half lands.",
 "I did not open tools/verse_map_oshb.json or ezek_device_inventory.json. Neither was needed - no verse in this lane is in the ch 20/21 zone, and v1 is superseded for counts - but their digests in my sources block are therefore TRANSCRIBED from the launch table, not MEASURED by me. Stated so no reader takes them as verified here.",
 "P02-001's literature_type_guess and P02-003's boundary_rationale both still carry 'sweep: 20 verses book-wide' for the transport class. I left every such figure byte-untouched: under section 12 the 20-versus-33 question is the controlling agent's, and changing the figure either way inside an unrelated edit would pre-empt the hold. Where I had to name membership (8:16), I named the strategy's closed list explicitly instead of a count.",
 "Two 7-gram collisions survive in my output and I could not remove them honestly: the same A6 quotation plus its in-field reference is ordered twice, once on P01-013 and once on P01-014 for the run 'my eye will not spare' at web:Ezek.7.4, and twice inside P02-001 for the 8:3 phrase. A quotation cannot be reworded without ceasing to be one, so if the ngram7 gate flags these the remedy is an exemption for delimited-and-referenced quotations, not a rewrite. I have not assumed such an exemption exists.",
 "Every count I wrote into a row carries its source in the same sentence. Where a figure came from a pinned artefact it is named (verse_inventory.json, ezek_device_inventory.v2.json, pmarks_Ezek.json); where it came from my own sweep of Ezek_oshb.txt the predicate is given in the prose so the number can be re-derived. No figure in any edit is labelled MEASURED on the strength of my having read it.",
]

OUT = dict(
 lane='ezek_author_l02',
 attempt_id='ezek_author_l02_a1',
 execution_id='ezek_author_l02_a1#e1',
 rows_file_sha256_pinned_by_lane=lane['rows_file_sha256'],
 item_id_scheme='L02-I<NN>, NN = zero-padded 0-based index into your_worklist_items of lane_02_worklist.json at sha256 744775131f147a8e1424dee62636079c8433d87dec48ef1c18eb8569dd6dc8e6. The lane file carries no item ids of its own; this is the only key available, and item_id_map below is the full crosswalk.',
 item_id_map=[dict(item='L02-I%02d' % i, row=it['row_id'], cls=it['cls'], field=it.get('field'),
                   citation=it.get('citation'), run=it.get('run'), action=it.get('action'))
              for i, it in enumerate(ITEMS)],
 sources=SOURCES,
 edits=EDITS,
 a6_judgements_no_edit=A6_NO_EDIT,
 items_discharged=DISCHARGED,
 items_NOT_discharged=NOT_DISCHARGED,
 escalations=ESC,
 changes_made_or_no_change=(
  "%d edits across all %d rows, discharging all %d worklist items: %d prose set edits, 1 set edit on a "
  "boundary_evidence_refs list that needed an in-place amendment alongside its appends, %d append_ref edits, "
  "%d set_confidence, and %d items discharged by a no-edit author judgement recorded in a6_judgements_no_edit. "
  "By sweep, counted off the edits themselves: confidence %d (P02-019 high -> medium); grounds %d across "
  "P01-013, P02-003, P02-009, P02-016, P02-019 and P02-020, carrying the six GROUNDS orders and the A9/A16 "
  "weighings; a4 %d installing all 45 ruled citations, each with exactly one ROLE token and every range "
  "citation taking a single range entry; a6 %d installing the double-curly delimiter and the in-field web: "
  "reference at 21 runs, with 7 further runs judged exempt or coincidental and no edit made; vocab %d carrying "
  "two of the three arithmetic corrections, the third riding with the P02-003 grounds rewrite. No seam moved, "
  "no span field touched, no confidence raised unasked. Four misquotations of the WEB were found while "
  "installing the A6 convention and corrected to the cited verses' own wording; three measured-false or "
  "superseded grounds (the 8:16 transport denial, the 11:17 gather-and-return denial, the 14:21 messenger "
  "denial) were corrected as ordered; and one mark was re-read as corroborating the rival rather than the row "
  "(the pe on MT 14:1). Four further defects found outside my worklist are escalated, not written."
  % (len(EDITS), len(set(e['row_id'] for e in EDITS)), len(IDS),
     sum(1 for e in EDITS if e['op'] == 'set' and e['field'] != 'boundary_evidence_refs'),
     sum(1 for e in EDITS if e['op'] == 'append_ref'),
     sum(1 for e in EDITS if e['op'] == 'set_confidence'),
     len(A6_NO_EDIT),
     sum(1 for e in EDITS if e['sweep'] == 'confidence'),
     sum(1 for e in EDITS if e['sweep'] == 'grounds'),
     sum(1 for e in EDITS if e['sweep'] == 'a4'),
     sum(1 for e in EDITS if e['sweep'] == 'a6'),
     sum(1 for e in EDITS if e['sweep'] == 'vocab'))),
 verification_evidence=VER,
 unresolved_uncertainty=UNRES,
 e19_selfreport=(
  "Exact-path law kept. Every file I opened is in the sources block and every one was named by exact path in "
  "the launch brief or the controlling brief; I ran no directory listing, no glob and no recursive search, and "
  "I tested for no directory. Every digest was verified BEFORE the file was read, and the two required files "
  "were verified before anything else was opened. Lane blindness kept: I read no other lane's rows or "
  "deliverable, nothing under reviews/, no peer packet, no fix-up order, no cure claim, no S-review, no "
  "transcript, and no ruling beyond what the controlling brief and my own worklist items quote. Hygiene: all "
  "work is in one uniquely-named private subdirectory, scratchpad/ezek_l02_work_7b3f, with no bare filename "
  "reused at scratch root; nothing was written anywhere under C:\\wt\\logos-t423-m8-fable; and this file was "
  "written at my first stage and rewritten at every stage after (E-29). No git, no receipts, no registry, no "
  "validator run, no row mutation."),
 limit=(
  "Four things this deliverable does not settle. (1) The seven no-edit A6 judgements rest on my reading of "
  "'the row names the device' and of what counts as a coincidental collocation; the measurements behind each "
  "are given so a reviewer can disagree with the judgement without re-measuring. (2) Role-token choice is a "
  "weight judgement, and two are genuinely arguable: web:Ezek.11.5 on P02-008, which the boundary_rationale "
  "calls internal texture while the rejected alternative weighs it, so DISCLOSURE-device would also be "
  "defensible and I chose WARRANT-rival; and web:Ezek.10.1-Ezek.10.8 on P02-006, where the token's stated "
  "trigger (an absence-over-range claim) and the WARRANT caution pull opposite ways. (3) Where an order named "
  "a field that does not hold what it describes (L02-I15, L02-I52) I placed the writing where the bytes are "
  "and said so; that is a judgement, not a ruling. (4) I did not resolve, and did not touch, the held "
  "transport 20-versus-33 question, P02-003's confidence grade, MT 33:20's sof pasuq (outside my span and not "
  "engaged), or any of the four escalated defects outside my worklist."),
)

path = os.path.join(D, 'ezek_author_l02_deliverable.json')
json.dump(OUT, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path)
print('edits=%d  discharged=%d  not_discharged=%d  total_items=%d' % (
    len(EDITS), len(DISCHARGED), len(NOT_DISCHARGED), len(IDS)))
