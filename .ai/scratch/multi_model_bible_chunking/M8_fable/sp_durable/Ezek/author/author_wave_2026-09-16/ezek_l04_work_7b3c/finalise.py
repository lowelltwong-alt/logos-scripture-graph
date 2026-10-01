# -*- coding: utf-8 -*-
import json, io, hashlib, collections

W = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l04_work_7b3c'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_04_worklist.json'
D = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'
lane = json.load(open(LANE, encoding='utf-8'))
EDITS = json.load(open(W + r'\edits.json', encoding='utf-8'))
IDS = json.load(open(W + r'\item_ids.json', encoding='utf-8'))
ITEMS = lane['your_worklist_items']

covered = set()
for e in EDITS:
    covered |= set(e['worklist_item_ids'])

# the five ruled AUTHOR_JUDGEMENT items whose honest outcome is "no edit owed"
NOEDIT = {}
def nj(idx, finding):
    NOEDIT[IDS[idx - 1]] = finding

nj(59, "A6_UNION, P06-010, run 'by the hand of strangers'. WHAT I FOUND, not whether I agreed: (a) the run IS real in the WEB - a whole-book scan of tools/verse_map_web.json puts it at exactly one verse, web:Ezek.28.10 (1 of 1273), which is this row's own close verse, so the peer's run is not an invention; (b) but it occurs in ZERO of P06-010's own fields - I normalised and scanned every string and every list member of the row and the run is absent, because the row quotes MT 28:10 in Hebrew only and never in English. A6's duty attaches to a run the ROW carries. This row carries none, so no delimiter and no in-field reference are owed and no edit is made. Tier: MEASURED for the WEB attachment and MEASURED for the row-field absence. This is 'nothing at the row', NOT 'the peer was wrong about the witness' - the two demand opposite responses and the difference is recorded deliberately.")
nj(66, "A6 AUTHOR_JUDGEMENT, P06-012, run 'to the house of israel' in boundary_rationale. WHAT I FOUND: the run occurs in the WEB at 16 verses book-wide (3:1, 3:4, 3:5, 3:17, 4:3, 12:6, 17:2, 20:27, 24:21, 28:24, 29:6, 33:7, 40:4, 43:10, 44:12, 45:8) - and one of them, web:Ezek.28.24, is INSIDE this row's span. The audit listed only 12:6, 17:2 and 20:27, so the flag's 'matches at a verse OUTSIDE this row's span' premise is INCOMPLETE, not false. JUDGEMENT: A6-b exempts, so no edit. 'house of Israel' is one of A6-b's expressly named addressee titles; the measured run is that title plus the preposition needed to attach it; and the row names the device it glosses, the addressee-class shift at 28:24. The row is describing 28:24, so the collocation with 12:6, 17:2 and 20:27 is coincidental and is not a quotation of any of them.")
nj(67, "A6 AUTHOR_JUDGEMENT, P06-012, run 'know that i am the lord'. WHAT I FOUND: the run occurs in the WEB at exactly five verses - 13:9, 23:49, 24:24, 28:24, 29:16 - which are verse for verse the v2 inventory's adonai-form recognition (D3) set of five, and one of them, web:Ezek.28.24, is in span (again omitted from the audit's three refs). JUDGEMENT: A6-b exempts squarely, so no edit. The run is the WEB's fixed rendering of a COUNTED DEVICE that A6-b names explicitly (the recognition formula), and the row names that device - it calls it an Adonai-form recognition variant and gives its 5-verse sweep. A second, independent ground: outside the six-word core the row is not reproducing the translation at all, since the row writes 'then they shall know that I am the Lord YHWH' where the WEB has 'Then they will know that I am the Lord Yahweh.'")
nj(68, "A6 AUTHOR_JUDGEMENT, P06-012, the same run in the refs field (boundary_evidence_refs entry 5 in file order, the Ezek.28.24 entry). WHAT I FOUND: the run sits inside a refs entry whose whole function is to name the device - 'addressee-class shift to the house of Israel; Adonai-form recognition close; parashah: samekh, single-witness'. JUDGEMENT: A6-b exempts, so no edit. A refs entry that names a census object IS the gloss-of-a-census-object case A6-b describes, and the addressee title is one A6-b lists. Separately noted: re-tokenising that pre-existing entry is out of scope, since the brief confines the ROLE vocabulary to installs.")
nj(71, "A6 AUTHOR_JUDGEMENT, P06-013, run 'for the house of israel'. WHAT I FOUND: the run occurs in the WEB at exactly three verses - 13:5, 29:21, 45:17 - and at NO verse inside this row's span; WEB 28:25, the verse the row is describing, reads 'When I have gathered the house of Israel from the peoples among whom they are scattered...', so the preposition 'for' is the ROW's own word and not the translation's. JUDGEMENT: not a quotation, so no edit. It is the row's own English construction around A6-b's inventoried addressee title, and the collocation with 13:5, 29:21 and 45:17 is coincidental - the row asserts nothing about any of those three verses.")

discharged = sorted(covered | set(NOEDIT))
assert len(discharged) == 85, (len(discharged), sorted(set(IDS) - set(discharged)))
assert set(discharged) == set(IDS), sorted(set(IDS) ^ set(discharged))

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

SOURCES = [
 {"path": D + r"\AUTHOR_WAVE_BRIEF.v1.md", "sha256": sha(D + r"\AUTHOR_WAVE_BRIEF.v1.md"),
  "read": "in full, before writing anything; digest verified against the launch table"},
 {"path": LANE, "sha256": sha(LANE),
  "read": "in full: all 22 rows' current bytes and all 85 worklist items, the item boilerplate read once per class after confirming it is uniform within the class"},
 {"path": D + r"\Ezek_oshb.txt", "sha256": sha(D + r"\Ezek_oshb.txt"),
  "read": "verse-keyed; read MT 22:31, 23:34, 23:35, 23:36, 24:6, 24:7, 24:8, 24:9, 24:10, 24:14, 24:15, 27:3, 27:36, 28:19, 29:6, 29:7, 29:8, 29:9, 29:10, 29:16, 29:17; whole-file scans for the ch-27 and ch-30 messenger and word-event formulae and for per-chapter verse counts"},
 {"path": D + r"\pmarks_Ezek.json", "sha256": sha(D + r"\pmarks_Ezek.json"),
  "read": "marks, paseq, kq, notes_other, marks_note, marks_tally, arithmetic_anomalies_resolved. A kq entry was read as the two-member LIST it is, not as a dict; a marks entry likewise is a LIST"},
 {"path": D + r"\book_strategy_Ezek.md", "sha256": sha(D + r"\book_strategy_Ezek.md"),
  "read": "lines 330-331 (density target and the scope of the 14-16 allowance), 345-358 (the over-split guard, line 351 verbatim, and the whole-chapter-span list), 398-416 (\u00a77 for chs 22-24, 25-32 and 33), and every heading line with its line number so \u00a76 and \u00a77 boundaries are measured not assumed"},
 {"path": D + r"\ezek_device_inventory.v2.json", "sha256": sha(D + r"\ezek_device_inventory.v2.json"),
  "read": "v2 as directed. formulae.messenger_formula_variant_census (incl. the short_form_yhwh_only 3-verse list and the_fourth_short_form_e13_R8), formulae.i_am_yhwh_spoken with its name-less sub-family, formulae.recognition_formula_2mp, formulae.utterance_short_yhwh, year_word_but_not_a_dateline, calendar_dates_not_datelines"},
 {"path": D + r"\ezek_device_inventory.json", "sha256": sha(D + r"\ezek_device_inventory.json"),
  "read": "NOT read for any count. Digest verified only, to confirm the v1 file on disk is the superseded one named in the brief and that I did not open it by mistake"},
 {"path": D + r"\verse_inventory.json", "sha256": sha(D + r"\verse_inventory.json"),
  "read": "digest verified; numbering_face = WEB taken from the brief and honoured in every reference I install"},
 {"path": D + r"\web_mt_offset_map.json", "sha256": sha(D + r"\web_mt_offset_map.json"),
  "read": "MEASURED AND REPORTED, since the launch table left it to be measured. rule.identity_outside_the_zone, rule.zone, zone_pairs, content_anchors, verification. This is the pinned authority for my statement that chs 22-30 are identity-mapped - I did not reach it by arithmetic"},
 {"path": D + r"\tools\verse_map_web.json", "sha256": sha(D + r"\tools\verse_map_web.json"),
  "read": "the WEB translation. Read the text of Ezek.25.2, 26.1, 26.3, 27.2, 27.36, 28.10, 28.12, 28.19, 28.24, 28.25, 29.9, and ran whole-book normalised scans (1273 verses) for each of the 14 A6/A6_UNION runs"},
 {"path": D + r"\tools\verse_map_oshb.json", "sha256": sha(D + r"\tools\verse_map_oshb.json"),
  "read": "digest verified; not needed, because no citation in my lane falls in the ch 20/21 divergence zone and the MT-keyed readings I needed came from Ezek_oshb.txt directly"},
]

ESC = [
 {"row": "P06-012 and P06-013",
  "what": "Strategy \u00a77 (book_strategy_Ezek.md lines 406-407) names the ch-28 tiling as '28:1-10 / 28:11-19 / 28:20-23 / 28:24-26', with 'the Israel coda 28:24-26 ... as its own salvation_oracle row'. These two rows take 28:20-24 and 28:25-26 instead, so the seam sits one verse later than the \u00a77 sketch. Under C2-amended the STRATEGY governs named cut sites, so this is a live divergence and not a wording matter.",
  "why_i_did_not_write_it": "It is a SEAM question and this wave never moves a seam. I also found that the bytes favour the rows: MEASURED from pmarks_Ezek.json, a SAMEKH stands on MT 28:24 and MT 28:26 and there is NO mark on MT 28:23, so the Masoretic division falls at 28:24/28:25 exactly where the rows cut; and MT 28:24 is one of the five adonai-form recognition (D3) verses in inventory v2, which reads more naturally as the Sidon verdict's close than as a coda's head. Both rows already weigh this alternative explicitly in their rejected-alternative fields, so nothing is hidden. The controlling agent should decide whether \u00a77's named cut site governs over the mark; both rows sit at medium_low, which is the conservative grade for a \u00a77-named region either way."},
 {"row": "P05-005",
  "what": "The row's stated reason for rejecting the 23:34/23:35 close is addressee continuity ('23:35 continues addressing the same second-person-singular target as a coda'). That reason is insufficient under the governing CUT-RULE. MEASURED from Ezek_oshb.txt, MT 23:34 ends VERSE-FINALLY on the utterance formula, and MT 23:35 opens with the long-form messenger formula, so CUT-RULE limb (b) is satisfied and the 23:34/23:35 rival is a LICENSED, two-faced rival - the addressee need not change for it to be licensed.",
  "why_i_did_not_write_it": "My order for this row was narrow: disclose the 23:35 SAMEKH. Rewriting the unordered strongest_rejected_alternative would be scope I was not given, and moving the seam is barred outright. I put the measured fact on the record inside the ordered grounds edit, without restating the rival's disposition, and escalate it here. The row's existing grade, medium, is already the correct CONF-CAL outcome for a licensed rival held on stated grounds, so nothing needs to change urgently; what needs re-ordering is the STATED GROUND, in a later grounds round."},
 {"row": "P07-004 and P07-009, and a self-inconsistency in a pinned input",
  "what": "Strategy \u00a77 line 409-410 reads '30:1-19 undated with four messenger paragraphs (30:2, 30:10, 30:13) inside'. The COUNT 'four' is byte-correct - MEASURED from Ezek_oshb.txt, the messenger formula occurs inside MT 30:1-19 at 30:2, 30:6, 30:10 and 30:13 - but the parenthetical LIST names only three, omitting MT 30:6. One pinned input's count and its own list disagree.",
  "why_i_did_not_write_it": "C2-amended directs me to report a self-contradicting input upward. It scored no row of mine and I therefore did not withhold any item on it: under C2-amended the INVENTORY governs list membership, the count is the byte-supported figure, and P07-004's device_notes already names all of 30:2, 30:6 and 30:10 correctly, so no row repeats the omission. Separately, these two rows split \u00a77's named 30:1-19 into 30:1-12 and 30:13-19; both weigh the nineteen-verse span explicitly in their rejected-alternative fields, and the seam is left exactly as found."},
 {"row": "P06-007 (recorded so a reader does not mistake a principled divergence for an oversight)",
  "what": "Strategy \u00a77 line 404-405 gives ch 26 as 'four messenger units (1-6, 7-14, 15-18 with the embedded qinah, 19-21) each with its own close - one row per unit is the default, held'. This row merges the last two into 26:15-21, so the lane's ch-26 tiling is three rows, not four.",
  "why_i_did_not_write_it": "No item ordered anything here and no seam may move. I verified the merge is CORRECT under the governing CUT-RULE rather than assuming either way: MEASURED from pmarks_Ezek.json a SAMEKH follows MT 26:18 and that is the only signal there, and MEASURED from Ezek_oshb.txt MT 26:19 reopens the messenger formula against the same 2fs addressee. So limb (a) fails for want of an addressee change, limb (b) fails because 26:18 ends on no close-role formula, and a mark alone never satisfies limb (b). \u00a77 marks the reading 'held', i.e. a named held question rather than a decree, and the row discloses the mark-only rival. No action sought beyond the record."},
 {"row": "P05-004 and P05-008 (an audit-input defect, not a row defect)",
  "what": "Both MARKS_3D items describe their mark as 'the closed-section mark' - on MT 22:31 and on MT 24:14 respectively. MEASURED from pmarks_Ezek.json, BOTH verses carry ['PE'], and that file's own marks_note defines SAMEKH as setumah (closed section) and PE as petuchah (open section). So in both items the mark's EXISTENCE and its ONSET-SEAM DIRECTION reproduce exactly, and its SECTION CLASS does not.",
  "why_i_did_not_write_it": "I did write the disclosures - both items are discharged - but with PE, and with the correction stated in the row rather than absorbed silently. I escalate the pattern rather than the instances: the same mislabel in two independent items points at the audit's mark-class field rather than at a slip, so any other lane's MARKS_3D items may carry it too. Corroborating detail: row P05-007, written before this wave, already calls the MT 24:14 mark a pe, which agrees with the file against the audit."},
]

OUT = collections.OrderedDict()
OUT['lane'] = 'ezek_author_l04'
OUT['attempt_id'] = 'ezek_author_l04_a1'
OUT['execution_id'] = 'ezek_author_l04_a1#e1'
OUT['item_id_convention'] = ("The worklist items carry no id field, so I assign one deterministically and reversibly: "
  "'<1-based index in your_worklist_items>:<row_id>:<cls>:<discriminator>', where the discriminator is the citation for "
  "A4_CITATION, the hyphenated run for A6/A6_UNION, 'set-<new_value>' for CONFIDENCE, 'mark' for MARKS_3D, 'grounds' for "
  "GROUNDS and 'boss_return' for BOSS_RETURN. The index alone identifies the item unambiguously against the pinned lane file.")
OUT['sources'] = SOURCES
OUT['edits'] = EDITS
OUT['items_discharged'] = discharged
OUT['items_NOT_discharged'] = []
OUT['judgement_items_discharged_without_an_edit'] = NOEDIT
OUT['escalations'] = ESC
OUT['changes_made_or_no_change'] = (
 "82 edits across all 22 rows, discharging all 85 worklist items; nothing is left in neither list. "
 "By sweep: CONFIDENCE 2 set_confidence moves (P05-008 and P07-001, high to medium, applied as ruled). "
 "GROUNDS 3 set edits (P05-005 boundary_rationale: the ordered 23:35 close-seam SAMEKH disclosure; "
 "P05-007 strongest_rejected_alternative: the ordered A9 weighing of the 24:8 PE and the 24:9 messenger formula; "
 "P07-001 strongest_rejected_alternative: the ordered naming and weighing of the 29:7/29:8 rival and the 29:1-16 tiling, "
 "with the A10 mark disclosure). MARKS-3D 2 set edits on device_notes (P05-004 for MT 22:31, P05-008 for MT 24:14), each in the "
 "three-direction form and each correcting the audit's section class from closed to open. BOSS_RETURN 1 item applied verbatim "
 "across 3 fields of P06-009: the 27:3 messenger-formula correction to the absolute 'no formula marks any internal point' sentence, "
 "the A7 benchmark correction from the 14-16 allowance to the governing 7-10 target, and the never-split sentence kept and sourced "
 "to the over-split guard at strategy \u00a76 line 351, with peer_07's four false positives not carried. A6 9 of 13 items produce edits "
 "(8 INSTALL plus the 28:19/27:36 misattribution repair at P06-009); 4 A6 items and the 1 A6_UNION item are discharged as judgements "
 "with NO edit, each with its finding recorded in judgement_items_discharged_without_an_edit. A4 66 append_ref installs: 63 for the "
 "63 citation items, one entry per citation and ONE RANGE ENTRY for each of the 5 range citations, plus 3 further entries "
 "(web:Ezek.22.31, web:Ezek.24.9, web:Ezek.29.8) that mirror in-window anchors my own ordered grounds and marks rewrites introduce, "
 "so the repair does not create fresh unmirrored citations; those 3 are attributed to the items that ordered the anchors. "
 "NO SEAM IS MOVED and no edit touches span, osis_start, osis_end, decision_id or any writer-identity field.")
OUT['verification_evidence'] = [
 "DIGESTS: all 10 pinned inputs hashed before reading. The two required files matched the launch table exactly "
 "(brief ccb7026f..., lane cabd3b2f...). Ezek_oshb.txt, pmarks_Ezek.json, book_strategy_Ezek.md, ezek_device_inventory.v2.json, "
 "ezek_device_inventory.json, verse_inventory.json, tools/verse_map_web.json and tools/verse_map_oshb.json all matched. "
 "web_mt_offset_map.json was left to be measured and is b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887.",
 "MARKS, MEASURED over pmarks_Ezek.json by script: MT 22:31 PE; 23:10 SAMEKH; 23:21 SAMEKH; 23:27 SAMEKH; 23:31 SAMEKH; "
 "23:34 SAMEKH; 23:35 SAMEKH; 23:45 SAMEKH; 23:49 PE; 24:5 SAMEKH; 24:8 PE; 24:9 none; 24:14 PE; 24:24 SAMEKH; 24:27 SAMEKH; "
 "25:5/25:7/25:11 SAMEKH; 25:14 PE; 25:17 SAMEKH; 26:6 PE; 26:14/26:18/26:21 SAMEKH; 27:36 SAMEKH; 28:5/28:10 SAMEKH; 28:19 PE; "
 "28:24/28:26 SAMEKH; 29:7 SAMEKH; 29:12/29:16 PE; 29:18/29:20 SAMEKH; 29:21 PE; 30:5 PE; 30:9/30:12 SAMEKH; 30:19 PE. "
 "Ch 27's only mark follows 27:36; no mark inside 30:14-30:18; no mark on 23:23-ish interiors beyond those listed; no mark on 29:6 or 29:9.",
 "PASEQ, MEASURED as occurrence counts over the pmarks paseq list (count-only by that file's own note, so no intra-verse position "
 "is claimed anywhere): 24:6 = 1, 24:17 = 1, 24:21 = 1, 26:15 = 1, 26:16 = 1, 28:2 = 1, 28:25 = 1, 29:3 = 1, 29:12 = 1, 30:22 = 1; "
 "and ZERO at 26:3, 28:5, 30:14 and 30:16. Every paseq disclosure standing in my rows reproduces, and ch 28's two paseq sites are "
 "28:2 and 28:25 exactly as P06-012 states.",
 "K/Q, MEASURED and read as LISTS, which is the structure a previous reader in this campaign mistook for a dict: "
 "kq[Ezek.23.43] is a TWO-member list, so P05-006's doubled-note claim reproduces; kq at 23:14, 23:16, 23:42, 24:2, 25:7, 25:9, "
 "27:3, 27:6, 27:15, 28:3, 29:4, 29:7 and 30:16 are each one-member lists. Chapter 27 carries exactly three K/Q verses (27:3, 27:6, "
 "27:15) and exactly two OSHB editorial notes (27:27, 27:29), both of the 'BHS has been faithful to the Leningrad Codex' class, "
 "so P06-009's apparatus figures reproduce.",
 "CUT-RULE at MT 24:9, MEASURED over Ezek_oshb.txt: 24:9 opens with the therefore-particle plus the long-form messenger formula; "
 "24:8 ends on a purpose infinitive with no utterance, recognition or I-YHWH-have-spoken signature; 24:6 already addresses the "
 "bloody city and 24:9 addresses that same city. Both limbs fail, so the rival is mark-only and, per CONF-CAL, never fatal.",
 "CUT-RULE at MT 23:35, MEASURED: 23:34 ends VERSE-FINALLY on the utterance formula and 23:35 opens with the long-form messenger "
 "formula, so limb (b) IS satisfied there. Recorded and escalated, not acted on.",
 "#e14 Q2 applied to the refinement rather than the bare phrase, MEASURED over Ezek_oshb.txt: MT 29:9's recognition formula ends at "
 "the etnachta and the rest of the verse is an INDEPENDENT causal clause on a finite verb, so it is the WEAK mid-verse shape - the "
 "brief's own example. MT 29:6's remaining words are a causal phrase on an infinitive construct, a DEPENDENT completion, so 29:6 "
 "grades as an ordinary licensed near-face signal. The distinction is the one Q2 draws and it is what separates the two rivals.",
 "The 29:7/29:8 addressee shift, MEASURED: MT 29:7 addresses a masculine singular and MT 29:8 a feminine singular, so CUT-RULE "
 "limb (a) is satisfied and that rival is licensed and two-faced. This is why medium, not high, is the right grade for P07-001 and "
 "it corroborates the ruling independently of it.",
 "BOSS_RETURN C1, reproduced from the pinned input rather than trusted: book_strategy_Ezek.md line 351 reads "
 "'unit (12:26-28 is 3; 33:21-22 is 2 and is held, \u00a77); a qinah-labelled unit is never split; a', matching the C1 reproduction "
 "verbatim. I also measured which section the line sits in instead of accepting the attribution: \u00a76 opens at line 285 and \u00a77 at "
 "line 360, so line 351 is inside \u00a76 and the work order's '\u00a76' is correct. \u00a77 line 405-406 independently names '27: one 36-verse "
 "qinah', and line 356 lists ch 27 among the whole-chapter spans that sit at medium_low with the cap disclosure.",
 "BOSS_RETURN (a), the 27:3 correction, reproduced independently: MEASURED over Ezek_oshb.txt, the long-form messenger formula "
 "occurs inside MT 27:3 and at NO other verse of ch 27, and the word-event formula occurs only at MT 27:1. So the row's absolute "
 "'no formula marks any internal point in the chapter' was FALSE and is corrected; under CUT-RULE the 27:3 formula licenses nothing "
 "(no addressee change, and 27:2 does not end on a close-role formula), so the row's conclusion survives on a true premise.",
 "BOSS_RETURN (b), the A7 benchmark: MEASURED, ch 27 has 36 verses (my own count over Ezek_oshb.txt, not a copied figure). "
 "EXTRACTED from book_strategy_Ezek.md lines 330-331, the target is 7-10 verses per row and the 14-16 allowance is granted only to "
 "the measured-and-listed blocks the strategy names by chapter, which do not include ch 27 - so disclosing against that allowance "
 "understated the deviation, exactly as the work order says.",
 "BOSS_RETURN, the field's own negative re-verified rather than assumed: MEASURED, none of MT 27:11, 27:12, 27:25 or 27:26 carries "
 "a parashah mark, a messenger formula or a word-event formula, so the existing sentence holds as written.",
 "A6 runs, MEASURED by whole-book normalised scan of tools/verse_map_web.json (1273 verses each): 'toward the children of ammon' 1 "
 "verse (25:2); 'in the eleventh year in the first of the month' 1 (26:1); 'behold i am against you' 10 (13:8, 13:20, 21:3, 26:3, "
 "28:22, 29:3, 29:10, 35:3, 38:3, 39:1); 'take up a lamentation over tyre' 1 (27:2); 'you have become a terror' 1 (28:19); "
 "'for i have spoken it' 4 (23:34, 26:5, 28:10, 39:5); 'by the hand of strangers' 1 (28:10); "
 "'son of man take up a lamentation over the king of tyre' 1 (28:12); 'over the king of tyre' 1 (28:12); "
 "'to the house of israel' 16; 'know that i am the lord' 5 (13:9, 23:49, 24:24, 28:24, 29:16); 'for the house of israel' 3 "
 "(13:5, 29:21, 45:17). THREE of the audit's attachment lists are INCOMPLETE where it matters to the judgement: for "
 "'behold i am against you' it named 3 of 10, and for both P06-012 runs it named only out-of-span verses while an IN-SPAN "
 "occurrence exists at web:Ezek.28.24. Reported because an incomplete premise and a false premise demand different responses.",
 "Two of those scans line up one-to-one with inventory v2 classes, which is a real corroboration and is why two A6-b judgements are "
 "confident: 'know that i am the lord' occurs at exactly the five adonai-form recognition (D3) verses, and 'for i have spoken it' at "
 "exactly the four name-less members of i_am_yhwh_spoken. The second of those also corrects a reading risk: MT 28:10 is a name-less "
 "member, NOT one of the 14 name-bearing, and my P06-010 edit says so.",
 "The P06-009 misattribution, MEASURED: WEB 27:36 reads 'The merchants among the peoples hiss at you. You have come to a terrible "
 "end, and you will be no more.' while WEB 28:19 reads 'All those who know you among the peoples will be astonished at you. You have "
 "become a terror, and you will exist no more.' The row attributed 28:19's English to ch 27's own colophon; the repair quotes the "
 "row's actual close verse. In the CONSONANTAL Hebrew the two verses DO end identically, differing only in pointing (feminine "
 "singular at 27:36, masculine singular at 28:19), which is why P06-011's mirror claim is narrowed to the Hebrew rather than struck.",
 "P07-004's 'one of three in the book' short-form messenger figure CHECKED AND FOUND CORRECT against v2, not silently 'fixed': "
 "formulae.messenger_formula_variant_census.shapes.short_form_yhwh_only has verses 3 (MT 11:5, 21:8, 30:6), and v2's fourth "
 "short-form VERSE, MT 21:14, is a different shape carrying adonai without the divine name - so the row's wording 'without the "
 "divine-name pair, one of three' matches v2 exactly. No edit made.",
 "FACE DISCIPLINE: EXTRACTED from web_mt_offset_map.json, rule.identity_outside_the_zone is true and the zone is confined to MT 21 "
 "= WEB 20:45-21:32. Every citation in my lane lies in chs 22-30, outside the zone, so WEB and MT numbering coincide throughout and "
 "single-face web: references are correct. I did not reach this by arithmetic. Where an A6 run's attachment list reached into the "
 "zone (web:Ezek.21.3, for 'behold i am against you') I deliberately did NOT cite it, both because it is not the row's claim and "
 "because citing it would owe dual-face writing.",
 "ROTATION RULE, MEASURED over my 66 installed entries: every free text is 6 words or fewer, so no 7-gram can form from it. "
 "Distinct formulations per token, counted by the same script that emitted the entries: WARRANT-close 17 entries / 17 distinct, "
 "WARRANT-rival 13/13, WARRANT-onset 10/10, DISCLOSURE-mark 8/8, DISCLOSURE-kq 5/5, ANCHOR 6/6, DISCLOSURE-paseq 3/3, "
 "DISCLOSURE-device 3/3, WARRANT-absence-over-range 1/1 - 66 entries, 66 distinct formulations, no repetition anywhere in the lane. "
 "The WARRANT-rival 13 and DISCLOSURE-mark 8 include the 3 extra mirror entries (web:Ezek.24.9 and web:Ezek.29.8 as rivals, "
 "web:Ezek.22.31 as a mark); the 63 citation items alone give WARRANT-rival 11 and DISCLOSURE-mark 7.",
 "HARNESS SAFETY, checked by assertion rather than by eye: every expected_before was read out of the pinned lane file and compared "
 "against it again at assembly (no drift); every prose edit's anchor was asserted to occur EXACTLY ONCE in the field before "
 "replacement, and one assertion did fire and caught a retyped Hebrew token, after which the three Hebrew-bearing anchors were "
 "resolved by slicing the row's own bytes between ASCII delimiters instead of being retyped; there is at most ONE set edit per "
 "(row, field); and all append_ref edits on a row share one identical expected_before list.",
]
OUT['unresolved_uncertainty'] = [
 "Item 62 (P06-011, literature_type_guess, run 'over the king of tyre'). I executed it as ruled, but I am not confident the rule "
 "intends it. literature_type_guess is a short genre LABEL, not argued prose, and the installed form reads oddly: "
 "qinah \u201cover the king of Tyre\u201d (web:Ezek.28.12, WEB). A6 as written is mechanical and A6-b does not reach the run (it is neither a "
 "counted device nor an inventoried addressee title), so the convention is owed; the item is marked INSTALL rather than "
 "AUTHOR_JUDGEMENT, so it was not mine to decline. If the wave would rather leave genre labels undelimited, this is the single edit "
 "to revert and it is isolated to one field.",
 "The rotation rule's floor of at least 4 distinct formulations cannot be REACHED for DISCLOSURE-paseq or DISCLOSURE-device in my "
 "lane, because my worklist yields only 3 citations of each. All 3 of each are distinct and 6 words or fewer, so no repetition and no "
 "7-gram risk arises. Stated plainly rather than left to look like compliance: the floor is unreachable here, not breached.",
 "Two of the eleven ROLE tokens, QUOTE and DISCLOSURE-note, appear nowhere in my 66 installs. I checked why rather than assuming it "
 "was fine: no A4 item in my lane cites an A6 quotation anchor or an OSHB editorial-note verse, because those verses (25:7, 27:2, "
 "27:27, 27:29, 28:3) are ALREADY mirrored in their rows' refs and so generated no citation item. If the spot wave expects all "
 "eleven to appear per lane, that expectation cannot be met from this worklist and the reason is structural.",
 "P05-008's demotion from high to medium: I applied it and recorded the seam facts I found, but I could not determine from the "
 "evidence available to me WHICH CONF-CAL limb the ruling relies on. The onset seam at 24:14/24:15 looks two-faced to me and the "
 "close at 24:27 carries a licensed near face, which reads as HIGH on a literal application; the live interior rival at 24:24/24:25 "
 "is the most plausible basis for MEDIUM. I did not reason backwards to a justification I cannot source. Confidence is ruled, not "
 "chosen, so the grade is applied; the rationale for it is REPORTED, not MEASURED, and I flag that asymmetry rather than paper over it.",
 "The 'why' text on my A4 entries describes what each cited verse does in the row's argument. Where I say a rationale 'rests on' a "
 "verse I am reading the row's existing prose, so that part of each WARRANT judgement is EXTRACTED from the row, not MEASURED over "
 "the witness; the verse-level facts inside the free text (marks, K/Q, paseq, formula presence and absence) are MEASURED. The two "
 "tiers are deliberately not blended.",
 "MT 33:20's sof pasuq is untouched: no row in my lane spans it, so I neither resolved it nor asserted anything either way. "
 "Likewise the transport class's 13 disputed verses (MT 3:12, 3:14, 37:2, 40:2, 40:3, 40:24, 40:48, 42:15, 43:1, 44:1, 46:21, 47:3, "
 "47:4) all lie outside chs 23-30, and no row of mine makes a transport-class membership claim, so the held question bound no item "
 "of mine and I invented none for peer_03 or peer_10.",
]
OUT['e19_selfreport'] = (
 "Exact paths only. No directory listing, no glob, no recursive search, and no directory was tested for existence. I opened exactly "
 "the two files the launch named plus the 8 further pinned paths it tabulated, every one by its full literal path and every one "
 "hashed before use. One distinction stated so it is not mistaken for a breach: I ran whole-book scans INSIDE "
 "tools/verse_map_web.json and Ezek_oshb.txt - 1273 verses each - which is scanning the CONTENT of a file opened by exact path, not "
 "searching the filesystem; it is what made the A6 attachment counts MEASURED instead of REPORTED. I did not read any other lane's "
 "rows or output, the reviews directory, any peer packet, any ruling not quoted in my brief, any fix-up order or any transcript; the "
 "only peer material I saw is what the BOSS_RETURN item itself carries. I read v2 of the device inventory for every count and opened "
 "v1 for nothing but its digest. All my work sits in the uniquely-named private directory "
 "scratchpad\\ezek_l04_work_7b3c; I wrote nothing under C:\\wt\\logos-t423-m8-fable, mutated no row, ran no validator, touched no git, "
 "wrote no receipt and no registry entry, and reused no bare filename at scratch root.")
OUT['limit'] = (
 "What this deliverable does NOT settle. (1) Four seam or tiling divergences from strategy \u00a77 stand unresolved in escalations - the "
 "ch-28 cut site at 28:24, the P05-005 rival's stated ground, the ch-30 split, and the ch-26 three-versus-four tiling. I moved no "
 "seam and I am not authorised to; three of the four rows already weigh their alternative, and the fourth (P05-005) needs a grounds "
 "order I was not given. (2) P05-008's confidence rationale is REPORTED, not reconstructed. (3) I could not verify the audit's "
 "section-class field beyond the two instances in my own lane, so whether other lanes carry the same closed-for-open mislabel is "
 "unknown to me and is why I escalated the pattern. (4) The A6 attachment lists I was handed are incomplete in three places; I "
 "measured the true sets and judged on those, but I cannot tell whether the same incompleteness affected items in other lanes. "
 "(5) I added 3 refs entries beyond the 63 citation items, to mirror in-window anchors my own ORDERED rewrites introduce; they are "
 "attributed to the ordering items and flagged here because they are the only edits in this deliverable not one-to-one with a "
 "citation item, and an auditor should see that rather than discover it.")

path = W + r'\ezek_author_l04_deliverable.json'
io.open(path, 'w', encoding='utf-8').write(json.dumps(OUT, ensure_ascii=False, indent=1))
print('deliverable written: %d edits, %d discharged, %d not discharged, %d no-edit judgements'
      % (len(EDITS), len(discharged), len(OUT['items_NOT_discharged']), len(NOEDIT)))
# rotation-rule proof
cnt = collections.defaultdict(list)
for e in EDITS:
    if e['op'] == 'append_ref':
        tok = e['role_token']
        cnt[tok].append(e['value'].split('] ', 1)[1])
for t, v in sorted(cnt.items()):
    mx = max(len(x.split()) for x in v)
    print('  %-28s entries=%2d distinct=%2d maxwords=%d' % (t, len(v), len(set(v)), mx))
    assert mx <= 6 and len(set(v)) == len(v)
