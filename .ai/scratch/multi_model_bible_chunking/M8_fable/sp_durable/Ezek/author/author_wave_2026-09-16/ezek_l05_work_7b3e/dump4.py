import json
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
j=json.load(open(LANE,encoding='utf-8'))
rows=j['your_rows']
items=j['your_worklist_items']
# index map
with open('item_index.txt','w',encoding='utf-8') as f:
    for i,it in enumerate(items):
        extra=it.get('citation') or it.get('run') or it.get('new_value') or ''
        f.write(f"l05_i{i:02d} {it['row_id']} {it['cls']:<12} {it.get('field','-'):<34} {extra}\n")
print(open('item_index.txt',encoding='utf-8').read())
print("ROW FIELD SIZES")
allkeys=set()
for r in rows: allkeys|=set(r.keys())
print(sorted(allkeys))
for r in rows:
    tot=len(json.dumps(r,ensure_ascii=False))
    print(r['decision_id'], r['span'], 'conf=',r['confidence'], 'bytes=',tot)
