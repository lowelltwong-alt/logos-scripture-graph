import re, json
BB = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'
V = {}
for line in open(BB + r'\Ezek_oshb.txt', encoding='utf-8').read().split('\n'):
    if not line.strip(): continue
    k, t = line.split('\t', 1)
    V[k] = t
def skel(s):
    s = ''.join(c for c in s if '\u05d0' <= c <= '\u05ea' or c == ' ')
    return re.sub(r'\s+', ' ', s).strip()
inv = json.load(open(BB + r'\ezek_device_inventory.v2.json', encoding='utf-8'))
som = set(inv['formulae']['son_of_man_address']['verses_mt'])
syf = set(inv['formulae']['set_your_face']['verses_mt'])
print("son-of-man address in ch14:", sorted([k for k in som if k.startswith('Ezek.14.')], key=lambda x:int(x.split('.')[2])))
print("set-your-face in ch14:", [k for k in syf if k.startswith('Ezek.14.')])
for k in ['Ezek.14.20','Ezek.14.21','Ezek.14.13','Ezek.11.15','Ezek.11.16','Ezek.11.17','Ezek.11.21','Ezek.13.10']:
    s = skel(V[k])
    print(f"\n{k} skeleton ({len(s)} chars):\n  {s}")
    print(f"  last 8 words: {' '.join(s.split()[-8:])}")
print()
# does 've-attah' or any vocative open 14:21?
print("14:21 first 6 skeleton words:", ' '.join(skel(V['Ezek.14.21']).split()[:6]))
print("14:12-14:23 son_of_man verses:", [k for k in som if k in [f'Ezek.14.{i}' for i in range(12,24)]])
