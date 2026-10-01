import json,re,unicodedata
LANE=r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
WEB=r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json'
items=json.load(open(LANE,encoding='utf-8'))['your_worklist_items']
web=json.load(open(WEB,encoding='utf-8'))

def norm_tokens(s):
    s=unicodedata.normalize('NFKD',s)
    s=s.replace('\u2019',"'").replace('\u2018',"'").replace('\u201c','"').replace('\u201d','"')
    s=re.sub(r'\[fn\]','',s)
    toks=re.findall(r"[A-Za-z']+(?:-[A-Za-z']+)*",s.lower())
    return toks

def locate(runwords, text):
    """return exact substring of text spanning the token run, or None"""
    s=re.sub(r'\[fn\]','',text)
    s2=s.replace('\u2019',"'").replace('\u2018',"'")
    toks=[(m.group(0).lower(),m.start(),m.end()) for m in re.finditer(r"[A-Za-z\u2019']+(?:-[A-Za-z\u2019']+)*",s2)]
    tl=[t[0].replace('\u2019',"'") for t in toks]
    n=len(runwords)
    hits=[]
    for i in range(len(tl)-n+1):
        if tl[i:i+n]==runwords:
            hits.append(s[toks[i][1]:toks[i+n-1][2]])
    return hits

print('idx row field words | verse | EXACT WEB SUBSTRING (hits) | run')
for i,it in enumerate(items):
    if it['cls']!='A6': continue
    rw=it['run'].split()
    # the primary verse for an in-span install is web_refs[0] when in_span
    for vref in it['web_refs']:
        e=web.get(vref)
        if e is None:
            print(f"{i:02d} {it['row_id']} {vref} <<MISSING VERSE>>"); continue
        hits=locate([w.replace('\u2019',"'") for w in rw], e['text'])
        print(f"{i:02d} {it['row_id']:8s} {it['field'][:18]:18s} w={it['words']:2d} in_span={str(it['in_span']):5s} | {vref:12s} | hits={len(hits)} {hits!r}")
    print(f"     run={it['run']!r}")
