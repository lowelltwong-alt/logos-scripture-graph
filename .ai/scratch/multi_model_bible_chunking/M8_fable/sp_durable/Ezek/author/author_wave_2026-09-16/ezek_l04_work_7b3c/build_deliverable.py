# -*- coding: utf-8 -*-
"""Assemble the ezek_author_l04 deliverable. Every expected_before is read from the
lane file, never retyped. Every A4 entry carries exactly one ROLE token."""
import json, io, hashlib

WORK = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l04_work_7b3c'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_04_worklist.json'
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
ITEMS = lane['your_worklist_items']

# ---- stable item ids: 1-based index in your_worklist_items + row + class + discriminator ----
def disc(it):
    if it['cls'] == 'A4_CITATION':
        return it['citation']
    if it['cls'] in ('A6', 'A6_UNION'):
        return it['run'].replace(' ', '-')
    if it['cls'] == 'CONFIDENCE':
        return 'set-' + it['new_value']
    if it['cls'] == 'MARKS_3D':
        return 'mark'
    if it['cls'] == 'GROUNDS':
        return 'grounds'
    return it['cls'].lower()

IDS = []
for i, it in enumerate(ITEMS, 1):
    IDS.append('%02d:%s:%s:%s' % (i, it['row_id'], it['cls'], disc(it)))
ID_OF = {}
for i, it in enumerate(ITEMS):
    ID_OF.setdefault((it['row_id'], it['cls'], disc(it)), IDS[i])

def iid(row, cls, d):
    return ID_OF[(row, cls, d)]

EDITS = []

# ================= SWEEP 1: confidence =================
for row in ('P05-008', 'P07-001'):
    cur = ROWS[row]['confidence']
    assert cur == 'high', cur
    why = {
      'P05-008': 'Applied as ruled, not chosen. What I found on the bytes: the onset seam at 24:14/24:15 is two-faced (full-form strict word-event at 24:15; verse-final utterance plus I-YHWH-have-spoken at 24:14) but the CLOSE seam at 24:27 has a licensed near face and, on its far face, MEASURED from pmarks_Ezek.json, only the samekh recorded after MT 24:27 with no signal in MT 25:1 direction beyond the next unit\u2019s own word-event; and the row carries a live interior rival at 24:24/24:25 with its own samekh after MT 24:24. medium is consistent with CONF-CAL and the four-value scale is respected.',
      'P07-001': 'Applied as ruled, not chosen, and independently corroborated. #e14 Q2 makes this row\u2019s close at 29:9 the WEAK mid-verse shape (recognition ends at the etnachta, an INDEPENDENT causal clause with a finite verb fills the rest of the verse) - the brief\u2019s own worked example - and the 29:7/29:8 rival is licensed and two-faced, which is CONF-CAL\u2019s MEDIUM limb. It is NOT medium_low: the far face of the close at 29:10 is not empty, it carries a fresh against-you verdict onset. The item carries held_by_e14_q2 = true and the refinement is applied, not the bare phrase.'}[row]
    EDITS.append(dict(row_id=row, field='confidence', op='set_confidence', expected_before=cur,
                      value='medium', worklist_item_ids=[iid(row, 'CONFIDENCE', 'set-medium')],
                      sweep='confidence', why=why,
                      tier='EXTRACTED from the ruling for the grade; MEASURED (pmarks_Ezek.json, Ezek_oshb.txt) for the seam facts I checked it against'))

# ================= SWEEPS 2-3, 5: prose (grounds, marks, a6, boss return) =================
SWEEP_OF = {('P05-004', 'device_notes'): 'marks', ('P05-008', 'device_notes'): 'marks',
            ('P05-005', 'boundary_rationale'): 'grounds', ('P05-007', 'strongest_rejected_alternative'): 'grounds',
            ('P07-001', 'strongest_rejected_alternative'): 'grounds',
            ('P06-009', 'boundary_rationale'): 'grounds', ('P06-009', 'strongest_rejected_alternative'): 'grounds',
            ('P06-009', 'device_notes'): 'grounds'}
ITEMKEY = {
  'P05-004/MARKS_3D/22:31': ('P05-004', 'MARKS_3D', 'mark'),
  'P05-008/MARKS_3D/24:14': ('P05-008', 'MARKS_3D', 'mark'),
  'P05-005/GROUNDS/23:35-samekh': ('P05-005', 'GROUNDS', 'grounds'),
  'P05-007/GROUNDS/A9-24:8-24:9': ('P05-007', 'GROUNDS', 'grounds'),
  'P07-001/GROUNDS/29:7-29:8+29:1-16': ('P07-001', 'GROUNDS', 'grounds'),
  'P06-009/BOSS_RETURN': ('P06-009', 'BOSS_RETURN', 'boss_return'),
  'P06-001/A6/toward-the-children-of-ammon': ('P06-001', 'A6', 'toward-the-children-of-ammon'),
  'P06-005/A6/in-the-eleventh-year': ('P06-005', 'A6', 'in-the-eleventh-year-in-the-first-of-the-month'),
  'P06-005/A6/behold-i-am-against-you': ('P06-005', 'A6', 'behold-i-am-against-you'),
  'P06-009/A6/take-up-a-lamentation-over-tyre': ('P06-009', 'A6', 'take-up-a-lamentation-over-tyre'),
  'P06-009/A6/you-have-become-a-terror': ('P06-009', 'A6', 'you-have-become-a-terror'),
  'P06-010/A6/for-i-have-spoken-it': ('P06-010', 'A6', 'for-i-have-spoken-it'),
  'P06-011/A6/son-of-man-take-up-a-lamentation': ('P06-011', 'A6', 'son-of-man-take-up-a-lamentation-over-the-king-of-tyre'),
  'P06-011/A6/you-have-become-a-terror': ('P06-011', 'A6', 'you-have-become-a-terror'),
  'P06-011/A6/over-the-king-of-tyre': ('P06-011', 'A6', 'over-the-king-of-tyre'),
}
for e in json.load(open(WORK + r'\prose_edits.json', encoding='utf-8')):
    assert ROWS[e['row_id']][e['field']] == e['expected_before'], 'DRIFT %s.%s' % (e['row_id'], e['field'])
    e['worklist_item_ids'] = [iid(*ITEMKEY[k]) for k in e['worklist_item_ids']]
    e['sweep'] = SWEEP_OF.get((e['row_id'], e['field']), 'a6')
    EDITS.append(e)

# ================= SWEEP 4: A4 reference installs =================
# (row, citation) -> (ROLE token, free text <=6 words, why)
A4 = {
 ('P05-004', 'Ezek.23.5-Ezek.23.10'): ('ANCHOR', 'Oholah narrative span, no seam claim', 'The prose delimits Oholah\u2019s narrative; the boundary rests on 23:1 and 23:21, not here. A range citation takes ONE range entry.'),
 ('P05-004', 'Ezek.23.11'): ('WARRANT-rival', 'rival onset, subject shifts here', 'The rejected 23:10/23:11 cut opens at 23:11; this is the A9 rival weighed at that verse.'),
 ('P05-004', 'Ezek.23.10'): ('DISCLOSURE-mark', 'setumah corroborating the rejected cut', 'MEASURED: pmarks records SAMEKH on Ezek.23.10. Under the precedence rule a mark supporting the RIVAL is disclosed for the rival, so it is tokenised as a mark, not as this row\u2019s warrant.'),
 ('P05-004', 'Ezek.23.2'): ('DISCLOSURE-device', 'son-of-man address inside span', 'An in-span device the boundary does not rest on.'),
 ('P05-004', 'Ezek.23.4'): ('ANCHOR', 'sisters named, allegory\u2019s dramatis personae', 'Content statement supporting the genre label, not a boundary claim.'),
 ('P05-004', 'Ezek.23.14'): ('DISCLOSURE-kq', 'one K/Q site, unquoted here', 'MEASURED: pmarks kq[Ezek.23.14] is a one-member LIST. Read as a list, not a dict.'),
 ('P05-004', 'Ezek.23.16'): ('DISCLOSURE-kq', 'second in-span ketiv/qere, disclosed only', 'MEASURED: pmarks kq[Ezek.23.16] is a one-member LIST.'),
 ('P05-004', 'Ezek.22.31'): ('DISCLOSURE-mark', 'petuchah behind the word-event onset', 'Mirrors the anchor my MARKS-3D disclosure introduces. MT 22:31 is first-1, inside the A4 window, so it would otherwise be an unmirrored citation of my own making. MEASURED: pmarks records PE, not SAMEKH.'),

 ('P05-005', 'Ezek.23.35'): ('WARRANT-close', 'coda verse where this unit ends', 'The row\u2019s close verse; the close rests on it.'),
 ('P05-005', 'Ezek.23.27'): ('DISCLOSURE-mark', 'mid-unit setumah, texture only', 'MEASURED: SAMEKH on Ezek.23.27, interior.'),
 ('P05-005', 'Ezek.23.31'): ('DISCLOSURE-mark', 'interior paragraph stop, no cut', 'MEASURED: SAMEKH on Ezek.23.31, interior.'),

 ('P05-006', 'Ezek.24.1'): ('WARRANT-close', 'next dateline onset, far face', 'The close seam 23:49/24:1 rests on the pe after 23:49 and the fused dateline plus word-event onset at 24:1, which is that seam\u2019s far face.'),
 ('P05-006', 'Ezek.23.42'): ('DISCLOSURE-kq', 'single note-layer variant, left unquoted', 'MEASURED: kq[Ezek.23.42] is a one-member LIST.'),
 ('P05-006', 'Ezek.23.43'): ('DISCLOSURE-kq', 'doubled pair, two K/Q entries', 'MEASURED: kq[Ezek.23.43] is a TWO-member LIST, so the row\u2019s doubled-note claim reproduces. This is the exact structure a previous reader mistook for a dict.'),

 ('P05-007', 'Ezek.24.2'): ('DISCLOSURE-kq', 'K/Q pair reserved to note layer', 'MEASURED: kq[Ezek.24.2] is a one-member LIST. Under DEF-A4-ARGUED clause 2 the row\u2019s two mentions of 24:2 (the son-of-man tag and the K/Q) are ONE citation, so one entry covers both; the disclosure duty is the load-bearing one.'),
 ('P05-007', 'Ezek.24.6'): ('DISCLOSURE-paseq', 'one stroke, position unsourceable here', 'MEASURED: Ezek.24.6 appears once in the pmarks paseq list, which is count-only.'),
 ('P05-007', 'Ezek.24.9'): ('WARRANT-rival', 'messenger onset of the weighed rival', 'Mirrors the anchor the ordered A9 weighing introduces; 24:9 is in span and would otherwise be unmirrored.'),

 ('P05-008', 'Ezek.24.25'): ('WARRANT-rival', 'rejected fresh start, no device', 'The rejected 24:24/24:25 cut would open at 24:25; MEASURED, no word-event, messenger formula or dateline stands there.'),
 ('P05-008', 'Ezek.24.16'): ('DISCLOSURE-device', 'son-of-man address, sign-act command', 'In-span device, not a boundary basis.'),
 ('P05-008', 'Ezek.24.17'): ('DISCLOSURE-paseq', 'count-only stroke, no position claim', 'MEASURED: one paseq occurrence at Ezek.24.17.'),
 ('P05-008', 'Ezek.24.21'): ('DISCLOSURE-paseq', 'second in-span paseq, counted only', 'MEASURED: one paseq occurrence at Ezek.24.21.'),

 ('P06-001', 'Ezek.25.6'): ('WARRANT-rival', 'same-addressee reopening, cut withheld', 'The 25:5/25:6 rival; the row holds because 25:6 reopens against Ammon with no addressee-class shift.'),
 ('P06-001', 'Ezek.25.8'): ('WARRANT-close', 'Moab shift ahead, forward face', 'Far face of this row\u2019s close seam at 25:7/25:8.'),

 ('P06-002', 'Ezek.25.7'): ('WARRANT-onset', 'prior close stands behind this onset', 'Far face of the onset seam 25:7/25:8.'),
 ('P06-002', 'Ezek.25.12'): ('WARRANT-close', 'Edom onset ahead of close', 'Far face of the close seam 25:11/25:12.'),
 ('P06-002', 'Ezek.25.1-Ezek.25.7'): ('WARRANT-rival', 'Ammon half of rejected merge', 'The rejected 25:1-11 merge; a range citation takes ONE range entry, not one per verse.'),

 ('P06-003', 'Ezek.25.11'): ('WARRANT-onset', 'Moab close behind this onset', 'Far face of the onset seam 25:11/25:12.'),
 ('P06-003', 'Ezek.25.15'): ('WARRANT-close', 'Philistia onset beyond the close', 'Far face of the close seam 25:14/25:15.'),

 ('P06-004', 'Ezek.25.14'): ('WARRANT-onset', 'Edom close, petuchah behind onset', 'Far face of the onset seam 25:14/25:15. MEASURED: PE on Ezek.25.14.'),

 ('P06-005', 'Ezek.26.2'): ('ANCHOR', 'Tyre\u2019s taunt, content not seam', 'Accusation content inside the span; the onset rests on 26:1.'),
 ('P06-005', 'Ezek.26.7'): ('WARRANT-close', 'fresh messenger unit begins ahead', 'Far face of the close seam 26:6/26:7.'),
 ('P06-005', 'Ezek.26.3'): ('DISCLOSURE-device', 'verdict idiom, corroboration not onset', 'In-span device the boundary does not rest on. Also mirrors the verse my A6 install references.'),

 ('P06-006', 'Ezek.26.6'): ('WARRANT-onset', 'recognition close sits behind onset', 'Far face of the onset seam 26:6/26:7. MEASURED: PE on Ezek.26.6.'),
 ('P06-006', 'Ezek.26.15'): ('WARRANT-close', 'princes\u2019 scene opens past close', 'Far face of the close seam 26:14/26:15.'),

 ('P06-007', 'Ezek.26.14'): ('WARRANT-onset', 'stacked close precedes this onset', 'Far face of the onset seam 26:14/26:15. MEASURED: SAMEKH on Ezek.26.14.'),
 ('P06-007', 'Ezek.27.1'): ('WARRANT-close', 'word-event onset follows the close', 'Far face of the close seam 26:21/27:1.'),

 ('P06-009', 'Ezek.27.12-Ezek.27.24'): ('ANCHOR', 'trade list, never cut inside', 'Structural statement supporting non-cutting, named by the strategy\u2019s over-split guard. ONE range entry.'),
 ('P06-009', 'Ezek.26.21'): ('WARRANT-onset', 'utterance close behind the onset', 'Far face of the onset seam 26:21/27:1. MEASURED: SAMEKH on Ezek.26.21.'),
 ('P06-009', 'Ezek.28.1'): ('WARRANT-close', 'prince oracle opens past close', 'Far face of the close seam 27:36/28:1.'),
 ('P06-009', 'Ezek.27.11'): ('WARRANT-rival', 'rival face, ship-description end', 'MEASURED: no mark, no messenger formula, no word-event at 27:11.'),
 ('P06-009', 'Ezek.27.12'): ('WARRANT-rival', 'trade-list onset, cut declined', 'MEASURED: no mark or formula at 27:12. Distinct from the 27:12-24 range entry, which carries a different assertion.'),
 ('P06-009', 'Ezek.27.25'): ('WARRANT-rival', 'list\u2019s end, second rival face', 'MEASURED: no mark or formula at 27:25.'),
 ('P06-009', 'Ezek.27.26'): ('WARRANT-rival', 'poem resumes, unmarked rival onset', 'MEASURED: no mark or formula at 27:26.'),

 ('P06-010', 'Ezek.27.36'): ('WARRANT-onset', 'mark-only close stands behind', 'Far face of the onset seam 27:36/28:1. MEASURED: SAMEKH on Ezek.27.36 and no close formula in that verse.'),
 ('P06-010', 'Ezek.28.11'): ('WARRANT-close', 'king lament opens after close', 'Far face of the close seam 28:10/28:11.'),
 ('P06-010', 'Ezek.28.7'): ('ANCHOR', 'verdict idiom, genre argument only', 'Cited to reject a genre reclassification, not to carry a seam.'),
 ('P06-010', 'Ezek.28.9'): ('ANCHOR', 'rhetorical boast, classification evidence only', 'Cited in the genre argument; no boundary rests on it.'),
 ('P06-010', 'Ezek.28.5'): ('DISCLOSURE-mark', 'interior setumah, symmetry disclosure only', 'MEASURED: SAMEKH on Ezek.28.5, interior to the span.'),

 ('P06-011', 'Ezek.28.10'): ('WARRANT-onset', 'prince unit closed just behind', 'Far face of the onset seam 28:10/28:11. MEASURED: SAMEKH on Ezek.28.10.'),
 ('P06-011', 'Ezek.28.20'): ('WARRANT-close', 'Sidon word-event opens ahead', 'Far face of the close seam 28:19/28:20.'),
 ('P06-011', 'Ezek.28.1-Ezek.28.10'): ('WARRANT-rival', 'the row this would absorb', 'The rejected fold-in; ONE range entry.'),

 ('P06-012', 'Ezek.28.19'): ('WARRANT-onset', 'qinah\u2019s petuchah close behind', 'Far face of the onset seam 28:19/28:20. MEASURED: PE on Ezek.28.19.'),
 ('P06-012', 'Ezek.28.25'): ('WARRANT-close', 'gathering promise opens beyond close', 'Far face of the close seam 28:24/28:25.'),

 ('P06-013', 'Ezek.29.1'): ('WARRANT-close', 'dateline hard seam lies ahead', 'Far face of the close seam 28:26/29:1.'),
 ('P06-013', 'Ezek.28.24'): ('WARRANT-rival', 'declined onset, Sidon verdict\u2019s close', 'The rejected 28:24 onset; MEASURED, SAMEKH stands on Ezek.28.24, which is why this is a real rival and not a straw one.'),

 ('P07-001', 'Ezek.29.10'): ('WARRANT-close', 'fresh verdict cycle past close', 'Far face of the close seam 29:9/29:10.'),
 ('P07-001', 'Ezek.29.6'): ('WARRANT-rival', 'earlier recognition, rival close weighed', 'The 29:6/29:7 rival. MEASURED: no mark on Ezek.29.6, and 29:7 opens with no onset device.'),
 ('P07-001', 'Ezek.28.26'): ('DISCLOSURE-mark', 'setumah behind the dateline onset', 'MEASURED: SAMEKH on Ezek.28.26. The onset rests on the dateline at 29:1, not on the mark, so the honest token is a disclosure.'),
 ('P07-001', 'Ezek.29.8'): ('WARRANT-rival', 'licensed rival, addressee turns feminine', 'Mirrors the anchor the ordered A9/A10 weighing introduces; 29:8 is in span and would otherwise be unmirrored.'),

 ('P07-002', 'Ezek.29.9'): ('WARRANT-onset', 'prior close, collision behind onset', 'Far face of the onset seam 29:9/29:10.'),
 ('P07-002', 'Ezek.29.17'): ('WARRANT-close', 'year-27 dateline bounds the close', 'Far face of the close seam 29:16/29:17.'),

 ('P07-003', 'Ezek.30.1'): ('WARRANT-close', 'undated word-event opens ahead', 'Far face of the close seam 29:21/30:1.'),
 ('P07-003', 'Ezek.29.16'): ('DISCLOSURE-mark', 'petuchah corroborating the dateline onset', 'MEASURED: PE on Ezek.29.16, behind this row\u2019s onset.'),

 ('P07-004', 'Ezek.30.13'): ('WARRANT-close', 'messenger onset immediately past close', 'Far face of the close seam 30:12/30:13.'),
 ('P07-004', 'Ezek.29.21'): ('DISCLOSURE-mark', 'open-section mark behind this onset', 'MEASURED: PE on Ezek.29.21.'),

 ('P07-009', 'Ezek.30.14-Ezek.30.18'): ('WARRANT-absence-over-range', 'no formula, no mark inside', 'MEASURED over pmarks_Ezek.json: no parashah mark on Ezek.30.14-30.18 (ch 30 marks follow 30:5, 30:9, 30:12, 30:19, 30:21, 30:26). MEASURED over Ezek_oshb.txt: no messenger formula in 30:14-18 (ch-30 occurrences at 30:2, 30:6, 30:10, 30:13, 30:22) and no word-event. One apparatus item DOES fall inside - a K/Q at MT 30:16 - which the row already discloses separately, so the absence claim is scoped to formula and mark and not overstated to K/Q. ONE range entry.'),
}
# extra entries that mirror anchors my ordered prose rewrites introduce
EXTRA = {('P05-004', 'Ezek.22.31'): ('P05-004', 'MARKS_3D', 'mark'),
         ('P05-007', 'Ezek.24.9'): ('P05-007', 'GROUNDS', 'grounds'),
         ('P07-001', 'Ezek.29.8'): ('P07-001', 'GROUNDS', 'grounds')}

a4_items = {}
for i, it in enumerate(ITEMS):
    if it['cls'] == 'A4_CITATION':
        a4_items[(it['row_id'], it['citation'])] = IDS[i]

missing = [k for k in a4_items if k not in A4]
assert not missing, 'A4 table missing %s' % missing
for row, cit in a4_items:
    pass
for key in A4:
    assert key in a4_items or key in EXTRA, 'stray A4 entry %s' % (key,)

for (row, cit), (token, txt) in sorted([(k, (v[0], v[1])) for k, v in A4.items()]):
    assert token in lane['role_vocabulary'], token
    assert len(txt.split()) <= 6, (cit, txt, len(txt.split()))
    entry = 'web:%s [%s] %s' % (cit, token, txt)
    cur = ROWS[row]['boundary_evidence_refs']
    items = [a4_items[(row, cit)]] if (row, cit) in a4_items else [iid(*EXTRA[(row, cit)])]
    EDITS.append(dict(row_id=row, field='boundary_evidence_refs', op='append_ref',
                      expected_before=cur, value=entry, worklist_item_ids=items,
                      sweep='a4', role_token=token, why=A4[(row, cit)][2],
                      tier='MEASURED: the citation is argued in the row\u2019s prose and no existing refs entry covers it; the verse-level facts named in the free text are measured over the pinned inputs'))

io.open(WORK + r'\edits.json', 'w', encoding='utf-8').write(json.dumps(EDITS, ensure_ascii=False, indent=1))
print('EDITS %d  (confidence %d, prose %d, append_ref %d)' % (
    len(EDITS), sum(1 for e in EDITS if e['op'] == 'set_confidence'),
    sum(1 for e in EDITS if e['op'] == 'set'), sum(1 for e in EDITS if e['op'] == 'append_ref')))
io.open(WORK + r'\item_ids.json', 'w', encoding='utf-8').write(json.dumps(IDS, ensure_ascii=False, indent=1))
# one edit per (row, field) for set ops
seen = {}
for e in EDITS:
    if e['op'] in ('set', 'set_confidence'):
        k = (e['row_id'], e['field'])
        assert k not in seen, 'TWO SET EDITS on %s' % (k,)
        seen[k] = 1
print('one-edit-per-row-field OK')
# every append_ref on a row shares the same expected_before
from collections import defaultdict
g = defaultdict(list)
for e in EDITS:
    if e['op'] == 'append_ref':
        g[e['row_id']].append(json.dumps(e['expected_before'], ensure_ascii=False))
for r, v in g.items():
    assert len(set(v)) == 1, r
print('append_ref shared expected_before OK for %d rows' % len(g))
