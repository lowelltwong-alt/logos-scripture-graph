# -*- coding: utf-8 -*-
import json, re, os, hashlib
D = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l02_work_7b3f'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_02_worklist.json'
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
dl = json.load(open(os.path.join(D, 'ezek_author_l02_deliverable.json'), encoding='utf-8'))
E = dl['edits']
fails = []

FORBIDDEN = {'span', 'osis_start', 'osis_end', 'decision_id', 'chunk_index_in_book',
             'writer_part', 'writer_decision_id', 'writer_attempt_id', 'book', 'model_id'}
ALLOWED = {'boundary_rationale', 'strongest_rejected_alternative', 'device_notes',
           'boundary_evidence_refs', 'confidence', 'observed_substrate_signals',
           'strong_or_hebrew_tags_used', 'literature_type_guess', 'unit_type'}

# 1. expected_before byte-exactness against the lane file
for i, e in enumerate(E):
    cur = ROWS[e['row_id']][e['field']]
    if e['expected_before'] != cur:
        fails.append('EXPECTED_BEFORE MISMATCH edit %d %s.%s' % (i, e['row_id'], e['field']))
    if e['field'] in FORBIDDEN:
        fails.append('FORBIDDEN FIELD edit %d %s' % (i, e['field']))
    if e['field'] not in ALLOWED:
        fails.append('FIELD NOT IN ALLOWED SET edit %d %s' % (i, e['field']))

# 2. one edit per (row, field) except append_ref
from collections import Counter
c = Counter((e['row_id'], e['field']) for e in E if e['op'] != 'append_ref')
for k, v in c.items():
    if v != 1:
        fails.append('MULTIPLE NON-APPEND EDITS on %s' % (k,))
# a row+field must not mix set and append_ref
mix = {}
for e in E:
    mix.setdefault((e['row_id'], e['field']), set()).add(e['op'])
for k, ops in mix.items():
    if 'append_ref' in ops and len(ops) > 1:
        fails.append('MIXED set+append_ref on %s' % (k,))

# 3. all append_ref on one row share identical expected_before
byrow = {}
for e in E:
    if e['op'] == 'append_ref':
        byrow.setdefault(e['row_id'], []).append(e)
for rid, es in byrow.items():
    if any(x['expected_before'] != es[0]['expected_before'] for x in es):
        fails.append('APPEND_REF expected_before differs on %s' % rid)

# 4. simulate application
sim = {rid: dict(r) for rid, r in ROWS.items()}
for e in E:
    if e['op'] == 'append_ref':
        sim[e['row_id']]['boundary_evidence_refs'] = list(sim[e['row_id']]['boundary_evidence_refs']) + [e['value']]
    else:
        sim[e['row_id']][e['field']] = e['value']
for rid, r in sim.items():
    for f in ('boundary_rationale', 'strongest_rejected_alternative', 'device_notes', 'literature_type_guess'):
        if not isinstance(r[f], str) or not r[f].strip():
            fails.append('EMPTY FIELD after apply %s.%s' % (rid, f))
    for x in r['boundary_evidence_refs']:
        if not isinstance(x, str) or not x.strip():
            fails.append('EMPTY REF after apply %s' % rid)
    if r['confidence'] not in ('high', 'medium', 'medium_low', 'low'):
        fails.append('OFF-SCALE CONFIDENCE %s -> %r' % (rid, r['confidence']))
    if r['span'] != ROWS[rid]['span']:
        fails.append('SPAN CHANGED %s' % rid)

# 5. role tokens present and unique per appended entry
VOCAB = lane['role_vocabulary']
newrefs = []
for e in E:
    if e['op'] == 'append_ref':
        newrefs.append(e['value'])
    elif e['field'] == 'boundary_evidence_refs':
        old = set(e['expected_before'])
        newrefs += [x for x in e['value'] if x not in old]
amended = [x for x in newrefs if not x.startswith('web:Ezek.')]
a4entries = [x for x in newrefs if x.startswith('web:Ezek.')]
print('new/changed refs strings: %d  (A4 installs: %d, in-place amendments: %d)'
      % (len(newrefs), len(a4entries), len(amended)))
if len(a4entries) != 45:
    fails.append('A4 ENTRY COUNT %d != 45' % len(a4entries))
for x in amended:
    if '“my eye will not spare” (web:Ezek.7.4)' not in x:
        fails.append('UNEXPECTED AMENDED ENTRY: %r' % x)
frees = []
for x in a4entries:
    br = re.findall(r'\[([^\]]+)\]', x)
    if len(br) != 1 or br[0] not in VOCAB:
        fails.append('ROLE TOKEN PROBLEM: %r -> %r' % (x, br))
        continue
    free = x.split(']', 1)[1].strip()
    frees.append(free)
    if len(free.split()) > 6:
        fails.append('FREE TEXT > 6 WORDS: %r' % x)
if len(set(frees)) != len(frees):
    fails.append('FREE TEXT REPEATS')
print('distinct free-text annotations: %d of %d' % (len(set(frees)), len(frees)))

# 6. seven-gram self-collision across the NEW prose I authored
def grams(s, n=7):
    w = re.sub(r'[^a-z0-9 ]', ' ', s.lower()).split()
    return set(tuple(w[i:i + n]) for i in range(max(0, len(w) - n + 1)))
newtext = {}
for e in E:
    if e['op'] == 'set' and e['field'] != 'boundary_evidence_refs':
        old = grams(e['expected_before'])
        added = grams(e['value']) - old
        newtext['%s.%s' % (e['row_id'], e['field'])] = added
keys = list(newtext)
coll = []
for a in range(len(keys)):
    for b in range(a + 1, len(keys)):
        inter = newtext[keys[a]] & newtext[keys[b]]
        if inter:
            coll.append((keys[a], keys[b], sorted(' '.join(t) for t in inter)[:4], len(inter)))
print('7-gram collisions among my newly authored prose: %d pair(s)' % len(coll))
for x in coll:
    print('   %s <-> %s  n=%d  e.g. %s' % (x[0], x[1], x[3], x[2]))

# 7. items check
ids = ['L02-I%02d' % i for i in range(len(lane['your_worklist_items']))]
disch = set(dl['items_discharged'])
nd = set(x['item'] for x in dl['items_NOT_discharged'])
assert disch | nd == set(ids), set(ids) - (disch | nd)
assert not (disch & nd)
print('items: %d discharged, %d not discharged, %d total, no overlap, no drop'
      % (len(disch), len(nd), len(ids)))

print()
if fails:
    print('FAILURES (%d):' % len(fails))
    for f in fails:
        print('  ', f)
else:
    print('SELF-CHECK CLEAN: all %d edits pass expected_before byte-equality, field legality, '
          'one-edit-per-(row,field), append_ref expected_before identity, post-apply integrity, '
          'role-token and free-text checks.' % len(E))
