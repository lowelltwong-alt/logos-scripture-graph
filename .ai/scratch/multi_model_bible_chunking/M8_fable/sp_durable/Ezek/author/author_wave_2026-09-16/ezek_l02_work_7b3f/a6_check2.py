import json, re
B = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_02_worklist.json'
web = json.load(open(B + r'\tools\verse_map_web.json', encoding='utf-8'))
lane = json.load(open(LANE, encoding='utf-8'))

def norm(s):
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c','"').replace('\u201d','"')
    s = re.sub(r'\[fn\]', ' ', s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9' ]", ' ', s)
    # drop apostrophes acting as quotation marks (not between two letters)
    s = re.sub(r"(?<![a-z])'", ' ', s)
    s = re.sub(r"'(?![a-z])", ' ', s)
    s = re.sub(r"\s+", ' ', s).strip()
    return s

NORM = {k: norm(v.get('clean') or v['text']) for k, v in web.items()}
def kk(k):
    p = k.split('.'); return (int(p[1]), int(p[2]))
ORD = sorted(NORM, key=kk)
rows = {r['decision_id']: r for r in lane['your_rows']}

def span_verses(span):
    a, b = span.split('-')
    c1, v1 = int(a.split('.')[1]), int(a.split('.')[2])
    c2, v2 = int(b.split('.')[1]), int(b.split('.')[2])
    out = []
    for k in ORD:
        c, v = kk(k)
        if (c, v) >= (c1, v1) and (c, v) <= (c2, v2): out.append(k)
    return out

items = lane['your_worklist_items']
for i, it in enumerate(items):
    if it['cls'] not in ('A6','A6_UNION'): continue
    r = norm(it['run'])
    hits = [k for k in ORD if (' '+r+' ') in (' '+NORM[k]+' ')]
    row = rows[it['row_id']]
    sv = set(span_verses(row['span']))
    inspan = [h for h in hits if h in sv]
    print(f"I{i:02d} {it['row_id']} span={row['span']} field={it.get('field')} w={it.get('words')} {it.get('kind')} fr={it.get('formula_rendering')}")
    print(f"    run_norm: {r!r}  (words={len(r.split())})")
    print(f"    cited={it.get('web_refs')}  hits={len(hits)}: {hits if len(hits)<=8 else hits[:8]+['...']}")
    print(f"    hits_inside_this_span={inspan}")
