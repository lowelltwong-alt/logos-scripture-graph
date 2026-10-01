#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A6 run locator for lane ezek_author_l03.
For every A6 / A6_UNION worklist item, searches EVERY string field of the row
for the item's run (normalised word sequence) and reports WHERE it was found,
plus whether that field already carries curly double quotes and a web: ref.
Reports findings, not booleans.
"""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LANE = (r"C:\Users\lowel\AppData\Local\Temp\claude"
        r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
        r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_03_worklist.json")
d = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in d['your_rows']}
ITEMS = d['your_worklist_items']

def norm(s):
    s = s.lower()
    for a, b in (('\u2019', "'"), ('\u2018', "'"), ('\u201c', '"'), ('\u201d', '"')):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9' ]+", ' ', s)
    s = s.replace("'", '')
    return re.sub(r'\s+', ' ', s).strip()

def field_strings(row):
    out = []
    for k, v in row.items():
        if isinstance(v, str):
            out.append((k, v))
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, str):
                    out.append((f"{k}[{i}]", x))
    return out

for n, it in enumerate(ITEMS):
    if it['cls'] not in ('A6', 'A6_UNION'):
        continue
    row = ROWS[it['row_id']]
    rw = norm(it['run']).split()
    print("=" * 76)
    print(f"idx {n:02d}  {it['row_id']}  {it['cls']}  kind={it.get('kind')}  "
          f"declared_field={it.get('field','-')}  in_span={it.get('in_span','-')}")
    print(f"   run({len(rw)}w) = {it['run']!r}")
    found = []
    for fname, text in field_strings(row):
        w = norm(text).split()
        for i in range(0, max(0, len(w) - len(rw) + 1)):
            if w[i:i + len(rw)] == rw:
                found.append(fname)
                break
    if not found:
        print("   FOUND: the run occurs in NO field of this row (0 field hits)")
    else:
        print(f"   FOUND in {len(found)} field(s): {found}")
        for fname in found:
            txt = dict(field_strings(row))[fname]
            has_curly = ('\u201c' in txt and '\u201d' in txt)
            webrefs = re.findall(r'web:Ezek\.\d+\.\d+', txt)
            print(f"      {fname}: curly_double_quotes={has_curly} "
                  f"web_refs_in_field={sorted(set(webrefs)) or 'NONE'}")
