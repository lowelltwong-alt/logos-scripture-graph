import json,re
WEB=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json"
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
w=json.load(open(WEB,encoding='utf-8')); lane=json.load(open(LANE,encoding='utf-8'))
rows={r['decision_id']:r for r in lane['your_rows']}; items=lane['your_worklist_items']
def norm(s):
    s=s.lower().replace('\u2019',"'").replace('\ufffd',"'").replace('\u201c','"').replace('\u201d','"')
    s=re.sub(r"\[fn\]"," ",s); s=re.sub(r"[^a-z' ]"," ",s)
    return " "+re.sub(r"\s+"," ",s).strip()+" "
o=open('infield_measured.txt','w',encoding='utf-8')
FIELDMAP={'refs':'boundary_evidence_refs'}
for idx,it in enumerate(items):
    if it['cls'] not in ('A6','A6_UNION'): continue
    rid=it['row_id']; run=it['run']; r=rows[rid]
    fname=FIELDMAP.get(it.get('field','-'),it.get('field','-'))
    o.write(f"--- l05_i{idx:02d} {rid} field={fname} run={run!r}\n")
    nr=" "+norm(run).strip()+" "
    targets = [(fname, r[fname])] if fname in r else [(k,r[k]) for k in ('boundary_rationale','strongest_rejected_alternative','device_notes','boundary_evidence_refs')]
    for k,val in targets:
        if isinstance(val,list):
            for i2,e in enumerate(val):
                if nr in norm(e): o.write(f"    PRESENT in {k}[{i2}]: {e}\n")
        else:
            if nr in norm(val):
                # show raw context window around a loose match
                o.write(f"    PRESENT in {k}\n")
                # find raw context by locating first word
                fw=run.split()[0]
                for m in re.finditer(re.escape(fw), val, re.I):
                    seg=val[max(0,m.start()-90):m.start()+len(run)+110]
                    if nr.strip().split()[-1] in norm(seg): o.write(f"      ctx: ...{seg}...\n")
            else:
                o.write(f"    ABSENT from {k}\n")
    o.write("\n")
o.write("\n\n=========== WEB verse texts (clean) ===========\n")
for v in ['Ezek.35.12','Ezek.35.3','Ezek.35.4','Ezek.35.9','Ezek.26.3','Ezek.13.8','Ezek.21.3','Ezek.38.3','Ezek.39.1','Ezek.37.14','Ezek.6.7','Ezek.39.21','Ezek.39.22','Ezek.39.23','Ezek.39.24','Ezek.39.29','Ezek.36.28','Ezek.36.32','Ezek.36.22','Ezek.33.2','Ezek.33.29','Ezek.32.18','Ezek.37.20','Ezek.37.3','Ezek.39.11','Ezek.39.14','Ezek.40.1','Ezek.40.2','Ezek.40.4','Ezek.36.1','Ezek.36.25','Ezek.33.20','Ezek.33.17','Ezek.36.23','Ezek.8.3']:
    e=w.get(v)
    o.write(f"{v}: mt={e.get('mt')}\n   {e.get('clean')}\n")
o.close(); print('ok')
