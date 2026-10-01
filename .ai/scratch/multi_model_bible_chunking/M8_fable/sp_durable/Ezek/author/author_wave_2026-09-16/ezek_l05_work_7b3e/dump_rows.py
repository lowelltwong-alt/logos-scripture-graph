import json,sys
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
j=json.load(open(LANE,encoding='utf-8'))
rows=j['your_rows']
want=sys.argv[1:]
f=open('rows_'+('_'.join(want) if want else 'all')+'.txt','w',encoding='utf-8')
FIELDS=['decision_id','span','confidence','unit_type','literature_type_guess','boundary_rationale','strongest_rejected_alternative','device_notes','observed_substrate_signals','boundary_evidence_refs']
for r in rows:
    if want and r['decision_id'] not in want: continue
    f.write("="*100+"\n")
    for k in FIELDS:
        v=r.get(k,'<<ABSENT>>')
        if isinstance(v,list):
            f.write(f"@{k} = [\n")
            for e in v: f.write("   "+json.dumps(e,ensure_ascii=False)+"\n")
            f.write("  ]\n")
        else:
            f.write(f"@{k} = {json.dumps(v,ensure_ascii=False)}\n")
    f.write("\n")
f.close()
print("done")
