"""CWO-1COR-05 reference (controlling r3 e1). Reads ROWS.jsonl; prints hits; writes --out if given."""
import json,re,sys,collections
SPLIT=re.compile(r"(?<=[.;])\s+")
P4=re.compile(r"(?i)pilcrow|\bparagraph marks?\b")
DIS4=re.compile(r"(?i)not weighed|formatting|decides? nothing|does not decide|do not decide|never drives?|neither drives? nor corroborates?|excluded|not (?:drive|corroborate)|without deciding|informs? and does not decide")
PD2=re.compile(r"(?i)corroborat|agree|\bjoin|confirm|support|favou?r|\blean|points? to|(?<!paragraph )(?<!-)\bmark(?:s|ed|ing)?\b|\bsignal|establish|determin")
PD3=re.compile(r"(?i)\b(?:opens?|opened|opening|closes|closed|decides?|decided|decisive|drives?|drove|driven|driving|begins?|began|begun)\b")
def units(r):
    for f in ("boundary_rationale","strongest_rejected_alternative","device_notes"):
        v=r.get(f)
        if isinstance(v,str):
            for s in SPLIT.split(v): yield f,None,s
    for f in ("observed_substrate_signals","boundary_evidence_refs"):
        for i,x in enumerate(r.get(f) or []): yield f,i,(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False))
def hits_of_unit(s):
    if not P4.search(s): return False
    if PD2.search(s): return False          # already CWO-1COR-04 support_use
    return bool(PD3.search(DIS4.sub(" ",s)))
if __name__=="__main__":
    if sys.argv[1]=="--plants":
        plants=[("The RP pilcrow at 1:10 opens the unit.",True),("The RP pilcrow at 15:35 closes the argument.",True),
                ("The RP pilcrow at 14:34 decides the seam.",True),("The RP pilcrow drives the cut at 15:50.",True),
                ("Pilcrows open both units.",True),("The pilcrow opens the unit and decides nothing.",True),
                ("RP pilcrow on the close seam (15:12)",False),("The RP pilcrow at 10:14 informs and does not decide.",False),
                ("RP pilcrow at 16:13 (close seam).",False),("The RP pilcrow at 1:10 marks the onset.",False),
                ("rp:1Cor.15.12 (conditional opens the following argument; RP pilcrow)",True)]
        ok=all(hits_of_unit(s)==e for s,e in plants)
        for s,e in plants: print(hits_of_unit(s)==e, e, s)
        print("PLANTS", "ALL_PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
    rows=[json.loads(x) for x in open(sys.argv[1],encoding='utf-8') if x.strip()]
    hs=[]
    for r in rows:
        for f,i,s in units(r):
            if hits_of_unit(s): hs.append({"row":r['decision_id'],"field":f,"index":i,"text":s})
    print("rows_scanned",len(rows),"hits",len(hs),"rows_hit",len({h['row'] for h in hs}))
    for h in hs:
        s=h['text']; m=P4.search(s); a=max(0,m.start()-120)
        print(f"{h['row']} {h['field']}[{h['index']}] :: {s[a:m.end()+100]}")
    if "--out" in sys.argv: open(sys.argv[sys.argv.index("--out")+1],'w',encoding='utf-8',newline='\n').write(json.dumps(hs,ensure_ascii=False,indent=1)+"\n")
