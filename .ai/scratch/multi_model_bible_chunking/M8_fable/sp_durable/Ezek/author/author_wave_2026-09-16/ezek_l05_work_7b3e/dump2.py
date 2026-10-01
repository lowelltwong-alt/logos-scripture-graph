import json
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
j=json.load(open(LANE,encoding='utf-8'))
items=j['your_worklist_items']
out=open('items_full.txt','w',encoding='utf-8')
order=['BOSS_RETURN','WORDING','CONFIDENCE','A4_CITATION','A6','A6_UNION']
for cls in order:
    sel=[i for i in items if i['cls']==cls]
    out.write(f"\n########## {cls}  ({len(sel)}) ##########\n")
    for i in sel:
        out.write(json.dumps(i, ensure_ascii=False, indent=1)+"\n")
# any class not covered
rest=[i for i in items if i['cls'] not in order]
if rest:
    out.write("\n########## OTHER ##########\n")
    for i in rest: out.write(json.dumps(i,ensure_ascii=False,indent=1)+"\n")
out.close()
print("wrote", sum(1 for _ in open('items_full.txt',encoding='utf-8')), "lines")
