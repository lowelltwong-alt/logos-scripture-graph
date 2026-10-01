import json,unicodedata as ud
P=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\pmarks_Ezek.json"
j=json.load(open(P,encoding='utf-8'))
o=open('kq_measured.txt','w',encoding='utf-8')
for v in ['Ezek.33.13','Ezek.33.16','Ezek.33.20','Ezek.36.13','Ezek.36.14','Ezek.36.15','Ezek.37.16','Ezek.37.19','Ezek.37.22','Ezek.39.25','Ezek.35.9','Ezek.35.12','Ezek.31.5','Ezek.32.31','Ezek.32.32']:
    e=j['kq'].get(v,None)
    if e is None:
        o.write(f"kq[{v}] = <<KEY ABSENT from pmarks kq>>\n\n"); continue
    o.write(f"kq[{v}] type={type(e).__name__} members={len(e) if isinstance(e,list) else 'n/a'}\n")
    if isinstance(e,list):
        for i,m in enumerate(e):
            o.write(f"   member[{i}] slash={m.count('/')} : {m}\n")
    else:
        o.write(f"   value: {e}\n")
    o.write("\n")
# codepoint diff for 37.16
e=j['kq']['Ezek.37.16']
if isinstance(e,list) and len(e)==2:
    a,b=e
    o.write("=== Ezek.37.16 codepoint diff (members) ===\n")
    for lbl,s in (('m0',a),('m1',b)):
        o.write(f"{lbl}: {s}\n")
        o.write("   "+ " ".join(f"U+{ord(c):04X}({ud.name(c,'?')})" for c in s if not c.isspace())+"\n")
    sa,sb=set(a),set(b)
    o.write(f"only in m0: {[f'U+{ord(c):04X} {ud.name(c,chr(39))}' for c in sa-sb]}\n")
    o.write(f"only in m1: {[f'U+{ord(c):04X} {ud.name(c,chr(39))}' for c in sb-sa]}\n")
o.close()
print("ok")
