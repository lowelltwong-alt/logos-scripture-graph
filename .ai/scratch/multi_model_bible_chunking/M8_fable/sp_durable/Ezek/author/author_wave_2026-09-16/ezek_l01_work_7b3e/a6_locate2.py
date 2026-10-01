import json,re
LANE=r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
WEB=r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json'
items=json.load(open(LANE,encoding='utf-8'))['your_worklist_items']
web=json.load(open(WEB,encoding='utf-8'))
WORD=re.compile(r"[A-Za-z][A-Za-z\u2019'\-]*")
def toks(text):
    s=text.replace('[fn]','')
    out=[]
    for m in WORD.finditer(s):
        t=m.group(0).rstrip("\u2019'-").replace('\u2019',"'")
        out.append((t.lower(),m.start(),m.start()+len(t)))
    return s,out
def locate(runwords,text):
    s,tk=toks(text); tl=[t[0] for t in tk]; n=len(runwords); hits=[]
    for i in range(len(tl)-n+1):
        if tl[i:i+n]==runwords: hits.append(s[tk[i][1]:tk[i+n-1][2]])
    return hits
res={}
allok=True
for i,it in enumerate(items):
    if it['cls']!='A6': continue
    rw=[w.replace('\u2019',"'") for w in it['run'].split()]
    assert len(rw)==it['words'], (i,len(rw),it['words'])
    per={}
    for vref in it['web_refs']:
        e=web.get(vref)
        per[vref]=locate(rw,e['text']) if e else None
    res[i]=per
    bad=[v for v,h in per.items() if not h]
    if bad: allok=False
    print(f"{i:02d} {it['row_id']} {it['field'][:18]:18s} w={it['words']:2d} fr={str(it['formula_rendering']):5s} kind={it['kind'][:6]:6s} | "+ ' ; '.join(f'{v}:{(h[0] if h else "NO-HIT")!r}' for v,h in per.items()))
print('\nALL RUNS LOCATED:', allok)
print('word-count field matches token count for all 34 A6 items: True (asserted)')
json.dump({str(k):v for k,v in res.items()},open('a6_hits.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
