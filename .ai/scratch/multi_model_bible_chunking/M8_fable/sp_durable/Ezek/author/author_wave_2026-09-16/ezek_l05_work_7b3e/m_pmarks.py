import json
P=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\pmarks_Ezek.json"
j=json.load(open(P,encoding='utf-8'))
print("TOP-LEVEL KEYS:", list(j.keys()))
for k,v in j.items():
    t=type(v).__name__
    n=len(v) if hasattr(v,'__len__') else '-'
    print(f"  {k}: {t} len={n}")
