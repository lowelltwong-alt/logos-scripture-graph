import json, re, sys
B = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_02_worklist.json'
web = json.load(open(B + r'\tools\verse_map_web.json', encoding='utf-8'))
lane = json.load(open(LANE, encoding='utf-8'))

def norm(s):
    s = s.replace('\u2019', "'").replace('\u201c','"').replace('\u201d','"')
    s = re.sub(r'\[fn\]', ' ', s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9' ]", ' ', s)
    s = re.sub(r"\s+", ' ', s).strip()
    return s

NORM = {k: norm(v.get('clean') or v['text']) for k, v in web.items()}
def key(k):
    p = k.split('.'); return (int(p[1]), int(p[2]))
ORD = sorted(NORM, key=key)

def find_run(run):
    r = norm(run)
    hits = [k for k in ORD if (' '+r+' ') in (' '+NORM[k]+' ')]
    return r, hits

items = lane['your_worklist_items']
for i, it in enumerate(items):
    if it['cls'] not in ('A6','A6_UNION'): continue
    run = it['run']
    r, hits = find_run(run)
    print(f"I{i:02d} {it['row_id']} {it['cls']} field={it.get('field')} words={it.get('words')} kind={it.get('kind')}")
    print(f"    run_norm: {r!r}")
    print(f"    cited web_refs: {it.get('web_refs')}")
    print(f"    MEASURED hits in WEB ({len(hits)}): {hits}")
