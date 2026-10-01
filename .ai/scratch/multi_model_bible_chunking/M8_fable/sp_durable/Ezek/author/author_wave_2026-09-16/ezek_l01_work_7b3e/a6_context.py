import json,re
LANE=r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
d=json.load(open(LANE,encoding='utf-8'))
rows={r['decision_id']:r for r in d['your_rows']}
items=d['your_worklist_items']
WORD=re.compile(r"[A-Za-z][A-Za-z\u2019'\-]*")
def toks(s):
    out=[]
    for m in WORD.finditer(s):
        t=m.group(0).rstrip("\u2019'-").replace('\u2019',"'")
        out.append((t.lower(),m.start(),m.start()+len(t)))
    return out
for i,it in enumerate(items):
    if it['cls']!='A6': continue
    fld='boundary_evidence_refs' if it['field']=='refs' else it['field']
    tgt=rows[it['row_id']][fld]
    texts=[('list[%d]'%n,x) for n,x in enumerate(tgt)] if isinstance(tgt,list) else [('',tgt)]
    rw=[w.replace('\u2019',"'") for w in it['run'].split()]; n=len(rw)
    print(f'--- item {i:02d} {it["row_id"]} {it["field"]} kind={it["kind"]} run={it["run"]!r}')
    found=False
    for tag,s in texts:
        tk=toks(s); tl=[t[0] for t in tk]
        for j in range(len(tl)-n+1):
            if tl[j:j+n]==rw:
                found=True
                a,b=tk[j][1],tk[j+n-1][2]
                print(f'    {tag} CTX: ...{s[max(0,a-55):a]}[[{s[a:b]}]]{s[b:b+55]}...')
    if not found: print('    *** RUN NOT PRESENT IN THE ROW FIELD ***')
