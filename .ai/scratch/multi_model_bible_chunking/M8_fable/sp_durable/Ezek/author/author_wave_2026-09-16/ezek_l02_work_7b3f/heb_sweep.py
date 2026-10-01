import re, json
p = r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\Ezek_oshb.txt'
V = {}
for line in open(p, encoding='utf-8').read().split('\n'):
    if not line.strip(): continue
    k, t = line.split('\t', 1)
    V[k] = t
def skel(s):
    s = ''.join(c for c in s if '\u05d0' <= c <= '\u05ea' or c == ' ')
    return re.sub(r'\s+', ' ', s).strip()
S = {k: skel(t) for k, t in V.items()}
def kk(k):
    a = k.split('.'); return (int(a[1]), int(a[2]))
ORD = sorted(S, key=kk)
def sweep(label, pat):
    hits = [k for k in ORD if re.search(pat, S[k])]
    occ = sum(len(re.findall(pat, S[k])) for k in hits)
    print(f"{label}: verses={len(hits)} occurrences={occ}")
    print(f"   {hits}")
sweep("lo tachos eini (my eye will not spare) 'לא תחוס עיני'", r'לא תחוס עיני')
sweep("kevod YHWH 'כבוד יהוה'", r'כבוד יהוה')
sweep("nehar Kevar 'נהר כבר'", r'נהר כבר')
sweep("be-marot elohim 'במראות אלהים'", r'ב?מראות אלהים')
sweep("marot elohim (any) 'מראות אלהים'", r'מראות אלהים')
sweep("bet ha-meri 'בית המרי'", r'בית המרי')
sweep("bet meri 'בית מרי'", r'בית מרי')
sweep("wheel 'אופן' any", r'אופ')
sweep("galgal 'הגלגל'", r'גלגל')
