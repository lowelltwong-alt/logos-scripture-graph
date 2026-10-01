# -*- coding: utf-8 -*-
import json
LANE=r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
d=json.load(open(LANE,encoding='utf-8'))
rows={r['decision_id']:r for r in d['your_rows']}
LD,RD='\u201c','\u201d'   # double curly quotes
LS,RS='\u2018','\u2019'   # single curly

# (item_idx, row, field, old_substring, new_substring)
S=[
 (1,'P01-001','boundary_evidence_refs',", 'the hands of a man')", ", %sthe hands of a man%s (web:Ezek.1.8))"%(LD,RD)),
 (3,'P01-002','boundary_rationale', "('he said to me, \u201cSon of man, stand on your feet\u201d (web:Ezek.2.1)')",
   "(%sHe said to me, %sSon of man, stand on your feet%s%s (web:Ezek.2.1))"%(LD,LS,RS,RD)),
 (4,'P01-002','boundary_rationale', "('I send you to the children of Israel')",
   "(%sI send you to the children of Israel%s (web:Ezek.2.3))"%(LD,RD)),
 (9,'P01-003','boundary_rationale', "('and you, son of man, hear\u2026')",
   "(WEB %sBut you, son of man, hear%s (web:Ezek.2.8))"%(LD,RD)),
 (10,'P01-003','boundary_rationale', "('behold, a hand stretched out to me')",
   "(%sbehold, a hand was stretched out to me%s (web:Ezek.2.9))"%(LD,RD)),
 (16,'P01-004','boundary_rationale', "('for all the house of Israel are obstinate and hard-hearted')",
   "(%sfor all the house of Israel are obstinate and hard-hearted%s (web:Ezek.3.7))"%(LD,RD)),
 (17,'P01-004','boundary_rationale', "('I have made your forehead as a diamond')",
   "(%sI have made your forehead as a diamond%s (web:Ezek.3.9))"%(LD,RD)),
 (18,'P01-004','boundary_rationale', "'moreover he said to me'",
   "%sMoreover he said to me%s (web:Ezek.3.10)"%(LD,RD)),
 (19,'P01-004','boundary_rationale', "('whether they will hear, or whether they will refuse')",
   "(%swhether they will hear, or whether they will refuse%s (web:Ezek.3.11))"%(LD,RD)),
 (27,'P01-005','boundary_rationale', "('then the Spirit lifted me up')",
   "(%sThen the Spirit lifted me up%s (web:Ezek.3.12))"%(LD,RD)),
 (28,'P01-005','boundary_rationale', "('I sat there overwhelmed among them seven days')",
   "(%sI sat there overwhelmed among them seven days%s (web:Ezek.3.15))"%(LD,RD)),
 (29,'P01-005','boundary_rationale', "'at the end of seven days'",
   "%sAt the end of seven days%s (web:Ezek.3.16)"%(LD,RD)),
 (32,'P01-006','boundary_rationale', None, None),   # filled below (apostrophe byte unknown)
 (33,'P01-006','boundary_rationale', "('I have made you a watchman to the house of Israel')",
   "(%sI have made you a watchman to the house of Israel%s (web:Ezek.3.17))"%(LD,RD)),
 (37,'P01-007','boundary_rationale', None, None),   # filled below
 (38,'P01-007','boundary_rationale', "'arise, go out into the plain'",
   "%sArise, go out into the plain%s (web:Ezek.3.22)"%(LD,RD)),
 (39,'P01-007','boundary_rationale', "('he who hears, let him hear; and he who refuses, let him refuse; for they are a rebellious house')",
   "(%sHe who hears, let him hear; and he who refuses, let him refuse; for they are a rebellious house%s (web:Ezek.3.27))"%(LD,RD)),
 (40,'P01-007','strongest_rejected_alternative', "('at the end of seven days')",
   "(%sAt the end of seven days%s (web:Ezek.3.16))"%(LD,RD)),
 (45,'P01-008','boundary_rationale', "('you also, son of man, take a tile')",
   "(%sYou also, son of man, take a tile%s (web:Ezek.4.1))"%(LD,RD)),
 (46,'P01-008','boundary_rationale', "('behold, I put ropes on you')",
   "(%sBehold, I put ropes on you%s (web:Ezek.4.8))"%(LD,RD)),
 (47,'P01-008','boundary_rationale', "('behold, I will break the staff of bread')",
   "(%sbehold, I will break the staff of bread%s (web:Ezek.4.16))"%(LD,RD)),
 (48,'P01-008','boundary_rationale', "('that they may lack bread and water')",
   "(%sthat they may lack bread and water%s (web:Ezek.4.17))"%(LD,RD)),
 (57,'P01-009','boundary_rationale', "('you, son of man, take a sharp sword')",
   "(%sYou, son of man, take a sharp sword%s (web:Ezek.5.1))"%(LD,RD)),
 (58,'P01-009','boundary_rationale', "'moreover I will make you a desolation'",
   "%sMoreover I will make you a desolation%s (web:Ezek.5.14)"%(LD,RD)),
 (75,'P01-010','boundary_rationale', "('set your face toward the mountains of Israel')",
   "(%sset your face toward the mountains of Israel%s (web:Ezek.6.2))"%(LD,RD)),
 (77,'P01-010','boundary_rationale', "('yet I will leave a remnant\u2026')",
   "(%sYet I will leave a remnant%s (web:Ezek.6.8))"%(LD,RD)),
 (79,'P01-010','strongest_rejected_alternative', "'yet I will leave a remnant'",
   "%sYet I will leave a remnant%s (web:Ezek.6.8)"%(LD,RD)),
]
# discover the exact bytes for items 32 and 37 (apostrophe form unknown)
import re
br6=rows['P01-006']['boundary_rationale']; br7=rows['P01-007']['boundary_rationale']
m32=re.search(r"\('at the end of seven days, Yahweh(.)s word came to me, saying'\)",br6)
m37=re.search(r"\('Yahweh(.)s hand was there on me'\)",br7)
print('item32 apostrophe codepoint:',hex(ord(m32.group(1))),'| item37:',hex(ord(m37.group(1))))
ap32=m32.group(1); ap37=m37.group(1)
S=[list(x) for x in S]
for x in S:
    if x[0]==32:
        x[3]=m32.group(0)
        x[4]="(%sAt the end of seven days, Yahweh%ss word came to me, saying%s (web:Ezek.3.16))"%(LD,'\u2019',RD)
    if x[0]==37:
        x[3]=m37.group(0)
        x[4]="(%sYahweh%ss hand was there on me%s (web:Ezek.3.22))"%(LD,'\u2019',RD)

# apply, asserting single occurrence
newvals={}   # (row,field) -> value
touched={}   # (row,field) -> [item idx]
for idx,row,field,old,new in S:
    cur=newvals.get((row,field))
    if cur is None:
        base=rows[row][field]
        cur=list(base) if isinstance(base,list) else base
    if field=='boundary_evidence_refs':
        hits=[i for i,e in enumerate(cur) if old in e]
        assert len(hits)==1,(idx,row,field,'refs hits',hits)
        assert cur[hits[0]].count(old)==1
        cur=list(cur); cur[hits[0]]=cur[hits[0]].replace(old,new)
    else:
        n=cur.count(old)
        assert n==1,(idx,row,field,'count',n,repr(old[:60]))
        cur=cur.replace(old,new)
    newvals[(row,field)]=cur
    touched.setdefault((row,field),[]).append(idx)
print('\nA6 surgeries applied OK. (row,field) -> items:')
for k,v in touched.items(): print('  ',k,v)
json.dump({'newvals':{f'{r}|{f}':v for (r,f),v in newvals.items()},
           'touched':{f'{r}|{f}':v for (r,f),v in touched.items()}},
          open('a6_newvals.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('\nwrote a6_newvals.json')
