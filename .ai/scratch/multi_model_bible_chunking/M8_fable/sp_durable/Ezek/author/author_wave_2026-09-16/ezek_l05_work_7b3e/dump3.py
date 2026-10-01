import json
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
j=json.load(open(LANE,encoding='utf-8'))
items=j['your_worklist_items']
out=open('a4_table.txt','w',encoding='utf-8')
n=0
for idx,it in enumerate(items):
    if it['cls']!='A4_CITATION': continue
    n+=1
    out.write(f"{idx:3d} | {it['row_id']} | {it['citation']:<28} | {it['citation_kind']:<6} | {it['a4_class']:<8} | field={it['field']:<32} | raw={it['raw']!r:<26} | vc={it['verse_count']:<2} | rep={it['repeats_in_row']}\n")
out.write(f"TOTAL A4 {n}\n")
out.close()
# A6 items full
out=open('a6_items.txt','w',encoding='utf-8')
for idx,it in enumerate(items):
    if it['cls'] not in ('A6','A6_UNION'): continue
    out.write(f"--- idx {idx} ---\n")
    out.write(json.dumps(it, ensure_ascii=False, indent=1)+"\n")
out.close()
print(open('a4_table.txt',encoding='utf-8').read())
