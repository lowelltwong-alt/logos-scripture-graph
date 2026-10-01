import json,re,unicodedata as ud
B=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"
osh={}
for l in open(B+r"\Ezek_oshb.txt",encoding='utf-8'):
    l=l.rstrip('\n')
    if l.strip():
        k,_,t=l.partition('\t'); osh[k]=t
pm=json.load(open(B+r"\pmarks_Ezek.json",encoding='utf-8'))
def cons(s):  # strip EVERY combining mark (Mn) and maqaf/meteg etc.
    return ''.join(c for c in ud.normalize('NFD',s) if ud.category(c)!='Mn')
o=open('fix_measured.txt','w',encoding='utf-8')
o.write("=== (6 REDONE) verses 40:5-41:5 whose consonantal text contains the root string ימד ===\n")
hits=[]
order=[f"Ezek.40.{i}" for i in range(5,50)]+[f"Ezek.41.{i}" for i in range(1,6)]
present=[v for v in order if v in osh]
o.write(f"  verses present in the pinned witness for 40:5-41:5: n={len(present)} (40:5-40:{max(int(v.split('.')[2]) for v in present if v.startswith('Ezek.40.'))}, 41:1-41:5)\n")
for v in present:
    c=cons(osh[v])
    n=len(re.findall('ימד',c))
    if n: hits.append((v,n))
o.write(f"  verses containing ימד: n={len(hits)}; total occurrences={sum(n for _,n in hits)}\n")
o.write(f"  {[v for v,_ in hits]}\n")
o.write(f"  per-verse counts: {hits}\n")
o.write(f"  40:5 consonantal: {cons(osh['Ezek.40.5'])}\n")
o.write("\n=== marks at Ezek.30.21 / 30.20 (P07-005 device_notes claim) ===\n")
for v in ['Ezek.30.20','Ezek.30.21','Ezek.30.22','Ezek.30.23','Ezek.30.24','Ezek.30.25','Ezek.30.26']:
    o.write(f"  marks[{v}] = {json.dumps(pm['marks'].get(v,'<<NONE>>'),ensure_ascii=False)}\n")
o.write("\n=== kq running-text confirmation: 33.13 / 33.16 ketiv appear unpointed in the running text ===\n")
for v,k in [('Ezek.33.13','צדקתו'),('Ezek.33.16','חטאתו')]:
    o.write(f"  {v}: ketiv string {k!r} present in running text = {k in osh[v]}\n")
o.write("\n=== 33.11 utterance formula position (CUT-RULE limb b test) ===\n")
ws=osh['Ezek.33.11'].split()
o.write(f"  33.11 has {len(ws)} words; final word = {ws[-1]}\n")
ne=[i for i,w in enumerate(ws) if cons(w)=='נאם']
o.write(f"  'נאם' word index(es) = {ne}  -> formula is mid-verse (not the final words) = {bool(ne) and ne[-1] < len(ws)-3}\n")
o.write(f"  words after the divine-name pair: {' '.join(ws[ne[0]+3:]) if ne else '-'}\n")
o.close(); print(open('fix_measured.txt',encoding='utf-8').read())
