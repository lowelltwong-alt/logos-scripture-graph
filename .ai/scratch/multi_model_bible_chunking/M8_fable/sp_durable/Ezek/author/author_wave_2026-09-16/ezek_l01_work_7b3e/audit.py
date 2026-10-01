# -*- coding: utf-8 -*-
import json, re
W = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l01_work_7b3e'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
d = json.load(open(LANE, encoding='utf-8'))
rows = {r['decision_id']: r for r in d['your_rows']}
items = d['your_worklist_items']
o = json.load(open(W + r'\ezek_author_l01_deliverable.json', encoding='utf-8'))
E = o['edits']
fail = []


def ck(name, cond, extra=''):
    print(('PASS  ' if cond else 'FAIL  ') + name + (('  ' + str(extra)) if extra else ''))
    if not cond:
        fail.append(name)


FORBIDDEN = {'span', 'osis_start', 'osis_end', 'decision_id', 'book', 'model_id',
             'chunk_index_in_book', 'writer_part', 'writer_decision_id', 'writer_attempt_id',
             'parent_collection', 'confidence'}
ALLOWED = {'boundary_rationale', 'strongest_rejected_alternative', 'device_notes',
           'boundary_evidence_refs', 'confidence', 'observed_substrate_signals',
           'strong_or_hebrew_tags_used', 'literature_type_guess', 'unit_type'}
VOCAB = set(d['role_vocabulary'])

ck('no edit touches a seam or identity field', not (set(e['field'] for e in E) & FORBIDDEN),
   sorted(set(e['field'] for e in E)))
ck('no edit touches confidence', not any(e['field'] == 'confidence' or e['op'] == 'set_confidence' for e in E))
ck('every field is in the allowed set', set(e['field'] for e in E) <= ALLOWED)
ck('every edit has row_id/field/op/expected_before/value/worklist_item_ids/sweep/why/tier',
   all(all(k in e for k in ('row_id', 'field', 'op', 'expected_before', 'value',
                            'worklist_item_ids', 'sweep', 'why', 'tier')) for e in E))
ck('every row_id is one of mine', all(e['row_id'] in rows for e in E))

# expected_before byte-exact (all but the one declared rebase)
bad = []
for e in E:
    cur = rows[e['row_id']][e['field']]
    if e['expected_before'] != cur:
        bad.append((e['row_id'], e['field'], e['sweep']))
ck('expected_before == lane-file bytes for all but the 1 declared rebase', len(bad) == 1, bad)
ck('the single exception is the declared P01-001 refs a6 rebase',
   bad == [('P01-001', 'boundary_evidence_refs', 'a6')])
reb = [e for e in E if e['row_id'] == 'P01-001' and e['sweep'] == 'a6'][0]
ap = [e['value'] for e in E if e['row_id'] == 'P01-001' and e['sweep'] == 'a4']
ck('rebase == original list + its a4 append',
   reb['expected_before'] == list(rows['P01-001']['boundary_evidence_refs']) + ap)
ck('rebase why names the dependency', 'REBASED' in reb['why'] or 'rebased' in reb['why'].lower())

# append_ref shape
ar = [e for e in E if e['op'] == 'append_ref']
ck('48 append_ref edits, all on boundary_evidence_refs, value is ONE string',
   len(ar) == 48 and all(e['field'] == 'boundary_evidence_refs' and isinstance(e['value'], str) for e in ar))
ck('every append_ref carries exactly one valid ROLE token',
   all(e.get('role_token') in VOCAB and e['value'].count('[') == 1 for e in ar))
ck('token in the entry string matches the role_token field',
   all(('[' + e['role_token'] + ']') in e['value'] for e in ar))
ck('range citations got RANGE entries, not per-verse entries',
   all(('-Ezek.' in e['value']) == (items[int(e['worklist_item_ids'][0].split('#')[1])]['citation_kind'] == 'range')
       for e in ar))
ck('every annotation is <= 6 words',
   all(len(e['value'].split(']', 1)[1].split()) <= 6 for e in ar))
ck('no dual-face ref written (span is wholly outside the ch 20/21 zone)',
   not any(' = oshb:' in e['value'] or 'web:Ezek.2' in e['value'] for e in ar))

# set edits
st = [e for e in E if e['op'] == 'set']
ck('15 set edits, one per (row,field)',
   len(st) == 15 and len({(e['row_id'], e['field']) for e in st}) == 15)
ck('every set value differs from its expected_before', all(e['value'] != e['expected_before'] for e in st))

# A6 convention present
LD, RD = '\u201c', '\u201d'
a6 = [e for e in st if e['sweep'] == 'a6']
ck('12 a6 set edits', len(a6) == 12)
for e in a6:
    v = e['value'] if isinstance(e['value'], str) else '\n'.join(e['value'])
    b = e['expected_before'] if isinstance(e['expected_before'], str) else '\n'.join(e['expected_before'])
    n = len(e['worklist_item_ids'])
    added_q = v.count(LD) - b.count(LD)
    added_r = len(re.findall(r'\(web:Ezek\.', v)) - len(re.findall(r'\(web:Ezek\.', b))
    okq, okr = added_q == n, added_r == n
    if not (okq and okr):
        fail.append('a6 convention %s/%s' % (e['row_id'], e['field']))
    print('  a6 %-9s %-32s items=%d  +opening-curly=%d  +web:refs=%d  %s'
          % (e['row_id'], e['field'], n, added_q, added_r, 'OK' if okq and okr else 'CHECK'))
ck('each a6 set adds exactly one double-curly delimiter and one web: ref per item it discharges',
   not [f for f in fail if f.startswith('a6 convention')])

# grounds edits
g = [e for e in st if e['sweep'] == 'grounds']
ck('3 grounds set edits on 2 items', len(g) == 3 and
   {i for e in g for i in e['worklist_item_ids']} == {'l01#56', 'l01#73'})
p8 = [e for e in g if e['row_id'] == 'P01-008'][0]['value']
ck('P01-008 SRA names the 4:3 samekh, the colophon and all three bare-ve-attah stages',
   all(s in p8 for s in ('samekh after oshb:Ezek.4.3', 'colophon', '4:3, 4:4 and 4:9', '\u00a77')))
dn = [e for e in g if e['field'] == 'device_notes'][0]['value']
ck('P01-009 device_notes retracts the false ground and names the three coincidences',
   ('false and is corrected' in dn) and all(s in dn for s in ('oshb:Ezek.5.5', 'oshb:Ezek.5.7', 'oshb:Ezek.5.8')))
ck('P01-009 device_notes no longer asserts the false clause',
   'none coincides with a formula onset' not in dn)
s9 = [e for e in g if e['row_id'] == 'P01-009' and e['field'] == 'strongest_rejected_alternative'][0]['value']
ck('P01-009 SRA weighs 5:4/5:5 under A16 naming the PE and the formula',
   all(s in s9 for s in ('A16', '5:4/5:5', 'PE recorded after', 'messenger formula')))
ck('P01-009 SRA keeps the pre-existing 5:13/5:15 rival', 'Cutting at 5:13 or 5:15' in s9)

# item accounting
allid = ['l01#%02d' % i for i in range(84)]
disc = set(o['items_discharged'])
nd = {x['item'] for x in o['items_NOT_discharged']}
ck('84 item ids, every one in exactly one list',
   len(disc | nd) == 84 and not (disc & nd) and set(allid) == (disc | nd))
wed = {i for e in E for i in e['worklist_item_ids']}
noed = {x['item'] for x in o['items_discharged_without_edit']}
ck('discharged == (items with an edit) union (7 exempt rulings)', disc == wed | noed)
ck('the 7 no-edit items have no edit anywhere', not (noed & wed), sorted(noed & wed))
ck('every no-edit item is an A6 item', all(items[int(x.split('#')[1])]['cls'] == 'A6' for x in noed))
ck('every no-edit item carries a ruling and a why',
   all(x.get('ruling') and len(x.get('why', '')) > 40 for x in o['items_discharged_without_edit']))
ck('every edit item id is a real index', all(0 <= int(i.split('#')[1]) < 84 for i in wed))
ck('each edit\'s items belong to that edit\'s row',
   all(items[int(i.split('#')[1])]['row_id'] == e['row_id'] for e in E for i in e['worklist_item_ids']))
ck('each edit\'s items belong to that edit\'s sweep class',
   all({'A6': 'a6', 'A4_CITATION': 'a4', 'GROUNDS': 'grounds'}[items[int(i.split('#')[1])]['cls']] == e['sweep']
       for e in E for i in e['worklist_item_ids']))
ck('no worklist item claimed moves_seam', all(items[int(i.split('#')[1])]['moves_seam'] is False for i in wed | noed))

# narrative completeness
for k in ('changes_made_or_no_change', 'e19_selfreport', 'limit'):
    ck('%s is substantive' % k, len(o[k]) > 200)
ck('verification_evidence has >= 10 entries', len(o['verification_evidence']) >= 10, len(o['verification_evidence']))
ck('unresolved_uncertainty has >= 5 entries', len(o['unresolved_uncertainty']) >= 5, len(o['unresolved_uncertainty']))
ck('escalations recorded', len(o['escalations']) == 5)
ck('12 sources, each with a read note', len(o['sources']) == 12 and all(s['read'] for s in o['sources']))

print('\n' + ('ALL AUDIT CHECKS PASSED' if not fail else 'FAILURES: %s' % sorted(set(fail))))
