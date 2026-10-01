# -*- coding: utf-8 -*-
import json, re
from collections import defaultdict, Counter

LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
d = json.load(open(LANE, encoding='utf-8'))
rows = {r['decision_id']: r for r in d['your_rows']}
items = d['your_worklist_items']
a6 = json.load(open('a6_newvals.json', encoding='utf-8'))
LD, RD = '\u201c', '\u201d'


def IID(i):
    return 'l01#%02d' % i


A4 = {
 2:  ('WARRANT-close', "far face of the close seam"),
 5:  ('WARRANT-onset', "the onset rests here"),
 6:  ('ANCHOR', "sending content, not boundary evidence"),
 7:  ('DISCLOSURE-device', "messenger embedded, not an onset"),
 8:  ('WARRANT-close', "sub-onset beyond this close"),
 11: ('WARRANT-onset', "sub-onset opens this unit"),
 12: ('ANCHOR', "scroll appears; no seam claimed"),
 13: ('WARRANT-rival', "rival cut weighed, not taken"),
 14: ('WARRANT-close', "next unit address opens here"),
 20: ('WARRANT-onset', "fresh address opens the unit"),
 21: ('ANCHOR', "audience description only"),
 22: ('WARRANT-close', "the close rests here"),
 23: ('WARRANT-rival', "rival onset candidate assessed"),
 24: ('WARRANT-absence-over-range', "no such device across range"),
 25: ('WARRANT-close', "transport scene opens past close"),
 26: ('DISCLOSURE-mark', "pe behind this unit opening"),
 30: ('WARRANT-onset', "transport verb opens the scene"),
 31: ('WARRANT-close', "word-event on the far face"),
 34: ('ANCHOR', "watchman charge, boundary-neutral"),
 35: ('WARRANT-close', "hand construct reopens beyond close"),
 36: ('WARRANT-rival', "backward extension weighed, declined"),
 41: ('WARRANT-close', "far side opened by sub-onset"),
 42: ('DISCLOSURE-device', "interior refrain; close falls later"),
 43: ('ANCHOR', "sign-act block named as content"),
 44: ('DISCLOSURE-mark', "samekh on record before onset"),
 49: ('WARRANT-onset', "prior refrain close behind onset"),
 50: ('DISCLOSURE-device', "second address intensifies only"),
 51: ('WARRANT-rival', "bare ve-attah rival, unlicensed"),
 52: ('WARRANT-close', "fresh sign-act begins past close"),
 53: ('WARRANT-rival', "A9 rival: colophon plus samekh"),
 54: ('DISCLOSURE-mark', "setumah inside the span"),
 55: ('DISCLOSURE-mark', "a further closed-section mark"),
 61: ('WARRANT-rival', "A16 rival far face"),
 62: ('DISCLOSURE-device', "verdict formula inside the span"),
 63: ('ANCHOR', "shared clause, first occurrence"),
 64: ('ANCHOR', "same clause recurring, no seam"),
 65: ('WARRANT-rival', "no onset follows the rival"),
 66: ('WARRANT-close', "strict word-event past this close"),
 67: ('DISCLOSURE-mark', "samekh follows; single witness"),
 68: ('DISCLOSURE-mark', "interior closed section noted"),
 69: ('ANCHOR', "parallel size case, structural only"),
 70: ('DISCLOSURE-mark', "petuchah before the messenger formula"),
 71: ('DISCLOSURE-mark', "open-section mark, disclosed only"),
 72: ('DISCLOSURE-mark', "pe at the opening seam"),
 80: ('ANCHOR', "oracle direction, not a warrant"),
 81: ('WARRANT-rival', "continuation defeats the earlier cut"),
 82: ('WARRANT-close', "messenger formula reopens after close"),
 83: ('DISCLOSURE-mark', "mark recorded behind this onset"),
}

VOCAB = set(d['role_vocabulary'])
a4_idx = [i for i, it in enumerate(items) if it['cls'] == 'A4_CITATION']
assert set(A4) == set(a4_idx), ('A4 coverage mismatch', set(a4_idx) ^ set(A4))

bytok = defaultdict(set)
for i, (tok, txt) in A4.items():
    assert tok in VOCAB, (i, tok)
    assert len(txt.split()) <= 6, (i, len(txt.split()), txt)
    bytok[tok].add(txt)

print('ROTATION CHECK (<=6 words each; >=4 distinct formulations where a token is used >=4 times):')
for tok in sorted(bytok):
    n = sum(1 for i, (t, _) in A4.items() if t == tok)
    ok = (len(bytok[tok]) >= 4) or (n < 4)
    print('  %-28s uses=%2d distinct=%2d OK=%s' % (tok, n, len(bytok[tok]), ok))
    assert ok, (tok, n, len(bytok[tok]))


def entry(i):
    it = items[i]
    tok, txt = A4[i]
    return 'oshb:%s [%s] %s' % (it['citation'], tok, txt)


appends = defaultdict(list)
for i in a4_idx:
    appends[items[i]['row_id']].append((i, entry(i)))
print('\nA4 entries per row: %s  total=%d' % ({r: len(v) for r, v in appends.items()},
                                              sum(len(v) for v in appends.values())))

# ---------------- GROUNDS rewrites ----------------
COLOPHON = '\u05d0\u05d5\u05b9\u05ea \u05d4\u05b4\u05d9\u05d0 \u05dc\u05b0\u05d1\u05b5\u05d9\u05ea \u05d9\u05b4\u05e9\u05b0\u05c2\u05e8\u05b8\u05d0\u05b5\u05dc'
VEATTAH_TITLED = '\u05d5\u05b0\u05d0\u05b7\u05ea\u05bc\u05b8\u05d4 \u05d1\u05b6\u05df \u05d0\u05b8\u05d3\u05b8\u05dd'
VEATTAH_BARE = '\u05d5\u05b0\u05d0\u05b7\u05ea\u05bc\u05b8\u05d4'
LAKHEN = '\u05dc\u05b8\u05db\u05b5\u05df'
END54 = '\u05de\u05b4\u05de\u05bc\u05b6\u05e0\u05bc\u05d5\u05bc \u05ea\u05b5\u05e6\u05b5\u05d0 \u05d0\u05b5\u05e9 \u05d0\u05b6\u05dc \u05db\u05bc\u05b8\u05dc \u05d1\u05bc\u05b5\u05d9\u05ea \u05d9\u05b4\u05e9\u05b0\u05c2\u05e8\u05b8\u05d0\u05b5\u05dc'
MESS55 = '\u05db\u05bc\u05b9\u05d4 \u05d0\u05b8\u05de\u05b7\u05e8 \u05d0\u05b2\u05d3\u05b9\u05e0\u05b8\u05d9 \u05d9\u05b0\u05d4\u05b9\u05d5\u05b4\u05d4'

G = {}

G[('P01-008', 'strongest_rejected_alternative')] = (
 "Splitting the tile sign-act (4:1-4:3) from the lying and food-rationing sign-acts (4:4-4:17) as two units. "
 "This is the question the strategy holds at \u00a77 for chs 4-7, and the 4:3/4:4 seam is its strongest form. "
 "Named and weighed under A9: on the near face the witness records a samekh after oshb:Ezek.4.3, and that verse "
 "closes on the sign-act colophon " + COLOPHON + " (oshb:Ezek.4.3), "
 + LD + "This shall be a sign to the house of Israel" + RD + " (web:Ezek.4.3), standing verse-final. "
 "On the far face oshb:Ezek.4.4 carries no formula whatever: in the pinned inventory no verse of ch 4 belongs to "
 "the messenger, utterance, recognition or word-event classes, the chapter's only listed members being the "
 "son-of-man address at 4:1 and 4:16 and the year-word non-datelines at 4:5-4:6. The colophon is not a close-role "
 "formula - oshb:Ezek.4.3 is absent from both the 81-verse utterance list and the 64-verse recognition family - so "
 "CUT-RULE's second limb is not met; and the addressee is unchanged across the seam, 2ms imperatives standing to "
 "the prophet on either side, so its first limb is not met either. A mark alone never satisfies limb (b). The "
 "rival is therefore paragraph-grade, held on those grounds, and the samekh is disclosed for the alternative it "
 "corroborates rather than for this row. The test is reworded because its earlier form omitted 4:3, the very verse "
 "the mark follows: the titled sub-onset " + VEATTAH_TITLED + " stands at 4:1 and again at 5:1, whereas bare "
 + VEATTAH_BARE + " without the title opens three interior stages - 4:3, 4:4 and 4:9 - so the text stages the "
 "siege-model, the iron pan, the two lying postures and the rationed food as one commanded act and not as "
 "separate commands.")

G[('P01-009', 'device_notes')] = (
 "17-verse unit, one verse past the 14-16 stretch cap; disclosed rather than forced into an unsupported internal "
 "cut, as at oshb:Ezek.4.1-4.17, since no refrain-plus-fresh-onset pair stands anywhere inside 5:1-5:17 to license "
 "a shorter cut. Paseq at 5:1 and 5:7 disclosed count-only, single-witness. Marks after 5:4 (pe), 5:6, 5:7, 5:9 "
 "(samekh) and 5:10 (pe) are disclosed as intra-row, single-witness texture. An earlier ground stated here was "
 "false and is corrected: three of those five marks DO coincide with a formula onset on the verse following them. "
 "The pe after 5:4 stands before the messenger formula at oshb:Ezek.5.5, and the samekh marks after 5:6 and 5:7 "
 "stand before the messenger formulae at oshb:Ezek.5.7 and oshb:Ezek.5.8; each of those three verses is a member "
 "of the inventory's 122-verse messenger class and each carries the formula verse-initially, 5:7 and 5:8 behind "
 + LAKHEN + ". The remaining two do not: oshb:Ezek.5.10 opens on " + LAKHEN + " with no messenger formula, and "
 "oshb:Ezek.5.11 opens on the oath with the utterance signature attached mid-verse. No one of the five is read as "
 "a unit-cutting seam, but the reason is CUT-RULE and not any absence of coincidence: not one of them follows a "
 "verse that ENDS on a close-role formula, since none of 5:4, 5:6, 5:7, 5:9 or 5:10 appears in either the "
 "utterance inventory or the 64-member recognition family, and a parashah mark by itself cannot license the cut. "
 "Single witness: a pe stands after MT 4:17, the mark on record at the seam where this unit begins.")

G[('P01-009', 'strongest_rejected_alternative')] = (
 "Cutting at 5:13 or 5:15, the first two 'I Yahweh have spoken' occurrences, to shorten the unit. Rejected because "
 "neither is followed by a fresh onset device - the material after each continues the same verdict speech without "
 "a messenger formula, word-event or address restarting it - so only 5:17's occurrence is unit-final. The stronger "
 "rival, weighed here under A16, is the 5:4/5:5 seam, the division the strategy holds at \u00a77 for this chapter "
 "(the sign-act 5:1-4 set against the interpretation 5:5-17). Its near face carries a PE recorded after "
 "oshb:Ezek.5.4 and nothing further: that verse ends " + END54 + ", and it appears in neither the utterance "
 "inventory nor the 64-member recognition family, so it does not close on a close-role formula. Its far face is "
 "genuinely strong, oshb:Ezek.5.5 carrying the messenger formula " + MESS55 + " verse-initially, "
 + LD + "The Lord Yahweh says" + RD + " (web:Ezek.5.5). But CUT-RULE makes a messenger formula a sub-onset only "
 "where the addressee changes or the preceding verse has closed on a verse-final close-role formula, and neither "
 "limb holds at this seam: 5:4 addresses the prophet in the 2ms while 5:5 carries no second person at all, the "
 "shift to 2mp arriving only at 5:7 and to 2fs at 5:8; and a parashah mark cannot meet that limb by itself. The "
 "row accordingly holds the seam on those stated grounds, and the PE is recorded as corroboration of the rival "
 "and not of this unit's onset.")

# ---------------- assemble ----------------
edits = []
for (row, field), val in G.items():
    iid = IID(56 if row == 'P01-008' else 73)
    edits.append(dict(row_id=row, field=field, op='set', expected_before=rows[row][field],
                      value=val, worklist_item_ids=[iid], sweep='grounds'))

for row, lst in appends.items():
    base = rows[row]['boundary_evidence_refs']
    for i, e in lst:
        edits.append(dict(row_id=row, field='boundary_evidence_refs', op='append_ref',
                          expected_before=base, value=e, worklist_item_ids=[IID(i)],
                          sweep='a4', role_token=A4[i][0]))

for key, val in a6['newvals'].items():
    row, field = key.split('|')
    ids = [IID(i) for i in a6['touched'][key]]
    eb = rows[row][field]
    rebased = False
    if field == 'boundary_evidence_refs':
        eb = list(rows[row]['boundary_evidence_refs']) + [e for _, e in appends[row]]
        val = list(val) + [e for _, e in appends[row]]
        rebased = True
    edits.append(dict(row_id=row, field=field, op='set', expected_before=eb, value=val,
                      worklist_item_ids=ids, sweep='a6', rebased_on_a4=rebased))

print('\nTOTAL EDITS: %d   by sweep: %s' % (len(edits), dict(Counter(e['sweep'] for e in edits))))
sets = [e for e in edits if e['op'] == 'set']
print('one set-edit per (row,field): %s' %
      (len({(e['row_id'], e['field']) for e in sets}) == len(sets)))
json.dump(edits, open('edits_raw.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def grams(s, n=7):
    w = re.findall(r"[A-Za-z\u2019'\-]+", s.lower())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


orig = set()
for r in d['your_rows']:
    for f in ('boundary_rationale', 'strongest_rejected_alternative', 'device_notes'):
        orig |= grams(r[f])

print('\n7-GRAM CHECK: new grounds text vs the original prose of all 10 rows')
for (row, field), val in G.items():
    newg = grams(val) - grams(rows[row][field])
    col = newg & orig
    print('  %s/%s: new=%d collisions=%d' % (row, field, len(newg), len(col)))
    for c in sorted(col)[:8]:
        print('     !', ' '.join(c))

print('\n7-GRAM CHECK between my three new grounds texts')
ks = list(G)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        c = grams(G[ks[i]]) & grams(G[ks[j]])
        print('  %s/%s vs %s/%s : %d' % (ks[i][0], ks[i][1][:10], ks[j][0], ks[j][1][:10], len(c)))
        for x in sorted(c)[:6]:
            print('     !', ' '.join(x))

print('\n7-GRAM CHECK: the 48 A4 annotations against each other and the original prose')
seen = {}
dupe = 0
for i, (tok, txt) in A4.items():
    g = grams(txt, 7)
    if g & orig:
        print('  ! item %d collides with existing prose: %s' % (i, txt))
        dupe += 1
print('  annotations with a 7-gram in existing prose: %d (each annotation is <=6 words, so none can form a 7-gram)' % dupe)
