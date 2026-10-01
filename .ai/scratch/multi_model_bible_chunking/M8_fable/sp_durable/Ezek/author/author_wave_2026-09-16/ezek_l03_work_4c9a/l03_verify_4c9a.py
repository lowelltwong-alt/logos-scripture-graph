#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ezek_author_l03 lane verification helper (private, uniquely named).
Reads ONLY by exact path. Emits FINDINGS, never bare booleans.
"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"
P = {
 'pmarks': D + r"\pmarks_Ezek.json",
 'inv2':   D + r"\ezek_device_inventory.v2.json",
 'web':    D + r"\tools\verse_map_web.json",
 'oshb':   D + r"\tools\verse_map_oshb.json",
 'offset': D + r"\web_mt_offset_map.json",
}
pm = json.load(open(P['pmarks'], encoding='utf-8'))
iv = json.load(open(P['inv2'], encoding='utf-8'))
WM = json.load(open(P['web'], encoding='utf-8'))
OM = json.load(open(P['oshb'], encoding='utf-8'))

def mt(c, v):
    return f"Ezek.{c}.{v}"

def marks(k):
    """FINDING: returns (present?, value, note)."""
    m = pm['marks']
    if k in m:
        return ('PRESENT', m[k])
    return ('ABSENT_FROM_KEYSET', None)

def kq(k):
    d = pm['kq']
    if k in d:
        v = d[k]
        return ('PRESENT', type(v).__name__, len(v) if isinstance(v, list) else None, v)
    return ('ABSENT_FROM_KEYSET', None, None, None)

def paseq(k):
    lst = pm['paseq']
    if isinstance(lst, list):
        n = sum(1 for x in lst if x == k)
        return ('LIST', n)
    if isinstance(lst, dict):
        return ('DICT', lst.get(k, 'ABSENT'))
    return ('OTHER', None)

def notes(k):
    d = pm['notes_other']
    if isinstance(d, dict):
        return d.get(k, 'ABSENT_FROM_KEYSET')
    if isinstance(d, list):
        return [x for x in d if (isinstance(x, str) and k in x) or (isinstance(x, dict) and x.get('verse') == k)]
    return None

def cmd_struct():
    for nm in ('paseq', 'kq', 'notes_other', 'marks'):
        o = pm[nm]
        print(f"pmarks[{nm}] type={type(o).__name__} len={len(o)}")
        if isinstance(o, dict):
            k0 = list(o)[0]
            print(f"   first key={k0!r} value={json.dumps(o[k0], ensure_ascii=False)[:220]}")
        else:
            print(f"   first items={json.dumps(o[:3], ensure_ascii=False)[:300]}")
    print("verse_map_web type=", type(WM).__name__, "len=", len(WM))
    k = list(WM)[:3] if isinstance(WM, dict) else None
    print("  web sample keys:", k)
    if k:
        print("  web sample val:", json.dumps(WM[k[0]], ensure_ascii=False)[:300])
    print("verse_map_oshb type=", type(OM).__name__, "len=", len(OM))
    k2 = list(OM)[:3] if isinstance(OM, dict) else None
    print("  oshb sample keys:", k2)
    if k2:
        print("  oshb sample val:", json.dumps(OM[k2[0]], ensure_ascii=False)[:300])

def cmd_verses(args):
    """report marks/kq/paseq/notes for each MT verse key given"""
    for k in args:
        print(f"--- {k}")
        print("   marks :", marks(k))
        print("   kq    :", json.dumps(kq(k), ensure_ascii=False))
        print("   paseq :", paseq(k))
        n = notes(k)
        print("   notes :", json.dumps(n, ensure_ascii=False)[:600])

def cmd_inv(args):
    """list membership for MT verse keys across every list in the inventory"""
    lists = {}
    def collect(o, path):
        if isinstance(o, dict):
            for kk, vv in o.items():
                if kk in ('verses_mt', 'verses_dual_written_in_the_zone', 'strategy_list',
                          'verses_the_predicate_adds') and isinstance(vv, list):
                    lists[path + '.' + kk] = vv
                elif isinstance(vv, (dict, list)):
                    collect(vv, path + '.' + kk)
        elif isinstance(o, list):
            for i, vv in enumerate(o):
                if isinstance(vv, (dict, list)):
                    collect(vv, path + f'[{i}]')
    collect(iv, '')
    for k in args:
        hits = sorted(nm for nm, l in lists.items() if k in l and 'dual_written' not in nm)
        print(f"{k}: " + (", ".join(hits) if hits else "IN NO INVENTORY verses_mt LIST"))

def cmd_webtext(args):
    for k in args:
        val = WM.get(k, 'ABSENT_FROM_KEYSET')
        print(f"--- {k}")
        print(json.dumps(val, ensure_ascii=False)[:1400])

def cmd_oshbtext(args):
    for k in args:
        val = OM.get(k, 'ABSENT_FROM_KEYSET')
        print(f"--- {k}")
        print(json.dumps(val, ensure_ascii=False)[:1400])

def _norm(s):
    import re
    s = s.lower()
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = re.sub(r"[^a-z0-9' ]+", ' ', s)
    s = re.sub(r"'", '', s)
    return re.sub(r'\s+', ' ', s).strip()

def _wtext(entry):
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        for kk in ('text', 'web', 'verse', 'value', 't'):
            if kk in entry and isinstance(entry[kk], str):
                return entry[kk]
        return json.dumps(entry, ensure_ascii=False)
    return str(entry)

def cmd_runscan(args):
    """args: the run (one quoted string). Reports EVERY WEB verse in Ezek whose
    normalised word sequence contains the run's normalised word sequence."""
    run = _norm(args[0])
    rw = run.split()
    hits = []
    for k, entry in WM.items():
        if not k.startswith('Ezek.'):
            continue
        w = _norm(_wtext(entry)).split()
        for i in range(0, max(0, len(w) - len(rw) + 1)):
            if w[i:i + len(rw)] == rw:
                hits.append(k)
                break
    print(f"RUN={args[0]!r} words={len(rw)}")
    print(f"WEB verses containing it: {len(hits)} -> {hits}")

if __name__ == '__main__':
    c = sys.argv[1]
    a = sys.argv[2:]
    {'struct': lambda: cmd_struct(), 'verses': lambda: cmd_verses(a), 'inv': lambda: cmd_inv(a),
     'webtext': lambda: cmd_webtext(a), 'oshbtext': lambda: cmd_oshbtext(a),
     'runscan': lambda: cmd_runscan(a)}[c]()
