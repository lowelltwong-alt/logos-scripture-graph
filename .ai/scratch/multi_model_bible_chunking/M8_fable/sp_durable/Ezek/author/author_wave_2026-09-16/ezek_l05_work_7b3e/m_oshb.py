import unicodedata as ud
P=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\Ezek_oshb.txt"
lines=open(P,encoding='utf-8').read().split('\n')
o=open('oshb_probe.txt','w',encoding='utf-8')
o.write(f"total lines={len(lines)}\nfirst 3 lines:\n")
for l in lines[:3]: o.write(repr(l)+"\n")
o.write("\n")
d={}
for l in lines:
    if not l.strip(): continue
    parts=l.split('\t') if '\t' in l else l.split(' ',1)
    d[parts[0]]=parts[1] if len(parts)>1 else ''
o.write(f"parsed keys={len(d)}; sample keys={list(d)[:3]}\n\n")
for v in ['Ezek.36.23','Ezek.33.17','Ezek.33.20','Ezek.29.9']:
    t=d.get(v)
    o.write(f"=== {v} ===\n{t}\n")
    if t:
        # word-by-word with accent names for the taamim of interest
        for w in t.split():
            marks=[ud.name(c,'?') for c in w if ud.category(c)=='Mn']
            key=[m for m in marks if 'ETNAHTA' in m or 'SOF PASUQ' in m or 'PASEQ' in m or 'SILLUQ' in m or 'METEG' in m]
            if key: o.write(f"   {w}  -> {key}\n")
    o.write("\n")
o.close(); print('ok')
