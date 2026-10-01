import json
LANE=r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json'
items=json.load(open(LANE,encoding='utf-8'))['your_worklist_items']
print('=== GROUNDS ITEMS IN FULL ===')
for i,it in enumerate(items):
    if it['cls']=='GROUNDS':
        print('idx',i, json.dumps(it,ensure_ascii=False,indent=1))
print()
print('=== ALL ITEMS COMPACT (idx | row | cls | key fields) ===')
for i,it in enumerate(items):
    c=it['cls']; r=it['row_id']
    if c=='A6':
        print(f"{i:02d} | {r} | A6   | field={it['field']:20s} words={it['words']:2d} kind={it['kind']:17s} in_span={str(it['in_span']):5s} formula={str(it['formula_rendering']):5s} web_refs={it['web_refs']} run={it['run']!r}")
    elif c=='A4_CITATION':
        print(f"{i:02d} | {r} | A4   | field={it['field']:20s} cite={it['citation']:22s} kind={it['citation_kind']:6s} a4={it['a4_class']:10s} vn={it['verse_count']:2d} rep={it['repeats_in_row']} raw={it['raw']!r} verses={it['verses_web']}")
    else:
        print(f"{i:02d} | {r} | {c} | field={it.get('field')} action={it['action'][:200]}")
