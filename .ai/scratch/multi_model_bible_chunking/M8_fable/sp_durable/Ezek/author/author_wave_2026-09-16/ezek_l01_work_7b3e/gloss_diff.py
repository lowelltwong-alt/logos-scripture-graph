import json,re
LANE=r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
WEBP=r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json'
d=json.load(open(LANE,encoding='utf-8')); web=json.load(open(WEBP,encoding='utf-8'))
rows={r['decision_id']:r for r in d['your_rows']}; items=d['your_worklist_items']
WORD=re.compile(r"[A-Za-z][A-Za-z\u2019'\-]*")
def tl(s): return [m.group(0).rstrip("\u2019'-").replace('\u2019',"'").lower() for m in WORD.finditer(s)]
INSTALL={1,3,4,9,10,15,16,17,18,19,27,28,29,32,33,37,38,39,40,45,46,47,48,57,58,75,77,79}
for i in sorted(INSTALL):
    it=items[i]
    fld='boundary_evidence_refs' if it['field']=='refs' else it['field']
    tgt=rows[it['row_id']][fld]
    texts=tgt if isinstance(tgt,list) else [tgt]
    # the verse the gloss belongs to: prefer the in-span web_ref, else first
    for s in texts:
        # find single-quoted glosses containing the run's first word
        for m in re.finditer(r"'([^']{5,200})'", s):
            g=m.group(1)
            if it['run'].split()[0] in tl(g) and all(w in tl(g) for w in it['run'].split()[:3]):
                for vref in it['web_refs']:
                    wt=web[vref]['text']
                    gt=tl(g); wtl=tl(wt)
                    # is the gloss token sequence a contiguous subsequence of the WEB verse?
                    exact=any(wtl[k:k+len(gt)]==gt for k in range(max(0,len(wtl)-len(gt)+1)))
                    print(f"item {i:02d} {it['row_id']} {vref}: gloss_is_WEB_exact={exact}")
                    print(f"    GLOSS: {g!r}")
                    if not exact: print(f"    WEB  : {wt[:190]!r}")
