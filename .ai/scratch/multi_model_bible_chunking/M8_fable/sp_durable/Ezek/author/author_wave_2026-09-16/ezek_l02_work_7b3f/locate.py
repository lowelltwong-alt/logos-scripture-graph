import json, re
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_02_worklist.json'
lane = json.load(open(LANE, encoding='utf-8'))
rows = {r['decision_id']: r for r in lane['your_rows']}
items = lane['your_worklist_items']

def wordseq(s):
    s = s.replace('\u2019',"'").replace('\u2018',"'")
    return s

for i, it in enumerate(items):
    if it['cls'] not in ('A6','A6_UNION'): continue
    row = rows[it['row_id']]
    fld = it.get('field')
    run = it['run']
    toks = run.split()
    # locate by first and last token, case-insensitive, in each candidate field
    cands = [fld] if fld and fld in row else ['boundary_rationale','strongest_rejected_alternative','device_notes','literature_type_guess']
    print(f"--- I{i:02d} {it['row_id']} field={fld} run={run!r}")
    for c in cands:
        txt = row.get(c)
        if not isinstance(txt,str): continue
        # build a fuzzy regex: tokens separated by up to 40 chars of non-letters/quote junk
        pat = r'[\'"\u2018\u2019\u201c\u201d]*'.join(re.escape(t.replace("'",'')) for t in toks)
        pat = pat.replace("", "")  # noop
        # simpler: allow any non-alnum between tokens
        pat = r'\W{0,12}'.join(re.escape(t) if "'" not in t else re.escape(t).replace("'", r"['\u2019]") for t in toks)
        m = re.search(pat, txt, re.I)
        if m:
            s=max(0,m.start()-90); e=min(len(txt),m.end()+90)
            print(f"    [{c}] FOUND at {m.start()}..{m.end()}")
            print(f"      matched: {txt[m.start():m.end()]!r}")
            print(f"      ctx: ...{txt[s:e]}...")
        else:
            print(f"    [{c}] not found by fuzzy match")
