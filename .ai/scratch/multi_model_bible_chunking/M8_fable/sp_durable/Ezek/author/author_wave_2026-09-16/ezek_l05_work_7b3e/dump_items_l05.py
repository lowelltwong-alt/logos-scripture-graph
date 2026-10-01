import json, sys, collections
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
j=json.load(open(LANE,encoding='utf-8'))
items=j['your_worklist_items']
print("ITEM COUNT", len(items))
keysets=collections.Counter()
for it in items:
    keysets[tuple(sorted(it.keys()))]+=1
for k,v in keysets.items():
    print("KEYSET", v, k)
print()
print("=== reminder ===")
print(json.dumps(j.get('reminder'), ensure_ascii=False, indent=1))
print("=== role_vocabulary ===")
print(json.dumps(j.get('role_vocabulary'), ensure_ascii=False, indent=1))
print("=== digests ===")
print(j.get('rows_file_sha256'), j.get('worklist_sha256'))
