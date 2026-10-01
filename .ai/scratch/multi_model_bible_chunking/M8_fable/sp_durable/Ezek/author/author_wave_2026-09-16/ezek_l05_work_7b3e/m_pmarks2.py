import json,unicodedata as ud
P=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\pmarks_Ezek.json"
j=json.load(open(P,encoding='utf-8'))
print("kq_note:", j['kq_note'])
print("kq_tally:", json.dumps(j['kq_tally'],ensure_ascii=False))
print("numbering:", j['numbering'])
print("marks_note:", j['marks_note'])
print("witness:", j['witness'])
print()
print("=== arithmetic_anomalies_resolved (FULL) ===")
print(json.dumps(j['arithmetic_anomalies_resolved'],ensure_ascii=False,indent=1))
print()
for v in ['Ezek.33.13','Ezek.33.16','Ezek.33.20','Ezek.36.13','Ezek.36.14','Ezek.36.15','Ezek.37.16','Ezek.37.19','Ezek.37.22','Ezek.39.25','Ezek.35.9','Ezek.35.12','Ezek.31.5','Ezek.32.31','Ezek.32.32']:
    e=j['kq'].get(v,'<<ABSENT from kq>>')
    print(f"kq[{v}] type={type(e).__name__} = {json.dumps(e,ensure_ascii=False)}")
    if isinstance(e,list):
        for i,m in enumerate(e):
            print(f"    member[{i}] slashcount={m.count('/')} repr={m!r}")
print()
print("notes_other keys present for my range:")
for v,e in j['notes_other'].items():
    c=int(v.split('.')[1])
    if 30<=c<=40: print("  ",v,"=",json.dumps(e,ensure_ascii=False))
