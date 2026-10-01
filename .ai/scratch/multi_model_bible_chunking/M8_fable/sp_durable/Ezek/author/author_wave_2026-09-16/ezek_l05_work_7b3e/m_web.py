import json,re
P=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json"
j=json.load(open(P,encoding='utf-8'))
o=open('web_probe.txt','w',encoding='utf-8')
o.write("type=%s len=%d\n"%(type(j).__name__,len(j)))
if isinstance(j,dict):
    ks=list(j)[:4]
    o.write("sample keys: %s\n"%ks)
    for k in ks: o.write("  %s -> %s\n"%(k,json.dumps(j[k],ensure_ascii=False)[:400]))
o.close(); print(open('web_probe.txt',encoding='utf-8').read()[:1500])
