import json,re
P=r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\pmarks_Ezek.json'
d=json.load(open(P,encoding='utf-8'))
def ch(k):
    m=re.match(r'Ezek\.(\d+)\.(\d+)',k)
    return (int(m.group(1)),int(m.group(2))) if m else (999,999)
for sec in ['marks','paseq','kq','notes_other','other_segs']:
    v=d.get(sec)
    print(f'--- {sec} ({type(v).__name__}) ---')
    if isinstance(v,dict):
        sub={k:val for k,val in v.items() if ch(k)[0]<=6}
        for k in sorted(sub,key=ch):
            print(f'  {k:14s} -> {json.dumps(sub[k],ensure_ascii=False)}')
        print(f'  [chs1-6 keys: {len(sub)} of {len(v)} total]')
    else:
        print('  ',json.dumps(v,ensure_ascii=False)[:800])
    note=d.get(sec+'_note'); 
    if note: print('  NOTE:',note)
    t=d.get(sec+'_tally')
    if t: print('  TALLY:',json.dumps(t,ensure_ascii=False))
print('--- marks_tally ---',json.dumps(d['marks_tally'],ensure_ascii=False))
print('--- seg_totals_in_xml ---',json.dumps(d.get('seg_totals_in_xml'),ensure_ascii=False))
print('--- arithmetic_anomalies_resolved ---',json.dumps(d.get('arithmetic_anomalies_resolved'),ensure_ascii=False)[:1500])
