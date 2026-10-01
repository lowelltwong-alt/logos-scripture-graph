# -*- coding: utf-8 -*-
import json, hashlib, re
from collections import defaultdict, Counter

W = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l01_work_7b3e'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
d = json.load(open(LANE, encoding='utf-8'))
rows = {r['decision_id']: r for r in d['your_rows']}
items = d['your_worklist_items']
edits = json.load(open(W + r'\edits_raw.json', encoding='utf-8'))

# ---------- expected_before byte-exactness audit ----------
prob = []
a4_first = {}
for e in edits:
    cur = rows[e['row_id']][e['field']]
    eb = e['expected_before']
    if e['sweep'] == 'a6' and e.get('rebased_on_a4'):
        continue                                  # verified separately below
    if eb != cur:
        prob.append((e['row_id'], e['field'], e['sweep'], e['op']))
print('expected_before identical to lane-file bytes for every non-rebased edit:', not prob)
for p in prob:
    print('   MISMATCH', p)

# rebased a6 edit: expected_before must equal (original list + that row's a4 appends, in order)
for e in edits:
    if e.get('rebased_on_a4'):
        base = list(rows[e['row_id']]['boundary_evidence_refs'])
        ap = [x['value'] for x in edits if x['row_id'] == e['row_id'] and x['sweep'] == 'a4']
        ok = e['expected_before'] == base + ap
        print('rebased a6 edit on %s: expected_before == original+%d a4 appends -> %s'
              % (e['row_id'], len(ap), ok))
        assert ok

# every append_ref on a row shares one expected_before
byrow = defaultdict(set)
for e in edits:
    if e['op'] == 'append_ref':
        byrow[e['row_id']].add(json.dumps(e['expected_before'], ensure_ascii=False))
print('all append_ref edits on a row share one expected_before:',
      all(len(v) == 1 for v in byrow.values()))

# ---------- item accounting ----------
def IID(i):
    return 'l01#%02d' % i

EXEMPT = {0: ('P01-001', 'and he said to me'),
          15: ('P01-004', 'to the house of israel'),
          59: ('P01-009', 'therefore the lord yahweh says'),
          60: ('P01-009', 'therefore the lord yahweh says'),
          74: ('P01-010', "yahweh's word came to me saying"),
          76: ('P01-010', 'know that i am yahweh'),
          78: ('P01-010', 'know that i am yahweh')}

with_edit = sorted({i for e in edits for i in e['worklist_item_ids']})
no_edit = [IID(i) for i in sorted(EXEMPT)]
discharged = sorted(set(with_edit) | set(no_edit))
all_ids = [IID(i) for i in range(len(items))]
print('\nitems: total=%d  discharged_with_edit=%d  discharged_no_edit=%d  discharged_total=%d'
      % (len(items), len(with_edit), len(no_edit), len(discharged)))
missing = [x for x in all_ids if x not in discharged]
print('items in NEITHER list:', missing)
assert not missing

EX_WHY = {
 0: ("A6-b EXEMPT, two independent grounds. (1) The detected 5-word run is a detector artifact: it "
     "straddles the row's own conjunction - the quoted material is only 'he said to me', 4 words, below A6's "
     "five-word threshold ('the transport-verb [and 'he said to me]' sweeps'). (2) That 4-word string is a "
     "device-sweep label the row names, i.e. a gloss of a census object. No edit. NOTE: this field also carries "
     "the transport-sweep claim I have escalated; editing the sentence would have forced a HELD membership "
     "question, and the exemption avoids it."),
 15: ("A6-b EXEMPT. The 5-word run is nothing but the WEB's fixed rendering of the addressee title 'house of "
      "Israel' (a phrase A6-b names) with its preposition, and the row names the addressee shift ('turning from "
      "the scroll itself to the audience'). FOUND, and decisive: the row's containing gloss 'go, get you to the "
      "house of Israel' is NOT a WEB run at all - WEB Ezek.3.4 reads 'He said to me, \u201cSon of man, go to the "
      "house of Israel' - so there is no WEB quotation of five or more words at this verse to delimit. The "
      "item's own web_refs (12:6, 17:2, 20:27) and in_span=false agree: the run matches the title elsewhere, "
      "not this verse."),
 59: ("A6-b EXEMPT. The run is the WEB's fixed rendering of the messenger formula, a counted device: MT 5:7 is a "
      "member of the inventory's 122-verse thus_says_the_lord_yhwh class and carries the formula verse-initially "
      "behind \u05dc\u05b8\u05db\u05b5\u05df (MEASURED). The row names the device explicitly - 'The messenger formula at 5:5' and 'two "
      "further therefore messenger formulae'. No edit."),
 60: ("A6-b EXEMPT, the second of the two occurrences. MT 5:8 is likewise a member of the 122-verse messenger "
      "class and carries the formula verse-initially (MEASURED); the row names the device. No edit."),
 74: ("A6-b EXEMPT. The run is the WEB's fixed rendering of the word-event formula, a counted device: MT 6:1 is a "
      "member of the inventory's 39-verse strict word-event list (MEASURED), and the row names it - 'a strict "
      "word-event, hard seam'. No edit."),
 76: ("A6-b EXEMPT. The run is the WEB's fixed rendering of the recognition formula, a counted device: MT 6:7 is "
      "a member of the 21-verse recognition_formula_2mp set (MEASURED), and the row names it - 'A 2mp "
      "recognition-family close'. No edit."),
 78: ("A6-b EXEMPT, the 6:10 occurrence. MT 6:10 is a member of the 28-verse strict recognition list (MEASURED) "
      "and the row names it - 'the strict recognition formula'. No edit."),
}

# ---------- per-edit why / tier ----------
A6_WHY = {
 'P01-001|boundary_evidence_refs': ("Installs the convention on the 5-word WEB run inside the 1:8 K/Q entry: double "
   "curly quotes plus an in-field web: reference. The run is WEB-exact at Ezek.1.8 (MEASURED by locator script)."),
 'P01-002|boundary_rationale': ("Two WEB runs were carried in single quotes: the 11-word run at 2:1 (whose web: ref "
   "was already present, only the delimiter was wrong) and the 8-word run at 2:3. Both are WEB-exact; nested WEB "
   "speech marks demoted to single curly so the outer delimiter is unambiguous."),
 'P01-003|boundary_rationale': ("Both runs corrected to the WEB's exact wording before delimiting, because both "
   "glosses were paraphrases: the row read 'and you, son of man, hear' where WEB Ezek.2.8 reads 'But you, son of "
   "man, hear', and 'a hand stretched out to me' where WEB Ezek.2.9 reads 'a hand was stretched out to me'. "
   "Delimiting a paraphrase as web: would have manufactured a false quotation. The 2:9 item's detected run also "
   "straddled the prose's own 'and'."),
 'P01-004|boundary_rationale': ("Four WEB-exact runs delimited and referenced (3:7, 3:9, 3:10, 3:11). WEB Ezek.3.7 "
   "carries a footnote marker between 'obstinate' and 'and'; the quotation omits that editorial marker and is "
   "otherwise word-identical."),
 'P01-005|boundary_rationale': ("Three WEB-exact runs delimited and referenced (3:12, 3:15, 3:16). Sentence-initial "
   "capitals restored to the WEB's. The transport wording in this field is deliberately untouched - see escalations."),
 'P01-006|boundary_rationale': "Two WEB-exact runs delimited and referenced (3:16, 3:17).",
 'P01-007|boundary_rationale': "Three WEB-exact runs delimited and referenced, two of them at 3:22 and one at 3:27.",
 'P01-007|strongest_rejected_alternative': "The 6-word WEB-exact run at 3:16 delimited and referenced.",
 'P01-008|boundary_rationale': ("Four WEB-exact runs delimited and referenced (4:1, 4:8, 4:16, 4:17); the 4:16 run is "
   "mid-verse in the WEB and keeps its lower-case initial."),
 'P01-009|boundary_rationale': "Two WEB-exact runs delimited and referenced (5:1, 5:14).",
 'P01-010|boundary_rationale': ("Two WEB-exact runs delimited and referenced (6:2, 6:8); the 6:2 run is mid-verse in "
   "the WEB and keeps its lower-case initial."),
 'P01-010|strongest_rejected_alternative': "The 6-word WEB-exact run at 6:8 delimited and referenced.",
}
G_WHY = {
 'P01-008|strongest_rejected_alternative': ("Discharges the A9 order. The samekh after oshb:Ezek.4.3 and the "
   "verse-final sign colophon are now named and weighed: near face = colophon + samekh, far face = a verse with no "
   "formula of any class in the inventory, CUT-RULE unmet on both limbs, so the rival is paragraph-grade and held, "
   "with the mark disclosed for the alternative it corroborates. The test is reworded because bare "
   "\u05d5\u05b0\u05d0\u05b7\u05ea\u05bc\u05b8\u05d4 opens THREE interior stages (4:3, 4:4, 4:9), not the two the old text named - and the omitted one "
   "was 4:3 itself, the verse the mark follows."),
 'P01-009|device_notes': ("Discharges the first limb of the order. The false ground was 'none coincides with a formula "
   "onset'. FOUND: three of the five interior marks do coincide - pe after 5:4 before the messenger formula at 5:5, "
   "samekh after 5:6 before 5:7, samekh after 5:7 before 5:8, all three next-verses members of the 122-verse "
   "messenger class and all three verse-initial. The correct ground is CUT-RULE: no near-face verse ends on a "
   "close-role formula."),
 'P01-009|strongest_rejected_alternative': ("Discharges the second limb of the order: the 5:4/5:5 rival weighed under "
   "A16, naming the PE and the messenger formula, with both CUT-RULE limbs tested and failed (no addressee change at "
   "5:5, which carries no second person; 5:4 does not close on a close-role formula). The pre-existing 5:13/5:15 "
   "rival is preserved."),
}
A4_WHY = {}
for e in edits:
    if e['sweep'] != 'a4':
        continue
    i = int(e['worklist_item_ids'][0].split('#')[1])
    it = items[i]
    A4_WHY[e['worklist_item_ids'][0]] = (
        "One entry for one citation (%s, %s), token chosen from the row's own use of the verse; "
        "annotation is %d words, under the 6-word rotation ceiling."
        % (it['citation'], it['citation_kind'], len(e['value'].split(']')[1].split())))

TIER_A6 = ("MEASURED: run existence and WEB-exactness measured by a6_locate2.py over tools/verse_map_web.json at the "
           "pinned digest; the A6/A6-b duty is my judgement at the row.")
TIER_A4 = ("MEASURED for the mirroring gap (the worklist's re-executed refs_mirror member) and for the verse's role, "
           "which I read off the row's own prose; EXTRACTED where the annotation names an inventory class.")
TIER_G = ("MEASURED over the pinned witness and inventory v2 by verify_l01.py (marks, verse-final text, class "
          "membership, ve-attah shapes); EXTRACTED from book_strategy_Ezek.md for the \u00a77 hold.")

for e in edits:
    k = '%s|%s' % (e['row_id'], e['field'])
    if e['sweep'] == 'grounds':
        e['why'] = G_WHY[k]; e['tier'] = TIER_G
    elif e['sweep'] == 'a6':
        e['why'] = A6_WHY[k] + (" expected_before is REBASED onto the a4 append for this row, because the "
                                "documented sweep order applies A4 installs (step 4) before A6 delimiting (step 5)."
                                if e.get('rebased_on_a4') else "")
        e['tier'] = TIER_A6
    else:
        e['why'] = A4_WHY[e['worklist_item_ids'][0]]; e['tier'] = TIER_A4
    e.pop('rebased_on_a4', None)

SRC = [
 ("C:\\Users\\lowel\\AppData\\Local\\Temp\\claude\\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\\scratchpad\\ezek_aw\\lanes\\ezek_author_l01_LAUNCH.md",
  None, "my launch brief, in full"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\AUTHOR_WAVE_BRIEF.v1.md",
  "ccb7026f908345d3f9800671e621cd8fbdedc3429d41c22dc244b03e0474bd79", "controlling instruction, read in full before writing; digest verified before reading"),
 ("C:\\Users\\lowel\\AppData\\Local\\Temp\\claude\\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\\scratchpad\\ezek_aw\\lanes\\lane_01_worklist.json",
  "f7701d740c0d03579f7df9fbc95a447d92829326605dd0157792bad18cb91d5a", "my 10 rows' complete current bytes and all 84 worklist items; digest verified before reading; every expected_before copied from here programmatically, never retyped"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\Ezek_oshb.txt",
  "337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e", "1273 verse lines; read Ezek 4:2-4:17 and 5:1-5:11 in full for the two GROUNDS rivals, plus consonantal-skeleton tests of 4:1, 4:3, 4:4, 4:9, 5:1 and verse-final tests of 4:3, 4:17, 3:27, 2:7, 3:3, 3:9, 5:4, 5:6, 5:7, 5:9, 5:10"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\pmarks_Ezek.json",
  "25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315", "marks/paseq/kq/notes_other for chs 1-6. kq read correctly as a dict verse -> LIST of concatenated ketiv+qere strings (not a dict): 5 K/Q verses in chs 1-6 (1:8, 3:15, 4:6, 4:15, 6:3), all disclosed by my rows; notes_other 1:11, 3:20, 4:6, all disclosed; 24 mark-carrying verses in chs 1-6; marks_note confirms a mark is recorded ON the verse it FOLLOWS"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\ezek_device_inventory.v2.json",
  "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f", "v2 as required by C2-amended and brief section 12; enumerated all 46 verse-list leaves and computed chs 1-6 membership for every class; derived family_48 = vayehi_any(41) union hayah_any(7) = 48 and any_form_49 = 48 + MT 1:3 = 49, reproducing the brief's arithmetic"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\ezek_device_inventory.json",
  "0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142", "v1: digest verified only, NOT used for any count or membership (superseded)"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\book_strategy_Ezek.md",
  "4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3", "read the over-split guard (line 350), the P1/P2 parent rows (270-271), the unit_type lists (291-295), the chapter-division and 2:8-3:3 guidance (334-338), and section 7 lines 367-375, which hold BOTH of my GROUNDS rivals: 4:1-3/4:4-8/4:9-17 and 5:1-4 against the interpretation 5:5-17. Also sourced the 23-verse ve-attah figure (121) and the 12-verse rebellious-house figure (124, 270)"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\verse_inventory.json",
  "7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54", "numbering_face = WEB, confirmed by reading the field"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\web_mt_offset_map.json",
  "b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887", "MEASURED (the launch table said measure and report). rule.identity_outside_the_zone = true and tier0_disclosure limits dual writing to WEB 20:45-49, WEB ch 21 and MT ch 21 'and only there'; my rows are chs 1-6, so single-face refs are unambiguous here and no dual writing is owed"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\tools\\verse_map_web.json",
  "bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98", "the WEB face for all 34 A6 runs; every run located at its named verse and every item's words field equals its token count"),
 ("C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Ezek\\tools\\verse_map_oshb.json",
  "408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901", "digest verified; not needed for content because chs 1-6 are numbering-identity and the Hebrew was read from Ezek_oshb.txt"),
]

out = {
 "lane": "ezek_author_l01",
 "attempt_id": "ezek_author_l01_a1",
 "execution_id": "ezek_author_l01_a1#e1",
 "item_id_scheme": ("The 84 worklist items carry NO id field (verified: no 'id' key on any item). I minted "
                    "deterministic ids l01#NN where NN is the 0-based index in your_worklist_items, so l01#00 is the "
                    "first item and l01#83 the last. item_identification below gives the (row, class, field, "
                    "citation-or-run) tuple for every id so the orchestrator can rebind without relying on my index."),
 "item_identification": {IID(i): {"row": it['row_id'], "cls": it['cls'],
                                  "field": it.get('field'),
                                  "citation": it.get('citation'), "run": it.get('run')}
                         for i, it in enumerate(items)},
 "sources": [{"path": p, "sha256": s, "read": r} for p, s, r in SRC],
 "edits": edits,
 "items_discharged": discharged,
 "items_discharged_without_edit": [
    {"item": IID(i), "row": EXEMPT[i][0], "run": EXEMPT[i][1], "ruling": "A6-b EXEMPT", "why": EX_WHY[i]}
    for i in sorted(EXEMPT)],
 "items_NOT_discharged": [],
 "escalations": [],
 "changes_made_or_no_change": "",
 "verification_evidence": [],
 "unresolved_uncertainty": [],
 "e19_selfreport": "",
 "limit": "",
}
json.dump(out, open(W + r'\_stage.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nstaged: %d edits, %d discharged (%d with an edit, %d by exempt ruling)'
      % (len(edits), len(discharged), len(with_edit), len(no_edit)))
print('token distribution:', dict(Counter(e['role_token'] for e in edits if 'role_token' in e)))
