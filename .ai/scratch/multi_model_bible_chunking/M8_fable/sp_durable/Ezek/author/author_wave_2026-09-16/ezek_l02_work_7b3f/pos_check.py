import re, json
BB = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek'
V = {}
for line in open(BB + r'\Ezek_oshb.txt', encoding='utf-8').read().split('\n'):
    if not line.strip(): continue
    k, t = line.split('\t', 1)
    V[k] = t
def skel(s):
    s = ''.join(c for c in s if '\u05d0' <= c <= '\u05ea' or c == ' ')
    return re.sub(r'\s+', ' ', s).strip()
inv = json.load(open(BB + r'\ezek_device_inventory.v2.json', encoding='utf-8'))
mess = set(inv['formulae']['thus_says_the_lord_yhwh']['verses_mt'])
utt = set(inv['formulae']['utterance_of_the_lord_yhwh']['verses_mt'])
rec28 = set(inv['formulae']['recognition_formula']['verses_mt'])
rec2mp = set(inv['formulae']['recognition_formula_2mp']['verses_mt'])
we = set(inv['formulae']['word_event_formula']['verses_mt'])

def rep(k, pat, label):
    s = skel(V[k])
    m = list(re.finditer(pat, s))
    if not m:
        print(f"  {k}: {label} NOT PRESENT in skeleton")
        return
    for mm in m:
        tail = s[mm.end():].strip()
        print(f"  {k}: {label} at chars {mm.start()}..{mm.end()} of {len(s)}; VERSE-FINAL={tail==''}; tail={tail!r}")

print("== utterance 'נאם אדני יהוה' positions")
for k in ['Ezek.14.14','Ezek.14.16','Ezek.14.18','Ezek.14.20','Ezek.14.23','Ezek.14.11','Ezek.11.21','Ezek.12.25','Ezek.12.28','Ezek.13.16','Ezek.16.14','Ezek.16.19','Ezek.15.8']:
    rep(k, r'נאם אדני יהוה', 'utterance')
print()
print("== messenger 'כה אמר אדני יהוה'")
for k in ['Ezek.14.21','Ezek.14.6','Ezek.14.4','Ezek.13.3','Ezek.13.8','Ezek.13.13','Ezek.15.6','Ezek.16.3','Ezek.6.11','Ezek.7.2','Ezek.7.5','Ezek.11.16','Ezek.11.17','Ezek.12.28','Ezek.12.23']:
    rep(k, r'כה אמר אדני יהוה', 'messenger')
print()
print("== membership in v2 lists")
for k in ['Ezek.14.20','Ezek.14.21','Ezek.14.23','Ezek.11.16','Ezek.11.17','Ezek.13.9','Ezek.7.9','Ezek.7.4','Ezek.16.14','Ezek.16.19','Ezek.15.8']:
    print(f"  {k}: messenger122={k in mess} utterance81={k in utt} rec28={k in rec28} rec2mp={k in rec2mp} wordevent39={k in we}")
print()
print("== recognition positions at 7:4, 7:9, 13:9, 12:20, 13:23")
for k,pat,lab in [('Ezek.7.4', r'וידעתם כי אני יהוה','rec2mp'),('Ezek.7.9', r'וידעתם כי אני יהוה','rec2mp'),('Ezek.13.9', r'וידעתם כי אני אדני יהוה','recD3'),('Ezek.12.20', r'וידעתם כי אני יהוה','rec2mp'),('Ezek.13.23', r'וידעתן כי אני יהוה','rec2fp'),('Ezek.6.14', r'וידעו כי אני יהוה','rec28'),('Ezek.7.27', r'וידעו כי אני יהוה','rec28'),('Ezek.6.10', r'וידעו כי אני יהוה','rec28')]:
    rep(k, pat, lab)
