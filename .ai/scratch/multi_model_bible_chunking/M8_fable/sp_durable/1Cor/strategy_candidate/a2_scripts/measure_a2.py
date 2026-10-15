"""Orchestrator measurements for the a2 reconciliation: C2 DEF-04 vocabulary on RP (accent-stripped stems), WEB slices
for C1 DEF-09, WEB renderings of ouk oidate and to teleion. Read-only on pinned files."""
import re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
SP = "C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable/1Cor/"
def load(f):
    out = {}
    for l in open(SP + f, encoding="utf-8").read().splitlines():
        if "\t" in l:
            r, t = l.split("\t", 1); out[r.split(".", 1)[1].replace(".", ":")] = t
    return out
rp = load("1Cor_rp.txt"); web = load("1Cor_web_clean.txt")
def key(r): c, v = r.split(":"); return (int(c), int(v))
def strip(s): return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()
def inrng(r, a, b): return key(a) <= key(r) <= key(b)
for stem, a, b in (("ειδωλοθυτ", "8:1", "11:1"), ("συνειδησ", "8:1", "11:1"), ("εξουσι", "8:1", "11:1"),
                   ("ελευθερ", "8:1", "11:1"), ("απολλω", "1:10", "4:21"), ("κηφα", "1:10", "4:21")):
    allh = sorted((r for r, t in rp.items() if stem in strip(t)), key=key)
    print(stem, "in %s-%s:" % (a, b), [r for r in allh if inrng(r, a, b)], "| whole book:", allh)
for r, s in (("1:17", "For Christ sent me not to baptize"), ("4:14", "I don\u2019t write these things"),
             ("7:12", "I\u2014not the Lord\u2014"), ("14:37", "If any man thinks")):
    print(r, repr(s), "in verse:", s in web[r], "| book hits:", sorted((x for x, t in web.items() if s in t), key=key))
for pat in ("know", "perfect", "complete"):
    print(pat, sorted((r for r, t in web.items() if re.search(r"\b" + pat, t, re.I)), key=key)[:30])
for r in ("6:2", "13:10"): print(r, web[r][:160])
