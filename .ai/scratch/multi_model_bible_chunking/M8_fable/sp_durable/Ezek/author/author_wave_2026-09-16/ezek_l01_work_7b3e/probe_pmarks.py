import json
P=r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\pmarks_Ezek.json'
d=json.load(open(P,encoding='utf-8'))
print('TOP TYPE', type(d).__name__)
if isinstance(d,dict):
    print('TOP KEYS', list(d.keys())[:40])
    for k in list(d.keys())[:6]:
        v=d[k]
        print(' ',k,'->',type(v).__name__, (str(v)[:400] if not isinstance(v,(list,dict)) else ''))
        if isinstance(v,list): print('    len',len(v),'first:',json.dumps(v[:3],ensure_ascii=False)[:400])
        if isinstance(v,dict): print('    keys',list(v.keys())[:20],'sample:',json.dumps(dict(list(v.items())[:3]),ensure_ascii=False)[:500])
