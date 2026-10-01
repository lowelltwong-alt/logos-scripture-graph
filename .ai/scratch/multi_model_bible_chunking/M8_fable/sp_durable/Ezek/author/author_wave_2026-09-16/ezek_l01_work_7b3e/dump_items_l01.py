import json, collections
LANE=r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
d=json.load(open(LANE,encoding='utf-8'))
items=d['your_worklist_items']
print('ITEM COUNT', len(items), 'declared', d['item_count'])
print('rows_file_sha256', d['rows_file_sha256'])
print('worklist_sha256', d['worklist_sha256'])
print('reminder:', d['reminder'])
print('role_vocabulary top-level:', d['role_vocabulary'])
# which fields vary
allkeys=collections.Counter()
for it in items: allkeys.update(it.keys())
print('KEYS:', dict(allkeys))
const={}
for k in allkeys:
    vals={json.dumps(it[k],ensure_ascii=False,sort_keys=True) for it in items if k in it}
    if len(vals)==1: const[k]=list(vals)[0]
print('\nCONSTANT-VALUED FIELDS (identical in every item that has them):')
for k,v in const.items(): print(' ',k,'=',v[:300])
print('\nBY CLASS:', dict(collections.Counter(it['cls'] for it in items)))
print('BY ROW:', dict(collections.Counter(it['row_id'] for it in items)))
print('moves_seam values:', {it.get('moves_seam') for it in items})
