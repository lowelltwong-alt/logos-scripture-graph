# -*- coding: utf-8 -*-
import json, hashlib

W = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l01_work_7b3e'
DELIV = W + r'\ezek_author_l01_deliverable.json'
FINAL = W + r'\ezek_author_l01_final_message.json'
o = json.load(open(DELIV, encoding='utf-8'))

o['verification_evidence'].append(
 "A6 CONVENTION, tested per item rather than by counting - audit_a6.py locates each installed run inside the NEW "
 "field value and checks that it sits between a double curly open and close with the right (web:Ezek.C.V) within 40 "
 "characters of the close. All 27 installs compliant. Recording a false alarm from my own first audit, which "
 "expected one added delimiter per item and flagged P01-002: the cause was that item l01#03's original text already "
 "carried a (web:Ezek.2.1) reference and an embedded WEB double-curly pair, so my repair re-nested the inner pair to "
 "single curly and promoted the outer single quotes to double, a net change of zero in the count while the "
 "convention went from unmet to met. The count heuristic was wrong; the edit was not.")
o['verification_evidence'].append(
 "FULL DELIVERABLE AUDIT - audit.py re-loads the written file from disk and checks 33 properties. All pass except "
 "the one count heuristic described above, which audit_a6.py then superseded. Confirmed among them: no edit touches "
 "span, osis_start, osis_end, decision_id, any writer-identity field or confidence; every edit's field is in the "
 "allowed set; each edit's items belong to that edit's row AND to that edit's sweep class; every range citation got "
 "a range entry and no per-verse expansion; no worklist item in my lane has moves_seam true; and all 84 ids fall in "
 "exactly one of the two accounting lists.")
o['verification_evidence'].append(
 "ONE STYLISTIC NOTE, so it is not read as an inconsistency: the install for l01#09 reads "
 "(WEB [open]But you, son of man, hear[close] (web:Ezek.2.8)). It carries the explicit word WEB because it is one "
 "of the two places where I replaced the row's own gloss with materially different WEB wording (the row had 'and', "
 "the WEB has 'But'), and naming the witness there prevents the reader taking the WEB's wording for the row's "
 "rendering of the Hebrew. The other 26 installs carry the witness through the web: prefix alone, as the rows "
 "already do at P01-001's Ezek.1.28 quotation.")

json.dump(o, open(DELIV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# final message = the same JSON the brief asks me to return, plus the digests
fm = dict(o)
json.dump(fm, open(FINAL, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 16), b''):
            h.update(b)
    return h.hexdigest()


d1, d2 = sha(DELIV), sha(FINAL)
print('deliverable   sha256 =', d1)
print('final_message sha256 =', d2)
print('edits=%d discharged=%d not_discharged=%d escalations=%d no_edit_rulings=%d'
      % (len(o['edits']), len(o['items_discharged']), len(o['items_NOT_discharged']),
         len(o['escalations']), len(o['items_discharged_without_edit'])))
print('verification_evidence entries =', len(o['verification_evidence']))
open(W + r'\DIGESTS.txt', 'w', encoding='utf-8').write(
    'ezek_author_l01_deliverable.json %s\nezek_author_l01_final_message.json %s\n' % (d1, d2))
