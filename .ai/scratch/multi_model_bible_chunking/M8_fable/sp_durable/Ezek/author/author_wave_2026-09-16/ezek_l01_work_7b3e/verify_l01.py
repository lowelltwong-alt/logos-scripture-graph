import json,re
B=r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'
osh={}
for ln in open(B+r'\Ezek_oshb.txt',encoding='utf-8'):
    ln=ln.rstrip('\n')
    if ln.strip(): r,_,t=ln.partition('\t'); osh[r]=t
inv=json.load(open(B+r'\ezek_device_inventory.v2.json',encoding='utf-8'))
pm=json.load(open(B+r'\pmarks_Ezek.json',encoding='utf-8'))
off=json.load(open(B+r'\web_mt_offset_map.json',encoding='utf-8'))
vinv=json.load(open(B+r'\verse_inventory.json',encoding='utf-8'))

def skel(s):
    return re.sub(r'\s+',' ',''.join(c for c in s if '\u05d0'<=c<='\u05ea' or c==' ')).strip()

print('### (a) NUMBERING FACE / OFFSET MAP, chs 1-6')
print('verse_inventory numbering_face:', vinv.get('numbering_face'))
print('offset map top keys:', list(off.keys())[:14] if isinstance(off,dict) else type(off))
s=json.dumps(off,ensure_ascii=False)
print('offset map mentions "identity":', 'identity' in s.lower())
for k,v in (off.items() if isinstance(off,dict) else []):
    if not isinstance(v,(dict,list)): print('  ',k,'=',str(v)[:220])
print()

print('### (b) ITEM 24 ABSENCE-OVER-RANGE: Ezek.3.10-3.11')
lists={
 'word_event_strict_39':inv['formulae']['word_event_formula']['verses_mt'],
 'word_event_vayehi_any_41':inv['formulae']['word_event_vayehi_any']['verses_mt'],
 'word_event_hayah_any_7':inv['formulae']['word_event_hayah_any']['verses_mt'],
 'hand_of_yhwh_7':inv['formulae']['hand_of_yhwh_upon_me']['verses_mt'],
 'dated_oracles_14':inv['dated_oracles']['verses_mt'],
}
fam48=set(lists['word_event_vayehi_any_41'])|set(lists['word_event_hayah_any_7'])
any49=fam48|{'Ezek.1.3'}
print('  derived family_48 size:',len(fam48),' any_form_49 size:',len(any49))
for tgt in ['Ezek.3.10','Ezek.3.11']:
    print(f'  {tgt}: in any49={tgt in any49}  in fam48={tgt in fam48}  in hand7={tgt in lists["hand_of_yhwh_7"]}  in datelines14={tgt in lists["dated_oracles_14"]}')
print('  => 0 of 49 word-event, 0 of 7 hand, 0 of 14 dateline in 3:10-3:11 :',
      all(t not in any49 and t not in lists['hand_of_yhwh_7'] and t not in lists['dated_oracles_14'] for t in ['Ezek.3.10','Ezek.3.11']))
print()

print('### (c) ve-attah SHAPE TEST (consonantal skeleton), ch 4-5')
VEATTAH='ואתה'; BENADAM='בן אדם'
for v in ['Ezek.4.1','Ezek.4.3','Ezek.4.4','Ezek.4.9','Ezek.5.1']:
    sk=skel(osh[v]); w=sk.split()
    opens=w[0]==VEATTAH
    titled=' '.join(w[1:3])==BENADAM if len(w)>2 else False
    print(f'  {v}: opens_ve_attah={opens}  next_two={" ".join(w[1:3])!r}  titled_ben_adam={titled}  first4={" ".join(w[:4])!r}')
print()

print('### (d) P01-009 INTERIOR MARKS vs MESSENGER-FORMULA ONSET (span 5:1-5:17)')
mess=set(inv['formulae']['thus_says_the_lord_yhwh']['verses_mt'])
print('  messenger list size:',len(mess),' in ch5:',sorted([m for m in mess if m.startswith("Ezek.5.")],key=lambda x:int(x.split(".")[2])))
marks=pm['marks']
interior=[v for v in marks if v.startswith('Ezek.5.') and 1<=int(v.split('.')[2])<=16]
interior.sort(key=lambda x:int(x.split('.')[2]))
for v in interior:
    n=int(v.split('.')[2]); nxt=f'Ezek.5.{n+1}'
    sk=skel(osh[nxt]); w=sk.split()
    starts_mess = ' '.join(w[:4])=='כה אמר אדני יהוה' or ' '.join(w[:5])=='לכן כה אמר אדני יהוה'
    print(f'  mark after {v} = {marks[v]} -> next verse {nxt}: in_messenger_list={nxt in mess}  verse_initial_messenger={starts_mess}  first5={" ".join(w[:5])!r}')
print()

print('### (e) CUT-RULE limb (b) TEST: does the near-face verse END on a close-role formula?')
utt=set(inv['formulae']['utterance_of_the_lord_yhwh']['verses_mt'])|set(inv['formulae']['utterance_short_yhwh']['verses_mt'])
rec=set(inv['formulae']['recognition_family_64']['verses_mt'])|set(inv['formulae']['recognition_formula_adonai_variant']['verses_mt'])
for v in ['Ezek.4.3','Ezek.5.4','Ezek.4.17','Ezek.3.27','Ezek.2.7','Ezek.3.3','Ezek.3.9','Ezek.5.9','Ezek.5.10','Ezek.5.6','Ezek.5.7']:
    sk=skel(osh[v]); w=sk.split()
    print(f'  {v}: in_utterance81={v in utt}  in_recognition_family64={v in rec}  last5={" ".join(w[-5:])!r}')
print()
print('### (f) MARK DIRECTION CONVENTION (from pmarks itself)')
print(' ',pm['marks_note'])
print('  marks on my rows\' cited verses:',{v:marks.get(v) for v in ['Ezek.3.3','Ezek.3.21','Ezek.4.3','Ezek.4.12','Ezek.4.14','Ezek.4.15','Ezek.4.17','Ezek.5.4','Ezek.5.6','Ezek.5.9','Ezek.5.10','Ezek.5.17','Ezek.6.10']})
