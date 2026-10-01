import json
B = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'
vi = json.load(open(B + r'\verse_inventory.json', encoding='utf-8'))
ch = vi['chapters']
om = json.load(open(B + r'\web_mt_offset_map.json', encoding='utf-8'))
print('offset map keys:', list(om.keys())[:10])
def n(c):
    return ch[str(c)] if isinstance(ch, dict) else ch[c-1]
print('WEB verses per chapter 6-16:', {c: n(c) for c in range(6,17)})
def count(c1,v1,c2,v2):
    if c1==c2: return v2-v1+1
    t = n(c1)-v1+1
    for c in range(c1+1,c2): t += n(c)
    return t+v2
for lbl,a,b in [('P02-002 rival 8:7-8:18',(8,7),(8,18)),
                ('P02-003 remainder 8:16-8:18',(8,16),(8,18)),
                ('P02-003 shorter 8:14-8:15',(8,14),(8,15)),
                ('P02-005 rival 10:1-10:17',(10,1),(10,17)),
                ('P02-020 span 14:12-14:23',(14,12),(14,23)),
                ('P02-006 rival 10:1-10:22',(10,1),(10,22)),
                ('P02-006 rival 10:1-11:13',(10,1),(11,13)),
                ('P01-013 rival 7:5-7:27',(7,5),(7,27)),
                ('P01-014 span 7:10-7:27',(7,10),(7,27)),
                ('P02-002 span 8:7-8:13',(8,7),(8,13)),
                ('P02-019 span 14:1-14:11',(14,1),(14,11)),
                ('P02-020 rival tail 14:21-14:23',(14,21),(14,23)),
                ('P03-002 span 16:1-16:14',(16,1),(16,14)),
                ('P03-003 span 16:15-16:19',(16,15),(16,19)),
                ('P02-009 span 11:14-11:21',(11,14),(11,21)),
                ]:
    print(f"{lbl}: {count(a[0],a[1],b[0],b[1])} verses")
