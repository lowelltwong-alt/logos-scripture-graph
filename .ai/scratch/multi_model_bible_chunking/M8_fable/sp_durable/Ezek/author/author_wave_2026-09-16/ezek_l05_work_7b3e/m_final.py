import json,re,unicodedata as ud
B=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"
osh={}
for l in open(B+r"\Ezek_oshb.txt",encoding='utf-8'):
    l=l.rstrip('\n')
    if l.strip():
        k,_,t=l.partition('\t'); osh[k]=t
pm=json.load(open(B+r"\pmarks_Ezek.json",encoding='utf-8'))
web=json.load(open(B+r"\tools\verse_map_web.json",encoding='utf-8'))
off=json.load(open(B+r"\web_mt_offset_map.json",encoding='utf-8'))
o=open('final_measured.txt','w',encoding='utf-8')

o.write("=== web_mt_offset_map.json (FULL) ===\n")
o.write(json.dumps(off,ensure_ascii=False,indent=1)+"\n\n")

o.write("=== (1) marks at Ezek.37.10 / 37.12 (P09-001 SRA claim) ===\n")
for i in range(1,15):
    v=f"Ezek.37.{i}"
    o.write(f"  marks[{v}] = {json.dumps(pm['marks'].get(v,'<<NONE>>'),ensure_ascii=False)}\n")

ET='\u0591'; MET='\u05BD'
def split_at_etnachta(v):
    t=osh[v]; ws=t.split()
    idx=[i for i,w in enumerate(ws) if ET in w]
    return ws,idx
o.write("\n=== (2) accent structure: 33.29, 36.32, 36.23, 33.20 ===\n")
for v in ['Ezek.33.29','Ezek.36.32','Ezek.36.23','Ezek.32.32','Ezek.36.38']:
    ws,idx=split_at_etnachta(v)
    o.write(f"  {v}: {osh[v]}\n")
    o.write(f"    etnachta word index {idx} -> a-half: {' '.join(ws[:idx[0]+1]) if idx else '(none)'}\n")
    o.write(f"    b-half: {' '.join(ws[idx[0]+1:]) if idx else '(none)'}\n")
    o.write(f"    final word: {ws[-1]}  has_U05BD={MET in ws[-1]}\n")

o.write("\n=== (3) 33.10 vs 33.12 addressee (CUT-RULE limb a) ===\n")
for v in ['Ezek.33.10','Ezek.33.11','Ezek.33.12','Ezek.33.13','Ezek.33.16']:
    o.write(f"  {v}: {osh[v]}\n")
    o.write(f"     WEB: {web[v]['clean']}\n")

o.write("\n=== (4) MT==WEB identity for every verse I will cite ===\n")
cite=['Ezek.30.19','Ezek.30.26','Ezek.31.1','Ezek.31.18','Ezek.32.1','Ezek.32.8','Ezek.32.9','Ezek.32.16','Ezek.32.17','Ezek.32.18','Ezek.32.19','Ezek.32.21','Ezek.33.7','Ezek.33.13','Ezek.33.16','Ezek.33.23','Ezek.33.24','Ezek.33.26','Ezek.33.28','Ezek.33.29','Ezek.34.1','Ezek.35.3','Ezek.35.12','Ezek.36.1','Ezek.36.12','Ezek.36.13','Ezek.36.14','Ezek.36.20','Ezek.36.22','Ezek.36.25','Ezek.36.28','Ezek.36.32','Ezek.36.38','Ezek.37.1','Ezek.37.2','Ezek.37.3','Ezek.37.10','Ezek.37.12','Ezek.37.14','Ezek.37.16','Ezek.37.20','Ezek.37.22','Ezek.38.3','Ezek.39.1','Ezek.39.11','Ezek.39.12','Ezek.39.14','Ezek.39.16','Ezek.39.21','Ezek.39.22','Ezek.39.23','Ezek.39.24','Ezek.39.25','Ezek.39.29','Ezek.40.1','Ezek.40.2','Ezek.40.4','Ezek.40.5','Ezek.41.5','Ezek.8.3']
bad=[(v,web[v]['mt']) for v in cite if web[v]['mt']!=v]
o.write(f"  checked {len(cite)} refs; NON-IDENTITY cases: {bad if bad else 'NONE (every cited ref has mt == web key)'}\n")

o.write("\n=== (5) v2 inventory: the 21-verse 2mp set; is 37.14 a member? ===\n")
inv=json.load(open(B+r"\ezek_device_inventory.v2.json",encoding='utf-8'))
def find(o2,path=''):
    if isinstance(o2,dict):
        for k,v in o2.items():
            yield from find(v,path+'/'+k)
    elif isinstance(o2,list):
        if o2 and isinstance(o2[0],str) and o2[0].startswith('Ezek.'): yield (path,o2)
hits=[(p,l) for p,l in find(inv) if len(l)==21]
for p,l in hits: o.write(f"  21-member list at {p}: 37.14 in list = {'Ezek.37.14' in l}\n    {l}\n")
o.write(f"  top keys of v2: {list(inv.keys())}\n")

o.write("\n=== (6) the vayyamod run 40:5-41:5 (row claims 'eighteen-verse run') ===\n")
vm=[]
for ch,lo,hi in [(40,5,49),(41,1,5)]:
    for i in range(lo,hi+1):
        v=f"Ezek.{ch}.{i}"
        if v in osh and re.search(r'\u05d9\u05de\u05d3',osh[v].replace('\u05b8','').replace('\u05bc','').replace('\u0591','')):
            vm.append(v)
o.write(f"  verses in 40:5-41:5 whose consonants contain ימד (loose, diacritic-stripped): n={len(vm)}\n  {vm}\n")

o.write("\n=== (7) WEB 39.25 ===\n")
o.write("  "+web['Ezek.39.25']['clean']+"\n")
o.close(); print('ok')
