# -*- coding: utf-8 -*-
# Proper A6 convention test: for each install item, is its run now enclosed in double curly
# quotes, with an in-field web: reference to the right verse immediately after the close?
import json, re
W = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l01_work_7b3e'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
d = json.load(open(LANE, encoding='utf-8'))
items = d['your_worklist_items']
o = json.load(open(W + r'\ezek_author_l01_deliverable.json', encoding='utf-8'))
LD, RD = '\u201c', '\u201d'
WORD = re.compile(r"[A-Za-z][A-Za-z\u2019'\-]*")

# the verse each install references (chosen by me = the verse the row cites there)
VERSE = {1: '1.8', 3: '2.1', 4: '2.3', 9: '2.8', 10: '2.9', 16: '3.7', 17: '3.9', 18: '3.10',
         19: '3.11', 27: '3.12', 28: '3.15', 29: '3.16', 32: '3.16', 33: '3.17', 37: '3.22',
         38: '3.22', 39: '3.27', 40: '3.16', 45: '4.1', 46: '4.8', 47: '4.16', 48: '4.17',
         57: '5.1', 58: '5.14', 75: '6.2', 77: '6.8', 79: '6.8'}

newval = {}
for e in o['edits']:
    if e['sweep'] == 'a6':
        newval[(e['row_id'], e['field'])] = (e['value'], e['worklist_item_ids'])

bad = []
n = 0
for (row, field), (val, ids) in sorted(newval.items()):
    texts = val if isinstance(val, list) else [val]
    for iid in ids:
        idx = int(iid.split('#')[1])
        it = items[idx]
        # the run as installed may be the WEB's exact wording, which can differ from the
        # detector's run for the three corrected paraphrases; test the run's own tokens where
        # they survive, else the corrected WEB tokens.
        cands = [it['run'].split()]
        if idx == 9:
            cands.append('but you son of man hear'.split())
        if idx == 10:
            cands.append('behold a hand was stretched out to me'.split())
        ok = False
        detail = ''
        for s in texts:
            tk = [(m.group(0).rstrip("\u2019'-").replace('\u2019', "'").lower(), m.start(), m.end())
                  for m in WORD.finditer(s)]
            tl = [t[0] for t in tk]
            for rw in cands:
                rw = [w.replace('\u2019', "'") for w in rw]
                for j in range(len(tl) - len(rw) + 1):
                    if tl[j:j + len(rw)] != rw:
                        continue
                    a, b = tk[j][1], tk[j + len(rw) - 1][2]
                    pre, post = s[:a], s[b:]
                    # nearest preceding opening curly, not already closed
                    lo = pre.rfind(LD)
                    closed_between = lo != -1 and RD in pre[lo:]
                    hi = post.find(RD)
                    if lo == -1 or closed_between or hi == -1:
                        detail = 'delimiter missing'
                        continue
                    tail = post[hi:hi + 40]
                    want = '(web:Ezek.%s)' % VERSE[idx]
                    if want in tail:
                        ok = True
                        detail = want
                        break
                    detail = 'ref %s not within 40 chars of close; saw %r' % (want, tail[:40])
                if ok:
                    break
            if ok:
                break
        n += 1
        print('%-8s %-6s %-30s %s  %s' % (iid, row, field[:30], 'OK ' if ok else 'BAD', detail))
        if not ok:
            bad.append((iid, row, field, detail))

print('\n%d install items tested; compliant=%d; non-compliant=%d' % (n, n - len(bad), len(bad)))
for b in bad:
    print('  BAD', b)
print('\nVERDICT:', 'ALL 27 A6 INSTALLS SATISFY THE CONVENTION' if not bad else 'NON-COMPLIANT INSTALLS PRESENT')
