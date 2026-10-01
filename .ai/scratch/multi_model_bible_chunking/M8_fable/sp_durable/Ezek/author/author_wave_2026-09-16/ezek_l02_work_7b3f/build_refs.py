# -*- coding: utf-8 -*-
import json
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_02_worklist.json'
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
ITEMS = lane['your_worklist_items']
VOCAB = set(lane['role_vocabulary'])

# (item index, row, citation-as-written-in-entry, ROLE token, free text <=6 words)
PLAN = [
 (2,  'P01-011', 'web:Ezek.7.1',                 'WARRANT-close',              'word-event reopens beyond the close'),
 (5,  'P01-012', 'web:Ezek.7.5',                 'WARRANT-close',              'fresh messenger formula past this close'),
 (6,  'P01-012', 'web:Ezek.7.5-Ezek.7.27',       'WARRANT-rival',              "the single continuous end oracle"),
 (7,  'P01-012', 'web:Ezek.6.14',                'DISCLOSURE-mark',            'pe recorded behind the onset'),
 (12, 'P01-013', 'web:Ezek.7.5',                 'WARRANT-onset',              'messenger formula opens this unit'),
 (13, 'P01-013', 'web:Ezek.7.10',                'WARRANT-close',              'no formula beyond this seam'),
 (14, 'P01-013', 'web:Ezek.7.5-Ezek.7.27',       'WARRANT-rival',              'single long row weighed here'),
 (19, 'P01-014', 'web:Ezek.7.10',                'WARRANT-onset',              'unmarked doom-poem opens here'),
 (20, 'P01-014', 'web:Ezek.7.23',                'ANCHOR',                     'tier-4 paragraphing, texture only'),
 (21, 'P01-014', 'web:Ezek.7.15',                'ANCHOR',                     'translation-layer break, no weight'),
 (24, 'P02-001', 'web:Ezek.8.5',                 'ANCHOR',                     'the eyes-lifted scene named'),
 (25, 'P02-001', 'web:Ezek.8.4',                 'WARRANT-rival',              'glory notice weighed as cut'),
 (26, 'P02-001', 'web:Ezek.8.7-Ezek.8.13',       'WARRANT-rival',              'extension into the next tableau'),
 (28, 'P02-002', 'web:Ezek.8.14',                'WARRANT-close',              'transport opens the next tableau'),
 (30, 'P02-003', 'web:Ezek.8.18',                'WARRANT-close',              'wrath declaration closes here'),
 (31, 'P02-003', 'web:Ezek.9.1',                 'WARRANT-close',              'the cry opens beyond this close'),
 (32, 'P02-003', 'web:Ezek.8.15',                'WARRANT-rival',              'pointer close of the held rival'),
 (35, 'P02-004', 'web:Ezek.8.18',                'WARRANT-onset',              'where the prior scene stopped'),
 (38, 'P02-006', 'web:Ezek.10.18',               'WARRANT-close',              'narration resumes past this close'),
 (39, 'P02-006', 'web:Ezek.10.1-Ezek.10.8',      'WARRANT-absence-over-range', 'no mark, no K-Q there'),
 (40, 'P02-006', 'web:Ezek.10.18-Ezek.10.22',    'WARRANT-rival',              'fold forward into that unit'),
 (41, 'P02-006', 'web:Ezek.10.1-Ezek.10.22',     'WARRANT-rival',              'whole chapter as one row'),
 (42, 'P02-006', 'web:Ezek.10.1-Ezek.11.13',     'WARRANT-rival',              'chapter plus courtyard scene together'),
 (45, 'P02-007', 'web:Ezek.11.1',                'WARRANT-close',              'transport onset just past close'),
 (46, 'P02-007', 'web:Ezek.11.1-Ezek.11.13',     'WARRANT-rival',              'one continuous east-gate scene'),
 (48, 'P02-008', 'web:Ezek.11.5',                'WARRANT-rival',              'sub-onset weighed, held as texture'),
 (50, 'P02-009', 'web:Ezek.11.22-Ezek.11.25',    'WARRANT-rival',              'folding into the return unit'),
 (51, 'P02-009', 'web:Ezek.11.19',               'ANCHOR',                     'content cited for the category'),
 (55, 'P02-010', 'web:Ezek.11.22',               'WARRANT-onset',              'vision frame resumes at onset'),
 (56, 'P02-010', 'web:Ezek.12.1',                'WARRANT-close',              'plain word-event past the seam'),
 (59, 'P02-011', 'web:Ezek.12.8',                'WARRANT-close',              'morning re-onset beyond close'),
 (60, 'P02-012', 'web:Ezek.12.1-Ezek.12.7',      'ANCHOR',                     'the paired row named'),
 (61, 'P02-012', 'web:Ezek.12.7',                'DISCLOSURE-mark',            'pe anchoring the onset side'),
 (62, 'P02-013', 'web:Ezek.12.21',               'WARRANT-close',              'strict word-event past this close'),
 (64, 'P02-014', 'web:Ezek.12.22',               'QUOTE',                      'the quoted proverb sits here'),
 (65, 'P02-015', 'web:Ezek.12.27',               'QUOTE',                      'quoted saying anchored here'),
 (69, 'P02-017', 'web:Ezek.13.10',               'WARRANT-onset',              'the whitewash turn opens here'),
 (73, 'P02-020', 'web:Ezek.15.1',                'WARRANT-close',              'fresh word-event beyond the close'),
 (75, 'P03-001', 'web:Ezek.15.2',                'WARRANT-onset',              'son-of-man address completes onset'),
 (76, 'P03-002', 'web:Ezek.16.2',                'WARRANT-onset',              'address inside the opening frame'),
 (77, 'P03-002', 'web:Ezek.16.15',               'WARRANT-close',              'unfaithfulness turn past close'),
 (78, 'P03-002', 'web:Ezek.16.8',                'WARRANT-rival',              'mid-verse oath weighed, refused'),
 (80, 'P03-003', 'web:Ezek.16.14',               'WARRANT-onset',              'verse-final close behind onset'),
 (81, 'P03-003', 'web:Ezek.16.20',               'WARRANT-close',              'new material opens past close'),
 (82, 'P03-003', 'web:Ezek.16.1-Ezek.16.14',     'WARRANT-rival',              'refusion with the first movement'),
]

# --- checks on the plan -------------------------------------------------------
a4_idx = [i for i, it in enumerate(ITEMS) if it['cls'] == 'A4_CITATION']
assert sorted(p[0] for p in PLAN) == a4_idx, (sorted(p[0] for p in PLAN), a4_idx)
by_tok = {}
for idx, row, cite, tok, txt in PLAN:
    assert tok in VOCAB, tok
    it = ITEMS[idx]
    assert it['row_id'] == row, (idx, row, it['row_id'])
    # the citation written into the entry must match the ruled citation, on the WEB face
    want = it['citation']
    got = cite.replace('web:', '')
    if it['citation_kind'] == 'range':
        assert got == want, (idx, got, want)
    else:
        assert got == want, (idx, got, want)
    w = len(txt.split())
    assert w <= 6, (idx, w, txt)
    by_tok.setdefault(tok, set()).add(txt)
print('role-token usage and distinct formulations:')
for t in sorted(by_tok):
    n = sum(1 for p in PLAN if p[3] == t)
    print('   %-28s entries=%2d distinct_formulations=%2d' % (t, n, len(by_tok[t])))
allt = [p[4] for p in PLAN]
assert len(allt) == len(set(allt)), 'a free-text formulation repeats'

def entry(cite, tok, txt):
    return '%s [%s] %s' % (cite, tok, txt)

EDITS = []
# --- P01-013 needs an in-place amendment (I11) as well as three appends, so its
# --- refs field takes ONE set edit carrying the complete final list.
row = ROWS['P01-013']
cur = row['boundary_evidence_refs']
old0 = cur[0]
new0 = old0.replace('\u2018my eye will not spare\u2019', '\u201cmy eye will not spare\u201d (web:Ezek.7.4)')
assert new0 != old0, old0
final = [new0] + list(cur[1:]) + [entry(c, t, x) for (i, r, c, t, x) in PLAN if r == 'P01-013']
EDITS.append(dict(row_id='P01-013', field='boundary_evidence_refs', op='set',
  expected_before=cur, value=final,
  worklist_item_ids=['L02-I11', 'L02-I12', 'L02-I13', 'L02-I14'], sweep='a4',
  role_token='WARRANT-onset | WARRANT-close | WARRANT-rival (one per appended entry, written into each entry)',
  why="This row's refs field carries BOTH an in-place amendment and appends, so it takes one set edit whose value is the complete final list, per the one-edit-per-(row,field) rule. Entry 1 is amended for A6 item I11: the five-word run inside it was delimited with curly SINGLE quotes and carried no in-field reference, so it now takes double curly quotes plus (web:Ezek.7.4), the verse MEASURED to carry that wording. The three ruled A4 citations are then appended, each with exactly one ROLE token. No existing entry is re-tokenised.",
  tier='MEASURED (the run and its single WEB occurrence re-measured over tools/verse_map_web.json; the three citations are the ruled set)'))

# --- every other row: pure append_ref, all sharing that row's current list ----
for rid in [r['decision_id'] for r in lane['your_rows']]:
    if rid == 'P01-013':
        continue
    plans = [p for p in PLAN if p[1] == rid]
    if not plans:
        continue
    expected = ROWS[rid]['boundary_evidence_refs']
    for (idx, r, cite, tok, txt) in plans:
        it = ITEMS[idx]
        EDITS.append(dict(row_id=rid, field='boundary_evidence_refs', op='append_ref',
          expected_before=expected, value=entry(cite, tok, txt),
          worklist_item_ids=['L02-I%02d' % idx], sweep='a4', role_token=tok,
          why="DEF-A4-ARGUED install for the ruled citation %s, argued in %s (%s, %s): one entry for the whole citation, %s. ROLE token %s: %s"
               % (it['citation'], it['field'], it['citation_kind'], it['a4_class'],
                  'a range citation taking a single range entry' if it['citation_kind'] == 'range' else 'a single-verse entry',
                  tok, {
                    'WARRANT-onset': "the row's onset rests on this verse",
                    'WARRANT-close': "the row's close rests on this verse",
                    'WARRANT-rival': 'this is the A9/A16 rival the row weighs at this verse or span',
                    'WARRANT-absence-over-range': 'the row makes a no-mark / no-K-Q claim over this range',
                    'DISCLOSURE-mark': 'this is a parashah-mark disclosure, not a driver',
                    'ANCHOR': 'a content or structural statement the boundary does not rest on',
                    'QUOTE': 'an A6 quotation run is anchored at this verse'}[tok]),
          tier='MEASURED (the citation is argued in the named field and no existing entry covers it under DEF-A4-ARGUED clause 3; written on the WEB face, which web_mt_offset_map.json states is identity outside the ch 20/21 zone, and this lane touches no verse in that zone)'))

json.dump(EDITS, open('refs_edits.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nOK %d refs edits built (%d append_ref + %d set)' % (
    len(EDITS), sum(1 for e in EDITS if e['op'] == 'append_ref'), sum(1 for e in EDITS if e['op'] == 'set')))
