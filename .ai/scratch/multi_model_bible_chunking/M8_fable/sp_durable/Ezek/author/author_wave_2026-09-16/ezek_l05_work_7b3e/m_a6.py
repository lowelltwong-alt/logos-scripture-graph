import json,re
WEB=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json"
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
w=json.load(open(WEB,encoding='utf-8'))
lane=json.load(open(LANE,encoding='utf-8'))
rows={r['decision_id']:r for r in lane['your_rows']}
items=lane['your_worklist_items']
def norm(s):
    s=s.lower().replace('\u2019',"'").replace('\ufffd',"'")
    s=re.sub(r"\[fn\]"," ",s)
    s=re.sub(r"[^a-z' ]"," ",s)
    return " "+re.sub(r"\s+"," ",s).strip()+" "
NV={k:norm(v.get('clean') or v.get('text','')) for k,v in w.items()}
def vkey(k):
    p=k.split('.'); return (int(p[1]),int(p[2]))
def occurrences(run):
    r=" "+norm(run).strip()+" "
    return [k for k in sorted(NV,key=vkey) if r in NV[k]]
o=open('a6_measured.txt','w',encoding='utf-8')
seen=set()
for idx,it in enumerate(items):
    if it['cls'] not in ('A6','A6_UNION'): continue
    run=it['run']; rid=it['row_id']
    span=rows[rid]['span']; a,b=span.split('-')
    ca,va=int(a.split('.')[1]),int(a.split('.')[2]); cb,vb=int(b.split('.')[1]),int(b.split('.')[2])
    occ=occurrences(run)
    inspan=[k for k in occ if (ca,va)<=vkey(k)<=(cb,vb)]
    o.write(f"--- l05_i{idx:02d} {rid} span={span} cls={it['cls']} kind={it['kind']} field={it.get('field','-')}\n")
    o.write(f"    run={run!r}  words_declared={it.get('words','n/a')} words_counted={len(run.split())}\n")
    o.write(f"    declared web_refs={it.get('web_refs','n/a')}\n")
    o.write(f"    MEASURED occurrences in WEB Ezek ({len(occ)}): {occ}\n")
    o.write(f"    in-span occurrences ({len(inspan)}): {inspan}\n")
    if 'web_refs' in it:
        for r2 in it['web_refs']:
            o.write(f"      cited {r2}: run_present={r2 in occ}\n")
    o.write("\n")
o.close(); print('ok')
