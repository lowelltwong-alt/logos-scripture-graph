# -*- coding: utf-8 -*-
import json, unicodedata as ud
B=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
lane=json.load(open(LANE,encoding='utf-8'))
ROWS={r['decision_id']:r for r in lane['your_rows']}
pm=json.load(open(B+r"\pmarks_Ezek.json",encoding='utf-8'))
osh={}
for l in open(B+r"\Ezek_oshb.txt",encoding='utf-8'):
    l=l.rstrip('\n')
    if l.strip(): k,_,t=l.partition('\t'); osh[k]=t

def split_kq(member):
    i=next(j for j,c in enumerate(member) if ud.category(c)=='Mn')
    return member[:i-1], member[i-1:]
def bare(s): return s.replace('/','')

# --- K/Q forms pulled from the pinned input, never typed ---
K3313,Q3313 = [bare(x) for x in split_kq(pm['kq']['Ezek.33.13'][0])]
K3316,Q3316 = [bare(x) for x in split_kq(pm['kq']['Ezek.33.16'][0])]
Q3716a = bare(split_kq(pm['kq']['Ezek.37.16'][0])[1])
Q3716b = bare(split_kq(pm['kq']['Ezek.37.16'][1])[1])
K3716  = bare(split_kq(pm['kq']['Ezek.37.16'][0])[0])
SEP3613=[m.count('/') for m in pm['kq']['Ezek.36.13']]
SEP3614=[m.count('/') for m in pm['kq']['Ezek.36.14']]
# 36:23 b-half tail (the dependent temporal infinitive), sliced from the witness
w3623=osh['Ezek.36.23'].split(); TAIL3623=' '.join(w3623[-3:])
w3317=osh['Ezek.33.17'].split(); COMPLAINT=' '.join(w3317[3:7])
w3310=osh['Ezek.33.10'].split(); ADDR3310=' '.join(w3310[5:7])
w3312=osh['Ezek.33.12'].split(); ADDR3312=' '.join(w3312[4:6])
out={'K3313':K3313,'Q3313':Q3313,'K3316':K3316,'Q3316':Q3316,'K3716':K3716,
     'Q3716a':Q3716a,'Q3716b':Q3716b,'SEP3613':SEP3613,'SEP3614':SEP3614,
     'TAIL3623':TAIL3623,'COMPLAINT':COMPLAINT,'ADDR3310':ADDR3310,'ADDR3312':ADDR3312}
json.dump(out,open('derived_strings.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
with open('derived_check.txt','w',encoding='utf-8') as f:
    for k,v in out.items(): f.write(f"{k} = {v}\n")
print("wrote derived strings")
