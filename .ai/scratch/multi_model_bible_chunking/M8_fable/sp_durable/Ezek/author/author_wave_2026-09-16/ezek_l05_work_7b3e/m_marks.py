import json
P=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\pmarks_Ezek.json"
j=json.load(open(P,encoding='utf-8'))
m=j['marks']
o=open('marks_measured.txt','w',encoding='utf-8')
o.write("marks entry sample: "+json.dumps({k:m[k] for k in list(m)[:2]},ensure_ascii=False)+"\n\n")
def mk(v): return m.get(v,'<<none>>')
o.write("--- P09-002 span MT 37.15-37.28, mark on the verse it FOLLOWS ---\n")
for i in range(14,30):
    v=f"Ezek.37.{i}"
    if v in m: o.write(f"  {v}: {json.dumps(m[v],ensure_ascii=False)}\n")
o.write("\n--- P08-002 span 33.10-33.20 ---\n")
for i in range(9,22):
    v=f"Ezek.33.{i}"
    if v in m: o.write(f"  {v}: {json.dumps(m[v],ensure_ascii=False)}\n")
o.write("\n--- 36.12-36.16 ---\n")
for i in range(11,17):
    v=f"Ezek.36.{i}"
    if v in m: o.write(f"  {v}: {json.dumps(m[v],ensure_ascii=False)}\n")
o.write("\n--- 36.20-36.33 ---\n")
for i in range(19,34):
    v=f"Ezek.36.{i}"
    if v in m: o.write(f"  {v}: {json.dumps(m[v],ensure_ascii=False)}\n")
o.write("\n--- ch40 1-6 + 39.29 ---\n")
for v in ['Ezek.39.29','Ezek.40.1','Ezek.40.2','Ezek.40.3','Ezek.40.4','Ezek.40.5','Ezek.40.6']:
    o.write(f"  {v}: {json.dumps(mk(v),ensure_ascii=False)}\n")
o.write("\n--- 30.19-30.26, 31.18, 32.16-32.17, 32.32, 33.7, 33.22-33.29, 34.1, 36.38, 37.1-37.3, 38.3, 39.11-39.17 ---\n")
for v in ['Ezek.30.19','Ezek.30.25','Ezek.30.26','Ezek.31.1','Ezek.31.18','Ezek.32.1','Ezek.32.16','Ezek.32.17','Ezek.32.32','Ezek.33.7','Ezek.33.22','Ezek.33.23','Ezek.33.24','Ezek.33.26','Ezek.33.28','Ezek.33.29','Ezek.34.1','Ezek.36.38','Ezek.37.1','Ezek.37.2','Ezek.37.3','Ezek.38.3','Ezek.39.11','Ezek.39.12','Ezek.39.14','Ezek.39.16','Ezek.39.17']:
    o.write(f"  {v}: {json.dumps(mk(v),ensure_ascii=False)}\n")
o.write("\nmarks_tally: "+json.dumps(j['marks_tally'],ensure_ascii=False)+"\n")
o.write("paseq entries for Ezek.40.1 / 39.17 / 33.11: ")
o.write(json.dumps([x for x in j['paseq'] if (isinstance(x,str) and x in('Ezek.40.1','Ezek.39.17','Ezek.33.11')) or (isinstance(x,dict) and x.get('verse') in ('Ezek.40.1','Ezek.39.17','Ezek.33.11'))],ensure_ascii=False)+"\n")
o.write("paseq sample: "+json.dumps(j['paseq'][:3],ensure_ascii=False)+"\n")
o.close(); print("ok")
