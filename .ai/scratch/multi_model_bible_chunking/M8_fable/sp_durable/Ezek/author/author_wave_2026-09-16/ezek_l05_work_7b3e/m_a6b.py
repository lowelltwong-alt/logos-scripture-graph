import json,re
WEB=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json"
LANE=r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
w=json.load(open(WEB,encoding='utf-8')); lane=json.load(open(LANE,encoding='utf-8'))
rows={r['decision_id']:r for r in lane['your_rows']}; items=lane['your_worklist_items']
def norm(s):
    s=s.lower()
    s=re.sub(r"\[fn\]"," ",s)
    s=re.sub(r"[^a-z]+"," ",s)          # EVERY non a-z becomes a space: apostrophes, quotes, ellipses, Hebrew
    return " "+s.strip()+" "
NV={k:norm(v.get('clean') or v.get('text','')) for k,v in w.items()}
def vkey(k):
    p=k.split('.'); return (int(p[1]),int(p[2]))
SORTED=sorted(NV,key=vkey)
def occ(run): 
    r=norm(run)
    return [k for k in SORTED if r in NV[k]]
FIELDMAP={'refs':'boundary_evidence_refs'}
o=open('a6_FINAL.txt','w',encoding='utf-8')
for idx,it in enumerate(items):
    if it['cls'] not in ('A6','A6_UNION'): continue
    rid=it['row_id']; run=it['run']; r=rows[rid]
    fname=FIELDMAP.get(it.get('field','-'),it.get('field','-'))
    sp=r['span']; a,b=sp.split('-')
    lo=(int(a.split('.')[1]),int(a.split('.')[2])); hi=(int(b.split('.')[1]),int(b.split('.')[2]))
    O=occ(run); ins=[k for k in O if lo<=vkey(k)<=hi]
    nr=norm(run)
    o.write(f"### l05_i{idx:02d} {rid} {sp} | {it['cls']}/{it['kind']} | field={fname} | formula={it.get('formula_rendering')} | item_in_span={it.get('in_span')}\n")
    o.write(f"  run={run!r} ({len(run.split())} w)  declared_refs={it.get('web_refs','-')}\n")
    o.write(f"  WEB occurrences n={len(O)}: {O if len(O)<=20 else O[:20]+['...']}\n")
    o.write(f"  IN-SPAN: {ins}\n")
    if 'web_refs' in it:
        o.write(f"  declared-ref check: "+", ".join(f"{x}={'YES' if x in O else 'NO'}" for x in it['web_refs'])+"\n")
    # in-field presence
    fields=[fname] if fname in r else ['boundary_rationale','strongest_rejected_alternative','device_notes','boundary_evidence_refs']
    for k in fields:
        v=r[k]
        if isinstance(v,list):
            hits=[i2 for i2,e in enumerate(v) if nr in norm(e)]
            o.write(f"  in-field {k}: entries {hits if hits else 'NONE'}; joined_present={nr in norm(' | '.join(v))}\n")
        else:
            o.write(f"  in-field {k}: {'PRESENT' if nr in norm(v) else 'ABSENT'}\n")
    o.write("\n")
o.close(); print('ok')
